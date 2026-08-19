#!/usr/bin/env python3
"""Pruebas del candado de secretos usado por pre-push."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(ROOT, ".pipeline", "check-secretos.sh")
HOOK = os.path.join(ROOT, ".pipeline", "hooks", "pre-push")


class SecretGate(unittest.TestCase):
    def test_current_only_ignora_historial_pero_bloquea_secreto_actual(self):
        with tempfile.TemporaryDirectory() as repo:
            pipe = os.path.join(repo, ".pipeline")
            os.makedirs(pipe)
            shutil.copyfile(CHECKER, os.path.join(pipe, "check-secretos.sh"))

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=repo, text=True, capture_output=True, check=True
                )

            def scan():
                return subprocess.run(
                    ["/bin/bash", ".pipeline/check-secretos.sh", "--current-only"],
                    cwd=repo, text=True, capture_output=True,
                )

            git("init", "-q")
            git("config", "user.name", "Prueba")
            git("config", "user.email", "prueba@example.invalid")
            git("add", "--", ".pipeline/check-secretos.sh")
            git("commit", "-qm", "checker")

            # El secreto existió en el historial, pero ya no está en el árbol actual.
            token = "sk-" + ("A" * 24)
            historial = os.path.join(repo, "viejo.txt")
            with open(historial, "w", encoding="utf-8") as archivo:
                archivo.write(token + "\n")
            git("add", "--", "viejo.txt")
            git("commit", "-qm", "secreto histórico de prueba")
            os.remove(historial)
            git("add", "--", "viejo.txt")
            git("commit", "-qm", "retira secreto")

            sano = scan()
            self.assertEqual(sano.returncode, 0, sano.stdout + sano.stderr)
            self.assertEqual(json.loads(sano.stdout)["hallazgos"], [])

            with open(os.path.join(repo, "actual.txt"), "w", encoding="utf-8") as archivo:
                archivo.write(token + "\n")
            bloqueado = scan()
            self.assertEqual(bloqueado.returncode, 2, bloqueado.stdout + bloqueado.stderr)
            hallazgos = json.loads(bloqueado.stdout)["hallazgos"]
            self.assertTrue(any(h["archivo"] == "actual.txt" for h in hallazgos))

    def test_hook_ejecuta_secretos_antes_del_escape_skip_gate(self):
        with open(HOOK, encoding="utf-8") as archivo:
            fuente = archivo.read()
        llamada = fuente.index('"$SECRET_CHECK" --current-only')
        escape = fuente.index('if [ "${SKIP_GATE:-0}" = "1" ]')
        self.assertLess(llamada, escape)


if __name__ == "__main__":
    unittest.main(verbosity=2)
