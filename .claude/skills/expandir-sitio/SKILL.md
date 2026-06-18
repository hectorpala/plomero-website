---
name: expandir-sitio
description: Agente de CRECIMIENTO autónomo — determina qué le falta al sitio (oportunidades GSC, geo, blog, mejoras), CREA las páginas con contenido único y, si pasan TODOS los candados, publica e indexa solo. Invocar con /expandir-sitio.
---

# Agente de crecimiento autónomo — `/expandir-sitio`

Hermano de `/mantener-sitio`: aquél **arregla** lo existente; éste **expande** el sitio
creando lo que le falta. Trabaja en rama, verifica con candados deterministas y
**auto-publica solo si TODO pasa** (si algo falla, deja en rama y avisa).

Muestra EVIDENCIA (salida de comando) en cada fase. NO afirmes éxito sin probarlo.

## Configuración de la corrida (defaults)
- `MAX_PAGINAS = 3` — tope duro de páginas nuevas por corrida (evita generación masiva = doorway).
- `DIMENSIONES = [gsc, geo, blog, mejoras]` — las 4 activas.
- `AUTO_PUBLICA = sí` — si los candados pasan, mergea a main + indexa. Si fallan, NO publica.
- Propiedad GSC: `https://plomeroculiacanpro.mx/`. Email del sitio: `info@plomeroculiacanpro.mx`.

## MODO AUTÓNOMO (NO PARAR)
Una vez invocado, ejecuta las 8 fases de corrido **sin detenerte a pedir confirmación**.
Decide con las REGLAS DURAS y los datos; no preguntes al humano. Al inicio, anuncia en UNA
lista breve QUÉ vas a hacer (las acciones priorizadas) y luego hazlo todo hasta publicar.
Las ÚNICAS razones legítimas para no publicar algo son:
  (a) un CANDADO falla → deja esa página en la rama, NO la publiques, y sigue con las demás;
  (b) una acción marcada como **decisión de negocio** (p.ej. un nicho nuevo que el dueño no ofrece):
      NO la ejecutes; solo anótala como PENDIENTE HUMANO y continúa.
Nunca te detengas "por si acaso". Si una acción es de bajo riesgo y pasa candados, publícala.

## REGLAS DURAS (innegociables — leer antes de crear nada)
1. **Anti-doorway:** jamás crear páginas casi-idénticas. Cada página debe tener contenido
   sustancialmente único (H1, hero, secciones, FAQ, schema). El candado
   `gate-pagina.py` BLOQUEA si la similitud Jaccard ≥ 0.80 con una hermana. Respétalo.
2. **Paridad de plantilla:** toda página nueva replica la estructura estándar del sitio.
   Por eso se generan con `gen-landing.py` desde un esqueleto que YA pasa
   validate-landing.sh — NO se escriben a mano desde cero.
3. **Email / anti-fuga:** el email correcto es `info@plomeroculiacanpro.mx`. NUNCA debe
   colarse "electricista" ni el GTM del electricista (GTM-5Z2QRZ5Q): el generador y el
   validador ABORTAN si detectan esa fuga de la plantilla origen.
4. **Sin enlaces rotos:** todo `href` interno debe resolver a un archivo real. Verifícalo.
5. **`index.html` es intocable salvo necesidad real:** si hay que cambiarlo, se arregla
   PRIMERO ahí y se propaga; no es el objetivo de este agente (su objetivo es crear páginas).
6. **noindex fuera del sitemap;** index dentro del sitemap. Cada página nueva indexable
   se agrega a `sitemaps/main_sitemap.xml` y se le dan enlaces ENTRANTES (no huérfanas).
7. **Hero CTA estándar:** toda página con hero usa el MISMO acomodo del esqueleto estándar
   (botón WhatsApp `btn-primary` + el bloque de contacto). No inventes variantes de hero.

---

## FASE 0 — Memoria
Lee `REGLAS.md`, `ESTADO.md` y las últimas líneas de `HISTORIAL.jsonl`. Anota qué ya se
hizo para no repetir (p.ej. las zona-pages y colonias ya existen).

## FASE 1 — Health check
Levanta `python3 -m http.server 8080` en background. `curl -sI` a la home y 2-3 páginas
clave (/contacto/, /servicios/, /blog/). Si algo ya está roto (≠200), PARA y repórtalo:
no se expande sobre un sitio roto.

## FASE 2 — AUDITORÍA DE HUECOS (determinar bien qué falta)
Recolecta señales de las 4 dimensiones y construye una lista RANKeada. Sé concreto.

### 2a. Oportunidades de GSC (datos reales — máxima prioridad)
Con el MCP `gsc` sobre la propiedad real `https://plomeroculiacanpro.mx/`:
- `mcp__gsc__gsc_opportunities` y `mcp__gsc__gsc_keywords` → queries con IMPRESIONES pero
  posición 8-30 y/o sin página dedicada (el sitio sale "de rebote"). Cada una = candidata
  a página propia que captaría ese tráfico.
- `mcp__gsc__gsc_performance` → páginas con CTR bajo / impresiones altas (mejora) y queries
  emergentes.
- `mcp__gsc__gsc_inspect` sobre páginas nuevas recientes → "descubierta sin indexar" =
  reforzar enlaces internos, no crear duplicado.
Para cada query/oportunidad anota: query, impresiones, posición, ¿existe página propia?,
tipo de página que la captaría (servicio / zona / colonia / blog).

### 2b. Expansión geográfica
Lista servicios/zona y colonias existentes (`ls servicios/`, colonias indexables con
`grep -L noindex`). Cruza con demanda real (2a). Detecta zonas/colonias con búsquedas pero
sin página única. NO inventes colonias sin señal de demanda (riesgo doorway).

### 2c. Blog SEO
Inventario `ls blog/`. Detecta keywords de plomería de Culiacán con volumen (de 2a o del
sentido común del nicho: "¿cuánto cuesta…?", problemas de fugas/drenajes/boiler/tinacos,
guías, normas de agua/gas) que el blog aún NO cubre. Una idea = un post con intención clara.

### 2d. Mejoras a páginas existentes
Corre `python3 .pipeline/check-plantilla.py` y `python3 .pipeline/check-indexabilidad.py`.
Identifica páginas FLOJAS: contenido delgado, sin FAQ, og:image incoherente, interlinking
pobre, meta description larga. Estas se MEJORAN (editar), no se recrean.

### Entregable de la fase
Escribe `.pipeline/oportunidades-<YYYYMMDD>.md` con una tabla rankeada:
`| # | oportunidad | dimensión | impacto (alto/med/bajo) | esfuerzo | riesgo doorway | acción |`
Ordena por impacto/riesgo. Esto es "determinar bien qué falta".

## FASE 3 — Priorizar (tope duro)
Elige las **top `MAX_PAGINAS`** acciones de menor riesgo y mayor impacto. Prefiere
oportunidades respaldadas por datos de GSC sobre las especulativas. Si NO hay ninguna
oportunidad de bajo riesgo y alto impacto, está PERMITIDO crear 0 páginas esta corrida y
solo dejar el reporte (no fuerces crecimiento sin señal — eso genera doorways).

## FASE 4 — CONSTRUIR (autónomo)
Para los dos casos más comunes hay GENERADORES REUSABLES (úsalos en vez de escribir
código desde cero; se apoyan en `gen-landing.py`, mantienen la garantía anti-drift):
- **Servicio nuevo:** `python3 scripts/crear-servicio.py spec.json`
  (plantilla del spec: `python3 scripts/crear-servicio.py --ejemplo`).
  El spec lleva el SEO/schema/hero + un campo `cuerpo_html` con la PROSA ÚNICA de la página
  (todas las secciones del cuerpo). Eso es lo que vence al anti-doorway: escríbelo verídico
  y específico de ESTE servicio en Culiacán.
- **Promover una colonia** (noindex doorway → indexable con contenido único):
  `python3 scripts/diferenciar-colonia.py spec.json` (`--ejemplo` para la plantilla).
  NOTA: hoy todas las colonias ya son indexables; esta herramienta es para colonias noindex
  futuras.
Para blog o casos especiales, escribe un spec de `gen-landing.py` a mano desde un esqueleto
de `blog/<post>/index.html` que pase los checkers.

Lo más simple y seguro: deja que el ORQUESTADOR haga el cableado y el candado por ti:
```
python3 scripts/crecer.py servicio /tmp/spec.json     # crea + sitemap + enlace home + bump sw + candado (revierte si falla)
python3 scripts/crecer.py colonia  /tmp/spec.json     # promueve colonia + sitemap + candado (revierte si falla)
```

## FASE 5 — CANDADOS (puerta de publicación)
Si construiste a mano (sin el orquestador), corre el candado todo-en-uno sobre CADA página
nueva/modificada:
```
python3 .pipeline/gate-pagina.py <ruta1/index.html> <ruta2/index.html> ...
```
Hace: validate-landing.sh + ci-gate (0 ALTA) + anti-doorway (Jaccard < 0.80).
Además verifica a mano: JSON-LD parsea, canonical==og:url==twitter:url, 0 enlaces rotos,
HTTP 200 en local (`curl`).
**Si el candado FALLA (exit≠0): NO publiques.** Deja todo en la rama, escribe el motivo en
ESTADO.md y termina avisando al humano. No "fuerces" el arreglo si implica romper otra regla.

## FASE 6 — PUBLICAR (auto, solo si FASE 5 fue 100% verde)
Lo más simple: usa el orquestador (rama + commit + merge --no-ff + push seguro, sin --force;
el pre-push auto-indexa en GSC):
```
python3 scripts/crecer.py publicar "feat: expansión autónoma — <resumen>"
```
Luego refuerza la indexación vía MCP (excluye las noindex):
`mcp__gsc__gsc_index(site, [urls indexables nuevas])`.

## FASE 7 — Bitácora
- `ESTADO.md`: nueva entrada ARRIBA con fecha, qué se creó, evidencia de candados, URLs indexadas.
- `HISTORIAL.jsonl`: una línea JSON por página creada/mejorada (campos: fecha, archivo,
  categoria, severidad, descripcion, estado, regla, nota).
- `REGLAS.md`: si aprendiste algo nuevo (un patrón, un casi-error), añádelo como una línea.

## FASE 8 — Reporte final
Resume: qué huecos se detectaron, qué se creó, resultado de los candados, qué se publicó e
indexó, y qué quedó como PENDIENTE HUMANO (oportunidades de alto impacto pero alto riesgo o
que exceden el tope). Sé honesto: si no se creó nada por falta de señal, dilo.
