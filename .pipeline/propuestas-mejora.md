# Propuestas de mejora del pipeline de revisión

## 2026-07-14 — Huecos ciegos detectados (lote rotativo: cambio-de-tuberias, correccion-baja-presion, emergencia-24-7, instalacion-de-boiler, plomero-centro-culiacan)

Crítico de completitud. SOLO propuestas — no se modificó nada del pipeline ni del sitio.
Se revisaron los 22 archivos `revisor-*.md`, `docs/REGLAS.md`, `data/HISTORIAL.jsonl` y los 20 últimos commits. Los huecos de abajo son categorías de problema que HOY ningún revisor cubre, con evidencia real del lote.

---

### HUECO 1 — Longitud de `<title>` y `meta description` (truncamiento en SERP)
- **Por qué es hueco:** `revisor-indexabilidad`/`check-indexabilidad.py` mira title y description SOLO para DUPLICADOS; ninguno mide su LONGITUD. `revisor-seo` (LLM) es subjetivo y no lo garantiza. Evidencia del lote:
  - `cambio-de-tuberias` — title 71 chars ("Cambio de Tuberías… · Garantía 6 Meses"): supera el presupuesto ~60 char/580px → Google trunca "· Garantía 6 Meses".
  - `correccion-baja-presion` — meta description 171 chars: supera ~155-160 char → se corta en el resultado de búsqueda.
- **Acción:** ampliar `check-indexabilidad.py` (y su revisor) con un check determinista de longitud: title fuera de ~30-60 chars → media; description fuera de ~70-158 chars → media. Es mecánico y auto-detectable (el reescribir es pendiente humano/editorial).
- **Regla nueva para REGLAS.md:** "SEO/SERP: `<title>` ~30-60 chars y `meta description` ~70-158 chars en páginas indexables; fuera de rango Google trunca. AUTO en check-indexabilidad (longitud). Severidad: media."

### HUECO 2 — Canibalización de keyword primaria entre páginas + coherencia title↔H1↔slug (intención de búsqueda)
- **Por qué es hueco:** ningún revisor detecta DOS páginas compitiendo por la misma keyword primaria, ni que el `<title>` no coincida con el H1/URL de su propia página (intención de búsqueda). `revisor-contenido` cubre thin/duplicado/ortografía pero NO alineación de keyword. Evidencia:
  - `correccion-baja-presion` — H1 y slug = "corrección de baja presión", pero su `<title>` ARRANCA con "Bombas de Agua en Culiacán | Instalación y Baja Presión". La keyword primaria del title es de OTRO servicio.
  - `servicios/reparacion-de-bombas-de-agua/` TAMBIÉN lleva "bombas de agua" en su `<title>` → dos URLs canibalizando "bombas de agua en Culiacán". El commit a3cb5ef9 dijo "fin de canibalizacion de bombas", pero reincide en el title de correccion-baja-presion.
- **Acción:** (a) checker determinista ligero que extraiga el head-term del `<title>` (antes del primer `|`/`·`) y marque cuando 2+ páginas indexables comparten el mismo head-term, y cuando el head-term del title no aparece en el H1/slug de la propia página. (b) Ampliar la parte SUBJETIVA de `revisor-contenido` para juzgar intención de búsqueda/densidad. Nuevo revisor no hace falta; ampliar contenido + un check en check-indexabilidad.
- **Regla nueva:** "SEO/CANIBALIZACIÓN: el head-term del `<title>` (texto antes de `|`/`·`) debe (1) aparecer en el H1/slug de la propia página y (2) NO repetirse como head-term de otra página indexable. Caso: correccion-baja-presion titula 'Bombas de Agua', keyword de reparacion-de-bombas-de-agua. Severidad: media."

### HUECO 3 — `og:type` ausente / completitud Open Graph más allá de `og:image`
- **Por qué es hueco:** `check-plantilla.py` valida que `og:image`/`twitter:image` EXISTAN como archivo y (en blog) `og:locale`/`og:site_name`; pero no exige `og:type` en páginas de servicio. Evidencia:
  - `emergencia-24-7` — tiene og:title, og:description, og:image, og:url pero **NO tiene `og:type`** (las otras 4 del lote sí lo llevan = "website"). Preview social incompleto/inconsistente.
- **Acción:** ampliar `check-plantilla.py` para exigir en toda página indexable el set mínimo Open Graph: og:type, og:title, og:description, og:url, og:image (y twitter:card). Es determinista y auto-detectable; auto-fixer opcional (heredar de la home).
- **Regla nueva:** "SEO/OPEN-GRAPH: toda página indexable lleva og:type + og:title + og:description + og:url + og:image + twitter:card (emergencia-24-7 quedó sin og:type). AUTO en check-plantilla. Severidad: baja/media."

### HUECO 4 — Validación real de datos estructurados (validez de JSON-LD / Rich Results), no solo coherencia de URLs
- **Por qué es hueco:** `check-indexabilidad` compara URLs del JSON-LD (canonical==og:url==breadcrumb) y `check-plantilla` caza aggregateRating self-serving en blog. NINGUNO valida que el JSON-LD sea SINTÁCTICAMENTE válido, sin campos requeridos faltantes, ni advierte de bloat/anidamiento sospechoso (lo que rechazaría el Rich Results Test de Google). Evidencia:
  - `instalacion-de-boiler` — 108 KB (vs 36-52 KB de las hermanas), con un `@graph` gigante: 35 `Place`, 17 `Organization`, 12 `Service`, 12 `Offer`, 11 `ImageObject`, 6 `Review`. Volumen anómalo y no verificado contra ningún validador — riesgo de schema inválido/ignorado por Google que hoy pasa el pipeline.
- **Acción:** nuevo checker `check-schema.py` (o ampliar indexabilidad) que: parsee cada bloque `application/ld+json` (falla de parseo = alta), verifique campos requeridos por tipo clave (Service.name, Offer.price/priceCurrency, Review.author/reviewProperties, LocalBusiness.address/telephone) y marque volumen anómalo de nodos vs mediana de hermanas. Encaja como revisor determinista nuevo o dentro de revisor-indexabilidad.
- **Regla nueva:** "SEO/SCHEMA-VALIDEZ: cada bloque ld+json debe parsear y tener los campos requeridos de su @type; vigilar bloat (instalacion-de-boiler: 108KB, 35 Place/17 Organization). AUTO en check-schema. Severidad: media (alta si no parsea)."

### HUECO 5 — Paridad de rich results (estrellas) entre servicios hermanos + Review individual self-serving
- **Por qué es hueco:** `check-plantilla` check 15 valida el VALOR del rating site-wide (4.8/150), pero NO su PRESENCIA. Resultado: unas páginas de servicio muestran estrellas en el SERP y otras no. Evidencia:
  - `cambio-de-tuberias` — 0 AggregateRating (sin estrellas), mientras emergencia/instalacion/plomero-centro sí las tienen.
  - `correccion-baja-presion` — un ÚNICO `Review` con `ratingValue:"5"` (self-serving individual, y encima 5★ vs el 4.8 site-wide) sin AggregateRating.
  - Inconsistencia de cobertura de rich results entre hermanas del mismo negocio.
- **Acción:** ampliar check 15 de `check-plantilla` para reportar DISPARIDAD de presencia de AggregateRating entre páginas de servicio hermanas, y marcar Review sueltos self-serving (ratingValue inventado). La decisión "¿ponemos rating a todas o a ninguna?" es del `decisor-negocio`.
- **Regla nueva:** "SEO/SCHEMA-RATING: las páginas de servicio hermanas deben ser homogéneas en presencia de AggregateRating (cambio-de-tuberias sin estrellas vs hermanas con); nada de Review individuales 5★ self-serving (correccion-baja-presion). Severidad: media, decisión decisor-negocio."

### HUECO 6 (menor) — Frescura y formato de `<lastmod>` en el sitemap
- **Por qué es hueco:** `check-indexabilidad` valida que cada `<loc>` exista/200/canonical, pero NO el `<lastmod>`. Hay formatos MEZCLADOS (`2026-06-18` fecha-sola vs `2026-07-09T00:00:00+00:00` datetime) y el lastmod más nuevo es 2026-07-09 pese a ediciones diarias → señal de frescura estancada/inconsistente para el rastreo.
- **Acción:** ampliar `check-indexabilidad` para exigir formato ISO uniforme del `<lastmod>` y compararlo con el mtime de git del archivo (desfase grande → media). Mecánico/auto-derivable.
- **Regla nueva:** "SEO/SITEMAP: `<lastmod>` en formato ISO uniforme y coherente con la fecha real de última edición (git). Formatos mixtos hoy. Severidad: baja."


---

## 2026-07-23 — Huecos ciegos detectados (lote rotativo: instalacion-de-sanitarios, mantenimiento-de-boiler, plomeria-comercial, plomero-zona-norte-culiacan, plomero-zona-sur-culiacan)

Crítico de completitud (FASE 3). SOLO propuestas — no se modificó nada del pipeline ni del sitio.
Se compararon las 5 páginas del lote contra el esqueleto (home) y hermanas sanas. Abajo, categorías que HOY ningún revisor cubre, con evidencia real del lote. Se evita re-listar los 6 huecos del 2026-07-14; el único que se repite se marca como RECURRENCIA.

### HUECO 7 — Piso de enlazado interno SALIENTE / paridad de cross-sell entre hermanas (media)
- **Por qué es hueco:** `revisor-enlazado-interno` (`check-linking.py`) solo caza huérfanas (0 enlaces ENTRANTES) y profundidad > 3 clics. NINGÚN revisor mira la escasez de enlaces SALIENTES contextuales: una página puede no estar huérfana (la alcanza el footer/nav) y aun así no repartir autoridad ni ofrecer rutas de navegación temática. Evidencia del lote (enlaces en el CUERPO a páginas hermanas `/servicios/…` o `/blog/…`, distintos):
  - `servicios/mantenimiento-de-boiler/` — **0** enlaces salientes en el cuerpo a hermanas.
  - `servicios/instalacion-de-sanitarios/` — **1**.
  - `servicios/plomeria-comercial/`, `plomero-zona-norte-culiacan/`, `plomero-zona-sur-culiacan/` — **6 cada una** (tejidos en prosa: baja-presión, instalación-de-boiler, emergencia-24-7, colonias, cerca-de-mí…).
  - Ninguna de las 3 páginas de servicio tiene una sección "Servicios relacionados"; las zona-pages compensan con enlaces en prosa, pero boiler/sanitarios quedaron casi sin salientes. Viola de facto la regla 2026-06-18 ("cross-sell como las hermanas") pero ningún checker lo verifica.
- **Acción:** ampliar `check-linking.py` (revisor-enlazado-interno) para marcar toda página indexable cuyos enlaces SALIENTES en el cuerpo a hermanas `/servicios/` o `/blog/` caigan bajo un PISO (p.ej. < 3) o muy por debajo de la mediana de sus hermanas. Auto-detectable; el arreglo (elegir a qué hermanas enlazar) lo hace el fixer-autonomo copiando el patrón de una hermana sana.
- **Regla nueva para REGLAS.md:** "SEO/ENLAZADO-SALIENTE: cada página de servicio/zona indexable debe tejer ≥3 enlaces internos en el cuerpo a hermanas relevantes (boiler tenía 0, sanitarios 1 vs 6 de las hermanas). AUTO en check-linking (piso saliente + paridad vs mediana). Severidad: media."

### HUECO 8 — Review/Rating self-serving en páginas de SERVICIO (no solo /blog/) + disparidad de cobertura (media)
- **Por qué es hueco:** `check-plantilla.py` check 3 caza `aggregateRating`/`Review` self-serving SOLO si la ruta empieza con `blog/` (`if r.startswith("blog/")`, línea 327). Las páginas de SERVICIO quedan fuera del check. Evidencia:
  - `mantenimiento-de-boiler` y `instalacion-de-sanitarios` incrustan cada una 3 `Review` + 3 `Rating` con autores tipo Persona ("Ricardo P.", "Sandra V.", "Alejandro M." / "Fernando S.", "Claudia M.", "Jorge L.") — reseñas self-serving en el propio marcado del negocio (Google no muestra rich-results de reseñas auto-servidas en las páginas de la propia organización desde 2019; señal ignorada, y roza la regla 2026-06-18 "NO inventar testimonios").
  - DISPARIDAD: solo **10 de 28** páginas de servicio llevan `Review`; las otras 18 no. Cobertura de rich-results incoherente entre hermanas (mismo hueco que HUECO 5 del 07-14, ahora confirmado a escala de todo `/servicios/`).
- **Acción:** (a) extender el SCOPE del check 3 de `check-plantilla.py` para reportar `Review`/`Rating` self-serving (autor Persona inventado) en páginas de servicio, no solo blog; (b) reportar DISPARIDAD de presencia de Review/AggregateRating entre servicios hermanos. La decisión "¿reseñas reales en todas, o en ninguna?" es del `decisor-negocio` (no inventar).
- **Regla nueva:** "SEO/SCHEMA-REVIEW: `Review`/`Rating` con autor Persona en el marcado del propio negocio (servicio) es self-serving — Google lo ignora; 10/28 servicios lo llevan (boiler, sanitarios…), el resto no = incoherente. AUTO en check-plantilla check 3 (scope ampliado a servicio + paridad). Severidad: media, decisión decisor-negocio."

### RECURRENCIA — Longitud de `<title>` sigue SIN mecanizarse (baja)
- **Estado:** el HUECO 1 del 2026-07-14 propuso un check de longitud de title/description; NO se implementó. `check-indexabilidad.py` sigue mirando solo DUPLICADOS de title (línea 386), no longitud. Reaparece en este lote: `mantenimiento-de-boiler` title = **70 chars** e `instalacion-de-sanitarios` = **67 chars** (> ~60 → Google trunca la cola "· Gas, Solar y Paso" / "WC, Lavabos y Mezcladoras"). Las descripciones (155-163) están dentro de rango.
- **Acción:** mecanizar ya el check de longitud de `<title>` (~30-60 chars) en `check-indexabilidad.py`; el reescribir es editorial pero la detección es mecánica y hoy ciega.

### NO es hueco (confirmación positiva) — FAQPage vs FAQ visible
- `instalacion-de-sanitarios` (5 preguntas en FAQPage vs 6 visibles) y `mantenimiento-de-boiler` (6 vs 7) tienen mismatch, PERO ya lo caza `check-plantilla.py` check 21 (`faq-mismatch-20260721`). Es backlog conocido (las "12 páginas" del 07-21), no un hueco ciego. El checker funciona.

**Resumen del lote:** 2 huecos NUEVOS (enlazado saliente/cross-sell; Review self-serving en servicio) + 1 RECURRENCIA no mecanizada (longitud de title). El resto de lo detectado ya lo cubre un checker existente.

---

## 2026-07-24 — Huecos ciegos detectados (lote rotativo: las-quintas, destape-de-drenajes, blog/como-identificar-buen-plomero, blog/cuanto-cuesta-plomeria-bano-completo, reparacion-de-llaves-y-mezcladoras)

Crítico de completitud (FASE 3). SOLO propuestas — no se modificó nada del pipeline ni del sitio.
Se revisaron las 5 páginas del lote + 4 con cambios de ayer (instalacion-de-sanitarios, mantenimiento-de-boiler, plomero-zona-norte, home). No se re-listan los HUECOS 1-8; abajo van 2 huecos NUEVOS + 2 RECURRENCIAS confirmadas/ampliadas.

### HUECO 9 (NUEVO) — Headers de respuesta de seguridad (HSTS / CSP / Permissions-Policy) sin verificar (media)
- **Por qué es hueco:** `netlify.toml` define 4 headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`) pero le FALTAN `Strict-Transport-Security` (HSTS — Netlify NO lo pone por defecto), `Content-Security-Policy` y `Permissions-Policy`. Ningún checker mira la sección `[[headers]]`: `check-indexabilidad.py` y `check-plantilla.py` leen `netlify.toml` SOLO para redirects/canonical (líneas 64/81 y 122/307), nunca para headers de seguridad. Categoría "seguridad básica" del brief, hoy 100% ciega.
- **Acción:** ampliar `revisor-produccion` o `revisor-infra-salud` con un check estático que parsee el bloque `[[headers]] for="/*"` de `netlify.toml` y marque ausencia de HSTS/CSP/Permissions-Policy. Determinista y auto-detectable; el valor del CSP es decisión humana (GTM/Clarity/Google inline lo complican → severidad media, no auto-fix ciego).
- **Regla nueva para REGLAS.md:** "SEGURIDAD/HEADERS: `netlify.toml` debe declarar HSTS (`Strict-Transport-Security`), `Content-Security-Policy` y `Permissions-Policy` además de los 4 headers ya presentes. Ningún checker lo cubría hasta hoy. Severidad: media."

### HUECO 10 (NUEVO) — Frescura de `dateModified` de Article y fecha visible al lector (media)
- **Por qué es hueco:** distinto de HUECO 6 (ese era `<lastmod>` de sitemap). Aquí es el `dateModified`/`datePublished` del JSON-LD `Article` y la fecha visible. Evidencia (git-edit de TODOS los posts = 2026-07-21):
  - `blog/cuanto-cuesta-plomeria-bano-completo` — `dateModified` == `datePublished` == **2025-11-18** (nunca se bumpeó pese a ediciones); `marcha-paz-culiacan-2025` 2025-09-07; `como-detectar-fugas`/`problemas-comunes` 2025-11-21. El `dateModified` está DESACOPLADO de las ediciones reales de contenido (p.ej. cuando el pipeline corrige precios en una FAQ, no se bumpea) → señal de frescura estancada para Google.
  - FECHA VISIBLE: solo **4 de 13** posts muestran "Publicado/Actualizado" al lector (como-identificar, cuanto-cobra-visita, drenaje-tapado, marcha-paz); los otros 9 no → E-E-A-T inconsistente entre hermanas y desalineado con el schema.
- **Acción:** (a) check determinista que compare `dateModified` del Article con la última fecha de edición de CONTENIDO (no de CSS/cache-bust) y marque desfase grande; (b) verificar presencia/consistencia de la fecha visible en `/blog/` (todas o ninguna). Ampliar `revisor-contenido` (parte mecánica) o `check-indexabilidad`. El bump correcto de `dateModified` debería engancharse al fixer que edita prosa/precios.
- **Regla nueva:** "SEO/FRESCURA-ARTICLE: `dateModified` del JSON-LD Article debe bumpearse cuando cambia el CONTENIDO (no en cache-bust de CSS) y coincidir con una fecha visible presente en TODOS los posts. Hoy 4/13 muestran fecha y varios `dateModified` llevan meses congelados. Severidad: media."

### RECURRENCIA (HUECO 2) — title↔H1↔slug divergente, ahora confirmado en BLOG y aún sin mecanizar (media)
- **Estado:** `blog/cuanto-cuesta-plomeria-bano-completo-culiacan` — `<title>` = "Lista de Precios de Plomería en Culiacán 2026 — Cotización Gratis" (head-term genérico "lista de precios de plomería") mientras H1 = "Plomería de Baño Completo en Culiacán" y slug = "…bano-completo…". El title apunta a una keyword MÁS AMPLIA y distinta del tema real de la página (baño completo) → intención de búsqueda difusa y riesgo de canibalizar con una futura página genérica de precios. Confirma que el HUECO 2 (head-term del title vs H1/slug) sigue sin mecanizarse y aplica también a `/blog/`.
- **Acción:** mecanizar ya el check de coherencia head-term(title) ⊂ {H1, slug} propuesto el 2026-07-14, extendido a blog. Detección mecánica; reescritura editorial.

### RECURRENCIA/AMPLIACIÓN (HUECO 5/8) — heterogeneidad de @type de schema entre hermanas, no solo AggregateRating (media)
- **Estado:** más amplio que "presencia de AggregateRating". Tipos de nodo por página del lote:
  - `destape-de-drenajes` — Service + AggregateRating + Review + Person + AggregateOffer + LocalBusiness + Organization + WebSite (set completo).
  - `reparacion-de-llaves-y-mezcladoras` — Service + AggregateOffer, pero **SIN** Review/AggregateRating/LocalBusiness/Organization/WebSite.
  - `plomero-colonias-culiacan/las-quintas` — **SIN** Service ni LocalBusiness (solo Place/FAQPage/Breadcrumb).
  El grafo de entidades (LocalBusiness/Organization/WebSite/Service) es INCONSISTENTE entre páginas del mismo negocio, no solo las estrellas.
- **Acción:** ampliar el check de disparidad (HUECO 5/8) para comparar el CONJUNTO de @type de schema entre hermanas del mismo tipo de página (servicio vs colonia) y marcar las que carezcan del núcleo esperado (Service/LocalBusiness/Organization/WebSite). Decisión de qué núcleo va en cada plantilla: `decisor-negocio`.

**Resumen del lote:** 2 huecos NUEVOS (headers de seguridad HSTS/CSP; frescura de dateModified + fecha visible en blog) + 2 RECURRENCIAS confirmadas y aún sin mecanizar (title↔H1↔slug en blog; heterogeneidad de @type de schema entre hermanas). Longitud de title (HUECO 1) esta vez OK en el lote (todas ≤65 chars). Sin mixed-content, sin anchors rotos, sin duplicados de title/description, jerarquía de headings correcta.
