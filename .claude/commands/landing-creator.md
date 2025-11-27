# Landing Creator

Crea nuevas landing pages clonando el estilo exacto de plomeroculiacanpro.mx. Solo necesitas proporcionar contenido y fotos.

## Qué hace este comando

1. **Clona estilos exactos** - Copia todos los estilos, colores, fuentes, botones de index.html
2. **Estructura idéntica** - Header, hero, secciones, footer iguales
3. **SEO completo** - Meta tags, Open Graph, JSON-LD schemas automáticos
4. **Responsive** - Mobile-first como la homepage
5. **Solo pides contenido** - Tú solo das textos y rutas de imágenes

## Uso

```
/landing-creator
```

El comando te pedirá la información necesaria paso a paso.

## Instrucciones para Claude

Cuando el usuario ejecute `/landing-creator`, sigue este proceso interactivo:

### Paso 1: Solicitar información básica

Preguntar al usuario (uno por uno, esperar respuesta):

```
🎨 Vamos a crear tu landing page con el estilo de plomeroculiacanpro.mx

1️⃣ ¿Cuál es el slug de la página? (ejemplo: plomero-urgente)
   Se creará en: /<slug>/index.html
```

Esperar respuesta del usuario.

```
2️⃣ ¿Cuál es la keyword principal? (ejemplo: plomero urgente)
   Esto se usará en title, H1, meta description
```

Esperar respuesta.

```
3️⃣ ¿Cuál es el título H1? (ejemplo: Plomero Urgente en Culiacán 24/7)
   Máximo 60 caracteres recomendado
```

Esperar respuesta.

```
4️⃣ ¿Meta description? (ejemplo: Plomero urgente en Culiacán con llegada inmediata...)
   120-155 caracteres recomendado
```

Esperar respuesta.

### Paso 2: Solicitar contenido del hero

```
5️⃣ ¿Subtítulo del hero? (el texto debajo del H1)
   Ejemplo: Atención inmediata en toda la ciudad. Llegada en 15-30 min.
```

Esperar respuesta.

```
6️⃣ ¿Ruta de la imagen hero? (debe existir en assets/images/)
   Ejemplo: emergencia-hero-1200w.webp

   IMPORTANTE: La imagen debe estar en formato WebP y ser responsiva
   Debes tener versiones: 800w y 1200w
```

Esperar respuesta.

### Paso 3: Solicitar secciones de contenido

```
7️⃣ ¿Cuántas secciones de beneficios quieres? (recomendado: 4)
   Ejemplo: Respuesta rápida, Sin sobrecargos, Garantía 6 meses, Técnicos certificados
```

Esperar respuesta.

Para cada beneficio:
```
Beneficio #1:
  • Título: [esperar]
  • Descripción corta: [esperar]
  • Ícono SVG (opcional, se usará uno por defecto): [esperar o skip]
```

### Paso 4: Solicitar FAQs

```
8️⃣ ¿Cuántas FAQs quieres incluir? (recomendado: 8-10)
```

Para cada FAQ:
```
FAQ #1:
  • Pregunta: [esperar]
  • Respuesta: [esperar]
```

### Paso 5: Generar la página

Después de recopilar toda la información:

```
✅ Información completa recibida

📋 Resumen:
  • Slug: <slug>
  • Keyword: <keyword>
  • H1: <h1>
  • Hero image: <imagen>
  • Beneficios: <cantidad>
  • FAQs: <cantidad>

Generando landing page con estilo idéntico a la homepage...
```

### Paso 6: Leer estilos de index.html

Leer el archivo `index.html` y extraer:

1. **Todo el <style> del <head>** - Critical CSS inline
2. **Estructura del <header>** con nav y logo
3. **Estructura del hero** con background image
4. **Estructura de secciones** (.section, .section-alt)
5. **Estructura de benefits/features**
6. **Estructura del footer**
7. **CTA fijo** (WhatsApp + Llamar)
8. **Scripts de tracking**

### Paso 7: Crear el HTML completo

Generar archivo `<slug>/index.html` con:

#### 1. Head completo

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><keyword> | Plomero Culiacán Pro</title>
<meta name="description" content="<meta description>">
<meta name="keywords" content="<keyword>, plomero culiacan, <variaciones>">
<meta name="robots" content="index, follow, max-image-preview:large">

<!-- Favicons (copiar exactos de index.html) -->
<link rel="icon" href="/assets/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">
<!-- ... todos los favicons ... -->

<link rel="canonical" href="https://plomeroculiacanpro.mx/<slug>/">

<!-- Open Graph -->
<meta property="og:title" content="<h1>">
<meta property="og:description" content="<meta description>">
<meta property="og:image" content="https://plomeroculiacanpro.mx/assets/images/<hero-image>">
<meta property="og:url" content="https://plomeroculiacanpro.mx/<slug>/">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<h1>">
<meta name="twitter:description" content="<meta description>">
<meta name="twitter:image" content="https://plomeroculiacanpro.mx/assets/images/<hero-image>">

<!-- Preloads -->
<link rel="preload" as="image" href="/assets/images/<hero-image>" fetchpriority="high">
<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
<link rel="preload" href="/assets/fonts/inter-500.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
<link rel="preload" href="/assets/fonts/montserrat-800.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">

<!-- COPIAR TODO EL <style> DE index.html EXACTO -->
<style>
  /* Copiar los estilos completos de index.html */
</style>

<!-- JSON-LD Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "name": "Plomero Culiacán Pro",
      "url": "https://plomeroculiacanpro.mx/",
      "logo": "https://plomeroculiacanpro.mx/assets/images/logo-512.png"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Inicio",
          "item": "https://plomeroculiacanpro.mx/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "<h1>",
          "item": "https://plomeroculiacanpro.mx/<slug>/"
        }
      ]
    },
    {
      "@type": "Service",
      "serviceType": "<keyword>",
      "name": "<h1>",
      "description": "<meta description>",
      "provider": {
        "@type": "HomeAndConstructionBusiness",
        "name": "Plomero Culiacán Pro",
        "telephone": "+52 667 392 2273",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Culiacán",
          "addressRegion": "Sinaloa",
          "addressCountry": "MX"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": "24.7903",
          "longitude": "-107.3878"
        },
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.8",
          "reviewCount": "150",
          "bestRating": "5"
        }
      },
      "areaServed": {
        "@type": "City",
        "name": "Culiacán"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        <!-- Generar cada FAQ proporcionada -->
        {
          "@type": "Question",
          "name": "<pregunta>",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "<respuesta>"
          }
        }
      ]
    }
  ]
}
</script>
</head>
```

#### 2. Body con estructura idéntica

```html
<body>
<!-- COPIAR <nav> EXACTO de index.html -->
<nav class="nav">
  <div class="container">
    <div class="nav-wrapper">
      <a href="/" class="logo">
        <img src="/assets/images/logo-512.webp" alt="Plomero Culiacán Pro" width="512" height="195">
      </a>
      <!-- Menu items -->
    </div>
  </div>
</nav>

<!-- Hero -->
<header id="inicio" class="hero">
  <div class="hero-background">
    <picture>
      <source srcset="/assets/images/<hero-800w>.webp 800w,
                      /assets/images/<hero-1200w>.webp 1200w"
              sizes="100vw">
      <img src="/assets/images/<hero-1200w>.webp" alt="<alt-text>" loading="eager">
    </picture>
  </div>
  <div class="container">
    <div class="hero-content">
      <h1><h1-text></h1>
      <p class="hero-subtitle"><subtitulo></p>

      <!-- Rating badge (copiar de index.html) -->
      <div class="hero-rating">
        <img src="/assets/icons/google-logo.svg" alt="Google" class="google-logo">
        <span class="rating-stars">★★★★★</span>
        <span class="rating-score">4.8</span>
        <span class="rating-divider">|</span>
        <span class="rating-count">150 reseñas</span>
      </div>

      <!-- Features (copiar estructura de index.html) -->
      <div class="hero-features">
        <div class="feature-item">
          <svg class="feature-icon"><!-- clock icon --></svg>
          <span>Llegada 30-60 min</span>
        </div>
        <div class="feature-item">
          <svg class="feature-icon"><!-- check icon --></svg>
          <span>Garantía 6 meses</span>
        </div>
        <div class="feature-item">
          <svg class="feature-icon"><!-- 24/7 icon --></svg>
          <span>Servicio 24/7</span>
        </div>
      </div>

      <a href="#contacto" class="btn-primary">Solicitar Servicio Ahora</a>
    </div>
  </div>
</header>

<!-- Sección Beneficios -->
<section class="section">
  <div class="container">
    <h2>¿Por qué elegirnos?</h2>
    <div class="benefits-grid">
      <!-- Para cada beneficio proporcionado -->
      <div class="benefit-card">
        <svg class="benefit-icon"><!-- SVG proporcionado o por defecto --></svg>
        <h3><titulo-beneficio></h3>
        <p><descripcion-beneficio></p>
      </div>
    </div>
  </div>
</section>

<!-- Sección Servicios (copiar estructura de index.html) -->
<section class="section section-alt">
  <div class="container">
    <h2>Servicios de <keyword></h2>
    <!-- Grid de servicios -->
  </div>
</section>

<!-- Sección FAQs -->
<section class="section">
  <div class="container">
    <h2>Preguntas Frecuentes</h2>
    <div class="faq-list">
      <!-- Para cada FAQ proporcionada -->
      <details class="faq-item">
        <summary><pregunta></summary>
        <p><respuesta></p>
      </details>
    </div>
  </div>
</section>

<!-- Sección Contacto (copiar de index.html) -->
<section id="contacto" class="section">
  <div class="container">
    <h2>Contacta con Nosotros</h2>
    <div class="final-cta">
      <p class="cta-text">WhatsApp: 52 667 392 2273 · Llamadas: 667 392 2273</p>
      <div class="cta-buttons">
        <a href="https://wa.me/526673922273" target="_blank" class="btn-primary btn-whatsapp">WhatsApp</a>
        <a href="tel:6673922273" class="btn-secondary">Llamar</a>
      </div>
    </div>
  </div>
</section>

<!-- COPIAR Footer EXACTO de index.html -->
<footer class="footer">
  <!-- ... -->
</footer>

<!-- COPIAR CTA fijo (WhatsApp + Llamar) EXACTO de index.html -->
<!-- CTA fijo con tracking -->
<style>
  .cta-bar{position:fixed;right:16px;bottom:16px;display:flex;gap:10px;z-index:9999}
  <!-- ... copiar todo el estilo ... -->
</style>
<div class="cta-bar">
  <a id="cta-whatsapp" class="cta-btn cta-wa" href="#">💬 WhatsApp</a>
  <a id="cta-llamar" class="cta-btn cta-tel" href="#">📞 Llamar</a>
</div>
<script>
  <!-- Copiar script de tracking exacto -->
</script>

</body>
</html>
```

### Paso 8: Crear directorio y archivo

1. Crear directorio: `<slug>/`
2. Crear archivo: `<slug>/index.html`
3. Escribir el HTML completo generado

### Paso 9: Confirmar y next steps

```
✅ Landing page creada exitosamente

📁 Ubicación: /<slug>/index.html
🌐 URL cuando publiques: https://plomeroculiacanpro.mx/<slug>/

📋 Archivos que necesitas agregar:
  ❌ /assets/images/<hero-800w>.webp  (NO EXISTE)
  ❌ /assets/images/<hero-1200w>.webp (NO EXISTE)

⚠️ IMPORTANTE: Antes de publicar
1. Agrega las imágenes hero en assets/images/
2. Verifica que las imágenes estén en formato WebP
3. Actualiza sitemap.xml (puedo hacerlo por ti)
4. Prueba la página localmente

¿Quieres que:
  a) Actualice sitemap.xml con esta nueva página
  b) Te ayude a optimizar las imágenes a WebP
  c) Publique directamente con /deploy-quick
```

## Reglas importantes

1. **NUNCA modificar estilos** - Copiar exactamente de index.html
2. **NUNCA inventar contenido** - Usar solo lo que el usuario proporciona
3. **SIEMPRE crear backup** - Antes de sobrescribir archivos
4. **SIEMPRE validar imágenes** - Verificar que existan las rutas proporcionadas
5. **SIEMPRE generar schemas completos** - WebSite, Service, FAQPage, BreadcrumbList

## Validaciones

Antes de generar:
- ✅ Slug no contiene espacios ni caracteres especiales
- ✅ Keyword tiene entre 2-5 palabras
- ✅ H1 tiene menos de 70 caracteres
- ✅ Meta description tiene 120-155 caracteres
- ✅ Al menos 3 beneficios proporcionados
- ✅ Al menos 5 FAQs proporcionadas

Si algo falta o es inválido, preguntar de nuevo.

## Ejemplo de flujo completo

```
Usuario: /landing-creator

Claude:
🎨 Vamos a crear tu landing page con el estilo de plomeroculiacanpro.mx

1️⃣ ¿Cuál es el slug de la página?

Usuario: plomero-urgente

Claude:
✅ Slug: plomero-urgente
   Se creará en: /plomero-urgente/index.html

2️⃣ ¿Cuál es la keyword principal?

Usuario: plomero urgente

Claude:
✅ Keyword: plomero urgente

3️⃣ ¿Cuál es el título H1?

Usuario: Plomero Urgente en Culiacán - Atención Inmediata 24/7

Claude:
✅ H1: Plomero Urgente en Culiacán - Atención Inmediata 24/7
   (65 caracteres - perfecto)

4️⃣ ¿Meta description?

Usuario: Plomero urgente en Culiacán con llegada en 15-30 minutos. Atención 24/7 para emergencias. Técnicos certificados. WhatsApp 667-392-2273

Claude:
✅ Meta description (142 caracteres - perfecto)

5️⃣ ¿Subtítulo del hero?

Usuario: Emergencias de plomería atendidas inmediatamente. Llegada rápida en toda la ciudad. Sin sobrecargos nocturnos.

Claude:
✅ Subtítulo guardado

6️⃣ ¿Ruta de la imagen hero?

Usuario: emergencia-nocturna-1200w.webp

Claude:
✅ Imagen hero: emergencia-nocturna-1200w.webp
   Nota: Deberás tener también emergencia-nocturna-800w.webp

7️⃣ ¿Cuántas secciones de beneficios quieres?

Usuario: 4

Claude:
Beneficio #1:
  • Título:

Usuario: Llegada Inmediata

Claude:
  • Descripción corta:

Usuario: Llegamos en 15-30 minutos a cualquier zona de Culiacán

Claude:
  • Ícono SVG (enter para usar por defecto):

[Usuario presiona enter]

Claude:
✅ Beneficio #1 guardado (ícono por defecto: reloj)

Beneficio #2:
  • Título:

[... continúa para los 4 beneficios ...]

Claude:
✅ 4 Beneficios guardados

8️⃣ ¿Cuántas FAQs quieres incluir?

Usuario: 6

Claude:
FAQ #1:
  • Pregunta:

Usuario: ¿Cuánto tardan en llegar en una emergencia urgente?

Claude:
  • Respuesta:

Usuario: Llegamos en 15-30 minutos a cualquier zona de Culiacán. Confirmamos tiempo exacto por WhatsApp antes de salir.

[... continúa para las 6 FAQs ...]

Claude:
✅ Información completa recibida

📋 Resumen:
  • Slug: plomero-urgente
  • Keyword: plomero urgente
  • H1: Plomero Urgente en Culiacán - Atención Inmediata 24/7
  • Hero image: emergencia-nocturna-1200w.webp
  • Beneficios: 4
  • FAQs: 6

Generando landing page con estilo idéntico a la homepage...

[Leer index.html...]
[Generar HTML completo...]
[Crear directorio plomero-urgente/...]
[Escribir index.html...]

✅ Landing page creada exitosamente

📁 Ubicación: /plomero-urgente/index.html
🌐 URL cuando publiques: https://plomeroculiacanpro.mx/plomero-urgente/

📋 Archivos que necesitas agregar:
  ❌ /assets/images/emergencia-nocturna-800w.webp  (NO EXISTE)
  ❌ /assets/images/emergencia-nocturna-1200w.webp (NO EXISTE)

⚠️ IMPORTANTE: Antes de publicar
1. Agrega las imágenes hero en assets/images/
2. Verifica que las imágenes estén en formato WebP
3. Actualiza sitemap.xml

¿Quieres que actualice sitemap.xml? (s/n)
```

## Estructura de directorios esperada

```
plomero-culiacan-pro/
├── assets/
│   ├── images/
│   │   ├── <hero-800w>.webp     ← Usuario debe agregar
│   │   ├── <hero-1200w>.webp    ← Usuario debe agregar
│   │   └── logo-512.webp
│   └── fonts/
│       ├── inter-400.woff2
│       └── ...
├── index.html
├── sitemap.xml
└── <slug>/                        ← Se crea automáticamente
    └── index.html                 ← Se genera con este comando
```

## Notas finales

- El estilo es 100% idéntico a index.html (copiar, no modificar)
- Solo el contenido cambia (textos, imágenes del usuario)
- Responsive automático (mismo CSS que homepage)
- SEO completo automático (schemas, meta tags, OG, canonical)
- El usuario solo necesita: textos + fotos
