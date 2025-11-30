# Comando: /daily-summary

Genera un resumen detallado del trabajo realizado hoy basándose en los commits de Git.

## Uso

```bash
/daily-summary
```

O con fecha específica:

```bash
/daily-summary 2024-11-26
```

---

## Instrucciones para Claude

Cuando el usuario ejecute este comando:

### Paso 1: Obtener commits del día

Ejecutar en paralelo:

```bash
# Commits de hoy
git log --since="midnight" --format="%h|%s|%an|%ar" --no-merges

# Estadísticas de archivos
git log --since="midnight" --stat --oneline --no-merges

# Archivos modificados únicos
git log --since="midnight" --name-only --pretty=format: --no-merges | sort -u
```

Si el usuario especifica fecha, usar `--since="YYYY-MM-DD 00:00" --until="YYYY-MM-DD 23:59"`

### Paso 2: Clasificar commits por tipo

Agrupar commits según su prefijo (Conventional Commits):

- **feat**: Nuevas funcionalidades
- **perf**: Optimizaciones de performance
- **fix**: Correcciones de bugs
- **style**: Cambios de diseño
- **docs**: Documentación
- **refactor**: Refactorización
- **chore**: Mantenimiento

### Paso 3: Analizar archivos modificados

Clasificar archivos por categoría:

- **Landing pages**: `*.html` en raíz o subdirectorios específicos
- **Estilos**: `*.css`, archivos en `assets/css/`
- **Imágenes**: `*.webp`, `*.jpg`, `*.png`, `*.svg`
- **Schemas**: Archivos con JSON-LD
- **Documentación**: `*.md`, README
- **Config**: sitemap.xml, robots.txt, .gitignore

### Paso 4: Calcular métricas

- Total de commits
- Total de archivos modificados
- Líneas agregadas (+)
- Líneas eliminadas (-)
- Balance neto de líneas

### Paso 5: Generar reporte

Formato del reporte:

```markdown
# 📊 Resumen Diario - [FECHA]

## 🎯 Resumen Ejecutivo

- **Total commits:** X
- **Archivos modificados:** Y
- **Líneas agregadas:** +XXX
- **Líneas eliminadas:** -XXX
- **Balance neto:** ±XXX líneas

---

## 📝 Commits Realizados (X)

### ✨ Nuevas Funcionalidades (feat) - X commits

1. **feat(landing)**: nueva página plomero-de-emergencia con SEO optimizado
   - Hash: `a1b2c3d`
   - Archivos: plomero-de-emergencia/index.html, sitemap.xml
   - Cambios: +847 líneas

2. **feat(schemas)**: agregar LocalBusiness schema con GPS

### ⚡ Optimizaciones (perf) - X commits

1. **perf(images)**: optimización hero images WebP
   - Hash: `d4e5f6g`
   - hero-plomero-visita: 122KB → 85KB (-30%)

### 🐛 Correcciones (fix) - X commits

1. **fix(mobile)**: logo no visible en viewport <375px
   - Ajuste responsive en CSS mobile

### 🎨 Diseño (style) - X commits

### 📚 Documentación (docs) - X commits

### 🔧 Otros (refactor, chore) - X commits

---

## 📁 Archivos Modificados por Categoría

### Landing Pages (X archivos)
- ✅ `/plomero-de-emergencia/index.html` (nuevo, +547 líneas)
- ✏️ `/plomero-24-horas/index.html` (actualizado, +12 -5 líneas)
- ✏️ `/servicios/reparacion-fugas/index.html` (fix breadcrumbs)

### Imágenes (X archivos)
- 🖼️ `assets/images/hero-plomero-visita-800w.webp` (optimizado, -37KB)
- 🖼️ `assets/images/emergencia-hero.webp` (nuevo)

### Estilos (X archivos)
- 📝 `assets/css/styles.min.css` (minificado, -19KB)

### Schemas & SEO (X archivos)
- 🔍 `sitemap.xml` (18 → 22 páginas)

### Documentación (X archivos)
- 📄 `.claude/commands/landing-creator.md` (actualizado)
- 📄 `CHANGELOG.md` (actualizado)

---

## 📊 Métricas de Performance

### Bundle Size
- Antes: XXX KB
- Después: XXX KB
- Diferencia: -XX KB (-X%)

### Páginas Nuevas
- /plomero-de-emergencia/ (keyword: 1,800 búsquedas/mes)

### SEO Improvements
- X schemas agregados/actualizados
- X FAQs nuevas
- X breadcrumbs implementados

---

## ✅ Tareas Completadas Hoy

- [x] Crear landing page /plomero-de-emergencia/
- [x] Optimizar imágenes hero (WebP)
- [x] Fix responsive logo mobile
- [x] Actualizar sitemap.xml
- [x] Agregar schemas JSON-LD

---

## 📌 Pendientes para Mañana

Basándose en commits incompletos, errores mencionados, o TODOs en código:

- [ ] Agregar Twitter Cards a /plomero-de-emergencia/
- [ ] Revisar SEO score de /plomero-urgente/
- [ ] Convertir 2 imágenes JPG → WebP

---

## 🔗 Enlaces Útiles

- Producción: https://plomeroculiacanpro.mx/
- Última página modificada: [URL de la última landing page]
- GitHub Actions: [link si hay deployments]

---

**Generado automáticamente por Claude Code** 🤖
```

### Paso 6: Ofrecer guardado

Preguntar al usuario:

```
¿Quieres guardar este resumen?

Opciones:
  1. Guardar en .claude/logs/YYYY-MM-DD.md
  2. Agregar a CHANGELOG.md
  3. Ambos
  4. Solo mostrar (no guardar)
```

Si usuario elige 1 o 3:
- Crear directorio `.claude/logs/` si no existe
- Guardar con nombre `YYYY-MM-DD.md`

Si usuario elige 2 o 3:
- Agregar sección al inicio de CHANGELOG.md

### Paso 7: Generar insights (opcional)

Si hay datos suficientes, agregar sección de insights:

```markdown
## 💡 Insights del Día

- Velocidad promedio: X commits/hora
- Tipo de trabajo predominante: 60% features, 30% optimization, 10% fixes
- Mayor impacto: Reducción -94KB bundle size
- Páginas más trabajadas: /plomero-de-emergencia/ (3 commits)
```

---

## Ejemplos de uso

### Ejemplo 1: Resumen del día actual

```
Usuario: /daily-summary

Claude:
[Lee commits desde midnight]
[Genera reporte completo]

# 📊 Resumen Diario - 27 Nov 2024

## 🎯 Resumen Ejecutivo
- Total commits: 5
- Archivos modificados: 12
- Líneas agregadas: +1,247
- Líneas eliminadas: -89
- Balance neto: +1,158 líneas

[... resto del reporte ...]

¿Quieres guardar este resumen?
```

### Ejemplo 2: Resumen de fecha específica

```
Usuario: /daily-summary 2024-11-26

Claude:
[Lee commits del 26 de noviembre]
[Genera reporte de ese día]
```

### Ejemplo 3: Día sin commits

```
Usuario: /daily-summary

Claude:
📊 Resumen Diario - 27 Nov 2024

No se encontraron commits para hoy.

Última actividad: 26 Nov 2024 (ayer)
- 3 commits
- feat(landing): nueva página plomero-urgente
```

---

## Notas importantes

- **NO modificar archivos** sin confirmación del usuario
- **Solo leer commits de Git** - fuente de verdad
- **Respetar formato Conventional Commits** al clasificar
- **Incluir métricas reales** desde git log y git diff
- **Ser específico** con números de línea y archivos exactos
- **Generar insights útiles** basados en patrones del día

---

## Tips para el usuario

### Mejor momento para ejecutar
- Al final del día antes de cerrar
- Antes de hacer último commit
- Cada viernes para compilar la semana

### Combinaciones útiles
```bash
/daily-summary              # Ver resumen de hoy
/deploy-quick               # Publicar cambios
/daily-summary              # Actualizar resumen con último deploy
```

### Para revisión semanal
Ejecutar `/daily-summary` cada día y guardar en logs, luego:
```bash
cat .claude/logs/2024-11-*.md > resumen-noviembre.md
```
