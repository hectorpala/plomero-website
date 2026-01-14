---
name: copia-paginas
description: Clone a reference page's HTML/CSS/JS structure exactly while changing only approved content fields; verify with structural diffs and report any deviations.
metadata:
  short-description: Copy page structure exactly; content-only changes
  version: 3.0.0
  triggers:
    - /copia-paginas
    - /copiar-pagina
    - /sync-pages
    - /clone-page
---

# Page Structure Clone (exact match)

## Objetivo
Copiar la pagina A como plantilla exacta para la pagina B.
Solo puede cambiar contenido. Todo lo demas debe quedar identico.

## Entradas requeridas
- `source_path`: ruta de la pagina fuente (A).
- `target_path`: ruta de la pagina destino (B).
- `content_allowlist`: lista estricta de campos que pueden cambiar.
- `tracking_allowlist` (opcional): IDs permitidos (GTM/GA/Clarity).
- `ignore_blocks` (opcional): selectores o bloques completos que pueden excluirse.

---

## Definicion de "contenido" (lo unico que puede cambiar)

```
PERMITIDO CAMBIAR:
- Texto visible (nodos de texto)
- Valores de href, src, srcset (solo la URL, no atributos asociados)
- alt, title
- Telefonos, emails, nombres de marca
- IDs de tracking SOLO si estan en tracking_allowlist
- Contenido de JSON-LD (schema) - solo datos, no estructura
```

---

## Todo lo demas es ESTRUCTURAL y debe quedar IDENTICO

```
PROHIBIDO CAMBIAR:
- Arbol de tags y orden exacto de nodos
- Clases, IDs, roles
- aria-*, data-* y cualquier atributo no permitido
- width, height, sizes, loading, decoding, fetchpriority
- Comentarios HTML
- Orden y ubicacion de scripts y estilos
- Orden de secciones y bloques (popup, CTA flotantes, footer, etc)
- Variables CSS (:root)
- Selectores CSS y sus propiedades
- Media queries y breakpoints
- Orden de reglas CSS
```

---

## Flujo obligatorio

### Paso 1: Lectura
```bash
# Abrir ambas paginas
read source_path  # Pagina A (plantilla)
read target_path  # Pagina B (destino)
```

### Paso 2: Copia base
```
# Copiar estructura de A como base en B
- HTML completo
- CSS (inline y externos)
- JS (orden y atributos)
- Assets referenciados (verificar existencia)
```

### Paso 3: Reemplazo de contenido
```
# Reemplazar SOLO contenido permitido:
FOR each element in content_allowlist:
  - Localizar elemento en B
  - Preservar estructura/atributos
  - Cambiar solo el valor de contenido
  - Verificar que no se altero estructura
```

### Paso 4: Validacion estructural
```
# Validar con diff estructural
- Comparar HTML normalizado
- Comparar CSS regla por regla
- Comparar orden de scripts
- Generar reporte de diferencias
```

### Paso 5: Reporte
```
# Reportar resultado
IF diferencias == 0:
  return PASS
ELSE:
  return FAIL + lista_diferencias
```

---

## Validacion minima obligatoria

### 1) HTML (estructura)

```python
# Proceso de validacion HTML:
1. Normalizar HTML de A y B
2. Reemplazar valores permitidos por placeholder <content>
3. Extraer secuencia de tags + atributos (sin texto visible)
4. Comparar linea por linea
5. Debe coincidir 1:1
```

**Elementos a validar:**
- [ ] Orden de tags
- [ ] Nombres de clases (exactos)
- [ ] IDs (exactos)
- [ ] Atributos aria-* (todos)
- [ ] Atributos data-* (todos)
- [ ] width, height en imagenes
- [ ] sizes, srcset pattern (no URLs)
- [ ] loading, fetchpriority, decoding
- [ ] Estructura de SVG inline
- [ ] Comentarios HTML

### 2) CSS

```python
# Proceso de validacion CSS:
1. Extraer todas las reglas de A
2. Extraer todas las reglas de B
3. Comparar selector por selector
4. Comparar propiedad por propiedad
5. Comparar valor por valor
```

**Archivos a validar:**
- [ ] CSS inline en head
- [ ] critical.css / critical.min.css
- [ ] styles.css / styles.min.css
- [ ] Cualquier otro CSS referenciado

**Reglas clave que DEBEN coincidir:**
```css
/* Variables */
:root { }

/* Nav */
.nav { }
.nav-wrapper { }
.logo { }
.logo img { }
.logo:hover { }
.nav-menu { }
.nav-link { }
.nav-link:hover { }
.mobile-menu-btn { }
.mobile-menu-btn span { }

/* Hero */
.hero { }
.hero-background { }
.hero-background img { }
.hero::after { }
.hero-content { }
.hero h1 { }
.hero-subtitle { }
.hero-rating { }
.hero-features { }
.btn-primary { }

/* Flotantes */
.floating-btn { }
.floating-call { }
.floating-whatsapp { }

/* Media Queries */
@media (max-width: 768px) { /* todas las reglas */ }
@media (max-width: 480px) { /* todas las reglas */ }
```

### 3) Scripts

```python
# Proceso de validacion Scripts:
1. Extraer todos los script de A
2. Extraer todos los script de B
3. Comparar orden exacto
4. Comparar atributos (async, defer, type, src)
5. No agregar ni quitar scripts fuera del allowlist
```

---

## Output requerido

### PASS (estructura identica)
```markdown
## Resultado: PASS

### Resumen
- Fuente: {source_path}
- Destino: {target_path}
- Diferencias estructurales: 0
- Cambios de contenido: {N}

### Contenido actualizado
| Elemento | Valor anterior | Valor nuevo |
|----------|---------------|-------------|
| title | "Plomero..." | "Electricista..." |
| h1 | "Plomero..." | "Electricista..." |
| tel: | 6672... | 6671... |

### Verificacion
- [x] HTML estructura identica
- [x] CSS identico
- [x] Scripts identicos
- [x] Contenido preservado
```

### FAIL (hay diferencias)
```markdown
## Resultado: FAIL

### Diferencias encontradas: {N}

| Archivo | Linea | Tipo | Esperado (A) | Encontrado (B) |
|---------|-------|------|--------------|----------------|
| index.html | 45 | attr | aria-label="Abrir menu" | (ausente) |
| critical.css | 23 | value | padding:16px 0 | padding:22px 0 |
| critical.css | 26 | value | height:86px | height:140px |

### Acciones requeridas
1. Agregar aria-label en button (linea 45)
2. Cambiar padding en .nav (linea 23)
3. Cambiar height en .logo img (linea 26)
```

---

## Reglas estrictas

### PROHIBIDO
- No afirmar "listo" sin validacion completa
- No asumir que algo esta correcto sin verificar
- No cambiar estructura "porque parece mejor"
- No omitir archivos CSS (si hay .min.css, validar ambos)
- No ignorar diferencias "menores"

### OBLIGATORIO
- Validar CADA selector CSS
- Validar CADA atributo HTML
- Reportar TODAS las diferencias
- Si no puedes validar algo, decirlo explicitamente
- Si hay dudas, preguntar ANTES de cambiar estructura

---

## Ejemplo de content_allowlist

```yaml
content_allowlist:
  # Textos
  - title
  - meta[name="description"]
  - h1, h2, h3, p (texto interno)
  - .hero-subtitle (texto)
  - .benefit-content p (texto)

  # URLs
  - link[rel="canonical"] href
  - meta[property="og:url"] content
  - a.logo href (si cambia dominio)
  - img src, srcset (URLs, no pattern)

  # Contacto
  - tel: enlaces
  - wa.me/ enlaces
  - mailto: enlaces

  # Schema
  - script[type="application/ld+json"] (contenido JSON)

  # Tracking (solo si en tracking_allowlist)
  - GTM-XXXXXX
  - G-XXXXXX
  - clarity project id

tracking_allowlist:
  - GTM-ABCD123
  - G-XYZ789

ignore_blocks:
  - Google Tag Manager comments
```

---

## Comandos de validacion

```bash
# Comparar estructura HTML (sin contenido)
diff <(grep -oE '<[^>]+>' A.html | sort) <(grep -oE '<[^>]+>' B.html | sort)

# Comparar CSS selector por selector
echo "=== A ===" && curl -s "url-A/css" | grep -oE "\.selector\{[^}]+\}"
echo "=== B ===" && curl -s "url-B/css" | grep -oE "\.selector\{[^}]+\}"

# Verificar atributos especificos
grep -n "aria-label\|aria-expanded\|aria-controls\|srcset\|sizes" archivo.html

# Comparar archivos CSS completos
diff <(cat A/critical.min.css) <(cat B/critical.min.css)
```

---

## Regla de oro

> **Si hay CUALQUIER diferencia estructural entre A y B, es un FAIL.**
>
> El agente NO puede reportar PASS hasta que la validacion muestre
> CERO diferencias en estructura, CSS, y orden de elementos.
>
> "Casi igual" NO es igual.
> "Solo un atributo" ES una diferencia.
> "Es menor" NO es excusa.

---

# CHECKLIST OBLIGATORIO DEL SKILL

## Inputs (antes de comenzar)

- [ ] Definir source_path y target_path
- [ ] Definir content_allowlist (texto, href/src/srcset/alt/title, telefonos, emails, marca)
- [ ] Definir tracking_allowlist (GTM/GA/Clarity) si aplica
- [ ] Definir ignore_blocks si hay bloques excluidos (por defecto vacio)

---

## Reglas duras (NO negociables)

```
VIOLACION = FAIL INMEDIATO

1. Estructura HTML identica: mismo arbol, mismo orden, mismas clases/IDs/roles/aria/data-*
2. Atributos identicos: orden exacto + comillas, width, height, sizes, loading, decoding, fetchpriority, rel, type, media
3. Orden identico de scripts y estilos
4. No anadir ni quitar bloques (popups, CTA flotantes, footer, formularios)
```

---

## Paso 1 - Copia base

- [ ] Copiar HTML completo de A a B
- [ ] Copiar CSS completo (critico + principal)
- [ ] Si hay minificado Y no minificado, copiar AMBOS
- [ ] Copiar JS completo si existe
- [ ] Verificar que assets referenciados existen

---

## Paso 2 - Reemplazo de contenido permitido

- [ ] Reemplazar SOLO elementos en content_allowlist
- [ ] NO tocar atributos fuera del allowlist
- [ ] Mantener el mismo numero de nodos y atributos
- [ ] Verificar que estructura no cambio despues del reemplazo

---

## Paso 3 - Validacion estructural HTML

```python
# Proceso:
1. Normalizar HTML reemplazando valores permitidos por <content>
2. Comparar secuencia de tags y atributos 1:1
3. Si hay diferencias: FAIL y listar archivo:linea
```

**Checklist HTML:**
- [ ] Orden de tags identico
- [ ] Orden de atributos identico (incluye comillas y orden exacto en <a> de tarjetas de servicios)
- [ ] Nombres de clases identicos
- [ ] IDs identicos
- [ ] Atributos aria-* identicos
- [ ] Atributos data-* identicos
- [ ] width/height en imagenes identicos
- [ ] sizes/srcset pattern identico (URLs pueden cambiar)
- [ ] loading/fetchpriority/decoding identicos
- [ ] Estructura SVG inline identica
- [ ] Comentarios HTML identicos

---

## Paso 4 - Validacion CSS

```python
# Proceso:
1. Comparar CSS critico 1:1 (regla por regla)
2. Comparar CSS principal 1:1 (regla por regla)
3. Asegurar que reglas nav/hero/sections/footer/popup/CTA flotantes coinciden
4. Si hay minificado, debe ser IDENTICO al no minificado en valores
```

**Archivos a validar:**
- [ ] CSS inline en head
- [ ] critical.css / critical.min.css
- [ ] styles.css / styles.min.css
- [ ] Cualquier otro CSS referenciado

**Selectores criticos que DEBEN coincidir:**
- [ ] :root (variables)
- [ ] .nav, .nav-wrapper, .logo, .logo img, .logo:hover
- [ ] .nav-menu, .nav-link, .nav-link:hover
- [ ] .mobile-menu-btn, .mobile-menu-btn span
- [ ] .hero, .hero-background, .hero-background img, .hero::after
- [ ] .hero-content, .hero h1, .hero-subtitle, .hero-rating
- [ ] .hero-features, .feature-item, .feature-icon
- [ ] .btn-primary, .btn-primary:hover
- [ ] .floating-btn, .floating-call, .floating-whatsapp
- [ ] @media (max-width: 768px) - TODAS las reglas
- [ ] @media (max-width: 480px) - TODAS las reglas

---

## Paso 5 - Validacion JS

- [ ] Orden de scripts identico
- [ ] Atributos de scripts identicos (defer, async, src, type)
- [ ] IDs de tracking solo si estan en tracking_allowlist
- [ ] No agregar ni quitar scripts fuera del allowlist

---

## Paso 6 - Validacion de imagenes

- [ ] Verificar width/height identicos
- [ ] Verificar sizes identicos
- [ ] Verificar srcset pattern identico (solo URLs cambian)
- [ ] Verificar loading/fetchpriority/decoding identicos
- [ ] Si cambia la proporcion de imagen, es FAIL

---

## Paso 7 - Reporte final

- [ ] Reportar PASS o FAIL
- [ ] En FAIL: enumerar diferencias exactas con archivo:linea + motivo
- [ ] Incluir tabla de cambios de contenido realizados
- [ ] Incluir checklist de verificacion marcado

---

# CHECKLIST POR SECCIONES (Auditoria Rapida)

## Head

- [ ] meta charset identico
- [ ] meta viewport identico
- [ ] title - solo texto puede cambiar
- [ ] meta name="description" - solo content puede cambiar
- [ ] meta name="keywords" - solo content puede cambiar
- [ ] Open Graph tags - estructura identica, solo content/URLs cambian
- [ ] Twitter tags - estructura identica, solo content/URLs cambian
- [ ] link rel="canonical" - solo href puede cambiar
- [ ] link rel="icon/favicon" - estructura identica
- [ ] Preload/preconnect - mismos recursos, mismo orden
- [ ] Fonts - mismas fonts, mismo orden
- [ ] CSS links - mismo orden, mismos atributos
- [ ] Scripts de analytics - solo IDs en tracking_allowlist pueden variar

## Nav

- [ ] nav class="nav" - estructura identica
- [ ] .nav-wrapper - estructura identica
- [ ] .logo con mismos atributos (solo src/alt/title cambian)
- [ ] .logo img - width/height/sizes/srcset pattern identicos
- [ ] button.mobile-menu-btn - aria-label/aria-expanded/aria-controls identicos
- [ ] .nav-menu - mismo ID, misma estructura
- [ ] .nav-link - mismo numero de items, mismo orden
- [ ] Solo texto de enlaces puede cambiar

## Hero

- [ ] header class="hero" o section class="hero" - misma estructura
- [ ] picture class="hero-background" - misma estructura
- [ ] source tags - mismo type, mismo media, mismo sizes pattern
- [ ] img hero - width/height/loading/fetchpriority/decoding identicos
- [ ] .hero-content - misma estructura interna
- [ ] .hero-eta-badge - misma estructura (si existe)
- [ ] .hero-rating - misma estructura SVG + spans
- [ ] .hero-features - mismo numero de .feature-item
- [ ] .btn-primary - mismos atributos, solo texto/href cambian

## Secciones (Benefits, Services, etc.)

- [ ] Mismo orden de secciones
- [ ] Mismo markup por seccion
- [ ] Mismo numero de cards/items
- [ ] Listas con mismos tags y atributos
- [ ] SVG icons - estructura identica
- [ ] Solo texto visible puede cambiar

## Cards de Servicios

- [ ] .card o .service-card - misma estructura
- [ ] .media-box - misma estructura
- [ ] picture - mismo pattern de sources
- [ ] <a> usa el mismo orden de atributos que la fuente (href antes de class, comillas dobles)
- [ ] href es relativo con ./ y termina en /index.html (formato identico a la fuente)
- [ ] img - width/height/loading/decoding identicos
- [ ] .service-list - mismo numero de items
- [ ] .service-cta - misma estructura

Ejemplo exacto (formato del <a>):
```html
<a href="./servicios/mi-servicio/index.html" class="card card--img">
```

Ejemplo exacto (srcset coherente con archivos):
```html
<source type="image/webp" srcset="assets/images/mi-servicio-420w.webp 420w, assets/images/mi-servicio-800w.webp 800w">
<img src="assets/images/mi-servicio-420w.webp" srcset="assets/images/mi-servicio-420w.webp 420w, assets/images/mi-servicio-800w.webp 800w" sizes="(max-width:768px) 100vw, 420px" width="420" height="420" loading="lazy" decoding="async">
```

## Blog/Noticias (si existe)

- [ ] .news-grid o similar - misma estructura
- [ ] article - misma estructura interna
- [ ] time - mismo atributo datetime format
- [ ] .read-more o similar - misma estructura

## Footer

- [ ] footer - misma estructura
- [ ] Mismo numero de columnas/secciones
- [ ] Mismo orden de enlaces
- [ ] Solo texto/URLs de enlaces pueden cambiar
- [ ] Copyright - solo year/nombre puede cambiar
- [ ] Social links - misma estructura, solo hrefs cambian

## Popup + CTAs flotantes

- [ ] .floating-btn - misma estructura
- [ ] .floating-call - mismos atributos, solo tel: cambia
- [ ] .floating-whatsapp - mismos atributos, solo wa.me/ cambia
- [ ] Popup (si existe) - misma estructura completa
- [ ] ARIA/roles - identicos

---

# COMANDOS DE VALIDACION RAPIDA

```bash
# 1. Comparar estructura de tags (sin contenido)
diff <(curl -s "URL-A" | grep -oE '<[^>]+>' | sort) \
     <(curl -s "URL-B" | grep -oE '<[^>]+>' | sort)

# 2. Comparar archivos CSS externos
diff <(curl -s "URL-A/assets/css/critical.min.css") \
     <(curl -s "URL-B/assets/css/critical.min.css")

# 3. Verificar atributos aria
grep -n "aria-label\|aria-expanded\|aria-controls" archivo.html

# 4. Verificar atributos de imagenes
grep -n "width=\|height=\|sizes=\|srcset=" archivo.html

# 5. Comparar orden de scripts
grep -n "<script" A.html > /tmp/a-scripts.txt
grep -n "<script" B.html > /tmp/b-scripts.txt
diff /tmp/a-scripts.txt /tmp/b-scripts.txt

# 6. Listar todas las clases CSS usadas
grep -oE 'class="[^"]*"' archivo.html | sort -u
```

---

# EJEMPLO DE EJECUCION COMPLETA

```yaml
# Inputs definidos:
source_path: /plomero-culiacan-pro/index.html
target_path: /electricista-culiacan-pro/index.html

content_allowlist:
  - title (texto)
  - meta[name="description"] content
  - meta[name="keywords"] content
  - link[rel="canonical"] href
  - meta[property="og:*"] content/url
  - h1, h2, h3, p (texto interno)
  - .hero-subtitle (texto)
  - .benefit-content p (texto)
  - img src, srcset (URLs)
  - img alt, title
  - a.logo href
  - tel: enlaces
  - wa.me/ enlaces
  - mailto: enlaces
  - script[type="application/ld+json"] (JSON completo)

tracking_allowlist:
  - GTM-W75CRTX5
  - G-XXXXXXXX
  - ukonwm7t1p (Clarity)

ignore_blocks: []
```

---

# RESUMEN EJECUTIVO

```
+----------------------------------------------------------+
|                    REGLA ABSOLUTA                         |
+----------------------------------------------------------+
|                                                           |
|  Si A y B no son BYTE-FOR-BYTE identicos en estructura,  |
|  es FAIL.                                                 |
|                                                           |
|  El contenido permitido es la UNICA excepcion.            |
|                                                           |
|  NO hay "casi igual".                                     |
|  NO hay "diferencia menor".                               |
|  NO hay "se ve bien asi".                                 |
|                                                           |
|  PASS = 0 diferencias estructurales                       |
|  FAIL = 1+ diferencias estructurales                      |
|                                                           |
+----------------------------------------------------------+
```


---

# ARCHIVOS DE REFERENCIA (ESTRUCTURA OBLIGATORIA)

## main.js - Secciones obligatorias (en este orden)

```javascript
// Main JavaScript - [Nombre del Proyecto]
// Loaded with defer for optimal performance
// Last updated: YYYY-MM-DD

// Mobile menu toggle with scroll position preservation
(function() {
    // DEBE incluir:
    // - let scrollY = 0;
    // - function openMenu() con scrollY save, body.style.top, aria-expanded, aria-label
    // - function closeMenu() con scrollY restore, aria-expanded, aria-label
    // - mobileMenuBtn.setAttribute('aria-expanded', 'true/false');
    // - mobileMenuBtn.setAttribute('aria-label', 'Cerrar/Abrir menú');
})();

// Real-time form validation
(function() {
    // validators object con nombre, telefono, email, mensaje
    // validateField, isFormValid, updateSubmitButton
})();

// Multi-layer lead capture: Netlify Forms + localStorage + GA4 + WhatsApp
(function() {
    // localStorage key: [proyecto]_leads (ej: electricista_leads)
    // dataLayer.push generate_lead
    // WhatsApp redirect
})();

// CTA fijo con tracking
(function() {
    // cta-whatsapp, cta-llamar
    // pushEvt("cta_click", ...)
})();

// Mini footer nav tracking
(function() {
    // .site-mini-nav a tracking
})();

// Tracking de tarjetas SEO - diferido con requestIdleCallback
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    // .seo-card tracking
    // scroll depth tracking con rAF throttle
})();

// Exit-Intent Popup
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    // showPopup, hidePopup
    // mobile: timer 30s + back button detection
    // desktop: mouseleave
}, 2500);

// Service Worker Registration
if ('serviceWorker' in navigator) { ... }

// Bottom Sheet Cotización Móvil
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    // quote-trigger, quote-overlay, quote-sheet
    // openSheet, closeSheet con scrollY preservation
    // touch swipe to close
    // focus trap
})();

// Hide floating buttons in critical sections
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    // IntersectionObserver para #contacto, .footer, .contact-form, .map-embed
    // MutationObserver para body class changes
})();
```

**Checklist main.js:**
- [ ] Mobile menu con scroll position preservation (scrollY, body.style.top)
- [ ] aria-expanded toggle en openMenu/closeMenu
- [ ] aria-label toggle (Cerrar/Abrir menú)
- [ ] localStorage key correcto ([proyecto]_leads)
- [ ] CTA tracking (cta-whatsapp, cta-llamar)
- [ ] Mini footer nav tracking
- [ ] SEO cards tracking con requestIdleCallback
- [ ] Scroll depth con rAF throttle
- [ ] Exit intent popup (mobile timer + back, desktop mouseleave)
- [ ] Bottom sheet con scroll preservation y focus trap
- [ ] Floating buttons visibility con IntersectionObserver

---

## critical.css - Selectores obligatorios

```css
/* Variables - DEBEN coincidir exactamente */
:root{--brand:#f97316;--brand-dark:#e36414;--text:#1a1a2e;--text-light:#4a4a68;--bg:#f8fafc;--bg-card:#fff;--border:#e2e8f0;--shadow:rgba(0,0,0,.08);--shadow-lg:rgba(0,0,0,.12);--gutter:1.5rem;--max-w:1200px;--gradient-brand:linear-gradient(135deg,#f97316,#e36414)}

/* Nav - CRITICO */
.nav{position:fixed;top:0;left:0;right:0;z-index:50;background:transparent;border-bottom:none;padding:16px 0}
.logo img{height:86px;width:auto;display:block;max-height:100px;mix-blend-mode:multiply}
@media(max-width:768px){.logo img{height:62px;max-height:72px}}
.mobile-menu-btn{display:none;flex-direction:column;justify-content:space-between;width:28px;height:20px;cursor:pointer;background:none;border:none;padding:0;gap:0}
.mobile-menu-btn span{display:block;height:3px;width:100%;background:#F97316;border-radius:2px;margin:0}

/* Hero - LCP Critical */
.hero{min-height:85vh;padding:140px 16px 2.5rem}
.hero-content{min-height:280px}
.btn-primary{border-radius:14px;padding:17px 34px}

/* Mobile */
@media(max-width:768px){
.hero{min-height:60vh;padding-top:80px}
.hero-content{min-height:260px!important}
}
```

**Checklist critical.css:**
- [ ] :root variables identicas
- [ ] .nav padding:16px 0 (NO 22px)
- [ ] .logo img height:86px (NO 140px)
- [ ] .mobile-menu-btn width:28px, height:20px, gap:0
- [ ] .mobile-menu-btn span height:3px, margin:0
- [ ] .hero min-height:85vh, padding:140px 16px 2.5rem
- [ ] .hero-content min-height:280px
- [ ] .btn-primary border-radius:14px, padding:17px 34px
- [ ] @media 768px .hero min-height:60vh
- [ ] @media 768px .hero-content min-height:260px

---

## styles.min.css - Selectores adicionales obligatorios

```css
/* Breadcrumb */
.breadcrumb-wrapper{margin-top:80px}
.breadcrumb a{color:#E36414}

/* Benefits */
.benefits-grid{grid-template-columns:repeat(2,1fr)}
.benefit-icon{width:48px;height:48px}
.whatsapp-cta-box{background:linear-gradient(135deg,#25D366,#128C7E)}

/* Cards */
.card.card--img h3{color:#1e3a8a!important}
.seo-card{border:1px solid #f0e6dc}
span.service-cta,.service-cta{background-color:#f97316!important;color:#fff!important}
```

---

## styles.7f293647.css - Archivo CSS externo

Este archivo contiene estilos non-critical y DEBE existir si está referenciado en index.html.

```bash
# Verificar existencia
ls -la styles.7f293647.css
```

---

# RECORDATORIO FINAL

> **Antes de reportar PASS:**
>
> 1. ¿main.js tiene scroll preservation en menú móvil?
> 2. ¿main.js tiene aria-expanded/aria-label toggle?
> 3. ¿main.js tiene las 10 secciones en el orden correcto?
> 4. ¿critical.css tiene .nav padding:16px 0?
> 5. ¿critical.css tiene .logo img height:86px?
> 6. ¿critical.css tiene .mobile-menu-btn con gap:0?
> 7. ¿Existe styles.7f293647.css si está referenciado?
> 8. ¿localStorage key es [proyecto]_leads?
>
> **Si alguna respuesta es NO → FAIL**
