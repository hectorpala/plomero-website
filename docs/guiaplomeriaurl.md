# Guía Completa para Crear una Página Web de Plomería de Alto Rendimiento

**Basado en el análisis de Plomero Culiacán Pro**
**Versión 1.0 - Noviembre 2024**

---

## Tabla de Contenido

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura Técnica](#arquitectura-técnica)
3. [Estructura de la Página](#estructura-de-la-página)
4. [Sección Hero](#sección-hero)
5. [Beneficios y Propuesta de Valor](#beneficios-y-propuesta-de-valor)
6. [Servicios](#servicios)
7. [Elementos de Confianza](#elementos-de-confianza)
8. [Calls-to-Action (CTAs)](#calls-to-action-ctas)
9. [Formulario de Contacto](#formulario-de-contacto)
10. [SEO On-Page](#seo-on-page)
11. [Performance y Core Web Vitals](#performance-y-core-web-vitals)
12. [Diseño Responsive](#diseño-responsive)
13. [Branding y Diseño Visual](#branding-y-diseño-visual)
14. [Elementos de Urgencia](#elementos-de-urgencia)
15. [Tracking y Analytics](#tracking-y-analytics)
16. [Checklist de Implementación](#checklist-de-implementación)

---

## Resumen Ejecutivo

Una página web de plomería exitosa debe balancear:

- ✅ **Conversión inmediata**: CTAs omnipresentes, urgencia 24/7
- ✅ **Confianza**: 150+ reseñas, garantías, certificaciones
- ✅ **SEO local**: Schema.org, geo-tags, contenido hiperlocal
- ✅ **Performance**: LCP <2.5s, FID <100ms, CLS <0.1
- ✅ **Mobile-first**: 70%+ del tráfico viene de móvil

**Métricas objetivo:**
- Tasa de conversión: 8-15%
- Tiempo en página: 3+ minutos
- Bounce rate: <40%
- Page speed: 90+ (mobile), 95+ (desktop)

---

## Arquitectura Técnica

### 1. Stack Tecnológico

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Performance: Critical CSS inline -->
    <style>
        /* Inline critical above-the-fold CSS */
    </style>

    <!-- Performance: Preload critical resources -->
    <link rel="preload" as="image" href="/hero-image.webp" fetchpriority="high">
    <link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>

    <!-- Performance: Preconnect external domains -->
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://wa.me">
</head>
```

**Tecnologías recomendadas:**
- **HTML5 semántico**: `<main>`, `<section>`, `<article>`, `<header>`, `<footer>`
- **CSS moderno**: Custom properties (variables CSS), Grid, Flexbox
- **JavaScript vanilla**: Sin frameworks pesados, defer scripts
- **Imágenes**: WebP con fallback, responsive srcset
- **Fonts**: WOFF2 local, font-display: swap
- **PWA**: manifest.json, service worker

### 2. Estructura de Archivos

```
/
├── index.html                  # Homepage
├── styles.css                  # CSS principal
├── styles.min.css              # CSS minificado para producción
├── main.js                     # JavaScript principal (defer)
├── sw.js                       # Service Worker (PWA)
├── manifest.json               # PWA manifest
├── robots.txt                  # SEO crawling
├── sitemap.xml                 # Sitemap XML
├── assets/
│   ├── fonts/
│   │   ├── inter-400.woff2
│   │   ├── inter-500.woff2
│   │   ├── montserrat-700.woff2
│   │   └── montserrat-800.woff2
│   ├── images/
│   │   ├── hero-plomero-800w.webp
│   │   ├── hero-plomero-1200w.webp
│   │   ├── reparacion-fugas-420w.webp
│   │   └── [servicio]-800w.webp
│   └── icons/
│       ├── favicon.ico
│       ├── favicon.png
│       ├── icon-192.webp
│       └── icon-512.webp
├── servicios/
│   ├── reparacion-de-fugas/index.html
│   ├── destape-de-drenajes/index.html
│   └── [servicio]/index.html
├── blog/
│   ├── index.html
│   └── [articulo]/index.html
└── logo-plomero.webp
```

### 3. Meta Tags Esenciales

```html
<!-- SEO Básico -->
<title>Plomero en [Ciudad] 24/7 | Llegada en 30-60 min + Garantía</title>
<meta name="description" content="Plomero certificado en [Ciudad] · Emergencia 24/7 con llegada en 30-60 min · Cobertura [Colonias] · WhatsApp inmediato · Factura disponible · Garantía escrita">

<!-- Geolocalización -->
<meta http-equiv="content-language" content="es-MX">
<meta name="geo.region" content="MX-SIN">
<meta name="geo.placename" content="Culiacán">
<meta name="geo.position" content="24.7903;-107.3878">
<meta name="ICBM" content="24.7903, -107.3878">

<!-- Open Graph (Facebook/WhatsApp) -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://tudominio.com/">
<meta property="og:title" content="Plomero en [Ciudad] 24/7">
<meta property="og:description" content="Emergencias de plomería en [Ciudad]. Llegada en 30-60 min.">
<meta property="og:image" content="https://tudominio.com/og-image.jpg">
<meta property="og:locale" content="es_MX">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Plomero en [Ciudad] 24/7">
<meta name="twitter:description" content="Emergencias de plomería en [Ciudad]">
<meta name="twitter:image" content="https://tudominio.com/twitter-image.jpg">

<!-- PWA -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0066cc">
<link rel="apple-touch-icon" href="/assets/icons/icon-192.png">

<!-- Favicons -->
<link rel="icon" href="/assets/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/icons/favicon.png">
```

---

## Estructura de la Página

### Orden de Secciones (Homepage)

```
1. Navegación fija (fixed, z-index: 50)
2. Hero Section (min-height: 85vh)
3. <main>
   ├── 4. Beneficios / ¿Por qué elegirnos?
   ├── 5. Servicios principales (6-8 cards)
   ├── 6. Servicios por colonia/zona
   ├── 7. Urgencias 24/7 / Horarios
   ├── 8. Zonas de servicio
   ├── 9. Precios transparentes
   ├── 10. Proceso en 4 pasos
   ├── 11. FAQs (Schema.org FAQPage)
   ├── 12. Blog (últimos 6 artículos)
   ├── 13. Testimonios / Reseñas
   ├── 14. Social Proof (antes/después)
   ├── 15. Formulario de contacto
   └── 16. Información de contacto + mapa
17. </main>
18. Footer
19. CTAs flotantes (fixed)
20. Exit-intent popup (modal)
21. JavaScript (defer)
```

### Contenedor Principal

```css
:root {
    --container-max-width: 1200px;
    --container-gutter: 24px;
}

.container {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--container-gutter);
}

/* Mobile: gutters más pequeños */
@media (max-width: 768px) {
    :root {
        --container-gutter: 16px;
    }
}
```

---

## Sección Hero

### 1. Anatomía del Hero

**Componentes obligatorios:**
- ✅ Imagen de fondo full-width (plomero en acción)
- ✅ Overlay oscuro (rgba(0,0,0,0.4-0.6))
- ✅ H1 con palabra clave principal
- ✅ Subtítulo con USPs (3-5 beneficios clave)
- ✅ Rating visual (Google, estrellas)
- ✅ 2-3 features icónicos
- ✅ CTA primario (contacto/WhatsApp)
- ✅ Información de contacto visible

### 2. HTML Estructura

```html
<header id="inicio" class="hero">
    <!-- Background Image (LCP optimizado) -->
    <picture class="hero-background">
        <source type="image/webp"
                srcset="/assets/images/hero-800w.webp 800w,
                        /assets/images/hero-1200w.webp 1200w"
                sizes="100vw">
        <img src="/assets/images/hero-1200w.webp"
             alt="Plomero profesional en [Ciudad] atendiendo emergencia 24 horas"
             width="1200" height="800"
             fetchpriority="high"
             decoding="async">
    </picture>

    <div class="container">
        <div class="hero-content">
            <!-- H1: Palabra clave principal -->
            <h1>Plomero en [Ciudad] – Emergencias 24/7</h1>

            <!-- Rating Badge (Google) -->
            <div class="hero-rating">
                <svg class="google-logo"><!-- SVG logo Google --></svg>
                <span class="rating-stars">★★★★★</span>
                <span class="rating-score">4.8/5</span>
                <span class="rating-divider">·</span>
                <span class="rating-count">Más de 150 clientes satisfechos</span>
            </div>

            <!-- Subtítulo con USPs -->
            <p class="hero-subtitle">
                Plomero certificado en [Ciudad] · Emergencia 24/7 con desplazamiento incluido
                en [Colonias]. Llegada en 30-60 minutos con garantía escrita.
            </p>

            <!-- Features con Iconografía -->
            <div class="hero-features">
                <div class="feature-item">
                    <svg class="feature-icon"><!-- Clock icon --></svg>
                    <span>Llegamos en 30-60 min</span>
                </div>
                <div class="feature-item">
                    <svg class="feature-icon"><!-- Shield icon --></svg>
                    <span>Garantía 6 meses</span>
                </div>
                <div class="feature-item">
                    <svg class="feature-icon"><!-- Document icon --></svg>
                    <span>Factura disponible</span>
                </div>
            </div>

            <!-- CTA Primario -->
            <a href="#contacto" class="btn-primary">Solicitar Atención Inmediata</a>
        </div>
    </div>
</header>
```

### 3. CSS Hero

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

/* Background image */
.hero-background {
    position: absolute;
    inset: 0;
    z-index: 0;
}

.hero-background img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
}

/* Overlay degradado sutil arriba */
.hero::after {
    content: "";
    position: absolute;
    top: -80px;
    left: 0;
    right: 0;
    height: 100px;
    z-index: 1;
    background: linear-gradient(180deg, rgba(10,18,36,0.75) 0%, transparent 100%);
    pointer-events: none;
}

/* Content box con glassmorphism */
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

/* H1 */
.hero h1 {
    color: #FFFFFF;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    letter-spacing: -0.025em;
    line-height: 1.2;
}

/* Subtítulo */
.hero-subtitle {
    font-size: 1.2rem;
    color: #F1F5F9;
    margin-bottom: 3rem;
    max-width: 640px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.55;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.4);
}

/* Rating badge */
.hero-rating {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1rem 0 1.5rem;
    padding: 0.85rem 1.5rem;
    background: rgba(255, 255, 255, 0.98);
    border-radius: 50px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
    font-size: 0.95rem;
}

.rating-stars {
    color: #FBBC04; /* Google yellow */
    font-size: 1.15rem;
    letter-spacing: 1px;
}

.rating-score {
    font-weight: 700;
    color: #1a73e8; /* Google blue */
}

/* Features */
.hero-features {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 2rem 0 2.5rem;
    flex-wrap: wrap;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #fff;
    font-size: 0.95rem;
    font-weight: 500;
}

.feature-icon {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
    color: #f97316; /* Brand orange */
}

/* Mobile adaptations */
@media (max-width: 768px) {
    .hero {
        min-height: 75vh;
        padding-top: 85px;
        align-items: flex-start;
    }

    .hero-content {
        padding: 1.5rem 1.25rem;
        background: rgba(255, 255, 255, 0.12);
    }

    .hero h1 {
        font-size: clamp(1.5rem, 5vw, 2rem);
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        display: none; /* Ocultar en mobile para simplificar */
    }

    .hero-features {
        gap: 1rem;
        margin: 1.5rem 0 2rem;
    }

    .feature-item {
        font-size: 0.85rem;
    }
}
```

### 4. Imágenes Hero

**Especificaciones:**
- **Formato**: WebP (95 KB @ 1200w), fallback PNG
- **Dimensiones**: 1200x800px (desktop), 800x600px (mobile)
- **Contenido**: Plomero profesional trabajando, herramientas visibles, uniforme limpio
- **Calidad**: 85-90 en compresión WebP
- **Alt text**: "Plomero profesional en [Ciudad] atendiendo emergencia 24 horas con herramientas especializadas"

**Optimización LCP:**
```html
<!-- Preload en <head> -->
<link rel="preload" as="image"
      href="/assets/images/hero-1200w.webp"
      imagesrcset="/assets/images/hero-800w.webp 800w,
                   /assets/images/hero-1200w.webp 1200w"
      imagesizes="100vw"
      fetchpriority="high">
```

---

## Beneficios y Propuesta de Valor

### 1. Sección "¿Por qué elegirnos?"

**5 beneficios esenciales:**

1. **Rapidez**: "Llegamos hoy mismo en 30-60 min"
2. **Precios**: "Precios claros sin cargos ocultos"
3. **Garantía**: "Garantía 6 meses en mano de obra"
4. **Facturación**: "Factura SAT válida mismo día"
5. **Disponibilidad**: "Respondemos en 10 minutos por WhatsApp"

### 2. HTML Estructura

```html
<section class="section section-alt">
    <div class="container benefits-container">
        <h2>¿Por qué elegirnos?</h2>
        <div class="benefits-grid">
            <!-- Beneficio 1: Rapidez -->
            <div class="benefit">
                <div class="benefit-icon">
                    <svg><!-- Clock icon --></svg>
                </div>
                <div class="benefit-content">
                    <h3>Llegamos hoy mismo</h3>
                    <p>Atendemos emergencias en 30-60 min en [Colonias]. Servicio 24/7 con herramientas completas.</p>
                </div>
            </div>

            <!-- Beneficio 2: Precios -->
            <div class="benefit">
                <div class="benefit-icon">
                    <svg><!-- Dollar icon --></svg>
                </div>
                <div class="benefit-content">
                    <h3>Precios claros</h3>
                    <p>Cotización por WhatsApp antes de ir. Desglose completo de mano de obra y materiales. Sin cargos ocultos.</p>
                </div>
            </div>

            <!-- Beneficio 3: Garantía -->
            <div class="benefit">
                <div class="benefit-icon">
                    <svg><!-- Shield icon --></svg>
                </div>
                <div class="benefit-content">
                    <h3>Garantía 6 meses</h3>
                    <p>Refacciones originales y técnicos certificados. Cada reparación queda documentada con garantía escrita.</p>
                </div>
            </div>

            <!-- Beneficio 4: Facturación -->
            <div class="benefit">
                <div class="benefit-icon">
                    <svg><!-- Document icon --></svg>
                </div>
                <div class="benefit-content">
                    <h3>Factura SAT</h3>
                    <p>Facturación válida el mismo día para empresas y condominios. Deducible para personas físicas y morales.</p>
                </div>
            </div>

            <!-- CTA WhatsApp adicional -->
            <div class="whatsapp-cta-box">
                <div class="whatsapp-cta-icon">
                    <svg><!-- WhatsApp icon --></svg>
                </div>
                <div class="whatsapp-cta-content">
                    <h3>¿Tienes dudas? Respondemos en 10 minutos</h3>
                    <p>Cotiza, agenda o reporta emergencias por WhatsApp</p>
                </div>
                <a href="https://wa.me/52XXXXXXXXXX?text=Hola,%20necesito%20información"
                   class="whatsapp-cta-button">
                    Abrir Chat
                </a>
            </div>
        </div>

        <p class="benefits-cta">
            <strong>Agenda tu visita hoy mismo desde WhatsApp o llamada al <a href="tel:XXXXXXXXXX">XXX XXX XXXX</a></strong>
            <br><span class="benefits-cta-subtitle">Experimenta el servicio de plomería más confiable de [Ciudad]</span>
        </p>
    </div>
</section>
```

### 3. CSS Beneficios

```css
.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.benefit {
    display: flex;
    gap: 1.25rem;
    padding: 1.5rem;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.benefit:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.benefit-icon {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #F97316 0%, #E36414 100%);
    border-radius: 12px;
    color: #fff;
}

.benefit-icon svg {
    width: 24px;
    height: 24px;
}

.benefit-content h3 {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #0F172A;
}

.benefit-content p {
    color: #475569;
    line-height: 1.6;
}

/* WhatsApp CTA destacado */
.whatsapp-cta-box {
    grid-column: 1 / -1; /* Full width */
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 2rem;
    background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
    border-radius: 16px;
    border: 2px solid #0EA5E9;
}

.whatsapp-cta-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: #22c55e;
    color: #fff;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.2s ease;
}

.whatsapp-cta-button:hover {
    background: #16a34a;
}

@media (max-width: 768px) {
    .whatsapp-cta-box {
        flex-direction: column;
        text-align: center;
    }
}
```

---

## Servicios

### 1. Servicios Principales (6-8 Cards)

**Servicios esenciales para plomería:**
1. Reparación de fugas
2. Destape de drenajes
3. Instalación de sanitarios
4. Mantenimiento de boiler
5. Corrección de baja presión
6. Detección de fugas
7. Instalación de tuberías (opcional)
8. Emergencias 24/7 (opcional)

### 2. HTML Card de Servicio

```html
<section id="servicios" class="section">
    <div class="container">
        <h2>Nuestros Servicios</h2>
        <div class="grid">
            <!-- Card: Reparación de fugas -->
            <a href="/servicios/reparacion-de-fugas/" class="card card--img">
                <div class="service-card">
                    <figure class="media-box">
                        <picture>
                            <source type="image/webp"
                                    srcset="/assets/images/reparacion-fugas-420w.webp 420w,
                                            /assets/images/reparacion-fugas-800w.webp 800w"
                                    sizes="(max-width:768px) 100vw, 420px">
                            <img src="/assets/images/reparacion-fugas-420w.webp"
                                 alt="Plomero reparando fuga de agua en tubería con herramientas profesionales"
                                 width="420" height="420"
                                 loading="lazy" decoding="async">
                        </picture>
                    </figure>
                </div>
                <h3>Reparación de fugas</h3>
                <p>Detectamos y reparamos fugas de agua en muros, techos y patios. Utilizamos equipo especializado para localizar la fuga sin romper innecesariamente.</p>
                <ul class="service-list">
                    <li>Detección con geófono y termografía</li>
                    <li>Garantía de 6 meses en reparación</li>
                </ul>
                <span class="service-cta">Más Información →</span>
            </a>

            <!-- Repetir para cada servicio -->
        </div>
    </div>
</section>
```

### 3. CSS Cards de Servicio

```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.card {
    display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-decoration: none;
    color: inherit;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.media-box {
    width: 100%;
    height: 280px;
    overflow: hidden;
}

.media-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.card:hover .media-box img {
    transform: scale(1.05);
}

.card h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1.5rem 1.5rem 0.75rem;
    color: #0F172A;
}

.card p {
    margin: 0 1.5rem 1rem;
    color: #475569;
    line-height: 1.6;
}

.service-list {
    list-style: none;
    padding: 0;
    margin: 0 1.5rem 1.5rem;
}

.service-list li {
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
    color: #475569;
}

.service-list li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #22c55e;
    font-weight: 700;
}

.service-cta {
    margin: auto 1.5rem 1.5rem;
    color: #0066cc;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.card:hover .service-cta {
    gap: 0.75rem;
}

@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
```

### 4. Especificaciones de Imágenes de Servicios

**Por cada servicio:**
- **Formatos**: WebP 420w (35 KB), 800w (85 KB)
- **Dimensiones**: Cuadradas 420x420px, 800x800px
- **Contenido**: Herramientas específicas, plomero en acción, resultado final
- **Alt text descriptivo**: "Plomero [acción] [objeto] con [herramienta] en [ciudad]"
- **Loading**: lazy (excepto primeros 3 servicios)

---

## Elementos de Confianza

### 1. Reseñas y Testimonios

**Estructura de testimonios:**

```html
<section class="section testimonials-section">
    <div class="container">
        <h2>Lo que dicen nuestros clientes</h2>
        <p class="section-subtitle">Más de 150 familias y negocios confían en nosotros</p>

        <div class="testimonials-grid">
            <!-- Testimonial 1 -->
            <div class="testimonial">
                <div class="testimonial-header">
                    <div class="testimonial-rating">★★★★★</div>
                    <div class="testimonial-source">
                        <svg class="google-icon"><!-- Google logo --></svg>
                        <span>Google</span>
                    </div>
                </div>
                <p class="testimonial-text">
                    "Tenía una fuga escondida en el muro desde hace meses. Llegaron con un aparato
                    y la encontraron en 20 minutos sin romper toda la pared. Excelente servicio."
                </p>
                <div class="testimonial-author">
                    <strong>Roberto M.</strong>
                    <span>Las Quintas · Hace 2 semanas</span>
                </div>
            </div>

            <!-- Repetir 5-6 testimonios -->
        </div>

        <div class="testimonials-cta">
            <a href="https://g.page/r/XXXXX/review" target="_blank" class="btn-secondary">
                Ver más reseñas en Google
            </a>
        </div>
    </div>
</section>
```

**CSS Testimonials:**

```css
.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.testimonial {
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.testimonial-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.testimonial-rating {
    color: #FBBC04;
    font-size: 1.1rem;
}

.testimonial-source {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: #5f6368;
}

.testimonial-text {
    color: #475569;
    line-height: 1.6;
    margin-bottom: 1rem;
    font-style: italic;
}

.testimonial-author strong {
    display: block;
    color: #0F172A;
    font-weight: 600;
}

.testimonial-author span {
    font-size: 0.875rem;
    color: #94a3b8;
}
```

### 2. Schema.org Review Markup

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "author": {
    "@type": "Person",
    "name": "Roberto M."
  },
  "datePublished": "2024-11-13",
  "reviewBody": "Tenía una fuga escondida en el muro desde hace meses. Llegaron con un aparato y la encontraron en 20 minutos sin romper toda la pared. Excelente servicio.",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Google"
  }
}
</script>
```

### 3. Garantías y Certificaciones

```html
<div class="trust-badges">
    <div class="badge">
        <svg class="badge-icon"><!-- Shield icon --></svg>
        <div class="badge-content">
            <strong>Garantía 6 meses</strong>
            <span>En mano de obra y materiales</span>
        </div>
    </div>
    <div class="badge">
        <svg class="badge-icon"><!-- Document icon --></svg>
        <div class="badge-content">
            <strong>Factura SAT</strong>
            <span>Deducible y válida</span>
        </div>
    </div>
    <div class="badge">
        <svg class="badge-icon"><!-- Certificate icon --></svg>
        <div class="badge-content">
            <strong>Técnicos certificados</strong>
            <span>15+ años de experiencia</span>
        </div>
    </div>
</div>
```

---

## Calls-to-Action (CTAs)

### 1. Ubicaciones de CTAs

**Frecuencia recomendada:** CTA cada 2-3 secciones (aprox. cada 800px de scroll)

| Ubicación | Tipo | Texto | Link |
|-----------|------|-------|------|
| Hero | Primario | Solicitar Atención Inmediata | #contacto |
| Beneficios | Secundario | Abrir Chat | wa.me/ |
| Servicios | Links | Más Información → | /servicios/[servicio]/ |
| Urgencias | Primario | WhatsApp: 52 XXX XXX XXXX | wa.me/ |
| FAQs | Secundario | ¿Tienes otra duda? Escríbenos | wa.me/ |
| Testimonios | Secundario | Ver más reseñas | Google/Facebook |
| Pre-Footer | Primario doble | WhatsApp + Llamar | wa.me/ + tel: |
| Flotante derecha | Fijo | Íconos | wa.me/ + tel: |
| Exit-intent | Modal | WhatsApp + Llamar | wa.me/ + tel: |

### 2. Botones Primarios

```css
.btn-primary {
    display: inline-block;
    background: linear-gradient(135deg, #fba336 0%, #f97316 45%, #e36414 100%);
    color: #fff;
    border: none;
    border-radius: 14px;
    padding: 17px 34px;
    font-weight: 700;
    font-size: 1rem;
    text-decoration: none;
    cursor: pointer;
    box-shadow: 0 10px 24px rgba(227, 100, 20, 0.28);
    min-height: 48px; /* Touch target accessibility */
    min-width: 48px;
    transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
}

.btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 32px rgba(227, 100, 20, 0.34);
    filter: brightness(1.04);
}

.btn-primary:active {
    transform: translateY(0);
    box-shadow: 0 10px 20px rgba(227, 100, 20, 0.28);
}
```

### 3. CTAs Flotantes

```html
<!-- WhatsApp Flotante -->
<a href="https://wa.me/52XXXXXXXXXX?text=Hola%2C%20necesito%20un%20plomero%20urgente"
   id="cta-whatsapp"
   class="floating-btn floating-whatsapp"
   target="_blank"
   aria-label="Contactar por WhatsApp">
    <svg width="24" height="24" fill="currentColor">
        <!-- WhatsApp icon path -->
    </svg>
</a>

<!-- Teléfono Flotante -->
<a href="tel:+52XXXXXXXXXX"
   id="cta-llamar"
   class="floating-btn floating-call"
   aria-label="Llamar ahora">
    <svg width="24" height="24" fill="currentColor">
        <!-- Phone icon path -->
    </svg>
</a>
```

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
    transition: transform 0.12s ease, box-shadow 0.12s ease;
    z-index: 60;
    text-decoration: none;
}

.floating-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.2);
    filter: brightness(1.05);
}

.floating-call {
    background: #0f4fa8; /* Blue */
    bottom: 18px;
}

.floating-whatsapp {
    background: #22c55e; /* WhatsApp green */
    bottom: 78px; /* 60px above phone button */
}

/* Mobile: reducir tamaño */
@media (max-width: 768px) {
    .floating-btn {
        width: 48px;
        height: 48px;
        right: 12px;
    }

    .floating-call {
        bottom: 12px;
    }

    .floating-whatsapp {
        bottom: 68px;
    }
}
```

### 4. Exit-Intent Popup

```html
<div id="exit-intent-popup" style="display:none;">
    <div class="exit-popup-overlay"></div>
    <div class="exit-popup-content">
        <button class="exit-popup-close" aria-label="Cerrar">×</button>
        <h3>¡Espera! 🛠️</h3>
        <p>¿Tienes una emergencia de plomería? Contáctanos ahora y llegamos en 30-60 minutos.</p>
        <div class="exit-popup-ctas">
            <a href="https://wa.me/52XXXXXXXXXX?text=Hola%2C%20necesito%20un%20plomero%20urgente"
               id="exit-popup-whatsapp"
               target="_blank"
               class="btn-primary">
                <svg><!-- WhatsApp icon --></svg>
                WhatsApp
            </a>
            <a href="tel:+52XXXXXXXXXX"
               id="exit-popup-phone"
               class="btn-secondary">
                <svg><!-- Phone icon --></svg>
                Llamar Ahora
            </a>
        </div>
    </div>
</div>
```

```css
#exit-intent-popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.exit-popup-content {
    background: #fff;
    border-radius: 16px;
    padding: 2rem;
    max-width: 400px;
    margin: 1rem;
    position: relative;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.exit-popup-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
    line-height: 1;
    padding: 0.25rem 0.5rem;
}

.exit-popup-ctas {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1.5rem;
}
```

**JavaScript (exit-intent detection):**

```javascript
// Exit Intent Popup
(function() {
    var popup = document.getElementById('exit-intent-popup');
    var hasShown = localStorage.getItem('exitPopupShown');
    var isExiting = false;
    var mouseY = 0;
    var timeOnPage = 0;
    var minTimeBeforePopup = 2000; // 2 segundos mínimo

    if (hasShown) return; // Solo mostrar una vez por sesión

    var pageLoadTime = Date.now();

    // Desktop: detectar mouse saliendo por arriba
    document.addEventListener('mousemove', function(e) {
        mouseY = e.clientY;
    });

    document.addEventListener('mouseout', function(e) {
        if (isExiting) return;
        var toElement = e.relatedTarget || e.toElement;
        timeOnPage = Date.now() - pageLoadTime;

        if (!toElement && mouseY < 10 && timeOnPage >= minTimeBeforePopup) {
            isExiting = true;
            showPopup();
        }
    });

    // Mobile: detectar scroll hacia arriba
    var lastScrollY = 0;
    window.addEventListener('scroll', function() {
        var currentScrollY = window.pageYOffset;
        var scrollingUp = currentScrollY < lastScrollY;
        timeOnPage = Date.now() - pageLoadTime;

        if (scrollingUp &&
            currentScrollY < 300 &&
            timeOnPage >= 10000 &&
            !isExiting) {
            isExiting = true;
            showPopup();
        }

        lastScrollY = currentScrollY;
    });

    function showPopup() {
        popup.style.display = 'flex';
        localStorage.setItem('exitPopupShown', 'true');
    }

    // Cerrar popup
    document.querySelector('.exit-popup-close').addEventListener('click', function() {
        popup.style.display = 'none';
    });

    popup.addEventListener('click', function(e) {
        if (e.target === popup) {
            popup.style.display = 'none';
        }
    });
})();
```

---

## Formulario de Contacto

### 1. HTML Formulario

```html
<section id="contacto" class="section">
    <div class="container">
        <h2>Solicita tu Cotización</h2>
        <p class="section-subtitle">
            También te contactaremos por WhatsApp. Respuesta en menos de 30 minutos.
        </p>

        <form id="contact-form"
              name="contacto-plomeria"
              method="POST"
              netlify
              netlify-honeypot="bot-field"
              action="/gracias">

            <!-- Honeypot anti-spam -->
            <input type="hidden" name="form-name" value="contacto-plomeria">
            <div style="display:none;">
                <label>No llenar: <input name="bot-field"></label>
            </div>

            <!-- Campo: Nombre -->
            <div class="form-field">
                <label for="nombre">Nombre completo *</label>
                <input type="text"
                       id="nombre"
                       name="nombre"
                       placeholder="Ej: Juan Pérez"
                       required
                       autocomplete="name">
                <span class="error-message">Por favor ingresa tu nombre</span>
            </div>

            <!-- Campo: Teléfono -->
            <div class="form-field">
                <label for="telefono">Teléfono (10 dígitos) *</label>
                <input type="tel"
                       id="telefono"
                       name="telefono"
                       placeholder="Ej: 6671234567"
                       required
                       pattern="[0-9]{10}"
                       autocomplete="tel">
                <span class="error-message">Ingresa 10 dígitos sin espacios</span>
            </div>

            <!-- Campo: Email -->
            <div class="form-field">
                <label for="email">Email *</label>
                <input type="email"
                       id="email"
                       name="email"
                       placeholder="Ej: juan@ejemplo.com"
                       required
                       autocomplete="email">
                <span class="error-message">Ingresa un email válido</span>
            </div>

            <!-- Campo: Mensaje -->
            <div class="form-field">
                <label for="mensaje">Describe tu problema o servicio *</label>
                <textarea id="mensaje"
                          name="mensaje"
                          placeholder="Ej: Tengo una fuga en el baño..."
                          rows="4"
                          required
                          minlength="10"></textarea>
                <span class="error-message">Describe brevemente el problema (mínimo 10 caracteres)</span>
            </div>

            <!-- Botón Submit -->
            <button type="submit" class="btn-primary">
                Enviar Solicitud
            </button>

            <!-- Alternativa WhatsApp -->
            <p class="form-alternative">
                O también puedes
                <a href="https://wa.me/52XXXXXXXXXX?text=Hola%2C%20necesito%20cotización"
                   target="_blank">
                    contactarnos directamente por WhatsApp
                </a>
            </p>
        </form>
    </div>
</section>
```

### 2. JavaScript Validación en Tiempo Real

```javascript
// Real-time form validation
(function() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const nombreField = document.getElementById('nombre');
    const telefonoField = document.getElementById('telefono');
    const emailField = document.getElementById('email');
    const mensajeField = document.getElementById('mensaje');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Validation functions
    const validators = {
        nombre: (value) => value.trim().length >= 2,
        telefono: (value) => /^[0-9]{10}$/.test(value.replace(/\s/g, '')),
        email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        mensaje: (value) => value.trim().length >= 10
    };

    // Validate single field
    function validateField(field, validatorKey) {
        const value = field.value;
        const fieldWrapper = field.closest('.form-field');
        const isValid = validators[validatorKey](value);

        if (value.length === 0) {
            fieldWrapper.classList.remove('valid', 'invalid');
        } else if (isValid) {
            fieldWrapper.classList.remove('invalid');
            fieldWrapper.classList.add('valid');
        } else {
            fieldWrapper.classList.remove('valid');
            fieldWrapper.classList.add('invalid');
        }

        updateSubmitButton();
        return isValid;
    }

    // Check if form is completely valid
    function isFormValid() {
        return validators.nombre(nombreField.value) &&
               validators.telefono(telefonoField.value) &&
               validators.email(emailField.value) &&
               validators.mensaje(mensajeField.value);
    }

    // Enable/disable submit button
    function updateSubmitButton() {
        if (isFormValid()) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            submitBtn.style.cursor = 'not-allowed';
        }
    }

    // Add event listeners
    nombreField.addEventListener('input', () => validateField(nombreField, 'nombre'));
    nombreField.addEventListener('blur', () => validateField(nombreField, 'nombre'));

    telefonoField.addEventListener('input', () => {
        telefonoField.value = telefonoField.value.replace(/\D/g, ''); // Only numbers
        validateField(telefonoField, 'telefono');
    });
    telefonoField.addEventListener('blur', () => validateField(telefonoField, 'telefono'));

    emailField.addEventListener('input', () => validateField(emailField, 'email'));
    emailField.addEventListener('blur', () => validateField(emailField, 'email'));

    mensajeField.addEventListener('input', () => validateField(mensajeField, 'mensaje'));
    mensajeField.addEventListener('blur', () => validateField(mensajeField, 'mensaje'));

    // Initial state: button disabled
    updateSubmitButton();

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const nombre = formData.get('nombre');
        const telefono = formData.get('telefono');
        const email = formData.get('email');
        const mensaje = formData.get('mensaje');

        // Track in GA4
        if (window.dataLayer) {
            window.dataLayer.push({
                'event': 'generate_lead',
                'form_name': 'contact_form_homepage',
                'value': 1
            });
        }

        // Submit to Netlify
        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData).toString()
            });

            if (response.ok) {
                // Open WhatsApp
                const whatsappMessage = `Hola! Solicito cotización:\\n\\nNombre: ${nombre}\\nTeléfono: ${telefono}\\nEmail: ${email}\\nMensaje: ${mensaje}`;
                const whatsappURL = `https://wa.me/52XXXXXXXXXX?text=${encodeURIComponent(whatsappMessage)}`;
                window.open(whatsappURL, '_blank');

                // Redirect to thank you page
                window.location.href = '/gracias';
            }
        } catch (error) {
            alert('Formulario enviado. Te redirigiremos a WhatsApp.');
            const whatsappMessage = `Hola! Solicito cotización:\\nNombre: ${nombre}\\nTeléfono: ${telefono}`;
            window.location.href = `https://wa.me/52XXXXXXXXXX?text=${encodeURIComponent(whatsappMessage)}`;
        }
    });
})();
```

### 3. CSS Validación Visual

```css
/* Form field wrapper */
.form-field {
    position: relative;
    margin-bottom: 1.25rem;
}

.form-field label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #0F172A;
}

.form-field input,
.form-field textarea {
    width: 100%;
    padding: 0.875rem;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.form-field input:focus,
.form-field textarea:focus {
    outline: none;
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

/* Valid state (green checkmark) */
.form-field.valid input,
.form-field.valid textarea {
    border-color: #28a745;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%2328a745'%3E%3Cpath d='M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.875rem center;
    background-size: 20px 20px;
    padding-right: 3rem;
}

/* Invalid state (red X) */
.form-field.invalid input,
.form-field.invalid textarea {
    border-color: #dc3545;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%23dc3545'%3E%3Cpath d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.875rem center;
    background-size: 20px 20px;
    padding-right: 3rem;
}

/* Error message */
.error-message {
    display: none;
    color: #dc3545;
    font-size: 0.875rem;
    margin-top: 0.375rem;
    font-weight: 500;
}

.form-field.invalid .error-message {
    display: block;
}

/* Disabled submit button */
button[type="submit"]:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.form-alternative {
    text-align: center;
    margin-top: 1.5rem;
    color: #475569;
}

.form-alternative a {
    color: #22c55e;
    font-weight: 600;
    text-decoration: none;
}
```

---

## SEO On-Page

### 1. Schema.org Structured Data

**Schema esencial para plomería:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://tudominio.com",
      "name": "Plomero [Ciudad] Pro",
      "image": "https://tudominio.com/logo.webp",
      "url": "https://tudominio.com/",
      "telephone": "+52XXXXXXXXXX",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "[Ciudad]",
        "addressRegion": "[Estado]",
        "addressCountry": "MX"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 24.8090556,
        "longitude": -107.3940556
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00",
        "closes": "23:59"
      },
      "sameAs": [
        "https://www.facebook.com/tuempresa",
        "https://www.instagram.com/tuempresa"
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": "150"
      }
    },
    {
      "@type": "Service",
      "serviceType": "Reparación de Fugas de Agua",
      "provider": {
        "@id": "https://tudominio.com"
      },
      "areaServed": {
        "@type": "City",
        "name": "[Ciudad]"
      },
      "description": "Reparación profesional de fugas de agua con equipo especializado"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Cuánto tiempo tarda la reparación de una fuga?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "La mayoría de reparaciones se completan en 2-4 horas, dependiendo de la ubicación y severidad."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Inicio",
          "item": "https://tudominio.com/"
        }
      ]
    }
  ]
}
</script>
```

### 2. Palabras Clave

**Palabras clave primarias:**
- Plomero en [Ciudad]
- Plomería [Ciudad]
- Plomero 24/7 [Ciudad]
- Emergencia plomería [Ciudad]

**Palabras clave secundarias:**
- Reparación de fugas [Ciudad]
- Destape de drenajes [Ciudad]
- Instalación de sanitarios [Ciudad]
- Plomero cerca de mí
- Plomero [Colonia]

**Implementación en HTML:**

```html
<!-- Title tag (50-60 caracteres) -->
<title>Plomero en Culiacán 24/7 | Llegada en 30-60 min + Garantía</title>

<!-- Meta description (150-160 caracteres) -->
<meta name="description" content="Plomero certificado en Culiacán · Emergencia 24/7 con llegada en 30-60 min · Cobertura Las Quintas, Tres Ríos, Centro · WhatsApp inmediato · Factura disponible">

<!-- H1 (único por página) -->
<h1>Plomero en Culiacán – Emergencias 24/7</h1>

<!-- H2 con variaciones -->
<h2>Servicios de Plomería en Culiacán</h2>
<h2>¿Por qué elegirnos como tu plomero de confianza?</h2>
<h2>Atendemos todas las colonias de Culiacán</h2>

<!-- H3 para servicios específicos -->
<h3>Reparación de fugas de agua en muros y techos</h3>
<h3>Destape de drenajes con maquinaria especializada</h3>
```

### 3. URLs Semánticas

```
Homepage:
https://tudominio.com/

Servicios:
https://tudominio.com/servicios/reparacion-de-fugas/
https://tudominio.com/servicios/destape-de-drenajes/
https://tudominio.com/servicios/instalacion-de-sanitarios/

Colonias:
https://tudominio.com/servicios/plomero-colonias-[ciudad]/[colonia]/

Blog:
https://tudominio.com/blog/como-detectar-fugas-agua-casa/
```

### 4. Alt Text para Imágenes

**Estructura:** `[Acción] + [Objeto] + [Contexto] + [Ubicación]`

**Ejemplos:**
```html
<!-- Hero -->
<img src="hero.webp" alt="Plomero profesional en Culiacán atendiendo emergencia 24 horas con herramientas especializadas">

<!-- Servicios -->
<img src="reparacion-fugas.webp" alt="Plomero reparando fuga de agua en tubería con herramientas profesionales en Culiacán">

<img src="destape-drenajes.webp" alt="Plomero destapando drenaje con sonda rotativa profesional en Culiacán">

<img src="instalacion-sanitarios.webp" alt="Instalación profesional de sanitario ahorrador de agua en baño moderno Culiacán">
```

### 5. Canonical Tags

```html
<!-- Homepage -->
<link rel="canonical" href="https://tudominio.com/">

<!-- Páginas de servicio -->
<link rel="canonical" href="https://tudominio.com/servicios/reparacion-de-fugas/">
```

---

## Performance y Core Web Vitals

### 1. Métricas Objetivo

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| LCP (Largest Contentful Paint) | <2.5s | <4s |
| FID (First Input Delay) | <100ms | <300ms |
| CLS (Cumulative Layout Shift) | <0.1 | <0.25 |
| FCP (First Contentful Paint) | <1.8s | <3s |
| TTI (Time to Interactive) | <3.8s | <7.3s |
| Speed Index | <3.4s | <5.8s |

### 2. Optimización de Imágenes

**WebP con fallback:**

```html
<picture>
    <source type="image/webp"
            srcset="/assets/images/hero-800w.webp 800w,
                    /assets/images/hero-1200w.webp 1200w"
            sizes="100vw">
    <img src="/assets/images/hero-1200w.jpg"
         srcset="/assets/images/hero-800w.jpg 800w,
                 /assets/images/hero-1200w.jpg 1200w"
         alt="Plomero profesional en Culiacán"
         width="1200"
         height="800"
         loading="lazy"
         decoding="async">
</picture>
```

**Tamaños recomendados:**
- Hero: 1200w (95 KB), 800w (51 KB)
- Servicios: 800w (85 KB), 420w (35 KB)
- Thumbnails: 420w (35 KB), 280w (18 KB)

**Comandos de conversión (cwebp):**

```bash
# Hero image (calidad 85)
cwebp -q 85 hero-original.jpg -o hero-1200w.webp
cwebp -resize 800 0 -q 85 hero-original.jpg -o hero-800w.webp

# Service images (calidad 90)
cwebp -q 90 servicio-original.jpg -o servicio-800w.webp
cwebp -resize 420 0 -q 90 servicio-original.jpg -o servicio-420w.webp
```

### 3. Critical CSS Inline

```html
<head>
    <!-- Critical CSS inline (above-the-fold) -->
    <style>
        /* Reset + variables + fonts + hero styles */
        @font-face{font-family:'Inter';src:url('assets/fonts/inter-400.woff2') format('woff2')}
        :root{--brand:#E36414;--text:#0F172A;--bg:#FFFFFF}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',sans-serif;font-size:16px;color:var(--text)}
        .hero{min-height:85vh;display:grid;place-items:center}
        /* ... más estilos críticos ... */
    </style>

    <!-- Non-critical CSS defer -->
    <link rel="preload" href="/styles.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/styles.min.css"></noscript>
</head>
```

### 4. Fonts Optimization

```css
/* Font-display: swap previene FOIT (Flash of Invisible Text) */
@font-face {
    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-display: swap; /* ← CRÍTICO */
    src: url('assets/fonts/inter-400.woff2') format('woff2');
}

@font-face {
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 800;
    font-display: swap;
    src: url('assets/fonts/montserrat-800.woff2') format('woff2');
}
```

**Preload fonts críticos:**

```html
<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
<link rel="preload" href="/assets/fonts/montserrat-800.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
```

### 5. JavaScript Optimization

```html
<!-- Main JS: defer para no bloquear rendering -->
<script src="/main.js" defer></script>

<!-- Analytics: async + low priority -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
```

**Service Worker (PWA):**

```javascript
// sw.js - Cache estratégico
const CACHE_NAME = 'plomero-v1';
const urlsToCache = [
  '/',
  '/styles.min.css',
  '/main.js',
  '/assets/fonts/inter-400.woff2',
  '/assets/fonts/montserrat-800.woff2',
  '/assets/images/hero-1200w.webp'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

### 6. Preconnect External Domains

```html
<!-- GTM -->
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">

<!-- WhatsApp -->
<link rel="preconnect" href="https://wa.me">
<link rel="dns-prefetch" href="https://wa.me">

<!-- Google Fonts (si se usan) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

### 7. Lazy Loading

```html
<!-- Imágenes below-the-fold: lazy -->
<img src="servicio.webp"
     alt="Servicio de plomería"
     loading="lazy"
     decoding="async">

<!-- Hero image: eager (default) -->
<img src="hero.webp"
     alt="Hero"
     fetchpriority="high"
     decoding="async">
```

---

## Diseño Responsive

### 1. Breakpoints

```css
/* Mobile-first approach */
:root {
    --container-gutter: 16px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
    :root {
        --container-gutter: 24px;
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    /* Estilos desktop */
}

/* Large desktop (1440px+) */
@media (min-width: 1440px) {
    /* Max width containers */
}
```

### 2. Grid Responsive

```css
/* Auto-fit: columnas automáticas según espacio disponible */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
}

/* Mobile: forzar 1 columna */
@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
```

### 3. Typography Responsive

```css
/* Clamp: tamaño fluido sin media queries */
h1 {
    font-size: clamp(2.5rem, 5vw, 4rem);
    /* Min: 2.5rem (40px)
       Preferido: 5vw (5% del viewport)
       Max: 4rem (64px) */
}

h2 {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
}

h3 {
    font-size: clamp(1.25rem, 3vw, 1.75rem);
}

body {
    font-size: clamp(0.875rem, 2vw, 1rem);
}
```

### 4. Hero Mobile Adaptations

```css
/* Desktop */
.hero {
    min-height: 85vh;
    padding: 140px 16px;
}

.hero-content {
    padding: 3rem 2.5rem;
    background: rgba(255, 255, 255, 0.15);
}

/* Mobile */
@media (max-width: 768px) {
    .hero {
        min-height: 75vh;
        padding-top: 85px;
        align-items: flex-start; /* Alinear arriba */
    }

    .hero-content {
        padding: 1.5rem 1.25rem;
        background: rgba(255, 255, 255, 0.12); /* Más opaco */
    }

    .hero h1 {
        font-size: clamp(1.5rem, 5vw, 2rem);
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        display: none; /* Simplificar en mobile */
    }

    .hero-features {
        gap: 1rem;
    }
}
```

### 5. Touch Targets

```css
/* Accessibility: mínimo 48x48px para táctil */
.btn-primary {
    min-height: 48px;
    min-width: 48px;
    padding: 17px 34px;
}

.floating-btn {
    width: 54px;
    height: 54px;
}

/* Mobile: reducir ligeramente */
@media (max-width: 768px) {
    .floating-btn {
        width: 48px;
        height: 48px;
    }
}
```

### 6. Navigation Mobile

```css
/* Desktop */
.nav-menu {
    display: flex;
    gap: 2rem;
}

.mobile-menu-btn {
    display: none;
}

/* Mobile */
@media (max-width: 768px) {
    .mobile-menu-btn {
        display: flex; /* Hamburger icon */
    }

    .nav-menu {
        position: fixed;
        top: 65px;
        left: -100%; /* Oculto por defecto */
        width: 100%;
        height: calc(100vh - 65px);
        background: rgba(255, 255, 255, 0.98);
        flex-direction: column;
        padding: 3rem 2rem;
        gap: 2rem;
        transition: left 0.3s ease;
    }

    .nav-menu.active {
        left: 0; /* Mostrar cuando active */
    }
}
```

---

## Branding y Diseño Visual

### 1. Paleta de Colores

```css
:root {
    /* Brand colors */
    --brand: #E36414;           /* Naranja oscuro */
    --brand-light: #F97316;     /* Naranja claro */
    --brand-dark: #C2410C;      /* Naranja más oscuro */

    /* Text colors */
    --text: #0F172A;            /* Azul oscuro casi negro */
    --text-light: #475569;      /* Gris medio */
    --text-muted: #94a3b8;      /* Gris claro */

    /* Background colors */
    --bg: #FFFFFF;              /* Blanco puro */
    --bg-soft: #F8FAFC;         /* Gris muy claro */
    --bg-alt: #E0F2FE;          /* Azul muy claro */

    /* Border & shadows */
    --border: #E2E8F0;          /* Gris borde */
    --shadow: rgba(15, 23, 42, 0.1); /* Sombra azul */

    /* Status colors */
    --success: #22c55e;         /* Verde (WhatsApp) */
    --error: #dc3545;           /* Rojo */
    --warning: #f59e0b;         /* Amarillo */
    --info: #0ea5e9;            /* Azul */

    /* Gradientes */
    --gradient-brand: linear-gradient(135deg, #F97316 0%, #E36414 100%);
    --gradient-bg: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
}
```

**Uso de colores:**

```css
/* Botón primario: degradado naranja */
.btn-primary {
    background: linear-gradient(135deg, #fba336 0%, #f97316 45%, #e36414 100%);
}

/* Links: azul */
a {
    color: #0066cc;
}

/* Success: verde */
.form-field.valid input {
    border-color: var(--success);
}

/* WhatsApp: verde oficial */
.floating-whatsapp {
    background: #22c55e;
}

/* Teléfono: azul */
.floating-call {
    background: #0f4fa8;
}
```

### 2. Tipografía

**Fuentes:**
- **Sans-serif primaria**: Inter (body text, UI)
- **Sans-serif display**: Montserrat (headings)

```css
/* Inter: body text */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    font-weight: 400;
}

/* Montserrat: headings */
h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

/* Jerarquía */
h1 {
    font-size: clamp(2.5rem, 5vw, 4rem);
    margin-bottom: 1.5rem;
}

h2 {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    margin-bottom: 1.25rem;
}

h3 {
    font-size: clamp(1.25rem, 3vw, 1.75rem);
    margin-bottom: 1rem;
}

/* Weights */
.font-normal { font-weight: 400; }  /* Body */
.font-medium { font-weight: 500; }  /* Nav */
.font-semibold { font-weight: 600; } /* Buttons */
.font-bold { font-weight: 700; }    /* Emphasis */
.font-extrabold { font-weight: 800; } /* Headings */
```

### 3. Spacing System

```css
/* Sistema de espaciado basado en múltiplos de 8px */
:root {
    --space-1: 0.25rem;  /* 4px */
    --space-2: 0.5rem;   /* 8px */
    --space-3: 0.75rem;  /* 12px */
    --space-4: 1rem;     /* 16px */
    --space-5: 1.25rem;  /* 20px */
    --space-6: 1.5rem;   /* 24px */
    --space-8: 2rem;     /* 32px */
    --space-10: 2.5rem;  /* 40px */
    --space-12: 3rem;    /* 48px */
    --space-16: 4rem;    /* 64px */
}

/* Uso */
.section {
    padding: var(--space-16) 0; /* 64px vertical */
}

.card {
    padding: var(--space-6); /* 24px */
    gap: var(--space-4); /* 16px */
}
```

### 4. Efectos Visuales

**Glassmorphism (hero content):**

```css
.hero-content {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

**Sombras (depth system):**

```css
/* Shadow scale */
.shadow-sm {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.shadow-md {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.shadow-lg {
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
}

.shadow-xl {
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.16);
}

/* Botones con sombra naranja */
.btn-primary {
    box-shadow: 0 10px 24px rgba(227, 100, 20, 0.28);
}

.btn-primary:hover {
    box-shadow: 0 14px 32px rgba(227, 100, 20, 0.34);
}
```

**Animaciones:**

```css
/* Transiciones suaves */
* {
    transition-duration: 0.2s;
    transition-timing-function: ease;
}

/* Hover lift effect */
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Button press */
.btn-primary:active {
    transform: translateY(0);
}

/* Fade in animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.6s ease-out;
}
```

**Border Radius:**

```css
/* Escalas de redondeo */
.rounded-sm { border-radius: 4px; }
.rounded-md { border-radius: 8px; }
.rounded-lg { border-radius: 12px; }
.rounded-xl { border-radius: 16px; }
.rounded-2xl { border-radius: 24px; }
.rounded-full { border-radius: 9999px; }

/* Uso */
.btn-primary { border-radius: 14px; }
.card { border-radius: 12px; }
.floating-btn { border-radius: 9999px; /* Full circle */ }
```

---

## Elementos de Urgencia

### 1. Mensajes de Urgencia

**Ubicaciones estratégicas:**

```html
<!-- Hero subtitle -->
<p class="hero-subtitle">
    Emergencia 24/7 con llegada en <strong>30-60 minutos</strong> con garantía escrita.
</p>

<!-- Beneficios -->
<h3>Llegamos hoy mismo</h3>
<p>Atendemos emergencias en <strong>30-60 min</strong>. Servicio 24/7 con herramientas completas.</p>

<!-- WhatsApp CTA -->
<h3>¿Tienes dudas? Respondemos en <strong>10 minutos</strong></h3>

<!-- Formulario -->
<p class="section-subtitle">
    También te contactaremos por WhatsApp. <strong>Respuesta en menos de 30 minutos.</strong>
</p>
```

### 2. Social Proof

**Rating badge en hero:**

```html
<div class="hero-rating">
    <svg class="google-logo"><!-- Google logo --></svg>
    <span class="rating-stars">★★★★★</span>
    <span class="rating-score">4.8/5</span>
    <span class="rating-divider">·</span>
    <span class="rating-count">Más de 150 vecinos de Culiacán satisfechos</span>
</div>
```

**Testimonios con fechas recientes:**

```html
<div class="testimonial-author">
    <strong>Roberto M.</strong>
    <span>Las Quintas · Hace 2 semanas</span>
</div>
```

### 3. Scarcity / Availability

```html
<!-- Sección urgencias -->
<section class="urgency-section">
    <div class="container">
        <h2>🚨 Atención de Emergencias</h2>
        <p>Estamos disponibles <strong>las 24 horas, todos los días del año</strong></p>
        <p>Tiempo promedio de llegada: <strong class="highlight">30-60 minutos</strong></p>
        <a href="https://wa.me/52XXXXXXXXXX" class="btn-primary">
            WhatsApp: 52 XXX XXX XXXX
        </a>
    </div>
</section>
```

```css
.urgency-section {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    padding: 3rem 1.5rem;
    text-align: center;
}

.highlight {
    color: #dc2626;
    font-weight: 700;
    font-size: 1.2em;
}
```

---

## Tracking y Analytics

### 1. Google Tag Manager

```html
<!-- Google Tag Manager (en <head>) -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>

<!-- Google Tag Manager (noscript en <body>) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
```

### 2. Eventos de Conversión

```javascript
// dataLayer push para eventos clave
window.dataLayer = window.dataLayer || [];

// Evento: Lead generado (form submit)
function trackLead() {
    window.dataLayer.push({
        'event': 'generate_lead',
        'form_name': 'contact_form_homepage',
        'method': 'netlify_forms',
        'value': 1,
        'currency': 'MXN'
    });
}

// Evento: CTA click
function trackCTA(type, label) {
    window.dataLayer.push({
        'event': 'cta_click',
        'cta_type': type,
        'cta_label': label,
        'page': location.pathname
    });
}

// Evento: Scroll depth
var scrollTracked = {};
window.addEventListener('scroll', function() {
    var scrollPercent = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);

    [25, 50, 75, 90].forEach(function(depth) {
        if (scrollPercent >= depth && !scrollTracked[depth]) {
            scrollTracked[depth] = true;
            window.dataLayer.push({
                'event': 'scroll_depth',
                'scroll_percentage': depth,
                'page_location': location.pathname
            });
        }
    });
});
```

### 3. Tracking de CTAs

```html
<!-- WhatsApp flotante -->
<a href="https://wa.me/52XXXXXXXXXX"
   id="cta-whatsapp"
   onclick="trackCTA('whatsapp', 'floating_button')"
   class="floating-btn floating-whatsapp">
    <!-- SVG -->
</a>

<!-- Teléfono flotante -->
<a href="tel:+52XXXXXXXXXX"
   id="cta-llamar"
   onclick="trackCTA('phone', 'floating_button')"
   class="floating-btn floating-call">
    <!-- SVG -->
</a>
```

---

## Checklist de Implementación

### ✅ Pre-Launch Checklist

#### SEO On-Page
- [ ] Title tag optimizado (50-60 caracteres)
- [ ] Meta description (150-160 caracteres)
- [ ] H1 único con palabra clave principal
- [ ] H2-H6 jerárquicos y con variaciones de keywords
- [ ] URLs semánticas y amigables
- [ ] Alt text en todas las imágenes
- [ ] Canonical tags en todas las páginas
- [ ] Schema.org implementado (Business, Service, Reviews, FAQPage)
- [ ] Open Graph tags (Facebook/WhatsApp)
- [ ] Twitter Card tags
- [ ] Robots.txt configurado
- [ ] Sitemap.xml generado y enviado a Search Console

#### Performance
- [ ] LCP <2.5s (Lighthouse)
- [ ] FID <100ms
- [ ] CLS <0.1
- [ ] Imágenes en WebP con fallback
- [ ] Responsive images (srcset)
- [ ] Critical CSS inline
- [ ] Fonts preloaded con font-display: swap
- [ ] JavaScript defer
- [ ] Service Worker (PWA)
- [ ] Manifest.json configurado
- [ ] Lazy loading en imágenes below-the-fold
- [ ] Preconnect external domains

#### Mobile
- [ ] Diseño responsive funcional (320px-1920px)
- [ ] Touch targets ≥48x48px
- [ ] Menu móvil funcional
- [ ] Formulario usable en móvil
- [ ] CTAs flotantes no obstruyen contenido
- [ ] Hero mobile optimizado (glassmorphism legible)

#### Funcionalidad
- [ ] Formulario con validación en tiempo real
- [ ] Netlify Forms configurado
- [ ] WhatsApp links funcionando
- [ ] Tel: links funcionando
- [ ] CTAs flotantes visibles y funcionales
- [ ] Exit-intent popup funcionando (desktop + mobile)
- [ ] Navegación smooth scroll
- [ ] Google Tag Manager instalado
- [ ] Eventos de conversión configurados

#### Contenido
- [ ] 6-8 servicios principales con descripciones
- [ ] 5+ testimonios con rating y fecha
- [ ] 8-10 FAQs con Schema.org
- [ ] Beneficios claros (5+)
- [ ] Información de contacto completa
- [ ] Horarios 24/7 visibles
- [ ] Garantías mencionadas
- [ ] Precios transparentes (rangos)
- [ ] Zonas/colonias de servicio listadas

#### Legal/Trust
- [ ] Facturación SAT mencionada
- [ ] Garantías escritas especificadas
- [ ] Términos y condiciones (opcional pero recomendado)
- [ ] Política de privacidad (opcional pero recomendado)
- [ ] Certificaciones/licencias (si aplica)

#### Testing
- [ ] Lighthouse score 90+ mobile
- [ ] Lighthouse score 95+ desktop
- [ ] Probado en Chrome, Safari, Firefox
- [ ] Probado en iOS + Android
- [ ] Formulario funcional (test de envío)
- [ ] Links externos abren en nueva pestaña
- [ ] Links internos funcionan
- [ ] 404 page personalizada
- [ ] Console sin errores JavaScript

#### Analytics
- [ ] Google Analytics 4 instalado
- [ ] Google Tag Manager configurado
- [ ] Eventos de conversión funcionando
- [ ] Search Console verificado
- [ ] Google My Business vinculado

---

## Recursos y Herramientas

### Optimización de Imágenes
- **WebP Converter**: `cwebp` (línea de comandos)
- **ImageOptim**: https://imageoptim.com/ (Mac)
- **Squoosh**: https://squoosh.app/ (web)

### Performance Testing
- **Lighthouse**: Chrome DevTools
- **PageSpeed Insights**: https://pagespeed.web.dev/
- **GTmetrix**: https://gtmetrix.com/
- **WebPageTest**: https://www.webpagetest.org/

### SEO Tools
- **Google Search Console**: https://search.google.com/search-console
- **Schema Markup Validator**: https://validator.schema.org/
- **Rich Results Test**: https://search.google.com/test/rich-results

### Fonts
- **Google Fonts**: https://fonts.google.com/
- **Font Squirrel**: https://www.fontsquirrel.com/
- **Fontsource**: https://fontsource.org/

### Icons
- **Heroicons**: https://heroicons.com/ (SVG)
- **Feather Icons**: https://feathericons.com/ (SVG)
- **Lucide**: https://lucide.dev/ (SVG)

---

## Conclusión

Esta guía proporciona un framework completo para crear una página web de plomería de alto rendimiento que:

✅ **Convierte visitantes en clientes** con CTAs omnipresentes y urgencia 24/7
✅ **Genera confianza** con reseñas, garantías y social proof
✅ **Rankea en Google** con SEO on-page robusto y Schema.org
✅ **Carga rápido** con Core Web Vitals optimizados (LCP <2.5s)
✅ **Funciona en móvil** con diseño responsive y touch-friendly

**Tiempo de implementación estimado**: 40-60 horas
**ROI esperado**: 8-15% tasa de conversión, ranking top 3 local en 3-6 meses

---

**Documento creado el**: 21 de noviembre de 2024
**Basado en**: Análisis de Plomero Culiacán Pro (https://plomeroculiacanpro.mx/)
**Versión**: 1.0
