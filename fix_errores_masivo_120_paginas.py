#!/usr/bin/env python3
"""
Corrección masiva de errores en las 120 páginas de colonias

Errores a corregir:
1. Doble "Culiacán" en nombres de schemas
2. ReviewCount inconsistente (estandarizar a 150)
3. OG image width 800 → 1200
4. OG image height 800 → 630
5. Map aspect ratio 28% → 56%
6. Footer incompleto
"""

from pathlib import Path
import re

base_dir = Path('servicios/plomero-colonias-culiacan')

print(f"🔧 CORRECCIÓN MASIVA DE ERRORES - 120 PÁGINAS")
print(f"{'='*70}\n")

total_paginas = 0
paginas_modificadas = 0
estadisticas = {
    'doble_culiacan': 0,
    'review_count': 0,
    'og_width': 0,
    'og_height': 0,
    'map_ratio': 0,
    'footer': 0
}

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
    correcciones_esta_pagina = []

    # ===== CORRECCIÓN 1: Doble "Culiacán" =====
    if 'Culiacán, Culiacán' in content:
        content = re.sub(r'(\w+)\s+Culiacán,\s+Culiacán', r'\1, Culiacán', content)
        correcciones_esta_pagina.append('doble_culiacan')

    # ===== CORRECCIÓN 2: ReviewCount inconsistente =====
    review_counts = re.findall(r'"reviewCount":\s*"(\d+)"', content)
    if len(set(review_counts)) > 1 or '127' in review_counts:
        content = re.sub(r'"reviewCount":\s*"\d+"', '"reviewCount": "150"', content)
        correcciones_esta_pagina.append('review_count')

    # ===== CORRECCIÓN 3: OG Width =====
    if 'og:image:width" content="800"' in content:
        content = content.replace('og:image:width" content="800"', 'og:image:width" content="1200"')
        correcciones_esta_pagina.append('og_width')

    # ===== CORRECCIÓN 4: OG Height =====
    if 'og:image:height" content="800"' in content:
        content = content.replace('og:image:height" content="800"', 'og:image:height" content="630"')
        correcciones_esta_pagina.append('og_height')

    # ===== CORRECCIÓN 5: Map Aspect Ratio =====
    if 'padding-bottom: 28%' in content:
        content = content.replace('padding-bottom: 28%', 'padding-bottom: 56%')
        correcciones_esta_pagina.append('map_ratio')

    # ===== CORRECCIÓN 6: Footer Incompleto =====
    if '<footer   ' in content or re.search(r'<footer\s+$', content, re.MULTILINE):
        content = re.sub(r'<footer\s+', '<footer class="footer">', content)
        correcciones_esta_pagina.append('footer')

    # Guardar si hubo cambios
    if content != original_content:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        paginas_modificadas += 1

        # Actualizar estadísticas
        for correccion in correcciones_esta_pagina:
            estadisticas[correccion] += 1

        # Mostrar progreso cada 20 páginas
        if paginas_modificadas % 20 == 0:
            print(f"  ✅ {paginas_modificadas} páginas corregidas...")

print(f"\n{'='*70}")
print(f"📊 RESUMEN DE CORRECCIÓN MASIVA")
print(f"{'='*70}\n")

print(f"Total de páginas procesadas: {total_paginas}")
print(f"Páginas modificadas: {paginas_modificadas}")
print(f"Páginas sin cambios: {total_paginas - paginas_modificadas}")

print(f"\n📋 Correcciones aplicadas:\n")
print(f"  1. Doble 'Culiacán' eliminado:        {estadisticas['doble_culiacan']} páginas")
print(f"  2. ReviewCount estandarizado a 150:   {estadisticas['review_count']} páginas")
print(f"  3. OG width corregido a 1200:         {estadisticas['og_width']} páginas")
print(f"  4. OG height corregido a 630:         {estadisticas['og_height']} páginas")
print(f"  5. Map ratio ajustado a 56%:          {estadisticas['map_ratio']} páginas")
print(f"  6. Footer tag corregido:              {estadisticas['footer']} páginas")

# Calcular porcentaje de mejora
if paginas_modificadas > 0:
    promedio_correcciones = sum(estadisticas.values()) / paginas_modificadas
    print(f"\n🎯 Promedio de correcciones por página: {promedio_correcciones:.1f}")

print(f"\n✅ Corrección masiva completada")
print(f"📈 {paginas_modificadas} páginas mejoradas de {total_paginas} totales")
print(f"\n💡 Siguiente paso: Ejecutar validación técnica completa\n")
