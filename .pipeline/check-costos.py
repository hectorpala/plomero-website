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
    # ── Detector de CORRIDA DESBOCADA: output_tokens y nº de mensajes vs mediana móvil.
    #    total_tokens lo domina cache_read (∝ contexto, barato); el costo de un loop sin
    #    freno se ve en output_tokens y en mensajes. Marca ALTA si la última corrida supera
    #    FACTOR× la mediana de las previas. (3 corridas a 606–654M / $1300+ tenían
    #    output 2.1–2.3M y 1415–1659 mensajes vs mediana 26.6M.)
    FACTOR = 5
    MIN_HIST = 4            # no juzgar sin historia suficiente
    def _mediana(xs):
        s = sorted(xs); n = len(s)
        if not n: return 0
        return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2
    if len(filas) > MIN_HIST:
        u = filas[-1]; prev = filas[:-1]
        for campo, etiqueta in (("output_tokens", "output"), ("mensajes", "mensajes")):
            cur = u.get(campo, 0) or 0
            med = _mediana([f.get(campo, 0) or 0 for f in prev])
            if med > 0 and cur > FACTOR * med:
                hallazgos.append({
                    "id": "costo-runaway-%s" % etiqueta, "archivo": ".pipeline/costos.jsonl", "linea": 0,
                    "severidad": "alta", "categoria": "costo",
                    "descripcion": "CORRIDA DESBOCADA: la última (%s) generó %s=%s, ~%.0f× la mediana (%s). Firma de loop sin freno, no de día grande." % (
                        u.get("etiqueta", "?"), etiqueta, f"{cur:,}", cur/med, f"{int(med):,}"),
                    "fix_sugerido": "Auditar la corrida: ¿loop-until-dry sin tope, fan-out de revisores sin lote, o re-trabajo en bucle? Poner freno por nº de páginas/iteraciones en el driver (crecer-diario) y/o bajar el fan-out paralelo.",
                })
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
    # ── Fila de 0 tokens: NO es una corrida barata, es un fallo silencioso —
    #    el recolector de costos no leyó los transcripts o la corrida no ejecutó.
    #    (Visto el 2026-07-01: auto-agente 20260701-182502 con total_tokens=0.)
    if filas and (filas[-1].get("total_tokens", 0) == 0):
        hallazgos.append({
            "id": "costo-000", "archivo": ".pipeline/costos.jsonl", "linea": 0,
            "severidad": "media", "categoria": "costo",
            "descripcion": "La última corrida (%s) registró 0 tokens: el medidor de costo falló o la corrida no ejecutó (no hay señal de gasto)." % (
                filas[-1].get("etiqueta", "?")),
            "fix_sugerido": "Revisar que el driver haya corrido y que el recolector de costos leyó los transcripts; un 0 oculta tanto una corrida caída como un medidor roto.",
        })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
