#!/usr/bin/env python3
"""
Ejemplo Avanzado: Exportar resultados a Google Sheets
Requiere: pip install gspread oauth2client
"""

import requests
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

API_URL = "http://localhost:8000/api/keyword-volume"

# Keywords a analizar
KEYWORDS = [
    "plomero culiacan",
    "plomero las quintas",
    "plomero urgencias culiacan",
    "reparacion de fugas culiacan",
    "destapado de drenaje culiacan",
]

LOCATION = "Sinaloa"

# Google Sheets configuración
# NOTA: Necesitas crear un Service Account en Google Cloud Console
# y descargar el JSON de credenciales
CREDENTIALS_FILE = "google-credentials.json"
SPREADSHEET_NAME = "Keyword Research - Plomero Culiacan"

# ============================================================================
# FUNCIONES
# ============================================================================

def analizar_keyword(keyword, location):
    """Analizar una keyword y retornar resultados"""
    try:
        response = requests.post(
            API_URL,
            json={
                "keyword": keyword,
                "location": location
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def conectar_google_sheets():
    """Conectar a Google Sheets"""
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            scope
        )

        client = gspread.authorize(creds)

        # Abrir o crear spreadsheet
        try:
            spreadsheet = client.open(SPREADSHEET_NAME)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(SPREADSHEET_NAME)

        return spreadsheet

    except Exception as e:
        print(f"❌ Error conectando a Google Sheets: {e}")
        print(f"\n💡 Pasos para configurar Google Sheets:")
        print(f"   1. Ir a: https://console.cloud.google.com/")
        print(f"   2. Crear Service Account")
        print(f"   3. Descargar JSON de credenciales")
        print(f"   4. Guardar como: {CREDENTIALS_FILE}")
        print(f"   5. Habilitar Google Sheets API")
        return None

def crear_worksheet(spreadsheet, nombre):
    """Crear o limpiar worksheet"""
    try:
        worksheet = spreadsheet.worksheet(nombre)
        worksheet.clear()
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=nombre,
            rows=100,
            cols=10
        )

    return worksheet

def exportar_a_sheets(spreadsheet, resultados):
    """Exportar resultados a Google Sheets"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet_name = f"Análisis {datetime.now().strftime('%Y-%m-%d')}"

    worksheet = crear_worksheet(spreadsheet, worksheet_name)

    # Headers
    headers = [
        'Keyword',
        'Volumen (búsquedas/mes)',
        'Confianza',
        'Google Trends Score',
        'Peak Score',
        'Tendencia',
        'Autocomplete Rank',
        'Keywords Relacionadas'
    ]

    # Escribir headers (con formato)
    worksheet.update('A1:H1', [headers])
    worksheet.format('A1:H1', {
        'textFormat': {'bold': True},
        'backgroundColor': {'red': 0.4, 'green': 0.5, 'blue': 0.9}
    })

    # Escribir datos
    row = 2
    for resultado in resultados:
        data = resultado['data']

        # Keywords relacionadas (join)
        related = ', '.join(data['trend_data'].get('related_queries', [])[:3])

        worksheet.update(f'A{row}:H{row}', [[
            data['keyword'],
            data['volume_estimate'],
            data['confidence'],
            data['trend_data']['interest_score'],
            data['trend_data']['peak_score'],
            data['trend_data']['trend'],
            data.get('autocomplete_rank', 'N/A'),
            related
        ]])

        # Formato condicional para confianza
        confidence_color = {
            'Alta': {'red': 0.8, 'green': 1.0, 'blue': 0.8},
            'Media': {'red': 1.0, 'green': 1.0, 'blue': 0.8},
            'Baja': {'red': 1.0, 'green': 0.9, 'blue': 0.9}
        }

        worksheet.format(f'C{row}', {
            'backgroundColor': confidence_color.get(
                data['confidence'],
                {'red': 1.0, 'green': 1.0, 'blue': 1.0}
            )
        })

        row += 1

    # Agregar timestamp
    worksheet.update(f'A{row + 2}', f'Generado: {timestamp}')

    # Auto-resize columnas
    worksheet.columns_auto_resize(0, 7)

    print(f"\n✅ Datos exportados a Google Sheets")
    print(f"   Spreadsheet: {SPREADSHEET_NAME}")
    print(f"   Worksheet: {worksheet_name}")
    print(f"   URL: {spreadsheet.url}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print(f"\n📊 KEYWORD ANALYSIS → GOOGLE SHEETS")
    print(f"{'='*70}\n")

    # 1. Conectar a Google Sheets
    print(f"🔗 Conectando a Google Sheets...")
    spreadsheet = conectar_google_sheets()

    if not spreadsheet:
        print(f"\n❌ No se pudo conectar a Google Sheets")
        print(f"\n💡 Alternativa: Usar CSV export")
        print(f"   python analizar_batch.py")
        exit(1)

    print(f"   ✅ Conectado exitosamente\n")

    # 2. Analizar keywords
    print(f"🔍 Analizando {len(KEYWORDS)} keywords...\n")

    resultados = []

    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"[{i}/{len(KEYWORDS)}] {keyword}...", end=" ")

        data = analizar_keyword(keyword, LOCATION)

        if data:
            resultados.append({
                'keyword': keyword,
                'data': data
            })
            print(f"✅ {data['volume_estimate']:,} búsquedas/mes")
        else:
            print(f"❌ Error")

        # Delay para evitar rate limits
        if i < len(KEYWORDS):
            time.sleep(2)

    # 3. Exportar a Google Sheets
    print(f"\n📤 Exportando a Google Sheets...")
    exportar_a_sheets(spreadsheet, resultados)

    print(f"\n✨ Proceso completado\n")
