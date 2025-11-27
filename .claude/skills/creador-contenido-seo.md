# Skill: Creador de Contenido SEO - Plomero Culiacán Pro

## Objetivo
Generar landing pages o artículos de blog listos para publicar con el mismo formato base (estructura y estilos) que `index.html`, plantillas de `servicios/` o `blog/`.

## Información del Proyecto

### Rutas
- **Proyecto:** `/Users/hectorpc/Documents/Hector Palazuelos/Google My Business/plomero culiacan pro`
- **Homepage:** `index.html`
- **Servicios:** `servicios/`
- **Blog:** `blog/`
- **Estilos:** `styles.min.css`
- **Assets:** `assets/images/`, `assets/fonts/`, `assets/icons/`

### NAP (Name, Address, Phone) - DATOS OFICIALES

**CRÍTICO:** Usar estos datos EXACTAMENTE como se muestran:

```
Nombre: Plomero Culiacán Pro
Teléfono texto: 667 392 2273
Teléfono internacional: +52 667 392 2273
WhatsApp URL: https://wa.me/526673922273
Tel URL: tel:+526673922273
Número limpio: 6673922273
Ciudad: Culiacán, Sinaloa
País: México
```

### Social Media (sameAs)
```json
"sameAs": [
  "https://www.facebook.com/plomeroculiacanpro",
  "https://www.instagram.com/plomeroculiacanpro",
  "https://twitter.com/plomeroculiacan"
]
```

## Reglas Obligatorias

### 1. NAP Consistente - USO DEL NÚMERO

**SIEMPRE usar: 6673922273**

#### En CTAs y botones:
```html
<!-- WhatsApp -->
<a href="https://wa.me/526673922273?text=Hola%2C%20necesito%20un%20plomero%20en%20Culiacán">

<!-- Teléfono -->
<a href="tel:+526673922273">

<!-- Texto visible -->
<p>WhatsApp: 52 667 392 2273</p>
<p>Teléfono: 667 392 2273</p>
```

#### En schemas JSON-LD:
```json
"telephone": "+52 667 392 2273"
```

### 2. Meta Tags SEO

#### Title Tag (≤60 caracteres)
```html
<title>[Keyword Principal] en Culiacán | Plomero Profesional 24/7</title>
```

**Ejemplos:**
- "Plomero 24 Horas Culiacán | Emergencia en 30-60 min"
- "Reparación de Fugas en Culiacán | Garantía Escrita"
- "Destapado de Drenaje Culiacán | Llegada Rápida"

#### Meta Description (120-155 caracteres)
```html
<meta name="description" content="[Keyword] en Culiacán ✓ Llegada 30-60 min ✓ [Beneficio 1] ✓ [Beneficio 2] ✓ Las Quintas, Tres Ríos, Centro ✓ WhatsApp 24/7">
```

**Ejemplos:**
- "Plomero 24 horas en Culiacán ✓ Emergencia inmediata ✓ Llegada 30-60 min ✓ Las Quintas, Tres Ríos ✓ Garantía escrita ✓ WhatsApp: 667-392-2273"
- "Reparación de fugas en Culiacán ✓ Detección con equipo profesional ✓ Presupuesto gratis ✓ Trabajo garantizado ✓ Tel: 667-392-2273"

#### Canonical URL
```html
<link rel="canonical" href="https://plomeroculiacanpro.mx/[slug]/">
```

#### Keywords (opcional, 5-8 keywords)
```html
<meta name="keywords" content="plomero culiacan, [keyword principal], [variante 1], [variante 2], [servicio especifico], [colonia principal]">
```

### 3. SEO On-Page

#### H1 - Único y con Keyword Principal
```html
<h1>[Keyword Principal] en Culiacán 24/7</h1>
```

**Ejemplos:**
- "Plomero de Emergencia en Culiacán 24/7"
- "Reparación de Fugas de Agua en Culiacán"
- "Destapado de Drenaje en Las Quintas, Culiacán"

#### H2/H3 - Subtítulos con Variantes de Keyword

**H2 principales:**
- "¿Por Qué Elegir Nuestro Servicio de [Keyword]?"
- "Servicios de [Keyword] en Culiacán"
- "Zonas de Cobertura en Culiacán"
- "Precios de [Keyword] 2025"
- "Preguntas Frecuentes sobre [Keyword]"

**H3 secundarios:**
- Beneficios individuales
- Servicios específicos
- Colonias/zonas
- FAQs

#### Bullets de Beneficios

**Usar estructura .benefit con iconos SVG:**

```html
<div class="benefit">
    <div class="benefit-icon">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="[icon path]"/>
        </svg>
    </div>
    <div class="benefit-content">
        <h3>[Título del Beneficio]</h3>
        <p>[Descripción breve 1-2 líneas]</p>
        <ul class="benefit-list">
            <li>[Detalle 1]</li>
            <li>[Detalle 2]</li>
            <li>[Detalle 3]</li>
        </ul>
    </div>
</div>
```

**Beneficios estándar a incluir:**
1. ⚡ Llegada Rápida (30-60 min)
2. 🔧 Garantía Escrita
3. 💰 Presupuesto Gratuito
4. ✅ Trabajo Certificado
5. 📞 Atención 24/7
6. 🏆 150+ Clientes Satisfechos

#### CTAs Dobles (WhatsApp + Teléfono)

**En hero:**
```html
<a href="https://wa.me/526673922273?text=Hola%2C%20necesito%20[servicio]%20en%20Culiacán"
   target="_blank"
   rel="noopener"
   class="btn-primary btn-whatsapp">
   WhatsApp 24/7
</a>
<a href="tel:+526673922273" class="btn-secondary">
   Llamar: 667-392-2273
</a>
```

**Botones flotantes:**
```html
<div class="cta-bar">
    <a href="https://wa.me/526673922273?text=Hola%2C%20necesito%20[servicio]%20en%20Culiacán"
       target="_blank"
       rel="noopener"
       class="cta-btn cta-wa"
       aria-label="WhatsApp">
        [SVG WhatsApp icon]
    </a>
    <a href="tel:+526673922273" class="cta-btn cta-tel" aria-label="Llamar">
        [SVG Phone icon]
    </a>
</div>
```

#### Zona de Servicio Local

**Colonias principales a mencionar:**
- Las Quintas
- Tres Ríos
- Centro
- Chapultepec
- Guadalupe
- Zona Dorada
- Campestre
- Montebello
- Santa Fe
- Las Palmas

**Formato recomendado:**
```html
<section class="section">
    <div class="container">
        <h2>Cobertura en Culiacán</h2>
        <p>Servicio de [keyword] en todas las zonas de Culiacán:</p>
        <ul class="zones-list">
            <li>Las Quintas (15-30 min)</li>
            <li>Tres Ríos (20-40 min)</li>
            <li>Centro (30-60 min)</li>
            [...]
        </ul>
    </div>
</section>
```

### 4. Schemas JSON-LD

#### Para Landing Pages de Servicios

**Schema @graph completo:**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://plomeroculiacanpro.mx/#website",
      "name": "Plomero Culiacán Pro",
      "url": "https://plomeroculiacanpro.mx/"
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
          "name": "[Nombre Página]",
          "item": "https://plomeroculiacanpro.mx/[slug]/"
        }
      ]
    },
    {
      "@type": "Service",
      "name": "[Nombre del Servicio]",
      "description": "[Descripción del servicio específico]",
      "provider": {
        "@type": "LocalBusiness",
        "name": "Plomero Culiacán Pro",
        "telephone": "+52 667 392 2273",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Culiacán",
          "addressRegion": "Sinaloa",
          "addressCountry": "MX"
        }
      },
      "areaServed": {
        "@type": "City",
        "name": "Culiacán",
        "addressCountry": "MX"
      },
      "availableChannel": {
        "@type": "ServiceChannel",
        "serviceUrl": "https://plomeroculiacanpro.mx/[slug]/",
        "servicePhone": {
          "@type": "ContactPoint",
          "telephone": "+52 667 392 2273",
          "contactType": "customer service",
          "availableLanguage": "es"
        }
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "[Pregunta 1]",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "[Respuesta 1 con keyword natural]"
          }
        },
        {
          "@type": "Question",
          "name": "[Pregunta 2]",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "[Respuesta 2]"
          }
        },
        {
          "@type": "Question",
          "name": "[Pregunta 3]",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "[Respuesta 3]"
          }
        }
      ]
    }
  ]
}
```

#### Para Artículos de Blog

```json
{
  "@type": "Article",
  "headline": "[Título H1]",
  "description": "[Meta description]",
  "author": {
    "@type": "Person",
    "name": "Plomero Culiacán Pro"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Plomero Culiacán Pro",
    "logo": {
      "@type": "ImageObject",
      "url": "https://plomeroculiacanpro.mx/assets/images/logo-512.png"
    }
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://plomeroculiacanpro.mx/blog/[slug]/"
  },
  "image": "https://plomeroculiacanpro.mx/assets/images/[imagen].webp"
}
```

### 5. Copy Local y Contenido

#### Tiempos de Llegada
**Usar siempre:**
- "Llegada en 30-60 minutos"
- "Atención 24/7" (para emergencias)
- "Disponibilidad inmediata"

**Por zona específica:**
- Las Quintas: 15-30 min
- Tres Ríos: 20-40 min
- Centro: 30-60 min

#### Horarios
```
Atención 24/7 para emergencias
Horario oficina: Lunes a Sábado 8:00-20:00
Domingos y festivos: Emergencias únicamente
```

#### Ejemplos de Trabajos y Precios

**Formato recomendado:**
```html
<div class="pricing-box">
    <h3>Precios Orientativos 2025</h3>
    <ul>
        <li>Visita diagnóstico: $150-300</li>
        <li>Reparación fuga simple: $400-800</li>
        <li>Cambio taza de baño: $800-1,500</li>
        <li>Destapado drenaje: $500-1,500</li>
    </ul>
    <p><small>*Precios sujetos a evaluación en sitio</small></p>
</div>
```

**IMPORTANTE:** No duplicar texto exacto de otras landings. Variar:
- Orden de beneficios
- Ejemplos de trabajos
- Testimonios/casos
- FAQs únicas para cada servicio

#### Testimonios Breves

**Formato:**
```html
<div class="testimonial-card">
    <div class="stars">★★★★★</div>
    <p>"[Testimonio breve 1-2 líneas sobre el servicio específico]"</p>
    <cite>— [Nombre], [Colonia]</cite>
</div>
```

**Ejemplos:**
- "Llegaron en 20 minutos, repararon la fuga rápido. Excelente servicio." — María G., Las Quintas
- "Muy profesionales, trabajo limpio y garantizado. Los recomiendo." — Carlos R., Tres Ríos

### 6. Estructura y Estilos

#### Mantener Classes Existentes

**NO cambiar:**
- `.hero`, `.hero-content`, `.hero-background`
- `.section`, `.section-alt`
- `.container`
- `.grid`, `.card`
- `.benefit`, `.benefit-icon`, `.benefit-content`
- `.btn-primary`, `.btn-secondary`
- `.faq`, `.faq-item`
- `.footer`, `.footer-content`
- `.cta-bar`, `.cta-btn`

#### CSS Crítico Inline

**Siempre incluir en `<head>`:**
```html
<style>
@font-face{font-family:'Inter';font-style:normal;font-weight:400;font-display:swap;src:url('/assets/fonts/inter-400.woff2') format('woff2')}
@font-face{font-family:'Montserrat';font-style:normal;font-weight:800;font-display:swap;src:url('/assets/fonts/montserrat-800.woff2') format('woff2')}
:root{--brand:#E36414;--brand-light:#F97316;--text:#0F172A;--text-light:#475569;--bg:#FFFFFF;--bg-soft:#F8FAFC;--border:#E2E8F0;--shadow:rgba(15,23,42,0.1);--gradient-brand:linear-gradient(135deg,#F97316 0%,#E36414 100%);--container-max-width:1200px;--container-gutter:24px}
[... resto del critical CSS ...]
</style>
```

#### Assets Globales

**NO modificar:**
- `styles.min.css`
- `main.js`
- Fonts en `assets/fonts/`
- Icons en `assets/icons/`

#### Imágenes

**Usar imágenes existentes:**
- `hero-plumbing-800w.webp`, `hero-plumbing-1200w.webp`
- `reparacion-fugas-420w.webp`, `reparacion-fugas-800w.webp`
- `emergencia-24-7-nocturna-800w.webp`
- `taza-de-baño-420w.webp`
- `destapandodrenaje-420w.webp`
- `tinaco-420w.webp`
- `arreglando-boiler-420w.webp`

**Alt text descriptivo:**
```html
<img src="/assets/images/reparacion-fugas-800w.webp"
     alt="Plomero profesional reparando fuga de agua en Culiacán"
     width="800"
     height="420"
     loading="lazy">
```

### 7. Entrega y Verificación

#### Formato de Respuesta

1. **Resumen breve** (3-4 líneas)
   - Keyword principal
   - Intención (informativa, transaccional, local)
   - Estructura (landing/blog)

2. **Rutas propuestas**
   ```
   Guardar en: /[tipo]/[slug]/index.html
   Ejemplo: /servicios/plomero-emergencia-culiacan/index.html
   Ejemplo: /blog/como-reparar-fuga-agua/index.html
   ```

3. **Código HTML completo**
   ```html
   <!DOCTYPE html>
   <html lang="es-MX">
   [... código listo para pegar/guardar ...]
   </html>
   ```

4. **Comandos de verificación**
   ```bash
   # Verificar keyword principal
   rg -i "keyword principal" [ruta]/index.html

   # Verificar número teléfono correcto
   rg "6673922273" [ruta]/index.html

   # Verificar canonical
   rg "canonical" [ruta]/index.html

   # Verificar schemas
   rg "@type.*Service" [ruta]/index.html
   rg "@type.*FAQPage" [ruta]/index.html
   ```

## Plantilla de Uso

Para generar contenido, el usuario debe proporcionar:

```
@creador-contenido-seo

Tema: [Servicio/Colonia/Problema específico]
Keyword principal: [keyword exacta]
Intención: [urgente/informativa/comparativa/local]
Tipo: [landing/artículo]
```

**Ejemplo:**
```
@creador-contenido-seo

Tema: Servicio de plomería de emergencia en Las Quintas
Keyword principal: plomero de emergencia las quintas
Intención: urgente + local
Tipo: landing
```

## Checklist Final

Antes de entregar el contenido, verificar:

- [ ] Número teléfono: 6673922273 en todos los CTAs
- [ ] Meta title ≤60 caracteres
- [ ] Meta description 120-155 caracteres
- [ ] Canonical URL correcto
- [ ] H1 único con keyword principal
- [ ] H2/H3 con variantes de keyword
- [ ] 4-6 beneficios con iconos SVG
- [ ] CTAs dobles (WhatsApp + teléfono) en hero y footer
- [ ] Zona de servicio con colonias
- [ ] Schema Service + FAQPage (3-5 preguntas)
- [ ] 3-5 testimonios breves
- [ ] Precios orientativos si aplica
- [ ] Imágenes con alt descriptivo
- [ ] Footer con NAP consistente
- [ ] Botones flotantes
- [ ] GTM incluido
- [ ] Critical CSS inline
- [ ] Link a styles.min.css
- [ ] Script main.js

## Notas Importantes

1. **Keyword density:** 1-2% (natural, no forzar)
2. **Longitud mínima:** 800-1200 palabras para landings, 1500-2500 para artículos
3. **Tone of voice:** Profesional, cercano, orientado a solución
4. **CTA placement:** Hero, mitad de página, footer, flotante
5. **Mobile-first:** Estructura responsive por defecto
6. **Performance:** Critical CSS inline, lazy loading de imágenes
7. **Accesibilidad:** aria-label en botones, alt en imágenes, semántica HTML5

## Ejemplos de Keywords y Estructura

### Landing de Servicio
- **Keyword:** "plomero 24 horas culiacan"
- **H1:** "Plomero 24 Horas en Culiacán | Emergencia Inmediata"
- **Estructura:** Hero + Beneficios + Servicios + Zonas + Precios + FAQs + CTA

### Landing de Colonia
- **Keyword:** "plomero las quintas culiacan"
- **H1:** "Plomero en Las Quintas, Culiacán | Llegada en 15-30 min"
- **Estructura:** Hero + Por qué elegirnos + Servicios + Testimonios locales + FAQs + CTA

### Artículo Informativo
- **Keyword:** "como detectar fugas de agua"
- **H1:** "Cómo Detectar Fugas de Agua en Casa: Guía Paso a Paso"
- **Estructura:** Intro + 7 métodos + Cuándo llamar plomero + FAQs + CTA

### Artículo de Precios
- **Keyword:** "cuanto cuesta un plomero en culiacan"
- **H1:** "¿Cuánto Cuesta un Plomero en Culiacán? Precios 2025"
- **Estructura:** Intro + Tabla precios + Factores que afectan + Consejos + FAQs + CTA
