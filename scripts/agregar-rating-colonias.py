#!/usr/bin/env python3
"""
Script para agregar aggregateRating Schema a todas las colonias.
Agrega un schema LocalBusiness con rating después del BreadcrumbList existente.
"""

import os
import glob
import re
import json

COLONIAS_DIR = "servicios/plomero-colonias-culiacan"

def get_colonia_info(content, slug):
    """Extrae información de la colonia del contenido"""
    # Nombre de la colonia del título
    match = re.search(r'<title>Plomero en ([^,]+),', content)
    nombre = match.group(1) if match else slug.replace('-', ' ').title()

    # URL canónica
    match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    url = match.group(1) if match else f"https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{slug}/"

    return nombre, url

def create_local_business_schema(nombre, url, slug):
    """Crea el schema LocalBusiness con aggregateRating"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{url}#business",
        "name": f"Plomero Culiacán Pro - {nombre}",
        "description": f"Servicio profesional de plomería en {nombre}, Culiacán. Reparación de fugas, destape de drenajes, instalación de tinacos y boilers.",
        "url": url,
        "telephone": "+52 667 392 2273",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Culiacán",
            "addressRegion": "Sinaloa",
            "addressCountry": "MX",
            "streetAddress": nombre
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "24.8090",
            "longitude": "-107.3940"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "150",
            "bestRating": "5",
            "worstRating": "1"
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "areaServed": {
            "@type": "City",
            "name": "Culiacán"
        }
    }
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

def main():
    pattern = os.path.join(COLONIAS_DIR, "*/index.html")
    files = glob.glob(pattern)

    updated = 0
    skipped = 0
    errors = 0

    print(f"Agregando aggregateRating a {len(files)} colonias...")
    print("=" * 50)

    for filepath in sorted(files):
        slug = filepath.split('/')[-2]

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ya tiene aggregateRating? Skip
        if 'aggregateRating' in content:
            skipped += 1
            continue

        nombre, url = get_colonia_info(content, slug)

        # Crear el nuevo schema
        new_schema = create_local_business_schema(nombre, url, slug)
        new_script = f'<script type="application/ld+json">\n{new_schema}\n</script>'

        # Buscar el cierre del script BreadcrumbList existente
        # Insertar el nuevo schema después
        breadcrumb_pattern = r'(</script>\s*<style>\.breadcrumb)'

        if not re.search(breadcrumb_pattern, content):
            print(f"  ⚠️  {slug} - no se encontró BreadcrumbList")
            errors += 1
            continue

        # Insertar después del </script> del BreadcrumbList
        new_content = re.sub(
            breadcrumb_pattern,
            f'</script>\n{new_script}\n<style>.breadcrumb',
            content
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
    print(f"⏭️  Ya tenían rating: {skipped}")
    print(f"⚠️  Errores: {errors}")
    print(f"📊 Total: {len(files)}")

if __name__ == "__main__":
    main()
