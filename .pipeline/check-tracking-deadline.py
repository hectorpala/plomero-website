#!/usr/bin/env python3
"""Supervisor FAIL-CLOSED de check-tracking.mjs: siempre emite el JSON de hallazgos.

POR QUÉ EXISTE
--------------
`check-tracking.mjs` promete emitir el contrato común {"hallazgos":[...],"analizadas":N}
incluso en sus rutas de error, pero esa promesa solo se cumple mientras el proceso JS
conserve el control. Si `page.close()`, `browser.close()` o el propio Chrome se cuelgan,
el checker muere (o se queda vivo para siempre) SIN escribir nada por stdout, y el
revisor-tracking reporta "verificación ciega" (ALTA) que bloquea la publicación del día.
Pasó el 2026-08-26 y el 2026-09-01 (ver data/HISTORIAL.jsonl,
id `tracking-verificacion-ciega-sin-stdout`) y contribuyó a que el sitio pasara 11 días
sin publicar.

La causa MÁS COMÚN del fallo de lanzamiento (Chrome no encontrado) ya se corrigió aparte:
`crecer-diario.sh` exporta `PUPPETEER_EXECUTABLE_PATH`. Lo que faltaba era el supervisor
para el caso de CUELGUE, que ningún `main().catch()` dentro del propio proceso puede cubrir.

QUÉ HACE
--------
1. Lanza `node .pipeline/check-tracking.mjs` en su PROPIO grupo de procesos
   (`start_new_session=True`), heredando el entorno tal cual (PUPPETEER_EXECUTABLE_PATH,
   TRACK_BASE, TRACK_URLS…). Node se localiza con `.pipeline/encontrar-node.py` porque
   `node` no está en el PATH de todos los shells (REGLAS.md, incidente 2026-07-10).
2. Espera hasta un DEADLINE de reloj de pared (`TRACK_DEADLINE_SECONDS`, default 300 s;
   el checker tarda ~47 s en condiciones normales, así que hay margen de sobra).
3. Si vence el plazo mata el GRUPO COMPLETO con `os.killpg` (SIGTERM y, si no muere en
   `TRACK_KILL_GRACE_SECONDS`, SIGKILL). El grupo importa: Chrome deja procesos hijos
   huérfanos que sobrevivirían a un kill del PID solo y seguirían comiendo CPU/RAM.
4. SIEMPRE escribe por stdout un objeto de hallazgos válido:
      - checker sano  -> se reemite su JSON tal cual (mismo contrato, mismos textos).
      - deadline vencido / stdout no-JSON / contrato incompleto / exit != 0 / sin salida
        -> UN hallazgo de severidad ALTA describiendo la verificación ciega.

NOTA para check-infra.mjs: este script SÍ emite el contrato {"hallazgos":[...],"analizadas":N},
o sea que es un SENSOR de pleno derecho y por eso NO lleva el marcador
`infra:utilidad-no-sensor` (ese marcador es solo para utilidades que no emiten hallazgos,
como check-contrato-checkers.mjs). Sin dependencias externas: solo stdlib de Python 3.
"""
import importlib.util
import json
import os
import signal
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE = os.path.join(ROOT, ".pipeline")
CHECKER = os.path.join(PIPELINE, "check-tracking.mjs")
CHECKER_REL = ".pipeline/check-tracking.mjs"

# ~47 s es lo normal; 300 s deja margen para una producción lenta sin tapar un cuelgue.
DEADLINE_S = max(1, int(os.environ.get("TRACK_DEADLINE_SECONDS", "300")))
# Gracia entre SIGTERM y SIGKILL al grupo de procesos.
KILL_GRACE_S = max(1, int(os.environ.get("TRACK_KILL_GRACE_SECONDS", "5")))

MAX_DETALLE = 1200


def _encontrar_node():
    """Reutiliza .pipeline/encontrar-node.py (nombre con guion: no se puede importar normal)."""
    ruta = os.path.join(PIPELINE, "encontrar-node.py")
    try:
        spec = importlib.util.spec_from_file_location("encontrar_node", ruta)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.encontrar(os.environ.get("PATH")) or ""
    except Exception:
        import shutil
        return shutil.which("node") or ""


def fallo(descripcion, detalle=""):
    """Hallazgo ALTA de verificación ciega, con el mismo contrato que los demás checkers."""
    detalle = (detalle or "").strip()
    texto = descripcion + ((": " + detalle[-MAX_DETALLE:]) if detalle else "")
    return {
        "hallazgos": [{
            "id": "trk-supervisor-001",
            "archivo": CHECKER_REL,
            "linea": 0,
            "severidad": "alta",
            "categoria": "tracking",
            "descripcion": texto,
            "fix_sugerido": (
                "El tracking NO se verificó: trata la corrida como NO publicable. "
                "1) Confirma que Chrome existe y que PUPPETEER_EXECUTABLE_PATH apunta a él "
                "(/Applications/Google Chrome.app/Contents/MacOS/Google Chrome), como ya hace "
                "crecer-diario.sh. 2) Corre a mano `node .pipeline/check-tracking.mjs` y mira su "
                "stderr. 3) Si tarda de más por producción lenta, sube TRACK_DEADLINE_SECONDS "
                "(default 300s). 4) Verifica que no queden procesos Chrome zombis "
                "(pgrep -f 'Google Chrome')."
            ),
        }],
        "analizadas": 0,
    }


def _comunicar(proc, timeout):
    """communicate() que nunca propaga TimeoutExpired; devuelve (stdout, stderr, vencio)."""
    try:
        out, err = proc.communicate(timeout=timeout)
        return out or "", err or "", False
    except subprocess.TimeoutExpired:
        return "", "", True


def _matar_grupo(proc):
    """SIGTERM al grupo entero y, si no muere, SIGKILL. Chrome deja hijos huérfanos."""
    for sig, espera in ((signal.SIGTERM, KILL_GRACE_S), (signal.SIGKILL, KILL_GRACE_S)):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        out, err, vencio = _comunicar(proc, espera)
        if not vencio:
            return out, err
    return "", ""


def _valida_contrato(data):
    if not isinstance(data, dict):
        return "la salida no es un objeto JSON"
    if not isinstance(data.get("hallazgos"), list):
        return 'falta el array "hallazgos"'
    if not isinstance(data.get("analizadas"), int) or isinstance(data.get("analizadas"), bool):
        return 'falta el entero "analizadas"'
    return ""


def main():
    node = _encontrar_node()
    if not node:
        return fallo(
            "verificación ciega: no se encontró un ejecutable de node para lanzar el checker de tracking")
    if not os.path.isfile(CHECKER):
        return fallo(f"verificación ciega: no existe {CHECKER_REL}")

    try:
        proc = subprocess.Popen(
            [node, CHECKER], cwd=ROOT, text=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            start_new_session=True, env=os.environ.copy())
    except Exception as exc:
        return fallo(f"verificación ciega: no se pudo lanzar el checker de tracking ({exc})")

    stdout, stderr, vencio = _comunicar(proc, DEADLINE_S)
    if vencio:
        _stdout_tarde, stderr_tarde = _matar_grupo(proc)
        return fallo(
            f"verificación ciega: check-tracking.mjs excedió el deadline de {DEADLINE_S}s "
            f"(Chrome/puppeteer colgado) y se mató su grupo de procesos completo; "
            f"el tracking NO se verificó",
            stderr_tarde)

    if proc.returncode != 0:
        return fallo(
            f"verificación ciega: check-tracking.mjs terminó con código {proc.returncode}",
            stderr or stdout)

    try:
        data = json.loads(stdout)
    except Exception as exc:
        return fallo(
            f"verificación ciega: check-tracking.mjs no imprimió JSON parseable por stdout ({exc})",
            stderr or stdout)

    problema = _valida_contrato(data)
    if problema:
        return fallo(
            f"verificación ciega: check-tracking.mjs rompió el contrato de salida ({problema})",
            stderr or stdout)

    return data


if __name__ == "__main__":
    sys.stdout.write(json.dumps(main(), ensure_ascii=False, indent=2) + "\n")
