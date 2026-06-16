# Última corrida — auto/mantenimiento-20260616-0831 (AUTÓNOMA)

**Fecha:** 2026-06-16 08:31 · **Modo:** autónomo, sin supervisión.

## Qué se arregló (1)
- **movil-501** (MEDIA) — `/precios/`: los 25 enlaces `.service-link` de la tabla de precios
  (selector solo en `<style>` inline, no en los 3 CSS compartidos) rendían **~41px** de alto
  en 375px, por debajo del mínimo táctil de **44px**. Fix: `display:inline-block; padding:0.35rem 0`
  → mín **60px ≥44** en 375px, 0 overflow móvil/desktop, enlaces desktop normales (38px).
  Solo `<style>` inline → **sin bump** de `?v=`/sw.js. Verificado headless en 375 y 1280.

## Health check + revisores
- 5/5 rutas clave en 200. Compuerta `revisor-infra-salud` exit 0 (sensores sanos).
- Deterministas limpios sobre corpus real (NO ciegos): indexabilidad 0, conversión 0/99,
  NAP 0/110, linking 0/99, e2e 0/3, producción 0 (real), secretos exit 0, perf-real OK.
  Plantilla 26 (todas BAJA conocidas), contenido-mec 1 (cont-001=R-02), tracking 4 (Consent Mode), perf-001 (baseline=R-03).
- revisor-gsc con datos REALES (no ciego): sin des-indexaciones nuevas.

## Pendientes para humano (nuevos, NO automatizados)
- **seo-404** (MEDIA, copy) — canibalización on-page "reparación de boiler" (mantenimiento-de-boiler vs reparacion-de-boiler).
- **seo-405** (MEDIA, copy) — canibalización "destape" (destape-de-drenajes vs desazolve-de-drenajes).
- a11y-402 (BAJA) — estrellas ★★★★★ sin aria en ~92 págs (excede candado de 15 archivos).
- a11y-403 (BAJA) — falta `<main>` en 46 págs (excede candado; hacerlo junto con a11y-401).
- perf-505 (BAJA) — montserrat-700/800.woff2 byte-idénticos (requiere subset + bump sw.js).
- gsc-219 (BAJA, tooling) — bug cosmético de logging en gsc-index.mjs L54 (doble slash; no afecta inspección).

## Publicación
- Candados paso 8 cumplidos: auto-revisión limpia (1 archivo de sitio, 2 líneas CSS inline,
  0 wa.me/JSON-LD/tests/assets compartidos), diff 1≤15, 0 borrados/renombrados, secretos exit 0.
- **PUBLICADO** (ver pie de ESTADO.md / commit de merge).
- Aprendizaje: 1 regla nueva (MÓVIL/TAP-TARGET para enlaces inline en tablas).
