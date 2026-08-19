#!/usr/bin/env python3
"""Encuentra un ejecutable de Node válido para drivers lanzados por launchd."""
import os
import shutil


def _ejecutable(path):
    return bool(path and os.path.isfile(path) and os.access(path, os.X_OK))


def encontrar(path_env=None, respaldos=None):
    candidatos = []
    por_path = shutil.which("node", path=path_env)
    if por_path:
        candidatos.append(por_path)
    if respaldos is None:
        respaldos = (
            "/usr/local/bin/node",
            "/opt/homebrew/bin/node",
            "/usr/bin/node",
        )
    candidatos.extend(respaldos)

    vistos = set()
    for path in candidatos:
        real = os.path.realpath(path) if path else ""
        if not real or real in vistos:
            continue
        vistos.add(real)
        if _ejecutable(path):
            return path
    return ""


def main():
    path = encontrar(os.environ.get("PATH"))
    if not path:
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
