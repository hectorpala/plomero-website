#!/usr/bin/env python3
"""Contrato de exclusión mutua entre los agentes que escriben el repositorio."""
import os
import re
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(relative):
    with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
        return fh.read()


class SharedPipelineLock(unittest.TestCase):
    def test_diaria_y_meta_comparten_el_mismo_lock(self):
        diaria = _read(".pipeline/crecer-diario.sh")
        meta = _read(".pipeline/meta-semanal.sh")
        expected = 'LOCK_DIR="/tmp/plomero-mantener-sitio.lock"'
        self.assertIn(expected, diaria)
        self.assertIn(expected, meta)
        self.assertNotIn("/tmp/plomero-meta.lock", meta)

    def test_meta_adquiere_lock_atomicamente_antes_de_codex(self):
        meta = _read(".pipeline/meta-semanal.sh")
        acquire = meta.index('if ! mkdir "$LOCK_DIR" 2>/dev/null; then')
        owner = meta.index('echo "$$" > "$LOCK_DIR/pid"', acquire)
        codex = meta.index('"$CODEX_BIN" exec', owner)
        self.assertLess(acquire, owner)
        self.assertLess(owner, codex)

    def test_meta_no_borra_directamente_un_lock_en_disputa(self):
        meta = _read(".pipeline/meta-semanal.sh")
        self.assertIsNone(re.search(r'rm -rf "\$LOCK_DIR"\s*;', meta))
        self.assertIn('mv "$LOCK_DIR" "$LOCK_DIR.stale.$$"', meta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
