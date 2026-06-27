#!/usr/bin/env python3
"""
Actualiza lastmod de las páginas de servicios que recibieron Review schemas.
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# Servicios modificados (6 páginas con Review schemas agregados)
servicios_modificados = [
    "correccion-baja-presion",
    "destape-de-drenajes",
    "deteccion-de-fugas",
    "instalacion-de-sanitarios",
    "mantenimiento-de-boiler",
    "reparacion-de-fugas",
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
for url_elem in root.findall('sm:url', ns) if 'sm' in root.tag else root.findall('ns0:url', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'}):
    loc_elem = url_elem.find('sm:loc', ns) if 'sm' in root.tag else url_elem.find('ns0:loc', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})

    if loc_elem is not None:
        loc_text = loc_elem.text

        # Verificar si esta URL es de un servicio modificado
        for servicio_slug in servicios_modificados:
            if f"/servicios/{servicio_slug}/" in loc_text:
                # Actualizar lastmod
                lastmod_elem = url_elem.find('sm:lastmod', ns) if 'sm' in root.tag else url_elem.find('ns0:lastmod', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
                if lastmod_elem is not None:
                    lastmod_elem.text = new_lastmod
                    updated_count += 1
                    print(f"✓ {servicio_slug} - lastmod actualizado")
                break

# Guardar XML con formato correcto
tree.write(sitemap_file, encoding='UTF-8', xml_declaration=True)

print(f"\n✅ Sitemap actualizado correctamente:")
print(f"   • Servicios actualizados: {updated_count}")
print(f"   • Nueva fecha lastmod: {new_lastmod}")
print(f"   • Archivo: {sitemap_file}")
