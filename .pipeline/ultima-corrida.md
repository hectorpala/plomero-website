# Última corrida del pipeline autónomo

**Rama:** auto/mantenimiento-20260612-2001
**Fecha:** 2026-06-12 ~20:01
**Modo:** AUTÓNOMO (sin supervisión)
**Resultado:** PUBLICADO ✅ (merge eee3c396 → main; push fcb190a1..eee3c396)

## Health check
- 9/9 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /blog/, /terminos/, /privacidad/, /gracias/, /404.html).
- main.js sintaxis OK (node v22.18 vía /usr/local/bin); URLs wa.me intactas (526673922273).
- 0 regresiones: los 6 revisores confirmaron que los fixes previos (perf-301..314 eager→lazy, og:url=canonical, fetchpriority único por página, versionado CSS/JS, enlaces) siguen sanos.

## Arreglado y verificado (3) — todos seo media, mecánicos
- **seo-301** servicios/instalacion-de-boiler — BreadcrumbList JSON-LD truncado a 1 item (Inicio→home); último item ≠ canonical.
- **seo-302** servicios/plomero-a-domicilio — ídem.
- **seo-303** servicios/plomero-cerca-de-mi — ídem.

Fix: añadidos niveles 2 (Servicios → /servicios/) y 3 (la propia página, item == canonical), igualando el patrón de las demás páginas de servicio (ref: instalacion-de-tinaco, cambio-de-tuberias).
Verificación escéptica: JSON-LD reparseado con node (parse OK, 1 bloque), último breadcrumb `item` == canonical en las 3, y HTTP 200 con el servidor local corriendo. Solo HTML estructural → sin bump de ?v=/sw.js (regla confirmada).

Diff: 3 archivos, +36 líneas, 0 borrados, 0 renombrados, 0 tests/CSS/JS tocados.

## Candados de publicación (paso 8)
- Auto-revisión limpia: ✅ (JSON-LD válido, último item == canonical, 200).
- Diff ≤ 200 archivos: ✅ (3).
- Sin borrados estructurales: ✅ (0).
→ **3/3 → PUBLICADO.**

## Indexación
- infra-001 (resuelto): el hook detectó las 17 URLs del push, incluidas las 3 páginas editadas.
- Cuota diaria de Google agotada → las 17 quedaron **encoladas en pending-index.json**; el job launchd diario (com.gscmcp.reindex) las reenvía cuando la cuota se reinicia. **0 URLs perdidas.**
- **infra-002 (nuevo, baja):** `git push` pelado abortó porque el hook llama `node` sin ruta absoluta y node no está en el PATH por defecto (vive en /usr/local/bin). Workaround usado: `PATH=/usr/local/bin:$PATH git push`. Pendiente: endurecer el hook.

## Pendientes para humano (10 nuevos)
- **gsc-210** cluster baño/WC tapado (~130 impr pos 7.1, CTR ~0.8%) → reescribir title/meta.
- **gsc-211** /correccion-baja-presion/ rankea solo "bombas de agua" (CTR 0); mismatch de intención (amplía gsc-207).
- **gsc-212** cluster "drenaje tapado" ~440 impr top10 sin clics → snippet débil.
- **gsc-213** "detección de fugas" fragmentado (pos 4.3–56); posible canibalización servicio↔blog.
- **gsc-214** ruido off-target (alemán, marcas ajenas) infla impresiones / deprime CTR agregado (informativo).
- **perf-401** main.js no minificado real → minificar con cuidado (riesgo de truncar wa.me).
- **perf-402** sin preload del hero LCP → medir antes de aplicar.
- **a11y-301** footer h4→h3 (salto h2→h4) en 18 páginas → mecánico pero baja y fuera de alcance auto.
- **movil-301** 2ª tabla sin .table-wrapper en blog/instalacion-tinaco-guia-compra (protegida por fallback global).
- **seo-304** desazolve breadcrumb de 2 niveles (último item OK == canonical; falta "Servicios"); **seo-305** typo año en og:url de marcha-paz (noindex).

## Aprendizaje (REGLAS.md)
1. **SEO/SCHEMA:** variante del bug og:url=canonical — el BreadcrumbList puede quedar truncado a 1 nivel con el último item apuntando a la home. Verificar que el último `item` == canonical y que existan los 3 niveles (`grep -c '"position": 3'` == 1 en servicios).
2. **INFRA/PUSH:** el hook pre-push necesita node en PATH; usar `PATH=/usr/local/bin:$PATH git push`.
