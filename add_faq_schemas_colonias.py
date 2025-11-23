#!/usr/bin/env python3
"""
Script para agregar FAQPage schema a todas las páginas de colonias
Agrega 8 preguntas específicas por colonia con contenido personalizado
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Definir preguntas base que se personalizarán por colonia
def generate_faq_schema(colonia_name, colonia_slug):
    """Genera el schema FAQPage personalizado para cada colonia"""

    # Determinar tipo de colonia para personalizar respuestas
    colonias_premium = ['las-quintas', 'tres-rios', 'country-tres-rios', 'campestre',
                        'colinas-de-san-miguel', 'lomas-del-boulevard']
    colonias_populares = ['guadalupe', 'centro', 'infonavit-humaya', 'bachigualato']

    es_premium = colonia_slug in colonias_premium
    es_popular = colonia_slug in colonias_populares

    # Tiempo de llegada personalizado
    tiempo_llegada = "20-30 minutos" if es_premium else "25-40 minutos"

    # Precio base personalizado
    if es_premium:
        rango_precio = "$1,000-$2,500"
        detalle_precio = "Los costos pueden ser mayores debido al uso de materiales premium y la complejidad de los sistemas en residencias de lujo."
    elif es_popular:
        rango_precio = "$600-$1,800"
        detalle_precio = "Ofrecemos precios accesibles sin comprometer la calidad del servicio."
    else:
        rango_precio = "$800-$2,000"
        detalle_precio = "El precio incluye diagnóstico, mano de obra, materiales y garantía de 6 meses."

    # Sistemas específicos
    if es_premium:
        sistemas_especificos = "sistemas hidroneumáticos, boilers de paso de alta gama, grifería importada (Grohe, Hansgrohe, Kohler) y múltiples baños con instalaciones complejas"
    else:
        sistemas_especificos = "tinaco estándar, boilers de depósito, grifería nacional y sistemas de 1-2 baños típicos de la zona"

    schema = f'''
    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "¿Cuánto tarda el plomero en llegar a {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Llegamos en {tiempo_llegada} a {colonia_name} desde nuestra base en Culiacán. Conocemos perfectamente la zona, los accesos principales y estamos familiarizados con las características específicas del fraccionamiento. Atendemos emergencias 24/7 todos los días del año."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Cuánto cuesta el servicio de plomería en {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Los precios en {colonia_name} generalmente van desde {rango_precio} dependiendo del tipo de trabajo: visita diagnóstico desde $300, reparación de fugas $800-$1,500, destape de drenaje $600-$1,200, instalación de sanitarios $900-$2,000. {detalle_precio} Cotizamos sin compromiso por WhatsApp al 667 163 1231."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Conocen los sistemas de plomería específicos de {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Sí, tenemos más de 10 años de experiencia trabajando en {colonia_name}. Conocemos los {sistemas_especificos}. Esto nos permite hacer diagnósticos más rápidos y reparaciones más efectivas porque sabemos exactamente qué esperar."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Atienden emergencias de plomería en {colonia_name} de madrugada?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Sí, nuestro servicio de emergencia 24/7 incluye atención en {colonia_name} durante madrugadas, fines de semana y días festivos. Para emergencias urgentes (fugas grandes, inundaciones, drenajes colapsados) llamar directamente al 667 163 1231. Para consultas menos urgentes, escribir por WhatsApp y respondemos en minutos."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Qué garantía ofrecen en los trabajos realizados en {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Todos nuestros trabajos en {colonia_name} incluyen garantía escrita de 6 meses en mano de obra y materiales. Esto cubre cualquier defecto relacionado con la reparación realizada. Usamos refacciones originales y técnicas profesionales certificadas. Si presenta algún problema dentro del período de garantía, regresamos sin costo adicional."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Dan factura electrónica por los servicios en {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Sí, emitimos factura electrónica (CFDI) para todos los servicios realizados en {colonia_name}. Solo necesitamos tu RFC y razón social. La factura se envía por correo electrónico el mismo día o al día siguiente del servicio. Aceptamos pagos en efectivo, transferencia bancaria y tarjetas de crédito/débito."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Cuáles son los problemas de plomería más comunes en {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "En {colonia_name} los problemas más frecuentes que atendemos son: fugas en tuberías ocultas (muros y pisos), drenajes tapados por acumulación de residuos, baja presión de agua, fallas en boilers y calentadores, fugas en llaves y mezcladoras, y problemas con tinaco o sistemas de bombeo. Cada zona tiene características particulares según la antigüedad de las construcciones."
          }}
        }},
        {{
          "@type": "Question",
          "name": "¿Necesito estar presente durante el servicio en {colonia_name}?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Idealmente sí, es recomendable que alguien esté presente durante el servicio en {colonia_name} para autorizar el trabajo, mostrar el problema específico y recibir explicaciones sobre la reparación realizada. Sin embargo, si no es posible, podemos coordinar con personal de confianza, familiares o vecinos. Enviamos fotos y videos del trabajo por WhatsApp para mantener informado al propietario."
          }}
        }}
      ]
    }}
    </script>
'''
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

    # Verificar si ya tiene FAQPage schema
    if '"@type": "FAQPage"' in content or '"@type":"FAQPage"' in content:
        print(f"✓ {colonia_dir.name} - FAQPage ya existe, omitiendo")
        contador_omitidos += 1
        continue

    # Extraer nombre de colonia del directorio
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Generar schema FAQPage
    faq_schema = generate_faq_schema(colonia_name, colonia_slug)

    # Buscar el lugar donde insertar (antes de </head> o antes de <style>)
    # Patrón más flexible para encontrar el cierre del BreadcrumbList
    pattern1 = r'(</script>\s*</head>)'
    pattern2 = r'(</script>\s*<style>)'
    pattern3 = r'(</head>)'

    inserted = False

    if re.search(pattern1, content):
        # Insertar FAQPage schema antes del cierre de </head>
        content = re.sub(pattern1, faq_schema + r'\1', content, count=1)
        inserted = True
    elif re.search(pattern2, content):
        # Insertar FAQPage schema antes del <style>
        content = re.sub(pattern2, faq_schema + r'\1', content, count=1)
        inserted = True
    elif re.search(pattern3, content):
        # Intentar insertar antes de </head> directamente
        content = re.sub(pattern3, faq_schema + r'\1', content, count=1)
        inserted = True

    if inserted:
        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {colonia_name} - FAQPage schema agregado exitosamente")
        contador_exitosos += 1
    else:
        print(f"❌ {colonia_name} - No se encontró el patrón de inserción")

print(f"\n{'='*60}")
print(f"📊 RESUMEN:")
print(f"  ✅ Exitosos: {contador_exitosos}")
print(f"  ⏭️  Omitidos (ya existían): {contador_omitidos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*60}")
print(f"\n🎯 FAQPage schema agregado a {contador_exitosos} páginas de colonias")
print(f"🔍 Verifica en Google Rich Results Test: https://search.google.com/test/rich-results")
