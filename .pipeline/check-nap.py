#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de NAP (Name-Address-Phone) para plomeroculiacanpro.mx.
La consistencia del NAP es señal de SEO local: el nombre del negocio, el teléfono
y el email deben ser IDÉNTICOS en todo el sitio (y coincidir con los de Google
Business Profile). Solo lee disco + parsea HTML local. Solo REPORTA. Salida estable.

NAP canónico:
  NAME  = "Plomero Culiacán Pro"          (con acento)
  PHONE = 667 392 2273 / 526673922273
  EMAIL = info@plomeroculiacanpro.mx       (REGLAS f8c72299: el malo es @plomeropro.com)

Chequeos (sobre cada .html servido):
  1. EMAIL dominio incorrecto `@plomeropro.com`            -> alta   (REGLAS f8c72299)
  2. EMAIL del dominio bueno con local-part != "info"
     (p.ej. contacto@plomeroculiacanpro.mx)                -> media  (variante NAP)
  3. NOMBRE del negocio en JSON-LD (Organization/LocalBusiness…) != canónico -> media
  4. NOMBRE sin acento "Plomero Culiacan Pro" en el texto  -> media  (variante NAP)
  5. TELÉFONO en JSON-LD (telephone de un nodo de negocio) con dígitos != correctos -> alta

Emite a stdout SOLO el JSON común:
  {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}],"analizadas":N}
categoria = "nap".
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = ("/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
             "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/",
             "/mcp-local-seo/", "/scripts/")

NAME_OK = "Plomero Culiacán Pro"
NAME_NOACCENT = "Plomero Culiacan Pro"
PHONE_OK = ("526673922273", "6673922273")
BIZ_TYPES = {"Organization", "LocalBusiness", "PlumbingBusiness", "Plumber",
             "ProfessionalService", "HomeAndConstructionBusiness", "Corporation",
             "Store", "GeneralContractor"}

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "nap-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "nap", "descripcion": desc, "fix_sugerido": fix,
    })

def rel(p):
    return os.path.relpath(p, ROOT)

def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

def _walk_biz(node, found):
    if isinstance(node, dict):
        ty = node.get("@type")
        types = ty if isinstance(ty, list) else [ty]
        if any(t in BIZ_TYPES for t in types):
            found.append(node)
        for v in node.values():
            _walk_biz(v, found)
    elif isinstance(node, list):
        for v in node:
            _walk_biz(v, found)

def biz_nodes(t):
    found = []
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                         t, re.I | re.S):
        try:
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        _walk_biz(data, found)
    return found

def main():
    paginas = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dn = "/" + os.path.relpath(dirpath, ROOT).replace(os.sep, "/") + "/"
        if any(s in dn for s in SKIP_DIRS):
            dirnames[:] = []
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            if ".backup" in fn or fn.endswith(".min.html") or fn == "404.html":
                continue
            paginas.append(os.path.join(dirpath, fn))
    paginas.sort()

    analizadas = 0
    localized = {}  # "Marca – <sufijo>" -> nº de páginas (patrón sistemático -> se agrega)
    for fpath in paginas:
        t = read(fpath)
        if not t:
            continue
        analizadas += 1
        r = rel(fpath)

        # 1. email dominio incorrecto @plomeropro.com
        bad = sorted(set(re.findall(r'[\w.+-]+@plomeropro\.com', t, re.I)))
        if bad:
            add("alta", r,
                "NAP: email con dominio INCORRECTO en %s: %s (el correcto es info@plomeroculiacanpro.mx — REGLAS f8c72299)" % (r, ", ".join(bad)),
                "Reemplazar por info@plomeroculiacanpro.mx en todas las apariciones")

        # 2. variante de local-part en el dominio bueno
        variantes = sorted(set(
            lp for lp in re.findall(r'([\w.+-]+)@plomeroculiacanpro\.mx', t, re.I)
            if lp.lower() != "info"))
        if variantes:
            add("media", r,
                "NAP: email con local-part VARIANTE en %s: %s@plomeroculiacanpro.mx (el canónico es info@)" % (r, ", ".join(v + "" for v in variantes)),
                "Unificar a info@plomeroculiacanpro.mx (consistencia NAP para SEO local)")

        # 3. nombre del negocio + teléfono en JSON-LD (dedup por página).
        #    Solo nombres "de marca" (contienen 'plomero') para no marcar a los
        #    Organization de reseñas (author/publisher "Google", etc.). El teléfono
        #    solo aparece en el nodo de negocio, no en los de reseña.
        name_vars, tel_vars = set(), set()
        for node in biz_nodes(t):
            nm = node.get("name")
            if (isinstance(nm, str) and "plomer" in nm.lower()  # plomero/plomería/plomera…
                    and nm.strip() not in (NAME_OK, NAME_NOACCENT)):
                name_vars.add(nm.strip())
            tel = node.get("telephone")
            if isinstance(tel, str) and tel.strip():
                d = re.sub(r"\D", "", tel)
                if d not in PHONE_OK and not (d.endswith("6673922273") and (len(d) == 10 or d.startswith("52"))):
                    tel_vars.add(tel.strip())
        for nm in sorted(name_vars):
            if nm.startswith(NAME_OK):
                # "Plomero Culiacán Pro – Las Quintas": marca + sufijo de colonia.
                # Patrón sistemático -> se agrega en UN solo hallazgo al final.
                localized[nm] = localized.get(nm, 0) + 1
            else:
                add("media", r,
                    "NAP: nombre de negocio VARIANTE INESPERADA en JSON-LD de %s: %r (el canónico es %r)" % (r, nm, NAME_OK),
                    "Unificar el name del schema de negocio a %r" % NAME_OK)
        for tel in sorted(tel_vars):
            add("alta", r,
                "NAP: teléfono VARIANTE en JSON-LD de %s: %r (el correcto es +52 667 392 2273)" % (r, tel),
                "Corregir telephone del schema al número correcto (526673922273)")

        # 4. nombre sin acento en el texto
        if NAME_NOACCENT in t:
            add("media", r,
                "NAP: nombre de negocio SIN acento en %s: '%s' (el canónico es '%s')" % (r, NAME_NOACCENT, NAME_OK),
                "Corregir a '%s' (con acento) para consistencia NAP" % NAME_OK)

    # Patrón localizado "Marca – <Colonia>" (p.ej. "Plomero Culiacán Pro – Las Quintas"):
    # DECISIÓN DE HÉCTOR (2026-06-14): es INTENCIONAL (nombre por colonia) -> se ACEPTA y
    # NO se reporta. Las variantes de marca que NO empiezan por el canónico sí se reportan
    # (bloque #3 de arriba); aquí solo se ignora el sufijo de colonia.
    _ = localized  # aceptado por decisión; sin hallazgo

    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
