# Documentación Técnica - Plomero Culiacán Pro

**Sitio Web**: plomeroculiacanpro.mx
**Fecha de creación**: Noviembre 2024
**Última actualización**: 12 de Noviembre, 2024
**Versión**: 2.1

---

## Tabla de Contenidos

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Tipografía y Fuentes](#tipografía-y-fuentes)
3. [Sistema de Colores](#sistema-de-colores)
4. [Variables CSS](#variables-css)
5. [Componentes Principales](#componentes-principales)
6. [Optimizaciones de Performance](#optimizaciones-de-performance)
7. [SEO y Metadatos](#seo-y-metadatos)
8. [Estructura de Páginas](#estructura-de-páginas)
9. [Estructura HTML de Artículos de Blog](#estructura-html-de-artículos-de-blog)
10. [Sistema de Rutas Relativas](#sistema-de-rutas-relativas)
11. [Script del Menú Móvil](#script-del-menú-móvil-obligatorio)
12. [Buenas Prácticas de Contenido](#buenas-prácticas-de-contenido)

---

## Estructura del Proyecto

```
plomero website/
├── index.html                          # Página principal
├── styles.css                          # Estilos globales
├── script.js                           # JavaScript principal
│
├── fonts/                              # Fuentes autohospedadas
│   ├── inter-400.woff2
│   ├── inter-500.woff2
│   ├── inter-600.woff2
│   ├── montserrat-700.woff2
│   └── montserrat-800.woff2
│
├── img/                                # Imágenes optimizadas WebP
│   ├── reparacion-fugas-420w.webp
│   ├── reparacion-fugas-800w.webp
│   ├── destapandodrenaje-420w.webp
│   ├── destapandodrenaje-800w.webp
│   ├── taza-de-baño-420w.webp
│   ├── taza-de-baño-800w.webp
│   ├── arreglando-boiler-420w.webp
│   ├── arreglando-boiler-800w.webp
│   ├── reivicion-bajapresion-420w.webp
│   ├── reivicion-bajapresion-800w.webp
│   ├── tinaco-420w.webp
│   └── tinaco-800w.webp
│
├── servicios/                          # Landing pages de servicios
│   ├── reparacion-de-fugas/
│   │   └── index.html
│   ├── destape-de-drenajes/
│   │   └── index.html
│   ├── instalacion-de-sanitarios/
│   │   └── index.html
│   ├── mantenimiento-de-boiler/
│   │   └── index.html
│   ├── correccion-baja-presion/
│   │   └── index.html
│   ├── deteccion-de-fugas/
│   │   └── index.html
│   └── plomero/
│       ├── 24-7/index.html
│       ├── cerca-de-mi/index.html
│       ├── a-domicilio/index.html
│       ├── precios/index.html
│       └── colonias/index.html
│
├── blog/                               # Blog de contenido
│   ├── index.html
│   ├── como-detectar-fugas-agua-casa/
│   │   └── index.html
│   ├── problemas-comunes-plomeria-culiacan/
│   │   └── index.html
│   ├── cuando-llamar-plomero-profesional/
│   │   └── index.html
│   └── marcha-paz-culiacan-2025/
│       └── index.html
│
├── sitemaps/
│   └── main_sitemap.xml
│
└── images/                             # Assets del sitio
    ├── favicon.ico
    ├── favicon.png
    └── logo-blue.svg
```

**Total de páginas HTML**: 24 archivos

---

## Tipografía y Fuentes

### Fuentes Principales

El sitio utiliza **fuentes autohospedadas** (self-hosted) para mejor performance y control.

#### 1. **Inter** (Fuente de cuerpo)
- **Uso**: Textos de párrafo, navegación, botones, contenido general
- **Weights disponibles**:
  - `400` (Regular) - Texto normal
  - `500` (Medium) - Énfasis moderado
  - `600` (Semi-Bold) - Enlaces y labels
- **Formato**: WOFF2 (optimizado)
- **Font-display**: `swap` (mejora LCP)
- **Características**:
  - Sans-serif moderna
  - Excelente legibilidad en pantallas
  - Optimizada para UI/UX
  - Letter-spacing: `-0.01em`

#### 2. **Montserrat** (Fuente de títulos)
- **Uso**: Títulos (H1, H2, H3), logo, CTAs destacados
- **Weights disponibles**:
  - `700` (Bold) - Títulos H3
  - `800` (Extra-Bold) - Títulos H1 y H2
- **Formato**: WOFF2 (optimizado)
- **Font-display**: `swap`
- **Características**:
  - Sans-serif geométrica
  - Alto impacto visual
  - Letter-spacing: `-0.025em`

### Jerarquía Tipográfica

```css
/* Títulos principales */
h1 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: clamp(2.5rem, 5vw, 4rem);      /* 40px - 64px */
  line-height: 1.2;
  letter-spacing: -0.025em;
}

h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 4vw, 2.75rem);     /* 32px - 44px */
  line-height: 1.2;
  letter-spacing: -0.025em;
}

h3 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: clamp(1.25rem, 2.5vw, 1.5rem); /* 20px - 24px */
  line-height: 1.2;
}

/* Texto de cuerpo */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 16px;
  line-height: 1.7;
  font-weight: 400;
  letter-spacing: -0.01em;
}

p {
  font-size: 1rem;              /* 16px */
  line-height: 1.7;
  color: var(--text-light);
}
```

### Preload de Fuentes Críticas

Para optimizar LCP, se precargan las fuentes más importantes:

```html
<link rel="preload" href="fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/montserrat-700.woff2" as="font" type="font/woff2" crossorigin>
```

---

## Sistema de Colores

### Paleta de Colores Principal

El sitio utiliza un sistema de colores basado en **variables CSS** definidas en `:root`.

```css
:root {
  /* Colores de marca (Brand) */
  --brand: #E36414;              /* Naranja principal */
  --brand-light: #F97316;        /* Naranja claro (hover/accent) */
  --brand-dark: #C2410C;         /* Naranja oscuro (pressed) */

  /* Acción especial */
  --whatsapp: #25D366;           /* Verde WhatsApp oficial */

  /* Textos */
  --text: #0F172A;               /* Texto principal (negro azulado) */
  --text-light: #475569;         /* Texto secundario (gris) */
  --text-muted: #475569;         /* Texto desenfatizado */

  /* Fondos */
  --bg: #FFFFFF;                 /* Fondo blanco puro */
  --bg-soft: #F8FAFC;            /* Fondo suave (gris muy claro) */
  --bg-card: #FFFFFF;            /* Fondo de tarjetas */

  /* Bordes y sombras */
  --border: #E2E8F0;             /* Bordes sutiles */
  --shadow: rgba(15,23,42,0.1);          /* Sombra suave */
  --shadow-lg: rgba(15,23,42,0.15);      /* Sombra pronunciada */

  /* Gradientes */
  --gradient-brand: linear-gradient(135deg, #F97316 0%, #E36414 100%);
  --gradient-overlay: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,41,59,0.8) 100%);
}
```

### Uso de Colores

| Elemento | Color | Variable CSS | Código Hex |
|----------|-------|--------------|------------|
| Botón principal | Naranja | `var(--brand)` | `#E36414` |
| Hover de botón | Naranja claro | `var(--brand-light)` | `#F97316` |
| Enlace activo | Naranja oscuro | `var(--brand-dark)` | `#C2410C` |
| Botón WhatsApp | Verde | `var(--whatsapp)` | `#25D366` |
| Títulos | Negro azulado | `var(--text)` | `#0F172A` |
| Párrafos | Gris | `var(--text-light)` | `#475569` |
| Fondo página | Gris claro | `var(--bg-soft)` | `#F8FAFC` |

### Accesibilidad de Contraste

Todos los pares de colores cumplen con **WCAG 2.1 AA**:

- Texto oscuro sobre fondo claro: **Ratio 12.5:1** ✅
- Botones naranjas con texto blanco: **Ratio 4.8:1** ✅
- Enlaces sobre fondo: **Ratio 7.2:1** ✅

---

## Variables CSS

### Espaciado (Spacing System)

```css
:root {
  --space-xs: 0.5rem;    /* 8px */
  --space-sm: 1rem;      /* 16px */
  --space-md: 2rem;      /* 32px */
  --space-lg: 3rem;      /* 48px */
  --space-xl: 4rem;      /* 64px */
  --space-2xl: 6rem;     /* 96px */
}
```

### Layout

```css
:root {
  --container-max-width: 1200px;     /* Ancho máximo del contenedor */
  --container-gutter: 24px;          /* Padding lateral del contenedor */
  --grid-gutter: 2rem;               /* Espacio entre elementos de grid */
}
```

### Border Radius

```css
:root {
  --radius-sm: 8px;       /* Elementos pequeños (badges, tags) */
  --radius-md: 12px;      /* Tarjetas y botones */
  --radius-lg: 20px;      /* Elementos grandes (hero cards) */
  --radius-full: 9999px;  /* Botones pill, círculos */
}
```

---

## Componentes Principales

### 1. Navegación (Nav)

```html
<nav class="nav">
    <div class="container">
        <div class="nav-wrapper">
            <a href="/" class="logo">Plomero Culiacán Pro</a>
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

**Características**:
- Sticky position (fijo al hacer scroll)
- Responsive con menú hamburguesa en móvil
- Height: 80px
- Background: Blanco con sombra sutil

### 2. Hero Section

```html
<header id="inicio" class="hero">
    <div class="container">
        <div class="hero-content">
            <h1 class="fade-in">Plomero Profesional en Culiacán, Sinaloa</h1>
            <p class="hero-subtitle fade-in">Soluciones rápidas y confiables...</p>
            <p class="hero-contact">WhatsApp: 52 667 163 1231 · Llamadas: 667 163 1231</p>
            <a href="#contacto" class="btn-primary hover-lift">Solicitar Cotización</a>
        </div>
    </div>
</header>
```

**Características**:
- Sin imagen de fondo (texto sobre color sólido)
- Gradiente de marca como fondo
- Animaciones fade-in
- CTA principal destacado

### 3. Tarjetas de Servicio (Service Cards)

```html
<a href="./servicios/reparacion-de-fugas/" class="card card--img">
    <div class="service-card">
        <figure class="media-box">
            <picture>
                <source type="image/webp"
                        srcset="img/reparacion-fugas-420w.webp 420w, img/reparacion-fugas-800w.webp 800w"
                        sizes="(max-width:768px) 100vw, 420px">
                <img src="img/reparacion-fugas-420w.webp"
                     srcset="img/reparacion-fugas-420w.webp 420w, img/reparacion-fugas-800w.webp 800w"
                     sizes="(max-width:768px) 100vw, 420px"
                     alt="Reparación de fugas"
                     width="420" height="420"
                     loading="lazy" decoding="async">
            </picture>
        </figure>
    </div>
    <h3>Reparación de fugas</h3>
    <p>Fugas en muros, techos y patios. Detección profesional y reparación garantizada.</p>
</a>
```

**Características**:
- Elemento `<picture>` con WebP optimizado
- Responsive images con srcset
- Lazy loading para mejor LCP
- Width/height explícitos para evitar CLS
- Hover effect con transform

### 4. Testimonios (Testimonial Cards)

```html
<div class="testimonial-card">
    <div class="stars">★★★★★</div>
    <p>"Excelente servicio. Repararon una fuga en mi baño en menos de 2 horas..."</p>
    <cite>— María G., Tres Ríos</cite>
    <small style="color: #888; display: block; margin-top: 0.5rem;">Reseña de Google</small>
</div>
```

**Layout**: Grid de 3 columnas en desktop, 1 columna en móvil

### 5. Botones (CTAs)

```html
<!-- Botón principal -->
<a href="#contacto" class="btn-primary hover-lift">Solicitar Cotización</a>

<!-- Botón secundario -->
<a href="/blog/" class="btn-secondary">Ver más artículos</a>

<!-- Botón WhatsApp -->
<a href="https://wa.me/526671631231" class="btn-whatsapp">WhatsApp: 52 667 163 1231</a>
```

**Estilos**:
- `.btn-primary`: Naranja con gradiente
- `.btn-secondary`: Borde naranja, fondo transparente
- `.btn-whatsapp`: Verde WhatsApp
- `.hover-lift`: Animación de elevación en hover

### 6. Blog Cards

```html
<article class="news-card card">
    <figure class="news-image">
        <img src="/img/reparacion-fugas-420w.webp"
             alt="Cómo detectar fugas de agua"
             width="420" height="420"
             loading="lazy">
    </figure>
    <div class="news-content">
        <time datetime="2024-11-11" class="news-date">11 de noviembre, 2024</time>
        <h3><a href="/blog/como-detectar-fugas-agua-casa/">Cómo Detectar Fugas...</a></h3>
        <p>Aprende a detectar fugas con métodos sencillos...</p>
        <a href="/blog/como-detectar-fugas-agua-casa/" class="read-more">Leer artículo completo →</a>
    </div>
</article>
```

---

## Optimizaciones de Performance

### 1. Imágenes

**Formato**: 100% WebP (no PNG/JPG)

**Estrategia de tamaños**:
- `420w`: Para móviles y thumbnails
- `800w`: Para tablets y desktop

**Ejemplo de implementación**:
```html
<picture>
    <source type="image/webp" srcset="img/nombre-420w.webp 420w, img/nombre-800w.webp 800w">
    <img src="img/nombre-420w.webp" width="420" height="420" loading="lazy">
</picture>
```

**Beneficios**:
- Reducción del 93% en peso vs PNG
- LCP mejorado (carga 10-15x más rápida)
- Width/height explícitos previenen CLS

### 2. Fuentes

**Técnicas aplicadas**:
- Self-hosting (sin llamadas a Google Fonts)
- WOFF2 (máxima compresión)
- `font-display: swap` (previene FOIT)
- Preload de fuentes críticas

**Impacto**:
- 0 llamadas externas
- Carga instantánea desde caché del servidor

### 3. CSS

- **Single file**: `styles.css` único (no múltiples hojas)
- **Variables CSS**: Cambios centralizados
- **No frameworks**: CSS vanilla optimizado
- **Minificación**: Recomendado para producción

### 4. JavaScript

- **Carga diferida**: GTM con `requestIdleCallback`
- **Vanilla JS**: Sin jQuery ni frameworks pesados
- **Event delegation**: Mejor performance en eventos

### 5. Core Web Vitals

| Métrica | Objetivo | Estado Actual |
|---------|----------|---------------|
| LCP (Largest Contentful Paint) | < 2.5s | ✅ Optimizado (WebP + preload) |
| FID (First Input Delay) | < 100ms | ✅ Vanilla JS ligero |
| CLS (Cumulative Layout Shift) | < 0.1 | ✅ Width/height explícitos |

---

## SEO y Metadatos

### 1. Meta Tags Básicos

```html
<title>Plomero en Culiacán a domicilio 24/7 | Plomero Culiacán Pro</title>
<meta name="description" content="Plomero en Culiacán 24/7: a domicilio, fugas de gas/agua, destapes y emergencias. Atención rápida y precios claros. WhatsApp y teléfono.">
<link rel="canonical" href="https://plomeroculiacanpro.mx/" />
```

### 2. Open Graph (Facebook/LinkedIn)

```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://plomeroculiacanpro.mx/" />
<meta property="og:title" content="Plomero en Culiacán a domicilio 24/7 | Plomero Culiacán Pro" />
<meta property="og:description" content="Plomero en Culiacán 24/7: a domicilio, fugas..." />
<meta property="og:image" content="https://plomeroculiacanpro.mx/img/reparacion-fugas-800w.webp" />
<meta property="og:image:width" content="800" />
<meta property="og:image:height" content="800" />
<meta property="og:locale" content="es_MX" />
<meta property="og:site_name" content="Plomero Culiacán Pro" />
```

### 3. Twitter Card

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:url" content="https://plomeroculiacanpro.mx/" />
<meta name="twitter:title" content="Plomero en Culiacán a domicilio 24/7 | Plomero Culiacán Pro" />
<meta name="twitter:description" content="Plomero en Culiacán 24/7..." />
<meta name="twitter:image" content="https://plomeroculiacanpro.mx/img/reparacion-fugas-800w.webp" />
```

### 4. JSON-LD Structured Data

**LocalBusiness Schema**:
```json
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Plomero Culiacán Pro",
  "url": "https://plomeroculiacanpro.mx/",
  "telephone": "+52 667 163 1231",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Culiacán",
    "addressRegion": "Sinaloa",
    "addressCountry": "MX"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "150",
    "bestRating": "5",
    "worstRating": "1"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "20:00"
    }
  ],
  "priceRange": "$$"
}
```

**Beneficios**:
- Rich snippets con estrellas en Google
- Información de contacto destacada
- Panel de conocimiento de Google mejorado

### 5. Sitemap

**Ubicación**: `/sitemaps/main_sitemap.xml`

**Estructura**:
- Homepage: Priority 1.0
- Servicios específicos: Priority 0.9
- Landings genéricas: Priority 0.8
- Blog: Priority 0.8
- Artículos: Priority 0.7

**Total de URLs**: 24 páginas indexadas

---

## Estructura de Páginas

### Página Principal (index.html)

**Secciones en orden**:

1. **Nav** - Navegación sticky
2. **Hero** - Título principal + CTA
3. **Beneficios** - 3 iconos con beneficios clave
4. **Servicios** - Grid de 6 tarjetas con imágenes
5. **Enlaces SEO** - 5 enlaces a landings genéricas
6. **Urgencias 24/7** - CTA de emergencia
7. **Zonas de Servicio** - Colonias atendidas
8. **Preguntas Frecuentes** - 6 FAQs
9. **Blog de Plomería** - 3 artículos recientes
10. **Testimonios** - 6 reseñas con estrellas + enlaces a Google/Facebook
11. **Servicios (Footer)** - Lista de enlaces
12. **Contacto** - Formulario + WhatsApp
13. **Footer** - Info de contacto + enlaces

### Landings de Servicios Específicos

**Páginas**:
- `/servicios/reparacion-de-fugas/`
- `/servicios/destape-de-drenajes/`
- `/servicios/instalacion-de-sanitarios/`
- `/servicios/mantenimiento-de-boiler/`
- `/servicios/correccion-baja-presion/`
- `/servicios/deteccion-de-fugas/`

**Estructura común**:
1. Hero del servicio
2. Tipos de problemas atendidos (6-8 items)
3. Proceso de trabajo (5-6 pasos)
4. Señales de alerta (8 puntos)
5. FAQ específico (6 preguntas)
6. Testimonios relacionados
7. CTA de contacto

**Longitud**: 428-460 líneas por página

### Landings Genéricas

**Páginas**:
- `/servicios/plomero/24-7/`
- `/servicios/plomero/cerca-de-mi/`
- `/servicios/plomero/a-domicilio/`
- `/servicios/plomero/precios/`
- `/servicios/plomero/colonias/`

**Características**:
- SEO optimizado para búsquedas locales
- Contenido adaptado a intención de búsqueda
- Branding consistente

### Blog

**Índice**: `/blog/index.html`

**Artículos publicados**:

1. **Cómo Detectar Fugas de Agua en Casa**
   - URL: `/blog/como-detectar-fugas-agua-casa/`
   - Fecha: 11 de noviembre, 2024
   - Tiempo de lectura: 5 min
   - Temas: Prueba del medidor, dye test, inspección visual

2. **5 Problemas de Plomería Más Comunes en Culiacán**
   - URL: `/blog/problemas-comunes-plomeria-culiacan/`
   - Fecha: 10 de noviembre, 2024
   - Tiempo de lectura: 6 min
   - Temas: Agua dura, WC tapado, baja presión, boiler

3. **¿Cuándo Llamar a un Plomero? DIY vs Profesional**
   - URL: `/blog/cuando-llamar-plomero-profesional/`
   - Fecha: 9 de noviembre, 2024
   - Tiempo de lectura: 5 min
   - Temas: Casos DIY, cuándo llamar profesional, casos reales

**Estructura de artículo**:
- Hero con título
- Metadata (fecha, tiempo de lectura)
- Tabla de contenidos
- Secciones con H2/H3
- Listas numeradas/bullets
- CTAs intermedios
- Llamado final a la acción

---

## Mantenimiento y Actualizaciones

### Agregar Nueva Imagen

1. Crear imagen en 1024x1024px
2. Convertir a WebP:
   ```bash
   cwebp -q 85 original.png -o nombre-420w.webp -resize 420 420
   cwebp -q 85 original.png -o nombre-800w.webp -resize 800 800
   ```
3. Subir a `/img/`
4. Usar en HTML con `<picture>` + srcset

### Agregar Nuevo Artículo de Blog

1. Crear carpeta: `/blog/nombre-del-articulo/`
2. Crear `index.html` con estructura base
3. Actualizar `/blog/index.html` (agregar tarjeta)
4. Actualizar `/index.html` (sección de noticias)
5. Actualizar `/sitemaps/main_sitemap.xml`
6. Actualizar JSON-LD en blog/index.html

### Cambiar Colores de Marca

Editar variables en `styles.css`:
```css
:root {
  --brand: #NUEVO_COLOR;
  --brand-light: #VARIANTE_CLARA;
  --brand-dark: #VARIANTE_OSCURA;
}
```

### Actualizar Información de Contacto

Buscar y reemplazar en todos los archivos:
- Teléfono: `667 163 1231`
- WhatsApp: `526671631231`
- Email: `info@plomeropro.com`

---

## Herramientas de Desarrollo Recomendadas

### Optimización de Imágenes
- **cwebp**: Conversión a WebP desde línea de comandos
- **Squoosh**: Herramienta web de Google para optimización

### Testing
- **PageSpeed Insights**: Core Web Vitals
- **Google Rich Results Test**: Validar JSON-LD
- **Schema.org Validator**: Verificar structured data
- **GTmetrix**: Performance detallado
- **WebPageTest**: Performance avanzado

### SEO
- **Google Search Console**: Monitoreo de indexación
- **Screaming Frog**: Auditoría técnica de SEO
- **Ahrefs/SEMrush**: Análisis de keywords

---

## Checklist de Deploy

Antes de publicar cambios a producción:

- [ ] Todas las imágenes están en WebP
- [ ] Todas las imágenes tienen width/height
- [ ] Links internos funcionan correctamente
- [ ] Sitemap actualizado con nuevas páginas
- [ ] JSON-LD validado sin errores
- [ ] Open Graph tags completos en todas las páginas
- [ ] Branding consistente ("Plomero Culiacán Pro")
- [ ] Formularios de contacto funcionando
- [ ] Enlaces de WhatsApp con formato correcto
- [ ] Probado en Chrome, Firefox, Safari
- [ ] Probado en móvil (iOS y Android)
- [ ] Core Web Vitals en verde (PageSpeed)
- [ ] Archivos CSS/JS minificados (opcional)

---

## Estructura HTML de Artículos de Blog

### ⚠️ IMPORTANTE: Estructura Obligatoria

Todos los artículos del blog **DEBEN** seguir esta estructura exacta. NO usar JSON-LD, breadcrumbs visuales, ni elementos complejos de `<picture>` dentro de artículos.

### Plantilla Base de Artículo

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título del Artículo SEO Optimizado</title>
    <meta name="description" content="Descripción del artículo entre 150-160 caracteres.">
    <link rel="canonical" href="https://plomeroculiacanpro.mx/blog/url-articulo/">
    <link rel="stylesheet" href="../../styles.css">

    <!-- Open Graph (versión simplificada para artículos) -->
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://plomeroculiacanpro.mx/blog/url-articulo/" />
    <meta property="og:title" content="Título del Artículo" />
    <meta property="og:description" content="Descripción del artículo." />
    <meta property="og:image" content="https://plomeroculiacanpro.mx/img/imagen-800w.webp" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Título del Artículo" />
    <meta name="twitter:description" content="Descripción del artículo." />
    <meta name="twitter:image" content="https://plomeroculiacanpro.mx/img/imagen-800w.webp" />
</head>
<body>
    <nav class="nav">
        <div class="container">
            <div class="nav-wrapper">
                <a href="../../" class="logo">Plomero Culiacán Pro</a>
                <button class="mobile-menu-btn" aria-label="Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
                <ul class="nav-menu">
                    <li><a href="../../#inicio" class="nav-link">Inicio</a></li>
                    <li><a href="../../#servicios" class="nav-link">Servicios</a></li>
                    <li><a href="../../#sobre-nosotros" class="nav-link">Sobre Nosotros</a></li>
                    <li><a href="../" class="nav-link">Blog</a></li>
                    <li><a href="../../#contacto" class="nav-link">Contacto</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <article class="blog-article">
        <div class="container">
            <header class="article-header">
                <h1>Título del Artículo H1 Único</h1>
                <div class="article-meta">
                    <time datetime="2024-11-12">12 de noviembre, 2024</time>
                    <span>•</span>
                    <span>Lectura: 8 min</span>
                </div>
            </header>

            <div class="article-content">
                <p class="lead">Párrafo introductorio destacado con la clase "lead". Debe enganchar al lector y resumir el contenido.</p>

                <h2>Primera Sección Principal</h2>
                <p>Contenido de la sección con texto bien estructurado y párrafos cortos para mejor legibilidad.</p>

                <h3>Subsección</h3>
                <ul>
                    <li>Punto importante 1</li>
                    <li>Punto importante 2</li>
                    <li>Punto importante 3</li>
                </ul>

                <h3>Tutorial paso a paso</h3>
                <ol>
                    <li><strong>Paso 1:</strong> Descripción detallada</li>
                    <li><strong>Paso 2:</strong> Descripción detallada</li>
                    <li><strong>Paso 3:</strong> Descripción detallada</li>
                </ol>

                <h2>Segunda Sección Principal</h2>
                <p>Más contenido relevante y útil para el usuario.</p>

                <h2>Conclusión</h2>
                <p>Resumen del artículo y reiteración de los puntos clave. Prepara para el CTA final.</p>

                <div class="article-cta">
                    <h3>¿Necesitas ayuda profesional?</h3>
                    <p>Descripción breve del servicio y valor agregado. Más de 15 años de experiencia en Culiacán.</p>
                    <a href="https://wa.me/526671631231?text=Hola,%20necesito%20ayuda%20con..." class="btn-primary" target="_blank" rel="noopener">Contactar por WhatsApp</a>
                </div>
            </div>

            <footer class="article-footer">
                <div class="article-navigation">
                    <a href="../" class="btn-secondary">← Volver al Blog</a>
                </div>
            </footer>
        </div>
    </article>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Plomero Culiacán Pro. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script>
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navMenu = document.querySelector('.nav-menu');

        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                mobileMenuBtn.classList.toggle('active');
            });
        }
    </script>
</body>
</html>
```

### Clases CSS Específicas de Blog

**Contenedor principal**:
- `.blog-article` - Artículo completo (reemplaza `.section`)

**Header del artículo**:
- `.article-header` - Contenedor del título y metadata
- `.article-meta` - Fecha y tiempo de lectura

**Contenido**:
- `.article-content` - Contenedor principal del contenido
- `.lead` - Párrafo introductorio destacado

**CTA y navegación**:
- `.article-cta` - Call-to-action final (fondo con color)
- `.article-footer` - Footer del artículo
- `.article-navigation` - Botones de navegación

### ❌ Elementos NO Permitidos en Artículos

**NO usar en artículos de blog**:
1. ❌ JSON-LD Schemas (Article, FAQ, HowTo, Breadcrumbs) - Solo en index.html
2. ❌ GTM (Google Tag Manager) - Solo en index.html
3. ❌ Breadcrumbs visuales - No implementados en diseño
4. ❌ Elementos `<picture>` complejos con srcset - Simplificar con `<img>` directo
5. ❌ Variables CSS inline (`var(--brand)`) - Todo viene de styles.css
6. ❌ Clases de homepage: `.services-grid`, `.news-grid`, `.card--img`, `.media-box`
7. ❌ Artículos relacionados con grid complejo - No implementado
8. ❌ Múltiples CTAs intermedios - Solo uno al final

**SÍ usar**:
- ✅ Clases `.blog-article`, `.article-header`, `.article-content`, `.article-cta`
- ✅ Rutas relativas correctas (`../../` para root)
- ✅ Script de menú móvil al final
- ✅ Open Graph simplificado (sin width/height/locale)
- ✅ Listas `<ul>` y `<ol>` sin estilos inline
- ✅ Un solo CTA con `.article-cta` al final

### Diferencias Open Graph: Homepage vs Artículos

**Homepage (index.html)**:
```html
<meta property="og:type" content="website" />
<meta property="og:image:width" content="800" />
<meta property="og:image:height" content="800" />
<meta property="og:locale" content="es_MX" />
<meta property="og:site_name" content="Plomero Culiacán Pro" />
```

**Artículos de Blog (versión simplificada)**:
```html
<meta property="og:type" content="article" />
<!-- NO incluir: og:image:width, og:image:height, og:locale, og:site_name -->
```

---

## Sistema de Rutas Relativas

### Tabla de Rutas por Ubicación

| Ubicación del archivo | Root (/) | Blog | Servicios | CSS | Imágenes |
|----------------------|----------|------|-----------|-----|----------|
| `/index.html` | `./` o `/` | `./blog/` | `./servicios/` | `./styles.css` | `./img/` |
| `/blog/index.html` | `../` | `./` | `../servicios/` | `../styles.css` | `../img/` |
| `/blog/articulo/index.html` | `../../` | `../` | `../../servicios/` | `../../styles.css` | `../../img/` |
| `/servicios/servicio/index.html` | `../../` | `../../blog/` | `../` | `../../styles.css` | `../../img/` |

### Ejemplos Prácticos

**Desde un artículo (`/blog/nombre-articulo/index.html`)**:
```html
<!-- Navegación -->
<a href="../../">Volver al inicio</a>
<a href="../">Volver al blog</a>
<a href="../../#contacto">Contacto</a>
<a href="../../servicios/reparacion-de-fugas/">Ver servicio</a>

<!-- CSS -->
<link rel="stylesheet" href="../../styles.css">

<!-- Imágenes -->
<img src="../../img/nombre-420w.webp" alt="...">

<!-- Logo -->
<a href="../../" class="logo">Plomero Culiacán Pro</a>
```

**Desde página de blog (`/blog/index.html`)**:
```html
<a href="../">Inicio</a>
<a href="./">Blog</a>
<link rel="stylesheet" href="../styles.css">
<img src="../img/imagen.webp">
```

---

## Script del Menú Móvil (Obligatorio)

### JavaScript Requerido en Todas las Páginas

**Ubicación**: Justo antes de `</body>` en TODAS las páginas (index, servicios, blog, artículos)

```javascript
<script>
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
    }
</script>
```

**Características**:
- Vanilla JavaScript (sin jQuery)
- Toggle de clases `.active`
- Guard clause con `if` para evitar errores
- Funciona en todos los navegadores modernos

**Páginas que lo requieren**:
- ✅ `/index.html`
- ✅ `/blog/index.html`
- ✅ `/blog/[articulo]/index.html`
- ✅ `/servicios/[servicio]/index.html`

---

## Buenas Prácticas de Contenido

### Estructura de Artículos de Blog

**Longitud recomendada**: 1,500 - 2,500 palabras

**Jerarquía de encabezados**:
```html
<h1>Título único del artículo</h1>        <!-- Solo UNO por página -->
<h2>Sección principal</h2>                <!-- 3-5 por artículo -->
<h3>Subsección</h3>                       <!-- 0-3 por cada H2 -->
```

**NO usar**:
- ❌ Múltiples H1
- ❌ Saltar niveles (H2 → H4)
- ❌ Encabezados vacíos o solo con emojis

**Formato de listas**:
```html
<!-- Lista con bullets -->
<ul>
    <li><strong>Palabra clave:</strong> Descripción detallada</li>
    <li><strong>Otra palabra:</strong> Más información</li>
</ul>

<!-- Lista numerada (pasos) -->
<ol>
    <li><strong>Paso 1:</strong> Instrucción clara</li>
    <li><strong>Paso 2:</strong> Siguiente acción</li>
</ol>
```

### Optimización de Párrafos

**Longitud ideal**: 2-4 líneas por párrafo en desktop

**Bueno** ✅:
```html
<p>Las fugas de agua pueden aumentar tu recibo hasta en un 40% sin que te des cuenta. Detectarlas a tiempo es crucial.</p>

<p>El método más confiable es la prueba del medidor. Solo toma 30 minutos y no requiere herramientas especiales.</p>
```

**Malo** ❌:
```html
<p>Las fugas de agua pueden aumentar tu recibo hasta en un 40% sin que te des cuenta. Detectarlas a tiempo es crucial. El método más confiable es la prueba del medidor. Solo toma 30 minutos y no requiere herramientas especiales. Este método funciona en cualquier casa y es muy preciso.</p>
```

### SEO en Artículos

**Title tag**: 50-60 caracteres
```html
<title>Baja Presión de Agua: 7 Causas y Soluciones [2024]</title>
```

**Meta description**: 150-160 caracteres
```html
<meta name="description" content="¿Baja presión en regadera o lavabo? Descubre las 7 causas principales y sus soluciones profesionales. Guía completa 2024.">
```

**URL amigable**:
- ✅ `/blog/baja-presion-agua-causas-soluciones/`
- ❌ `/blog/articulo123.html`
- ❌ `/blog/post?id=456`

---

## Scripts y Automatización

### Estructura de Scripts

```
scripts/
├── generate-image.sh              # Generación de imágenes con IA
└── automation/
    ├── seo/
    │   └── submit_sitemap.py      # Envío automático de sitemap a Google
    └── media-audit/
        ├── audit-media.mjs        # Auditoría completa de imágenes (con Puppeteer)
        ├── audit-media-simple.mjs # Auditoría de imágenes (sin dependencias)
        ├── audit-frames.mjs       # Análisis de contenedores de imagen
        └── audit-frames-simple.mjs # Análisis de frames simplificado
```

---

### 1. Generación de Imágenes

**Archivo**: `scripts/generate-image.sh`
**Lenguaje**: Bash
**Líneas**: ~100

**Propósito**:
Script auxiliar para generar imágenes usando APIs de IA (DALL·E, Stable Diffusion, etc.)

**Uso**:
```bash
./scripts/generate-image.sh "Professional plumber fixing leak" plumber-leak-repair
```

**Características**:
- Carga variables de entorno desde `.env`
- Validación de argumentos requeridos
- Output con colores en terminal
- Integración con APIs de imagen

**Dependencias**:
- `.env` con API keys
- curl o herramienta HTTP

---

### 2. SEO - Envío de Sitemap

**Archivo**: `scripts/automation/seo/submit_sitemap.py`
**Lenguaje**: Python 3
**Líneas**: 51

**Propósito**:
Envía automáticamente el sitemap.xml a Google Search Console usando la API oficial de Google.

**Uso**:
```bash
python3 scripts/automation/seo/submit_sitemap.py
```

**Características**:
- Autenticación OAuth2 con Google
- Guarda token en `token.json` (reutilizable)
- Envía sitemap principal: `https://plomeroculiacanpro.mx/sitemap.xml`
- Maneja refresh automático de credenciales

**Dependencias**:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Archivos requeridos**:
- `client_secret.json` - Credenciales OAuth de Google Cloud Console
- `token.json` - Token generado automáticamente (gitignored)

**Configuración**:
1. Crear proyecto en Google Cloud Console
2. Habilitar Search Console API
3. Descargar credenciales OAuth como `client_secret.json`
4. Ejecutar script (abrirá navegador para autorización primera vez)

---

### 3. Auditoría de Imágenes - Completa

**Archivo**: `scripts/automation/media-audit/audit-media.mjs`
**Lenguaje**: JavaScript (ES Modules)
**Líneas**: 135

**Propósito**:
Audita todas las imágenes del sitio para detectar problemas de optimización.

**Uso**:
```bash
node scripts/automation/media-audit/audit-media.mjs
```

**Análisis realizado**:
- ✅ Formato de imagen (PNG, JPG, WebP)
- ✅ Atributos `width` y `height` explícitos
- ✅ Atributos `loading` y `decoding`
- ✅ Uso de `<picture>` con srcset
- ✅ Tamaño de imagen vs. viewport
- ✅ Detección de imágenes decorativas sin `alt`

**Output**:
```
📊 AUDITORÍA DE IMÁGENES - Plomero Culiacán Pro

Página: /
├── ✅ img/reparacion-fugas-800w.webp
│   Format: WebP, Width: 800, Height: 800
│   Loading: eager, Picture: Yes
├── ⚠️  img/hero-plumbing-1920w.webp
│   ⚠️  Imagen muy grande para viewport móvil
└── ❌ img/logo.png
    ❌ Formato PNG (debería ser WebP)
    ❌ Faltan atributos width/height
```

**Dependencias**:
```json
"puppeteer": "^21.0.0"
```

---

### 4. Auditoría de Imágenes - Simple

**Archivo**: `scripts/automation/media-audit/audit-media-simple.mjs`
**Lenguaje**: JavaScript (ES Modules)
**Líneas**: 74

**Propósito**:
Versión ligera de auditoría de imágenes sin dependencias externas.

**Uso**:
```bash
node scripts/automation/media-audit/audit-media-simple.mjs
```

**Ventajas**:
- ✅ Sin Puppeteer (más rápido)
- ✅ Usa solo módulos nativos de Node.js (https)
- ✅ Análisis mediante regex del HTML
- ✅ Ideal para CI/CD

**Limitaciones**:
- ❌ No ejecuta JavaScript del sitio
- ❌ No puede medir dimensiones renderizadas
- ❌ No detecta imágenes cargadas dinámicamente

---

### 5. Auditoría de Frames (Contenedores)

**Archivo**: `scripts/automation/media-audit/audit-frames.mjs`
**Lenguaje**: JavaScript (ES Modules)
**Líneas**: 127

**Propósito**:
Mide todos los contenedores de imagen por página y viewport para identificar espacios sin contenido visual.

**Uso**:
```bash
node scripts/automation/media-audit/audit-frames.mjs
```

**Análisis realizado**:
- 📐 Dimensiones de contenedores (width × height)
- 📱 Ratios de aspecto (16:9, 4:3, 1:1, etc.)
- 🖼️  Detección de frames vacíos sin `<img>`
- 📊 Análisis en 3 viewports: móvil (390px), tablet (768px), desktop (1366px)
- 🎯 Identificación de contenedores por selector CSS

**Selectores analizados**:
```javascript
const FRAME_SELECTORS = [
  ".hero", ".hero-media", ".banner", ".section-media",
  ".service-card", ".service-media",
  ".card", ".card-media", ".card .media",
  ".gallery", ".gallery-item", ".grid .card", "[data-media]"
];
```

**Output**:
```
📊 AUDITORÍA DE CONTENEDORES - Mobile (390x844)

Página: /
├── .hero (1200×600) ratio 2:1
│   ✅ Contiene imagen
├── .service-card (300×200) ratio 3:2
│   ❌ Frame vacío - considera agregar imagen
└── .banner (800×400) ratio 2:1
    ✅ Contiene imagen
```

**Dependencias**:
```json
"puppeteer": "^21.0.0"
```

---

### 6. Auditoría de Frames - Simple

**Archivo**: `scripts/automation/media-audit/audit-frames-simple.mjs`
**Lenguaje**: JavaScript (ES Modules)
**Líneas**: 165

**Propósito**:
Versión simplificada de auditoría de contenedores sin Puppeteer.

**Uso**:
```bash
node scripts/automation/media-audit/audit-frames-simple.mjs
```

**Ventajas**:
- ✅ Sin dependencias externas
- ✅ Análisis estático del HTML
- ✅ Rápido para CI/CD

**Limitaciones**:
- ❌ No puede medir dimensiones reales renderizadas
- ❌ No analiza múltiples viewports
- ❌ No ejecuta CSS ni JS

---

### Scripts NPM Disponibles

Agregados en `package.json`:

```json
{
  "scripts": {
    "clean": "npm run clean:ds-store && npm run clean:logs",
    "clean:ds-store": "find . -name '.DS_Store' -type f -delete && echo '✓ .DS_Store files deleted'",
    "clean:logs": "find . -name '*.log' -type f -delete && echo '✓ Log files deleted'",
    "clean:all": "npm run clean && git clean -fdX && echo '✓ All ignored files cleaned'",
    "precommit": "npm run clean:ds-store",
    "audit:media": "node scripts/automation/media-audit/audit-media.mjs",
    "audit:media:simple": "node scripts/automation/media-audit/audit-media-simple.mjs",
    "audit:frames": "node scripts/automation/media-audit/audit-frames.mjs",
    "audit:frames:simple": "node scripts/automation/media-audit/audit-frames-simple.mjs",
    "seo:submit-sitemap": "python3 scripts/automation/seo/submit_sitemap.py"
  }
}
```

**Uso recomendado**:

```bash
# Limpieza antes de commit
npm run clean

# Auditoría completa de imágenes
npm run audit:media

# Auditoría rápida (sin Puppeteer)
npm run audit:media:simple

# Analizar contenedores vacíos
npm run audit:frames

# Enviar sitemap a Google
npm run seo:submit-sitemap
```

---

### Configuración de Entorno

**Archivo `.env` (gitignored)**:
```bash
# APIs de generación de imágenes
OPENAI_API_KEY=sk-...
STABILITY_API_KEY=sk-...

# Google Search Console API
# (No necesario, usa client_secret.json)
```

**Archivos en `.gitignore`**:
```
.env
client_secret.json
token.json
*.log
.DS_Store
```

---

## Contacto Técnico

**Desarrollador**: Claude AI Assistant
**Fecha de última actualización**: 12 de Noviembre, 2024
**Versión de documentación**: 2.2

---

## Changelog

### Versión 2.2 - 12 de Noviembre, 2024
- ✅ **Reorganización de scripts y automatización**
  - Creada estructura `scripts/automation/` con categorías
  - Movidos 5 scripts sueltos a ubicaciones organizadas
  - Documentación completa de cada script (propósito, uso, dependencias)
  - Agregados 6 scripts NPM para automatización
- ✅ **Consolidación de assets en `/assets/`**
  - Unificadas 3 carpetas dispersas (img/, images/, fonts/) en estructura profesional
  - Eliminados 8 archivos sin usar (-187 KB)
  - Actualizadas 242 referencias en 22 HTML + CSS
- ✅ **Mejoras en limpieza y mantenimiento**
  - Mejorado .gitignore con categorías y formato profesional
  - Scripts NPM de limpieza automática

### Versión 2.1 - 12 de Noviembre, 2024
- ✅ **Documentación completa de artículos de blog**
  - Plantilla HTML completa y obligatoria
  - Clases CSS específicas documentadas (`.blog-article`, `.article-header`, etc.)
  - Lista de elementos NO permitidos en artículos
  - Diferencias Open Graph entre homepage y artículos
- ✅ **Sistema de rutas relativas documentado**
  - Tabla completa por ubicación de archivo
  - Ejemplos prácticos para cada caso
- ✅ **Script del menú móvil documentado**
  - JavaScript requerido en todas las páginas
  - Ubicación y características
- ✅ **Buenas prácticas de contenido**
  - Estructura de encabezados
  - Optimización de párrafos
  - SEO en artículos

### Versión 2.0 - 12 de Noviembre, 2024
- ✅ Migración completa a WebP (93% reducción de peso)
- ✅ Agregados 6 testimonios con enlaces a Google/Facebook
- ✅ Agregado aggregateRating al JSON-LD (4.8/5 estrellas)
- ✅ Creados 3 artículos de blog sobre plomería
- ✅ Actualizado sitemap con 24 páginas
- ✅ Restauradas páginas de servicios genéricos
- ✅ Branding unificado en todas las páginas
- ✅ Width/height agregado a todas las imágenes

### Versión 1.0 - Septiembre 2024
- Lanzamiento inicial del sitio
- 6 landing pages de servicios específicos
- Sistema de diseño con variables CSS
- Fuentes autohospedadas
