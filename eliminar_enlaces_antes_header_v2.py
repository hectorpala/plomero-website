#!/usr/bin/env python3
"""
Eliminar sección de Enlaces Internos ANTES del header - VERSION 2
Patrón mejorado para capturar correctamente la sección
"""

from pathlib import Path
import re

base_dir = Path('servicios/plomero-colonias-culiacan')

print(f"🗑️  ELIMINANDO ENLACES ANTES DEL HEADER - V2")
print(f"{'='*70}\n")

total_paginas = 0
paginas_modificadas = 0

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    total_paginas += 1

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Patrón mejorado: desde el script GTM hasta el noscript, eliminando la sección en medio
    pattern = r'(<!-- Google Tag Manager -->\s*<script>.*?</script>)\s*<!-- Sección de Enlaces Internos a Colonias Cercanas -->.*?</section>\s*(<!-- Google Tag Manager \(noscript\) -->)'

    # Reemplazar: mantener GTM script + noscript, eliminar todo en medio
    replacement = r'\1\n\n    \2'

    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Guardar si hubo cambios
    if content != original_content:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        paginas_modificadas += 1

        if paginas_modificadas % 20 == 0:
            print(f"  ✅ {paginas_modificadas} páginas limpiadas...")

print(f"\n{'='*70}")
print(f"📊 RESUMEN")
print(f"{'='*70}\n")

print(f"Total: {total_paginas}")
print(f"Modificadas: {paginas_modificadas}")
print(f"Sin cambios: {total_paginas - paginas_modificadas}")

if paginas_modificadas > 0:
    print(f"\n✅ Sección eliminada de {paginas_modificadas} páginas")
else:
    print(f"\n✅ Todas las páginas ya estaban limpias")

print(f"\n✨ Completado\n")
