#!/usr/bin/env python3
"""Contrato del timeout real de cada intento de la corrida diaria."""
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, ".pipeline", "crecer-diario.sh")


class DailyTimeoutContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DRIVER, encoding="utf-8") as fh:
            cls.source = fh.read()

    def test_deadline_de_intento_usa_reloj_de_pared(self):
        self.assertIn(
            "ATTEMPT_DEADLINE=$(( $(date +%s) + TIMEOUT_MIN * 60 ))",
            self.source,
        )
        self.assertIn('"$(date +%s)" -ge "$ATTEMPT_DEADLINE"', self.source)
        self.assertNotIn("sleep $((TIMEOUT_MIN * 60))", self.source)

    def test_watchdog_termina_y_recolecta_solo_el_pid_de_codex(self):
        deadline = self.source.index('"$(date +%s)" -ge "$ATTEMPT_DEADLINE"')
        term = self.source.index('kill "$CPID"', deadline)
        still_alive = self.source.index('kill -0 "$CPID"', term)
        force = self.source.index('kill -9 "$CPID"', still_alive)
        reap = self.source.index('wait "$WPID"', force)
        self.assertLess(deadline, term)
        self.assertLess(term, still_alive)
        self.assertLess(still_alive, force)
        self.assertLess(force, reap)

    def test_timeout_no_puede_contar_como_salida_exitosa(self):
        wait_success = self.source.index('if wait "$CPID"; then')
        timeout_guard = self.source.index(
            'if attempt_has_fixed "TIMEOUT ${TIMEOUT_MIN}min"; then',
            wait_success,
        )
        success = self.source.index("CODEX_OK=1", timeout_guard)
        self.assertLess(wait_success, timeout_guard)
        self.assertLess(timeout_guard, success)


if __name__ == "__main__":
    unittest.main(verbosity=2)
