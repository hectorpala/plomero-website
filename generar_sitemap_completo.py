#!/usr/bin/env python3
"""
Generar sitemap.xml completo con todas las 120 colonias
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET

base_dir = Path('servicios/plomero-colonias-culiacan')

# Timestamp actual
tz = timezone(timedelta(hours=-7))
current_timestamp = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
current_timestamp = current_timestamp[:-2] + ':' + current_timestamp[-2:]

print(f"📄 GENERANDO SITEMAP COMPLETO\n")
print(f"{'='*70}")

# Crear root del sitemap
root = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# URLs principales del sitio
main_urls = [
    ('https://plomeroculiacanpro.mx/', '1.0', 'daily'),
    ('https://plomeroculiacanpro.mx/servicios/', '0.9', 'weekly'),
    ('https://plomeroculiacanpro.mx/servicios/reparacion-de-fugas/', '0.9', 'weekly'),
    ('https://plomeroculiacanpro.mx/servicios/destapado-de-drenaje/', '0.9', 'weekly'),
    ('https://plomeroculiacanpro.mx/servicios/instalacion-de-calentadores/', '0.9', 'weekly'),
    ('https://plomeroculiacanpro.mx/servicios/reparacion-de-tinacos/', '0.9', 'weekly'),
    ('https://plomeroculiacanpro.mx/blog/', '0.8', 'weekly'),
]

# Agregar URLs principales
for url, priority, changefreq in main_urls:
    url_elem = ET.SubElement(root, 'url')
    ET.SubElement(url_elem, 'loc').text = url
    ET.SubElement(url_elem, 'lastmod').text = current_timestamp
    ET.SubElement(url_elem, 'changefreq').text = changefreq
    ET.SubElement(url_elem, 'priority').text = priority

print(f"✅ URLs principales agregadas: {len(main_urls)}")

# Agregar colonias
colonias_agregadas = 0

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    url_colonia = f"https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_dir.name}/"

    url_elem = ET.SubElement(root, 'url')
    ET.SubElement(url_elem, 'loc').text = url_colonia
    ET.SubElement(url_elem, 'lastmod').text = current_timestamp
    ET.SubElement(url_elem, 'changefreq').text = 'weekly'
    ET.SubElement(url_elem, 'priority').text = '0.8'

    colonias_agregadas += 1

print(f"✅ Colonias agregadas: {colonias_agregadas}")

# Crear árbol XML y guardar
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)

sitemap_file = Path('sitemap.xml')
tree.write(sitemap_file, encoding='utf-8', xml_declaration=True)

print(f"\n{'='*70}")
print(f"📊 SITEMAP GENERADO")
print(f"{'='*70}")
print(f"Archivo: {sitemap_file}")
print(f"URLs totales: {len(main_urls) + colonias_agregadas}")
print(f"  - URLs principales: {len(main_urls)}")
print(f"  - Colonias: {colonias_agregadas}")
print(f"Timestamp: {current_timestamp}")
print(f"\n✅ Sitemap completo y actualizado")
print(f"🌐 URL: https://plomeroculiacanpro.mx/sitemap.xml")
print(f"\n📋 Próximo paso: Enviar a Google Search Console\n")
