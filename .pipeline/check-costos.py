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
from datetime import date, datetime, timedelta

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTOS = os.path.join(ROOT, ".pipeline", "costos.jsonl")

# ── PRESUPUESTO. Dos correcciones (2026-07-08):
# 1) UMBRAL_TOKENS era 28M "≈2x una corrida normal (11.8M)". Pero total_tokens lo domina
#    cache_read (contexto releído, BARATO) y el contexto creció: la mediana de las últimas
#    12 corridas es 26.4M y las recientes traen 83–147M -> el umbral disparaba en más de la
#    mitad de las corridas. Una alarma que siempre suena es una alarma que nadie lee.
#    Ahora mide lo que de verdad significa: EXPLOSIÓN DE CONTEXTO (cache_read desbocado).
# 2) usd_equiv_api_ref cambió de base: antes TODO se cotizaba a precios Opus aunque la corrida
#    es multi-modelo; ahora cada mensaje va con SU modelo (ver registrar-costo.mjs). Las filas
#    viejas traen base "opus" (inflada ~5x) y las nuevas base "por-modelo". El umbral se elige
#    según `base_precios` para no leer mal ninguna de las dos.
UMBRAL_TOKENS = 200_000_000  # explosión de contexto (mediana 26M; cache_read domina y es barato)
UMBRAL_USD_OPUS = 250        # filas viejas (base "opus", inflada ~5x). El 70 original disparaba
                             # en la mayoría: la mediana en esa base es $90. 250 ≈ corrida de verdad
                             # anómala (la desbocada del 26-jun marcó $1420).
UMBRAL_USD_REAL = 70         # filas nuevas (base "por-modelo"). Conservador a propósito:
                             # recalibrar tras ~4 corridas reales, cuando haya mediana propia.

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
            # Excluir filas de 0 tokens (corridas fallidas) de la mediana: la deprimen
            # y generan falsos positivos de runaway en la siguiente corrida normal.
            med = _mediana([f.get(campo, 0) or 0 for f in prev if (f.get("total_tokens", 0) or 0) > 0])
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
        # Base de precios de ESTA fila: las viejas no traen el campo y están en base "opus".
        base = u.get("base_precios", "opus")
        umbral_usd = UMBRAL_USD_REAL if base == "por-modelo" else UMBRAL_USD_OPUS
        if tok > UMBRAL_TOKENS or usd > umbral_usd:
            # El desglose por modelo delata la causa: si aparece opus con mucho volumen en una
            # corrida cuyo orquestador va en sonnet, o corrió un subagente caro o se coló otra sesión.
            pm = u.get("por_modelo") or {}
            detalle = "  ·  ".join(
                "%s $%s" % (f, a.get("usd", 0)) for f, a in sorted(pm.items(), key=lambda kv: -(kv[1].get("usd") or 0)) if f != "sintetico"
            )
            hallazgos.append({
                "id": "costo-001", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "La última corrida (%s) consumió %.1fM tokens (~$%.0f api-ref, base %s), sobre presupuesto (%.0fM / $%.0f).%s" % (
                    u.get("etiqueta", "?"), tok/1e6, usd, base, UMBRAL_TOKENS/1e6, umbral_usd,
                    (" Desglose: %s." % detalle) if detalle else ""),
                "fix_sugerido": "Auditar la corrida: ¿demasiados revisores en paralelo, lote grande, o un loop sin freno? Si el desglose muestra OPUS con mucho volumen y el orquestador va en sonnet, revisar qué subagente lo usó (o si se contó una sesión interactiva ajena). Bajar fan-out o modelo en revisores deterministas.",
            })
        # Un modelo nuevo sin precio se cotiza como opus (conservador) pero hay que registrarlo.
        if u.get("modelos_desconocidos"):
            hallazgos.append({
                "id": "costo-modelo-nuevo", "archivo": ".pipeline/registrar-costo.mjs", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "Modelo(s) sin precio en la tabla: %s. Se cotizaron como Opus (no subestima), pero la referencia de costo queda inexacta." % ", ".join(u["modelos_desconocidos"]),
                "fix_sugerido": "Añadir la familia y sus precios a PRECIOS en .pipeline/registrar-costo.mjs (patrón: out=5x in, cacheW=1.25x in, cacheR=0.1x in).",
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
    # ── CONTINUIDAD: día(s) SIN fila = el auto-agente no corrió (o no registró) y nadie
    #    avisó. Caso real: 04→06-jul-2026, 3 días sin corrida completa y ningún sensor
    #    gritó (el catch-up miraba el log del sitio hermano). Umbral 2: la fila de HOY
    #    puede no existir aún cuando este checker corre a mitad de la corrida.
    if filas:
        fechas = [f.get("fecha", "") for f in filas if f.get("fecha")]
        try:
            ultima = max(datetime.strptime(x, "%Y-%m-%d").date() for x in fechas)
            dias = (date.today() - ultima).days
            if dias >= 2:
                hallazgos.append({
                    "id": "costo-continuidad", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                    "severidad": "alta", "categoria": "costo",
                    "descripcion": "CONTINUIDAD ROTA: la última fila del ledger es del %s (%d días sin corrida registrada). El auto-agente no está corriendo o no está registrando." % (ultima.isoformat(), dias),
                    "fix_sugerido": "Revisar launchctl (com.plomeroculiacan.autoagente), el log más reciente en ~/Library/Logs/mantener-sitio/ y los failnotes fail-*.md; el catch-up debería recuperar al siguiente arranque.",
                })
        except ValueError:
            pass
    # ── CORRIDA ENANA: fila con pocos mensajes = la corrida arrancó y murió a los minutos
    #    (p.ej. 2026-07-01: 1 mensaje). No es 0 (eso lo caza costo-000) pero tampoco corrió.
    if filas:
        u = filas[-1]
        msj = u.get("mensajes", 0) or 0
        if 0 < msj <= 5:
            hallazgos.append({
                "id": "costo-enana", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "CORRIDA ENANA: la última (%s) registró solo %d mensaje(s) — arrancó y murió casi de inmediato (una corrida normal trae cientos)." % (u.get("etiqueta", "?"), msj),
                "fix_sugerido": "Revisar el log de esa corrida y el failnote correspondiente; la causa típica es error temprano del CLI (red/credenciales).",
            })
    print(json.dumps({"hallazgos": hallazgos, "analizadas": len(filas)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
