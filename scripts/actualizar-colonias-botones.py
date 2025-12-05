#!/usr/bin/env python3
"""
Script para actualizar los botones flotantes de las colonias al estilo de la homepage.
Cambia de cta-btn/cta-bar a floating-btn circulares con SVG.
"""

import os
import glob
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

# Nuevos estilos y botones (formato homepage)
NEW_STYLES = '<style>.floating-btn{position:fixed;right:18px;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:1.1rem;box-shadow:0 10px 28px rgba(0,0,0,0.16);transition:transform .12s ease,box-shadow .12s ease,filter .12s ease;z-index:60;text-decoration:none}.floating-btn:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,0.2);filter:brightness(1.05)}.floating-call{background:#0f4fa8;bottom:18px}.floating-whatsapp{background:#22c55e;bottom:78px}</style>'

WHATSAPP_SVG = '<svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'

PHONE_SVG = '<svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/></svg>'

def get_colonia_name_from_path(filepath):
    """Extrae el nombre de colonia del path"""
    parts = filepath.split('/')
    return parts[-2]

def get_colonia_display_name(content):
    """Extrae el nombre de display de la colonia del título"""
    match = re.search(r'<title>Plomero en ([^,]+),', content)
    if match:
        return match.group(1)
    return None

def create_new_buttons(colonia_name):
    """Crea el HTML de los nuevos botones flotantes"""
    # URL encode el nombre para WhatsApp
    wa_name = colonia_name.replace(' ', '%20')

    wa_button = f'<a href="https://wa.me/526673922273?text=Hola%2C%20necesito%20un%20plomero%20en%20{wa_name}" class="floating-btn floating-whatsapp" target="_blank" rel="noopener noreferrer" aria-label="Contactar por WhatsApp">{WHATSAPP_SVG}</a>'

    phone_button = f'<a href="tel:+526673922273" class="floating-btn floating-call" aria-label="Llamar ahora">{PHONE_SVG}</a>'

    return f'{NEW_STYLES}\n{wa_button}\n{phone_button}'

def main():
    pattern = os.path.join(COLONIAS_DIR, "*/index.html")
    files = glob.glob(pattern)

    updated = 0
    skipped = 0
    errors = 0

    print(f"Actualizando botones en {len(files)} colonias...")
    print("=" * 50)

    for filepath in sorted(files):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ya tiene floating-btn? Skip
        if 'floating-btn' in content:
            skipped += 1
            continue

        # Verificar que tiene el estilo antiguo
        if 'cta-bar' not in content and 'cta-btn' not in content:
            colonia = get_colonia_name_from_path(filepath)
            print(f"  ⚠️  {colonia} - sin botones CTA")
            errors += 1
            continue

        # Obtener nombre de colonia del título
        colonia_name = get_colonia_display_name(content)
        if not colonia_name:
            colonia = get_colonia_name_from_path(filepath)
            print(f"  ⚠️  {colonia} - no se pudo extraer nombre")
            errors += 1
            continue

        # Patrón más flexible para el bloque de estilos CTA
        style_pattern = r'<style>\.cta-bar\{[^}]+\}[^<]*</style>'

        # Patrón más flexible para el div de botones (con o sin id)
        div_pattern = r'<div class="cta-bar">.*?</div>'

        new_buttons = create_new_buttons(colonia_name)

        # Primero eliminar el div de botones
        new_content = re.sub(div_pattern, '', content, flags=re.DOTALL)

        # Luego reemplazar el estilo
        new_content = re.sub(style_pattern, new_buttons, new_content, flags=re.DOTALL)

        if new_content == content:
            colonia = get_colonia_name_from_path(filepath)
            print(f"  ⚠️  {colonia} - no se pudo reemplazar")
            errors += 1
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        colonia = get_colonia_name_from_path(filepath)
        print(f"  ✅ {colonia}")
        updated += 1

    print("=" * 50)
    print(f"✅ Actualizadas: {updated}")
    print(f"⏭️  Ya tenían floating-btn: {skipped}")
    print(f"⚠️  Errores: {errors}")
    print(f"📊 Total: {len(files)}")

if __name__ == "__main__":
    main()
