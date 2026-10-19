# Comando: /validar

Valida una página nueva contra index.html para detectar errores ANTES de hacer commit.

## Uso

```bash
/validar [ruta-relativa-a-la-página]
```

**Ejemplos:**
```bash
/validar blog/como-identificar-buen-plomero-culiacan/index.html
/validar plomero-24-horas/index.html
/validar servicios/reparacion-fugas/index.html
```

---

## Instrucciones para Claude

Cuando el usuario ejecute este comando:

### 1. Leer Archivos (en paralelo)
- Lee `index.html` (homepage de referencia)
- Lee la página a validar (ruta proporcionada por usuario)

### 2. Validar Hero (CRÍTICO)

Busca en la página nueva la sección `<header` con clase `hero`:

**✅ DEBE CUMPLIR:**
- [ ] Tiene `<picture class="hero-background">` (NO `<div class="hero-background">`)
- [ ] Dentro del `<picture>` hay `<source type="image/webp">` con atributo `srcset`
- [ ] El `<img>` tiene atributos: `decoding="async"` y `fetchpriority="high"`
- [ ] La imagen es `hero-plomero-visita-800w.webp` y `hero-plomero-visita-1200w.webp` (o la que especifique usuario)
- [ ] NO usa `hero-plumbing-*.webp` (imagen obsoleta)

**Reportar línea exacta si hay error.**

### 3. Validar Botones Flotantes (CRÍTICO)

Busca en la página nueva los botones flotantes (antes del cierre `</body>`):

**✅ DEBE CUMPLIR:**
- [ ] Botón WhatsApp tiene clase `floating-btn floating-whatsapp` (NO `cta-btn`)
- [ ] Botón Teléfono tiene clase `floating-btn floating-call` (NO `cta-btn`)
- [ ] Ambos botones contienen `<svg>` con `<path>` (NO emojis 💬 📞)
- [ ] WhatsApp tiene `background:#22c55e` en CSS (verificar en `<style>`)
- [ ] Teléfono tiene `background:#0f4fa8` en CSS
- [ ] NO están dentro de un `<div class="cta-bar">`

**Reportar línea exacta si hay error.**

### 4. Validar Clases CSS Custom (CRÍTICO)

Busca en el `<style>` de la página nueva:

**❌ PROHIBIDO (NO deben existir):**
- [ ] `.highlight-box` con background amarillo (#fef3c7)
- [ ] `.warning-box` con background rojo (#fee2e2)
- [ ] `.info-box`, `.note-box`, `.alert-box` o similar
- [ ] Cualquier clase con `border-left: 4px solid`
- [ ] Fondos de colores que NO existan en index.html

**Reportar línea exacta si encuentra alguna.**

### 5. Validar HTML de Cajas de Colores

Busca en el `<body>` de la página nueva:

**❌ PROHIBIDO (NO deben existir):**
- [ ] `<div class="highlight-box">`
- [ ] `<div class="warning-box">`
- [ ] Divs con `style="background:#fef3c7"` o similar inline

**Reportar línea exacta si encuentra alguna.**

### 6. Validar Barra WhatsApp CTA (OBLIGATORIO)

Busca en el `<body>` dentro de la sección `.benefits-grid`:

**✅ DEBE CUMPLIR:**
- [ ] Tiene `<div class="whatsapp-cta-box">` presente
- [ ] Contiene heading `<h3>` con texto exacto: "¿Tienes dudas? Respondemos en 10 minutos"
- [ ] Tiene botón con clase `whatsapp-cta-button` y texto "Abrir Chat"
- [ ] Link apunta a: `https://wa.me/526674787021?text=...`
- [ ] Está ubicado dentro de `.benefits-grid` (después de los 4 benefits)
- [ ] Usa SVG para iconos (NO emojis)

**❌ ERROR COMÚN:**
- Falta completamente el elemento `.whatsapp-cta-box`
- Texto del heading incorrecto o abreviado
- Botón no dice "Abrir Chat"
- Link no apunta a WhatsApp correcto (526674787021)
- Ubicado fuera de `.benefits-grid`

**Reportar línea exacta si falta o está incorrecto.**

### 7. Validar Estructura General

**✅ DEBE TENER (comparar con index.html):**
- [ ] `<nav class="nav">` idéntico
- [ ] `<footer class="footer">` idéntico
- [ ] Mismo `<link>` a `styles.min.css`
- [ ] Mismo `<script>` de `main.js`
- [ ] Paths correctos (absolutos `/` en raíz, relativos `../../` en subdirectorios)

### 8. Formato del Reporte

Presenta el resultado en este formato:

```markdown
## 🔍 Validación de [nombre-página]

### ✅ APROBADAS (X/7)

- ✅ Hero estructura correcta
- ✅ Botones flotantes con SVG
- ✅ Sin clases CSS custom
- ✅ Sin cajas de colores en HTML
- ✅ Barra WhatsApp CTA presente
- ✅ Estructura general correcta
- ✅ Paths correctos

### ❌ ERRORES DETECTADOS (X)

#### 🚨 Error 1: [Descripción]
- **Archivo:** [ruta]
- **Línea:** [número]
- **Encontrado:** `[código incorrecto]`
- **Debe ser:** `[código correcto]`
- **Fix:** [instrucción específica]

#### 🚨 Error 2: [...]

---

## 📊 Resultado Final

**Estado:** ✅ LISTO PARA COMMIT | ❌ REQUIERE CORRECCIONES

**Acción recomendada:**
- Si TODO ✅: Puedes proceder con `git commit`
- Si HAY ❌: Corrígelos primero ejecutando: [comandos específicos]
```

### 8. Ser Específico

**NO digas:** "El hero está mal"
**SÍ di:** "Línea 145: Hero usa `<div class="hero-background">` pero debe ser `<picture class="hero-background">`"

**NO digas:** "Los botones están incorrectos"
**SÍ di:** "Línea 627-635: Botones usan emojis 💬 📞, deben usar SVG con path d='M17.472...'"

---

## Ejemplo de Uso Completo

```bash
Usuario: /validar blog/articulo-nuevo/index.html

Claude: [Lee ambos archivos]
Claude: [Valida las 6 áreas]
Claude: [Genera reporte]

## 🔍 Validación de articulo-nuevo

### ✅ APROBADAS (5/7)
- ✅ Estructura general correcta
- ✅ Paths correctos
- ✅ Sin cajas de colores en HTML
- ✅ Hero estructura correcta
- ✅ Barra WhatsApp CTA presente

### ❌ ERRORES DETECTADOS (2)

#### 🚨 Error 1: Botones flotantes usan emojis
- **Archivo:** blog/articulo-nuevo/index.html
- **Línea:** 450-455
- **Encontrado:** `<a class="cta-btn">💬</a>`
- **Debe ser:** `<a class="floating-btn floating-whatsapp"><svg>...</svg></a>`
- **Fix:** Reemplazar con estructura de index.html línea 1356-1373

#### 🚨 Error 2: Clase CSS custom prohibida
- **Archivo:** blog/articulo-nuevo/index.html
- **Línea:** 85
- **Encontrado:** `.highlight-box{background:#fef3c7;...}`
- **Debe ser:** NO debe existir esta clase
- **Fix:** Eliminar línea 85 y líneas 320-325 (HTML que la usa)

---

## 📊 Resultado Final

**Estado:** ❌ REQUIERE CORRECCIONES

**Acción recomendada:**
Por favor corrígelos primero. ¿Quieres que los corrija automáticamente?
```

---

## Notas Importantes

- Este comando NO modifica archivos, solo reporta
- Siempre compara contra index.html como fuente de verdad
- Reporta TODAS las diferencias, no solo la primera
- Usa números de línea exactos para facilitar corrección
- Prioriza errores críticos (hero, botones) sobre warnings menores
