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

## [PENDIENTE] costo — Detector de CORRIDA DESBOCADA (output/mensajes vs mediana), no solo volumen total   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** El tripwire actual (`check-costos.py`) solo mira `total_tokens > 28M`. Pero `total_tokens` lo domina el `cache_read` (barato por token y proporcional al CONTEXTO, no al trabajo). El modo de fallo caro de verdad es un **loop que se desboca**: la corrida genera millones de `output_tokens` y miles de mensajes. Ese eje hoy NO se vigila, y un umbral fijo sobre el total no distingue "día grande pero acotado" de "loop sin freno".
**Evidencia (brief de costo, 15 corridas):** 3 de las últimas ~11 corridas explotaron a **606M · 617M · 654M tokens (~$1307 · $1343 · $1420 api-ref)** vs **mediana 26.6M**. Las tres comparten la firma de desboque: `output_tokens` **2.1–2.3M** (vs ~150–260K normal, ≈10×) y **1453 · 1659 · 1415 mensajes** (vs 36–368 normal). El total fijo las marca, pero como `media` y sin nombrar la causa; el discriminante real (output/mensajes) queda invisible.
**Propuesta:** Añadir a `check-costos.py` un segundo cheque que compare la última corrida contra la **mediana móvil** de las previas en DOS ejes de trabajo real —`output_tokens` y `mensajes`— y emita `alta` ("corrida desbocada") cuando cualquiera supere ~5× la mediana. Mantiene el cheque de volumen actual como `media`. Cambio aditivo, sin red, auto-drenado por el diario.
**DRAFT (listo para merge — añadir a `.pipeline/check-costos.py`, dentro de `main()` tras leer `filas`):**
```python
    # ── Detector de CORRIDA DESBOCADA: output_tokens y nº de mensajes vs mediana móvil.
    #    total_tokens lo domina cache_read (∝ contexto, barato); el costo de un loop sin
    #    freno se ve en output_tokens y en mensajes. Marca ALTA si la última corrida supera
    #    FACTOR× la mediana de las previas. (3 corridas a 606–654M / $1300+ tenían
    #    output 2.1–2.3M y 1415–1659 mensajes vs mediana 26.6M.)
    FACTOR = 5
    MIN_HIST = 4            # no juzgar sin historia suficiente
    def _mediana(xs):
        s = sorted(xs); n = len(s)
        if not n: return 0
        return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2
    if len(filas) > MIN_HIST:
        u = filas[-1]; prev = filas[:-1]
        for campo, etiqueta in (("output_tokens", "output"), ("mensajes", "mensajes")):
            cur = u.get(campo, 0) or 0
            med = _mediana([f.get(campo, 0) or 0 for f in prev])
            if med > 0 and cur > FACTOR * med:
                hallazgos.append({
                    "id": "costo-runaway-%s" % etiqueta, "archivo": ".pipeline/costos.jsonl", "linea": 0,
                    "severidad": "alta", "categoria": "costo",
                    "descripcion": "CORRIDA DESBOCADA: la última (%s) generó %s=%s, ~%.0f× la mediana (%s). Firma de loop sin freno, no de día grande." % (
                        u.get("etiqueta", "?"), etiqueta, f"{cur:,}", cur/med, f"{int(med):,}"),
                    "fix_sugerido": "Auditar la corrida: ¿loop-until-dry sin tope, fan-out de revisores sin lote, o re-trabajo en bucle? Poner freno por nº de páginas/iteraciones en el driver (crecer-diario) y/o bajar el fan-out paralelo.",
                })
```

---

## [PENDIENTE] infra — Convertir el over-budget de REGLAS.md en tarea DRENABLE (no solo exit 1 de FASE 9)   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** El presupuesto de `REGLAS.md` lo vigila `check-reglas.py`, pero es una **utilidad** (`infra:utilidad-no-sensor`, exit 0/1) que solo corre en FASE 9 y depende de que el bibliotecario actúe esa corrida. Si la fase se salta o el agente ignora el exit 1, el over-budget queda silencioso y se arrastra entre corridas. Nada lo mete a la cola de hallazgos que el diario DRENA solo.
**Evidencia (brief de REGLAS):** `~3997 tokens estimados (presupuesto 4000) ⚠️ cerca/encima del tope`. La señal persiste pegada al cap corrida tras corrida → la consolidación no está ocurriendo de forma fiable; el guard actual no la fuerza.
**Propuesta:** Un sensor delgado `check-reglas-presupuesto.py` que REUSA el mismo estimado (chars/4) y emite el contrato `{hallazgos}` (no exit-code) con `media` cuando REGLAS pasa el 95% del presupuesto o tiene reglas gordas, listando las ofensoras. Así el over-budget se vuelve un hallazgo que `check-infra` smoke-testea y el diario drena como tarea de consolidación, en vez de un exit-1 que se puede ignorar. No reemplaza a `check-reglas.py` (sigue siendo el gate duro de FASE 9); lo complementa con visibilidad continua.
**DRAFT (listo para merge — crear `.pipeline/check-reglas-presupuesto.py`):**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensor de PRESUPUESTO de REGLAS.md (versión que emite el contrato {hallazgos}).
Complementa a check-reglas.py (utilidad exit-0/1 de FASE 9): convierte el over-budget en un
hallazgo DRENABLE por el diario, en vez de un exit-1 que se puede ignorar si la fase se salta.
REGLAS.md se inyecta en cada corrida y lo lee cada subagente (~19 lecturas/día); si se arrastra
sobre el tope, cuesta tokens y diluye atención. Emite a stdout SOLO {"hallazgos":[...]}.
"""
import os, json

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(ROOT, "docs", "REGLAS.md")
MAX_TOKENS     = 4000   # idéntico a check-reglas.py
MAX_RULE_CHARS = 900
AVISO_FRAC     = 0.95   # avisar al rozar el cap, no solo al pasarlo (hoy: 3997/4000)

def main():
    hallazgos = []
    if os.path.isfile(REGLAS):
        lines = open(REGLAS, encoding="utf-8", errors="replace").read().splitlines()
        rules = [ln for ln in lines if ln.lstrip().startswith("- [")]
        total_chars = sum(len(ln) for ln in lines)
        est_tokens = total_chars // 4
        gordas = [ln for ln in rules if len(ln) > MAX_RULE_CHARS]
        if est_tokens >= MAX_TOKENS * AVISO_FRAC:
            hallazgos.append({
                "id": "reglas-presupuesto", "archivo": "docs/REGLAS.md", "linea": 0,
                "severidad": "media", "categoria": "infra",
                "descripcion": "REGLAS.md ~%d tokens estimados (presupuesto %d). Se inyecta en cada corrida y lo lee cada subagente; arrastrarlo sobre el tope cuesta tokens y diluye atención." % (est_tokens, MAX_TOKENS),
                "fix_sugerido": "Consolidar: cada regla = qué hacer + el checker que lo caza. Cuando un error ya está mecanizado, reduce la regla a «qué + checker» y manda el relato a HISTORIAL.jsonl.",
            })
        if gordas:
            hallazgos.append({
                "id": "reglas-gordas", "archivo": "docs/REGLAS.md", "linea": 0,
                "severidad": "media", "categoria": "infra",
                "descripcion": "%d regla(s) de REGLAS.md pasan de %d chars (relato de incidente sin podar): %s" % (
                    len(gordas), MAX_RULE_CHARS, " | ".join(ln[:70] for ln in gordas[:3])),
                "fix_sugerido": "Podar cada regla gorda a 1-2 líneas accionables; el relato largo va a HISTORIAL.jsonl, no a REGLAS.md.",
            })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

---

## [PENDIENTE] infra — Gate PROACTIVO de contrato de checkers en pre-push (matar la clase infra-003 al commit, no a la corrida siguiente)   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** Cuando se añade un `check-*.{py,mjs}` que NO emite `{hallazgos}` ni declara `infra:utilidad-no-sensor`, el dead-man's switch (`check-infra.mjs`) lo descubre — pero solo en la **corrida diaria siguiente**, disparando una ALTA falsa de "verificación ciega" que cuesta un ciclo manual de fix. La detección es REACTIVA: el checker roto ya se commiteó y la próxima corrida tropieza con él.
**Evidencia (HISTORIAL, regresiones):** `infra-003` (añadir check-parte.py/check-reglas.py sin actualizar NOT_PAGE_CHECKERS → 2 ALTA falsas), `infra-001-css-paridad` (check-css-paridad.py imprimía texto humano → ALTA "verificación ciega"), descritas explícitamente como **"clase infra-003/005"**. Es un patrón reincidente (≥3 veces) que se mecaniza solo a medias.
**Propuesta:** Hacer el smoke PROACTIVO: un guard liviano que en `pre-push` (sección gate de `main`) corra cada `check-*.{py,mjs}` que NO sea NOT_PAGE_CHECKER ni utilidad declarada, y aborte el push si alguno no imprime un JSON con array `hallazgos`. Así un checker roto **nunca llega** a una corrida diaria; el fallo se ve al pushear, con criterio humano presente. Reusa exactamente las reglas de clasificación de `check-infra.mjs`.
**DRAFT (listo para merge — crear `.pipeline/check-contrato-checkers.mjs`):**
```javascript
#!/usr/bin/env node
// Gate PROACTIVO del contrato de checkers (clase regresión infra-003/005).
// Corre cada .pipeline/check-*.{py,mjs} que sea SENSOR DE PÁGINA (no NOT_PAGE_CHECKERS ni
// utilidad declarada) y verifica que imprima un JSON con array "hallazgos". exit 1 si alguno
// no cumple — pensado para pre-push, para que un checker roto no llegue a la corrida diaria
// (donde hoy dispara una ALTA falsa de "verificación ciega" un ciclo después).
const fs = require("fs");
const cp = require("child_process");
const dir = __dirname;
const NOT_PAGE = new Set(["check-infra.mjs", "check-secretos.sh", "check-contrato-checkers.mjs"]);
const HEAVY = new Set(["check-produccion.mjs", "check-perf.mjs", "check-tracking.mjs", "check-e2e.mjs"]); // tocan red: omitir en pre-push
const esUtilidad = (f) => {
  try { return fs.readFileSync(`${dir}/${f}`, "utf8").slice(0, 800).includes("infra:utilidad-no-sensor"); }
  catch { return false; }
};
const checkers = fs.readdirSync(dir)
  .filter((f) => /^check-.*\.(py|mjs)$/.test(f) && !NOT_PAGE.has(f) && !HEAVY.has(f) && !esUtilidad(f))
  .sort();
let fallos = 0;
for (const f of checkers) {
  const runner = f.endsWith(".py") ? "python3" : process.execPath;
  let ok = false, motivo = "";
  try {
    const r = cp.spawnSync(runner, [`${dir}/${f}`], { encoding: "utf8", timeout: 60000 });
    if (r.status !== 0) { motivo = `exit ${r.status}: ${(r.stderr || "").slice(0, 160)}`; }
    else {
      const data = JSON.parse(r.stdout);
      if (Array.isArray(data.hallazgos)) ok = true;
      else motivo = "el JSON no tiene array \"hallazgos\"";
    }
  } catch (e) { motivo = `no devolvió JSON parseable (${String(e).slice(0, 120)})`; }
  if (!ok) { fallos++; console.error(`❌ ${f}: ${motivo}`); }
}
if (fallos) {
  console.error(`\n${fallos} checker(s) NO emiten el contrato {hallazgos}. Si es una UTILIDAD, ` +
    `declara \`infra:utilidad-no-sensor\` en su cabecera; si es un sensor, arregla su salida.`);
  process.exit(1);
}
console.log(`✅ ${checkers.length} checkers emiten el contrato {hallazgos}.`);
```
**DRAFT (2/2 — añadir en `.pipeline/hooks/pre-push`, dentro del bloque gate de `main`, junto a la llamada a `ci-gate.py`):**
```bash
  # 1c) Contrato de checkers: ningún sensor de página puede dejar de emitir {hallazgos}
  #     (clase regresión infra-003/005). Proactivo: bloquea aquí, no en la corrida siguiente.
  if [ -x "$NODE" ] && [ -f "$REPO/.pipeline/check-contrato-checkers.mjs" ]; then
    if ! ( cd "$REPO" && "$NODE" .pipeline/check-contrato-checkers.mjs ); then
      echo ""
      echo "❌ PUSH BLOQUEADO: un checker no emite el contrato {hallazgos} (ver arriba)."
      exit 1
    fi
  fi
```

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

## [HECHO 2026-06-19] costo — Tripwire de visibilidad de costo por corrida   (impacto B · esfuerzo S · riesgo bajo)
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
