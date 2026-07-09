#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensor de IMPACTO: "¿qué se rompe si toco este script?".

POR QUÉ EXISTE. El acoplamiento de este pipeline NO se ve por `import`: los scripts se
invocan entre sí por subprocess/shell (`ci-gate.py` corre `check-plantilla.py`, el driver
`.sh` corre `crecer.py`…). Un analizador AST clásico no ve esas aristas — se comprobó con
Graphify (2026-07-08): halló 12 aristas archivo→archivo, y a `graphify affected ci-gate.py`
respondió "No affected nodes found", cuando en realidad rompe gate-pagina.py y crecer.py.

CÓMO. Misma técnica que check-rutas-pipeline.py: para .py se leen los LITERALES DE STRING
del AST (así un comentario no inventa una dependencia); para .sh/.mjs/.js se lee el texto
sin comentarios. Si un archivo menciona el basename de otro, hay arista invocador→invocado.

SIN ARGUMENTOS: analiza los archivos modificados en el working tree (staged + unstaged) y
emite un hallazgo por cada uno que tenga dependientes. Con argumentos: usa esa lista.
Emite el JSON común {"hallazgos":[...]}. Severidad `media` a propósito: es VISIBILIDAD,
no un candado (ci-gate corta en ALTA; tocar un script central es normal, ignorarlo no).
"""
import ast, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Dónde vive el código propio (nunca node_modules/keyword-volume-tool/.git).
FUENTES = [(".pipeline", (".py", ".mjs", ".sh")), ("scripts", (".py",)),
           ("mcp-local-seo", (".mjs", ".js")), (".", (".js",))]
SELF = os.path.basename(__file__)
# Cadena de publicación: tocarlas es lo más caro (bloquea el push o deja pasar páginas malas).
CRITICOS = {"ci-gate.py", "gate-pagina.py", "check-pagina-nueva.py",
            "check-contrato-checkers.mjs", "crecer.py"}


def _archivos():
    out = []
    for d, exts in FUENTES:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if f.endswith(exts) and os.path.isfile(os.path.join(p, f)):
                out.append(os.path.normpath(os.path.join(d, f)))
    return out


def _textos_referenciables(rel):
    """Devuelve el texto donde puede haber referencias a otros scripts, sin comentarios."""
    try:
        src = open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()
    except OSError:
        return ""
    if rel.endswith(".py"):
        # Solo literales de string del AST: un comentario NO crea dependencia.
        # Y se EXCLUYEN los docstrings: son prosa, no invocaciones. (Sin esto, el docstring
        # de este mismo archivo —que cita ci-gate.py, gate-pagina.py…— inventaba aristas.)
        try:
            arbol = ast.parse(src)
        except SyntaxError:
            return src
        docs = set()
        for n in ast.walk(arbol):
            if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                d = ast.get_docstring(n, clean=False)
                if d:
                    docs.add(d)
        return "\n".join(n.value for n in ast.walk(arbol)
                         if isinstance(n, ast.Constant) and isinstance(n.value, str)
                         and n.value not in docs)
    # .sh / .mjs / .js: quita comentarios de línea (aprox, suficiente para basenames).
    src = re.sub(r"^\s*#.*$", "", src, flags=re.M) if rel.endswith(".sh") else src
    src = re.sub(r"^\s*//.*$", "", src, flags=re.M)
    return src


def _grafo(archivos):
    base = {os.path.basename(a): a for a in archivos}
    inverso = {a: set() for a in archivos}          # invocado -> {invocadores}
    for a in archivos:
        # Este archivo NO invoca a nadie: nombra scripts (CRITICOS) para clasificarlos.
        # Si se analizara a sí mismo, se declararía dependiente de media cadena de publicación.
        if os.path.basename(a) == SELF:
            continue
        txt = _textos_referenciables(a)
        if not txt:
            continue
        for bn, destino in base.items():
            if destino == a or bn == SELF:
                continue
            if re.search(r"(?<![\w.-])" + re.escape(bn) + r"(?![\w])", txt):
                inverso[destino].add(a)
    return inverso


def _cambiados():
    """Archivos tocados en el working tree (staged + unstaged), relativos a ROOT."""
    vistos = []
    for args in (["diff", "--name-only"], ["diff", "--name-only", "--cached"]):
        try:
            r = subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True, timeout=20)
            if r.returncode == 0:
                vistos += [l.strip() for l in r.stdout.splitlines() if l.strip()]
        except (OSError, subprocess.SubprocessError):
            pass
    return sorted(set(vistos))


def main():
    archivos = _archivos()
    inverso = _grafo(archivos)
    objetivo = [os.path.normpath(a) for a in sys.argv[1:]] or _cambiados()

    hallazgos = []
    for f in objetivo:
        directos = sorted(inverso.get(f, ()))
        if not directos:
            continue                                  # no es nodo del grafo, o nadie depende
        nivel2 = sorted({p for d in directos for p in inverso.get(d, ())} - set(directos) - {f})
        bn = os.path.basename(f)
        critico = bn in CRITICOS or any(os.path.basename(d) in CRITICOS for d in directos)
        hallazgos.append({
            "id": "impacto-%s" % bn,
            "archivo": f, "linea": 0,
            "severidad": "media", "categoria": "impacto",
            "descripcion": "Tocaste %s: %d script(s) dependen de él%s%s. Corre esos antes de publicar." % (
                bn, len(directos),
                " (CADENA DE PUBLICACIÓN)" if critico else "",
                " → " + ", ".join(os.path.basename(d) for d in directos)),
            "fix_sugerido": "Verificar dependientes directos: %s.%s" % (
                ", ".join(directos),
                (" En 2º grado: %s." % ", ".join(nivel2)) if nivel2 else ""),
        })

    print(json.dumps({"hallazgos": hallazgos, "archivos_grafo": len(archivos),
                      "analizados": len(objetivo)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
