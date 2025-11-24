#!/usr/bin/env python3
"""
Remover referencias PNG fallback innecesarias
Las imágenes WebP son soportadas por todos los navegadores modernos (2025)
"""

from pathlib import Path
import re

print(f"\n🔧 CORRECCIÓN: Remover PNG Fallback")
print(f"{'='*70}\n")

base_dir = Path('servicios/plomero-colonias-culiacan')

total_paginas = 0
paginas_modificadas = 0

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    total_paginas += 1

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Patrón para encontrar <picture> con source WebP + img PNG fallback
    # El formato tiene múltiples líneas y atributos sizes

    # Pattern: <picture> ... </picture> con WebP source y PNG img
    pattern = r'<picture>\s*<source\s+type="image/webp"\s+srcset="([^"]+)"\s+sizes="[^"]*">\s*<img\s+src="[^"]*\.png"[^>]*>\s*</picture>'

    # Extraer la primera URL WebP del srcset (la de 420w)
    def replace_picture(match):
        webp_srcset = match.group(1)
        # Obtener la primera URL (420w)
        first_url = webp_srcset.split(',')[0].strip().split()[0]
        return f'<img src="{first_url}" loading="lazy" class="service-img">'

    content = re.sub(pattern, replace_picture, content, flags=re.DOTALL)

    # Guardar si hubo cambios
    if content != original_content:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        paginas_modificadas += 1

        if paginas_modificadas % 20 == 0:
            print(f"  ✅ {paginas_modificadas} páginas corregidas...")

print(f"\n{'='*70}")
print(f"📊 RESUMEN")
print(f"{'='*70}\n")

print(f"Total páginas: {total_paginas}")
print(f"Páginas modificadas: {paginas_modificadas}")
print(f"Páginas sin cambios: {total_paginas - paginas_modificadas}")

if paginas_modificadas > 0:
    print(f"\n✅ PNG fallback removido de {paginas_modificadas} páginas")
    print(f"\n📈 Mejoras:")
    print(f"   - HTML más simple y limpio")
    print(f"   - Sin referencias a archivos inexistentes")
    print(f"   - WebP soportado por todos los navegadores modernos (2025)")
    print(f"   - Reducción de bytes en HTML")
else:
    print(f"\n✅ No se encontraron referencias PNG para remover")

print(f"\n✨ Completado\n")
