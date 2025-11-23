#!/usr/bin/env python3
"""
Crear 5 colonias adicionales - Ronda 3 (total: 60 páginas).
Estructura idéntica a Las Quintas, solo cambia el contenido personalizado.
"""

import os
import re
from pathlib import Path

# Leer template de Las Quintas
template_file = Path('servicios/plomero-colonias-culiacan/las-quintas/index.html')

with open(template_file, 'r', encoding='utf-8') as f:
    template = f.read()

# 5 colonias nuevas - Ronda 3
nuevas_colonias = [
    {'slug': 'ferrocarrilera', 'name': 'Ferrocarrilera', 'premium': False},
    {'slug': 'el-barrio', 'name': 'El Barrio', 'premium': False},
    {'slug': 'antonio-rosales', 'name': 'Antonio Rosales', 'premium': False},
    {'slug': 'cedros', 'name': 'Cedros', 'premium': False},
    {'slug': 'el-mirador', 'name': 'El Mirador', 'premium': False}
]

base_dir = Path('servicios/plomero-colonias-culiacan')

print(f"🏘️  CREANDO 5 COLONIAS - RONDA 3 (TOTAL: 60)\n")
print(f"{'='*70}")

for colonia in nuevas_colonias:
    slug = colonia['slug']
    name = colonia['name']
    es_premium = colonia['premium']

    # Crear directorio
    colonia_dir = base_dir / slug
    colonia_dir.mkdir(exist_ok=True)

    # Personalizar contenido
    content = template

    # 1. Reemplazar "Las Quintas" por nombre de colonia
    content = content.replace('Las Quintas', name)
    content = content.replace('las-quintas', slug)

    # 2. URL canónica y breadcrumbs
    content = re.sub(
        r'https://plomeroculiacanpro\.mx/servicios/plomero-colonias-culiacan/las-quintas/',
        f'https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{slug}/',
        content
    )

    # 3. Ajustar pricing según tipo de colonia
    if es_premium:
        pricing_min = "1000"
        pricing_max = "2500"
        pricing_range = "$1,000 - $2,500 MXN"
        hero_subtitle = f"Servicio especializado en residencias premium de {name}. Técnicos certificados con más de 10 años de experiencia. Respuesta inmediata las 24 horas del día, los 7 días de la semana."
    else:
        pricing_min = "800"
        pricing_max = "2000"
        pricing_range = "$800 - $2,000 MXN"
        hero_subtitle = f"Servicio confiable de plomería en {name}, Culiacán. Atención rápida, precios justos y trabajo garantizado. Disponibles 24/7 para emergencias y servicio programado."

    # Actualizar precios en Service Schema
    content = re.sub(
        r'"minPrice": "\d+"',
        f'"minPrice": "{pricing_min}"',
        content
    )
    content = re.sub(
        r'"maxPrice": "\d+"',
        f'"maxPrice": "{pricing_max}"',
        content
    )

    # 4. Hero subtitle (buscar el <p class="hero-subtitle">)
    pattern_hero = r'(<p class="hero-subtitle"[^>]*>)[^<]+(</p>)'
    content = re.sub(pattern_hero, rf'\1{hero_subtitle}\2', content)

    # 5. Mapa - usar ubicación específica de la colonia
    map_query = name.replace(' ', '+')
    map_url = f"https://www.google.com/maps?q={map_query},+Culiacán,+Sinaloa,+México&output=embed"

    content = re.sub(
        r'<iframe src="https://www\.google\.com/maps\?q=[^"]+&output=embed"',
        f'<iframe src="{map_url}"',
        content
    )

    # 6. Actualizar alt text de imágenes con nombre de colonia
    imagenes = [
        ('reparacion-fugas', f'Plomero reparando fuga en {name}, Culiacán'),
        ('arreglando-boiler', f'Técnico reparando boiler en {name}'),
        ('taza-de-baño', f'Instalación de grifería en {name}, Culiacán'),
        ('destapandodrenaje', f'Destape de drenaje en {name}'),
        ('reivicion-bajapresion', f'Revisión de presión de agua en {name}'),
        ('emergencia-24-7', f'Servicio de emergencia 24/7 en {name}, Culiacán')
    ]

    for img_name, alt_text in imagenes:
        pattern = f'(<img[^>]*{img_name}[^>]*alt=")[^"]*(")'
        content = re.sub(pattern, rf'\1{alt_text}\2', content)

    # 7. Title attributes en imágenes (para SEO)
    title_attributes = [
        ('reparacion-fugas', f'Reparación profesional de fugas en {name} - Plomero certificado'),
        ('arreglando-boiler', f'Mantenimiento y reparación de boilers en {name}, Culiacán'),
        ('taza-de-baño', f'Instalación de grifería y sanitarios en {name} - Trabajo garantizado'),
        ('destapandodrenaje', f'Destape profesional de drenajes en {name} - Equipos especializados'),
        ('reivicion-bajapresion', f'Corrección de baja presión de agua en {name}, Culiacán'),
        ('emergencia-24-7', f'Servicio de emergencias 24/7 en {name} - Llegada inmediata')
    ]

    for img_name, title_text in title_attributes:
        pattern = f'(<img[^>]*{img_name}[^>]*alt="[^"]*")'
        matches = list(re.finditer(pattern, content))
        for match in reversed(matches):
            if 'title=' not in match.group(0):
                replacement = match.group(0) + f' title="{title_text}"'
                content = content[:match.start()] + replacement + content[match.end():]

    # 8. Actualizar ImageObject schema con nombre de colonia
    content = re.sub(
        r'"name": "Plomero profesional reparando fuga en [^"]+, Culiacán"',
        f'"name": "Plomero profesional reparando fuga en {name}, Culiacán"',
        content
    )
    content = re.sub(
        r'"description": "Técnico especializado en reparación de fugas de agua en [^.]+\.',
        f'"description": "Técnico especializado en reparación de fugas de agua en {name}.',
        content
    )

    # 9. Logo title attribute
    pattern_logo = r'(<img src="[^"]*logo-plomero-culiacan-pro\.webp" alt="Plomero Culiacán Pro - Logo")'
    if re.search(pattern_logo, content):
        match = re.search(pattern_logo, content)
        if 'title=' not in match.group(0):
            replacement = match.group(0) + f' title="Plomero certificado en {name}, Culiacán - Servicio 24/7"'
            content = content.replace(match.group(0), replacement)

    # Guardar archivo
    index_file = colonia_dir / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ {name:30} → {slug}")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ 5 nuevas colonias creadas (Ronda 3)")
print(f"  📁 Total de colonias: 60")
print(f"  🗺️  Mapa: Ubicación específica de cada colonia")
print(f"  📱 Responsive: Media queries incluidas")
print(f"  ⚡ Performance: Optimizaciones aplicadas")
print(f"  🖼️  SEO imágenes: Title attributes + ImageObject schema")
print(f"\n🎯 Próximo paso: Actualizar sitemap con las 5 nuevas URLs")
