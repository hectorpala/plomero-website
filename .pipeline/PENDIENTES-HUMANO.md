# PENDIENTES PARA HUMANO — corrección del sistema de mantenimiento (2026-06-14)

Items que **NO** se automatizaron porque tocan producción en vivo, secretos, color de
marca, estrategia de contenido, o tienen un riesgo que no debe correr sin supervisión.
Cada uno: **qué es · por qué importa · cómo hacerlo · por qué NO se automatizó.**

Esto NO incluye el backlog de contenido/SEO ya documentado en `ESTADO.md` (gsc-201..214,
seo-002/104/107/109, a11y-101/201, etc.) — ese sigue ahí. Aquí va lo de esta ronda.

---

## H-06 — Rollback automático tras push (movido desde la cola AUTO, item A7)

**Qué es.** Añadir al pipeline, tras un `git push` EXITOSO en la publicación: esperar el
deploy de Netlify, re-correr `.pipeline/check-produccion.mjs` contra producción, y si
aparece un `pageerror` o algún no-200, hacer `git revert` del merge (SIN `--force`) y
escribir la alerta en ESTADO.md.

**Por qué importa.** Hoy el pipeline publica y se va; si un deploy rompe producción (caso
prod-001: una excepción JS que el `node --check` no atrapa porque es de runtime), nadie se
entera hasta la siguiente corrida. Un guardia post-deploy cerraría ese hueco.

**Por qué NO se automatizó (riesgo real, no pereza).** El propio `fix/seo-check-workflow`
que acabamos de mergear ELIMINÓ el trigger `push` de seo-check.yml por esta razón exacta,
documentada en el YAML: *"No hay señal fiable del fin del deploy de Netlify sin API/token
(carrera con el deploy)."* A7 propone un `git revert` + push **autónomo y no supervisado**
disparado por esa MISMA señal no fiable. Los modos de fallo:
- Si la espera es muy corta, `check-produccion.mjs` mide el deploy VIEJO → puede revertir
  un fix BUENO (falso positivo) o no ver el error nuevo (falso negativo).
- Un `git revert` + push automático en bucle puede thrashear producción (revierte trabajo
  bueno, re-pushea, etc.).
Auto-revertir producción sobre una señal no confiable, sin un humano mirando, es
precisamente el tipo de acción que el prompt del loop pide NO automatizar.

**Cómo hacerlo (propuesta de diseño conservadora, para implementar tú o supervisado):**
1. **Conseguir una señal de deploy fiable primero** (sin esto, lo demás es adivinar):
   usar la **Netlify API** con un token (`GET /api/v1/sites/{site_id}/deploys`, esperar a
   que el deploy del commit pusheado pase a `state:"ready"`), o un **webhook** de
   "Deploy succeeded" de Netlify. Token nuevo → va a Keychain/secret, no al repo (ver H-07).
2. **Paso nuevo en el pipeline** (prompt tras paso 9 / SKILL tras paso 13), PARAMETRIZADO:
   `ROLLBACK_AUTOMATICO=false` por defecto. Con la señal de deploy lista, re-correr
   `check-produccion.mjs`; si hay `pageerror`/no-200:
   - Por defecto (flag en false): **NO** revertir. Escribir alerta LOUD en ESTADO.md con el
     comando de revert exacto sugerido (`git revert -m 1 <merge>`) y notificar — un humano
     decide.
   - Solo si `ROLLBACK_AUTOMATICO=true` Y la señal de deploy fue confirmada (no timeout):
     ejecutar `git revert` (SIN `--force`) + push, y alertar.
3. Nunca revertir por timeout de la espera (ausencia de señal ≠ deploy roto).

**Recomendación:** implementar primero la señal Netlify-API; hasta entonces, dejar el paso
en modo "alerta, no revierte". No inventar una señal de deploy.

---

## H-07 — Sacar secretos de la raíz del repo y rotarlos

**Qué es.** `.env`, `client_secret.json` y `token.json` viven EN CLARO en la raíz del repo.
Verificado hoy: los 3 existen, están **gitignored** y **NO trackeados** (no están en la
historia de git), pero siguen en disco en texto plano.

**Por qué importa.** Aunque no estén en git, un secreto en claro en el working dir es
superficie de ataque (backup, sync a la nube, otro proceso, copia accidental). Y `token.json`
de OAuth caduca (ligado a H-09).

**Cómo hacerlo.** Mover los secretos fuera del árbol del repo (p.ej. `~/.config/gsc-mcp/` o
Keychain), apuntar los scripts/MCP a la nueva ubicación vía variable de entorno, y **ROTAR**
las credenciales (regenerar `client_secret`/token en la consola de Google, nuevo `.env`).
Confirmar que nada en git los referenció nunca (`git log --all -- .env client_secret.json
token.json` → vacío).

**Por qué NO se automatizó.** Toca el filesystem fuera del repo y exige rotación de
credenciales reales en una consola externa. Acción sensible e irreversible-ish (rotar
invalida tokens en uso); decisión y ejecución humana.

---

## H-08 — Compilar los 3 CSS desde una sola fuente

**Qué es.** Hay 3 CSS que deben ir en paridad manual: `styles.css` (fuente, 50.486 b),
`styles.min.css` (50.768 b — ni siquiera está minificado de verdad, perf-104) y
`styles.7f293647.css` (37.207 b, el `.hash` realmente servido). Hoy un cambio hay que
aplicarlo a mano en los 3 (REGLAS.md lo exige) y la paridad ya reincidió varias veces
(movil-203, f44ef39f).

**Por qué importa.** La paridad manual es una fuente recurrente de bugs (una regla queda en
2 de 3 archivos). El checker (`check_css_parity`) la caza pero es un parche, no la cura.

**Cómo hacerlo (refactor, proponer plan, no ejecutar):** una sola fuente `styles.css` →
build que genere el `.min` y el `.hash` (con bump de `?v=` + `sw.js`). Definir herramienta
(esbuild/lightningcss/postcss), dónde corre (script local o CI), y cómo se versiona el hash.
Migrar y verificar visualmente que el render no cambia en las páginas clave.

**Por qué NO se automatizó.** Refactor grande de build con validación visual completa; cambia
cómo se sirven los estilos de TODO el sitio. Requiere plan y revisión humana.

---

## H-09 — Publicar la app OAuth de Search Console a producción

**Qué es.** La app OAuth de Google (la que usa el MCP/`gsc-index.mjs` para leer Search
Console) está en modo **"Testing"** en la consola de Google. En ese modo el token de refresh
muere cada ~7 días.

**Por qué importa.** Cuando el token muere, `revisor-gsc` se queda CIEGO (no lee datos
reales). Con el A2 que acabamos de implementar (verificación ciega), ahora al menos eso
GRITA un hallazgo ALTA en vez de pasar callando — pero la causa raíz es el modo Testing.

**Cómo hacerlo.** En Google Cloud Console → OAuth consent screen → **Publish app** (pasar de
Testing a In production). Revisar scopes; si pide verificación, completarla. Tras publicar,
re-generar el token (ligado a H-07: el nuevo token va fuera del repo).

**Por qué NO se automatizó.** Acción en una consola externa de Google (no es código del
repo). Decisión y ejecución humana.

---

## H-10 — Performance que requiere MEDIR LCP antes/después

**Qué es.** Optimizaciones de assets que NO son defectos rotos sino tuning, y que solo deben
aplicarse si miden mejor (Lighthouse/LCP antes y después). Verificado hoy:
- **perf-502:** `assets/fonts/inter-400/500/600.woff2` son **byte-idénticos** (38.760 b cada
  uno) → ~76 KB desperdiciados; se preloadean hasta 3 URLs iguales.
- **perf-503:** `assets/images/logo-2048.png` pesa **383 KB** y (según ESTADO) sin
  referencias.
- **perf-504:** `fuga-tuberia-rota-1200w.webp` ~200 KB recomprimible.
- **perf-501:** 26 páginas con fuentes en `fetchpriority="high"` compitiendo con el hero LCP.

**Por qué importa.** Son KB reales y carriles de LCP, pero tocar binarios/preloads a ciegas
puede empeorar la percepción visual o el LCP si no se mide.

**Cómo hacerlo.** Medir LCP con Lighthouse en la(s) página(s) afectada(s); re-subsetear las
fuentes Inter desde los `.original` (que sí difieren) o colapsar a 1 `@font-face`; borrar
`logo-2048.png` si de verdad no se referencia (confirmar antes); recomprimir el webp; quitar
`fetchpriority="high"` de los `<link rel=preload as=font>` para igualar el patrón de la home.
Aplicar SOLO lo que mida mejor; si se cambia un asset servido, bump de `sw.js`.

**Por qué NO se automatizó.** Requiere medición LCP antes/después (juicio sobre el resultado)
y borrar/recomprimir binarios visuales. Mismo criterio que perf-104/401/402.

---

## H — Decidir el color de marca real

**Qué es.** REGLAS.md fija el color de marca en **`#F97316`** (regla [2026-06-03]). Pero el
sitio usa AMBOS naranjas mezclados: verificado hoy, **72 archivos** usan `#E36414` y **85**
usan `#F97316`.

**Por qué importa.** Inconsistencia de marca visible; y el checker de `theme-color` y los
revisores de contraste (a11y-101) dependen de saber cuál es EL color correcto. Mientras haya
dos, cualquier "arreglo" de color es ambiguo.

**Cómo hacerlo.** Decidir el color de marca real (negocio/diseño). Una vez decidido,
actualizar REGLAS.md y, opcionalmente, unificar el sitio al color elegido (reemplazo masivo
+ verificación visual + de contraste WCAG).

**Por qué NO se automatizó.** Es una decisión de marca/diseño, no mecánica. Unificar a ciegas
podría cambiar la identidad visual a un color equivocado.

---

## H — GSC: canibalización, clusters y head terms (estrategia de contenido)

**Qué es.** `gsc-205..214` (en ESTADO.md/HISTORIAL): canibalización (`/precios/` vs
`/servicios/plomero-precios/`; "detección de fugas" fragmentado), clusters de baño/drenaje/
fugas con CTR ~0, head terms ("plomero culiacan", "plomero") estancados al borde de página 2,
intención de "bombas de agua" vs corrección de presión.

**Por qué importa.** Es donde está el tráfico real perdido, pero todo son decisiones de copy
y arquitectura de contenido.

**Cómo hacerlo.** Reescribir titles/metas para captar la frase exacta; decidir URLs canónicas
y consolidar enlazado interno; decidir si el negocio atiende intenciones tangenciales (bombas
de agua). Ver el detalle por id en ESTADO.md.

**Por qué NO se automatizó.** Copy y estrategia de contenido/arquitectura; el prompt del loop
lo prohíbe explícitamente en automático.

---

_Generado por la ronda de corrección autónoma (en ramas, sin push) del 2026-06-14._

---

## REVISORES NUEVOS (rama feat/revisores-faltantes) — pendientes humanos (2026-06-14)

### R-01 — ROTAR el client_secret de Google OAuth (estaba en el historial git) 🔴 URGENTE
**Qué es.** `revisor-secretos` detectó que `client_secret.json` (Google OAuth, proyecto
`odsappi-apuestas`, client_id `13662482854-…apps.googleusercontent.com`) fue commiteado en
`8788d6ab` y removido en `e41ab25e`, pero SIGUE en el historial.
**Cómo hacerlo.** Rotar/revocar ese client secret en Google Cloud Console (Credentials). Con eso
la copia del historial queda inservible. NO hace falta purgar el historial (exigiría push --force,
prohibido por el pipeline, y rompe clones) — basta rotar. **Por qué NO se automatizó:** toca
credenciales reales en Google Cloud.

### R-02 — Enlace de reseñas roto en reparacion-de-fugas (placeholder g.page) 🟠
**Qué es.** `revisor-contenido` halló `https://g.page/r/XXXXX/review` (el `XXXXX` es placeholder, el
botón "déjanos una reseña" no funciona).
**Cómo hacerlo.** Conseguir el short-link real de reseñas del Perfil de Empresa de Google y
reemplazar `XXXXX`. **Por qué NO se automatizó:** el ID real solo lo tienes tú (Héctor lo deja
pendiente; me lo pasa y lo arreglo).

### R-03 — Establecer la baseline de Core Web Vitals (post-merge) 🟠
**Qué es.** `revisor-perf-real` compara contra `.pipeline/perf-baseline.json`, que aún no existe.
**Cómo hacerlo.** Tras mergear, correr una vez `node .pipeline/check-perf.mjs --update-baseline` en
un entorno con datos reales (idealmente CI con Lighthouse: `PERF_REPORTS` apuntando a los
`lighthouse-run-*.json`) y commitear el resultado. **Por qué NO se automatizó:** mezclar métricas de
puppeteer (local) con Lighthouse (CI) para la baseline sería apples-to-oranges; mejor fijarla con la
fuente real.

### Resueltos en esta ronda (no requieren acción)
- NAP colonias "Plomero Culiacán Pro – <Colonia>": **intencional** (decisión Héctor) → revisor-nap
  ajustado para aceptarlo.
- Año "2025" en h1 de 7 blogs + acento en tecnico-de-gas: **arreglados** en la rama
  `fix/contenido-nap-jun2026` (pendiente tu revisión + merge).
