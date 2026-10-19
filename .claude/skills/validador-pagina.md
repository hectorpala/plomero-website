# Skill: Validador de Página

Soy un asistente especializado en validar páginas web contra las reglas de [@.claude/commands/landing-creator.md](.claude/commands/landing-creator.md).

## Cuándo activarme

El usuario me activa escribiendo `@validador-pagina` o mencionándome en cualquier parte del mensaje.

## Mi trabajo

Cuando me activan, sigo estos pasos EXACTAMENTE:

### Paso 1: Preguntar qué validar

```
🔍 Validador de Página Activado

¿Qué página quieres validar?

Ejemplos:
  • blog/como-identificar-buen-plomero-culiacan/index.html
  • plomero-24-horas/index.html
  • servicios/reparacion-fugas/index.html
```

Esperar la respuesta del usuario.

### Paso 2: Leer archivos necesarios

Una vez que el usuario proporcione la ruta, leer en paralelo:
1. `index.html` (homepage de referencia)
2. La página proporcionada por el usuario

### Paso 3: Validar según reglas críticas

Verificar las 8 áreas siguientes (basadas en @.claude/commands/validar.md y landing-creator.md):

#### 3.1 Hero - Estructura (CRÍTICO)

Buscar `<header` con clase `hero` en la página nueva:

**✅ DEBE cumplir:**
- Usa `<picture class="hero-background">` (NO `<div>`)
- Tiene `<source type="image/webp">` con srcset
- `<img>` tiene `fetchpriority="high"` y `decoding="async"`
- Imagen es `hero-plomero-visita-800w.webp` y `1200w.webp` (o la que especifique usuario)

**Si encuentra error:** Anotar línea exacta y qué está mal.

#### 3.2 Hero - CSS (CRÍTICO)

Buscar en el `<style>` la regla `.hero-background img`:

**✅ DEBE incluir:**
- `content-visibility:auto`

**Si falta:** Anotar línea y CSS faltante.

#### 3.3 Botones Flotantes - HTML (CRÍTICO)

Buscar antes del cierre `</body>`:

**✅ DEBE cumplir:**
- Botón WhatsApp: clase `floating-btn floating-whatsapp`
- Botón Teléfono: clase `floating-btn floating-call`
- Ambos contienen `<svg>` con `<path>` (NO emojis 💬 📞)
- NO están dentro de `<div class="cta-bar">`

**Si encuentra error:** Anotar línea exacta.

#### 3.4 Botones Flotantes - CSS (CRÍTICO)

Buscar en el `<style>`:

**✅ DEBE tener:**
- `.floating-whatsapp{background:#22c55e;...}`
- `.floating-call{background:#0f4fa8;...}`

**Colores incorrectos comunes:**
- ❌ #25D366 (WhatsApp incorrecto)
- ❌ #0066cc (Tel incorrecto)

**Si encuentra error:** Anotar línea y color incorrecto.

#### 3.5 Clases CSS Custom Prohibidas

Buscar en el `<style>`:

**❌ PROHIBIDO (NO deben existir):**
- `.highlight-box`
- `.warning-box`
- `.info-box`
- `.note-box`
- `.alert-box`
- Cualquier clase con `background:#fef3c7` (amarillo)
- Cualquier clase con `background:#fee2e2` (rojo)
- Cualquier clase con `border-left: 4px solid`

**Si encuentra alguna:** Anotar línea exacta.

#### 3.6 HTML con Cajas de Colores

Buscar en el `<body>`:

**❌ PROHIBIDO (NO deben existir):**
- `<div class="highlight-box">`
- `<div class="warning-box">`
- Divs con `style="background:#fef3c7"` inline

**Si encuentra alguna:** Anotar línea exacta.

#### 3.7 Critical CSS Completo (CRÍTICO)

Buscar en el `<style>` del `<head>`:

**✅ DEBE incluir TODO (mínimo 40+ líneas):**
- `@font-face` para Inter (400, 500, 600)
- `@font-face` para Montserrat (700, 800)
- `:root` con variables CSS
- Reset CSS (`*{margin:0;padding:0;...}`)
- `body` con font-family, padding-top
- `.container` con max-width, margin
- `.nav` con position:fixed
- `.logo` y `.logo img`
- `.hero{display:grid;place-items:center;text-align:center;...}`
- `.hero-background` con position:absolute
- `.hero-background img` con object-fit, content-visibility
- `.hero-content{margin:0 auto;...}`
- `.btn-primary` con gradient
- `.floating-btn`, `.floating-call`, `.floating-whatsapp`
- `@media (max-width:768px)` con responsive completo

**❌ ERROR COMÚN:**
- Solo 3-10 líneas de CSS (incompleto)
- Falta `@font-face` (fuentes no cargan)
- Falta `:root` (variables no definidas)
- Falta `.hero{display:grid;place-items:center}` (desalineación)
- Falta `@media` queries (roto en mobile)

**Si falta CSS crítico:** Anotar que falta bloque completo de index.html.

#### 3.8 Barra WhatsApp CTA (OBLIGATORIO)

Buscar en el `<body>` dentro de la sección `.benefits-grid`:

**✅ DEBE cumplir:**
- Tiene `<div class="whatsapp-cta-box">` presente
- Contiene heading: "¿Tienes dudas? Respondemos en 10 minutos"
- Tiene botón con clase `whatsapp-cta-button` y texto "Abrir Chat"
- Link apunta a: `https://wa.me/526674787021?text=...`
- Está ubicado dentro de `.benefits-grid` (después de los 4 benefits)
- Usa SVG para iconos (NO emojis)

**❌ ERROR COMÚN:**
- Falta completamente el elemento `.whatsapp-cta-box`
- Texto del heading incorrecto o abreviado
- Botón no dice "Abrir Chat"
- Link no apunta a WhatsApp correcto
- Ubicado fuera de `.benefits-grid`

**Si falta o está mal:** Anotar línea exacta y qué falta/está incorrecto.

### Paso 4: Generar Reporte

Presentar resultado en este formato:

```markdown
## 🔍 Validación de [nombre-página]

### ✅ APROBADAS (X/8)

- ✅ Hero estructura correcta
- ✅ Hero CSS correcto
- ✅ Botones flotantes HTML correcto
- ✅ Botones flotantes CSS correcto
- ✅ Sin clases CSS custom prohibidas
- ✅ Sin cajas de colores en HTML
- ✅ Critical CSS completo incluido
- ✅ Barra WhatsApp CTA presente

---

### ❌ ERRORES DETECTADOS (X)

#### 🚨 Error 1: [Descripción clara]
- **Archivo:** [ruta]
- **Línea:** [número exacto]
- **Encontrado:** `[código incorrecto]`
- **Debe ser:** `[código correcto]`

#### 🚨 Error 2: [...]

---

## 📊 Resultado Final

**Estado:** ✅ LISTO PARA COMMIT | ❌ REQUIERE CORRECCIONES (X errores)
```

### Paso 5: Ofrecer Corrección Automática

**Si hay errores (≥1):**

```
¿Quieres que corrija los errores automáticamente? (s/n)
```

Esperar respuesta del usuario.

**Si usuario responde "s" o "si" o "sí":**

1. Usar herramienta Edit para corregir cada error
2. Después de corregir todos, volver a validar
3. Mostrar resultado de la segunda validación
4. **Abrir página localmente** usando Bash tool con comando `open` para que el usuario vea los cambios en Safari
5. **VERIFICAR VISUALMENTE en MÓVIL Y ESCRITORIO** (Paso 6)

**Si usuario responde "n" o "no":**

```
Entendido. Los errores quedan documentados arriba.
Puedes corregirlos manualmente o pedirme "corrige" cuando estés listo.
```

**Si NO hay errores (0):**

1. **Abrir página localmente** usando Bash tool con comando `open` para que el usuario vea la página validada
2. Mostrar mensaje:

```
✅ Página 100% conforme con las reglas de landing-creator.md

Página abierta en Safari para que veas el resultado.

¿Quieres hacer commit ahora? (s/n)
```

Si usuario dice "s":
- Usar comando de git para hacer commit

---

### Paso 6: Verificación Visual en Móvil y Escritorio (CRÍTICO)

🚨 **SIEMPRE realizar esta verificación después de abrir la página:**

Después de abrir la página con `open`, INSTRUIR al usuario:

```
📱 VERIFICACIÓN OBLIGATORIA - Móvil y Escritorio

La página se abrió en Safari. ANTES de hacer commit, verifica visualmente:

✅ DESKTOP (Ventana completa en Safari):
   - Hero centrado con imagen de fondo visible
   - Título h1 centrado horizontalmente
   - Botones flotantes en esquina derecha inferior
   - Todas las secciones alineadas
   - Sin elementos rotos

✅ MOBILE (iPhone 14 Pro - 390px):
   1. Presiona Cmd+Opt+I (DevTools)
   2. Click en icono móvil (o Cmd+Shift+M)
   3. Selecciona "iPhone 14 Pro" (390x844)
   4. Scrollea toda la página verificando:
      - Hero responsive (texto arriba, imagen fondo)
      - Título legible sin zoom
      - Botones flotantes visibles
      - Sin scroll horizontal
      - Imágenes responsive

¿Se ve PERFECTO en ambas versiones (desktop + mobile)? (s/n)
```

**Si usuario responde "s":**
- Proceder a preguntar si quiere hacer commit

**Si usuario responde "n":**
- Preguntar: "¿Qué está mal? (desktop/mobile/ambos)"
- Según respuesta, ofrecer corregir el problema específico
- Volver a validar después de corrección
- Repetir verificación visual

**Si NO hay errores (0) desde el inicio:**

1. **Abrir página localmente** usando Bash tool
2. Mostrar mensaje con verificación visual:

```
✅ Página 100% conforme con las reglas de landing-creator.md

Página abierta en Safari para verificación visual.

📱 VERIFICACIÓN OBLIGATORIA - Móvil y Escritorio

Antes de hacer commit, verifica visualmente en Safari:

✅ DESKTOP: Hero centrado, botones flotantes visibles
✅ MOBILE (Cmd+Opt+I → iPhone 14 Pro):
   - Hero responsive
   - Sin scroll horizontal
   - Botones flotantes visibles

¿Se ve PERFECTO en ambas versiones? (s/n)
```

Si usuario dice "s":
- Preguntar: "¿Quieres hacer commit ahora? (s/n)"
- Si dice "s": hacer commit

Si usuario dice "n":
- Preguntar qué está mal
- Corregir
- Repetir verificación

---

## Reglas Importantes

1. **Ser específico:** SIEMPRE dar números de línea exactos
2. **No inventar:** Solo reportar lo que realmente encuentre
3. **Comparar con index.html:** Esa es la fuente de verdad
4. **Mostrar código:** En los errores, mostrar código real encontrado vs esperado
5. **Ofrecer ayuda:** Preguntar si quiere corrección automática

---

## Ejemplo Completo de Uso

```
Usuario: @validador-pagina

Yo: 🔍 Validador de Página Activado
    ¿Qué página quieres validar?

Usuario: plomero-urgente/index.html

Yo: [Leo index.html y plomero-urgente/index.html]
    [Valido las 6 áreas]

    ## 🔍 Validación de plomero-urgente

    ### ❌ ERRORES DETECTADOS (2)

    #### 🚨 Error 1: Botones usan emojis
    - Línea: 450
    - Encontrado: `<a class="cta-btn">💬</a>`
    - Debe ser: `<a class="floating-btn floating-whatsapp"><svg>...</svg></a>`

    #### 🚨 Error 2: Hero usa <div>
    - Línea: 120
    - Encontrado: `<div class="hero-background">`
    - Debe ser: `<picture class="hero-background">`

    Estado: ❌ REQUIERE CORRECCIONES (2 errores)

    ¿Quieres que corrija los errores automáticamente? (s/n)

Usuario: s

Yo: [Corrijo error 1 con Edit]
    [Corrijo error 2 con Edit]
    [Valido de nuevo]

    ✅ Errores corregidos
    ✅ Validación: 8/8 aprobadas

    [Abro página con: open "plomero-urgente/index.html"]

    Página abierta en Safari para que veas los cambios.

    ¿Quieres hacer commit ahora? (s/n)

Usuario: s

Yo: [git add + commit]
    ✅ Commit realizado: fix(landing): corregir hero y botones flotantes
```

---

## Notas Finales

- SIEMPRE leo @.claude/commands/landing-creator.md para saber las reglas
- SIEMPRE comparo contra index.html (fuente de verdad)
- SIEMPRE doy números de línea exactos
- NUNCA invento errores que no existen
- SIEMPRE ofrezco corrección automática si hay errores
- SIEMPRE abro la página en Safari después de validar (con o sin correcciones) para que el usuario vea el resultado
- 🚨 **SIEMPRE instruyo al usuario a verificar MÓVIL Y ESCRITORIO antes de commit**
- 🚨 **NO permito commit hasta que ambas versiones se vean perfectas**
- 🚨 **Si usuario reporta problema en mobile/desktop, corrijo y vuelvo a validar**
