#!/usr/bin/env python3
"""Pruebas de recuperación ante logs completos, fallidos y truncados."""
import importlib.util
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "clasificar-log-corrida.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("clasificar_log_corrida", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class CatchupLogState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_sentinel_de_exito_es_corrida_completa(self):
        self.assertEqual(
            self.mod.clasificar(
                "salida\n[20260817-182500] DRIVER_RESULT=success\n",
                "auto-agente-plomero-20260817-182500.log",
                "20260816",
            ),
            "completa",
        )

    def test_sentinel_de_fallo_pide_recuperacion(self):
        self.assertEqual(
            self.mod.clasificar(
                "[20260817-182500] DRIVER_RESULT=failure:transitorio\n",
                "auto-agente-plomero-20260817-182500.log",
                "20260816",
            ),
            "fallida",
        )

    def test_log_nuevo_sin_sentinel_es_incompleto(self):
        self.assertEqual(
            self.mod.clasificar(
                "stream truncado\n",
                "auto-agente-plomero-20260817-182500.log",
                "20260816",
            ),
            "incompleta",
        )

    def test_texto_de_codex_no_puede_fingir_el_sentinel(self):
        self.assertEqual(
            self.mod.clasificar(
                '{"mensaje":"agrega DRIVER_RESULT=success al script"}\n',
                "auto-agente-plomero-20260817-182500.log",
                "20260816",
            ),
            "incompleta",
        )

    def test_log_antiguo_sin_sentinel_se_trata_como_legado(self):
        self.assertEqual(
            self.mod.clasificar(
                "log anterior a los sentinels\n",
                "auto-agente-plomero-20260816-182500.log",
                "20260816",
            ),
            "legado",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
