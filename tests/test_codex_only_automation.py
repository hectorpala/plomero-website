#!/usr/bin/env python3
"""Evita que una ruta heredada vuelva a ejecutar Claude por accidente."""
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(relative):
    with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
        return fh.read()


class CodexOnlyAutomation(unittest.TestCase):
    def test_script_heredado_delega_al_driver_codex(self):
        source = _read(".pipeline/deprecados/mantener-diario.sh")
        self.assertIn(".pipeline/crecer-diario.sh", source)
        self.assertIn('exec /bin/bash "$DRIVER"', source)
        self.assertNotIn("RUTA_CLAUDE", source)
        self.assertNotIn("/bin/claude", source.lower())
        self.assertNotIn("--model sonnet", source)

    def test_respaldo_ya_no_describe_a_claude_como_principal(self):
        source = _read(".pipeline/respaldo-codex-prompt.txt")
        for stale in (
            "Claude Code falló",
            "corrida normal de Claude",
            "pendiente para Claude",
            "Claude alcanzó su límite",
        ):
            self.assertNotIn(stale, source)
        self.assertIn("corrida diaria completa de Codex", source)

    def test_driver_vigente_usa_codex_exec_no_interactivo(self):
        source = _read(".pipeline/crecer-diario.sh")
        self.assertIn('"$CODEX_BIN" exec', source)
        self.assertIn("--json", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
