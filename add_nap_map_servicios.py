#!/usr/bin/env python3
"""
FASE 2: Agregar bloque NAP + Mapa a las páginas de servicios.

Diferencias vs colonias:
- Mapa: Muestra "Culiacán, Sinaloa" (ciudad completa, no colonia específica)
- NAP: "Área de cobertura: Todo Culiacán y área metropolitana"
- Mensaje personalizado por tipo de servicio
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios")

# Servicios a procesar (excluir colonias)
servicios = [
    'correccion-baja-presion',
    'destape-de-drenajes',
    'deteccion-de-fugas',
    'emergencia-24-7',
    'instalacion-de-sanitarios',
    'mantenimiento-de-boiler',
    'plomero-a-domicilio',
    'plomero-cerca-de-mi',
    'plomero-precios',
    'plomero',
    'reparacion-de-fugas'
]

# Mapeo de slugs a nombres legibles para el mensaje personalizado
servicio_nombres = {
    'correccion-baja-presion': 'corrección de baja presión',
    'destape-de-drenajes': 'destape de drenajes',
    'deteccion-de-fugas': 'detección de fugas',
    'emergencia-24-7': 'emergencias 24/7',
    'instalacion-de-sanitarios': 'instalación de sanitarios',
    'mantenimiento-de-boiler': 'mantenimiento de boiler',
    'plomero-a-domicilio': 'plomero a domicilio',
    'plomero-cerca-de-mi': 'plomero cerca de ti',
    'plomero-precios': 'servicios de plomería',
    'plomero': 'plomería profesional',
    'reparacion-de-fugas': 'reparación de fugas'
}

print(f"🔧 AGREGANDO NAP + MAPA A {len(servicios)} PÁGINAS DE SERVICIOS\n")
print(f"{'='*70}")

contador_exitosos = 0

for servicio_slug in servicios:
    servicio_dir = base_dir / servicio_slug
    index_file = servicio_dir / "index.html"

    if not index_file.exists():
        print(f"⚠️  {servicio_slug} - archivo index.html no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nombre legible del servicio
    servicio_nombre = servicio_nombres.get(servicio_slug, servicio_slug.replace('-', ' '))

    # Verificar si ya tiene el bloque NAP
    if '📞 Información de Contacto' in content:
        print(f"⏭️  {servicio_nombre} - Ya tiene bloque NAP, omitiendo")
        continue

    # 1. AGREGAR MAPA (si no existe ya)
    if 'Mapa Interactivo' not in content and 'google.com/maps' not in content:
        mapa_section = '''
        <!-- Mapa Interactivo -->
        <section style="margin: 40px 0; padding: 30px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">
            <h2 style="color: #2c3e50; margin-bottom: 20px; font-size: 1.8em; text-align: center;">
                📍 Área de Servicio en Culiacán
            </h2>

            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 50%; margin: 0 auto;">
                <p style="color: #555; margin-bottom: 20px; line-height: 1.6;">
                    Brindamos servicio profesional en toda la ciudad de <strong>Culiacán, Sinaloa</strong>
                    y área metropolitana. Llegada rápida a cualquier colonia.
                </p>

                <!-- Google Maps Embed -->
                <div style="position: relative; padding-bottom: 28%; height: 0; overflow: hidden; border-radius: 8px;">
                    <iframe src="https://www.google.com/maps?q=Culiacán,+Sinaloa,+México&output=embed"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                        allowfullscreen=""
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade"
                        title="Mapa de Culiacán, Sinaloa">
                    </iframe>
                </div>

                <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">
                    <p style="margin: 0; color: #2e7d32; font-weight: 600;">
                        ⚡ Tiempo de llegada promedio: 20-40 minutos a cualquier punto de Culiacán
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
        </section>
'''
        # Buscar el footer para insertar el mapa antes
        pattern_mapa = r'(\s*<footer)'
        if re.search(pattern_mapa, content):
            content = re.sub(pattern_mapa, mapa_section + r'\n\1', content, count=1)

    # 2. AGREGAR BLOQUE NAP (después del mapa, antes del footer)
    nap_block = f'''
    <!-- Bloque NAP (Name, Address, Phone) para SEO Local -->
    <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; margin: 30px 0; border-left: 4px solid #0066cc;">
        <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 1.3em;">
            📞 Información de Contacto
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div>
                <p style="margin: 5px 0; color: #555;">
                    <strong>Teléfono:</strong><br>
                    <a href="tel:6671631231" style="color: #0066cc; text-decoration: none; font-size: 1.1em;">667 163 1231</a>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; color: #555;">
                    <strong>WhatsApp:</strong><br>
                    <a href="https://wa.me/526671631231" style="color: #0066cc; text-decoration: none; font-size: 1.1em;">52 667 163 1231</a>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; color: #555;">
                    <strong>Área de cobertura:</strong><br>
                    <span style="font-weight: 600; color: #2c3e50;">Todo Culiacán y área metropolitana</span>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; color: #555;">
                    <strong>Horario:</strong><br>
                    <span style="color: #0066cc; font-weight: 600;">24/7 - Emergencias incluidas</span>
                </p>
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
            <p style="margin: 0; color: #555; font-size: 0.95em;">
                ✅ <strong>Servicio profesional de {servicio_nombre}</strong> - Atención inmediata en toda la ciudad
            </p>
        </div>
    </div>
'''

    # Buscar el footer y agregar NAP antes
    pattern_nap = r'(\s*<footer)'
    if re.search(pattern_nap, content):
        content = re.sub(pattern_nap, nap_block + r'\n\1', content, count=1)

        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {servicio_nombre.title()} - NAP + Mapa agregados")
        contador_exitosos += 1
    else:
        print(f"⚠️  {servicio_nombre} - No se encontró el footer")

print(f"\n{'='*70}")
print(f"📊 RESUMEN FASE 2:")
print(f"  ✅ NAP + Mapa agregados: {contador_exitosos}/{len(servicios)}")
print(f"  📄 Total servicios procesados: {len(servicios)}")
print(f"{'='*70}")

print(f"\n🎯 ELEMENTOS AGREGADOS:")
print(f"  • Mapa de Culiacán (ciudad completa)")
print(f"  • NAP consistente con colonias")
print(f"  • Área de cobertura: Todo Culiacán")
print(f"  • Mensaje personalizado por servicio")

print(f"\n✨ IMPACTO SEO LOCAL ESPERADO:")
print(f"  • NAP consistente en 30 colonias + 11 servicios = 41 páginas")
print(f"  • Google detecta patrón de negocio local sólido")
print(f"  • Señal local reforzada en páginas generales")
print(f"  • Mejor ranking para búsquedas de servicio + ciudad")
print(f"  • Click-to-call optimizado en todas las páginas")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"  1. Commit y deploy (git add + commit + push)")
print(f"  2. Regenerar sitemap con timestamps actualizados")
print(f"  3. Verificar en Google Search Console (48-72h)")
print(f"  4. Monitorear rankings (1-4 semanas)")
