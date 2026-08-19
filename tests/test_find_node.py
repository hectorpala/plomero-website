#!/usr/bin/env python3
"""Pruebas del descubrimiento compartido del ejecutable de Node."""
import importlib.util
import json
import os
import stat
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(ROOT, ".pipeline", "encontrar-node.py")


def _cargar():
    spec = importlib.util.spec_from_file_location("encontrar_node", RUTA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _executable(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nexit 0\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)


class FindNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _cargar()

    def test_prefiere_el_node_disponible_en_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = os.path.join(tmp, "bin", "node")
            _executable(binary)
            self.assertEqual(
                self.mod.encontrar(os.path.dirname(binary), respaldos=()),
                binary,
            )

    def test_usa_respaldo_ejecutable_si_path_no_tiene_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = os.path.join(tmp, "homebrew", "node")
            _executable(binary)
            self.assertEqual(self.mod.encontrar("", respaldos=(binary,)), binary)

    def test_ignora_archivos_no_ejecutables(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = os.path.join(tmp, "node")
            with open(binary, "w", encoding="utf-8") as fh:
                fh.write("no ejecutable\n")
            self.assertEqual(self.mod.encontrar("", respaldos=(binary,)), "")

    def test_drivers_activos_usan_el_resolver_y_no_fijan_usr_local(self):
        for relative in (
            ".pipeline/crecer-diario.sh",
            ".pipeline/meta-semanal.sh",
            ".pipeline/maraton.sh",
        ):
            with self.subTest(relative=relative):
                with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
                    source = fh.read()
                self.assertIn(".pipeline/encontrar-node.py", source)
                self.assertIn('NODE_BIN=$(python3 "$NODE_FINDER"', source)
                self.assertNotIn("/usr/local/bin/node", source)

    def test_mcp_de_diario_y_maraton_recibe_la_ruta_resuelta(self):
        for relative in (".pipeline/crecer-diario.sh", ".pipeline/maraton.sh"):
            with self.subTest(relative=relative):
                with open(os.path.join(ROOT, relative), encoding="utf-8") as fh:
                    source = fh.read()
                self.assertIn('mcp_servers.gsc.command=\\"$NODE_BIN\\"', source)
                self.assertIn('mcp_servers.local-seo.command=\\"$NODE_BIN\\"', source)

    def test_dead_man_switch_reutiliza_su_runtime(self):
        with open(os.path.join(ROOT, ".pipeline", "check-infra.mjs"), encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn("const NODE = process.execPath;", source)
        self.assertNotIn('fs.existsSync("/usr/local/bin/node")', source)

    def test_config_mcp_portatil_delega_node_al_path(self):
        with open(os.path.join(ROOT, ".pipeline", "mcp-run.json"), encoding="utf-8") as fh:
            config = json.load(fh)
        for server in config["mcpServers"].values():
            with self.subTest(server=server):
                self.assertEqual(server["command"], "/usr/bin/env")
                self.assertEqual(server["args"][0], "node")


if __name__ == "__main__":
    unittest.main(verbosity=2)
