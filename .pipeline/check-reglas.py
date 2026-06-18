#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-reglas.py — Guard de PRESUPUESTO de REGLAS.md.

REGLAS.md se inyecta como contexto en CADA corrida y lo lee CADA subagente (~19 lecturas/día).
Si crece sin control, cuesta tokens y diluye la atención del agente — justo el modo de fallo
que el propio diseño advierte ("podar sin piedad"). Este guard lo hace AUTO-CUMPLIDO: la FASE 9
(aprender) corre este check y, si excede el presupuesto, el bibliotecario DEBE consolidar antes
de cerrar la corrida.

Presupuesto:
  • Tamaño total  ≤ MAX_TOKENS (estimado chars/4).
  • Regla individual ≤ MAX_RULE_CHARS (una regla larga = relato de incidente sin podar;
    ese relato va a HISTORIAL.jsonl, no aquí. La regla se queda en 1-2 líneas accionables).

Uso:  python3 .pipeline/check-reglas.py     # exit 0 si está dentro de presupuesto, 1 si no.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(ROOT, "REGLAS.md")

MAX_TOKENS = 4000        # presupuesto total (estimado)
MAX_RULE_CHARS = 900     # una sola regla no debería pasar de ~1-2 líneas accionables


def main():
    if not os.path.isfile(REGLAS):
        print("⚠️  no existe REGLAS.md"); sys.exit(0)
    with open(REGLAS, encoding="utf-8") as f:
        lines = f.read().splitlines()

    rules = [ln for ln in lines if ln.lstrip().startswith("- [")]
    total_chars = sum(len(ln) for ln in lines)
    est_tokens = total_chars // 4
    gordas = sorted(
        [(len(ln), ln) for ln in rules if len(ln) > MAX_RULE_CHARS],
        reverse=True,
    )

    print("📏 REGLAS.md: %d reglas · %d chars · ~%d tokens estimados (presupuesto %d)"
          % (len(rules), total_chars, est_tokens, MAX_TOKENS))

    problemas = 0
    if est_tokens > MAX_TOKENS:
        print("❌ Excede el presupuesto total por ~%d tokens." % (est_tokens - MAX_TOKENS))
        problemas += 1
    if gordas:
        print("❌ %d regla(s) demasiado larga(s) (> %d chars) — consolidar a 1-2 líneas y "
              "mover el relato a HISTORIAL.jsonl:" % (len(gordas), MAX_RULE_CHARS))
        for n, ln in gordas:
            print("   • %d chars · %s…" % (n, ln[:90]))
        problemas += 1

    if problemas:
        print("\n→ CONSOLIDA: cada regla = qué hacer + el checker que lo caza. "
              "Cuando un error ya está mecanizado, la regla se reduce a «qué + checker».")
        sys.exit(1)
    print("✅ REGLAS.md dentro de presupuesto.")
    sys.exit(0)


if __name__ == "__main__":
    main()
