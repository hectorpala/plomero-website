#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de ESTRUCTURA a nivel de TODO el sitio (no solo páginas del diff).
Cierra el hueco: validate-landing/gate-pagina solo corren sobre las páginas editadas, así
que defectos PRE-EXISTENTES (sin <meta robots>, hero sin .hero-content) quedan invisibles
hasta que alguien toca esa página y el push se bloquea por sorpresa
(HISTORIAL: seo-meta-robots-repfugas, plt-hero-tinaco, deuda-robots-001).

Recorre TODAS las <loc> indexables del sitemap y verifica:
  R1 (media) <meta name="robots"> presente.
  R2 (media) si la página tiene class="hero", debe envolver su contenido en .hero-content.

Emite a stdout SOLO el JSON común de hallazgos. Sin argumentos: barre el sitio completo.
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://plomeroculiacanpro.mx"
SITEMAP = os.path.join(ROOT, "sitemaps", "main_sitemap.xml")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "estr-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "plantilla",
        "descripcion": desc, "fix_sugerido": fix,
    })

def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

def url_to_path(loc):
    path = loc[len(BASE):] if loc.startswith(BASE) else loc
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return os.path.join(ROOT, "index.html")
    rels = path.strip("/")
    if path.endswith("/"):
        return os.path.join(ROOT, rels, "index.html")
    if path.endswith(".html"):
        return os.path.join(ROOT, rels)
    cand = os.path.join(ROOT, rels, "index.html")
    if os.path.isfile(cand):
        return cand
    return os.path.join(ROOT, rels + ".html")

NOINDEX         = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
HAS_ROBOTS      = re.compile(r'<meta[^>]+name=["\']robots["\']', re.I)
HAS_HERO        = re.compile(r'class=["\'][^"\']*(?<![\w-])hero(?![\w-])', re.I)        # token "hero" exacto (no "hero-content")
HAS_HEROCONTENT = re.compile(r'class=["\'][^"\']*(?<![\w-])hero-content(?![\w-])', re.I)

def main():
    txt = read(SITEMAP)
    seen = set()
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt):
        fpath = url_to_path(loc)
        if fpath in seen or not os.path.isfile(fpath):
            continue
        seen.add(fpath)
        rel = os.path.relpath(fpath, ROOT)
        t = read(fpath)
        if NOINDEX.search(t):
            continue  # noindex: fuera del estándar indexable
        if not HAS_ROBOTS.search(t):
            add("media", rel,
                "%s (indexable, en sitemap) no emite <meta name=\"robots\">; deuda PRE-EXISTENTE que el gate solo expone al editar la página" % loc,
                "Añadir antes del canonical: <meta name=\"robots\" content=\"index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1\"> (idéntico a las hermanas nuevas, p.ej. reparacion-de-fugas)")
        if HAS_HERO.search(t) and not HAS_HEROCONTENT.search(t):
            add("media", rel,
                "%s tiene class=\"hero\" pero le falta el wrapper div.hero-content del estándar (validate-landing/gate FALLAN al editarla)" % loc,
                "Envolver h1+subtitle+CTA del hero en <div class=\"hero-content\">…</div> como el resto de servicios; verificar visual headless 375/1280")
    # "analizadas" habilita la guardia genérica de check-infra (analizadas==0 → ALTA):
    # con el sitemap ilegible este checker imprimía {"hallazgos":[]} y pasaba por sano.
    print(json.dumps({"hallazgos": hallazgos, "analizadas": len(seen)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
