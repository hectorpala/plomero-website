#!/usr/bin/env python3
"""
Corregir 7 errores detectados en la página de Las Quintas
y verificar si existen en otras páginas
"""

from pathlib import Path
import re

base_dir = Path('servicios/plomero-colonias-culiacan')
las_quintas_file = base_dir / 'las-quintas' / 'index.html'

print(f"🔧 CORRECCIÓN DE ERRORES - LAS QUINTAS")
print(f"{'='*70}\n")

# Leer el archivo
with open(las_quintas_file, 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content
errores_corregidos = []

# ===== ERROR 1: Contenido duplicado - Enlaces Internos =====
print("1. Eliminando sección duplicada 'Enlaces Internos'...")

# Buscar la sección duplicada (la que aparece ANTES del body)
pattern_duplicate = r'<section style="background: #f8f9fa; padding: 40px 20px; margin: 40px 0;">.*?<h2>🏘️ También Brindamos Servicio en Colonias Cercanas</h2>.*?</section>\s*(?=.*<body)'

matches = re.findall(pattern_duplicate, content, re.DOTALL)
if matches:
    # Eliminar SOLO la primera ocurrencia (la que está fuera del body)
    content = re.sub(pattern_duplicate, '', content, count=1, flags=re.DOTALL)
    errores_corregidos.append("✅ Sección duplicada eliminada")
    print("   ✅ Sección duplicada eliminada (antes del body)")
else:
    print("   ⚠️  No se encontró sección duplicada con el patrón esperado")

# ===== ERROR 2: Footer incompleto =====
print("\n2. Corrigiendo tag <footer incompleto...")

if '<footer   ' in content or '<footer\n' in content or re.search(r'<footer\s+$', content, re.MULTILINE):
    # Buscar y reemplazar el footer incompleto
    content = re.sub(r'<footer\s+', '<footer class="footer">', content)
    errores_corregidos.append("✅ Tag <footer> corregido")
    print("   ✅ Tag <footer> corregido")
else:
    print("   ⚠️  Tag <footer> parece estar bien")

# ===== ERROR 3: Doble "Culiacán" en schemas =====
print("\n3. Corrigiendo 'Las Quintas Culiacán, Culiacán'...")

before_count = content.count('Las Quintas Culiacán, Culiacán')
content = content.replace('Las Quintas Culiacán, Culiacán', 'Las Quintas, Culiacán')
after_count = content.count('Las Quintas Culiacán, Culiacán')

if before_count > after_count:
    errores_corregidos.append(f"✅ {before_count} instancias de doble 'Culiacán' corregidas")
    print(f"   ✅ {before_count} instancias corregidas")
else:
    print("   ⚠️  No se encontró 'Las Quintas Culiacán, Culiacán'")

# ===== ERROR 4: PriceRange incorrecto =====
print("\n4. Actualizando priceRange a '$-$$'...")

# Buscar "priceRange": "$" en schemas y cambiar a "$-$$"
pattern_price = r'"priceRange":\s*"\$"'
matches_price = re.findall(pattern_price, content)

if matches_price:
    content = re.sub(pattern_price, '"priceRange": "$-$$"', content)
    errores_corregidos.append(f"✅ PriceRange actualizado ({len(matches_price)} instancias)")
    print(f"   ✅ {len(matches_price)} instancia(s) actualizada(s)")
else:
    print("   ⚠️  No se encontró priceRange con valor '$'")

# ===== ERROR 5: ReviewCount inconsistente =====
print("\n5. Estandarizando reviewCount a 150...")

# Cambiar todos los reviewCount a 150
pattern_review = r'"reviewCount":\s*"\d+"'
matches_review = re.findall(pattern_review, content)

if matches_review:
    content = re.sub(pattern_review, '"reviewCount": "150"', content)
    errores_corregidos.append(f"✅ ReviewCount estandarizado a 150 ({len(matches_review)} instancias)")
    print(f"   ✅ {len(matches_review)} instancia(s) estandarizada(s) a 150")
else:
    print("   ⚠️  No se encontró reviewCount")

# ===== ERROR 6: Dimensiones OG incorrectas =====
print("\n6. Corrigiendo dimensiones OG image (1200x630)...")

og_width_fixed = False
og_height_fixed = False

if 'og:image:width" content="800"' in content:
    content = content.replace('og:image:width" content="800"', 'og:image:width" content="1200"')
    og_width_fixed = True

if 'og:image:height" content="800"' in content:
    content = content.replace('og:image:height" content="800"', 'og:image:height" content="630"')
    og_height_fixed = True

if og_width_fixed or og_height_fixed:
    errores_corregidos.append("✅ Dimensiones OG corregidas a 1200x630")
    print(f"   ✅ Width: {'✓' if og_width_fixed else '✗'} | Height: {'✓' if og_height_fixed else '✗'}")
else:
    print("   ⚠️  Dimensiones OG no encontradas o ya correctas")

# ===== ERROR 7: Aspect ratio del mapa =====
print("\n7. Ajustando aspect ratio del mapa (28% → 56%)...")

if 'padding-bottom: 28%' in content:
    content = content.replace('padding-bottom: 28%', 'padding-bottom: 56%')
    errores_corregidos.append("✅ Aspect ratio del mapa ajustado a 56%")
    print("   ✅ Aspect ratio ajustado a 56%")
else:
    print("   ⚠️  Padding 28% no encontrado")

# ===== GUARDAR CAMBIOS =====
print(f"\n{'='*70}")
print(f"📊 RESUMEN DE CORRECCIONES")
print(f"{'='*70}\n")

if content != original_content:
    # Guardar archivo corregido
    with open(las_quintas_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Archivo actualizado: {las_quintas_file}")
    print(f"\nErrores corregidos:")
    for i, error in enumerate(errores_corregidos, 1):
        print(f"  {i}. {error}")

    print(f"\n🎯 Total de correcciones: {len(errores_corregidos)}/7")
else:
    print("⚠️  No se realizaron cambios (archivo ya estaba correcto)")

# ===== VERIFICAR OTRAS PÁGINAS =====
print(f"\n{'='*70}")
print(f"🔍 VERIFICANDO ERRORES EN OTRAS 119 PÁGINAS")
print(f"{'='*70}\n")

paginas_con_errores = []

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__' or colonia_dir.name == 'las-quintas':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        page_content = f.read()

    errores_encontrados = []

    # Verificar cada tipo de error
    if re.search(r'<section style="background: #f8f9fa.*?Enlaces Internos.*?</section>.*?<section style="background: #f8f9fa.*?Enlaces Internos.*?</section>', page_content, re.DOTALL):
        errores_encontrados.append("Contenido duplicado")

    if '<footer   ' in page_content or re.search(r'<footer\s+$', page_content, re.MULTILINE):
        errores_encontrados.append("Footer incompleto")

    if re.search(r'Culiacán, Culiacán', page_content):
        errores_encontrados.append("Doble Culiacán")

    if '"priceRange": "$"' in page_content and ('Premium' in page_content or 'Residencial' in page_content):
        errores_encontrados.append("PriceRange incorrecto")

    review_counts = re.findall(r'"reviewCount":\s*"(\d+)"', page_content)
    if len(set(review_counts)) > 1:
        errores_encontrados.append(f"ReviewCount inconsistente {set(review_counts)}")

    if 'og:image:width" content="800"' in page_content:
        errores_encontrados.append("OG width 800")

    if 'padding-bottom: 28%' in page_content:
        errores_encontrados.append("Map aspect ratio 28%")

    if errores_encontrados:
        paginas_con_errores.append({
            'colonia': colonia_dir.name,
            'errores': errores_encontrados
        })

if paginas_con_errores:
    print(f"⚠️  Se encontraron errores similares en {len(paginas_con_errores)} páginas:\n")

    # Mostrar primeras 10 páginas con errores
    for i, pagina in enumerate(paginas_con_errores[:10], 1):
        print(f"  {i}. {pagina['colonia']}")
        for error in pagina['errores']:
            print(f"      - {error}")

    if len(paginas_con_errores) > 10:
        print(f"\n  ... y {len(paginas_con_errores) - 10} páginas más")

    print(f"\n💡 RECOMENDACIÓN: Ejecutar corrección masiva en las {len(paginas_con_errores)} páginas")
else:
    print("✅ No se encontraron errores similares en otras páginas")

print(f"\n✨ Corrección de Las Quintas completada")
print(f"📋 Revisar cambios antes de continuar con corrección masiva\n")
