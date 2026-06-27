#!/usr/bin/env python3
"""
Actualiza lastmod de las 29 colonias que recibieron LocalBusiness schema.
Versión corregida que no corrompe el XML.
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# Colonias modificadas (todas excepto las-quintas que ya tenía LocalBusiness)
colonias_modificadas = [
    "tres-rios", "centro", "montebello", "guadalupe", "chapultepec",
    "isla-del-oeste", "country-tres-rios", "hacienda-los-huertos",
    "real-del-valle", "zona-dorada", "campestre", "santa-fe",
    "las-palmas", "nuevo-culiacan", "infonavit-humaya", "bachigualato",
    "lomas-del-boulevard", "villa-universidad", "colinas-de-san-miguel",
    "altamira", "cumbres-tres-rios", "bosques-del-humaya",
    "hacienda-del-valle", "portales-del-rio", "colinas-de-la-rivera",
    "jardines-del-valle", "lomas-de-san-isidro", "real-san-angel",
    "villa-bonita"
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

        # Verificar si esta URL es de una colonia modificada
        for colonia_slug in colonias_modificadas:
            if f"/servicios/plomero-colonias-culiacan/{colonia_slug}/" in loc_text:
                # Actualizar lastmod
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if lastmod_elem is not None:
                    lastmod_elem.text = new_lastmod
                    updated_count += 1
                    print(f"✓ {colonia_slug} - lastmod actualizado")
                break

# Guardar XML con formato correcto
tree.write(sitemap_file, encoding='UTF-8', xml_declaration=True)

print(f"\n✅ Sitemap actualizado correctamente:")
print(f"   • Colonias actualizadas: {updated_count}")
print(f"   • Nueva fecha lastmod: {new_lastmod}")
print(f"   • Archivo: {sitemap_file}")
