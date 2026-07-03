#!/usr/bin/env python3
"""Checker DETERMINISTA: rutas hardcodeadas rotas en .pipeline/*.py y scripts/*.py.

Caza la clase de regresión "rutas post-reorganización" (REGLAS.md, familia
infra-006/infra-007/0d3fb737): una ruta literal que apuntaba a la raíz antes de
que el repo se reordenara en scripts/ + docs/ + data/, y que nadie actualizó al
mover el archivo real. DOS formas de la MISMA clase:

  A) os.path.join(ROOT, "BACKLOG.jsonl")                (forma infra-007)
  B) open("BACKLOG.jsonl") / _jsonl("BACKLOG.jsonl")    (forma infra-006: literal
     relativo pasado directo a open()/helper, SIN ROOT — el que dejó el backlog
     reportando "0 tareas" durante días)

Solo mira LITERALES (sin *, sin f-strings con variables) que terminan en una
extensión de DATOS/CONFIG conocida — evita falsos positivos con globs
(`servicios/*/index.html`) y con plantillas .html abiertas contra un base ya
resuelto. Emite el contrato común {"hallazgos":[...]} para que check-infra.mjs
lo recoja solo.
"""
import ast
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["scripts", ".pipeline"]
SELF = os.path.basename(__file__)

# Extensiones de datos/config que se resuelven contra la raíz del repo. Se
# excluyen .html/.webp/.css/.js a propósito (suelen abrirse contra un base de
# página ya calculado -> alto ruido).
EXT_DATOS = {".jsonl", ".json", ".md", ".txt", ".csv", ".sh", ".tsv", ".yml", ".yaml"}
# Funciones cuyo PRIMER argumento es una ruta de archivo relativa a la raíz.
OPEN_FUNCS = {"open", "_jsonl"}


def _es_literal_str(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def _modo_de_open(node):
    """Modo de una llamada open(path, mode=...) si es literal; 'r' por defecto."""
    if len(node.args) >= 2 and _es_literal_str(node.args[1]):
        return node.args[1].value
    for kw in node.keywords:
        if kw.arg == "mode" and _es_literal_str(kw.value):
            return kw.value
    return "r"


def _literal_join_paths(src):
    """Forma A: os.path.join(ROOT, "a", "b", ...) con literales tras ROOT."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        is_join = (isinstance(f, ast.Attribute) and f.attr == "join") or \
                  (isinstance(f, ast.Name) and f.id == "join")
        if not is_join or not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Name) and first.id == "ROOT"):
            continue
        parts, ok = [], True
        for a in node.args[1:]:
            if _es_literal_str(a):
                parts.append(a.value)
            else:
                ok = False
                break
        if ok and parts:
            found.append((os.path.join(*parts), node.lineno))
    return found


def _literal_open_paths(src):
    """Forma B: open("lit.ext") / _jsonl("lit.ext") — literal relativo directo,
    solo en modo LECTURA (crear/escribir un archivo que aún no existe es válido)."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        f = node.func
        name = f.id if isinstance(f, ast.Name) else (
            f.attr if isinstance(f, ast.Attribute) else None)
        if name not in OPEN_FUNCS:
            continue
        first = node.args[0]
        if not _es_literal_str(first):
            continue
        if name == "open" and any(c in _modo_de_open(node) for c in ("w", "a", "x")):
            continue  # escribe/crea -> que no exista es legítimo
        found.append((first.value, node.lineno))
    return found


def _ruta_rota(rel, ext_whitelist):
    if os.path.isabs(rel) or "*" in rel:
        return False
    ext = os.path.splitext(rel)[1].lower()
    if not ext:
        return False  # sin extensión -> probablemente un directorio
    if ext_whitelist is not None and ext not in ext_whitelist:
        return False
    return not os.path.exists(os.path.join(ROOT, rel))


def _hallazgo(seq, full, lineno, rel, forma):
    return {
        "id": f"rutas-{seq:03d}",
        "archivo": os.path.relpath(full, ROOT),
        "linea": lineno,
        "severidad": "alta",
        "categoria": "infra",
        "descripcion": (
            f"RUTA ROTA ({forma}): apunta a '{rel}', que no existe en el repo "
            "(posible regresión de rutas post-reorganización — familia infra-006/007)."
        ),
        "fix_sugerido": (
            f"Corregir la constante/llamada para que apunte a la ubicación real de "
            f"'{os.path.basename(rel)}'."
        ),
    }


def main():
    hallazgos = []
    analizadas = 0
    seq = 0
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if not name.endswith(".py") or name == SELF:
                continue
            full = os.path.join(base, name)
            try:
                src = open(full, encoding="utf-8").read()
            except OSError:
                continue
            analizadas += 1
            for rel, lineno in _literal_join_paths(src):
                if _ruta_rota(rel, None):        # forma A: cualquier extensión (como hoy)
                    seq += 1
                    hallazgos.append(_hallazgo(seq, full, lineno, rel, "join(ROOT, …)"))
            for rel, lineno in _literal_open_paths(src):
                if _ruta_rota(rel, EXT_DATOS):   # forma B: solo extensiones de datos
                    seq += 1
                    hallazgos.append(_hallazgo(seq, full, lineno, rel,
                                               "open()/_jsonl() literal relativo"))
    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
