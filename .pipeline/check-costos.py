#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tripwire de COSTO/CUOTA. Lee .pipeline/costos.jsonl; si la ÚLTIMA corrida superó el
presupuesto de tokens/USD, emite un hallazgo (media) para que el dueño VEA el costo en el
reporte diario en vez de descubrirlo en la factura. Solo VISIBILIDAD: no corta nada.
(Corrida grande del 2026-06-18: 35.5M tok / ~$91 api-ref vs 11.8M normal.)
Emite el JSON común {"hallazgos":[...]}. Sin argumentos.
"""
import os, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTOS = os.path.join(ROOT, ".pipeline", "costos.jsonl")
UMBRAL_TOKENS = 28_000_000   # ~2x una corrida diaria normal (11.8M)
UMBRAL_USD    = 70           # usd_equiv_api_ref

def main():
    hallazgos, filas = [], []
    if os.path.isfile(COSTOS):
        for ln in open(COSTOS, encoding="utf-8", errors="replace"):
            ln = ln.strip()
            if ln:
                try: filas.append(json.loads(ln))
                except Exception: pass
    if filas:
        u   = filas[-1]
        tok = u.get("total_tokens", 0)
        usd = u.get("usd_equiv_api_ref", 0)
        if tok > UMBRAL_TOKENS or usd > UMBRAL_USD:
            hallazgos.append({
                "id": "costo-001", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "La última corrida (%s) consumió %.1fM tokens (~$%.0f api-ref), sobre presupuesto (%.0fM / $%.0f)." % (
                    u.get("etiqueta", "?"), tok/1e6, usd, UMBRAL_TOKENS/1e6, UMBRAL_USD),
                "fix_sugerido": "Auditar la corrida: ¿demasiados revisores en paralelo, lote grande, o un loop sin freno? Bajar fan-out o usar modelo más barato en revisores deterministas.",
            })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
