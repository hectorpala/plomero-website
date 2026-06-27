# Sistema de automatización — Plomero Culiacán

> Clon adaptado del "Auto Agente" del sitio Electricista Culiacán. El motor determinista,
> el orquestador, los generadores y el cerebro diario se copiaron y se ADAPTARON a las
> realidades de este sitio (dominio plomeroculiacanpro.mx, email info@plomeroculiacanpro.mx,
> sitemap hijo `sitemaps/main_sitemap.xml`, `sw.js` con `CACHE_NAME='plomero-culiacan-vN'`,
> directorio de colonias `plomero-colonias-culiacan`, roster de revisores propio de plomero).
> La PALABRA-FUGA está INVERTIDA respecto al electricista: aquí la contaminación a bloquear
> es **"electricista"** y el GTM del electricista **GTM-5Z2QRZ5Q** (el generador y el
> validador ABORTAN si aparecen).

## 🤖 Auto Agente Plomero (todo el sistema junto, 1 corrida diaria)

**Auto Agente Plomero** es el sistema completo corriendo solo, sin supervisión, una vez al
día (18:25). En una sola corrida hace CUATRO trabajos:

| Fase | Qué hace |
|---|---|
| **A) Corrige** | Errores **mecánicos** (CSS, links/imágenes rotas, schema, CLS…) **y humanos/de contenido** (ortografía, caracteres mal codificados, claims que violan reglas, email contaminado, fuga "electricista") — reescritos bien y por completo. |
| **B) Crece** | **Loop-until-dry según Google Search Console** (MCP): detecta TODOS los huecos con datos reales (impresiones sin página propia), los encola en el backlog y los drena por prioridad. SIN tope numérico — el freno es DEMANDA REAL + anti-doorway, no un número. 0 páginas si no hay señal (nunca fuerza doorways); la optimización se drena sin límite. |
| **C) Verifica** | Un **agente verificador** independiente y escéptico re-corre los candados y carga cada página tocada para demostrar que **todo quedó bien** ANTES de publicar. Si algo falla, no publica. |
| **D) Aprende** | Un **agente aprendiz** convierte cada error en una **regla permanente** (REGLAS.md) y, si es mecanizable, en un **checker**. El sistema se vuelve más inteligente con cada corrida. |

Solo publica si pasa TODOS los candados (verificador ok + diff acotado + sin borrados raros) y
sincronizando con el remoto (jamás `git push --force`). Te manda el **parte por email** siempre.

**Piezas:** `.pipeline/crecer-diario-prompt.txt` (las 10 fases) · `.pipeline/crecer-diario.sh` (driver) ·
`.pipeline/launchd/com.plomeroculiacan.autoagente.plist` (horario 18:25).

**Activar** (reemplaza al viejo job de solo-mantenimiento para no correr ambos):
```bash
launchctl unload ~/Library/LaunchAgents/com.plomeroculiacan.mantener.plist 2>/dev/null
cp ".pipeline/launchd/com.plomeroculiacan.autoagente.plist" ~/Library/LaunchAgents/
launchctl load  ~/Library/LaunchAgents/com.plomeroculiacan.autoagente.plist
launchctl start com.plomeroculiacan.autoagente   # opcional: probar una corrida YA
```

---

## El orquestador: `scripts/crecer.py` (punto de entrada del crecimiento)

| Comando | Qué hace |
|---|---|
| `python3 scripts/crecer.py estado` | Dashboard: nº de servicios, colonias (total/indexables), blogs, URLs en `sitemaps/main_sitemap.xml`, versión de sw, último commit, candados. |
| `python3 scripts/crecer.py servicio spec.json` | Crea servicio **+ sitemap + enlace en la home + bump sw + candado**, todo automático (revierte si falla). |
| `python3 scripts/crecer.py colonia spec.json` | Promueve colonia noindex→indexable **+ sitemap + candado** (revierte si falla). |
| `python3 scripts/crecer.py gate <ruta>` | Atajo al candado. |
| `python3 scripts/crecer.py publicar "msg"` | Rama → commit → merge `--no-ff` → push seguro (el pre-push **auto-indexa** en Google). |

Specs de contenido:
- `python3 scripts/crear-servicio.py --ejemplo > spec.json`  (servicio nuevo; el campo `cuerpo_html` lleva la PROSA ÚNICA)
- `python3 scripts/diferenciar-colonia.py --ejemplo > spec.json`  (promover colonia noindex; hoy no hay ninguna noindex)

## Motor determinista (garantiza calidad y bloquea doorways)
- `.pipeline/gen-landing.py` — genera una landing copiando un esqueleto byte a byte + sustituciones afirmadas (aborta ante drift o fuga "electricista").
- `.pipeline/gate-pagina.py` — candado todo-en-uno: `validate-landing.sh` + `ci-gate.py` (0 ALTA) + anti-doorway (Jaccard < 0.80 vs hermanas).
- `.pipeline/ci-gate.py` — corre `check-plantilla.py` + `check-indexabilidad.py` y FALLA si hay ALTA.
- `validate-landing.sh` — valida la estructura estándar de una landing de servicio (referencia: `servicios/plomero-zona-oriente-culiacan/`).
- `scripts/crear-servicio.py` · `scripts/diferenciar-colonia.py` — generadores de contenido (specs JSON).

## El cerebro (decide qué crear)
- `.claude/skills/expandir-sitio/SKILL.md` — agente de crecimiento (`/expandir-sitio`). Audita huecos con datos reales de GSC (MCP), encola en `.pipeline/gestor-backlog.py` y drena en loop-until-dry (sin tope numérico; freno = demanda real + anti-doorway) vía el orquestador. Ver `.pipeline/BACKLOG-DESIGN.md`.
- `.claude/skills/mantener-sitio/SKILL.md` — hermano que *arregla* lo existente (`/mantener-sitio`).

## Esqueleto representativo
La plantilla estándar de servicio es la de las páginas ~520 líneas (p.ej. las zona-pages).
`servicios/plomero-cerca-de-mi/` es una página ATÍPICA e inflada (1476 líneas) — NO usar de
esqueleto. `crear-servicio.py` usa `servicios/plomero-zona-oriente-culiacan/` como esqueleto.
