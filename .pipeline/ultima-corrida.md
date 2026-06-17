# Última corrida — auto/mantenimiento-20260617-1117 (AUTÓNOMA)

**Fecha:** 2026-06-17 · **Modo:** autónomo sin supervisión · **Revisores:** 18

## Health check
- 5/5 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /blog/), node v22 vía /usr/local/bin.
- Compuerta `revisor-infra-salud` (check-infra.mjs): **exit 0, 0 hallazgos** (sensores sanos).
- main = origin/main al inicio.

## Contexto de corpus (importante)
El corpus de páginas indexables bajó de ~99 a **66** (conversión 66, NAP 77, linking 66; total HTML 108). **NO es ceguera**: hoy un humano ("Carril C") consolidó **32 colonias doorway → 4 hubs de zona** con 301 (commit `eaf83781`) y `/precios/` (`246336db`). Verificado contra los commits reales. Los deterministas corrieron sobre corpus real, no vacío.

## Deterministas (corridos directos, no ciegos)
- indexabilidad 0 · conversión 0/66 · NAP 0/77 · linking 0/66 · e2e 0/3 · producción 0 (prod LIMPIA, real) · secretos **exit 0** (sec-001 en historial inmutable = R-01) · perf-real solo perf-001 (falta baseline=R-03) · tracking trk-001..004 (Consent Mode esperado) · contenido-mecánico 1 (cont-001=R-02, placeholder XXXX g.page).
- **check-plantilla: 25 enlaces internos ROTOS (ALTA)** → la regresión de esta corrida (ver abajo). El resto de plantilla: 25 BAJA conocidas (theme-color + 3 tablas).

## Arreglado y verificado (1)
**links-201 (ALTA — REGRESIÓN de la consolidación humana `eaf83781`).** En `servicios/plomero-colonias-culiacan/index.html`, la rejilla de tarjetas `<a class="card" href="./slug/">` conservaba **25 enlaces a directorios de colonia borrados** (altamira, campestre, zona-dorada…). El humano reescribió la lista `<ul>` (forma absoluta) pero **omitió la rejilla relativa**. Reescrito cada `href="./slug/"` roto al **destino 301 exacto de `_redirects`** (hub de zona norte/sur/poniente o el índice de colonias), en forma absoluta canónica (no vía redirect; regla seo-401).
- **Verificación:** check-plantilla 25→**0** enlaces rotos; check-linking 0; conversión 0/66; página 200; **0 errores JS headless**; menú hamburguesa funciona (inline); los 4 hubs destino 200; wa.me (526673922273) y JSON-LD intactos. Solo HTML → **sin bump** de `?v=`/sw.js.

## Verificado NO-bug
- **main.js ausente** en `plomero-colonias-culiacan/index.html`: **falsa alarma** de revisor-perf. Es plantilla antigua con 5 `<script>` inline; el script #3 maneja menú + formulario. Headless OK, 0 errores. Funciona.

## Pendientes humano nuevos (secuelas de la consolidación)
- **cont-010 / cont-011 (MEDIA, copy):** ancla VACÍA `Plomero en </a>` → culiacan-tres-rios, y truncada `Plomero en Nuevo` → nuevo-culiacan (el generador de la lista cortó "Culiacán"). Restaurar nombres.
- **cont-012/013/014 (BAJA, copy):** conteo h2 "30 colonias" vs title "640+" desincronizado; 8 self-links (decisión del humano en _redirects); acentos/preposiciones en lista autogenerada.
- **seo-501..506 (BAJA-MEDIA, arquitectura):** anclas auto-referenciales en los 4 hubs; centro aplanó 6 anclas al mismo href; relevancia temática débil en 3 redirects. NO doorways (hubs ~2000 palabras, distintos).
- **movil-601..604 (MEDIA):** tap targets <44px en directorios de colonias; movil-602/603 exigen regla `.checklist a` en los 3 CSS + bump → corrida dedicada.
- **perf-601..604 (BAJA-MEDIA, binarios):** las 5 hubs usan plantilla WebP-only sin AVIF; hero de centro 196KB. Requiere recomprimir/generar AVIF.
- **links-data (BAJA):** 21 URLs obsoletas en `colonias-completas-culiacan.json` (data file no servido por ninguna página).

## Candados paso 8
auto-revisión limpia (1 archivo de sitio, 25/25 href, 0 CSS/JS/XML/test/sw), diff 1≤15, 0 borrados/renombrados, secretos exit 0 → **cumplidos**.

## Aprendizaje
1 regla nueva en REGLAS.md (SEO/ENLACES): al consolidar, los enlaces a páginas borradas existen en MÚLTIPLES formas en la misma página (rejilla relativa `./slug/` + lista absoluta); una reescritura parcial deja unas rotas. Verificar `check-plantilla` 0 y que ninguna página conserve `href="./<slug-borrado>/"`. Nota del bug del generador que trunca "Culiacán" en anclas (cont-010/011).

## Publicación
Ver bloque "publicado" en ESTADO.md (actualizado tras el push).
