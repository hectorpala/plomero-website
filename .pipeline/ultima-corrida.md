# Última corrida del pipeline — 2026-06-14 18:25

**Rama:** `auto/mantenimiento-20260614-1825` · **Modo:** AUTÓNOMO · **Revisores:** 18

## Health check
- 5/5 rutas clave en 200 (`/`, `/precios/`, `/contacto/`, `/servicios/`, `/blog/`).
- Compuerta `revisor-infra-salud` (`check-infra.mjs`): **exit 0, 0 hallazgos** → sensores sanos, corrida confiable.
- node v22.18 vía `/usr/local/bin` (infra-002 vigente: `node` no está en el PATH por defecto).

## Revisores
- **Deterministas limpios sobre corpus real** (NO ciegos): indexabilidad 0, conversión 0/99, NAP 0/110, linking 0/99, e2e 0/3, producción 0 (prod LIMPIA, prod-001 sin regresión), secretos **exit 0**.
- **Deterministas con hallazgos:** plantilla 26 (todas BAJA: theme-color faltante/placeholder + 3 tablas sin wrapper protegidas por fallback), contenido-mecánico 1 (cont-001 = R-02), perf-real (presupuesto absoluto OK, falta baseline = R-03).
- **Tracking (4, MEDIA pero esperado):** GA4 no emite beacon en headless por Consent Mode denegado por defecto — verificar en GA4 Realtime con navegador real/consentido (no es bug).
- **LLM (subjetivos):** seo, móvil, a11y, perf, links, contenido-subj, gsc.

## Arreglado y verificado (3)
1. **movil-401 (ALTA)** — `servicios/reparacion-de-boiler/index.html`: botones flotantes WhatsApp/llamada rotos en móvil. Era la única página que usa `.floating-btn` en el HTML pero sin las reglas en su `<style>` inline (no están en los 3 CSS compartidos) → `position:static`, <44px, sin color. Añadidas las 4 reglas verbatim. **Verificado headless 375px:** ambos `position:fixed` 54×54, colores correctos, `border-radius:50%`, wa.me intacto (526673922273), 0 pageerror.
2. **cont-003 (MEDIA)** — año caduco en el título de la tarjeta del post de tinaco: 2024/2025 → **2026** (coincide con el título real "[2026]") en `index.html` + 5 servicios. El `datetime` de publicación NO se tocó.
3. **seo-401 (MEDIA)** — 59 enlaces internos `/servicios/<slug>/index.html` → forma de directorio canónica (igual que los 535+ restantes) en `index.html` + 5 servicios. checker-linking sigue en 0 (no rompe nada).

Solo HTML (`<style>` inline + texto/href) → **sin bump de `?v=`/sw.js**. Diff: **7 archivos HTML**, 0 tests/CSS/JS/XML, 0 borrados.

## Candados de publicación (paso 8): TODOS cumplidos
- Auto-revisión limpia (solo HTML, wa.me intacto en los 7, JSON-LD válido, deterministas re-corridos sin regresión).
- Diff 7 ≤ 15 archivos. 0 borrados/renombrados. Secretos exit 0 (sec-001 está en historial inmutable = R-01, no bloquea).

## Pendientes para humano (nuevos esta corrida)
- **cont-002 (ALTA)** — `tecnico-de-gas-culiacan`: cuerpo entero sin acentos (incl. "anos"→"años"). Re-acentuar es un cambio de COPY amplio → fuera de auto.
- **gsc-217 (ALTA)** — hub `/servicios/` nunca rastreado por Google pese a sitemap/enlaces/robots correctos. Solicitar indexación en GSC + revisar señales de calidad/duplicación.
- **seo-402 (MEDIA)** — NAP/geo de relleno ("Culiacán", CP 80000, 2ª coordenada) en el LocalBusiness del hub + 10 servicios, distinto de la dirección real de la home. Confirmar el NAP oficial antes de propagar.
- **seo-403 (MEDIA)** — 3ª URL en la canibalización de precios (`cuanto-cuesta-plomeria-bano-completo` con title genérico). Copy/estrategia.
- **a11y-401 (MEDIA)** — skip-link "Saltar al contenido" falta en ~114 páginas (solo está en la home). Mecánico pero excede el candado de 15 archivos → corrida dedicada.
- **gsc-218 (MEDIA)** — `tecnico-de-gas-culiacan` (página nueva) sin indexar; vigilar.

## Aprendizaje (REGLAS.md)
3 reglas nuevas:
1. **MÓVIL/PLANTILLA** — los botones flotantes se estilan con CSS inline por página; si el HTML usa `class="floating-btn"`, su `<style>` debe traer `.floating-btn` (chequeo grep). A largo plazo mover a los 3 CSS compartidos.
2. **SEO/ENLACES** — enlaces internos en forma de directorio (`/servicios/<slug>/`), no `/index.html`, para coincidir con el canonical.
3. **CONTENIDO/AÑO** — el año embebido a mano en títulos de tarjetas de "artículo relacionado" se desincroniza del título real del post; unificar al año real (sin tocar `datetime`).
