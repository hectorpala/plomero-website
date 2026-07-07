#!/usr/bin/env python3
"""Gate determinista (CI + pre-commit).

Corre los checkers de DISCO (no requieren red ni puppeteer) y FALLA (exit 1) si
hay algún hallazgo de severidad 'alta'. Las 'media'/'baja' se reportan pero no
bloquean. Los checkers de producción en vivo (check-produccion.mjs / check-*.mjs)
NO se incluyen aquí: validan producción post-deploy, su lugar es el pipeline
nocturno, no el gate pre-merge.

Uso:  python3 .pipeline/ci-gate.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# check-rutas-pipeline: caza la clase infra-006/007 (ruta rota tras mover archivos)
# ANTES del push; antes solo la detectaba el pipeline nocturno, un día después.
CHECKERS = ["check-plantilla.py", "check-indexabilidad.py", "check-estructura-sitio.py",
            "check-rutas-pipeline.py"]

def _parse_json_lenient(s):
    """Tolera texto extra antes/después del JSON (p.ej. un warning a stdout) extrayendo
    el objeto {…} más externo. Sigue fallando cerrado (lanza) si no hay JSON parseable."""
    try:
        return json.loads(s)
    except Exception:
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j > i:
            return json.loads(s[i:j + 1])
        raise


total_alta = 0
for c in CHECKERS:
    path = os.path.join(ROOT, ".pipeline", c)
    res = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=ROOT)
    try:
        data = _parse_json_lenient(res.stdout)
    except Exception as e:
        print(f"❌ {c}: la salida no es JSON válido ({e})")
        sys.stderr.write(res.stdout[:800] + "\n" + res.stderr[:800] + "\n")
        sys.exit(2)
    # Un checker que imprime JSON válido y LUEGO crashea no es un checker sano:
    # su barrido pudo quedar a medias (falso "0 hallazgos"). Fallar cerrado.
    if res.returncode != 0:
        print(f"❌ {c}: terminó con exit {res.returncode} (barrido posiblemente incompleto)")
        sys.stderr.write(res.stderr[:800] + "\n")
        sys.exit(2)
    hallazgos = data.get("hallazgos", [])
    alta = [h for h in hallazgos if h.get("severidad") == "alta"]
    otras = len(hallazgos) - len(alta)
    print(f"▶ {c}: {len(alta)} ALTA · {otras} media/baja")
    for h in alta:
        print(f"   • {h.get('archivo','?')}: {h.get('descripcion','')[:120]}")
    total_alta += len(alta)

print("")
if total_alta:
    print(f"❌ Gate FALLA: {total_alta} hallazgo(s) de severidad ALTA. Corrige antes de mergear/commit.")
    sys.exit(1)
print("✅ Gate OK: sin hallazgos de severidad ALTA.")
sys.exit(0)
