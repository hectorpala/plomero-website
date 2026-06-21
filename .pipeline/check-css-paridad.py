#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-css-paridad.py — Paridad CSS COMPLETA (no solo firmas).

infra:utilidad-no-sensor  (utilidad standalone: imprime texto humano, no el contrato
JSON {"hallazgos":[...]}; la paridad CSS la enforce el pipeline via check-plantilla.py.
Sin este marcador el dead-man's switch check-infra.mjs dispara una ALTA falsa.)

El sitio sirve DOS hojas de estilo distintas:
  - styles.7f293647.css  -> la sirven la home (index.html) + las paginas de colonia
  - styles.min.css       -> la sirve el resto del sitio (servicios, blog, etc.)
y styles.css es la FUENTE (no se sirve). REGLAS.md exige que las tres tengan las
MISMAS reglas (paridad). Si una se queda atras, esas paginas renderizan distinto.

El checker viejo en check-plantilla.py solo comparaba 3 firmas hardcodeadas, asi
que la deriva real (.hero .hero-image, @keyframes slideInUp, etc.) paso inadvertida.

Este script descompone cada styles*.css en ATOMOS (selector individual + bloque de
declaraciones normalizado, con su contexto @media), e informa todo atomo presente
en alguna hoja pero ausente en otra. Ignora diferencias puras de agrupacion de
selectores y de minificacion (espacios) -> sin falsos positivos.

Salida: lista de derivas. Codigo 1 si hay paridad rota, 0 si esta limpia.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def _norm_sel(s):
    """Colapsa espacio redundante pero CONSERVA el combinador descendiente
    (' '), que es semantico: '.hero .hero-image' != '.hero.hero-image'."""
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*([>+~,])\s*", r"\1", s)
    return s


def _norm_decls(body):
    """Normaliza el bloque de declaraciones: colapsa espacio, quita el de
    alrededor de ; : , pero conserva el interno de los valores
    (p.ej. 'margin:0 0 0 8px'). Ordena para ignorar el orden de escritura."""
    b = re.sub(r"\s+", " ", body).strip()
    b = re.sub(r"\s*([;:,])\s*", r"\1", b)
    parts = [d.strip() for d in b.split(";") if d.strip()]
    return ";".join(sorted(parts))


def _split_rules(css):
    """Parte CSS en (prelude, cuerpo) de primer nivel. 'cuerpo' es lo de adentro
    de las llaves, sin las llaves. Maneja anidamiento por profundidad."""
    rules = []
    depth = 0
    prelude = []
    buf = []
    for ch in css:
        if ch == "{":
            if depth == 0:
                prelude_s = "".join(prelude)
                prelude = []
                depth = 1
            else:
                depth += 1
                buf.append(ch)
        elif ch == "}":
            depth -= 1
            if depth == 0:
                rules.append((prelude_s.strip(), "".join(buf)))
                buf = []
            else:
                buf.append(ch)
        else:
            (prelude if depth == 0 else buf).append(ch)
    return rules


def _style_atoms(prelude, body, ctx=""):
    """Un atomo por cada selector individual del grupo: (ctx, selector, decls)."""
    decls = _norm_decls(body)
    out = []
    for sel in _norm_sel(prelude).split(","):
        if sel:
            out.append("%s%s{%s}" % (ctx, sel, decls))
    return out


def atoms(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # fuera comentarios
    out = set()
    for prelude, body in _split_rules(css):
        p = _norm_sel(prelude)
        head = p.split("(")[0].lower()
        if head.startswith("@media") or head.startswith("@supports"):
            ctx = re.sub(r"\s+", "", p) + "||"
            for inner_prelude, inner_body in _split_rules(body):
                out.update(_style_atoms(inner_prelude, inner_body, ctx))
        elif p.startswith("@"):  # @keyframes, @font-face, etc -> bloque entero
            out.add(re.sub(r"\s+", "", p) + "{" + re.sub(r"\s+", "", body) + "}")
        else:
            out.update(_style_atoms(prelude, body))
    return out


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "styles*.css")))
    if len(files) < 2:
        print("Solo hay un styles*.css; nada que comparar.")
        return 0
    A = {f: atoms(read(f)) for f in files}
    union = set().union(*A.values())
    roto = False
    print("== Paridad CSS (%d archivos) ==" % len(files))
    for f in files:
        print("  %-24s %4d atomos" % (os.path.basename(f), len(A[f])))
    print()
    for atom in sorted(union):
        tienen = [f for f in files if atom in A[f]]
        if len(tienen) == len(files):
            continue
        roto = True
        faltan = [os.path.basename(f) for f in files if atom not in A[f]]
        print("DERIVA: %s" % atom)
        print("   tienen : %s" % ", ".join(os.path.basename(f) for f in tienen))
        print("   FALTAN : %s" % ", ".join(faltan))
        print()
    if not roto:
        print("OK: las hojas servidas estan en paridad total.")
    return 1 if roto else 0


if __name__ == "__main__":
    sys.exit(main())
