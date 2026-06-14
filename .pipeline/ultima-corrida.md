# Última corrida del pipeline — 2026-06-13 20:00

**Rama:** `auto/mantenimiento-20260613-2000` (basada en main limpio) · **Modo:** AUTÓNOMO · **Estado:** ✅ PUBLICADA (merge `e2418d1e`)

## Health check
- 9/9 rutas clave en 200 (`/`, `/precios/`, `/contacto/`, `/servicios/`, `/servicios/plomero-precios/`, `/blog/`, `/sitemap.xml`, `/main.js`, `/sw.js`).
- `main.js` sintaxis OK (node v22.18), `wa.me/526673922273` intacto.
- Versionado consistente: `main.js?v=20260613` (30 refs), CSS `?v=20260612c`, sw.js v25 precachea la versión correcta.
- **0 regresiones**: los 8 revisores confirmaron sanos perf-301..314, prod-001 (sin reaparecer), og:url=canonical, fetchpriority único, versionado y enlaces.

## Revisión (8 revisores en paralelo)
seo · móvil · a11y · perf · links · gsc · indexabilidad · producción.
- **revisor-produccion:** producción LIMPIA — 0 `pageerror` en /, /precios/, /contacto/; **prod-001 sin regresión**; 8/8 URLs 200; HSTS/X-Content-Type-Options/Referrer-Policy presentes; form 2xx; 0 mixed content.
- **revisor-links:** 0 enlaces/recursos rotos.
- **revisor-indexabilidad:** idx-001 (= seo-304).

## Arreglado y verificado (2)
1. **seo-304 / idx-001 (ALTA)** — `servicios/desazolve-de-drenajes/`: `BreadcrumbList` de 2 niveles sin el intermedio "Servicios". Insertado pos2 `Servicios → /servicios/` y renumerada la página a pos3 (item == canonical). El checker de indexabilidad pasó de **1 → 0 hallazgos**.
2. **a11y-302 (MEDIA)** — exit-intent popup sin `role="dialog" aria-modal="true" aria-labelledby` en 5 páginas de servicio (cerca-de-mi, desazolve, a-domicilio, economico, instalacion-de-boiler). Añadidos los atributos + `id="exit-popup-title"` al `<h3>`, replicando index.html. Reemplazo exacto (1 div + 1 h3 por archivo). **5/5 verificadas**: popup-role=1, title-id=1, HTTP 200, JSON-LD válido, wa.me intacto.

Solo HTML (sin CSS/JS) → **sin bump de `?v=`/sw.js**.

## Candados de publicación (paso 8) — 3/3 ✅
- Auto-revisión limpia (diff = solo cambios intencionados; JSON-LD válido; wa.me intacto; sin tests/CSS/JS/contenido/copy).
- Diff ≤ 200 archivos: **5**.
- Sin borrados estructurales: **0** borrados, **0** renombrados.

→ Merge `--no-ff` **e2418d1e** + push **ef3b57f7..e2418d1e main**.
**Indexación COMPLETA:** el hook envió las 5 URLs editadas a Google (5 enviadas, 0 en cola, 0 descartadas — cuota disponible hoy). Push completado con `PATH=/usr/local/bin:$PATH git push` (infra-002 sigue vigente).

## Pendientes para humano (nuevos)
- **gsc-215 (media, recomendado pronto)** — bug de 1 string en `mcp-local-seo/gsc-index.mjs` L53 (`SITE_URL_HTTP` → debe ser `SITE_URL`/sc-domain). Deja CIEGA la verificación de indexación en cada corrida. No afecta el sitio servido. No auto-arreglado por precedente infra-002 (infra/tooling fuera del auto-fix de sitio).
- gsc-216 — ping a endpoint de sitemap retirado por Google (ruido 404). `gsc-index.mjs` L18-24.
- perf-501 — 26 páginas con fuentes en `fetchpriority="high"`; requiere medir LCP antes/después.
- perf-502 — 3 woff2 de Inter byte-idénticos (~76KB duplicados); requiere re-subset.
- perf-503/504 — `logo-2048.png` 383KB sin referencias; `fuga-tuberia-rota-1200w.webp` 200KB recomprimible.
- a11y-303 — mobile-menu-btn sin `aria-expanded`/`aria-controls` estáticos en 99 páginas (baja).
- seo-004 — 6 redirect-stubs `servicios/plomero/*` sin `meta robots noindex` (baja).
- Bajas no tocadas: seo-305 (typo año marcha-paz noindex), movil-301, seo-002/107 (geo colonias, ligado a doorways).

## Aprendizaje
1 regla nueva en REGLAS.md — **A11Y/PLANTILLA**: el exit-intent popup de páginas de servicio debe llevar `role="dialog" aria-modal="true" aria-labelledby="exit-popup-title"` y su `<h3>` el `id="exit-popup-title"`, igual que index.html. Chequeo: `grep -c 'id="exit-intent-popup" role="dialog"' index.html` == 1.
