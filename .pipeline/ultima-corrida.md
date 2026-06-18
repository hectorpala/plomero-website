# Última corrida — auto/mantenimiento-20260617-1826 (AUTÓNOMA)

**Fecha:** 2026-06-17 18:26 · **Modo:** autónomo sin supervisión · **Revisores:** 18

## Health check
- 5/5 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /blog/), node v22.18 vía /usr/local/bin.
- Compuerta `revisor-infra-salud` (check-infra.mjs): **exit 0, 0 hallazgos** (sensores sanos).
- main = origin/main al inicio (sincronizado con fetch + merge --ff-only).

## Contexto de corpus
Corpus indexable estable tras la consolidación de colonias: conversión 66, NAP 77, linking 66, contenido 77, secretos 414, total HTML 108. **NO es ceguera** — todos los deterministas corrieron sobre datos reales. Varios pendientes de la corrida 1117 de hoy ya quedaron resueltos en commits intermedios (perf-601..604 AVIF, cont-010/011, cont-012/013/014, movil-601..604, seo-501..506+links-data).

## Deterministas (corridos directos, no ciegos)
indexabilidad 0 · conversión 0/66 · NAP 0/77 · linking 0/66 · e2e 0/3 · producción 0 (prod LIMPIA real) · secretos **exit 0** (sec-001 historial inmutable = R-01) · perf-real perf-001 (falta baseline = R-03) · tracking trk-001..004 (Consent Mode esperado) · contenido-mec 1 (cont-001 = R-02, placeholder XXXX) · plantilla 25 **todas BAJA** (theme-color + 3 tablas con fallback = plt-001..025). **0 hallazgos mecánicos ALTA/MEDIA nuevos en deterministas.**

## Revisores LLM (6 en paralelo)
- **revisor-movil:** 1 NUEVO MEDIA → **movil-502** (abajo). Resto = conocidos, sin regresiones; 0 overflow en 21 páginas medidas a 375px.
- **revisor-contenido (subjetivo):** 1 NUEVO MEDIA → **cont-020** (doorway, pendiente humano). 0 ortografía nueva, 0 thin content real.
- **revisor-a11y / links / seo / perf:** 0 hallazgos nuevos accionables (lo detectado excede el candado de 15 archivos o es pendiente conocido: 24 colonias sin twitter:image, 42 SVG decorativos sin aria-hidden).

## Arreglado y verificado (1)
**movil-502 (MEDIA — residual de movil-501).** El fix de movil-501 acotó el selector a `.price-table .service-link`, dejando fuera **5 CTA `.service-link` en PROSA** (`<p>` L478/507/571 de `precios/index.html`: "Ver servicio completo de destape →", "Ver servicio de reparación de fugas →", "Detección de fugas sin romper →", "Ver reparación de boiler →", "Ver mantenimiento de boiler →") que rendían **20px** de alto en 375px (< 44px táctil). Se intentó primero ampliar el selector a `.service-link` global pero el padding 0.35rem solo llevaba la prosa a **38px** (insuficiente: en la tabla alcanza porque las celdas envuelven a 2-3 líneas). **Fix final:** regla separada `p .service-link{display:inline-block; padding:0.6rem 0}` en el `<style>` inline — la tabla conserva su 0.35rem (ya cumplía, no se ve más alta).
- **Verificación headless:** 375px → prosa 46–74px, tabla 60px (todos ≥44); 1280px → sin overflow. /precios/ 200, wa.me (526673922273) intacto, **0 errores JS**, plantilla 25 BAJA sin cambio, conversión 0/66, e2e 0/3. Solo CSS inline → **sin bump** de `?v=`/sw.js.

## Pendiente humano nuevo (1)
- **cont-020 (MEDIA, copy/estrategia):** `servicios/plomero-cerca-de-mi/index.html` es casi-clon indexable de la home (~92% del cuerpo: 6/72 bloques únicos, 15/16 H2 verbatim, rejilla de 6 servicios + tarjetas de zona + 6 testimonios + blog cards idénticos = patrón **doorway**). Solo la intro "cerca de mí" y los tiempos de llegada son propios. Reescritura/consolidación → prohibido en auto; amplía seo-002.

## Candados paso 8
auto-revisión limpia (1 archivo de sitio, 4 líneas, solo `<style>` inline; 0 CSS compartidos/JS/XML/test/sw; wa.me y JSON-LD intactos), diff 1≤15, 0 borrados/renombrados, secretos **exit 0** → **cumplidos**.

## Aprendizaje
Ampliada la regla MÓVIL/TAP-TARGET (movil-501) en REGLAS.md con la reincidencia movil-502: (1) al arreglar tap targets de una clase, revisar **todas** sus instancias en la página, no solo las del contenedor principal; (2) el padding **no es transferible** entre contextos — `0.35rem` basta en tabla (celdas multilinea, 60px) pero un enlace de prosa de una línea solo llega a 38px; usar `0.6rem` para prosa.

## Publicación
Ver el bloque "publicado" en ESTADO.md (actualizado tras el push).
