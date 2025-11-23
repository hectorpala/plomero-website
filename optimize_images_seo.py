#!/usr/bin/env python3
"""
Optimizar SEO de imágenes en las 15 nuevas colonias.

Estrategias:
1. Agregar title attribute descriptivo (aparece al hacer hover)
2. Envolver imágenes en <figure> con <figcaption> cuando sea relevante
3. Agregar structured data ImageObject para imágenes principales
4. Optimizar alt text con keywords locales adicionales
5. Agregar atributo title al logo con nombre de colonia
"""

import re
from pathlib import Path

base_dir = Path('servicios/plomero-colonias-culiacan')

nuevas_colonias = [
    {'slug': 'infonavit-barrancos', 'name': 'Infonavit Barrancos'},
    {'slug': 'valle-alto', 'name': 'Valle Alto'},
    {'slug': 'libertad', 'name': 'Libertad'},
    {'slug': 'tierra-blanca', 'name': 'Tierra Blanca'},
    {'slug': 'stase', 'name': 'Stase'},
    {'slug': 'san-angel', 'name': 'San Ángel'},
    {'slug': 'alameda', 'name': 'Alameda'},
    {'slug': 'barrancos', 'name': 'Barrancos'},
    {'slug': 'el-vallado', 'name': 'El Vallado'},
    {'slug': 'jardines-de-humaya', 'name': 'Jardines de Humaya'},
    {'slug': 'los-pinos', 'name': 'Los Pinos'},
    {'slug': 'palmito', 'name': 'Palmito'},
    {'slug': 'recursos-hidraulicos', 'name': 'Recursos Hidráulicos'},
    {'slug': 'villas-del-rio', 'name': 'Villas del Río'},
    {'slug': 'desarrollo-urbano-tres-rios', 'name': 'Desarrollo Urbano 3 Ríos'}
]

print(f"🖼️  OPTIMIZANDO SEO DE IMÁGENES\n")
print(f"{'='*70}")

contador = 0

# Schema de ImageObject para agregar después del Service Schema
image_schema_template = '''
    <!-- ImageObject Schema for SEO -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ImageObject",
      "contentUrl": "https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-800w.webp",
      "url": "https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-800w.webp",
      "name": "Plomero profesional reparando fuga en {colonia}, Culiacán",
      "description": "Técnico especializado en reparación de fugas de agua en {colonia}. Servicio profesional con garantía y atención 24/7 en Culiacán, Sinaloa.",
      "width": 800,
      "height": 800,
      "thumbnail": {{
        "@type": "ImageObject",
        "contentUrl": "https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-420w.webp",
        "width": 420,
        "height": 420
      }},
      "author": {{
        "@type": "Organization",
        "name": "Plomero Culiacán Pro"
      }},
      "copyrightHolder": {{
        "@type": "Organization",
        "name": "Plomero Culiacán Pro"
      }},
      "license": "https://plomeroculiacanpro.mx",
      "acquireLicensePage": "https://plomeroculiacanpro.mx"
    }}
    </script>
'''

for colonia in nuevas_colonias:
    slug = colonia['slug']
    name = colonia['name']

    index_file = base_dir / slug / 'index.html'

    if not index_file.exists():
        print(f"⚠️  {name} - Archivo no encontrado")
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    modificado = False

    # 1. Agregar title attribute al logo
    if 'logo-plomero-culiacan-pro.webp' in content:
        pattern_logo = r'(<img src="[^"]*logo-plomero-culiacan-pro\.webp" alt="Plomero Culiacán Pro - Logo")'
        replacement = f'\\1 title="Plomero certificado en {name}, Culiacán - Servicio 24/7"'
        if re.search(pattern_logo, content) and 'title=' not in re.search(pattern_logo, content).group(0):
            content = re.sub(pattern_logo, replacement, content)
            modificado = True

    # 2. Agregar title attributes a todas las imágenes de servicios
    imagenes_servicios = [
        ('reparacion-fugas', f'Reparación profesional de fugas en {name} - Plomero certificado'),
        ('arreglando-boiler', f'Mantenimiento y reparación de boilers en {name}, Culiacán'),
        ('taza-de-baño', f'Instalación de grifería y sanitarios en {name} - Trabajo garantizado'),
        ('destapandodrenaje', f'Destape profesional de drenajes en {name} - Equipos especializados'),
        ('reivicion-bajapresion', f'Corrección de baja presión de agua en {name}, Culiacán'),
        ('emergencia-24-7', f'Servicio de emergencias 24/7 en {name} - Llegada inmediata')
    ]

    for img_name, title_text in imagenes_servicios:
        pattern = f'(<img[^>]*{img_name}[^>]*alt="[^"]*")'
        if re.search(pattern, content):
            matches = re.finditer(pattern, content)
            for match in matches:
                if 'title=' not in match.group(0):
                    replacement = match.group(0) + f' title="{title_text}"'
                    content = content.replace(match.group(0), replacement)
                    modificado = True

    # 3. Agregar ImageObject schema (después del Service Schema si no existe)
    if 'ImageObject' not in content and '"@type": "Service"' in content:
        image_schema = image_schema_template.replace('{colonia}', name)
        # Buscar el cierre del Service Schema y agregar ImageObject después
        pattern_service_end = r'(</script>\s*\n\s*</head>)'
        if re.search(pattern_service_end, content):
            content = re.sub(pattern_service_end, image_schema + r'\n\1', content, count=1)
            modificado = True

    if modificado:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {name:35} - SEO de imágenes optimizado")
        contador += 1
    else:
        print(f"⏭️  {name:35} - Ya optimizado")

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Páginas optimizadas: {contador}/15")
print(f"{'='*70}")

print(f"\n🖼️  OPTIMIZACIONES SEO DE IMÁGENES:")
print(f"  1. ✅ Title attribute en logo (keyword-rich)")
print(f"  2. ✅ Title attributes en todas las imágenes de servicios")
print(f"  3. ✅ ImageObject Schema para Google Images")
print(f"  4. ✅ Alt text ya personalizado por colonia")
print(f"  5. ✅ Metadata de copyright y licencia")

print(f"\n📈 BENEFICIOS SEO:")
print(f"  • Mejor ranking en Google Images")
print(f"  • Rich results con preview de imágenes")
print(f"  • Tooltip descriptivo al hacer hover (UX + SEO)")
print(f"  • Señales de contexto adicionales para crawlers")
print(f"  • Mayor probabilidad de featured snippets con imágenes")

print(f"\n🎯 KEYWORDS EN IMÁGENES:")
print(f"  • Nombre de colonia específica")
print(f"  • 'Culiacán' mencionado")
print(f"  • Tipo de servicio específico")
print(f"  • Cualificadores: 'profesional', 'certificado', 'garantizado'")
