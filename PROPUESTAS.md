# PROPUESTAS del Crítico-Sistema

Aquí `critico-sistema` (3×/semana) deja mejoras al SISTEMA **con el draft ya escrito**, listas para que
solo les des merge. Las más nuevas van ARRIBA. Nada de esto se aplica solo — tú apruebas.

Formato de cada propuesta:

```
## [PENDIENTE] <area> — <título>   (impacto A/M/B · esfuerzo S/M/L · riesgo bajo/medio/alto)
**Problema:** ...
**Evidencia:** ... (dato duro del brief)
**Propuesta:** ...
**DRAFT (listo para merge):**
   <el código del checker/auto-fixer, o el bloque de prompt exacto>
```

Cuando apruebes una, cambia `[PENDIENTE]` → `[HECHO <fecha>]` (o bórrala).

---

## [HECHO 2026-06-19] cobertura — Barrido estructural de TODO el sitio (no solo páginas editadas)   (impacto A · esfuerzo M · riesgo bajo)
> ✅ Mergeada: `.pipeline/check-estructura-sitio.py` creado + en `ci-gate`. Encontró 12 páginas con `<meta robots>` faltante; se cerraron con un auto-fixer `meta-robots` nuevo (12/12). Checker ahora en 0.
**Problema:** El gate (`validate-landing` / `gate-pagina.py`) solo corre sobre las páginas del diff. Por eso defectos PRE-EXISTENTES quedan invisibles hasta que alguien toca esa página por casualidad y el push se **bloquea por sorpresa**. Ningún checker determinista barre el sitio entero buscando estos invariantes de plantilla.
**Evidencia (datos duros del HISTORIAL):** `seo-meta-robots-repfugas` ("el gate pre-push expuso una falla pre-existente: faltaba `<meta robots>`... deuda amplia 10+ páginas"), `deuda-robots-001` (8 páginas indexables sin `<meta robots>`), `plt-hero-tinaco` ("No detectado antes porque el gate solo corre sobre páginas editadas"). 3 hallazgos del mismo patrón = deuda reactiva, no proactiva.
**Propuesta:** Nuevo checker determinista `check-estructura-sitio.py` que recorre TODAS las `<loc>` indexables del sitemap y verifica los invariantes que hoy solo valida el gate: (R1) `<meta name="robots">` presente; (R2) si la página tiene `class="hero"`, debe envolver su contenido en `.hero-content`. Emite el contrato común `{"hallazgos":[...]}`, así que `check-infra.mjs` lo smoke-testea y el Auto Agente diario lo drena solo. Convierte "sorpresa al editar" → "tarea de backlog priorizada". Es el lever del 90%.
**DRAFT (listo para merge — crear `.pipeline/check-estructura-sitio.py`):**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checker DETERMINISTA de ESTRUCTURA a nivel de TODO el sitio (no solo páginas del diff).
Cierra el hueco: validate-landing/gate-pagina solo corren sobre las páginas editadas, así
que defectos PRE-EXISTENTES (sin <meta robots>, hero sin .hero-content) quedan invisibles
hasta que alguien toca esa página y el push se bloquea por sorpresa
(HISTORIAL: seo-meta-robots-repfugas, plt-hero-tinaco, deuda-robots-001).

Recorre TODAS las <loc> indexables del sitemap y verifica:
  R1 (media) <meta name="robots"> presente.
  R2 (media) si la página tiene class="hero", debe envolver su contenido en .hero-content.

Emite a stdout SOLO el JSON común de hallazgos. Sin argumentos: barre el sitio completo.
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://plomeroculiacanpro.mx"
SITEMAP = os.path.join(ROOT, "sitemaps", "main_sitemap.xml")

hallazgos = []
_seq = 0
def add(sev, archivo, desc, fix, linea=0):
    global _seq
    _seq += 1
    hallazgos.append({
        "id": "estr-%03d" % _seq, "archivo": archivo, "linea": linea,
        "severidad": sev, "categoria": "plantilla",
        "descripcion": desc, "fix_sugerido": fix,
    })

def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

def url_to_path(loc):
    path = loc[len(BASE):] if loc.startswith(BASE) else loc
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return os.path.join(ROOT, "index.html")
    rels = path.strip("/")
    if path.endswith("/"):
        return os.path.join(ROOT, rels, "index.html")
    if path.endswith(".html"):
        return os.path.join(ROOT, rels)
    cand = os.path.join(ROOT, rels, "index.html")
    if os.path.isfile(cand):
        return cand
    return os.path.join(ROOT, rels + ".html")

NOINDEX         = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
HAS_ROBOTS      = re.compile(r'<meta[^>]+name=["\']robots["\']', re.I)
HAS_HERO        = re.compile(r'class=["\'][^"\']*(?<![\w-])hero(?![\w-])', re.I)        # token "hero" exacto (no "hero-content")
HAS_HEROCONTENT = re.compile(r'class=["\'][^"\']*(?<![\w-])hero-content(?![\w-])', re.I)

def main():
    txt = read(SITEMAP)
    seen = set()
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", txt):
        fpath = url_to_path(loc)
        if fpath in seen or not os.path.isfile(fpath):
            continue
        seen.add(fpath)
        rel = os.path.relpath(fpath, ROOT)
        t = read(fpath)
        if NOINDEX.search(t):
            continue  # noindex: fuera del estándar indexable
        if not HAS_ROBOTS.search(t):
            add("media", rel,
                "%s (indexable, en sitemap) no emite <meta name=\"robots\">; deuda PRE-EXISTENTE que el gate solo expone al editar la página" % loc,
                "Añadir antes del canonical: <meta name=\"robots\" content=\"index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1\"> (idéntico a las hermanas nuevas, p.ej. reparacion-de-fugas)")
        if HAS_HERO.search(t) and not HAS_HEROCONTENT.search(t):
            add("media", rel,
                "%s tiene class=\"hero\" pero le falta el wrapper div.hero-content del estándar (validate-landing/gate FALLAN al editarla)" % loc,
                "Envolver h1+subtitle+CTA del hero en <div class=\"hero-content\">…</div> como el resto de servicios; verificar visual headless 375/1280")
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

---

## [HECHO 2026-06-19] seo — Cazar `og:url` AUSENTE (no solo el incorrecto) en páginas indexables   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** `check-indexabilidad.py` (~L296) solo marca `og:url` cuando está presente Y difiere del canonical (`if og is not None and og != ref`). Si la etiqueta **falta del todo**, no la caza nadie — la inconsistencia queda como deuda silenciosa.
**Evidencia (HISTORIAL):** `seo-ogurl-6serv` — "6 de 8 páginas de servicio no emiten `<meta property=og:url>`... Inconsistencia con el estándar... og:url ausente != og:url incorrecto" → quedó PENDIENTE porque el checker no lo detecta. Mismo eje que las regresiones `seo-206/207` (og:url) ya mecanizadas para el caso "incorrecto".
**Propuesta:** Añadir una rama `elif og is None` al bloque que ya existe, severidad `media` (ausencia es inconsistencia, no contradicción → no bloquea, pero el diario la drena). Edición de 5 líneas en el checker que YA recorre todas las páginas del sitemap.
**DRAFT (listo para merge — reemplazar el bloque en `.pipeline/check-indexabilidad.py` ~L293-299):**
```python
            # 2: og:url == canonical (referencia seo-201..207, seo-ogurl-6serv)
            ref = canonical or loc
            og = get_og_url(t)
            if og is not None and og != ref:
                add("alta", r,
                    "og:url (%s) != canonical (%s) en %s" % (og, ref, loc),
                    "Corregir <meta property=\"og:url\"> a %s" % ref)
            elif og is None:
                add("media", r,
                    "%s (indexable) no emite <meta property=\"og:url\">; inconsistente con el estándar (las hermanas sí lo tienen). Ausente != incorrecto, pero deja la página sin la señal" % loc,
                    "Añadir <meta property=\"og:url\" content=\"%s\"> junto al resto de etiquetas og en el <head>" % ref)
```

---

## [HECHO 2026-06-19] infra — Eliminar el acoplamiento que hace mentir al dead-man's switch (regresión infra-003)   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** `check-infra.mjs` clasifica los checkers con una denylist HARDCODEADA (`NOT_PAGE_CHECKERS`). Cada vez que se añade un checker UTILITARIO (que no emite el contrato `{hallazgos}`) hay que acordarse de editar ese set central; si se olvida, el sensor emite ALTA falsa de "verificación ciega". El sensor miente.
**Evidencia (HISTORIAL):** `infra-003` — "REGRESION introducida por commit 2871010f: se añadieron check-parte.py y check-reglas.py sin actualizar NOT_PAGE_CHECKERS → 2 ALTA falsas de 'verificación ciega'. El sensor mentía." (categoría infra, severidad alta).
**Propuesta:** Hacer que una utilidad pueda **auto-excluirse declarando un marcador en su propio archivo** (`infra:utilidad-no-sensor`), sin tocar `check-infra.mjs`. Cambio puramente ADITIVO (la denylist sigue valiendo para el núcleo): elimina el acoplamiento que causó la regresión, es local y auto-documentado. (No invertir a allowlist: un olvido ahí apagaría un sensor REAL en silencio — peor que una ALTA ruidosa.)
**DRAFT (listo para merge — en `.pipeline/check-infra.mjs`):**
```javascript
// (1) Añadir este helper cerca de la función que lista los checkers:
// Una utilidad (no-sensor de página) puede auto-excluirse SIN tocar este archivo
// declarando el marcador `infra:utilidad-no-sensor` en sus primeras líneas. Evita la
// regresión infra-003 (añadir un check-*.py utilitario y olvidar NOT_PAGE_CHECKERS
// -> ALTA falsa de "verificación ciega").
function esUtilidadDeclarada(f) {
  try {
    const head = fs.readFileSync(`${__dirname}/${f}`, "utf8").slice(0, 800);
    return head.includes("infra:utilidad-no-sensor");
  } catch (_) { return false; }
}

// (2) Cambiar el filtro de listado (la línea ~137) a:
  return fs.readdirSync(__dirname)
    .filter((f) => /^check-.*\.(py|mjs)$/.test(f) && !NOT_PAGE_CHECKERS.has(f) && !esUtilidadDeclarada(f))
    .sort();

// (3) (opcional) Migrar las utilidades actuales: añadir el comentario
//     `# infra:utilidad-no-sensor` en la cabecera de check-parte.py y check-reglas.py,
//     y dejar en NOT_PAGE_CHECKERS solo el núcleo (check-infra.mjs, check-secretos.sh).
```

---

## [PENDIENTE] costo — Tripwire de visibilidad de costo por corrida   (impacto B · esfuerzo S · riesgo bajo)
**Problema:** El costo por corrida se registra en `costos.jsonl` pero nada lo VIGILA: un pico solo se descubriría en la factura. No hay alerta cuando una corrida se dispara.
**Evidencia (brief de costo):** corridas en M tokens: `35.5 · 11.8`; la corrida grande del 2026-06-18 = **35.5M tokens / ~$91 api-ref** (3× la corrida normal de 11.8M). Solo 2 datapoints, pero el pico es real.
**Propuesta:** Checker liviano `check-costos.py` que lee la última fila de `costos.jsonl` y emite un hallazgo `media` si supera el presupuesto (tokens o USD). Solo VISIBILIDAD (no corta nada): el pico aparece en el reporte diario. Se auto-integra (emite `{hallazgos}`, lo smoke-testea check-infra). Umbral conservador (≈2× la corrida normal) para no alertar de rutina.
**DRAFT (listo para merge — crear `.pipeline/check-costos.py`):**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tripwire de COSTO/CUOTA. Lee .pipeline/costos.jsonl; si la ÚLTIMA corrida superó el
presupuesto de tokens/USD, emite un hallazgo (media) para que el dueño VEA el costo en el
reporte diario en vez de descubrirlo en la factura. Solo VISIBILIDAD: no corta nada.
(Corrida grande del 2026-06-18: 35.5M tok / ~$91 api-ref vs 11.8M normal.)
Emite el JSON común {"hallazgos":[...]}. Sin argumentos.
"""
import os, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTOS = os.path.join(ROOT, ".pipeline", "costos.jsonl")
UMBRAL_TOKENS = 28_000_000   # ~2x una corrida diaria normal (11.8M)
UMBRAL_USD    = 70           # usd_equiv_api_ref

def main():
    hallazgos, filas = [], []
    if os.path.isfile(COSTOS):
        for ln in open(COSTOS, encoding="utf-8", errors="replace"):
            ln = ln.strip()
            if ln:
                try: filas.append(json.loads(ln))
                except Exception: pass
    if filas:
        u   = filas[-1]
        tok = u.get("total_tokens", 0)
        usd = u.get("usd_equiv_api_ref", 0)
        if tok > UMBRAL_TOKENS or usd > UMBRAL_USD:
            hallazgos.append({
                "id": "costo-001", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "La última corrida (%s) consumió %.1fM tokens (~$%.0f api-ref), sobre presupuesto (%.0fM / $%.0f)." % (
                    u.get("etiqueta", "?"), tok/1e6, usd, UMBRAL_TOKENS/1e6, UMBRAL_USD),
                "fix_sugerido": "Auditar la corrida: ¿demasiados revisores en paralelo, lote grande, o un loop sin freno? Bajar fan-out o usar modelo más barato en revisores deterministas.",
            })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

---

_(Las propuestas más nuevas van ARRIBA de esta línea.)_
