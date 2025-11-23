#!/usr/bin/env python3
"""
Crear 15 nuevas páginas de colonias usando Las Quintas como plantilla.
Estructura y estilo EXACTAMENTE IGUAL, solo cambios de contenido personalizado.
"""

import os
import re
from pathlib import Path
import shutil

# 15 colonias prioritarias a crear
nuevas_colonias = [
    {'slug': 'infonavit-barrancos', 'name': 'Infonavit Barrancos', 'premium': False},
    {'slug': 'valle-alto', 'name': 'Valle Alto', 'premium': True},
    {'slug': 'libertad', 'name': 'Libertad', 'premium': False},
    {'slug': 'tierra-blanca', 'name': 'Tierra Blanca', 'premium': False},
    {'slug': 'stase', 'name': 'Stase', 'premium': False},
    {'slug': 'san-angel', 'name': 'San Ángel', 'premium': True},
    {'slug': 'alameda', 'name': 'Alameda', 'premium': False},
    {'slug': 'barrancos', 'name': 'Barrancos', 'premium': False},
    {'slug': 'el-vallado', 'name': 'El Vallado', 'premium': False},
    {'slug': 'jardines-de-humaya', 'name': 'Jardines de Humaya', 'premium': False},
    {'slug': 'los-pinos', 'name': 'Los Pinos', 'premium': False},
    {'slug': 'palmito', 'name': 'Palmito', 'premium': False},
    {'slug': 'recursos-hidraulicos', 'name': 'Recursos Hidráulicos', 'premium': False},
    {'slug': 'villas-del-rio', 'name': 'Villas del Río', 'premium': True},
    {'slug': 'desarrollo-urbano-tres-rios', 'name': 'Desarrollo Urbano 3 Ríos', 'premium': True}
]

# Paths
base_dir = Path('servicios/plomero-colonias-culiacan')
plantilla_path = base_dir / 'las-quintas' / 'index.html'

print("🏗️  CREANDO 15 NUEVAS PÁGINAS DE COLONIAS")
print("="*70)
print(f"Plantilla base: {plantilla_path}")
print(f"Total a crear: {len(nuevas_colonias)} colonias\n")

# Leer plantilla de Las Quintas
with open(plantilla_path, 'r', encoding='utf-8') as f:
    plantilla_content = f.read()

contador_creadas = 0
contador_premium = 0

for colonia in nuevas_colonias:
    slug = colonia['slug']
    name = colonia['name']
    es_premium = colonia['premium']

    # Crear directorio
    colonia_dir = base_dir / slug
    colonia_dir.mkdir(parents=True, exist_ok=True)

    # Personalizar contenido
    content = plantilla_content

    # 1. Reemplazos básicos de nombre
    content = content.replace('Las Quintas', name)
    content = content.replace('las-quintas', slug)
    content = content.replace('las Quintas', name)

    # 2. Actualizar título y meta description
    if es_premium:
        hero_subtitle = f"Servicio especializado en residencias premium de {name}. Más de 10 años de experiencia. Conocemos sistemas de alta presión, hidroneumáticos, instalaciones de lujo. Llegada en 20-30 minutos. Atención 24/7."
        pricing_min = "1000"
        pricing_max = "2500"
        pricing_text = f"Los precios son transparentes y justos. Reparación de fuga desde $600, destape desde $400, cambio de WC desde $800. Los costos pueden ser mayores debido al uso de materiales premium y la complejidad de los sistemas en residencias de lujo. Te damos presupuesto exacto antes de iniciar."
        caracteristica_especial = "✓ Acceso Controlado: Conocemos protocolos de seguridad, llegamos identificados profesionalmente."
        contador_premium += 1
    else:
        hero_subtitle = f"Servicio confiable de plomería en {name}. Más de 10 años de experiencia. Atención profesional, rápida y con garantía. Llegada en 20-40 minutos. Disponibles 24/7."
        pricing_min = "800"
        pricing_max = "2000"
        pricing_text = f"Los precios son transparentes y justos. Reparación de fuga desde $500, destape desde $350, cambio de WC desde $700. Te damos presupuesto exacto antes de iniciar. Sin costos ocultos."
        caracteristica_especial = "✓ Precios Justos: Tarifas competitivas sin comprometer la calidad del servicio."

    # 3. Actualizar hero subtitle
    pattern_hero = r'(<p class="hero-subtitle fade-in">)[^<]+(</p>)'
    content = re.sub(pattern_hero, r'\1' + hero_subtitle + r'\2', content)

    # 4. Actualizar pricing en Service Schema
    pattern_precio_min = r'"minPrice": "\d+"'
    pattern_precio_max = r'"maxPrice": "\d+"'
    content = re.sub(pattern_precio_min, f'"minPrice": "{pricing_min}"', content)
    content = re.sub(pattern_precio_max, f'"maxPrice": "{pricing_max}"', content)

    # 5. Actualizar texto de precios en FAQ
    pattern_pricing_faq = r'(<h3>¿Cuánto cobran por servicio en [^<]+</h3>\s*<p>)[^<]+(</p>)'
    content = re.sub(
        r'(<h3>¿Cuánto cobran por servicio en )[^<]+(</h3>\s*<p>)[^<]+(</p>)',
        r'\1' + name + r'\2' + pricing_text + r'\3',
        content
    )

    # 6. Actualizar característica especial
    pattern_acceso = r'<p><strong>✓ Acceso Controlado:[^<]+</strong></p>'
    if not es_premium:
        content = re.sub(pattern_acceso, f'<p><strong>{caracteristica_especial}</strong></p>', content)

    # 7. Actualizar mensaje WhatsApp
    wa_msg = f"Hola, necesito un plomero en {name}, Culiacán"
    pattern_wa = r'var waMsg="[^"]+";'
    content = re.sub(pattern_wa, f'var waMsg="{wa_msg}";', content)

    # 8. Actualizar colonia en tracking
    pattern_colonia_track = r'colonia:"[^"]+"'
    content = re.sub(pattern_colonia_track, f'colonia:"{slug}"', content)

    # 9. Actualizar copyright
    pattern_copyright = r'(&copy; 2025 Plomero Culiacán Pro\. Servicio especializado en )[^<]+(\.</p>)'
    content = re.sub(pattern_copyright, r'\1' + name + r'\2', content)

    # Escribir archivo
    output_file = colonia_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    tipo = "PREMIUM" if es_premium else "ESTÁNDAR"
    print(f"✅ {name:30} [{tipo}] → {slug}/")
    contador_creadas += 1

print(f"\n{'='*70}")
print(f"📊 RESUMEN DE CREACIÓN:")
print(f"  ✅ Colonias creadas: {contador_creadas}/{len(nuevas_colonias)}")
print(f"  ⭐ Premium: {contador_premium}")
print(f"  📋 Estándar: {contador_creadas - contador_premium}")
print(f"{'='*70}")

print(f"\n📁 ESTRUCTURA GENERADA:")
for colonia in nuevas_colonias:
    print(f"  servicios/plomero-colonias-culiacan/{colonia['slug']}/index.html")

print(f"\n✨ CARACTERÍSTICAS IMPLEMENTADAS:")
print(f"  ✅ Estructura IDÉNTICA a Las Quintas")
print(f"  ✅ NAP + Mapa incluidos")
print(f"  ✅ 3 Schemas (BreadcrumbList, FAQPage, Service)")
print(f"  ✅ Pricing personalizado (premium vs estándar)")
print(f"  ✅ WhatsApp tracking por colonia")
print(f"  ✅ SEO optimizado por colonia")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"  1. Commit y push de las 15 nuevas páginas")
print(f"  2. Actualizar sitemap")
print(f"  3. Indexar en Google Search Console")
print(f"  4. Total de colonias: 45 (30 + 15)")
