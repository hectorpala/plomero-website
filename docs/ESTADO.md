# ESTADO del pipeline de agentes

```json
{
  "ultima_corrida_actual": {
    "fecha": "2026-07-09",
    "rama": "auto/diario-20260709-1826 -> publicado en main en 2 commits (2bc63e69 arreglos, 3cbfa6d9 aprender)",
    "modo": "AUTONOMO (diario completo: FASE 0-10)",
    "resumen": "Health check 4/4 200. FASE 3: fan-out de 11 revisores del PISO site-wide (0 hallazgos reales; 1 ALTA falso-positivo de check-plantilla contra un artefacto de graphify no-servido, investigado y confirmado; 4 falsos-positivos de tracking por Consent Mode; INP de home con ruido de entorno 3er día consecutivo, sin acción) + 4 revisores de JUICIO (a11y/contenido/links/seo) sobre 10 páginas (5 cambiadas ayer por otra sesión + lote rotativo de 5 viejas) -> ~34 hallazgos reales. FASE 5: arreglados 11 clases (8 fixes de contraste WCAG AA + 2 tap-targets en los 3 CSS compartidos incl. el boton CTA principal y el de WhatsApp; caja de tip + footer inline en 3 posts de blog; color de breadcrumb inline en 8 páginas; 3 anclas de footer 'Instalación de sanitarios' mal enrutadas (regresión 3x, ahora mecanizada); 1 enlace index.html no-canónico; aggregateRating unificado 4.8/150 en emergencia-24-7; twitter:url agregado/corregido en 3 páginas; JSON-LD headline+breadcrumb name sincronizados con <title> + dateModified en 3 blogs; sitemap lastmod actualizado en las 10 páginas; garantía unificada a 6 meses en zona-poniente). HALLAZGO CRÍTICO del verificador FASE 7 (1ra pasada, ok=false): casi se excluyó obsidian-vault/ (bitácora interna trackeada y SERVIDA en producción por netlify publish='.') de 2 checkers bajo premisa falsa -> revertido + bloqueado con _redirects 404! forzado + robots.txt Disallow, confirmado con curl -I en producción real (HTTP 404). 2da pasada del verificador: ok=true. FASE 6: GSC revisado en vivo (427 clics +14%, 41439 impr +58%, pos 6.4); 0 páginas nuevas (toda la demanda mapea a páginas existentes o a decisiones ya tomadas de no re-tocar clusters CTR); reforzada indexación de reparacion-de-bombas-de-agua (seguía 'nunca rastreada'). FASE 9: 3 reglas ampliadas/nuevas en REGLAS.md (49 reglas, dentro de presupuesto tras podar 4 reglas viejas verbosas) + 2 checkers nuevos en check-plantilla.py (check 14: ancla-vs-servicio-real, detectó 16 instancias adicionales sin arreglar hoy; check 15: consistencia de aggregateRating site-wide) + 14 líneas en HISTORIAL.jsonl.",
    "arreglados": "11 clases (ver resumen), 20 archivos de contenido + 3 CSS + sw.js + sitemap + _redirects + robots.txt + 2 checkers. Detalle completo en HISTORIAL.jsonl (14 líneas fecha 2026-07-09, 11 arreglados + 3 pendientes).",
    "crecimiento": "0 páginas nuevas. 1 acción de indexación (gsc_index reparacion-de-bombas-de-agua). Ver .pipeline/oportunidades-20260709.md.",
    "verificado_ok": "true en la 2da pasada (la 1ra dio ok=false por el hallazgo de obsidian-vault, remediado y re-verificado). ci-gate 0 ALTA (16 media, todos del checker NUEVO de hoy sobre páginas fuera del lote, no bloquean). gate-pagina CANDADO OK en las 10 páginas (instalacion-de-boiler con warning Jaccard 0.72<0.80, preexistente). Headless: 0 errores JS en 13 páginas, JSON-LD parsea, canonical==og:url==twitter:url. Contraste medido con Chrome real (no solo CSS declarado): todos ≥4.5:1 AA. Producción verificada en vivo: obsidian-vault -> 404, rating 4.8 servido, 4 páginas clave 200.",
    "publicado": "SI, 2 commits vía scripts/crecer.py publicar: (1) 70b8dec3/2bc63e69 - los 11 arreglos + bloqueo de seguridad; (2) 40c05770/3cbfa6d9 - FASE 9 (reglas+checkers+historial). Push seguro (fetch+merge+push, sin --force); pre-push auto-indexó las URLs tocadas.",
    "pendientes_nuevos": "(auto, prioridad media, MECANIZADO) pend-links-ancla-servicio-20260709: 16 páginas más con anclas mal enrutadas detectadas por el checker nuevo, no arregladas hoy (fuera del lote), quedan visibles en ci-gate hasta que se corrijan. (humano, prioridad media) pend-titulo-correccion-baja-presion-ambiguo-20260709: título migró hacia 'Bombas de Agua' pero el contenido sigue siendo de 'baja presión' — decidir completar la migración o revertir. (humano, prioridad baja) pend-plomero-settings-bak-commiteado-20260709: scripts/crecer.py publicar commiteó un archivo stray pre-existente (sin secretos) — decidir si se borra y auditar el staging del script.",
    "_corrida_anterior": {
    "fecha": "2026-07-08",
    "rama": "auto/diario-20260708-1541 -> publicado en main (6c2b470e, 4b39f87a, merge fa2f31f9)",
    "modo": "AUTONOMO (diario completo: FASE 0-10)",
    "resumen": "Health check 4/4 200. FASE 3: fan-out de 11 revisores del PISO site-wide (todos 0 hallazgos salvo secretos-en-historial ya conocido/pendiente-humano, y 4 falsos-positivos esperados de tracking por Consent Mode en headless) + 7 revisores de JUICIO acotados a un lote rotativo de 5 páginas viejas (destape-de-bano-inodoro, reparacion-de-llaves-y-mezcladoras, plomero-cerca-de-mi, desazolve-de-drenajes, instalacion-de-tinaco). El lote arrojó ~35 hallazgos con bastante solape entre revisores; tras dedup contra HISTORIAL.jsonl, 13 clases reales arregladas: anclas de footer con destino equivocado + enlaces a cadena de redirect + enlace no-canónico /index.html; twitter:url mal en desazolve; contradicción de garantía de tinaco (6 meses vs 1 año) unificada a 1 año en su propia página Y en los JSON-LD Service embebidos en 2 páginas hermanas; un BUG DE CONTENIDO grande (4 entidades Service del catálogo JSON-LD de desazolve-de-drenajes tenían la MISMA descripción del servicio anfitrión pegada por error, restauradas las 4 correctas); H1 sin acento en plomero-cerca-de-mi; CLS por height declarado (800) vs real (534, verificado con sips) en reparacion-de-llaves; a11y: class=nav-link faltante en el menú móvil de tinaco (tap target 18px→52.8px) y contraste insuficiente de .whatsapp-link (1.98:1→7.67:1, #075E54) y de breadcrumb activo (4.45:1→7.19:1); móvil: 3 reglas CSS compartidas nuevas para tap-targets <44px (.footer p a, .read-more, lista de servicios sin clase) + 2 fixes de estilo inline puntuales; meta geo.* agregados a tinaco (no tenía ninguno). Cache-busting: ?v= bumpeado en 71 páginas + sw.js v32→v34 (dos pasadas de auto-reparo). Verificado con ci-gate (0 ALTA), gate-pagina OK en las 5 páginas, Chrome headless (contraste y tap-targets confirmados con mediciones reales), y un verificador independiente de solo-lectura confirmó ok=true/0 problemas antes de publicar (incluyendo la observación de que 3 archivos .pipeline/launchd/*.plist en el working tree son de otro trabajo de infra ajeno a esta corrida, correctamente excluidos del commit). FASE 6 (crecer): GSC revisado en vivo (446 clics +24%, 41,436 impr +62%, pos 6.5) — todas las oportunidades reales mapean a páginas ya existentes o a un pendiente humano ya conocido (cluster de precios seo-403); 0 páginas nuevas (ver .pipeline/oportunidades-20260708.md). FASE 9: 2 reglas nuevas + 1 ampliada en REGLAS.md (dentro de presupuesto, 48 reglas/~3978 tokens) + 17 líneas en HISTORIAL.jsonl (13 arreglados, 4 pendientes).",
    "arreglados": "5 archivos de contenido (13 clases de hallazgo): ver resumen arriba. Detalle completo en HISTORIAL.jsonl (17 líneas fecha 2026-07-08).",
    "crecimiento": "0 páginas nuevas (GSC revisado vía MCP en vivo: toda la demanda real ya tiene página dedicada o es un pendiente de decisión humana ya registrado — cluster 'precios' seo-403).",
    "verificado_ok": "true (verificador SOLO-LECTURA independiente, ok=true 0 problemas): git status/diff coincide exactamente con lo descrito (5 páginas de contenido + ~70 con solo bump ?v= + 3 CSS + sw.js); ci-gate 0 ALTA; gate-pagina CANDADO OK en las 5; HTTP 200 en las 5; JSON-LD parsea; canonical==og:url==twitter:url; 0 enlaces internos rotos nuevos; Chrome headless confirmó whatsapp-link rgb(7,94,84), footer/.read-more >=44px, menú móvil de tinaco 52.8px; 0 precios tocados; 0 páginas borradas; 0 electricista/GTM ajeno; cache-busting íntegro (71 páginas en el token nuevo, sw.js v34).",
    "publicado": "SI, en 2 commits + 1 merge: (1) 6c2b470e - los 13 arreglos de contenido/a11y/móvil/perf; (2) 4b39f87a - FASE 9 (REGLAS.md + HISTORIAL.jsonl); (3) fa2f31f9 - merge --no-ff a main + push. Secuencia segura (fetch + merge --ff-only + merge --no-ff + push, sin --force); pre-push auto-indexó 68 URLs en GSC.",
    "pendientes_nuevos": "(auto, prioridad media) pend-tinaco-fuera-de-esqueleto: instalacion-de-tinaco no sigue el esqueleto compartido (CSS inline propio ~9.4KB, hero sin preload, sin Service Worker) — requiere una sesión dedicada de migración, no un parche. (auto, prioridad media) pend-social-proof-srcset: imágenes de reseñas/antes-después sin srcset/sizes en 2 páginas, pesan hasta 159KB en móvil — requiere generar variantes de imagen. (auto, prioridad media) pend-form-labels-visibles: formulario de contacto sin <label> visible (solo aria-label+placeholder), probablemente un patrón compartido por más páginas — mejor una sesión que lo aplique a toda la plantilla de una vez. (auto, prioridad media, sin acción) perf-inp-home-ruido: INP de home varió 33/104/88ms en 3 mediciones sin que el home fuera tocado hoy — se sospecha ruido del entorno sandbox, no re-baselineado a ciegas. (humano, ALTA, sin cambio, ya conocido) pend-secreto-historial-git: 2 credenciales siguen expuestas en el historial de git (client_secret genérico + Google OAuth GOCSPX), requiere que el dueño las rote/revoque. (humano, MEDIA, ya conocido) seo-403/pend-geo-servicio: cluster de 'precios de plomería' con posible canibalización de URL y coordenadas GPS genéricas repetidas en ~18 páginas de servicio — ambos requieren una decisión del dueño (URL canónica / geocodificación real), no se inventó nada.",
    "_corrida_anterior": {
    "fecha": "2026-07-07",
    "rama": "auto/diario-20260707-1535 + auto/aprender-20260707-1535 -> publicado en main (2c8140e7, 4400a587)",
    "modo": "AUTONOMO (diario completo: FASE 0-10, incluye meta-pase pendiente del critico-sistema 2026-07-06 encontrado sin commitear)",
    "resumen": "Antes de empezar se encontraron 3 archivos sin commitear de una corrida previa del critico-sistema (2026-07-06: 4 propuestas nuevas en docs/PROPUESTAS.md + costos.jsonl/ultima-meta.md), verificados en sus meritos (son solo docs, no tocan el sitio) y commiteados aparte. Health check 4/4 200. FASE 3: fan-out de 11 revisores del PISO site-wide (todos 0 hallazgos, salvo secretos-en-historial ya conocido y pendiente de que el dueno rote la credencial, y tracking con 4 falsos-positivos esperados por Consent Mode en headless) + 7 revisores de JUICIO acotados a un lote rotativo de 5 paginas viejas (mantenimiento-de-boiler, plomeria-comercial, instalacion-de-sanitarios, plomero-zona-norte-culiacan, plomero-zona-sur-culiacan). El lote arrojo 12 hallazgos reales en esas 5 paginas: enlaces de footer con texto/destino distinto, contradicciones de garantia (6 meses vs 'un año'/'3 meses' segun el bloque), un hero con contraste insuficiente (se descubrio ademas que el CSS COMPARTIDO tiene un bloque 'hero mobile' pensado solo para el home que se cuela a cualquier pagina con las mismas clases — requirio un segundo fix tras verificar con Chrome headless que el primer intento dejaba texto oscuro sobre fondo oscuro en movil), un <img> con width/height que no coincidian con el asset real (CLS), tap-target faltante en una pagina hermana, contraste de breadcrumb bajo el minimo AA, e iconos decorativos sin aria-hidden. Se arreglo TODO (5 archivos), se verifico con ci-gate + gate-pagina + Chrome headless real (no solo curl), y un verificador independiente de solo-lectura confirmo ok=true/0 problemas antes de publicar. FASE 6 (crecer): se reviso GSC (find_opportunities) — las mismas 2 oportunidades de CTR ya detectadas el 2026-06-26 (desatascar-wc, drenaje-tapado) siguen con title/meta ya optimizados (0-clic es por SERP-features, no snippet debil, decision ya tomada de no tocarlas); sin demanda nueva para pagina nueva -> 0 paginas nuevas hoy (permitido por las reglas). FASE 9: 4 reglas nuevas en REGLAS.md (ampliando una existente para no exceder presupuesto) + 6 lineas en HISTORIAL.jsonl (5 arreglados, 1 pendiente: GPS de zona duplicado/inconsistente en las 4 paginas de zona, requiere geocodificacion real que esta sesion no pudo derivar de forma confiable).",
    "arreglados": "5 archivos (12 hallazgos): (1) links: 3 footers con anchor 'Instalacion de sanitarios' apuntando al hub generico en vez de la pagina real; (2) contenido: garantia contradictoria unificada a 6 meses en instalacion-de-sanitarios y mantenimiento-de-boiler (JSON-LD vs cuerpo visible); (3) a11y/CSS: hero de instalacion-de-sanitarios sin contraste garantizado, arreglado con scrim oscuro rgba(0,0,0,.5) + color blanco explicito en el h1 dentro de su propio @media movil (para ganarle a un override del CSS compartido pensado solo para el home); (4) perf: img hero de mantenimiento-de-boiler con width/height que no coincidian con el asset real (CLS); (5) a11y: tap-target de .checklist en zona-norte, contraste de breadcrumb en 4 paginas, aria-hidden en 10 iconos decorativos de instalacion-de-sanitarios.",
    "crecimiento": "0 paginas nuevas (GSC revisado via find_opportunities: sin demanda nueva; las 2 oportunidades de CTR conocidas ya estan optimizadas segun decision previa del 2026-06-26, no se tocaron para evitar cambio-por-cambiar).",
    "verificado_ok": "true (verificador SOLO-LECTURA independiente, ok=true 0 problemas): git diff main = exactamente los 5 archivos anunciados; ci-gate 0 ALTA; gate-pagina CANDADO OK en las 5 (Jaccard 0.24-0.42); HTTP 200 en las 5; JSON-LD parsea; canonical==og:url==twitter:url; 93 hrefs internos verificados 200; Chrome headless real confirmo los 8 arreglos puntuales (incl. contraste .hero h1 blanco sobre rgba(0,0,0,.5) en 375/1280px y tap-targets de 44px exactos); 0 precios tocados; 0 paginas borradas; 0 electricista/GTM ajeno; instalacion-de-sanitarios sigue con 25 enlaces entrantes (no huerfana).",
    "publicado": "SI, en 2 commits: (1) 2c8140e7 - los 5 arreglos de contenido/a11y/perf (merge --no-ff + push, pre-push OK, auto-indexadas las 5 URLs en GSC); (2) 4400a587 - FASE 9 (REGLAS.md + HISTORIAL.jsonl), sin tocar paginas. Ambos via la misma secuencia segura de scripts/crecer.py publicar (fetch + merge --ff-only + merge --no-ff + push, sin --force).",
    "pendientes_nuevos": "(auto, prioridad media) seo-2026070701-gps-zona-duplicado: las 4 paginas de zona (norte/sur/oriente/poniente) comparten el mismo meta geo.position/ICBM generico, inconsistente con su propio JSON-LD -> requiere geocodificar cada zona con datos reales (no se inventaron coordenadas). (humano, ALTA, sin cambio) pend-secreto-historial-git: el client_secret de Google sigue expuesto en el historial de git (arbol actual limpio) — requiere que el dueno lo rote/revoque. NOTA: el token GSC (bk-12b83ae9) esta VIVO — confirmado hoy por revisor-infra-salud y por el pre-push (token valido, 33-36 min de vigencia); ese pendiente puede cerrarse.",
    "_corrida_anterior": {
      "fecha": "2026-07-02",
      "rama": "auto/diario-20260630-1827 -> publicado en main (5dfa860b, 482a3d54)",
      "resumen": "Al iniciar la corrida diaria de ese dia, la rama auto/diario-20260630-1827 tenia TODO el trabajo de la corrida del 2026-06-30 sin commitear (interrumpida antes de FASE 7/8/9/10): cache-busting de CSS compartido (?v=20260621->20260630 en ~70 paginas + sw.js CACHE_NAME v31->v32), fix de imagen incorrecta en servicios/destape-de-bano-inodoro (tinaco->taza de bano), y un fix de infra (rutas post-reorganizacion en gestor-backlog.py/recolecta-senales.py). Verificado en sus meritos y ADOPTADO. Durante la FASE 7 se encontro una REGRESION de la misma clase (gate-pagina.py con ruta rota a validate-landing.sh) que se arreglo y se mecanizo con check-rutas-pipeline.py.",
      "arreglados": "3 clases: cache-busting CSS ~70 paginas+3 CSS+sw.js; imagen incorrecta en destape-de-bano-inodoro; 3 scripts con rutas rotas post-reorganizacion + checker nuevo.",
      "verificado_ok": "true (verificador SOLO-LECTURA, ok=true 0 problemas tras el fix de gate-pagina.py).",
      "publicado": "SI, en 2 commits (5bbabf82/5dfa860b y c1d1b888/482a3d54) via scripts/crecer.py publicar.",
      "_corrida_anterior": {
      "fecha": "2026-06-26",
      "rama": "auto/crecer-20260626-120322",
      "modo": "MARATÓN (pasada única: 1 unidad tipo a)",
      "resumen": "Piso determinista LIMPIO (ci-gate 0 ALTA, check-plantilla 0, check-indexabilidad 0). GSC vivo por MCP: 0 reescrituras CTR (blogs ya tienen match exacto, 0-clic=SERP-features). Unidad elegida: a11y-109 (MEDIA) — salto h2->h4 en blog/cuanto-cuesta-plomeria-bano-completo-culiacan (comparacion-materiales: Economico/Estandar/Premium). Fix: 3x h4->h3 + selector CSS inline .comparison-card h4->.comparison-card h3 (preserva estilos naranja/1.1rem). Headless: 0 JS errors, h3s=['ECONOMICO','ESTANDAR','PREMIUM'] en cards, 0 h4 restantes. ci-gate 0 ALTA, gate-pagina Jaccard 0.29, HTTP 200. Publicado commit 978b3999 + push 15247052 + gsc_index /blog/cuanto-cuesta-plomeria-bano-completo-culiacan/.",
      "arreglados": "1 archivo: blog/cuanto-cuesta-plomeria-bano-completo-culiacan/index.html — jerarquia h1->h2->h3 sin saltos.",
      "crecimiento": "0 paginas nuevas.",
      "verificado_ok": "determinista (sin verificador independiente en pasada maraton): ci-gate 0 ALTA, gate-pagina CANDADO OK Jaccard 0.29, headless 0 JS errors, HTTP 200.",
      "publicado": "SI (1 archivo <= candado 18; candados todos OK).",
      "pendientes_nuevos": "ninguno nuevo.",
      "_corrida_anterior": {
        "fecha": "2026-06-26",
        "rama": "auto/diario-20260626-1113",
        "modo": "AUTONOMO (diario: mantener+crecer+verificar+aprender)",
        "resumen": "Al iniciar habia CAMBIOS SIN COMMITEAR en el arbol (corrida previa interrumpida): 18 colonias+home tocadas por fix-colonia-eta.py + el script nuevo. Verificados en sus meritos y ADOPTADOS (no creados hoy): el hero-eta-badge contradecia el ETA del cuerpo en 17 colonias (deriva-no-inventes: las 3 fuentes del cuerpo coinciden y el badge difiere) + 8 metas truncadas. El cambio de link de la home se DIFIRIO (revertido) para dejar 1 fix coherente bajo el cap. Health 6/6 200, 0 electricista/GTM ajeno. PISO determinista LIMPIO: ci-gate 0 ALTA, nap 0, conversion 0, linking 0, css-paridad OK. GSC REVIVIO via MCP (ciego 06-22/06-23): 359 clics/29577 impr 28d (+13%/+26% pos 6.7).",
        "arreglados": "1 clase, 17 HTML colonia (fix-colonia-eta-20260626): hero-eta-badge igualado al ETA dominante del cuerpo (meta+benefit+cobertura) — ej amorada/barrio-estacion 20-30->25-35; + 8 metas recortadas al borde de clausula completo (ej '...conexiones r'->'...color rojizo'). dry-run post-fix=0 colonias (consistente). MECANIZADO: check 13 en check-plantilla.py (dispara contra el badge viejo, 0 en arbol limpio).",
        "crecimiento": "0 paginas nuevas (toda la demanda GSC mapea a paginas existentes, sin hueco). 0 reescrituras CTR: los 2 blogs de mayor volumen (drenaje-tapado 415 impr 0-clic; desatascar-wc ~440 impr) YA tienen title/meta con match exacto fuerte -> 0-clic es SERP-features/PAA (gsc-214), no snippet -> reescribir seria cambio-por-cambiar. Bombas-de-agua sigue 'nunca rastreada' pese a 2 inlinks+sitemap -> gsc_index tras publicar.",
        "verificado_ok": "true (verificador SOLO-LECTURA independiente, ok=true 0 problemas): git diff origin/main = 17 HTML colonia + costos + fix-colonia-eta.py; ci-gate 0 ALTA; gate-pagina 17/17 (Jaccard max 0.68); dry-run ETA 0 colonias; 0 metas truncadas; HTTP 17/17 200; JSON-LD parsea; canonical==og:url; index.html FUERA del diff; 0 electricista/GTM ajeno; email+wa.me intactos; 0 CSS/JS/sitemap/precios/tests; 0 paginas vivas borradas.",
        "publicado": "SI (17 <= candado 18; verificador ok=true). Merge ff-only -> no-ff -> push al cierre + gsc_index colonias mejoradas + bombas.",
        "pendientes_nuevos": "(humano, ALTA) re-auth mcp-local-seo/gsc-token.json: el SENSOR check-infra.mjs sigue ciego (token CLI invalid_grant) aunque el MCP gsc vive; bk-12b83ae9/infra-gsc-cli-token. (diferido) link home emergencia-24-7/index.html->/ (forma directorio seo-401, arrastra el doorway pre-existente home/cerca-de-mi cont-020 al candado); twitter:url ausente en las 17 colonias (pre-existente, las blogs si lo traen). (vigilar) bombas-de-agua sin rastrear; amorada 'rastreada sin indexar' (presion doorway colonias).",
        "_archivo_anterior": {
          "fecha": "2026-06-22",
          "rama": "auto/diario-20260622-1914",
          "resumen": "Nada SERVIDO cambió desde 998c23b8. PISO LIMPIO. infra-salud reportó 'GSC ciego' = token CLI mcp-local-seo (invalid_grant) pero el MCP gsc SÍ vivía (gsc_list_sites OK) -> FASE 6 usó datos reales. Lote rotativo destapó breadcrumb.",
          "arreglados": "1 clase, 19 págs: BreadcrumbList nivel intermedio 'Servicios' apuntaba a /#servicios en vez del hub /servicios/. MECANIZADO check 2b en check-indexabilidad.py.",
          "verificado_ok": "true (verificador SOLO-LECTURA, ok=true 0 problemas sobre 19).",
          "publicado": "NO — 19>18 candado => PASE SUPERVISADO. Mergeado por humano el 2026-06-23 (890d13de en origin/main)."
        }
      }
    }
    }
    }
  },
  "pendientes": [
    {
      "id": "prod-001",
      "categoria": "produccion",
      "estado": "RESUELTO 2026-06-13 (commit ea91bc12)",
      "descripcion": "EXCEPCION JS NO CAPTURADA en produccion. RESUELTO: eran 2 bugs encadenados en main.js — (1) L273 '()' espurio invocaba un id como funcion ('is not a function'); (2) L274 el polyfill pasaba 2500 a requestIdleCallback (espera {timeout:..}) -> 'IdleRequestOptions', oculto detras del bug 1. Fix: L273 '})();'->'});' ; L274 polyfill->setTimeout directo. Versionado main.js?v=20260613 en 30 HTML + sw.js v24->v25. Verificado en headless local (0 errores en / /precios/ /contacto/) Y contra produccion con check-produccion.mjs (hallazgos vacios). wa.me intacto. Revivio popup salida-intencion, quote-sheet, registro SW y scroll tracking.",
      "severidad": "alta"
    },
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
      "descripcion": "Footer abre con <h4> tras un <h2> (salto h2->h4) en 18 paginas (servicios/*, contacto, precios); la otra variante de footer ya usa h3. Cambiar las 4 cabeceras del footer de h4 a h3.",
      "severidad": "baja",
      "razon": "baja; mecanico pero fuera de alcance auto (solo alta/media); 18 archivos"
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
      "id": "seo-304",
      "categoria": "indexabilidad",
      "estado": "RESUELTO 2026-06-13 (merge e2418d1e)",
      "descripcion": "/servicios/desazolve-de-drenajes/ BreadcrumbList de 2 niveles sin el nivel intermedio 'Servicios'. RESUELTO: insertado pos2 Servicios->/servicios/ y renumerada la pagina a pos3 (item==canonical); checker indexabilidad 0 hallazgos. Lo elevo el revisor-indexabilidad a alta (idx-001).",
      "severidad": "alta"
    },
    {
      "id": "gsc-215",
      "categoria": "gsc",
      "estado": "RESUELTO 2026-06-14",
      "descripcion": "BUG tooling en mcp-local-seo/gsc-index.mjs: urlInspection.index.inspect pasaba siteUrl=SITE_URL_HTTP (https://...) en vez de la propiedad verificada SITE_URL (sc-domain:...) -> 'You do not own this site' -> deteccion de des-indexaciones CIEGA. RESUELTO: cambiado a SITE_URL y quitado el const SITE_URL_HTTP huerfano. Verificado corriendo el script: ahora devuelve estado real (Enviada e indexada / Descubierta sin indexar). No afecta el sitio servido.",
      "severidad": "media"
    },
    {
      "id": "gsc-216",
      "categoria": "gsc",
      "estado": "RESUELTO 2026-06-14",
      "descripcion": "gsc-index.mjs hacia ping a www.google.com/ping?sitemap= (endpoint retirado por Google en 2023, siempre 404). RESUELTO: eliminado el bloque de ping (conservando const sitemapUrl que usa el submit por API). El submit por API sigue funcionando (Sitemap enviado OK).",
      "severidad": "baja"
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
      "id": "infra-001",
      "categoria": "infra",
      "estado": "RESUELTO 2026-06-12",
      "descripcion": "El hook pre-push (auto-indexacion Google) no enviaba URLs porque ~/gsc-mcp/sites.json tenia el 'folder' de Plomero apuntando a la ruta vieja '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacan' (ya inexistente); auto-index.mjs hace git -C en esa carpeta -> 0 html -> 'Sin paginas HTML que indexar'. CORREGIDO: folder -> '/Users/openclaw/Sitios Web/Plomero Culiacan'. Verificado: git -C en ruta nueva detecta los 17 html del push. Nota: lo de 'node fuera del PATH' era falsa alarma (esa frase es output del propio script; node corrio bien). AUTOMATIZADO: auto-index.mjs ahora encola en ~/gsc-mcp/pending-index.json las URLs que fallan por cuota/error transitorio (en vez de perderlas), y el job launchd 'com.gscmcp.reindex' (diario 9:10) las reintenta con 'node auto-index.mjs --drain-all' cuando la cuota se reinicia. Las 16 paginas del push 7efbf5bb..fcb190a1 (que hoy chocaron con 'Quota exceeded') ya estan en la cola; se enviaran solas manana.",
      "severidad": "baja"
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
      "descripcion": "56 colonias siguen siendo plantillas casi identicas (doorway). Consolidar en zonas con 301 o reescribir.",
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
      "descripcion": "Geo duplicada o generica en 7 paginas de colonia.",
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
      "descripcion": "Salto h2->h4 en blog/bano-completo.",
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

## Resumen de la corrida 2026-06-26 11:13 (auto/diario-20260626-1113 — AUTÓNOMA, diario)

- **Estado inicial anómalo:** al arrancar había **cambios SIN COMMITEAR** en el árbol de `main` (18 colonias + `index.html` + `.pipeline/fix-colonia-eta.py` nuevo + `costos.jsonl`), de una corrida previa que aplicó el fix pero **nunca lo verificó/commiteó**. El reflog confirma que la última rama (`auto/diario-20260625-1141`) ya se mergeó; estos quedaron huérfanos. NO los borré a ciegas: los verifiqué en sus méritos y los adopté (los que pasan candados).
- **Health check:** 6/6 rutas 200 (/, /contacto/, /servicios/, /blog/, /precios/, colonia barrio-estacion). 0 "electricista", 0 GTM ajeno en la home. Server local en 8092.
- **Adoptado y verificado (1 clase, 17 colonias):** `fix-colonia-eta.py` corrigió el **hero-eta-badge** que contradecía el ETA del cuerpo (el badge decía "Llegamos en 20-30 min" pero meta+beneficio+cobertura decían 25-35; el script solo cambia el badge cuando las 3 fuentes del cuerpo coinciden → **deriva, no inventa**) en 17 colonias, y recortó **8 meta descriptions truncadas** a mitad de palabra ("...conexiones r · Llegada" → "...color rojizo · Llegada"). Dry-run post-fix = 0 colonias (todo consistente).
- **Decisión de alcance:** el cambio de link de la home (`emergencia-24-7/index.html` → `/`, forma-directorio seo-401) estaba completo pero (a) subía el diff a 19 HTML > cap 18 y (b) arrastraba el doorway PRE-EXISTENTE home/cerca-de-mi (cont-020, falla anti-doorway en origin/main también) al candado de publicación. Lo **diferí** (revertí) para dejar 1 fix coherente (17 colonias) auto-publicable. No es gamear el cap: es disciplina de alcance.
- **PISO determinista LIMPIO:** ci-gate 0 ALTA (plantilla/indexabilidad/estructura), nap 0, conversion 0, linking 0, css-paridad OK (415 átomos). infra-salud: único ALTA = token CLI GSC (humano, conocido).
- **GSC REVIVIÓ (vía MCP):** ciego 06-22/06-23, hoy `gsc_list_sites/performance/opportunities` responden. 28d: **359 clics (+13%), 29.577 impresiones (+26%), pos 6.7**. (El sensor `check-infra.mjs` sigue marcando "GSC ciego" porque usa el token CLI de mcp-local-seo, muerto e independiente del MCP.)
- **Crecimiento (FASE 6): 0 páginas nuevas** (toda la demanda mapea a páginas existentes). **0 reescrituras CTR:** los 2 blogs de mayor volumen (drenaje-tapado 415 impr 0-clic; desatascar-wc ~440 impr) ya tienen title/meta con match exacto fuerte → el 0-clic es SERP-features/PAA (gsc-214), no snippet débil → reescribir sería cambio-por-cambiar. La página de bombas sigue "nunca rastreada" pese a 2 enlaces + sitemap → `gsc_index` explícito tras publicar.
- **Verificador (FASE 7): ok=true, 0 problemas** (alcance 17 colonias; ci-gate 0 ALTA; gate-pagina 17/17 Jaccard máx 0.68; dry-run ETA 0; 0 metas truncadas; HTTP 17/17 200; index.html fuera del diff; anti-fuga limpia; 0 páginas vivas borradas).
- **Mecanización (FASE 9):** check 13 en `check-plantilla.py` (badge ETA ≠ cuerpo + meta truncada) — dispara contra el badge viejo, 0 en árbol limpio, JSON válido, ci-gate sigue 0 ALTA. REGLAS.md consolidada a 3985/4000 tokens (42 reglas).
- **Publicación (FASE 8): SÍ** (17 ≤ 18, verificador ok=true). Merge ff-only → no-ff → push + `gsc_index` de colonias mejoradas y bombas.

## Resumen de la corrida 2026-06-23 18:26 (auto/diario-20260623-1826 — AUTÓNOMA, diario)

- **Contexto:** el PASE SUPERVISADO de ayer (breadcrumb, 890d13de) ya está en origin/main (humano lo mergeó). `main` LOCAL quedó atrás en 29c6e96d → lo sincronicé a origin/main; el diff de la corrida se mide contra **origin/main** (10 págs reales, no las 29 falsas que daba el main viejo).
- **Health check:** 6/6 rutas 200 (/, /contacto/, /servicios/, /blog/, /precios/, /servicios/reparacion-de-bombas-de-agua/), 0 "electricista", 0 GTM ajeno. Server en 8091.
- **Selector:** nada SERVIDO cambió desde 890d13de → solo PISO + lote rotativo.
- **PISO determinista LIMPIO (0 ciegos):** plantilla 0/68, indexabilidad 0/68, nap 0/79, conversión 0/68, enlazado 0/68, e2e 0/3, producción EN VIVO 0; señales conocidas perf-001 (R-03 baseline), trk-001..004 (R-04 Consent Mode), sec-001 (R-01 secreto histórico, exit 0). infra-salud: único ALTA = token GSC.
- **GSC CIEGO hoy:** ambas tools de local-seo (find_opportunities + search_keywords) devuelven "Token expirado y no se pudo renovar". A diferencia de ayer (el MCP aún vivía), hoy el token `gsc-token.json` está totalmente expirado (invalid_grant). NO se intentó copiar/eludir el token (el clasificador lo bloqueó el 06-22, correctamente). = bk-12b83ae9, degradado por completo → 0 páginas nuevas (candado de demanda ciego).
- **Arreglado (3 clases, 10 HTML blog):**
  - **a11y-501/502 = bk-64bed7fd:** `<header class="article-header" aria-hidden="true">` ocultaba la fecha de publicación (`<time>`) y el tiempo de lectura al lector de pantalla en 8 posts. 3 posts ya tenían el patrón correcto (sin aria-hidden). Quitado el aria-hidden del header; el `.article-title-hidden` interior conserva el suyo (título redundante sigue oculto). Posts: como-detectar-fugas, baja-presion, cuando-llamar, cuanto-cuesta-plomeria-bano, desatascar-wc, mantenimiento-boiler-noritz, instalacion-tinaco, problemas-comunes.
  - **cont-003:** "aeradores" → "aireadores" (×2) en problemas-comunes (lo destapó el revisor-contenido del lote rotativo).
  - **cont-004/005:** fecha visible `<time>` contradecía datePublished (12/10 nov vs 21 nov en schema) → alineada a 2025-11-21 (campo canónico) en baja-presion + problemas-comunes.
  - + limpieza: 2 .bak huérfanos borrados (pasaron limpiar-huerfanos.py).
- **FALSO POSITIVO descartado:** movil-001 (revisor-movil dijo botón menú 24×18px a 375px). Medido con headless: **48×48px reales** porque `min-width/min-height:48px` del `@media 768px` gana sobre `width:24px` del `@media 480px`. El revisor leyó la declaración sin la cascada → se evitó un cambio CSS site-wide inútil.
- **Mecanización (FASE 9):** checks 4e (header aria-hidden) y 4f (blog indexable sin og:locale/og:site_name/twitter:url) en `check-plantilla.py`; disparan en pre-fix, 0 en árbol limpio. Regla BLOG/PLANTILLA consolidada en REGLAS.md (40 reglas, 3992/4000 tokens).
- **Crecimiento (FASE 6):** 0 páginas nuevas (GSC ciego). Optimización drenada: **bk-546d0a06** (9 blogs indexables + og:locale + og:site_name + twitter:url=canonical; marcha-paz noindex excluido). Cerrado STALE **bk-891b5be6** (breadcrumb ya resuelto en 890d13de).
- **Verificador (FASE 7): ok=true, 0 problemas** (alcance 10 HTML + 2 .bak; ci-gate 0 ALTA; gate-pagina 10/10 Jaccard máx 0.29; HTTP 200; JSON-LD parsea; fixes aplicados; anti-fuga limpia; 0 páginas vivas borradas).
- **Publicación (FASE 8): SÍ** (10 ≤ 18, verificador ok=true). Merge ff-only → no-ff → push al cierre.
- **Pendientes (humano):** re-auth GSC (ALTA, bloquea crecimiento); decisión badge "4.8/5" visible en blogs; diferidos a11y nav aria-label site-wide + :focus-visible botones; bk-6a3a1bcc imagen destape-bano; bk-b2b4878f year-desync cuanto-cobra (precios).

## Resumen de la corrida 2026-06-22 19:14 (auto/diario-20260622-1914 — AUTÓNOMA, diario)

- **Health check:** 6/6 rutas 200 (/, /contacto/, /servicios/, /blog/, /precios/, /servicios/reparacion-de-bombas-de-agua/), 0 "electricista" en home. Server en 8091 (concurrencia con sitio hermano).
- **Selector:** nada SERVIDO cambió desde 998c23b8 (solo scripts del driver) → solo PISO + lote rotativo.
- **PISO determinista LIMPIO:** ci-gate 0 ALTA; plantilla/indexabilidad/nap/linking/conversion 0; producción EN VIVO 0; e2e 0/3; secretos sec-001 (R-01); tracking trk Consent Mode (R-04); perf-real perf-001 baseline (R-03). 0 ciegos.
- **GSC:** infra-salud reportó "GSC ciego" → es el token CLI de mcp-local-seo (`invalid_grant`, refresh revocado). El **MCP gsc SÍ está vivo** (`gsc_list_sites` devolvió la propiedad) → GSC NO ciego; FASE 6 usó datos reales. Re-auth del token CLI = humano (bk-12b83ae9). Intento de copiar el token vivo de ~/gsc-mcp fue bloqueado por el clasificador (credential-exploration) — no se eludió.
- **Arreglado (1 clase, 19 págs):** BreadcrumbList JSON-LD nivel intermedio "Servicios" apuntaba a la ANCLA de la home `/#servicios` en vez del hub real `/servicios/`. Lo destapó el lote rotativo (2: plomeria-comercial, reparacion-de-llaves) y el checker nuevo (resto). 15 con formato sin espacios + **4 con espacios** (`emergencia-24-7`, `reparacion-de-fugas`, `reparacion-de-boiler`, `plomero-colonias-culiacan` hub) que un replace de string exacto SIN espacios falló → cazadas por el checker parse-aware. Colonias hijas NO tocadas (su nivel intermedio legítimo es el hub de colonias).
- **Mecanización (FASE 9):** check 2b en `check-indexabilidad.py` (ningún item intermedio del breadcrumb = `BASE/#...`); regla seo-201..304 consolidada en REGLAS.md (40 reglas, 3982/4000 tokens, dentro de presupuesto).
- **Crecimiento (FASE 6):** 0 páginas nuevas (sin hueco de demanda sin canibalizar). 1 enlazado: la página nueva de bombas (06-21) está "Google no reconoce esta URL — nunca rastreada", 1 enlace entrante. Añadido enlace contextual desde `correccion-baja-presion` (autoridad temática "bomba" ×38, rankea "bombas de agua" pos 4.7) → 1→2 enlaces entrantes, ruteando intención de reparar/instalar bomba (gsc-207/211). Indexación MCP tras merge.
- **Verificador (FASE 7): ok=true, 0 problemas** sobre el árbol final de 19 (re-corrido tras añadir las 4 + el checker).
- **Publicación (FASE 8): NO.** 19 págs HTML > candado de 18 → **PASE SUPERVISADO**, consistente con la decisión documentada 2026-06-18. Rama verificada, lista para aprobación/merge del dueño.


## Resumen de la corrida 2026-06-20 18:26 (auto/diario-20260620-1826 — AUTÓNOMA, diario)

- **Concurrencia:** el puerto 8080 estaba ocupado por OTRO agente autónomo (sitio hermano *electricista*, PID 9567); mi `http.server` falló al bindear y los curl golpeaban el sitio equivocado (/precios/ daba 404 falso). Levanté MI server en **8091** → health check válido del sitio plomero: **5/5 200** (/, /contacto/, /servicios/, /blog/, /precios/), 0 "electricista" en la home.
- **PISO determinista:** infra-salud **destapó infra-001 (ALTA, regresión)** → arreglado. ci-gate 0 ALTA, nap 0/78, conversión 0/67, linking 0/67, contenido-mecánico 0/78, e2e 0/3, producción EN VIVO 0, perf-001=R-03 (baseline), trk-001..004=R-04 (Consent Mode headless), sec-001=R-01 (secreto histórico inmutable). JUICIO (acotado): contenido+seo en las 2 doorway-diff de hoy (a-domicilio/cerca-de-mi) + lote rotativo de 5 servicios viejos (a11y/movil/contenido).
- **Arreglados y verificados (8 clases):**
  - **infra-001 (ALTA, regresión clase infra-003/005):** `check-css-paridad.py` (checker nuevo del 06-19) imprime texto humano, no JSON → el dead-man's switch lo marcó "verificación ciega". Añadido marcador `infra:utilidad-no-sensor` en cabecera. Re-corrido 0 hallazgos; paridad real OK (415 átomos).
  - **seo-001 (ALTA):** cerca-de-mi `twitter:url` apuntaba a la home → corregido a su canonical. canonical==og:url==twitter:url.
  - **color-form-rgba (5 servicios):** azul off-brand `#0066cc` en forma `rgba(0,102,204,0.1)` en el box-shadow de foco de formulario (el check 12 hex no lo cazaba); en economico con `outline:none` = foco casi invisible (a11y ALTA). → `rgba(227,100,20,0.25)` naranja, foco claramente visible. Solo inline → sin bump.
  - **color-red-rgba (2 blogs):** rojo `#dc2626`=`rgba(220,38,38)` en box-shadow → naranja. **Lo cazó el detector rgb NUEVO** del check 12.
  - **cont-001 (cerca-de-mi):** tiempos de llegada contradictorios (15-25/20-30/"30 min o menos" vs 30-60) → unificados al rango defendible 30-60 (gradiente 30-40→60 por sector).
  - **cont-002 (5 servicios):** "Ver todas las colonias (1,895)" inflado → "(643)" (alineado a la home, fuente de verdad).
  - **anclas-centro (bk-254d3596):** lista "con página propia" del centro listaba 9 colonias pero 6 enlazaban al hub (sin página) → dejadas las 3 reales.
  - **bk-3527704a:** verificado YA resuelto (hero tinaco con `.hero-content`, gate OK) → backlog cerrado.
- **Mecanización (FASE 9):** check 12 de `check-plantilla.py` AMPLIADO — detecta los colores off-brand también en `rgb()/rgba()` (deriva el triplete de cada hex del denylist; cazó 2 rojos que el hex no veía). 2 reglas consolidadas en REGLAS.md (39 reglas, 3988/4000 tokens): MARCA/COLOR (hex+rgb) e INFRA/SENSOR (log-regex + marcador utilidad).
- **Verificador independiente (FASE 7): ok=true, 0 problemas.** Re-corrió ci-gate (0 ALTA), check-infra (0), check-plantilla (JSON válido, 0), gate-pagina 8/8 CANDADO OK, HTTP 200 8/8, JSON-LD parsea 8/8, canonical==og:url==twitter:url en cerca-de-mi, 0 residuales (azul/1,895/rojo/tiempos viejos), 0 fuga electricista/GTM ajeno, email y wa.me intactos, 0 styles/sw/tests/precios tocados, 0 huérfanas.
- **Crecimiento (FASE 6):** GSC real (local-seo find_opportunities, NO ciego): demanda concentrada en 3 blogs (drenaje/wc/presión, 0 clics = ranking/SERP-features, gsc-214, no se toca). Bombas-de-agua confirmada (25+16 impr, pos 4.9/7.9) pero la página dedicada sigue diferida (bk-51f9103d, corrida dedicada). **0 páginas nuevas**; optimización drenada: 2 colores off-brand + anclas centro + 2 backlog cerrados.
- **Pendientes (no auto):** bombas-de-agua (página nueva, backlog), año-desync cuanto-cobra (decisión de frescura/precios del dueño), breadcrumb 42px template-wide (excede candado, requiere bump CSS), index.min.html muerto con datos viejos (borrado humano), + conocidos (a11y-301 footer h4, a11y-402/403 estrellas/main, perf-501/502).

## Resumen de la corrida 2026-06-19 11:10 (auto/diario-20260619-1110 — AUTÓNOMA, diario)

- **Health check:** 5/5 rutas clave 200 (/, /contacto/, /servicios/, /blog/, /precios/).
- **Cambios servidos desde la última auto-diario (acb8440c):** barrido meta site-wide (1 línea: `<meta robots>` a ~17 págs, mecánico) + **lead-tracking UNIVERSAL de hoy** (commit 18119d9b): listener delegado en captura que LEE el href de wa.me/tel sin reescribirlo → 0 riesgo de truncado wa.me; `main.js?v=20260619` versionado en las 31 refs, `sw.js` v27. Verificado limpio.
- **PISO determinista:** infra-salud **destapó infra-005 (ALTA)** → arreglado; ci-gate 0 ALTA (25 media/baja conocidas), nap 0, conversión 0, linking 0, indexabilidad 0, contenido-mecánico 0, secretos 0, producción EN VIVO 0, e2e 0. tracking trk-001..004 = Consent Mode headless (R-04, esperado). JUICIO (lote rotativo de 5 págs viejas): contenido/seo/a11y convergieron en defectos de plantilla de blog.
- **Arreglados y verificados (4 clases):**
  - **infra-005 (ALTA, dead-man's switch ciego):** el driver se renombró a `auto-agente-*.log` pero `check-infra.mjs` solo matcheaba `run-*.log` → ALTA falsa "mantenimiento DETENIDO" CADA día pese a correr. Regex → `/^(run|auto-agente)-.*\.log$/`. Re-corrido 0 hallazgos, JSON válido.
  - **Blog plantilla — div dentro de `<h2>` (8 posts):** CTA `<div>` de bloque embebido en el `<h2>` (HTML inválido). Cerrado el `</h2>` y movido el div a hermano. El revisor LLM halló 7; el **checker nuevo cazó el 8º** (cuanto-cobra, h2 con `style=` que el grep ad-hoc omitió).
  - **Blog plantilla — `related-articles` duplicada (5 posts):** removida la 2ª sección idéntica (queda 1).
  - **cont-014 año (como-detectar-fugas):** `Guía Práctica 2025`→`2026` (×4) al año del título real; fechas intactas.
  - **bk-2a3a24ed conteo colonias:** hub `640+`→`600+` (×4); el dataset real tiene 631 colonias → 600+ defendible, 640+ no. Unificado con la home ("más de 600"). Backlog cerrado.
- **Mecanización (FASE 9):** 2 checks nuevos en `check-plantilla.py` (4c: `<div>` en `<h2>`; 4d: `related-articles` duplicada) — disparan contra la versión pre-arreglo, 0 en el árbol limpio. 2 reglas nuevas en REGLAS.md (37 reglas, 3619/4000 tokens).
- **Verificador independiente (FASE 7): ok=true, 0 problemas** (descartó un falso "electricista" = prosa de negocio pre-existente, no en el diff). gate-pagina 8/8 OK, ci-gate 0 ALTA, HTTP 200, JSON-LD parsea, canonical==og:url, wa.me 526673922273 intacta, 0 GTM ajeno, 0 huérfanas. Headless: 0 errores JS, 0 h2-con-div en las páginas tocadas.
- **Crecimiento (FASE 6):** 1 optimización drenada (conteo colonias). **0 páginas nuevas** (sin hueco de demanda sin canibalizar; bombas-de-agua aprobada pero diferida como contenido extenso). **CTR-fix descartado**: el post de mayor impresión (drenaje-tapado, ~400 impr pos 3-8, 0 clics) YA tiene title/meta fuertes → 0 clics es ranking/SERP-features, no snippet (gsc-214); reescribir sería cambio-por-cambiar.
- **Diff:** 12 archivos de sitio/pipeline (check-infra.mjs, check-plantilla.py, 8 blogs, hub colonias, BACKLOG) + docs — bajo el tope de 18. Sin CSS/JS servidos, sitemap, precios ni tests tocados.
- **Pendientes encolados (no auto):** aria-hidden en `article-header` de 8 posts (a11y, oculta fecha al lector de pantalla), metas de blog faltantes (twitter:url/og:locale/og:site_name/theme-color), anclas engañosas en plomero-centro-culiacan, año-freshness de cuanto-cobra (decisión humana), + conocidos (bombas-de-agua, breadcrumb-#servicios 18 págs).

## Resumen de la corrida 2026-06-18 15:37 (auto/diario-20260618-1537 — AUTÓNOMA, 2ª del día / FORCE_RUN)

- **Contexto:** la corrida diaria normal ya había corrido y PUBLICADO hoy (merge `1f89c325`, marca `last-run-day=20260618`). Esta es una 2ª corrida forzada (driver PID 58553). Por eso el diff de páginas servidas desde la última auto-diario es casi nulo.
- **Health check:** 5/5 rutas clave 200 (/, /contacto/, /servicios/, /blog/, /precios/).
- **Fan-out selectivo:** selector contra `1f89c325` → 1 sola página servida cambiada (reparacion-de-fugas, el `<meta robots>` ya publicado hoy). PISO determinista corrido directo, **limpio sobre corpus real**: infra-salud exit 0 (sensores sanos), ci-gate 0 ALTA (25 media/baja conocidas = theme-color+tablas), NAP 0/78, conversión 0/67, e2e 0/3, indexabilidad 0, producción EN VIVO 0 hallazgos. Conocidos/esperados sin re-reportar: sec-001 (secreto histórico en git, R-01, no bloquea publicación), trk-001..004 (Consent Mode denegado en headless = esperado).
- **Crecimiento (FASE 6) — drenado 1 de optimización del backlog:**
  - **bk-028dd6c5 / deuda-robots-001** (BAJA, fix-deuda): 8 páginas de servicio indexables (en sitemap, ninguna noindex) no tenían `<meta name="robots">` — lo expone el gate al editarlas (mismo patrón que reparacion-de-fugas hoy). Añadido el estándar `index, follow, max-image-preview:large…` antes del canonical en: correccion-baja-presion, deteccion-de-fugas, emergencia-24-7, instalacion-de-sanitarios, mantenimiento-de-boiler, plomero-colonias-culiacan, reparacion-de-boiler, tecnico-de-gas-culiacan. Solo HTML → sin bump `?v=`/sw.js. **gate-pagina 8/8 OK** (Jaccard 0.19–0.42), ci-gate 0 ALTA, HTTP 200 en las 8.
  - Backlog: el resto NO se drenó por riesgo/alcance: bombas-de-agua (página nueva aprobada por el dueño, contenido extenso — se deja en cola para una corrida dedicada, no se rushea), conteo colonias 600/640+ (no toco claim sin cifra real), imagen tinaco (asset binario), breadcrumb #servicios 18 págs (excede candado).
- **Verificador independiente (FASE 7): ok=true, 0 problemas.** Re-corrió gate-pagina 8/8, ci-gate 0 ALTA, HTTP 200, canonical==og:url donde existe, robots ×1 por página antes del canonical, 0 fuga electricista/GTM ajeno, email correcto, wa.me intactas, instalacion-de-tinaco intacta.
- **Hallazgo nuevo (pendiente, NO auto):** **plt-hero-tinaco** (MEDIA) — `instalacion-de-tinaco` tiene `class="hero"` pero le falta el wrapper `div.hero-content` del estándar → validate-landing/gate-pagina FALLAN. Por eso se EXCLUYÓ del lote de robots (editarla la metía al gate y bloqueaba el push). Encolado bk-3527704a (requiere reestructura de hero + verificación visual). También **seo-ogurl-6serv** (BAJA): 6 de las 8 páginas no emiten `<meta property="og:url>` (canonical correcto; inconsistencia, no rotura).
- **Candados paso 8:** verificador ok=true; diff 8 archivos de sitio + docs ≤ 18; 0 borrados/renombrados; 0 tests/precios/CSS/JS tocados; sin electricista/GTM ajeno. → cumplidos.

## Resumen de la corrida 2026-06-16 08:31 (auto/mantenimiento-20260616-0831 — AUTÓNOMA)

- **Health check:** 5/5 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /blog/), node v22.18 vía /usr/local/bin. Compuerta `revisor-infra-salud` (check-infra.mjs) **exit 0, 0 hallazgos** (sensores sanos). main = origin/main sincronizados al inicio.
- **18 revisores.** Deterministas (corridos directos) **limpios sobre corpus real** (no ciegos): indexabilidad 0, conversión 0/99, NAP 0/110, linking 0/99, e2e 0/3, producción 0 (prod LIMPIA, real), secretos exit 0, perf-real OK presupuesto. Con hallazgos: plantilla 26 (todas BAJA: theme-color + 3 tablas = plt-001..026 conocidos), contenido-mecánico 1 (cont-001=R-02), tracking 4 (Consent Mode esperado), perf-real perf-001 (falta baseline=R-03). LLM (seo, móvil, a11y, perf, links, contenido-subj, gsc-datos-reales) en paralelo.
- **Arreglado y verificado (1):**
  - **movil-501** (MEDIA) — `/precios/`: los 25 enlaces `.service-link` de la tabla de precios (selector solo en `<style>` inline, no en los 3 CSS) rendían ~41px de alto en 375px (< 44px táctil). Añadido `display:inline-block; padding:0.35rem 0` → mín 60px ≥44 en 375px, 0 overflow móvil/desktop, enlaces desktop normales (38px). Solo CSS inline → sin bump de `?v=`/sw.js. Verificado headless 375 y 1280. Deterministas re-corridos sin regresión (conversión 0/99, indexabilidad 0, secretos exit 0, /precios/ 200).
- **Candados paso 8:** auto-revisión limpia (1 archivo de sitio, 2 líneas, solo CSS inline, 0 wa.me/JSON-LD/tests/assets compartidos), diff 1≤15, 0 borrados/renombrados, secretos exit 0. → cumplidos.
- **Pendientes humano nuevos (6):** **seo-404** (MEDIA — canibalización on-page "reparación de boiler" entre mantenimiento-de-boiler y reparacion-de-boiler, copy), **seo-405** (MEDIA — canibalización "destape" entre destape-de-drenajes y desazolve-de-drenajes, copy), a11y-402 (estrellas ★★★★★ sin aria en ~92 págs, BAJA, excede candado), a11y-403 (falta `<main>` en 46 págs, BAJA, excede candado), perf-505 (montserrat-700/800.woff2 byte-idénticos, BAJA, requiere subset+bump sw.js), gsc-219 (bug cosmético de logging en gsc-index.mjs L54, BAJA, tooling). Bajas: trk-001..004 (Consent Mode), plt-001..026 (theme-color/tablas), perf-001=R-03, cont-001=R-02, sec-001=R-01.
- **revisor-gsc NO ciego:** datos GSC reales (source: search_console_api, 50 keywords, 8 páginas inspeccionadas, propiedad correcta sc-domain). Confirmados conocidos sin re-reportar: gsc-217/202 (hub /servicios/ aún "Descubierta sin indexar/nunca"), gsc-218 (tecnico-de-gas sin indexar). Sin des-indexaciones nuevas.
- **Aprendizaje:** 1 regla nueva en REGLAS.md — MÓVIL/TAP-TARGET: los enlaces inline dentro de tablas (p.ej. `.service-link` en /precios/) rinden a la altura de línea (~41px) y quedan bajo 44px; fix `display:inline-block; padding` (amplía el patrón de tap targets de breadcrumbs a enlaces de tabla).

## Resumen de la corrida 2026-06-14 18:25 (auto/mantenimiento-20260614-1825 — AUTÓNOMA)

- **Health check:** 5/5 rutas clave en 200 (/, /precios/, /contacto/, /servicios/, /blog/), node v22.18 vía /usr/local/bin. Compuerta `revisor-infra-salud` (check-infra.mjs) **exit 0, 0 hallazgos** (sensores sanos).
- **18 revisores.** Deterministas (corridos directos) **limpios sobre corpus real** (no ciegos): indexabilidad 0, conversión 0/99, NAP 0/110, linking 0/99, e2e 0/3, producción 0 (prod-001 sin regresión, prod LIMPIA), secretos exit 0. Con hallazgos: plantilla 26 (todas BAJA: theme-color + 3 tablas), contenido-mecánico 1 (cont-001=R-02), tracking 4 (Consent Mode esperado), perf-real OK presupuesto (falta baseline=R-03). LLM (seo, móvil, a11y, perf, links, contenido-subj, gsc) en paralelo.
- **Arreglados y verificados (3):**
  - **movil-401** (ALTA) — `servicios/reparacion-de-boiler`: botones flotantes WhatsApp/llamada rotos en móvil (única página con esos botones en HTML sin sus reglas `.floating-btn` en el `<style>` inline; no están en los 3 CSS compartidos) → caían a `position:static` y <44px. Añadidas las 4 reglas verbatim. Verificado headless 375px: ambos `position:fixed` 54×54, colores correctos, `border-radius:50%`, wa.me intacto, 0 pageerror.
  - **cont-003** (MEDIA) — año caduco en el título de la tarjeta del post de tinaco (2024/2025 → 2026, coincide con el título real "[2026]") en home + 5 servicios. `datetime` de publicación intacto.
  - **seo-401** (MEDIA) — 59 enlaces internos a `/servicios/<slug>/index.html` → forma de directorio canónica (home + 5 servicios), igualando los 535+ restantes. checker-linking sigue 0.
  - Solo HTML (`<style>` inline + texto/href) → sin bump de `?v=`/sw.js. Diff: 7 archivos HTML (los 6 de cont-003/seo-401 se solapan + reparacion-de-boiler).
- **Candados paso 8:** auto-revisión limpia (solo HTML, 0 tests/CSS/JS/XML, wa.me intacto en los 7, JSON-LD válido), diff 7≤15, 0 borrados/renombrados, secretos exit 0. → cumplidos.
- **Pendientes humano nuevos:** **cont-002** (ALTA — cuerpo de `tecnico-de-gas-culiacan` entero sin acentos, incl. "anos"→"años"; es copy amplio, fuera de auto), **gsc-217** (ALTA — hub /servicios/ nunca rastreado pese a sitemap/enlaces correctos; acción GSC + revisar calidad), seo-402 (NAP/geo de relleno en LocalBusiness del hub+10 servicios), seo-403 (3ª URL canibalización precios), a11y-401 (skip-link falta en ~114 págs → excede candado), gsc-218 (tecnico-de-gas nuevo sin indexar, vigilar). Bajas: trk-001..004 (Consent Mode), plt-001..026 (theme-color/tablas), perf-001=R-03, cont-001=R-02, sec-001=R-01.
- **Aprendizaje:** 3 reglas nuevas en REGLAS.md — (1) MÓVIL/PLANTILLA: los botones flotantes se estilan inline por página; si el HTML los usa, el `<style>` debe traer `.floating-btn` (chequeo grep). (2) SEO/ENLACES: enlaces internos en forma de directorio, no `/index.html`. (3) CONTENIDO/AÑO: el año embebido en títulos de tarjetas de relacionados se desincroniza del título real del post.

## Resumen de la corrida 2026-06-13 20:00 (auto/mantenimiento-20260613-2000 — AUTÓNOMA, PUBLICADA)

- **Health check:** 9/9 rutas en 200, main.js sintaxis OK (node v22.18 vía /usr/local/bin), wa.me intacto (526673922273), main.js?v=20260613 (30 refs) y CSS ?v=20260612c consistentes, sw.js v25 precachea la versión correcta. 0 regresiones (los 8 revisores confirmaron perf-301..314, prod-001 sin reaparecer, og:url=canonical, fetchpriority único, versionado y links sanos).
- **Revisores (8 en paralelo):** seo, móvil, a11y, perf, links, gsc, indexabilidad, producción. revisor-produccion: **producción LIMPIA** (0 pageerror en /, /precios/, /contacto/; prod-001 sin regresión; 8/8 URLs 200; HSTS/XCTO/RefPol presentes; form 2xx). revisor-links: 0 rotos. revisor-indexabilidad: idx-001 (=seo-304).
- **Arreglados y verificados (2):**
  - **seo-304** (ALTA, idx-001) — servicios/desazolve-de-drenajes: BreadcrumbList de 2 niveles sin el intermedio "Servicios". Insertado pos2 Servicios→/servicios/ y renumerada la página a pos3 (item==canonical). El checker de indexabilidad pasó de 1 a **0 hallazgos**.
  - **a11y-302** (MEDIA) — exit-intent popup sin `role="dialog" aria-modal="true" aria-labelledby` en 5 páginas de servicio (cerca-de-mi, desazolve, a-domicilio, economico, instalacion-de-boiler). Añadidos los atributos + `id="exit-popup-title"` al h3, replicando index.html. 5/5 verificadas (popup-role=1, title-id=1, HTTP 200, JSON-LD válido, wa.me intacto).
  - Solo HTML (sin CSS/JS) → sin bump de ?v=/sw.js.
- **Candados paso 8: 3/3 cumplidos → PUBLICADO.** Diff: 5 archivos, 11 inserciones / 5 borrados, 0 archivos borrados/renombrados, 0 tests tocados. Merge **e2418d1e** a main + push **ef3b57f7..e2418d1e**. **Indexación COMPLETA**: el hook envió las 5 URLs editadas a Google (5 enviadas, 0 en cola, 0 descartadas — cuota disponible hoy). infra-002 sigue vigente: push con `PATH=/usr/local/bin:$PATH git push`.
- **Pendientes humano nuevos:** **gsc-215** (bug 1-string en gsc-index.mjs L53 que deja CIEGA la verificación de indexación — recomendado arreglar pronto), gsc-216 (ping sitemap a endpoint Google muerto), perf-501 (fuentes con fetchpriority=high en 26 págs, medir LCP), perf-502 (3 woff2 Inter idénticos ~76KB), perf-503/504 (binarios pesados), a11y-303 (menu-btn aria en 99 págs), seo-004 (6 redirect-stubs sin noindex). Bajas no tocadas: seo-305, movil-301, seo-002/107.
- **Aprendizaje:** 1 regla nueva en REGLAS.md — A11Y/PLANTILLA: el exit-intent popup de páginas de servicio debe llevar `role="dialog" aria-modal="true" aria-labelledby="exit-popup-title"` + `id` en el h3, igual que index.html (chequeo `grep -c 'id="exit-intent-popup" role="dialog"'` == 1).

## Resumen de la corrida 2026-06-12 20:01 (auto/mantenimiento-20260612-2001 — AUTÓNOMA, PUBLICADA)

- **Health check:** 9/9 rutas en 200, main.js sintaxis OK (node v22.18 vía /usr/local/bin), wa.me intactas (526673922273). 0 regresiones (los 6 revisores confirmaron que perf-301..314, og:url=canonical, fetchpriority único, versionado CSS/JS y links siguen sanos).
- **Arreglados y verificados (3):** seo-301/302/303 — BreadcrumbList JSON-LD truncado a 1 item (Inicio→home, último item ≠ canonical) en 3 páginas de servicio indexables (instalacion-de-boiler, plomero-a-domicilio, plomero-cerca-de-mi). Añadidos niveles 2 (Servicios) y 3 (la página, item==canonical), igualando el patrón del resto. Verificado: JSON-LD reparseado OK, pos3==canonical, HTTP 200 en las 3. Solo HTML → sin bump de ?v=/sw.js.
- **Candados paso 8: 3/3 cumplidos → PUBLICADO.** Merge eee3c396 a main + push fcb190a1..eee3c396. Indexación: el hook (infra-001 resuelto) detectó las 17 URLs (incl. las 3 editadas) pero la cuota diaria de Google sigue agotada → encoladas en pending-index.json para reintento automático (0 perdidas). El `git push` pelado falló por `node: command not found` en el hook (infra-002); se completó con `PATH=/usr/local/bin:$PATH git push`.
- **Pendientes humano nuevos (10):** gsc-210..214 (clusters baño/drenaje/bombas/fugas con CTR 0 + ruido off-target), perf-401 (minificar main.js, riesgo wa.me), perf-402 (preload hero), a11y-301 (footer h4→h3 en 18 págs), movil-301 (2ª tabla sin wrapper), infra-002 (hook pre-push sin node en PATH). Bajas no tocadas: seo-304 (desazolve breadcrumb 2 niveles), seo-305 (typo año marcha-paz noindex).
- **Aprendizaje:** 2 reglas en REGLAS.md — (1) variante del bug og:url=canonical: el BreadcrumbList puede quedar truncado a 1 nivel con el último item apuntando a la home; verificar que el último `item` == canonical y que existan los 3 niveles en páginas de servicio. (2) infra/push: el hook pre-push necesita node en PATH (`/usr/local/bin`); usar `PATH=/usr/local/bin:$PATH git push`.
