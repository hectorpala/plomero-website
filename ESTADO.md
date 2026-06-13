# ESTADO del pipeline de agentes

```json
{
  "ultima_corrida": {
    "fecha": "2026-06-12",
    "rama": "auto/mantenimiento-20260612-2001",
    "modo": "AUTONOMO",
    "revisores": 6,
    "hallazgos_brutos": 16,
    "hallazgos_unicos_nuevos": 13,
    "arreglados": 3,
    "verificados": 3,
    "regresiones": "0",
    "pendientes_humano_nuevos": "10 (gsc-210..214, perf-401/402, a11y-301, movil-301, infra-002)",
    "bajas_no_tocadas": "4 (seo-304 desazolve breadcrumb 2 niveles, seo-305 typo anio marcha-paz, movil-301, a11y-301)",
    "candados_paso8": {
      "auto_revision_limpia": true,
      "diff_max_200_archivos": "3 <= 200",
      "sin_borrados_estructurales": "0 archivos borrados, 0 renombrados",
      "tests_tocados": "0",
      "publicado": true,
      "merge": "eee3c396",
      "push": "fcb190a1..eee3c396 main -> main",
      "nota_indexacion": "INDEXACION OK (infra-001 ya resuelto): el hook detecto 17 URLs (incluidas las 3 paginas editadas) pero la cuota diaria de Google sigue agotada -> las 17 quedaron encoladas en pending-index.json para reintento automatico (job launchd diario). 0 URLs perdidas. NOTA infra-002: el push pelado fallo porque el hook llama 'node' sin ruta y node no esta en el PATH por defecto; se reintento con PATH=/usr/local/bin:$PATH git push y funciono."
    },
    "detalle_arreglos": "seo-301/302/303: BreadcrumbList JSON-LD truncado a 1 item (Inicio->home) en 3 paginas de servicio indexables; el ultimo item no coincidia con el canonical. Anadidos niveles 2 (Servicios) y 3 (la pagina, item==canonical) igual que el patron del resto de servicios. JSON-LD revalidado (parse OK), pos3==canonical y HTTP 200 en las 3."
  },
  "corrida_previa": {
    "fecha": "2026-06-12",
    "rama": "auto/mantenimiento-20260612-1720",
    "merge": "2bcea0df",
    "arreglados": 19,
    "nota": "perf-301..314 eager->lazy; seo-206/207; movil-203/204; links-204"
  },
  "pendientes": [
    {"id": "infra-002", "categoria": "infra", "descripcion": "El hook .git/hooks/pre-push llama 'node' sin ruta absoluta; con 'git push' pelado node no esta en el PATH por defecto -> exit 127 -> ABORTA el push. Workaround usado: PATH=/usr/local/bin:$PATH git push. Endurecer el hook (ruta absoluta de node o env).", "severidad": "baja", "razon": "cambiar el hook de git toca infra; workaround conocido funciona"},
    {"id": "gsc-210", "categoria": "gsc", "descripcion": "Cluster 'bano/WC tapado': /blog/desatascar-wc-metodos-profesionales/ ~130 impr 'como destapar un bano' pos 7.1 + ~30 variantes, CTR ~0.8%. Reescribir title/meta para captar 'bano/inodoro tapado' (no solo 'WC').", "severidad": "media", "razon": "copy/posicionamiento"},
    {"id": "gsc-211", "categoria": "gsc", "descripcion": "/servicios/correccion-baja-presion/: TODO su volumen real viene de 'bombas de agua' (Culiacan 17 impr, Sinaloa 13 impr, reparacion/taller) con CTR 0; intencion = reparar/vender bomba, no presion. Amplia gsc-207.", "severidad": "media", "razon": "estrategia de oferta/contenido"},
    {"id": "gsc-212", "categoria": "gsc", "descripcion": "Cluster 'drenaje tapado': /blog/drenaje-tapado-senales-prevencion/ ~440 impr top10 (pos 3-8.5) con 0 clics; snippet debil. Reescribir title/meta con la frase exacta.", "severidad": "media", "razon": "copy/snippet"},
    {"id": "gsc-213", "categoria": "gsc", "descripcion": "'deteccion de fugas' fragmentado: misma intencion en pos 4.3 a 56 en queries casi identicas; posible canibalizacion entre /servicios/deteccion-de-fugas/ y blog. Definir URL canonica y consolidar enlazado.", "severidad": "media", "razon": "arquitectura de contenido"},
    {"id": "gsc-214", "categoria": "gsc", "descripcion": "Trafico off-target (queries en aleman, marcas ajenas Calorex/Bosch, ciudades ajenas) infla impresiones y deprime el CTR agregado. Observacion: no malinterpretar el CTR bajo agregado como problema de snippet.", "severidad": "baja", "razon": "informativo, sin accion de codigo"},
    {"id": "a11y-301", "categoria": "a11y", "descripcion": "Footer abre con <h4> tras un <h2> (salto h2->h4) en 18 paginas (servicios/*, contacto, precios); la otra variante de footer ya usa h3. Cambiar las 4 cabeceras del footer de h4 a h3.", "severidad": "baja", "razon": "baja; mecanico pero fuera de alcance auto (solo alta/media); 18 archivos"},
    {"id": "movil-301", "categoria": "movil", "descripcion": "2a tabla (Desglose de Inversion) en /blog/instalacion-tinaco-guia-compra/ L493 sin .table-wrapper; protegida en prod por el fallback global table{overflow-x:auto}. Inconsistencia, no overflow real. Envolver para consistencia.", "severidad": "baja", "razon": "baja; no desborda en render 375px"},
    {"id": "perf-401", "categoria": "perf", "descripcion": "main.js (20KB) no esta minificado real (677 lineas, 1 salto por sentencia); se sirve immutable 1 anio y lo precachea el SW. Minificar a main.min.js de una linea + bump ?v=/sw.js.", "severidad": "baja", "razon": "RIESGO: minificar puede truncar URLs wa.me (REGLA f8c72299); requiere validacion completa antes de publicar"},
    {"id": "perf-402", "categoria": "perf", "descripcion": "Ninguna pagina hace <link rel=preload as=image> del hero LCP. Mejora opcional de LCP.", "severidad": "baja", "razon": "requiere medir LCP antes/despues con Lighthouse; aplicar solo si hay mejora real"},
    {"id": "seo-304", "categoria": "seo", "descripcion": "/servicios/desazolve-de-drenajes/ tiene BreadcrumbList de 2 niveles (Inicio > Desazolve) sin el nivel intermedio 'Servicios'; el ultimo item SI == canonical (no es bug de mismatch, solo inconsistencia con el patron de 3 niveles).", "severidad": "baja", "razon": "baja; no se toca en auto (solo alta/media)"},
    {"id": "seo-305", "categoria": "seo", "descripcion": "/blog/marcha-paz-culiacan-2025/ og:url con typo de anio 2026 (canonical es 2025); pagina noindex,follow off-topic.", "severidad": "baja", "razon": "baja; pagina noindex"},
    {"id": "infra-001", "categoria": "infra", "estado": "RESUELTO 2026-06-12", "descripcion": "El hook pre-push (auto-indexacion Google) no enviaba URLs porque ~/gsc-mcp/sites.json tenia el 'folder' de Plomero apuntando a la ruta vieja '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacan' (ya inexistente); auto-index.mjs hace git -C en esa carpeta -> 0 html -> 'Sin paginas HTML que indexar'. CORREGIDO: folder -> '/Users/openclaw/Sitios Web/Plomero Culiacan'. Verificado: git -C en ruta nueva detecta los 17 html del push. Nota: lo de 'node fuera del PATH' era falsa alarma (esa frase es output del propio script; node corrio bien). AUTOMATIZADO: auto-index.mjs ahora encola en ~/gsc-mcp/pending-index.json las URLs que fallan por cuota/error transitorio (en vez de perderlas), y el job launchd 'com.gscmcp.reindex' (diario 9:10) las reintenta con 'node auto-index.mjs --drain-all' cuando la cuota se reinicia. Las 16 paginas del push 7efbf5bb..fcb190a1 (que hoy chocaron con 'Quota exceeded') ya estan en la cola; se enviaran solas manana.", "severidad": "baja"},
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

## Resumen de la corrida 2026-06-12 20:01 (auto/mantenimiento-20260612-2001 — AUTÓNOMA, PUBLICADA)

- **Health check:** 9/9 rutas en 200, main.js sintaxis OK (node v22.18 vía /usr/local/bin), wa.me intactas (526673922273). 0 regresiones (los 6 revisores confirmaron que perf-301..314, og:url=canonical, fetchpriority único, versionado CSS/JS y links siguen sanos).
- **Arreglados y verificados (3):** seo-301/302/303 — BreadcrumbList JSON-LD truncado a 1 item (Inicio→home, último item ≠ canonical) en 3 páginas de servicio indexables (instalacion-de-boiler, plomero-a-domicilio, plomero-cerca-de-mi). Añadidos niveles 2 (Servicios) y 3 (la página, item==canonical), igualando el patrón del resto. Verificado: JSON-LD reparseado OK, pos3==canonical, HTTP 200 en las 3. Solo HTML → sin bump de ?v=/sw.js.
- **Candados paso 8: 3/3 cumplidos → PUBLICADO.** Merge eee3c396 a main + push fcb190a1..eee3c396. Indexación: el hook (infra-001 resuelto) detectó las 17 URLs (incl. las 3 editadas) pero la cuota diaria de Google sigue agotada → encoladas en pending-index.json para reintento automático (0 perdidas). El `git push` pelado falló por `node: command not found` en el hook (infra-002); se completó con `PATH=/usr/local/bin:$PATH git push`.
- **Pendientes humano nuevos (10):** gsc-210..214 (clusters baño/drenaje/bombas/fugas con CTR 0 + ruido off-target), perf-401 (minificar main.js, riesgo wa.me), perf-402 (preload hero), a11y-301 (footer h4→h3 en 18 págs), movil-301 (2ª tabla sin wrapper), infra-002 (hook pre-push sin node en PATH). Bajas no tocadas: seo-304 (desazolve breadcrumb 2 niveles), seo-305 (typo año marcha-paz noindex).
- **Aprendizaje:** 2 reglas en REGLAS.md — (1) variante del bug og:url=canonical: el BreadcrumbList puede quedar truncado a 1 nivel con el último item apuntando a la home; verificar que el último `item` == canonical y que existan los 3 niveles en páginas de servicio. (2) infra/push: el hook pre-push necesita node en PATH (`/usr/local/bin`); usar `PATH=/usr/local/bin:$PATH git push`.
