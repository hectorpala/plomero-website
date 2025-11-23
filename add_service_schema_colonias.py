#!/usr/bin/env python3
"""
Agrega Service schema a las 30 páginas de colonias.
Complementa BreadcrumbList y FAQPage existentes.
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Definir preguntas base que se personalizarán por colonia
def generate_service_schema(colonia_name, colonia_slug):
    """Genera el Service schema personalizado para cada colonia"""

    # Determinar tipo de colonia para personalizar
    colonias_premium = ['las-quintas', 'tres-rios', 'country-tres-rios', 'campestre',
                        'colinas-de-san-miguel', 'lomas-del-boulevard', 'chapultepec']

    es_premium = colonia_slug in colonias_premium

    # Precio personalizado
    if es_premium:
        precio_min = "1000"
        precio_max = "2500"
        precio_currency = "MXN"
    else:
        precio_min = "800"
        precio_max = "2000"
        precio_currency = "MXN"

    # Descripción específica
    if es_premium:
        descripcion = f"Servicio profesional de plomería en {colonia_name}, Culiacán. Especialistas en residencias premium con sistemas hidroneumáticos, boilers de paso y grifería importada. Atención 24/7 con llegada en 20-30 minutos. Garantía de 6 meses."
    else:
        descripcion = f"Servicio profesional de plomería en {colonia_name}, Culiacán. Experiencia en sistemas residenciales, reparación de fugas, destape de drenajes e instalaciones. Atención 24/7 con llegada en 25-40 minutos. Garantía de 6 meses."

    schema = f'''
    <!-- Service Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Service",
      "serviceType": "Servicios de Plomería Residencial",
      "name": "Plomero en {colonia_name}",
      "description": "{descripcion}",
      "provider": {{
        "@type": "LocalBusiness",
        "name": "Plomero Culiacán Pro",
        "telephone": "+526671631231",
        "priceRange": "$$",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "Culiacán",
          "addressRegion": "Sinaloa",
          "addressCountry": "MX"
        }},
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "4.8",
          "reviewCount": "150"
        }}
      }},
      "areaServed": {{
        "@type": "Place",
        "name": "{colonia_name}, Culiacán, Sinaloa",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "Culiacán",
          "addressRegion": "Sinaloa",
          "addressCountry": "MX"
        }}
      }},
      "offers": {{
        "@type": "Offer",
        "priceCurrency": "{precio_currency}",
        "price": "{precio_min}",
        "priceSpecification": {{
          "@type": "PriceSpecification",
          "minPrice": "{precio_min}",
          "maxPrice": "{precio_max}",
          "priceCurrency": "{precio_currency}"
        }},
        "availability": "https://schema.org/InStock"
      }},
      "availableChannel": {{
        "@type": "ServiceChannel",
        "serviceUrl": "https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_slug}/",
        "servicePhone": "+526671631231",
        "availableLanguage": {{
          "@type": "Language",
          "name": "Spanish"
        }}
      }},
      "hoursAvailable": {{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"
        ],
        "opens": "00:00",
        "closes": "23:59"
      }},
      "serviceOutput": [
        "Reparación de fugas de agua",
        "Destape de drenajes y tuberías",
        "Instalación de sanitarios y llaves",
        "Mantenimiento de boilers",
        "Detección de fugas con equipo especializado",
        "Corrección de baja presión de agua"
      ]
    }}
    </script>'''

    return schema

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"🔍 Encontradas {len(colonias)} colonias para procesar\n")

contador_exitosos = 0
contador_omitidos = 0

for colonia_dir in sorted(colonias):
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        print(f"⚠️  {colonia_dir.name} - archivo index.html no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar si ya tiene Service schema
    if '"@type": "Service"' in content or '"@type":"Service"' in content:
        print(f"✓ {colonia_dir.name} - Service schema ya existe, omitiendo")
        contador_omitidos += 1
        continue

    # Extraer nombre de colonia del directorio
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Generar schema Service
    service_schema = generate_service_schema(colonia_name, colonia_slug)

    # Buscar el lugar donde insertar (después de FAQPage, antes de </head>)
    # Patrón: encontrar el cierre del FAQPage y agregar Service después
    pattern1 = r'(}\s*</script>\s*</head>)'
    pattern2 = r'(</head>)'

    inserted = False

    # Intentar insertar después del último </script> antes de </head>
    if re.search(pattern1, content):
        content = re.sub(pattern1, service_schema + r'\1', content, count=1)
        inserted = True
    elif re.search(pattern2, content):
        # Insertar antes de </head> directamente
        content = re.sub(pattern2, service_schema + r'\1', content, count=1)
        inserted = True

    if inserted:
        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {colonia_name} - Service schema agregado exitosamente")
        contador_exitosos += 1
    else:
        print(f"❌ {colonia_name} - No se encontró el patrón de inserción")

print(f"\n{'='*60}")
print(f"📊 RESUMEN:")
print(f"  ✅ Exitosos: {contador_exitosos}")
print(f"  ⏭️  Omitidos (ya existían): {contador_omitidos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*60}")
print(f"\n🎯 Service schema agregado a {contador_exitosos} páginas de colonias")
print(f"\n📋 SCHEMAS POR PÁGINA:")
print(f"  1. BreadcrumbList ✅ (navegación)")
print(f"  2. FAQPage ✅ (8 preguntas)")
print(f"  3. Service ✅ (definición del servicio) ← NUEVO")
print(f"\n🔍 Beneficios del Service Schema:")
print(f"  • Mejor comprensión por Google del servicio ofrecido")
print(f"  • Información de precios estructurada")
print(f"  • Horarios de disponibilidad 24/7")
print(f"  • Área de servicio específica por colonia")
print(f"  • Rating y reseñas del negocio")
print(f"\n🔍 Verifica en Google Rich Results Test:")
print(f"  https://search.google.com/test/rich-results")
