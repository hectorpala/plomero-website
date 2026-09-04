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
import re
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
    # ── REGRESIONES: clasificadas, no un contador opaco.
    # Antes se buscaba la subcadena "regres" en el JSON COMPLETO de cada fila, así que
    # contaba por igual un incidente ya arreglado, uno pendiente y una fila que solo
    # menciona la palabra dentro de una regla o un fix. El resultado ("39 regresiones")
    # alarmaba sin decir qué hacer, y escondía las reincidencias: la misma firma
    # (tracking-verificacion-ciega-sin-stdout) aparecía 3 veces contada como 3 cosas.
    # Ahora: se detecta solo en los campos que describen el INCIDENTE, se normaliza la
    # firma (sin fecha ni sufijo numérico) y se separan resueltas / pendientes / sin estado.
    CAMPOS_INCIDENTE = ("id", "descripcion", "hallazgo")

    def es_regresion(e):
        return any("regres" in str(e.get(c, "")).lower() for c in CAMPOS_INCIDENTE)

    def firma(e):
        s = str(e.get("id", "") or e.get("descripcion", "")[:60]).lower()
        s = re.sub(r"20\d{6}", "", s)           # fecha embebida: -20260901
        s = re.sub(r"[-_]?\d+$", "", s)          # sufijo numérico: movil-109
        return re.sub(r"[-_]+$", "", s) or "(sin id)"

    def estado(e):
        if e.get("arreglado"): return "resuelta"
        if e.get("pendiente"): return "pendiente"
        return "sin estado"

    regres = [e for e in h if es_regresion(e)]
    por_estado = Counter(estado(e) for e in regres)
    print("  Regresiones: %d — %d resueltas · %d PENDIENTES · %d sin estado" % (
        len(regres), por_estado["resuelta"], por_estado["pendiente"], por_estado["sin estado"]))

    # Lo accionable primero: firmas PENDIENTES que reinciden, con su última fecha.
    pendientes = [e for e in regres if estado(e) == "pendiente"]
    firmas = {}
    for e in pendientes:
        f = firma(e)
        firmas.setdefault(f, []).append(e)
    recurrentes = sorted(firmas.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    if recurrentes:
        print("  Firmas pendientes (reincidentes primero):")
        for f, es in recurrentes[:6]:
            ult = max((x.get("fecha", "") for x in es), default="?")
            marca = "  ⚠️ reincide → mecanizar en checker" if len(es) >= 2 else ""
            print("    %-46s ×%d  última %s%s" % (f[:46], len(es), ult, marca))
    elif regres:
        print("    (ninguna pendiente: todas resueltas o sin estado)")

    pend = [e for e in h if (e.get("estado") or "").lower() == "pendiente"]
    print("  Marcadas 'pendiente' aún: %d\n" % len(pend))


def sec_costos():
    c = _jsonl(".pipeline/costos.jsonl")
    print("## COSTO/CUOTA — uso por corrida (%d corridas registradas)" % len(c))
    if not c:
        print("  (sin datos)\n"); return
    # El PICO NO se mide con `total_tokens` crudo: en las filas de la era API ese campo
    # incluía cache_read (~10% del precio de un token normal) y lo dominaba — el
    # 2026-07-14, 144.0M de 148.1M (97%) eran caché, así que una corrida barata con mucha
    # caché daba ALARMA y una 54% más cara en dólares pasaba callada.
    #
    # Tampoco basta con mirar `usd_equiv_api_ref`: desde la migración a Codex,
    # `registrar-costo.mjs` escribe usd=0 a propósito (`base_precios:
    # codex-suscripcion-sin-precio`), porque la suscripción no reporta tarifa por token.
    # Un disparador que solo mire dólares queda INERTE para siempre en el régimen actual.
    #
    # Solución: elegir la métrica según lo que el registro SÍ mide, y comparar siempre
    # like-con-like (misma base de precios), igual que check-perf.mjs compara solo dentro
    # de la misma fuente. Proxy sin dólares = input+output, que EXCLUYE cache_read.
    ult = c[-1]
    base_ult = ult.get("base_precios", "(ausente)")
    mismos = [x for x in c if x.get("base_precios", "(ausente)") == base_ult]
    hay_usd = bool(ult.get("usd_equiv_api_ref", 0))

    def facturable(x):
        return (x.get("input_tokens", 0) or 0) + (x.get("output_tokens", 0) or 0)

    if hay_usd:
        metrica, unidad, valores = "costo", "$", [x.get("usd_equiv_api_ref", 0) for x in mismos]
        fmt = lambda v: "$%.2f" % v
    else:
        metrica, unidad, valores = "tokens facturables (input+output, sin caché)", "", [facturable(x) for x in mismos]
        fmt = lambda v: "%.2fM" % (v / 1e6)

    prev = [v for v in valores[:-1] if v > 0]
    mediana = sorted(prev)[len(prev) // 2] if prev else 0
    actual = valores[-1] if valores else 0
    print("  Base de medición: %s (%d corridas comparables de %d)" % (base_ult, len(mismos), len(c)))
    print("  Últimas (%s): %s" % (metrica, " · ".join(fmt(v) for v in valores[-6:])))
    print("  Mediana: %s · última: %s (%s)" % (fmt(mediana), fmt(actual), ult.get("etiqueta", "")))
    if mediana > 0 and actual > 1.5 * mediana:
        print("  ⚠️ PICO: la última corrida gastó >1.5× la mediana en %s → ¿qué la disparó?" % metrica)
    if not hay_usd:
        print("  ℹ️ sin dólares en el registro (%s): el pico se vigila por tokens facturables." % base_ult)
    # cache_read alto SIN gasto facturable alto es dato informativo, no alarma.
    cr = ult.get("cache_read_tokens", 0) or 0
    if cr and actual and cr > 4 * actual:
        print("  ℹ️ la corrida estuvo dominada por cache_read (%.1fM releídos): mucho contexto, poco gasto nuevo." % (cr / 1e6))
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
    # La EDAD es la señal, no el conteo: una tarea humana de 2 días y una de 77 se veían
    # idénticas, así que ni el meta-pase ni el parte al dueño escalaban las que se pudren
    # (bk-218a5844 llevaba 77 días esperando decisión el 2026-09-04).
    hum = [t for t in b if t.get("estado") == "requiere_humano"]
    if hum:
        print("  ⏳ esperando decisión humana: %d" % len(hum))
        filas = []
        for t in hum:
            creado = str(t.get("creado") or t.get("fecha") or "")[:10]
            try:
                edad = (date.today() - date.fromisoformat(creado)).days
            except ValueError:
                edad = None
            filas.append((edad if edad is not None else -1, creado, t))
        for edad, creado, t in sorted(filas, key=lambda x: -x[0]):
            etiqueta = "%d días" % edad if edad >= 0 else "edad desconocida"
            marca = "  ⚠️ lleva más de una semana — repítela en el parte al dueño" if edad > 7 else ""
            print("     %-28s %-16s (desde %s)%s" % (
                t.get("objetivo", "?")[:28], etiqueta, creado or "?", marca))
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
