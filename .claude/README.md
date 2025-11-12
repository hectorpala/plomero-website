# Configuración de Claude Code - Plomero Culiacán Pro

**Proyecto**: plomeroculiacanpro.mx
**Última actualización**: 12 de Noviembre, 2024
**Versión**: 1.0

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Agentes Especializados](#agentes-especializados)
3. [Permisos y Seguridad](#permisos-y-seguridad)
4. [Uso de Agentes](#uso-de-agentes)
5. [Configuración Local](#configuración-local)

---

## Visión General

Este proyecto utiliza **Claude Code** con agentes especializados para automatizar tareas específicas del desarrollo web y despliegue.

### Estructura de Configuración

```
.claude/
├── README.md                          # Este archivo (documentación general)
├── settings.local.json                # Configuración de permisos y directorios
└── agents/
    ├── README.md                      # Guía de generación de imágenes
    ├── gitops-publisher-turbo.md      # Despliegue automático
    ├── ui-ux-surgeon-turbo.md         # Modificaciones UI precisas
    ├── plumbing-image-prompts.md      # Generación de prompts (manual)
    ├── plumbing-image-generator.md    # Generación automática con API
    └── kitchen-image-prompt-generator.md # (No usado actualmente)
```

---

## Agentes Especializados

### 1. GitOps Publisher Turbo 🚀

**Archivo**: `agents/gitops-publisher-turbo.md`
**Color**: Rojo
**Modelo**: Claude Sonnet

**Propósito**:
Maneja despliegues a producción vía GitHub Pages sin tocar archivos de código. Especialista en operaciones git, workflows de GitHub y verificación de despliegues.

**Comandos disponibles**:

```bash
# Despliegue directo a main (merge fast-forward)
PUBLICA YA

# Crear PR y auto-merge (workflow completo)
PR AUTO

# Verificar estado del despliegue
STATUS
```

**Qué hace**:
- ✅ Operaciones git (fetch, pull, merge, push)
- ✅ Creación automática de Pull Requests
- ✅ Verificación de GitHub Pages deployment
- ✅ Entrega de URLs de producción con cache-busting (`?v=sha`)
- ❌ NUNCA modifica archivos de código

**Cuándo usar**:
- Tienes cambios listos en una rama y quieres desplegar
- Necesitas crear PR y mergear automáticamente
- Quieres verificar estado de despliegue en GitHub Pages

**Output esperado**:
```
- SHORT_SHA: a1b2c3d
- PROD_URL: https://plomeroculiacanpro.mx/?v=a1b2c3d
- PAGES_STATUS: deployed
```

---

### 2. UI/UX Surgeon Turbo 🎨

**Archivo**: `agents/ui-ux-surgeon-turbo.md`
**Color**: Azul
**Modelo**: Claude Sonnet

**Propósito**:
Modificaciones quirúrgicas y precisas de UI/UX con mínimos cambios. Opera en "modo turbo" haciendo solo las modificaciones exactas solicitadas en archivos específicos.

**Características**:
- ✅ Solo modifica lo explícitamente solicitado
- ✅ Solo toca archivos específicamente indicados
- ✅ Verifica estado actual antes de cambios
- ✅ Entrega diff mínimo y unificado
- ✅ Preview en localhost antes de commit
- ❌ NUNCA commit/push sin comando explícito

**Workflow estructurado**:
```
PLAN → EVIDENCIA → DIFF → VERIF POST → ESTADO GIT → LISTO
```

**Cuándo usar**:
- Cambiar color de un botón específico
- Ajustar padding/margin de una clase CSS
- Modificar alineación de un componente
- Tweaks UI precisos sin efectos colaterales

**Ejemplos**:
```
"Change the submit button color to blue in components/Form.jsx"
"Increase the padding on .header class to 20px in styles/main.css"
"Fix flexbox alignment in components/Navbar.vue"
```

**Ventajas**:
- Cambios quirúrgicos (minimal diff)
- Verificación antes y después
- Sin sorpresas ni cambios no solicitados

---

### 3. Plumbing Image Prompts 🖼️

**Archivo**: `agents/plumbing-image-prompts.md`
**Modelo**: Claude Sonnet

**Propósito**:
Genera prompts profesionales optimizados para DALL·E, Midjourney, Stable Diffusion. **No requiere API keys** - tú generas las imágenes manualmente.

**Qué hace**:
- ✅ Genera 10 prompts profesionales por petición
- ✅ Optimizados para fotorrealismo y contexto mexicano
- ✅ Incluye especificaciones técnicas (16:9, lighting, etc.)
- ✅ Adaptados al servicio solicitado (fugas, drenajes, boilers)

**Cuándo usar**:
- No tienes API keys de OpenAI/Stability AI
- Quieres control total sobre la generación
- Usas ChatGPT Plus o Midjourney manualmente
- Estás empezando o en fase de pruebas

**Workflow**:
```
1. User: "Necesito 10 imágenes para servicios de plomería"
2. Claude genera 10 prompts profesionales
3. Copias prompts a ChatGPT Plus/Midjourney
4. Descargas imágenes generadas
5. Claude las optimiza a WebP (420w, 800w, 1200w)
6. Claude genera HTML con picture elements
```

**Tipos de imágenes**:
- Hero images (plomero profesional, herramientas)
- Service cards (reparación, limpieza, mantenimiento)
- Blog headers (específicos por artículo)
- Before/After transformations

**Ver más**: Consulta `agents/README.md` para guía completa con ejemplos y mejores prácticas.

---

### 4. Plumbing Image Generator 🤖

**Archivo**: `agents/plumbing-image-generator.md`
**Modelo**: Claude Sonnet

**Propósito**:
Workflow completo automatizado: prompt → generación → descarga → WebP → HTML. **Requiere API keys** de OpenAI o Stability AI.

**Qué hace**:
- ✅ Genera prompt optimizado automáticamente
- ✅ Llama API de DALL·E 3 para generar imagen
- ✅ Descarga imagen generada
- ✅ Convierte a WebP (3 tamaños: 420w, 800w, 1200w)
- ✅ Entrega HTML con picture element listo para usar

**Cuándo usar**:
- Tienes API key de OpenAI (DALL·E 3)
- Quieres generación completamente automática
- Necesitas generar muchas imágenes rápidamente
- Estás en fase de producción

**Configuración requerida**:
```bash
# 1. Crear archivo .env
cp .env.example .env

# 2. Agregar API key
OPENAI_API_KEY=sk-proj-tu-key-aqui
```

**Costo aproximado**:
- DALL·E 3 HD (1792x1024): ~$0.08 por imagen
- 10 imágenes: ~$0.80 USD
- Sitio completo (25 imágenes): ~$2.00 USD

**Workflow**:
```
1. User: "Genera imagen de plomero reparando fuga"
2. Claude genera prompt optimizado
3. Llama API de DALL·E 3
4. Descarga imagen (1792x1024)
5. Convierte a 3 tamaños WebP
6. Entrega HTML listo
Total: ~60 segundos
```

---

### 5. Kitchen Image Prompt Generator 🍳

**Archivo**: `agents/kitchen-image-prompt-generator.md`
**Estado**: No usado actualmente (proyecto de cocinas)

Este agente fue configurado para un proyecto anterior de diseño de cocinas. Está disponible pero no se usa en el proyecto de plomería.

---

## Permisos y Seguridad

### Configuración de Permisos

**Archivo**: `settings.local.json`

El proyecto tiene configurados permisos específicos para operaciones seguras:

**Comandos permitidos (allow)**:
```json
{
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git restore:*)",
      "Bash(cwebp:*)",
      "Bash(find:*)",
      "Bash(ls:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(awk:*)",
      "Bash(shasum:*)",
      "Bash(tree:*)",
      "Read(//Users/hectorpc/Documents/**)"
    ],
    "deny": [],
    "ask": []
  }
}
```

**Directorios adicionales**:
```json
"additionalDirectories": [
  "/Users/hectorpc/Downloads",     # Para imágenes generadas
  "/opt/homebrew/bin"              # Para herramientas (cwebp, etc.)
]
```

### Archivos Protegidos (.gitignore)

Los siguientes archivos de configuración **NO se suben a GitHub**:

```
.env                    # API keys (OpenAI, Stability AI)
client_secret.json      # Credenciales OAuth Google
token.json              # Token de autenticación Google
settings.local.json     # Configuración local de Claude
*.log                   # Logs de operaciones
.DS_Store              # Archivos macOS
```

---

## Uso de Agentes

### Opción 1: Invocación Automática

Claude invoca automáticamente el agente correcto basándose en tu petición:

```bash
# Despliegue automático → gitops-publisher-turbo
User: "PUBLICA YA"

# Modificación UI → ui-ux-surgeon-turbo
User: "Cambia el color del botón de enviar a azul en styles.css"

# Generación de imágenes → plumbing-image-prompts
User: "Necesito 5 prompts para imágenes de servicios"
```

### Opción 2: Invocación Explícita

También puedes invocar agentes específicamente:

```bash
# Usar agente de despliegue
User: "@gitops PUBLICA YA"

# Usar agente UI
User: "@ui-ux-surgeon aumenta el padding del header"

# Usar agente de prompts
User: "@plumbing-prompts genera imagen para hero section"
```

### Opción 3: Scripts NPM

Algunos agentes tienen scripts NPM asociados:

```bash
# Limpieza antes de desplegar
npm run clean

# Generar imagen con script helper
./scripts/generate-image.sh "Professional plumber..." output-name

# Enviar sitemap (relacionado con SEO automation)
npm run seo:submit-sitemap
```

---

## Configuración Local

### Paso 1: Clonar Configuración

```bash
# La carpeta .claude/ ya está en el repositorio
# settings.local.json es específico de tu máquina (gitignored)
```

### Paso 2: Configurar API Keys (Opcional)

Solo si usas `plumbing-image-generator`:

```bash
# 1. Crear archivo .env
cp .env.example .env

# 2. Editar y agregar API keys
nano .env

# Contenido:
OPENAI_API_KEY=sk-proj-...
```

### Paso 3: Configurar Google Search Console (Opcional)

Solo si usas `scripts/automation/seo/submit_sitemap.py`:

```bash
# 1. Crear proyecto en Google Cloud Console
# 2. Habilitar Search Console API
# 3. Descargar credenciales OAuth como client_secret.json
# 4. Ejecutar script (autoriza primera vez):
python3 scripts/automation/seo/submit_sitemap.py
```

### Paso 4: Verificar Permisos

```bash
# Verifica que Claude tiene acceso a directorios
ls -la ~/Downloads
ls -la /opt/homebrew/bin/cwebp
```

---

## Workflows Comunes

### Workflow 1: Agregar Nueva Imagen

**Opción A - Manual (sin API)**:
```
1. "Genera 3 prompts para imágenes de reparación de fugas"
2. Copiar prompts a ChatGPT Plus
3. Descargar imágenes a ~/Downloads
4. "Optimiza las 3 últimas imágenes de Downloads a WebP"
5. Claude convierte y actualiza HTML
```

**Opción B - Automática (con API)**:
```
1. "Genera imagen de plomero reparando fuga bajo lavabo"
2. Claude genera, descarga, optimiza y entrega HTML
3. Listo en ~60 segundos
```

### Workflow 2: Modificar UI

```
1. "Cambia el color del botón CTA a #E36414 en styles.css"
2. @ui-ux-surgeon hace cambio quirúrgico
3. Preview en localhost:5173
4. Si OK: "PUBLICA YA"
```

### Workflow 3: Desplegar a Producción

```
1. Terminas desarrollo en rama feature/nueva-seccion
2. "PUBLICA YA"
3. @gitops-publisher-turbo:
   - Hace merge a main
   - Push a GitHub
   - Verifica deployment
   - Entrega URL: https://plomeroculiacanpro.mx/?v=abc123d
4. Listo
```

### Workflow 4: Crear PR y Auto-merge

```
1. Terminas desarrollo
2. "PR AUTO"
3. @gitops-publisher-turbo:
   - Push rama actual
   - Crea PR
   - Auto-merge con squash
   - Espera deployment
   - Entrega URLs
4. Listo
```

---

## Troubleshooting

### Error: "No se pudo generar imagen"

**Causa**: API key no configurada o sin créditos

**Solución**:
```bash
# Verificar API key
cat .env | grep OPENAI_API_KEY

# Verificar créditos en OpenAI
# https://platform.openai.com/account/usage
```

### Error: "Permission denied en cwebp"

**Causa**: cwebp no instalado o no en PATH

**Solución**:
```bash
# Instalar cwebp con Homebrew
brew install webp

# Verificar instalación
which cwebp
```

### Error: "Git push failed"

**Causa**: Rama protegida o conflictos

**Solución**:
```bash
# Opción 1: Usar PR AUTO en vez de PUBLICA YA
"PR AUTO"

# Opción 2: Resolver conflictos manualmente
git pull origin main
# Resolver conflictos
git push
```

### Agente no se invoca automáticamente

**Causa**: Comando no reconocido

**Solución**:
```bash
# Invocar explícitamente
"@gitops PUBLICA YA"
"@ui-ux-surgeon cambia el color"
"@plumbing-prompts genera 5 prompts"
```

---

## Mejores Prácticas

### DO ✅

- **Usa comandos claros**: "PUBLICA YA", "PR AUTO", "STATUS"
- **Sé específico con UI**: "Cambia el color del botón submit a #E36414 en styles.css"
- **Genera prompts primero**: Antes de usar API, genera prompts y revísalos
- **Usa @agente**: Cuando quieras forzar un agente específico
- **Limpia antes de desplegar**: `npm run clean` antes de "PUBLICA YA"

### DON'T ❌

- **No commits manuales con agentes**: Los agentes manejan git, déjalos trabajar
- **No modifiques settings.local.json directamente**: Usa interfaz de Claude
- **No subas .env a GitHub**: NUNCA - contiene API keys
- **No uses agentes para tareas generales**: Son especializados, úsalos correctamente
- **No ignores verificaciones**: Los agentes verifican estado, revisa su output

---

## Recursos

### Documentación Claude Code
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Agent Configuration](https://docs.anthropic.com/claude-code/agents)
- [Permissions System](https://docs.anthropic.com/claude-code/permissions)

### APIs Usadas
- [OpenAI DALL·E 3](https://platform.openai.com/docs/guides/images)
- [Google Search Console API](https://developers.google.com/webmaster-tools)
- [GitHub REST API](https://docs.github.com/en/rest)

### Herramientas
- [cwebp Documentation](https://developers.google.com/speed/webp/docs/cwebp)
- [Git Documentation](https://git-scm.com/doc)

---

## Changelog

### Versión 1.0 - 12 de Noviembre, 2024
- ✅ Documentación inicial de configuración Claude
- ✅ 5 agentes documentados:
  - gitops-publisher-turbo (despliegue)
  - ui-ux-surgeon-turbo (modificaciones UI)
  - plumbing-image-prompts (generación manual)
  - plumbing-image-generator (generación automática)
  - kitchen-image-prompt-generator (no usado)
- ✅ Permisos y seguridad documentados
- ✅ Workflows comunes documentados
- ✅ Troubleshooting agregado

---

## Contacto Técnico

**Proyecto**: Plomero Culiacán Pro
**Desarrollador**: Claude AI Assistant
**Última actualización**: 12 de Noviembre, 2024
**Versión de documentación**: 1.0
