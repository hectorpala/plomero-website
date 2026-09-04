# Agentes de plomeroculiacanpro.mx

Índice de los agentes VIVOS. Cada uno es un rol que el Auto Agente diario ejecuta como pasada
independiente (con Codex no se delega: se lee el archivo completo y se ejecuta el rol).

Quién orquesta: `.pipeline/crecer-diario-prompt.txt` (10 fases) y `.claude/skills/mantener-sitio/SKILL.md`.
Qué revisores caros correr según lo que cambió: `python3 .pipeline/selector-revisores.py`.
Política de modelos: [`MODELO-ROUTING.md`](MODELO-ROUTING.md).

## Revisores DETERMINISTAS (haiku — corren un checker y devuelven su JSON, sin reinterpretarlo)

Son el piso de seguridad: siempre corren, sobre todo el sitio, y son baratos.

| Agente | Checker que ejecuta | Qué garantiza |
|---|---|---|
| `revisor-infra-salud` | `check-infra.mjs` | Dead-man's switch: que los SENSORES funcionan. Corre PRIMERO. |
| `revisor-plantilla` | `check-plantilla.py` | Las reglas mecánicas de REGLAS.md (26 checks) |
| `revisor-indexabilidad` | `check-indexabilidad.py` | Canonical, sitemap, breadcrumbs, noindex |
| `revisor-nap` | `check-nap.py` | Nombre, teléfono y email idénticos en todo el sitio |
| `revisor-conversion` | `check-conversion.py` | Que cada página indexable tenga camino de conversión |
| `revisor-enlazado-interno` | `check-linking.py` | Grafo de enlaces: huérfanas y páginas a >3 clics |
| `revisor-contenido` | `check-contenido.py` + juicio | Restos de plantilla, años caducos, precios visibles |
| `revisor-e2e-funcional` | `check-e2e.mjs` | Menú, wa.me y la VALIDACIÓN VIVA del formulario en todas las páginas donde vive |
| `revisor-visual` | `check-visual.mjs` | El único que mira cómo SE VE la página (diff contra línea base) |
| `revisor-perf-real` | `check-perf.mjs` | Core Web Vitals contra presupuesto y baseline |
| `revisor-produccion` | `check-produccion.mjs` | Uptime, errores JS reales, cabeceras, mixed content |
| `revisor-tracking` | `check-tracking-deadline.py` | GTM + GA4 con supervisor de deadline |
| `revisor-secretos` | `check-secretos.sh` | Claves en el árbol y en el historial. Su exit code es candado de publicación. |

## Revisores de JUICIO (sonnet/opus — lo SUBJETIVO, que ningún checker puede mecanizar)

Caros. No corren siempre: los selecciona `selector-revisores.py` según lo que cambió.

| Agente | Cubre |
|---|---|
| `revisor-seo` | Intención de búsqueda, canibalización, doorways |
| `revisor-contenido` | Thin content, duplicado, ortografía, claims sin respaldo |
| `revisor-a11y` | Contraste, lectores de pantalla, foco |
| `revisor-movil` | Cómo se usa de verdad en un teléfono |
| `revisor-perf` | Decisiones de rendimiento que piden criterio |
| `revisor-links` | Enlaces que existen pero llevan al lugar equivocado |
| `revisor-gsc` | Demanda real en Search Console (corre en la FASE 6, no en revisión) |

## Roles que no son revisores

| Agente | Rol |
|---|---|
| `verificador` | FASE 7. SOLO-LECTURA, escéptico: intenta demostrar que algo quedó MAL antes de publicar. JAMÁS se sustituye por un agente general (incidente verifier-rogue, 2026-06-21). |
| `decisor-negocio` | Decide qué crear/enriquecer según NEGOCIO.md + demanda GSC |
| `fixer-autonomo` | Aplica los arreglos mecánicos de bajo riesgo |
| `critico-sistema` | 3×/semana: propone mejoras al SISTEMA con el draft ya escrito, en `docs/PROPUESTAS.md` |
| `critico-completitud` | Revisa que el parte al dueño cuadre con los cambios reales |

## Historial

El 2026-09-04 se borraron 12 agentes huérfanos que ningún prompt ni skill referenciaba: los cinco de
febrero de 2026 (`revisor-feb-2026`, `qa-validator`, `page-rebuilder`, `style-critic`, `style-extractor`,
`image-size-auditor`), los tres de generación de imágenes (`plumbing-image-prompts`,
`plumbing-image-generator`, `kitchen-image-prompt-generator`), los dos "turbo"
(`gitops-publisher-turbo`, `ui-ux-surgeon-turbo`) y el `revisor` genérico, superado por los
especializados. Siguen recuperables en el historial de git.
