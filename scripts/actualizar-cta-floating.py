#!/usr/bin/env python3
"""
Script para actualizar botones cta-bar a floating-btn en todas las páginas.
"""

import os
import re
import glob

# CSS para floating-btn (se agrega si no existe)
FLOATING_CSS = '.floating-btn{position:fixed;right:18px;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:1.1rem;box-shadow:0 10px 28px rgba(0,0,0,0.16);transition:transform .12s ease,box-shadow .12s ease,filter .12s ease;z-index:60;text-decoration:none}.floating-btn:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,0,0,0.2);filter:brightness(1.05)}.floating-call{background:#0f4fa8;bottom:18px}.floating-whatsapp{background:#22c55e;bottom:78px}'

# SVGs para los botones
WHATSAPP_SVG = '<svg width="26" height="26" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'

PHONE_SVG = '<svg width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>'

# Número estándar
PHONE = "526673922273"

def get_floating_html():
    wa_url = f"https://wa.me/{PHONE}?text=Hola%2C%20necesito%20un%20plomero%20en%20Culiacán"
    return f'''<!-- Floating CTA Buttons -->
<a href="{wa_url}" target="_blank" rel="noopener" class="floating-btn floating-whatsapp" aria-label="WhatsApp">{WHATSAPP_SVG}</a>
<a href="tel:+{PHONE}" class="floating-btn floating-call" aria-label="Llamar">{PHONE_SVG}</a>'''

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'floating-btn' in content and 'cta-bar' not in content:
        return "skip", "ya tiene floating-btn"

    if 'cta-bar' not in content:
        return "skip", "no tiene cta-bar"

    original = content

    # Patrón 1: div con cta-bar y botones con emoji
    pattern1 = r'<div class="cta-bar"[^>]*>\s*<a[^>]*class="cta-btn cta-wa"[^>]*>[^<]*</a>\s*<a[^>]*class="cta-btn cta-tel"[^>]*>[^<]*</a>\s*</div>'

    # Patrón 2: div con cta-bar y botones con SVG
    pattern2 = r'<div class="cta-bar"[^>]*>\s*<a[^>]*class="cta-btn cta-wa"[^>]*>.*?</a>\s*<a[^>]*class="cta-btn cta-tel"[^>]*>.*?</a>\s*</div>'

    # Patrón 3: comentario + div
    pattern3 = r'<!--[^>]*CTA[^>]*-->\s*<div class="cta-bar"[^>]*>\s*<a[^>]*class="cta-btn cta-wa"[^>]*>.*?</a>\s*<a[^>]*class="cta-btn cta-tel"[^>]*>.*?</a>\s*</div>'

    # Patrón 4: Botones Flotantes CTA
    pattern4 = r'<!--\s*Botones Flotantes CTA\s*-->\s*<div class="cta-bar">\s*<a[^>]*class="cta-btn cta-wa"[^>]*>\s*<svg[^>]*>.*?</svg>\s*</a>\s*<a[^>]*class="cta-btn cta-tel"[^>]*>\s*<svg[^>]*>.*?</svg>\s*</a>\s*</div>'

    replaced = False
    for pattern in [pattern4, pattern3, pattern2, pattern1]:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, get_floating_html(), content, flags=re.DOTALL)
            replaced = True
            break

    if not replaced:
        return "error", "patrón no reconocido"

    # Agregar CSS si no existe
    if '.floating-btn{' not in content:
        if '</style>' in content:
            content = content.replace('</style>', FLOATING_CSS + '\n</style>', 1)
        else:
            # Agregar antes de </head>
            content = content.replace('</head>', f'<style>{FLOATING_CSS}</style>\n</head>')

    if content == original:
        return "skip", "sin cambios"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return "ok", "actualizado"

def main():
    # Archivos a actualizar (excepto colonias individuales que ya se hicieron)
    files = [
        "servicios/plomero-precios/index.html",
        "servicios/emergencia-24-7/index.html",
        "servicios/plomero-colonias-culiacan/index.html",
        "blog/cuanto-cuesta-plomeria-bano-completo-culiacan/index.html",
        "blog/drenaje-tapado-senales-prevencion/index.html",
        "blog/cuanto-cuesta-cambiar-taza-bano-culiacan/index.html",
        "blog/cuanto-cobra-plomero-visita-culiacan/index.html",
    ]

    # También buscar otros blogs
    blog_files = glob.glob("blog/*/index.html")
    for f in blog_files:
        if f not in files:
            files.append(f)

    print(f"Actualizando {len(files)} archivos...")
    print("=" * 50)

    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"  ❌ {filepath} - no existe")
            errors += 1
            continue

        status, msg = update_file(filepath)

        if status == "ok":
            print(f"  ✅ {filepath}")
            updated += 1
        elif status == "skip":
            print(f"  ⏭️  {filepath} - {msg}")
            skipped += 1
        else:
            print(f"  ⚠️  {filepath} - {msg}")
            errors += 1

    print("=" * 50)
    print(f"✅ Actualizados: {updated}")
    print(f"⏭️  Saltados: {skipped}")
    print(f"⚠️  Errores: {errors}")

if __name__ == "__main__":
    main()
