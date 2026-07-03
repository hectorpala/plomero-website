# Meta-pase del Crítico-Sistema — 2026-07-03

Dejé **3 propuestas nuevas**, todas con su DRAFT ya escrito y listas para merge en `docs/PROPUESTAS.md`
(las nuevas van arriba). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto
1. **(A) Cerrar el segundo hueco de "rutas rotas".** El sistema ya se tropezó DOS veces seguidas
   (infra-006 y infra-007, las 2 corridas más recientes) con rutas que quedaron mal tras reorganizar el
   repo. El checker de la vez pasada solo tapó una mitad; el draft tapa la otra —la que dejó el backlog
   marcando "0 tareas" varios días sin que nadie lo notara.
2. **(M) Cazar la corrida de 0 tokens.** Una corrida marcó "0 tokens" (2026-07-01) y el vigilante de
   costo la leyó como "todo barato" cuando en realidad el medidor se rompió o la corrida no corrió. El
   draft hace que ese 0 salte en el reporte diario en vez de esconderse.
3. **(M) Vigilar que los arreglos móviles lleguen a TODAS las páginas de servicio.** Un arreglo se
   aplicó a 1 de 18 páginas y las otras 17 se quedaron sin él hasta notarlo a ojo (familia movil-502/701/801).
   El draft es un vigilante que revisa la paridad solo, para siempre, y hoy arranca limpio (18/18 ya cubiertas).

**Estado del sistema:** sano en lo esencial. 0 hallazgos marcados pendientes en HISTORIAL; backlog con 2
tareas pendientes y 2 en espera de decisión humana (doorway-domicilio, re-auth token GSC). La señal más
fuerte es la REINCIDENCIA de la clase "rutas rotas" (2 de 2 corridas recientes) → la propuesta 1 la cierra.
El costo tuvo un pico de ~654M tokens (~25× la mediana) y una fila de 0 tokens; el pico ya lo cubre la
propuesta de "corrida desbocada" que sigue pendiente, y el 0 lo cubre la nueva propuesta 2.

Todas están listas para merge en `docs/PROPUESTAS.md`.
