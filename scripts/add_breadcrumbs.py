#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Get all colonia subdirectories
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

for colonia_dir in colonias:
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        continue

    # Extract colonia name from directory
    colonia_slug = colonia_dir.name

    # Convert slug to title (e.g., "las-quintas" -> "Las Quintas")
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Read file
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if BreadcrumbList already exists
    if '"@type": "BreadcrumbList"' in content:
        print(f"✓ {colonia_name} - BreadcrumbList ya existe")
        continue

    # Create breadcrumb schema
    breadcrumb_schema = f'''        ,
        {{
            "@type": "BreadcrumbList",
            "@id": "https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/#breadcrumb",
            "itemListElement": [
                {{
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Inicio",
                    "item": "https://plomeroculiacanpro.mx/"
                }},
                {{
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Servicios",
                    "item": "https://plomeroculiacanpro.mx/#servicios"
                }},
                {{
                    "@type": "ListItem",
                    "position": 3,
                    "name": "Colonias Culiacán",
                    "item": "https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/"
                }},
                {{
                    "@type": "ListItem",
                    "position": 4,
                    "name": "Plomero en {colonia_name}",
                    "item": "https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/"
                }}
            ]
        }}'''

    # Find the position to insert (after Service schema, before FAQPage)
    # Look for the closing of Service schema (just before FAQPage)
    pattern = r'(\s+},\s+{\s+"@type": "FAQPage")'

    if re.search(pattern, content):
        # Insert breadcrumb before FAQPage
        content = re.sub(pattern, breadcrumb_schema + r'\1', content, count=1)

        # Write back
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ {colonia_name} - BreadcrumbList agregado")
    else:
        print(f"✗ {colonia_name} - No se encontró el patrón para insertar")

print("\n✅ Proceso completado")
