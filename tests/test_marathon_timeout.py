#!/usr/bin/env python3
"""Pruebas del deadline duro por pasada del maratón."""
import importlib.util
import os
import stat
import tempfile
import time
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "ejecutar-hasta.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("ejecutar_hasta", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _fake(directory, body):
    path = os.path.join(directory, "fake-command")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\n" + body + "\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
    return path


class MarathonTimeout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_propaga_exito(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = _fake(tmp, "exit 0")
            self.assertEqual(self.mod.ejecutar(time.time() + 2, [command]), 0)

    def test_propaga_fallo(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = _fake(tmp, "exit 9")
            self.assertEqual(self.mod.ejecutar(time.time() + 2, [command]), 9)

    def test_termina_comando_colgado(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = _fake(tmp, "sleep 5")
            start = time.time()
            self.assertEqual(
                self.mod.ejecutar(time.time() + 0.2, [command]),
                self.mod.TIMEOUT_EXIT,
            )
            self.assertLess(time.time() - start, 2.5)

    def test_maraton_limita_cada_pasada_y_respeta_el_fin_total(self):
        with open(os.path.join(ROOT, ".pipeline", "maraton.sh"), encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn("MARATON_PASS_TIMEOUT_SECONDS:-1200", source)
        self.assertIn('PASS_DEADLINE=$((PASS_START + PASS_TIMEOUT_SECONDS))', source)
        self.assertIn('[ "$PASS_DEADLINE" -gt "$END" ] && PASS_DEADLINE="$END"', source)
        self.assertIn('python3 "$DEADLINE_RUNNER" "$PASS_DEADLINE" "$CODEX_BIN" exec', source)
        self.assertIn('if [ "$PASS_RC" -eq 124 ]', source)
        self.assertNotIn('"$CODEX_BIN" exec --cd', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
