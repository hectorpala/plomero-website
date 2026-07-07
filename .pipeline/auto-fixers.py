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
TAP_SELECTORS = [".breadcrumb-item a"]


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
    """Sube el token `styles*.css?v=…` a `version` en TODAS las páginas HTML.
    Esto es OBLIGATORIO al cambiar un CSS: se sirve con `immutable` (max-age 1 año), así que
    un visitante que regresa solo re-pide el CSS si CAMBIA la URL (el ?v=). Reemplazo literal
    del token → seguro (no toca estructura). Devuelve (páginas tocadas, fallos de escritura).
    El patrón acepta 8-12 dígitos: dos cambios de CSS el mismo día necesitan token con hora
    (AAAAMMDDHHMM), si no el segundo bump repetiría la URL y no rompería el cache."""
    n_files, fallos = 0, 0
    htmls = sorted(set(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)))
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
    un selector embebido en un grupo (`.x,.sel{...}`) para no alterar declaraciones compartidas."""
    n = 0
    for sel in TAP_SELECTORS:
        pat = re.compile(r"(^|\})(" + re.escape(sel) + r")\{([^}]*)\}", re.M)
        m = pat.search(css)
        if not m:
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
