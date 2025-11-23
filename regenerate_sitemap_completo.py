#!/usr/bin/env python3
"""
Regenera el sitemap COMPLETO con todas las páginas del sitio.
Incluye: homepage, servicios, colonias, blog, contacto
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import subprocess

# Namespace para sitemap
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

def get_git_lastmod(file_path):
    """Obtiene la fecha de última modificación desde git"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%aI', file_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    # Fallback a fecha actual
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")

# Crear root element
urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

# Lista de páginas para el sitemap
pages = []

# 1. HOMEPAGE
pages.append({
    'loc': 'https://plomeroculiacanpro.mx/',
    'file': 'index.html',
    'changefreq': 'weekly',
    'priority': '1.0'
})

# 2. SERVICIOS PRINCIPALES
servicios = [
    ('emergencia-24-7', '0.9'),
    ('reparacion-de-fugas', '0.9'),
    ('destape-de-drenajes', '0.9'),
    ('deteccion-de-fugas', '0.9'),
    ('plomero-a-domicilio', '0.8'),
    ('instalacion-de-sanitarios', '0.8'),
    ('mantenimiento-de-boiler', '0.8'),
    ('correccion-baja-presion', '0.8'),
    ('plomero-cerca-de-mi', '0.7'),
    ('plomero-precios', '0.7'),
]

for servicio, priority in servicios:
    pages.append({
        'loc': f'https://plomeroculiacanpro.mx/servicios/{servicio}/',
        'file': f'servicios/{servicio}/index.html',
        'changefreq': 'monthly',
        'priority': priority
    })

# 3. ÍNDICE DE COLONIAS
pages.append({
    'loc': 'https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/',
    'file': 'servicios/plomero-colonias-culiacan/index.html',
    'changefreq': 'monthly',
    'priority': '0.9'
})

# 4. PÁGINAS DE COLONIAS (30 colonias)
colonias_dir = Path('servicios/plomero-colonias-culiacan')
if colonias_dir.exists():
    colonias = sorted([d.name for d in colonias_dir.iterdir() if d.is_dir()])

    # Colonias premium (prioridad alta)
    colonias_premium = ['las-quintas', 'tres-rios', 'chapultepec', 'campestre',
                        'country-tres-rios', 'colinas-de-san-miguel', 'lomas-del-boulevard']

    for colonia in colonias:
        priority = '0.8' if colonia in colonias_premium else '0.7'
        pages.append({
            'loc': f'https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia}/',
            'file': f'servicios/plomero-colonias-culiacan/{colonia}/index.html',
            'changefreq': 'monthly',
            'priority': priority
        })

# 5. BLOG - ÍNDICE
pages.append({
    'loc': 'https://plomeroculiacanpro.mx/blog/',
    'file': 'blog/index.html',
    'changefreq': 'weekly',
    'priority': '0.7'
})

# 6. ARTÍCULOS DEL BLOG
blog_dir = Path('blog')
if blog_dir.exists():
    articulos = []
    for item in blog_dir.iterdir():
        if item.is_dir() and (item / 'index.html').exists():
            articulos.append(item.name)

    # Ordenar para consistencia
    articulos = sorted(articulos)

    for articulo in articulos:
        # Prioridad más baja para artículo no relacionado
        priority = '0.3' if articulo == 'marcha-paz-culiacan-2025' else '0.6'

        pages.append({
            'loc': f'https://plomeroculiacanpro.mx/blog/{articulo}/',
            'file': f'blog/{articulo}/index.html',
            'changefreq': 'monthly',
            'priority': priority
        })

# 7. CONTACTO
pages.append({
    'loc': 'https://plomeroculiacanpro.mx/contacto/',
    'file': 'contacto/index.html',
    'changefreq': 'monthly',
    'priority': '0.5'
})

# Generar XML para cada página
print(f"🔍 Generando sitemap con {len(pages)} URLs...\n")

for page in pages:
    url_elem = ET.SubElement(urlset, 'url')

    # <loc>
    loc = ET.SubElement(url_elem, 'loc')
    loc.text = page['loc']

    # <lastmod> - obtener de git
    lastmod = ET.SubElement(url_elem, 'lastmod')
    if os.path.exists(page['file']):
        lastmod.text = get_git_lastmod(page['file'])
    else:
        lastmod.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # <changefreq>
    changefreq = ET.SubElement(url_elem, 'changefreq')
    changefreq.text = page['changefreq']

    # <priority>
    priority = ET.SubElement(url_elem, 'priority')
    priority.text = page['priority']

# Crear árbol XML
tree = ET.ElementTree(urlset)

# Pretty print
ET.indent(tree, space='  ', level=0)

# Escribir archivo
output_file = 'sitemaps/main_sitemap.xml'
tree.write(output_file, encoding='UTF-8', xml_declaration=True)

print(f"✅ Sitemap generado exitosamente!")
print(f"📄 Archivo: {output_file}")
print(f"📊 Total de URLs: {len(pages)}\n")

# Resumen por categoría
print("📈 RESUMEN POR CATEGORÍA:")
print(f"  • Homepage: 1")
print(f"  • Servicios principales: {len(servicios)}")
print(f"  • Índice colonias: 1")

colonias_count = len([p for p in pages if 'plomero-colonias-culiacan' in p['loc'] and p['loc'].count('/') == 5])
print(f"  • Páginas de colonias: {colonias_count}")

print(f"  • Blog índice: 1")

articulos_count = len([p for p in pages if '/blog/' in p['loc'] and p['loc'].count('/') == 4])
print(f"  • Artículos blog: {articulos_count}")

print(f"  • Contacto: 1")
print(f"\n  TOTAL: {len(pages)} URLs")

print("\n🔍 Verificación:")
print(f"  - Sitemap anterior: 7 URLs ❌")
print(f"  - Sitemap nuevo: {len(pages)} URLs ✅")
print(f"  - Incremento: +{len(pages) - 7} URLs\n")

print("📌 PRÓXIMOS PASOS:")
print("  1. Revisa el archivo: sitemaps/main_sitemap.xml")
print("  2. Haz commit y push a GitHub")
print("  3. Espera 5-10 min para que GitHub Pages actualice")
print("  4. Ve a Google Search Console > Sitemaps")
print("  5. Re-envía el sitemap o espera que Google lo crawlee")
print("  6. En 24-48 horas verás las 60+ URLs descubiertas")
