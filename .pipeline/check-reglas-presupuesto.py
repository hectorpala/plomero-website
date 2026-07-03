#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensor de PRESUPUESTO de REGLAS.md (versión que emite el contrato {hallazgos}).
Complementa a check-reglas.py (utilidad exit-0/1 de FASE 9): convierte el over-budget en un
hallazgo DRENABLE por el diario, en vez de un exit-1 que se puede ignorar si la fase se salta.
REGLAS.md se inyecta en cada corrida y lo lee cada subagente (~19 lecturas/día); si se arrastra
sobre el tope, cuesta tokens y diluye atención. Emite a stdout SOLO {"hallazgos":[...]}.
"""
import os, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(ROOT, "docs", "REGLAS.md")
MAX_TOKENS     = 4000   # idéntico a check-reglas.py
MAX_RULE_CHARS = 900
AVISO_FRAC     = 0.95   # avisar al rozar el cap, no solo al pasarlo (hoy: 3997/4000)

def main():
    hallazgos = []
    if os.path.isfile(REGLAS):
        lines = open(REGLAS, encoding="utf-8", errors="replace").read().splitlines()
        rules = [ln for ln in lines if ln.lstrip().startswith("- [")]
        total_chars = sum(len(ln) for ln in lines)
        est_tokens = total_chars // 4
        gordas = [ln for ln in rules if len(ln) > MAX_RULE_CHARS]
        if est_tokens >= MAX_TOKENS * AVISO_FRAC:
            hallazgos.append({
                "id": "reglas-presupuesto", "archivo": "docs/REGLAS.md", "linea": 0,
                "severidad": "media", "categoria": "infra",
                "descripcion": "REGLAS.md ~%d tokens estimados (presupuesto %d). Se inyecta en cada corrida y lo lee cada subagente; arrastrarlo sobre el tope cuesta tokens y diluye atención." % (est_tokens, MAX_TOKENS),
                "fix_sugerido": "Consolidar: cada regla = qué hacer + el checker que lo caza. Cuando un error ya está mecanizado, reduce la regla a «qué + checker» y manda el relato a HISTORIAL.jsonl.",
            })
        if gordas:
            hallazgos.append({
                "id": "reglas-gordas", "archivo": "docs/REGLAS.md", "linea": 0,
                "severidad": "media", "categoria": "infra",
                "descripcion": "%d regla(s) de REGLAS.md pasan de %d chars (relato de incidente sin podar): %s" % (
                    len(gordas), MAX_RULE_CHARS, " | ".join(ln[:70] for ln in gordas[:3])),
                "fix_sugerido": "Podar cada regla gorda a 1-2 líneas accionables; el relato largo va a HISTORIAL.jsonl, no a REGLAS.md.",
            })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
