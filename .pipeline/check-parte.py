#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-parte.py — CUADRE determinista del parte por email contra los cambios reales.

Cierra el hueco: la completitud del parte (.pipeline/ultima-corrida.md) la auto-reporta el LLM
en la FASE 10. Este check verifica, SIN depender del LLM, que el parte cuadre:

  1) CONSISTENCIA INTERNA (duro): los conteos del encabezado ("Encontré N: arreglé X · Y · Z")
     igualan el nº de bullets de cada sección (Arreglé / Necesito que decidas / No pude / Mejoré),
     y N == X+Y+Z. Caza el error típico: "arreglé 3" pero lista 2.
  2) URLs REALES (duro): toda URL https://plomeroculiacanpro.mx/... citada en Arreglé/Mejoré
     debe resolver a un archivo que EXISTE en el repo. Caza páginas "arregladas" inventadas.
  3) CUADRE vs DIFF (duro, solo con --diff-base): toda página que el parte dice haber tocado
     debe aparecer en `git diff <base>...HEAD`. Caza fixes que el parte afirma pero no ocurrieron.
  4) HISTORIAL (blando): compara "arreglé X" contra las entradas 'arreglado' de hoy en HISTORIAL.jsonl.

Uso:
  python3 .pipeline/check-parte.py .pipeline/ultima-corrida.md                  # 1,2,4
  python3 .pipeline/check-parte.py .pipeline/ultima-corrida.md --diff-base main # + 3 (rama viva)

Salida: reporte legible. Exit 0 si cuadra; 1 si hay discrepancia DURA (1/2/3).
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMINIO = "plomeroculiacanpro.mx"


def leer(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def secciones(texto):
    """Parte el markdown en {clave_seccion: [lineas]} por encabezados ## ..."""
    out, actual = {}, None
    for ln in texto.splitlines():
        if re.match(r"^\s*#{1,3}\s", ln):
            h = ln.lower()
            if "no pude" in h:
                actual = "no_pude"
            elif "arregl" in h:                # "✅ Arreglé"
                actual = "arreglados"
            elif "decidas" in h or "necesito que" in h:
                actual = "para_ti"
            elif "mejor" in h or "agregu" in h:  # "🌱 Mejoré / agregué"
                actual = "mejoras"
            else:
                actual = None
            if actual:
                out.setdefault(actual, [])
            continue
        if actual:
            out[actual].append(ln)
    return out


def contar_bullets(lineas):
    return sum(1 for ln in lineas if re.match(r"^\s*-\s+\S", ln))


def urls_de(lineas):
    txt = "\n".join(lineas)
    return re.findall(r"https?://%s(/[^\s)\]]*)" % re.escape(DOMINIO), txt)


def path_existe(url_path):
    """¿La URL resuelve a un archivo del repo? Acepta /ruta/, /ruta, /ruta/index.html."""
    p = url_path.strip("/")
    if p == "":
        return os.path.isfile(os.path.join(ROOT, "index.html"))  # home
    cand = [os.path.join(ROOT, p, "index.html"), os.path.join(ROOT, p)]
    return any(os.path.isfile(c) for c in cand)


def main():
    args = sys.argv[1:]
    diff_base = None
    if "--diff-base" in args:
        i = args.index("--diff-base")
        diff_base = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if not args:
        print("Uso: check-parte.py <parte.md> [--diff-base <ref>]"); sys.exit(2)
    parte = args[0]
    if not os.path.isfile(parte):
        print("❌ no existe el parte: %s" % parte); sys.exit(1)

    texto = leer(parte)
    errores, avisos = [], []

    # ── Encabezado de conteo ──────────────────────────────────────────────
    if not re.search(r"\*\*Resultado:\*\*", texto):
        errores.append("falta la línea `**Resultado:**` (de ahí sale el asunto del correo).")

    # Ancla al renglón ÚNICO "Encontré N cosas: arreglé X · Y necesitan tu decisión · Z no pude…"
    # (el «cosas:» lo distingue de la línea **Resultado:**; sin re.S para no cruzar renglones).
    m = re.search(r"[Ee]ncontr[ée]\s+(\d+)\s+cosas?:\s*arregl[ée]\s+(\d+).*?(\d+)\s+necesitan.*?(\d+)\s+no pude",
                  texto)
    if not m:
        errores.append("no encuentro el conteo «Encontré N: arreglé X · Y necesitan tu decisión · "
                       "Z no pude arreglar solo» — el parte no sigue la estructura esperada.")
        N = X = Y = Z = None
    else:
        N, X, Y, Z = (int(g) for g in m.groups())
        if N != X + Y + Z:
            errores.append("el encabezado no suma: encontré %d ≠ arreglé %d + para-ti %d + no-pude %d (=%d)."
                           % (N, X, Y, Z, X + Y + Z))

    sec = secciones(texto)
    b_arr = contar_bullets(sec.get("arreglados", []))
    b_pt = contar_bullets(sec.get("para_ti", []))
    b_np = contar_bullets(sec.get("no_pude", []))
    b_mej = contar_bullets(sec.get("mejoras", []))

    # ── 1) Consistencia interna conteo ↔ bullets ──────────────────────────
    if X is not None and b_arr != X:
        errores.append("«arreglé %d» pero la sección ✅ Arreglé tiene %d ítems." % (X, b_arr))
    if Y is not None and b_pt != Y:
        errores.append("«%d necesitan tu decisión» pero la sección ⏳ tiene %d ítems." % (Y, b_pt))
    if Z is not None and b_np != Z:
        errores.append("«%d no pude arreglar» pero la sección ⚠️ tiene %d ítems." % (Z, b_np))

    # ── 2) URLs de páginas arregladas/mejoradas deben EXISTIR ─────────────
    urls = urls_de(sec.get("arreglados", []) + sec.get("mejoras", []))
    for u in urls:
        if not path_existe(u):
            errores.append("URL citada que NO existe en el repo (¿fix inventado?): %s%s" % (DOMINIO, u))

    # ── 3) Cuadre vs diff de la corrida (rama viva) ───────────────────────
    if diff_base:
        try:
            r = subprocess.run(["git", "diff", "--name-only", "%s...HEAD" % diff_base],
                               capture_output=True, text=True, cwd=ROOT, check=True)
            cambiados = set(r.stdout.split())
        except Exception as e:
            avisos.append("no pude calcular el diff vs %s (%s) — omito el cuadre con git." % (diff_base, e))
            cambiados = None
        if cambiados is not None:
            for u in urls:
                p = u.strip("/")
                esperado = (p + "/index.html") if p else "index.html"
                # ¿algún archivo cambiado corresponde a esta página?
                if not any(c == esperado or c.startswith(p + "/") for c in cambiados):
                    errores.append("el parte dice haber tocado %s%s, pero esa página NO está en el "
                                   "diff de la corrida (%s...HEAD)." % (DOMINIO, u, diff_base))

    # ── 4) HISTORIAL.jsonl de hoy (blando) ────────────────────────────────
    hist = os.path.join(ROOT, "HISTORIAL.jsonl")
    if X is not None and os.path.isfile(hist):
        hoy = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
        arreglados_hoy = 0
        for ln in leer(hist).splitlines():
            if hoy in ln and "arreglado" in ln.lower():
                arreglados_hoy += 1
        if arreglados_hoy and arreglados_hoy != X:
            avisos.append("«arreglé %d» en el parte vs %d entradas 'arreglado' con fecha de hoy en "
                          "HISTORIAL.jsonl (revisa que no falte ni sobre un arreglo)." % (X, arreglados_hoy))

    # ── Veredicto ─────────────────────────────────────────────────────────
    print("📋 Cuadre del parte: arreglé=%s/✅%d · para-ti=%s/⏳%d · no-pude=%s/⚠️%d · mejoras/🌱%d · URLs %d"
          % (X, b_arr, Y, b_pt, Z, b_np, b_mej, len(urls)))
    for a in avisos:
        print("   ⚠️  " + a)
    if errores:
        print("\n❌ EL PARTE NO CUADRA con los cambios reales:")
        for e in errores:
            print("   • " + e)
        sys.exit(1)
    print("✅ El parte cuadra (conteos, URLs reales%s)." % (" y diff" if diff_base else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
