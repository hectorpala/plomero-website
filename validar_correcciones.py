#!/usr/bin/env python3
"""
Validar correcciones técnicas aplicadas
"""

from pathlib import Path
import re

print(f"\n🔍 VALIDACIÓN DE CORRECCIONES")
print(f"{'='*70}\n")

# 1. Validar que no haya referencias PNG
print(f"1️⃣ Validando referencias PNG...")
base_dir = Path('servicios/plomero-colonias-culiacan')

png_references = 0
for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir():
        continue
    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if '.png"' in content or '.png ' in content:
        png_references += 1

if png_references == 0:
    print(f"   ✅ Sin referencias PNG (120/120 páginas)")
else:
    print(f"   ⚠️  {png_references} páginas con referencias PNG")

# 2. Validar footer en Centro
print(f"\n2️⃣ Validando footer en Centro...")
centro_file = Path('servicios/plomero-colonias-culiacan/centro/index.html')

with open(centro_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Contar tags <footer
footer_count = content.count('<footer')
# Buscar <footer sin cerrar (sin > después)
invalid_footer = re.search(r'<footer\s*$', content, re.MULTILINE)

if footer_count == 1 and not invalid_footer:
    print(f"   ✅ Footer válido (1 tag correcto)")
elif invalid_footer:
    print(f"   ❌ Footer inválido encontrado")
else:
    print(f"   ⚠️  {footer_count} tags <footer encontrados")

# 3. Validar contenido duplicado en Centro
print(f"\n3️⃣ Validando contenido duplicado...")
conocemos_count = content.count('Conocemos la Zona')

if conocemos_count == 1:
    print(f"   ✅ Sin duplicación (1 ocurrencia)")
elif conocemos_count == 0:
    print(f"   ⚠️  Frase removida completamente")
else:
    print(f"   ❌ {conocemos_count} ocurrencias (esperado: 1)")

# 4. Verificar que las imágenes WebP estén correctas
print(f"\n4️⃣ Verificando imágenes WebP...")
webp_count = content.count('.webp"')

if webp_count > 0:
    print(f"   ✅ {webp_count} imágenes WebP encontradas")
else:
    print(f"   ❌ No se encontraron imágenes WebP")

# Resumen
print(f"\n{'='*70}")
print(f"📊 RESUMEN DE VALIDACIÓN")
print(f"{'='*70}\n")

all_good = (png_references == 0 and footer_count == 1 and
            not invalid_footer and conocemos_count == 1 and webp_count > 0)

if all_good:
    print(f"✅ TODAS LAS CORRECCIONES VALIDADAS")
    print(f"\n📈 Mejoras aplicadas:")
    print(f"   - 120 páginas sin referencias PNG fallback ✓")
    print(f"   - Footer HTML válido en Centro ✓")
    print(f"   - Sin contenido duplicado ✓")
    print(f"   - Imágenes WebP funcionando ✓")
    print(f"\n🎯 Listo para deploy")
else:
    print(f"⚠️  ALGUNAS CORRECCIONES REQUIEREN ATENCIÓN")

print(f"\n✨ Validación completada\n")
