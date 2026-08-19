#!/usr/bin/env python3
"""Ejecuta `codex login status` con timeout de reloj de pared."""
import os
import signal
import subprocess
import sys
import time


TIMEOUT_EXIT = 124


def comprobar(binary, timeout_seconds):
    try:
        proc = subprocess.Popen(
            [binary, "login", "status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
    except OSError as exc:
        print("No se pudo iniciar codex login status: %s" % exc, file=sys.stderr)
        return 127

    deadline = time.time() + timeout_seconds
    while proc.poll() is None and time.time() < deadline:
        time.sleep(0.1)

    timed_out = proc.poll() is None
    if timed_out:
        print(
            "codex login status excedió %ss; termino el preflight para liberar el lock."
            % timeout_seconds,
            file=sys.stderr,
        )
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=2)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    output, _ = proc.communicate()
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    return TIMEOUT_EXIT if timed_out else proc.returncode


def main(argv):
    if len(argv) != 3:
        print("uso: codex-login-preflight.py CODEX_BIN TIMEOUT_SEGUNDOS", file=sys.stderr)
        return 2
    try:
        timeout = float(argv[2])
    except ValueError:
        return 2
    if timeout <= 0:
        return 2
    return comprobar(argv[1], timeout)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
