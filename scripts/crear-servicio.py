#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crear-servicio.py — Genera una página de SERVICIO de PLOMERÍA nueva, con paridad
de plantilla garantizada y contenido único (anti-doorway).

Reusa un esqueleto estándar (`servicios/plomero-zona-oriente-culiacan/index.html`)
y delega la sustitución estructural en `.pipeline/gen-landing.py` (que aborta si algo
no calza o si hay fuga "electricista" de la plantilla origen).

A diferencia del generador del electricista (páginas muy uniformes con ~25 anclas),
las páginas de plomero son PROSA ÚNICA por página. Por eso este generador es más
robusto: hace 3 cosas grandes y predecibles en vez de 25 frágiles:
  1) REGENERA el bloque JSON-LD completo (WebSite + LocalBusiness + Service + FAQPage
     + BreadcrumbList) desde el spec.
  2) REEMPLAZA todo el CUERPO visible (de </header> a <footer>) por la prosa única
     del spec (campo `cuerpo_html`) — esto es lo que vence al anti-doorway.
  3) RETARGUETEA head + hero: slug, title, metas, og/twitter, canonical, h1,
     subtítulo del hero, alt del hero y el nombre del breadcrumb.

USO:
    python3 scripts/crear-servicio.py spec.json
    python3 scripts/crear-servicio.py --ejemplo > spec.json   # plantilla de spec

DESPUÉS de generar (lo hace solo si usas el orquestador):
    python3 scripts/crecer.py servicio spec.json
    → crea la página + sitemap + enlace entrante en la home + bump sw + CANDADO,
      y si el candado falla, REVIERTE y deja el árbol limpio.
"""
import json, os, sys, subprocess, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = "servicios/plomero-zona-oriente-culiacan/index.html"
SITE = "https://plomeroculiacanpro.mx"

# Valores ÚNICOS del esqueleto que se retarguetean (deben calzar EXACTO; si el
# esqueleto cambia, gen-landing aborta y avisa qué ancla no calzó).
SK_SLUG   = "plomero-zona-oriente-culiacan"
SK_TITLE  = "Plomero Zona Oriente de Culiacán | La Campiña · 24/7"
SK_DESC   = "Plomero en la zona oriente de Culiacán: La Campiña, Las Coloradas, Díaz Ordaz y El Barrio. Tinacos, cisternas, fugas y drenajes 24/7. Tel 667 392 2273."
SK_KW     = "plomero zona oriente culiacán, plomero la campiña, plomero las coloradas, plomero díaz ordaz, plomero el barrio culiacan, plomero oriente culiacan, fontanero zona oriente culiacan, plomero salida a sanalona, plomero salida a imala"
SK_OGD    = "Plomero a domicilio en el oriente de Culiacán: La Campiña, El Barrio, Díaz Ordaz y Las Coloradas. Tinacos, cisternas, fugas y drenajes con garantía escrita."
SK_TWD    = "Plomero en La Campiña, El Barrio, Díaz Ordaz y Las Coloradas. Tinacos, cisternas y drenajes 24/7."
SK_H1     = "Plomero en la Zona Oriente de Culiacán"
SK_HSUB   = "Atendemos La Campiña, El Barrio, Díaz Ordaz, Las Coloradas y todas las colonias rumbo a la salida a Sanalona e Imala. Tinacos, cisternas, fugas y drenajes con garantía escrita, 24/7."
SK_HALT   = "Plomero en la Zona Oriente de Culiacán — Plomero Culiacán Pro"
SK_BCNAME = "Plomero Zona Oriente"


EJEMPLO = {
  "slug": "instalacion-de-calentadores-solares",
  "title": "Instalación de Calentadores Solares en Culiacán | 24/7",
  "desc": "Meta description ≤160 car. que vende y refleja la página. Incluye 'Culiacán' y un beneficio claro.",
  "kw": "keyword1 culiacan, keyword2, keyword3",
  "ogt": "Título Open Graph del Servicio",
  "ogd": "Descripción OG corta y vendedora (puede diferir de la meta).",
  "twd": "Descripción Twitter corta.",
  "h1": "H1 de la página (lo que promete)",
  "hsub": "Subtítulo del hero: el dolor del cliente + qué resolvemos + 24/7.",
  "halt": "Alt del hero: describe la foto + ' — Plomero Culiacán Pro'.",
  "bc": "Nombre Corto (breadcrumb activo)",
  "wa": "Hola,%20necesito%20cotizar%20la%20instalación%20de%20un%20calentador%20solar",
  "svct": "Tipo de servicio (schema serviceType)",
  "svcn": "Nombre completo del servicio en Culiacán",
  "svcd": "Descripción larga del servicio para el JSON-LD (1-2 frases).",
  "area": ["Las Quintas, Culiacán", "Tres Ríos, Culiacán", "Centro, Culiacán"],
  "lowprice": "500", "highprice": "8000", "offercount": "4",
  "faqs": [
    ["¿Pregunta real pre-llamada 1?", "Respuesta concreta, sin evasivas."],
    ["¿Pregunta 2?", "Respuesta."],
    ["¿Atienden de urgencia 24/7?", "Sí, ..."]
  ],
  "cuerpo_html": (
    "    <section class=\"section section-alt\">\n"
    "        <div class=\"container\">\n"
    "            <h2>Sección 1 con prosa ÚNICA de este servicio</h2>\n"
    "            <p class=\"about-text\">Párrafo único y verídico, específico de este servicio en Culiacán...</p>\n"
    "        </div>\n"
    "    </section>\n"
    "    <!-- ... agrega TODAS las secciones del cuerpo (servicios, precios, FAQ visible, CTA,\n"
    "         sobre nosotros, contacto). Debe ser prosa ÚNICA: el candado anti-doorway exige\n"
    "         Jaccard < 0.80 vs las páginas hermanas. Usa la estructura del esqueleto como guía. -->\n"
  )
}


def _js(s): return json.dumps(s, ensure_ascii=False)


def build_jsonld(z):
    url = "%s/servicios/%s/" % (SITE, z["slug"])
    area = ",".join('{"@type":"Place","name":%s}' % _js(a) for a in z["area"])
    faqs = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (_js(q), _js(a))
        for q, a in z["faqs"])
    g = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@graph":['
        '{"@type":"WebSite","@id":"%(site)s/#website","url":"%(site)s/","name":"Plomero Culiacán Pro",'
        '"description":"Servicio profesional de plomería en Culiacán, Sinaloa","publisher":{"@id":"%(site)s/#organization"}},'
        '{"@type":"LocalBusiness","@id":"%(site)s/#organization","name":"Plomero Culiacán Pro",'
        '"image":"%(site)s/assets/images/instalacion-tinaco-hero-800w.webp","url":"%(site)s/",'
        '"telephone":"+526673922273","priceRange":"$500-$8,000 MXN",'
        '"address":{"@type":"PostalAddress","streetAddress":"Culiacán","addressLocality":"Culiacán","addressRegion":"Sinaloa","postalCode":"80000","addressCountry":"MX"},'
        '"geo":{"@type":"GeoCoordinates","latitude":24.8090556,"longitude":-107.3940556},'
        '"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"},'
        '"sameAs":["https://www.facebook.com/plomeroculiacanpro","https://www.instagram.com/plomeroculiacanpro"],'
        '"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"150","bestRating":"5","worstRating":"1"}},'
        '{"@type":"Service","@id":"%(url)s#service","name":%(svcn)s,"serviceType":%(svct)s,'
        '"provider":{"@id":"%(site)s/#organization"},"areaServed":[%(area)s],"description":%(svcd)s,'
        '"offers":{"@type":"AggregateOffer","lowPrice":"%(low)s","highPrice":"%(high)s","priceCurrency":"MXN","offerCount":"%(oc)s"}},'
        '{"@type":"FAQPage","mainEntity":[%(faqs)s]},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Inicio","item":"%(site)s/"},'
        '{"@type":"ListItem","position":2,"name":"Servicios","item":"%(site)s/#servicios"},'
        '{"@type":"ListItem","position":3,"name":%(bc)s,"item":"%(url)s"}]}]}</script>'
        % {"site": SITE, "url": url, "svcn": _js(z["svcn"]), "svct": _js(z["svct"]),
           "svcd": _js(z["svcd"]), "area": area, "faqs": faqs,
           "low": z.get("lowprice", "500"), "high": z.get("highprice", "8000"),
           "oc": z.get("offercount", str(len(z["faqs"]))), "bc": _js(z["bc"])}
    )
    return g


def build_spec(z, skel):
    # Bloque JSON-LD del esqueleto (una sola línea <script ...>...</script>) y CUERPO
    # (de </header> a <footer>) se extraen del esqueleto para no hardcodearlos.
    m_ld = re.search(r'<script type="application/ld\+json">.*?</script>', skel, re.S)
    if not m_ld:
        sys.exit("❌ no encontré el bloque JSON-LD en el esqueleto")
    ld_old = m_ld.group(0)
    m_body = re.search(r'</header>(.*?)\n    <footer', skel, re.S)
    if not m_body:
        sys.exit("❌ no encontré el cuerpo (</header> ... <footer>) en el esqueleto")
    body_old = m_body.group(1)

    cuerpo = z["cuerpo_html"].rstrip("\n")
    reps = [
        # 1) JSON-LD completo (1)
        {"old": ld_old, "new": build_jsonld(z)},
        # 2) cuerpo visible completo (1)
        {"old": "</header>" + body_old + "\n    <footer",
         "new": "</header>\n" + cuerpo + "\n\n    <footer"},
        # 3) retargueteo de head + hero. ORDEN IMPORTA (cuentas exactas tras quitar JSON-LD y
        #    cuerpo): el alt del hero CONTIENE al H1 como substring → se reemplaza ANTES; el
        #    título CONTIENE "Plomero Zona Oriente" (nombre del breadcrumb) → se reemplaza antes,
        #    y el breadcrumb se ancla con "</li>" para no colisionar con un título nuevo.
        {"old": SK_SLUG, "new": z["slug"], "n": 3},          # canonical + og:url + twitter:url
        {"old": SK_TITLE, "new": z["title"], "n": 3},        # <title> + og:title + twitter:title
        {"old": SK_HALT, "new": z["halt"], "n": 1},          # alt del hero (contiene al H1)
        {"old": SK_H1, "new": z["h1"], "n": 1},
        {"old": SK_HSUB, "new": z["hsub"], "n": 1},
        {"old": SK_DESC, "new": z["desc"], "n": 1},
        {"old": SK_KW, "new": z["kw"], "n": 1},
        {"old": SK_OGD, "new": z["ogd"], "n": 1},
        {"old": SK_TWD, "new": z["twd"], "n": 1},
        {"old": ">" + SK_BCNAME + "</li>", "new": ">" + z["bc"] + "</li>", "n": 1},  # breadcrumb activo
    ]
    return {"skeleton": SK, "output": "servicios/%s/index.html" % z["slug"], "replacements": reps}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    if sys.argv[1] == "--ejemplo":
        print(json.dumps(EJEMPLO, ensure_ascii=False, indent=2)); sys.exit(0)
    z = json.load(open(sys.argv[1], encoding="utf-8"))
    skel = open(os.path.join(ROOT, SK), encoding="utf-8").read()
    spec = build_spec(z, skel)
    r = subprocess.run([sys.executable, os.path.join(ROOT, ".pipeline/gen-landing.py"), "-"],
                       input=json.dumps(spec), capture_output=True, text=True, cwd=ROOT)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode == 0:
        print("\nSIGUIENTE:  python3 scripts/crecer.py servicio %s" % sys.argv[1])
        print("  (crea + sitemap + enlace en home + bump sw + candado; revierte si falla)")
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
