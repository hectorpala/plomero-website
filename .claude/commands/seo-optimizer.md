# SEO Optimizer

Analiza y optimiza SEO de páginas HTML con reporte detallado y mejoras automáticas.

## Qué hace este comando

1. **Analiza keywords** - Densidad, posición en elementos críticos (H1, H2, title, meta)
2. **Valida meta tags** - Title, description, Open Graph, Twitter Cards, canonical
3. **Verifica schemas JSON-LD** - Sintaxis, tipos, campos obligatorios, validación Schema.org
4. **Analiza imágenes** - Alt text, formatos (WebP), tamaños, lazy loading
5. **Revisa enlaces internos** - Estructura, breadcrumbs, sitemap
6. **Valida performance SEO** - Headings hierarchy, structured data, semantic HTML
7. **Genera reporte priorizado** - Lista de mejoras con impacto SEO estimado

## Uso

```
/seo-optimizer <archivo>
```

Ejemplos:
```
/seo-optimizer index.html
/seo-optimizer plomero-24-horas/index.html
/seo-optimizer servicios/destape-drenaje/index.html
```

## Instrucciones para Claude

Cuando el usuario ejecute `/seo-optimizer <archivo>`, sigue estos pasos:

### Paso 1: Leer el archivo HTML

Leer el archivo especificado usando Read tool.

Si no existe, reportar error:
```
❌ Archivo no encontrado: <archivo>
```

### Paso 2: Analizar Keywords

Extraer keyword principal de:
- Title tag
- H1
- Meta description
- URL path

Calcular:
- **Densidad keyword** - Apariciones totales / palabras totales × 100
  - Óptimo: 1-2%
  - Aceptable: 0.5-3%
  - Problema: <0.5% (keyword stuffing si >3%)

- **Posición en elementos críticos:**
  - ✅ H1 contiene keyword
  - ✅ Title contiene keyword (primeros 30 caracteres)
  - ✅ Meta description contiene keyword
  - ✅ Primera frase del contenido (<100 palabras)
  - ✅ URL contiene keyword

- **Variaciones semánticas:**
  - Detectar keywords relacionadas (plurales, sinónimos)
  - Ejemplo: "plomero" → "plomería", "plomeros", "fontanero"

**Output:**
```
✅ Keywords
  • Keyword principal: "plomero 24 horas"
  • Densidad: 1.2% (8 menciones en 667 palabras) ✓
  • Posición:
    ✅ H1: "Plomero 24 Horas en Culiacán"
    ✅ Title (posición 0): "Plomero 24 Horas Culiacán..."
    ✅ Meta description (posición 12)
    ✅ Primera frase del contenido
    ✅ URL: /plomero-24-horas/
  • Variaciones: "plomero", "plomería 24h", "plomero nocturno" (3)
```

O si hay problemas:
```
⚠️ Keywords
  • Keyword principal: "plomero urgente"
  • Densidad: 0.3% (2 menciones en 667 palabras) ❌ BAJA
  • Posición:
    ✅ H1: "Plomero Urgente en Culiacán"
    ❌ Title no contiene keyword (tiene "Fontanero rápido...")
    ✅ Meta description
    ❌ No aparece en primeras 100 palabras
    ✅ URL: /plomero-urgente/

💡 Recomendación:
  - Agregar 3-4 menciones más de "plomero urgente"
  - Actualizar title: "Plomero Urgente Culiacán 24/7..."
  - Mencionar keyword en primer párrafo
```

### Paso 3: Validar Meta Tags

Verificar presencia y formato de:

#### Title Tag
- Longitud: 50-60 caracteres (óptimo), max 70
- Contiene keyword principal
- Formato: "Keyword | Modificador | Marca"
- No repetido (único por página)

#### Meta Description
- Longitud: 120-155 caracteres (óptimo), max 160
- Contiene keyword + CTA
- Formato: "Descripción con keyword. CTA. Contacto."

#### Canonical URL
- Presente
- URL absoluta
- Apunta a la URL correcta

#### Open Graph (Facebook)
- og:title (max 60 caracteres)
- og:description (max 155 caracteres)
- og:image (min 1200×630px)
- og:url (URL canónica)
- og:type (website, article, etc.)
- og:locale (es_MX)

#### Twitter Cards
- twitter:card (summary_large_image)
- twitter:title
- twitter:description
- twitter:image

#### Otros
- Robots meta (noindex?, nofollow?)
- Hreflang (si multiidioma)
- Viewport (responsive)

**Output:**
```
✅ Meta Tags
  • Title: 58 caracteres ✓
    "Plomero 24 Horas Culiacán | Emergencias | Plomero Pro"
  • Description: 142 caracteres ✓
    "Plomero 24 horas en Culiacán. Llegamos en 15-30 min. WhatsApp 667-392-2273"
  • Canonical: ✓ https://plomeroculiacanpro.mx/plomero-24-horas/

  Open Graph:
  • og:title: ✓
  • og:description: ✓
  • og:image: ❌ FALTA
  • og:url: ✓
  • og:type: ✓ website
  • og:locale: ✓ es_MX

  Twitter Cards:
  • twitter:card: ❌ FALTA
  • twitter:title: ❌ FALTA
  • twitter:description: ❌ FALTA
  • twitter:image: ❌ FALTA

💡 Recomendación:
  - Agregar og:image (1200×630px)
  - Agregar Twitter Cards completas
```

### Paso 4: Verificar Schemas JSON-LD

Buscar `<script type="application/ld+json">` en el HTML.

Para cada schema encontrado:

1. **Parsear JSON** - Verificar sintaxis válida
2. **Identificar @type** - WebSite, LocalBusiness, Service, FAQPage, BreadcrumbList, etc.
3. **Validar campos obligatorios** según tipo:

#### WebSite
- @type: "WebSite"
- name ✓
- url ✓
- logo (opcional pero recomendado)

#### LocalBusiness / HomeAndConstructionBusiness
- @type
- name ✓
- address (streetAddress, addressLocality, addressRegion, postalCode, addressCountry) ✓
- telephone ✓
- openingHoursSpecification ✓
- geo (latitude, longitude) - **MUY IMPORTANTE para "cerca de mí"**
- aggregateRating (opcional pero recomendado)
- priceRange (opcional pero recomendado)

#### Service
- @type: "Service"
- serviceType ✓
- provider ✓
- areaServed ✓
- description (recomendado)

#### FAQPage
- @type: "FAQPage"
- mainEntity (array de Questions) ✓
- Cada Question:
  - @type: "Question"
  - name ✓
  - acceptedAnswer ✓
    - @type: "Answer"
    - text ✓

#### BreadcrumbList
- @type: "BreadcrumbList"
- itemListElement ✓
- Cada item:
  - @type: "ListItem"
  - position ✓
  - name ✓
  - item (URL) ✓

**Output:**
```
✅ JSON-LD Schemas (5 schemas válidos)

  1. WebSite ✓
     • name: "Plomero Culiacán Pro"
     • url: ✓
     • logo: ✓

  2. HomeAndConstructionBusiness ✓
     • name: ✓
     • address: ✓ (Culiacán, Sinaloa)
     • telephone: ✓ +52 667 392 2273
     • geo: ✓ (24.8093, -107.3940) ← EXCELENTE para SEO local
     • aggregateRating: ✓ 4.8/5 (150 reviews)
     • openingHours: ✓ 24/7

  3. Service ✓
     • serviceType: "Plomería 24 Horas"
     • provider: ✓
     • areaServed: ✓ Culiacán

  4. FAQPage ✓
     • 10 Questions/Answers ✓

  5. BreadcrumbList ✓
     • 4 niveles ✓

🎯 Schema Score: 100/100
   • Todos los schemas válidos
   • GPS coordinates presentes (clave para "cerca de mí")
   • Rich snippets: Estrellas, Breadcrumbs, FAQ
```

O si hay errores:
```
⚠️ JSON-LD Schemas (3 válidos, 1 con errores)

  1. WebSite ✓

  2. LocalBusiness ⚠️
     • name: ✓
     • address: ✓
     • telephone: ✓
     • geo: ❌ FALTA ← Crítico para "plomero cerca de mí"
     • aggregateRating: ❌ FALTA (perderías rich snippets con estrellas)

  3. Service ✓

  4. FAQPage ❌ ERROR SINTAXIS
     Error en línea 156: Expected ',' but got '}'

🎯 Schema Score: 65/100

💡 Recomendaciones prioritarias:
  1. Agregar geo coordinates a LocalBusiness
  2. Agregar aggregateRating (4.8/5)
  3. Corregir sintaxis FAQPage
```

### Paso 5: Analizar Imágenes

Buscar todas las tags `<img>` en el HTML.

Para cada imagen verificar:

1. **Alt text**
   - Presente ✓
   - Descriptivo (>5 palabras)
   - Contiene keyword (si es relevante)
   - No es keyword stuffing

2. **Formato**
   - WebP ✓ (mejor)
   - AVIF ✓ (mejor aún)
   - JPG/PNG ⚠️ (convertir a WebP)

3. **Lazy loading**
   - loading="lazy" presente (excepto hero/LCP)
   - fetchpriority="high" en imagen LCP

4. **Dimensiones**
   - width y height especificados (previene CLS)

5. **Tamaño archivo** (si es accesible)
   - <100KB ✓ (óptimo)
   - 100-200KB ⚠️ (aceptable)
   - >200KB ❌ (optimizar)

**Output:**
```
✅ Imágenes (5 imágenes analizadas)

  1. logo-plomero-culiacan-pro.webp ✓
     • Alt: "Plomero Culiacán Pro - Logo empresa plomería" ✓
     • Formato: WebP ✓
     • Lazy: No (es LCP) ✓
     • Dimensiones: 512×512 ✓
     • Tamaño: 16KB ✓

  2. hero-plomero-24-horas.webp ✓
     • Alt: "Plomero profesional reparando fuga emergencia 24 horas" ✓
     • Formato: WebP ✓
     • fetchpriority: high ✓
     • Dimensiones: 1200×800 ✓
     • Tamaño: 85KB ✓

  3. reparacion-fugas.webp ✓
     • Alt: "Reparación de fugas de agua" ✓
     • Formato: WebP ✓
     • Lazy: ✓
     • Dimensiones: 800×800 ✓

  4. servicio-destape.jpg ⚠️
     • Alt: ✓ "Destape de drenajes profesional"
     • Formato: JPG ❌ (convertir a WebP)
     • Lazy: ✓
     • Dimensiones: ❌ FALTAN width/height (causa CLS)
     • Tamaño: 245KB ❌ (demasiado grande)

  5. emergencia-icon.svg ✓
     • Alt: ✓
     • Formato: SVG ✓
     • Dimensiones: ✓

🎯 Imágenes Score: 80/100

💡 Recomendaciones:
  1. Convertir servicio-destape.jpg → WebP (-60% tamaño)
  2. Agregar width/height a servicio-destape
  3. Optimizar servicio-destape: 245KB → <100KB
```

### Paso 6: Revisar Estructura HTML Semántica

Verificar:

#### Headings Hierarchy
- Un solo H1 ✓
- H2-H6 en orden correcto (no saltar niveles)
- Keywords en headings principales

#### Semantic HTML
- `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- `<time>` para fechas
- `<address>` para contacto

#### Enlaces Internos
- Enlaces a otras páginas del sitio
- Anchor text descriptivo (no "click aquí")
- No broken links

#### Breadcrumbs
- Presentes en HTML
- Matches BreadcrumbList schema

**Output:**
```
✅ Estructura HTML

  Headings:
  • H1 (1): "Plomero 24 Horas en Culiacán" ✓
  • H2 (6): Todos relevantes ✓
  • H3 (4): ✓
  • Jerarquía: ✓ Sin saltos de nivel

  Semantic HTML:
  • <header> ✓
  • <nav> ✓
  • <main> ✓
  • <section> ✓ (8 secciones)
  • <footer> ✓

  Enlaces Internos:
  • 15 enlaces internos ✓
  • Anchor text descriptivo ✓
  • No broken links ✓

  Breadcrumbs:
  • HTML: ✓
  • Schema: ✓ (sincronizados)
```

### Paso 7: Generar Reporte Final con Prioridades

Consolidar todos los análisis en un reporte final con:

1. **Score general** (0-100)
2. **Sección por sección** (Keywords, Meta, Schemas, Imágenes, HTML)
3. **Lista priorizada de mejoras** con impacto estimado

**Criterios de prioridad:**

- **🔴 CRÍTICO (P0)** - Impacto SEO alto, fácil de arreglar
  - Falta geo coordinates en LocalBusiness
  - Title/description faltantes o mal optimizados
  - H1 faltante o duplicado
  - Keyword density <0.5%

- **🟠 ALTO (P1)** - Impacto SEO medio-alto
  - Falta aggregateRating en schema
  - Falta Open Graph image
  - Imágenes >200KB sin optimizar
  - Keywords no en primeros 100 palabras

- **🟡 MEDIO (P2)** - Impacto SEO medio
  - Falta Twitter Cards
  - Imágenes sin lazy loading
  - JPG/PNG sin convertir a WebP
  - Falta canonical URL

- **🟢 BAJO (P3)** - Mejoras incrementales
  - Agregar más variaciones de keywords
  - Optimizar anchor text
  - Agregar más FAQs

**Output final:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Análisis SEO: plomero-24-horas/index.html
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Score General: 82/100

✅ Keywords               95/100
✅ Meta Tags              85/100
✅ JSON-LD Schemas       100/100
⚠️ Imágenes               70/100
✅ Estructura HTML        90/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Mejoras Prioritarias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRÍTICO (P0) - Arreglar YA

  1. Agregar Open Graph image
     Impacto: Alto (mejora CTR en redes sociales)
     Esfuerzo: 5 min
     Acción: Agregar <meta property="og:image" content="...hero.webp">

🟠 ALTO (P1) - Próxima sesión

  2. Convertir servicio-destape.jpg a WebP
     Impacto: Medio (reduce LCP ~150ms)
     Esfuerzo: 2 min
     Acción: cwebp servicio-destape.jpg -o servicio-destape.webp -q 85

  3. Agregar Twitter Cards
     Impacto: Medio (mejora CTR en Twitter/X)
     Esfuerzo: 3 min

🟡 MEDIO (P2) - Cuando tengas tiempo

  4. Agregar width/height a servicio-destape
     Impacto: Bajo (reduce CLS)
     Esfuerzo: 1 min

  5. Aumentar keyword density 0.8% → 1.2%
     Impacto: Bajo
     Esfuerzo: 5 min
     Acción: Agregar 2-3 menciones naturales de "plomero 24 horas"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ¿Quieres que implemente las mejoras automáticamente? (s/n)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Paso 8: Implementar mejoras automáticas (opcional)

Si el usuario responde "s" (sí), implementar las mejoras que sean automatizables:

**Mejoras automatizables:**
- ✅ Agregar meta tags faltantes (og:image, twitter cards, canonical)
- ✅ Agregar width/height a imágenes (si se pueden detectar dimensiones)
- ✅ Agregar lazy loading a imágenes
- ✅ Corregir errores de sintaxis en JSON-LD
- ❌ NO automatizar: Cambios de contenido (keywords, descripciones)

**Proceso:**
1. Hacer backup del archivo: `<archivo>.backup-seo`
2. Aplicar cambios usando Edit tool
3. Reportar cambios realizados
4. Preguntar si desea ver diff o publicar

```
✅ Mejoras implementadas en plomero-24-horas/index.html

Cambios realizados:
  • Agregado og:image (1200×630)
  • Agregado Twitter Cards (4 meta tags)
  • Agregado width/height a servicio-destape.jpg
  • Agregado lazy loading a 3 imágenes

Backup creado: plomero-24-horas/index.html.backup-seo

Nuevo Score SEO: 82 → 92 (+10 puntos)

¿Quieres publicar estos cambios?
  • Ver diferencias: diff
  • Publicar ahora: /deploy-quick
  • Revertir cambios: revert
```

## Notas importantes

- **NO cambiar contenido** sin confirmación explícita del usuario
- **NO modificar diseño visual** (solo meta tags y atributos técnicos)
- **SIEMPRE crear backup** antes de modificar archivos
- **Validar JSON-LD** antes de guardar (sintaxis correcta)
- **Reportar claramente** qué se cambió y por qué

## Ejemplos de uso

### Ejemplo 1: Análisis rápido sin cambios

```
Usuario: /seo-optimizer index.html

Claude:
[Genera reporte completo con score 88/100]

¿Quieres que implemente las mejoras automáticamente? (s/n)

Usuario: n

Claude: Ok, reporte guardado. Puedes revisar las recomendaciones cuando quieras.
```

### Ejemplo 2: Análisis + implementación automática

```
Usuario: /seo-optimizer plomero-urgente/index.html

Claude:
[Genera reporte con score 75/100, 3 mejoras críticas]

¿Quieres que implemente las mejoras automáticamente? (s/n)

Usuario: s

Claude:
✅ Mejoras implementadas
   • og:image agregado
   • Twitter Cards agregados
   • 2 imágenes optimizadas

Nuevo Score: 75 → 90 (+15 puntos)

Usuario: /deploy-quick

Claude: [Publica cambios con commit message optimizado]
```

### Ejemplo 3: Detectar problema grave

```
Usuario: /seo-optimizer servicios/instalacion-boiler/index.html

Claude:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Análisis SEO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Score General: 45/100 ⚠️

❌ Keywords               30/100 - CRÍTICO
   • Keyword density: 0.1% (demasiado baja)
   • H1 faltante
   • Title duplicado con homepage

⚠️ JSON-LD Schemas        40/100
   • Sin geo coordinates
   • Sin aggregateRating
   • FAQPage con error sintaxis

🔴 URGENTE: Esta página tiene problemas SEO graves
   1. Agregar H1 único
   2. Cambiar title (actualmente duplicado)
   3. Aumentar menciones de keyword
   4. Corregir JSON-LD

¿Quieres que te ayude a arreglar estos problemas?
```

## Cálculo de Score

**Score General** (promedio ponderado):

- Keywords: 25%
- Meta Tags: 20%
- JSON-LD Schemas: 25%
- Imágenes: 15%
- Estructura HTML: 15%

**Interpretación:**
- 90-100: Excelente
- 80-89: Muy bueno
- 70-79: Bueno (hay mejoras fáciles)
- 60-69: Regular (necesita trabajo)
- <60: Crítico (problemas graves)
