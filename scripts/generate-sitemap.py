#!/usr/bin/env python3
"""
Generador de Sitemap XML para plomeroculiacanpro.mx
Incluye todas las páginas del sitio incluyendo las 643+ colonias
"""

import os
from datetime import datetime
from pathlib import Path

BASE_URL = "https://plomeroculiacanpro.mx"
PROJECT_ROOT = Path(__file__).parent.parent

def get_lastmod(file_path):
    """Get file modification time in ISO format"""
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%S-07:00')
    except:
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S-07:00')

def generate_sitemap():
    urls = []

    # Homepage
    urls.append({
        'loc': f"{BASE_URL}/",
        'lastmod': get_lastmod(PROJECT_ROOT / 'index.html'),
        'changefreq': 'weekly',
        'priority': '1.0'
    })

    # Landing Pages Principales (alta prioridad)
    main_landings = [
        'servicios/plomero-24-horas/',
        'servicios/plomero-a-domicilio/',
        'servicios/plomero-cerca-de-mi/',
        'servicios/plomero-de-emergencia/',
        'servicios/plomero-economico/',
        'servicios/plomero-urgente/',
    ]

    for landing in main_landings:
        file_path = PROJECT_ROOT / landing / 'index.html'
        if file_path.exists():
            urls.append({
                'loc': f"{BASE_URL}/{landing}",
                'lastmod': get_lastmod(file_path),
                'changefreq': 'monthly',
                'priority': '0.9'
            })

    # Servicios específicos
    servicios = [
        'servicios/reparacion-de-fugas/',
        'servicios/desazolve-de-drenajes/',
        'servicios/instalacion-de-boiler/',
        'servicios/destape-de-drenajes/',
        'servicios/deteccion-de-fugas/',
        'servicios/instalacion-de-sanitarios/',
        'servicios/instalacion-de-tinaco/',
        'servicios/mantenimiento-de-boiler/',
        'servicios/correccion-baja-presion/',
        'servicios/emergencia-24-7/',
        'servicios/plomero-precios/',
        'servicios/plomero-colonias-culiacan/',
    ]

    for servicio in servicios:
        file_path = PROJECT_ROOT / servicio / 'index.html'
        if file_path.exists():
            priority = '0.8' if 'reparacion' in servicio or 'desazolve' in servicio or 'boiler' in servicio else '0.7'
            urls.append({
                'loc': f"{BASE_URL}/{servicio}",
                'lastmod': get_lastmod(file_path),
                'changefreq': 'monthly',
                'priority': priority
            })

    # Colonias - todas las 643+
    colonias_dir = PROJECT_ROOT / 'servicios' / 'plomero-colonias-culiacan'
    if colonias_dir.exists():
        for colonia in sorted(colonias_dir.iterdir()):
            if colonia.is_dir():
                index_file = colonia / 'index.html'
                if index_file.exists():
                    colonia_name = colonia.name
                    urls.append({
                        'loc': f"{BASE_URL}/servicios/plomero-colonias-culiacan/{colonia_name}/",
                        'lastmod': get_lastmod(index_file),
                        'changefreq': 'yearly',
                        'priority': '0.6'
                    })

    # Blog
    blog_index = PROJECT_ROOT / 'blog' / 'index.html'
    if blog_index.exists():
        urls.append({
            'loc': f"{BASE_URL}/blog/",
            'lastmod': get_lastmod(blog_index),
            'changefreq': 'weekly',
            'priority': '0.7'
        })

    # Blog posts
    blog_dir = PROJECT_ROOT / 'blog'
    if blog_dir.exists():
        for post in sorted(blog_dir.iterdir()):
            if post.is_dir() and post.name != 'index.html':
                index_file = post / 'index.html'
                if index_file.exists():
                    urls.append({
                        'loc': f"{BASE_URL}/blog/{post.name}/",
                        'lastmod': get_lastmod(index_file),
                        'changefreq': 'monthly',
                        'priority': '0.6'
                    })

    # Contacto
    contacto = PROJECT_ROOT / 'contacto' / 'index.html'
    if contacto.exists():
        urls.append({
            'loc': f"{BASE_URL}/contacto/",
            'lastmod': get_lastmod(contacto),
            'changefreq': 'yearly',
            'priority': '0.5'
        })

    # Términos
    terminos = PROJECT_ROOT / 'terminos' / 'index.html'
    if terminos.exists():
        urls.append({
            'loc': f"{BASE_URL}/terminos/",
            'lastmod': get_lastmod(terminos),
            'changefreq': 'yearly',
            'priority': '0.3'
        })

    return urls

def write_sitemap(urls, output_path):
    """Write sitemap XML file"""
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    return len(urls)

def main():
    print("Generando sitemap...")

    urls = generate_sitemap()

    # Write main sitemap
    output_path = PROJECT_ROOT / 'sitemaps' / 'main_sitemap.xml'
    count = write_sitemap(urls, output_path)

    print(f"✅ Sitemap generado: {output_path}")
    print(f"   Total URLs: {count}")

    # Count by type
    colonias = len([u for u in urls if 'plomero-colonias-culiacan/' in u['loc'] and u['loc'].count('/') > 4])
    print(f"   - Colonias: {colonias}")
    print(f"   - Otras páginas: {count - colonias}")

if __name__ == '__main__':
    main()
