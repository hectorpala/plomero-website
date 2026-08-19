#!/usr/bin/env python3
"""Contrato del timeout del meta-agente que conserva el lock compartido."""
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, ".pipeline", "meta-semanal.sh")


class MetaTimeoutContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(META, encoding="utf-8") as fh:
            cls.source = fh.read()

    def test_timeout_esta_acotado_y_usa_reloj_de_pared(self):
        self.assertIn("META_TIMEOUT_MIN=45", self.source)
        self.assertIn(
            "META_DEADLINE=$((RUN_START + META_TIMEOUT_MIN * 60))",
            self.source,
        )
        self.assertIn('"$(date +%s)" -ge "$META_DEADLINE"', self.source)

    def test_codex_corre_en_background_y_watchdog_lo_termina(self):
        codex = self.source.index('"$CODEX_BIN" exec')
        pid = self.source.index("META_PID=$!", codex)
        terminate = self.source.index('kill "$META_PID"', pid)
        reap = self.source.index('wait "$META_PID"', terminate)
        self.assertLess(codex, pid)
        self.assertLess(pid, terminate)
        self.assertLess(terminate, reap)

    def test_timeout_no_puede_contar_como_exito(self):
        success_gate = self.source.index('if [ "$META_RC" -eq 0 ]')
        timeout_guard = self.source.index(
            '&& ! grep -q "META_TIMEOUT ${META_TIMEOUT_MIN}min" "$LOG"',
            success_gate,
        )
        completed = self.source.index('&& grep -q \'"type":"turn.completed"\'', timeout_guard)
        self.assertLess(success_gate, timeout_guard)
        self.assertLess(timeout_guard, completed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
