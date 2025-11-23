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

# Lista de servicios actualizados hoy
servicios_actualizados = [
    'correccion-baja-presion',
    'destape-de-drenajes',
    'deteccion-de-fugas',
    'emergencia-24-7',
    'instalacion-de-sanitarios',
    'mantenimiento-de-boiler',
    'plomero-a-domicilio',
    'plomero-cerca-de-mi',
    'plomero-precios',
    'reparacion-de-fugas'
]

# Actualizar URLs de servicios que acabamos de modificar
for url in root.findall('ns:url', ns):
    loc = url.find('ns:loc', ns)
    lastmod = url.find('ns:lastmod', ns)

    if loc is not None and lastmod is not None:
        # Check si es un servicio actualizado
        for servicio in servicios_actualizados:
            if f'servicios/{servicio}/' in loc.text:
                lastmod.text = current_timestamp
                contador += 1
                servicio_name = servicio.replace('-', ' ').title()
                print(f"✅ {servicio_name}: {current_timestamp}")
                break

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ URLs actualizadas: {contador}")
print(f"  📅 Nueva fecha: {current_timestamp}")
print(f"{'='*70}")

# Guardar el sitemap actualizado
tree.write('sitemaps/main_sitemap.xml', encoding='utf-8', xml_declaration=True)

print(f"\n✨ Sitemap actualizado exitosamente")
print(f"📋 Próximo paso: Commit y push del sitemap actualizado")
