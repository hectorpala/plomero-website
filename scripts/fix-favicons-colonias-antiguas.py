#!/usr/bin/env python3
"""
Script para arreglar favicons en las 37 colonias antiguas con estructura diferente.
"""

import os
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

COLONIAS_ANTIGUAS = [
    "21-de-marzo", "6-de-enero", "altamira", "alturas-del-sur", "antonio-toledo-corro",
    "benito-juarez", "bosques-del-humaya", "burocrata", "campestre", "chulavista",
    "colinas-de-la-rivera", "country-tres-rios", "cumbres-tres-rios", "emiliano-zapata",
    "francisco-villa", "gabriel-leyva", "hacienda-del-valle", "hacienda-los-huertos",
    "humaya", "independencia", "infonavit-humaya", "isla-del-oeste", "lazaro-cardenas",
    "lomas-de-san-isidro", "lombardo-toledano", "luis-donaldo-colosio", "miguel-hidalgo",
    "portales-del-rio", "real-del-valle", "real-san-angel", "recursos-hidraulicos",
    "revolucion", "terranova", "tres-rios", "universitaria", "vista-hermosa", "zona-dorada"
]

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
    print(f"Arreglando favicons en {len(COLONIAS_ANTIGUAS)} colonias antiguas...")
    print("=" * 50)

    updated = 0
    errors = 0

    for slug in COLONIAS_ANTIGUAS:
        filepath = f"{COLONIAS_DIR}/{slug}/index.html"

        if not os.path.exists(filepath):
            print(f"  ❌ {slug} - no existe")
            errors += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ya tiene manifest? Skip
        if 'rel="manifest"' in content:
            print(f"  ⏭️  {slug} - ya tiene manifest")
            continue

        # Patrón flexible para colonias antiguas (con espacios/indentación)
        old_pattern = r'<link rel="icon" href="/favicon\.ico" sizes="any">\s*<link rel="icon" type="image/png"[^>]*href="/assets/icons/favicon-32x32\.png"[^>]*>\s*<link rel="apple-touch-icon"[^>]*href="/assets/icons/favicon-32x32\.png"[^>]*>'

        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, NEW_FAVICONS, content)
        else:
            # Otro patrón posible
            old_pattern2 = r'<link rel="icon" href="/favicon\.ico" sizes="any">\s*<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32\.png">\s*<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon\.png">'
            if re.search(old_pattern2, content):
                new_content = re.sub(old_pattern2, NEW_FAVICONS, content)
            else:
                print(f"  ⚠️  {slug} - patrón no reconocido")
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
    print(f"⚠️  Errores: {errors}")

if __name__ == "__main__":
    main()
