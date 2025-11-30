# Auditoría SEO Completa del Sitio

Interpreta reportes de Ahrefs Site Audit o Semrush Site Audit y genera un plan de acción priorizado.

## Uso

```
/auditoria-seo
```

Luego pega:
- El resumen del Health Score de Ahrefs/Semrush
- O el export CSV/JSON de errores
- O screenshots del dashboard

## Instrucciones para Claude

Cuando el usuario ejecute `/auditoria-seo`, guíalo paso a paso para obtener los datos y generar el plan de acción.

### Paso 1: Solicitar Datos del Audit

Pregunta al usuario:

```
Para generar tu plan de acción SEO, necesito los datos de tu auditoría.

¿Qué herramienta usaste?
1. Ahrefs Site Audit
2. Semrush Site Audit
3. Screaming Frog
4. Google Search Console
5. Otra

Pega aquí uno de los siguientes:
- Health Score y resumen de errores
- Export CSV de issues
- Screenshot del dashboard
- Lista de errores principales
```

### Paso 2: Parsear y Categorizar Errores

Clasifica los errores en estas categorías:

#### 2.1 Errores Técnicos Críticos (Impacto Alto)

| Error | Descripción | Impacto SEO |
|-------|-------------|-------------|
| **4xx Errors** | Páginas que devuelven 404, 410, etc. | Crítico - Google desindexará |
| **5xx Errors** | Errores de servidor | Crítico - Afecta crawl budget |
| **Redirect Chains** | Más de 1 redirect (A→B→C) | Alto - Pierde link juice |
| **Redirect Loops** | Redirects infinitos | Crítico - No indexable |
| **Canonical Issues** | Canonical apunta a página incorrecta | Alto - Contenido duplicado |
| **Hreflang Errors** | Conflictos en tags multiidioma | Alto - SEO internacional |
| **HTTPS Mixed Content** | HTTP resources en página HTTPS | Medio - Warnings navegador |
| **Missing SSL** | Páginas sin HTTPS | Crítico - Chrome marca inseguro |

#### 2.2 Crawlability & Indexación

| Error | Descripción | Impacto SEO |
|-------|-------------|-------------|
| **Orphan Pages** | Páginas sin enlaces internos | Alto - Difícil de encontrar |
| **Deep Pages** | Páginas a >3 clicks del home | Medio - Menor crawl priority |
| **Robots.txt Block** | Páginas importantes bloqueadas | Crítico - No indexadas |
| **Noindex Issues** | Páginas con noindex incorrecto | Crítico - No aparecen |
| **Sitemap Errors** | URLs en sitemap que dan 404 | Medio - Desperdicia crawl |
| **Crawl Depth** | Estructura muy profunda | Medio - SEO arquitectura |

#### 2.3 On-Page SEO

| Error | Descripción | Impacto SEO |
|-------|-------------|-------------|
| **Missing Title** | Sin `<title>` tag | Crítico - Google genera título |
| **Title Too Long** | >60 caracteres | Bajo - Se trunca en SERPs |
| **Title Too Short** | <30 caracteres | Bajo - Oportunidad perdida |
| **Duplicate Titles** | Mismo title en varias URLs | Alto - Canibalización |
| **Missing H1** | Sin heading principal | Alto - Estructura confusa |
| **Multiple H1** | Más de un H1 por página | Medio - Puede confundir |
| **Duplicate H1** | Mismo H1 en varias páginas | Alto - Canibalización |
| **Missing Meta Desc** | Sin meta description | Medio - Google genera snippet |
| **Duplicate Meta Desc** | Misma description repetida | Medio - Oportunidad perdida |
| **Missing Alt Text** | Imágenes sin alt | Medio - Accesibilidad + SEO |

#### 2.4 Performance & Core Web Vitals

| Métrica | Bueno | Necesita Mejora | Pobre |
|---------|-------|-----------------|-------|
| **LCP** (Largest Contentful Paint) | <2.5s | 2.5-4s | >4s |
| **FID** (First Input Delay) | <100ms | 100-300ms | >300ms |
| **CLS** (Cumulative Layout Shift) | <0.1 | 0.1-0.25 | >0.25 |
| **TTFB** (Time to First Byte) | <200ms | 200-500ms | >500ms |
| **Page Size** | <1MB | 1-3MB | >3MB |
| **Requests** | <50 | 50-100 | >100 |

#### 2.5 Content & Keywords

| Issue | Descripción | Acción |
|-------|-------------|--------|
| **Thin Content** | Páginas con <300 palabras | Expandir o consolidar |
| **Keyword Cannibalization** | Varias URLs compitiendo por misma keyword | Elegir URL principal |
| **Content Gaps** | Keywords de competidores que no tienes | Crear contenido nuevo |
| **Declining Pages** | URLs perdiendo tráfico/rankings | Actualizar contenido |
| **Low CTR** | Páginas con impresiones pero pocos clicks | Mejorar titles/descriptions |

#### 2.6 Backlinks (si incluye datos)

| Issue | Descripción | Acción |
|-------|-------------|--------|
| **Toxic Backlinks** | Links de sitios spam/penalizados | Disavow si necesario |
| **Lost Backlinks** | Links que ya no existen | Intentar recuperar |
| **Broken Link Building** | Tus páginas 404 con backlinks | Redirect o restaurar |
| **Competitor Gap** | Sitios que linkan competidores pero no a ti | Outreach |

### Paso 3: Generar Health Score Interpretado

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AUDITORÍA SEO: plomeroculiacanpro.mx
  Herramienta: [Ahrefs/Semrush]
  Fecha: [fecha]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 HEALTH SCORE: [XX]/100

Interpretación:
  90-100: Excelente - Solo optimizaciones menores
  80-89:  Muy bueno - Algunos issues a corregir
  70-79:  Bueno - Necesita trabajo en áreas específicas
  60-69:  Regular - Problemas afectando rankings
  <60:    Crítico - Requiere atención inmediata

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RESUMEN DE ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Errores Críticos:     [X] issues
🟠 Warnings:             [X] issues
🟡 Notices:              [X] issues
📄 Páginas Crawleadas:   [X] URLs
🔗 Enlaces Internos:     [X] links
🖼️ Recursos:             [X] archivos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DESGLOSE POR CATEGORÍA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Técnico:        [█████████░] 90%
On-Page:        [███████░░░] 70%
Performance:    [████████░░] 80%
Content:        [██████░░░░] 60%
Backlinks:      [███░░░░░░░] 30%
```

### Paso 4: Crear Plan de Acción Priorizado

Usa la matriz Impacto vs Esfuerzo:

```
                    IMPACTO ALTO
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │   QUICK WINS       │   BIG PROJECTS     │
    │   (Hacer primero)  │   (Planificar)     │
    │                    │                    │
    │   • 404 errors     │   • Site migration │
POCO ├────────────────────┼────────────────────┤ MUCHO
ESFUERZO                 │                    ESFUERZO
    │                    │                    │
    │   FILL-INS         │   THANKLESS        │
    │   (Cuando haya     │   (Evitar o        │
    │    tiempo)         │    automatizar)    │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    IMPACTO BAJO
```

**Output del Plan:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PLAN DE ACCIÓN SEO
  Meta: Health Score [XX] → [XX+15]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 SEMANA 1: QUICK WINS (Crítico + Fácil)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ 1. Corregir 404 errors (X páginas)
     Impacto: +5 puntos Health Score
     Esfuerzo: 30 min
     Acción: Crear redirects 301 o restaurar páginas
     URLs afectadas:
       - /pagina-antigua/ → redirect a /pagina-nueva/
       - /servicio-eliminado/ → redirect a /servicios/

□ 2. Arreglar redirect chains (X casos)
     Impacto: +3 puntos
     Esfuerzo: 15 min
     Acción: Cambiar A→B→C a A→C directo
     Casos:
       - /old/ → /temp/ → /new/ (simplificar)

□ 3. Agregar meta descriptions faltantes (X páginas)
     Impacto: +2 puntos + mejor CTR
     Esfuerzo: 45 min
     URLs:
       - /pagina-1/
       - /pagina-2/

□ 4. Corregir titles duplicados (X grupos)
     Impacto: +3 puntos
     Esfuerzo: 30 min
     Grupos duplicados:
       - "Plomero Culiacán" (5 páginas) → diferenciar

🟠 SEMANA 2: ALTO IMPACTO (Importante + Moderado esfuerzo)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ 5. Optimizar Core Web Vitals
     Impacto: +5 puntos + mejor UX
     Esfuerzo: 2-3 horas
     Issues:
       - LCP: 4.2s → <2.5s (optimizar hero image)
       - CLS: 0.18 → <0.1 (agregar width/height)

□ 6. Resolver orphan pages (X páginas)
     Impacto: +2 puntos
     Esfuerzo: 1 hora
     Acción: Agregar enlaces internos desde páginas relacionadas

□ 7. Actualizar sitemap.xml
     Impacto: +1 punto
     Esfuerzo: 15 min
     Issues:
       - Remover URLs 404
       - Agregar nuevas landing pages

🟡 SEMANA 3-4: CONTENT & KEYWORDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ 8. Expandir thin content (X páginas con <300 palabras)
     Impacto: Medio-Alto
     Esfuerzo: 2-4 horas por página
     Páginas:
       - /servicio-corto/ (150 palabras → 500+)

□ 9. Resolver keyword cannibalization
     Impacto: Alto
     Esfuerzo: 1-2 horas análisis + implementación
     Keywords afectadas:
       - "plomero culiacán" → 3 páginas compitiendo
       Acción: Elegir URL principal, actualizar otras

□ 10. Crear contenido para content gaps
      Impacto: Alto (nuevas keywords)
      Esfuerzo: 3-5 horas por página
      Oportunidades:
        - "plomero económico culiacán" (1,200 búsquedas/mes)
        - "urgencias plomería culiacán" (800 búsquedas/mes)

🟢 ONGOING: MANTENIMIENTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Monitorear Health Score semanal
□ Revisar Search Console por nuevos errores
□ Actualizar contenido evergreen cada 6 meses
□ Auditoría completa cada trimestre
```

### Paso 5: Generar Checklist Ejecutable

Para cada item del plan, generar checklist específico:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHECKLIST: Corregir 404 Errors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preparación:
□ Exportar lista de 404s del audit
□ Identificar si página debe restaurarse o redirect

Por cada URL 404:
□ Verificar si hay backlinks (mantener URL si tiene links)
□ Identificar página destino más relevante
□ Crear redirect 301 en .htaccess o _redirects
□ Verificar redirect funciona
□ Actualizar enlaces internos que apuntaban a 404

Verificación:
□ Re-crawlear con Screaming Frog
□ Verificar en Search Console (puede tardar días)
□ Documentar redirects creados

Comandos útiles:
  # Buscar enlaces rotos en el sitio
  grep -r "href=\"/url-404\"" *.html

  # Crear redirect en Netlify (_redirects)
  /url-vieja /url-nueva 301
```

### Paso 6: Tracking de Progreso

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TRACKING: Auditoría SEO Q4 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Health Score Inicial: 72/100
Meta: 87/100 (+15 puntos)

Semana 1 (Nov 25 - Dic 1)
━━━━━━━━━━━━━━━━━━━━━━━━
✅ 404 errors corregidos (8/8)      +5 pts
✅ Redirect chains arreglados (3/3) +3 pts
⬜ Meta descriptions (0/12)         +2 pts pendiente
Health Score Actual: 80/100

Semana 2 (Dic 2 - Dic 8)
━━━━━━━━━━━━━━━━━━━━━━━━
⬜ Core Web Vitals                  +5 pts
⬜ Orphan pages                     +2 pts
⬜ Sitemap actualizado              +1 pt
Health Score Meta: 85/100

Gráfico Progreso:
Inicio:  [███████░░░] 72%
Sem 1:   [████████░░] 80%
Sem 2:   [████████░░] 85% (meta)
Final:   [█████████░] 87% (stretch)
```

## Integraciones con Otros Comandos

Después de la auditoría, sugerir:

```
📋 Próximos pasos recomendados:

1. Para cada página con issues on-page:
   /seo-optimizer servicios/pagina-con-issues/index.html

2. Para crear nuevas landing pages (content gaps):
   /generador-seo "servicio nuevo" "slug-nuevo"

3. Para publicar correcciones:
   PUBLICA YA

4. Para verificar después de fix:
   Re-ejecutar auditoría en 1 semana
```

## Interpretación de Métricas Específicas

### Ahrefs Site Audit

```
Métricas clave a revisar:

1. Health Score (0-100)
   - Promedio ponderado de todos los issues
   - Meta: >80%

2. Errors (rojos)
   - Requieren acción inmediata
   - Afectan indexación/rankings

3. Warnings (naranjas)
   - Importantes pero no críticos
   - Planificar corrección

4. Notices (azules)
   - Mejoras opcionales
   - Hacer cuando haya tiempo

5. Charts importantes:
   - Distribution of issues by category
   - Pages by depth
   - Internal link distribution
```

### Semrush Site Audit

```
Métricas clave:

1. Site Health (%)
   - Similar a Ahrefs Health Score

2. Errors / Warnings / Notices
   - Misma interpretación que Ahrefs

3. Thematic Reports:
   - Crawlability: ¿Google puede rastrear todo?
   - HTTPS: ¿Implementación correcta?
   - International SEO: hreflang issues
   - Performance: Core Web Vitals
   - Internal Linking: Estructura de enlaces

4. Top Issues
   - Lista priorizada por impacto
   - Empezar por arriba
```

### Google Search Console

```
Datos complementarios:

1. Coverage Report
   - Valid pages (indexadas)
   - Excluded (y por qué)
   - Errors (no indexables)

2. Core Web Vitals Report
   - Mobile vs Desktop
   - Good/Needs Improvement/Poor URLs

3. Manual Actions
   - Penalizaciones manuales (raro pero crítico)

4. Links Report
   - Top linking sites
   - Top linked pages
   - Anchor text distribution
```

## Template de Reporte Final

```markdown
# Reporte Auditoría SEO
**Sitio:** plomeroculiacanpro.mx
**Fecha:** [fecha]
**Herramienta:** Ahrefs Site Audit

## Resumen Ejecutivo

- **Health Score:** 72/100 → Meta: 87/100
- **Errores Críticos:** 8 (todos corregibles en 1 semana)
- **Quick Wins:** 5 acciones que sumarán +13 puntos
- **Inversión estimada:** 4-6 horas de trabajo

## Top 5 Prioridades

1. 🔴 Corregir 8 páginas 404 (+5 pts)
2. 🔴 Arreglar 3 redirect chains (+3 pts)
3. 🟠 Agregar 12 meta descriptions (+2 pts)
4. 🟠 Optimizar LCP en 5 páginas (+3 pts)
5. 🟡 Resolver 2 casos de cannibalization (+2 pts)

## Plan de Acción Detallado

[Ver sección Plan de Acción arriba]

## Métricas a Monitorear

| Métrica | Actual | Meta | Deadline |
|---------|--------|------|----------|
| Health Score | 72 | 87 | 4 semanas |
| 404 Errors | 8 | 0 | 1 semana |
| LCP Mobile | 4.2s | <2.5s | 2 semanas |
| Indexed Pages | 45 | 52 | 3 semanas |

## Próxima Auditoría

Fecha: [fecha + 1 mes]
```

## Notas Importantes

- **Priorizar Quick Wins** - Errores fáciles de corregir con alto impacto
- **No todo es urgente** - Notices pueden esperar
- **Medir antes/después** - Documentar Health Score inicial
- **Re-auditar** - Verificar mejoras después de implementar
- **Automatizar** - Configurar alertas para nuevos errores críticos

## Frecuencia Recomendada

| Tipo de Auditoría | Frecuencia | Herramienta |
|-------------------|------------|-------------|
| Quick Check | Semanal | Search Console |
| Site Audit | Mensual | Ahrefs/Semrush |
| Full Audit + Plan | Trimestral | Ahrefs + GSC + Manual |
| Competitive Analysis | Semestral | Semrush/Ahrefs |
