#!/usr/bin/env python3
"""
FASE 1: Agregar bloque NAP después del mapa en las 30 colonias.

NAP (Name, Address, Phone) es crítico para SEO local:
- Consistencia exacta del teléfono en todas las páginas
- Asociación NAP + Mapa + Geo-específico = señal perfecta
- Google detecta patrones de contacto consistentes
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"📞 AGREGANDO BLOQUE NAP A 30 COLONIAS\n")
print(f"{'='*70}")

contador_exitosos = 0

for colonia_dir in sorted(colonias):
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        print(f"⚠️  {colonia_dir.name} - archivo index.html no encontrado")
        continue

    # Leer contenido
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer nombre de colonia
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()

    # Verificar si ya tiene el bloque NAP
    if '📞 Información de Contacto' in content:
        print(f"⏭️  {colonia_name} - Ya tiene bloque NAP, omitiendo")
        continue

    # Crear bloque NAP personalizado para esta colonia
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
                    <strong>Servicio en:</strong><br>
                    <span style="font-weight: 600; color: #2c3e50;">{colonia_name}, Culiacán, Sinaloa</span>
                </p>
            </div>
            <div>
                <p style="margin: 5px 0; color: #555;">
                    <strong>Horario:</strong><br>
                    <span style="color: #0066cc; font-weight: 600;">24/7 - Todos los días</span>
                </p>
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
            <p style="margin: 0; color: #555; font-size: 0.95em;">
                ✅ <strong>Servicio inmediato en {colonia_name}</strong> - Plomeros certificados disponibles 24 horas
            </p>
        </div>
    </div>
'''

    # Buscar el cierre de la sección del mapa y agregar NAP después
    # Patrón: Buscar </section> que cierra la sección del mapa (después de los 3 divs de servicio)
    # La estructura es: </div> (cierra grid) </div> (cierra contenedor blanco) </section> (cierra mapa)
    pattern = r'(</div>\s*</div>\s*</section>\s*\n\s*<footer)'

    if re.search(pattern, content):
        # Insertar bloque NAP después del cierre de la sección del mapa, antes del footer
        content = re.sub(pattern, r'\1' + nap_block + r'\n\n        <footer', content, count=1)

        # Escribir archivo actualizado
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {colonia_name} - Bloque NAP agregado")
        contador_exitosos += 1
    else:
        print(f"⚠️  {colonia_name} - No se encontró la sección del mapa")

print(f"\n{'='*70}")
print(f"📊 RESUMEN FASE 1:")
print(f"  ✅ Bloques NAP agregados: {contador_exitosos}/30")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*70}")

print(f"\n🎯 ELEMENTOS NAP CONSISTENTES:")
print(f"  • Teléfono: 667 163 1231 (formato consistente)")
print(f"  • WhatsApp: 52 667 163 1231 (con código país)")
print(f"  • Dirección: [Colonia], Culiacán, Sinaloa (personalizada)")
print(f"  • Horario: 24/7 - Todos los días")

print(f"\n✨ IMPACTO SEO LOCAL ESPERADO:")
print(f"  • Google detecta NAP consistente en 30 páginas")
print(f"  • Señal NAP + Mapa + Geo = TRIPLE refuerzo local")
print(f"  • Mejor posicionamiento en Google Local Pack")
print(f"  • Click-to-call optimizado para móviles")
print(f"  • WhatsApp directo para conversiones rápidas")

print(f"\n📋 PRÓXIMOS PASOS:")
print(f"  1. Commit y deploy (git add + commit + push)")
print(f"  2. Regenerar sitemap con timestamps actualizados")
print(f"  3. Verificar en Google Search Console (48-72h)")
print(f"  4. Monitorear rankings locales (1-4 semanas)")
