#!/usr/bin/env python3
"""
Corrige 3 problemas críticos detectados en las páginas de colonias:
1. Script tag duplicado (línea 147-148)
2. Contenido duplicado "Conocemos la Zona"
3. Font preloads faltantes en 4 páginas
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Páginas que necesitan font preloads
paginas_sin_preloads = ['centro', 'chapultepec', 'guadalupe', 'montebello']

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"🔧 CORRIGIENDO 3 PROBLEMAS CRÍTICOS\n")
print(f"{'='*70}")

# Contadores
fix1_contador = 0
fix2_contador = 0
fix3_contador = 0

for colonia_dir in sorted(colonias):
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        continue

    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    modificado = False

    # FIX #1: Eliminar script tag duplicado
    # Buscar el patrón: </script>\n</script> (después del FAQPage schema)
    pattern_script_duplicado = r'(\}\s*\]\s*\}\s*\n\s*</script>)\n\s*</script>'
    if re.search(pattern_script_duplicado, content):
        content = re.sub(pattern_script_duplicado, r'\1', content)
        fix1_contador += 1
        modificado = True
        print(f"✅ {colonia_name}: Script tag duplicado corregido")

    # FIX #2: Eliminar contenido duplicado "Conocemos la Zona"
    # Buscar dos líneas consecutivas que mencionen "Conocemos la Zona"
    pattern_duplicado = r'(<p><strong>✓ Conocemos la Zona:[^<]+</p>\s*<p><strong>✓ Experiencia Local:[^<]+</p>\s*)<p><strong>✓ Conocemos la Zona:[^<]+</p>'
    if re.search(pattern_duplicado, content):
        content = re.sub(pattern_duplicado, r'\1', content)
        fix2_contador += 1
        modificado = True
        print(f"✅ {colonia_name}: Contenido duplicado eliminado")

    # FIX #3: Agregar font preloads si faltan
    if colonia_slug in paginas_sin_preloads:
        # Verificar si ya tiene los preloads
        if 'preload' not in content or 'inter-400.woff2' not in content:
            # Buscar el cierre de </title> o viewport para insertar después
            pattern_insert = r'(<meta name="viewport" content="[^"]+">)'

            font_preloads = '''
    <!-- Preload critical fonts -->
    <link rel="preload" href="../../../assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="../../../assets/fonts/montserrat-700.woff2" as="font" type="font/woff2" crossorigin>'''

            if re.search(pattern_insert, content):
                content = re.sub(pattern_insert, r'\1' + font_preloads, content)
                fix3_contador += 1
                modificado = True
                print(f"✅ {colonia_name}: Font preloads agregados")

    # Escribir archivo si hubo modificaciones
    if modificado:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\n{'='*70}")
print(f"📊 RESUMEN DE CORRECCIONES:")
print(f"  🔧 FIX #1 - Script tag duplicado eliminado: {fix1_contador}/30 páginas")
print(f"  🔧 FIX #2 - Contenido duplicado eliminado: {fix2_contador} páginas")
print(f"  🔧 FIX #3 - Font preloads agregados: {fix3_contador}/4 páginas esperadas")
print(f"{'='*70}")

print(f"\n✨ IMPACTO ESPERADO:")
print(f"  • HTML ahora es válido (W3C compliant)")
print(f"  • Google Search Console sin errores de estructura")
print(f"  • Schemas JSON-LD procesados correctamente")
print(f"  • Mejor experiencia de usuario (sin duplicados)")
print(f"  • Core Web Vitals mejorados (LCP más rápido)")
print(f"  • PageSpeed Insights con mejor puntuación")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"  1. Commit y push de los cambios")
print(f"  2. Esperar 5-10 min para GitHub Pages")
print(f"  3. Validar HTML en validator.w3.org")
print(f"  4. Verificar en Google Search Console (24-48h)")
