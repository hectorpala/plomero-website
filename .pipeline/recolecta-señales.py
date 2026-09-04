#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recolecta-señales.py — junta (determinista, barato) las SEÑALES del sistema en un brief
compacto para que critico-sistema (Codex) las JUZGUE. Patrón del repo: el recolector es tonto y
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
import subprocess
from collections import Counter
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True,
                          errors="replace")


def sec_ramas_atascadas():
    """Expone ramas auto/* no fusionadas: antes podían quedar bloqueadas por el cap sin
    aparecer en el brief del crítico-sistema durante días."""
    r = _git("branch", "--no-merged", "main", "--format=%(refname:short)")
    ramas = sorted(b.strip() for b in r.stdout.splitlines() if b.strip().startswith("auto/"))
    print("## RAMAS AUTOMÁTICAS NO FUSIONADAS — %d" % len(ramas))
    if not ramas:
        print("  (ninguna)\n"); return
    hoy = date.today()
    for rama in ramas:
        log = _git("log", "--reverse", "--format=%ct", "main..%s" % rama)
        primera = next((x.strip() for x in log.stdout.splitlines() if x.strip().isdigit()), "")
        if primera:
            inicio = datetime.fromtimestamp(int(primera)).date()
            edad = max(0, (hoy - inicio).days)
            marca = "  ⚠️ ATASCADA" if edad >= 2 else ""
            print("  • %s — %d día(s) desde su primer commit%s" % (rama, edad, marca))
        else:
            print("  • %s — sin commit exclusivo detectable" % rama)
    print()


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
    h = _jsonl("data/HISTORIAL.jsonl")
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
    c = _jsonl(".pipeline/costos.jsonl")
    print("## COSTO/CUOTA — uso por corrida (%d corridas registradas)" % len(c))
    if not c:
        print("  (sin datos)\n"); return
    # El PICO se mide en DINERO, no en tokens crudos. `total_tokens` suma
    # input+output+cache_write+cache_read, y cache_read (~10% del precio de un token
    # normal) domina el total: el 2026-07-14, 144.0M de 148.1M tokens (97%) fueron
    # cache_read. Con el disparador viejo, una corrida barata con mucha caché daba
    # ALARMA y una corrida 54% más cara en dólares pasaba callada. El propio
    # costos.jsonl ya calcula `usd_equiv_api_ref` por-modelo desde 2026-07-09.
    tot = [x.get("total_tokens", 0) for x in c]
    usd = [x.get("usd_equiv_api_ref", 0) for x in c]
    ult = c[-1]
    mediana_tok = sorted(tot)[len(tot) // 2]
    usd_validos = [u for u in usd if u]
    mediana_usd = sorted(usd_validos)[len(usd_validos) // 2] if usd_validos else 0
    ult_usd = ult.get("usd_equiv_api_ref", 0)
    print("  Últimas corridas (USD ref): " + " · ".join("%.2f" % u for u in usd[-6:]))
    print("  Mediana: $%.2f · última: $%.2f (%s)" % (mediana_usd, ult_usd, ult.get("etiqueta", "")))
    print("  Tokens (informativo, M): " + " · ".join("%.1f" % (t / 1e6) for t in tot[-6:]))
    if mediana_usd > 0 and ult_usd > 1.5 * mediana_usd:
        print("  ⚠️ PICO DE COSTO: la última corrida gastó >1.5× la mediana en dólares → ¿qué la disparó?")
    elif not usd_validos:
        print("  ⚠️ sin `usd_equiv_api_ref` en el registro: no se puede medir el costo real")
    # Tokens altos SIN costo alto sigue siendo dato útil (corrida con mucha caché),
    # pero es informativo, no alarma.
    if mediana_tok > 0 and ult.get("total_tokens", 0) > 1.5 * mediana_tok and not (
            mediana_usd > 0 and ult_usd > 1.5 * mediana_usd):
        print("  ℹ️ tokens por encima de la mediana pero SIN pico de costo (corrida dominada por cache_read)")
    print()


def sec_backlog():
    b = _jsonl("data/BACKLOG.jsonl")
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
    p = os.path.join(ROOT, "docs", "REGLAS.md")
    if not os.path.isfile(p):
        return
    chars = sum(len(l) for l in open(p, encoding="utf-8"))
    print("## REGLAS.md — presupuesto de memoria")
    print("  ~%d tokens estimados (presupuesto 4000)%s\n" % (
        chars // 4, "  ⚠️ cerca/encima del tope → consolidar" if chars // 4 > 3600 else ""))


def main():
    print("# BRIEF DE SEÑALES DEL SISTEMA — %s" % date.today().isoformat())
    print("(datos duros para que critico-sistema PROPONGA; no es un veredicto, es materia prima)\n")
    sec_ramas_atascadas()
    sec_historial()
    sec_costos()
    sec_backlog()
    sec_reglas()


if __name__ == "__main__":
    main()
