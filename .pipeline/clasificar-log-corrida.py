#!/usr/bin/env python3
"""Clasifica el cierre del log diario sin confundir frescura con éxito."""
import os
import re
import sys


SENTINEL = re.compile(
    r"^\[[^\]\r\n]+\] DRIVER_RESULT=(success|failure(?::[^\s]+)?)\s*$",
    re.MULTILINE,
)
DAY_IN_NAME = re.compile(r"(?:auto-agente-plomero-|run-)(20\d{6})-")


def clasificar(texto, nombre, ultimo_dia_exitoso=""):
    resultados = SENTINEL.findall(texto)
    if resultados:
        return "completa" if resultados[-1] == "success" else "fallida"

    match = DAY_IN_NAME.search(os.path.basename(nombre))
    dia_log = match.group(1) if match else ""
    if dia_log and ultimo_dia_exitoso and dia_log <= ultimo_dia_exitoso:
        return "legado"
    return "incompleta"


def main(argv):
    if len(argv) not in (2, 3):
        print("incompleta")
        return 0
    ruta = argv[1]
    ultimo = argv[2] if len(argv) == 3 else ""
    try:
        with open(ruta, encoding="utf-8", errors="replace") as fh:
            texto = fh.read()
    except OSError:
        print("incompleta")
        return 0
    print(clasificar(texto, ruta, ultimo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
