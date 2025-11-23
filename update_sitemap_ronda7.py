#!/usr/bin/env python3
"""
Actualizar sitemap.xml con las 10 colonias de la Ronda 7 (total: 95).
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Timestamp actual en formato ISO 8601 con timezone
tz = timezone(timedelta(hours=-7))  # PST/MST
current_timestamp = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
current_timestamp = current_timestamp[:-2] + ':' + current_timestamp[-2:]

# 10 colonias - Ronda 7
nuevas_colonias = [
    'amado-nervo',
    'antonio-toledo-corro',
    'ampliacion-el-barrio',
    'altos-de-bachigualato',
    'agrarista-mexicana',
    'cinco-de-febrero',
    'seis-de-enero',
    'veintiuno-de-marzo',
    'campestre-los-laureles',
    'campestre-san-jorge'
]

# Leer sitemap existente
sitemap_file = 'sitemap.xml'

tree = ET.parse(sitemap_file)
root = tree.getroot()

# Namespace de sitemap
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

print(f"📄 ACTUALIZANDO SITEMAP - RONDA 7\n")
print(f"{'='*70}")

urls_existentes = [loc.text for loc in root.findall('.//sm:loc', ns)]

contador = 0

for colonia_slug in nuevas_colonias:
    url_completa = f"https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/"

    # Verificar si ya existe
    if url_completa in urls_existentes:
        print(f"⏭️  {colonia_slug:30} - Ya en sitemap")
        continue

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

    nombre = colonia_slug.replace('-', ' ').title()
    print(f"✅ {nombre:30} - Agregada al sitemap")
    contador += 1

# Guardar sitemap actualizado
tree.write(sitemap_file, encoding='utf-8', xml_declaration=True)

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ URLs nuevas agregadas: {contador}")
print(f"  📄 Sitemap actualizado: sitemap.xml")
print(f"  🕒 Timestamp: {current_timestamp}")
print(f"  🔗 Total de colonias en sitemap: 95")
print(f"\n🎯 Siguiente paso: git commit y deploy")
