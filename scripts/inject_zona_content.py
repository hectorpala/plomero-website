#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_zona_content.py
Inyecta contenido único por zona geográfica en las páginas de colonias
de Plomero Culiacán Pro.

Uso:
  python3 inject_zona_content.py --test          # Solo las-quintas y bachigualato
  python3 inject_zona_content.py --all           # Las 643 colonias
  python3 inject_zona_content.py --slug bachigualato las-quintas  # Colonias específicas
"""

import json
import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path("/Users/hectorpc/Documents/Hector Palazuelos/Google My Business/plomero culiacan pro")
COLONIAS_DIR = BASE_DIR / "servicios" / "plomero-colonias-culiacan"
JSON_PATH = BASE_DIR / "colonias-completas-culiacan.json"
BACKUP_DIR = BASE_DIR / "scripts" / "backups_inject_zona"

# ── Perfiles de zona ───────────────────────────────────────────────────────────
ZONA_PERFILES = {
    "NORTE": {
        "problema_comun": "tuberías de PVC de 15-20 años con presión irregular",
        "problema_comun_corto": "presión irregular en tuberías",
        "servicio_mas_solicitado": "detección y reparación de fugas ocultas",
        "tiempo_llegada": "20-35 min",
    },
    "PONIENTE": {
        "problema_comun": "fraccionamientos con instalaciones bajo garantía vencida",
        "problema_comun_corto": "fugas en muros por garantía vencida",
        "servicio_mas_solicitado": "instalación de boiler y reparación de fugas en muros",
        "tiempo_llegada": "25-40 min",
    },
    "CENTRO": {
        "problema_comun": "tuberías galvanizadas de 30-50 años con sarro acumulado",
        "problema_comun_corto": "sarro y obstrucciones en tubería galvanizada",
        "servicio_mas_solicitado": "cambio de tubería y destape de drenaje",
        "tiempo_llegada": "15-25 min",
    },
    "ORIENTE": {
        "problema_comun": "drenajes colapsados por raíces de árboles",
        "problema_comun_corto": "drenaje colapsado por raíces",
        "servicio_mas_solicitado": "desazolve y destape de drenajes",
        "tiempo_llegada": "20-30 min",
    },
    "SUR": {
        "problema_comun": "baja presión de agua y tinacos con sedimento",
        "problema_comun_corto": "baja presión y sedimento en tinaco",
        "servicio_mas_solicitado": "instalación y limpieza de tinacos y rebombeo",
        "tiempo_llegada": "30-45 min",
    },
}

# Centroide de fallback
CENTROIDE = {"lat": 24.7903, "lng": -107.3878}


# ── Clasificación de zona ──────────────────────────────────────────────────────
def clasificar_zona(gps):
    """Devuelve el nombre de zona según las coordenadas GPS."""
    if gps is None:
        lat = CENTROIDE["lat"]
        lng = CENTROIDE["lng"]
    else:
        lat = gps.get("lat", CENTROIDE["lat"])
        lng = gps.get("lng", CENTROIDE["lng"])

    # Reglas en orden de prioridad.
    #
    # NORTE prioritario: lat >= 24.825 (aeropuerto, Humaya estricto) fuera del
    # poniente profundo. Captura Bachigualato (24.845) e Infonavit Humaya (24.83)
    # sin arrastrar Las Quintas (24.8207 < 24.825).
    if lat >= 24.825 and lng > -107.46:
        return "NORTE"
    # PONIENTE: longitud muy al oeste (<= -107.42), incluye Las Quintas, Tres Ríos,
    # country clubs, fraccionamientos nuevos.
    if lng <= -107.42:
        return "PONIENTE"
    # NORTE residual: lat >= 24.82 y no poniente (ya cubierto arriba).
    if lat >= 24.82:
        return "NORTE"
    # CENTRO histórico.
    if 24.79 <= lat <= 24.82 and -107.41 <= lng <= -107.37:
        return "CENTRO"
    # ORIENTE: longitud poco profunda (>= -107.37).
    if lng >= -107.37:
        return "ORIENTE"
    # SUR: fraccionamientos nuevos al sur.
    if lat <= 24.79:
        return "SUR"

    # Fallback centroide
    return "CENTRO"


# ── Carga de datos JSON ────────────────────────────────────────────────────────
def cargar_colonias_json():
    """Carga el JSON y devuelve dict indexado por slug."""
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    colonias = data.get("colonias_culiacan", [])
    return {c["slug"]: c for c in colonias}


# ── Generación de HTML único ───────────────────────────────────────────────────
def generar_parrafo_intro(nombre, calle, zona):
    """Devuelve el <p class='colonia-intro-unico'> con datos únicos."""
    p = ZONA_PERFILES[zona]
    return (
        f'<p class="colonia-intro-unico">\n'
        f'En <strong>{nombre}</strong>, sobre {calle}, atendemos emergencias de plomería '
        f'con llegada en {p["tiempo_llegada"]}. La zona presenta frecuentemente {p["problema_comun"]}. '
        f'Nuestro equipo conoce las instalaciones típicas de {nombre} y llega equipado '
        f'para resolver sin segunda visita.\n'
        f'</p>'
    )


def generar_testimonios(nombre, calle, zona):
    """Devuelve el bloque HTML de 2 testimonios únicos."""
    p = ZONA_PERFILES[zona]
    return (
        f'<div class="testimonio-unico">\n'
        f'  <p>"Llamé por {p["problema_comun_corto"]} y llegaron en menos de {p["tiempo_llegada"]}. '
        f'Trabajo limpio y garantía. Los recomiendo en {nombre}."</p>\n'
        f'  <span>— Vecino de {calle}, {nombre}</span>\n'
        f'</div>\n'
        f'<div class="testimonio-unico">\n'
        f'  <p>"El mejor servicio de plomería que he contratado en {nombre}. '
        f'Resolvieron el {p["servicio_mas_solicitado"]} el mismo día."</p>\n'
        f'  <span>— Cliente frecuente en {nombre}, Culiacán</span>\n'
        f'</div>'
    )


# ── Balanceador de divs ────────────────────────────────────────────────────────
def encontrar_cierre_div(html, start_pos):
    """
    Dado el índice donde comienza un <div ...>, devuelve el índice
    del carácter inmediatamente después del </div> correspondiente
    (balanceando la profundidad de apertura/cierre).

    Devuelve -1 si no se encuentra cierre balanceado.
    """
    depth = 0
    pos = start_pos
    # Regex para detectar apertura o cierre de div
    tag_re = re.compile(r'<(/?div)\b', re.IGNORECASE)

    for m in tag_re.finditer(html, pos):
        tag = m.group(1).lower()
        if tag == "div":
            depth += 1
        else:  # /div
            depth -= 1
            if depth == 0:
                # Encontrar el '>' que cierra este </div>
                end = html.index('>', m.start()) + 1
                return end
    return -1


# ── Modificación del HTML ──────────────────────────────────────────────────────
def modificar_html(html, nombre, calle, zona):
    """
    Aplica las dos modificaciones al HTML:
    1. Inserta <p class='colonia-intro-unico'> antes del primer <h2> dentro de <main>.
    2. Reemplaza los 2 testimonios genéricos por los únicos.

    Devuelve (html_modificado, reporte_dict).
    """
    reporte = {
        "intro_insertado": False,
        "testimonios_reemplazados": False,
        "advertencias": [],
    }

    # ── 1. Párrafo intro ──────────────────────────────────────────────────────
    # Buscar el primer <h2> dentro de <main>
    main_match = re.search(r'<main\b[^>]*>', html, re.IGNORECASE)
    if not main_match:
        reporte["advertencias"].append("No se encontró etiqueta <main>. No se insertó párrafo intro.")
    else:
        main_start = main_match.end()
        h2_match = re.search(r'<h2\b[^>]*>', html[main_start:], re.IGNORECASE)
        if not h2_match:
            reporte["advertencias"].append("No se encontró <h2> dentro de <main>. No se insertó párrafo intro.")
        else:
            # Solo insertar si NO existe ya un párrafo intro (idempotencia)
            if 'class="colonia-intro-unico"' in html:
                reporte["advertencias"].append("Ya existe colonia-intro-unico. No se vuelve a insertar.")
            else:
                parrafo = generar_parrafo_intro(nombre, calle, zona)
                insert_pos = main_start + h2_match.start()
                html = html[:insert_pos] + parrafo + "\n" + html[insert_pos:]
                reporte["intro_insertado"] = True

    # ── 2. Testimonios ────────────────────────────────────────────────────────
    # Verificar idempotencia primero
    if 'class="testimonio-unico"' in html:
        reporte["advertencias"].append("Ya existen testimonios únicos. No se reemplazan.")
    else:
        # Localizar <div class="testimonials">
        open_tag_match = re.search(r'<div class="testimonials">', html, re.IGNORECASE)
        if not open_tag_match:
            reporte["advertencias"].append(
                'No se encontró <div class="testimonials">. No se reemplazaron testimonios.'
            )
        else:
            start_pos = open_tag_match.start()
            end_pos = encontrar_cierre_div(html, start_pos)

            if end_pos == -1:
                reporte["advertencias"].append(
                    'No se pudo balancear el cierre de <div class="testimonials">. No se reemplazaron testimonios.'
                )
            else:
                bloque_completo = html[start_pos:end_pos]
                inner = html[open_tag_match.end():end_pos - len("</div>")]

                # Verificar que contiene los testimonios genéricos conocidos
                tiene_excelente = "Excelente servicio" in inner
                tiene_destaparon = "Destaparon el drenaje" in inner

                if tiene_excelente or tiene_destaparon:
                    nuevos_testimonios = generar_testimonios(nombre, calle, zona)
                    nuevo_bloque = (
                        '<div class="testimonials">\n'
                        + nuevos_testimonios
                        + "\n</div>"
                    )
                    html = html[:start_pos] + nuevo_bloque + html[end_pos:]
                    reporte["testimonios_reemplazados"] = True
                else:
                    reporte["advertencias"].append(
                        f"Testimonios no son los genéricos esperados. inner[:120]={inner[:120]!r}. No se reemplazaron."
                    )

    return html, reporte


# ── Procesamiento de una colonia ───────────────────────────────────────────────
def procesar_colonia(slug, colonias_json, dry_run=False, preview=False):
    """
    Procesa el index.html de una colonia.
    - dry_run=True: solo muestra el reporte sin escribir.
    - preview=True: imprime el HTML modificado relevante.
    """
    html_path = COLONIAS_DIR / slug / "index.html"

    if not html_path.exists():
        print(f"  [SKIP] {slug}: archivo no encontrado")
        return {"slug": slug, "status": "no_encontrado"}

    # Datos de la colonia (puede no estar en JSON)
    colonia_data = colonias_json.get(slug)
    if colonia_data:
        nombre = colonia_data.get("nombre", slug.replace("-", " ").title())
        gps = colonia_data.get("gps")
        calle = colonia_data.get("calle_principal", "Calle Principal")
    else:
        nombre = slug.replace("-", " ").title()
        gps = None
        calle = "Calle Principal"

    zona = clasificar_zona(gps)

    with open(html_path, "r", encoding="utf-8") as f:
        html_original = f.read()

    html_modificado, reporte = modificar_html(html_original, nombre, calle, zona)

    cambios = reporte["intro_insertado"] or reporte["testimonios_reemplazados"]

    if cambios and not dry_run:
        # Backup (solo si no existe uno previo para preservar el original)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_path = BACKUP_DIR / f"{slug}_index.html.bak"
        if not backup_path.exists():
            shutil.copy2(html_path, backup_path)

        # Escribir modificado
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_modificado)

    status = "modificado" if cambios else "sin_cambios"
    if reporte["advertencias"] and not cambios:
        status = "advertencia"

    print(
        f"  [{status.upper():12s}] {slug:45s} | Zona: {zona:8s} | "
        f"intro={reporte['intro_insertado']} | testimonios={reporte['testimonios_reemplazados']}"
    )
    for w in reporte["advertencias"]:
        print(f"    AVISO: {w}")

    if preview and cambios:
        _mostrar_preview(html_modificado, nombre)

    return {
        "slug": slug,
        "zona": zona,
        "nombre": nombre,
        "calle": calle,
        "status": status,
        **reporte,
    }


def _mostrar_preview(html, nombre):
    """Imprime los fragmentos relevantes del HTML modificado."""
    print(f"\n{'─'*70}")
    print(f"  PREVIEW: {nombre}")
    print(f"{'─'*70}")

    # Mostrar párrafo intro
    intro_match = re.search(
        r'(<p class="colonia-intro-unico">.*?</p>)',
        html, re.DOTALL
    )
    if intro_match:
        print("  [PARRAFO INTRO]")
        print(intro_match.group(1))
        print()

    # Mostrar bloque testimonios (completo)
    open_tag = re.search(r'<div class="testimonials">', html)
    if open_tag:
        end = encontrar_cierre_div(html, open_tag.start())
        if end != -1:
            print("  [SECCIÓN TESTIMONIOS]")
            print(html[open_tag.start():end])
    print(f"{'─'*70}\n")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Inyecta contenido por zona en páginas de colonias.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test", action="store_true",
                       help="Prueba en las-quintas y bachigualato (con preview)")
    group.add_argument("--all", action="store_true",
                       help="Procesa las 643 colonias")
    group.add_argument("--slug", nargs="+", metavar="SLUG",
                       help="Slugs específicos a procesar")

    parser.add_argument("--dry-run", action="store_true",
                        help="Simula sin escribir archivos")
    parser.add_argument("--preview", action="store_true",
                        help="Muestra fragmentos HTML modificados")

    args = parser.parse_args()

    print(f"\n{'='*70}")
    print("  PLOMERO CULIACÁN PRO — Inyector de Contenido por Zona")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.dry_run:
        print("  MODO DRY-RUN (no se escriben archivos)")
    print(f"{'='*70}\n")

    colonias_json = cargar_colonias_json()
    print(f"  JSON cargado: {len(colonias_json)} colonias con datos GPS\n")

    # Determinar slugs a procesar
    if args.test:
        slugs = ["las-quintas", "bachigualato"]
        preview = True
    elif args.slug:
        slugs = args.slug
        preview = args.preview
    else:  # --all
        slugs = sorted([d.name for d in COLONIAS_DIR.iterdir() if d.is_dir()])
        preview = args.preview

    print(f"  Procesando {len(slugs)} colonia(s)...\n")

    resultados = []
    for slug in slugs:
        r = procesar_colonia(
            slug,
            colonias_json,
            dry_run=args.dry_run,
            preview=preview,
        )
        resultados.append(r)

    # Resumen
    modificados = sum(1 for r in resultados if r.get("status") == "modificado")
    sin_cambios = sum(1 for r in resultados if r.get("status") == "sin_cambios")
    advertencias = sum(1 for r in resultados if r.get("status") == "advertencia")
    no_encontrados = sum(1 for r in resultados if r.get("status") == "no_encontrado")

    print(f"\n{'='*70}")
    print("  RESUMEN FINAL")
    print(f"{'─'*70}")
    print(f"  Total procesados : {len(resultados)}")
    print(f"  Modificados      : {modificados}")
    print(f"  Sin cambios      : {sin_cambios}")
    print(f"  Con advertencias : {advertencias}")
    print(f"  No encontrados   : {no_encontrados}")
    if not args.dry_run and modificados > 0:
        print(f"  Backups en       : {BACKUP_DIR}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
