#!/usr/bin/env python3
"""Pruebas del preflight acotado de autenticación de Codex."""
import importlib.util
import os
import stat
import tempfile
import time
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "codex-login-preflight.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("codex_login_preflight", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _fake(directory, body):
    path = os.path.join(directory, "fake-codex")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\n" + body + "\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
    return path


class CodexLoginPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_propaga_exito(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = _fake(tmp, 'test "$1" = login && test "$2" = status')
            self.assertEqual(self.mod.comprobar(binary, 1), 0)

    def test_propaga_fallo_de_autenticacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = _fake(tmp, "exit 7")
            self.assertEqual(self.mod.comprobar(binary, 1), 7)

    def test_corta_comando_colgado(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = _fake(tmp, "sleep 5")
            start = time.time()
            self.assertEqual(self.mod.comprobar(binary, 0.2), self.mod.TIMEOUT_EXIT)
            self.assertLess(time.time() - start, 2.5)

    def test_los_tres_drivers_usan_el_preflight_acotado(self):
        for relative in (
            ".pipeline/crecer-diario.sh",
            ".pipeline/meta-semanal.sh",
            ".pipeline/maraton.sh",
        ):
            with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
                source = fh.read()
            self.assertIn("codex-login-preflight.py", source)
            self.assertIn("AUTH_TIMEOUT_SECONDS=30", source)
            self.assertNotIn('"$CODEX_BIN" login status', source)
            self.assertNotIn('"$CODEX_CMD" login status', source)

    def test_maraton_conserva_el_codigo_real_del_preflight(self):
        with open(os.path.join(ROOT, ".pipeline", "maraton.sh"), encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn('|| AUTH_RC=$?', source)
        self.assertIn('if [ "$AUTH_RC" -ne 0 ]', source)
        self.assertNotIn('if ! python3 "$AUTH_CHECK"', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
