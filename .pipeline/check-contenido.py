#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de RESTOS DE PLANTILLA / contenido caduco (parte MECÁNICA del
revisor-contenido). Lo SUBJETIVO (thin content, duplicado, ortografía) NO está aquí:
lo cubre el revisor LLM revisor-contenido. Solo lee disco + parsea HTML local. Solo
REPORTA. Salida estable.

Detecta (sobre cada .html servido, ignorando <script>/<style>):
  1. Tokens de plantilla sin renderizar: {{...}}, ${...}                      -> alta
  2. Placeholders en corchete [ciudad]/[colonia]/[servicio]/[zona]/...         -> alta
  3. "lorem ipsum"                                                            -> alta
  4. Marcas de desarrollo: "TODO:" (con dos puntos), "FIXME"                  -> media
     (OJO: "TODO" suelto NO se marca: en español "todo" es palabra común.)
  5. Placeholder "XXXX" (4+ equis)                                            -> media
  6. Año caduco (< año actual) en <title> o <h1> (p.ej. "Precios 2024")       -> media

Emite a stdout SOLO el JSON común:
  {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}],"analizadas":N}
categoria = "contenido".
"""
import os
import re
import json
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_YEAR = datetime.date.today().year

SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
             "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
             "/mcp-local-seo/", "/scripts/")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "cont-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "contenido", "descripcion": desc, "fix_sugerido": fix,
    })

def rel(p):
    return os.path.relpath(p, ROOT)

def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

def has_noindex(t):
    for m in re.finditer(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*>', t, re.I):
        c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
        if c and "noindex" in c.group(1).lower():
            return True
    return False

def strip_code(t):
    """Quita <script> y <style> (evita falsos positivos de JS: ${}, TODO en comments)."""
    t = re.sub(r'<script\b[^>]*>.*?</script>', ' ', t, flags=re.I | re.S)
    t = re.sub(r'<style\b[^>]*>.*?</style>', ' ', t, flags=re.I | re.S)
    return t

# (regex, severidad, etiqueta, fix)
PATTERNS = [
    (re.compile(r'\{\{[^}\n]{1,40}\}\}'), "alta", "token de plantilla sin renderizar {{...}}",
     "Renderizar/quitar el token de plantilla: quedó literal en el HTML servido"),
    (re.compile(r'\$\{[^}\n]{1,40}\}'), "alta", "template literal sin renderizar ${...}",
     "Renderizar/quitar el ${...}: quedó literal en el HTML servido"),
    (re.compile(r'\[(?:ciudad|colonia|servicio|zona|nombre|barrio|sector|precio|keyword|empresa)\]', re.I),
     "alta", "placeholder en corchete sin reemplazar",
     "Reemplazar el placeholder [..] por el valor real (resto de la plantilla)"),
    (re.compile(r'lorem ipsum', re.I), "alta", "texto de relleno 'lorem ipsum'",
     "Reemplazar el lorem ipsum por contenido real"),
    (re.compile(r'\bTODO\s*:'), "media", "marca de desarrollo 'TODO:'",
     "Quitar la marca TODO: del contenido servido (es residuo de desarrollo)"),
    (re.compile(r'\bFIXME\b'), "media", "marca de desarrollo 'FIXME'",
     "Quitar la marca FIXME del contenido servido"),
    (re.compile(r'\bX{4,}\b'), "media", "placeholder 'XXXX'",
     "Reemplazar el placeholder XXXX por el valor real"),
]

def main():
    paginas = []
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
            paginas.append(os.path.join(dirpath, fn))
    paginas.sort()

    analizadas = 0
    for fpath in paginas:
        raw = read(fpath)
        if not raw:
            continue
        analizadas += 1
        r = rel(fpath)
        t = strip_code(raw)

        # 1-5: patrones de residuo (dedup por (página, etiqueta), muestra un ejemplo)
        for rx, sev, label, fix in PATTERNS:
            m = rx.search(t)
            if m:
                ej = m.group(0)
                ej = (ej[:40] + "…") if len(ej) > 40 else ej
                add(sev, r,
                    "CONTENIDO: %s en %s (ej.: %r)" % (label, r, ej), fix)

        # 6: año caduco en <title> / <h1> — solo páginas INDEXABLES (las noindex
        #    suelen ser archivos/eventos históricos: un año pasado ahí es correcto,
        #    p.ej. blog/marcha-paz-culiacan-2025).
        if has_noindex(raw):
            continue
        zonas = []
        mt = re.search(r'<title>(.*?)</title>', t, re.I | re.S)
        if mt:
            zonas.append(("title", mt.group(1)))
        for mh in re.finditer(r'<h1\b[^>]*>(.*?)</h1>', t, re.I | re.S):
            zonas.append(("h1", mh.group(1)))
        caducos = set()
        for donde, texto in zonas:
            for y in re.findall(r'\b(20[12][0-9])\b', texto):
                if int(y) < CURRENT_YEAR:
                    caducos.add((donde, y))
        for donde, y in sorted(caducos):
            add("media", r,
                "CONTENIDO: año caduco %s en <%s> de %s (año actual %d) — copy desactualizado para SEO" % (y, donde, r, CURRENT_YEAR),
                "Actualizar el año en el %s a %d (o quitarlo si no aporta)" % (donde, CURRENT_YEAR))

    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
