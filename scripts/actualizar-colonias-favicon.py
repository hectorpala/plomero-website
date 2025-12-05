#!/usr/bin/env python3
"""
Script para actualizar las colonias antiguas con los favicons completos.
Agrega favicon-32x32.png y apple-touch-icon a las colonias que solo tienen favicon.ico
"""

import os
import glob

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

# Líneas a buscar y reemplazar
OLD_FAVICON = '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="stylesheet"'

NEW_FAVICON = '''<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
<link rel="stylesheet"'''

def main():
    # Encontrar todos los archivos index.html en colonias
    pattern = os.path.join(COLONIAS_DIR, "*/index.html")
    files = glob.glob(pattern)

    updated = 0
    skipped = 0

    print(f"📁 Encontrados {len(files)} archivos de colonias")
    print("=" * 50)

    for filepath in sorted(files):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si ya tiene los favicons completos
        if 'favicon-32x32.png' in content:
            skipped += 1
            continue

        # Verificar si tiene la estructura antigua
        if OLD_FAVICON in content:
            new_content = content.replace(OLD_FAVICON, NEW_FAVICON)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            colonia = filepath.split('/')[-2]
            print(f"  ✅ {colonia}")
            updated += 1
        else:
            colonia = filepath.split('/')[-2]
            print(f"  ⚠️  {colonia} - estructura diferente")

    print("=" * 50)
    print(f"✅ Actualizadas: {updated}")
    print(f"⏭️  Ya tenían favicons: {skipped}")
    print(f"📊 Total procesados: {len(files)}")

if __name__ == "__main__":
    main()
