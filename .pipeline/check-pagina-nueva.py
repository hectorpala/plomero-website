#!/usr/bin/env python3
# infra:utilidad-no-sensor (candado por-argumentos; no emite el contrato {hallazgos} — se auto-excluye del dead-man's switch)
"""
check-pagina-nueva.py — CANDADO para páginas NUEVAS (recién creadas en el push).
Hace AUTOMÁTICO (bloqueante) lo que el dueño pidió y antes solo vivía como nota:
  1) SIN precio VISIBLE: una página nueva no debe mostrar precios en el cuerpo
     (priceRange en JSON-LD está permitido; lo visible no). -> usa "cotización gratis".
  2) SIN reseñas/testimonios inventados ni aggregateRating (seo-104).

Solo aplica a páginas NUEVAS (el pre-push le pasa las añadidas, --diff-filter=A).
Las páginas EXISTENTES conservan sus precios y no se tocan aquí.

Uso:  python3 check-pagina-nueva.py <ruta1/index.html> [ruta2 ...]
Exit 0 = OK (o sin páginas nuevas).  Exit 1 = viola una regla -> BLOQUEA el push.
"""
import sys, re

viol = []
revisadas = 0
for f in sys.argv[1:]:
    try:
        s = open(f, encoding="utf-8").read()
    except OSError:
        continue
    revisadas += 1
    # cuerpo visible = quitar <script> (JSON-LD/JS) y <style>
    body = re.sub(r"<script.*?</script>", "", s, flags=re.S | re.I)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", body)

    # 1) precio visible: $1,500 / $350 / "1500 pesos" / "1,500 MXN"
    precios = re.findall(r"\$\s?[0-9][0-9.,]*", text)
    precios += re.findall(r"[0-9][0-9.,]*\s?(?:pesos|MXN|mxn)\b", text)
    if precios:
        viol.append(f"{f}: PRECIO VISIBLE en página nueva {precios[:3]} — el cuerpo va sin precio (usa 'cotización gratis'); el priceRange solo en JSON-LD.")

    # 2) testimonios VISIBLES inventados (tarjetas "Lo que dicen nuestros clientes").
    # OJO: NO se bloquea el aggregateRating del JSON-LD — eso es estándar de la plantilla
    # en TODO el sitio (seo-104, decisión aparte); aquí solo lo VISIBLE inventado en el cuerpo.
    if re.search(r'class="[^"]*testimonial', body, re.I):
        viol.append(f"{f}: TESTIMONIO VISIBLE en página nueva — no inventar reseñas de clientes (seo-104).")

if viol:
    print("❌ CANDADO PÁGINA NUEVA: bloqueado por:")
    for v in viol:
        print("   -", v)
    sys.exit(1)

print(f"✅ Candado página nueva OK ({revisadas} página(s) nueva(s) revisada(s); sin precio visible ni reseñas inventadas).")
sys.exit(0)
