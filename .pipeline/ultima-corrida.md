# Última corrida — auto/mantenimiento-20260612-1720 (AUTÓNOMA, PUBLICADA)

**Fecha:** 2026-06-12 17:20
**Modo:** autónomo, sin supervisión
**Resultado:** PUBLICADO a main (merge `2bcea0df`, push `7efbf5bb..2bcea0df`)

## Health check (antes de tocar nada)
- 8/8 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /gracias/, /privacidad/, /terminos/, /blog/).
- main.js sintaxis OK (`node --check`), wa.me intacta (`526673922273`), sw v24.
- 0 regresiones preexistentes de la corrida de la noche.

## Revisión (6 subagentes en paralelo)
- 22 hallazgos brutos → 19 únicos nuevos tras dedup contra HISTORIAL/ESTADO.
- a11y: 0 hallazgos nuevos (sitio limpio en alt/aria/foco).

## Arreglados y verificados (7 grupos, 19 ediciones) — todos MECÁNICOS
1. **perf-301..314** — 14 páginas: la 2ª imagen de contenido (bajo el fold) pasó de `loading="eager"` a `"lazy"`. Hero (`fetchpriority="high"`) y logo del nav intactos. Regla segura aplicada: solo imgs sin `fetchpriority="high"` y src sin "logo". Regresión de REGLA línea 28. 14/14 en 200, 0 content-imgs eager restantes.
2. **seo-206/207** — `og:url` apuntaba a la home en `instalacion-de-boiler` y `plomero-cerca-de-mi` (indexables) → corregido al canonical. Servido y verificado; JSON-LD válido. Reincidencia de REGLA og:url=canonical.
3. **seo-208** — `/contacto/` declaraba `twitter:card=summary_large_image` sin `twitter:image` → añadido (= og:image). 4 JSON-LD válidos.
4. **movil-203** — bloque fallback global de scroll de tablas (`@media(max-width:768px){table{display:block;overflow-x:auto}}`) faltaba en `styles.css`; copiado para paridad 1/1/1. **Sin bump de ?v=/sw.js**: styles.css es solo fuente, ninguna página lo sirve (sirven min/hash que ya lo tenían) → asset servido sin cambio.
5. **movil-204** — única `price-table` del sitio sin `.table-wrapper` (tecnico-de-gas) → envuelta. Balance div 75/75.
6. **links-204** — CTA principal de marcha-paz con `#contacto` inerte → `/#contacto` (sección vive en la home). Página noindex.

## Candados paso 8 — 3/3 CUMPLIDOS → publicado
- Auto-revisión limpia: JSON-LD válido en todas las editadas, health 200, div balance OK, paridad 1/1/1, diff sin copy/contenido/precios.
- Diff: **18 archivos ≤ 200**.
- Borrados estructurales: **0** (0 borrados, 0 renombrados, 0 tests tocados).

## Pendientes para humano (nuevos)
- **gsc-205..209** (copy/estrategia, datos reales GSC): tinaco CTR0 en queries de precio; cluster boiler con cobertura marginal; baja-presión rankea "bombas de agua" (mismatch intención); colonia mónaco CTR0; head terms "plomero culiacan"/"plomero" estancados pos ~10.6.
- **movil-205/206**: `terminos/` y `privacidad/` no enlazan el CSS compartido (solo inline + placeholder #0066cc) → tap targets <44px. Añadir stylesheet = cambio de diseño con riesgo de restyle, requiere validación visual humana.
- **seo-209**: 56 colonias sin `twitter:image` (ligado a doorways seo-002, no tocar hasta decidir consolidación).
- **movil-207**: `.footer-logo img` duplicado en `styles.min.css` (ruido de paridad, baja).

## ⚠️ Infra — indexación NO ejecutada
El hook `pre-push` corrió pero su script de auto-indexación tiene una ruta hardcodeada obsoleta (`/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán`) que ya no existe tras la mudanza a `~/Sitios Web` (commit 76e3b9d0). Resultado: "Sin páginas HTML que indexar" — **no se enviaron URLs a Google**. El push sí se completó. Corregir la ruta del hook es tarea de infra/humano (toca OAuth/indexación, fuera del alcance mecánico auto). Mientras tanto, indexación manual en GSC pendiente (junto con gsc-203).

## Aprendizaje (REGLAS.md)
- Regla NUEVA: la plantilla de servicio/blog emite img#2 (bajo el fold) con `loading="eager"`; debe ser `lazy`. Patrón recurrente.
- Reincidencia anotada: og:url=home en plantilla de servicio; paridad CSS con bloque fallback de tablas; nota de que styles.css no es servido (no requiere bump).
