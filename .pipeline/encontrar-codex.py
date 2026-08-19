#!/usr/bin/env python3
"""Encuentra un ejecutable de Codex válido para drivers lanzados por launchd."""
import glob
import os
import shutil
import sys


def _ejecutable(path):
    return bool(path and os.path.isfile(path) and os.access(path, os.X_OK))


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        # Una extensión puede desaparecer mientras VS Code se actualiza.
        return -1


def encontrar(home, path_env=None):
    candidatos = [os.path.join(home, ".local", "bin", "codex")]
    por_path = shutil.which("codex", path=path_env)
    if por_path:
        candidatos.append(por_path)

    extensiones = glob.glob(
        os.path.join(
            home,
            ".vscode",
            "extensions",
            "openai.chatgpt-*",
            "bin",
            "macos-*",
            "codex",
        )
    )
    extensiones.sort(key=_mtime, reverse=True)
    candidatos.extend(extensiones)

    vistos = set()
    for path in candidatos:
        real = os.path.realpath(path) if path else ""
        if real in vistos:
            continue
        vistos.add(real)
        if _ejecutable(path):
            return path
    return ""


def main():
    path = encontrar(os.path.expanduser("~"), os.environ.get("PATH"))
    if not path:
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
