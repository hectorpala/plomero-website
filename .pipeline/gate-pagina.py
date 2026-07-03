#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candado todo-en-uno para páginas NUEVAS o modificadas antes de publicar.

Corre, para cada página dada:
  1) validate-landing.sh   — estructura de plantilla del sitio (omite noindex).
  2) ci-gate.py            — checkers deterministas del sitio: 0 hallazgos ALTA.
  3) Anti-doorway          — similitud Jaccard del texto VISIBLE de cada página
                             nueva contra TODAS las hermanas indexables del sitio.
                             FALLA si alguna pareja ≥ UMBRAL_FAIL (casi-idénticas).

Uso:
    python3 .pipeline/gate-pagina.py servicios/plomero-zona-norte-culiacan/index.html [más...]

Salida: reporte legible; exit 0 si TODO pasa, 1 si algo falla (no publicar).
Las páginas noindex se saltan el anti-doorway (no compiten por ranking).
"""
import glob
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMBRAL_FAIL = 0.80   # ≥ esto = doorway (bloquea)
UMBRAL_WARN = 0.72   # ≥ esto = advertencia (revisar, no bloquea)


_TOK_CACHE = {}


def visible_tokens(path):
    key = os.path.abspath(path)
    if key in _TOK_CACHE:
        return _TOK_CACHE[key]
    h = open(path, encoding="utf-8").read()
    if re.search(r'<meta name="robots"[^>]*noindex', h):
        _TOK_CACHE[key] = None
        return None  # noindex → no entra al anti-doorway
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    toks = set(re.findall(r"\w{4,}", html.unescape(h).lower()))
    _TOK_CACHE[key] = toks
    return toks


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a and b) else 0.0


def siblings(path):
    """TODAS las páginas indexables del sitio (servicios, colonias y blog), MENOS la propia —
    no solo las del mismo directorio (cierra el hueco de un duplicado escondido en otra
    familia, p.ej. un servicio que clona una colonia o un blog)."""
    me = os.path.abspath(path)
    pats = [
        os.path.join(ROOT, "servicios", "*", "index.html"),
        os.path.join(ROOT, "servicios", "plomero-colonias-culiacan", "*", "index.html"),
        os.path.join(ROOT, "blog", "*", "index.html"),
    ]
    out, seen = [], set()
    for pat in pats:
        for f in glob.glob(pat):
            af = os.path.abspath(f)
            if af != me and af not in seen:
                seen.add(af); out.append(f)
    return out


def main():
    pages = sys.argv[1:]
    if not pages:
        print("Uso: gate-pagina.py <ruta/index.html> [...]"); sys.exit(2)

    errors = 0

    # 1) validate-landing.sh por página (solo landings de servicio; los blogs usan
    #    otra plantilla y se omiten — su paridad se evalúa contra hermanas de blog).
    print("── 1) validate-landing.sh ──")
    vs = os.path.join(ROOT, "scripts", "validate-landing.sh")
    for p in pages:
        pn = p.replace("\\", "/")
        if "blog" in pn.split("/"):
            print("  ⏭  " + p + " → blog (plantilla distinta a servicios; validate-landing omitido)")
            continue
        if "plomero-colonias-culiacan" in pn and pn.rstrip("/").count("/") >= 3:
            print("  ⏭  " + p + " → colonia (plantilla distinta a servicios; validate-landing omitido)")
            continue
        r = subprocess.run(["bash", vs, p], capture_output=True, text=True, cwd=ROOT)
        last = (r.stdout.strip().splitlines() or ["(sin salida)"])[-1]
        ok = r.returncode == 0
        print(("  ✅ " if ok else "  ❌ ") + p + " → " + last)
        if not ok:
            errors += 1

    # 2) ci-gate (checkers del sitio: 0 ALTA)
    print("── 2) ci-gate.py (checkers deterministas, 0 ALTA) ──")
    r = subprocess.run([sys.executable, os.path.join(ROOT, ".pipeline", "ci-gate.py")],
                       capture_output=True, text=True, cwd=ROOT)
    print("  " + "\n  ".join(r.stdout.strip().splitlines()[-3:]))
    if r.returncode != 0:
        errors += 1

    # 3) Anti-doorway
    print("── 3) Anti-doorway (Jaccard vs todo el sitio indexable) ──")
    for p in pages:
        tv = visible_tokens(p)
        if tv is None:
            print("  ⏭  " + p + " → noindex, no compite por ranking (omitido)")
            continue
        worst = 0.0; worst_sib = None
        for sib in siblings(p):
            ts = visible_tokens(sib)
            if ts is None:
                continue
            j = jaccard(tv, ts)
            if j > worst:
                worst, worst_sib = j, sib
        tag = "✅"
        if worst >= UMBRAL_FAIL:
            tag = "❌ DOORWAY"; errors += 1
        elif worst >= UMBRAL_WARN:
            tag = "⚠️  REVISAR"
        sib_name = os.path.basename(os.path.dirname(worst_sib)) if worst_sib else "(sin hermanas)"
        print("  %s %s → Jaccard máx %.2f vs %s" % (tag, p, worst, sib_name))

    print("")
    if errors:
        print("❌ CANDADO FALLA: %d problema(s). NO publicar; dejar en rama y revisar." % errors)
        sys.exit(1)
    print("✅ CANDADO OK: estructura + checkers + anti-doorway. Apto para publicar.")
    sys.exit(0)


if __name__ == "__main__":
    main()
