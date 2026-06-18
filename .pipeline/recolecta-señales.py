#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recolecta-señales.py — junta (determinista, barato) las SEÑALES del sistema en un brief
compacto para que critico-sistema (Opus) las JUZGUE. Patrón del repo: el recolector es tonto y
barato; la inteligencia (qué proponer) la pone el LLM encima, sobre datos duros, no crawleando.

Lee lo que el sistema YA produce y NO inventa nada:
  • HISTORIAL.jsonl  → áreas de error recurrentes + regresiones (candidatas a mecanizar en checker)
  • costos.jsonl     → tendencia de consumo de cuota + picos
  • BACKLOG.jsonl    → tareas bloqueadas, atascadas o esperando decisión humana
  • REGLAS.md        → presupuesto (¿se está hinchando?)

Uso:  python3 .pipeline/recolecta-señales.py        # imprime el brief a stdout
"""
import json
import os
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _jsonl(path):
    p = os.path.join(ROOT, path)
    if not os.path.isfile(p):
        return []
    out = []
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def sec_historial():
    h = _jsonl("HISTORIAL.jsonl")
    print("## HISTORIAL — errores (%d entradas)" % len(h))
    if not h:
        print("  (sin datos)\n"); return
    cats = Counter((e.get("categoria") or e.get("category") or "?") for e in h)
    print("  Áreas más frecuentes (categoria → veces):")
    for c, n in cats.most_common(8):
        flag = "  ⚠️ recurrente → ¿mecanizar en checker?" if n >= 3 else ""
        print("    %-16s %d%s" % (c, n, flag))
    # regresiones (mismo error que reapareció)
    regres = [e for e in h if "regres" in json.dumps(e, ensure_ascii=False).lower()]
    print("  Regresiones detectadas: %d%s" % (
        len(regres), "  ⚠️ falta regla/checker que lo prevenga de raíz" if regres else ""))
    pend = [e for e in h if (e.get("estado") or "").lower() == "pendiente"]
    print("  Marcadas 'pendiente' aún: %d\n" % len(pend))


def sec_costos():
    c = _jsonl("costos.jsonl")
    print("## COSTO/CUOTA — uso por corrida (%d corridas registradas)" % len(c))
    if not c:
        print("  (sin datos)\n"); return
    tot = [x.get("total_tokens", 0) for x in c]
    ult = c[-1]
    mediana = sorted(tot)[len(tot) // 2]
    print("  Últimas corridas (M tokens): " + " · ".join("%.1f" % (t / 1e6) for t in tot[-6:]))
    print("  Mediana: %.1fM · última: %.1fM (%s)" % (
        mediana / 1e6, ult.get("total_tokens", 0) / 1e6, ult.get("etiqueta", "")))
    if ult.get("total_tokens", 0) > 1.5 * mediana and mediana > 0:
        print("  ⚠️ PICO: la última corrida gastó >1.5× la mediana → ¿qué la disparó?")
    print()


def sec_backlog():
    b = _jsonl("BACKLOG.jsonl")
    print("## BACKLOG — cola de mejoras (%d tareas)" % len(b))
    if not b:
        print("  (sin datos)\n"); return
    est = Counter(t.get("estado", "?") for t in b)
    print("  Por estado: " + " · ".join("%s=%d" % kv for kv in sorted(est.items())))
    bloq = [t for t in b if t.get("estado") == "bloqueado"]
    if bloq:
        print("  ⚠️ BLOQUEADAS (≥1 = falta capacidad o el prompt no alcanza):")
        for t in bloq:
            print("    %s [%s] intentos=%s — %s" % (
                t.get("id"), t.get("tipo"), t.get("intentos"), t.get("objetivo")))
    hum = [t for t in b if t.get("estado") == "requiere_humano"]
    if hum:
        print("  ⏳ esperando decisión humana: %d (%s)" % (
            len(hum), ", ".join(t.get("objetivo", "?") for t in hum)))
    print()


def sec_reglas():
    p = os.path.join(ROOT, "REGLAS.md")
    if not os.path.isfile(p):
        return
    chars = sum(len(l) for l in open(p, encoding="utf-8"))
    print("## REGLAS.md — presupuesto de memoria")
    print("  ~%d tokens estimados (presupuesto 4000)%s\n" % (
        chars // 4, "  ⚠️ cerca/encima del tope → consolidar" if chars // 4 > 3600 else ""))


def main():
    print("# BRIEF DE SEÑALES DEL SISTEMA — %s" % date.today().isoformat())
    print("(datos duros para que critico-sistema PROPONGA; no es un veredicto, es materia prima)\n")
    sec_historial()
    sec_costos()
    sec_backlog()
    sec_reglas()


if __name__ == "__main__":
    main()
