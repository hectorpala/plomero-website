# Meta-pase del Crítico-Sistema — 2026-06-19

Dejé **4 propuestas nuevas**, todas con su DRAFT ya escrito y listas para merge en `PROPUESTAS.md`
(las nuevas van arriba). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto
1. **Barrido estructural de TODO el sitio** (impacto A) — hoy el gate solo revisa las páginas que se editan, así que faltas viejas (sin `<meta robots>`, hero sin `.hero-content`) quedan ocultas hasta que tocas la página y el push se traba por sorpresa. Un checker nuevo barre el sitio entero y las convierte en tareas de backlog antes de que estorben.
2. **Cazar `og:url` ausente** (impacto M) — el checker de indexabilidad solo marca el `og:url` *equivocado*, no el que *falta*; por eso 6 páginas de servicio sin esa etiqueta quedaron como deuda silenciosa. Son 5 líneas extra en un checker que ya existe.
3. **Quitar el acoplamiento que hace mentir al sensor de salud** (impacto M) — el 18-jun se añadieron 2 utilidades y el dead-man's switch gritó 2 alarmas falsas porque había que actualizar una lista central a mano. La propuesta deja que cada utilidad se auto-excluya con un marcador, sin tocar ese archivo central.

La 4ª (impacto B): un *tripwire de costo* que avisa en el reporte cuando una corrida se dispara
(la grande del 18-jun fueron 35.5M tokens / ~$91, 3× lo normal). Solo da visibilidad, no corta nada.

**Estado del sistema:** sano. Backlog sin tareas bloqueadas (5 pendientes, 0 esperando humano);
REGLAS.md al 85% del presupuesto (3411/4000 tok); sin regresiones nuevas sin atender.
Los dos drafts en Python los validé contra datos reales (lógica y sintaxis OK).

Todas están listas para merge en `PROPUESTAS.md`.
