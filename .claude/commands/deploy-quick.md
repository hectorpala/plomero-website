# Deploy Quick

Automatiza el proceso completo de publicación a producción (GitHub Pages) con commit inteligente y monitoreo de deployment.

## Qué hace este comando

1. **Detecta cambios** - Analiza `git status` para identificar archivos modificados
2. **Genera commit message inteligente** - Crea mensaje usando Conventional Commits basado en los cambios
3. **Publica a GitHub** - Ejecuta `git add`, `git commit`, `git push`
4. **Monitorea deployment** - Verifica que GitHub Actions complete exitosamente
5. **Confirma producción** - Valida que los cambios estén live en plomeroculiacanpro.mx

## Instrucciones para Claude

Cuando el usuario ejecute `/deploy-quick`, sigue estos pasos:

### Paso 1: Analizar cambios (git status)

Ejecuta estos comandos en paralelo:
```bash
git status --short
git diff --stat
```

Identifica:
- Archivos nuevos (?? o A)
- Archivos modificados (M)
- Archivos eliminados (D)
- Tipo de archivos (HTML, CSS, JS, imágenes, fonts, schemas, etc.)

### Paso 2: Generar commit message inteligente

Usa **Conventional Commits** format: `<type>(<scope>): <description>`

#### Types (por prioridad):

- **feat** - Nueva funcionalidad, landing page, sección completa
  - Ejemplo: "feat(landing): nueva página plomero-de-emergencia con SEO optimizado"
  - Ejemplo: "feat(schemas): LocalBusiness con GPS en 30 páginas colonias"

- **perf** - Optimización performance (LCP, CLS, carga, bundle size)
  - Ejemplo: "perf(fonts): font subsetting -37KB payload"
  - Ejemplo: "perf(html): minification -19KB sin cambios visuales"

- **fix** - Corrección de bug, error, problema visible
  - Ejemplo: "fix(mobile): logo no visible en viewport <375px"
  - Ejemplo: "fix(schema): JSON-LD syntax error en FAQ"

- **style** - Cambios de diseño, CSS, colores, spacing (sin afectar funcionalidad)
  - Ejemplo: "style(hero): ajustar padding mobile 24px → 16px"
  - Ejemplo: "style(cta): cambiar color botón #0066cc → #0052a3"

- **refactor** - Refactorización código sin cambiar funcionalidad
  - Ejemplo: "refactor(css): consolidar media queries mobile"

- **docs** - Documentación (README, comments, markdown)
  - Ejemplo: "docs(readme): agregar instrucciones deployment"

- **chore** - Mantenimiento, dependencias, config
  - Ejemplo: "chore(deps): actualizar gh-pages action v4"

#### Scopes comunes:

- `seo` - Cambios SEO (meta tags, schemas, sitemap, keywords)
- `landing` - Landing pages (/plomero-24-horas/, /plomero-cerca-de-mi/)
- `schemas` - JSON-LD, structured data
- `fonts` - Font files, subsetting, preloading
- `html` - HTML structure, minification
- `css` - Stylesheets, critical CSS
- `mobile` - Mobile-specific fixes
- `images` - Image optimization, WebP conversion
- `perf` - Performance optimizations
- `branding` - Logo, WhatsApp, teléfono, marca

#### Estructura del mensaje completo:

```
<type>(<scope>): <descripción corta max 72 caracteres>

<body opcional: detalles, lista de cambios, contexto>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Reglas para generar el mensaje:

1. **Analiza los archivos cambiados** y determina el type correcto:
   - index.html minificado → `perf(html)`
   - Nueva landing page → `feat(landing)`
   - Logo actualizado → `style(branding)` o `fix(branding)`
   - Schemas JSON-LD → `feat(schemas)` o `fix(schemas)`
   - Fonts subsetting → `perf(fonts)`

2. **Description debe ser concreta y específica:**
   - ❌ "actualizar archivos"
   - ✅ "minify HTML -19KB sin cambios visuales"
   - ❌ "mejorar SEO"
   - ✅ "agregar LocalBusiness schema con GPS a 30 colonias"

3. **Body (opcional)** incluir si:
   - Múltiples cambios relacionados (listarlos con bullets)
   - Métricas importantes (-X KB, +Y páginas, performance score)
   - Contexto necesario para entender el cambio

4. **Siempre terminar con:**
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

### Paso 3: Ejecutar git workflow

Usa **heredoc** para el mensaje completo:

```bash
git add . && git commit -m "$(cat <<'EOF'
<type>(<scope>): <descripción>

<body opcional>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)" && git push
```

**IMPORTANTE:**
- Ejecutar los 3 comandos juntos con `&&`
- Si alguno falla, detener proceso y reportar error
- NO usar `--no-verify` (respetar hooks)

### Paso 4: Monitorear GitHub Actions

Después de `git push`, ejecutar:

```bash
gh run list --limit 1
```

Esperar 5 segundos y verificar status:

```bash
gh run list --limit 1 --json status,conclusion,displayTitle
```

Status posibles:
- `queued` - Esperando inicio
- `in_progress` - Ejecutando
- `completed` - Terminado (verificar conclusion)

Conclusion posibles (si completed):
- `success` ✅ - Deployment exitoso
- `failure` ❌ - Error en deployment
- `cancelled` ⚠️ - Cancelado

**Esperar hasta que status = completed** (máximo 60 segundos, checar cada 5s)

### Paso 5: Confirmar deployment exitoso

Si conclusion = success:

```
✅ Deployment exitoso

Commit: <hash> - <mensaje>
GitHub Actions: ✅ success (build + deploy completados)
Producción: https://plomeroculiacanpro.mx/

Cambios publicados en ~30 segundos.
```

Si conclusion = failure:

```
❌ Deployment falló

Ver logs: gh run view --log
```

### Manejo de errores

#### Error: No hay cambios (git status vacío)

```
ℹ️ No hay cambios para publicar

git status: limpio
```

Detener proceso, no crear commit vacío.

#### Error: git push falló (sin autenticación, permisos, etc.)

```
❌ Error en git push

<mensaje de error>

Verificar:
- Credenciales GitHub (gh auth status)
- Permisos del repositorio
- Conexión a internet
```

#### Error: Conflictos en push (remote tiene cambios)

```
❌ Conflicto: remote tiene cambios no sincronizados

Ejecutar:
  git pull --rebase
  /deploy-quick
```

## Ejemplos de uso

### Ejemplo 1: Optimización performance

```
Usuario: /deploy-quick

Claude:
📦 Cambios detectados:
  M index.html (minified, -19KB)
  M assets/fonts/inter-500.woff2 (subset, -9KB)

💬 Commit message:
  perf(html): minification + font subsetting -28KB

  - HTML minificado: 119KB → 100KB (-19KB)
  - Font subsetting: 47KB → 38KB (-9KB)
  - Sin cambios visuales

✅ Deployment exitoso
   Commit: a1b2c3d - perf(html): minification + font subsetting -28KB
   GitHub Actions: ✅ success
   Producción: https://plomeroculiacanpro.mx/
```

### Ejemplo 2: Nueva landing page

```
Usuario: /deploy-quick

Claude:
📦 Cambios detectados:
  A plomero-24-horas/index.html
  A assets/images/emergencia-hero.webp
  M sitemap.xml

💬 Commit message:
  feat(landing): nueva página plomero-24-horas con SEO optimizado

  - Keyword: "plomero 24 horas" (2,400 búsquedas/mes)
  - JSON-LD completo (Service + LocalBusiness + FAQ)
  - 10 FAQs únicas sobre emergencias
  - Hero optimizado con imagen WebP
  - Actualizado sitemap.xml

✅ Deployment exitoso
   Commit: d4e5f6g - feat(landing): nueva página plomero-24-horas
   GitHub Actions: ✅ success
   Producción: https://plomeroculiacanpro.mx/plomero-24-horas/
```

### Ejemplo 3: Fix de bug

```
Usuario: /deploy-quick

Claude:
📦 Cambios detectados:
  M index.html (logo path corregido)

💬 Commit message:
  fix(mobile): logo no visible en viewport <375px

  Corregir path absoluto /assets/images/logo.svg

✅ Deployment exitoso
   Commit: g7h8i9j - fix(mobile): logo no visible
   GitHub Actions: ✅ success
   Producción: https://plomeroculiacanpro.mx/
```

## Notas importantes

- **NO pedir confirmación** - El comando debe ejecutar automáticamente
- **Generar mensaje inteligente** - Analizar cambios para type/scope correcto
- **Esperar GitHub Actions** - No confirmar hasta que deployment complete
- **Reportar problemas** - Si hay errores, mostrar claramente qué falló
- **Respetar hooks** - NO usar --no-verify

## Flujo completo (timing)

1. git status + diff (2s)
2. Generar commit message (1s)
3. git add + commit + push (3s)
4. Monitorear GitHub Actions (20-30s)
5. Confirmar deployment (1s)

**Total: ~30-40 segundos** (vs 2-3 minutos manual)
