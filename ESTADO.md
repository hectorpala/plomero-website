# ESTADO del pipeline de agentes

```json
{
  "ultima_corrida": {
    "fecha": "2026-06-12",
    "rama": "auto/mantenimiento-20260612",
    "modo": "PRUEBA SUPERVISADA del guion diario (publicación frenada por instrucción humana)",
    "hallazgos_brutos": 71,
    "hallazgos_unicos": 64,
    "arreglados_grupos": 12,
    "arreglados_individuales": 35,
    "verificados": 35,
    "regresiones": 1,
    "pendientes_humano_nuevos": 10,
    "bajas_no_tocadas": 16,
    "candados_paso8": {
      "auto_revision_limpia": true,
      "diff_max_200_archivos": "106 <= 200",
      "sin_borrados_estructurales": "0 archivos borrados",
      "habria_publicado": true,
      "publicado": false,
      "razon_no_publicado": "prueba supervisada: el humano pidió detenerse antes del paso 9"
    }
  },
  "pendientes": [
    {"id": "seo-002", "categoria": "seo", "descripcion": "56 colonias siguen siendo plantillas casi identicas (doorway). Consolidar en zonas con 301 o reescribir.", "severidad": "alta", "razon": "decision estrategica"},
    {"id": "a11y-101", "categoria": "a11y", "descripcion": "Contraste CTA WhatsApp (.whatsapp-link 1.98:1, .btn-whatsapp 1.98:1) y naranja .btn-primary 2.8-3.4:1. Falla WCAG AA en los CTA principales.", "severidad": "alta", "razon": "cambiar colores de marca es decision visual/negocio"},
    {"id": "seo-104", "categoria": "seo", "descripcion": "aggregateRating 4.8/150 auto-servido en 15 paginas de negocio, valor inconsistente (4.7/120 en emergencia-24-7) y 6 reseñas duplicadas en 6 URLs.", "severidad": "media", "razon": "REGLAS.md actual permite reviews en paginas de negocio; quitar/consolidar es decision SEO"},
    {"id": "seo-107", "categoria": "seo", "descripcion": "Geo duplicada o generica en 7 paginas de colonia.", "severidad": "media", "razon": "ligado a seo-002; no corregir geo de paginas que quiza se consoliden"},
    {"id": "seo-109", "categoria": "seo", "descripcion": "4 paginas de servicio 77-84% identicas entre si (canibalizacion).", "severidad": "media", "razon": "reescribir/consolidar es estrategia"},
    {"id": "perf-104", "categoria": "perf", "descripcion": "styles.min.css NO esta minificado (50KB); 45 paginas cargan ~14KB extra.", "severidad": "media", "razon": "regenerar asset requiere validacion visual completa"},
    {"id": "perf-106", "categoria": "perf", "descripcion": "~6MB de archivos sin referencias desplegados (logo PNG 4MB, fotos/*.jpg, variantes logo-whatsapp).", "severidad": "media", "razon": "borrar archivos requiere humano"},
    {"id": "perf-108", "categoria": "perf", "descripcion": "icon-512.png 164KB precacheado a todos; heros 1200w de 145-200KB.", "severidad": "media", "razon": "recomprimir binarios altera assets visuales"},
    {"id": "a11y-109", "categoria": "a11y", "descripcion": "Salto h2->h4 en blog/bano-completo.", "severidad": "media", "razon": "cambio de estructura de contenido"},
    {"id": "html-001", "categoria": "html", "descripcion": "Desbalance <div> 143/144 preexistente en servicios/desazolve-de-drenajes (ya estaba en main).", "severidad": "baja", "razon": "requiere localizar el div sobrante a mano"}
  ],
  "baseline": {
    "fecha": "2026-06-12",
    "hallazgos_totales_diagnostico": 41,
    "por_categoria": {"seo": 10, "movil": 9, "a11y": 7, "perf": 11, "links": 4}
  }
}
```

## Resumen de la corrida 2026-06-12 tarde (rama auto/mantenimiento-20260612 — PRUEBA SUPERVISADA)

- **Arreglados y verificados (12 grupos / 35 hallazgos):** 110 srcset 800w rotos (5 servicios), 10 og:image rotas (5 páginas), 11 anchors #contacto muertos (blog), 48 aria-label (12 formularios), foco visible en 4 posts, width/height en 5 imágenes, lazy en 6 footers, 6 tablas con table-wrapper, regla breadcrumb en styles.css (REGRESIÓN de paridad), tap targets .footer-links + bump ?v=20260612b (102 págs) + sw v23.
- **Regresión (1):** paridad CSS — fix de breadcrumbs faltaba en styles.css. Regla CSS/PARIDAD reforzada en REGLAS.md con verificación 1/1/1.
- **Pendientes humano nuevos (10):** contraste de CTAs (decisión de marca), aggregateRating en 15 páginas (decisión SEO), geo de colonias (ligado a seo-002), canibalización de 4 servicios, min.css sin minificar, ~6MB sin referencias, recompresión de íconos/heros, headings, div preexistente.
- **Bajas (16):** registradas en HISTORIAL, no tocadas en modo auto.
- **Candados paso 8: los 3 cumplidos — habría publicado SÍ.** No se publicó por instrucción humana (prueba supervisada). Rama intacta, main intacto, sin push.
