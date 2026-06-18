#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de reglas de PLANTILLA para plomeroculiacanpro.mx.

Convierte en comprobaciones mecanicas (grep/parseo, sin juicio) las reglas de
REGLAS.md que hoy dependian de que un revisor LLM "recordara leerlas" (seo, movil,
a11y, perf, links). Lo subjetivo (contraste, intencion de busqueda, similitud de
doorways, calidad de copy) NO esta aqui: se queda en los revisores LLM.

Solo LEE disco y parsea archivos locales. Sin red, sin servidor. Solo REPORTA.
Salida DETERMINISTA: idéntica entre corridas (los hallazgos se ordenan de forma
estable antes de asignar ids).

Emite a stdout SOLO el JSON comun de hallazgos:
  {"hallazgos":[{"id":"plt-001","archivo":"ruta","linea":0,
                 "severidad":"alta|media|baja","categoria":"seo|movil|a11y|perf|links",
                 "descripcion":"...","fix_sugerido":"..."}]}

Reglas mecanicas (todas ancladas en REGLAS.md):
  1. links  (alta)  Enlace/recurso interno (href/src/srcset) a archivo inexistente
                    en disco y sin redirect que lo cubra.            (8a747e6e, f8c72299)
  2. seo    (alta)  og:image / twitter:image apuntando a archivo inexistente.
                                                          (590d3e4a, f8c72299, 26cf9939)
  3. seo    (alta)  aggregateRating / Review self-serving en paginas de /blog/. (08a95902)
  4. seo    (media) Email de dominio incorrecto @plomeropro.com.         (f8c72299)
  5. a11y   (media) #exit-intent-popup sin role=dialog / aria-modal / aria-labelledby,
                    o su titulo sin id="exit-popup-title".              (a11y-302)
  6. perf   (media) Mas de UNA <img> con fetchpriority="high" (compiten por el LCP).
                                                            (perf-202/203/204)
  7. perf   (media) <img loading="eager"> que NO es el hero (sin fetchpriority=high)
                    ni el logo del nav -> debe ir loading="lazy".       (perf-301..314)
  8. perf   (media) <img> sin width y/o height (CLS).                    (bd9ccadf)
  9. movil  (media) Paridad CSS: una regla critica presente en algun styles*.css pero
                    ausente en otro (los 3 deben tener la misma regla). (f44ef39f + reinc.)
 10. movil  (baja)  <table> sin envoltura <div class="table-wrapper"> (mitigado por el
                    fallback CSS global, por eso baja).                 (f44ef39f)
 11. perf   (baja)  theme-color == #0066cc (placeholder prohibido); o pagina indexable
                    sin meta theme-color alguna.                   (bd9ccadf, fdc89c6c)
"""
import os
import re
import json
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz del repo
BASE = "https://plomeroculiacanpro.mx"

# Directorios que NUNCA son paginas servidas del sitio (mismo criterio que
# check-indexabilidad.py).
SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
             "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
             "/mcp-local-seo/", "/scripts/")

# Extensiones que son RECURSOS en disco (un href/src a esto debe existir tal cual).
RESOURCE_EXT = (".css", ".js", ".mjs", ".webp", ".png", ".jpg", ".jpeg", ".gif",
                ".svg", ".ico", ".webmanifest", ".json", ".xml", ".pdf", ".txt",
                ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".webm", ".avif")

# ---------------------------------------------------------------- hallazgos
_findings = []  # se ordenan y se les asigna id al final (determinismo)


def add(sev, archivo, categoria, desc, fix):
    _findings.append({
        "archivo": archivo, "linea": 0, "severidad": sev,
        "categoria": categoria, "descripcion": desc, "fix_sugerido": fix,
    })


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


# ---------------------------------------------------------------- redirects (para no
# marcar como roto un enlace que Netlify resuelve via 301/200 rewrite)
def _mk_redirect(frm, status):
    if frm.endswith("*"):
        return (frm[:-1], True, status)   # "/foo/*" -> prefijo "/foo/"
    return (frm, False, status)


def load_redirects():
    rules = []  # (prefijo_o_ruta, es_prefijo, status)
    rp = os.path.join(ROOT, "_redirects")
    if os.path.isfile(rp):
        for line in read(rp).splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            status = parts[-1] if parts[-1].isdigit() else "301"
            rules.append(_mk_redirect(parts[0], status))
    nt = os.path.join(ROOT, "netlify.toml")
    if os.path.isfile(nt):
        txt = read(nt)
        for blk in re.split(r"\[\[redirects\]\]", txt)[1:]:
            mf = re.search(r'from\s*=\s*"([^"]+)"', blk)
            ms = re.search(r'status\s*=\s*(\d+)', blk)
            if mf:
                rules.append(_mk_redirect(mf.group(1), ms.group(1) if ms else "301"))
    return rules


def redirect_covers(path, rules):
    """True solo si una regla ESPECIFICA reescribe/redirige el path a un destino real
    (2xx/3xx). Se ignoran: el comodin raiz "/" (demasiado amplio) y las reglas 4xx/5xx
    como el fallback `/* -> /404.html 404` (que ES el caso de enlace roto, no lo tapa)."""
    for pref, is_prefix, status in rules:
        if status[:1] in ("4", "5"):
            continue
        if is_prefix and pref in ("", "/"):
            continue  # catch-all: no cuenta como redirect intencional de un enlace
        if is_prefix:
            if path.startswith(pref):
                return True
        elif path == pref:
            return True
    return False


# ---------------------------------------------------------------- helpers de parseo
def attr(tag, name):
    m = re.search(name + r'\s*=\s*["\']([^"\']*)["\']', tag, re.I)
    return m.group(1) if m else None


def imgs(t):
    return re.findall(r'<img\b[^>]*>', t, re.I)


def is_stub(t):
    return bool(re.search(r'<meta[^>]*http-equiv=["\']refresh["\']', t, re.I))


def has_noindex(t):
    for m in re.finditer(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*>', t, re.I):
        c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
        if c and "noindex" in c.group(1).lower():
            return True
    return False


# ---------------------------------------------------------------- recoleccion de paginas
def collect_pages():
    pages = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dn = "/" + os.path.relpath(dirpath, ROOT).replace(os.sep, "/") + "/"
        if any(s in dn for s in SKIP_DIRS):
            dirnames[:] = []
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            if fn.endswith(".min.html") or ".backup" in fn:
                continue
            pages.append(os.path.join(dirpath, fn))
    pages.sort()
    return pages


# ---------------------------------------------------------------- mapeo enlace -> disco
def resolve_to_disk(value, page_dir):
    """Devuelve (ruta_disco_o_None, url_path_normalizada) para un href/src interno.
    None en ruta -> no es un enlace interno verificable (externo/anchor/etc.)."""
    v = value.strip()
    if not v:
        return None, None
    low = v.lower()
    if (low.startswith(("http://", "https://", "//", "mailto:", "tel:", "#",
                        "data:", "javascript:", "sms:", "geo:"))):
        return None, None
    # quitar query y fragmento
    clean = v.split("#")[0].split("?")[0]
    if not clean:
        return None, None
    # ruta URL normalizada (para redirects): siempre absoluta desde la raiz del sitio
    if clean.startswith("/"):
        disk = os.path.normpath(os.path.join(ROOT, clean.lstrip("/")))
        url_path = clean
    else:
        disk = os.path.normpath(os.path.join(page_dir, clean))
        url_path = "/" + os.path.relpath(disk, ROOT).replace(os.sep, "/")
    # mapear a archivo concreto
    if clean.endswith("/"):
        return os.path.join(disk, "index.html"), url_path
    _, ext = os.path.splitext(disk)
    ext = ext.lower()
    if ext in RESOURCE_EXT or ext in (".html", ".htm"):
        return disk, url_path  # referencia directa a un archivo concreto
    # sin extension y sin slash final: ruta "bonita" -> dir/index.html, luego .html
    cand = os.path.join(disk, "index.html")
    if os.path.isfile(cand):
        return cand, url_path
    if os.path.isfile(disk + ".html"):
        return disk + ".html", url_path
    return cand, url_path  # se reportara como inexistente (index.html del dir)


def link_candidates(t):
    """Lista de valores de href/src/srcset del documento."""
    vals = []
    for m in re.finditer(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', t, re.I):
        vals.append(m.group(1))
    for m in re.finditer(r'srcset\s*=\s*["\']([^"\']+)["\']', t, re.I):
        for piece in m.group(1).split(","):
            url = piece.strip().split()[0] if piece.strip() else ""
            if url:
                vals.append(url)
    return vals


# ================================================================ CHECKS por pagina
def check_page(fpath, t, noindex, redirects):
    r = rel(fpath)
    page_dir = os.path.dirname(fpath)

    # --- 1. enlaces/recursos internos rotos (alta, links)
    seen = set()
    for val in link_candidates(t):
        disk, url_path = resolve_to_disk(val, page_dir)
        if disk is None:
            continue
        key = (disk, url_path)
        if key in seen:
            continue
        seen.add(key)
        if os.path.isfile(disk):
            continue
        if url_path and redirect_covers(url_path, redirects):
            continue  # lo cubre un redirect/rewrite: no es 404
        add("alta", r, "links",
            "Enlace/recurso interno a archivo inexistente: %s" % val,
            "Corregir la ruta a un archivo que exista en disco, o eliminar el enlace; "
            "si la URL depende de un redirect, añadir la regla en _redirects/netlify.toml")

    # --- 2. og:image / twitter:image a archivo inexistente (alta, seo)
    for m in re.finditer(r'<meta\b[^>]*>', t, re.I):
        tag = m.group(0)
        prop = (attr(tag, "property") or attr(tag, "name") or "").lower()
        if prop not in ("og:image", "twitter:image"):
            continue
        content = attr(tag, "content")
        if not content:
            continue
        disk, _ = resolve_to_disk(content, page_dir)
        if disk is None:
            continue  # imagen externa (CDN): no verificable en disco
        if not os.path.isfile(disk):
            add("alta", r, "seo",
                "%s apunta a un archivo inexistente: %s" % (prop, content),
                "Apuntar %s a una imagen que exista en disco (ej. un .webp del repo)" % prop)

    # --- 3. aggregateRating / Review en /blog/ (alta, seo)
    if r.startswith("blog/"):
        if re.search(r'"aggregateRating"', t) or re.search(r'"@type"\s*:\s*"Review"', t):
            add("alta", r, "seo",
                "Schema con aggregateRating/Review self-serving en página de blog",
                "Quitar aggregateRating/Review del JSON-LD del blog (política self-serving "
                "de Google); las reseñas solo en páginas de negocio")

    # --- 4. email de dominio incorrecto @plomeropro.com (media, seo)
    if re.search(r'@plomeropro\.com', t, re.I):
        add("media", r, "seo",
            "Email con dominio incorrecto @plomeropro.com",
            "Usar info@plomeroculiacanpro.mx (dominio correcto)")

    # --- 4b. fuga de esqueleto: wa.me ?text= con una "zona" ajena al slug de la página (media, contenido)
    #     caso crece-001: una página de servicio nueva heredó "zona oriente" del esqueleto de zona,
    #     así el lead de WhatsApp llega con la intención equivocada.
    for m in re.finditer(r'wa\.me/\d+\?text=([^"\'\s>]+)', t, re.I):
        texto = m.group(1).replace("%20", " ").lower()
        for z in ("oriente", "norte", "poniente", "sur"):
            if ("zona " + z) in texto and ("zona-" + z) not in r:
                add("media", r, "contenido",
                    "Mensaje de WhatsApp prellenado con 'zona %s' en una página cuyo slug no es de esa zona "
                    "(fuga del esqueleto plomero-zona-%s-culiacan)" % (z, z),
                    "Reemplazar el ?text= del enlace wa.me por un mensaje acorde al servicio/zona de ESTA página")
                break

    # --- 5. exit-intent-popup sin ARIA (media, a11y)
    mp = re.search(r'<div\b[^>]*id=["\']exit-intent-popup["\'][^>]*>', t, re.I)
    if mp:
        tag = mp.group(0)
        falta = []
        if not re.search(r'role=["\']dialog["\']', tag, re.I):
            falta.append('role="dialog"')
        if not re.search(r'aria-modal=["\']true["\']', tag, re.I):
            falta.append('aria-modal="true"')
        if not re.search(r'aria-labelledby=', tag, re.I):
            falta.append('aria-labelledby')
        if not re.search(r'id=["\']exit-popup-title["\']', t, re.I):
            falta.append('título con id="exit-popup-title"')
        if falta:
            add("media", r, "a11y",
                "#exit-intent-popup sin atributos de diálogo modal: falta %s" % ", ".join(falta),
                'Igualar al patrón correcto (index.html): <div id="exit-intent-popup" '
                'role="dialog" aria-modal="true" aria-labelledby="exit-popup-title"> y el '
                '<h3> con id="exit-popup-title"')

    # --- 6/7/8. checks sobre <img>
    img_tags = imgs(t)
    high = 0
    for tag in img_tags:
        is_high = bool(re.search(r'fetchpriority=["\']high["\']', tag, re.I))
        if is_high:
            high += 1
        # 7. loading=eager que no es hero ni logo
        if re.search(r'loading=["\']eager["\']', tag, re.I):
            src = (attr(tag, "src") or "")
            if not is_high and "logo" not in src.lower():
                add("media", r, "perf",
                    "<img> con loading=\"eager\" que no es el hero LCP ni el logo: %s"
                    % (src or tag[:60]),
                    'Cambiar a loading="lazy" (solo el hero con fetchpriority="high" va eager)')
        # 8. sin width y/o height
        if not re.search(r'\bwidth\s*=', tag, re.I) or not re.search(r'\bheight\s*=', tag, re.I):
            src = (attr(tag, "src") or "")
            add("media", r, "perf",
                "<img> sin width y/o height (CLS): %s" % (src or tag[:60]),
                "Declarar width y height explícitos en la imagen para reservar espacio (evitar CLS)")
    # 6. mas de una img high
    if high > 1:
        add("media", r, "perf",
            "%d imágenes con fetchpriority=\"high\" (solo el hero LCP debe llevarlo)" % high,
            "Dejar fetchpriority=\"high\" en UNA sola imagen (el hero); quitarlo del resto")

    # --- 10. tabla sin table-wrapper (baja, movil)
    for tm in re.finditer(r'<table\b', t, re.I):
        start = tm.start()
        window = t[max(0, start - 200):start]
        if "table-wrapper" not in window:
            add("baja", r, "movil",
                "<table> sin envoltura <div class=\"table-wrapper\"> (scroll horizontal móvil)",
                'Envolver la <table> en <div class="table-wrapper"> (patrón establecido); '
                'el fallback CSS global mitiga, pero el wrapper es el patrón correcto')

    # --- 11. theme-color (baja, perf)
    tc_metas = re.findall(r'<meta\b[^>]*name=["\']theme-color["\'][^>]*>', t, re.I)
    if tc_metas:
        for tag in tc_metas:
            val = (attr(tag, "content") or "").strip().lower()
            if val == "#0066cc":
                add("baja", r, "perf",
                    "theme-color usa el placeholder prohibido #0066cc",
                    "Cambiar theme-color al color de marca vigente del sitio (no el placeholder #0066cc)")
    elif not noindex:
        add("baja", r, "perf",
            "Página indexable sin <meta name=\"theme-color\">",
            "Añadir <meta name=\"theme-color\" content=\"#...\"> con el color de marca en el <head>")


# ================================================================ CHECK global: paridad CSS
# Firmas EXACTAS (normalizadas sin espacios) de reglas que REGLAS.md documenta como
# reincidentes en paridad. Se comprueba PRESENCIA (>=1) en cada styles*.css: si una
# firma esta en algun archivo pero falta (0) en otro -> regresion de paridad.
CSS_PARITY_SIGNATURES = [
    "table-wrapper{overflow-x:auto",          # envoltura de tablas (f44ef39f)
    "table{display:block;overflow-x:auto",    # fallback global de tablas (movil-203)
    ".footer-logoimg",                         # regla del logo del footer (f44ef39f)
]


def check_css_parity():
    css_files = sorted(glob.glob(os.path.join(ROOT, "styles*.css")))
    if len(css_files) < 2:
        return  # nada que comparar
    norm = {}
    for c in css_files:
        norm[c] = re.sub(r"\s+", "", read(c))
    for sig in CSS_PARITY_SIGNATURES:
        present = {c: (sig in norm[c]) for c in css_files}
        if any(present.values()) and not all(present.values()):
            tienen = sorted(rel(c) for c in css_files if present[c])
            faltan = sorted(c for c in css_files if not present[c])
            for c in faltan:
                add("media", rel(c), "movil",
                    "Paridad CSS rota: la regla '%s' existe en %s pero falta aquí"
                    % (sig, ", ".join(tienen)),
                    "Copiar la regla '%s' a este archivo para mantener los 3 CSS en paridad "
                    "(styles.css fuente + styles.min.css + styles.<hash>.css servido)" % sig)


# ================================================================ MAIN
def main():
    redirects = load_redirects()
    for fpath in collect_pages():
        t = read(fpath)
        if is_stub(t):
            continue  # stub de redireccion (meta-refresh): no es pagina de contenido
        check_page(fpath, t, has_noindex(t), redirects)
    check_css_parity()

    # orden estable + asignacion de ids deterministas
    sev_rank = {"alta": 0, "media": 1, "baja": 2}
    _findings.sort(key=lambda h: (h["archivo"], sev_rank.get(h["severidad"], 9),
                                  h["categoria"], h["descripcion"]))
    out = []
    for i, h in enumerate(_findings, 1):
        out.append({
            "id": "plt-%03d" % i, "archivo": h["archivo"], "linea": h["linea"],
            "severidad": h["severidad"], "categoria": h["categoria"],
            "descripcion": h["descripcion"], "fix_sugerido": h["fix_sugerido"],
        })
    print(json.dumps({"hallazgos": out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
