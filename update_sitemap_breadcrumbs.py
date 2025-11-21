#!/usr/bin/env python3
"""
Actualiza lastmod de las páginas que recibieron breadcrumbs visuales.
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# Páginas modificadas (50 páginas con breadcrumbs visuales)
servicios_modificados = [
    "plomero-precios",
    "plomero-cerca-de-mi",
    "destape-de-drenajes",
    "plomero-colonias-culiacan",
    "deteccion-de-fugas",
    "plomero-a-domicilio",
    "emergencia-24-7",
    "mantenimiento-de-boiler",
    "instalacion-de-sanitarios",
    "reparacion-de-fugas",
    "correccion-baja-presion",
]

colonias_modificadas = [
    "campestre", "bosques-del-humaya", "villa-universidad", "lomas-del-boulevard",
    "real-del-valle", "infonavit-humaya", "isla-del-oeste", "lomas-de-san-isidro",
    "colinas-de-la-rivera", "jardines-del-valle", "bachigualato", "real-san-angel",
    "las-palmas", "nuevo-culiacan", "hacienda-del-valle", "hacienda-los-huertos",
    "tres-rios", "country-tres-rios", "colinas-de-san-miguel", "altamira",
    "portales-del-rio", "cumbres-tres-rios", "montebello", "villa-bonita",
    "guadalupe", "zona-dorada", "santa-fe", "centro", "chapultepec"
]

blog_modificados = [
    "cuanto-cuesta-plomeria-bano-completo-culiacan",
    "problemas-comunes-plomeria-culiacan",
    "cuanto-cuesta-cambiar-taza-bano-culiacan",
    "como-identificar-buen-plomero-culiacan",
    "instalacion-tinaco-guia-compra",
    "cuanto-cobra-plomero-visita-culiacan",
    "drenaje-tapado-senales-prevencion",
    "como-detectar-fugas-agua-casa",
    "baja-presion-agua-causas-soluciones",
    "cuando-llamar-plomero-profesional",
]

# Fecha actual para lastmod
new_lastmod = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")

sitemap_file = "sitemaps/main_sitemap.xml"

# Parsear XML
tree = ET.parse(sitemap_file)
root = tree.getroot()

# Namespace de sitemaps
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

updated_count = 0

# Iterar sobre todos los <url>
for url_elem in root.findall('sm:url', ns):
    loc_elem = url_elem.find('sm:loc', ns)

    if loc_elem is not None:
        loc_text = loc_elem.text

        # Verificar si es un servicio modificado
        for servicio_slug in servicios_modificados:
            if f"/servicios/{servicio_slug}/" in loc_text:
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if lastmod_elem is not None:
                    lastmod_elem.text = new_lastmod
                    updated_count += 1
                    print(f"✓ servicio/{servicio_slug}")
                break

        # Verificar si es una colonia modificada
        for colonia_slug in colonias_modificadas:
            if f"/servicios/plomero-colonias-culiacan/{colonia_slug}/" in loc_text:
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if lastmod_elem is not None:
                    lastmod_elem.text = new_lastmod
                    updated_count += 1
                    print(f"✓ colonia/{colonia_slug}")
                break

        # Verificar si es un artículo de blog modificado
        for blog_slug in blog_modificados:
            if f"/blog/{blog_slug}/" in loc_text:
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if lastmod_elem is not None:
                    lastmod_elem.text = new_lastmod
                    updated_count += 1
                    print(f"✓ blog/{blog_slug}")
                break

# Guardar XML con formato correcto
tree.write(sitemap_file, encoding='UTF-8', xml_declaration=True)

print(f"\n✅ Sitemap actualizado correctamente:")
print(f"   • Páginas actualizadas: {updated_count}")
print(f"   • Nueva fecha lastmod: {new_lastmod}")
print(f"   • Archivo: {sitemap_file}")
