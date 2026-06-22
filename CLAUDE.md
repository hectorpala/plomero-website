# Plomero Culiacán — Instrucciones del proyecto

## Memoria (LEER SIEMPRE antes de trabajar)
- ANTES de hacer cualquier cambio, lee REGLAS.md (errores ya cometidos que NO debes repetir).
- **NEGOCIO.md** = fuente de verdad del NEGOCIO (servicios que ofrece/no, política precios/año, qué se auto-crea). Las decisiones de negocio se DERIVAN de ahí ("auto si es plomería"), no se mandan a humano si la respuesta ya está en el archivo.
- **Quién DECIDE el negocio**: el panel `subagent_type: decisor-negocio` (`.claude/agents/decisor-negocio.md`) = dev senior + maestro plomero/experto de Culiacán. Lee NEGOCIO.md + demanda GSC y decide crear/enriquecer/escalar (FASE 6). Decide; el backbone determinista ejecuta y los candados verifican.
- Registra hallazgos nuevos en HISTORIAL.jsonl (una línea JSON por hallazgo).
- El estado de la última corrida está en ESTADO.md.
- VERIFICADOR (FASE 7) = `subagent_type: verificador` (`.claude/agents/verificador.md`), SOLO-LECTURA (sin Edit/Write, git de solo-lectura). JAMÁS general-purpose (incidente verifier-rogue 2026-06-21).

## Reglas de trabajo (estilo Anthropic)
- VERIFICA tu trabajo antes de darlo por hecho: corre el sitio y compruébalo, no asumas que "se ve bien".
- HEALTH CHECK primero: antes de tocar nada, revisa que lo existente no esté roto.
- UNA mejora por sesión. No abarques de más.
- JAMÁS borres ni edites tests para "hacer pasar" algo. Eso oculta funcionalidad rota.
- Cambios mínimos. No refactorices fuera del alcance pedido.
- Muestra EVIDENCIA (salida de comando, captura) en vez de afirmar éxito.

## Reglas duras del sitio (resumen — el detalle está en REGLAS.md)
- CSS: al cambiar estilos, versionar URL (?v=AAAAMMDD) Y subir versión del service worker (sw.js). Aplicar el fix en los TRES archivos CSS (styles.css, styles.min.css y el .hash.css servido).
- MÓVIL: tablas con scroll horizontal; imágenes con max-width:100%; grids con auto-fit minmax, no columnas fijas; tap targets ~44px.
- SEO: nada de doorways (páginas casi idénticas); coordenadas GPS reales y únicas; sin aggregateRating self-serving en blog; og:image/twitter:image deben existir; al borrar páginas, cero enlaces rotos + actualizar sitemap.
- JS: tras minificar, verificar que las URLs wa.me no queden truncadas (rompe todo el sitio).
- CONTACTO: el email correcto es info@plomeroculiacanpro.mx. NUNCA un email de "electricista" (sería fuga de la plantilla origen del clon).
- ANTI-FUGA (clon del electricista): la palabra "electricista" y el GTM del electricista (GTM-5Z2QRZ5Q) JAMÁS deben aparecer en este sitio de plomería. El generador (`gen-landing.py`) y `validate-landing.sh` ABORTAN si las detectan.
- MARCA/ESTILO (contrato — la home `index.html` es la FUENTE DE VERDAD): la paleta es NARANJA — `--brand:#E36414`, `--brand-light:#F97316`, `--brand-dark:#C2410C` (texto/acento `#C2410C`, fondos claros `#FFF7ED`) + neutros slate (`#475569`/`#64748b`/`#1e293b`…). Verdes LEGÍTIMOS que se conservan: `#22c55e` (punto "disponible"), `#25d366` (WhatsApp), `#34a853`/`#4285f4`/`#ea4335`/`#fbbc05` (logo de Google, solo en `<path fill>` de SVG). PROHIBIDO cualquier azul/morado/rojo/verde decorativo (cajas "tip" en HTML inline) — hacían verse el blog distinto de la home. Tipografía: Montserrat 800 (títulos) + Inter (cuerpo) vía `@font-face` inline; espaciado/sistema visual viven en los `styles*.css` (las 3 hojas en PARIDAD). Las páginas NUEVAS heredan todo porque se crean COPIANDO un esqueleto byte a byte (`gen-landing.py`→`servicios/plomero-cerca-de-mi/`, `crear-servicio.py`→`servicios/plomero-zona-oriente-culiacan/`, `generar-colonias.py`) — NUNCA escribir colores/tipografía a mano. Enforcement: `check-plantilla.py` (check 12) MARCA color off-brand y `auto-fixers.py` (fixer `color-off-brand`) lo AUTO-SANA a diario. Detalle/casos en REGLAS.md (color-blog-2026062x).

## Pipeline de crecimiento autónomo (clon adaptado del Auto Agente del electricista)
- **Mapa completo del sistema: `AUTOMATIZACION.md`** (cómo encajan skill + orquestador + motor + driver diario).
- **Orquestador (punto de entrada determinista): `scripts/crecer.py`** — `estado` | `servicio spec.json` | `colonia spec.json` | `gate <ruta>` | `publicar "msg"`. Automatiza crear + sitemap (`sitemaps/main_sitemap.xml`) + enlace en la home + bump sw (`CACHE_NAME='plomero-culiacan-vN'`) + candado + publicar.
- Invocar el cerebro con `/expandir-sitio` (skill en `.claude/skills/expandir-sitio/SKILL.md`). Hermano de `/mantener-sitio`: aquél ARREGLA, éste CREA lo que falta. La auditoría GSC (propiedad `https://plomeroculiacanpro.mx/`) y la indexación por MCP viven en el skill. SIN tope numérico: loop-until-dry sobre el backlog (`.pipeline/gestor-backlog.py`), con freno por DEMANDA REAL + anti-doorway, no por un número (ver `.pipeline/BACKLOG-DESIGN.md`).
- Backbone determinista (garantiza paridad de plantilla y bloquea doorways):
  - `python3 .pipeline/gen-landing.py spec.json` — genera copiando un esqueleto byte a byte + sustituciones afirmadas (aborta si no calzan o si hay fuga "electricista").
  - `python3 .pipeline/gate-pagina.py <ruta/index.html> ...` — candado: validate-landing + ci-gate (0 ALTA) + anti-doorway (Jaccard < 0.80 vs hermanas).
- Generadores reusables (corren `--ejemplo` para ver el spec): `scripts/crear-servicio.py` (servicio nuevo; esqueleto `servicios/plomero-zona-oriente-culiacan/`, el campo `cuerpo_html` lleva la PROSA ÚNICA) · `scripts/diferenciar-colonia.py` (promueve colonia noindex→indexable; hoy no hay colonias noindex).
- AUTONOMÍA AMPLIADA (2026-06-21): `auto-fixers.py` ahora tiene ASSET FIXERS de CSS compartido (p.ej. `tap-target-44`) que editan los 3 CSS y **bumpean `?v=` en las ~70 páginas + `sw.js`** (el CSS es `immutable` 1 año → cambiar contenido NO basta, hay que cambiar la URL). `.pipeline/limpiar-huerfanos.py run --apply` borra artefactos huérfanos (`*.min.html`/`*.bak`) solo si pasan 4 condiciones (cero refs + no en sitemap + git-trackeado). El agente ya NO punto-humano estos dos. RED de seguridad en `.git/hooks/pre-push` (copia rastreada en `.pipeline/hooks/`, instala con `install.sh`): ABORTA si se borra una página viva (referenciada/en sitemap) o la home. El cap de 18 de FASE 8 cuenta PÁGINAS HTML; un cambio de asset (CSS+?v=+sw.js) o un borrado de huérfano NO cuentan.

## Auto Agente diario (mantener + crecer + verificar + aprender, una corrida)
- Driver: `.pipeline/crecer-diario.sh` · Prompt (10 fases): `.pipeline/crecer-diario-prompt.txt` · Horario 18:25: `.pipeline/launchd/com.plomeroculiacan.autoagente.plist`.
- Reemplaza al viejo job de solo-mantenimiento (comparten el lock `/tmp/plomero-mantener-sitio.lock` para no correr ambos). El `catchup.sh` recupera la corrida si la Mac estaba apagada a la hora.

## Comandos útiles
- git log --oneline -30  (ver historia reciente)
- Servidor local para probar: (usar el que ya use el proyecto)
