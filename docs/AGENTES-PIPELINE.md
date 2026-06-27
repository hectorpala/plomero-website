# Pipeline de agentes autónomos para sitios web

Diseño de un sistema reusable (para los 7 sitios) que **construye, revisa, depura y verifica**
sin asistencia humana, y que puede correr **recurrente / desatendido**.

---

## 1. Principios (lo que hace que funcione sin ti)

1. **Especialización + fan-out.** No un agente que hace todo, sino varios revisores en
   paralelo, cada uno con UNA lente (SEO, móvil, a11y, performance, links).
2. **Salida estructurada (JSON con schema).** Cada agente devuelve datos validados, no prosa.
   Así el siguiente paso los procesa sin ambigüedad.
3. **Verificación adversarial.** Un agente escéptico intenta REFUTAR cada fix, corriendo el
   sitio de verdad (servidor local + Playwright/screenshots), no leyendo código.
4. **Loop-until-dry.** Se repite revisar→arreglar→verificar hasta que 2 rondas seguidas no
   encuentren nada nuevo. Ese es el criterio de "terminado".
5. **Idempotencia.** Cada corrida puede ejecutarse muchas veces sin romper lo ya bueno.
   Imprescindible para el modo desatendido.
6. **Gate de seguridad antes de publicar.** Nada llega a `main`/producción sin pasar la
   verificación. El humano puede quedar fuera del fix pero el sitio roto no se publica.

---

## 2. Arquitectura de fases

```
        ┌─────────────────────────────────────────────────────┐
        │                    ORQUESTADOR                        │
        │           (Workflow tool / skill maestro)             │
        └─────────────────────────────────────────────────────┘
              │
   FASE 0  ── Orientación + Memoria ───────────────────────────
              Detecta tipo de sitio, páginas, stack, baseline Y
              LEE REGLAS.md + ESTADO.md (lo aprendido hasta hoy).
              │
   FASE 0.5 ─ HEALTH CHECK (¡antes de tocar nada!) ────────────
              Levanta el servidor y corre los e2e básicos para
              cazar bugs no documentados desde la corrida anterior.
              (Patrón de Anthropic: revisar que "lo de ayer" sigue sano.)
              │
   FASE 1  ── Construir / Modificar (UNA mejora por sesión) ────
              builder aplica el brief o el cambio pedido.
              │
   FASE 2  ── Revisar (FAN-OUT en paralelo) ───────────────────
              ┌── seo-tecnico      ──┐
              ├── movil            ──┤
              ├── accesibilidad    ──┤── cada uno → JSON de hallazgos
              ├── performance      ──┤
              ├── links-rotos      ──┤
              └── contenido/copy   ──┘
              │
   FASE 3  ── Depurar (un fixer por hallazgo) ─────────────────
              Pipeline: cada hallazgo confirmado → fix aislado.
              │
   FASE 4  ── Verificar (adversarial, sitio corriendo) ────────
              3 verificadores votan: ¿el fix es real? mayoría manda.
              │
              └──── ¿hallazgos nuevos? ── SÍ → vuelve a FASE 2
                          │ NO (2 rondas limpias)
   FASE 5  ── Publicar (gate) ─────────────────────────────────
              Solo si verificación 100% OK → commit + push
              (tu pre-push hook ya dispara la indexación en Google).
              │
   FASE 6  ── Aprender (bibliotecario) ────────────────────────
              Escribe REGLAS.md + HISTORIAL.jsonl → la corrida de
              mañana arranca leyéndolos y NO repite el error.
```

---

## 3. Catálogo de agentes (rol + prompt base + salida)

> Cada uno corre como subagente con su propio contexto. El prompt es el "system" del rol.

### builder
- **Rol:** aplica el cambio o construye desde el brief.
- **Prompt base:** "Eres un desarrollador frontend. Aplica EXACTAMENTE el cambio descrito.
  No toques nada fuera del alcance. Respeta los patrones del repo (CSS versionado `?v=`,
  service worker, estructura de páginas). Devuelve la lista de archivos tocados."
- **Salida:** `{ archivos: [{path, resumen_cambio}] }`

### Revisores (FASE 2) — todos devuelven el mismo schema de hallazgos:
```json
{ "hallazgos": [
  { "id": "seo-001", "archivo": "index.html", "linea": 42,
    "severidad": "alta|media|baja", "categoria": "seo",
    "descripcion": "...", "fix_sugerido": "..." }
]}
```

| Agente | Lente | Qué busca |
|---|---|---|
| `seo-tecnico` | SEO | title/description faltantes o duplicados, schema.org, sitemap, canonical, hreflang, noindex mal puesto |
| `movil` | Responsive | overflow horizontal, tap targets <44px, viewport, tablas desbordadas |
| `accesibilidad` | a11y | contraste, alt en imágenes, labels, jerarquía de headings, foco |
| `performance` | Velocidad | imágenes sin optimizar/WebP, CSS/JS pesado, LCP, lazy-load |
| `links-rotos` | Integridad | enlaces internos/externos 404, anchors muertos, recursos faltantes |
| `contenido` | Copy/UX | textos placeholder, info de contacto incorrecta, CTAs ausentes |

### fixer (FASE 3)
- **Rol:** arregla UN hallazgo confirmado.
- **Prompt base:** "Arregla SOLO el hallazgo {id}. Cambio mínimo. No introduzcas regresiones.
  Si arreglarlo requiere tocar algo fuera del archivo indicado, decláralo y detente."
- **Aislamiento:** si varios fixers corren a la vez → worktree por fixer.
- **Salida:** `{ id, arreglado: true|false, archivos, nota }`

### verificador (FASE 4) — adversarial
- **Rol:** intentar REFUTAR que el fix sirvió, con el sitio corriendo.
- **Prompt base:** "Eres escéptico. Levanta el sitio en local, abre la página afectada y
  comprueba si el problema {id} SIGUE presente. Por defecto asume que NO se arregló salvo
  prueba clara. Reporta refutado=true si lo ves roto."
- **Voto:** 3 verificadores independientes; se da por bueno si ≥2 dicen refutado=false.
- **Salida:** `{ id, refutado: bool, evidencia }`

### bibliotecario (FASE 6) — el que hace que aprenda
- **Rol:** convertir lo que pasó en la corrida en REGLAS que eviten repetir el error.
- **Prompt base:** "Revisa los hallazgos verificados de esta corrida y el HISTORIAL. Para
  cada error real pregúntate: ¿qué regla, de haber existido, lo habría evitado? Escribe/
  actualiza REGLAS.md. CONSOLIDA: si ya existe una regla parecida, edítala, no dupliques.
  Borra reglas obsoletas. Una regla SOLO nace de un error que pasó la verificación
  adversarial — nunca de una sospecha. Marca regresiones (errores ya vistos que reaparecen)
  como prioridad alta."
- **Salida:** `{ reglas_nuevas, reglas_actualizadas, reglas_borradas, regresiones }`

---

## 4. Modo desatendido / recurrente

Tres niveles, de menos a más autónomo:

1. **`/loop` con auto-pace** — un comando que repite el pipeline hasta loop-until-dry y se
   detiene solo. Tú lo disparas, pero no lo supervisas.
2. **`/schedule` (cron en la nube)** — corre el pipeline de auditoría+fix cada noche/semana
   sobre cada sitio y abre PR con los arreglos. Tú solo revisas el PR (o ni eso).
3. **Hook en git** — ya tienes pre-push que indexa. Puedes añadir un hook que corra la
   verificación (gate) ANTES de permitir el push, bloqueando si el sitio queda roto.

**Recomendación para 7 sitios:** `/schedule` semanal por sitio → cada uno genera un PR
"mantenimiento automático" con los hallazgos arreglados y el reporte de verificación.
Tú apruebas en lote. Cero trabajo diario.

---

## 5. Cómo se implementa (cuando decidas montarlo)

- **Orquestación:** un script del **Workflow tool**. Usa `pipeline()` para el flujo por
  hallazgo, `parallel()` para el fan-out de revisores, y un `while` para loop-until-dry.
- **Reusabilidad para 7 sitios:** parametriza por `args` = `{ ruta_sitio, url_base }`.
  El mismo script sirve para todos; solo cambia el argumento.
- **Verificación real:** servidor local (`python -m http.server` o el que uses) +
  Playwright/skill `webapp-testing` para abrir páginas y comprobar comportamiento.
- **Skills que ya tienes y encajan:** `auditoria-seo`, `validar`, `seo-optimizer`,
  `deploy-quick`, `publica`, `webapp-testing`, `code-review`. El pipeline las orquesta.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El fixer "dice" que arregló pero no | Verificación adversarial con sitio corriendo + voto mayoría |
| Loop infinito | Tope de rondas (p. ej. 5) + criterio loop-until-dry explícito |
| Fixers se pisan archivos | Worktree por fixer en paralelo |
| Publica algo roto | Gate de verificación obligatorio antes del push |
| Falsos positivos inundan | Severidad + umbral (solo alta/media en modo desatendido) |
| Costo de tokens | Revisores con modelo más barato; solo síntesis/verificación con el potente |

---

## 7. Capa de memoria — para que aprenda y NO repita errores

Sin memoria, el pipeline redescubre los mismos errores cada día. La solución es un
**feedback loop**: cada corrida ESCRIBE lo aprendido y la siguiente lo LEE antes de empezar.

```
   Día N:  REVISAR → ARREGLAR → VERIFICAR → APRENDER ──┐
                ↑                                        │
                │         escribe reglas nuevas          │
   REGLAS.md ───┴─────────────────────────────────────  ┘
                │
   Día N+1: lee REGLAS.md ANTES de revisar → no repite el error
```

### Tres archivos de memoria (por sitio)

| Archivo | Qué guarda | Lo lee | Lo escribe |
|---|---|---|---|
| **`REGLAS.md`** | Reglas duras: "siempre WebP", "tablas en div scroll", "nunca noindex en zonas" | builder + revisores (al inicio, como guardrails) | bibliotecario (FASE 6) |
| **`HISTORIAL.jsonl`** | Cada hallazgo con fecha, archivo, si se arregló, si reapareció | de-duplicador | orquestador (cada corrida) |
| **`ESTADO.md`** | Foto actual: pendientes, aprobados, baseline de métricas | orquestador (al arrancar) | orquestador (al cerrar) |

`REGLAS.md` es el cerebro anti-repetición. Funciona igual que el MEMORY.md de Claude Code:
contexto inyectado antes de trabajar. Ejemplo:

```markdown
## Reglas aprendidas — Plomero Culiacán
- [2026-06-12] Tablas: SIEMPRE envolver en <div class="tabla-scroll"> —
  causó overflow móvil 2 veces (commit f44ef39f). Severidad: alta.
- [2026-06-12] Imágenes nuevas: convertir a WebP antes de commit, nunca PNG directo.
- [2026-06-11] Páginas de zona: NUNCA noindex — consolidación 301 ya resuelta (320950bc).
```

### Detección de regresiones ("el mismo error otra vez")

El de-duplicador busca cada hallazgo en `HISTORIAL.jsonl` por **firma**
(`archivo + categoría + descripción normalizada`):

- **Nuevo** → se procesa normal.
- **Ya visto, arreglado, reaparece** → ⚠️ REGRESIÓN. Prioridad alta. Señal de que falta una
  regla o algo lo re-introduce → el bibliotecario crea regla que lo prevenga de raíz.
- **Ya visto, sigue pendiente** → no re-reporta; solo incrementa contador.

Así el ruido BAJA con el tiempo en vez de subir.

### Salvaguardas para que la auto-alimentación no degenere

1. **Curación, no solo acumulación.** El bibliotecario consolida y BORRA reglas obsoletas.
   Si `REGLAS.md` crece sin control, contamina el contexto.
2. **Regla = error verificado.** Solo nace de algo que pasó la verificación adversarial,
   nunca de una sospecha. Evita reglas falsas que limiten al builder sin razón.

### El montaje diario completo

```
/schedule → cada día 3am, por sitio (args = {ruta_sitio, url_base}):
   1. lee REGLAS.md + ESTADO.md                    (memoria)
   2. corre pipeline (revisar→fix→verificar, loop-until-dry)
   3. bibliotecario actualiza REGLAS.md + HISTORIAL.jsonl
   4. si todo verde → PR "mantenimiento auto [fecha]"
   5. pre-push hook indexa en Google
```

Tú solo ves el PR. Como el builder arranca leyendo `REGLAS.md`, deja de cometer los errores
que ya costaron una vez. El sistema mejora solo.

### Arranque (seed) de REGLAS.md

No empieza vacío: se siembra a partir de los **commits recientes**, que ya contienen
lecciones reales (overflow de tablas, versionado de CSS, noindex de zonas, WebP). Esos
mensajes de commit ya son "errores aprendidos" — el seed los convierte en reglas el día 1.

---

## 8. Validación: cómo lo hace Anthropic (los dueños de Claude)

Este diseño se contrastó con la documentación oficial de Anthropic. Coincide en ~90%.
Lo que sigue son los patrones confirmados que adoptamos.

### Harness de dos agentes
- **Initializer** (corre 1 vez): prepara entorno, siembra REGLAS.md.
- **Coding agent** (corre cada día): avanza incremental con estado limpio.
- Mapea a: seed inicial (una vez) + pipeline diario (recurrente).

### Loop de sesión con orden fijo (de Anthropic)
`Orientación → HEALTH CHECK → Selección → Implementar → Verificar → Documentar`
- El **HEALTH CHECK** (FASE 0.5) es la pieza clave que añadimos: correr e2e ANTES de
  tocar nada para cazar regresiones de la corrida anterior.

### Reglas duras adoptadas
- **JAMÁS borrar ni editar tests** — ocultaría funcionalidad rota. (Anthropic lo marca
  como "inaceptable".)
- **UNA mejora por sesión** — evita abarcar de más y perder contexto.
- **JSON sobre Markdown para archivos de estado** — el agente los corrompe menos.
  Por eso HISTORIAL es `.jsonl` y ESTADO conviene estructurarlo.
- **Podar REGLAS.md sin piedad** — "¿borrar esta línea causaría un error? Si no, bórrala."

### Verificación (3 formas de gate, de Anthropic)
1. `/goal` — un evaluador re-checa tras cada turno hasta cumplir la condición.
2. **Stop hook** — script determinista que BLOQUEA el cierre de turno hasta pasar el check.
   Es el gate más fuerte para modo desatendido.
3. **Subagente verificador** en contexto fresco (ve solo el diff + criterios). = FASE 4.

### Motor del modo desatendido
- **`claude -p "prompt"`** — modo headless sin sesión, para cron/CI/hooks. Base del
  `/schedule` diario.
- **Fan-out** `for sitio in ...; do claude -p ...` — exactamente cómo se replica a los 7 sitios.
- **Auto mode** — clasificador que aprueba/bloquea comandos solo, sin aprobar cada paso.
- El bundled `/code-review` ya hace la revisión adversarial del diff en subagente fresco.

### Dónde vamos MÁS ALLÁ que Anthropic
- El **fan-out de revisores especializados en paralelo** (SEO/móvil/a11y/perf). Anthropic
  dice que si conviene un agente general o varios especializados "sigue siendo pregunta
  abierta" — aún no lo implementan. Nuestra capa paralela es una apuesta razonable, no algo
  que contradiga su enfoque.

### Fuentes
- Anthropic — *Effective harnesses for long-running agents*:
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Claude Code Docs — *Best practices*: https://code.claude.com/docs/en/best-practices
- Anthropic — *How Anthropic teams use Claude Code* (PDF):
  https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
- Anthropic — *Building agents with the Claude Agent SDK*:
  https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
```
