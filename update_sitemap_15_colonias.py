#!/usr/bin/env python3
"""
Agregar 15 nuevas colonias al sitemap con la fecha actual.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Parsear sitemap existente
tree = ET.parse('sitemaps/main_sitemap.xml')
root = tree.getroot()

# Namespace para sitemap XML
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Obtener la fecha/hora actual en MST (UTC-7)
mst = timezone(timedelta(hours=-7))
now = datetime.now(mst)
current_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S%z')
current_timestamp = current_timestamp[:-2] + ':' + current_timestamp[-2:]

print(f"📅 Agregando 15 nuevas colonias al sitemap")
print(f"🕐 Timestamp: {current_timestamp}\n")
print(f"{'='*70}")

# 15 nuevas colonias
nuevas_colonias = [
    'infonavit-barrancos',
    'valle-alto',
    'libertad',
    'tierra-blanca',
    'stase',
    'san-angel',
    'alameda',
    'barrancos',
    'el-vallado',
    'jardines-de-humaya',
    'los-pinos',
    'palmito',
    'recursos-hidraulicos',
    'villas-del-rio',
    'desarrollo-urbano-tres-rios'
]

# Verificar si ya existen en el sitemap
urls_existentes = set()
for url in root.findall('ns:url', ns):
    loc = url.find('ns:loc', ns)
    if loc is not None:
        urls_existentes.add(loc.text)

contador_agregadas = 0

for colonia_slug in nuevas_colonias:
    url_completa = f"https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/"

    # Solo agregar si no existe
    if url_completa not in urls_existentes:
        # Crear nuevo elemento <url>
        url_element = ET.SubElement(root, 'url')

        loc = ET.SubElement(url_element, 'loc')
        loc.text = url_completa

        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = current_timestamp

        changefreq = ET.SubElement(url_element, 'changefreq')
        changefreq.text = 'weekly'

        priority = ET.SubElement(url_element, 'priority')
        priority.text = '0.8'

        colonia_name = colonia_slug.replace('-', ' ').title()
        print(f"✅ {colonia_name:35} → {url_completa}")
        contador_agregadas += 1
    else:
        colonia_name = colonia_slug.replace('-', ' ').title()
        print(f"⏭️  {colonia_name:35} → Ya existe en sitemap")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ URLs agregadas al sitemap: {contador_agregadas}")
print(f"  📅 Fecha: {current_timestamp}")
print(f"{'='*70}")

# Guardar el sitemap actualizado
tree.write('sitemaps/main_sitemap.xml', encoding='utf-8', xml_declaration=True)

print(f"\n✨ Sitemap actualizado exitosamente")
print(f"📋 Total de colonias ahora: 45 (30 anteriores + 15 nuevas)")
