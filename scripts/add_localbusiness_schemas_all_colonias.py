#!/usr/bin/env python3
"""
Script para agregar schema LocalBusiness con GPS a las 643 páginas de colonias
del sitio Plomero Culiacán Pro.

Comportamiento:
- Lee cada servicios/plomero-colonias-culiacan/*/index.html
- Si la página YA tiene <script type="application/ld+json"> con LocalBusiness → salta
- Si NO tiene schema → inyecta bloque JSON-LD antes de </head>

GPS real: tomado de colonias-completas-culiacan.json (30 colonias)
GPS fallback (centroide Culiacán): lat=24.7903, lng=-107.3878
"""

import os
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuración fija
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
COLONIAS_DIR = PROJECT_ROOT / "servicios" / "plomero-colonias-culiacan"
COLONIAS_JSON = PROJECT_ROOT / "colonias-completas-culiacan.json"

PHONE = "+52 667 392 2273"
FALLBACK_LAT = 24.7903
FALLBACK_LNG = -107.3878


# ---------------------------------------------------------------------------
# Cargar GPS reales desde JSON
# ---------------------------------------------------------------------------
def load_gps_from_json(json_path: Path) -> dict:
    """Devuelve dict slug → {lat, lng} a partir del JSON de colonias."""
    if not json_path.exists():
        print(f"ADVERTENCIA: No se encontro {json_path}, se usara solo fallback GPS.")
        return {}
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    gps_map = {}
    for entry in data.get("colonias_culiacan", []):
        slug = entry.get("slug", "")
        gps = entry.get("gps", {})
        if slug and "lat" in gps and "lng" in gps:
            gps_map[slug] = {"lat": gps["lat"], "lng": gps["lng"]}
    return gps_map


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def slug_to_nombre(slug: str) -> str:
    """
    Convierte slug a nombre legible usando Title Case.
    Ejemplo: 'las-quintas' → 'Las Quintas'
    """
    return slug.replace("-", " ").title()


def build_schema(slug: str, nombre: str, lat: float, lng: float) -> str:
    """Construye el bloque JSON-LD como string formateado."""
    base_url = "https://plomeroculiacanpro.mx"
    page_url = f"{base_url}/servicios/plomero-colonias-culiacan/{slug}/"

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Plumber", "LocalBusiness"],
                "@id": f"{page_url}#business",
                "name": f"Plomero Culiacán Pro – {nombre}",
                "telephone": PHONE,
                "url": page_url,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Culiacán",
                    "addressRegion": "Sinaloa",
                    "postalCode": "80000",
                    "addressCountry": "MX",
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": lat,
                    "longitude": lng,
                },
                "areaServed": {
                    "@type": "Place",
                    "name": f"{nombre}, Culiacán, Sinaloa",
                },
                "openingHoursSpecification": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ],
                    "opens": "00:00",
                    "closes": "23:59",
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.8",
                    "reviewCount": "150",
                    "bestRating": "5",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Inicio",
                        "item": f"{base_url}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Plomero en Colonias",
                        "item": f"{base_url}/servicios/plomero-colonias-culiacan/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": f"Plomero en {nombre}",
                        "item": page_url,
                    },
                ],
            },
        ],
    }

    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    block = (
        "<!-- Schema LocalBusiness + BreadcrumbList -->\n"
        '<script type="application/ld+json">\n'
        f"{schema_json}\n"
        "</script>"
    )
    return block


def has_localbusiness_schema(content: str) -> bool:
    """
    Devuelve True si la página ya contiene un bloque JSON-LD con LocalBusiness.
    Verifica la presencia de application/ld+json Y el tipo LocalBusiness o Plumber.
    """
    if '<script type="application/ld+json">' not in content:
        return False
    # Si tiene el tag pero no menciona LocalBusiness/Plumber, no cuenta
    if "LocalBusiness" in content or '"Plumber"' in content:
        return True
    return False


def inject_schema(file_path: Path, schema_block: str) -> bool:
    """
    Inyecta el schema_block antes de </head>.
    Devuelve True si tuvo éxito, False si no encontró </head>.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "</head>" not in content:
        return False

    new_content = content.replace("</head>", f"\n{schema_block}\n</head>", 1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 65)
    print("  Inyeccion de schemas LocalBusiness a colonias de Culiacan")
    print("=" * 65)

    # Cargar mapa GPS desde JSON
    gps_map = load_gps_from_json(COLONIAS_JSON)
    print(f"GPS reales cargados desde JSON: {len(gps_map)} colonias")
    print(f"Fallback GPS (centroide): lat={FALLBACK_LAT}, lng={FALLBACK_LNG}\n")

    # Recopilar todas las paginas de colonias
    colony_pages = sorted(
        [
            p
            for p in COLONIAS_DIR.iterdir()
            if p.is_dir() and (p / "index.html").exists()
        ],
        key=lambda p: p.name,
    )

    total = len(colony_pages)
    injected = 0
    skipped = 0
    errors = 0
    used_real_gps = 0
    used_fallback_gps = 0

    print(f"Total de paginas de colonias encontradas: {total}\n")
    print(f"{'Procesando...'}")
    print("-" * 65)

    for colony_dir in colony_pages:
        slug = colony_dir.name
        index_file = colony_dir / "index.html"

        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verificar si ya tiene LocalBusiness schema
        if has_localbusiness_schema(content):
            skipped += 1
            print(f"  [SKIP]  {slug} — ya tiene LocalBusiness schema")
            continue

        # Determinar GPS
        if slug in gps_map:
            lat = gps_map[slug]["lat"]
            lng = gps_map[slug]["lng"]
            gps_source = "real"
            used_real_gps += 1
        else:
            lat = FALLBACK_LAT
            lng = FALLBACK_LNG
            gps_source = "fallback"
            used_fallback_gps += 1

        # Obtener nombre legible
        nombre = slug_to_nombre(slug)

        # Construir schema
        schema_block = build_schema(slug, nombre, lat, lng)

        # Inyectar
        success = inject_schema(index_file, schema_block)

        if success:
            injected += 1
            print(f"  [OK]    {slug} | GPS={gps_source} ({lat}, {lng})")
        else:
            errors += 1
            print(f"  [ERROR] {slug} — no se encontro </head>")

    # ---------------------------------------------------------------------------
    # Reporte final
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("  REPORTE FINAL")
    print("=" * 65)
    print(f"  Total paginas procesadas  : {total}")
    print(f"  Schemas inyectados        : {injected}")
    print(f"  Saltadas (ya tenian)      : {skipped}")
    print(f"  Errores                   : {errors}")
    print(f"  GPS reales usados         : {used_real_gps}")
    print(f"  GPS fallback usados       : {used_fallback_gps}")
    print("=" * 65)


if __name__ == "__main__":
    main()
