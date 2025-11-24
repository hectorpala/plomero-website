#!/usr/bin/env python3
"""
Extraer HTML completo de una página para análisis en Gemini
"""

from pathlib import Path
import sys

def extraer_html_para_gemini(colonia_name):
    """
    Extrae el HTML completo de una página de colonia
    """
    base_dir = Path('servicios/plomero-colonias-culiacan')
    colonia_dir = base_dir / colonia_name
    index_file = colonia_dir / 'index.html'

    if not index_file.exists():
        print(f"❌ ERROR: No se encontró la página para '{colonia_name}'")
        print(f"   Ruta esperada: {index_file}")
        return None

    with open(index_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Guardar en archivo temporal para copiar fácilmente
    output_file = Path('HTML_PARA_GEMINI.txt')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"CÓDIGO HTML DE: {colonia_name}\n")
        f.write(f"Página: https://plomeroculiacanpro.mx/servicios/plomero-colonias-culiacan/{colonia_name}/\n")
        f.write("=" * 80 + "\n\n")
        f.write(html_content)

    # Estadísticas
    num_lines = len(html_content.split('\n'))
    num_chars = len(html_content)
    num_words = len(html_content.split())

    print(f"\n✅ HTML EXTRAÍDO EXITOSAMENTE")
    print(f"{'='*70}")
    print(f"Página: {colonia_name}")
    print(f"Líneas: {num_lines:,}")
    print(f"Caracteres: {num_chars:,}")
    print(f"Palabras: {num_words:,}")
    print(f"\n📄 Guardado en: {output_file}")
    print(f"{'='*70}\n")

    print("📋 PASOS SIGUIENTES:\n")
    print("1. Abre el archivo HTML_PARA_GEMINI.txt")
    print("2. Copia TODO el contenido (CMD+A, CMD+C)")
    print("3. Ve a https://gemini.google.com")
    print("4. Pega el prompt de PROMPT_GEMINI_SEO_AUDIT.md")
    print("5. Reemplaza [PEGAR AQUÍ EL CÓDIGO HTML] con el HTML copiado")
    print("6. Envía y espera el análisis completo\n")

    return output_file

def listar_colonias_disponibles():
    """
    Muestra lista de colonias disponibles
    """
    base_dir = Path('servicios/plomero-colonias-culiacan')

    if not base_dir.exists():
        print(f"❌ ERROR: No se encontró el directorio {base_dir}")
        return

    colonias = []
    for colonia_dir in sorted(base_dir.iterdir()):
        if colonia_dir.is_dir() and colonia_dir.name != '__pycache__':
            index_file = colonia_dir / 'index.html'
            if index_file.exists():
                colonias.append(colonia_dir.name)

    print(f"\n📂 COLONIAS DISPONIBLES ({len(colonias)} total):\n")

    # Mostrar en columnas
    for i, colonia in enumerate(colonias, 1):
        print(f"  {i:3d}. {colonia}")
        if i % 30 == 0:
            print()  # Espacio cada 30

    print(f"\n💡 USO: python3 extraer_html_para_gemini.py [nombre-colonia]")
    print(f"   Ejemplo: python3 extraer_html_para_gemini.py las-quintas\n")

if __name__ == "__main__":
    print(f"\n🔍 EXTRACTOR DE HTML PARA GEMINI SEO AUDIT")
    print(f"{'='*70}\n")

    if len(sys.argv) < 2:
        print("ℹ️  No se especificó colonia. Mostrando lista...\n")
        listar_colonias_disponibles()
    else:
        colonia_name = sys.argv[1]
        extraer_html_para_gemini(colonia_name)
