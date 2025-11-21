#!/usr/bin/env python3
"""
Script para agregar breadcrumbs visuales a todas las páginas.
Extrae la información del BreadcrumbList schema existente en JSON-LD.

Mejora UX y muestra breadcrumbs en Google Search Results.
"""

import os
import re
import json
from pathlib import Path

# CSS para breadcrumbs (se agregará inline en cada página)
BREADCRUMB_CSS = """
    <style>
    .breadcrumb {
        background: #f8f9fa;
        padding: 12px 0;
        font-size: 14px;
        border-bottom: 1px solid #e9ecef;
    }
    .breadcrumb-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .breadcrumb-list {
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        padding: 0;
        flex-wrap: wrap;
    }
    .breadcrumb-item {
        display: flex;
        align-items: center;
    }
    .breadcrumb-item a {
        color: #0066cc;
        text-decoration: none;
        transition: color 0.2s;
    }
    .breadcrumb-item a:hover {
        color: #004499;
        text-decoration: underline;
    }
    .breadcrumb-item.active {
        color: #6c757d;
    }
    .breadcrumb-separator {
        margin: 0 8px;
        color: #6c757d;
        user-select: none;
    }
    @media (max-width: 768px) {
        .breadcrumb {
            font-size: 13px;
            padding: 10px 0;
        }
        .breadcrumb-separator {
            margin: 0 6px;
        }
    }
    </style>
"""

def extract_breadcrumbs_from_jsonld(html_content):
    """Extrae breadcrumbs del BreadcrumbList schema."""
    # Buscar el JSON-LD
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        return None

    try:
        schema_data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

    # Buscar BreadcrumbList en @graph
    if '@graph' not in schema_data:
        return None

    breadcrumb_list = None
    for item in schema_data['@graph']:
        if item.get('@type') == 'BreadcrumbList':
            breadcrumb_list = item
            break

    if not breadcrumb_list or 'itemListElement' not in breadcrumb_list:
        return None

    return breadcrumb_list['itemListElement']

def create_breadcrumb_html(items):
    """Crea el HTML de breadcrumbs a partir de los items del schema."""
    if not items:
        return ""

    breadcrumb_items = []

    for i, item in enumerate(items):
        name = item.get('name', '')
        url = item.get('item', '')
        is_last = (i == len(items) - 1)

        if is_last:
            # Último item (página actual) - sin enlace
            breadcrumb_items.append(
                f'            <li class="breadcrumb-item active" aria-current="page">{name}</li>'
            )
        else:
            # Items anteriores - con enlace
            breadcrumb_items.append(
                f'            <li class="breadcrumb-item"><a href="{url}">{name}</a></li>\n'
                f'            <li class="breadcrumb-separator" aria-hidden="true">›</li>'
            )

    html = f"""    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb" aria-label="breadcrumb">
        <div class="breadcrumb-container">
            <ol class="breadcrumb-list">
{chr(10).join(breadcrumb_items)}
            </ol>
        </div>
    </nav>
"""

    return html

def add_breadcrumbs_to_page(file_path):
    """Agrega breadcrumbs visuales a una página."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si ya tiene breadcrumbs visuales
    if '<nav class="breadcrumb"' in content or 'class="breadcrumb-list"' in content:
        return False, "Ya tiene breadcrumbs visuales"

    # Extraer breadcrumbs del JSON-LD
    breadcrumb_items = extract_breadcrumbs_from_jsonld(content)

    if not breadcrumb_items:
        return False, "No tiene BreadcrumbList schema"

    # Crear HTML de breadcrumbs
    breadcrumb_html = create_breadcrumb_html(breadcrumb_items)

    # Agregar CSS en el <head> antes de </head>
    if BREADCRUMB_CSS not in content:
        content = content.replace('</head>', f'{BREADCRUMB_CSS}\n</head>')

    # Insertar breadcrumbs después de </nav> pero antes de <header> o <main>
    # Patrón: encontrar el cierre de nav y el inicio de header/main
    nav_pattern = r'(</nav>\s*\n)'

    match = re.search(nav_pattern, content)
    if match:
        insert_position = match.end()
        content = content[:insert_position] + '\n' + breadcrumb_html + content[insert_position:]
    else:
        return False, "No se encontró </nav> para insertar breadcrumbs"

    # Escribir archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True, f"{len(breadcrumb_items)} items"

def process_directory(directory_pattern):
    """Procesa todas las páginas en un directorio."""
    files = list(Path('.').glob(directory_pattern))

    added = 0
    skipped = 0
    errors = 0

    for file_path in files:
        try:
            success, message = add_breadcrumbs_to_page(str(file_path))

            if success:
                # Obtener nombre legible
                parts = str(file_path).split('/')
                if len(parts) >= 2:
                    page_name = parts[-2].replace('-', ' ').title()
                else:
                    page_name = str(file_path)

                print(f"✓ {page_name} - Breadcrumbs agregadas ({message})")
                added += 1
            else:
                if "Ya tiene breadcrumbs" in message:
                    skipped += 1
                else:
                    errors += 1
        except Exception as e:
            print(f"✗ {file_path} - Error: {str(e)}")
            errors += 1

    return added, skipped, errors

def main():
    """Procesa todas las páginas del sitio."""
    print("🍞 Agregando breadcrumbs visuales para mejor UX y SEO\n")

    total_added = 0
    total_skipped = 0
    total_errors = 0

    # 1. Páginas de servicios principales
    print("📍 Procesando servicios principales...")
    added, skipped, errors = process_directory('servicios/*/index.html')
    total_added += added
    total_skipped += skipped
    total_errors += errors
    print(f"   Agregadas: {added} | Ya existían: {skipped} | Errores: {errors}\n")

    # 2. Páginas de colonias
    print("📍 Procesando colonias...")
    added, skipped, errors = process_directory('servicios/plomero-colonias-culiacan/*/index.html')
    total_added += added
    total_skipped += skipped
    total_errors += errors
    print(f"   Agregadas: {added} | Ya existían: {skipped} | Errores: {errors}\n")

    # 3. Artículos de blog
    print("📍 Procesando blog...")
    added, skipped, errors = process_directory('blog/*/index.html')
    total_added += added
    total_skipped += skipped
    total_errors += errors
    print(f"   Agregadas: {added} | Ya existían: {skipped} | Errores: {errors}\n")

    # Resumen final
    print("=" * 60)
    print(f"✅ Proceso completado:")
    print(f"   • Total breadcrumbs agregadas: {total_added}")
    print(f"   • Ya existían: {total_skipped}")
    print(f"   • Errores: {total_errors}")
    print(f"\n📊 Beneficios:")
    print(f"   • Breadcrumbs visibles en resultados de Google")
    print(f"   • Mejor navegación para usuarios")
    print(f"   • CTR esperado: +5-10% por breadcrumbs en SERPs")
    print(f"   • Señales de jerarquía para Google")

if __name__ == "__main__":
    main()
