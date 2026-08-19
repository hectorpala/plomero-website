#!/usr/bin/env python3
"""Contratos de seguridad del publicador autónomo."""
import importlib.util
import os
import subprocess
import tempfile
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
        self.assertNotIn('["git", "add", "-A"]', fuente)

    def test_bloquea_archivo_ajeno_sin_preparar_y_preserva_staging(self):
        """Un untracked ajeno no se agrega ni se publica junto con un cambio preparado."""
        with tempfile.TemporaryDirectory() as repo:
            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=repo, text=True, capture_output=True, check=True
                )

            git("init", "-q")
            git("config", "user.name", "Prueba")
            git("config", "user.email", "prueba@example.invalid")
            base = os.path.join(repo, "base.txt")
            with open(base, "w", encoding="utf-8") as archivo:
                archivo.write("base\n")
            git("add", "--", "base.txt")
            git("commit", "-qm", "base")
            git("branch", "-M", "main")

            with open(base, "a", encoding="utf-8") as archivo:
                archivo.write("cambio permitido\n")
            git("add", "--", "base.txt")
            with open(os.path.join(repo, "ajeno.txt"), "w", encoding="utf-8") as archivo:
                archivo.write("no publicar\n")

            anterior = self.crecer.ROOT
            self.crecer.ROOT = repo
            try:
                with self.assertRaises(SystemExit) as salida:
                    self.crecer.cmd_publicar(["fix: prueba"])
            finally:
                self.crecer.ROOT = anterior

            self.assertIn("git add -A", str(salida.exception))
            self.assertEqual(git("diff", "--cached", "--name-only").stdout.strip(), "base.txt")
            self.assertEqual(git("ls-files", "--others", "--exclude-standard").stdout.strip(), "ajeno.txt")
            self.assertEqual(git("branch", "--show-current").stdout.strip(), "main")
            self.assertEqual(git("branch", "--list", "auto/*").stdout.strip(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
