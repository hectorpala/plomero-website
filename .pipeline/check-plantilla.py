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
             "/mcp-local-seo/", "/scripts/", "/graphify-plomero/")
# NOTA (2026-07-09): NO agregar "/obsidian-vault/" aquí sin verificar primero con
# `git ls-files | grep obsidian` — está TRACKEADO (commit a3cb5ef9) y Netlify lo SIRVE en
# produccion (publish="." en netlify.toml). Bloqueado con _redirects 404! + robots.txt
# Disallow, pero el checker debe seguir viéndolo por si el bloqueo falla. Ver HISTORIAL.jsonl.

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


# ---------------------------------------------------------------- mapa nombre servicio -> ruta
_SERVICE_NAME_MAP = None


def _service_name_map():
    """Mapa {texto de servicio normalizado -> ruta canonica}, derivado del H1 de cada
    servicios/<slug>/index.html. Caza anclas cuyo TEXTO nombra un servicio real pero el HREF
    apunta a otro destino -- regresion vista 3x (2026-07-07/07-08/07-09): "Instalacion de
    sanitarios" enlazando al hub generico /servicios/ en vez de la pagina real."""
    global _SERVICE_NAME_MAP
    if _SERVICE_NAME_MAP is not None:
        return _SERVICE_NAME_MAP
    m = {}
    for fpath in sorted(glob.glob(os.path.join(ROOT, "servicios", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(fpath))
        if slug == "plomero-colonias-culiacan":
            continue
        try:
            txt = read(fpath)
        except Exception:
            continue
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.S)
        if not h1:
            continue
        name = re.sub(r'<[^>]+>', '', h1.group(1))
        name = re.sub(r'\s+', ' ', name).strip()
        name_norm = re.sub(r'\s+en\s+culiac[aá]n.*$', '', name, flags=re.I).strip().lower()
        if len(name_norm) < 6:
            continue
        m[name_norm] = "/servicios/%s/" % slug
    _SERVICE_NAME_MAP = m
    return m


def _norm_url_path(p):
    if not p:
        return p
    if p.endswith("index.html"):
        p = p[: -len("index.html")]
    if not p.endswith("/"):
        p += "/"
    return p


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

    # --- 4c. ANTI-FUGA site-wide (alta, contenido): la palabra "electricista" y el GTM
    #     del sitio hermano JAMÁS deben aparecer aquí. gen-landing/validate-landing solo
    #     cubren la CREACIÓN de servicios; ediciones de colonias/blog no pasaban por
    #     ningún guard (auditoría 2026-07-07) — este check cierra el hueco en todo el sitio.
    low_t = t.lower()
    for bad in ("electricista", "gtm-5z2qrz5q"):
        if bad in low_t:
            add("alta", r, "contenido",
                "FUGA del sitio hermano: la página contiene %r (contaminación de la plantilla origen)" % bad,
                "Eliminar toda mención/tracking del electricista; esta página es del sitio de PLOMERÍA")
            break

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

    # --- 4c. <div> de bloque anidado dentro de un <h2> = HTML inválido (media, a11y)
    #     caso 20260619: la plantilla de blog metió un CTA <div> dentro del <h2>; el lector
    #     de pantalla anuncia todo el bloque como texto del encabezado y rompe la navegación.
    if re.search(r'<h2\b[^>]*>(?:(?!</h2>).)*?<div\b', t, re.I | re.S):
        add("media", r, "a11y",
            "Un <div> de bloque está anidado dentro de un <h2> (HTML inválido); el lector de "
            "pantalla anuncia todo el contenido como texto del encabezado",
            "Cerrar el </h2> tras el texto del encabezado y mover el <div> a elemento hermano")

    # --- 4d. <section class="related-articles"> duplicada en la misma página (media, seo)
    #     caso 20260619: la plantilla de blog dejó 2 secciones idénticas de "Artículos Relacionados".
    if len(re.findall(r'<section\b[^>]*class=["\'][^"\']*related-articles[^"\']*["\']', t, re.I)) > 1:
        add("media", r, "seo",
            "Sección <section class=\"related-articles\"> duplicada (aparece más de una vez) en la "
            "misma página: contenido y encabezado repetidos",
            "Dejar una sola sección de artículos relacionados; eliminar la duplicada")

    # --- 4e. <header class="article-header" aria-hidden="true"> oculta fecha/lectura al lector (media, a11y)
    #     caso bk-64bed7fd / a11y-501..502 (20260623): la plantilla de blog marcó TODO el header
    #     como aria-hidden, ocultando <time> y tiempo de lectura. Solo el título redundante interior
    #     (.article-title-hidden) debe ir oculto.
    if r.startswith("blog/") and re.search(
            r'<header\b[^>]*class=["\'][^"\']*article-header[^"\']*["\'][^>]*aria-hidden=["\']true["\']',
            t, re.I):
        add("media", r, "a11y",
            "<header class=\"article-header\"> con aria-hidden=\"true\" oculta la fecha de "
            "publicación y el tiempo de lectura al lector de pantalla",
            "Quitar aria-hidden del <header>; si hay un título redundante, ocultar solo el "
            "<div class=\"article-title-hidden\" aria-hidden=\"true\"> interior")

    # --- 4f. blog/colonia indexable sin metas de plantilla og:locale/og:site_name/twitter:url (baja, seo)
    #     caso bk-546d0a06 (20260623): posts de blog omitían metas que las páginas de servicio sí traen.
    #     caso twitter-url-colonias-20260627: 24 páginas de colonia carecían de twitter:url/title/desc/img.
    is_blog_or_colonia = r.startswith("blog/") or r.startswith("servicios/plomero-colonias-culiacan/")
    if is_blog_or_colonia and not noindex:
        faltan_og = [m for m in ("og:locale", "og:site_name") if m not in t]
        faltan_tw = [m for m in ("twitter:url", "twitter:title", "twitter:description", "twitter:image") if m not in t]
        faltan = faltan_og + faltan_tw
        if faltan:
            add("baja", r, "seo",
                "Página indexable sin metas de plantilla: falta %s" % ", ".join(faltan),
                "Añadir og:locale=es_MX, og:site_name=\"Plomero Culiacán Pro\" y twitter:url/title/desc/image "
                "(= canonical/og equivalentes) como en las páginas de servicio")

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

    # --- 12. marca/color: hex AZUL/MORADO/ROJO off-brand prohibidos (seo)
    # La marca del sitio es NARANJA (--brand:#E36414, --brand-light:#F97316, --brand-dark:#C2410C)
    # + neutros slate (#475569, #64748b, #1e293b…) + verde WhatsApp. El blog (y restos en
    # servicios) traía CAJAS azules/moradas/rojas hardcodeadas inline que hacían verse esas
    # páginas DISTINTAS de la home (la home es la fuente de verdad: 0 azul/rojo decorativo).
    # Denylist EXPLÍCITA (no hue automático: los neutros slate son levemente azulados y darían
    # falsos positivos; los colores del logo de Google van en <path fill> y son legítimos).
    # Casos color-blog-20260619 / color-blog-20260620. Si aparece un tono nuevo, añádelo aquí.
    OFFBRAND_HEX = (
        # azul / morado
        "#0066cc", "#0284c7", "#0369a1", "#667eea", "#764ba2", "#004499", "#0c4a6e",
        "#0f4fa8", "#1e40af", "#e0f2fe", "#f0f9ff", "#0ea5e9", "#075985", "#1a5276",
        "#1a73e8", "#bae6fd", "#e8f4fd", "#f0f8ff", "#2c3e50",
        # rojo (NO confundir con naranja de marca; #ea4335 es del logo de Google y NO va aquí)
        "#dc2626", "#dc3545", "#b91c1c", "#991b1b", "#fef2f2",
        # verde decorativo de cajas "tip" (NO el verde de marca/disponibilidad #22c55e,
        # NI WhatsApp #25d366, NI el logo de Google #34a853 — esos son legítimos)
        "#059669", "#166534", "#16a34a", "#28a745", "#10b981", "#dcfce7", "#f0fdf4", "#ecfdf5",
    )
    offb = {h: len(re.findall(h, t, re.I)) for h in OFFBRAND_HEX}
    offb = {h: n for h, n in offb.items() if n}
    # 12b. mismas familias off-brand pero en forma rgb()/rgba(): un mismo color puede
    # escribirse como hex O como rgb. Caso real color-form-rgba-20260620: el azul #0066cc
    # reapareció como rgba(0, 102, 204, .1) en el box-shadow de foco de 5 formularios de
    # servicio y la denylist HEX no lo cazó. Para cada hex de la denylist, buscar también su
    # triplete rgb (tolerante a espacios). Mismo conjunto de colores -> sin FP nuevos.
    def _hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    for h in OFFBRAND_HEX:
        r_, g_, b_ = _hex_to_rgb(h)
        n = len(re.findall(r"rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\b" % (r_, g_, b_), t, re.I))
        if n:
            k = "rgb(%d,%d,%d)" % (r_, g_, b_)
            offb[k] = offb.get(k, 0) + n
    if offb:
        detalle = ", ".join("%s×%d" % (h, n) for h, n in offb.items())
        add("media", r, "seo",
            "Color off-brand (azul/morado/rojo) en la página: %s — la marca es NARANJA como la home" % detalle,
            "Reemplazar por la paleta de marca: texto/acentos #C2410C o #E36414, fondos claros #FFF7ED. "
            "No tocar el logo de Google (#4285f4/#ea4335 van en <path fill> de SVG).")

    # --- 13. colonia: badge ETA contradice el cuerpo / meta truncada (media, contenido)
    #     caso fix-colonia-eta 20260626: el hero-eta-badge ("Llegamos en NN-NN min a X")
    #     mostraba un ETA distinto al del cuerpo (meta + benefit-h3 + cobertura). Solo se marca
    #     cuando las 3 fuentes del cuerpo COINCIDEN y el badge difiere (deriva, no inventa: el
    #     cuerpo manda). También: meta description truncada a mitad de palabra antes de "· Llegada".
    if "plomero-colonias-culiacan/" in r and r.count("/") >= 3:
        def _eta(pat):
            m = re.search(pat, t)
            return m.group(1) if m else None
        meta_eta = _eta(r'<meta name="description" content="[^"]*?([0-9]{2}-[0-9]{2}) min')
        badge = re.search(r'hero-eta-badge[^>]*>(?:<[^>]+>)*\s*<span>Llegamos en ([0-9]{2}-[0-9]{2}) min a ', t)
        benefit = _eta(r'<h3>Llegada (?:en|R[aá]pida)[^<]*?([0-9]{2}-[0-9]{2}) min') or _eta(r'Llegada R[aá]pida</h3><p>([0-9]{2}-[0-9]{2}) min')
        cob = _eta(r'Cobertura.*?Llegamos en ([0-9]{2}-[0-9]{2}) min')
        body = [v for v in (meta_eta, benefit, cob) if v]
        if badge and len(body) == 3 and len(set(body)) == 1 and badge.group(1) != body[0]:
            add("media", r, "contenido",
                "El badge de llegada del hero dice %s min pero el cuerpo (meta+beneficio+cobertura) dice %s min" % (badge.group(1), body[0]),
                "Igualar el ETA del hero-eta-badge al del cuerpo (el cuerpo manda: deriva, no inventes). "
                "Auto: python3 .pipeline/fix-colonia-eta.py --apply")
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if m and ' · Llegada' in m.group(1):
            head = m.group(1).split(' · Llegada')[0].rstrip()
            last = head.split(' ')[-1] if head else ''
            if re.fullmatch(r'[a-záéíóúñ]{1,3},?', last) or head.endswith(','):
                add("media", r, "contenido",
                    "Meta description truncada a mitad de cláusula antes de '· Llegada' (termina en '%s')" % last,
                    "Recortar el fragmento colgante al último borde de cláusula completo. "
                    "Auto: python3 .pipeline/fix-colonia-eta.py --apply")

    # --- 14. ancla cuyo TEXTO nombra un servicio real pero el HREF apunta a otro destino
    #     (regresion vista 3x: "Instalacion de sanitarios" -> hub generico /servicios/ en vez
    #     de /servicios/instalacion-de-sanitarios/). No es un 404 (el hub existe) asi que el
    #     check 1 no lo caza; aqui se compara el TEXTO de la ancla contra el H1 real de cada
    #     pagina de servicio.
    smap = _service_name_map()
    for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', t, re.I):
        href, text = m.group(1), m.group(2)
        text_norm = re.sub(r'\s+', ' ', text).strip().lower()
        text_norm = re.sub(r'\s+en\s+culiac[aá]n.*$', '', text_norm)
        expected = smap.get(text_norm)
        if not expected:
            continue
        disk, url_path = resolve_to_disk(href, page_dir)
        if url_path is None:
            continue
        url_norm = _norm_url_path(url_path)
        if url_norm != expected:
            add("media", r, "links",
                "Ancla dice '%s' (nombre real de un servicio) pero enlaza a %s en vez de %s" % (text.strip(), href, expected),
                "Corregir el href para que apunte a la pagina real del servicio que el texto nombra.")


# ================================================================ CHECK global: paridad CSS
# PARIDAD TOTAL (no solo firmas): el sitio sirve DOS hojas distintas
#   - styles.<hash>.css  -> la sirven la home (index.html) + las paginas de colonia
#   - styles.min.css     -> la sirve el resto del sitio
# y styles.css es la FUENTE. Las tres DEBEN tener las mismas reglas; si una se queda
# atras, esas paginas renderizan distinto (caso real 20260619: logo movil 100px vs 62px,
# animacion hero fadeInUp vs slideInUp, .hero .hero-image ausente). El checker viejo solo
# comparaba 3 firmas hardcodeadas y dejaba pasar el resto.
#
# Se descompone cada styles*.css en ATOMOS (selector individual + bloque de declaraciones
# normalizado, con su contexto @media) y se reporta todo atomo presente en alguna hoja pero
# ausente en otra. Ignora diferencias de minificacion (espacios) y de agrupacion de
# selectores -> sin falsos positivos. (Logica espejo de .pipeline/check-css-paridad.py.)
def _css_norm_sel(s):
    # conserva el combinador descendiente (' '), que es semantico
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s*([>+~,])\s*", r"\1", s)


def _css_norm_decls(body):
    b = re.sub(r"\s+", " ", body).strip()
    b = re.sub(r"\s*([;:,])\s*", r"\1", b)
    return ";".join(sorted(d.strip() for d in b.split(";") if d.strip()))


def _css_split_rules(css):
    rules, depth, prelude, buf, prelude_s = [], 0, [], [], ""
    for ch in css:
        if ch == "{":
            if depth == 0:
                prelude_s, prelude, depth = "".join(prelude), [], 1
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


def _css_style_atoms(prelude, body, ctx=""):
    decls = _css_norm_decls(body)
    return ["%s%s{%s}" % (ctx, sel, decls)
            for sel in _css_norm_sel(prelude).split(",") if sel]


def _css_atoms(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for prelude, body in _css_split_rules(css):
        p = _css_norm_sel(prelude)
        head = p.split("(")[0].lower()
        if head.startswith("@media") or head.startswith("@supports"):
            ctx = re.sub(r"\s+", "", p) + "||"
            for ip, ib in _css_split_rules(body):
                out.update(_css_style_atoms(ip, ib, ctx))
        elif p.startswith("@"):
            out.add(re.sub(r"\s+", "", p) + "{" + re.sub(r"\s+", "", body) + "}")
        else:
            out.update(_css_style_atoms(prelude, body))
    return out


def check_css_parity():
    css_files = sorted(glob.glob(os.path.join(ROOT, "styles*.css")))
    if len(css_files) < 2:
        return  # nada que comparar
    A = {c: _css_atoms(read(c)) for c in css_files}
    union = set().union(*A.values())
    for atom in sorted(union):
        tienen = [c for c in css_files if atom in A[c]]
        if len(tienen) == len(css_files):
            continue
        nombres = ", ".join(sorted(os.path.basename(c) for c in tienen))
        for c in css_files:
            if atom not in A[c]:
                add("media", rel(c), "movil",
                    "Paridad CSS rota: la regla '%s' existe en %s pero falta aquí" % (atom, nombres),
                    "Copiar la regla a este archivo para mantener los 3 CSS en paridad total "
                    "(styles.css fuente + styles.min.css + styles.<hash>.css servido). "
                    "Si tras corregir cambia el render, versionar ?v= y subir CACHE_NAME en sw.js.")


# ================================================================ CHECK global: aggregateRating
# aggregateRating debe ser el MISMO en todo el sitio para el mismo LocalBusiness (mismo
# negocio real) -- caso real 20260709: emergencia-24-7 traia ratingValue 4.7/reviewCount 120
# mientras 14 paginas mas traian 4.8/150 para el MISMO negocio. Usa el valor MAYORITARIO
# como verdad (deriva, no inventes) -- solo dispara si hay una mayoria clara (>=50%).
def check_rating_consistency():
    from collections import Counter
    valores = {}
    for fpath in collect_pages():
        try:
            t = read(fpath)
        except Exception:
            continue
        mr = re.search(r'"ratingValue"\s*:\s*"([0-9.]+)"', t)
        mc = re.search(r'"reviewCount"\s*:\s*"([0-9]+)"', t)
        if mr and mc:
            valores[fpath] = (mr.group(1), mc.group(1))
    if len(valores) < 3:
        return
    counts = Counter(valores.values())
    mayoria, n = counts.most_common(1)[0]
    if n < len(valores) * 0.5:
        return  # sin mayoria clara, no hay "verdad" derivable
    for fpath, val in valores.items():
        if val != mayoria:
            add("media", rel(fpath), "seo",
                "aggregateRating %s/%s difiere del valor mayoritario del sitio %s/%s para el mismo negocio (LocalBusiness)" % (val[0], val[1], mayoria[0], mayoria[1]),
                "Unificar al valor mayoritario ya existente (deriva, no inventes) salvo que el dueño confirme un cambio real de rating.")


# ================================================================ MAIN
def main():
    redirects = load_redirects()
    for fpath in collect_pages():
        t = read(fpath)
        if is_stub(t):
            continue  # stub de redireccion (meta-refresh): no es pagina de contenido
        check_page(fpath, t, has_noindex(t), redirects)
    check_css_parity()
    check_rating_consistency()

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
