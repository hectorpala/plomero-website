# Comando: /weekly-report

Genera un reporte ejecutivo semanal con métricas, highlights y proyecciones.

## Uso

```bash
/weekly-report
```

Genera reporte de la semana actual (lunes-domingo).

```bash
/weekly-report last
```

Genera reporte de la semana pasada.

```bash
/weekly-report 2024-11-18
```

Genera reporte de la semana que contiene esa fecha.

---

## Instrucciones para Claude

Cuando el usuario ejecute este comando:

### Paso 1: Determinar rango de fechas

Calcular inicio y fin de semana:

- **Esta semana**: Desde lunes 00:00 hasta domingo 23:59
- **Semana pasada**: 7 días atrás
- **Fecha específica**: Encontrar lunes y domingo de esa semana

### Paso 2: Obtener datos de Git

Ejecutar en paralelo:

```bash
# Commits de la semana
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --format="%h|%s|%an|%ar|%ad" --date=short --no-merges

# Estadísticas detalladas
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --shortstat --oneline --no-merges

# Archivos modificados agrupados
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --name-only --pretty=format: --no-merges | sort | uniq -c | sort -nr

# Actividad por día
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --format="%ad" --date=short --no-merges | sort | uniq -c
```

### Paso 3: Analizar y clasificar

**Por tipo de commit:**
- feat (features)
- perf (performance)
- fix (bugs)
- style (diseño)
- docs (documentación)
- otros

**Por categoría de archivos:**
- Landing pages nuevas
- Landing pages actualizadas
- Imágenes optimizadas
- Schemas agregados/actualizados
- Documentación
- Config (sitemap, robots.txt)

### Paso 4: Calcular métricas clave

**Productividad:**
- Total commits
- Commits por día (promedio)
- Archivos modificados
- Líneas de código (+/-)

**SEO & Content:**
- Páginas nuevas publicadas
- Keywords target (inferir de nombres de archivo)
- Schemas JSON-LD agregados
- FAQs creadas
- Blog posts publicados

**Performance:**
- Bundle size reduction (si hay commits perf)
- Imágenes optimizadas (JPG→WebP)
- Font subsetting

**Deployments:**
- Total deployments exitosos
- Deployments fallidos
- Tiempo promedio de deployment

### Paso 5: Generar reporte ejecutivo

Formato del reporte:

```markdown
# 📊 Reporte Semanal - Semana del [FECHA INICIO] al [FECHA FIN]

## 🎯 Resumen Ejecutivo

### Productividad
- **XX commits** realizados (promedio: X/día)
- **XX archivos** modificados
- **+X,XXX líneas** agregadas
- **-XXX líneas** eliminadas
- **XX deployments** exitosos a producción

### Impacto SEO
- **X páginas nuevas** publicadas (total: XX páginas live)
- **X,XXX búsquedas/mes** de keywords target agregadas
- **X schemas** JSON-LD implementados
- **XX FAQs** únicas creadas

### Optimizaciones
- **-XXX KB** reducción bundle size (-X%)
- **X imágenes** optimizadas a WebP
- **LCP mejorado**: X.Xs → X.Xs (-XX%)

---

## 📈 Highlights de la Semana

### 🚀 Nuevas Landing Pages (X)

1. **/plomero-24-horas/**
   - Keyword: "plomero 24 horas" (2,400 búsquedas/mes)
   - Schema: Service + LocalBusiness + FAQPage
   - FAQs: 10 únicas
   - Status: ✅ Live
   - URL: https://plomeroculiacanpro.mx/plomero-24-horas/

2. **/plomero-de-emergencia/**
   - Keyword: "plomero de emergencia" (1,800 búsquedas/mes)
   - Schema: Completo con GPS coordinates
   - Status: ✅ Live

3. **/plomero-cerca-de-mi/**
   - Keyword: "plomero cerca de mí" (3,200 búsquedas/mes)
   - Optimización: Geo tags + LocalBusiness schema
   - Status: ✅ Live

**Total keywords target agregadas: 7,400 búsquedas/mes**

### ⚡ Optimizaciones de Performance

#### Bundle Size Reduction
- Antes: XXX KB
- Después: XXX KB
- Ahorro: **-XXX KB (-XX%)**

Desglose:
- Font subsetting: -47KB
- Image optimization: -89KB
- HTML minification: -20KB

#### Core Web Vitals
- LCP: 2.1s → 1.4s (**-33% mejora**)
- CLS: 0.05 → 0.02 (-60%)
- FID: <100ms ✅

#### Imágenes Optimizadas (X)
- hero-plomero-visita: 122KB → 85KB (-30%)
- servicio-destape: 245KB → 98KB (-60%)
- [lista completa...]

### 🔍 SEO Improvements

#### Schemas JSON-LD
- **X schemas nuevos** agregados
- **X schemas** actualizados
- Tipos: Service (X), LocalBusiness (X), FAQPage (X), BreadcrumbList (X)

#### Content
- **XX FAQs** únicas agregadas
- **X breadcrumbs** implementados
- **Sitemap**: 18 → 22 páginas (+22%)

#### Meta Tags
- Open Graph completo en X páginas
- Twitter Cards agregadas: X páginas
- Canonical URLs: X páginas

---

## 📊 Análisis de Actividad

### Commits por Día

```
Lun 25 Nov: ████████ 8 commits
Mar 26 Nov: ██████ 6 commits
Mié 27 Nov: ███████████ 11 commits
Jue 28 Nov: ████ 4 commits
Vie 29 Nov: █████ 5 commits
Sáb 30 Nov: ██ 2 commits
Dom 01 Dic: █ 1 commit

Total: 37 commits
Promedio: 5.3 commits/día
Día más productivo: Miércoles (11 commits)
```

### Distribución de Trabajo

```
Features (feat):     60% ████████████
Performance (perf):  20% ████
Fixes (fix):         10% ██
Design (style):       5% █
Docs (docs):          5% █
```

### Top 5 Archivos Más Modificados

1. `plomero-de-emergencia/index.html` (5 commits, +847 líneas)
2. `sitemap.xml` (4 commits)
3. `.claude/commands/landing-creator.md` (3 commits, +105 líneas)
4. `assets/images/hero-*.webp` (6 archivos, optimizados)
5. `CHANGELOG.md` (2 commits)

---

## 🎯 Objetivos vs Resultados

### Objetivos de la Semana
- [ ] ~~Crear 5 landing pages~~ ✅ 4 completadas (80%)
- [x] Optimizar bundle size -100KB ✅ -156KB (156%)
- [x] Implementar schemas en todas las páginas ✅
- [ ] ~~Blog: 3 artículos~~ ❌ 0 completados (pendiente)

### Desviaciones
- Landing pages: -1 página (planeada para próxima semana)
- Performance: +56KB adicionales optimizados
- Blog: Pospuesto por prioridad en landing pages

---

## 💰 Impacto Estimado

### SEO Value
- **7,400 búsquedas/mes** agregadas (keywords target)
- Estimado CTR 3%: **222 visitas/mes** potenciales
- Tasa conversión 5%: **11 leads/mes** estimados

### Performance Savings
- **-156KB** bundle size
- Usuarios promedio: 1,000/mes
- Ahorro bandwidth: **156 MB/mes**

### Technical Debt
- **0 bugs críticos** pendientes
- **2 warnings** menores (no bloquean)
- Cobertura schemas: **100%** de páginas

---

## 📅 Calendario de Deployments

| Día | Deployments | Status | Tiempo Promedio |
|-----|-------------|--------|-----------------|
| Lun | 3 | ✅✅✅ | 28s |
| Mar | 2 | ✅✅ | 32s |
| Mié | 4 | ✅✅✅✅ | 29s |
| Jue | 1 | ✅ | 25s |
| Vie | 2 | ✅✅ | 31s |
| Sáb | 1 | ✅ | 27s |
| Dom | 0 | - | - |

**Total: 13 deployments exitosos, 0 fallidos**
**Promedio: 29 segundos por deployment**

---

## 📝 Commits Destacados

### 🏆 Commit de la Semana

**feat(landing): nueva página plomero-de-emergencia con SEO optimizado**
- Hash: `a1b2c3d`
- Fecha: 27 Nov 2024
- Impacto: +847 líneas, keyword 1,800 búsquedas/mes
- Why: Página más completa de la semana con schema perfecto

### 🚀 Performance Win

**perf(bundle): font subsetting + image optimization -156KB**
- Hash: `d4e5f6g`
- Impacto: -156KB total (-12% bundle size)
- LCP improvement: -700ms

### 🐛 Critical Fix

**fix(mobile): logo no visible en viewport <375px**
- Hash: `g7h8i9j`
- Impacto: 15% de usuarios móviles afectados
- Resolución: Mismo día reportado

---

## 🔮 Proyecciones para Próxima Semana

### Tareas Planeadas
- [ ] Crear 3 páginas de colonias (/colonia-guadalupe/, /colonia-centro/, /colonia-alameda/)
- [ ] Blog: 2 artículos ("Cómo elegir plomero confiable", "5 emergencias comunes")
- [ ] Optimizar 5 imágenes restantes JPG → WebP
- [ ] Agregar Twitter Cards a 4 páginas pendientes

### Métricas Objetivo
- 5-7 commits/día (mantener ritmo actual)
- 3 páginas nuevas mínimo
- -50KB bundle size adicional
- 2 blog posts publicados

### Riesgos Identificados
- ⚠️ Backlog blog creciendo (6 artículos pendientes)
- ⚠️ Algunas imágenes aún en JPG (5 pendientes)
- ✅ Sin riesgos técnicos críticos

---

## 📚 Aprendizajes de la Semana

### What Went Well
- ✅ Ritmo constante de commits (5.3/día)
- ✅ 0 deployments fallidos (13/13 exitosos)
- ✅ Performance gains superaron objetivo (+56%)
- ✅ Schemas 100% implementados

### What Could Be Better
- ⚠️ Blog posts atrasados (0/3 objetivo)
- ⚠️ Algunas landing pages tardaron 2 días (meta: 1 día)
- ⚠️ Twitter Cards no se agregaron consistentemente

### Action Items
- Priorizar blog en próxima semana
- Crear template de Twitter Cards para agilizar
- Documentar proceso de creación de landing page (reducir a 1 día)

---

**Generado automáticamente por Claude Code** 🤖
**Fecha de generación**: [TIMESTAMP]
```

### Paso 6: Ofrecer guardado y distribución

Preguntar al usuario:

```
📊 Reporte semanal generado

¿Qué quieres hacer con este reporte?

1. Guardar en .claude/reports/weekly-YYYY-WXX.md
2. Agregar resumen a CHANGELOG.md
3. Copiar a clipboard para compartir
4. Enviar por email (formato markdown)
5. Solo mostrar (no guardar)
```

### Paso 7: Generar gráficos ASCII (opcional)

Si hay suficientes datos, agregar visualizaciones:

```markdown
## 📊 Visualizaciones

### Productividad por Día de Semana

    Commits
    15 ┤
    12 ┤     ╭─╮
     9 ┤  ╭──╯ ╰╮
     6 ┤╭─╯     ╰─╮
     3 ┤╯         ╰─╮
     0 └─────────────╯
       L M M J V S D

### Bundle Size Evolution

    KB
    500 ┤╮
    400 ┤╰╮
    300 ┤ ╰╮
    200 ┤  ╰──────────
    100 ┤
      0 └────────────
        Inicio   Fin
        (-156KB)
```

---

## Notas importantes

- **Calcular métricas reales** desde Git, no estimaciones
- **Incluir URLs** de páginas nuevas para fácil verificación
- **Destacar achievements** significativos
- **Identificar riesgos** proactivamente
- **Proyecciones realistas** basadas en velocidad actual
- **Insights accionables** para próxima semana

---

## Frecuencia recomendada

- **Viernes EOD**: Revisar semana completa
- **Domingo noche**: Planear próxima semana
- **Mensual**: Compilar 4 reportes semanales

---

## Combinaciones útiles

```bash
# Viernes workflow
/daily-summary              # Resumen del viernes
/weekly-report              # Reporte semanal completo
/deploy-quick               # Último deploy de la semana

# Review mensual
/weekly-report 2024-11-04   # Semana 1
/weekly-report 2024-11-11   # Semana 2
/weekly-report 2024-11-18   # Semana 3
/weekly-report 2024-11-25   # Semana 4
```
