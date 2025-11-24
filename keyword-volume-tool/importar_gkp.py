#!/usr/bin/env python3
"""
Script para importar datos de Google Keyword Planner a la herramienta
Lee el CSV descargado y lo importa automáticamente
"""

import csv
import requests
import re
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Ruta al CSV descargado de Google Keyword Planner
CSV_FILE = "/Users/hectorpc/Downloads/Keyword Stats 2025-11-23 at 20_27_04.csv"

# URL de la API local
API_URL = "http://localhost:8000/api/import-gkp"

# ============================================================================
# FUNCIONES
# ============================================================================

def limpiar_numero(texto):
    """Convertir texto de volumen a número"""
    if not texto or texto.strip() in ['', '--', '—']:
        return None

    # Remover espacios y caracteres especiales
    texto = texto.strip().replace(',', '').replace('.', '')

    # Detectar rangos (ej: "100-1K" o "1K-10K")
    if '-' in texto:
        partes = texto.split('-')
        if len(partes) == 2:
            try:
                min_val = convertir_volumen(partes[0].strip())
                max_val = convertir_volumen(partes[1].strip())
                return (min_val, max_val)
            except:
                return None

    # Si es un número directo
    try:
        return int(texto)
    except:
        return None

def convertir_volumen(texto):
    """Convertir notación K/M a número"""
    texto = texto.strip().upper()

    # Remover espacios
    texto = texto.replace(' ', '')

    # Convertir K (miles) y M (millones)
    if 'K' in texto:
        numero = float(texto.replace('K', ''))
        return int(numero * 1000)
    elif 'M' in texto:
        numero = float(texto.replace('M', ''))
        return int(numero * 1000000)
    else:
        return int(texto)

def parsear_csv_gkp(archivo):
    """
    Parsear CSV de Google Keyword Planner
    Maneja el formato UTF-16 con espacios entre caracteres
    """
    keywords_data = []

    with open(archivo, 'r', encoding='utf-16') as f:
        contenido = f.read()

        # Dividir en líneas
        lineas = contenido.strip().split('\n')

        # Encontrar la línea de headers (contiene "Keyword")
        header_idx = -1
        for i, linea in enumerate(lineas):
            if 'K e y w o r d' in linea or 'Keyword' in linea:
                header_idx = i
                break

        if header_idx == -1:
            print("❌ No se encontraron headers en el CSV")
            return []

        # Procesar líneas de datos (después del header)
        for i in range(header_idx + 1, len(lineas)):
            linea = lineas[i]

            # Dividir por tabuladores
            campos = linea.split('\t')

            if len(campos) < 3:
                continue

            # Extraer datos
            keyword = campos[0].strip()
            volumen_texto = campos[2].strip()  # "Avg. monthly searches"

            # Saltar si keyword está vacío ANTES de limpiar
            if not keyword or keyword == '':
                continue

            # Limpiar espacios entre caracteres (UTF-16 issue)
            # Solo remover espacios dobles, no todos los espacios
            while '  ' in keyword:
                keyword = keyword.replace('  ', ' ')
            keyword = keyword.strip()

            # Saltar si después de limpiar está vacío
            if not keyword or keyword == '':
                continue

            # Procesar volumen
            volumen = limpiar_numero(volumen_texto)

            if volumen is None:
                continue

            # Si es un rango (tuple)
            if isinstance(volumen, tuple):
                volume_min, volume_max = volumen
            else:
                # Si es un número exacto, crear rango ±20%
                volume_min = int(volumen * 0.8)
                volume_max = int(volumen * 1.2)

            # Agregar a lista
            keywords_data.append({
                'keyword': keyword,
                'volume_min': volume_min,
                'volume_max': volume_max,
                'cpc': 0  # GKP no siempre da CPC en modo free
            })

    return keywords_data

def importar_a_api(keywords_data):
    """Importar keywords a la API"""
    try:
        response = requests.post(
            API_URL,
            json={'keywords_data': keywords_data},
            timeout=30
        )

        if response.status_code == 200:
            resultado = response.json()
            return resultado
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error conectando a API: {e}")
        print(f"\n💡 Asegúrate de que el backend esté corriendo:")
        print(f"   cd keyword-volume-tool/backend")
        print(f"   source venv/bin/activate")
        print(f"   python main.py")
        return None

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print(f"\n📥 IMPORTAR DATOS DE GOOGLE KEYWORD PLANNER")
    print(f"{'='*70}\n")

    # 1. Leer y parsear CSV
    print(f"📄 Leyendo CSV: {CSV_FILE}")
    keywords_data = parsear_csv_gkp(CSV_FILE)

    if not keywords_data:
        print(f"\n❌ No se encontraron keywords válidas en el CSV")
        exit(1)

    print(f"✅ {len(keywords_data)} keywords encontradas\n")

    # Mostrar preview
    print(f"📊 Preview de keywords a importar:")
    print(f"{'-'*70}")
    for i, kw in enumerate(keywords_data[:10], 1):
        print(f"{i:2}. {kw['keyword']:40} → {kw['volume_min']:,} - {kw['volume_max']:,} búsquedas/mes")

    if len(keywords_data) > 10:
        print(f"    ... y {len(keywords_data) - 10} más")

    print(f"{'-'*70}\n")

    # 2. Importar automáticamente (sin confirmación para scripts)
    # respuesta = input(f"¿Importar estas {len(keywords_data)} keywords? (s/n): ")
    # if respuesta.lower() != 's':
    #     print(f"\n❌ Importación cancelada")
    #     exit(0)

    # 3. Importar a API
    print(f"\n📤 Importando a la base de datos...")
    resultado = importar_a_api(keywords_data)

    if resultado:
        print(f"\n✅ IMPORTACIÓN EXITOSA")
        print(f"{'-'*70}")
        print(f"   Importadas: {resultado.get('imported', 0)}")
        print(f"   Actualizadas: {resultado.get('updated', 0)}")
        print(f"   Total en DB: {resultado.get('total', 0)}")
        print(f"{'-'*70}\n")

        print(f"💡 Ahora cuando analices estas keywords, usarán datos de GKP")
        print(f"   Precisión esperada: ±5-10% (vs ±20-30% con ML)\n")

        print(f"🔍 Prueba en: http://localhost:3000")
        print(f"   Busca: 'plomero' y verás datos de GKP\n")
    else:
        print(f"\n❌ Error en la importación")
        exit(1)
