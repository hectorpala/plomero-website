# Generador de Contenido SEO para Servicios de Plomería

Genera contenido SEO optimizado para un servicio de plomería en Culiacán.

## Input

Recibes:
- **Nombre del servicio**: Ej. "Reparación de Fugas"
- **Slug**: Ej. "reparacion-de-fugas"

## Output esperado

Debes generar contenido optimizado para SEO específico para servicios de plomería en Culiacán, Sinaloa, México.

### 1. **Title** (50-60 caracteres)
- Debe incluir el servicio + "Culiacán"
- Incluir un beneficio clave o valor agregado
- Entre 50-60 caracteres EXACTOS
- Ejemplo: `Reparación de Fugas Culiacán | Plomero Profesional`

### 2. **Meta Description** (120-155 caracteres)
- Emoji inicial 🔧
- Descripción del servicio
- Beneficio principal
- Call to action con teléfono 667 478 7021
- Entre 120-155 caracteres EXACTOS
- Ejemplo: `🔧 Reparación de fugas en Culiacán. Detección y reparación en el día. Garantía por escrito. ¡Llama: 667 478 7021!`

### 3. **Keywords** (6-8 keywords separadas por comas)
- Formato: keyword1 culiacan, keyword2 culiacan, plomero culiacan...
- Incluir variaciones long-tail
- Todas en minúsculas, sin acentos
- Ejemplo: `reparacion fugas culiacan, fugas de agua culiacan, plomero fugas culiacan, detectar fugas culiacan`

### 4. **H1** (título principal)
- Debe incluir el servicio + "Culiacán"
- Incluir beneficio clave
- Formato: "Servicio en Culiacán | Beneficio"
- Ejemplo: `Reparación de Fugas en Culiacán | Detección y Reparación Profesional`

### 5. **Subtitle** (hero subtitle - 1-2 líneas)
- Descripción del servicio
- Mencionar tipos o variantes del servicio
- Incluir garantía y profesionalismo
- 30-50 palabras
- Ejemplo: `Servicio profesional de reparación de fugas de agua en Culiacán. Detectamos y reparamos fugas en tuberías, llaves, inodoros y regaderas. Atención rápida y garantía por escrito.`

### 6. **WhatsApp Text**
- Texto corto para el mensaje de WhatsApp
- Solo el nombre del servicio en minúsculas
- Ejemplo: `reparación de fugas`

### 7. **Breadcrumb**
- Nombre corto para el breadcrumb
- Capitalizado
- Ejemplo: `Reparación de Fugas`

### 8. **Service Type** (para Schema.org)
- Nombre formal del servicio
- Capitalizado
- Ejemplo: `Reparación de Fugas de Agua`

### 9. **Schema Description**
- Descripción detallada para Schema.org
- 2-3 frases
- Mencionar tipos, beneficios y características
- 40-60 palabras
- Ejemplo: `Servicio profesional de reparación de fugas de agua en hogares y negocios. Detectamos y reparamos fugas en tuberías, llaves, inodoros y regaderas con equipo especializado y garantía de 6 meses.`

### 10. **Benefits** (4 benefits específicos del servicio)

Cada benefit debe tener:
- **title**: Título del beneficio (5-8 palabras)
- **description**: Descripción detallada (40-60 palabras) con datos concretos, cifras, o detalles técnicos

**Criterios para los benefits:**
1. **Específicos del servicio**: No genéricos, deben ser únicos para este servicio
2. **Con datos concretos**: Incluir números, porcentajes, tiempos, garantías
3. **Orientados a soluciones**: Resolver problemas específicos del cliente
4. **Profesionales**: Mostrar expertise y certificación

**Ejemplo de benefits para "Reparación de Fugas":**

```json
{
  "title": "Detección precisa con equipo profesional",
  "description": "Utilizamos equipo de detección de fugas por presión y sonido. Localizamos fugas ocultas en paredes, pisos y tuberías enterradas sin romper de más. Ahorro del 70% en costos de reparación vs métodos tradicionales."
}
```

---

## Formato de Output

Debes responder EXACTAMENTE en este formato JSON:

```json
{
  "seo": {
    "title": "Título aquí (50-60 chars)",
    "description": "Descripción aquí (120-155 chars)",
    "keywords": "keyword1, keyword2, keyword3..."
  },
  "content": {
    "h1": "H1 aquí",
    "subtitle": "Subtitle aquí (30-50 palabras)",
    "whatsapp_text": "texto whatsapp",
    "breadcrumb": "Breadcrumb",
    "service_type": "Service Type"
  },
  "schema": {
    "description": "Descripción Schema.org (40-60 palabras)"
  },
  "benefits": [
    {
      "title": "Benefit 1 title",
      "description": "Benefit 1 description (40-60 palabras)"
    },
    {
      "title": "Benefit 2 title",
      "description": "Benefit 2 description (40-60 palabras)"
    },
    {
      "title": "Benefit 3 title",
      "description": "Benefit 3 description (40-60 palabras)"
    },
    {
      "title": "Benefit 4 title",
      "description": "Benefit 4 description (40-60 palabras)"
    }
  ]
}
```

---

## Contexto del negocio

**Negocio**: Plomero Culiacán Pro
**Ubicación**: Culiacán, Sinaloa, México
**Zonas de servicio**: Las Quintas, Tres Ríos, Chapultepec, Montebello, Centro
**Teléfono**: 667 478 7021
**Rating**: 4.9★ en Google
**Clientes**: 200+ clientes satisfechos

**Valores clave a comunicar:**
- Servicio profesional y certificado
- Respuesta rápida (24/7 para emergencias)
- Garantía por escrito
- Precios justos y transparentes
- Experiencia comprobada

---

## Reglas importantes

1. **SIEMPRE incluir "Culiacán"** en title, description, h1, keywords
2. **Teléfono siempre es 667 478 7021**
3. **No usar emojis** excepto 🔧 en la meta description
4. **Benefits deben ser únicos** para cada servicio (no genéricos)
5. **Contar caracteres exactos** en title (50-60) y description (120-155)
6. **Keywords sin acentos** y en minúsculas
7. **Tone profesional** pero cercano
8. **Enfoque en soluciones** no en problemas
9. **Incluir garantía** cuando sea relevante
10. **Mencionar certificación** cuando aplique

---

## Ejemplos de servicios y sus características únicas

### Reparación de Fugas
- Focus: Detección, tuberías, ahorro agua, prevención daños
- Benefits: Equipo detección, reparación sin romper, mismo día, garantía

### Destape de Drenajes
- Focus: Velocidad, equipo hidráulico, prevención, cocinas/baños
- Benefits: Destape en 30min, equipo profesional, sin químicos, raíz/grasa

### Instalación de Calentadores
- Focus: Ahorro gas, seguridad, marcas, paso/depósito
- Benefits: Instalación certificada, ahorro 40%, marcas reconocidas, garantía

### Reparación de WC/Inodoros
- Focus: Fugas internas, mecanismos, ahorro agua, silencio
- Benefits: Repuestos originales, eliminar goteo, ahorro recibo, mismo día

### Instalación de Tinacos
- Focus: Capacidad, presión, materiales, ubicación
- Benefits: Cálculo correcto, instalación segura, conexiones garantizadas

### Plomería Comercial
- Focus: Negocios, restaurantes, locales, mantenimiento preventivo
- Benefits: Contrato mantenimiento, respuesta rápida, mínima interrupción

---

**IMPORTANTE**: Adapta los benefits según el tipo de servicio. Cada servicio debe tener benefits ÚNICOS y específicos.
