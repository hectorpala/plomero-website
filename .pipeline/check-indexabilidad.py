#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de indexabilidad para plomeroculiacanpro.mx.
Solo lee disco + parsea archivos locales (sin red externa). Levanta UN servidor
estatico local efimero en 127.0.0.1 solo para confirmar el codigo HTTP 200/404.

Emite a stdout SOLO el JSON comun de hallazgos:
  {"hallazgos":[{"id":"idx-001","archivo":"ruta","linea":0,
                 "severidad":"alta|media|baja","categoria":"indexabilidad",
                 "descripcion":"...","fix_sugerido":"..."}]}

Tres chequeos (ver REGLAS.md / TAREA):
  1. SITEMAP vs REALIDAD: cada <loc> debe existir en disco (y dar 200 local),
     no estar 301 en _redirects/netlify.toml, canonical apuntando a SI MISMA,
     sin noindex. Y al reves: .html indexables del repo que NO esten en el sitemap.
  2. CANONICAL == og:url == ultimo item BreadcrumbList == WebPage @id;
     y las paginas /servicios/ deben tener breadcrumb de 3 niveles (pos 1,2,3).
  3. DUPLICADOS: colision de <title> o meta description entre >=2 paginas (NO auto).
"""
import os, re, json, sys, html, threading, socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz del repo
BASE = "https://plomeroculiacanpro.mx"
SITEMAP = os.path.join(ROOT, "sitemaps", "main_sitemap.xml")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "idx-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "indexabilidad",
        "descripcion": desc, "fix_sugerido": fix,
    })

def rel(p):
    return os.path.relpath(p, ROOT)

# ---------------------------------------------------------------- mapeo URL->archivo
def url_to_path(loc):
    """Devuelve la ruta de archivo en disco que Netlify serviria para esta loc."""
    path = loc[len(BASE):] if loc.startswith(BASE) else loc
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return os.path.join(ROOT, "index.html")
    rels = path.strip("/")
    if path.endswith("/"):
        return os.path.join(ROOT, rels, "index.html")
    if path.endswith(".html"):
        return os.path.join(ROOT, rels)
    # sin slash ni extension: probar dir/index.html luego .html
    cand = os.path.join(ROOT, rels, "index.html")
    if os.path.isfile(cand):
        return cand
    return os.path.join(ROOT, rels + ".html")

# ---------------------------------------------------------------- redirects
def load_redirects():
    """Lista de (prefijo, es_prefijo, status) de _redirects y netlify.toml."""
    rules = []
    rp = os.path.join(ROOT, "_redirects")
    if os.path.isfile(rp):
        with open(rp, encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                parts = s.split()
                if len(parts) < 2:
                    continue
                frm = parts[0]
                status = "301"
                if parts[-1].isdigit():
                    status = parts[-1]
                rules.append(_mk_rule(frm, status))
    nt = os.path.join(ROOT, "netlify.toml")
    if os.path.isfile(nt):
        txt = open(nt, encoding="utf-8", errors="replace").read()
        for blk in re.split(r"\[\[redirects\]\]", txt)[1:]:
            mf = re.search(r'from\s*=\s*"([^"]+)"', blk)
            ms = re.search(r'status\s*=\s*(\d+)', blk)
            if mf:
                rules.append(_mk_rule(mf.group(1), ms.group(1) if ms else "301"))
    return rules

def _mk_rule(frm, status):
    if frm.endswith("/*"):
        return (frm[:-1], True, status)   # prefijo: "/foo/*" -> "/foo/"
    if frm.endswith("*"):
        return (frm[:-1], True, status)
    return (frm, False, status)

def redirect_status(path, rules):
    """Devuelve status de redirect que aplicaria si NO hubiera archivo estatico."""
    for pref, is_prefix, status in rules:
        if is_prefix:
            if path.startswith(pref):
                return status
        elif path == pref:
            return status
    return None

# ---------------------------------------------------------------- parse HTML
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

def get_og_url(t):
    m = re.search(r'<meta[^>]*(?:property|name)=["\']og:url["\'][^>]*>', t, re.I)
    if not m:
        # orden inverso: content antes de property
        m = re.search(r'<meta[^>]*content=["\'][^"\']*["\'][^>]*property=["\']og:url["\'][^>]*>', t, re.I)
    if not m:
        return None
    c = re.search(r'content=["\']([^"\']+)["\']', m.group(0), re.I)
    return c.group(1).strip() if c else None

def has_noindex(t):
    for m in re.finditer(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*>', t, re.I):
        c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
        if c and "noindex" in c.group(1).lower():
            return True
    return False

def get_title(t):
    m = re.search(r'<title>(.*?)</title>', t, re.I | re.S)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1)).strip()) if m else None

def get_meta_desc(t):
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*>', t, re.I)
    if not m:
        return None
    c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
    return html.unescape(re.sub(r'\s+', ' ', c.group(1)).strip()) if c else None

def _walk(node, found):
    """Recolecta nodos por @type dentro de cualquier estructura JSON-LD."""
    if isinstance(node, dict):
        ty = node.get("@type")
        types = ty if isinstance(ty, list) else [ty]
        if "BreadcrumbList" in types:
            found.setdefault("breadcrumbs", []).append(node)
        if "WebPage" in types and node.get("@id"):
            found.setdefault("webpage_ids", []).append(node["@id"])
        # mainEntityOfPage suele traer el WebPage @id
        mep = node.get("mainEntityOfPage")
        if isinstance(mep, dict) and mep.get("@id"):
            found.setdefault("webpage_ids", []).append(mep["@id"])
        for v in node.values():
            _walk(v, found)
    elif isinstance(node, list):
        for v in node:
            _walk(v, found)

def parse_jsonld(t):
    found = {}
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                         t, re.I | re.S):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except Exception:
            continue
        _walk(data, found)
    return found

def breadcrumb_info(found):
    """(ultimo_item, set_de_posiciones, {posicion: item}) consolidando todos los BreadcrumbList."""
    last_item = None
    last_pos = -1
    positions = set()
    pos_items = {}
    for bc in found.get("breadcrumbs", []):
        items = bc.get("itemListElement") or []
        for it in items:
            if not isinstance(it, dict):
                continue
            try:
                pos = int(it.get("position"))
            except (TypeError, ValueError):
                continue
            positions.add(pos)
            target = it.get("item")
            if isinstance(target, dict):
                target = target.get("@id") or target.get("url")
            if target:
                pos_items.setdefault(pos, target.strip())
            if pos > last_pos and target:
                last_pos = pos
                last_item = target.strip()
    return last_item, positions, pos_items

# ---------------------------------------------------------------- servidor local
class _QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a, **k):   # sin logs de acceso a stderr
        pass

def start_server():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    httpd = HTTPServer(("127.0.0.1", port), _QuietHandler)
    th = threading.Thread(target=httpd.serve_forever, daemon=True); th.start()
    return httpd, port

def http_code(port, loc):
    path = loc[len(BASE):] if loc.startswith(BASE) else loc
    if not path:
        path = "/"
    try:
        r = urlopen("http://127.0.0.1:%d%s" % (port, path), timeout=5)
        code = r.getcode()
        r.read(); r.close()   # consumir el cuerpo para no dejar el socket a medias (BrokenPipe)
        return code
    except HTTPError as e:
        try: e.read()
        except Exception: pass
        return e.code
    except (URLError, OSError):
        return None

# ================================================================ MAIN
def main():
    if not os.path.isfile(SITEMAP):
        print(json.dumps({"hallazgos": [], "error": "no se encontro main_sitemap.xml"}))
        return
    sm = read(SITEMAP)
    locs = re.findall(r'<loc>\s*([^<]+?)\s*</loc>', sm)
    loc_set = set(locs)
    rules = load_redirects()

    httpd, port = start_server()
    try:
        # ---- CHECK 1 + 2: por cada loc del sitemap
        for loc in locs:
            fpath = url_to_path(loc)
            r = rel(fpath)
            url_path = loc[len(BASE):] if loc.startswith(BASE) else loc
            if not url_path:
                url_path = "/"

            exists = os.path.isfile(fpath)
            red = redirect_status(url_path, rules)

            # 1a/1b: existencia + redirect (Netlify: archivo estatico gana al redirect no forzado)
            if not exists:
                if red and red.startswith("3"):
                    add("alta", r,
                        "Sitemap lista %s pero NO existe archivo en disco y un redirect %s aplica (_redirects/netlify.toml)" % (loc, red),
                        "Quitar la <url> de sitemaps/main_sitemap.xml (la URL redirige %s; un sitemap no debe listar URLs redirigidas)" % red)
                else:
                    add("alta", r,
                        "Sitemap lista %s pero NO existe archivo en disco (404)" % loc,
                        "Quitar la <url> de sitemaps/main_sitemap.xml (404) o restaurar el archivo si debe existir")
                continue  # sin archivo no hay nada mas que validar

            # confirmacion HTTP local (no autoritativa; el disco manda)
            code = http_code(port, loc)
            if code is not None and code != 200 and not (300 <= code < 400):
                add("alta", r,
                    "Sitemap lista %s; el archivo existe pero el servidor local devolvio HTTP %s" % (loc, code),
                    "Revisar por que %s no responde 200 en local (permiso/index faltante)" % r)

            t = read(fpath)

            # 1d: noindex en pagina del sitemap
            if has_noindex(t):
                add("alta", r,
                    "%s esta en el sitemap pero tiene noindex (contradiccion: noindex + sitemap)" % loc,
                    "Quitar la <url> del sitemap O quitar el noindex de la pagina (decidir cual corresponde)")

            canonical = get_canonical(t)
            # 1c / 2: canonical apunta a SI MISMA (== su propia loc)
            if not canonical:
                add("alta", r, "%s no tiene <link rel=canonical>" % loc,
                    "Anadir <link rel=\"canonical\" href=\"%s\"> en el <head>" % loc)
            elif canonical != loc:
                add("alta", r,
                    "canonical de %s apunta a OTRA URL (%s), no a si misma" % (loc, canonical),
                    "Corregir canonical a %s" % loc)

            # 2: og:url == canonical (referencia seo-201..207, seo-ogurl-6serv)
            ref = canonical or loc
            og = get_og_url(t)
            if og is not None and og != ref:
                add("alta", r,
                    "og:url (%s) != canonical (%s) en %s" % (og, ref, loc),
                    "Corregir <meta property=\"og:url\"> a %s" % ref)
            elif og is None:
                add("media", r,
                    "%s (indexable) no emite <meta property=\"og:url\">; inconsistente con el estándar (las hermanas sí lo tienen). Ausente != incorrecto, pero deja la página sin la señal" % loc,
                    "Añadir <meta property=\"og:url\" content=\"%s\"> junto al resto de etiquetas og en el <head>" % ref)

            # 2: BreadcrumbList ultimo item == canonical + 3 niveles en /servicios/ (seo-301..303)
            found = parse_jsonld(t)
            last_item, positions, pos_items = breadcrumb_info(found)
            if last_item is not None and last_item != ref:
                add("alta", r,
                    "ultimo item del BreadcrumbList (%s) != canonical (%s) en %s" % (last_item, ref, loc),
                    "Corregir el ultimo itemListElement del BreadcrumbList para que 'item' == %s" % ref)
            es_servicio = url_path.startswith("/servicios/") and url_path != "/servicios/"
            if es_servicio and last_item is not None and not {1, 2, 3}.issubset(positions):
                add("alta", r,
                    "pagina de servicio %s sin breadcrumb de 3 niveles (posiciones presentes: %s)" % (loc, sorted(positions)),
                    "Reconstruir BreadcrumbList con 3 niveles: Inicio(1)->/ , Servicios(2)->/servicios/ , [Pagina](3)->%s" % ref)
            # 2b: ningun nivel intermedio del breadcrumb debe apuntar a una ancla de la home (BASE/#...),
            # debe ser un hub indexable real (p.ej. /servicios/). Caso /#servicios (seo-201..304).
            for p, target in sorted(pos_items.items()):
                if p == 1:
                    continue
                if target == last_item:
                    continue  # el ultimo item ya se valida contra canonical arriba
                if target.startswith(BASE + "/#"):
                    add("media", r,
                        "BreadcrumbList posicion %d (%s) apunta a una ancla de la home en vez de un hub indexable real, en %s" % (p, target, loc),
                        "Corregir el item de la posicion %d a un hub real (p.ej. %s/servicios/)" % (p, BASE))

            # 2: WebPage @id == canonical (si existe)
            for wid in found.get("webpage_ids", []):
                if wid and wid != ref:
                    add("media", r,
                        "WebPage/mainEntityOfPage @id (%s) != canonical (%s) en %s" % (wid, ref, loc),
                        "Alinear el @id del WebPage/mainEntityOfPage a %s" % ref)
                    break

        # ---- CHECK 1 (reverso): .html indexables del repo que NO estan en el sitemap
        # NOTA (2026-07-09): NO agregar "/obsidian-vault/" — está TRACKEADO y SERVIDO en
        # producción (ver check-plantilla.py para el detalle). Bloqueado vía _redirects/robots.txt.
        SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
                     "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
                     "/mcp-local-seo/", "/scripts/", "/graphify-plomero/")
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
                canonical = get_canonical(t)
                title = get_title(t)
                if not canonical or not title:
                    continue  # sin canonical/title no es una pagina indexable formal
                if has_noindex(t):
                    continue  # noindex: correctamente fuera del sitemap
                if canonical not in loc_set:
                    add("alta", rel(fpath),
                        "Pagina indexable (index,follow, canonical=%s) NO esta en main_sitemap.xml" % canonical,
                        "Anadir <url><loc>%s</loc>... al sitemap, o ponerle noindex si no debe indexarse" % canonical)

        # ---- CHECK 3: duplicados de title / meta description (NO auto-arreglar)
        titles = {}
        descs = {}
        for loc in locs:
            fpath = url_to_path(loc)
            if not os.path.isfile(fpath):
                continue
            t = read(fpath)
            ti = get_title(t)
            de = get_meta_desc(t)
            if ti:
                titles.setdefault(ti, []).append(loc)
            if de:
                descs.setdefault(de, []).append(loc)
        for ti, urls in titles.items():
            if len(urls) >= 2:
                add("media", "sitemaps/main_sitemap.xml",
                    "TITLE duplicado en %d paginas: %r -> %s" % (len(urls), ti[:80], ", ".join(urls)),
                    "PENDIENTE HUMANO (no auto): diferenciar el <title> de cada pagina; requiere criterio editorial")
        for de, urls in descs.items():
            if len(urls) >= 2:
                add("media", "sitemaps/main_sitemap.xml",
                    "META DESCRIPTION duplicada en %d paginas: %r -> %s" % (len(urls), de[:80], ", ".join(urls)),
                    "PENDIENTE HUMANO (no auto): diferenciar la meta description de cada pagina; requiere criterio editorial")
    finally:
        httpd.shutdown()

    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
