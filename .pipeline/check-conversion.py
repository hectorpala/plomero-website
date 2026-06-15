#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de CONVERSIÓN para plomeroculiacanpro.mx.
Solo lee disco + parsea HTML local (sin red). Solo REPORTA. Salida estable.

Por cada página INDEXABLE (canonical + title, sin noindex; mismo criterio que
check-indexabilidad.py) asegura que existan los caminos de conversión:
  1. >=1 enlace `tel:` con el número correcto (667 392 2273 / 526673922273).   (alta)
  2. >=1 enlace `wa.me` (o api.whatsapp.com) con el número correcto 526673922273.(alta)
  3. un CTA "antes del fold" (CTA en el hero/header o botón flotante tel/wa).    (media)
  4. formulario de captación en las PÁGINAS CLAVE (/ y /contacto/, acordado con
     Héctor: hoy ambas tienen <form>; el resto convierte por tel/wa/CTA).       (alta)

Emite a stdout SOLO el JSON común:
  {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}],"analizadas":N}
categoria = "conversion".
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://plomeroculiacanpro.mx"

SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
             "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
             "/mcp-local-seo/", "/scripts/")

# Páginas clave que DEBEN tener formulario (acordado con Héctor 2026-06-14).
KEY_FORM_PATHS = ("/", "/contacto/")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "conv-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "conversion",
        "descripcion": desc, "fix_sugerido": fix,
    })

def rel(p):
    return os.path.relpath(p, ROOT)

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

def url_path_of(canonical):
    p = canonical[len(BASE):] if canonical.startswith(BASE) else canonical
    p = p.split("#")[0].split("?")[0]
    return p or "/"

# ------------------------------------------------- validación de números
def tel_digits_ok(href):
    d = re.sub(r"\D", "", href.split("?")[0])
    if d in ("6673922273", "526673922273"):
        return True
    # tolera prefijo 52/521 + el nacional de 10 dígitos
    return d.endswith("6673922273") and (len(d) == 10 or d.startswith("52"))

def wa_number_ok(href):
    m = re.search(r'(?:wa\.me/|api\.whatsapp\.com/send\?[^"\']*phone=)(\d+)', href, re.I)
    if not m:
        return False
    return m.group(1).startswith("526673922273")

def anchors(t):
    """Lista de href de <a ...>."""
    out = []
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\']', t, re.I):
        out.append(m.group(1))
    return out

def above_fold_region(t):
    """Subcadena desde <body> hasta el primer cierre de hero/header/section, o 15k chars."""
    mb = re.search(r'<body\b', t, re.I)
    start = mb.start() if mb else 0
    tail = t[start:start + 30000]
    end = len(tail)
    for pat in (r'</header>', r'</section>'):
        m = re.search(pat, tail, re.I)
        if m:
            end = min(end, m.end())
    return tail[:min(end, 15000)] if end else tail[:15000]

def has_above_fold_cta(t):
    region = above_fold_region(t)
    if re.search(r'href=["\'](?:tel:|[^"\']*wa\.me|[^"\']*api\.whatsapp\.com)', region, re.I):
        return True
    if re.search(r'class=["\'][^"\']*(?:btn-primary|cta-buttons|floating-btn|btn-whatsapp|emergency-btn|final-cta)', region, re.I):
        return True
    return False

# ================================================================ MAIN
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
        t = read(fpath)
        canonical = get_canonical(t)
        title = get_title(t)
        if not canonical or not title or has_noindex(t):
            continue  # no es una página indexable formal
        analizadas += 1
        r = rel(fpath)
        upath = url_path_of(canonical)

        hrefs = anchors(t)
        tels = [h for h in hrefs if h.lower().startswith("tel:")]
        was = [h for h in hrefs if "wa.me" in h.lower() or "api.whatsapp.com" in h.lower()]

        # 1. tel:
        if not tels:
            add("alta", r, "CONVERSIÓN: %s no tiene ningún enlace tel: (sin CTA de llamada)" % canonical,
                "Añadir un enlace <a href=\"tel:+526673922273\"> visible (botón de llamada)")
        elif not any(tel_digits_ok(h) for h in tels):
            add("alta", r,
                "CONVERSIÓN: %s tiene enlaces tel: pero NINGUNO con el número correcto (667 392 2273 / 526673922273): %s" % (canonical, ", ".join(sorted(set(tels))[:3])),
                "Corregir el href tel: al número correcto +526673922273")

        # 2. wa.me
        if not was:
            add("alta", r, "CONVERSIÓN: %s no tiene ningún enlace wa.me/WhatsApp (sin CTA de WhatsApp)" % canonical,
                "Añadir un enlace <a href=\"https://wa.me/526673922273\"> visible")
        elif not any(wa_number_ok(h) for h in was):
            add("alta", r,
                "CONVERSIÓN: %s tiene enlaces wa.me pero NINGUNO con el número correcto 526673922273: %s" % (canonical, ", ".join(sorted(set(w[:60] for w in was))[:3])),
                "Corregir el enlace a https://wa.me/526673922273 (ver REGLAS.md: una URL wa.me truncada rompe el sitio)")

        # 3. CTA antes del fold (heurístico -> media)
        if not has_above_fold_cta(t):
            add("media", r,
                "CONVERSIÓN: %s no parece tener un CTA antes del fold (ni tel/wa ni botón en el hero/header ni botón flotante)" % canonical,
                "Asegurar un CTA visible sin hacer scroll (botón de llamar/WhatsApp en el hero o flotante)")

        # 4. formulario en páginas clave
        if upath in KEY_FORM_PATHS and not re.search(r'<form\b', t, re.I):
            add("alta", r,
                "CONVERSIÓN: la página clave %s no tiene <form> de captación de leads" % canonical,
                "Restaurar/añadir el formulario de contacto en la página clave")

    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
