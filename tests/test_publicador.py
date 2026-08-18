#!/usr/bin/env python3
"""Contratos de seguridad del publicador autónomo."""
import importlib.util
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, "scripts", "crecer.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("crecer_publicador", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class PublicadorSeguro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.crecer = _cargar()

    def test_reutiliza_rama_automatica(self):
        rama, reusa = self.crecer._rama_publicacion("auto/diario-20260817", "marca")
        self.assertEqual(rama, "auto/diario-20260817")
        self.assertTrue(reusa)

    def test_crea_rama_solo_fuera_de_auto(self):
        rama, reusa = self.crecer._rama_publicacion("main", "20260817-210000")
        self.assertEqual(rama, "auto/crecer-20260817-210000")
        self.assertFalse(reusa)

    def test_no_reintroduce_reset_destructivo_ni_atribucion_claude(self):
        with open(RUTA, encoding="utf-8") as archivo:
            fuente = archivo.read()
        self.assertNotIn('git("reset", "--hard"', fuente)
        self.assertNotIn("Claude Opus", fuente)


if __name__ == "__main__":
    unittest.main(verbosity=2)
