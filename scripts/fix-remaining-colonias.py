#!/usr/bin/env python3
"""
Script para arreglar las colonias restantes que no fueron actualizadas.
"""

import os
import re

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

# Lista de colonias con problemas
COLONIAS_SIN_CTA = [
    "altamira", "bosques-del-humaya", "campestre", "colinas-de-la-rivera",
    "country-tres-rios", "cumbres-tres-rios", "hacienda-del-valle",
    "hacienda-los-huertos", "infonavit-humaya", "isla-del-oeste",
    "lomas-de-san-isidro", "portales-del-rio", "real-del-valle",
    "real-san-angel", "zona-dorada"
]

COLONIAS_FORMATO_DIFERENTE = [
    "benito-juarez", "francisco-villa", "humaya", "independencia",
    "lazaro-cardenas", "miguel-hidalgo"
]

NEW_BUTTONS_TEMPLATE = '''<style>.floating-btn{{position:fixed;right:18px;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:1.1rem;box-shadow:0 10px 28px rgba(0,0,0,0.16);transition:transform .12s ease,box-shadow .12s ease,filter .12s ease;z-index:60;text-decoration:none}}.floating-btn:hover{{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,0.2);filter:brightness(1.05)}}.floating-call{{background:#0f4fa8;bottom:18px}}.floating-whatsapp{{background:#22c55e;bottom:78px}}</style>
<a href="https://wa.me/526673922273?text=Hola%2C%20necesito%20un%20plomero%20en%20{colonia_url}" class="floating-btn floating-whatsapp" target="_blank" rel="noopener noreferrer" aria-label="Contactar por WhatsApp"><svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
<a href="tel:+526673922273" class="floating-btn floating-call" aria-label="Llamar ahora"><svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/></svg></a>
</body>'''

def get_colonia_display_name(content):
    """Extrae el nombre de display de la colonia del título"""
    match = re.search(r'<title>Plomero en ([^,]+),', content)
    if match:
        return match.group(1)
    return None

def fix_colonia_sin_cta(slug):
    """Agrega botones flotantes a colonias que no tienen ninguno"""
    filepath = f"{COLONIAS_DIR}/{slug}/index.html"

    if not os.path.exists(filepath):
        print(f"  ❌ {slug} - archivo no existe")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'floating-btn' in content:
        print(f"  ⏭️  {slug} - ya tiene floating-btn")
        return True

    colonia_name = get_colonia_display_name(content)
    if not colonia_name:
        print(f"  ❌ {slug} - no se pudo extraer nombre")
        return False

    colonia_url = colonia_name.replace(' ', '%20')
    new_buttons = NEW_BUTTONS_TEMPLATE.format(colonia_url=colonia_url)

    # Insertar antes de </body>
    new_content = content.replace('</body>', new_buttons)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✅ {slug} - agregados botones nuevos")
    return True

def fix_colonia_formato_diferente(slug):
    """Reemplaza botones con formato diferente"""
    filepath = f"{COLONIAS_DIR}/{slug}/index.html"

    if not os.path.exists(filepath):
        print(f"  ❌ {slug} - archivo no existe")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'floating-btn' in content:
        print(f"  ⏭️  {slug} - ya tiene floating-btn")
        return True

    colonia_name = get_colonia_display_name(content)
    if not colonia_name:
        print(f"  ❌ {slug} - no se pudo extraer nombre")
        return False

    colonia_url = colonia_name.replace(' ', '%20')
    new_buttons = NEW_BUTTONS_TEMPLATE.format(colonia_url=colonia_url)

    # Eliminar estilos CTA antiguos (formato multilinea)
    content = re.sub(r'<style>\s*\.cta-bar\{[^}]+\}[^<]*</style>', '', content, flags=re.DOTALL)

    # Eliminar div de botones CTA antiguos
    content = re.sub(r'<div class="cta-bar"[^>]*>.*?</div>', '', content, flags=re.DOTALL)

    # Eliminar script de tracking CTA
    content = re.sub(r'<script>\s*\(function\(\)\{[^}]*cta-whatsapp[^}]*\}\)\(\);\s*</script>', '', content, flags=re.DOTALL)

    # Insertar nuevos botones antes de </body>
    new_content = content.replace('</body>', new_buttons)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✅ {slug} - reemplazados botones")
    return True

def main():
    print("Arreglando colonias sin CTA...")
    print("=" * 50)

    for slug in COLONIAS_SIN_CTA:
        fix_colonia_sin_cta(slug)

    print("\nArreglando colonias con formato diferente...")
    print("=" * 50)

    for slug in COLONIAS_FORMATO_DIFERENTE:
        fix_colonia_formato_diferente(slug)

    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()
