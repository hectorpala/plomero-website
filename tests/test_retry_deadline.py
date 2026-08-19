#!/usr/bin/env python3
"""Contrato del deadline de reloj de pared del driver diario."""
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, ".pipeline", "crecer-diario.sh")


class RetryDeadlineContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DRIVER, encoding="utf-8") as fh:
            cls.source = fh.read()

    def test_deadline_es_de_tres_horas_desde_inicio(self):
        start = self.source.index("RUN_START=$(date +%s)")
        deadline = self.source.index("RETRY_DEADLINE=$((RUN_START + 3 * 3600))")
        loop = self.source.index('for attempt in $(seq 1 "$MAX_ATTEMPTS")')
        self.assertLess(start, deadline)
        self.assertLess(deadline, loop)

    def test_sleep_no_puede_continuar_con_reintento_atrasado(self):
        sleep = self.source.index('sleep "$WAIT"')
        guard = self.source.index(
            'if [ "$(date +%s)" -gt "$RETRY_DEADLINE" ]; then', sleep
        )
        mark = self.source.index('FAIL_KIND="deadline_reintentos"', guard)
        stop = self.source.index("break", mark)
        loop_end = self.source.index("done", sleep)
        self.assertLess(sleep, guard)
        self.assertLess(guard, mark)
        self.assertLess(mark, stop)
        self.assertLess(stop, loop_end)

    def test_correo_explica_cancelacion_por_deadline(self):
        self.assertIn("deadline_reintentos)", self.source)
        self.assertIn("fuera de la ventana segura de reintentos", self.source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
