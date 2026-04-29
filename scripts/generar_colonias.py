#!/usr/bin/env python3
"""
Generador de páginas de colonias — Plomero Culiacán Pro
Lee colonias-data.json y aplica contenido real a cada página HTML.

Uso:
    python3 scripts/generar_colonias.py                    # genera todas
    python3 scripts/generar_colonias.py --slug burocrata   # genera solo una
    python3 scripts/generar_colonias.py --dry-run          # muestra qué haría sin escribir
"""

import json
import os
import re
import argparse
from pathlib import Path

# ─── Rutas ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
COLONIAS_DIR = BASE_DIR / "servicios" / "plomero-colonias-culiacan"
DATA_FILE = BASE_DIR / "colonias-data.json"

# ─── Narrativas por era ───────────────────────────────────────────────────────
# Cada era define: intro_p1_template, intro_p2, beneficios, servicios
# Las variables {nombre}, {calle_principal}, {landmark}, {cp} se reemplazan dinámicamente.

ERAS = {
    "pre1960": {
        "label": "Barrio popular pre-1960",
        "descripcion_era": "fundado antes de 1960",
        "antiguedad": "60-80 años",
        "tuberia": "tuberías galvanizadas originales — y en muchos casos de asbesto-cemento",
        "problema_central": "agua con olor metálico o color rojizo, fugas en conexiones roscadas oxidadas y drenajes de barro vidriado con décadas de acumulación",
        "intro_p2": (
            "Las construcciones originales de {nombre} eran de tabique y materiales reciclados "
            "que se ampliaron generación tras generación. Esas ampliaciones mezclaron tubería "
            "galvanizada de los años 50-60 con cobre de los 70 y PVC de los 80-90, creando "
            "instalaciones incompatibles que generan corrosión galvánica y fugas crónicas. "
            "El drenaje original era de barro vidriado — con décadas de acumulación que ningún "
            "parche temporal resuelve. Conocemos la colonia y llegamos preparados."
        ),
        "beneficios": [
            ("🏚️", "Instalaciones 60+ años", "Diagnóstico de galvanizado, cobre y PVC mezclados en una sola casa"),
            ("⚡", "Llegada en 25-35 min", "Desde {calle_principal} hasta cualquier calle interna"),
            ("💧", "Agua Herrumbrosa", "Señal de galvanizado vencido — lo resolvemos de raíz"),
            ("🔧", "Drenaje Histórico", "Limpieza de albañales con décadas de barro y sedimento"),
            ("🧾", "Factura SAT", "Para vecinos y negocios de {nombre}"),
        ],
        "servicios": [
            ("Diagnóstico de Instalaciones Mixtas",
             "Galvanizado + cobre + PVC de distintas épocas en una misma casa. Identificamos "
             "la causa raíz de la corrosión y la resolvemos definitivamente."),
            ("Reemplazo de Tubería Antigua",
             "Galvanizado y asbesto de 60-70 años reemplazado por CPVC uniforme. "
             "La solución definitiva para presión baja y agua con olor metálico."),
            ("Destape de Drenajes Históricos",
             "Tuberías de barro vidriado con 60+ años de sedimento, grasa y raíces. "
             "Limpieza profesional con equipo de alta presión."),
            ("Reparación de Fugas en Muros",
             "Conexiones roscadas de 50-70 años con fisuras por corrosión. "
             "Detección y reparación sin demolición innecesaria."),
            ("Tinacos y Cisternas",
             "Revisión de flotadores y válvulas en sistemas con décadas de uso. "
             "Mantenimiento preventivo antes de que fallen."),
            ("Emergencias 24/7",
             "Atención inmediata en toda {nombre}: desde {calle_principal} "
             "hasta las calles más internas. Cualquier día."),
        ],
        "cobertura": [
            "{calle_principal} y calles internas",
            "Zona {landmark}",
            "Privadas y callejones del barrio",
        ],
    },

    "1960s-1975": {
        "label": "Colonia popular/obrera 1960s-1975",
        "descripcion_era": "desarrollado entre los años 60 y 75",
        "antiguedad": "50-60 años",
        "tuberia": "tuberías galvanizadas de primera y segunda generación",
        "problema_central": "baja presión crónica, fugas en codos y uniones roscadas, y calentadores con sarro por el agua dura de Culiacán",
        "intro_p2": (
            "Con 50-60 años de antigüedad, las instalaciones hidráulicas de {nombre} "
            "presentan el deterioro típico del galvanizado: corrosión interna que reduce "
            "el diámetro útil de la tubería, manchas oxidadas en el agua y caídas de "
            "presión en horas pico. El agua dura que distribuye JAPAC acumula sarro en "
            "boilers y calentadores de paso, reduciendo su vida útil varios años. "
            "Llegamos preparados para resolver sin segunda visita."
        ),
        "beneficios": [
            ("🔧", "Tubería 50+ años", "Reemplazamos galvanizado de los 60s-70s por CPVC o cobre"),
            ("⚡", "Llegada en 25-35 min", "Desde {calle_principal} hasta cualquier calle interna"),
            ("💧", "Baja Presión", "Diagnóstico de red interior, hidroneumáticos y conexión JAPAC"),
            ("🔥", "Sarro en Calentadores", "Limpieza y mantenimiento por agua dura de Culiacán"),
            ("🧾", "Factura SAT", "Para casas y negocios de {nombre}"),
        ],
        "servicios": [
            ("Cambio de Tubería Galvanizada",
             "Instalaciones de los años 60s-70s reemplazadas por CPVC o cobre. "
             "La solución definitiva para presión baja crónica en {nombre}."),
            ("Baja Presión Crónica",
             "Diagnóstico de red interior, hidroneumáticos y conexión a la red JAPAC. "
             "Frecuente en casas de más de 50 años en la zona."),
            ("Limpieza de Calentadores",
             "El agua dura de Culiacán acumula sarro en boilers y calentadores de paso. "
             "Mantenimiento y reparación con garantía escrita."),
            ("Reparación de Fugas",
             "Detección y reparación de fugas ocultas en muros y losas. "
             "Sin demolición innecesaria en casas de tabique antiguo."),
            ("Destape de Drenajes",
             "Limpieza de albañales con 50+ años de acumulación. "
             "Equipo de alta presión para obstrucciones severas."),
            ("Emergencias 24/7",
             "Atención inmediata en toda {nombre}: desde {calle_principal} "
             "hasta las privadas más internas. Cualquier día."),
        ],
        "cobertura": [
            "{calle_principal} y calles internas",
            "Zona {landmark}",
            "Privadas residenciales del sector",
        ],
    },

    "infonavit": {
        "label": "INFONAVIT / FOVISSSTE 1972-1990",
        "descripcion_era": "desarrollado por INFONAVIT o FOVISSSTE entre 1972 y 1990",
        "antiguedad": "35-50 años",
        "tuberia": "tubería galvanizada de primera generación instalada por el instituto",
        "problema_central": "corrosión interna en galvanizado, golpes de ariete por cortes de JAPAC y sarro en boilers por agua dura",
        "intro_p2": (
            "Las viviendas de interés social de {nombre} tienen entre 35 y 50 años de "
            "antigüedad con instalaciones hidráulicas en galvanizado que nunca se han "
            "renovado integralmente. Los cortes de agua programados y emergencias de JAPAC "
            "generan golpes de ariete que dañan válvulas y conexiones ya debilitadas. "
            "El agua dura de Culiacán acumula sarro en boilers y calentadores de paso. "
            "Conocemos la colonia y llegamos preparados."
        ),
        "beneficios": [
            ("🏗️", "Vivienda Social 40+ años", "Galvanizado original sin renovar — diagnóstico y reemplazo definitivo"),
            ("⚡", "Llegada en 25-35 min", "Desde {calle_principal} hasta cualquier calle interna"),
            ("💧", "Post-Corte JAPAC", "Revisión de válvulas y presión tras interrupciones de la red"),
            ("🔥", "Sarro en Calentadores", "Mantenimiento preventivo por agua dura"),
            ("🧾", "Factura SAT", "Para casas y comercios de {nombre}"),
        ],
        "servicios": [
            ("Diagnóstico de Tubería Galvanizada",
             "40-50 años de deterioro: oxidación interna, baja presión y fugas ocultas. "
             "Diagnóstico completo y reemplazo definitivo por CPVC."),
            ("Revisión Post-Corte JAPAC",
             "Los cortes de la red generan golpes de ariete que dañan válvulas y conexiones "
             "en instalaciones ya debilitadas. Revisión y normalización de presión."),
            ("Limpieza de Calentadores",
             "El agua dura de Culiacán daña boilers en 8-12 años aunque sean de buena marca. "
             "Limpieza y mantenimiento preventivo con garantía."),
            ("Baja Presión Crónica",
             "Red interna de vivienda social sin renovar. "
             "Diagnóstico de instalación interior, bomba y conexión a JAPAC."),
            ("Destape de Drenajes",
             "Albañales con décadas de sedimento y grasa. "
             "Limpieza profesional con equipo de alta presión."),
            ("Emergencias 24/7",
             "Atención inmediata en toda {nombre}: desde {calle_principal} "
             "hasta las privadas más internas. Cualquier día."),
        ],
        "cobertura": [
            "{calle_principal} y calles internas",
            "Zona {landmark}",
            "Circuitos y privadas del fraccionamiento",
        ],
    },

    "residencial-70-90": {
        "label": "Fraccionamiento residencial 1970-1990",
        "descripcion_era": "desarrollado entre 1970 y 1990",
        "antiguedad": "35-55 años",
        "tuberia": "tuberías galvanizadas o de cobre de los años 70-80",
        "problema_central": "fugas ocultas en muros, presión baja por corrosión interna y sarro en hidroneumáticos y calentadores",
        "intro_p2": (
            "Las casas residenciales de {nombre} tienen entre 35 y 55 años de antigüedad "
            "con instalaciones hidráulicas que en muchos casos nunca se han renovado "
            "integralmente. El galvanizado instalado en los años 70-80 presenta corrosión "
            "interna que reduce el flujo hasta la mitad. Los sistemas hidroneumáticos y "
            "calentadores de paso acumulan sarro por el agua dura de JAPAC. "
            "Llegamos preparados para resolver sin segunda visita."
        ),
        "beneficios": [
            ("🔍", "Fugas Ocultas", "Detección sin demoler en muros de casas de 40-50 años"),
            ("⚡", "Llegada en 25-35 min", "Desde {calle_principal} hasta cualquier calle interna"),
            ("💧", "Hidroneumáticos", "Reparación y sustitución de sistemas con 20-30 años de uso"),
            ("🔥", "Sarro en Calentadores", "Mantenimiento por agua dura JAPAC"),
            ("🧾", "Factura SAT", "Para casas y negocios de {nombre}"),
        ],
        "servicios": [
            ("Detección de Fugas Ocultas",
             "Casas de 40-50 años con galvanizado o cobre presentan fugas en muros sin "
             "manifestación visible. Detección con equipo especializado sin demoler."),
            ("Cambio de Tubería Galvanizada",
             "Instalaciones de los 70s-80s reemplazadas por CPVC o cobre. "
             "La solución definitiva para presión baja crónica en {nombre}."),
            ("Hidroneumáticos y Bombas",
             "Reparación y sustitución de membrana, presostato y bomba en sistemas "
             "con 20-30 años de uso. Común en residencias de la zona."),
            ("Limpieza de Calentadores",
             "El agua dura de Culiacán acumula sarro en boilers y calentadores. "
             "Mantenimiento preventivo y reparación con garantía escrita."),
            ("Cisternas Subterráneas",
             "Revisión, limpieza y sellado de grietas en cisternas con 30-50 años. "
             "Mantenimiento recomendado cada 2 años."),
            ("Emergencias 24/7",
             "Atención inmediata en toda {nombre}: desde {calle_principal} "
             "hasta todas las privadas. Cualquier día."),
        ],
        "cobertura": [
            "{calle_principal} y calles internas",
            "Zona {landmark}",
            "Privadas residenciales del sector",
        ],
    },

    "moderno-90-2010": {
        "label": "Fraccionamiento moderno 1990-2010",
        "descripcion_era": "desarrollado entre 1990 y 2010",
        "antiguedad": "15-35 años",
        "tuberia": "tubería PVC/CPVC de 15-30 años",
        "problema_central": "sarro en calentadores por agua dura, variaciones de presión por cortes de JAPAC y fugas en uniones de PVC",
        "intro_p2": (
            "Aunque las construcciones de {nombre} son más recientes que en colonias "
            "tradicionales, la zona tiene sus propios retos: el agua dura que distribuye "
            "JAPAC acumula sarro en calentadores de paso con apenas 8-12 años de uso. "
            "Las variaciones de presión por cortes programados generan golpes de ariete "
            "que dañan uniones y válvulas de PVC. Conocemos la colonia y llegamos "
            "en 25-35 minutos."
        ),
        "beneficios": [
            ("🔥", "Sarro en Calentadores", "El agua de Culiacán los daña aunque sean nuevos"),
            ("⚡", "Llegada en 25-35 min", "Desde {calle_principal} hasta todas las privadas"),
            ("💧", "Post-Corte JAPAC", "Revisión de válvulas y presión tras interrupciones"),
            ("🔧", "Fugas en PVC", "Uniones que fallan por golpes de presión"),
            ("🧾", "Factura SAT", "Para casas y negocios de {nombre}"),
        ],
        "servicios": [
            ("Limpieza de Calentadores",
             "El agua dura de Culiacán daña boilers en 5-10 años aunque sean nuevos. "
             "Mantenimiento preventivo y reparación con garantía escrita."),
            ("Revisión Post-Corte JAPAC",
             "Los cortes de la red generan golpes de ariete que dañan válvulas y uniones "
             "de PVC. Revisión completa y normalización de presión."),
            ("Fugas en Conexiones PVC",
             "Uniones y codos que fallan por variaciones de presión o instalación deficiente. "
             "Detección y reparación sin demolición mayor."),
            ("Destape de Drenajes",
             "Tuberías de 15-25 años con acumulación de grasa y raíces. "
             "Limpieza profesional con equipo de alta presión."),
            ("Tinacos y Cisternas",
             "Limpieza, revisión de flotadores y válvulas de llenado. "
             "Importante después de interrupciones prolongadas de JAPAC."),
            ("Emergencias 24/7",
             "Atención inmediata en toda {nombre}: desde {calle_principal} "
             "hasta todas las privadas. Cualquier día."),
        ],
        "cobertura": [
            "{calle_principal} y calles internas",
            "Zona {landmark}",
            "Privadas y circuitos del fraccionamiento",
        ],
    },
}

# Era por defecto si no se especifica
ERA_DEFAULT = "residencial-70-90"

# ─── Plantillas HTML ──────────────────────────────────────────────────────────

def build_main_section(colonia: dict, era_data: dict) -> str:
    nombre = colonia["nombre"]
    slug = colonia["slug"]
    calle = colonia.get("calle_principal") or "las calles principales"
    landmark = colonia.get("landmark") or "los puntos de referencia de la zona"
    cp = colonia.get("cp") or "80000"
    era_label = era_data["descripcion_era"]
    antiguedad = era_data["antiguedad"]
    nota = colonia.get("nota") or ""

    def fmt(s):
        return s.format(nombre=nombre, calle_principal=calle, landmark=landmark,
                        cp=cp, era_label=era_label, antiguedad=antiguedad)

    # Intro párrafo 1
    if nota:
        intro_p1 = (
            f'<strong>{nombre}</strong> es una colonia de Culiacán {era_label}, '
            f'con viviendas de {antiguedad} de antigüedad, '
            f'ubicada sobre {calle}. '
            f'{nota}'
        )
    else:
        intro_p1 = (
            f'<strong>{nombre}</strong> es una colonia de Culiacán {era_label}, '
            f'con viviendas de {antiguedad} de antigüedad. '
            f'Ubicada sobre {calle}, tiene como referencia '
            f'{landmark} y forma parte del tejido urbano consolidado de la ciudad.'
        )

    # Intro párrafo 2
    intro_p2 = fmt(era_data["intro_p2"])

    # Beneficios
    beneficios_html = ""
    for icon, titulo, desc in era_data["beneficios"]:
        t = fmt(titulo)
        d = fmt(desc)
        beneficios_html += (
            f'  <div class="benefit"><div class="benefit-icon">{icon}</div>'
            f'<h3>{t}</h3><p>{d}</p></div>\n'
        )

    # Servicios
    servicios_html = ""
    for titulo, desc in era_data["servicios"]:
        t = fmt(titulo)
        d = fmt(desc)
        servicios_html += (
            f'  <div class="card"><h3>{t}</h3><p>{d}</p></div>\n'
        )

    # Cobertura
    cobertura_items = ""
    for item in era_data["cobertura"]:
        cobertura_items += f'<p>✓ {fmt(item)}</p>'

    # Testimonios (genéricos pero con calle real)
    test1 = (
        f'"Llevaba meses con baja presión en la regadera. Vinieron, revisaron '
        f'y me explicaron que la tubería tenía {antiguedad} de uso. La cambiaron '
        f'ese mismo día. Ahora el agua sale perfecta. Los recomiendo en {nombre}."'
    )
    test2 = (
        f'"El calentador no calentaba bien y resultó ser sarro por dentro. '
        f'Lo limpiaron y quedó como nuevo. Precio justo y garantía por escrito. '
        f'Son los mejores que he contratado en la zona."'
    )

    wa_nombre = nombre.replace(" ", "%20")

    return f"""<main>
<section class="section section-alt"><div class="container">
<p class="colonia-intro-unico">
{intro_p1}
</p>
<p style="margin-top:1rem;color:#475569;">
{intro_p2}
</p>
<h2 style="margin-top:2rem;">¿Por qué elegirnos en {nombre}?</h2>
<div class="benefits-grid">
{beneficios_html}</div>
</div></section>
<section class="section"><div class="container"><h2>Servicios más solicitados en {nombre}</h2><div class="grid">
{servicios_html}</div></div></section>
<section class="section section-alt"><div class="container"><h2>Cobertura en {nombre}</h2><div class="pricing-box"><h3>Atendemos toda {nombre}</h3>{cobertura_items}<p>✓ Llegamos en 25-35 minutos</p><p>✓ Cotización gratis · Lunes a domingo 24/7</p><p>✓ Garantía 6 meses por escrito</p></div></div></section>
<section class="section"><div class="container"><h2>Testimonios de vecinos de {nombre}</h2><div class="testimonials">
<div class="testimonial">
  <p>{test1}</p>
  <span>— Vecino de {calle}, {nombre}</span>
</div>
<div class="testimonial">
  <p>{test2}</p>
  <span>— Cliente en {nombre}, Culiacán</span>
</div>
</div></div></section>
<section id="contacto" class="section section-alt"><div class="container"><div class="final-cta"><h2>¿Necesitas Plomero?</h2><p>WhatsApp: <strong>667 392 2273</strong></p><div class="cta-buttons"><a href="https://wa.me/526673922273?text=Hola,%20necesito%20plomero%20en%20{wa_nombre}" class="btn-primary" target="_blank">WhatsApp</a><a href="tel:6673922273" class="btn-secondary">Llamar</a></div></div></div></section>
</main>"""


def build_meta_description(colonia: dict, era_data: dict) -> str:
    nombre = colonia["nombre"]
    calle = colonia.get("calle_principal") or "zona residencial"
    antiguedad = era_data["antiguedad"]
    problema = era_data["problema_central"][:60]
    return (
        f'Plomero en {nombre}, Culiacán · Casas de {antiguedad} · '
        f'{problema} · Llegada 25-35 min · 667 392 2273'
    )


def update_postal_code(html: str, cp: str) -> str:
    return re.sub(
        r'("postalCode":\s*)"[0-9]+"',
        f'"postalCode": "{cp}"',
        html
    )


def process_colonia(colonia: dict, dry_run: bool = False) -> bool:
    slug = colonia["slug"]
    era_key = colonia.get("era_key") or ERA_DEFAULT
    era_data = ERAS.get(era_key, ERAS[ERA_DEFAULT])

    html_path = COLONIAS_DIR / slug / "index.html"
    if not html_path.exists():
        print(f"  ⚠️  No existe: {html_path}")
        return False

    html = html_path.read_text(encoding="utf-8")

    # 1. Actualizar meta description
    meta_nueva = build_meta_description(colonia, era_data)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{meta_nueva}"',
        html
    )

    # 2. Actualizar postal code en schema
    cp = colonia.get("cp") or "80000"
    html = update_postal_code(html, cp)

    # 3. Reemplazar <main>...</main>
    main_nuevo = build_main_section(colonia, era_data)
    html = re.sub(r'<main>.*?</main>', main_nuevo, html, flags=re.DOTALL)

    if dry_run:
        print(f"  [DRY-RUN] {slug}: meta y main generados correctamente")
        return True

    html_path.write_text(html, encoding="utf-8")
    nombre = colonia["nombre"]
    print(f"  ✅ {slug} ({nombre}) — CP {cp} — era: {era_key}")
    return True


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generador de páginas de colonias")
    parser.add_argument("--slug", help="Procesar solo esta colonia (por slug)")
    parser.add_argument("--dry-run", action="store_true", help="No escribe archivos")
    parser.add_argument("--data", default=str(DATA_FILE), help="Ruta al JSON de datos")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"❌ No se encontró el archivo de datos: {data_path}")
        print("   Crea colonias-data.json primero.")
        return

    with open(data_path, encoding="utf-8") as f:
        colonias = json.load(f)

    if args.slug:
        colonias = [c for c in colonias if c["slug"] == args.slug]
        if not colonias:
            print(f"❌ No se encontró slug '{args.slug}' en el JSON")
            return

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Procesando {len(colonias)} colonias...\n")
    ok = 0
    for colonia in colonias:
        if process_colonia(colonia, dry_run=args.dry_run):
            ok += 1

    print(f"\n{'─'*50}")
    print(f"✅ {ok}/{len(colonias)} colonias procesadas correctamente")
    if not args.dry_run and ok > 0:
        print("\nPróximo paso:")
        print("  cd 'plomero culiacan pro'")
        print("  git add servicios/plomero-colonias-culiacan/")
        print("  git commit -m 'SEO: contenido generado en batch'")
        print("  git push origin main")


if __name__ == "__main__":
    main()
