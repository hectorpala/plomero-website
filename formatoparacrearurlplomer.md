# Formato obligatorio para crear nuevas URLs (Plomero Culiacán Pro)

Este documento es **la norma** para publicar cualquier landing o artículo dentro del dominio. Todo punto marcado como “Obligatorio” debe cumplirse al 100 %. Si alguna sección falta o se altera la jerarquía, la URL **no se aprueba para despliegue**.

---

## 1. Objetivo y alcance
- Aplica a **todas** las páginas de servicio, colonias, precios, artículos SEO y micrositios que vivan en `/servicios/`, `/blog/`, `/contacto/` u otras rutas internas.
- Su propósito es preservar: identidad visual (Inter/Montserrat), promesa de llegada 30‑60 min, cobertura por colonias de Culiacán, datos de contacto visibles y performance equivalente al homepage.

---

## 2. Principios de marca y UX
1. **Tipografía**: solo `Inter` (texto) e `Montserrat` (encabezados) desde `assets/fonts/`. Ninguna otra familia es aceptada.
2. **Paleta**: primario `#E36414`, secundarios `#C2410C`, `#0066cc`, fondos claros `#f8fafc`. No crear colores nuevos sin aprobación.
3. **Voz**: urgente, profesional, centrada en Culiacán. Debe mencionar colonias específicas (Las Quintas, Tres Ríos, Chapultepec, Centro, etc.) y tiempos de llegada.
4. **Confianza**: mínimo una mención a garantía de 6 meses, facturación SAT y soporte por WhatsApp. Uso moderado de emojis (máx. uno por bloque).

---

## 3. Plano obligatorio de la página
Sigue la secuencia exacta. Cada bloque debe ir delimitado por `<section>` (o la etiqueta semántica indicada) y encabezado correcto (`h1` único, luego `h2` → `h3`).

### 3.0 Header de Navegación (obligatorio)
Todas las páginas deben incluir el header de navegación idéntico al de la homepage (`https://plomeroculiacanpro.mx/`):

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

**Requisitos:**
- Logo debe apuntar a la raíz `/` siempre
- Enlaces de navegación deben usar `#inicio`, `#servicios`, `#sobre-nosotros`, `#contacto` (anclas dentro de la página, que si no existen redirigen a homepage)
- Enlace a Blog debe ser `/blog/` (absoluto)
- Mobile menu button con 3 `<span>` para el ícono hamburguesa
- Clases CSS: `.nav`, `.container`, `.nav-wrapper`, `.logo`, `.mobile-menu-btn`, `.nav-menu`, `.nav-link`
- `aria-label="Menu"` en el botón móvil para accesibilidad
- La estructura debe ser **idéntica** en todas las páginas del sitio (copiar exactamente de homepage)

### 3.1 Head SEO (obligatorio)
- `<title>` = `Servicio + en Culiacán | Beneficio directo`. Ej.: “Destape de drenajes en Culiacán | Llegada 30‑60 min”.
- `<meta name="description">` con urgencia + cobertura + contacto (tel/WhatsApp).
- `lang="es-MX"` en `<html>`.
- `<link rel="canonical">` hacia la URL final (sin parámetros).
- OG/Twitter replican título, descripción e imagen hero (`https://plomeroculiacanpro.mx/assets/...`).
- Preloads exactos:  
  ```html
  <link rel="preload" href="/assets/fonts/inter-400.woff2" ...>
  <link rel="preload" href="/assets/fonts/montserrat-700.woff2" ...>
  ```
  (Se rechaza cualquier preload a rutas inexistentes).

### 3.2 JSON-LD (obligatorio)
Incluir un bloque `<script type="application/ld+json">` con `@graph` que contenga:
1. `WebSite`
2. `BreadcrumbList`
3. `HomeAndConstructionBusiness` (NAP, `aggregateRating`, `priceRange`, `areaServed`, `sameAs`)
4. `Service` específico (nombre = servicio, `serviceType`, `areaServed` Culiacán, `provider` apuntando al negocio)
5. `FAQPage` si la página incluye preguntas (mín. 8).  
La ausencia de cualquiera de estos nodos se considera falla crítica.

### 3.3 Hero (obligatorio)
- `<section id="inicio" class="hero">` con estructura:
  - `h1` con keyword exacta + promesa (“Plomero 24/7 en Culiacán – Emergencias en 30‑60 min”).
  - Subtítulo describiendo síntomas y colonias.
  - Bloque de contacto textual (Tel / WhatsApp) y CTA principal (`<a class="btn-primary">`).
  - **Badge visible**: `★★★★★ 4.8/5 (150+ reseñas verificadas)`.
  - Imagen hero:
    ```html
    <picture>
      <source type="image/webp" srcset="/assets/images/...-800w.webp 800w, ...-1200w.webp 1200w">
      <img src="/assets/images/...-800w.webp"
           width="1200" height="800"
           loading="eager" fetchpriority="high"
           alt="Descripción acción + servicio + Culiacán">
    </picture>
    ```
  - Si falta cualquiera de estos elementos (imagen, badge, CTA, contacto), la página no pasa QA.

### 3.4 Bloque de beneficios (obligatorio)
- Grid 4‑5 tarjetas (`.benefits-grid .benefit`): icono, `h3`, texto de 2‑3 líneas y lista con 2 bullets.
- Debe cubrir: llegada el mismo día, precios claros, refacciones/garantía, facturación, soporte WhatsApp.

### 3.5 Sección “Nuestros servicios” (obligatorio)
- Mínimo 4 cards `<a class="card card--img">` enlazando a servicios relacionados.
- Cada card incluye `<picture>` con `srcset` WebP, `width/height`, `loading="lazy"`, `decoding="async"` y `alt` con acción + servicio + ubicación.
- Texto: título (h3), párrafo descriptivo y lista de 2 bullets.

### 3.6 CTA de emergencias (obligatorio)
- Bloque diferenciado (fondo alterno) con copy directo (“Cierra la llave…”) y botón a WhatsApp con `target="_blank"`.

### 3.7 Links SEO / interlinking (obligatorio)
- Grid `.seo-links` con al menos 5 `.seo-card` apuntando a las landings clave.
- Cada tarjeta debe tener `data-card-name`, `data-card-position` y CTA textual.

### 3.8 Zonas de servicio (obligatorio)
- Sección enumerando colonias (mín. 8 nombres) + invitación a escribir si la colonia no aparece.

### 3.9 Testimonios (obligatorio)
- Mínimo 3 testimonios con:
  - Texto de cliente
  - Nombre + colonia en `<cite>`
  - Mención de servicio realizado

### 3.10 Preguntas frecuentes (obligatorio)
- Mínimo 8 preguntas/respuestas únicas, enfocadas en tiempos, costos, cobertura, garantía y materiales.
- Deben coincidir con el JSON-LD `FAQPage`. Evita duplicar copy entre preguntas.

### 3.11 Contacto, formulario y mapa (obligatorio)
- Bloque con NAP completo: Tel, WhatsApp (link), correo, horarios, cobertura.
- Formulario idéntico al de la home: `#contact-form` con inputs `nombre`, `telefono`, `email`, `mensaje`.
- Debe incluir fallback server-side o instrucciones para captura (si no existe, anotar en ticket).
- Iframe de Google Maps con `title` y lista de colonias inmediatamente debajo.

### 3.12 Footer, mini-nav y scripts (obligatorio)
- Footer con aviso de derechos + tagline “Servicio profesional…”.
- Mini nav adicional con enlaces a Inicio, servicios clave, blog, contacto.
- Scripts:
  1. Toggle menú móvil
  2. Envío de formulario → WhatsApp
  3. CTA flotante (WhatsApp + Llamar) con `dataLayer` events
  4. Tracking de tarjetas SEO (click)
  5. Scroll Depth  
  Todos dentro de IIFEs, sin variables globales. GTM debe cargarse aun sin `requestIdleCallback` (usa fallback con `setTimeout`).

---

## 4. Estándares de imágenes y assets
| Elemento | Requisitos |
| --- | --- |
| Hero | WebP 1200×800, `fetchpriority="high"`, `loading="eager"`, `alt` = “Plomero … en Culiacán …” |
| Cards | WebP 420/800, `width`/`height`, `loading="lazy"`, `decoding="async"` |
| OG/Twitter | Ruta absoluta `https://plomeroculiacanpro.mx/assets/images/...-800w.webp` |
| Renombrado | Usa nombres semánticos (`plomero-destape-drenaje-culiacan.webp`). |
| Alt text | Formato: `Acción + servicio + ubicación`, ej. “Plomero destapando drenaje en Tres Ríos Culiacán con equipo rotativo”. |

No se aprueban páginas sin imágenes ni con rutas relativas en OG/Twitter.

---

## 5. Copywriting y SEO
1. **Keywords principales**: “plomero en Culiacán”, “servicio + Culiacán”, “plomería 24/7 Culiacán”.
2. **Secundarias**: tiempos de llegada, diagnóstico gratis, garantía 6 meses, facturación SAT, nombres de colonias.
3. **Encabezados**:  
   - 1× `h1`  
   - `h2` para cada bloque mayor (Beneficios, Servicios, Precios, FAQ, Contacto)  
   - `h3` para subtemas/testimonios/preguntas.
4. **Enlaces internos**: usar anchors descriptivos (“Ver precios completos de plomería en Culiacán”) hacia otras landings/blog.
5. **CTA**: repetir tel/WhatsApp en hero, CTA emergencia, testimonios y footer.
6. **Localización**: menciona colonias distintas en hero, beneficios, CTA y FAQs. No repetir siempre las mismas 3.

---

## 6. Performance, accesibilidad y tracking
- Nada de CSS inline extenso; define estilos en `styles.css`. Solo se permiten ajustes mínimos (<3 reglas) cuando sea imposible evitarlo.
- JS crítico debe tener fallback; GTM no puede depender solo de `requestIdleCallback`.
- Verifica contraste AA, botones ≥ 44px de alto, y atributos `aria-label` en CTA flotante.
- La página debe cargar fonts, imágenes y scripts desde HTTPS y rutas existentes (auditar 404).

---

## 7. Checklist QA antes de publicar
1. [ ] Actualicé `sitemaps/main_sitemap.xml` con la nueva URL y `lastmod` real (ISO 8601).
2. [ ] Validé el JSON-LD completo en Rich Results (sin warnings críticos).
3. [ ] Corrí Lighthouse (Desktop/Mobile) y obtuve LCP < 2.5 s, CLS < 0.1.
4. [ ] Probé formulario y CTAs con y sin JS (al menos verificar apertura de WhatsApp/teléfono).
5. [ ] Revisé ortografía y acentos (“plomería”, “Culiacán”).
6. [ ] Añadí anotación en GA4/Search Console con la fecha de publicación.
7. [ ] Confirmé que la página enlaza a las landings clave y desde ellas se regresa.

**Ninguna URL se libera si un punto del checklist queda sin marcar.**

---

## 8. Registro de verificaciones (llenar por quien publica)
| Fecha | URL creada | Revisor | ¿Checklist completo? | Observaciones |
| --- | --- | --- | --- | --- |
| ____ | __________________________ | __________________ | Sí / No | __________________ |

Actualiza esta tabla cada vez que publiques para mantener trazabilidad.
