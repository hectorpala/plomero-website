#!/usr/bin/env python3
"""
Reduce el tamaño del contenedor del mapa a la mitad.
Cambia el aspect ratio de 16:9 (56.25%) a aproximadamente 8:4.5 (28%)
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"📐 Reduciendo tamaño de mapas en {len(colonias)} colonias\n")

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

    # Buscar y reemplazar el padding-bottom del contenedor del mapa
    # Actual: 56.25% (16:9 aspect ratio)
    # Nuevo: 28% (aproximadamente la mitad de altura)

    pattern = r'padding-bottom:\s*56\.25%;'
    replacement = 'padding-bottom: 28%;'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)

        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {colonia_name} - Mapa reducido a la mitad")
        contador_exitosos += 1
    else:
        print(f"⚠️  {colonia_name} - No se encontró el patrón de padding")

print(f"\n{'='*60}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas redimensionados: {contador_exitosos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*60}")
print(f"\n✨ CAMBIOS APLICADOS:")
print(f"  • Altura reducida de 56.25% a 28%")
print(f"  • Mapa ahora ocupa la mitad del espacio vertical")
print(f"  • Mantiene funcionalidad completa")
print(f"  • Responsive en todos los dispositivos")
