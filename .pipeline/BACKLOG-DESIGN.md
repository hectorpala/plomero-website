# Diseño — Crecimiento autónomo MÁXIMO (BACKLOG + loop-until-dry, sin budget)

Objetivo: que el Auto Agente **construya y optimice lo MÁS posible solo** cada corrida —
descubriendo temas y creando páginas— sin un tope numérico arbitrario, pero **sin caer en la
trampa que ya costó caro a este sitio: páginas en masa = doorways que penalizan TODO el sitio**.

## La idea central

Hoy el freno es `MAX_PAGINAS = 3` (un número arbitrario). Se reemplaza por los **frenos NATURALES**:

1. **DEMANDA REAL** — solo se crea una página si hay señal real en GSC (impresiones / queries con
   intención). Sin demanda → no hay página. Esto **acota la oferta de páginas nuevas a lo que el
   mercado realmente busca**: es imposible inflar doorways porque no hay demanda que los respalde.
2. **ANTI-DOORWAY (Jaccard < 0.80)** — cada página debe ser sustancialmente única. `gate-pagina.py`
   ya lo bloquea. Es el segundo candado.
3. **VERIFICACIÓN + diff cap por corrida** — el verificador escéptico y el tope de archivos siguen.

Con eso, "lo más posible" se vuelve seguro:

| Tipo de trabajo | ¿Cuánto por corrida? | Por qué |
|---|---|---|
| **Optimización** (CTR, enriquecer, enlazado, schema, perf, fix-deuda) | **TODO lo que haya** | Cero riesgo de doorway. Mientras más, mejor. |
| **Páginas nuevas** | **Tantas como huecos de demanda REAL pasen los candados** | El límite es el mercado + la unicidad, no un número. |

## El motor: backlog persistente + loop-until-dry

```
DESCUBRIR (llena BACKLOG.jsonl con TODO lo que califica) ─┐
                                                          │
   ┌── LOOP (drena por prioridad, riesgo<=medio) ─────────┘
   │   saca tarea → construye (generador del tipo) → gate-pagina → verifica →
   │   publica si pasa · si falla 2× revierte y marca 'bloqueado' · cierra la tarea
   └── repite hasta que: 2 rondas de descubrimiento no encuentren NADA nuevo (loop-until-dry)
                          o se acabe la ventana de tiempo de la corrida
   → lo que no se alcanzó queda en el backlog y se drena la próxima corrida (nada se pierde)
```

- **No hay tope de tareas.** El loop drena hasta agotar el backlog auto-ejecutable o hasta
  `MINUTOS_MAX` (cota de tiempo de la corrida, no de tokens — corre por suscripción).
- **Continuidad entre días:** el backlog es persistente. Si hoy quedan 20 tareas y se drenan 8,
  mañana arranca con 12 + las nuevas. El sitio mejora **continuamente** hasta saturar el espacio
  de temas con demanda, luego se concentra en optimizar lo existente.
- **Riesgo alto nunca se auto-ejecuta** (p.ej. "¿vende bombas de agua?"): queda en
  `requiere_humano` y sale en el parte para tu decisión.

## DESCUBRIMIENTO ancho (de dónde salen "temas que puede desarrollar")

Mientras más fuentes, más huecos legítimos que construir. Cada hallazgo se encola con su señal:

1. **GSC oportunidades** — queries pos 8-30 con impresiones sin página propia (lo que ya hace).
2. **GSC CTR bajo** — páginas con muchas impresiones y CTR bajo → tarea `ctr-fix` (sin doorway).
3. **GSC query que rankea de rebote en una genérica** → `enriquecer` la página dedicada.
4. **Matriz servicio × intención** — cada servicio × {precio, urgencia, cómo, cuánto cuesta, cerca}
   → candidata a página/ sección SI hay query con demanda (no forzar el producto cartesiano).
5. **Minería de preguntas** (PAA / "cómo / por qué / cuánto") → secciones FAQ o posts de blog.
6. **Expansión de keywords** (`keyword-volume-tool/`) — variantes y problemas ("fuga en la pared",
   "llave que gotea") con volumen.
7. **Gap de competidores** — lo que rankean los competidores permitidos y nosotros no.
8. **Estacional/temporal** — picos por temporada (lluvias → drenajes, frío → boilers).

Regla de oro: **cada candidata a página nueva DEBE traer una señal de demanda**. Si no la trae, no
se encola como página — a lo sumo como `enriquecer`/`enlazado` (mejora sin riesgo).

## Cambios propuestos (para tu OK — no los apliqué al prompt núcleo todavía)

1. **`expandir-sitio` / FASE 6 del prompt diario:** quitar `MAX_PAGINAS = 3`; sustituir por:
   - `UMBRAL_DEMANDA` (mínimo de impresiones/volumen para justificar una página nueva).
   - **loop-until-dry**: descubrir → encolar → drenar, repetir hasta 2 rondas vacías o `MINUTOS_MAX`.
   - drenar **todas** las tareas de optimización pendientes (sin tope).
2. **Frecuencia:** el guard "ya corrió hoy" evita duplicados accidentales, no productividad. Para
   "más", la palanca es **loop-until-dry dentro de la corrida** (no más corridas). Si aun así
   quieres 2-3 corridas/día, se agregan horarios al launchd (cada una drena lo que haya).
3. **Paralelizar la construcción** (Workflow + worktree por tarea) cuando el backlog lo justifique.

## Piezas ya entregadas
- `BACKLOG.jsonl` — la cola (sembrada con los pendientes reales de la corrida).
- `.pipeline/gestor-backlog.py` — add / next / close / stats / list (+ dedup + gate de riesgo).

## Lo que NO se hace (el freno que protege el SEO)
- NO crear páginas sin demanda real (doorway → penalización de TODO el sitio: ya pasó, ver REGLAS
  "consolidar 320950bc").
- NO bajar el umbral de unicidad del anti-doorway para "producir más".
- NO tocar precios, borrar páginas ni añadir servicios que el negocio no ofrece (decisión humana).
