#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diferenciar-colonia.py — Promueve una página de colonia de noindex (doorway)
a indexable, dándole contenido ÚNICO real para que NO sea doorway.

Hace 4 cosas sobre servicios/plomero-colonias-culiacan/<slug>/index.html:
  1) flip  <meta robots noindex> -> index, follow
  2) reemplaza la meta description de plantilla por una ÚNICA de esa colonia
  3) inyecta la sección "Plomería en <Colonia>: lo que debes saber"
     (3 párrafos propios + "Problemas de plomería comunes" + "Servicios más solicitados")
  4) arregla el item 3 del BreadcrumbList (le pone su URL propia)

USO:
    python3 scripts/diferenciar-colonia.py spec.json
    python3 scripts/diferenciar-colonia.py --ejemplo > spec.json

NOTA (estado actual del sitio de plomería, 2026-06): TODAS las colonias de
plomero-colonias-culiacan ya están diferenciadas e indexables (0 noindex). Esta
herramienta queda como utilidad para FUTURAS colonias que se agreguen como
noindex doorway y luego se quieran promover con demanda real. Por eso no se
ha podido smoke-testear contra una colonia noindex (no existe ninguna hoy).

DESPUÉS (recordatorio al final):
    1) agregar al sitemap (priority 0.6)  →  scripts/crecer.py colonia spec.json lo hace
    2) candado:  python3 .pipeline/gate-pagina.py servicios/plomero-colonias-culiacan/<slug>/index.html
       (el anti-doorway DEBE quedar Jaccard < 0.80 vs hermanas; si no, hazla más única)
    3) rama + merge + push

REGLAS (ver REGLAS.md): el contenido de cada colonia debe ser genuinamente distinto
(zona real, tipo de casas, necesidades de plomería propias). NO inventes geografía falsa.
Solo diferencia colonias con demanda; NO promuevas cientos de doorways de golpe.
"""
import json, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLONIAS_DIR = "servicios/plomero-colonias-culiacan"
BASEURL = "https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/"

EJEMPLO = {
  "slug": "nombre-colonia",
  "nombre": "Nombre Colonia",
  "meta": "Plomero en Nombre Colonia, Culiacán: <servicios clave de esa colonia>. Servicio 24/7, llegada 30-60 min.",
  "p1": "Qué ES la colonia: zona (norte/sur/oriente/poniente/centro), tipo de casas/época, carácter (popular/residencial/campestre). REAL y específico.",
  "p2": "Qué se pide MÁS ahí (según el tipo de casa: tinacos por baja presión, drenajes con raíces, fugas en casas viejas) y el ETA. Específico de la colonia.",
  "p3": "Un ángulo extra ÚNICO (un problema típico de esa zona, una recomendación, una referencia local segura). NO reciclar p1.",
  "problemas": ["Problema de plomería típico 1", "Problema 2", "Problema 3", "Problema 4"],
  "servicios": ["Servicio 1", "Servicio 2", "Servicio 3", "Servicio 4"]
}


def seccion(nom, p1, p2, p3, probs, servs):
    pli = "".join("<li>%s</li>" % html.escape(x) for x in probs)
    sli = "".join("<li>%s</li>" % html.escape(x) for x in servs)
    return ('<section class="section">\n  <div class="container">\n'
            '    <h2>Plomería en %s: lo que debes saber</h2>\n'
            '    <p>%s</p>\n    <p>%s</p>\n    <p>%s</p>\n'
            '    <h3>Problemas de plomería comunes en %s</h3>\n    <ul class="servicios-zona">%s</ul>\n'
            '    <h3>Servicios más solicitados en %s</h3>\n    <ul class="servicios-zona">%s</ul>\n'
            '  </div>\n</section>\n\n'
            % (html.escape(nom), html.escape(p1), html.escape(p2), html.escape(p3),
               html.escape(nom), pli, html.escape(nom), sli))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    if sys.argv[1] == "--ejemplo":
        print(json.dumps(EJEMPLO, ensure_ascii=False, indent=2)); sys.exit(0)
    z = json.load(open(sys.argv[1], encoding="utf-8"))
    slug = z["slug"]
    f = os.path.join(ROOT, COLONIAS_DIR, slug, "index.html")
    if not os.path.isfile(f):
        sys.exit("❌ no existe la colonia: %s" % slug)
    h = open(f, encoding="utf-8").read()
    if "lo que debes saber" in h:
        sys.exit("⚠️ ya diferenciada (tiene 'lo que debes saber'): %s" % slug)

    # 1) robots noindex -> index
    h2 = h.replace('<meta name="robots" content="noindex, follow">',
                   '<meta name="robots" content="index, follow">', 1)
    if h2 == h:
        sys.exit("❌ no se encontró <meta robots noindex> en %s (¿ya es indexable?)" % slug)
    h = h2
    # 2) meta description única. La plantilla de colonia de plomero abre con
    #    "Plomero en <Colonia>, Culiacán ...". Reemplazo con FUNCIÓN para insertar el
    #    texto LITERAL (un '\1'/'\g<>' en la meta no se interpreta como backreference).
    desc_re = re.compile(r'(<meta name="description" content=")[^"]*(">)')
    n_meta = len(desc_re.findall(h))
    if n_meta < 1:
        sys.exit("❌ no encontré <meta name=\"description\"> en %s" % slug)
    h = desc_re.sub(lambda m: m.group(1) + html.escape(z["meta"]) + m.group(2), h, count=1)
    # 3) inyectar sección única antes del bloque final-cta
    fc = h.find('class="final-cta"')
    if fc < 0:
        sys.exit("❌ no se encontró el bloque final-cta en %s" % slug)
    ss = h.rfind('<section', 0, fc)
    h = h[:ss] + seccion(z["nombre"], z["p1"], z["p2"], z["p3"], z["problemas"], z["servicios"]) + h[ss:]
    # 4) breadcrumb item 3 con URL propia (si aún no la tiene). Reemplazo con FUNCIÓN
    #    para insertar el slug LITERAL (un '\1'/'\g<>' en el slug no se interpreta).
    #    Regex con \s* entre tokens y VERIFICACIÓN de match: con JSON-LD compacto (sin
    #    espacios) el patrón rígido no calzaba y el script reportaba éxito sin tocar el
    #    breadcrumb (no-op silencioso, clase documentada en REGLAS.md 2026-06-12).
    bc_re = re.compile(r'(\{\s*"@type":\s*"ListItem",\s*"position":\s*3,\s*"name":\s*"[^"]*")\s*\}')
    if '"position": 3' in h or '"position":3' in h:
        h2 = bc_re.sub(lambda m: m.group(1) + ', "item": "%s%s/"}' % (BASEURL, slug), h, count=1)
        if h2 == h and ('"item"' not in h.split('"position"')[-1][:200]):
            sys.exit("❌ breadcrumb item 3 existe pero el patrón no calzó (¿JSON-LD con formato inesperado?) — reviso a mano, no publico a medias")
        h = h2

    open(f, "w", encoding="utf-8").write(h)
    print("✅ %s diferenciada e indexable (meta única + sección + breadcrumb)" % slug)
    print("\nSIGUIENTE:")
    print("  1) python3 scripts/crecer.py colonia %s   (sitemap + candado, revierte si falla)" % sys.argv[1])
    print("     (anti-doorway Jaccard < 0.80 vs hermanas; si no, hazla más única)")


if __name__ == "__main__":
    main()
