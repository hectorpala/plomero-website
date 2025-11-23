#!/usr/bin/env python3
"""
Actualiza las fechas lastmod del sitemap basándose en las fechas de git commits.
Para páginas que cambiaron hoy, usa la fecha/hora actual.
"""

import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Parsear sitemap existente
tree = ET.parse('sitemaps/main_sitemap.xml')
root = tree.getroot()

# Namespace para sitemap XML
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Obtener la fecha/hora actual en MST (UTC-7)
# Sinaloa usa Mountain Standard Time durante todo el año
mst = timezone(timedelta(hours=-7))
now = datetime.now(mst)
current_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S%z')
# Formatear timezone como -07:00 en lugar de -0700
current_timestamp = current_timestamp[:-2] + ':' + current_timestamp[-2:]

print(f"🕐 Actualizando sitemap con timestamp: {current_timestamp}\n")
print(f"{'='*70}")

contador = 0

# Actualizar todas las URLs de colonias (que acabamos de modificar)
for url in root.findall('ns:url', ns):
    loc = url.find('ns:loc', ns)
    lastmod = url.find('ns:lastmod', ns)

    if loc is not None and 'plomero-colonias-culiacan' in loc.text:
        if lastmod is not None:
            lastmod.text = current_timestamp
            contador += 1
            # Extraer nombre de colonia de la URL
            colonia = loc.text.split('/')[-2].replace('-', ' ').title()
            print(f"✅ {colonia}: {current_timestamp}")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ URLs actualizadas: {contador}")
print(f"  📅 Nueva fecha: {current_timestamp}")
print(f"{'='*70}")

# Guardar el sitemap actualizado
tree.write('sitemaps/main_sitemap.xml', encoding='utf-8', xml_declaration=True)

print(f"\n✨ Sitemap actualizado exitosamente")
print(f"📋 Próximo paso: Commit y push del sitemap actualizado")
