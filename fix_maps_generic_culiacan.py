#!/usr/bin/env python3
"""
Cambiar los mapas a una vista genérica de Culiacán en lugar de colonias específicas.
Esto evita el logo gigante de Google cuando no encuentra la ubicación exacta.
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

print(f"🔧 CAMBIANDO MAPAS A VISTA GENÉRICA DE CULIACÁN\n")
print(f"{'='*70}")

contador = 0

# URL genérica de Culiacán que siempre funciona
generic_map_url = "https://www.google.com/maps?q=Culiacán,+Sinaloa,+México&output=embed"

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

    # Reemplazar URL del mapa por la genérica
    pattern_map_url = r'<iframe src="https://www\.google\.com/maps\?q=[^"]+&output=embed"'
    replacement = f'<iframe src="{generic_map_url}"'

    if re.search(pattern_map_url, content):
        content = re.sub(pattern_map_url, replacement, content)

        # Actualizar el texto descriptivo del mapa
        pattern_map_text = r'(Nuestro equipo de plomeros profesionales brinda servicio en toda la colonia <strong>)[^<]+(</strong>)'
        content = re.sub(pattern_map_text, r'\1' + name + r'\2', content)

        # Actualizar el título del mapa para mantener el nombre de la colonia
        pattern_map_title = r'title="Mapa de [^"]+"'
        content = re.sub(pattern_map_title, f'title="Área de servicio en {name}, Culiacán"', content)

        # Escribir archivo corregido
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {name:35} → Mapa genérico de Culiacán")
        contador += 1
    else:
        print(f"⚠️  {name} - No se encontró el iframe del mapa")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas actualizados: {contador}/15")
print(f"{'='*70}")

print(f"\n✨ Solución aplicada:")
print(f"  • Todos los mapas ahora muestran Culiacán completo")
print(f"  • Se eliminó el problema del logo gigante de Google")
print(f"  • El texto mantiene el nombre de la colonia específica")
print(f"  • Misma estrategia que en Las Quintas original")
