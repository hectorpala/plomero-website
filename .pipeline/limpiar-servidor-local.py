#!/usr/bin/env python3
"""Termina solo un http.server huérfano cuyo cwd sea este repositorio."""
import os
import re
import signal
import subprocess
import sys


def pertenece_al_repo(command, cwd, repo, port):
    if not cwd or not repo:
        return False
    try:
        mismo_cwd = os.path.realpath(cwd) == os.path.realpath(repo)
    except (OSError, TypeError):
        return False
    servidor = re.search(r"(?:^|\s)http\.server(?:\s|$)", command or "")
    puerto = re.search(r"(?:^|\s)%s(?:\s|$)" % re.escape(str(port)), command or "")
    return bool(mismo_cwd and servidor and puerto)


def _run(args):
    return subprocess.run(args, capture_output=True, text=True, check=False)


def _pids_en_puerto(port):
    result = _run([
        "/usr/sbin/lsof", "-nP", "-iTCP:%s" % port, "-sTCP:LISTEN", "-t"
    ])
    if result.returncode not in (0, 1):
        raise RuntimeError("lsof no pudo inspeccionar el puerto")
    return [line.strip() for line in result.stdout.splitlines() if line.strip().isdigit()]


def _cwd(pid):
    result = _run(["/usr/sbin/lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"])
    if result.returncode != 0:
        return ""
    for line in result.stdout.splitlines():
        if line.startswith("n"):
            return line[1:]
    return ""


def _command(pid):
    result = _run(["/bin/ps", "-p", str(pid), "-o", "command="])
    return result.stdout.strip() if result.returncode == 0 else ""


def _leer_pid(ruta):
    try:
        with open(ruta, encoding="ascii") as fh:
            value = fh.read().strip()
    except FileNotFoundError:
        return None
    return int(value) if value.isdigit() else None


def _olvidar_pid(ruta):
    try:
        os.unlink(ruta)
    except FileNotFoundError:
        pass


def main(argv):
    if len(argv) != 4 or not argv[2].isdigit():
        print("uso: limpiar-servidor-local.py REPO PUERTO ARCHIVO_PID", file=sys.stderr)
        return 2
    repo, port, pid_file = argv[1], int(argv[2]), argv[3]
    pid = _leer_pid(pid_file)
    if pid is None:
        # Sin comprobante de propiedad no se mata nada, aunque el puerto esté ocupado.
        return 0

    listeners = set(_pids_en_puerto(port))
    if str(pid) not in listeners:
        print("PID registrado %s ya no escucha en %s; retiro marcador obsoleto." % (pid, port))
        _olvidar_pid(pid_file)
        return 0

    command, cwd = _command(pid), _cwd(pid)
    if pertenece_al_repo(command, cwd, repo, port):
        try:
            os.kill(pid, signal.SIGTERM)
            print("Servidor local huérfano del repo terminado (pid %s, puerto %s)." % (pid, port))
        except ProcessLookupError:
            print("El servidor registrado ya había terminado (pid %s)." % pid)
    else:
        print("El PID registrado ahora pertenece a un proceso ajeno (pid %s); no se toca." % pid)
    _olvidar_pid(pid_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
