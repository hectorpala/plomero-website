#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador determinista de landings con PARIDAD ESTRUCTURAL por construcción.

Copia un esqueleto (una página que YA pasa validate-landing.sh) byte a byte y
aplica SOLO sustituciones de contenido explícitas, afirmando que cada una ocurre
el número exacto de veces esperado. Si una sustitución no calza, ABORTA (no
escribe nada): así es imposible introducir "drift" de plantilla, y el contenido
único por página lo aporta quien escribe el spec (anti-doorway).

Uso:
    python3 .pipeline/gen-landing.py spec.json
    cat spec.json | python3 .pipeline/gen-landing.py -

Formato del spec (JSON):
{
  "skeleton": "servicios/plomero-cerca-de-mi/index.html",   # ruta relativa a la raíz
  "output":   "servicios/plomero-zona-X-culiacan/index.html",
  "replacements": [
     {"old": "<title>...</title>", "new": "<title>...</title>", "n": 1},
     {"old": "plomero-cerca-de-mi", "new": "plomero-zona-x-culiacan", "n": 8}
     ...
  ]
}

- "n" es opcional (default 1). El número de ocurrencias DEBE ser exacto.
- El orden importa: las sustituciones se aplican en secuencia sobre el texto.
- Salida: escribe el archivo y reporta líneas; exit 0. En error: exit 1, no escribe.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fail(msg):
    print("❌ gen-landing ABORT: " + msg)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        fail("falta el spec.json (uso: gen-landing.py spec.json | -)")
    raw = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    try:
        spec = json.loads(raw)
    except Exception as e:
        fail("spec no es JSON válido: %s" % e)

    for k in ("skeleton", "output", "replacements"):
        if k not in spec:
            fail("falta la clave '%s' en el spec" % k)

    sk_path = os.path.join(ROOT, spec["skeleton"])
    if not os.path.isfile(sk_path):
        fail("esqueleto no existe: %s" % spec["skeleton"])
    s = open(sk_path, encoding="utf-8").read()

    for i, r in enumerate(spec["replacements"]):
        old, new, n = r.get("old"), r.get("new"), int(r.get("n", 1))
        if old is None or new is None:
            fail("replacement #%d sin 'old'/'new'" % i)
        c = s.count(old)
        if c != n:
            fail("replacement #%d: se esperaban %d ocurrencias, hay %d.\n     OLD=%r" % (i, n, c, old[:120]))
        s = s.replace(old, new, n)

    # Guardas anti-fuga genéricas del sitio. En el sitio de PLOMERÍA la fuga
    # contaminante es la del sitio ORIGEN de la plantilla (electricista): si aparece
    # "electricista", el GTM del electricista o un email de electricista, la plantilla
    # quedó contaminada por copy-paste. (Inverso exacto del guard del electricista.)
    low = s.lower()
    for bad in ("electricista", "gtm-5z2qrz5q", "contacto@electricista"):
        if bad in low:
            fail("fuga detectada en el resultado: %r (plantilla origen contaminada)" % bad)

    out_path = os.path.join(ROOT, spec["output"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(s)
    print("✅ %s  (%d líneas, %d sustituciones)" % (spec["output"], s.count("\n") + 1, len(spec["replacements"])))
    sys.exit(0)


if __name__ == "__main__":
    main()
