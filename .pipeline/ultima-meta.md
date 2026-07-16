# Meta-pase del Crítico-Sistema — 2026-07-15

Dejé **2 propuestas nuevas**, con su DRAFT ya escrito y verificado en vivo contra el sitio real, arriba de
`docs/PROPUESTAS.md` (quedan **12 pendientes en total**, sumando las de pases anteriores que aún no tienen
merge). Yo no apliqué nada — tú apruebas.

## Top por impacto

1. **(A) La regresión más reincidente del sistema sigue sin checker, y una de sus dos formas sigue viva
   HOY.** El color del breadcrumb (`.breadcrumb-item a`, `#E36414` en vez de `#C2410C`) regresó 3 veces
   (9, 13 y 14 de julio) porque el fix vivía copiado a mano en el `<style>` de cada página en vez de
   centralizado — la propia corrida del 13 de julio lo diagnosticó así, y aun así volvió a pasar al día
   siguiente. Peor: verifiqué HOY los 3 CSS servidos y `.breadcrumb-item.active{color:#6c757d}` (4.44:1,
   por debajo del mínimo de accesibilidad 4.5:1) **sigue ahí, sin arreglar** — la corrida del 14 de julio
   lo detectó y lo dejó marcado "pendiente" por ser un cambio a nivel sitio, pero nunca se convirtió en
   tarea de la cola y se quedó huérfano. El draft mecaniza los dos: un checker que vigila esos 2 pares
   selector/color tanto en las 3 hojas compartidas como en cualquier `<style>` inline, más el auto-fixer
   que los corrige solo.
2. **(M) La alarma de "pico de costo" no mide costo real.** Se dispara comparando tokens totales, pero
   el 97% de esos tokens en la corrida de ayer fueron lectura de caché (barata, ~10% del precio normal) —
   el propio archivo de costos ya calcula el $ real de cada corrida y no se está usando para la alarma.
   Resultado: hoy marcó "PICO" la corrida del 14 de julio ($77) mientras la del 13 de julio, que ya no era
   la más reciente, costó más de verdad ($119) y no disparó nada. Draft de una función, cambia el criterio
   a dólares reales.

**Cómo lo verifiqué:** corrí `.pipeline/recolecta-señales.py` (255 entradas de historial, 29 corridas de
costo, 14 tareas de backlog, REGLAS.md al 100% del presupuesto — ya tiene su propio sensor que lo va a
marcar solo, no hace falta otra propuesta). Confirmé con `grep` en vivo contra los 3 `styles*.css` reales
que `.breadcrumb-item.active` sigue con el color prohibido, y contra `data/BACKLOG.jsonl` que esa tarea
nunca se abrió. Revisé los 2 ítems `pendiente`/`requiere_humano` del backlog (doorway domicilio-vs-cerca-de-mi,
year-desync de precios) — ambos son decisiones de negocio genuinas, no huecos del sistema, así que no
generaron propuesta nueva.

**Estado del sistema:** sano en general — la única corrida atascada es una decisión que sigue esperando al
dueño (2 tareas), no una falla del pipeline. El patrón de esta semana repite el de julio: un fix que se
aplica en el sitio pero nunca se convierte en regla mecánica, así que el mismo bug puede volver a colarse
en la próxima página nueva. Las 12 propuestas pendientes de `docs/PROPUESTAS.md` siguen listas para merge.
