#!/usr/bin/env python3
"""Contratos de idempotencia del driver diario."""
import importlib.util
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "detectar-publicacion.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("detectar_publicacion", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class EstadoPublicacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_solo_reintenta_si_remote_y_local_siguen_iguales(self):
        self.assertEqual(
            self.mod.clasificar("r1", "r1", "l1", "l1"),
            ("seguro_reintentar", 0),
        )

    def test_remote_distinto_bloquea_reintento(self):
        self.assertEqual(
            self.mod.clasificar("r1", "r2", "l1", "l2"),
            ("origin_cambio", 10),
        )

    def test_main_local_distinta_bloquea_aunque_remote_no_cambie(self):
        self.assertEqual(
            self.mod.clasificar("r1", "r1", "l1", "l2"),
            ("main_local_cambio", 11),
        )

    def test_remote_no_verificable_bloquea_reintento(self):
        self.assertEqual(
            self.mod.clasificar("r1", "", "l1", "l1"),
            ("no_verificable", 12),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
