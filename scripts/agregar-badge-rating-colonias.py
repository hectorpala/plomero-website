#!/usr/bin/env python3
"""
Script para agregar el badge visual de Google Rating al hero de las colonias.
"""

import os
import glob
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

# Badge HTML con logo de Google y estrellas
RATING_BADGE_HTML = '''<div class="hero-rating"><svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg><span class="rating-stars">★★★★★</span><span class="rating-score">4.8/5</span><span class="rating-divider">·</span><span class="rating-count">150+ reseñas en Google</span></div>'''

# CSS para el badge (se agrega a los estilos existentes del breadcrumb)
RATING_CSS = '''.hero-rating{display:inline-flex;align-items:center;gap:0.5rem;margin:1rem 0;padding:0.6rem 1rem;background:#fff;border-radius:50px;box-shadow:0 2px 8px rgba(0,0,0,0.1);font-size:0.85rem;border:1px solid rgba(66,133,244,0.15)}.google-logo{width:18px;height:18px;flex-shrink:0}.rating-stars{color:#FBBC04;font-size:1rem;letter-spacing:1px}.rating-score{font-weight:700;color:#1a73e8;font-size:0.95rem}.rating-divider{color:#dadce0;margin:0 0.15rem}.rating-count{color:#5f6368;font-size:0.8rem}'''

def main():
    pattern = os.path.join(COLONIAS_DIR, "*/index.html")
    files = glob.glob(pattern)

    updated = 0
    skipped = 0
    errors = 0

    print(f"Agregando badge de rating a {len(files)} colonias...")
    print("=" * 50)

    for filepath in sorted(files):
        slug = filepath.split('/')[-2]

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ya tiene hero-rating? Skip
        if 'hero-rating' in content:
            skipped += 1
            continue

        # Buscar el patrón del H1 para insertar después
        # El H1 termina con </h1> y luego viene <p class="hero-subtitle
        h1_pattern = r'(</h1>)(<p class="hero-subtitle)'

        if not re.search(h1_pattern, content):
            # Intentar otro patrón
            h1_pattern2 = r'(class="fade-in">Plomero en [^<]+</h1>)(<p class="hero-subtitle)'
            if not re.search(h1_pattern2, content):
                print(f"  ⚠️  {slug} - no se encontró patrón H1")
                errors += 1
                continue
            h1_pattern = h1_pattern2

        # Insertar el badge después del H1
        new_content = re.sub(
            h1_pattern,
            f'\\1{RATING_BADGE_HTML}\\2',
            content
        )

        # Agregar CSS al bloque de estilos del breadcrumb
        if '.breadcrumb{' in new_content and '.hero-rating{' not in new_content:
            new_content = new_content.replace(
                '.breadcrumb-separator{margin:0 8px;color:#6c757d}</style>',
                f'.breadcrumb-separator{{margin:0 8px;color:#6c757d}}{RATING_CSS}</style>'
            )

        if new_content == content:
            print(f"  ⚠️  {slug} - no se pudo insertar")
            errors += 1
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ {slug}")
        updated += 1

    print("=" * 50)
    print(f"✅ Actualizadas: {updated}")
    print(f"⏭️  Ya tenían badge: {skipped}")
    print(f"⚠️  Errores: {errors}")
    print(f"📊 Total: {len(files)}")

if __name__ == "__main__":
    main()
