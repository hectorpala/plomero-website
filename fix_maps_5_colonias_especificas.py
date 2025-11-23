#!/usr/bin/env python3
"""
Corregir mapas de las 5 nuevas colonias para mostrar ubicación específica.
Cada colonia debe mostrar su propia ubicación en el mapa.
"""

import re
from pathlib import Path

base_dir = Path('servicios/plomero-colonias-culiacan')

# 5 nuevas colonias con URLs específicas para Google Maps
colonias_mapas = [
    {
        'slug': 'adolfo-lopez-mateos',
        'name': 'Adolfo López Mateos',
        'map_query': 'Adolfo+López+Mateos,+Culiacán,+Sinaloa,+México'
    },
    {
        'slug': 'aeropuerto',
        'name': 'Aeropuerto',
        'map_query': 'Aeropuerto,+Culiacán,+Sinaloa,+México'
    },
    {
        'slug': 'diez-de-mayo',
        'name': '10 de Mayo',
        'map_query': '10+de+Mayo,+Culiacán,+Sinaloa,+México'
    },
    {
        'slug': 'emiliano-zapata',
        'name': 'Emiliano Zapata',
        'map_query': 'Emiliano+Zapata,+Culiacán,+Sinaloa,+México'
    },
    {
        'slug': 'francisco-i-madero',
        'name': 'Francisco I. Madero',
        'map_query': 'Francisco+I.+Madero,+Culiacán,+Sinaloa,+México'
    }
]

print(f"🗺️  ACTUALIZANDO MAPAS CON UBICACIONES ESPECÍFICAS\n")
print(f"{'='*70}")

contador = 0

for colonia in colonias_mapas:
    slug = colonia['slug']
    name = colonia['name']
    map_query = colonia['map_query']

    index_file = base_dir / slug / 'index.html'

    if not index_file.exists():
        print(f"⚠️  {name} - Archivo no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nueva URL del mapa específica
    new_map_url = f"https://www.google.com/maps?q={map_query}&output=embed"

    # Reemplazar URL del mapa
    old_pattern = r'<iframe src="https://www\.google\.com/maps\?q=[^"]+&output=embed"'
    new_iframe = f'<iframe src="{new_map_url}"'

    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_iframe, content)

        # Guardar archivo
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {name:30} - Mapa actualizado")
        contador += 1
    else:
        print(f"⚠️  {name:30} - No se encontró iframe del mapa")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas actualizados: {contador}/5")
print(f"  🗺️  Cada colonia ahora muestra su ubicación específica")
print(f"\n🎯 Próximo paso: git commit y push")
