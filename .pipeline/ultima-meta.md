# Meta-pase del Crítico-Sistema — 2026-07-24

Dejé **1 propuesta nueva**, con su DRAFT ya escrito y verificado en vivo contra el sitio real, arriba de
`docs/PROPUESTAS.md` (quedan **12 pendientes en total**, sumando las de pases anteriores que aún no tienen
merge — ninguna se resolvió sola, siguen esperando tu aprobación). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto

1. **(A, nueva) Una clase de bug de enlaces lleva reincidiendo 4 veces desde julio y hoy siguen vivas
   11 páginas con el mismo problema, sin checker que lo cace.** El sitio tiene páginas "redirect-stub"
   (URLs viejas que solo redirigen, ej. `servicios/plomero/24-7/`) y cada vez que alguien las enlaza en
   vez de enlazar el destino final, se corrige a mano SOLO en las páginas del lote de ese día — nunca se
   mecanizó. El checker existente para esto (check 14) solo funciona si el TEXTO del enlace coincide con
   el nombre exacto de un servicio; textos genéricos como "Servicio 24/7" se le escapan por diseño, por
   eso reapareció el 7, 9 y 14 (dos veces) y el 21 de julio. Verifiqué hoy en vivo: 11 páginas (incluido
   un archivo huérfano, `partials/footer_nav.html`, que ningún generador usa) siguen enlazando a stubs en
   vez del destino real. El draft cierra la clase COMPLETA de una vez, sin depender del texto del enlace.
2. **(M, de un pase anterior, sigue sin merge) La alarma de "pico de costo" sigue midiendo mal, y hoy
   volvió a dar una falsa alarma.** El brief de hoy marcó "⚠️ PICO" en la corrida de ayer (131.5M
   tokens) — pero verifiqué el $ real: costó $65.94, MENOS que la mediana de $69.71. Es exactamente el
   bug que ya describí en un pase anterior (la alarma usa tokens totales, dominados por lectura de caché
   barata, en vez del dólar real que el propio sistema ya calcula). El draft para arreglarlo sigue
   esperando merge en `docs/PROPUESTAS.md`.
3. **(M, de un pase anterior, sigue sin merge) La tarea de doorway `plomero-a-domicilio` vs
   `plomero-cerca-de-mi` lleva 35 días esperando decisión humana** (abierta el 2026-06-19) y el brief no
   muestra su edad, así que es fácil no notar cuánto lleva parada. Ya hay un draft pendiente para que el
   brief muestre la edad de las tareas `requiere_humano`.

**Cómo lo verifiqué:** corrí `.pipeline/recolecta-señales.py` (273 entradas de historial, 33 corridas de
costo, 14 tareas de backlog, REGLAS.md 14 tokens sobre su presupuesto de 4000 — marginal, su propio sensor
ya lo marca solo). Para la propuesta nueva, confirmé en vivo con `grep -rl` los 4 destinos de stub
(`24-7`, `cerca-de-mi`, `a-domicilio`, `precios`) contra todo el sitio (11 páginas hoy), leí las 4 entradas
de `data/HISTORIAL.jsonl` donde reincidió esta clase, y confirmé que el checker existente (check 14) es
estructuralmente incapaz de cazarla porque compara texto-de-ancla contra H1, no ruta-de-destino contra
stub. Para el costo, recalculé `usd_equiv_api_ref` de las últimas 8 corridas de `costos.jsonl` a mano y
confirmé que la corrida marcada "PICO" hoy cuesta MENOS en dólares reales que la mediana. Revisé
`data/BACKLOG.jsonl`: solo 2 tareas fuera de `hecho`/`descartado` (la doorway de 35 días y un `pendiente`
de year-desync de precios) — ambas son decisiones de negocio genuinas, no huecos del sistema.

**Estado del sistema:** sano en general — el bug de enlaces a stubs es el único hueco NUEVO real de hoy;
el resto son propuestas de pases anteriores que siguen sin merge (el sistema sigue produciendo la misma
alarma de costo falsa y la misma tarea de 35 días sin visibilidad de edad porque esos drafts no se han
aplicado). Las 12 propuestas pendientes de `docs/PROPUESTAS.md` siguen listas para merge.
