# Changelog - Plomero Culiacán Pro

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2024-11-27]

### Agregado
- Sistema de comandos Claude (.claude/commands/) para automatización de workflow
- Comando `/landing-creator` para crear landing pages con SEO optimizado
- Comando `/validar` para validar páginas antes de commit (210 líneas)
- Comando `/deploy-quick` para deployment automático a GitHub Pages
- Comando `/seo-optimizer` para análisis y optimización SEO
- Comando `/daily-summary` para resúmenes diarios de trabajo (307 líneas)
- Comando `/weekly-report` para reportes semanales ejecutivos (619 líneas)
- Skill `@validador-pagina` para validación interactiva de páginas (392 líneas)
- Checklist pre-commit (CHECKLIST-ANTES-DE-PUBLICAR.md, 121 líneas)
- CHANGELOG.md para tracking automático de cambios
- Sistema de logs diarios en `.claude/logs/`

### Documentado
- **REGLA #0** - Prohibición estricta de elementos custom (36 líneas)
- **REGLA #0.1** - Estructura Hero crítica con `<picture>` (66 líneas)
- **REGLA #0.2** - Botones flotantes con SVG (56 líneas)
- **REGLA #0.3** - Critical CSS completo obligatorio (89 líneas)
- **REGLA #0.4** - Verificación móvil y escritorio obligatoria (108 líneas)
- **REGLA #0.5** - Optimización SEO obligatoria (105 líneas)

### Mejorado
- landing-creator.md: +1,179 líneas de documentación técnica (7 commits)
- validador-pagina.md: +355 líneas con validación automática (3 commits)
- Blog rediseñado con estilo idéntico a homepage (-646 líneas código duplicado)
- Limpieza masiva de elementos custom incompatibles (-1,225 líneas)

### Corregido
- **Fix crítico:** Homepage aspect-ratio causaba duplicación imagen hero en móvil
- Blog: Estructura hero corregida (usar `<picture>` en lugar de `<div>`)
- Blog: Botones flotantes cambiados a SVG (eliminar emojis)
- Blog: Imagen hero actualizada a hero-plomero-visita.webp
- Blog: Agregado content-visibility:auto para performance
- Servicios: Corregido instalacion-de-sanitarios según landing-creator.md
- Servicios: Corregido reparacion-de-fugas según reglas

### Estadísticas del Día
- **19 commits** realizados
- **+3,951 líneas** agregadas
- **-1,957 líneas** eliminadas
- **11 archivos** modificados
- **5.4 commits/hora** (velocidad promedio)

### Completado
- ✅ Sistema de validación completo (@validador-pagina + /validar)
- ✅ 6 reglas críticas documentadas (REGLA #0 a #0.5)
- ✅ Blog rediseñado y corregido (2 páginas)
- ✅ Servicios corregidos (2 páginas)
- ✅ Sistema de comandos copiado a proyecto electricista
- ✅ Comandos /daily-summary y /weekly-report creados

### Pendiente
- [ ] Validar todas las landing pages con nuevo sistema @validador-pagina
- [ ] Generar primer weekly-report del proyecto
- [ ] Crear más landing pages SEO (plomero-urgente, plomero-barato)

---

## Formato de Changelog

Cada entrada debe seguir este formato:

### Agregado
- Nuevas funcionalidades, landing pages, secciones completas

### Mejorado
- Optimizaciones de performance (LCP, CLS, bundle size)
- Mejoras SEO (keywords, schemas, meta tags)
- Refinamientos de diseño sin cambiar funcionalidad

### Corregido
- Corrección de bugs, errores, problemas visuales
- Fixes de schemas JSON-LD, breadcrumbs, paths

### Eliminado
- Funcionalidades removidas, archivos obsoletos
