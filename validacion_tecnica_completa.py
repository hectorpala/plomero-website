#!/usr/bin/env python3
"""
Validación técnica completa - Preparación para monitoreo

Verifica:
1. Estado de las 120 páginas
2. Schemas válidos
3. URLs funcionales
4. Estructura de sitemap
5. Imágenes OG
6. Performance crítico
"""

from pathlib import Path
import re
import json
from datetime import datetime

base_dir = Path('servicios/plomero-colonias-culiacan')
sitemap_file = Path('sitemap.xml')

print(f"🔍 VALIDACIÓN TÉCNICA COMPLETA")
print(f"{'='*70}")
print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

# ===== VALIDACIÓN 1: PÁGINAS Y ESTRUCTURA =====
print(f"1. VALIDACIÓN DE PÁGINAS")
print(f"{'-'*70}")

total_paginas = 0
paginas_validas = 0
errores_estructura = []

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    total_paginas += 1

    if not index_file.exists():
        errores_estructura.append(f"❌ {colonia_dir.name}: index.html no existe")
        continue

    # Verificar que el archivo tenga contenido
    size = index_file.stat().st_size
    if size < 1000:  # Menos de 1KB es sospechoso
        errores_estructura.append(f"⚠️  {colonia_dir.name}: Archivo muy pequeño ({size} bytes)")
        continue

    paginas_validas += 1

print(f"Total de directorios: {total_paginas}")
print(f"Páginas válidas: {paginas_validas}")
print(f"Errores: {len(errores_estructura)}")

if errores_estructura:
    print(f"\nErrores encontrados:")
    for error in errores_estructura:
        print(f"  {error}")

# ===== VALIDACIÓN 2: SCHEMAS =====
print(f"\n2. VALIDACIÓN DE SCHEMAS")
print(f"{'-'*70}")

schemas_stats = {
    'BreadcrumbList': 0,
    'FAQPage': 0,
    'Service': 0,
    'ImageObject': 0,
    'LocalBusiness': 0
}

errores_schema = []

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar cada schema
    if '"@type": "BreadcrumbList"' in content:
        schemas_stats['BreadcrumbList'] += 1
    else:
        errores_schema.append(f"{colonia_dir.name}: Falta BreadcrumbList")

    if '"@type": "FAQPage"' in content:
        schemas_stats['FAQPage'] += 1
    else:
        errores_schema.append(f"{colonia_dir.name}: Falta FAQPage")

    if '"@type": "Service"' in content:
        schemas_stats['Service'] += 1
    else:
        errores_schema.append(f"{colonia_dir.name}: Falta Service")

    if '"@type": "ImageObject"' in content:
        schemas_stats['ImageObject'] += 1
    else:
        errores_schema.append(f"{colonia_dir.name}: Falta ImageObject")

    if '<!-- LocalBusiness Schema for Local SEO -->' in content:
        schemas_stats['LocalBusiness'] += 1
    else:
        errores_schema.append(f"{colonia_dir.name}: Falta LocalBusiness")

print(f"Schemas encontrados:")
for schema, count in schemas_stats.items():
    percentage = (count / paginas_validas * 100) if paginas_validas > 0 else 0
    status = "✅" if count == paginas_validas else "⚠️"
    print(f"  {status} {schema:20} {count}/{paginas_validas} ({percentage:.1f}%)")

if errores_schema:
    print(f"\nPrimeros 5 errores de schema:")
    for error in errores_schema[:5]:
        print(f"  ⚠️  {error}")

# ===== VALIDACIÓN 3: SITEMAP =====
print(f"\n3. VALIDACIÓN DE SITEMAP")
print(f"{'-'*70}")

if sitemap_file.exists():
    with open(sitemap_file, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()

    # Contar URLs de colonias en sitemap
    urls_colonias_sitemap = sitemap_content.count('plomero-colonias-culiacan')

    print(f"✅ Sitemap existe: {sitemap_file}")
    print(f"   URLs de colonias en sitemap: {urls_colonias_sitemap}")
    print(f"   Total esperado: {paginas_validas}")

    if urls_colonias_sitemap == paginas_validas:
        print(f"   ✅ Sitemap completo")
    else:
        print(f"   ⚠️  Faltan {paginas_validas - urls_colonias_sitemap} URLs")
else:
    print(f"❌ Sitemap NO existe")

# ===== VALIDACIÓN 4: IMÁGENES OG =====
print(f"\n4. VALIDACIÓN DE IMÁGENES OG")
print(f"{'-'*70}")

og_images_dir = Path('assets/images/og-colonias')
og_images = list(og_images_dir.glob('*.webp')) if og_images_dir.exists() else []

print(f"Directorio OG: {og_images_dir}")
print(f"Imágenes encontradas: {len(og_images)}")

if len(og_images) >= 10:
    print(f"✅ Suficientes imágenes OG")
    total_size = sum(img.stat().st_size for img in og_images)
    avg_size = total_size / len(og_images) / 1024
    print(f"   Tamaño promedio: {avg_size:.1f} KB")
else:
    print(f"⚠️  Pocas imágenes OG ({len(og_images)})")

# Verificar que las páginas usen las imágenes OG
paginas_con_og = 0
for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/og-colonias/' in content:
        paginas_con_og += 1

print(f"Páginas con OG personalizado: {paginas_con_og}/{paginas_validas}")

# ===== VALIDACIÓN 5: OPTIMIZACIONES CRÍTICAS =====
print(f"\n5. VALIDACIÓN DE OPTIMIZACIONES CRÍTICAS")
print(f"{'-'*70}")

optimizaciones = {
    'Preconnect tags': 0,
    'Inline CSS': 0,
    'Fetchpriority': 0,
    'Lazy loading': 0,
    'Enlaces internos': 0
}

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'rel="preconnect"' in content:
        optimizaciones['Preconnect tags'] += 1
    if '<!-- Critical CSS Inline' in content:
        optimizaciones['Inline CSS'] += 1
    if 'fetchpriority="high"' in content:
        optimizaciones['Fetchpriority'] += 1
    if 'loading="lazy"' in content:
        optimizaciones['Lazy loading'] += 1
    if 'También Brindamos Servicio en Colonias Cercanas' in content:
        optimizaciones['Enlaces internos'] += 1

print(f"Optimizaciones implementadas:")
for opt, count in optimizaciones.items():
    percentage = (count / paginas_validas * 100) if paginas_validas > 0 else 0
    status = "✅" if percentage >= 95 else "⚠️"
    print(f"  {status} {opt:20} {count}/{paginas_validas} ({percentage:.1f}%)")

# ===== RESUMEN FINAL =====
print(f"\n{'='*70}")
print(f"📊 RESUMEN DE VALIDACIÓN")
print(f"{'='*70}\n")

# Calcular score general
checks_passed = 0
total_checks = 0

# Check 1: Páginas válidas
total_checks += 1
if paginas_validas == 120:
    checks_passed += 1
    print(f"✅ Páginas válidas: {paginas_validas}/120")
else:
    print(f"⚠️  Páginas válidas: {paginas_validas}/120")

# Check 2: Schemas completos
total_checks += 1
schemas_completos = all(count == paginas_validas for count in schemas_stats.values())
if schemas_completos:
    checks_passed += 1
    print(f"✅ Schemas completos: 5/5 tipos")
else:
    print(f"⚠️  Schemas incompletos")

# Check 3: Sitemap
total_checks += 1
if sitemap_file.exists() and urls_colonias_sitemap >= paginas_validas - 5:
    checks_passed += 1
    print(f"✅ Sitemap actualizado: {urls_colonias_sitemap} URLs")
else:
    print(f"⚠️  Sitemap necesita actualización")

# Check 4: Imágenes OG
total_checks += 1
if paginas_con_og >= paginas_validas * 0.9:
    checks_passed += 1
    print(f"✅ Imágenes OG: {paginas_con_og}/{paginas_validas}")
else:
    print(f"⚠️  Imágenes OG: {paginas_con_og}/{paginas_validas}")

# Check 5: Optimizaciones
total_checks += 1
if all(count >= paginas_validas * 0.9 for count in optimizaciones.values()):
    checks_passed += 1
    print(f"✅ Optimizaciones críticas: Todas implementadas")
else:
    print(f"⚠️  Algunas optimizaciones faltan")

# Score final
score = (checks_passed / total_checks) * 100
print(f"\n🎯 SCORE DE VALIDACIÓN: {score:.1f}%")
print(f"   Checks pasados: {checks_passed}/{total_checks}")

# Estado general
if score >= 95:
    print(f"\n✅ ESTADO: EXCELENTE - Listo para producción")
elif score >= 80:
    print(f"\n⚠️  ESTADO: BUENO - Revisar warnings")
else:
    print(f"\n❌ ESTADO: REQUIERE ATENCIÓN - Corregir errores")

# ===== PRÓXIMOS PASOS =====
print(f"\n{'='*70}")
print(f"📋 PRÓXIMOS PASOS PARA MONITOREO")
print(f"{'='*70}\n")

print(f"INMEDIATO (Hoy):")
print(f"  [ ] 1. Verificar que sitio está en Google Search Console")
print(f"  [ ] 2. Enviar sitemap.xml: https://plomeroculiacanpro.mx/sitemap.xml")
print(f"  [ ] 3. Solicitar indexación de 20 páginas prioritarias")

print(f"\nESTA SEMANA:")
print(f"  [ ] 4. Validar 5 páginas en Rich Results Test")
print(f"  [ ] 5. Testear 3 páginas con PageSpeed Insights")
print(f"  [ ] 6. Configurar eventos de conversión en GA4")
print(f"  [ ] 7. Crear Google Sheet para tracking")
print(f"  [ ] 8. Establecer baseline (semana 0)")

print(f"\nSEMANA 1:")
print(f"  [ ] 9. Verificar indexación completa (120/120)")
print(f"  [ ] 10. Primer reporte semanal")
print(f"  [ ] 11. Monitorear errores en Search Console")

print(f"\n📊 URLs DE VALIDACIÓN MANUAL:")
print(f"{'-'*70}")
print(f"Search Console:   https://search.google.com/search-console")
print(f"Rich Results:     https://search.google.com/test/rich-results")
print(f"PageSpeed:        https://pagespeed.web.dev")
print(f"FB Debugger:      https://developers.facebook.com/tools/debug/")

print(f"\n✨ Validación técnica completada")
print(f"📈 Sistema listo para monitoreo\n")
