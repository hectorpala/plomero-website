# Última corrida — 2026-06-12 (tarde) — PRUEBA SUPERVISADA

**Rama:** `auto/mantenimiento-20260612` · **Commit:** 5ad90987 · **Publicado:** NO (frenado por instrucción humana, no por candados)

## Qué se arregló (12 grupos, 35 hallazgos, todos verificados con el sitio corriendo)

| # | Hallazgo | Sev. | Fix |
|---|----------|------|-----|
| links-101..105 | 110 candidatos srcset 800w relativos → 404 en 5 páginas de servicios | alta | `/` antepuesto; 0 restantes; imagen 200 |
| links-106..110 | og:image/twitter:image a webp inexistentes (5 páginas) | media | repuntadas a webp existentes (200 verificado) |
| links-111..120,122 | 11 CTA `#contacto` muertos en blog | media | `→ /#contacto` |
| a11y-105/106 | 48 inputs sin aria-label (8 servicios + 4 posts) | alta | aria-label patrón del home |
| a11y-107 | outline:none inline anulaba el foco arreglado hoy (4 posts) | media | outline 2px #C2410C |
| perf-101/102 | 5 imágenes sin width/height (CLS), incl. logo /precios/ | alta/media | dimensiones intrínsecas |
| perf-103 | 6 logos de footer sin lazy | media | loading=lazy decoding=async |
| movil-101+ | 6 tablas sin .table-wrapper | media | envueltas; balance div OK |
| movil-109 | **REGRESIÓN**: regla breadcrumb faltaba en styles.css (paridad) | media | copiada; 1/1/1 |
| movil-110 | .footer-links tap targets ~20px | media | regla en 3 CSS + `?v=20260612b` (102 págs) + sw v23 |

## Qué quedó pendiente para humano (no mecánico)

- **a11y-101/102 (alta):** contraste de los CTA WhatsApp (1.98:1) — cambiar color de marca es decisión de negocio.
- **seo-104/105/106:** aggregateRating self-serving en 15 páginas de negocio + valores inconsistentes — decisión SEO.
- **seo-107/108:** geo duplicada/genérica en 7 colonias — ligado al pendiente estratégico seo-002.
- **seo-109:** 4 páginas de servicio 77-84% idénticas — consolidar/reescribir prohibido en auto.
- **perf-104/106/108:** re-minificar min.css, borrar ~6MB sin referencias, recomprimir íconos/heros — regeneración/borrado de assets.
- **a11y-109, html-001** y 16 bajas registradas en HISTORIAL.

## Candados del paso 8 (evaluados de verdad)

1. Auto-revisión sin problemas de correctitud: ✅ (JSON-LD 0 inválidos en 102 HTML; único desbalance div es preexistente en main; tests y contenido intactos)
2. Diff ≤ 200 archivos: ✅ 106 archivos
3. Sin borrados estructurales: ✅ 0 archivos borrados

**Veredicto: HABRÍA PUBLICADO (3/3). Se detuvo solo por la excepción de prueba supervisada.**
