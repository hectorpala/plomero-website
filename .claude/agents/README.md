# Agentes Especializados - Plomero Culiacán Pro

Este directorio contiene agentes especializados para optimizar y mejorar el sitio web de plomería.

## 📋 Agentes Disponibles

## 🎯 Agentes de SEO y Contenido

### 1. `agente-seo` ⭐ NUEVO

**Qué hace:**
- Genera contenido SEO optimizado para páginas de colonias y servicios
- Crea meta descriptions, H1s, FAQs únicos
- Analiza contenido existente y sugiere mejoras
- Asegura 0% contenido duplicado

**Cuándo usar:**
- Necesitas crear páginas nuevas de colonias
- Quieres optimizar contenido existente
- Necesitas FAQs únicas para múltiples páginas
- Buscas mejorar rankings en Google

**Cómo usar:**
```
User: "Genera contenido SEO para la colonia Las Quintas"
→ Claude usa Task tool con agente-seo
→ Analiza docs existentes (auditorías, análisis)
→ Genera contenido único optimizado
→ Incluye: H1, meta, hero, FAQs, contenido único
→ Te da HTML listo para implementar

User: "Necesito 10 páginas de colonias con contenido único"
→ Agente genera 10 páginas completamente diferentes
→ Sin contenido duplicado
→ Keywords naturalmente integrados
→ Schema markup sugerido
```

**Capacidades:**
- ✅ Análisis de keywords y competencia
- ✅ Contenido 100% único para cada colonia
- ✅ FAQs optimizadas para schema markup
- ✅ Meta descriptions que convierten
- ✅ Enlaces internos estratégicos
- ✅ Local SEO (referencias a Culiacán)

## 🎨 Agentes de Generación de Imágenes

### 2. `plumbing-image-prompts` (Recomendado para empezar)

**Qué hace:**
- Genera prompts profesionales optimizados para DALL·E, Midjourney, Stable Diffusion
- No requiere API keys
- Tú generas las imágenes manualmente con los prompts

**Cuándo usar:**
- No tienes API keys de OpenAI/Stability AI
- Quieres control total sobre la generación
- Usas ChatGPT Plus o Midjourney manualmente

**Cómo usar:**
```
User: "Necesito 10 imágenes para servicios de plomería"
→ Claude usa Task tool con plumbing-image-prompts
→ Recibes 10 prompts listos para copiar/pegar
→ Los usas en ChatGPT Plus/Midjourney
→ Descargas las imágenes
→ Claude las optimiza a WebP
```

### 3. `plumbing-image-generator` (Avanzado)

**Qué hace:**
- Workflow completo: prompt → generación → descarga → WebP → HTML
- Requiere API keys (OpenAI o Stability AI)
- Automatiza todo el proceso

**Cuándo usar:**
- Tienes API key de OpenAI (DALL·E 3)
- Quieres generación automática sin intervención manual
- Necesitas generar muchas imágenes rápidamente

**Cómo usar:**
```
1. Configurar API key (ver sección abajo)
2. User: "Genera imagen de plomero reparando fuga"
→ Claude usa plumbing-image-generator
→ Genera prompt optimizado
→ Llama API de DALL·E
→ Descarga imagen
→ Convierte a WebP (420w, 800w, 1200w)
→ Te da HTML listo para usar
```

## 🔑 Configuración de API Keys

### Paso 1: Obtener API Key

**OpenAI (DALL·E 3) - Recomendado:**
1. Ve a https://platform.openai.com/api-keys
2. Crea una cuenta si no tienes
3. Genera un API key
4. Agrega crédito ($5-10 USD es suficiente para 50-100 imágenes)

**Costo aproximado:**
- DALL·E 3 HD (1792x1024): ~$0.08 por imagen
- 10 imágenes = ~$0.80 USD

**Stability AI (alternativa):**
1. Ve a https://platform.stability.ai/
2. Crea cuenta y genera API key
3. Más barato pero calidad variable

### Paso 2: Configurar en el proyecto

```bash
# 1. Copia el archivo de ejemplo
cp .env.example .env

# 2. Edita .env y agrega tu API key
nano .env  # o usa tu editor favorito

# Contenido del .env:
OPENAI_API_KEY=sk-proj-tu-key-aqui
```

**IMPORTANTE:** El archivo `.env` está en `.gitignore` - NUNCA se subirá a GitHub por seguridad.

### Paso 3: Verificar configuración

```bash
# Carga las variables
source .env

# Verifica que esté configurada
echo $OPENAI_API_KEY
# Debe mostrar: sk-proj-...
```

## 🚀 Guías de Uso

### Opción A: Workflow Manual (Sin API keys)

**Mejor para:** Empezar rápido, control total, sin costos de API

```
1. Pedir prompts a Claude:
   "Genera 5 prompts para imágenes de servicios de plomería"

2. Claude usa agente plumbing-image-prompts
   Te da 5 prompts profesionales

3. Copiar prompts a ChatGPT Plus:
   "Create an image: [pegar prompt aquí]"

4. Descargar imágenes generadas

5. Decir a Claude:
   "Descargué 5 imágenes en ~/Downloads, optimízalas a WebP"

6. Claude convierte y te da HTML para implementar
```

### Opción B: Workflow Automático (Con API keys)

**Mejor para:** Muchas imágenes, velocidad, automatización

```
1. Configurar API key (pasos arriba)

2. Pedir a Claude:
   "Genera imagen de plomero profesional para hero section"

3. Claude usa plumbing-image-generator:
   - Crea prompt optimizado
   - Llama DALL·E 3 API
   - Descarga imagen
   - Convierte a WebP (3 tamaños)
   - Te da HTML listo

4. Todo automatizado, ~60 segundos
```

### Opción C: Workflow Híbrido (Recomendado)

**Mejor para:** Balance entre control y automatización

```
1. Generar prompts con Claude (gratis)
2. Revisar y ajustar prompts a tu gusto
3. Usar script helper para generar:

   ./scripts/generate-image.sh "Professional plumber..." plumber-hero

4. Script hace:
   - Generación con DALL·E
   - Conversión a WebP
   - Te da HTML snippet
```

## 📝 Ejemplos Prácticos

### Ejemplo 1: Hero Image

```bash
# Usando el script helper
./scripts/generate-image.sh \
  "Professional Mexican plumber in clean blue uniform standing confidently in modern home, holding toolbox, natural daylight from window, photorealistic professional photography, trustworthy expression, 16:9 aspect ratio" \
  plumber-hero-professional

# Resultado:
# img/plumber-hero-professional-420w.webp
# img/plumber-hero-professional-800w.webp
# img/plumber-hero-professional-1200w.webp
```

### Ejemplo 2: Service Cards (6 imágenes)

```
1. User: "Necesito 6 imágenes para tarjetas de servicios"

2. Claude usa plumbing-image-prompts:
   - Leak repair
   - Drain cleaning
   - Boiler maintenance
   - Emergency service
   - Bathroom installation
   - Tool display

3. Generas en ChatGPT Plus o con script

4. Claude convierte todo a WebP y actualiza HTML
```

### Ejemplo 3: Blog Header

```
User: "Genera imagen para artículo sobre mantenimiento de boilers"

Claude:
1. Crea prompt específico para boiler
2. Genera con DALL·E (si tienes API)
3. Optimiza a WebP
4. Sugiere dónde usarla
```

## 🎨 Tipos de Imágenes que Puedes Generar

### Hero Images
- Plomero profesional (portrait)
- Plomero en acción
- Vista de herramientas profesionales

### Service Cards
- Reparación de fugas
- Limpieza de drenajes
- Mantenimiento de boiler
- Servicio de emergencia 24/7
- Instalación de sanitarios
- Detección de fugas

### Blog Headers
- Específicas por artículo
- Ilustraciones técnicas
- Diagramas explicativos

### Before/After
- Transformaciones de reparaciones
- Comparativas de servicios

### Customer Testimonials
- Cliente satisfecho con plomero
- Apretón de manos
- Trabajo completado

## 💡 Tips para Mejores Resultados

### DO ✅
- Sé específico con lighting ("natural window light", "bright daylight")
- Menciona "professional photography, photorealistic"
- Incluye "16:9 aspect ratio, sharp focus"
- Describe setting ("modern Mexican home", "Culiacán residence")
- Especifica attire ("clean blue uniform", "professional")

### DON'T ❌
- No uses palabras vagas ("nice", "good", "beautiful")
- Evita "stock photo" aesthetic
- No pidas poses artificiales
- No uses lighting oscuro o dramático
- No olvides el contexto mexicano

## 🔍 Troubleshooting

### "No se pudo generar la imagen"
- Verifica que API key esté en .env
- Revisa que tengas créditos en OpenAI
- Intenta simplificar el prompt

### "Imagen no se ve profesional"
- Agrega más detalles al prompt
- Incluye "professional photography"
- Especifica lighting explícitamente
- Usa DALL·E 3 HD quality

### "WebP muy grande"
- Ajusta quality en cwebp (-q 80 en vez de 85)
- Reduce tamaño de resize
- Verifica que imagen original no sea gigante

## 📊 Comparación de Opciones

| Aspecto | Manual | Script | Agente Full |
|---------|--------|--------|-------------|
| Costo | $0 (ChatGPT Plus) | ~$0.08/img | ~$0.08/img |
| Velocidad | 5-10 min/img | 1-2 min/img | 1 min/img |
| Control | Alto | Medio | Bajo |
| Automatización | Ninguna | Media | Alta |
| Requiere API | No | Sí | Sí |
| Mejor para | Empezar | Producción | Escala |

## 🎯 Recomendación de Uso

### Para SEO y Contenido
1. Usa `agente-seo` para todas las páginas nuevas
2. Revisa contenido existente y optimiza con el agente
3. Genera FAQs únicas para mejorar schema markup
4. Costo: $0 (incluido en Claude Code)

### Para Imágenes

**Para empezar:**
1. Usa `plumbing-image-prompts` (gratis, manual)
2. Genera 3-5 imágenes en ChatGPT Plus
3. Claude las optimiza a WebP

**Cuando tengas budget:**
1. Configura API key de OpenAI ($10)
2. Usa `plumbing-image-generator` o script
3. Genera todas las imágenes necesarias (~20 imágenes = $1.60)

**Para mantenimiento continuo:**
1. Usa script helper cuando necesites nuevas imágenes
2. ~1-2 imágenes/semana para blog
3. Costo: ~$0.32/mes

## 📚 Recursos

- [OpenAI API Docs](https://platform.openai.com/docs/guides/images)
- [DALL·E 3 Guide](https://platform.openai.com/docs/guides/images/usage)
- [Midjourney Docs](https://docs.midjourney.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## ❓ Preguntas Frecuentes

**P: ¿Cuánto cuesta generar imágenes con API?**
R: DALL·E 3 HD: ~$0.08/imagen. 10 imágenes = ~$0.80 USD.

**P: ¿Puedo usar las imágenes comercialmente?**
R: Sí, OpenAI permite uso comercial de imágenes DALL·E.

**P: ¿Qué tamaño de imágenes genero?**
R: DALL·E 3: 1792x1024 (16:9), luego convertimos a 420w, 800w, 1200w WebP.

**P: ¿Cuántas imágenes necesito para el sitio?**
R: Mínimo: 10-15 (hero + 6 servicios + 3-4 blog)
   Ideal: 25-30 (completo)

**P: ¿Puedo regenerar si no me gusta?**
R: Sí, ajusta el prompt y regenera. Cada intento cuesta $0.08.
