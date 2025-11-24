#!/usr/bin/env python3
"""
Ejemplo: Analizar múltiples keywords en batch
Genera reporte CSV con volúmenes estimados
"""

import requests
import time
import csv
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

API_URL = "http://localhost:8000/api/keyword-volume"

# Lista de keywords a analizar
KEYWORDS = [
    "plomero culiacan",
    "plomero las quintas",
    "plomero urgencias culiacan",
    "reparacion de fugas culiacan",
    "destapado de drenaje culiacan",
    "instalacion de calentadores culiacan",
    "plomero 24 horas culiacan",
    "plomero economico culiacan",
    "plomero profesional culiacan",
    "servicio de plomeria culiacan",
]

LOCATION = "Sinaloa"

# Delay entre requests (evitar rate limits)
DELAY_SECONDS = 2

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def analizar_keywords(keywords, location):
    """Analizar lista de keywords y generar reporte"""

    print(f"\n🔍 ANÁLISIS BATCH DE KEYWORDS")
    print(f"{'='*70}\n")
    print(f"Total keywords: {len(keywords)}")
    print(f"Ubicación: {location}")
    print(f"Delay entre requests: {DELAY_SECONDS}s\n")

    resultados = []

    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keywords)}] Analizando: {keyword}...", end=" ")

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
                data = response.json()

                resultado = {
                    'keyword': keyword,
                    'volumen': data['volume_estimate'],
                    'confianza': data['confidence'],
                    'trend_score': data['trend_data']['interest_score'],
                    'peak_score': data['trend_data']['peak_score'],
                    'tendencia': data['trend_data']['trend'],
                    'autocomplete_rank': data.get('autocomplete_rank', 'N/A'),
                    'cached': data['cached']
                }

                resultados.append(resultado)

                print(f"✅ {data['volume_estimate']:,} búsquedas/mes ({data['confidence']})")

            else:
                print(f"❌ Error {response.status_code}")
                resultados.append({
                    'keyword': keyword,
                    'volumen': 0,
                    'confianza': 'Error',
                    'trend_score': 0,
                    'peak_score': 0,
                    'tendencia': 'error',
                    'autocomplete_rank': 'N/A',
                    'cached': False
                })

        except Exception as e:
            print(f"❌ Error: {e}")
            resultados.append({
                'keyword': keyword,
                'volumen': 0,
                'confianza': 'Error',
                'trend_score': 0,
                'peak_score': 0,
                'tendencia': 'error',
                'autocomplete_rank': 'N/A',
                'cached': False
            })

        # Delay para evitar rate limits
        if i < len(keywords):
            time.sleep(DELAY_SECONDS)

    return resultados

# ============================================================================
# GENERAR REPORTE CSV
# ============================================================================

def generar_csv(resultados, filename=None):
    """Generar archivo CSV con resultados"""

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"keyword_analysis_{timestamp}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'keyword',
            'volumen',
            'confianza',
            'trend_score',
            'peak_score',
            'tendencia',
            'autocomplete_rank',
            'cached'
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\n✅ Reporte guardado: {filename}")

# ============================================================================
# MOSTRAR RESUMEN
# ============================================================================

def mostrar_resumen(resultados):
    """Mostrar resumen de resultados"""

    print(f"\n{'='*70}")
    print(f"📊 RESUMEN DE ANÁLISIS")
    print(f"{'='*70}\n")

    # Ordenar por volumen
    resultados_sorted = sorted(resultados, key=lambda x: x['volumen'], reverse=True)

    print(f"🏆 TOP 5 KEYWORDS POR VOLUMEN:\n")

    for i, r in enumerate(resultados_sorted[:5], 1):
        print(f"{i}. {r['keyword']}")
        print(f"   Volumen: {r['volumen']:,} búsquedas/mes")
        print(f"   Confianza: {r['confianza']}")
        print(f"   Trend: {r['trend_score']}/100")
        print()

    # Estadísticas
    total_volumen = sum(r['volumen'] for r in resultados)
    avg_volumen = total_volumen / len(resultados) if resultados else 0

    alta_confianza = sum(1 for r in resultados if r['confianza'] == 'Alta')
    media_confianza = sum(1 for r in resultados if r['confianza'] == 'Media')
    baja_confianza = sum(1 for r in resultados if r['confianza'] == 'Baja')

    print(f"📈 ESTADÍSTICAS:")
    print(f"   Total keywords analizadas: {len(resultados)}")
    print(f"   Volumen total estimado: {total_volumen:,} búsquedas/mes")
    print(f"   Promedio por keyword: {int(avg_volumen):,} búsquedas/mes")
    print()
    print(f"   Confianza Alta: {alta_confianza} keywords")
    print(f"   Confianza Media: {media_confianza} keywords")
    print(f"   Confianza Baja: {baja_confianza} keywords")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        # 1. Analizar keywords
        resultados = analizar_keywords(KEYWORDS, LOCATION)

        # 2. Generar CSV
        generar_csv(resultados)

        # 3. Mostrar resumen
        mostrar_resumen(resultados)

        print(f"\n✨ Análisis completado\n")

    except KeyboardInterrupt:
        print(f"\n\n⚠️  Análisis interrumpido por usuario\n")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}\n")
