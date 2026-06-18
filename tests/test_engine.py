#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests del MOTOR determinista del Auto Agente (sin red, herméticos).

Blindan las dos piezas de las que depende toda la seguridad de generación:
  • .pipeline/gen-landing.py  — copia de esqueleto + sustituciones afirmadas + guardas anti-fuga.
  • .pipeline/gate-pagina.py  — tokenizador de texto visible + Jaccard del candado anti-doorway.

Si alguien rompe el conteo exacto de sustituciones, la guarda anti-fuga "electricista", o
el tokenizador anti-doorway, ESTOS tests fallan ANTES de que llegue a producción.

Correr:  python3 -m unittest discover -s tests -p 'test_*.py'
   o:     npm test
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(ROOT, ".pipeline")
TMP = os.path.join(ROOT, "tests", "_tmp")


def _load_module(path, name):
    """Importa un .py por ruta (gate-pagina.py tiene guion → no es importable normal)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Esqueleto mínimo pero realista: dos marcadores de slug + un título. NO contiene palabras-fuga.
SKELETON = (
    "<!doctype html><html><head><title>Plomero en Zona Vieja</title>\n"
    '<link rel="canonical" href="https://plomeroculiacanpro.mx/servicios/plomero-zona-vieja-culiacan/">\n'
    "</head><body><h1>Plomero en Zona Vieja</h1>\n"
    '<a href="/servicios/plomero-zona-vieja-culiacan/">Zona Vieja</a>\n'
    "<p>Servicio de plomería en la zona vieja de Culiacán.</p></body></html>\n"
)


class GenLandingCLI(unittest.TestCase):
    """Contrato de CLI de gen-landing.py vía subproceso (como lo usa el sistema real)."""

    def setUp(self):
        os.makedirs(TMP, exist_ok=True)
        self.skel_rel = os.path.join("tests", "_tmp", "skel.html")
        self.out_rel = os.path.join("tests", "_tmp", "out.html")
        with open(os.path.join(ROOT, self.skel_rel), "w", encoding="utf-8") as f:
            f.write(SKELETON)
        self.addCleanup(shutil.rmtree, TMP, ignore_errors=True)

    def _run(self, spec):
        spec_path = os.path.join(TMP, "spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(spec, f)
        return subprocess.run(
            [sys.executable, os.path.join(PIPE, "gen-landing.py"), spec_path],
            capture_output=True, text=True, cwd=ROOT,
        )

    def test_happy_path_escribe_y_sale_0(self):
        """Sustituciones con conteo exacto → escribe el output y exit 0."""
        spec = {
            "skeleton": self.skel_rel,
            "output": self.out_rel,
            "replacements": [
                {"old": "Plomero en Zona Vieja", "new": "Plomero en Zona Norte", "n": 2},
                {"old": "plomero-zona-vieja-culiacan", "new": "plomero-zona-norte-culiacan", "n": 2},
                {"old": "zona vieja de Culiacán", "new": "zona norte de Culiacán", "n": 1},
                {"old": ">Zona Vieja<", "new": ">Zona Norte<", "n": 1},
            ],
        }
        r = self._run(spec)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out_abs = os.path.join(ROOT, self.out_rel)
        self.assertTrue(os.path.isfile(out_abs))
        with open(out_abs, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("plomero-zona-norte-culiacan", content)
        self.assertNotIn("plomero-zona-vieja-culiacan", content)

    def test_drift_conteo_incorrecto_aborta_sin_escribir(self):
        """Si el nº de ocurrencias no calza, ABORTA (exit 1) y NO escribe — esto impide el drift de plantilla."""
        spec = {
            "skeleton": self.skel_rel,
            "output": self.out_rel,
            # "Plomero en Zona Vieja" aparece 2 veces, pero afirmamos 5 → debe abortar.
            "replacements": [{"old": "Plomero en Zona Vieja", "new": "X", "n": 5}],
        }
        r = self._run(spec)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("ABORT", r.stdout)
        self.assertFalse(os.path.isfile(os.path.join(ROOT, self.out_rel)))

    def test_fuga_electricista_aborta(self):
        """Si una sustitución introduce la palabra-fuga del clon ('electricista'), ABORTA."""
        spec = {
            "skeleton": self.skel_rel,
            "output": self.out_rel,
            "replacements": [
                {"old": "Plomero en Zona Vieja", "new": "Electricista en Zona Vieja", "n": 2},
            ],
        }
        r = self._run(spec)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("fuga", r.stdout.lower())
        self.assertFalse(os.path.isfile(os.path.join(ROOT, self.out_rel)))

    def test_fuga_gtm_electricista_aborta(self):
        """El GTM del electricista (GTM-5Z2QRZ5Q) tampoco debe poder colarse."""
        spec = {
            "skeleton": self.skel_rel,
            "output": self.out_rel,
            "replacements": [
                {"old": "zona vieja de Culiacán", "new": "zona (GTM-5Z2QRZ5Q) de Culiacán", "n": 1},
            ],
        }
        r = self._run(spec)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertFalse(os.path.isfile(os.path.join(ROOT, self.out_rel)))

    def test_falta_clave_aborta(self):
        """Spec sin la clave 'replacements' → aborta limpio (exit 1)."""
        r = self._run({"skeleton": self.skel_rel, "output": self.out_rel})
        self.assertEqual(r.returncode, 1, r.stdout)


class AntiDoorway(unittest.TestCase):
    """Funciones puras del candado anti-doorway de gate-pagina.py."""

    @classmethod
    def setUpClass(cls):
        cls.gp = _load_module(os.path.join(PIPE, "gate-pagina.py"), "gate_pagina")
        os.makedirs(TMP, exist_ok=True)

    def setUp(self):
        os.makedirs(TMP, exist_ok=True)
        self.addCleanup(shutil.rmtree, TMP, ignore_errors=True)

    def _write(self, name, html):
        p = os.path.join(TMP, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_jaccard_identico_es_1(self):
        a = {"plomero", "culiacan", "fuga", "drenaje"}
        self.assertEqual(self.gp.jaccard(a, set(a)), 1.0)

    def test_jaccard_disjunto_es_0(self):
        self.assertEqual(self.gp.jaccard({"alfa", "beta"}, {"gamma", "delta"}), 0.0)

    def test_jaccard_parcial(self):
        a, b = {"uno", "dos", "tres", "cuatro"}, {"tres", "cuatro", "cinco", "seis"}
        self.assertAlmostEqual(self.gp.jaccard(a, b), 2 / 6)

    def test_visible_tokens_quita_script_style_y_tags(self):
        p = self._write(
            "vis.html",
            "<html><head><style>.x{color:red}</style>"
            "<script>var secreto='zzzz'</script></head>"
            "<body><h1>Reparacion</h1><p>Fugas Culiacan</p></body></html>",
        )
        toks = self.gp.visible_tokens(p)
        self.assertIn("reparacion", toks)
        self.assertIn("culiacan", toks)
        # Lo que vive dentro de <script>/<style> NO debe contar como texto visible.
        self.assertNotIn("zzzz", toks)
        self.assertNotIn("color", toks)

    def test_noindex_devuelve_none(self):
        """Una página noindex no compite por ranking → queda fuera del anti-doorway."""
        p = self._write(
            "noindex.html",
            '<html><head><meta name="robots" content="noindex,follow"></head>'
            "<body><p>lo que sea</p></body></html>",
        )
        self.assertIsNone(self.gp.visible_tokens(p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
