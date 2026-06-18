#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selector-revisores.py — FAN-OUT SELECTIVO: decide QUÉ revisores correr según lo que cambió.

Combina con el routing de modelos (.claude/agents/MODELO-ROUTING.md):
  • Los DETERMINISTAS (haiku) corren SIEMPRE site-wide: son baratos y dan el piso de seguridad +
    verificación ciega + el candado de secretos. No se seleccionan: siempre van.
  • Los de JUICIO (sonnet/opus, los caros) se SELECCIONAN por tipo de cambio: no tiene sentido
    correr revisor-contenido (opus) si solo tocaste CSS, ni revisor-movil si solo cambió texto.

Si el cambio NO toca archivos servidos del sitio (solo .pipeline/scripts/tests/docs), NO corre
ningún revisor de juicio: solo el piso. (Ahorro grande en corridas de infra.)

Uso:
  python3 .pipeline/selector-revisores.py --base origin/main      # diff contra una ref
  git diff --name-only A...B | python3 .pipeline/selector-revisores.py -   # lista por stdin
  python3 .pipeline/selector-revisores.py f1.html f2.css ...             # lista explícita

Salida: razón legible + dos líneas máquina:  PISO: ...   y   JUICIO: ...
Exit 0 siempre (es un asesor, no un candado).
"""
import os
import re
import subprocess
import sys

# Piso que SIEMPRE corre (deterministas haiku + el gate de secretos). Cubre todo el sitio.
PISO = [
    "infra-salud", "plantilla", "indexabilidad", "nap", "conversion",
    "enlazado-interno", "e2e-funcional", "perf-real", "produccion", "tracking",
    "secretos",
]

# Revisores de JUICIO (caros) y qué tipo de cambio los hace relevantes.
REGLAS = [
    # (test sobre la ruta, [revisores de juicio a sumar])
    (lambda f, nuevo: f.endswith(".css") or "styles" in f,            ["movil", "perf"]),
    (lambda f, nuevo: re.search(r"(^|/)(servicios|blog)/.+\.html$", f) or f.endswith("index.html"),
                                                                       ["contenido", "seo", "a11y", "links"]),
    (lambda f, nuevo: nuevo and f.endswith("index.html"),             ["critico-completitud"]),
    (lambda f, nuevo: "sitemap" in f or f.endswith("_redirects"),     ["links"]),
]

# Archivos servidos del sitio (si NO se toca ninguno, no corre juicio).
def es_servido(f):
    return (f.endswith((".html", ".css", ".js", ".xml", ".webp", ".woff2"))
            or f.endswith("_redirects")) and not f.startswith((".pipeline/", "scripts/", "tests/"))


def cambios_desde_args(argv):
    if "--base" in argv:
        base = argv[argv.index("--base") + 1]
        r = subprocess.run(["git", "diff", "--name-status", "%s...HEAD" % base],
                           capture_output=True, text=True, errors="replace")
        out = []
        for ln in r.stdout.splitlines():
            parts = ln.split("\t")
            if len(parts) >= 2:
                out.append((parts[-1], parts[0].startswith("A")))  # (ruta, es_nuevo)
        return out
    if argv and argv[0] == "-":
        return [(ln.strip(), False) for ln in sys.stdin.read().splitlines() if ln.strip()]
    return [(a, False) for a in argv if not a.startswith("--")]


def main():
    cambios = cambios_desde_args(sys.argv[1:])
    servidos = [(f, n) for f, n in cambios if es_servido(f)]
    juicio = set()
    for f, nuevo in servidos:
        for test, revs in REGLAS:
            if test(f, nuevo):
                juicio.update(revs)

    print("📂 cambios: %d archivos (%d servidos del sitio)" % (len(cambios), len(servidos)))
    if not servidos:
        print("   → no se tocó nada servido (solo infra/scripts/docs): solo corre el PISO.")
    else:
        ej = ", ".join(f for f, _ in servidos[:6]) + (" …" if len(servidos) > 6 else "")
        print("   servidos: " + ej)
    print("")
    print("PISO: " + ",".join(PISO))
    print("JUICIO: " + (",".join(sorted(juicio)) if juicio else "(ninguno)"))
    print("")
    print("→ correr %d revisores (%d piso + %d juicio); se OMITEN los de juicio no relevantes: %s"
          % (len(PISO) + len(juicio), len(PISO), len(juicio),
             ",".join(sorted({"movil", "perf", "contenido", "seo", "a11y", "links",
                              "critico-completitud", "gsc"} - juicio)) or "ninguno"))


if __name__ == "__main__":
    main()
