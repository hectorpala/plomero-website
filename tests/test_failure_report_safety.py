#!/usr/bin/env python3
"""Contratos para no alterar el parte anterior cuando la corrida falla."""
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, ".pipeline", "crecer-diario.sh")


class FailureReportSafetyContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DRIVER, encoding="utf-8") as fh:
            cls.source = fh.read()

    def test_check_parte_solo_corre_tras_exito_y_frescura(self):
        freshness = self.source.index("# CANDADO DE FRESCURA")
        gate = self.source.index(
            'if [ "${CODEX_OK:-0}" = 1 ] && [ -f "$PARTE" ]; then',
            freshness,
        )
        checker = self.source.index('check-parte.py" "$PARTE"', gate)
        failure_email = self.source.index("# Parte por email", checker)

        self.assertLess(freshness, gate)
        self.assertLess(gate, checker)
        self.assertLess(checker, failure_email)

    def test_no_regresa_al_guard_incondicional(self):
        self.assertNotIn('if [ -f "$PARTE" ]; then', self.source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
