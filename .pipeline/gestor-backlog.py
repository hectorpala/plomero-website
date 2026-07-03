#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gestor-backlog.py — cola PERSISTENTE de tareas de mejora autónoma (BACKLOG.jsonl).

El Auto Agente deja de ser "reacciona a los errores de hoy" y pasa a "drena un roadmap
priorizado". DESCUBRIR llena la cola; el LOOP la drena hasta toparse con el presupuesto
(ver presupuesto-corrida.py). Una sola línea JSON por tarea (el agente corrompe menos JSONL
que Markdown). DEDUP por firma = `tipo::objetivo`: la misma tarea NO se encola dos veces.

Comandos:
  add  [spec.json | -]   Encola (o actualiza) una tarea. DEDUP por firma. Riesgo 'alto' → cola humana.
  next [--max N] [--riesgo-max medio]   Top-N PENDIENTES auto-ejecutables, por prioridad (JSON).
  close --id X --estado hecho|descartado|bloqueado [--nota ".."] [--commit SHA]
  approve --id X [--riesgo bajo|medio] [--nota ".."]   Aprobación humana: requiere_humano → pendiente.
  stats                  Resumen por estado/tipo/riesgo + tamaño de la cola humana.
  list [--estado E] [--tipo T] [--riesgo R]
  --ejemplo              Imprime un spec de tarea de ejemplo.

Prioridad = impacto / esfuerzo (mayor = antes). Solo riesgo<=medio se auto-drena; 'alto' queda
en estado 'requiere_humano' (jamás automático). Reescribe el archivo de forma atómica.
"""
import hashlib
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKLOG = os.path.join(ROOT, "data", "BACKLOG.jsonl")

ESTADOS = {"pendiente", "en_progreso", "hecho", "descartado", "bloqueado", "requiere_humano"}
RIESGOS = {"bajo": 0, "medio": 1, "alto": 2}
ABIERTOS = {"pendiente", "en_progreso", "requiere_humano", "bloqueado"}  # no resucitar cerrados

EJEMPLO = {
    "tipo": "ctr-fix",
    "objetivo": "/servicios/reparacion-de-fugas/",
    "descripcion": "Reescribir title/meta hacia la query real de mayor CTR potencial.",
    "evidencia": "GSC 30d: 1200 impresiones, CTR 0.8%, posición 6.2 — title genérico.",
    "impacto": 4,          # 1-5 (cuánto mueve la aguja)
    "esfuerzo": 2,         # 1-5 (cuánto cuesta hacerlo bien)
    "riesgo": "bajo",      # bajo|medio (auto) · alto (requiere humano)
    "origen": "revisor-gsc",
}

TIPOS_CONOCIDOS = [
    "ctr-fix", "enriquecer", "enlazado", "schema", "imagen",
    "pagina-nueva", "blog", "fix-deuda", "otro",
]


def hoy():
    return date.today().isoformat()


def firma_de(t):
    objetivo = (t.get("objetivo") or "").strip().lower().strip("/")
    return "%s::%s" % ((t.get("tipo") or "otro").strip().lower(), objetivo)


def id_de(firma):
    return "bk-" + hashlib.sha1(firma.encode("utf-8")).hexdigest()[:8]


def prioridad_de(t):
    imp = max(1, int(t.get("impacto", 1)))
    esf = max(1, int(t.get("esfuerzo", 1)))
    return round(imp / esf, 3)


def cargar():
    if not os.path.isfile(BACKLOG):
        return []
    out = []
    with open(BACKLOG, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                out.append(json.loads(ln))
            except Exception:
                # Línea corrupta: la saltamos (no perder el resto de la cola).
                sys.stderr.write("⚠️  línea de BACKLOG ilegible, omitida\n")
    return out


def guardar(tareas):
    tmp = BACKLOG + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for t in tareas:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    os.replace(tmp, BACKLOG)


def cmd_add(args):
    raw = sys.stdin.read() if (not args or args[0] == "-") else open(args[0], encoding="utf-8").read()
    try:
        spec = json.loads(raw)
    except Exception as e:
        print("❌ spec no es JSON válido: %s" % e); sys.exit(2)
    for k in ("tipo", "objetivo", "descripcion"):
        if not spec.get(k):
            print("❌ falta el campo '%s' en la tarea" % k); sys.exit(2)

    firma = firma_de(spec)
    tid = id_de(firma)
    riesgo = (spec.get("riesgo") or "medio").strip().lower()
    if riesgo not in RIESGOS:
        riesgo = "medio"

    tareas = cargar()
    por_id = {t["id"]: t for t in tareas if "id" in t}
    if tid in por_id:
        ex = por_id[tid]
        if ex.get("estado") in ("hecho", "descartado"):
            print("↩︎  ya existe y está '%s' (%s); no la reabro." % (ex.get("estado"), tid)); return
        # actualizar evidencia/impacto/esfuerzo sin tocar el estado abierto
        ex.update({
            "descripcion": spec["descripcion"],
            "evidencia": spec.get("evidencia", ex.get("evidencia", "")),
            "impacto": int(spec.get("impacto", ex.get("impacto", 3))),
            "esfuerzo": int(spec.get("esfuerzo", ex.get("esfuerzo", 3))),
            "riesgo": riesgo,
        })
        ex["prioridad"] = prioridad_de(ex)
        guardar(tareas)
        print("♻️  actualizada %s (%s)" % (tid, ex.get("estado"))); return

    t = {
        "id": tid,
        "firma": firma,
        "tipo": spec["tipo"].strip().lower(),
        "objetivo": spec["objetivo"].strip(),
        "descripcion": spec["descripcion"].strip(),
        "evidencia": spec.get("evidencia", "").strip(),
        "impacto": int(spec.get("impacto", 3)),
        "esfuerzo": int(spec.get("esfuerzo", 3)),
        "riesgo": riesgo,
        "estado": "requiere_humano" if riesgo == "alto" else "pendiente",
        "origen": spec.get("origen", "desconocido"),
        "creado": hoy(),
        "intentos": 0,
        "cerrado": None,
        "nota": "",
    }
    t["prioridad"] = prioridad_de(t)
    tareas.append(t)
    guardar(tareas)
    print("✅ encolada %s [%s] prioridad %.2f · estado %s" % (tid, t["tipo"], t["prioridad"], t["estado"]))


def cmd_next(args):
    mx = 5
    riesgo_max = "medio"
    if "--max" in args:
        mx = int(args[args.index("--max") + 1])
    if "--riesgo-max" in args:
        riesgo_max = args[args.index("--riesgo-max") + 1]
    tope = RIESGOS.get(riesgo_max, 1)
    tareas = [t for t in cargar()
              if t.get("estado") == "pendiente" and RIESGOS.get(t.get("riesgo", "medio"), 1) <= tope]
    tareas.sort(key=lambda t: (-prioridad_de(t), -int(t.get("impacto", 1)), t.get("creado", "")))
    print(json.dumps(tareas[:mx], ensure_ascii=False, indent=2))


def cmd_close(args):
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default
    tid = opt("--id")
    estado = opt("--estado")
    if not tid or estado not in ESTADOS:
        print("uso: close --id <id> --estado hecho|descartado|bloqueado [--nota ..] [--commit ..]"); sys.exit(2)
    tareas = cargar()
    for t in tareas:
        if t.get("id") == tid:
            t["estado"] = estado
            t["cerrado"] = hoy()
            if opt("--nota"):
                t["nota"] = opt("--nota")
            if opt("--commit"):
                t["commit"] = opt("--commit")
            if estado == "bloqueado":
                t["intentos"] = int(t.get("intentos", 0)) + 1
            guardar(tareas)
            print("✅ %s → %s" % (tid, estado)); return
    print("❌ no encontré la tarea %s" % tid); sys.exit(1)


def cmd_approve(args):
    """Aprobación HUMANA: pasa una tarea 'requiere_humano'/'bloqueado' a 'pendiente' auto-ejecutable
    (decisión de negocio resuelta). Baja el riesgo al nivel dado (default 'medio')."""
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default
    tid = opt("--id")
    riesgo = (opt("--riesgo", "medio") or "medio").lower()
    if not tid or riesgo not in RIESGOS:
        print("uso: approve --id <id> [--riesgo bajo|medio] [--nota ..]"); sys.exit(2)
    tareas = cargar()
    for t in tareas:
        if t.get("id") == tid:
            t["estado"] = "pendiente"
            t["riesgo"] = riesgo
            t["cerrado"] = None
            if opt("--nota"):
                t["nota"] = opt("--nota")
            t["prioridad"] = prioridad_de(t)
            guardar(tareas)
            print("✅ aprobada %s → pendiente (riesgo %s, prioridad %.2f)" % (tid, riesgo, t["prioridad"])); return
    print("❌ no encontré la tarea %s" % tid); sys.exit(1)


def cmd_stats(_args):
    tareas = cargar()
    por_estado, por_tipo = {}, {}
    for t in tareas:
        por_estado[t.get("estado", "?")] = por_estado.get(t.get("estado", "?"), 0) + 1
        por_tipo[t.get("tipo", "?")] = por_tipo.get(t.get("tipo", "?"), 0) + 1
    pend = [t for t in tareas if t.get("estado") == "pendiente"]
    auto = [t for t in pend if RIESGOS.get(t.get("riesgo", "medio"), 1) <= 1]
    print("📦 BACKLOG: %d tareas" % len(tareas))
    print("   por estado: " + " · ".join("%s=%d" % kv for kv in sorted(por_estado.items())))
    print("   por tipo:   " + " · ".join("%s=%d" % kv for kv in sorted(por_tipo.items())))
    print("   auto-ejecutables ahora (pendiente, riesgo<=medio): %d" % len(auto))
    print("   esperando decisión humana (requiere_humano): %d"
          % sum(1 for t in tareas if t.get("estado") == "requiere_humano"))


def cmd_list(args):
    def opt(name):
        return args[args.index(name) + 1] if name in args else None
    fe, ft, fr = opt("--estado"), opt("--tipo"), opt("--riesgo")
    for t in cargar():
        if fe and t.get("estado") != fe:
            continue
        if ft and t.get("tipo") != ft:
            continue
        if fr and t.get("riesgo") != fr:
            continue
        print("%-13s [%-12s] P%.2f r:%-5s %-14s %s"
              % (t.get("id"), t.get("tipo"), prioridad_de(t), t.get("riesgo"),
                 t.get("estado"), t.get("objetivo")))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "--ejemplo":
        print(json.dumps(EJEMPLO, ensure_ascii=False, indent=2)); return
    {"add": cmd_add, "next": cmd_next, "close": cmd_close, "approve": cmd_approve,
     "stats": cmd_stats, "list": cmd_list}.get(cmd, lambda a: (
        print("comando desconocido: %s" % cmd) or sys.exit(2)))(rest)


if __name__ == "__main__":
    main()
