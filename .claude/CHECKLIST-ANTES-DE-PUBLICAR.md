# ⚠️ CHECKLIST PRE-PUBLICACIÓN

**IMPORTANTE:** Antes de ejecutar `git commit` en cualquier página nueva (landing, artículo, servicio), **DEBES** completar este checklist.

---

## 🌐 1. ABRIR AMBAS PÁGINAS EN NAVEGADOR

□ **Homepage:** `open index.html` en Safari
□ **Página nueva:** `open [ruta-nueva-pagina]/index.html` en Safari
□ Coloca ambas ventanas lado a lado para comparación visual

---

## 🎨 2. HERO - Lo Más Crítico

### Comparación Visual
□ ¿El hero de la nueva página se ve IGUAL al de index.html?
□ ¿Tiene imagen de fondo? (NO debe verse overlay oscuro sobre tubería)
□ ¿El texto se lee bien sobre la imagen?

### Inspección Técnica (Abrir DevTools - Cmd+Option+I)
□ Click derecho en el hero → "Inspect Element"
□ **VERIFICAR:** `<picture class="hero-background">` ← DEBE ser `<picture>`, NO `<div>`
□ **VERIFICAR:** Dentro hay `<source type="image/webp">` con srcset
□ **VERIFICAR:** Imagen es `hero-plomero-visita-800w.webp` y `hero-plomero-visita-1200w.webp`
□ **VERIFICAR:** `<img>` tiene atributos `decoding="async"` y `fetchpriority="high"`

**❌ Si el hero NO se ve igual → DETENTE y pide corrección**

---

## 📞 3. BOTONES FLOTANTES (Abajo derecha)

### Comparación Visual
□ ¿Hay 2 botones circulares abajo a la derecha?
□ **WhatsApp:** ¿Es verde #22c55e con ícono SVG? (NO emoji 💬)
□ **Teléfono:** ¿Es azul #0f4fa8 con ícono SVG? (NO emoji 📞)
□ ¿Los íconos se ven EXACTAMENTE iguales a index.html?

### Inspección Técnica
□ Click derecho en botón WhatsApp → "Inspect Element"
□ **VERIFICAR:** Clase es `floating-btn floating-whatsapp` (NO `.cta-btn`)
□ **VERIFICAR:** Dentro hay `<svg>` con `<path>`, NO emoji

**❌ Si los botones usan emojis o se ven diferentes → DETENTE y pide corrección**

---

## 🎨 4. ELEMENTOS VISUALES (Cajas de colores)

□ Scroll por toda la página nueva
□ **VERIFICAR:** ¿NO hay cajas amarillas (#fef3c7)?
□ **VERIFICAR:** ¿NO hay cajas rojas (#fee2e2)?
□ **VERIFICAR:** ¿NO hay cajas azules/verdes con bordes de colores?
□ Los únicos colores deben ser del brand (naranja #F97316 y azul)

**❌ Si ves cajas de colores que NO están en index.html → DETENTE y pide corrección**

---

## 📱 5. RESPONSIVE (Móvil)

□ Achica la ventana de Safari a tamaño móvil (≈375px de ancho)
□ ¿El menú hamburguesa aparece y funciona?
□ ¿El hero se ve bien en móvil?
□ ¿Los botones flotantes NO se solapan con contenido?
□ ¿Todo el texto es legible?

---

## 🔍 6. SEO Y METADATA (Opcional pero recomendado)

□ Click derecho → "View Page Source"
□ Busca `<title>` - ¿Tiene menos de 60 caracteres?
□ Busca `<meta name="description">` - ¿Tiene 120-155 caracteres?
□ Busca `@type": "Article"` o `"Service"` - ¿Existe schema JSON-LD?

---

## ✅ DECISIÓN FINAL

**SI TODAS LAS VERIFICACIONES PASARON:**
```bash
✅ TODO CORRECTO → Procede con:
   "git add ."
   "git commit -m 'feat: [descripción]'"
```

**SI ENCONTRASTE ERRORES:**
```bash
❌ HAY DIFERENCIAS → Reporta a Claude:
   "Encontré estos errores:
   - [lista específica de lo que está mal]
   Por favor corrígelos antes del commit"
```

---

## 💡 Tips de Eficiencia

1. **Primera vez:** Este checklist toma ~2 minutos
2. **Con práctica:** Lo reduces a ~30 segundos
3. **Beneficio:** Evitas 5+ commits de correcciones posteriores
4. **Regla de oro:** Si algo se ve diferente a index.html → está mal

---

## 📋 Resumen Rápido de Errores Comunes

| Error | Señal Visual | Solución |
|-------|--------------|----------|
| Hero incorrecto | Tubería con overlay oscuro | Debe usar `<picture>` y hero-plomero-visita |
| Botones incorrectos | Emojis 💬 📞 | Deben ser SVG icons profesionales |
| Cajas amarillas/rojas | Elementos con fondos de color | Eliminar - no existen en index.html |
| Imagen equivocada | Se ve diferente al homepage | Cambiar por hero-plomero-visita-*.webp |

---

**Última actualización:** Enero 2025
**Basado en:** 5 commits de correcciones del artículo "Como Identificar Buen Plomero"
