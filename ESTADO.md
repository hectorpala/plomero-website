# ESTADO del pipeline de agentes

```json
{
  "ultima_corrida": {
    "fecha": "2026-06-12",
    "rama": "auto/mantenimiento-20260612-1720",
    "modo": "AUTONOMO",
    "revisores": 6,
    "hallazgos_brutos": 22,
    "hallazgos_unicos_nuevos": 19,
    "arreglados": 19,
    "verificados": 19,
    "regresiones": "3 (seo-206/207 og:url=home, movil-203 paridad CSS)",
    "pendientes_humano_nuevos": 5,
    "bajas_no_tocadas": 3,
    "candados_paso8": {
      "auto_revision_limpia": true,
      "diff_max_200_archivos": "18 <= 200",
      "sin_borrados_estructurales": "0 archivos borrados, 0 renombrados",
      "tests_tocados": "0",
      "publicado": true,
      "merge": "2bcea0df",
      "push": "7efbf5bb..2bcea0df main -> main",
      "nota_indexacion": "INDEXACION NO EJECUTADA: el hook pre-push tiene ruta hardcodeada obsoleta (/Users/openclaw/Documents/Mis Apps/...) tras la mudanza a ~/Sitios Web; dijo 'Sin paginas HTML que indexar'. El push si se completo. Ver infra-001."
    },
    "detalle_arreglos": "perf-301..314 (14 imgs bajo-el-fold eager->lazy, hero/logo intactos); seo-206/207 (og:url->canonical); seo-208 (twitter:image en /contacto/); movil-203 (paridad bloque fallback tablas en styles.css, sin bump=asset servido sin cambio); movil-204 (table-wrapper en tecnico-de-gas); links-204 (#contacto->/#contacto en marcha-paz)"
  },
  "corrida_previa": {
    "fecha": "2026-06-12",
    "rama": "auto/mantenimiento-20260612-noche",
    "merge": "6688d219",
    "arreglados": 8,
    "nota": "primera corrida autonoma que publico"
  },
  "pendientes": [
    {"id": "infra-001", "categoria": "infra", "descripcion": "El hook .git/hooks/pre-push (auto-indexacion Google) tiene una ruta hardcodeada obsoleta '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacan' que ya no existe; no envia URLs a la Indexing API. Corregir la ruta a ~/Sitios Web. Tambien: 'node' no esta en el PATH por defecto del entorno (esta en /usr/local/bin); el push requiere PATH=/usr/local/bin:$PATH para que el hook corra.", "severidad": "media", "razon": "modificar hooks/OAuth/indexacion es infra; fuera del alcance mecanico auto"},
    {"id": "gsc-205", "categoria": "gsc", "descripcion": "/servicios/instalacion-de-tinaco/ CTR 0% en 27 keywords de precio (pos 7-11). Anadir rango de precio visible en title/meta/H1.", "severidad": "media", "razon": "copy; validar precio real con el negocio"},
    {"id": "gsc-206", "categoria": "gsc", "descripcion": "Cluster 'reparacion/mantenimiento de boiler' con demanda real y cobertura marginal (CTR 0% en 'reparacion de boiler' pos 11.1; 'cerca de mi' pos 2.3 sin clics). Evaluar pagina dedicada sin canibalizar.", "severidad": "media", "razon": "estrategia de contenido"},
    {"id": "gsc-207", "categoria": "gsc", "descripcion": "/servicios/correccion-baja-presion/ rankea 'bombas de agua' (pos 6-8, CTR 0) pero intencion = comprar/reparar bomba (taller); mismatch. Decidir si el negocio atiende esa intencion.", "severidad": "media", "razon": "estrategia/negocio"},
    {"id": "gsc-208", "categoria": "gsc", "descripcion": "Colonia /monaco/ 31 impr pos 9.3 CTR 0 ('monaco culiacan' es navegacional). Vigilar doorway (ligado a seo-002).", "severidad": "media", "razon": "estrategia, ligado a consolidacion de colonias"},
    {"id": "gsc-209", "categoria": "gsc", "descripcion": "Head terms 'plomero culiacan' (159 impr pos 10.7) y 'plomero' (123 impr pos 10.6) estancados al borde de pagina 2. Reforzar home/hub con enlazado interno (ligado a gsc-202).", "severidad": "media", "razon": "estrategia/autoridad"},
    {"id": "movil-205-206", "categoria": "movil", "descripcion": "terminos/ y privacidad/ no enlazan el CSS compartido (solo <style> inline) y usan placeholder #0066cc; por eso ningun fix movil aplica (tap targets <44px). Anadir <link stylesheet> o replicar reglas inline.", "severidad": "media", "razon": "anadir stylesheet completo a paginas que hoy solo usan inline = cambio de diseno con riesgo de restyle; requiere validacion visual humana"},
    {"id": "gsc-201", "categoria": "gsc", "descripcion": "/precios/ (pagina de dinero) NUNCA indexada; canibalizada por /servicios/plomero-precios/ que SI esta indexada con title casi identico. Consolidar con 301 o canonical.", "severidad": "alta", "razon": "consolidar paginas es decision estrategica"},
    {"id": "gsc-202", "categoria": "gsc", "descripcion": "Hub /servicios/ invisible para Google ('no reconoce esta URL'): solo 2 paginas lo enlazan, la home usa el ancla #servicios. Anadir enlace real en nav/footer.", "severidad": "alta", "razon": "cambio de navegacion sitio-completo"},
    {"id": "seo-002", "categoria": "seo", "descripcion": "56 colonias siguen siendo plantillas casi identicas (doorway). Consolidar en zonas con 301 o reescribir.", "severidad": "alta", "razon": "decision estrategica"},
    {"id": "a11y-101", "categoria": "a11y", "descripcion": "Contraste CTA WhatsApp (.whatsapp-link 1.98:1, .btn-whatsapp 1.98:1) y naranja .btn-primary 2.8-3.4:1. Falla WCAG AA en los CTA principales.", "severidad": "alta", "razon": "cambiar colores de marca es decision visual/negocio"},
    {"id": "gsc-203", "categoria": "gsc", "descripcion": "Copia de Google del sitemap rancia (descarga 06-03/06-04, pre-consolidacion). Reenviar sitemap.xml y sitemaps/main_sitemap.xml en GSC (1 minuto).", "severidad": "media", "razon": "accion externa en GSC fuera del alcance auto"},
    {"id": "gsc-204", "categoria": "gsc", "descripcion": "CTR 0 con alta visibilidad en 2 posts de blog (drenaje-tapado ~430 impr pos 6-8.4; desatascar-wc pos 1.9). Reescribir titles/metas.", "severidad": "media", "razon": "copy"},
    {"id": "a11y-201", "categoria": "a11y", "descripcion": "Contraste 2.0:1 en .hero-availability ('Disponibles ahora', verde #22c55e). Recomendado #15803d (~4.7:1) en inline index.html + 3 CSS.", "severidad": "media", "razon": "cambio de color es decision visual (criterio a11y-101/103)"},
    {"id": "seo-104", "categoria": "seo", "descripcion": "aggregateRating 4.8/150 auto-servido en 15 paginas de negocio, valor inconsistente (4.7/120 en emergencia-24-7) y 6 reseñas duplicadas en 6 URLs.", "severidad": "media", "razon": "REGLAS.md actual permite reviews en paginas de negocio; quitar/consolidar es decision SEO"},
    {"id": "seo-107", "categoria": "seo", "descripcion": "Geo duplicada o generica en 7 paginas de colonia.", "severidad": "media", "razon": "ligado a seo-002; no corregir geo de paginas que quiza se consoliden"},
    {"id": "seo-109", "categoria": "seo", "descripcion": "4 paginas de servicio 77-84% identicas entre si (canibalizacion).", "severidad": "media", "razon": "reescribir/consolidar es estrategia"},
    {"id": "perf-104", "categoria": "perf", "descripcion": "styles.min.css NO esta minificado (50KB); 45 paginas cargan ~14KB extra.", "severidad": "media", "razon": "regenerar asset requiere validacion visual completa"},
    {"id": "perf-106", "categoria": "perf", "descripcion": "~6MB de archivos sin referencias desplegados (logo PNG 4MB, fotos/*.jpg, variantes logo-whatsapp).", "severidad": "media", "razon": "borrar archivos requiere humano"},
    {"id": "perf-108", "categoria": "perf", "descripcion": "icon-512.png 164KB precacheado a todos; heros 1200w de 145-200KB.", "severidad": "media", "razon": "recomprimir binarios altera assets visuales"},
    {"id": "a11y-109", "categoria": "a11y", "descripcion": "Salto h2->h4 en blog/bano-completo.", "severidad": "media", "razon": "cambio de estructura de contenido"},
    {"id": "html-001", "categoria": "html", "descripcion": "Desbalance <div> 143/144 preexistente en servicios/desazolve-de-drenajes (ya estaba en main).", "severidad": "baja", "razon": "requiere localizar el div sobrante a mano"},
    {"id": "bajas-20260612-noche", "categoria": "varios", "descripcion": "seo-203/204 (og:url a la home en 2 servicios), seo-205 (typo año en marcha-paz noindex), movil-202 (link Terminos 65x19 en 44 paginas), perf-206 (dims logo en instalacion-de-tinaco).", "severidad": "baja", "razon": "bajas: no se tocan en auto"}
  ],
  "baseline": {
    "fecha": "2026-06-12",
    "hallazgos_totales_diagnostico": 41,
    "por_categoria": {"seo": 10, "movil": 9, "a11y": 7, "perf": 11, "links": 4}
  }
}
```

## Resumen de la corrida 2026-06-12 noche (auto/mantenimiento-20260612-noche — AUTÓNOMA, PUBLICADA)

- **Health check:** 9/9 rutas en 200, main.js sintaxis OK, wa.me intactas. 0 regresiones de la corrida de la tarde (los 6 revisores lo confirmaron explícitamente).
- **Arreglados y verificados (8):** URLs de JSON-LD/og:url sin `/servicios/` en plomero-economico y desazolve (seo-201/202); dims reales del hero de tecnico-de-gas (perf-201); fetchpriority=high solo en el hero LCP en 3 servicios (perf-202/203/204); preload con imagesrcset en emergencia-24-7 (perf-205); tap targets ≥44px en enlaces de texto tel:/wa.me con regla en los 3 CSS + bump ?v=20260612c + sw.js v24 (movil-201, medido con Chrome headless a 375px y desktop).
- **Candados paso 8: 3/3 cumplidos → PUBLICADO.** Merge 6688d219 a main + push (la indexación automática agotó cuota diaria; se renueva mañana).
- **Pendientes humano nuevos (5):** gsc-201 (consolidar /precios/, ALTA), gsc-202 (enlazar hub /servicios/, ALTA), gsc-203 (reenviar sitemaps en GSC, 1 min), gsc-204 (titles con CTR 0), a11y-201 (verde de disponibilidad 2.0:1).
- **Aprendizaje:** 3 reglas nuevas en REGLAS.md (og:url/JSON-LD = canonical; un solo fetchpriority=high por página; cuidado con la cascada al añadir CSS al final — un selector casi des-oculta .hero-phone-link en desktop, cazado antes de publicar).
