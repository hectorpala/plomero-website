#!/usr/bin/env python3
"""
Corregir las URLs de los mapas en las 15 nuevas colonias.
El problema: Todos los mapas apuntan a "Las Quintas" en lugar de su colonia específica.
"""

import re
from pathlib import Path

# Base directory
base_dir = Path('servicios/plomero-colonias-culiacan')

# 15 nuevas colonias a corregir
nuevas_colonias = [
    {'slug': 'infonavit-barrancos', 'name': 'Infonavit Barrancos'},
    {'slug': 'valle-alto', 'name': 'Valle Alto'},
    {'slug': 'libertad', 'name': 'Libertad'},
    {'slug': 'tierra-blanca', 'name': 'Tierra Blanca'},
    {'slug': 'stase', 'name': 'Stase'},
    {'slug': 'san-angel', 'name': 'San Ángel'},
    {'slug': 'alameda', 'name': 'Alameda'},
    {'slug': 'barrancos', 'name': 'Barrancos'},
    {'slug': 'el-vallado', 'name': 'El Vallado'},
    {'slug': 'jardines-de-humaya', 'name': 'Jardines de Humaya'},
    {'slug': 'los-pinos', 'name': 'Los Pinos'},
    {'slug': 'palmito', 'name': 'Palmito'},
    {'slug': 'recursos-hidraulicos', 'name': 'Recursos Hidráulicos'},
    {'slug': 'villas-del-rio', 'name': 'Villas del Río'},
    {'slug': 'desarrollo-urbano-tres-rios', 'name': 'Desarrollo Urbano 3 Ríos'}
]

print(f"🔧 CORRIGIENDO MAPAS EN 15 COLONIAS\n")
print(f"{'='*70}")

contador = 0

for colonia in nuevas_colonias:
    slug = colonia['slug']
    name = colonia['name']

    index_file = base_dir / slug / 'index.html'

    if not index_file.exists():
        print(f"⚠️  {name} - Archivo no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Crear URL del mapa con el nombre de la colonia
    # Reemplazar espacios por + para URL
    colonia_url = name.replace(' ', '+')
    map_url = f"https://www.google.com/maps?q={colonia_url},+Culiacán,+Sinaloa,+México&output=embed"

    # Patrón para encontrar y reemplazar la URL del mapa
    # Busca: <iframe src="https://www.google.com/maps?q=...
    pattern_map_url = r'<iframe src="https://www\.google\.com/maps\?q=[^"]+&output=embed"'
    replacement = f'<iframe src="{map_url}"'

    if re.search(pattern_map_url, content):
        content = re.sub(pattern_map_url, replacement, content)

        # También actualizar el title del mapa
        pattern_map_title = r'title="Mapa de [^"]+"'
        content = re.sub(pattern_map_title, f'title="Mapa de {name}, Culiacán"', content)

        # Escribir archivo corregido
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {name:35} → Mapa actualizado a {name}")
        contador += 1
    else:
        print(f"⚠️  {name} - No se encontró el iframe del mapa")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas corregidos: {contador}/15")
print(f"{'='*70}")

print(f"\n✨ Ahora cada colonia tiene su propio mapa personalizado")
print(f"📋 Próximo paso: Verificar en navegador y hacer commit")
