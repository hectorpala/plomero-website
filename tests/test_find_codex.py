#!/usr/bin/env python3
"""Pruebas del descubrimiento compartido del ejecutable de Codex."""
import importlib.util
import os
import stat
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "encontrar-codex.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("encontrar_codex", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _executable(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nexit 0\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)


class FindCodex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_prefiere_instalacion_local_estable(self):
        with tempfile.TemporaryDirectory() as home:
            local = os.path.join(home, ".local", "bin", "codex")
            path_bin = os.path.join(home, "path", "codex")
            _executable(local)
            _executable(path_bin)
            self.assertEqual(self.mod.encontrar(home, os.path.dirname(path_bin)), local)

    def test_usa_path_si_no_hay_instalacion_local(self):
        with tempfile.TemporaryDirectory() as home:
            binary = os.path.join(home, "path", "codex")
            _executable(binary)
            self.assertEqual(self.mod.encontrar(home, os.path.dirname(binary)), binary)

    def test_usa_extension_vscode_como_ultimo_respaldo(self):
        with tempfile.TemporaryDirectory() as home:
            binary = os.path.join(
                home,
                ".vscode",
                "extensions",
                "openai.chatgpt-prueba-darwin-arm64",
                "bin",
                "macos-aarch64",
                "codex",
            )
            _executable(binary)
            self.assertEqual(self.mod.encontrar(home, ""), binary)

    def test_devuelve_vacio_si_no_existe_codex(self):
        with tempfile.TemporaryDirectory() as home:
            self.assertEqual(self.mod.encontrar(home, ""), "")

    def test_los_tres_drivers_usan_el_mismo_resolver(self):
        for relative in (
            ".pipeline/crecer-diario.sh",
            ".pipeline/meta-semanal.sh",
            ".pipeline/maraton.sh",
        ):
            with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
                source = fh.read()
            self.assertIn(".pipeline/encontrar-codex.py", source)
            self.assertIn('CODEX_BIN=$(python3 "$CODEX_FINDER"', source)
            self.assertNotIn('CODEX_BIN="/Users/openclaw/.local/bin/codex"', source)

    def test_maraton_conserva_override_explicito_para_pruebas(self):
        with open(os.path.join(ROOT, ".pipeline", "maraton.sh"), encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn('if [ -n "${MARATON_CODEX:-}" ]', source)
        self.assertIn('CODEX_BIN="$MARATON_CODEX"', source)
        self.assertNotIn("CODEX_CMD=", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
