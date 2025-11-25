# Landing Page: Mantenimiento de Boiler en Culiacán

## 📋 Archivos en este directorio

1. **INSTRUCCIONES-COMPLETAS.md** - TODO el contenido SEO (meta tags, FAQs, testimonios, etc.)
2. **RESUMEN-PROYECTO.md** - Overview del proyecto completo
3. **schema-jsonld-completo.json** - JSON-LD para copiar al `<head>`
4. **index-nuevo.html** - Placeholder temporal (NO usar en producción)
5. **index.html** - Archivo actual (DEBE reemplazarse)
6. **index.html.backup-YYYYMMDD** - Backup del archivo anterior

---

## 🚨 Próximos Pasos (CRÍTICO)

### Paso 1: Copiar el GOLDEN TEMPLATE

```bash
# Navega al directorio raíz del proyecto
cd "/Users/hectorpc/Documents/Hector Palazuelos/Google My Business/plomero culiacan pro"

# Copia el golden template
cp plomero-de-emergencia/index.html servicios/mantenimiento-de-boiler/index.html
```

### Paso 2: Editar SOLO el contenido

Abre `servicios/mantenimiento-de-boiler/index.html` y reemplaza:

1. **En `<head>`:**
   - `<title>` → "Mantenimiento de Boiler en Culiacán | Diagnóstico Gratis 24/7"
   - `<meta name="description">` → Ver en INSTRUCCIONES-COMPLETAS.md
   - Bloque `<script type="application/ld+json">` → Copiar de schema-jsonld-completo.json
   - Imagen preload → `before-after-water-heater-boiler-1200w.webp`

2. **Hero Section (`<header class="hero">`):**
   - `<h1>` → "Mantenimiento de Boiler en Culiacán – Diagnóstico Gratis"
   - Subtitle (`.hero-subtitle`) → Ver en INSTRUCCIONES-COMPLETAS.md
   - 3 feature items → Diagnóstico gratis, Garantía 6 meses, Técnicos certificados
   - WhatsApp link text → "Solicitar Diagnóstico Gratuito"

3. **Benefits Section (4 tarjetas):**
   - Mantén los SVG icons exactos
   - Cambia SOLO los títulos (h3) y textos (p)
   - Ver contenido en INSTRUCCIONES-COMPLETAS.md

4. **Services Section (4 tarjetas):**
   - Cambiar títulos y descripciones
   - Alt text de imágenes específico
   - Ver INSTRUCCIONES-COMPLETAS.md

5. **FAQs (10 preguntas):**
   - Reemplazar TODAS las preguntas y respuestas
   - Ver texto completo en INSTRUCCIONES-COMPLETAS.md
   - Deben coincidir con el JSON-LD

6. **Testimonials (4 testimonios):**
   - Cambiar nombres, colonias y experiencias
   - Ver INSTRUCCIONES-COMPLETAS.md

### Paso 3: NO cambiar

❌ **NO cambies:**
- Estructura HTML
- CSS inline en `<style>` del `<head>`
- Glassmorphism del hero
- Rating badge de Google
- Navegación `<nav>`
- Footer `<footer>`
- Floating CTAs (WhatsApp + Phone)
- JavaScript al final del `<body>`
- Secciones como: Zonas de Servicio, SEO Links, Contacto

✅ **Solo cambias:**
- Textos dentro de los elementos existentes
- Contenido de FAQs
- Testimonios
- Títulos y descripciones

---

## 📊 Información de la Keyword

- **Keyword principal:** "mantenimiento de boiler en culiacán"
- **Volumen mensual:** ~1,800 búsquedas
- **Dificultad:** Media-Baja (poca competencia con páginas dedicadas)
- **Intención:** Transaccional (usuarios buscando contratar servicio)

**Keywords secundarias:**
- limpieza de boiler culiacán
- mantenimiento preventivo boiler
- cambio ánodo magnesio
- servicio boiler profesional

---

## ✅ Checklist de Implementación

Antes de publicar, verifica:

- [ ] HTML copiado de `/plomero-de-emergencia/index.html`
- [ ] H1 cambiado a "Mantenimiento de Boiler..."
- [ ] Meta description actualizada
- [ ] Schema JSON-LD reemplazado (10 FAQs)
- [ ] 4 benefits con SVG icons (NO emojis)
- [ ] 10 FAQs completas (no solo 3-5)
- [ ] 4 testimonios actualizados
- [ ] Imagen hero actualizada (before-after-water-heater-boiler)
- [ ] WhatsApp links funcionan correctamente
- [ ] Tel links funcionan (667 163 1231)
- [ ] Floating CTAs visibles (WhatsApp + Phone)

---

## 🧪 Testing Post-Implementación

1. **Validación técnica:**
   ```bash
   # PageSpeed Insights
   https://pagespeed.web.dev/

   # Rich Results Test (Schema)
   https://search.google.com/test/rich-results

   # Mobile-Friendly Test
   https://search.google.com/test/mobile-friendly
   ```

2. **Pruebas funcionales:**
   - [ ] Hero se ve correctamente en desktop y mobile
   - [ ] Rating badge de Google visible
   - [ ] Glassmorphism aplicado (fondo borroso)
   - [ ] FAQs se expanden al hacer click
   - [ ] Formulario envía a WhatsApp
   - [ ] Floating CTAs visibles y funcionan
   - [ ] Imágenes cargan en WebP
   - [ ] Mobile navigation funciona

3. **SEO:**
   - [ ] Agregar URL a sitemap.xml
   - [ ] Enviar a Google Search Console
   - [ ] Solicitar indexación manual
   - [ ] Verificar que el schema aparece sin errores

---

## 📈 Métricas a Monitorear

**Semana 1-2:**
- Indexación en Google
- Impresiones en Search Console

**Mes 1:**
- Posición para "mantenimiento de boiler culiacán"
- CTR en SERPs
- Primeros clicks orgánicos

**Mes 3:**
- Leads generados desde la página
- Conversión de visitas a WhatsApp/Tel
- Posicionamiento top 10

---

## 🎯 Objetivo Final

**Posicionarse en Top 3 de Google para:**
- "mantenimiento de boiler culiacán"
- "limpieza de boiler culiacán"
- "servicio de boiler culiacán"

**Generar:**
- 5-10 leads cualificados por mes
- Autoridad sobre el tema de mantenimiento de boilers
- Contenido reutilizable para redes sociales y Google Business

---

## 📞 Datos de Contacto (NAP)

Verificar que estén consistentes en TODA la página:

- **Teléfono:** 667 163 1231
- **WhatsApp:** 667 163 1231
- **Horario:** Lunes a Domingo · 24/7 Emergencias
- **Cobertura:** Todas las colonias de Culiacán, Sinaloa

---

## 🔗 Enlaces Importantes

- **Golden Template:** `/plomero-de-emergencia/index.html`
- **Arquitectura:** `/formatoparacrearurlplomer.md`
- **Contenido completo:** `INSTRUCCIONES-COMPLETAS.md`
- **Schema JSON-LD:** `schema-jsonld-completo.json`

---

## ⚠️ Recordatorio Final

**EL GOLDEN TEMPLATE ES OBLIGATORIO**

No inventes una estructura nueva. Copia exactamente la de `/plomero-de-emergencia/index.html` y cambia SOLO el contenido (textos, no estructura).

Cuando tengas duda: **copia del golden template**.

---

_Última actualización: 2025-11-23_
