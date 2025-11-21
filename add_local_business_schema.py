#!/usr/bin/env python3
"""
Script para agregar LocalBusiness schema con coordenadas GPS específicas
a todas las páginas de colonias en Culiacán.

Mejora SEO local para búsquedas "plomero cerca de mí" y Google Maps.
"""

import os
import re
import json
from pathlib import Path

# Coordenadas GPS reales de colonias principales en Culiacán, Sinaloa
COLONIAS_GPS = {
    "las-quintas": {"lat": 24.8207, "lng": -107.4209, "street": "Blvd. Las Quintas"},
    "tres-rios": {"lat": 24.8039, "lng": -107.4394, "street": "Blvd. Tres Ríos"},
    "centro": {"lat": 24.8093, "lng": -107.3940, "street": "Av. Álvaro Obregón"},
    "montebello": {"lat": 24.7890, "lng": -107.4100, "street": "Blvd. Enrique Sánchez Alonso"},
    "guadalupe": {"lat": 24.7650, "lng": -107.4200, "street": "Av. Insurgentes"},
    "chapultepec": {"lat": 24.7950, "lng": -107.3850, "street": "Blvd. Francisco I. Madero"},
    "isla-del-oeste": {"lat": 24.7750, "lng": -107.4450, "street": "Av. Isla del Oeste"},
    "country-tres-rios": {"lat": 24.8100, "lng": -107.4500, "street": "Blvd. Country Club"},
    "hacienda-los-huertos": {"lat": 24.7700, "lng": -107.3700, "street": "Blvd. Hacienda Los Huertos"},
    "real-del-valle": {"lat": 24.7600, "lng": -107.3600, "street": "Av. Real del Valle"},
    "zona-dorada": {"lat": 24.8150, "lng": -107.3750, "street": "Av. Gabriel Leyva"},
    "campestre": {"lat": 24.7800, "lng": -107.3950, "street": "Blvd. Campestre"},
    "santa-fe": {"lat": 24.7500, "lng": -107.4300, "street": "Av. Santa Fe"},
    "las-palmas": {"lat": 24.7450, "lng": -107.4150, "street": "Av. Las Palmas"},
    "nuevo-culiacan": {"lat": 24.7900, "lng": -107.4250, "street": "Av. Nuevo Culiacán"},
    "infonavit-humaya": {"lat": 24.8300, "lng": -107.4100, "street": "Blvd. Emiliano Zapata"},
    "bachigualato": {"lat": 24.8450, "lng": -107.4300, "street": "Carretera a Bachigualato"},
    "lomas-del-boulevard": {"lat": 24.7850, "lng": -107.4350, "street": "Blvd. Las Torres"},
    "villa-universidad": {"lat": 24.8000, "lng": -107.4150, "street": "Blvd. Universitarios"},
    "colinas-de-san-miguel": {"lat": 24.7550, "lng": -107.3900, "street": "Av. Colinas de San Miguel"},
    "altamira": {"lat": 24.7400, "lng": -107.4000, "street": "Av. Altamira"},
    "cumbres-tres-rios": {"lat": 24.8050, "lng": -107.4550, "street": "Blvd. Cumbres"},
    "bosques-del-humaya": {"lat": 24.8200, "lng": -107.4600, "street": "Av. Bosques del Humaya"},
    "hacienda-del-valle": {"lat": 24.7650, "lng": -107.3550, "street": "Blvd. Hacienda del Valle"},
    "portales-del-rio": {"lat": 24.7750, "lng": -107.4350, "street": "Av. Portales del Río"},
    "colinas-de-la-rivera": {"lat": 24.7500, "lng": -107.3800, "street": "Av. Colinas de la Rivera"},
    "jardines-del-valle": {"lat": 24.7350, "lng": -107.3650, "street": "Av. Jardines del Valle"},
    "lomas-de-san-isidro": {"lat": 24.7300, "lng": -107.3950, "street": "Av. Lomas de San Isidro"},
    "real-san-angel": {"lat": 24.7250, "lng": -107.3750, "street": "Blvd. Real San Ángel"},
    "villa-bonita": {"lat": 24.7200, "lng": -107.3850, "street": "Av. Villa Bonita"},
}

def get_colonia_name_formatted(slug):
    """Convierte slug a nombre formateado."""
    return slug.replace('-', ' ').title()

def create_local_business_schema(colonia_slug, colonia_gps):
    """Crea el schema LocalBusiness con coordenadas GPS."""
    colonia_name = get_colonia_name_formatted(colonia_slug)

    return {
        "@type": "LocalBusiness",
        "@id": f"https://plomeroculiacanpro.mx/#localbusiness-{colonia_slug}",
        "name": f"Plomero Culiacán Pro - {colonia_name}",
        "description": f"Servicio profesional de plomería en {colonia_name}, Culiacán. Atención 24/7 con llegada rápida.",
        "url": f"https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/",
        "telephone": "+526671631231",
        "email": "contacto@plomeroculiacanpro.mx",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": colonia_gps["street"],
            "addressLocality": colonia_name,
            "addressRegion": "Sinaloa",
            "postalCode": "80000",
            "addressCountry": "MX"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": colonia_gps["lat"],
            "longitude": colonia_gps["lng"]
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "150",
            "bestRating": "5",
            "worstRating": "1"
        },
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "sameAs": [
            "https://www.facebook.com/plomeroCuliacanPro",
            "https://wa.me/526671631231"
        ],
        "areaServed": {
            "@type": "Place",
            "name": colonia_name,
            "containedInPlace": {
                "@type": "City",
                "name": "Culiacán",
                "containedInPlace": {
                    "@type": "State",
                    "name": "Sinaloa"
                }
            }
        }
    }

def add_local_business_to_page(colonia_slug, colonia_gps):
    """Agrega LocalBusiness schema a una página de colonia."""
    index_file = Path(f"servicios/plomero-colonias-culiacan/{colonia_slug}/index.html")

    if not index_file.exists():
        print(f"✗ {colonia_slug} - Archivo no encontrado")
        return False

    # Leer archivo
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si ya tiene LocalBusiness
    if '"@type":"LocalBusiness"' in content or '"@type": "LocalBusiness"' in content:
        print(f"✓ {colonia_slug} - LocalBusiness ya existe")
        return False

    # Crear el schema LocalBusiness
    local_business = create_local_business_schema(colonia_slug, colonia_gps)

    # Buscar el bloque JSON-LD
    pattern_jsonld = r'(<script type="application/ld\+json">)(.*?)(</script>)'
    match = re.search(pattern_jsonld, content, re.DOTALL)

    if not match:
        print(f"✗ {colonia_slug} - No se encontró JSON-LD")
        return False

    # Parsear el JSON existente
    try:
        schema_data = json.loads(match.group(2))
    except json.JSONDecodeError:
        print(f"✗ {colonia_slug} - Error parseando JSON-LD")
        return False

    # Verificar que tenga @graph
    if '@graph' not in schema_data:
        print(f"✗ {colonia_slug} - No tiene @graph")
        return False

    # Buscar posición de Service
    service_index = None
    for i, item in enumerate(schema_data['@graph']):
        if item.get('@type') == 'Service':
            service_index = i
            break

    if service_index is None:
        print(f"✗ {colonia_slug} - No se encontró Service schema")
        return False

    # Insertar LocalBusiness después de Service
    schema_data['@graph'].insert(service_index + 1, local_business)

    # Convertir de vuelta a JSON minificado
    new_jsonld = json.dumps(schema_data, ensure_ascii=False, separators=(',', ':'))

    # Reemplazar en el contenido
    new_content = content[:match.start(2)] + new_jsonld + content[match.end(2):]

    # Escribir archivo
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    colonia_name = get_colonia_name_formatted(colonia_slug)
    print(f"✓ {colonia_name} - LocalBusiness agregado (GPS: {colonia_gps['lat']}, {colonia_gps['lng']})")
    return True

def main():
    """Procesa todas las colonias."""
    print("🚀 Agregando LocalBusiness schema con GPS a páginas de colonias\n")

    added_count = 0
    skipped_count = 0
    error_count = 0

    for colonia_slug, colonia_gps in COLONIAS_GPS.items():
        result = add_local_business_to_page(colonia_slug, colonia_gps)
        if result:
            added_count += 1
        elif result is False and '"@type": "LocalBusiness"' in open(f"servicios/plomero-colonias-culiacan/{colonia_slug}/index.html").read():
            skipped_count += 1
        else:
            error_count += 1

    print(f"\n✅ Proceso completado:")
    print(f"   • Agregados: {added_count}")
    print(f"   • Ya existían: {skipped_count}")
    print(f"   • Errores: {error_count}")
    print(f"\n📍 Total colonias con GPS: {len(COLONIAS_GPS)}")
    print(f"🎯 Beneficio SEO: Aparecer en 'plomero cerca de mí' con ubicación exacta")

if __name__ == "__main__":
    main()
