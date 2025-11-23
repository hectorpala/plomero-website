#!/usr/bin/env python3
"""
Reduce el ancho del contenedor del mapa al 50% y lo centra.
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"📐 Reduciendo ancho de mapas al 50% y centrando en {len(colonias)} colonias\n")

contador_exitosos = 0

for colonia_dir in sorted(colonias):
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        print(f"⚠️  {colonia_dir.name} - archivo index.html no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer nombre de colonia
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Buscar el contenedor blanco del mapa y agregar max-width + margin auto
    # Patrón: <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

    pattern = r'(<div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba\(0,0,0,0\.1\);">)'
    replacement = r'<div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 50%; margin: 0 auto;">'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)

        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {colonia_name} - Mapa reducido al 50% y centrado")
        contador_exitosos += 1
    else:
        print(f"⚠️  {colonia_name} - No se encontró el contenedor del mapa")

print(f"\n{'='*60}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas redimensionados: {contador_exitosos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*60}")
print(f"\n✨ CAMBIOS APLICADOS:")
print(f"  • Ancho reducido al 50% (max-width: 50%)")
print(f"  • Centrado automáticamente (margin: 0 auto)")
print(f"  • Altura ya estaba al 28% (reducida previamente)")
print(f"  • Mapa ahora es compacto y centrado")
