#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checker DETERMINISTA: PARIDAD de reglas de plantilla en la familia de páginas de servicio.

Caza la clase de regresión movil-502 / movil-701 / movil-801: un fix de <style> inline
(o de estructura) se aplica a UNA página de servicio y no se propaga a sus hermanas del
mismo esqueleto -> la mayoría se queda sin el fix hasta que alguien lo nota a ojo.

Modelo: un REGISTRO de reglas obligatorias. Cada regla dice «si la página CONTIENE
<disparador>, DEBE contener <patrón>». Al añadir un fix nuevo a la familia, se agrega
una línea aquí y el pipeline vigila la paridad solo, para siempre.

Emite el contrato común {"hallazgos":[...]} — check-infra.mjs lo recoge sin tocar nada.
Sin argumentos.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICIOS_GLOB = os.path.join(ROOT, "servicios", "*", "index.html")

# (id, categoría, disparador-regex, patrón-obligatorio-regex, descripción)
REGLAS_FAMILIA = [
    (
        "familia-about-text-tap",
        "movil",
        re.compile(r"\.about-text\b"),
        re.compile(r"\.about-text\s+a\s*\{[^}]*display\s*:\s*inline-block", re.S),
        "Página de servicio con .about-text SIN la regla de tap-target ~44px "
        "(@media(max-width:768px){.about-text a{display:inline-block;padding:.6rem 0}}) — "
        "regresión de la familia movil-502/701/801.",
    ),
    # Añadir aquí futuras reglas de familia: (id, categoría, disparador, obligatorio, desc)
]


def main():
    hallazgos = []
    seq = 0
    for full in sorted(glob.glob(SERVICIOS_GLOB)):
        try:
            html = open(full, encoding="utf-8").read()
        except OSError:
            continue
        rel = os.path.relpath(full, ROOT)
        for rid, cat, disparador, obligatorio, desc in REGLAS_FAMILIA:
            if disparador.search(html) and not obligatorio.search(html):
                seq += 1
                hallazgos.append({
                    "id": f"{rid}-{seq:03d}",
                    "archivo": rel,
                    "linea": 0,
                    "severidad": "media",
                    "categoria": cat,
                    "descripcion": desc,
                    "fix_sugerido": "Copiar la regla ya probada desde una página hermana (mismo esqueleto) a esta página; verificar headless a 375px que el tap-target quede >=44px.",
                })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
