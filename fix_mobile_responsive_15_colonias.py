#!/usr/bin/env python3
"""
Hacer el mapa y NAP totalmente responsive en las 15 nuevas colonias.
Agregar media queries para móvil.
"""

import re
from pathlib import Path

# Base directory
base_dir = Path('servicios/plomero-colonias-culiacan')

# 15 nuevas colonias a corregir
nuevas_colonias = [
    'infonavit-barrancos', 'valle-alto', 'libertad', 'tierra-blanca', 'stase',
    'san-angel', 'alameda', 'barrancos', 'el-vallado', 'jardines-de-humaya',
    'los-pinos', 'palmito', 'recursos-hidraulicos', 'villas-del-rio',
    'desarrollo-urbano-tres-rios'
]

print(f"📱 OPTIMIZANDO DISEÑO RESPONSIVE PARA MÓVIL\n")
print(f"{'='*70}")

contador = 0

# Estilos responsive para agregar antes de </head>
responsive_styles = '''
    <style>
        /* Responsive styles for map and NAP sections */
        @media (max-width: 768px) {
            /* Map container - full width on mobile */
            section > div[style*="max-width: 50%"] {
                max-width: 100% !important;
                padding: 15px !important;
            }

            /* Map section padding */
            section[style*="margin: 40px 0"] {
                margin: 20px 0 !important;
                padding: 20px 10px !important;
            }

            /* Map title */
            section h2[style*="font-size: 1.8em"] {
                font-size: 1.4em !important;
            }

            /* Grid in map section - single column on mobile */
            div[style*="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))"] {
                grid-template-columns: 1fr !important;
            }

            /* NAP block title */
            h3[style*="font-size: 1.3em"] {
                font-size: 1.1em !important;
            }
        }
    </style>
'''

for slug in nuevas_colonias:
    index_file = base_dir / slug / 'index.html'

    if not index_file.exists():
        print(f"⚠️  {slug} - Archivo no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si ya tiene los estilos responsive
    if '/* Responsive styles for map and NAP sections */' in content:
        print(f"⏭️  {slug:35} - Ya tiene estilos responsive")
        continue

    # Buscar </head> y agregar estilos antes
    if '</head>' in content:
        content = content.replace('</head>', responsive_styles + '\n</head>')

        # Escribir archivo
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        nombre = slug.replace('-', ' ').title()
        print(f"✅ {nombre:35} - Estilos responsive agregados")
        contador += 1
    else:
        print(f"⚠️  {slug} - No se encontró </head>")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Páginas optimizadas: {contador}/15")
print(f"{'='*70}")

print(f"\n📱 OPTIMIZACIONES APLICADAS:")
print(f"  • Mapa: 100% ancho en móvil (vs 50% en desktop)")
print(f"  • Padding reducido en secciones móviles")
print(f"  • Títulos más pequeños (1.4em vs 1.8em)")
print(f"  • Grids de una columna en móvil")
print(f"  • Media query: @media (max-width: 768px)")
print(f"\n✨ Páginas 100% responsive para móvil")
