#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensor de PRESUPUESTO DE CONTEXTO: vigila los archivos que el orquestador carga en CADA
corrida y que, por tanto, se releen en CADA llamada a la API.

POR QUÉ. El costo/cuota de una corrida NO lo domina lo que el modelo escribe (output ≈ 11%)
sino lo que RELEE: `cache_read` ≈ (tamaño del contexto) × (nº de llamadas). Medido el
2026-07-08: la corrida de 1,115 mensajes gastó 143.1M de cacheR; el preámbulo fijo (CLAUDE.md
+ REGLAS + ESTADO + NEGOCIO + prompt ≈ 30k tokens) explica ~34M de esos (24%). Cada 1k tokens
que se recorten del preámbulo ahorran ~1.1M de cacheR por corrida.

QUÉ HACE. Estima los tokens (~chars/4) de cada archivo residente en contexto y avisa cuando
alguno —o el total— pasa su presupuesto, para que el AGENTE BIBLIOTECARIO (FASE 9) lo compacte,
igual que ya se hace con REGLAS.md. Es VISIBILIDAD: severidad `media`, nunca bloquea el push.
No reescribe nada: decidir qué se archiva es criterio, no mecánica.

Emite el JSON común {"hallazgos":[...]}. Sin argumentos.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Archivo -> presupuesto en tokens. REGLAS.md ya usaba 4000 por convención del pipeline.
# ESTADO.md se fija en 6000: hoy trae 17k porque acumuló bitácora histórica; solo necesita
# el estado de la ÚLTIMA corrida + pendientes abiertos (lo viejo vive en HISTORIAL.jsonl).
PRESUPUESTOS = {
    "CLAUDE.md": 2_500,
    "docs/REGLAS.md": 4_000,
    "docs/ESTADO.md": 6_000,
    "docs/NEGOCIO.md": 1_500,
    ".pipeline/crecer-diario-prompt.txt": 7_000,
}
PRESUPUESTO_TOTAL = 20_000

# Nº de llamadas de una corrida típica, para traducir tokens de preámbulo a cacheR ahorrable.
MENSAJES_TIPICOS = 1_100


def _tokens(path):
    try:
        return os.path.getsize(path) // 4      # ~4 chars por token; basta para un presupuesto
    except OSError:
        return None


def main():
    hallazgos, total, medidos = [], 0, {}
    for rel, presupuesto in PRESUPUESTOS.items():
        tok = _tokens(os.path.join(ROOT, rel))
        if tok is None:
            continue                            # archivo movido/ausente: no es asunto de este sensor
        medidos[rel] = tok
        total += tok
        if tok > presupuesto:
            exceso = tok - presupuesto
            hallazgos.append({
                "id": "contexto-%s" % os.path.basename(rel),
                "archivo": rel, "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "%s pesa ~%s tokens, %s sobre su presupuesto (%s). Se relee en cada llamada: "
                               "~%.1fM de cache_read por corrida solo por el exceso." % (
                                   rel, f"{tok:,}", f"{exceso:,}", f"{presupuesto:,}",
                                   exceso * MENSAJES_TIPICOS / 1e6),
                "fix_sugerido": "Compactar: mover lo histórico a HISTORIAL.jsonl (o docs/archivo/) y dejar solo "
                                "lo vigente. Es la misma consolidación que ya se aplica a REGLAS.md.",
            })

    if total > PRESUPUESTO_TOTAL:
        detalle = " · ".join("%s %s" % (os.path.basename(k), f"{v:,}")
                             for k, v in sorted(medidos.items(), key=lambda kv: -kv[1]))
        hallazgos.append({
            "id": "contexto-total", "archivo": "docs/", "linea": 0,
            "severidad": "media", "categoria": "costo",
            "descripcion": "El preámbulo residente suma ~%s tokens (presupuesto %s) y se relee en cada una de las "
                           "~%s llamadas: ~%.0fM de cache_read por corrida. Desglose: %s." % (
                               f"{total:,}", f"{PRESUPUESTO_TOTAL:,}", f"{MENSAJES_TIPICOS:,}",
                               total * MENSAJES_TIPICOS / 1e6, detalle),
            "fix_sugerido": "Recortar el archivo más gordo primero: cada 1k tokens menos ≈ 1.1M de cacheR menos por "
                            "corrida. El output del modelo es solo ~11% del gasto; el contexto releído es el grueso.",
        })

    print(json.dumps({"hallazgos": hallazgos, "tokens_preambulo": total,
                      "medidos": medidos}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
