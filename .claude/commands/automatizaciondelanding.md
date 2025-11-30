# Automatización de Landing Pages

Crea la estructura base de una landing page automáticamente. Requiere pasos manuales para personalización del contenido SEO.

## Uso

```
/automatizaciondelanding "Nombre del Servicio"
```

**Ejemplos:**
- `/automatizaciondelanding "Plomero 24 Horas"`
- `/automatizaciondelanding "Plomero de Emergencia"`
- `/automatizaciondelanding "Plomero Urgente"`

---

## Lo que hace automáticamente

1. Genera el slug del servicio (ej: "plomero-24-horas")
2. Crea config.json con contenido placeholder
3. Copia el template v2.0.0 base
4. **Corrige paths relativos para subdirectorio** (CSS, fonts, imágenes, links)
5. Valida y crea imágenes faltantes (1200w desde 800w)
6. Verifica que el HTML sea válido
7. Abre el resultado en el navegador

## Pasos que requieren intervención manual

8. **Generar contenido SEO**: Debes usar `generador-seo.md` para crear title, description, keywords y 4 benefits personalizados
9. **Aplicar contenido al HTML**: Debes usar `@agentconstructor` con el config.json para reemplazar las 21 secciones

**Tiempo estimado: 10-15 minutos** (incluye pasos manuales)

---

## Ejecución

Cuando ejecutes este comando, verás:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOMATIZACIÓN DE LANDING INICIADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Servicio: {nombre del servicio}
 Slug: {slug generado}

[PASO 1/7] Generando slug...
 Slug creado

[PASO 2/7] Generando contenido SEO con IA...
  Generador SEO pendiente - Usando placeholder

[PASO 3/7] Creando config.json...
 config.json creado

[PASO 4/7] Copiando template v2.0.0...
 Template copiado

[PASO 4.5/7] Corrigiendo paths para subdirectorio...
  ✓ CSS externo: styles.min.css → /styles.min.css
  ✓ Fonts: assets/fonts/ → /assets/fonts/
  ✓ Imágenes srcset: assets/images/ → /assets/images/
  ✓ Imágenes src: assets/images/ → /assets/images/
  ✓ Links servicios: ./servicios/ → /servicios/
 Paths corregidos (5 tipos)

[PASO 5/7] Aplicando contenido con agentconstructor...
  Agentconstructor pendiente - Requiere integración manual
  Por ahora, usa: @agentconstructor con el config.json

[PASO 6/7] Validando imágenes...
 Imágenes validadas

[PASO 7/7] Validando HTML...
 HTML validado

 LANDING CREADA EXITOSAMENTE
 Ubicación: servicios/{slug}/index.html
 Tiempo: {X} segundos
```

---

## Requisitos

Antes de ejecutar, asegúrate de tener:

1. Template base en: `index.html` (página principal https://plomeroculiacanpro.mx/)
2. Script ejecutable: `scripts/crear-landing-auto.sh`
3. Imagen hero en: `assets/images/optimizadas/{slug}-culiacan-800w.webp`

**Importante:** Este comando crea la estructura base. Necesitarás completar manualmente:
- Generación de contenido SEO con `generador-seo.md`
- Aplicación del contenido con `@agentconstructor`

---

## Flujo interno

Este comando ejecuta el script `scripts/crear-landing-auto.sh` que:
1. Genera el slug automáticamente
2. Crea config.json con contenido placeholder (SEO pendiente)
3. Copia template v2.0.0
4. **Corrige paths relativos** (CSS, fonts, imágenes, links a servicios)
5. Muestra warning sobre agentconstructor (requiere manual)
6. Valida imágenes (crea 1200w desde 800w si falta)
7. Valida estructura HTML
8. Abre el navegador

**Pasos manuales posteriores:**
- Usar `generador-seo.md` para contenido SEO optimizado
- Usar `@agentconstructor` para aplicar contenido al HTML

---

## Notas

- El slug se genera automáticamente desde el nombre del servicio
- La imagen hero debe llamarse: `{slug}-culiacan-800w.webp`
- Si falta la imagen 1200w, se crea automáticamente desde la 800w
- El resultado se guarda en: `servicios/{slug}/`
- **Paths corregidos automáticamente:**
  - `styles.min.css` → `/styles.min.css`
  - `assets/fonts/` → `/assets/fonts/`
  - `assets/images/` → `/assets/images/`
  - `./servicios/` → `/servicios/`

## Limitaciones Actuales

**El script crea una landing base, pero requiere pasos manuales para completarla:**

1. **Contenido SEO placeholder**: El config.json se crea con contenido genérico. Debes generar contenido optimizado manualmente usando:
   - Comando: Llamar a `generador-seo.md` con el nombre del servicio
   - Editar: `servicios/{slug}/config.json` con el contenido generado

2. **HTML sin personalizar**: El index.html es una copia exacta del template. Debes aplicar el contenido usando:
   - Comando: `@agentconstructor` con path `servicios/{slug}/`
   - El agente leerá config.json y reemplazará las 21 secciones

**Workflow completo recomendado:**
```bash
# 1. Ejecutar automatización
/automatizaciondelanding "Nombre del Servicio"

# 2. Generar contenido SEO (manual)
# Usar generador-seo.md para crear contenido optimizado
# Actualizar servicios/{slug}/config.json

# 3. Aplicar contenido al HTML (manual)
@agentconstructor servicios/{slug}/

# 4. Validar resultado
./validate-landing.sh servicios/{slug}/index.html
```
