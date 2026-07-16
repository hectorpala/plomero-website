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

## [PENDIENTE] a11y/movil — Denylist de color prohibido en `.breadcrumb-item` — reincidió 3 veces (07-09/07-13/07-14) por vivir en `<style>` inline por-página, y `.breadcrumb-item.active` sigue fallando AA HOY en las 3 hojas compartidas   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** El contraste del breadcrumb es la regresión MÁS reincidente del sistema. `.breadcrumb-item a{color:#E36414}` (3.26-3.27:1, falla AA 4.5:1) reapareció el 2026-07-09, el 2026-07-13 (la propia corrida lo diagnosticó: "el fix nunca se centralizó — vivía duplicado en el `<style>` inline de cada página y en ninguna parte del CSS compartido") y de nuevo el 2026-07-14 en 2 páginas más. Cada vez el "fix" fue manual y por-página, así que la siguiente página nueva/editada podía volver a traer el valor viejo. Además, verificado en vivo HOY (2026-07-15) contra los 3 CSS servidos: **`.breadcrumb-item.active{color:#6c757d}` SIGUE en la hoja compartida** (4.44-4.45:1, bajo AA 4.5:1) — la propia corrida del 07-14 lo detectó y lo dejó explícitamente `"arreglado": false, "pendiente": true` por ser "un cambio site-wide fuera de alcance de una sola corrida", y nunca se promovió a `BACKLOG.jsonl` (no aparece ahí) — quedó huérfano. Ninguno de los dos vive hoy en `check-plantilla.py`: el propio docstring del archivo dice explícitamente "Lo subjetivo (contraste...) NO está aquí" — pero esto YA NO es subjetivo, es un par (selector, color prohibido) conocido y medido 5 veces.
**Evidencia:** `data/HISTORIAL.jsonl` — `a11y-breadcrumb-color-inline-20260709`, `a11y-regresion-breadcrumb-color-20260713`, `a11y-breadcrumb-color-regresion-20260714` (las 3 con `#E36414`→`#C2410C`), `a11y-breadcrumb-active-contraste-marginal-20260714` (`"pendiente": true`, sin fix). Verificado en vivo: `grep -o '\.breadcrumb-item\.active[^}]*}' styles.css styles.min.css styles.7f293647.css` → `.breadcrumb-item.active{color:#6c757d}` en las 3, HOY. `grep "6c757d" data/BACKLOG.jsonl` → 0 resultados (nunca se abrió tarea).
**Propuesta:** (1) Checker nuevo (check 19 de `check-plantilla.py`) con una DENYLIST explícita de `(selector, color prohibido, color correcto)` — arranca con los 2 pares ya medidos 5 veces — que marca cualquier página cuyo `<style>` inline traiga el valor prohibido, MÁS un check global que vigila las 3 hojas compartidas (así el `.breadcrumb-item.active` actual sale ALTA/MEDIA en la próxima corrida en vez de seguir invisible). (2) Auto-fixer gemelo (página + asset) que corrige automáticamente al valor correcto, reutilizando el bump de `?v=`/sw.js ya existente para el asset fixer. Ámbito deliberadamente ESTRECHO (solo los 2 pares ya evidenciados) — no es contraste general, es cerrar una clase de bug específica y ya medida.
**DRAFT (listo para merge — 1/3 pegar en `.pipeline/check-plantilla.py`, dentro de `check_page()` justo antes de `# ================================================================ CHECK global: paridad CSS`, y añadir un nuevo check global + su llamada en `main()`):**
```python
    # --- 19. denylist de (selector, color prohibido): pares que YA regresaron 3+ veces por
    #     vivir duplicados en <style> INLINE por-página en vez de las 3 hojas compartidas (nunca
    #     se centralizaron -> cada página nueva/editada podía traer el valor viejo). Ver
    #     REGLAS.md (CSS/PARIDAD, consolidada 2026-06-19/2026-07-13) e HISTORIAL
    #     a11y-breadcrumb-color-inline-20260709 / -regresion-...-20260713 / -...-20260714.
    for block in re.findall(r'<style\b[^>]*>(.*?)</style>', t, re.S | re.I):
        for sel, bad, good, evidencia in DENYLIST_COLOR:
            if re.search(re.escape(sel) + r'\s*\{[^}]*\bcolor\s*:\s*' + re.escape(bad) + r'\b', block, re.I):
                add("media", r, "a11y",
                    "%s con color:%s INLINE en el <style> de esta página (%s)" % (sel, bad, evidencia),
                    "Cambiar a color:%s (ya es el valor correcto en las 3 hojas compartidas); "
                    "mejor aún, borrar el bloque <style> inline duplicado y dejar que herede de "
                    "styles*.css (la duplicación es la causa raíz de la reincidencia)" % good)
```
```python
# Denylist compartida entre el check de página (19) y el check global de las 3 hojas.
# Cada par ya reincidió como bug real medido con Chrome headless -- no es un umbral de
# contraste general, es cerrar UNA clase de bug ya vista 3+ veces.
DENYLIST_COLOR = (
    (".breadcrumb-item a", "#E36414", "#C2410C",
     "3.26-3.27:1, falla AA 4.5:1 -- reincidió 2026-07-09/07-13/07-14"),
    (".breadcrumb-item.active", "#6c757d", "#475569",
     "4.44-4.45:1, justo bajo AA 4.5:1 -- sigue en las 3 hojas compartidas HOY, marcado "
     "pendiente 2026-07-14 sin fix"),
)


# ================================================================ CHECK global: denylist de color en las 3 hojas compartidas
def check_denylist_color_css():
    for c in sorted(glob.glob(os.path.join(ROOT, "styles*.css"))):
        css = read(c)
        for sel, bad, good, evidencia in DENYLIST_COLOR:
            if re.search(re.escape(sel) + r'\s*\{[^}]*\bcolor\s*:\s*' + re.escape(bad) + r'\b', css, re.I):
                add("media", rel(c), "a11y",
                    "%s sigue con color:%s en la hoja compartida (%s)" % (sel, bad, evidencia),
                    "Cambiar a color:%s en styles.css + styles.min.css + styles.<hash>.css, "
                    "bump ?v= en las páginas y CACHE_NAME en sw.js" % good)
```
```diff
--- a/.pipeline/check-plantilla.py
+++ b/.pipeline/check-plantilla.py
@@ def main():
     check_css_parity()
     check_rating_consistency()
+    check_denylist_color_css()
```
**DRAFT (2/3 — auto-fixer gemelo en `.pipeline/auto-fixers.py`; función compartida por el fixer de página y el asset fixer, reutiliza el bump ?v=/sw.js ya existente en `cmd_run_assets`):**
```python
# ── denylist de (selector, color prohibido) YA reincidente 3+ veces (check 19 de
#    check-plantilla.py / check_denylist_color_css). Misma función sirve para el <style>
#    inline de una página Y para el CSS compartido -- el patrón solo ancla en el texto
#    "selector{...color:bad" y es agnóstico de si eso vive dentro de HTML o de un .css. ──
_DENYLIST_COLOR = (
    (".breadcrumb-item a", "#E36414", "#C2410C"),
    (".breadcrumb-item.active", "#6c757d", "#475569"),
)

def _det_denylist_color(h):
    return any(
        re.search(re.escape(sel) + r'\s*\{[^}]*?\bcolor\s*:\s*' + re.escape(bad) + r'\b', h, re.I)
        for sel, bad, good in _DENYLIST_COLOR)

def _fix_denylist_color(h):
    n = 0
    for sel, bad, good in _DENYLIST_COLOR:
        pat = re.compile(r'(' + re.escape(sel) + r'\s*\{[^}]*?\bcolor\s*:\s*)' + re.escape(bad) + r'\b', re.I)
        h, k = pat.subn(r'\g<1>' + good, h)
        n += k
    return h, n
```
```diff
--- a/.pipeline/auto-fixers.py
+++ b/.pipeline/auto-fixers.py
@@ FIXERS = [
     ("ancla-servicio", "ancla cuyo TEXTO nombra un servicio real pero el HREF apunta a otro destino → corrige al href canónico (regresión 3x, check 14 de check-plantilla.py)",
      "mecanico", None, None),  # caso especial en cmd_run(): necesita page_dir para resolver hrefs relativos
+    ("denylist-color-inline", "color prohibido conocido (.breadcrumb-item a #E36414, .breadcrumb-item.active #6c757d) duplicado en <style> inline de la página → valor AA-safe centralizado (regresión 3x, check 19 de check-plantilla.py)",
+     "mecanico", _det_denylist_color, _fix_denylist_color),
 ]
@@ ASSET_FIXERS = [
     ("tap-target-44",
      "tap target <44px en selectores interactivos compartidos (migas) → min-height:44px en los 3 CSS + bump sw.js",
      "mecanico", _fix_tap_target),
+    ("denylist-color-css",
+     "color prohibido conocido (.breadcrumb-item a, .breadcrumb-item.active) en las 3 hojas compartidas → valor AA-safe + bump sw.js",
+     "mecanico", _fix_denylist_color),
 ]
```
**DRAFT (3/3 — REGLAS.md, añadir a la regla existente en la línea 13 la referencia al checker nuevo para que quede AUTO-anotada como las demás):**
```diff
--- a/docs/REGLAS.md
+++ b/docs/REGLAS.md
@@
-- [2026-06-11, consolidada 2026-06-19/2026-07-13/2026-07-14] CSS/PARIDAD: las 3 hojas (styles.css=fuente no servida; min/hash=servidas) deben tener las MISMAS reglas — `check-css-paridad.py`. Un fix que solo vive en un `<style>` inline por-página REGRESA al perder esa página su copia local (breadcrumb #E36414→#C2410C reincidió 3 veces, la última 2026-07-14) — centralizar SIEMPRE en las 3 hojas + bump ?v=/sw.js. Severidad: media.
+- [2026-06-11, consolidada 2026-06-19/2026-07-13/2026-07-14/2026-07-15] CSS/PARIDAD: las 3 hojas (styles.css=fuente no servida; min/hash=servidas) deben tener las MISMAS reglas — `check-css-paridad.py`. Un fix que solo vive en un `<style>` inline por-página REGRESA al perder esa página su copia local (breadcrumb #E36414→#C2410C reincidió 3 veces, la última 2026-07-14; `.breadcrumb-item.active` #6c757d sigue fallando AA hoy) — centralizar SIEMPRE en las 3 hojas + bump ?v=/sw.js. AUTO en `check-plantilla.py` check 19 (`check_denylist_color_css` + inline) + auto-fixer `denylist-color-inline`/`denylist-color-css`. Severidad: media.
```

## [PENDIENTE] costo/cuota — `recolecta-señales.py` marca "PICO" usando `total_tokens` crudo, dominado por `cache_read` barato — la alarma de costo no mide costo real   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** `sec_costos()` (línea 68) dispara "⚠️ PICO" cuando `total_tokens` de la última corrida supera 1.5× la mediana — pero `total_tokens` sale de sumar `input+output+cache_write+cache_read`, y `cache_read` (lectura de caché, ~10% del precio de un token normal) domina el total: en la corrida del 2026-07-14, de 148.1M tokens totales, 144.0M (97%) fueron `cache_read`. El propio `costos.jsonl` YA calcula `usd_equiv_api_ref` (el $ real, con precio por-modelo desde el 2026-07-09) en cada entrada, pero `sec_costos()` no lo usa para la alarma — así que el brief puede gritar "PICO" en una corrida barata (mucho cache, poco $ nuevo) y quedarse callado en una corrida cara con menos tokens pero de tipos caros. El propio brief de HOY lo confirma: marcó PICO en la corrida del 07-14 (148.1M tokens) mientras la corrida del 07-13 gastó MÁS $ real ($119.19 vs $77.23) con tokens totales similares (284.3M) y ni siquiera es la última.
**Evidencia:** `.pipeline/costos.jsonl` línea del 2026-07-14: `"cache_read_tokens":144043570` de `"total_tokens":148072897` (97.2%) con `"usd_equiv_api_ref":77.23`. Línea del 2026-07-13: `"usd_equiv_api_ref":119.19` (54% más caro en $ real) pero NO fue la que disparó el PICO de hoy porque ya no es la última corrida. `.pipeline/recolecta-señales.py` línea 62-69: `tot = [x.get("total_tokens", 0) for x in c]` y la comparación en línea 68 usa `tot`, nunca `usd_equiv_api_ref`.
**Propuesta:** Cambiar el disparador de PICO de `total_tokens` a `usd_equiv_api_ref` (el $ real que el propio pipeline ya calcula por-modelo desde 2026-07-09), y anotar cuando tokens-altos NO se traduce en $-alto (para no perder la señal de "corrida con mucho cache" como dato informativo, solo dejar de tratarla como alarma).
**DRAFT (listo para merge — reemplaza `sec_costos()` completa en `.pipeline/recolecta-señales.py`):**
```python
def sec_costos():
    c = _jsonl(".pipeline/costos.jsonl")
    print("## COSTO/CUOTA — uso por corrida (%d corridas registradas)" % len(c))
    if not c:
        print("  (sin datos)\n"); return
    tot = [x.get("total_tokens", 0) for x in c]
    usd = [x.get("usd_equiv_api_ref", 0) for x in c]
    ult = c[-1]
    mediana = sorted(tot)[len(tot) // 2]
    mediana_usd = sorted(usd)[len(usd) // 2]
    print("  Últimas corridas (M tokens): " + " · ".join("%.1f" % (t / 1e6) for t in tot[-6:]))
    print("  Últimas corridas (USD equiv): " + " · ".join("$%.0f" % x for x in usd[-6:]))
    print("  Mediana: %.1fM tok / $%.2f · última: %.1fM tok / $%.2f (%s)" % (
        mediana / 1e6, mediana_usd, ult.get("total_tokens", 0) / 1e6,
        ult.get("usd_equiv_api_ref", 0), ult.get("etiqueta", "")))
    ult_usd = ult.get("usd_equiv_api_ref", 0)
    if mediana_usd > 0 and ult_usd > 1.5 * mediana_usd:
        print("  ⚠️ PICO DE COSTO REAL ($): la última corrida costó >1.5× la mediana en USD → ¿qué la disparó?")
    elif ult.get("total_tokens", 0) > 1.5 * mediana and mediana > 0:
        print("  (nota: total_tokens fue >1.5× la mediana pero el $ real NO — probablemente "
              "cache_read barato, no es una alarma de costo real)")
    print()
```

## [HECHO 2026-07-13] infra — 5 revisores llaman `node` SIN el `export PATH` ya probado — el mismo bug ya reincidió 3 veces y solo 1 de 6 sitios de llamada quedó parcheado   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** `node` no está en el PATH por defecto del shell de los subagentes de este pipeline (a veces vive en `/usr/local/bin`, a veces en `/opt/homebrew/bin`). Esto YA causó 3 falsos "verificación ciega" ALTA distintos (infra-002 2026-06-12, perf-real-falsa-ciega 2026-06-21, infra-produccion-path-falso-ciego-20260710), y REGLAS.md tiene la regla desde el 2026-06-12 ("anteponer siempre `export PATH=\"/opt/homebrew/bin:$PATH\" &&` antes de `node ...` en agentes/hooks que lo invoquen"). Pero el fix solo se aplicó al PASO 1 de `revisor-produccion.md` (el agente que disparó el 3er incidente) — los OTROS 5 sitios donde un revisor invoca `node` en su PASO 1/prosa quedaron intactos: `revisor-e2e-funcional.md`, `revisor-infra-salud.md`, `revisor-perf-real.md`, `revisor-tracking.md` (los 4 con el mismo patrón exacto `PASO 1 — ejecuta exactamente:\n    node .pipeline/check-X.mjs`) y `revisor-gsc.md` (invoca `node mcp-local-seo/gsc-index.mjs` en prosa). Es la clase de bug que critico-sistema existe para cazar: una regresión YA identificada y YA mecanizada UNA vez, pero no propagada a sus hermanos — 5 revisores siguen en riesgo de producir el mismo falso ALTA con solo `git status`/reboot descolocando el PATH del shell.
**Evidencia:** `grep -rl "PATH=" .claude/agents/*.md` → SOLO `revisor-produccion.md`. `grep -L "PATH=" .claude/agents/*.md | xargs grep -l "node \|puppeteer\|Node.js"` → `revisor-e2e-funcional.md`, `revisor-gsc.md`, `revisor-infra-salud.md`, `revisor-perf-real.md`, `revisor-tracking.md` (verificado hoy, líneas exactas listadas abajo). REGLAS.md línea 32 (ampliada 2026-07-10) ya generaliza la regla a "agentes/hooks" — nunca se auditó contra el resto de `.claude/agents/*.md`.
**Propuesta:** Aplicar el MISMO parche ya probado en `revisor-produccion.md` (línea 13-14) a los otros 5 archivos: anteponer `export PATH="/opt/homebrew/bin:$PATH" && ` a la llamada de `node`, con la misma frase explicativa. Es texto puro en prompts de agente — cero riesgo de romper código, mismo patrón ya en producción hace 3 días sin incidentes.
**DRAFT (listo para merge — 4 diffs idénticos + 1 distinto para revisor-gsc):**
```diff
--- a/.claude/agents/revisor-e2e-funcional.md
+++ b/.claude/agents/revisor-e2e-funcional.md
@@
-PASO 1 — ejecuta exactamente:
-    node .pipeline/check-e2e.mjs
+PASO 1 — ejecuta exactamente (el `export PATH` es necesario: el shell de esta tarea a veces no hereda /opt/homebrew/bin, y sin él `node` da "command not found" que ANTES se reportaba como falso "verificación ciega" — incidente 2026-07-10):
+    export PATH="/opt/homebrew/bin:$PATH" && node .pipeline/check-e2e.mjs
```
```diff
--- a/.claude/agents/revisor-infra-salud.md
+++ b/.claude/agents/revisor-infra-salud.md
@@
-PASO 1 — ejecuta exactamente:
-    node .pipeline/check-infra.mjs
+PASO 1 — ejecuta exactamente (el `export PATH` es necesario: el shell de esta tarea a veces no hereda /opt/homebrew/bin, y sin él `node` da "command not found" que ANTES se reportaba como falso "verificación ciega" — incidente 2026-07-10):
+    export PATH="/opt/homebrew/bin:$PATH" && node .pipeline/check-infra.mjs
```
```diff
--- a/.claude/agents/revisor-perf-real.md
+++ b/.claude/agents/revisor-perf-real.md
@@
-PASO 1 — ejecuta exactamente:
-    node .pipeline/check-perf.mjs
+PASO 1 — ejecuta exactamente (el `export PATH` es necesario: el shell de esta tarea a veces no hereda /opt/homebrew/bin, y sin él `node` da "command not found" que ANTES se reportaba como falso "verificación ciega" — incidente 2026-07-10):
+    export PATH="/opt/homebrew/bin:$PATH" && node .pipeline/check-perf.mjs
```
```diff
--- a/.claude/agents/revisor-tracking.md
+++ b/.claude/agents/revisor-tracking.md
@@
-PASO 1 — ejecuta exactamente:
-    node .pipeline/check-tracking.mjs
+PASO 1 — ejecuta exactamente (el `export PATH` es necesario: el shell de esta tarea a veces no hereda /opt/homebrew/bin, y sin él `node` da "command not found" que ANTES se reportaba como falso "verificación ciega" — incidente 2026-07-10):
+    export PATH="/opt/homebrew/bin:$PATH" && node .pipeline/check-tracking.mjs
```
```diff
--- a/.claude/agents/revisor-gsc.md
+++ b/.claude/agents/revisor-gsc.md
@@
-- Si necesitas estado de indexación/sitemap de páginas clave, puedes ejecutar `node mcp-local-seo/gsc-index.mjs`.
+- Si necesitas estado de indexación/sitemap de páginas clave, puedes ejecutar `export PATH="/opt/homebrew/bin:$PATH" && node mcp-local-seo/gsc-index.mjs` (el `export PATH` es necesario: el shell de esta tarea a veces no hereda /opt/homebrew/bin — incidente 2026-07-10).
```

## [PENDIENTE] contenido — Catálogo `Service` en JSON-LD con `description` duplicada entre servicios distintos — REGLAS.md lo marca ALTA y dice literalmente "Sin checker aún"   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** REGLAS.md línea 51 (2026-07-08, CONTENIDO/SCHEMA, severidad ALTA) documenta un bug real: "un catálogo JSON-LD de varios `Service` embebido puede tener su `description` sobreescrita en bloque por error (todas las entidades con la del anfitrión)... Sin checker aún — revisar a mano el `@graph`." Es la única regla de severidad ALTA en todo REGLAS.md sin ningún checker anotado (todas sus vecinas dicen `AUTO en check-X.py`). Si una página nueva o un batch de edición vuelve a sobreescribir `description` en bloque (mismo patrón que ya pasó una vez), nada lo atrapa hasta revisión manual del `@graph`.
**Evidencia:** `grep -n "^- \[" docs/REGLAS.md | grep -vi AUTO` → línea 51 es la única de severidad `alta` sin checker (comparado con líneas 38/39/44/53/54 que sí son alta y sí tienen `AUTO`/mecanismo). Verificado en vivo con el script del draft contra las páginas actuales: **0 hallazgos hoy** (no hay regresión activa) — el valor es CERRAR la puerta, igual que el proceso ya usado para `twitter:url` (propuesta de arriba, mismo patrón "regla ya escrita, checker cierra la puerta").
**Propuesta:** Añadir un check GLOBAL a `check-plantilla.py` que, por cada bloque JSON-LD con `@graph`, agrupe las entidades `@type:"Service"` por su `description` exacta; si ≥2 servicios con `name` DISTINTO comparten la MISMA `description`, marca ALTA (coincide con la severidad ya asignada en REGLAS.md). Cero falsos positivos esperados: dos servicios reales nunca deberían tener el mismo texto de descripción palabra por palabra.
**DRAFT (listo para merge — pegar en `.pipeline/check-plantilla.py` justo ANTES de `# ================================================================ MAIN`, y añadir la llamada `check_service_catalog_description_dup()` en `main()` junto a `check_rating_consistency()`):**
```python
# ================================================================ CHECK global: catalogo Service con description duplicada
# Bug real 2026-07-08 (REGLAS.md, severidad alta, "Sin checker aun"): un catalogo JSON-LD de
# varios Service embebido en @graph tuvo su description sobreescrita en bloque por error --
# TODAS las entidades quedaron con la descripcion del anfitrion en vez de la propia.
def check_service_catalog_description_dup():
    for fpath in collect_pages():
        try:
            t = read(fpath)
        except Exception:
            continue
        for m in re.finditer(
                r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                t, re.S | re.I):
            try:
                data = json.loads(m.group(1))
            except Exception:
                continue
            graph = data.get("@graph") if isinstance(data, dict) else None
            if not isinstance(graph, list):
                continue
            servicios = []
            for item in graph:
                if not isinstance(item, dict):
                    continue
                tipo = item.get("@type")
                tipos = tipo if isinstance(tipo, list) else [tipo]
                if "Service" not in tipos:
                    continue
                nombre, desc = item.get("name"), item.get("description")
                if nombre and desc:
                    servicios.append((nombre, desc))
            if len(servicios) < 2:
                continue
            por_desc = {}
            for nombre, desc in servicios:
                por_desc.setdefault(desc, set()).add(nombre)
            for desc, nombres in por_desc.items():
                if len(nombres) >= 2:
                    add("alta", rel(fpath), "contenido",
                        "Catalogo Service en JSON-LD: %d servicios distintos (%s) comparten la MISMA description ('%s...') -- probable sobreescritura en bloque (REGLAS.md 2026-07-08)" % (
                            len(nombres), ", ".join(sorted(nombres)[:4]), desc[:60]),
                        "Restaurar la description PROPIA de cada Service (revisar el @graph a mano o el generador que lo produjo); ninguna debe copiar la del anfitrion ni la de otro servicio.")
```
```diff
--- a/.pipeline/check-plantilla.py
+++ b/.pipeline/check-plantilla.py
@@ def main():
     check_css_parity()
     check_rating_consistency()
+    check_service_catalog_description_dup()
```

## [PENDIENTE] seo — `twitter:url` se valida solo por PRESENCIA, no por VALOR (reincidió 3 veces con el HOME en vez del canonical)   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** El check 4f de `check-plantilla.py` (línea 380) solo verifica que `<meta name="twitter:url">` EXISTA en páginas de blog/colonia — nunca compara su VALOR contra el canonical. `check-indexabilidad.py` sí hace esa comparación para `og:url`, pero nadie la hace para `twitter:url`. Resultado: la misma clase de bug (twitter:url apuntando al HOME en vez de la página) reincidió DESPUÉS de que el check de presencia ya existía.
**Evidencia:** HISTORIAL.jsonl: 2026-06-20 "twitter:url apuntaba a la home... viola canon[ical]"; 2026-07-08 "twitter:url apuntaba a la home en vez del canonical de la página"; 2026-07-09 "instalacion-de-boiler: twitter:url apuntaba al home en vez del canonical. emergencia-24-7 y reparacion-de-boiler[igual]" — 3 recurrencias, la última DOS páginas a la vez, todas DESPUÉS del check de presencia (mecanizado 2026-06-27 por bk-546d0a06). Verificado en vivo con el script de abajo contra las 86 páginas actuales: 0 hallazgos ahora mismo (ya las arreglaron a mano) — el valor de este checker es CERRAR la puerta para que no sea necesaria una 4ª ronda manual.
**Propuesta:** Añadir un check GLOBAL (paralelo a `check_rating_consistency`) que, para toda página indexable con `<link rel="canonical">`, compare el `content` de `<meta name="twitter:url">` (si existe) contra el canonical y marque MEDIA si difieren.
**DRAFT (listo para merge — pegar en `.pipeline/check-plantilla.py` justo ANTES de `# ================================================================ CHECK global: aggregateRating`, y añadir la llamada `check_twitter_url_canonical()` en `main()` junto a `check_rating_consistency()`):**
```python
# ================================================================ CHECK global: twitter:url == canonical
# El check 4f (arriba) solo valida que <meta name="twitter:url"> EXISTA -- nunca su VALOR.
# Bug real recurrente (20260620, 20260708, 20260709): twitter:url apuntaba al HOME en vez del
# canonical de la pagina; al compartir en X/Twitter la tarjeta enlaza a la URL equivocada.
def check_twitter_url_canonical():
    for fpath in collect_pages():
        try:
            t = read(fpath)
        except Exception:
            continue
        if has_noindex(t):
            continue
        mc = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', t, re.I)
        if not mc:
            continue  # sin canonical -- ya lo caza check-indexabilidad
        canonical = mc.group(1)
        mt = re.search(r'<meta[^>]*name=["\']twitter:url["\'][^>]*content=["\']([^"\']+)["\']', t, re.I)
        if not mt:
            mt = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']twitter:url["\']', t, re.I)
        if mt and mt.group(1) != canonical:
            add("media", rel(fpath), "seo",
                "twitter:url (%s) != canonical (%s) -- la tarjeta de X/Twitter enlaza a la URL equivocada" % (mt.group(1), canonical),
                "Corregir <meta name=\"twitter:url\" content=\"%s\">" % canonical)
```
```diff
--- a/.pipeline/check-plantilla.py
+++ b/.pipeline/check-plantilla.py
@@ def main():
     check_css_parity()
     check_rating_consistency()
+    check_twitter_url_canonical()
```

## [PENDIENTE] seo — Coordenada GPS GENÉRICA del centro en páginas de zona/colonia — la regla existe desde 2026-06-11 pero JAMÁS se mecanizó (impacto A · esfuerzo M · riesgo bajo)
**Problema:** REGLAS.md tiene la regla desde el 2026-06-11 ("cada página local debe tener coordenadas GPS reales y únicas, no la coordenada genérica del centro repetida — es señal de doorway"), pero es de las POCAS reglas de esa lista SIN `AUTO en check-X.py` anotado. Reincidió 3 veces (2026-06-30, 2026-07-07, 2026-07-08) y sigue sin arreglar HOY: verificado en vivo, las 4 páginas de zona (`plomero-zona-norte/sur/oriente/poniente-culiacan`) + `plomero-centro-culiacan` comparten LITERALMENTE la misma `geo.position`/`ICBM` (24.7903;-107.3878), y la colonia `barrio-estacion` tiene esa misma latitud/longitud genérica en su JSON-LD (mientras sus 24 colonias hermanas SÍ tienen coordenadas únicas: amorada=24.8352, barrancos=24.7544, centro=24.8093...).
**Evidencia:** `grep -rl "24.7903" servicios/ | grep -E "zona-(norte|sur|oriente|poniente)|centro-culiacan|colonia"` → 6 páginas HOY (verificado con el script del draft, 0 falsos positivos: se acotó a páginas que EXPLÍCITAMENTE representan una zona/colonia, no a páginas de servicio city-wide como `destape-de-drenajes` donde un centro genérico es defendible).
**Propuesta:** Añadir un check GLOBAL que, solo para páginas cuyo slug indica una zona/colonia específica (`zona-{norte,sur,oriente,poniente}-culiacan`, `centro-culiacan`, o bajo `/plomero-colonias-culiacan/`), marque MEDIA si `geo.position`/`ICBM`/JSON-LD `latitude`+`longitude` coinciden con el valor genérico conocido del centro (24.7903,-107.3878).
**DRAFT (listo para merge — pegar en `.pipeline/check-plantilla.py` junto a `check_twitter_url_canonical()`, y añadir la llamada `check_geo_generica()` en `main()`):**
```python
# ================================================================ CHECK global: geo generica en zona/colonia
# REGLAS.md 2026-06-11: cada pagina LOCAL debe tener coordenadas GPS reales y unicas, no la
# generica del centro (senal de doorway). Reincidio 3 veces (20260630/0707/0708) SIN checker.
CENTRO_LAT = "24.7903"
CENTRO_LON = "-107.3878"


def _es_pagina_local_especifica(r):
    return bool(re.search(
        r'zona-(norte|sur|oriente|poniente)-culiacan|centro-culiacan|/plomero-colonias-culiacan/',
        r))


def check_geo_generica():
    for fpath in collect_pages():
        r = rel(fpath)
        if not _es_pagina_local_especifica(r):
            continue
        try:
            t = read(fpath)
        except Exception:
            continue
        if has_noindex(t):
            continue
        fuentes = []
        mp = re.search(r'<meta[^>]*name=["\']geo\.position["\'][^>]*content=["\']([^"\']+)["\']', t, re.I)
        if mp and CENTRO_LAT in mp.group(1) and CENTRO_LON in mp.group(1):
            fuentes.append("meta geo.position")
        mi = re.search(r'<meta[^>]*name=["\']ICBM["\'][^>]*content=["\']([^"\']+)["\']', t, re.I)
        if mi and CENTRO_LAT in mi.group(1) and CENTRO_LON in mi.group(1):
            fuentes.append("meta ICBM")
        mlat = re.search(r'"latitude"\s*:\s*(-?[0-9.]+)', t)
        mlon = re.search(r'"longitude"\s*:\s*(-?[0-9.]+)', t)
        if mlat and mlon and mlat.group(1) == CENTRO_LAT and mlon.group(1) == CENTRO_LON:
            fuentes.append("JSON-LD latitude/longitude")
        if fuentes:
            add("media", r, "seo",
                "Coordenada GENERICA del centro de Culiacan (%s,%s) en %s -- esta pagina representa "
                "una zona/colonia especifica y deberia tener su coordenada REAL, no la generica "
                "(senal de doorway, REGLAS 2026-06-11)" % (CENTRO_LAT, CENTRO_LON, " + ".join(fuentes)),
                "Poner la coordenada REAL de la zona/colonia (lat/lon real del area que atiende esta "
                "pagina) en meta geo.position/ICBM y JSON-LD GeoCoordinates, no la generica del centro")
```
```diff
--- a/.pipeline/check-plantilla.py
+++ b/.pipeline/check-plantilla.py
@@ def main():
     check_css_parity()
     check_rating_consistency()
     check_twitter_url_canonical()
+    check_geo_generica()
```

## [PENDIENTE] contenido — Garantía contradictoria DENTRO de la misma página — la regla agrupa "garantía, precio o rating" pero el checker (check 15) solo cubre rating   (impacto M · esfuerzo S · riesgo medio — heurística, requiere revisión humana antes de tocar copy)
**Problema:** REGLAS.md (2026-07-07, ampliada 2026-07-09) dice explícitamente "garantía, **precio** o aggregateRating no puede contradecirse... AUTO en check-plantilla.py check 15 (rating, site-wide)" — pero el check 15 real (línea 653, `check_rating_consistency`) SOLO mira `ratingValue`/`reviewCount`. Garantía quedó fuera pese a estar nombrada en la misma regla, y reincidió 3 veces DESPUÉS de escrita la regla (2026-07-07, 07-08, 07-09).
**Evidencia:** Corrida en vivo del regex del draft contra las 86 páginas: **5 páginas HOY** con dos duraciones de garantía DISTINTAS en el mismo `<body>` — `precios/index.html` (30 días vs 3 meses), `servicios/desazolve-de-drenajes/index.html` y `servicios/plomero-cerca-de-mi/index.html` (6 meses vs 1 año), y 2 posts de blog (3 vs 6 meses; 6 vs 24 meses). El regex EXCLUYE a propósito "garantía del fabricante"/marcas (Noritz, Rheem) para no confundir la garantía del PRODUCTO con la del SERVICIO — sin ese filtro salían 10 falsos positivos en vez de 5.
**Propuesta:** Checker heurístico de severidad BAJA (no ALTA: puede haber garantías legítimamente distintas por línea de servicio) que solo AVISA — el `fix_sugerido` pide confirmar a mano antes de unificar, igual que ya hace la regla 2026-07-08 del catálogo JSON-LD ("revisar a mano").
**DRAFT (listo para merge — pegar en `.pipeline/check-plantilla.py` junto a los checks anteriores, y añadir la llamada `check_garantia_intra_pagina()` en `main()`):**
```python
# ================================================================ CHECK global: garantia contradictoria intra-pagina
# REGLAS.md 2026-07-07/09 agrupa "garantia, precio o rating" pero solo rating se mecanizo
# (check 15). Heuristica de severidad BAJA: extrae menciones "garantia + duracion", normaliza
# a dias y avisa si la MISMA pagina trae >=2 valores distintos. Excluye "garantia del
# fabricante"/marcas (producto, no servicio) para no confundir dos garantias legitimamente
# distintas. NO autocorrige: el fix pide confirmar a mano (mismo criterio que REGLAS 2026-07-08
# para el catalogo JSON-LD de Service).
_DUR_DIAS_UNIDAD = {"dia": 1, "dias": 1, "mes": 30, "meses": 30, "ano": 365, "anos": 365}
_GARANTIA_EXCLUYE = ("fabricante", "noritz", "rheem", "bosch", "extendida")
_RE_GARANTIA_1 = re.compile(r'garant[ií]a[^.<]{0,40}?(\d+)\s*(d[ií]as?|mes(?:es)?|a[ñn]os?)', re.I)
_RE_GARANTIA_2 = re.compile(r'(\d+)\s*(d[ií]as?|mes(?:es)?|a[ñn]os?)[^.<]{0,40}?garant[ií]a', re.I)


def _normaliza_duracion(num, unidad):
    u = unidad.lower().replace("í", "i").replace("ñ", "n")
    for clave, dias in _DUR_DIAS_UNIDAD.items():
        if u.startswith(clave):
            return int(num) * dias
    return None


def check_garantia_intra_pagina():
    for fpath in collect_pages():
        r = rel(fpath)
        try:
            t = read(fpath)
        except Exception:
            continue
        if has_noindex(t):
            continue
        hallados = {}
        for rx in (_RE_GARANTIA_1, _RE_GARANTIA_2):
            for m in rx.finditer(t):
                frag = m.group(0).lower()
                if any(x in frag for x in _GARANTIA_EXCLUYE):
                    continue
                dias = _normaliza_duracion(m.group(1), m.group(2))
                if dias:
                    hallados[dias] = m.group(0).strip()[:60]
        if len(hallados) >= 2:
            valores = "; ".join("'%s' (~%dd)" % (txt, d) for d, txt in sorted(hallados.items()))
            add("baja", r, "contenido",
                "Garantia con valores DISTINTOS en la misma pagina: %s -- puede ser una "
                "contradiccion real o garantias legitimas de lineas de servicio distintas" % valores,
                "Revisar A MANO si es contradiccion (unificar al valor mayoritario del sitio, "
                "REGLAS 2026-07-07) o si son garantias distintas legitimas por servicio/tier; "
                "NO autocorregir sin confirmar")
```
```diff
--- a/.pipeline/check-plantilla.py
+++ b/.pipeline/check-plantilla.py
@@ def main():
     check_css_parity()
     check_rating_consistency()
     check_twitter_url_canonical()
     check_geo_generica()
+    check_garantia_intra_pagina()
```

## [PENDIENTE] proceso — Backlog `requiere_humano` con una tarea ZOMBIE: `bk-12b83ae9` (reauth GSC) sigue abierta pese a estar resuelta desde el 2026-06-26   (impacto B · esfuerzo S · riesgo bajo)
**Problema:** `bk-12b83ae9` ("Re-autenticar mcp-local-seo/gsc-token.json") sigue `estado: requiere_humano` en `data/BACKLOG.jsonl`, pero el problema real se resolvió hace 14 días SIN necesidad de re-autenticación: HISTORIAL.jsonl 2026-06-26 registra "GSC REVIVIO via MCP" copiando credenciales vivas de `~/gsc-mcp/` sobre `mcp-local-seo/{client_secret,gsc-token}.json" (sin re-login al cliente OAuth muerto). `check-infra.mjs` ya devuelve `{"hallazgos":[]}` para el sensor GSC. La tarea es ruido puro: cada corrida que lea el backlog (y el brief de `recolecta-señales.py`) sigue reportándola como pendiente de decisión humana cuando no hay decisión que tomar.
**Evidencia:** `data/BACKLOG.jsonl` bk-12b83ae9 creada 2026-06-22, `cerrado: null` HOY (2026-07-10, 18 días abierta); HISTORIAL 2026-06-26 documenta la resolución real; memoria del propio pipeline (`mcp-local-seo-token.md`) confirma "Resuelto 2026-06-26 SIN re-login". Nota: la propuesta pendiente de este mismo archivo ("Mostrar la EDAD de las tareas requiere_humano") habría mostrado esta tarea con 18 días y ⚠️ ATASCADA — pero eso solo la haría más VISIBLE, no la cierra: sigue siendo ruido porque el objeto ya no aplica.
**Propuesta:** Cerrar la tarea con el comando propio de `gestor-backlog.py` (no requiere código nuevo — el comando `close` ya existe, línea 167).
**DRAFT (listo para pegar/ejecutar):**
```bash
python3 .pipeline/gestor-backlog.py close --id bk-12b83ae9 --estado descartado --nota "Resuelto 2026-06-26 sin re-auth: credenciales vivas de ~/gsc-mcp copiadas sobre mcp-local-seo/. check-infra.mjs ya da GSC ok. Ver HISTORIAL 2026-06-26."
```

---

## [PENDIENTE] infra — Logs compartidos entre sitios: el catch-up y el sensor de frescura del cron pueden leer al ELECTRICISTA como si fuera el Plomero   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** Los dos sitios (Plomero y Electricista) escriben sus logs de corrida con el MISMO nombre (`auto-agente-<stamp>.log`) en el MISMO directorio (`~/Library/Logs/mantener-sitio/`). Dos sensores del Plomero eligen "el log más nuevo" SIN filtrar por sitio: (1) `catchup.sh` (decide si recuperar una corrida saltada) y (2) `check-infra.mjs` checkCron (el dead-man's switch de "el cron está vivo"). Escenario de fallo: el LaunchAgent del Plomero muere, pero el Electricista sigue corriendo a diario → el catch-up dice "última corrida hace 0h, OK → sin acción" y check-infra dice "cron fresco" — el Plomero queda MUERTO EN SILENCIO, que es exactamente lo que estos dos sensores existen para impedir.
**Evidencia:** Verificado HOY (2026-07-06): `auto-agente-20260705-201428.log` en ese directorio es del ELECTRICISTA (lo escribió `/Users/openclaw/Sitios Web/Electricista Culiacán/.pipeline/crecer-diario.sh`, pid 78944; su `claude` reintentaba a las 11:13 con el prompt de electricistaculiacanpro.mx). El `crecer-diario.sh` del Electricista usa el MISMO `LOG_DIR="$HOME/Library/Logs/mantener-sitio"` (su línea 19) y el mismo patrón de nombre. Consumidores sin filtro en ESTE repo: `.pipeline/catchup.sh` línea 23 (`ls -t "$LOG_DIR"/auto-agente-2*.log …`) y `.pipeline/check-infra.mjs` línea 78 (`/^(run|auto-agente)-.*\.log$/`). El marcador `last-run-day` sí está namespaceado (`auto-agente-plomero-last-run-day`) — los logs no.
**Propuesta:** Namespacear el log del Plomero (`auto-agente-plomero-<stamp>.log`) y que los dos consumidores filtren por ese prefijo (+ `run-*.log` legado, que era exclusivo de este sitio). Espejo recomendado en el repo del Electricista (su log → `auto-agente-electricista-*`), pero el fix de ESTE repo ya lo protege solo.
**DRAFT (listo para merge — 3 parches + 1 migración):**
```bash
# ── Parche 1: .pipeline/crecer-diario.sh (línea 20) ──────────────────────────
# ANTES:
LOG="$LOG_DIR/auto-agente-$STAMP.log"
# DESPUÉS (namespacear: el electricista escribe auto-agente-*.log en el MISMO dir):
LOG="$LOG_DIR/auto-agente-plomero-$STAMP.log"

# ── Parche 2: .pipeline/catchup.sh (línea 23) ────────────────────────────────
# ANTES:
NEWEST=$(ls -t "$LOG_DIR"/auto-agente-2*.log "$LOG_DIR"/run-2*.log 2>/dev/null | head -1)
# DESPUÉS (solo logs del PLOMERO: prefijo nuevo + run-* legado, exclusivo de este sitio):
NEWEST=$(ls -t "$LOG_DIR"/auto-agente-plomero-2*.log "$LOG_DIR"/run-2*.log 2>/dev/null | head -1)

# ── Migración (UNA vez, junto con el merge): renombrar los logs históricos que
#    son del Plomero para que la frescura del cron no dé una ALTA falsa ese día.
#    Discriminador: solo el parte del Plomero dice "Auto Agente Plomero"/plomeroculiacanpro.
for f in "$HOME/Library/Logs/mantener-sitio"/auto-agente-2*.log; do
  [ -f "$f" ] || continue
  grep -ql "Auto Agente Plomero\|plomeroculiacanpro" "$f" \
    && mv "$f" "${f/auto-agente-/auto-agente-plomero-}"
done
# (Los que no matcheen quedan con el nombre viejo: inofensivo — ya no los mira nadie
#  del Plomero, y el primer cron tras el merge escribe el primer log con nombre nuevo.)
```
```js
// ── Parche 3: .pipeline/check-infra.mjs (línea 78, dentro de checkCron) ──────
// ANTES:
entries = fs.readdirSync(LOG_DIR).filter((f) => /^(run|auto-agente)-.*\.log$/.test(f));
// DESPUÉS (excluir los logs del electricista, que comparten directorio y prefijo):
entries = fs.readdirSync(LOG_DIR).filter((f) => /^(run-|auto-agente-plomero-).*\.log$/.test(f));
```

## [PENDIENTE] costo/visibilidad — `check-costos.py`: detectar el HUECO de días sin corrida y la CORRIDA ENANA que murió a medias   (impacto A · esfuerzo S · riesgo bajo)
**Problema:** Hoy el sistema lleva 4 días sin una corrida diaria COMPLETADA y ningún sensor lo dice: el 07-04 no corrió NADA (no hay fila en costos.jsonl — la diaria se saltó en silencio) y el 07-05 la corrida agotó sus 3 intentos de API ("Connection closed mid-response") dejando una fila enana que ningún detector actual distingue de un "día tranquilo". `check-costos.py` ya caza el 0 exacto (costo-000) y la corrida desbocada, pero un DÍA AUSENTE o una corrida al 12% de la mediana pasan limpios. `ESTADO.md` sigue diciendo "ultima_corrida: 2026-07-02".
**Evidencia:** `costos.jsonl`: existe `auto-agente 20260703-182515` y luego salta a `20260705-183943` — el 2026-07-04 no tiene fila. La del 07-05: output 25,861 tokens / 48 mensajes vs mediana 216,528 / ~300 (12% — su log `auto-agente-20260705-183943.log` muestra los 3 intentos fallidos), y dejó la rama `auto/diario-20260705-2032` con trabajo sin commitear. `catchup.log` no registra nada desde el 06-24 (solo dispara al boot; la Mac duerme, no se reinicia).
**Propuesta:** Añadir a `check-costos.py` dos detectores: (1) HUECO — si entre las dos últimas corridas hay >1 día calendario, hallazgo (alta si faltan ≥2 días); (2) ENANA — si la última corrida tiene `output_tokens` > 0 pero < 25% de la mediana previa (calibrado: caza el 25.8k del 07-05 con mediana 216k, sin marcar la corta legítima de 102k del 07-02), hallazgo media con la instrucción de ADOPTAR el trabajo huérfano de su rama (patrón ya usado el 2026-07-02).
**DRAFT (listo para merge — pegar en `.pipeline/check-costos.py` DESPUÉS del bloque costo-000 y ANTES del `print(json.dumps(...))` final):**
```python
    # ── HUECO de días y CORRIDA ENANA (familia 20260704/20260705): una diaria que NO
    #    ocurrió (Mac apagada, launchd sin disparar, catch-up ciego) no deja NINGUNA
    #    fila; una que murió a medias (reintentos de API agotados) deja una fila enana.
    #    En ambos casos ESTADO.md se queda viejo y nadie lo nota hasta a ojo.
    import datetime as _dt
    import re as _re

    def _dia_corrida(fila):
        # El día REAL va en la etiqueta ("auto-agente 20260705-183943"); "fecha" es
        # cuándo se recolectó el costo (a veces el día siguiente).
        m = _re.search(r"(20\d{6})-\d{6}", fila.get("etiqueta", "") or "")
        if m:
            s = m.group(1)
            try:
                return _dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
            except ValueError:
                pass
        try:
            return _dt.date.fromisoformat(fila.get("fecha", "") or "")
        except ValueError:
            return None

    dias = [d for d in (_dia_corrida(f) for f in filas) if d]
    if len(dias) >= 2 and (dias[-1] - dias[-2]).days > 1:
        perdidos = (dias[-1] - dias[-2]).days - 1
        hallazgos.append({
            "id": "costo-hueco", "archivo": ".pipeline/costos.jsonl", "linea": 0,
            "severidad": "alta" if perdidos >= 2 else "media", "categoria": "costo",
            "descripcion": "HUECO de corridas: entre %s y %s NO hubo corrida diaria (%d día(s) sin fila en costos.jsonl). La diaria se saltó en silencio (Mac apagada / launchd sin disparar / catch-up ciego)." % (
                dias[-2], dias[-1], perdidos),
            "fix_sugerido": "Revisar ~/Library/Logs/mantener-sitio/ y catchup.log de esos días; confirmar que el LaunchAgent y el catch-up están cargados (launchctl list | grep plomero).",
        })
    if len(filas) > MIN_HIST:
        u = filas[-1]
        cur = u.get("output_tokens", 0) or 0
        med = _mediana([f.get("output_tokens", 0) or 0 for f in filas[:-1]])
        if med > 0 and 0 < cur < 0.25 * med:
            hallazgos.append({
                "id": "costo-enana", "archivo": ".pipeline/costos.jsonl", "linea": 0,
                "severidad": "media", "categoria": "costo",
                "descripcion": "CORRIDA ENANA: la última (%s) generó output=%s, %.0f%% de la mediana (%s) — firma de corrida que MURIÓ A MEDIAS (reintentos de API agotados), no de día tranquilo." % (
                    u.get("etiqueta", "?"), f"{cur:,}", 100.0 * cur / med, f"{int(med):,}"),
                "fix_sugerido": "Revisar el log auto-agente-*.log de esa corrida y su rama auto/diario-*: puede haber trabajo a medio commitear que la corrida de hoy debe ADOPTAR o descartar (patrón ya usado el 2026-07-02).",
            })
```

## [PENDIENTE] infra — Reintentos del driver con deadline de RELOJ DE PARED (el `sleep` se pausa cuando la Mac duerme)   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** El backoff del loop de reintentos de `crecer-diario.sh` usa `sleep 120/240`, pero `sleep` se PAUSA cuando la Mac se duerme: un "reintento en 240s" puede ejecutarse horas después, en la madrugada o al día siguiente — compitiendo por cuota y solapándose con el meta-pase o con la corrida diaria siguiente. Un intento que despierta 15 horas tarde ya no es "la corrida de hoy" y no debería correr.
**Evidencia:** `auto-agente-20260705-183943.log`: intento 2 @ 19:31, "reintento en 240s" → intento 3 @ **03:06:13** (7h35m después). El gemelo electricista (mismo driver): intento 1 @ 20:14 del 07-05, "reintento en 120s" → intento 2 @ **11:13:49 del 07-06** (15 h después), corriendo HOY en paralelo con los dos meta-pases de las 11:12.
**Propuesta:** Deadline de reloj de pared: si al despertar del `sleep` ya pasaron >3h desde `RUN_START`, abandonar los reintentos (el propio driver ya promete "el catch-up o la corrida de mañana lo recuperan" en su email de fallo — esto lo hace verdad). Espejo recomendado en el driver del Electricista.
**DRAFT (listo para merge — 2 toques a `.pipeline/crecer-diario.sh`):**
```bash
# ── Toque 1: justo DESPUÉS de la línea  RUN_START=$(date +%s)   (línea ~50) ──
# Deadline de RELOJ DE PARED para los reintentos: `sleep` se pausa si la Mac duerme
# (2026-07-05: "reintento en 240s" ejecutado 7h35m después, a las 03:06; el gemelo
# electricista: "120s" → 15h después, solapado con el meta-pase del día siguiente).
RETRY_DEADLINE=$((RUN_START + 3*3600))

# ── Toque 2: en el loop de reintentos, REEMPLAZAR este bloque: ────────────────
  if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
    WAIT=$((attempt * 120))   # backoff: 120s, luego 240s
    echo "[$STAMP] Error $FAIL_KIND (NO de cuota); reintento en ${WAIT}s." >> "$LOG"
    sleep "$WAIT"
  else
# ── por este (solo se AÑADE el if tras el sleep): ─────────────────────────────
  if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
    WAIT=$((attempt * 120))   # backoff: 120s, luego 240s
    echo "[$STAMP] Error $FAIL_KIND (NO de cuota); reintento en ${WAIT}s." >> "$LOG"
    sleep "$WAIT"
    if [ "$(date +%s)" -gt "$RETRY_DEADLINE" ]; then
      echo "[$STAMP] Desperté FUERA de la ventana de la corrida (>3h desde el inicio: la Mac durmió durante el sleep). Abandono los reintentos; el catch-up o la corrida de mañana lo recuperan." >> "$LOG"
      break
    fi
  else
```

## [PENDIENTE] proceso — Mostrar la EDAD de las tareas `requiere_humano` en el brief (2 llevan 14 y 17 días esperando)   (impacto M · esfuerzo S · riesgo bajo)
**Problema:** `recolecta-señales.py` imprime "⏳ esperando decisión humana: 2" pero NO cuánto llevan esperando. Una tarea humana de 2 días y una de 17 se ven igual, así que ni el meta-pase ni el parte diario escalan las que se pudren — y una de ellas mantiene un SENSOR ciego mientras espera.
**Evidencia:** `data/BACKLOG.jsonl`: bk-218a5844 (doorway domicilio/cerca-de-mi, Jaccard 0.85) creada 2026-06-19 → **17 días**; bk-12b83ae9 (re-auth token GSC del CLI) creada 2026-06-22 → **14 días**, y mientras tanto `check-infra.mjs` sigue dando ALTA de "GSC ciego" en cada corrida. El bloque actual (sec_backlog, líneas 86-89) solo lista los objetivos.
**Propuesta:** Que el brief imprima la edad en días de cada tarea `requiere_humano` y marque ⚠️ las >7 días, para que el parte al dueño las repita hasta que decida.
**DRAFT (listo para merge — en `.pipeline/recolecta-señales.py`, sec_backlog(), REEMPLAZAR el bloque `hum` de las líneas 86-89):**
```python
    hum = [t for t in b if t.get("estado") == "requiere_humano"]
    if hum:
        hoy = date.today()
        print("  ⏳ esperando decisión humana: %d" % len(hum))
        for t in hum:
            edad = ""
            try:
                dias = (hoy - date.fromisoformat((t.get("creado") or "")[:10])).days
                edad = " — lleva %d días%s" % (
                    dias, "  ⚠️ ATASCADA >7d → repetirla en el parte al dueño" if dias > 7 else "")
            except ValueError:
                pass
            print("    %s [%s] %s%s" % (t.get("id"), t.get("tipo"), t.get("objetivo", "?"), edad))
```

## [HECHO 2026-07-03] infra — Cerrar la forma B (open/`_jsonl` literal) de la clase "rutas rotas"   (impacto A · esfuerzo S · riesgo bajo)
> ✅ Mergeada: `.pipeline/check-rutas-pipeline.py` reemplazado con el detector de forma B. Verificado: 51 archivos analizados, 0 rutas rotas; check-infra.mjs lo acepta (0 hallazgos, sin ALTA falsa).
**Problema:** La clase de regresión "rutas post-reorganización" ya reincidió DOS veces seguidas (infra-006 el 06-30, infra-007 el 07-02). El checker `check-rutas-pipeline.py` que se mecanizó en infra-007 **solo caza la forma `os.path.join(ROOT, "lit.ext")`** (forma A). Pero infra-006 —el que dejó el backlog reportando "0 tareas" durante días sin que nadie lo notara— fue la **forma B**: un literal relativo pasado directo a un helper (`_jsonl("BACKLOG.jsonl")`, SIN `ROOT`). Esa forma B sigue sin red: si mañana otro `open("data/algo.jsonl")` apunta a una ruta movida, nadie lo caza hasta que un síntoma aparece a ojo.
**Evidencia (brief):** 14 regresiones en HISTORIAL; **2 de ellas (infra-006, infra-007) son esta misma clase en las 2 corridas más recientes**. El checker actual (líneas 23-52) exige `node.args[0] == ROOT` → estructuralmente nunca ve la forma B.
**Propuesta:** Extender `check-rutas-pipeline.py` con un segundo detector AST que cace literales de string pasados como PRIMER argumento a `open(...)` o `_jsonl(...)` en **modo lectura**, con extensión de datos/config conocida (`.jsonl/.json/.md/.txt/.csv/.sh/.yml/.yaml`) que no resuelva desde `ROOT`. Se excluyen `.html/.css/.js/.webp` (se abren contra un base de página ya calculado → ruido) y el modo escritura/crear (`w/a/x`, donde que el archivo no exista es legítimo). Sigue emitiendo el mismo contrato `{"hallazgos":[...]}`.
**DRAFT (listo para merge — reemplaza `.pipeline/check-rutas-pipeline.py` completo):**
```python
#!/usr/bin/env python3
"""Checker DETERMINISTA: rutas hardcodeadas rotas en .pipeline/*.py y scripts/*.py.

Caza la clase de regresión "rutas post-reorganización" (REGLAS.md, familia
infra-006/infra-007/0d3fb737): una ruta literal que apuntaba a la raíz antes de
que el repo se reordenara en scripts/ + docs/ + data/, y que nadie actualizó al
mover el archivo real. DOS formas de la MISMA clase:

  A) os.path.join(ROOT, "BACKLOG.jsonl")                (forma infra-007)
  B) open("BACKLOG.jsonl") / _jsonl("BACKLOG.jsonl")    (forma infra-006: literal
     relativo pasado directo a open()/helper, SIN ROOT — el que dejó el backlog
     reportando "0 tareas" durante días)

Solo mira LITERALES (sin *, sin f-strings con variables) que terminan en una
extensión de DATOS/CONFIG conocida — evita falsos positivos con globs
(`servicios/*/index.html`) y con plantillas .html abiertas contra un base ya
resuelto. Emite el contrato común {"hallazgos":[...]} para que check-infra.mjs
lo recoja solo.
"""
import ast
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["scripts", ".pipeline"]
SELF = os.path.basename(__file__)

# Extensiones de datos/config que se resuelven contra la raíz del repo. Se
# excluyen .html/.webp/.css/.js a propósito (suelen abrirse contra un base de
# página ya calculado -> alto ruido).
EXT_DATOS = {".jsonl", ".json", ".md", ".txt", ".csv", ".sh", ".tsv", ".yml", ".yaml"}
# Funciones cuyo PRIMER argumento es una ruta de archivo relativa a la raíz.
OPEN_FUNCS = {"open", "_jsonl"}


def _es_literal_str(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def _modo_de_open(node):
    """Modo de una llamada open(path, mode=...) si es literal; 'r' por defecto."""
    if len(node.args) >= 2 and _es_literal_str(node.args[1]):
        return node.args[1].value
    for kw in node.keywords:
        if kw.arg == "mode" and _es_literal_str(kw.value):
            return kw.value
    return "r"


def _literal_join_paths(src):
    """Forma A: os.path.join(ROOT, "a", "b", ...) con literales tras ROOT."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        is_join = (isinstance(f, ast.Attribute) and f.attr == "join") or \
                  (isinstance(f, ast.Name) and f.id == "join")
        if not is_join or not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Name) and first.id == "ROOT"):
            continue
        parts, ok = [], True
        for a in node.args[1:]:
            if _es_literal_str(a):
                parts.append(a.value)
            else:
                ok = False
                break
        if ok and parts:
            found.append((os.path.join(*parts), node.lineno))
    return found


def _literal_open_paths(src):
    """Forma B: open("lit.ext") / _jsonl("lit.ext") — literal relativo directo,
    solo en modo LECTURA (crear/escribir un archivo que aún no existe es válido)."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        f = node.func
        name = f.id if isinstance(f, ast.Name) else (
            f.attr if isinstance(f, ast.Attribute) else None)
        if name not in OPEN_FUNCS:
            continue
        first = node.args[0]
        if not _es_literal_str(first):
            continue
        if name == "open" and any(c in _modo_de_open(node) for c in ("w", "a", "x")):
            continue  # escribe/crea -> que no exista es legítimo
        found.append((first.value, node.lineno))
    return found


def _ruta_rota(rel, ext_whitelist):
    if os.path.isabs(rel) or "*" in rel:
        return False
    ext = os.path.splitext(rel)[1].lower()
    if not ext:
        return False  # sin extensión -> probablemente un directorio
    if ext_whitelist is not None and ext not in ext_whitelist:
        return False
    return not os.path.exists(os.path.join(ROOT, rel))


def _hallazgo(seq, full, lineno, rel, forma):
    return {
        "id": f"rutas-{seq:03d}",
        "archivo": os.path.relpath(full, ROOT),
        "linea": lineno,
        "severidad": "alta",
        "categoria": "infra",
        "descripcion": (
            f"RUTA ROTA ({forma}): apunta a '{rel}', que no existe en el repo "
            "(posible regresión de rutas post-reorganización — familia infra-006/007)."
        ),
        "fix_sugerido": (
            f"Corregir la constante/llamada para que apunte a la ubicación real de "
            f"'{os.path.basename(rel)}'."
        ),
    }


def main():
    hallazgos = []
    analizadas = 0
    seq = 0
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if not name.endswith(".py") or name == SELF:
                continue
            full = os.path.join(base, name)
            try:
                src = open(full, encoding="utf-8").read()
            except OSError:
                continue
            analizadas += 1
            for rel, lineno in _literal_join_paths(src):
                if _ruta_rota(rel, None):        # forma A: cualquier extensión (como hoy)
                    seq += 1
                    hallazgos.append(_hallazgo(seq, full, lineno, rel, "join(ROOT, …)"))
            for rel, lineno in _literal_open_paths(src):
                if _ruta_rota(rel, EXT_DATOS):   # forma B: solo extensiones de datos
                    seq += 1
                    hallazgos.append(_hallazgo(seq, full, lineno, rel,
                                               "open()/_jsonl() literal relativo"))
    print(json.dumps({"hallazgos": hallazgos, "analizadas": analizadas},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

---

## [HECHO 2026-07-03] costo — Cazar la corrida de 0 tokens (medidor roto / corrida caída)   (impacto M · esfuerzo S · riesgo bajo)
> ✅ Mergeada: bloque `costo-000` añadido a `.pipeline/check-costos.py`. Verificado: dispararía sobre la fila real de 0 tokens (auto-agente 20260701-182502); 0 hallazgos hoy porque la última corrida tiene 22M tokens.
**Problema:** `check-costos.py` solo evalúa `total_tokens > 28M` sobre la última fila. Una fila con **`total_tokens: 0`** pasa como "todo bien" cuando en realidad significa lo contrario: el recolector de costos falló o la corrida no ejecutó. Es un fallo SILENCIOSO — un 0 se lee igual que "corrida barata". (Complementa, no reemplaza, la propuesta de "corrida desbocada" de abajo, que cubre el otro extremo.)
**Evidencia (brief de costo):** Las últimas 6 corridas fueron `654.2 · 26.6 · 24.9 · 66.2 · **0.0** · 22.1` M tokens. La fila `0.0` es real: `auto-agente 20260701-182502` con `total_tokens: 0` (verificado en `costos.jsonl`). Ninguna condición actual la marca.
**Propuesta:** Bloque aditivo en `main()` de `check-costos.py`: si la última fila tiene `total_tokens == 0`, emitir `costo-000` (media) para que el diario lo SURJA en vez de esconderlo. No corta nada (solo visibilidad).
**DRAFT (listo para merge — añadir a `.pipeline/check-costos.py`, dentro de `main()`, justo antes del `print(json.dumps(...))` final):**
```python
    # ── Fila de 0 tokens: NO es una corrida barata, es un fallo silencioso —
    #    el recolector de costos no leyó los transcripts o la corrida no ejecutó.
    #    (Visto el 2026-07-01: auto-agente 20260701-182502 con total_tokens=0.)
    if filas and (filas[-1].get("total_tokens", 0) == 0):
        hallazgos.append({
            "id": "costo-000", "archivo": ".pipeline/costos.jsonl", "linea": 0,
            "severidad": "media", "categoria": "costo",
            "descripcion": "La última corrida (%s) registró 0 tokens: el medidor de costo falló o la corrida no ejecutó (no hay señal de gasto)." % (
                filas[-1].get("etiqueta", "?")),
            "fix_sugerido": "Revisar que el driver haya corrido y que el recolector de costos leyó los transcripts; un 0 oculta tanto una corrida caída como un medidor roto.",
        })
```

---

## [HECHO 2026-07-03] movil — Checker de PARIDAD de plantilla en la familia de páginas de servicio   (impacto M · esfuerzo S · riesgo bajo)
> ✅ Mergeada: `.pipeline/check-familia-servicios.py` creado. Verificado: 18 páginas tienen el disparador `.about-text` y 18/18 la regla tap-target (paridad completa); 0 hallazgos; check-infra.mjs lo acepta.
**Problema:** Cuando un fix de `<style>` inline se aplica a UNA página de servicio, nada garantiza que llegue a sus 17 hermanas del mismo esqueleto. El fix se queda huérfano hasta que alguien nota la regresión a ojo, corrida tras corrida.
**Evidencia (HISTORIAL):** La familia movil-502 → movil-701 → **movil-801** (06-30) es exactamente esto: la regla de tap-target `.about-text a{display:inline-block;padding:.6rem 0}` vivía en **1 de 18** páginas y las otras 17 "nunca la recibieron". Hoy la paridad está completa (verifiqué: 18/18 la tienen), pero no hay tripwire que impida que la próxima página nueva o el próximo fix parcial reabra el hueco.
**Propuesta:** Nuevo checker `check-familia-servicios.py` con un REGISTRO de reglas «si la página contiene `<disparador>`, DEBE contener `<patrón>`». Al añadir un fix de familia en el futuro, se agrega UNA línea al registro y el pipeline vigila la paridad para siempre. Emite el contrato `{"hallazgos":[...]}` → `check-infra.mjs` lo recoge automáticamente (patrón sin-args, como `check-costos.py`). Hoy devuelve 0 hallazgos → arranca limpio y solo dispara ante una regresión real.
**DRAFT (listo para merge — crear `.pipeline/check-familia-servicios.py`):**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checker DETERMINISTA: PARIDAD de reglas de plantilla en la familia de páginas de servicio.

Caza la clase de regresión movil-502 / movil-701 / movil-801: un fix de <style> inline
(o de estructura) se aplica a UNA página de servicio y no se propaga a sus hermanas del
mismo esqueleto -> la mayoría se queda sin el fix hasta que alguien lo nota a ojo.

Modelo: un REGISTRO de reglas obligatorias. Cada regla dice «si la página CONTIENE
<disparador>, DEBE contener <patrón>». Al añadir un fix nuevo a la familia, se agrega
una línea aquí y el pipeline vigila la paridad solo, para siempre.

Emite el contrato común {"hallazgos":[...]} — check-infra.mjs lo recoge sin tocar nada.
Sin argumentos.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICIOS_GLOB = os.path.join(ROOT, "servicios", "*", "index.html")

# (id, categoría, disparador-regex, patrón-obligatorio-regex, descripción)
REGLAS_FAMILIA = [
    (
        "familia-about-text-tap",
        "movil",
        re.compile(r"\.about-text\b"),
        re.compile(r"\.about-text\s+a\s*\{[^}]*display\s*:\s*inline-block", re.S),
        "Página de servicio con .about-text SIN la regla de tap-target ~44px "
        "(@media(max-width:768px){.about-text a{display:inline-block;padding:.6rem 0}}) — "
        "regresión de la familia movil-502/701/801.",
    ),
    # Añadir aquí futuras reglas de familia: (id, categoría, disparador, obligatorio, desc)
]


def main():
    hallazgos = []
    seq = 0
    for full in sorted(glob.glob(SERVICIOS_GLOB)):
        try:
            html = open(full, encoding="utf-8").read()
        except OSError:
            continue
        rel = os.path.relpath(full, ROOT)
        for rid, cat, disparador, obligatorio, desc in REGLAS_FAMILIA:
            if disparador.search(html) and not obligatorio.search(html):
                seq += 1
                hallazgos.append({
                    "id": f"{rid}-{seq:03d}",
                    "archivo": rel,
                    "linea": 0,
                    "severidad": "media",
                    "categoria": cat,
                    "descripcion": desc,
                    "fix_sugerido": "Copiar la regla ya probada desde una página hermana (mismo esqueleto) a esta página; verificar headless a 375px que el tap-target quede >=44px.",
                })
    print(json.dumps({"hallazgos": hallazgos}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

---

## [HECHO 2026-07-03] costo — Detector de CORRIDA DESBOCADA (output/mensajes vs mediana), no solo volumen total   (impacto A · esfuerzo S · riesgo bajo)
> ✅ Mergeada: bloque `costo-runaway-*` añadido a `.pipeline/check-costos.py`. Verificado: campos output_tokens/mensajes en 18/18 filas; arranca limpio (última corrida 0.4×/0.7× la mediana); cazaría las 3 desbocadas históricas (output 2.13M/2.31M/2.16M vs mediana ~238K).
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

## [HECHO 2026-07-03] infra — Convertir el over-budget de REGLAS.md en tarea DRENABLE (no solo exit 1 de FASE 9)   (impacto M · esfuerzo S · riesgo bajo)
> ✅ Mergeada: `.pipeline/check-reglas-presupuesto.py` creado; check-infra.mjs y el gate de contrato lo aceptan. Como se diseñó, dispara YA `reglas-presupuesto` (media) porque REGLAS.md está al 99.6% del tope (3986/4000) — el over-budget ahora es un hallazgo DRENABLE por el diario en vez de un exit-1 ignorable. `reglas-gordas` no dispara (0 reglas >900 chars). El DRENADO (consolidar REGLAS.md a «qué + checker» y mandar relato a HISTORIAL) queda como tarea deliberada — es edición de la red de seguridad, criterio humano.
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

## [HECHO 2026-07-03] infra — Gate PROACTIVO de contrato de checkers en pre-push (matar la clase infra-003 al commit, no a la corrida siguiente)   (impacto M · esfuerzo S · riesgo bajo)
> ✅ Mergeada: `.pipeline/check-contrato-checkers.mjs` creado + bloque 1c en `.pipeline/hooks/pre-push` (instalado en `.git/hooks`). 2 BUGS del draft corregidos al aplicar: (1) el `.mjs` usaba `require()`/`__dirname` → ES module scope → fallaba SIEMPRE (bloquearía todo push); reescrito a `import`/`fileURLToPath`. (2) el gate no traía el marcador `infra:utilidad-no-sensor` → check-infra.mjs lo marcaba como "verificación ciega" (¡la misma clase infra-003 que dice cerrar!); añadido. Verificado: gate corre 10 checkers OK (exit 0), check-infra en 0, hook idéntico en ambas copias.
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
