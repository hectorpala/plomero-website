#!/usr/bin/env python3
"""Checker DETERMINISTA: rutas hardcodeadas rotas en .pipeline/*.py y scripts/*.py.

Caza la clase de regresión "rutas post-reorganización" (REGLAS.md, familia
infra-006/0d3fb737/e6f6f89d): una constante de ruta tipo
`os.path.join(ROOT, "BACKLOG.jsonl")` o `os.path.join(ROOT, "validate-landing.sh")`
que apuntaba a la raíz antes de que el repo se reordenara en scripts/ + docs/ +
data/, y que nadie actualizó al mover el archivo real.

Solo mira LITERALES (sin *, sin f-strings con variables) que terminan en una
extensión de archivo — evita falsos positivos con globs (`servicios/*/index.html`).
Emite el contrato común {"hallazgos":[...]} para que check-infra.mjs lo recoja solo.
"""
import ast
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["scripts", ".pipeline"]
SELF = os.path.basename(__file__)


def _literal_join_paths(src):
    """Devuelve rutas relativas de llamadas os.path.join(ROOT, "a", "b", ...) con
    todos los argumentos posteriores a ROOT como literales de string."""
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
        parts = []
        ok = True
        for a in node.args[1:]:
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                parts.append(a.value)
            else:
                ok = False
                break
        if ok and parts:
            found.append((os.path.join(*parts), node.lineno))
    return found


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
                if "*" in rel:
                    continue
                if not os.path.splitext(rel)[1]:
                    continue  # sin extensión -> probablemente un directorio, no un archivo
                if os.path.exists(os.path.join(ROOT, rel)):
                    continue
                seq += 1
                hallazgos.append({
                    "id": f"rutas-{seq:03d}",
                    "archivo": os.path.relpath(full, ROOT),
                    "linea": lineno,
                    "severidad": "alta",
                    "categoria": "infra",
                    "descripcion": (
                        f"RUTA ROTA: os.path.join(ROOT, ...) apunta a '{rel}', que no existe "
                        "en el repo (posible regresión de rutas post-reorganización — familia infra-006)."
                    ),
                    "fix_sugerido": f"Corregir la constante para que apunte a la ubicación real de '{os.path.basename(rel)}'.",
                })
    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
