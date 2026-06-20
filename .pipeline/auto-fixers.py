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

Salida: qué arregló (o arreglaría) por página. Exit 0 siempre.
"""
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

def _det_color(h):
    low = h.lower()
    return any(c in low for c in _COLOR_OFFBRAND)

def _fix_color(h):
    n = 0
    for c in _COLOR_LIGHT_BG:
        h, k = re.subn(re.escape(c), "#FFF7ED", h, flags=re.I); n += k
    for c in _COLOR_ACCENT:
        h, k = re.subn(re.escape(c), "#C2410C", h, flags=re.I); n += k
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
    for fid, desc, riesgo, _, _ in FIXERS:
        print("  • %-12s %s" % (fid, desc))
    print("\nLo que NO vive aquí (reestructuras/negocio/precios/borrar): ver .pipeline/CALIDAD-Y-VERDAD.md")


def cmd_run(args):
    apply = "--apply" in args
    solo = args[args.index("--solo") + 1] if "--solo" in args else None
    paths = [a for a in args if not a.startswith("--") and a != solo]
    if not paths:
        paths = paginas_default()
    fixers = [f for f in FIXERS if (solo is None or f[0] == solo)]

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
