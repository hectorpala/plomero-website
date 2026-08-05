# ESTADO del pipeline de agentes

> **Convención (desde 2026-07-28):** este archivo guarda solo las **últimas ~6 corridas** anidadas.
> Había crecido sin tope (llegó a 643 líneas / ~31,000 tokens — superó el límite de lectura por
> defecto de 25,000 tokens: cualquier corrida que intentara leerlo entero en FASE 0 fallaba). El
> historial completo hasta hoy (todas las corridas desde 2026-06-12, con más detalle narrativo) vive
> íntegro en `docs/ESTADO-ARCHIVO.md` — nada se perdió. El relato línea-por-hallazgo sigue en
> `data/HISTORIAL.jsonl` y el detalle de commits en `git log`. Cada corrida nueva debe: (1) agregar su
> entrada arriba, (2) si la cadena anidada pasa de ~6 corridas, cortar la más vieja y mover su detalle
> completo a `docs/ESTADO-ARCHIVO.md` (append), dejando solo un puntero corto.

```json
{
  "ultima_corrida_actual": {
    "fecha": "2026-08-04",
    "rama": "auto/diario-20260726-1826 (continuada, 10mo dia consecutivo — mismo bloqueo, sin cambios de contenido del sitio)",
    "modo": "AUTONOMO (diario). FASE 0 confirmo que la rama sigue igual: mismo diff de 64 archivos vs main. 7a vez consecutiva con este diff ya verificado ok=true dos veces (07-27) — no se repitio el fan-out completo de FASE 3 ni un verificador independiente nuevo; se hizo health check + re-verificacion ligera + GSC en vivo, igual que 07-29 a 08-03.",
    "resumen": "Health check 4/4 200 en local Y 4/4 200 en produccion real. ci-gate.py: 0 ALTA (17 media/baja, mismas de siempre). check-reglas.py: 54 reglas, 3998/4000 tokens — sigue al borde. gestor-backlog.py: 14 tareas, 0 auto-ejecutables, 1 requiere_humano sin cambio. GSC en vivo: 601 clics (+22%), 60,103 impresiones (+29%), posicion 6.4 — mismo panorama de crecimiento organico sostenido, sin cambios de sitio. docs/ESTADO.md volvio a pasarse del presupuesto (8,687 tokens vs 6,000) — podado hoy archivando 07-28/07-29 completas a docs/ESTADO-ARCHIVO.md.",
    "arreglados": "1 clase (infraestructura interna, no toca el sitio servido): docs/ESTADO.md podado de nuevo — nested completos de 07-28 y 07-29 archivados integros en docs/ESTADO-ARCHIVO.md, reducidos a puntero corto aqui.",
    "crecimiento": "0 paginas nuevas — deliberado: agregar mas a una rama YA bloqueada por tamano de diff empeoraria el problema, no lo resuelve. Backlog persistente sin cambio.",
    "verificado_ok": "no se re-lanzo un verificador independiente completo (7a vez consecutiva con el mismo diff de contenido, ya ok=true dos veces el 07-27). Re-confirmado a mano: ci-gate.py 0 ALTA, check-reglas.py dentro de presupuesto (al borde), health check 4/4 local+produccion, backlog sin sorpresas.",
    "publicado": "NO — 10mo dia consecutivo (desde 2026-07-26) con el MISMO bloqueo: CAP EXCEDIDO, 64 archivos en el diff (>18 del cap de FASE 8). El verificador ya confirmo ok=true de fondo hace dias. Sigue esperando la decision explicita de Hector entre las 2 opciones ofrecidas el 07-28 (forzar el diff completo con CAP_OK=1, o dividirlo en lotes por causa raiz). 10 dias sin respuesta por email ni en el chat directo del 08-02 — no se fuerza publicacion ni se divide la rama sin autorizacion.",
    "pendientes_nuevos": "(sistema, prioridad ALTA, escalado por persistencia — 10mo dia) sistema-cap-18-excedido-no-publicado. (sigue vigente) docs/REGLAS.md a 3998/4000 tokens. (sin cambio) bk-218a5844/doorway-domicilio-vs-cerca-de-mi, a11y-101, a11y-301, seo-107, etc. — ver lista completa abajo en 'pendientes'.",
    "_corrida_anterior": {
      "fecha": "2026-08-03",
      "nota": "9no dia del mismo bloqueo de cap. Health check 4/4, ci-gate 0 ALTA, GSC 615 clics/60,480 impresiones. Podo ESTADO.md de 9,476 a 8,687 tokens (insuficiente, se volvio a exceder — completado hoy 08-04). Detalle completo en docs/ESTADO-ARCHIVO.md y HISTORIAL.jsonl fecha 2026-08-03."
    },
    "_corrida_anterior_ref1": {
      "fecha": "2026-08-02",
      "nota": "8vo dia del mismo bloqueo de cap. Se le pregunto DIRECTO a Hector en el chat tras 7 dias sin respuesta por email. Detalle completo en docs/ESTADO-ARCHIVO.md y HISTORIAL.jsonl fecha 2026-08-02."
    },
    "_corrida_anterior_ref2": {
      "fecha": "2026-07-28 y 2026-07-29",
      "nota": "3ra y 4ta corrida consecutiva sobre el mismo bloqueo de cap (48→64 archivos). 07-28: primera poda grande de ESTADO.md (643 lineas). Detalle completo archivado en docs/ESTADO-ARCHIVO.md (seccion 'Corridas 2026-07-28 y 2026-07-29') y HISTORIAL.jsonl."
    },
    "_corrida_anterior_ref3": {
      "fecha": "2026-07-27, 07-25, 07-21, 07-20, 07-14",
      "nota": "07-27 NO publicada (mismo bloqueo). 07-25 publicado 87 archivos. 07-21 publicado 32 paginas+3 CSS+sw.js. 07-20 publicado 38 paginas. 07-14 publicado 5 paginas+3 CSS+sw.js+3 checks nuevos. Detalle completo en docs/ESTADO-ARCHIVO.md."
    },
    "_historial_anterior_a_2026-07-14": "TODAS las corridas desde 2026-06-12 (narrativa completa) viven integras en docs/ESTADO-ARCHIVO.md — nada se perdio al podar este archivo el 2026-07-28, 2026-08-03 y 2026-08-04."
  },
  "pendientes": [
    {
      "id": "infra-002",
      "categoria": "infra",
      "descripcion": "El hook .git/hooks/pre-push llama 'node' sin ruta absoluta; con 'git push' pelado node no esta en el PATH por defecto -> exit 127 -> ABORTA el push. Workaround usado: PATH=/usr/local/bin:$PATH git push. Endurecer el hook (ruta absoluta de node o env).",
      "severidad": "baja",
      "razon": "cambiar el hook de git toca infra; workaround conocido funciona"
    },
    {
      "id": "gsc-210",
      "categoria": "gsc",
      "descripcion": "Cluster 'bano/WC tapado': /blog/desatascar-wc-metodos-profesionales/ ~130 impr 'como destapar un bano' pos 7.1 + ~30 variantes, CTR ~0.8%. Reescribir title/meta para captar 'bano/inodoro tapado' (no solo 'WC').",
      "severidad": "media",
      "razon": "copy/posicionamiento"
    },
    {
      "id": "gsc-211",
      "categoria": "gsc",
      "descripcion": "/servicios/correccion-baja-presion/: TODO su volumen real viene de 'bombas de agua' (Culiacan 17 impr, Sinaloa 13 impr, reparacion/taller) con CTR 0; intencion = reparar/vender bomba, no presion. Amplia gsc-207.",
      "severidad": "media",
      "razon": "estrategia de oferta/contenido"
    },
    {
      "id": "gsc-212",
      "categoria": "gsc",
      "descripcion": "Cluster 'drenaje tapado': /blog/drenaje-tapado-senales-prevencion/ ~440 impr top10 (pos 3-8.5) con 0 clics; snippet debil. Reescribir title/meta con la frase exacta.",
      "severidad": "media",
      "razon": "copy/snippet"
    },
    {
      "id": "gsc-213",
      "categoria": "gsc",
      "descripcion": "'deteccion de fugas' fragmentado: misma intencion en pos 4.3 a 56 en queries casi identicas; posible canibalizacion entre /servicios/deteccion-de-fugas/ y blog. Definir URL canonica y consolidar enlazado.",
      "severidad": "media",
      "razon": "arquitectura de contenido"
    },
    {
      "id": "gsc-214",
      "categoria": "gsc",
      "descripcion": "Trafico off-target (queries en aleman, marcas ajenas Calorex/Bosch, ciudades ajenas) infla impresiones y deprime el CTR agregado. Observacion: no malinterpretar el CTR bajo agregado como problema de snippet.",
      "severidad": "baja",
      "razon": "informativo, sin accion de codigo"
    },
    {
      "id": "a11y-301",
      "categoria": "a11y",
      "descripcion": "Footer abre con <h4> tras un <h2> (salto h2->h4); ya convertidas precios/ y reparacion-de-fugas (07-25) con la regla de color .footer-section h3 centralizada. Quedan ~16 páginas más (servicios/*, contacto).",
      "severidad": "baja",
      "razon": "baja; mecanico pero fuera de alcance auto (solo alta/media); >15 archivos"
    },
    {
      "id": "movil-301",
      "categoria": "movil",
      "descripcion": "2a tabla (Desglose de Inversion) en /blog/instalacion-tinaco-guia-compra/ L493 sin .table-wrapper; protegida en prod por el fallback global table{overflow-x:auto}. Inconsistencia, no overflow real. Envolver para consistencia.",
      "severidad": "baja",
      "razon": "baja; no desborda en render 375px"
    },
    {
      "id": "perf-401",
      "categoria": "perf",
      "descripcion": "main.js (20KB) no esta minificado real (677 lineas, 1 salto por sentencia); se sirve immutable 1 anio y lo precachea el SW. Minificar a main.min.js de una linea + bump ?v=/sw.js.",
      "severidad": "baja",
      "razon": "RIESGO: minificar puede truncar URLs wa.me (REGLA f8c72299); requiere validacion completa antes de publicar"
    },
    {
      "id": "perf-402",
      "categoria": "perf",
      "descripcion": "Ninguna pagina hace <link rel=preload as=image> del hero LCP. Mejora opcional de LCP.",
      "severidad": "baja",
      "razon": "requiere medir LCP antes/despues con Lighthouse; aplicar solo si hay mejora real"
    },
    {
      "id": "perf-501",
      "categoria": "perf",
      "descripcion": "26 paginas de servicio/blog preloadean 2-3 woff2 con fetchpriority='high', en el mismo carril que el hero LCP; index.html (home) preloadea las fuentes SIN fetchpriority. Quitar fetchpriority='high' de los <link rel=preload as=font> para igualar el patron de home.",
      "severidad": "media",
      "razon": "optimizacion de tuning, no defecto roto; requiere medir LCP antes/despues como perf-104/401/402"
    },
    {
      "id": "perf-502",
      "categoria": "perf",
      "descripcion": "Los 3 pesos de Inter (inter-400/500/600.woff2) son BYTE-IDENTICOS (mismo md5, 38760 bytes c/u); el CSS declara 3 @font-face y se preloadean hasta 3 URLs identicas (~76KB desperdiciados). Re-subsetear desde los .original (que SI difieren) o colapsar a 1 @font-face.",
      "severidad": "media",
      "razon": "requiere herramienta de subset de fuentes; si se cambia un woff2 servido, bump de sw.js"
    },
    {
      "id": "a11y-303",
      "categoria": "a11y",
      "descripcion": "mobile-menu-btn con solo aria-label en 99 paginas; falta aria-expanded='false' y aria-controls='nav-menu' estaticos + id='nav-menu' en el <ul> (index.html si los tiene). Mitigado porque main.js setea aria-expanded al abrir/cerrar.",
      "severidad": "baja",
      "razon": "baja; mecanico pero fuera de alcance auto (solo alta/media); 99 archivos"
    },
    {
      "id": "seo-004",
      "categoria": "seo",
      "descripcion": "6 redirect-stubs servicios/plomero/{index,24-7,a-domicilio,cerca-de-mi,colonias,precios} sin <meta robots noindex> (titles 'Redirigiendo...' identicos); riesgo bajo porque el canonical ya consolida la senal y no estan en sitemap.",
      "severidad": "baja",
      "razon": "baja; opcional"
    },
    {
      "id": "seo-305",
      "categoria": "seo",
      "descripcion": "/blog/marcha-paz-culiacan-2025/ og:url con typo de anio 2026 (canonical es 2025); pagina noindex,follow off-topic.",
      "severidad": "baja",
      "razon": "baja; pagina noindex"
    },
    {
      "id": "gsc-205",
      "categoria": "gsc",
      "descripcion": "/servicios/instalacion-de-tinaco/ CTR 0% en 27 keywords de precio (pos 7-11). Anadir rango de precio visible en title/meta/H1.",
      "severidad": "media",
      "razon": "copy; validar precio real con el negocio"
    },
    {
      "id": "gsc-206",
      "categoria": "gsc",
      "descripcion": "Cluster 'reparacion/mantenimiento de boiler' con demanda real y cobertura marginal (CTR 0% en 'reparacion de boiler' pos 11.1; 'cerca de mi' pos 2.3 sin clics). Evaluar pagina dedicada sin canibalizar.",
      "severidad": "media",
      "razon": "estrategia de contenido"
    },
    {
      "id": "gsc-207",
      "categoria": "gsc",
      "descripcion": "/servicios/correccion-baja-presion/ rankea 'bombas de agua' (pos 6-8, CTR 0) pero intencion = comprar/reparar bomba (taller); mismatch. Decidir si el negocio atiende esa intencion.",
      "severidad": "media",
      "razon": "estrategia/negocio"
    },
    {
      "id": "gsc-208",
      "categoria": "gsc",
      "descripcion": "Colonia /monaco/ 31 impr pos 9.3 CTR 0 ('monaco culiacan' es navegacional). Vigilar doorway (ligado a seo-002).",
      "severidad": "media",
      "razon": "estrategia, ligado a consolidacion de colonias"
    },
    {
      "id": "gsc-209",
      "categoria": "gsc",
      "descripcion": "Head terms 'plomero culiacan' (159 impr pos 10.7) y 'plomero' (123 impr pos 10.6) estancados al borde de pagina 2. Reforzar home/hub con enlazado interno (ligado a gsc-202).",
      "severidad": "media",
      "razon": "estrategia/autoridad"
    },
    {
      "id": "movil-205-206",
      "categoria": "movil",
      "descripcion": "terminos/ y privacidad/ no enlazan el CSS compartido (solo <style> inline) y usan placeholder #0066cc; por eso ningun fix movil aplica (tap targets <44px). Anadir <link stylesheet> o replicar reglas inline.",
      "severidad": "media",
      "razon": "anadir stylesheet completo a paginas que hoy solo usan inline = cambio de diseno con riesgo de restyle; requiere validacion visual humana"
    },
    {
      "id": "gsc-201",
      "categoria": "gsc",
      "descripcion": "/precios/ (pagina de dinero) NUNCA indexada; canibalizada por /servicios/plomero-precios/ que SI esta indexada con title casi identico. Consolidar con 301 o canonical.",
      "severidad": "alta",
      "razon": "consolidar paginas es decision estrategica"
    },
    {
      "id": "gsc-202",
      "categoria": "gsc",
      "descripcion": "Hub /servicios/ invisible para Google ('no reconoce esta URL'): solo 2 paginas lo enlazan, la home usa el ancla #servicios. Anadir enlace real en nav/footer.",
      "severidad": "alta",
      "razon": "cambio de navegacion sitio-completo"
    },
    {
      "id": "seo-002",
      "categoria": "seo",
      "descripcion": "56 colonias siguen siendo plantillas casi identicas (doorway). Consolidar en zonas con 301 o reescribir. NOTA 2026-07: verificar si sigue vigente — CLAUDE.md indica que hoy todas las colonias ya están diferenciadas e indexables (0 noindex); podría estar RESUELTO, no confirmado explícitamente en una corrida.",
      "severidad": "alta",
      "razon": "decision estrategica"
    },
    {
      "id": "a11y-101",
      "categoria": "a11y",
      "descripcion": "Contraste CTA WhatsApp (.whatsapp-link 1.98:1, .btn-whatsapp 1.98:1) y naranja .btn-primary 2.8-3.4:1. Falla WCAG AA en los CTA principales.",
      "severidad": "alta",
      "razon": "cambiar colores de marca es decision visual/negocio"
    },
    {
      "id": "gsc-203",
      "categoria": "gsc",
      "descripcion": "Copia de Google del sitemap rancia (descarga 06-03/06-04, pre-consolidacion). Reenviar sitemap.xml y sitemaps/main_sitemap.xml en GSC (1 minuto).",
      "severidad": "media",
      "razon": "accion externa en GSC fuera del alcance auto"
    },
    {
      "id": "gsc-204",
      "categoria": "gsc",
      "descripcion": "CTR 0 con alta visibilidad en 2 posts de blog (drenaje-tapado ~430 impr pos 6-8.4; desatascar-wc pos 1.9). Reescribir titles/metas.",
      "severidad": "media",
      "razon": "copy"
    },
    {
      "id": "a11y-201",
      "categoria": "a11y",
      "descripcion": "Contraste 2.0:1 en .hero-availability ('Disponibles ahora', verde #22c55e). Recomendado #15803d (~4.7:1) en inline index.html + 3 CSS.",
      "severidad": "media",
      "razon": "cambio de color es decision visual (criterio a11y-101/103)"
    },
    {
      "id": "seo-104",
      "categoria": "seo",
      "descripcion": "aggregateRating 4.8/150 auto-servido en 15 paginas de negocio, valor inconsistente (4.7/120 en emergencia-24-7) y 6 reseñas duplicadas en 6 URLs.",
      "severidad": "media",
      "razon": "REGLAS.md actual permite reviews en paginas de negocio; quitar/consolidar es decision SEO"
    },
    {
      "id": "seo-107",
      "categoria": "seo",
      "descripcion": "Geo duplicada o generica en paginas de zona (norte/sur/oriente/poniente/centro) — requiere geocodificacion real por zona, no inventar coordenadas.",
      "severidad": "media",
      "razon": "ligado a seo-002; no corregir geo de paginas que quiza se consoliden"
    },
    {
      "id": "seo-109",
      "categoria": "seo",
      "descripcion": "4 paginas de servicio 77-84% identicas entre si (canibalizacion).",
      "severidad": "media",
      "razon": "reescribir/consolidar es estrategia"
    },
    {
      "id": "perf-104",
      "categoria": "perf",
      "descripcion": "styles.min.css NO esta minificado (50KB); 45 paginas cargan ~14KB extra.",
      "severidad": "media",
      "razon": "regenerar asset requiere validacion visual completa"
    },
    {
      "id": "perf-106",
      "categoria": "perf",
      "descripcion": "~6MB de archivos sin referencias desplegados (logo PNG 4MB, fotos/*.jpg, variantes logo-whatsapp).",
      "severidad": "media",
      "razon": "borrar archivos requiere humano"
    },
    {
      "id": "perf-108",
      "categoria": "perf",
      "descripcion": "icon-512.png 164KB precacheado a todos; heros 1200w de 145-200KB.",
      "severidad": "media",
      "razon": "recomprimir binarios altera assets visuales"
    },
    {
      "id": "a11y-109",
      "categoria": "a11y",
      "descripcion": "Salto h2->h4 en blog/bano-completo. NOTA 2026-07: la corrida 2026-06-26 registra haber corregido este mismo salto en ese archivo — verificar si ya está resuelto antes de re-trabajarlo.",
      "severidad": "media",
      "razon": "cambio de estructura de contenido"
    },
    {
      "id": "html-001",
      "categoria": "html",
      "descripcion": "Desbalance <div> 143/144 preexistente en servicios/desazolve-de-drenajes (ya estaba en main).",
      "severidad": "baja",
      "razon": "requiere localizar el div sobrante a mano"
    },
    {
      "id": "bajas-20260612-noche",
      "categoria": "varios",
      "descripcion": "seo-203/204 (og:url a la home en 2 servicios), seo-205 (typo año en marcha-paz noindex), movil-202 (link Terminos 65x19 en 44 paginas), perf-206 (dims logo en instalacion-de-tinaco).",
      "severidad": "baja",
      "razon": "bajas: no se tocan en auto"
    },
    {
      "id": "seo-404",
      "categoria": "seo",
      "descripcion": "Canibalizacion on-page 'reparacion de boiler Culiacan': servicios/mantenimiento-de-boiler usa 'Reparacion' como termino principal en title/h1/meta, misma intencion que la pagina dedicada servicios/reparacion-de-boiler. Cuerpos solo 16% iguales (NO doorway), es targeting on-page. Amplia gsc-206.",
      "severidad": "media",
      "razon": "copy/estrategia: reenfocar a 'mantenimiento preventivo' o consolidar con 301"
    },
    {
      "id": "seo-405",
      "categoria": "seo",
      "descripcion": "Canibalizacion on-page 'destape de drenajes/destapacanos' entre servicios/destape-de-drenajes y servicios/desazolve-de-drenajes (ambas usan 'destape' como gancho; desazolve trae 'Destape Garantizado' en title/h1). Cuerpos 1.8% iguales (NO doorway).",
      "severidad": "media",
      "razon": "copy/estrategia: diferenciar intencion (destape=urgencia vs desazolve=limpieza profunda) o 301"
    },
    {
      "id": "a11y-402",
      "categoria": "a11y",
      "descripcion": "Calificaciones por estrellas ★★★★★ como glifos literales sin aria-label/role=img ni aria-hidden en ~92 paginas (.rating-stars en 75 + .stars en 17); lector de pantalla anuncia 5x 'estrella negra' sin contexto numerico.",
      "severidad": "baja",
      "razon": "mecanico pero ~92 archivos excede el candado (<=15); lote/supervisado"
    },
    {
      "id": "a11y-403",
      "categoria": "a11y",
      "descripcion": "46 de 110 paginas servidas sin landmark <main> ni role=main; navegacion por landmarks no ofrece 'saltar al contenido'. Criterio WCAG distinto de a11y-401 (skip-link). index.html SI lo tiene.",
      "severidad": "baja",
      "razon": "mecanico pero 46 archivos excede el candado; hacerlo junto con a11y-401 para dar destino al skip-link"
    },
    {
      "id": "perf-505",
      "categoria": "perf",
      "descripcion": "montserrat-700.woff2 y montserrat-800.woff2 byte-identicos (md5 3d42f7e7..., 33508b c/u) y sus .original tambien; 2 @font-face al mismo glyph (~33KB desperdiciados). Mismo defecto que perf-502 pero Montserrat; el remedio de perf-502 (re-subsetear de .original) NO aplica (los .original tambien identicos).",
      "severidad": "baja",
      "razon": "colapsar a 1 @font-face o re-subsetear pesos reales; cambio de woff2 servido (PRECACHE) exige bump CACHE_NAME sw.js + validar render"
    },
    {
      "id": "gsc-219",
      "categoria": "gsc",
      "descripcion": "Bug cosmetico de logging en mcp-local-seo/gsc-index.mjs L54: url.replace('https://...', ''||'/') -> ''||'/' siempre '/' y produce rutas con doble slash ('//servicios/') en el reporte. NO afecta la inspeccion (inspectionUrl real correcto, veredictos reales).",
      "severidad": "baja",
      "razon": "tooling, no toca el sitio servido; L54 mover el ||'/' fuera del replace"
    },
    {
      "id": "cont-020",
      "categoria": "contenido",
      "descripcion": "servicios/plomero-cerca-de-mi es casi-clon indexable de la home (~92% del cuerpo: 6/72 bloques unicos, 15/16 H2 verbatim, rejilla de 6 servicios + tarjetas de zona + 6 testimonios + blog cards identicos). Patron doorway. Solo intro 'cerca de mi' y tiempos de llegada son propios.",
      "severidad": "media",
      "razon": "reescritura de copy/estrategia + posible consolidacion -> prohibido en auto; amplia seo-002"
    }
  ],
  "baseline": {
    "fecha": "2026-06-12",
    "hallazgos_totales_diagnostico": 41,
    "por_categoria": {
      "seo": 10,
      "movil": 9,
      "a11y": 7,
      "perf": 11,
      "links": 4
    }
  }
}
```

Historial narrativo completo de corridas anteriores a 2026-07-14 (con resúmenes largos en Markdown): ver `docs/ESTADO-ARCHIVO.md`.
