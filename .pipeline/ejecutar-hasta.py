#!/usr/bin/env python3
"""Ejecuta un comando hasta un deadline epoch y termina todo su grupo al vencer."""
import os
import signal
import subprocess
import sys
import time


TIMEOUT_EXIT = 124


def ejecutar(deadline, comando, poll_seconds=0.1, grace_seconds=2):
    try:
        proc = subprocess.Popen(comando, start_new_session=True)
    except OSError as exc:
        print("No se pudo iniciar el comando: %s" % exc, file=sys.stderr)
        return 127

    while proc.poll() is None:
        restante = deadline - time.time()
        if restante <= 0:
            break
        time.sleep(min(poll_seconds, restante))

    if proc.poll() is not None:
        return proc.returncode

    print(
        "DEADLINE_TIMEOUT: termino el proceso y sus hijos para liberar el lock.",
        file=sys.stderr,
    )
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
    return TIMEOUT_EXIT


def main(argv):
    if len(argv) < 3:
        print("uso: ejecutar-hasta.py DEADLINE_EPOCH COMANDO [ARG ...]", file=sys.stderr)
        return 2
    try:
        deadline = float(argv[1])
    except ValueError:
        print("deadline inválido", file=sys.stderr)
        return 2
    return ejecutar(deadline, argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
