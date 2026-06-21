#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""limpiar-huerfanos.py — borrado SEGURO de archivos huérfanos (modo conservador).

El Auto Agente NO debe borrar a ciegas. Este script solo propone/borra un archivo si cumple
TODAS estas condiciones (defensa en profundidad; si falla una, NO lo toca):
  1) Calza un PATRÓN DE ARTEFACTO conocido (*.min.html, *.bak*, *.tmp, *.old, *~) — modo
     conservador: nunca un .html/.css/.js de página o asset en uso.
  2) CERO referencias entrantes: ningún .html/.xml/_redirects rastreado lo nombra.
  3) NO está en el sitemap.
  4) Está RASTREADO por git (el borrado es recuperable con `git restore`).

Uso:
  python3 .pipeline/limpiar-huerfanos.py list           # DRY-RUN: JSON de candidatos seguros
  python3 .pipeline/limpiar-huerfanos.py run --apply     # `git rm` los seguros (recuperable)

Exit 0 siempre (no bloquea la corrida). Borra SOLO lo provadamente huérfano; lo dudoso lo deja.
"""
import fnmatch
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (1) Patrones de ARTEFACTO. Conservador: extensiones que NUNCA son una página/asset servido.
ARTIFACT_GLOBS = ["*.min.html", "*.bak", "*.bak-*", "*.tmp", "*.old", "*~"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)


def tracked_files():
    out = git("ls-files").stdout
    return [l for l in out.splitlines() if l]


def es_artefacto(rel):
    base = os.path.basename(rel)
    return any(fnmatch.fnmatch(base, g) for g in ARTIFACT_GLOBS)


def tiene_referencias(rel):
    """¿Algún .html/.xml/_redirects rastreado nombra este archivo (por su basename)?"""
    base = os.path.basename(rel)
    r = git("grep", "-l", "--fixed-strings", base, "--",
            "*.html", "*.xml", "_redirects")
    # git grep exit 1 = sin coincidencias. Excluir el propio archivo de los hits.
    hits = [l for l in r.stdout.splitlines() if l and l != rel]
    return len(hits) > 0


def en_sitemap(rel):
    base = os.path.basename(rel)
    for sm in ("sitemaps/main_sitemap.xml", "sitemap.xml"):
        p = os.path.join(ROOT, sm)
        try:
            if base in open(p, encoding="utf-8").read():
                return True
        except Exception:
            continue
    return False


def evaluar():
    """Devuelve (seguros, rechazados[(rel, motivo)])."""
    seguros, rechazados = [], []
    for rel in tracked_files():
        if not es_artefacto(rel):
            continue                                   # (1) no es patrón de artefacto
        if tiene_referencias(rel):
            rechazados.append((rel, "tiene referencias entrantes")); continue   # (2)
        if en_sitemap(rel):
            rechazados.append((rel, "está en el sitemap")); continue            # (3)
        # (4) rastreado por git: por construcción viene de `git ls-files`, lo es.
        seguros.append(rel)
    return seguros, rechazados


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    apply = "--apply" in sys.argv
    seguros, rechazados = evaluar()

    if cmd == "list":
        print(json.dumps({"seguros_para_borrar": seguros,
                          "rechazados": [{"archivo": a, "motivo": m} for a, m in rechazados]},
                         ensure_ascii=False, indent=2))
        return

    if cmd == "run":
        if rechazados:
            print("Candidatos de artefacto PROTEGIDOS (no se tocan):")
            for a, m in rechazados:
                print("  🛡  %s — %s" % (a, m))
        if not seguros:
            print("✅ Nada que limpiar: 0 huérfanos seguros."); return
        for rel in seguros:
            if apply:
                r = git("rm", rel)
                ok = r.returncode == 0
                print("  %s %s (huérfano, recuperable con git restore)" % ("🗑 " if ok else "⚠️ ", rel))
                if not ok:
                    print("     " + r.stderr.strip())
            else:
                print("  ○ %s (dry-run; corre con --apply)" % rel)
        return

    print("comando desconocido: %s" % cmd); sys.exit(2)


if __name__ == "__main__":
    main()
