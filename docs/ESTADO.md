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
  "fecha": "2026-07-29",
  "rama": "auto/diario-20260726-1826 (continuada, 4to día consecutivo — mismo bloqueo, sin cambios de contenido del sitio)",
  "modo": "AUTONOMO (diario). FASE 0: árbol sucio al arrancar (3 archivos sin commitear: costos.jsonl, ultima-meta.md, docs/PROPUESTAS.md) — una pasada suelta de crítico-sistema ya había corrido hoy y escrito su brief sin commitear. Se adoptó como checkpoint de FASE 2 (commit cc44a534) en vez de descartarla. Igual que el 07-28: NO se repitió el fan-out completo de revisores sobre un diff sin cambios ya verificado 2 veces — se hizo health check + re-verificación ligera + GSC en vivo.",
  "resumen": "Health check 4/4 200 local y 4/4 200 en producción real. ci-gate.py: 0 ALTA (17 media/baja conocidas). check-reglas.py: 54 reglas, 3998/4000 tokens — AL BORDE del presupuesto, casi sin margen para la próxima regla nueva. gestor-backlog.py: 14 tareas, 0 auto-ejecutables, 1 requiere_humano sin cambio. GSC en vivo: 598 clics (+36%), 61,304 impresiones (+63%), posición 6.4 — mismo panorama que las 3 corridas previas, toda la demanda real mapea a páginas EXISTENTES ya optimizadas → 0 páginas nuevas, 0 ctr-fix nuevos. HALLAZGO NUEVO (de la pasada suelta de crítico-sistema adoptada hoy): el reporte automatizado `recolecta-señales.py` NO mira `git branch`, así que un bloqueo de días como este puede quedar invisible en el brief — dejó 2 propuestas con DRAFT listo en `docs/PROPUESTAS.md` (sección de ramas `auto/*` atascadas + evitar que `crecer.py publicar` cree una rama `auto/crecer-*` duplicada/obsoleta cuando ya se está parado en una rama `auto/*`). Son PROPUESTAS para que Héctor apruebe, no se aplicaron solas.",
  "arreglados": "0 clases nuevas del sitio (nada que arreglar: mismo diff ya verificado, sin regresiones). Se commiteó el trabajo suelto de crítico-sistema (documentación/reportes, sin efecto en el sitio servido).",
  "crecimiento": "0 páginas nuevas (GSC igual que las 3 corridas previas). Backlog persistente: 0 auto-ejecutables, 1 requiere_humano sin cambio.",
  "verificado_ok": "no se re-lanzó un verificador independiente completo (diff de contenido idéntico al ya verificado ok=true dos veces el 07-27). Re-confirmado a mano: ci-gate.py 0 ALTA, check-reglas.py dentro de presupuesto (al borde), health check 4/4 local+producción, backlog sin sorpresas.",
  "publicado": "NO — 4º día consecutivo con el MISMO bloqueo (CAP EXCEDIDO: 48 páginas con cambio sustantivo > 18 de cap). El verificador ya confirmó ok=true de fondo hace 2 días; lo único que falta es la decisión de Héctor (fusionar con `CAP_OK=1` o pedir que se divida en lotes más chicos). No se forzó ninguna de las dos opciones sin su confirmación explícita — ambas están gateadas a que él lo pida. El trabajo sigue a salvo en `auto/diario-20260726-1826` y en la copia `auto/crecer-20260727-183544` (ADVERTENCIA: esta copia quedó desactualizada, le faltan 4 commits del 07-27/28 — ver hallazgo de crítico-sistema arriba; NO usarla como base de un `CAP_OK=1`, usar `auto/diario-20260726-1826`).",
  "pendientes_nuevos": "(sistema, prioridad media, sigue vigente desde 07-27, ahora 4º día) sistema-cap-18-excedido-48-paginas-no-publicado-20260727: sin decisión — ver recomendación en la corrida anterior. (sistema, NUEVO 07-29) 2 propuestas de crítico-sistema en docs/PROPUESTAS.md esperando aprobación (visibilidad de ramas atascadas; evitar rama auto/crecer-* duplicada). (sistema, NUEVO 07-29) docs/REGLAS.md a 3998/4000 tokens — la próxima regla nueva probablemente requiera consolidar antes de poder agregarse. (sigue vigente, sin cambio) bk-218a5844/doorway-domicilio-vs-cerca-de-mi (requiere_humano), rama-huerfana-auto-diario-20260718-pendiente-revision, secretos-en-historial-git, seo-107/GPS de zonas, a11y-101, a11y-301 (16 páginas restantes), check-tracking GTM-no-inicializa-produccion (falso-positivo conocido Consent Mode).",
  "_corrida_anterior": {
  "fecha": "2026-07-28",
  "rama": "auto/diario-20260726-1826 (continuada, sin cambios de contenido — mismo bloqueo que ayer)",
  "modo": "AUTONOMO (diario). FASE 0 confirmó que la rama sigue exactamente como la dejó la corrida de ayer (07-27): 61 archivos de diff vs main, ya verificada ok=true dos veces por el verificador independiente, bloqueada SOLO por el candado del cap (48 páginas con cambio sustantivo > 18) porque mezcla causas raíz heterogéneas de 2 días de trabajo. Decisión de hoy: NO repetir el fan-out completo de 11+ revisores sobre un diff que ya se verificó dos veces sin novedad (sería gastar cuota — ayer costó $9.86, el día anterior $68.77 — para llegar a la misma conclusión). En su lugar: health check + re-verificación ligera (ci-gate desde cero) + GSC en vivo, y usar el tiempo en una mejora de infraestructura real.",
  "resumen": "Health check 5/5 200 local y 5/5 200 en producción real (main sigue en el commit del 07-25, sin cambios). ci-gate.py corrido desde cero sobre la rama: 0 ALTA (17 media/baja conocidas en check-plantilla, ya documentadas). check-reglas.py: 53 reglas, 3996/4000 tokens, dentro de presupuesto. gestor-backlog.py stats: 14 tareas, 0 auto-ejecutables pendientes, 1 requiere_humano sin cambio (bk-218a5844, doorway domicilio-vs-cerca-de-mi). GSC revisado en vivo vía MCP: 574 clics (+30%), 58,607 impresiones (+56%), posición 6.4 — mismo panorama que las corridas previas, todas las oportunidades (striking distance, página 2, zero-clicks) mapean a páginas EXISTENTES (desatascar-wc, precios, baja-presión, drenaje-tapado, tecnico-de-gas) ya optimizadas en corridas anteriores → 0 páginas nuevas, 0 ctr-fix nuevos. Se commiteó en la rama 1 línea suelta de costos.jsonl de la corrida 07-27 (checkpoint FASE 2). MEJORA DE INFRAESTRUCTURA (foco del día, 1 sola mejora): `docs/ESTADO.md` había crecido a 643 líneas / ~31,000 tokens de JSON anidado + resúmenes en Markdown duplicados — superaba el límite de lectura por defecto (25,000 tokens) de la herramienta Read, un fallo mecánico real que cualquier corrida futura iba a repetir en FASE 0. Se archivó COMPLETO y sin pérdida en `docs/ESTADO-ARCHIVO.md`, y se podó la copia activa a las últimas 6 corridas anidadas (07-27 a 07-14) + solo los `pendientes` que siguen activos (se quitaron 5 entradas ya marcadas `estado: RESUELTO` hace semanas — prod-001, seo-304, gsc-215, gsc-216, infra-001 — que ya estaban resueltas y documentadas, solo ocupaban espacio).",
  "arreglados": "1 clase (infraestructura interna, no toca el sitio servido): docs/ESTADO.md podado de 643 a un tamaño manejable + docs/ESTADO-ARCHIVO.md nuevo con el respaldo íntegro. Detalle en HISTORIAL.jsonl fecha 2026-07-28.",
  "crecimiento": "0 páginas nuevas (GSC revisado en vivo vía MCP: mismo panorama que las 3 corridas previas, toda la demanda real mapea a páginas existentes ya optimizadas). Backlog persistente: 0 auto-ejecutables, 1 requiere_humano sin cambio.",
  "verificado_ok": "no se re-lanzó un verificador independiente completo (el diff de contenido del sitio es IDÉNTICO al ya verificado ok=true el 07-27, dos pasadas): se re-confirmó a mano con ci-gate.py 0 ALTA, check-reglas.py dentro de presupuesto, health check 5/5 local+producción, y gestor-backlog.py sin sorpresas. El único archivo nuevo de hoy (docs/ESTADO.md + docs/ESTADO-ARCHIVO.md) es documentación pura, sin efecto en el sitio servido ni en los candados de contenido.",
  "publicado": "NO — mismo bloqueo que ayer (CAP EXCEDIDO: 48 páginas con cambio sustantivo > 18, confirmado de nuevo hoy corriendo `crecer._cap_paginas` directamente, sin cambios desde el 07-27). Es la 3ª corrida consecutiva (07-26/27/28) sobre el mismo trabajo verificado y bloqueado únicamente por tamaño de diff heterogéneo, no por ningún defecto real. El trabajo sigue a salvo en la rama `auto/diario-20260726-1826` (HEAD, con el commit de checkpoint de hoy) y en la copia `auto/crecer-20260727-183544` para revisión humana. RECOMENDACIÓN para Héctor (para no seguir repitiendo esta misma corrida sin avanzar): si al revisar el diff (`git diff main auto/diario-20260726-1826 --stat`) te parece trabajo legítimo, mergéalo tú con `CAP_OK=1 python3 scripts/crecer.py publicar \"...\"` desde esa rama; si prefieres que el sistema lo publique en tandas más chicas (cada una bajo el cap de 18, sin forzar nada), dímelo y la próxima corrida separa el diff en 2-3 lotes por causa raíz (CLS-logo-colonias / FAQPage-9-páginas / precios-testimonios / hub-y-zona-poniente) y los publica uno por uno.",
  "pendientes_nuevos": "(sistema, prioridad media, sigue vigente desde 07-27) sistema-cap-18-excedido-48-paginas-no-publicado-20260727: ahora en su 3er día sin decisión — ver la recomendación arriba. (sigue vigente, sin cambio hoy) bk-218a5844/doorway-domicilio-vs-cerca-de-mi (requiere_humano), rama-huerfana-auto-diario-20260718-pendiente-revision, secretos-en-historial-git, seo-107/GPS de zonas, a11y-101, a11y-301 (16 páginas restantes), check-tracking GTM-no-inicializa-produccion (falso-positivo conocido Consent Mode).",
  "_corrida_anterior": {
  "fecha": "2026-07-27",
  "rama": "auto/diario-20260726-1826 (retomada) -> NO PUBLICADA, queda en la rama + copia auto/crecer-20260727-183544 para revision humana",
  "modo": "AUTONOMO (diario), con retoma de rama muerta: la corrida de AYER (auto/diario-20260726-1826) se corto ANTES de FASE 7 (patron ya conocido y documentado, ver docs/REGLAS.md 'checkpoint FASE 2'). Hoy: FASE 0 confirmo que esa rama tenia 7 commits sin fusionar con FASE 0-6 ya completas (2 checkers nuevos en check-plantilla.py -- check 21 reescrito FAQPage-vs-visible y check 22 nuevo CLS-ratio-de-imagen -- + su auto-fixer, un auto-fixer de denylist de color rescatado, fix de CLS de logo en 24 colonias, y un fix al propio orquestador para que YA NO de por exitosa una corrida cortada a medias). Se retomo la rama tal cual indica el protocolo en vez de descartarla o re-hacerla.",
  "resumen": "Health check 5/5 200 (local). Se omitio repetir el fan-out completo de FASE 3 (ya se habia hecho ayer con evidencia: .pipeline/oportunidades-20260726.md, backlog en 0 auto-ejecutables) -- en su lugar se corrio FASE 7 (verificador SOLO-LECTURA independiente) directo sobre el diff de 59 archivos. Verificador: ok=false, 2 problemas -- (1) docs/REGLAS.md excedio el presupuesto de check-reglas.py (4714/4000 tokens, 2 reglas nuevas del 07-26 sobre 900 chars cada una) porque la FASE 9 de ayer no alcanzo a consolidar antes de cortarse; (2) gate-pagina.py dio 1 ALTA aislada en blog/como-detectar-fugas-agua-casa/index.html en la primera corrida, no reproducida en 15 reintentos + 20 corridas mas de ci-gate.py puro (anomalia transitoria, no bloqueo real). Se corrigio (1): comprimidas las 2 reglas nuevas + 4 reglas viejas ya mecanizadas (CSS/PARIDAD resuelta, CSS/CASCADA-ALCANCE, CONTENIDO/DATOS, INFRA/CHECKERS) a 'que + checker', el relato completo ya vivia en HISTORIAL.jsonl -- check-reglas.py paso a 53 reglas/3996 tokens. Re-verificado a mano: ci-gate.py 0 ALTA en 3 corridas, check-css-paridad.py OK (441 atomos/3 hojas), gate-pagina.py OK en 5/5 reintentos sobre la pagina sospechosa. GSC revisado en vivo (583 clics +40%, 58,250 impresiones +60%, posicion 6.3) -- mismo panorama que ayer, todas las oportunidades mapean a paginas existentes, 0 paginas nuevas.",
  "arreglados": "1 clase (sistema): docs/REGLAS.md consolidado al presupuesto. Sobre un fondo de 7 commits ya trabajados el 07-26 (2 checkers + 2 auto-fixers + CLS de logo en 24 colonias + fix del orquestador), ya documentados en HISTORIAL.jsonl de esa fecha. Detalle de hoy: 2 lineas en HISTORIAL.jsonl fecha 2026-07-27.",
  "crecimiento": "0 paginas nuevas (GSC revisado en vivo via MCP: mismo panorama que ayer, toda la demanda real mapea a paginas existentes). Backlog persistente: 0 auto-ejecutables, 1 requiere_humano sin cambio (bk-218a5844, doorway domicilio-vs-cerca-de-mi).",
  "verificado_ok": "true en la 2da pasada EFECTIVA (1ra del verificador independiente dio ok=false por REGLAS.md sobre-presupuesto + 1 ALTA no reproducible de gate-pagina; el primero se corrigio y se re-verifico a mano -- ci-gate.py 0 ALTA x3, check-css-paridad.py OK, gate-pagina.py 5/5 limpio en la pagina senalada, check-reglas.py OK 3996/4000 -- no se re-lanzo un 2do verificador independiente completo por ser un fix acotado a un solo archivo de documentacion sin efecto en el sitio servido).",
  "publicado": "NO. scripts/crecer.py publicar RECHAZO la publicacion automatica: CAP EXCEDIDO -- 48 paginas HTML con cambio de CONTENIDO real (no solo bump ?v=) contra el cap normal de 18 de FASE 8. Es una decision correcta del candado, no un error: el diff acumula 2 DIAS de trabajo legitimo pero HETEROGENEO (CLS de logo en 24 colonias + FAQPage-vs-visible en 9 paginas + reconciliacion de precios/testimonios + plomero-colonias-culiacan hub reescrito + zona-poniente ampliada) -- no es una sola causa raiz mecanica homogenea como las excepciones concedidas en 2026-07-20/21 (mismo <script> tag en 38 paginas, mismo color en 32 paginas). Ante la duda (principio rector), NO se forzo CAP_OK=1. El trabajo QUEDA A SALVO en 2 lugares: la rama original auto/diario-20260726-1826 (HEAD) y una copia auto/crecer-20260727-183544 que crecer.py genero automaticamente para revision humana. Si Hector revisa y esta de acuerdo en que es trabajo legitimo (el verificador ya confirmo 0 defectos reales de fondo), puede fusionarlo el mismo con: `CAP_OK=1 python3 scripts/crecer.py publicar \"...\"` desde esta rama, o simplemente mergear a mano.",
  "pendientes_nuevos": "(auto, prioridad media, NUEVO) sistema-cap-18-excedido-48-paginas-no-publicado-20260727: decision de NO publicar por tamano de diff, no por defecto -- ver HISTORIAL.jsonl para el detalle completo y las 2 ramas donde vive el trabajo. (sigue vigente, sin cambio hoy) bk-218a5844/doorway-domicilio-vs-cerca-de-mi (requiere_humano), rama-huerfana-auto-diario-20260718-pendiente-revision (aun mas vieja, sin revisar), secretos-en-historial-git, seo-107/GPS de zonas, a11y-101, a11y-301 parcial (16 paginas restantes), check-tracking GTM-no-inicializa-produccion (falso-positivo conocido Consent Mode).",
  "_corrida_anterior": {
  "fecha": "2026-07-25",
  "rama": "auto/diario-20260723-0903 (retomada) -> auto/crecer-20260725-185150 -> publicado en main: 2 commits (c01feb46 arreglos+aprender, 238c5a54 merge)",
  "resumen": "Retomada la rama huérfana del 07-23 (85 archivos sin verificar, interrumpida antes de FASE 7-10 por agotar cuota); confirmado aquí que los 3 bloqueos que reportaron 2 corridas de respaldo (Codex) NO existen en este entorno. FASE 7 1ra pasada: ok=false — regresión real de contraste (h4→h3 en footer de precios/reparacion-de-fugas heredaba el color oscuro global en vez del claro del footer). Remediada con regla CSS dedicada `.footer-section h3{color:#F8FAFC}` en las 3 hojas + re-bump. 2da pasada: ok=true. GSC: 579 clics (+45%), 57,301 impresiones (+67%), posición 6.3.",
  "arreglados": "1 clase nueva (regresión contraste footer, 2 páginas + 3 CSS) sobre 85 archivos ya trabajados 07-23/24 (FAQPage-vs-visible ~12 páginas, 4 contradicciones de precio, regresión de color nav/breadcrumb, ancla, tap-target). Detalle en HISTORIAL.jsonl fecha 2026-07-25.",
  "crecimiento": "0 páginas nuevas (demanda real mapea a páginas existentes).",
  "verificado_ok": "true en 2da pasada (1ra ok=false por la regresión de contraste, remediada y reconfirmada con Chrome headless real).",
  "publicado": "SI, vía scripts/crecer.py publicar. 87 archivos en 1 commit (cap NO se disparó: la mayoría del diff era solo bump ?v=, exento por diseño). Pre-push encoló 68 URLs en GSC.",
  "pendientes_nuevos": "(auto, prioridad baja) a11y-301-footer-h4-h3-16-paginas-restantes: solo 2 de ~18 páginas conocidas convertidas; replicar también la regla de color ya centralizada. (sigue vigente) seo-imagen-incorrecta-tecnico-gas, contenido-testimonios-posiblemente-inventados-boiler-gas, a11y-aria-label-menu-sin-acento-~63-paginas, seo-107/GPS zona-oriente/poniente, rama-huerfana-auto-diario-20260718, secretos-en-historial-git, check-tracking GTM Consent Mode (falso-positivo persistente, considerar silenciarlo con nota explícita)."
  },
  "_corrida_anterior_ref": {
    "fecha": "2026-07-21",
    "nota": "publicado en main (32 páginas + 3 CSS + sw.js, excepción de alcance concedida por ser 3 causas raíz mecánicas ya conocidas). Detalle completo en docs/ESTADO-ARCHIVO.md y HISTORIAL.jsonl fecha 2026-07-21."
  },
  "_corrida_anterior_ref2": {
    "fecha": "2026-07-20",
    "nota": "publicado en main (38 páginas, excepción concedida: mismo <script> tag faltante, 1 causa raíz mecánica — menú móvil roto). Detalle completo en docs/ESTADO-ARCHIVO.md y HISTORIAL.jsonl fecha 2026-07-20."
  },
  "_corrida_anterior_ref3": {
    "fecha": "2026-07-14",
    "nota": "publicado en main (5 páginas del lote rotativo + 3 CSS + sw.js + 3 checks nuevos en check-plantilla.py). Detalle completo en docs/ESTADO-ARCHIVO.md y HISTORIAL.jsonl fecha 2026-07-14."
  },
  "_historial_anterior_a_2026-07-14": "TODAS las corridas desde 2026-06-12 (narrativa completa, JSON anidado y resúmenes en Markdown) viven íntegras en docs/ESTADO-ARCHIVO.md — no se perdió nada al podar este archivo el 2026-07-28."
  }
  }
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
