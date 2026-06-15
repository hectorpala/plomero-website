# Progreso — Revisores faltantes (9 nuevos: 9 → 18)

Rama: `feat/revisores-faltantes` (desde main). UN commit por revisor. NO push / NO merge.
Patrón por revisor: checker `.pipeline/check-<x>.{py|mjs|sh}` (solo REPORTA, JSON común,
determinista) + agente `.claude/agents/revisor-<x>.md` + registro en
`.pipeline/mantener-prompt.txt` (paso 3) y `.claude/skills/mantener-sitio/SKILL.md` (FASE 1) +
evidencia (sintaxis, corrida real, PRUEBA NEGATIVA, determinismo md5) + commit.

JSON común: `{"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}]}`

Umbrales acordados con Héctor (2026-06-14):
- "Página clave" con formulario obligatorio (ALTA): **/contacto/ y home** únicamente (hoy ambas
  tienen `<form>` → 0 falsos positivos). `tel:` (667 392 2273 / 526673922273) + `wa.me` + CTA
  antes del fold se exigen en TODA página indexable. "Form en cada servicio" queda como posible
  mejora futura, NO hallazgo ALTA.
- Core Web Vitals: Google "good" → LCP<2.5s, CLS<0.1, INP<200ms + regresión vs baseline
  (mediana de 3 corridas).

Leyenda estado: ⬜ pendiente · 🔄 en curso · ✅ hecho+commit · 🧑 cola humana (con pregunta)

---

## FASE 1 — confianza en los sensores + seguridad
- [x] ✅ #1 revisor-infra-salud → `.pipeline/check-infra.mjs` (dead-man's switch, corre PRIMERO)
- [x] ✅ #2 revisor-secretos → `.pipeline/check-secretos.sh` (+ candado de publicación)

## FASE 2 — conectar lo que ya existe
- [x] ✅ #3 revisor-perf-real → baseline + presupuesto CWV — ⚠️ TOCA site-monitor.yml → **push SSH**
- [x] ✅ #4 revisor-tracking → `verificar-tracking.js` envuelto (dataLayer/GTM/GA)

## FASE 3 — ofensiva / negocio
- [x] ✅ #5 revisor-conversion → `.pipeline/check-conversion.py`
- [x] ✅ #6 revisor-nap → teléfono/email/nombre idénticos en todas las páginas

## FASE 4 — profundidad
- [x] ✅ #7 revisor-enlazado-interno → `.pipeline/check-linking.py` (huérfanas, profundidad >3)
- [ ] #8 revisor-contenido → parte mecánica (regex restos plantilla); subjetivo → LLM
- [ ] #9 revisor-e2e-funcional → `.pipeline/check-e2e.mjs` (puppeteer)

---

## Bitácora de diseño y evidencia

### #1 revisor-infra-salud — ✅ HECHO (commit en esta rama)
**Qué valida:** dead-man's switch del pipeline (no el sitio, los SENSORES). (a) frescura del
cron: log run-*.log más reciente en ~/Library/Logs/mantener-sitio/ <26h; (b) GSC vivo:
`webmasters.sites.list` con el token de mcp-local-seo (401/vacío → ALTA "GSC ciego"); (c)
checkers sanos: los deterministas LOCALES (indexabilidad, plantilla, + nuevos) se corren
completos y deben dar exit 0 + JSON con `hallazgos` + sin `error` + `analizadas`>0 si lo
exponen; los PESADOS (produccion, perf, tracking, e2e) reciben smoke (`node --check` +
puppeteer resuelve); + sanidad de corpus (sitemap >0 `<loc>`, >0 .html servidos); (d)
producción 200. Corre PRIMERO en el pipeline.
**Decisiones:** no se modifican los 3 checkers existentes → `analizadas` es campo opcional;
los pesados solo smoke para no duplicar trabajo caro (cada uno corre como su revisor).
Overrides solo-para-autopruebas vía env (INFRA_LOG_DIR / INFRA_CRON_MAX_HOURS / INFRA_BASE),
nunca seteados en producción (mismo patrón que PUPPETEER_EXECUTABLE_PATH en check-produccion).
**Determinista:** SÍ. Caso sano → `{"hallazgos":[]}`; descripciones sin timestamps/edades
volátiles. 2 corridas back-to-back → md5 idéntico (382b13bc...).
**Prueba negativa (6 ramas, todas detectan, repo restaurado idéntico):**
- (a) cron viejo: `INFRA_CRON_MAX_HOURS=0.0001` → ALTA "el log de cron más reciente ... supera el umbral".
- (b) GSC ciego: token movido a /tmp → ALTA "GSC ciego — webmasters.sites.list falló"; token restaurado.
- (c) local analizadas:0: scratch `check-zzscratchA.py` → ALTA "analizó 0 páginas/URLs"; borrado.
- (c) local JSON inválido: scratch `check-zzscratchB.py` → ALTA "no imprimió JSON parseable"; borrado.
- (c) heavy sintaxis rota: scratch `check-tracking.mjs` roto → ALTA "no pasa 'node --check'"; borrado.
- (d) prod caída: `INFRA_BASE=http://127.0.0.1:9` → ALTA "producción ... no responde (fetch failed)".
**Corrida real sobre el repo:** `{"hallazgos":[]}` (todos los sensores vivos: cron fresco,
token GSC válido, indexabilidad+plantilla limpios, prod 200).

### #2 revisor-secretos — ✅ HECHO (commit en esta rama)
**Qué valida:** que ninguna credencial llegue (o haya llegado) al repo. 3 barridos:
(1) WORKING TREE (alta, BLOQUEA) — patrones `sk-`, `AIza`, `gh*_`, `-----BEGIN PRIVATE KEY-----`,
y `client_secret`/`refresh_token` como VALOR asignado, sobre git ls-files + untracked no
ignorados; (2) GITIGNORE vs ÍNDICE (alta, BLOQUEA) — ningún archivo trackeado coincide con un
patrón de secretos de .gitignore (`git ls-files --ignored --cached`); (3) HISTORIAL (alta, NO
bloquea) — los mismos patrones sobre `git log -p`. Usa gitleaks si existe; si no, regex (aquí no
hay gitleaks → corre regex).
**Decisiones clave:**
- `client_secret`/`refresh_token` SOLO como valor asignado (regex `name[:=] "valor"`), porque la
  palabra suelta aparece en código legítimo (auth-setup.js, gsc-index.mjs…) → evita falsos positivos.
- El CANDADO (exit code) bloquea solo por secretos ACTUALES (working tree / archivo trackeado →
  exit 2). El historial NO bloquea (el pasado es inmutable; lo accionable es ROTAR, no "no
  publicar") → se reporta como ALTA pero exit sigue 0.
- check-infra excluye este checker de su barrido (exit≠0 es esperado), por eso está en NOT_PAGE_CHECKERS.
**Determinista:** SÍ. md5 idéntico en 2 corridas (879550...). Orden estable (sort antes de emitir).
**Prueba negativa (todas detectan, repo restaurado idéntico):**
- (1) secreto en working tree: scratch `zz-secret-scratch.txt` con `sk-…` → ALTA "posible openai-key" + **exit 2**; borrado.
- (2) archivo de secreto trackeado: `client_secret.json` force-added → ALTA "archivo … TRACKEADO" + **exit 2**; `git rm --cached` + borrado.
- (3) historial: detecta sobre el repo real (ver hallazgo real abajo); caso limpio → exit 0.
**Corrida real sobre el repo:** 1 hallazgo (HISTORIAL) — ver cola humana. Exit 0 (no bloquea publicación).

### #3 revisor-perf-real — ✅ HECHO (commit en esta rama) — ⚠️ requiere push SSH
**Qué valida:** Core Web Vitals reales (no el "score" de Lighthouse que se tiraba). Mediana de
varias corridas de LCP/CLS/INP comparada contra (a) presupuesto absoluto Google "good"
(LCP<2500ms, CLS<0.1, INP<200ms) y (b) regresión vs baseline (.pipeline/perf-baseline.json):
empeora >20% Y supera piso de ruido (LCP +200ms, CLS +0.02, INP +50ms).
**Fuentes:** (1) reportes Lighthouse JSON de site-monitor.yml (`PERF_REPORTS` o
`.pipeline/lighthouse-run-*.json`); (2) fallback puppeteer+Chrome (3 cargas, mismo stack que
check-produccion) para la corrida LOCAL del pipeline. Sin fuente → verificación ciega ALTA.
**Cambios en site-monitor.yml (⚠️ push por SSH):** la corrida de Lighthouse pasa de 1 a 3 y
guarda `.pipeline/lighthouse-run-{1,2,3}.json` (ya NO se tiran); nuevo step "Evaluar Core Web
Vitals" corre check-perf.mjs sobre los 3 reportes; nuevo step sube los JSON + `cwv-result.json`
como artefacto (retención 30d); el Issue de monitoreo se dispara también por regresión CWV.
.gitignore: se ignoran los reportes transitorios (`lighthouse-run-*.json`, `cwv-result.json`);
la baseline `perf-baseline.json` SÍ se versiona.
**Decisiones:** INP no existe en el "lab" de Lighthouse → si el audit no está, se usa TBT como
PROXY documentado (severidad media, no alta). Baseline se ESCRIBE solo con `--update-baseline`
(el checker normal solo REPORTA). INP/LCP/CLS mecánicos ya los caza revisor-plantilla; aquí se MIDE.
**Determinista:** SÍ sobre entradas fijas (reportes Lighthouse). md5 idéntico en 2 corridas con
fixtures (5d6e6c...). La medición LIVE con puppeteer es no-determinista por naturaleza (igual que
check-produccion), por eso la determinación se prueba con fixtures.
**Prueba negativa (fixtures, todas detectan):**
- sobre presupuesto: LCP~3000/CLS~0.2 → ALTA "LCP mediana 3000ms supera presupuesto 2500ms" + CLS.
- regresión: baseline LCP 1000 vs medido 3000 → media "LCP subió de 1000ms a 3000ms (+200%)".
- verificación ciega: reporte sin métricas → ALTA "no se pudieron MEDIR Core Web Vitals".
- fallback live: con PERF_URLS por defecto midió 2 URLs reales bajo presupuesto (puppeteer OK).
**Pendiente operativo (cola humana):** establecer la primera baseline tras el merge (correr
`--update-baseline` en un entorno con Lighthouse, idealmente CI) — ver cola humana abajo.

### #4 revisor-tracking — ✅ HECHO (commit en esta rama)
**Qué valida:** que el tracking REALMENTE funcione en producción, no solo que el snippet esté en
el HTML. Envuelve la lógica de `verificar-tracking.js` (snippet manual) en puppeteer (mismo stack
que check-produccion). Por página clave: (1) HTML referencia GTM (si no, página clave → media);
(2) dataLayer existe (si no con GTM → alta); (3) contenedor GTM carga (si no → alta); (4) GA:
sin GA4 configurado → alta; GA4 cargó pero sin beacon /g/collect → media con salvedad de consent.
**Descubrimiento clave (evitó falsos positivos):** el sitio DIFIERE GTM a propósito — lo carga en
la primera interacción (`scroll/click/touchstart/keydown`) o a los 12s (fallback), para proteger el
LCP (index.html líneas 107-120). Un primer borrador sin interacción daba falsos positivos
inconsistentes. El checker ahora SIMULA la interacción y hace POLL hasta 8s.
**Segundo descubrimiento (calibró severidad):** en prod, GTM + GA4 (G-NSV2K9N2ZD) cargan pero NO
se ve beacon /g/collect en headless — causa probable Consent Mode denegado por defecto (un usuario
real que acepta sí dispararía). Por eso ese caso es MEDIA + "verificar en GA4 Realtime", no ALTA
(evita crying-wolf diario). "Sin GA4 del todo" o "contenedor no carga" sí son ALTA.
**Determinista:** la parte local (fixture sin red) es determinista (md5 idéntico c2e600...). La
medición contra prod es no-determinista por naturaleza (red/headless), igual que check-produccion.
**Prueba negativa (fixtures locales + prod, todas detectan):**
- página clave sin GTM (fixture local) → media "NO referencia GTM".
- GTM con id inexistente GTM-FAKE0000 (fixture local, gtm.js 404) → alta "el CONTENEDOR no carga".
- prod real "/" → media (GA4 cargó, sin beacon: consent) — ver cola humana.
**Corrida real:** "/" → 1 media (consent). Detección coherente entre páginas tras el fix de interacción.

### #5 revisor-conversion — ✅ HECHO (commit en esta rama)
**Qué valida:** que cada página INDEXABLE tenga los caminos de conversión. (1) >=1 `tel:` con el
número correcto (667 392 2273 / 526673922273) → alta; (2) >=1 `wa.me`/api.whatsapp.com con
526673922273 → alta; (3) un CTA antes del fold (tel/wa o botón con clase btn-primary/cta/
floating-btn/emergency/whatsapp en hero/header/flotante) → media (heurístico); (4) formulario en
las páginas clave (/ y /contacto/) → alta.
**Decisión (acordada con Héctor):** "página clave con formulario" = solo / y /contacto/ (ambas ya
lo tienen → 0 falsos positivos). tel/wa/CTA se exigen en TODAS las indexables. "Form en cada
servicio" queda como posible mejora futura, no hallazgo.
**Validación de números:** tel: tolera `+526673922273`, `6673922273`, prefijo 52/521; wa.me exige
empezar con 526673922273. Calibrado sobre el markup real (btn-primary, floating-btn, etc.).
**Determinista:** SÍ, solo lee disco, orden estable (md5 idéntico df04ed...).
**Prueba negativa (fixtures scratch, todas detectan; repo restaurado):**
- sin tel/wa/CTA → 2 alta (sin tel, sin wa) + 1 media (sin CTA).
- tel/wa con número equivocado (+521112223333) → 2 alta (número incorrecto).
- canonical=/contacto/ sin <form> → alta "página clave sin form".
**Corrida real:** 99 páginas indexables analizadas, 0 hallazgos (el sitio ya está completo en
conversión: todas con tel/wa/CTA y las dos clave con formulario).

### #6 revisor-nap — ✅ HECHO (commit en esta rama)
**Qué valida:** consistencia NAP (señal de SEO local). Checker propio (NO toca check-plantilla, que
es de un revisor existente). (1) email `@plomeropro.com` → alta; (2) email del dominio bueno con
local-part != info → media; (3) nombre de negocio "de marca" (contiene "plomer") en JSON-LD de
nodos de negocio distinto al canónico → media; (4) nombre sin acento en texto → media; (5) telephone
de schema con dígitos != correctos → alta.
**Decisiones clave (evitaron falsos positivos masivos):**
- Filtro de MARCA ("plomer" en el name): descarta los Organization de reseñas (author/publisher
  "Google") que comparten @type Organization con el negocio. Sin esto daba 13+ falsos "name: Google".
- AGREGACIÓN del patrón "Marca – <Colonia>" (56 páginas de colonia con nombre localizado): un solo
  hallazgo + decisión humana, en vez de inundar con 55. Las variantes brand-like que NO empiezan con
  el canónico sí se reportan por página.
- Stem "plomer" (no "plomero") para cazar también "Plomería/Plomeria".
- Se saltan `.min.html` (artefactos no servidos) — por eso los 2 `contacto@` de index.min.html no se
  reportan (consistente con los demás checkers).
**Determinista:** SÍ (md5 idéntico 0a1e84...). 110 páginas analizadas.
**Prueba negativa (fixture scratch, todas detectan; repo restaurado):**
- email @plomeropro.com → alta; ventas@plomeroculiacanpro.mx → media; telephone +52 555… → alta;
- name "Plomeria Pro de Culiacan" → media "VARIANTE INESPERADA".
**Corrida real:** 2 hallazgos — (a) tecnico-de-gas: nombre SIN acento (media, fixable); (b) agregado:
56 colonias con "Marca – Colonia" (media, decisión humana). Ver cola humana.

### #7 revisor-enlazado-interno — ✅ HECHO (commit en esta rama)
**Qué valida:** grafo dirigido de enlaces internos (`<a href>`) entre páginas indexables. (1)
HUÉRFANAS = 0 enlaces entrantes (solo por sitemap) → media; (2) PROFUNDIDAD >3 clics desde "/"
(BFS) o inalcanzables por enlaces → media. Resuelve rutas relativas + alias (con/sin barra,
index.html) e ignora externos/mailto/tel/#. >8 del mismo tipo → se agregan.
**Determinista:** SÍ (output vacío estable). 99 nodos.
**Verificación del grafo (escéptica):** reconstruí el grafo aparte → 99 nodos, 904 aristas,
out-degree del home=31, distribución de profundidad {0:1, 1:31, 2:67}, 0 inalcanzables. Confirma
que el 0-hallazgos es real (no un bug de resolución): el sitio está bien interligado.
**Prueba negativa (fixtures, ambas ramas; repo restaurado):**
- `/zz-deep-a/` sin entrantes → media "es HUÉRFANA".
- `/zz-deep-b/` con entrante desde a pero inalcanzable desde home → media "a ∞ (inalcanzable) clics".
- (bug encontrado y corregido en el camino: depth None de páginas inalcanzables rompía `%d`).
**Corrida real:** 99 páginas, 0 hallazgos (sin huérfanas ni páginas a >3 clics).

---

## Cola humana / propuestas (de los revisores construidos)

### 🧑 [#2 — REAL, ALTA] Secreto de Google OAuth en el historial git
`check-secretos.sh` detectó que `client_secret.json` (Google OAuth: client_id
`13662482854-…apps.googleusercontent.com`, proyecto `odsappi-apuestas`, con su `client_secret`
real) fue **commiteado** en `8788d6ab` y removido en `e41ab25e` ("fix(security): remover
client_secret.json"). El secreto **sigue en el historial** → sigue expuesto.
**Acción humana requerida:** ROTAR/revocar ese client secret en Google Cloud Console (asúmelo
comprometido). Opcional: purgar el historial (`git filter-repo`) — decisión tuya; NO bloquea
publicación (el pasado es inmutable). NO lo hago yo: toca credenciales reales y reescritura de historia.

### 🧑 [#3 — operativo] Establecer la baseline de Core Web Vitals
Tras mergear, no hay `.pipeline/perf-baseline.json` (no se sembró con números falsos). Para
activar la detección de REGRESIÓN (no solo el presupuesto absoluto), correr una vez
`node .pipeline/check-perf.mjs --update-baseline` en un entorno con datos reales — idealmente CI
con Lighthouse (PERF_REPORTS apuntando a los lighthouse-run-*.json) y commitear el resultado, o
en local con puppeteer. No lo siembro yo porque mezclar métricas de puppeteer (local) con las de
Lighthouse (CI) para comparar regresión sería apples-to-oranges.

### 🧑 [#4 — verificar] ¿GA4 recibe hits en producción?
revisor-tracking observó en headless que GTM + GA4 (G-NSV2K9N2ZD) cargan pero NO sale el beacon
`/g/collect`. La causa más probable es Consent Mode denegado por defecto (headless no acepta el
banner). **Acción humana:** abrir el sitio en un navegador real, ACEPTAR consentimiento y mirar
GA4 → Realtime; si llegan hits, está bien (esperado). Si NO llegan ni aceptando, revisar el trigger
page_view de la etiqueta GA4 dentro del contenedor GTM-W75CRTX5. No es necesariamente un bug.

### 🧑 [#6 — REAL] Inconsistencias NAP detectadas
1. `servicios/tecnico-de-gas-culiacan/` usa "Plomero **Culiacan** Pro" (sin acento) en el texto —
   debería ser "Plomero Culiacán Pro". Fix mecánico simple.
2. 56 páginas de colonia usan nombre de negocio LOCALIZADO "Plomero Culiacán Pro – <Colonia>" en el
   schema. **Pregunta concreta:** ¿es intencional el sufijo por colonia? Si SÍ → lo dejo y ajusto el
   checker para aceptar el patrón "Marca – <Colonia>" (dejaría de reportarlo). Si NO → unificar todos
   los `name` de schema a "Plomero Culiacán Pro". No lo decido yo (afecta estrategia de SEO local).

### 💡 [#2 — PROPUESTA, no instalada] Hook pre-commit anti-secretos
Para atajar secretos ANTES de que entren al historial, propongo (sin instalar sin tu OK) un
`.git/hooks/pre-commit` (o `core.hooksPath`):
```sh
#!/bin/sh
# Aborta el commit si check-secretos.sh halla un secreto actual (exit 2).
out=$(bash .pipeline/check-secretos.sh) || code=$?
if [ "${code:-0}" -eq 2 ]; then
  echo "⛔ commit abortado: hay un secreto en el working tree / un archivo de secreto trackeado." >&2
  echo "$out" | grep -E '"descripcion"' >&2
  exit 1
fi
exit 0
```
Dime si lo instalo (es local, no se versiona; quedaría en tu máquina/cron).
