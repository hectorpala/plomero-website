#!/usr/bin/env python3
"""
Script Simple de Optimización Masiva
Optimiza todas las páginas HTML inyectando componentes optimizados
"""

import os
import re
import glob
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).parent.parent.parent
PARTIALS_DIR = BASE_DIR / 'templates' / 'partials'
BASE_URL = 'https://plomeroculiacanpro.mx'

# Colores para output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def log(message, color=Colors.CYAN):
    print(f"{color}{message}{Colors.END}")

def load_partial(filename):
    """Carga un archivo partial"""
    filepath = PARTIALS_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_meta_data(html):
    """Extrae título y descripción del HTML"""
    title_match = re.search(r'<title>(.*?)</title>', html)
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)

    title = title_match.group(1) if title_match else 'Plomero en Culiacán 24/7'
    description = desc_match.group(1) if desc_match else 'Servicio de plomería profesional'

    return title, description

def get_page_url(filepath):
    """Genera la URL de la página"""
    rel_path = os.path.relpath(filepath, BASE_DIR)
    url_path = rel_path.replace('index.html', '').replace('.html', '').replace('\\', '/')
    return f"{BASE_URL}/{url_path}"

def optimize_page(html, filepath):
    """Aplica todas las optimizaciones a una página"""
    url = get_page_url(filepath)
    title, description = extract_meta_data(html)

    # 1. Verificar si ya tiene security headers
    if 'X-Content-Type-Options' in html:
        return html  # Ya optimizado

    # 2. Cargar head optimizado
    head_template = load_partial('head-optimized.html')
    if not head_template:
        return html

    # 3. Reemplazar variables
    head_content = head_template
    head_content = head_content.replace('{{URL}}', url)
    head_content = head_content.replace('{{TITLE}}', title)
    head_content = head_content.replace('{{DESCRIPTION}}', description)

    # 4. Inyectar después de meta description
    desc_pattern = r'(<meta\s+name="description"[^>]*>)'
    if re.search(desc_pattern, html):
        optimized = re.sub(
            desc_pattern,
            r'\1\n\n' + head_content,
            html,
            count=1
        )
    else:
        # Inyectar antes de </head>
        optimized = html.replace('</head>', f'\n{head_content}\n</head>')

    return optimized

def process_files(pattern='**/*.html', dry_run=True):
    """Procesa todos los archivos HTML"""
    log(f"🚀 Iniciando optimización masiva...")
    if dry_run:
        log(f"🔍 Modo DRY-RUN (no se guardarán cambios)", Colors.YELLOW)

    # Buscar archivos
    exclude_patterns = ['node_modules', 'templates', '.git', 'gracias']
    files = []

    for filepath in BASE_DIR.glob(pattern):
        if filepath.is_file():
            # Verificar que no esté en carpetas excluidas
            if not any(excl in str(filepath) for excl in exclude_patterns):
                files.append(filepath)

    log(f"\n📄 Encontradas {len(files)} páginas HTML\n")

    processed = 0
    optimized_count = 0
    errors = 0

    for i, filepath in enumerate(files, 1):
        try:
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"[{i}/{len(files)}] {rel_path}... ", end='')

            with open(filepath, 'r', encoding='utf-8') as f:
                original_html = f.read()

            optimized_html = optimize_page(original_html, filepath)

            if original_html != optimized_html:
                if not dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(optimized_html)
                log("✅ OPTIMIZADO", Colors.GREEN)
                optimized_count += 1
            else:
                log("⏭️  Sin cambios")

            processed += 1

        except Exception as e:
            log(f"❌ ERROR: {str(e)}", Colors.RED)
            errors += 1

    # Resumen
    log("\n" + "="*60)
    log("📊 RESUMEN DE OPTIMIZACIÓN")
    log("="*60)
    log(f"Total procesadas: {processed}")
    log(f"Optimizadas: {optimized_count}", Colors.GREEN)
    log(f"Sin cambios: {processed - optimized_count}")
    log(f"Errores: {errors}", Colors.RED if errors > 0 else Colors.GREEN)
    log("="*60 + "\n")

    if dry_run:
        log("⚠️  Modo DRY-RUN: Los cambios NO se guardaron", Colors.YELLOW)
        log("💡 Ejecuta con --apply para aplicar cambios")
    else:
        log("✅ Optimización completada!", Colors.GREEN)
        log("📝 Recuerda hacer git commit y push")

if __name__ == '__main__':
    import sys
    dry_run = '--apply' not in sys.argv
    process_files(dry_run=dry_run)
