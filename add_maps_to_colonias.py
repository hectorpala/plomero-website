#!/usr/bin/env python3
"""
Agrega mapas interactivos de Google Maps a las 30 páginas de colonias.
Mejora UX local y señales de geolocalización para SEO.
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Coordenadas aproximadas del centro de cada colonia en Culiacán
# Formato: (latitud, longitud, zoom_level)
COORDENADAS_COLONIAS = {
    'las-quintas': (24.8247, -107.4177, 15),
    'tres-rios': (24.8089, -107.4386, 15),
    'country-tres-rios': (24.8156, -107.4419, 15),
    'chapultepec': (24.7989, -107.3936, 15),
    'campestre': (24.8203, -107.3947, 15),
    'colinas-de-san-miguel': (24.8334, -107.4267, 15),
    'lomas-del-boulevard': (24.8156, -107.3825, 15),
    'guadalupe': (24.8556, -107.3936, 15),
    'centro': (24.8089, -107.3936, 15),
    'infonavit-humaya': (24.7922, -107.4219, 15),
    'bachigualato': (24.8556, -107.4519, 15),
    'hacienda-del-valle': (24.8403, -107.4486, 15),
    'hacienda-los-huertos': (24.8269, -107.4553, 15),
    'villa-universidad': (24.8469, -107.4086, 15),
    'cumbres-tres-rios': (24.8203, -107.4486, 15),
    'portales-del-rio': (24.8203, -107.4353, 15),
    'real-del-valle': (24.8334, -107.4419, 15),
    'real-san-angel': (24.8269, -107.4286, 15),
    'bosques-del-humaya': (24.7989, -107.4386, 15),
    'jardines-del-valle': (24.8403, -107.4219, 15),
    'colinas-de-la-rivera': (24.8469, -107.4153, 15),
    'lomas-de-san-isidro': (24.8334, -107.3825, 15),
    'las-palmas': (24.8089, -107.4086, 15),
    'nuevo-culiacan': (24.7789, -107.4086, 15),
    'montebello': (24.8469, -107.3936, 15),
    'villa-bonita': (24.8203, -107.4086, 15),
    'zona-dorada': (24.8089, -107.3825, 15),
    'santa-fe': (24.8334, -107.4086, 15),
    'altamira': (24.8156, -107.4219, 15),
    'isla-del-oeste': (24.7856, -107.4553, 15),
}

def generate_map_section(colonia_name, colonia_slug):
    """Genera la sección del mapa interactivo para cada colonia"""

    # Obtener coordenadas (usar coordenadas por defecto si no existe)
    lat, lng, zoom = COORDENADAS_COLONIAS.get(
        colonia_slug,
        (24.8089, -107.3936, 14)  # Centro de Culiacán por defecto
    )

    map_section = f'''
        <!-- Mapa Interactivo de la Zona -->
        <section style="margin: 40px 0; padding: 30px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">
            <h2 style="color: #2c3e50; margin-bottom: 20px; font-size: 1.8em; text-align: center;">
                📍 Ubicación y Zona de Servicio en {colonia_name}
            </h2>

            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="color: #555; margin-bottom: 20px; line-height: 1.6;">
                    Nuestro equipo de plomeros profesionales brinda servicio en toda la colonia <strong>{colonia_name}</strong>
                    y áreas circundantes. El mapa a continuación muestra nuestra zona de cobertura principal.
                </p>

                <!-- Google Maps Embed -->
                <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px;">
                    <iframe
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3554.{int(lat*100)}.{int(lng*100)}!2d{lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2z{lat}°N%20{abs(lng)}°W!5e0!3m2!1ses-419!2smx!4v{zoom}z"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                        allowfullscreen=""
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade"
                        title="Mapa de {colonia_name}, Culiacán">
                    </iframe>
                </div>

                <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">
                    <p style="margin: 0; color: #2e7d32; font-weight: 600;">
                        ⚡ Tiempo de llegada promedio a {colonia_name}: {'20-30 minutos' if colonia_slug in ['las-quintas', 'tres-rios', 'country-tres-rios', 'campestre', 'colinas-de-san-miguel', 'lomas-del-boulevard', 'chapultepec'] else '25-40 minutos'}
                    </p>
                </div>

                <div style="margin-top: 15px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="padding: 15px; background: #fff3e0; border-radius: 6px;">
                        <p style="margin: 0; color: #e65100; font-weight: 600;">📞 Llamada</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Respuesta inmediata 24/7</p>
                    </div>
                    <div style="padding: 15px; background: #e3f2fd; border-radius: 6px;">
                        <p style="margin: 0; color: #1565c0; font-weight: 600;">🚗 Llegada</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Unidad equipada lista</p>
                    </div>
                    <div style="padding: 15px; background: #f3e5f5; border-radius: 6px;">
                        <p style="margin: 0; color: #6a1b9a; font-weight: 600;">🔧 Servicio</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Solución profesional</p>
                    </div>
                </div>
            </div>
        </section>'''

    return map_section

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"🗺️  Preparando mapas interactivos para {len(colonias)} colonias\n")

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

    # Verificar si ya tiene mapa
    if '📍 Ubicación y Zona de Servicio' in content or 'maps.google.com/maps/embed' in content:
        print(f"✓ {colonia_dir.name} - Mapa ya existe, omitiendo")
        contador_omitidos += 1
        continue

    # Extraer nombre de colonia
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Generar sección del mapa
    map_section = generate_map_section(colonia_name, colonia_slug)

    # Buscar el lugar donde insertar (después de las FAQs, antes del footer/final)
    # Patrón: Insertar antes de la sección de contacto o antes del cierre de main/body
    patterns = [
        (r'(<section[^>]*class="cta"[^>]*>)', 'antes del CTA'),
        (r'(<footer)', 'antes del footer'),
        (r'(</main>)', 'antes del cierre de main'),
        (r'(</body>)', 'antes del cierre de body'),
    ]

    inserted = False

    for pattern, desc in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, map_section + r'\n\n        \1', content, count=1, flags=re.IGNORECASE)
            inserted = True
            print(f"✅ {colonia_name} - Mapa agregado exitosamente ({desc})")
            break

    if inserted:
        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        contador_exitosos += 1
    else:
        print(f"❌ {colonia_name} - No se encontró patrón de inserción adecuado")

print(f"\n{'='*60}")
print(f"📊 RESUMEN:")
print(f"  ✅ Mapas agregados: {contador_exitosos}")
print(f"  ⏭️  Omitidos (ya existían): {contador_omitidos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*60}")
print(f"\n🗺️  Mapas interactivos agregados a {contador_exitosos} páginas")
print(f"\n📋 BENEFICIOS:")
print(f"  • Mejor UX - usuarios ven la zona de cobertura")
print(f"  • Señales de geolocalización para Google")
print(f"  • Reduce dudas sobre si llegamos a su zona")
print(f"  • Aumenta confianza al ver ubicación exacta")
print(f"  • Embedded iframe = señal de contenido rico")
print(f"\n✨ CARACTERÍSTICAS DE LOS MAPAS:")
print(f"  • Google Maps embebido responsive")
print(f"  • Coordenadas específicas por colonia")
print(f"  • Tiempo de llegada estimado")
print(f"  • Diseño visual atractivo con gradientes")
print(f"  • Iconos de proceso (llamada → llegada → servicio)")
print(f"  • Lazy loading para mejor rendimiento")
