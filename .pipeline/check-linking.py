#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de ENLAZADO INTERNO para plomeroculiacanpro.mx.
Arma el grafo de enlaces internos (hrefs <a>) entre páginas INDEXABLES y detecta:
  1. HUÉRFANAS: páginas indexables con 0 enlaces internos entrantes (solo llegan por
     sitemap; Google las rastrea peor y reparten 0 PageRank interno).      -> media
  2. PROFUNDIDAD > 3 clics desde el home: páginas a las que solo se llega con más de
     3 saltos desde "/" (o inalcanzables por enlaces, = profundidad infinita). -> media
Solo lee disco + parsea HTML local. Solo REPORTA. Salida estable.

Emite a stdout SOLO el JSON común:
  {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}],"analizadas":N}
categoria = "enlazado".
"""
import os
import re
import json
from collections import deque
from urllib.parse import urljoin, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://plomeroculiacanpro.mx"
MAX_DEPTH = 3

SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
             "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
             "/mcp-local-seo/", "/scripts/")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "lnk-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "enlazado", "descripcion": desc, "fix_sugerido": fix,
    })

def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

def get_canonical(t):
    m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*>', t, re.I)
    if not m:
        return None
    h = re.search(r'href=["\']([^"\']+)["\']', m.group(0), re.I)
    return h.group(1).strip() if h else None

def get_title(t):
    m = re.search(r'<title>(.*?)</title>', t, re.I | re.S)
    return m.group(1).strip() if m else None

def has_noindex(t):
    for m in re.finditer(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*>', t, re.I):
        c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
        if c and "noindex" in c.group(1).lower():
            return True
    return False

def file_url_path(fpath):
    """URL path que Netlify serviría para este archivo."""
    relp = os.path.relpath(fpath, ROOT).replace(os.sep, "/")
    if relp == "index.html":
        return "/"
    if relp.endswith("/index.html"):
        return "/" + relp[:-len("index.html")]   # conserva la barra final
    return "/" + relp

def main():
    # ------------------------------------------------ recolectar páginas indexables
    pages = {}     # url_path -> (fpath, html)
    for dirpath, dirnames, files in os.walk(ROOT):
        dn = "/" + os.path.relpath(dirpath, ROOT).replace(os.sep, "/") + "/"
        if any(s in dn for s in SKIP_DIRS):
            dirnames[:] = []
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            if ".backup" in fn or fn.endswith(".min.html") or fn == "404.html":
                continue
            fpath = os.path.join(dirpath, fn)
            t = read(fpath)
            if not get_canonical(t) or not get_title(t) or has_noindex(t):
                continue  # no indexable -> no entra al grafo
            # preferir el path del canonical (lo que Google considera la URL real)
            can = get_canonical(t)
            cp = can[len(BASE):] if can.startswith(BASE) else None
            up = cp if cp else file_url_path(fpath)
            up = up.split("#")[0].split("?")[0] or "/"
            pages[up] = (fpath, t)

    node_paths = set(pages.keys())

    # alias: distintas formas de escribir el mismo nodo -> path canónico del nodo
    alias = {}
    for p in node_paths:
        alias[p] = p
        if p != "/" and p.endswith("/"):
            alias[p.rstrip("/")] = p          # sin barra final
        alias[p + "index.html"] = p           # con index.html explícito
    alias.setdefault("/index.html", "/")
    alias.setdefault("", "/")

    def resolve(href, base_path):
        h = href.strip()
        if not h or h.startswith(("mailto:", "tel:", "javascript:", "#", "data:", "sms:")):
            return None
        full = urljoin(BASE + base_path, h)
        sp = urlsplit(full)
        if sp.netloc and sp.netloc != urlsplit(BASE).netloc:
            return None  # externo
        path = sp.path or "/"
        if path in alias:
            return alias[path]
        if not path.endswith("/") and (path + "/") in alias:
            return alias[path + "/"]
        return None

    # ------------------------------------------------ aristas
    incoming = {p: set() for p in node_paths}
    outgoing = {p: set() for p in node_paths}
    for src, (fpath, t) in pages.items():
        for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\']', t, re.I):
            dst = resolve(m.group(1), src)
            if dst is None or dst == src or dst not in node_paths:
                continue
            outgoing[src].add(dst)
            incoming[dst].add(src)

    # ------------------------------------------------ BFS de profundidad desde "/"
    depth = {}
    if "/" in node_paths:
        depth["/"] = 0
        q = deque(["/"])
        while q:
            u = q.popleft()
            for v in sorted(outgoing[u]):
                if v not in depth:
                    depth[v] = depth[u] + 1
                    q.append(v)

    analizadas = len(node_paths)

    # ------------------------------------------------ 1. huérfanas
    huerfanas = sorted(p for p in node_paths if p != "/" and not incoming[p])
    if huerfanas:
        if len(huerfanas) > 8:
            add("media", "(grafo de enlaces internos)",
                "ENLAZADO: %d páginas indexables son HUÉRFANAS (0 enlaces internos entrantes); p.ej. %s" % (len(huerfanas), ", ".join(huerfanas[:8])),
                "Enlazarlas desde páginas relevantes (hub de servicios/colonias, footer, contenido relacionado); sin enlaces internos Google las rastrea peor y no reciben PageRank interno")
        else:
            for p in huerfanas:
                fp = os.path.relpath(pages[p][0], ROOT)
                add("media", fp,
                    "ENLAZADO: %s es HUÉRFANA (0 enlaces internos entrantes; solo se llega por sitemap)" % p,
                    "Añadir enlaces internos hacia esta página desde hubs/contenido relacionado")

    # ------------------------------------------------ 2. profundidad > 3
    profundas = sorted((p for p in node_paths if p != "/" and depth.get(p, 10**9) > MAX_DEPTH and incoming[p]),
                       key=lambda p: (depth.get(p, 10**9), p))
    if profundas:
        if len(profundas) > 8:
            ej = ", ".join("%s(%s)" % (p, depth.get(p, "∞")) for p in profundas[:8])
            add("media", "(grafo de enlaces internos)",
                "ENLAZADO: %d páginas a más de %d clics del home; p.ej. %s" % (len(profundas), MAX_DEPTH, ej),
                "Acercarlas al home (enlaces desde hubs o el menú) para bajar la profundidad de clic a <=3")
        else:
            for p in profundas:
                fp = os.path.relpath(pages[p][0], ROOT)
                d = depth.get(p)
                dtxt = str(d) if d is not None else "∞ (inalcanzable por enlaces internos)"
                add("media", fp,
                    "ENLAZADO: %s está a %s clics del home (>%d)" % (p, dtxt, MAX_DEPTH),
                    "Acercarla al home con enlaces desde hubs o el menú (profundidad de clic <=3)")

    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
