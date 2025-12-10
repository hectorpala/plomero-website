#!/usr/bin/env python3
"""
Script para estandarizar los favicons de las colonias al mismo nivel que la homepage.
"""

import os
import glob
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

# Favicons actuales (básicos)
OLD_FAVICONS = '''<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">'''

# Favicons completos (como homepage)
NEW_FAVICONS = '''<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/icons/icon-512.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="152x152" href="/assets/icons/icon-152.png">
<link rel="apple-touch-icon" sizes="144x144" href="/assets/icons/icon-144.png">
<link rel="apple-touch-icon" sizes="128x128" href="/assets/icons/icon-128.png">
<link rel="apple-touch-icon" sizes="96x96" href="/assets/icons/icon-96.png">
<link rel="apple-touch-icon" sizes="72x72" href="/assets/icons/icon-72.png">
<link rel="manifest" href="/manifest.json">'''

def main():
    pattern = os.path.join(COLONIAS_DIR, "*/index.html")
    files = glob.glob(pattern)

    updated = 0
    skipped = 0
    errors = 0

    print(f"Estandarizando favicons en {len(files)} colonias...")
    print("=" * 50)

    for filepath in sorted(files):
        slug = filepath.split('/')[-2]

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ya tiene manifest.json? Probablemente ya está completo
        if 'rel="manifest"' in content:
            skipped += 1
            continue

        # Buscar el patrón de favicons básicos
        # Patrón flexible para diferentes formatos
        old_pattern = r'<link rel="icon" href="/favicon\.ico" sizes="any">\s*<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32\.png">\s*<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon\.png">'

        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, NEW_FAVICONS, content)
        else:
            # Intentar reemplazo línea por línea
            if '<link rel="icon" href="/favicon.ico" sizes="any">' in content:
                # Reemplazar solo la primera línea y agregar el resto
                new_content = content.replace(
                    '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">\n<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">',
                    NEW_FAVICONS
                )
                if new_content == content:
                    print(f"  ⚠️  {slug} - patrón no coincide")
                    errors += 1
                    continue
            else:
                print(f"  ⚠️  {slug} - sin favicon.ico")
                errors += 1
                continue

        if new_content == content:
            print(f"  ⚠️  {slug} - sin cambios")
            errors += 1
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ {slug}")
        updated += 1

    print("=" * 50)
    print(f"✅ Actualizadas: {updated}")
    print(f"⏭️  Ya completas: {skipped}")
    print(f"⚠️  Errores: {errors}")
    print(f"📊 Total: {len(files)}")

if __name__ == "__main__":
    main()
