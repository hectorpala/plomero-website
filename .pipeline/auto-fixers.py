#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""auto-fixers.py — REGISTRO de arreglos MECÁNICOS conocidos (la apuesta del 90%).

Filosofía: detectar ya lo hacen los check-*.py; lo que faltaba es APLICAR el fix en vez de
diferirlo. Cada fixer es una receta ESTRECHA y determinista (NO "que el LLM arregle lo que sea"):
detecta un patrón conocido → aplica el fix exacto. Lo MECÁNICO se drena sin límite; lo grande
(reestructuras, claims de negocio, precios, borrar páginas) NO vive aquí — ver CALIDAD-Y-VERDAD.md.

Cada fixer respeta el SCOPE: p.ej. og:url solo en páginas INDEXABLES (una noindex no lo necesita).

Uso:
  python3 .pipeline/auto-fixers.py list                      # lista los fixers
  python3 .pipeline/auto-fixers.py run                       # DRY-RUN sobre todo el sitio (no escribe)
  python3 .pipeline/auto-fixers.py run --apply               # aplica y escribe
  python3 .pipeline/auto-fixers.py run --solo og-url [paths] # un fixer / rutas concretas

Salida: qué arregló (o arreglaría) por página. Exit 0 salvo bump de cache-busting
incompleto (exit 1: estado inconsistente que NO debe publicarse).
"""
import datetime
import glob
import html as _html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def es_noindex(h):
    return bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', h, re.I))


def canonical_de(h):
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', h, re.I)
    return m.group(1) if m else None


# ── Cada fixer: (id, descripcion, riesgo, detecta(h)->bool, arregla(h)->(h, n)) ──

def _det_ogurl(h):
    return (not es_noindex(h)) and canonical_de(h) and 'property="og:url"' not in h and "property='og:url'" not in h

def _fix_ogurl(h):
    can = canonical_de(h)
    # inserta el og:url justo después de la línea del canonical, con su misma sangría
    def repl(m):
        return m.group(0) + "\n" + m.group(1) + '<meta property="og:url" content="%s">' % can
    nuevo, n = re.subn(r'(^[ \t]*)<link[^>]+rel=["\']canonical["\'][^>]*>', repl, h, count=1, flags=re.I | re.M)
    return nuevo, n


def _det_theme(h):
    return '#0066cc' in h and 'name="theme-color"' in h

def _fix_theme(h):
    return re.subn(r'(name=["\']theme-color["\'][^>]*content=["\'])#0066cc', r'\g<1>#F97316', h, flags=re.I)


# Añade theme-color de marca a páginas INDEXABLES que no lo tengan (scope: indexables).
def _det_theme_add(h):
    return (not es_noindex(h)) and canonical_de(h) and not re.search(r'<meta[^>]+name=["\']theme-color["\']', h, re.I)

def _fix_theme_add(h):
    return re.subn(r'</head>', '<meta name="theme-color" content="#F97316"></head>', h, count=1, flags=re.I)


def _det_email(h):
    return 'info@plomeropro.com' in h

def _fix_email(h):
    return (h.replace('info@plomeropro.com', 'info@plomeroculiacanpro.mx'),
            h.count('info@plomeropro.com'))


_ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'

def _det_robots(h):
    # página indexable (tiene canonical, no es noindex) que NO emite <meta name="robots">
    return (not es_noindex(h)) and canonical_de(h) and not re.search(r'<meta[^>]+name=["\']robots["\']', h, re.I)

def _fix_robots(h):
    # inserta el robots estándar justo ANTES de la línea del canonical, con su misma sangría
    def repl(m):
        return m.group(1) + _ROBOTS + "\n" + m.group(0)
    return re.subn(r'(^[ \t]*)<link[^>]+rel=["\']canonical["\'][^>]*>', repl, h, count=1, flags=re.I | re.M)


# ── color off-brand → paleta de marca (NARANJA). Auto-sana el azul/morado/rojo/verde
#    decorativo que se cuela en el HTML inline (blog/servicios). CONSERVA los legítimos:
#    #22c55e (disponibilidad), #25d366 (WhatsApp), #34a853/#4285f4/#ea4335/#fbbc05 (logo
#    Google), grises slate (#475569…). Espejo del check 12 de check-plantilla.py. ──
_COLOR_LIGHT_BG = ("#e0f2fe", "#f0f9ff", "#bae6fd", "#e8f4fd", "#f0f8ff",
                   "#fef2f2", "#dcfce7", "#f0fdf4", "#ecfdf5")          # fondos claros → tinte naranja
_COLOR_ACCENT = ("#0066cc", "#0284c7", "#0369a1", "#667eea", "#764ba2", "#004499",
                 "#0c4a6e", "#0f4fa8", "#1e40af", "#0ea5e9", "#075985", "#1a5276",
                 "#1a73e8", "#2c3e50", "#dc2626", "#dc3545", "#b91c1c", "#991b1b",
                 "#059669", "#166534", "#16a34a", "#28a745", "#10b981")  # texto/acento → marca oscura
_COLOR_OFFBRAND = _COLOR_LIGHT_BG + _COLOR_ACCENT

def _sin_svg(h):
    """Quita los bloques <svg>…</svg> (para detectar sin tocar arte vectorial)."""
    return re.sub(r"<svg\b.*?</svg>", " ", h, flags=re.S | re.I)

def _det_color(h):
    low = _sin_svg(h).lower()
    return any(c in low for c in _COLOR_OFFBRAND)

def _fix_color(h):
    # PROTEGER los <svg>: el reemplazo global ciego podía repintar un fill legítimo
    # dentro de arte vectorial (p.ej. #1a73e8 en un ícono de Google) — se apartan los
    # bloques svg, se sanan los colores del resto, y se restauran intactos.
    n = 0
    svgs = []
    def _stash(m):
        svgs.append(m.group(0))
        return "\x00SVG%d\x00" % (len(svgs) - 1)
    h = re.sub(r"<svg\b.*?</svg>", _stash, h, flags=re.S | re.I)
    for c in _COLOR_LIGHT_BG:
        h, k = re.subn(re.escape(c), "#FFF7ED", h, flags=re.I); n += k
    for c in _COLOR_ACCENT:
        h, k = re.subn(re.escape(c), "#C2410C", h, flags=re.I); n += k
    h = re.sub(r"\x00SVG(\d+)\x00", lambda m: svgs[int(m.group(1))], h)
    return h, n


# ── denylist de (selector, color prohibido) ya reincidente (check 19 de check-plantilla.py /
#    check_denylist_color_css). El SENSOR existia desde 2026-07-18 pero nunca se porto el
#    SANADOR: cada corrida detectaba la regresion y un LLM la arreglaba a mano -- por eso el
#    color del breadcrumb reincidio 4 veces (07-09/13/14/16). Esto la cura sola.
#    La lista se IMPORTA de check-plantilla.py: una sola fuente de verdad, cero divergencia
#    sensor-fixer (si divergieran, el fixer "arreglaria" a un valor que el checker rechaza).
#    Misma funcion sirve para el <style> inline de una pagina Y para el CSS compartido: el
#    patron ancla en "selector{...color:bad" y no le importa si eso vive en HTML o en un .css.
def _cargar_denylist_color():
    try:
        import importlib.util
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check-plantilla.py")
        spec = importlib.util.spec_from_file_location("check_plantilla_af", ruta)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)          # seguro: el modulo tiene guard __main__
        return tuple((sel, bad, good) for sel, bad, good, _ev in mod.DENYLIST_COLOR)
    except Exception as e:
        # FAIL-SAFE: sin lista, el fixer no detecta nada y no toca nada. El checker sigue
        # marcando el hallazgo, asi que se degrada a "no auto-fix", NUNCA a "fix equivocado".
        print("aviso: no pude leer DENYLIST_COLOR de check-plantilla.py (%s); "
              "el fixer denylist-color queda inactivo esta corrida." % e, file=sys.stderr)
        return ()

_DENYLIST_COLOR = _cargar_denylist_color()

def _det_denylist_color(h):
    return any(
        re.search(re.escape(sel) + r'\s*\{[^}]*?\bcolor\s*:\s*' + re.escape(bad) + r'\b', h, re.I)
        for sel, bad, good in _DENYLIST_COLOR)

def _fix_denylist_color(h):
    n = 0
    for sel, bad, good in _DENYLIST_COLOR:
        pat = re.compile(r'(' + re.escape(sel) + r'\s*\{[^}]*?\bcolor\s*:\s*)' + re.escape(bad) + r'\b', re.I)
        h, k = pat.subn(r'\g<1>' + good, h)
        n += k
    return h, n


# ── FAQ visible ↔ FAQPage JSON-LD. Google exige que el marcado refleje literalmente el
#    contenido que puede leer el usuario. Cuando se amplía o reescribe el acordeón visible,
#    sincroniza sus preguntas Y respuestas en vez de dejar un schema viejo. Se limita a
#    `.faq-item` con encabezado + párrafo: si el markup no es inequívoco, no toca nada.
def _texto_visible_faq(fragmento):
    texto = re.sub(r'<[^>]+>', ' ', fragmento)
    return re.sub(r'\s+', ' ', _html.unescape(texto)).strip()


def _faq_items_visibles(h):
    items = []
    for m in re.finditer(
            r'<div\b[^>]*class=["\'][^"\']*\bfaq-item\b[^"\']*["\'][^>]*>(.*?)</div>',
            h, re.S | re.I):
        bloque = m.group(1)
        mq = re.search(r'<(?:h[2-6]|summary|dt)\b[^>]*>(.*?)</(?:h[2-6]|summary|dt)>',
                       bloque, re.S | re.I)
        ma = re.search(r'<(?:p|dd)\b[^>]*>(.*?)</(?:p|dd)>', bloque, re.S | re.I)
        if not (mq and ma):
            return []  # fail-safe: un acordeón ambiguo no se reescribe a medias
        pregunta = _texto_visible_faq(mq.group(1))
        respuesta = _texto_visible_faq(ma.group(1))
        if not pregunta or not respuesta:
            return []
        items.append({
            "@type": "Question",
            "name": pregunta,
            "acceptedAnswer": {"@type": "Answer", "text": respuesta},
        })
    return items


def _fin_array_json(s, inicio):
    """Devuelve el offset posterior al `]` que abre en inicio, respetando strings JSON."""
    nivel, en_string, escape = 0, False, False
    for i in range(inicio, len(s)):
        c = s[i]
        if en_string:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                en_string = False
            continue
        if c == '"':
            en_string = True
        elif c == '[':
            nivel += 1
        elif c == ']':
            nivel -= 1
            if nivel == 0:
                return i + 1
    return None


def _fix_faq_visible(h):
    visibles = _faq_items_visibles(h)
    if not visibles:
        return h, 0
    nuevo_array = json.dumps(visibles, ensure_ascii=False, separators=(',', ':'))
    cambios = 0

    def sincroniza_script(m):
        nonlocal cambios
        contenido = m.group(2)
        tipo = re.search(r'"@type"\s*:\s*"FAQPage"', contenido)
        if not tipo:
            return m.group(0)
        entidad = re.search(r'"mainEntity"\s*:\s*\[', contenido[tipo.end():])
        if not entidad:
            return m.group(0)
        ini = tipo.end() + entidad.end() - 1
        fin = _fin_array_json(contenido, ini)
        if fin is None:
            return m.group(0)
        try:
            actuales = json.loads(contenido[ini:fin])
        except Exception:
            return m.group(0)
        if actuales == visibles:
            return m.group(0)
        cambios += 1
        contenido = contenido[:ini] + nuevo_array + contenido[fin:]
        return m.group(1) + contenido + m.group(3)

    patron = re.compile(
        r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
        re.S | re.I)
    return patron.sub(sincroniza_script, h), cambios


def _det_faq_visible(h):
    return _fix_faq_visible(h)[1] > 0


# ── ancla cuyo TEXTO nombra un servicio real pero el HREF apunta a otro destino (regresion
#    vista 3x: 2026-07-07/08/09, mecanizada como check 14 de check-plantilla.py pero sin
#    fixer -> aqui se APLICA el mismo mapeo texto-ancla -> ruta canonica del servicio). ──
_SERVICE_NAME_MAP_CACHE = None

def _service_name_map_af():
    global _SERVICE_NAME_MAP_CACHE
    if _SERVICE_NAME_MAP_CACHE is not None:
        return _SERVICE_NAME_MAP_CACHE
    m = {}
    for fpath in sorted(glob.glob(os.path.join(ROOT, "servicios", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(fpath))
        if slug == "plomero-colonias-culiacan":
            continue
        try:
            txt = open(fpath, encoding="utf-8").read()
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
    _SERVICE_NAME_MAP_CACHE = m
    return m

def _norm_url_path_af(p):
    if not p:
        return p
    if p.endswith("index.html"):
        p = p[: -len("index.html")]
    if not p.endswith("/"):
        p += "/"
    return p

def _resolve_href_af(href, page_dir):
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
        return None
    path = href.split("#")[0].split("?")[0]
    if not path:
        return None
    if path.startswith("/"):
        return path
    # relativo -> normaliza contra el directorio de la pagina, luego a ruta "/"-absoluta
    abs_disk = os.path.normpath(os.path.join(page_dir, path))
    rel_root = os.path.relpath(abs_disk, ROOT).replace(os.sep, "/")
    return "/" + rel_root

# El detector/fix real necesita el directorio de la pagina (para resolver hrefs relativos),
# que el contrato (id, desc, riesgo, detecta(h), arregla(h)) de FIXERS no pasa -> se resuelve
# con un caso especial en cmd_run() (busca fid == "ancla-servicio") en vez de forzar la firma.
def _scan_and_fix_ancla(t, fpath):
    """Aplica el fixer ancla-vs-servicio sobre texto YA leído de fpath (necesita su directorio
    para resolver hrefs relativos). Sustituye por SPAN exacto de cada <a>, nunca por valor de
    href a secas -> evita el bug 2026-07-10 donde dos anclas distintas compartían el mismo href
    (p.ej. el nav-link "Servicios" -> /servicios/ Y la ancla rota "Instalación de sanitarios"
    -> /servicios/ en la MISMA página) y el reemplazo por href tocaba la ancla equivocada."""
    smap = _service_name_map_af()
    page_dir = os.path.dirname(fpath)
    out, last, n = [], 0, 0
    for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', t, re.I):
        href, text = m.group(1), m.group(2)
        text_norm = re.sub(r'\s+', ' ', text).strip().lower()
        text_norm = re.sub(r'\s+en\s+culiac[aá]n.*$', '', text_norm)
        expected = smap.get(text_norm)
        if not expected:
            continue
        url_path = _resolve_href_af(href, page_dir)
        if url_path is None or _norm_url_path_af(url_path) == expected:
            continue
        out.append(t[last:m.start(1)])
        out.append(expected)
        last = m.end(1)
        n += 1
    out.append(t[last:])
    return ("".join(out) if n else t), n


def _scan_and_fix_img_ratio(t, fpath):
    """width/height declarados con un ratio distinto al del archivo REAL -> los pone reales
    (check 22 de check-plantilla.py). Necesita el directorio de la pagina para resolver src
    relativos, por eso no cabe en la firma normal de FIXERS.

    Sustituye por SPAN EXACTO de cada atributo (como _scan_and_fix_ancla): una misma pagina
    puede traer DOS <img> del mismo logo con valores distintos -- el caso real del 2026-07-26,
    donde el nav y el footer diferian y un reemplazo por valor habria tocado el equivocado.
    Reescribe SOLO width/height: el tamano renderizado lo manda el CSS, estos atributos solo
    declaran la FORMA, asi que corregirlos no cambia como se ve la pagina."""
    dims = _dims_imagen_af()
    if dims is None:
        return t, 0
    page_dir = os.path.dirname(fpath)
    edits, n = [], 0
    for m in re.finditer(r'<img\b[^>]*>', t, re.I):
        tag = m.group(0)
        msrc = re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        mw = re.search(r'\bwidth\s*=\s*["\'](\d+)["\']', tag, re.I)
        mh = re.search(r'\bheight\s*=\s*["\'](\d+)["\']', tag, re.I)
        if not (msrc and mw and mh):
            continue
        w, h = int(mw.group(1)), int(mh.group(1))
        if not w or not h:
            continue
        src = msrc.group(1)
        if src.startswith(("http://", "https://", "data:", "//")):
            continue
        disk = os.path.normpath(os.path.join(ROOT if src.startswith("/") else page_dir,
                                             src.lstrip("/").split("?")[0]))
        if not os.path.isfile(disk):
            continue          # inexistente: es hallazgo del check 1, no de este fixer
        real = dims(disk)
        if not real:
            continue
        rw, rh = real
        if abs(w / h - rw / rh) / (rw / rh) <= 0.02:
            continue
        # offsets absolutos dentro del documento, para sustituir sin tocar nada mas
        edits.append((m.start() + mw.start(1), m.start() + mw.end(1), str(rw)))
        edits.append((m.start() + mh.start(1), m.start() + mh.end(1), str(rh)))
        n += 1
    if not n:
        return t, 0
    out, last = [], 0
    for ini, fin, val in sorted(edits):
        out.append(t[last:ini]); out.append(val); last = fin
    out.append(t[last:])
    return "".join(out), n


_DIMS_FN_CACHE = []

def _dims_imagen_af():
    """Reusa el lector de dimensiones de check-plantilla.py (misma fuente de verdad que el
    check 22: si divergieran, el fixer 'arreglaria' a un valor que el checker rechaza).
    Si no se puede importar, el fixer se desactiva en vez de adivinar."""
    if _DIMS_FN_CACHE:
        return _DIMS_FN_CACHE[0]
    try:
        import importlib.util
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check-plantilla.py")
        spec = importlib.util.spec_from_file_location("check_plantilla_dims", ruta)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _DIMS_FN_CACHE.append(mod.dims_imagen)
    except Exception as e:
        print("aviso: no pude cargar dims_imagen de check-plantilla.py (%s); "
              "el fixer img-ratio-real queda inactivo esta corrida." % e, file=sys.stderr)
        _DIMS_FN_CACHE.append(None)
    return _DIMS_FN_CACHE[0]


FIXERS = [
    ("og-url", "og:url faltante en página indexable → copia el canonical (scope: solo indexables)",
     "mecanico", _det_ogurl, _fix_ogurl),
    ("theme-color", "theme-color placeholder #0066cc → color de marca #F97316",
     "mecanico", _det_theme, _fix_theme),
    ("theme-color-add", "página indexable sin theme-color → añade el de marca #F97316 (scope: indexables)",
     "mecanico", _det_theme_add, _fix_theme_add),
    ("color-off-brand", "color off-brand (azul/morado/rojo/verde decorativo) → paleta de marca naranja; conserva #22c55e/WhatsApp/Google",
     "mecanico", _det_color, _fix_color),
    ("email", "email contaminado info@plomeropro.com → info@plomeroculiacanpro.mx",
     "mecanico", _det_email, _fix_email),
    ("meta-robots", "página indexable sin <meta name=robots> → añade el estándar index,follow (scope: indexables)",
     "mecanico", _det_robots, _fix_robots),
    ("ancla-servicio", "ancla cuyo TEXTO nombra un servicio real pero el HREF apunta a otro destino → corrige al href canónico (regresión 3x, check 14 de check-plantilla.py)",
     "mecanico", None, None),  # caso especial en cmd_run(): necesita page_dir para resolver hrefs relativos
    ("denylist-color-inline", "color de la denylist (.breadcrumb-item a #E36414, .breadcrumb-item.active #6c757d) duplicado en el <style> inline de la página → valor AA-safe (regresión 4x, check 19 de check-plantilla.py)",
     "mecanico", _det_denylist_color, _fix_denylist_color),
    ("faq-visible", "FAQPage JSON-LD desfasado → copia literalmente preguntas y respuestas de cada .faq-item visible (check 21 de check-plantilla.py)",
     "mecanico", _det_faq_visible, _fix_faq_visible),
    ("img-ratio-real", "width/height de un <img> con ratio distinto al del archivo real (CLS) → dimensiones reales; el CSS sigue mandando el tamaño (check 22 de check-plantilla.py)",
     "mecanico", None, None),  # caso especial en cmd_run(): necesita page_dir para resolver src relativos
]


# ──────────────────── ASSET FIXERS (CSS/JS COMPARTIDO, no por página) ────────────────────
# Operan UNA vez sobre los assets compartidos (los 3 CSS). Cuando tocan CSS, el flujo completo
# de cache-busting es OBLIGATORIO: bump del token ?v= en TODAS las páginas (el CSS se sirve
# `immutable` 1 año — sin cambiar la URL, los visitantes que regresan no re-piden el CSS) +
# bump de CACHE_NAME en sw.js (para los clientes con service worker). Ver REGLAS.md (CACHÉ).
# Riesgo mecánico → auto, sin límite.
CSS_FILES = ["styles.css", "styles.min.css", "styles.7f293647.css"]
SW_FILE = "sw.js"

# Selectores interactivos que DEBEN ser tap-target ≥44px en móvil. Ampliar esta lista cuando
# un revisor a11y encuentre uno nuevo (así se MECANIZA el fix — FASE 9 del Auto Agente).
TAP_SELECTORS = [".breadcrumb-item a", ".footer-bottom a", ".article-content a", ".card h3 a"]


def _bump_sw():
    """Sube CACHE_NAME 'plomero-culiacan-vN' → vN+1 en sw.js (cache-busting de 1 archivo)."""
    p = os.path.join(ROOT, SW_FILE)
    try:
        s = open(p, encoding="utf-8").read()
    except Exception:
        return 0
    def repl(m):
        return "%s%d%s" % (m.group(1), int(m.group(2)) + 1, m.group(3))
    nuevo, n = re.subn(r"(CACHE_NAME\s*=\s*['\"]plomero-culiacan-v)(\d+)(['\"])", repl, s, count=1)
    if n:
        open(p, "w", encoding="utf-8").write(nuevo)
    return n


def _bump_css_version_html(version):
    """Sube el token `styles*.css?v=…` a `version` en TODAS las páginas HTML **y en el
    precache de sw.js** (lleva la URL ?v= hardcodeada — sin alinearla, el SW nuevo
    precacheaba el CSS viejo aunque CACHE_NAME subiera; hallazgo del port al electricista).
    Esto es OBLIGATORIO al cambiar un CSS: se sirve con `immutable` (max-age 1 año), así que
    un visitante que regresa solo re-pide el CSS si CAMBIA la URL (el ?v=). Reemplazo literal
    del token → seguro (no toca estructura). Devuelve (páginas tocadas, fallos de escritura).
    El patrón acepta 8-12 dígitos: dos cambios de CSS el mismo día necesitan token con hora
    (AAAAMMDDHHMM), si no el segundo bump repetiría la URL y no rompería el cache."""
    n_files, fallos = 0, 0
    htmls = sorted(set(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)))
    htmls.append(os.path.join(ROOT, SW_FILE))
    for p in htmls:
        if "/node_modules/" in p or "/.git/" in p:
            continue
        try:
            s = open(p, encoding="utf-8").read()
        except Exception:
            continue
        s2, k = re.subn(r'(styles[\w.]*\.css\?v=)\d{8,12}', r'\g<1>' + version, s)
        if k and s2 != s:
            try:
                open(p, "w", encoding="utf-8").write(s2)
                n_files += 1
            except Exception:
                # Antes un fallo de ESCRITURA abortaba el barrido a medias sin aviso:
                # unas páginas bumpeadas y otras no.
                fallos += 1
    return n_files, fallos


# Estado del cache-busting: hash del contenido de los 3 CSS registrado DESPUÉS del último
# bump exitoso. Si al arrancar el hash actual difiere del registrado, un cambio de CSS quedó
# SIN bump (p.ej. el fixer murió entre escribir el CSS y bumpear) → se repara aquí mismo.
BUMP_STATE = os.path.join(ROOT, ".pipeline", "css-bump-state.json")

def _css_hash():
    import hashlib
    hh = hashlib.sha256()
    for css_name in CSS_FILES:
        try:
            hh.update(open(os.path.join(ROOT, css_name), "rb").read())
        except Exception:
            hh.update(b"(ausente)")
    return hh.hexdigest()

def _token_version():
    """Token ?v= nuevo: fecha (AAAAMMDD); si las páginas YA traen el de hoy, fecha+hora
    (AAAAMMDDHHMM) para que el segundo cambio del día también rompa el cache."""
    hoy = datetime.date.today().strftime("%Y%m%d")
    try:
        home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        if re.search(r'styles[\w.]*\.css\?v=' + hoy + r'(?!\d)', home):
            return datetime.datetime.now().strftime("%Y%m%d%H%M")
    except Exception:
        pass
    return hoy

def _do_full_bump(motivo):
    """Bump completo (?v= en páginas + sw.js) y registro del estado. Devuelve True si OK."""
    version = _token_version()
    np, nf = _bump_css_version_html(version)
    print("  ✅ ?v=%s bumpeado en %d página(s)%s [%s]" % (
        version, np, (" · ⚠️ %d fallo(s) de escritura" % nf) if nf else "", motivo))
    nb = _bump_sw()
    print("  ✅ %s → CACHE_NAME +1" % SW_FILE if nb else "  ⚠️  no pude bumpear %s" % SW_FILE)
    ok = (nf == 0 and nb > 0)
    if ok:
        import json as _json
        try:
            open(BUMP_STATE, "w", encoding="utf-8").write(
                _json.dumps({"css_sha256": _css_hash(), "token": version,
                             "fecha": datetime.datetime.now().isoformat(timespec="seconds")}) + "\n")
        except Exception:
            print("  ⚠️  no pude escribir %s (el auto-reparo del próximo run re-bumpeará)" % BUMP_STATE)
    return ok


def _fix_tap_target(css):
    """Garantiza min-height:44px + inline-flex centrado en cada TAP_SELECTORS. Idempotente:
    si la regla ya cumple, 0 cambios. Solo toca reglas STANDALONE (inicio o tras `}`), nunca
    un selector embebido en un grupo (`.x,.sel{...}`) para no alterar declaraciones compartidas.
    Si el selector NO existe todavía en la hoja, AÑADE una regla nueva al final (mismo patrón
    que las reglas de tap-target existentes) en vez de quedarse callado."""
    n = 0
    for sel in TAP_SELECTORS:
        pat = re.compile(r"(^|\})(" + re.escape(sel) + r")\{([^}]*)\}", re.M)
        m = pat.search(css)
        if not m:
            css = css.rstrip() + "\n" + sel + "{display:inline-flex;align-items:center;min-height:44px}\n"
            n += 1
            continue
        decl = m.group(3)
        if "min-height:44px" in decl.replace(" ", ""):
            continue  # ya cumple → no tocar
        nuevo = decl
        if "display:inline-flex" not in nuevo.replace(" ", ""):
            nuevo = re.sub(r"display:\s*inline-block", "display:inline-flex;align-items:center", nuevo)
            if "display:inline-flex" not in nuevo.replace(" ", ""):
                nuevo = "display:inline-flex;align-items:center;" + nuevo
        nuevo = "min-height:44px;" + nuevo
        css = css[:m.start()] + m.group(1) + sel + "{" + nuevo + "}" + css[m.end():]
        n += 1
    return css, n


# (id, descripcion, riesgo, arregla(css)->(css, n))
ASSET_FIXERS = [
    ("tap-target-44",
     "tap target <44px en selectores interactivos compartidos (migas) → min-height:44px en los 3 CSS + bump sw.js",
     "mecanico", _fix_tap_target),
    ("denylist-color-css",
     "color de la denylist (.breadcrumb-item a, .breadcrumb-item.active) en las 3 hojas compartidas → valor AA-safe + bump sw.js",
     "mecanico", _fix_denylist_color),
]


def cmd_run_assets(apply, solo=None):
    """Corre los ASSET_FIXERS sobre los 3 CSS; si alguno toca CSS y se aplica, corre el bump
    completo. AUTO-REPARO previo: si el hash actual de los CSS difiere del registrado tras el
    último bump (fixer muerto a medias en una corrida anterior), se re-bumpea aunque hoy no
    haya nada que arreglar — sin esto, un CSS cambiado sin bump quedaba invisible PARA SIEMPRE
    (URL immutable cacheada 1 año y ningún checker lo vigila). Devuelve (total, bump_fallido)."""
    fixers = [f for f in ASSET_FIXERS if (solo is None or f[0] == solo)]
    if not fixers:
        return 0, False
    bump_fallido = False

    # Auto-reparo del estado de bump (solo con --apply; el dry-run solo avisa).
    import json as _json
    try:
        estado = _json.loads(open(BUMP_STATE, encoding="utf-8").read())
    except Exception:
        estado = None
    if estado and estado.get("css_sha256") and estado["css_sha256"] != _css_hash():
        if apply:
            print("ASSET fixers: ⚠️ los CSS cambiaron SIN bump registrado (corrida anterior muerta a medias) → re-bump:")
            if not _do_full_bump("auto-reparo"):
                bump_fallido = True
        else:
            print("ASSET fixers: ⚠️ los CSS difieren del último bump registrado — con --apply se auto-repara (re-bump).")

    total, css_tocado, lineas = 0, False, []
    for fid, _, _, fix in fixers:
        for css_name in CSS_FILES:
            p = os.path.join(ROOT, css_name)
            try:
                s = open(p, encoding="utf-8").read()
            except Exception:
                continue
            s2, n = fix(s)
            if n:
                total += n
                css_tocado = True
                if apply:
                    open(p, "w", encoding="utf-8").write(s2)
                lineas.append("  %s %s → %s×%d%s" % (
                    "✅" if apply else "○", css_name, fid, n, "" if apply else " (dry-run)"))
    if lineas:
        print("ASSET fixers (CSS compartido):")
        for ln in lineas:
            print(ln)
        if css_tocado and apply:
            if not _do_full_bump("fix aplicado"):
                bump_fallido = True
        elif css_tocado:
            print("  (con --apply: bumpea ?v= en las páginas + sw.js — necesario por el cache immutable)")
    elif apply and estado is None:
        # Primer run con el estado nuevo: registrar la línea base sin bumpear nada.
        try:
            open(BUMP_STATE, "w", encoding="utf-8").write(
                _json.dumps({"css_sha256": _css_hash(), "token": "(baseline)",
                             "fecha": datetime.datetime.now().isoformat(timespec="seconds")}) + "\n")
            print("ASSET fixers: línea base de bump registrada (%s)." % os.path.relpath(BUMP_STATE, ROOT))
        except Exception:
            pass
    return total, bump_fallido


def paginas_default():
    pats = [
        "index.html",
        "*/index.html",                                      # secciones top-level (contacto, precios, blog…)
        "servicios/*/index.html",
        "servicios/plomero-colonias-culiacan/*/index.html",
        "blog/*/index.html",
    ]
    out = []
    for p in pats:
        out += glob.glob(os.path.join(ROOT, p))
    return sorted(set(out))


def cmd_list():
    print("Auto-fixers registrados (todos riesgo MECÁNICO → auto, sin límite):")
    print(" PÁGINA (HTML, por archivo):")
    for fid, desc, riesgo, _, _ in FIXERS:
        print("  • %-14s %s" % (fid, desc))
    print(" ASSET (CSS/JS compartido, una vez + bump sw.js):")
    for fid, desc, riesgo, _ in ASSET_FIXERS:
        print("  • %-14s %s" % (fid, desc))
    print("\nBorrar archivos huérfanos: .pipeline/limpiar-huerfanos.py (no vive aquí: es borrado, no edición).")
    print("Lo que NO se mecaniza (reestructuras/negocio/precios): ver .pipeline/CALIDAD-Y-VERDAD.md")


def cmd_run(args):
    apply = "--apply" in args
    solo = args[args.index("--solo") + 1] if "--solo" in args else None
    paths = [a for a in args if not a.startswith("--") and a != solo]
    full_run = not paths   # sin rutas explícitas → barrido de todo el sitio
    if not paths:
        paths = paginas_default()
    fixers = [f for f in FIXERS if (solo is None or f[0] == solo)]
    asset_ids = {f[0] for f in ASSET_FIXERS}

    total = 0
    for p in paths:
        try:
            h = open(p, encoding="utf-8").read()
        except Exception:
            continue
        orig = h
        aplicados = []
        for fid, _, _, det, fix in fixers:
            if fid == "ancla-servicio":
                h2, n = _scan_and_fix_ancla(h, p)
                if n:
                    h = h2
                    aplicados.append("%s×%d" % (fid, n))
                continue
            if fid == "img-ratio-real":
                h2, n = _scan_and_fix_img_ratio(h, p)
                if n:
                    h = h2
                    aplicados.append("%s×%d" % (fid, n))
                continue
            if det(h):
                h2, n = fix(h)
                if n:
                    h = h2
                    aplicados.append("%s×%d" % (fid, n))
        if aplicados:
            total += 1
            rel = os.path.relpath(p, ROOT)
            if apply and h != orig:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h)
                print("  ✅ %s → %s" % (rel, ", ".join(aplicados)))
            else:
                print("  ○ %s → %s (dry-run)" % (rel, ", ".join(aplicados)))

    print("")
    if total == 0:
        print("✅ Nada que arreglar: el sitio ya está limpio para estos fixers.")
    else:
        print("%s %d página(s) con fix mecánico%s." % (
            "✅ Arregladas" if apply else "○ Arreglaría", total, "" if apply else " (corre con --apply)"))

    # ASSET fixers (CSS compartido): en barrido completo, o si --solo nombra uno de asset.
    if full_run or (solo in asset_ids):
        _, bump_fallido = cmd_run_assets(apply, solo=solo if solo in asset_ids else None)
        if bump_fallido:
            # Exit ≠ 0: un CSS cambiado sin bump completo es un estado inconsistente que
            # el orquestador DEBE ver (antes solo se imprimía un ⚠️ y exit 0).
            print("❌ bump de cache-busting INCOMPLETO — revisar antes de publicar.")
            sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "run":
        cmd_run(sys.argv[2:])
    else:
        print("comando desconocido: %s" % cmd); sys.exit(2)


if __name__ == "__main__":
    main()
