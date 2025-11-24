# Guía Completa para Crear una Página Web de Plomería de Alto Rendimiento

**Basado en el análisis de Plomero Culiacán Pro**
**Versión 2.0 - Noviembre 2025**
**Actualización:** Estructura vigente del sitio real

---

## Tabla de Contenido

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura Técnica](#arquitectura-técnica)
3. [Estructura Real de la Página Principal](#estructura-real-de-la-página-principal)
4. [Sección Hero](#sección-hero)
5. [Navegación Fixed](#navegación-fixed)
6. [Beneficios y Propuesta de Valor](#beneficios-y-propuesta-de-valor)
7. [Servicios](#servicios)
8. [Colonias y Servicio Local](#colonias-y-servicio-local)
9. [FAQs y Schema Markup](#faqs-y-schema-markup)
10. [Social Proof y Reseñas](#social-proof-y-reseñas)
11. [Sobre Nosotros](#sobre-nosotros)
12. [Blog/Noticias](#blognoticias)
13. [Formulario de Contacto](#formulario-de-contacto)
14. [Calls-to-Action (CTAs)](#calls-to-action-ctas)
15. [SEO On-Page](#seo-on-page)
16. [Performance y Core Web Vitals](#performance-y-core-web-vitals)
17. [Diseño Responsive](#diseño-responsive)
18. [Branding y Diseño Visual](#branding-y-diseño-visual)
19. [Tracking y Analytics](#tracking-y-analytics)
20. [Checklist de Implementación](#checklist-de-implementación)

---

## Resumen Ejecutivo

Una página web de plomería exitosa debe balancear:

- ✅ **Conversión inmediata**: CTAs omnipresentes, urgencia 24/7
- ✅ **Confianza**: 150+ reseñas, garantías, certificaciones
- ✅ **SEO local**: Schema.org, geo-tags, contenido hiperlocal (120 páginas de colonias)
- ✅ **Performance**: LCP <2.5s, FID <100ms, CLS <0.1
- ✅ **Mobile-first**: 70%+ del tráfico viene de móvil

**Métricas objetivo:**
- Tasa de conversión: 8-15%
- Tiempo en página: 3+ minutos
- Bounce rate: <40%
- Page speed: 90+ (mobile), 95+ (desktop)

---

## Arquitectura Técnica

### 1. Stack Tecnológico Real

**Tecnologías utilizadas:**
- **HTML5 semántico**: `<main>`, `<section>`, `<header>`, `<nav>`, `<footer>`
- **CSS moderno**: Custom properties (variables CSS), Grid, Flexbox
- **JavaScript vanilla**: Sin frameworks, defer scripts
- **Imágenes**: WebP con responsive srcset
- **Fonts**: WOFF2 self-hosted (Inter 400/500/600, Montserrat 700/800)
- **PWA**: manifest.json configurado

### 2. Estructura de Archivos Actual

```
/
├── index.html                  # Homepage
├── styles.css                  # CSS sin minificar
├── styles.min.css              # CSS minificado (producción)
├── main.js                     # JavaScript principal (defer)
├── manifest.json               # PWA manifest
├── robots.txt                  # SEO crawling
├── sitemap.xml                 # Sitemap XML
├── logo-plomero-culiacan-pro.webp  # Logo principal
├── assets/
│   ├── fonts/
│   │   ├── inter-400.woff2
│   │   ├── inter-500.woff2
│   │   ├── inter-600.woff2
│   │   ├── montserrat-700.woff2
│   │   └── montserrat-800.woff2
│   ├── images/
│   │   ├── hero-plomero-visita-800w.webp
│   │   ├── hero-plomero-visita-1200w.webp
│   │   ├── reparacion-fugas-800w.webp
│   │   ├── destapandodrenaje-800w.webp
│   │   ├── taza-de-baño-800w.webp
│   │   ├── emergencia-24-7-nocturna-1200w.webp
│   │   └── social-proof/
│   │       ├── before-after/
│   │       └── google-reviews/
│   └── icons/
│       ├── favicon.ico
│       ├── favicon.png
│       ├── icon-192.png
│       └── icon-512.png
├── servicios/
│   ├── plomero-colonias-culiacan/ (120 páginas de colonias)
│   │   ├── campestre/index.html
│   │   ├── las-quintas/index.html
│   │   └── [colonia]/index.html
│   ├── reparacion-de-fugas/index.html
│   ├── destape-de-drenajes/index.html
│   └── instalacion-de-sanitarios/index.html
├── blog/
│   └── index.html
└── plomero-cerca-de-mi/
    └── index.html
```

### 3. Meta Tags Esenciales (Implementados)

```html
<!-- SEO Básico -->
<title>Plomero en Culiacán 24/7 | Llegada en 30-60 min + Garantía</title>
<meta name="description" content="Plomero certificado en Culiacán · Emergencia 24/7 con llegada en 30-60 min · Cobertura Las Quintas, Tres Ríos, Centro · WhatsApp inmediato · Factura disponible · Garantía escrita">

<!-- Geolocalización -->
<meta http-equiv="content-language" content="es-MX">
<meta name="geo.region" content="MX-SIN">
<meta name="geo.placename" content="Culiacán">
<meta name="geo.position" content="24.7903;-107.3878">
<meta name="ICBM" content="24.7903, -107.3878">

<!-- PWA -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0066cc">

<!-- Favicons -->
<link rel="icon" href="/assets/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/icons/favicon.png">
<link rel="apple-touch-icon" href="/assets/icons/favicon.png">
```

---

## Estructura Real de la Página Principal

### Orden de Secciones Actual (index.html)

```
1. <nav class="nav"> - Navegación fija (z-index: 50)
2. <header id="inicio" class="hero"> - Hero con glassmorphism
3. <main>
   ├── 4. Sección Beneficios (¿Por qué elegirnos?)
   ├── 5. <section id="servicios"> - Servicios principales (6 cards)
   ├── 6. <section id="colonias-destacadas"> - Colonias con enlaces
   ├── 7. Urgencias 24/7 - CTA destacado
   ├── 8. Zonas de servicio - Mapa visual
   ├── 9. Proceso en 4 pasos
   ├── 10. <div class="faq"> - Preguntas frecuentes (10+ FAQs)
   ├── 11. Pricing/Precios transparentes
   ├── 12. <section id="sobre-nosotros"> - Historia y equipo
   ├── 13. <section id="noticias"> - Blog/Artículos recientes
   ├── 14. <section class="social-proof"> - Reseñas Google (fotos)
   ├── 15. Testimonios - Reviews con rating
   ├── 16. Before/After Gallery - Social proof visual
   ├── 17. <section id="contacto"> - Formulario + NAP
   └── 18. Mapa de cobertura - Colonias atendidas
19. </main>
20. <footer class="footer"> - Footer simple (sin logo gigante)
21. CTAs flotantes - WhatsApp + Teléfono (fixed, z-index: 60)
22. Exit-intent popup (modal)
23. <script src="/main.js" defer> - JavaScript diferido
```

### Diferencias Clave vs Guía Original

**REMOVIDO:**
- ❌ Logo gigante en footer (eliminado)
- ❌ Precios por colonia (simplificado)

**ACTUALIZADO:**
- ✅ 120 páginas de colonias (no 6-8)
- ✅ 10+ FAQs con Schema.org FAQPage
- ✅ Social proof con imágenes reales de Google Reviews
- ✅ Before/After gallery destacada
- ✅ Blog integrado en homepage
- ✅ Glassmorphism en hero (backdrop-filter: blur)
- ✅ Rating de Google visible en hero
- ✅ Navegación con logo grande (86px desktop, 62px mobile)

---

## Sección Hero

### 1. Anatomía del Hero (Implementada)

**Componentes actuales:**
- ✅ Imagen de fondo full-width (`hero-plomero-visita-1200w.webp`)
- ✅ Overlay con degradado sutil (::after pseudo-elemento)
- ✅ H1: "Plomero en Culiacán – Emergencias 24/7"
- ✅ Rating de Google visible (4.8/5, 150+ clientes)
- ✅ Subtítulo con USPs
- ✅ 3 features con iconos (Llegada 30-60min, Garantía 6 meses, Factura SAT)
- ✅ CTA primario (Solicitar Atención Inmediata)
- ✅ Glassmorphism content box con backdrop-filter

### 2. CSS Hero Real

```css
.hero {
    min-height: 85vh;
    display: grid;
    place-items: center;
    text-align: center;
    padding: 140px 16px;
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "";
    position: absolute;
    top: -80px;
    left: 0;
    right: 0;
    height: 100px;
    z-index: 1;
    background: linear-gradient(180deg, rgba(10,18,36,0.75) 0%, rgba(10,18,36,0.5) 60%, transparent 100%);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 900px;
    width: min(90vw, 840px);
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Mobile adaptations */
@media (max-width: 768px) {
    .hero {
        min-height: 75vh;
        padding-top: 85px;
        align-items: flex-start;
    }

    .hero-content {
        margin-top: 0;
        padding: 1.5rem 1.25rem;
        background: rgba(255, 255, 255, 0.12);
    }

    .hero h1 {
        font-size: clamp(1.5rem, 5vw, 2rem);
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        display: none; /* Simplificado en mobile */
    }

    .hero-rating {
        margin-top: 20rem;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.9);
    }

    .hero-cta, .hero-contact, .hero-guarantee, .hero .btn-primary {
        display: none; /* Simplificado en mobile */
    }
}
```

---

## Navegación Fixed

### 1. Estructura Real

```html
<nav class="nav">
    <div class="container">
        <div class="nav-wrapper">
            <a href="#inicio" class="logo">
                <img src="logo-plomero-culiacan-pro.webp"
                     alt="Plomero Culiacán Pro - Logo">
            </a>
            <button class="mobile-menu-btn" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="#inicio" class="nav-link">Inicio</a></li>
                <li><a href="#servicios" class="nav-link">Servicios</a></li>
                <li><a href="#sobre-nosotros" class="nav-link">Sobre Nosotros</a></li>
                <li><a href="/blog/" class="nav-link">Blog</a></li>
                <li><a href="#contacto" class="nav-link">Contacto</a></li>
            </ul>
        </div>
    </div>
</nav>
```

### 2. CSS Navegación

```css
.nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 50;
    background: transparent; /* Transparente sobre hero */
    border-bottom: none;
    padding: 22px 0;
}

.logo img {
    height: 86px; /* Desktop */
    width: auto;
    mix-blend-mode: multiply;
}

.nav-link {
    color: #fff;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease;
}

.nav-link:hover {
    color: var(--brand-light);
}

/* Mobile */
@media (max-width: 768px) {
    .logo img {
        height: 62px; /* Mobile más pequeño */
    }

    .mobile-menu-btn {
        display: flex;
    }

    .nav-menu {
        position: fixed;
        top: 65px;
        left: -100%;
        width: 100%;
        height: calc(100vh - 65px);
        background: rgba(255, 255, 255, 0.98);
        flex-direction: column;
        padding: 3rem 2rem;
        gap: 2rem;
        transition: left 0.3s ease;
    }

    .nav-menu.active {
        left: 0;
    }

    .nav-link {
        color: var(--text); /* Texto oscuro en mobile */
    }
}
```

---

## Beneficios y Propuesta de Valor

### Sección Actual

Ubicada después del hero, esta sección destaca 4-5 beneficios principales con iconos.

**Beneficios implementados:**
1. **Rapidez**: Llegamos hoy mismo en 30-60 min
2. **Precios claros**: Sin cargos ocultos
3. **Garantía**: 6 meses en mano de obra
4. **Facturación SAT**: Válida para deducción
5. **WhatsApp CTA**: Respondemos en 10 minutos

---

## Servicios

### 1. Servicios Principales Implementados (6 cards)

```html
<section id="servicios" class="section">
    <div class="container">
        <h2>Nuestros Servicios</h2>
        <div class="grid">
            <!-- 6 servicios principales -->
            1. Reparación de fugas
            2. Destape de drenajes
            3. Instalación de sanitarios
            4. Reparación de boiler/calentadores
            5. Instalación de tinaco/hidroneumático
            6. Emergencias 24/7
        </div>
    </div>
</section>
```

### 2. Características de Cards

- Imagen WebP 800w (loading="lazy")
- Alt text descriptivo con ciudad
- Título H3 con keyword
- Descripción breve (2-3 líneas)
- Lista de características (2-3 bullets)
- Link "Más Información →"
- Hover effect (translateY + shadow)

---

## Colonias y Servicio Local

### 1. Sección "Colonias Destacadas" (Implementada)

```html
<section class="section section-alt" id="colonias-destacadas">
    <div class="container">
        <h2>Atendemos todas las colonias de Culiacán</h2>
        <p>Cobertura completa con llegada en 30-60 minutos</p>

        <!-- 120 páginas de colonias linkadas -->
        <div class="colonias-grid">
            <!-- Por zona -->
            <div class="zona-norte">
                <h3>Zona Norte</h3>
                <a href="/servicios/plomero-colonias-culiacan/las-quintas/">Las Quintas</a>
                <a href="/servicios/plomero-colonias-culiacan/tres-rios/">Tres Ríos</a>
                <!-- ... más colonias -->
            </div>

            <div class="zona-centro">
                <h3>Centro</h3>
                <!-- ... colonias -->
            </div>

            <div class="zona-sur">
                <h3>Zona Sur</h3>
                <!-- ... colonias -->
            </div>
        </div>
    </div>
</section>
```

### 2. Estrategia de 120 Páginas de Colonias

**Estructura:**
- `/servicios/plomero-colonias-culiacan/[colonia]/index.html`
- Contenido único por colonia
- Schema LocalBusiness específico
- Breadcrumbs schema
- FAQs específicas de zona
- Fotos relevantes compartidas

**SEO Local Benefit:**
- Long-tail keywords: "plomero [colonia]"
- Featured snippets potenciales
- Internal linking masivo (120 páginas)
- Autoridad topical local

---

## FAQs y Schema Markup

### 1. Implementación Actual

```html
<section class="section">
    <div class="container">
        <h2>Preguntas Frecuentes</h2>
        <div class="faq">
            <!-- 10+ preguntas con Schema.org -->
            <details class="faq-item">
                <summary>¿Cuánto cuesta la visita del plomero?</summary>
                <p>La visita tiene un costo de $300-500 pesos...</p>
            </details>

            <!-- Más FAQs -->
        </div>
    </div>
</section>

<!-- Schema.org FAQPage -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta la visita del plomero?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "La visita tiene un costo de $300-500 pesos..."
      }
    }
    // ... más preguntas
  ]
}
</script>
```

### 2. Beneficios SEO

- ✅ Featured snippets en SERP
- ✅ Rich results en búsqueda
- ✅ FAQ accordion en mobile
- ✅ Reduce bounce rate (responde dudas)

---

## Social Proof y Reseñas

### 1. Sección Social Proof (Implementada)

```html
<section class="social-proof">
    <div class="container">
        <h2>Reseñas Verificadas de Google</h2>
        <p class="social-proof-subtitle">
            Más de 150 clientes satisfechos en Culiacán
        </p>

        <!-- Grid de reseñas con FOTOS de Google -->
        <div class="google-reviews-grid">
            <div class="google-review-card">
                <img src="/assets/images/social-proof/google-reviews/review-1.webp"
                     alt="Reseña 5 estrellas de cliente satisfecho"
                     class="google-review-image">
                <div class="google-review-badge">
                    <p>★★★★★ 5.0</p>
                    <p>Roberto M. - Las Quintas</p>
                </div>
            </div>

            <!-- 3-6 reviews con fotos -->
        </div>

        <!-- Before/After Gallery -->
        <div class="before-after-gallery">
            <h3>Trabajos Recientes</h3>
            <div class="before-after-grid">
                <img src="/assets/images/social-proof/before-after/before-after-drain-cleaning-1200w.webp"
                     alt="Antes y después de destape de drenaje">
                <img src="/assets/images/social-proof/before-after/before-after-water-heater-boiler-1200w.webp"
                     alt="Instalación de calentador Noritz">
            </div>
        </div>
    </div>
</section>
```

### 2. Elementos de Confianza

- ✅ Rating de Google en hero (4.8/5)
- ✅ Fotos reales de reseñas
- ✅ Before/After con imágenes profesionales
- ✅ Testimonios con nombre + colonia + fecha
- ✅ Badges de garantía y facturación
- ✅ Certificaciones (si aplica)

---

## Sobre Nosotros

### Implementación Actual

```html
<section id="sobre-nosotros" class="section section-alt">
    <div class="container">
        <h2>Sobre Nosotros</h2>
        <p>15+ años de experiencia en plomería residencial y comercial en Culiacán</p>

        <!-- Team showcase -->
        <div class="team-showcase">
            <h3>Nuestro Equipo</h3>
            <div class="team-grid">
                <!-- Fotos y nombres del equipo -->
                <div class="team-member">
                    <img src="/assets/images/team/plomero-1.webp"
                         alt="Técnico certificado"
                         class="team-photo">
                    <h4>Nombre del Técnico</h4>
                    <p>15 años de experiencia</p>
                </div>
            </div>
        </div>

        <!-- Certificaciones, garantías -->
    </div>
</section>
```

---

## Blog/Noticias

### Implementación

```html
<section id="noticias" class="section">
    <div class="container">
        <h2>Últimos Artículos del Blog</h2>
        <div class="blog-grid">
            <!-- 3-6 artículos recientes -->
            <article class="blog-card">
                <img src="/blog/thumbnail.webp" alt="Artículo">
                <h3>Título del Artículo</h3>
                <p>Resumen breve...</p>
                <a href="/blog/articulo/">Leer más →</a>
            </article>
        </div>
    </div>
</section>
```

---

## Formulario de Contacto

### Implementación Real (con validación en tiempo real)

```html
<section id="contacto" class="section">
    <div class="container">
        <h2>Solicita tu Cotización</h2>
        <form id="contact-form" method="POST" netlify>
            <!-- Honeypot anti-spam -->
            <input type="hidden" name="form-name" value="contacto-plomeria">

            <!-- Campos con validación real-time -->
            <div class="form-field">
                <label for="nombre">Nombre completo *</label>
                <input type="text" id="nombre" name="nombre" required>
                <span class="error-message">Por favor ingresa tu nombre</span>
            </div>

            <div class="form-field">
                <label for="telefono">Teléfono (10 dígitos) *</label>
                <input type="tel" id="telefono" pattern="[0-9]{10}" required>
                <span class="error-message">Ingresa 10 dígitos</span>
            </div>

            <div class="form-field">
                <label for="email">Email *</label>
                <input type="email" id="email" required>
                <span class="error-message">Email inválido</span>
            </div>

            <div class="form-field">
                <label for="mensaje">Describe tu problema *</label>
                <textarea id="mensaje" rows="4" minlength="10" required></textarea>
                <span class="error-message">Mínimo 10 caracteres</span>
            </div>

            <button type="submit" class="btn-primary">Enviar Solicitud</button>
        </form>

        <!-- NAP (Name, Address, Phone) -->
        <div class="contact-info">
            <h3>Información de Contacto</h3>
            <p><strong>Teléfono:</strong> 667 163 1231</p>
            <p><strong>WhatsApp:</strong> 667 163 1231</p>
            <p><strong>Horario:</strong> 24/7 Emergencias</p>
            <p><strong>Cobertura:</strong> Todas las colonias de Culiacán</p>
        </div>
    </div>
</section>
```

---

## Calls-to-Action (CTAs)

### 1. CTAs Flotantes (Implementados)

```html
<!-- WhatsApp Flotante -->
<a href="https://wa.me/526671631231?text=Hola%2C%20necesito%20un%20plomero%20urgente"
   id="cta-whatsapp"
   class="floating-btn floating-whatsapp"
   target="_blank"
   aria-label="Contactar por WhatsApp">
    <svg width="24" height="24" fill="currentColor">
        <!-- WhatsApp icon SVG -->
    </svg>
</a>

<!-- Teléfono Flotante -->
<a href="tel:+526671631231"
   id="cta-llamar"
   class="floating-btn floating-call"
   aria-label="Llamar ahora">
    <svg width="24" height="24" fill="currentColor">
        <!-- Phone icon SVG -->
    </svg>
</a>
```

### 2. CSS CTAs Flotantes

```css
.floating-btn {
    position: fixed;
    right: 18px;
    width: 54px;
    height: 54px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #fff;
    font-size: 1.1rem;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16);
    transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
    z-index: 60;
    text-decoration: none;
}

.floating-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.2);
    filter: brightness(1.05);
}

.floating-call {
    background: #0f4fa8; /* Azul */
    bottom: 18px;
}

.floating-whatsapp {
    background: #22c55e; /* Verde WhatsApp */
    bottom: 78px;
}
```

### 3. Exit-Intent Popup

```html
<div id="exit-intent-popup" style="display:none;">
    <div class="exit-popup-content">
        <button class="exit-popup-close">×</button>
        <h3>¡Espera!</h3>
        <p>¿Emergencia de plomería? Llegamos en 30-60 minutos</p>
        <a href="https://wa.me/526671631231" class="btn-primary">WhatsApp</a>
        <a href="tel:+526671631231" class="btn-secondary">Llamar</a>
    </div>
</div>
```

---

## SEO On-Page

### 1. Schema.org Implementado

**Schemas actuales:**
- ✅ `HomeAndConstructionBusiness` (LocalBusiness)
- ✅ `Service` (múltiples servicios)
- ✅ `FAQPage` (10+ preguntas)
- ✅ `BreadcrumbList`
- ✅ `AggregateRating` (4.8/5, 150 reviews)
- ✅ `Review` (testimonios individuales)

### 2. Internal Linking

**Estrategia implementada:**
- 120 páginas de colonias linkeadas desde homepage
- Links bidireccionales (colonia ↔ homepage)
- Servicios principales linkeados desde cards
- Blog linkeado desde sección noticias
- Footer con enlaces principales

---

## Performance y Core Web Vitals

### 1. Optimizaciones Implementadas

**Critical CSS:**
- Inline en `<head>` para above-the-fold
- Fonts, variables, hero styles inlined
- Non-critical CSS defer load

**Fonts:**
- Self-hosted WOFF2
- `font-display: swap`
- Preload critical fonts (Inter 400, Montserrat 800)

**Images:**
- WebP format (95 KB @ 1200w)
- Responsive srcset (800w, 1200w)
- `loading="lazy"` en below-the-fold
- `fetchpriority="high"` en hero
- Hero preload en `<head>`

**JavaScript:**
- Defer main.js
- No frameworks pesados
- Vanilla JS para validación

---

## Diseño Responsive

### Breakpoints Implementados

```css
/* Mobile-first */
body {
    padding-top: 80px; /* Fixed nav height */
}

/* Tablet (768px+) */
@media (min-width: 768px) {
    .grid {
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
    }
}
```

---

## Branding y Diseño Visual

### Paleta de Colores Implementada

```css
:root {
    /* Brand */
    --brand: #E36414;
    --brand-light: #F97316;

    /* Text */
    --text: #0F172A;
    --text-light: #475569;

    /* Background */
    --bg: #FFFFFF;
    --bg-soft: #F8FAFC;

    /* Borders */
    --border: #E2E8F0;
    --shadow: rgba(15, 23, 42, 0.1);

    /* Gradients */
    --gradient-brand: linear-gradient(135deg, #F97316 0%, #E36414 100%);
}
```

---

## Tracking y Analytics

### Google Tag Manager Implementado

```html
<!-- GTM en <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## Checklist de Implementación

### ✅ Completado (Estado Actual)

#### SEO On-Page
- [x] Title tag optimizado
- [x] Meta description
- [x] H1 único con keyword
- [x] H2-H6 jerárquicos
- [x] URLs semánticas
- [x] Alt text en todas las imágenes
- [x] Schema.org (Business, Service, FAQPage, Reviews)
- [x] Open Graph tags
- [x] Canonical tags
- [x] 120 páginas de colonias con SEO local

#### Performance
- [x] LCP <2.5s
- [x] Imágenes WebP
- [x] Responsive images (srcset)
- [x] Critical CSS inline
- [x] Fonts preloaded + font-display: swap
- [x] JavaScript defer
- [x] PWA manifest
- [x] Lazy loading

#### Mobile
- [x] Diseño responsive
- [x] Touch targets ≥48x48px
- [x] Menu móvil funcional
- [x] CTAs flotantes

#### Funcionalidad
- [x] Formulario con validación real-time
- [x] WhatsApp links
- [x] Tel: links
- [x] CTAs flotantes
- [x] Exit-intent popup
- [x] Google Tag Manager

#### Contenido
- [x] 6 servicios principales
- [x] 10+ FAQs con schema
- [x] Testimonios con rating
- [x] Before/After gallery
- [x] Blog integrado
- [x] 120 colonias linkeadas
- [x] NAP completo

---

## Cambios vs Guía Original

### ❌ REMOVIDO:
1. **Logo gigante en footer** - Eliminado por UX
2. **Sección de precios detallada** - Simplificado

### ✅ ACTUALIZADO:
1. **120 páginas de colonias** (no 6-8 mencionadas originalmente)
2. **Social proof con fotos reales** de Google Reviews
3. **Before/After gallery** prominente
4. **Glassmorphism** en hero content
5. **Rating de Google** visible en hero
6. **Blog integrado** en homepage
7. **10+ FAQs** con Schema.org
8. **Footer simple** con texto (sin logo)
9. **Navegación con logo grande** (86px desktop)
10. **Exit-intent popup** implementado

---

## Conclusión

Esta guía refleja la **arquitectura real y vigente** del sitio Plomero Culiacán Pro (Noviembre 2025):

✅ **Conversión**: CTAs omnipresentes + urgencia 24/7 + exit-intent
✅ **Confianza**: 150+ reviews + before/after + garantías
✅ **SEO local**: 120 páginas de colonias + Schema.org robusto
✅ **Performance**: LCP <2.5s + WebP + critical CSS inline
✅ **Mobile-first**: Responsive design + touch-friendly

**Estructura validada y funcional**
**Versión**: 2.0 (Actualizada Noviembre 2025)
