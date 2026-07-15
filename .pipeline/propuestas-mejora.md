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

