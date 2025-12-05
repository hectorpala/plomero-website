#!/usr/bin/env python3
"""
Script para agregar badge de rating a las colonias antiguas con estructura diferente.
"""

import os
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

COLONIAS_FALTANTES = [
    "campestre", "revolucion", "bosques-del-humaya", "vista-hermosa",
    "lazaro-cardenas", "miguel-hidalgo", "real-del-valle", "chulavista",
    "infonavit-humaya", "burocrata", "21-de-marzo", "independencia",
    "isla-del-oeste", "luis-donaldo-colosio", "lomas-de-san-isidro",
    "terranova", "colinas-de-la-rivera", "recursos-hidraulicos",
    "alturas-del-sur", "gabriel-leyva", "real-san-angel", "lombardo-toledano",
    "hacienda-del-valle", "francisco-villa", "hacienda-los-huertos",
    "tres-rios", "antonio-toledo-corro", "country-tres-rios", "altamira",
    "humaya", "benito-juarez", "portales-del-rio", "cumbres-tres-rios",
    "6-de-enero", "zona-dorada", "universitaria", "emiliano-zapata"
]

RATING_BADGE_HTML = '<div class="hero-rating"><svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg><span class="rating-stars">★★★★★</span><span class="rating-score">4.8/5</span><span class="rating-divider">·</span><span class="rating-count">150+ reseñas en Google</span></div>'

RATING_CSS = '.hero-rating{display:inline-flex;align-items:center;gap:0.5rem;margin:1rem 0;padding:0.6rem 1rem;background:#fff;border-radius:50px;box-shadow:0 2px 8px rgba(0,0,0,0.1);font-size:0.85rem;border:1px solid rgba(66,133,244,0.15)}.google-logo{width:18px;height:18px;flex-shrink:0}.rating-stars{color:#FBBC04;font-size:1rem;letter-spacing:1px}.rating-score{font-weight:700;color:#1a73e8;font-size:0.95rem}.rating-divider{color:#dadce0;margin:0 0.15rem}.rating-count{color:#5f6368;font-size:0.8rem}'

def main():
    print(f"Agregando badge a {len(COLONIAS_FALTANTES)} colonias antiguas...")
    print("=" * 50)

    updated = 0
    errors = 0

    for slug in COLONIAS_FALTANTES:
        filepath = f"{COLONIAS_DIR}/{slug}/index.html"

        if not os.path.exists(filepath):
            print(f"  ❌ {slug} - no existe")
            errors += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'hero-rating' in content:
            print(f"  ⏭️  {slug} - ya tiene badge")
            continue

        # Patrón flexible: buscar </h1> seguido de espacios/saltos y <p class="hero-subtitle
        pattern = r'(</h1>)\s*(<p class="hero-subtitle)'

        if re.search(pattern, content):
            new_content = re.sub(pattern, f'\\1\n{RATING_BADGE_HTML}\n\\2', content)
        else:
            # Otro intento: buscar </h1> y cualquier cosa antes de hero-subtitle
            pattern2 = r'(</h1>)(.*?)(<p class="hero-subtitle)'
            match = re.search(pattern2, content, re.DOTALL)
            if match:
                between = match.group(2)
                if len(between.strip()) < 50:  # Solo si no hay mucho contenido entre ellos
                    new_content = re.sub(pattern2, f'\\1\n{RATING_BADGE_HTML}\\2\\3', content, flags=re.DOTALL)
                else:
                    print(f"  ⚠️  {slug} - contenido inesperado entre H1 y subtitle")
                    errors += 1
                    continue
            else:
                print(f"  ⚠️  {slug} - no se encontró patrón")
                errors += 1
                continue

        # Agregar CSS si no existe
        if '.hero-rating{' not in new_content:
            # Buscar el cierre de algún bloque style existente
            if '</style>' in new_content:
                # Insertar antes del primer </style>
                new_content = new_content.replace('</style>', f'{RATING_CSS}</style>', 1)

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
