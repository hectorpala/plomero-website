# Meta-pase del Crítico-Sistema — 2026-07-13

Dejé **2 propuestas nuevas**, con su DRAFT ya escrito y probado en vivo contra el sitio real, arriba de
`docs/PROPUESTAS.md` (quedan 10 pendientes en total, sumando las de pases anteriores que aún no tienen
merge). Yo no apliqué nada — tú apruebas.

## Top por impacto

1. **(A) 5 revisores siguen sin el `export PATH` que ya arregló este mismo bug hace 3 días.** `node` no
   está en el PATH por defecto de varios shells del pipeline — esto YA reventó 3 veces como falso "ALTA:
   verificación ciega" (12-jun, 21-jun, 10-jul), y REGLAS.md tiene la regla escrita desde el 12 de junio.
   Pero el parche solo se aplicó a `revisor-produccion.md` (el que disparó el último incidente). Revisé
   los otros 6 revisores hoy: `revisor-e2e-funcional`, `revisor-gsc`, `revisor-infra-salud`,
   `revisor-perf-real` y `revisor-tracking` invocan `node` SIN el `export PATH` — cualquiera de los 5
   puede reportar el mismo falso positivo mañana. El draft es el mismo texto ya probado, copiado a los
   5 archivos.
2. **(A) El catálogo de servicios en JSON-LD puede quedar con la misma descripción copiada en todos —
   y REGLAS.md dice literalmente "sin checker aún".** Es la única regla de severidad ALTA en todo
   REGLAS.md que no tiene un checker anotado (todas sus vecinas sí). Ya pasó una vez (8 de julio):
   varios `Service` de un mismo catálogo quedaron con la descripción del anfitrión pegada por error.
   Probé el draft contra el sitio real hoy: 0 hallazgos (no hay regresión activa ahora mismo) — el valor
   es cerrar la puerta para la próxima vez que alguien edite ese catálogo a mano.

**Cómo lo verifiqué:** corrí `.pipeline/recolecta-señales.py` (211 entradas de historial, 27 corridas de
costo, 14 tareas de backlog, REGLAS.md al 99.9% del presupuesto — ese último ya tiene su propia tarea
drenable desde el 3 de julio, no hace falta otra propuesta). Confirmé con `grep` en vivo que los 5
archivos de revisor realmente carecen del `export PATH`, y corrí el checker de catálogo `Service` contra
las páginas reales del sitio (0 falsos positivos hoy).

**Estado del sistema:** sano — sin corridas perdidas por causas evitables (las 3 corridas en 0 tokens de
las últimas 4 semanas fueron límites reales del plan/organización, ya bien manejadas por el driver:
aviso honesto por correo, sin reintentos inútiles). El patrón de esta semana es el mismo que el del
10 de julio: un arreglo puntual (el `export PATH`) que se probó en UN solo lugar en vez de propagarse a
sus hermanos, y una regla de REGLAS.md marcada ALTA que nunca se tradujo a checker. Las 10 propuestas
pendientes de `docs/PROPUESTAS.md` siguen listas para merge.
