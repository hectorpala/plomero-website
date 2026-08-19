#!/usr/bin/env python3
"""Pruebas de alcance para la limpieza defensiva del puerto 8080."""
import importlib.util
import os
import tempfile
import unittest
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "limpiar-servidor-local.py")
DRIVER = os.path.join(ROOT, ".pipeline", "crecer-diario.sh")
PROMPT = os.path.join(ROOT, ".pipeline", "crecer-diario-prompt.txt")


def _cargar():
    spec = importlib.util.spec_from_file_location("limpiar_servidor_local", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class LocalServerCleanup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_acepta_http_server_del_repo_y_puerto_exactos(self):
        self.assertTrue(
            self.mod.pertenece_al_repo(
                "python3 -m http.server 8080", ROOT, ROOT, 8080
            )
        )

    def test_no_toca_servidor_de_otro_proyecto(self):
        self.assertFalse(
            self.mod.pertenece_al_repo(
                "python3 -m http.server 8080", "/tmp/otro", ROOT, 8080
            )
        )

    def test_no_toca_otro_programa_que_use_8080(self):
        self.assertFalse(
            self.mod.pertenece_al_repo("node app.js --port 8080", ROOT, ROOT, 8080)
        )

    def test_cwd_no_verificable_falla_cerrado(self):
        self.assertFalse(
            self.mod.pertenece_al_repo(
                "python3 -m http.server 8080", "", ROOT, 8080
            )
        )

    def test_no_acepta_puerto_con_coincidencia_parcial(self):
        self.assertFalse(
            self.mod.pertenece_al_repo(
                "python3 -m http.server 80801", ROOT, ROOT, 8080
            )
        )

    def test_driver_no_regresa_al_pkill_global(self):
        with open(DRIVER, encoding="utf-8") as fh:
            source = fh.read()
        self.assertNotIn('pkill -f "http.server 8080"', source)
        self.assertIn(
            'limpiar-servidor-local.py "$PWD" 8080 /tmp/plomero-http-server.pid',
            source,
        )

    def test_prompt_registra_y_retira_el_pid_del_servidor(self):
        with open(PROMPT, encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn("echo $! > /tmp/plomero-http-server.pid", source)
        self.assertIn("Apaga exclusivamente el servidor registrado", source)
        self.assertIn("nunca\nuses `pkill`", source)

    def test_sin_pid_registrado_no_mata_ningun_listener(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_file = os.path.join(tmp, "ausente.pid")
            with mock.patch.object(self.mod, "_pids_en_puerto") as listeners, \
                    mock.patch.object(self.mod.os, "kill") as kill:
                rc = self.mod.main(["limpiar", ROOT, "8080", pid_file])
            self.assertEqual(rc, 0)
            listeners.assert_not_called()
            kill.assert_not_called()

    def test_solo_mata_el_pid_registrado_y_verificado(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_file = os.path.join(tmp, "server.pid")
            with open(pid_file, "w", encoding="ascii") as fh:
                fh.write("123")
            with mock.patch.object(self.mod, "_pids_en_puerto", return_value=["123"]), \
                    mock.patch.object(self.mod, "_command", return_value="python3 -m http.server 8080"), \
                    mock.patch.object(self.mod, "_cwd", return_value=ROOT), \
                    mock.patch.object(self.mod.os, "kill") as kill:
                rc = self.mod.main(["limpiar", ROOT, "8080", pid_file])
            self.assertEqual(rc, 0)
            kill.assert_called_once_with(123, self.mod.signal.SIGTERM)
            self.assertFalse(os.path.exists(pid_file))

    def test_pid_reutilizado_por_otro_proceso_no_se_mata(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_file = os.path.join(tmp, "server.pid")
            with open(pid_file, "w", encoding="ascii") as fh:
                fh.write("123")
            with mock.patch.object(self.mod, "_pids_en_puerto", return_value=["123"]), \
                    mock.patch.object(self.mod, "_command", return_value="node app.js --port 8080"), \
                    mock.patch.object(self.mod, "_cwd", return_value=ROOT), \
                    mock.patch.object(self.mod.os, "kill") as kill:
                rc = self.mod.main(["limpiar", ROOT, "8080", pid_file])
            self.assertEqual(rc, 0)
            kill.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
