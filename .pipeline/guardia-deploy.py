#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guardia-deploy.py — H-06: guardia post-deploy con señal fiable de Netlify.

Cierra el hueco "el pipeline publica y se va": tras un push a main, espera a que el
deploy de ESE commit esté `state:"ready"` en la API de Netlify (la señal fiable que
faltaba; ver PENDIENTES-HUMANO.md H-06), re-corre los checkers de producción y:

  - Todo limpio  → exit 0.
  - Hallazgos    → alerta LOUD en docs/ESTADO.md con el comando de revert exacto
                   sugerido. NO revierte solo (ROLLBACK_AUTOMATICO=false por diseño).
                   exit 1.
  - Sin señal    → timeout NO es deploy roto: NUNCA se revierte por timeout. exit 2.

El token vive en el Llavero de macOS (NUNCA en el repo):
  security add-generic-password -a plomero -s netlify-api-token -w '<token>'

Uso:
  python3 .pipeline/guardia-deploy.py                # vigila el HEAD actual de main
  python3 .pipeline/guardia-deploy.py --sha <sha>    # vigila un commit específico
  python3 .pipeline/guardia-deploy.py --timeout 600
  ROLLBACK_AUTOMATICO=true python3 .pipeline/guardia-deploy.py   # revert automático
      (solo con señal CONFIRMADA de deploy ready; jamás por timeout)
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = "66c63c79-dfd3-4874-998f-319c161d8166"   # plomerocul → plomeroculiacanpro.mx
API = "https://api.netlify.com/api/v1"
ESTADO = os.path.join(ROOT, "docs", "ESTADO.md")
CHECKERS = ["check-produccion.mjs", "check-e2e.mjs"]
POLL_S = 10


def token_llavero():
    """Lee el token del Llavero. Acepta la entrada canónica y la variante con espacio
    final en la cuenta (así quedó la creada a mano en Accesos del Llavero, 20-ago-2026)."""
    for svc, acct in (("netlify-api-token", "plomero"), ("plomero", "netlify-api-token "),
                      ("plomero", "netlify-api-token")):
        r = subprocess.run(["security", "find-generic-password", "-s", svc, "-a", acct, "-w"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    sys.exit("❌ guardia: no hay token de Netlify en el Llavero "
             "(security add-generic-password -a plomero -s netlify-api-token -w '<token>').")


def api_get(tok, path):
    req = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + tok})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def sh(*args):
    return subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True)


def esperar_deploy(tok, sha, timeout_s):
    """Espera el deploy del commit `sha`. Devuelve (estado, deploy_id):
    'ready' | 'error' | 'timeout'."""
    t0 = time.time()
    visto = None
    while time.time() - t0 < timeout_s:
        try:
            deploys = api_get(tok, "/sites/%s/deploys?per_page=15" % SITE_ID)
        except Exception as e:
            print("  … API no respondió (%s); reintento." % e)
            time.sleep(POLL_S)
            continue
        for d in deploys:
            if (d.get("commit_ref") or "").startswith(sha[:12]) or sha.startswith((d.get("commit_ref") or "~")[:12]):
                visto = d
                st = d.get("state")
                if st == "ready":
                    return "ready", d.get("id")
                if st in ("error", "failed"):
                    return "error", d.get("id")
                print("  … deploy %s en estado '%s'; espero." % (d.get("id", "?")[:8], st))
                break
        else:
            print("  … aún no aparece un deploy para %s; espero." % sha[:12])
        time.sleep(POLL_S)
    return "timeout", (visto or {}).get("id")


def correr_checkers():
    hallazgos = []
    for c in CHECKERS:
        p = os.path.join(ROOT, ".pipeline", c)
        if not os.path.exists(p):
            continue
        r = sh("node", p)
        try:
            # la salida es JSON {"hallazgos": [...]}; tolera ruido antes del JSON
            out = r.stdout[r.stdout.index("{"):]
            hallazgos += json.loads(out).get("hallazgos", [])
        except Exception:
            hallazgos.append({"id": "guardia-checker-roto", "severidad": "alta",
                              "descripcion": "%s no emitió JSON parseable (verificación ciega)" % c,
                              "salida": (r.stdout + r.stderr)[-400:]})
    return hallazgos


def alerta_estado(sha, hallazgos):
    fecha = time.strftime("%Y-%m-%d %H:%M")
    lineas = "\n".join("  - [%s] %s: %s" % (h.get("severidad", "?"), h.get("id", "?"),
                                            str(h.get("descripcion", ""))[:200]) for h in hallazgos)
    bloque = ("\n\n---\n## 🚨 ALERTA guardia-deploy %s — PRODUCCIÓN CON HALLAZGOS TRAS DEPLOY\n"
              "Commit publicado: `%s` (deploy Netlify ready, señal confirmada).\n"
              "Hallazgos de los checkers de producción:\n%s\n\n"
              "**Revert sugerido (NO ejecutado — decide un humano):**\n"
              "```bash\ngit revert -m 1 %s && git push origin main\n```\n"
              "Tras revertir, re-correr `python3 .pipeline/guardia-deploy.py` para confirmar.\n"
              % (fecha, sha, lineas, sha))
    with open(ESTADO, "a", encoding="utf-8") as f:
        f.write(bloque)


def main():
    args = sys.argv[1:]
    sha = None
    timeout_s = 300
    while args:
        a = args.pop(0)
        if a == "--sha" and args:
            sha = args.pop(0)
        elif a == "--timeout" and args:
            timeout_s = int(args.pop(0))
        else:
            sys.exit("uso: guardia-deploy.py [--sha <sha>] [--timeout <segundos>]")
    if not sha:
        # default: lo último PUSHEADO (origin/main), no el HEAD local — el agente diario
        # deja commits locales en ramas auto/* que nunca corresponden a un deploy.
        sh("git", "fetch", "origin")
        sha = sh("git", "rev-parse", "origin/main").stdout.strip()
    if not sha:
        sys.exit("❌ guardia: no pude resolver el sha a vigilar.")

    print("🛡  guardia-deploy: vigilando deploy de %s (timeout %ds)…" % (sha[:12], timeout_s))
    tok = token_llavero()
    estado, deploy_id = esperar_deploy(tok, sha, timeout_s)

    if estado == "timeout":
        print("⏱  Sin señal de deploy en %ds. Timeout NO es deploy roto: no se toca nada." % timeout_s)
        print("   Revisa a mano: https://app.netlify.com/sites/plomerocul/deploys")
        sys.exit(2)
    if estado == "error":
        print("❌ Netlify reporta el deploy %s en estado ERROR (el build falló; producción\n"
              "   sigue sirviendo el deploy anterior). Revisa el log en Netlify." % (deploy_id or "?"))
        sys.exit(2)

    print("✅ Deploy %s ready (señal confirmada). Corriendo checkers de producción…" % (deploy_id or "?")[:8])
    hallazgos = correr_checkers()
    if not hallazgos:
        print("✅ guardia-deploy: producción limpia tras el deploy de %s." % sha[:12])
        sys.exit(0)

    print("🚨 %d hallazgo(s) en producción tras el deploy:" % len(hallazgos))
    for h in hallazgos:
        print("   - [%s] %s" % (h.get("severidad", "?"), str(h.get("descripcion", ""))[:120]))
    alerta_estado(sha, hallazgos)
    print("📝 Alerta escrita en docs/ESTADO.md con el revert sugerido (NO ejecutado).")
    if os.environ.get("ROLLBACK_AUTOMATICO") == "true":
        print("↩️  ROLLBACK_AUTOMATICO=true y señal confirmada → ejecutando revert…")
        r1 = sh("git", "revert", "--no-edit", "-m", "1", sha)
        print((r1.stdout + r1.stderr).strip()[-300:])
        if r1.returncode == 0:
            r2 = sh("git", "push", "origin", "main")
            print((r2.stdout + r2.stderr).strip()[-300:])
        else:
            print("❌ revert falló (¿conflicto?); queda para humano.")
    sys.exit(1)


if __name__ == "__main__":
    main()
