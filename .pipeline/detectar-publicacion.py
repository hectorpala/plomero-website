#!/usr/bin/env python3
# infra:utilidad-no-sensor (requiere subcomando; no emite {hallazgos})
"""Detecta si una corrida fallida pudo haber publicado antes de reintentarse.

Exit codes de ``check``:
  0  origin/main y main local siguen iguales: es seguro reintentar.
  10 origin/main cambió: una publicación pudo completarse.
  11 origin/main no cambió, pero main local sí: hay una integración incompleta.
  12 no se pudo consultar origin/main: no es seguro asumir que no se publicó.
"""
import argparse
import json
import os
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _git(args, timeout=25):
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        r = subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True,
            timeout=timeout, env=env,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def remote_main():
    out = _git([
        "-c", "credential.interactive=never", "ls-remote", "origin", "refs/heads/main"
    ])
    return out.split()[0] if out else ""


def local_main():
    return _git(["rev-parse", "refs/heads/main"], timeout=10)


def tracking_main():
    return _git(["rev-parse", "refs/remotes/origin/main"], timeout=10)


def clasificar(remote_antes, remote_ahora, local_antes, local_ahora):
    if not remote_antes or not remote_ahora:
        return "no_verificable", 12
    if remote_ahora != remote_antes:
        return "origin_cambio", 10
    if not local_antes or not local_ahora:
        return "no_verificable", 12
    if local_ahora != local_antes:
        return "main_local_cambio", 11
    return "seguro_reintentar", 0


def cmd_baseline():
    # La lectura remota es preferible. El tracking local es un fallback conservador: si
    # estaba atrasado, el chequeo posterior puede detener un reintento innecesariamente,
    # pero nunca autoriza un duplicado.
    sha = remote_main() or tracking_main()
    if not sha:
        return 2
    print(sha)
    return 0


def cmd_check(args):
    remote_ahora = remote_main()
    local_ahora = local_main()
    estado, rc = clasificar(args.remote_antes, remote_ahora, args.local_antes, local_ahora)
    print(json.dumps({
        "estado": estado,
        "remote_antes": args.remote_antes or None,
        "remote_ahora": remote_ahora or None,
        "local_antes": args.local_antes or None,
        "local_ahora": local_ahora or None,
        "seguro_reintentar": rc == 0,
    }, ensure_ascii=False, separators=(",", ":")))
    return rc


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("baseline")
    check = sub.add_parser("check")
    check.add_argument("--remote-antes", default="")
    check.add_argument("--local-antes", default="")
    args = p.parse_args()
    return cmd_baseline() if args.cmd == "baseline" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
