# GUÍA DE IMPLEMENTACIÓN - ACCIONES ESPECÍFICAS
## Plomero Culiacán Pro - SEO Colonias

---

## ACCION 1: CREAR FAQ DIFERENCIADAS POR COLONIA
**Prioridad:** CRÍTICA (Semana 1-2)
**Impacto:** +20-25% relevancia local
**Esfuerzo:** 8-10 horas
**ROI:** MUY ALTO

### PROBLEMA
Todas las colonias tienen EXACTAMENTE las mismas 8 preguntas FAQ:
1. "¿Cuánto tarda el plomero en llegar a [Colonia]?"
2. "¿Cuánto cuesta el servicio en [Colonia]?"
3. "¿Conocen los sistemas específicos de [Colonia]?"
4. "¿Atienden emergencias de madrugada en [Colonia]?"
5. "¿Qué garantía ofrecen en los trabajos?"
6. "¿Dan factura electrónica?"
7. "¿Cuáles son los problemas de plomería más comunes?"
8. "¿Necesito estar presente durante el servicio?"

**Google detecta duplicidad** = Penalización potencial

### SOLUCIÓN

#### CLASIFICAR COLONIAS POR TIPO
```
TIPO 1: PREMIUM/LUJO (Las Quintas, Jardines Humaya, Aeropuerto, etc.)
TIPO 2: RESIDENCIAL ESTABLECIDO (Bosques Humaya, Colinas Humaya, etc.)
TIPO 3: COMERCIAL/MIXTA (Ferrocarrilera, Centro, etc.)
TIPO 4: RESIDENCIAL NUEVA (Infonavit, Cañadas, etc.)
```

#### CREAR FAQ TEMPLATES DIFERENCIADOS

**TIPO 1: PREMIUM/LUJO**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Cómo accedo a [Colonia] siendo fraccionamiento cerrado?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Conocemos perfectamente los protocolos de seguridad de [Colonia]. 
        Nos identificamos en las casetas con placas profesionales, credencial 
        y documentación de la llamada. Los residentes nos reconocen por años 
        de servicio confiable. Llegamos con discreción y profesionalismo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Conocen sistemas hydroneumáticos y de alta presión?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, especialistas en sistemas de alta gama de [Colonia]. 
        Conocemos tanques hydroneumáticos marca Amtrol/Flexcon, boilers 
        de paso Rinnai y Noritz, grifería Grohe/Hansgrohe y sistemas 
        de múltiples baños. Mantenemos capacitación en marcas premium."
      }
    },
    {
      "@type": "Question",
      "name": "¿Pueden reparar grifería importada de lujo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, experiencia con Grohe, Hansgrohe, Kohler, Moen, Delta. 
        Contamos con refacciones importadas y técnica especializada. 
        Muchos residentes de [Colonia] confían en nosotros para sus 
        instalaciones de lujo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Respetan la privacidad en fraccionamiento exclusivo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Absoluto. Trabajamos con discreción total, respeto a los horarios 
        y espacios privados. No compartimos información de residentes. 
        Somos plomeros de confianza para residencias de lujo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuáles son los problemas más frecuentes en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "En [Colonia] atendemos principalmente: fugas en sistemas 
        de tubería oculta (muros de acabado premium), problemas con 
        boilers importados, reparación de válvulas cartucho en grifería 
        de lujo, mantenimiento de sistemas hydroneumáticos y drenajes 
        en construcciones complejas de múltiples niveles."
      }
    },
    {
      "@type": "Question",
      "name": "¿Qué experiencia tienen específicamente en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Más de 10 años trabajando en [Colonia]. Hemos atendido decenas 
        de residencias en el fraccionamiento, conocemos los constructores 
        de la zona y los sistemas típicos de cada desarrollador. Somos 
        plomeros de referencia entre vecinos."
      }
    },
    {
      "@type": "Question",
      "name": "¿Garantizan el trabajo en instalaciones premium?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, garantía escrita de 6 meses en mano de obra y materiales 
        (si son originales). En [Colonia] trabajamos con las exigencias 
        más altas de calidad y respaldamos cada proyecto."
      }
    },
    {
      "@type": "Question",
      "name": "¿Pueden hacer trabajos grandes sin afectar el lugar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, especialistas en proyectos complejos en [Colonia]. 
        Trabajamos con protección de pisos marmóreos, plástico en muros, 
        limpieza durante y después, y coordinación con arquitectos si es necesario."
      }
    }
  ]
}
</script>
```

**TIPO 2: RESIDENCIAL ESTABLECIDO**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Tienen experiencia con sistemas de tinaco?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, especialistas en sistemas de tinaco tradicionales que son 
        típicos de [Colonia]. Reparamos válvulas de flotador, limpiamos 
        tinacos, instalamos nuevos y mantenemos sistemas eficientes."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuál es el problema más frecuente en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El envejecimiento de tuberías de cobre (35-40 años) causa fugas 
        internas difíciles de detectar. En [Colonia], frecuentemente 
        encontramos óxido en tuberías que requiere reemplazo parcial."
      }
    },
    {
      "@type": "Question",
      "name": "¿A qué edad típicamente fallan las tuberías aquí?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Las residencias de [Colonia] tienen 35-45 años en promedio. 
        Tuberías de cobre duran 50-70 años, pero en [Colonia] vemos 
        problemas a los 35-40 años por agua con alto contenido mineral."
      }
    },
    {
      "@type": "Question",
      "name": "¿Hacen limpieza de tubería preventiva?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, ofrecemos descalcificación y limpieza de tuberías. 
        En [Colonia] es frecuente acumular sedimentos por agua dura. 
        La prevención ahorra dinero a largo plazo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Atienden problemas de baja presión común aquí?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, muy frecuente en [Colonia] por envejecimiento de sistemas. 
        Diagnosticamos, limpiamos filtros, ajustamos reguladores y 
        reemplazamos válvulas según sea necesario."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta una reparación típica en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Reparaciones típicas: fuga pequeña $600-900, destape $500-1,000, 
        cambio de WC $800-1,200, boiler $1,200-2,000. Cada caso es diferente. 
        Cotizamos sin compromiso por WhatsApp."
      }
    },
    {
      "@type": "Question",
      "name": "¿Tienen referencias de vecinos en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, cientos de vecinos satisfechos de [Colonia] que pueden 
        referenciar. Trabajamos en [Colonia] desde hace más de 10 años. 
        Pregunten en su colonia, probablemente conocen nuestro trabajo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Ofrecen mantenimiento preventivo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, revisión anual de sistema completo: boiler, tinaco, tuberías, 
        válvulas. En [Colonia] la edad de las casas hace recomendable 
        revisión preventiva anual para evitar sorpresas."
      }
    }
  ]
}
</script>
```

**TIPO 3: COMERCIAL/MIXTA**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Atienden negocios o solo residencias en [Colonia]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ambos. En [Colonia] tenemos experiencia en restaurantes, 
        consultorios, oficinas y tiendas. Conocemos exigencias comerciales 
        y códigos de salud."
      }
    },
    {
      "@type": "Question",
      "name": "¿Manejan sistemas de alta capacidad?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, sistemas hydroneumáticos, tanques de almacenamiento grandes, 
        bombas de recirculación para negocios en [Colonia]. Tenemos 
        experiencia con múltiples salidas simultáneas."
      }
    },
    {
      "@type": "Question",
      "name": "¿Pueden responder rápido en horario comercial?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, prioridad en negocios activos. En [Colonia] entendemos que 
        un problema de agua afecta ingresos. Llegamos en 15-30 minutos 
        para emergencias comerciales."
      }
    },
    {
      "@type": "Question",
      "name": "¿Hacen trabajos grandes sin afectar el negocio?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, coordinamos horarios fuera de atención. En [Colonia] hemos 
        hecho instalaciones complejas en restaurantes cerrados, planeando 
        todo previo para minimizar tiempo."
      }
    },
    {
      "@type": "Question",
      "name": "¿Tienen experiencia con filtros industriales?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, mantenimiento de sistemas de filtración para restaurantes 
        y negocios en [Colonia]. Limpieza, cambio de cartuchos y 
        calibración de presión."
      }
    },
    {
      "@type": "Question",
      "name": "¿Entienden de sistemas de agua para comercios?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, cumplimiento de normativas sanitarias COFEPRIS, sistemas 
        de recirculación para agua caliente constante, instalaciones 
        para múltiples baños en negocios de [Colonia]."
      }
    },
    {
      "@type": "Question",
      "name": "¿Ofrecen contrato de mantenimiento?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, paquetes mensuales o trimestrales para negocios en [Colonia]. 
        Revisión preventiva, prioridad en emergencias, descuentos en 
        reparaciones y materiales."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuál es la emergencia más común aquí?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Fugas en tuberías de agua caliente para restaurantes/cafeterías 
        en [Colonia], drenajes tapados por acumulación, sistemas de 
        presión inestables y problemas con boilers comerciales."
      }
    }
  ]
}
</script>
```

### IMPLEMENTACIÓN
1. Identificar clasificación de cada una de las 120 colonias
2. Asignar template apropiado
3. Personalizar referencias de la colonia específica
4. Reemplazar en HTML
5. Testing en Google Search Console

---

## ACCION 2: IMPLEMENTAR ENLAZADO INTERNO ESTRATEGICO
**Prioridad:** CRÍTICA (Semana 1-2)
**Impacto:** +15-20% autoridad
**Esfuerzo:** 6-8 horas
**ROI:** MUY ALTO

### PROBLEMA
- Cada página enlaza solo a 3-4 colonias
- 120 colonias = 95% oportunidad de enlazado perdida
- Mismo anchor text "Plomero en X" en todas
- Solo enlaces al footer

### SOLUCIÓN: CREAR MATRIZ DE ENLAZADO

#### PASO 1: Crear archivo `colonias-geolocation.json`
```json
{
  "colonias": {
    "las-quintas": {
      "nombre": "Las Quintas",
      "tipo": "premium",
      "coordenadas": [24.2805, -107.2540],
      "cercanas": [
        "tres-rios",
        "bosques-del-humaya",
        "jardines-de-humaya",
        "colinas-del-humaya",
        "altamira"
      ]
    },
    "ferrocarrilera": {
      "nombre": "Ferrocarrilera",
      "tipo": "comercial",
      "coordenadas": [24.2850, -107.3050],
      "cercanas": [
        "centro",
        "estacion-obispo",
        "tierra-blanca",
        "residencial-campestre"
      ]
    }
    // ... etc para 120 colonias
  }
}
```

#### PASO 2: Crear nueva sección en HTML
```html
<section class="seo-links" aria-labelledby="seo-links-title">
  <h2 id="seo-links-title">Servicios en Colonias Cercanas a [Colonia]</h2>
  <div class="seo-grid">
    <a class="seo-card" href="../tres-rios/">
      <span>Plomero en Tres Ríos</span>
    </a>
    <a class="seo-card" href="../bosques-del-humaya/">
      <span>Reparación de fugas Bosques Humaya</span>
    </a>
    <a class="seo-card" href="../jardines-de-humaya/">
      <span>Destape drenajes Jardines Humaya</span>
    </a>
    <a class="seo-card" href="../colinas-del-humaya/">
      <span>Servicio 24/7 Colinas Humaya</span>
    </a>
    <a class="seo-card" href="../altamira/">
      <span>Plomero certificado Altamira</span>
    </a>
  </div>
</section>
```

#### PASO 3: Variar anchor text
```
NO: "Plomero en X", "Plomero en Y", "Plomero en Z"

SÍ: 
  - "Plomero en Tres Ríos"
  - "Reparación de fugas Bosques Humaya"
  - "Destape drenajes Jardines Humaya"
  - "Emergencias 24/7 Colinas Humaya"
  - "Servicio plomería Altamira"
  - "Plomero certificado [Colonia]"
```

#### PASO 4: Agregar enlaces contextuales en cuerpo
```html
<p>En [Colonia], realizamos frecuentemente trabajos de 
<a href="../../reparacion-de-fugas/">reparación de fugas</a>. 
Si necesitas el mismo servicio en 
<a href="../bosques-del-humaya/">Bosques del Humaya</a> o 
<a href="../jardines-de-humaya/">Jardines de Humaya</a>, 
también contamos con experiencia especializada.</p>
```

---

## ACCION 3: OPTIMIZAR RENDIMIENTO
**Prioridad:** ALTA (Semana 2-3)
**Impacto:** +5-10% Core Web Vitals
**Esfuerzo:** 2-4 horas
**ROI:** ALTO

### 3.1 AGREGAR PRECONNECT TAGS (5 de 6 páginas)

**AGREGAR EN <head>:**
```html
<link rel="preconnect" href="https://www.google.com" crossorigin>
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://maps.googleapis.com" crossorigin>
<link rel="preconnect" href="https://www.gstatic.com" crossorigin>
```

**BENEFICIO:** -100-200ms en FCP

### 3.2 AGREGAR FETCHPRIORITY (5 de 6 páginas)

```html
<link rel="preload" href="../../../styles.min.css" as="style" fetchpriority="high">
<link rel="preload" href="../../../assets/fonts/inter-400.woff2" 
      as="font" type="font/woff2" crossorigin fetchpriority="high">
```

**BENEFICIO:** -50-100ms en FCP

### 3.3 INLINE CSS CRÍTICO

Crear archivo `critical-css.css` (~3-5KB):
```css
/* Critical CSS - inline */
html, body {
  margin: 0;
  padding: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
body {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}
.hero {
  padding: 40px 20px;
  background: linear-gradient(...);
}
.hero h1 {
  font-size: 2.5rem;
  font-weight: 700;
}
.btn-primary {
  display: inline-block;
  padding: 12px 24px;
  background: #0066cc;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}
/* ... más estilos críticos ... */
```

**Incluir en HTML:**
```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* Inline critical CSS */
    /* ... contenido de critical-css.css ... */
  </style>
  <link rel="stylesheet" href="styles.min.css">
</head>
```

**BENEFICIO:** -200-400ms en LCP

---

## ACCION 4: MEJORAR SOCIAL MEDIA SHARING
**Prioridad:** MEDIA (Semana 2-3)
**Impacto:** +5-10% social sharing
**Esfuerzo:** 2-3 horas
**ROI:** MEDIO

### 4.1 CREAR IMÁGENES ESPECÍFICAS POR COLONIA

Usar Canva/Photoshop para crear (dimensiones 1200x630px):
- `colonia-las-quintas-og.webp`
- `colonia-ferrocarrilera-og.webp`
- `colonia-humaya-og.webp`
- etc.

### 4.2 ACTUALIZAR OG TAGS

```html
<!-- ACTUAL (mal) -->
<meta property="og:image" 
      content="https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-800w.webp" />

<!-- MEJORADO (bien) -->
<meta property="og:image" 
      content="https://plomeroculiacanpro.mx/assets/images/og-colonias/las-quintas-og.webp" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

### 4.3 ACTUALIZAR TWITTER CARDS

```html
<!-- AGREGAR -->
<meta name="twitter:site" content="@plomerculiacan" />
<meta name="twitter:creator" content="@plomerculiacan" />
<meta name="twitter:card" content="summary_large_image" />
```

---

## ACCION 5: AGREGAR IMAGEOBJECT SCHEMAS
**Prioridad:** MEDIA (Semana 2-3)
**Impacto:** +5-8% tráfico imagen
**Esfuerzo:** 3-4 horas
**ROI:** MEDIO

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "url": "https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-800w.webp",
  "name": "Plomero reparando fuga de agua en Las Quintas",
  "description": "Servicio profesional de reparación de fugas de agua en residencia de Las Quintas, Culiacán",
  "contentUrl": "https://plomeroculiacanpro.mx/assets/images/reparacion-fugas-800w.webp",
  "encodingFormat": "image/webp",
  "height": 800,
  "width": 800,
  "author": {
    "@type": "Person",
    "name": "Plomero Culiacán Pro"
  },
  "datePublished": "2025-11-23"
}
</script>
```

**Agregar para las 6 imágenes principales por colonia**

---

## ACCION 6: AGREGAR TITLE ATTRIBUTES A IMÁGENES
**Prioridad:** BAJA (Semana 3)
**Impacto:** +1-2% UX
**Esfuerzo:** 1-2 horas
**ROI:** BAJO

```html
<!-- ACTUAL -->
<img src="..." alt="Plomero reparando fuga en Las Quintas">

<!-- MEJORADO -->
<img src="..." 
     alt="Plomero reparando fuga en Las Quintas"
     title="Reparación profesional de fugas en Las Quintas - Plomero certificado">
```

**Formato recomendado:**
```
title="[Servicio] [ubicación específica] - [diferenciador]"
```

---

## ACCION 7: EXPANDIR CONTENIDO A 4,500+ PALABRAS
**Prioridad:** MEDIA (Semana 3-4)
**Impacto:** +3-5% ranking
**Esfuerzo:** 4-6 horas por colonia
**ROI:** MEDIO-ALTO

### SECCIONES A AGREGAR:

1. **Casos de Éxito Específicos** (300-400 palabras)
```markdown
## Casos de Éxito en [Colonia]

Hace poco atendimos una fuga compleja en una residencia de [Colonia] 
donde las tuberías estaban ocultas en muros. Usando nuestro equipo 
de termografía, localizamos la fuga sin romper...
```

2. **Historia de la Colonia** (200-300 palabras)
```markdown
## Historia y Características de [Colonia]

[Colonia] fue fundada en 1980... es una zona establecida con 
residencias que promedian 35-40 años... las construcciones típicas 
tienen sistemas de tinaco...
```

3. **Problemas Frecuentes ESPECIFICOS** (300-400 palabras)
```markdown
## Problemas Específicos de [Colonia]

En [Colonia] vemos más fugas de cobre por [razón], mientras que en 
otras colonias el problema principal es [otro]. Esto se debe a...
```

4. **Instalaciones Típicas** (200-300 palabras)
```markdown
## Sistemas Típicos en [Colonia]

Las residencias de [Colonia] generalmente tienen sistemas de tinaco 
tradicional con boilers de depósito...
```

---

## CRONOGRAMA RECOMENDADO

```
SEMANA 1:
├─ Lunes-Martes: Clasificar 120 colonias por tipo (2 tipos)
├─ Miércoles: Crear FAQ templates
├─ Jueves-Viernes: Aplicar FAQ a 6 colonias piloto
└─ Testing en Search Console

SEMANA 2:
├─ Lunes: Crear JSON de geolocalización
├─ Martes-Miércoles: Agregar enlaces internos (6 colonias piloto)
├─ Jueves: Agregar preconnect tags (5 colonias)
└─ Viernes: Testing performance (Core Web Vitals)

SEMANA 3:
├─ Lunes: Agregar fetchpriority
├─ Martes-Miércoles: Inline CSS crítico
├─ Jueves: Mejorar OG/Twitter images
└─ Viernes: Agregar ImageObject schemas

SEMANA 4:
├─ Lunes-Martes: Title attributes imágenes
├─ Miércoles-Jueves: Expandir contenido
└─ Viernes: Testing final + publicación

POST-IMPLEMENTACIÓN:
├─ Semana 5-8: Monitorear Google Search Console
├─ Semana 9-12: Analizar impacto en tráfico
└─ Mes 3: Expandir a colonias restantes
```

---

## METRICAS ANTES Y DESPUES

### ANTES (Línea Base)
```
Impresiones promedio por colonia: [X]
CTR promedio: [X]%
Posición media: [X]
Core Web Vitals: 
  - LCP: [?]ms
  - FID: [?]ms
  - CLS: [?]
Conversiones/mes: [?] (llamadas + WhatsApp)
```

### DESPUES (Esperado - 60-90 días)
```
Impresiones: +10-15% esperado
CTR: +5-10% esperado
Posición media: -0.5 a -1 lugar (mejora)
Core Web Vitals:
  - LCP: <2.5s
  - FID: <100ms
  - CLS: <0.1
Conversiones: +8-12% esperado
Tráfico orgánico: +15-25% estimado
```

---

## HERRAMIENTAS NECESARIAS

**Gratuitas:**
- Google Search Console
- Google PageSpeed Insights
- Google Lighthouse
- Google Analytics

**Opcionales (pagas):**
- SEMrush ($99-500/mes) - ranking tracking
- Ahrefs ($99-999/mes) - análisis competitivo
- Screaming Frog ($99 anual) - auditoría técnica

---

## RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Duplicado de contenido detectado | MEDIA | ALTO | Testing en GSC después cambios |
| Romper URLs con cambios | BAJA | ALTO | Mantener URLs idénticas, cambiar solo contenido |
| Performance empeorar | BAJA | MEDIO | Testing con PageSpeed antes publicar |
| Conversiones bajar | MUY BAJA | ALTO | Mantener CTAs idénticos |

---

## CHECKLIST DE IMPLEMENTACION

```
FASE 1 - CONTENIDO (FAQ + Enlazado)
  ☐ Clasificar 120 colonias por tipo
  ☐ Crear FAQ templates diferenciados
  ☐ Crear JSON geolocalización
  ☐ Aplicar FAQ a 6 colonias piloto
  ☐ Agregar enlaces internos matriz
  ☐ Testing Google Search Console
  
FASE 2 - PERFORMANCE (Tags + CSS)
  ☐ Agregar preconnect tags (5 colonias)
  ☐ Agregar fetchpriority (5 colonias)
  ☐ Crear e inline CSS crítico
  ☐ Testing PageSpeed Insights
  ☐ Verificar Core Web Vitals
  
FASE 3 - SOCIAL + SCHEMAS
  ☐ Crear OG images específicas
  ☐ Mejorar Twitter cards
  ☐ Agregar ImageObject schemas
  ☐ Agregar title attributes imágenes
  ☐ Testing en redes sociales
  
FASE 4 - CONTENIDO EXPANDIDO
  ☐ Agregar casos de éxito
  ☐ Agregar historia colonia
  ☐ Expandir problemas específicos
  ☐ Agregar instalaciones típicas
  ☐ Testing legibilidad + longitud
  
POST-LAUNCH
  ☐ Monitorear GSC (días 1-7)
  ☐ Monitorear Analytics (días 1-30)
  ☐ Ajustar según datos
  ☐ Expandir a colonias restantes
```

---

## CONCLUSION

Implementar estas 7 acciones en orden debería resultar en:
- **+15-25% tráfico orgánico** en 60-90 días
- **+8-12% conversiones** (llamadas/WhatsApp)
- **+16-20 puntos SEO score** (72/100 → 88-92/100)
- **-100-400ms en Core Web Vitals**

Esfuerzo total estimado: **40-60 horas**
ROI: **MUY ALTO** (tráfico recurrente de bajo costo)

