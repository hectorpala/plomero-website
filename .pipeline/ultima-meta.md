# Meta-pase del Crítico-Sistema — 2026-07-06

Dejé **4 propuestas nuevas**, todas con su DRAFT ya escrito y listas para merge en `docs/PROPUESTAS.md`
(las nuevas van arriba). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto
1. **(A) Los vigilantes del Plomero pueden confundirse con el sitio del Electricista.** Los dos sitios
   guardan sus registros de corrida en la MISMA carpeta con el MISMO nombre. El vigilante que revisa
   "¿corrió hoy el sistema?" y el que recupera corridas saltadas toman "el registro más nuevo" sin fijarse
   de qué sitio es: si el del Plomero se muere pero el del Electricista sigue corriendo, nadie se enteraría.
   Lo comprobé hoy con un caso real. El draft les pone apellido a los registros del Plomero (3 parches chicos).
2. **(A) El sistema lleva 4 días sin completar una corrida y ningún sensor lo dijo.** El 4 de julio no corrió
   nada (día perdido en silencio) y el 5 de julio la corrida murió a medias por fallas de conexión (3 intentos
   agotados). Hoy nada lo reporta: el registro simplemente "no tiene fila". El draft añade dos detectores al
   vigilante de costos: "hubo un día sin corrida" y "la corrida quedó enana (murió a medias); adopta su trabajo".
3. **(M) Los reintentos "de 2 minutos" pueden ocurrir 15 horas después.** Cuando la Mac se duerme, la espera
   entre reintentos se congela: un reintento programado para las 8 de la noche corrió a las 3 de la madrugada,
   y en el sitio hermano uno corrió al día siguiente a media mañana, encimado con otros procesos. El draft
   pone un límite de reloj real: si ya pasaron más de 3 horas, se abandona y lo recupera la corrida de mañana.

La 4ª (M): el brief ahora dirá cuántos DÍAS lleva esperándote cada decisión pendiente — hay una de 17 días
(páginas casi gemelas por consolidar) y una de 14 (reconectar el sensor de Google Search Console del CLI).

**Estado del sistema:** los checkers en sí están sanos y el backlog no tiene tareas bloqueadas; el problema
de esta semana es de CONTINUIDAD (corridas que no ocurren o mueren a medias sin que nadie lo diga) — las
propuestas 1-3 cierran justo eso. Todas están listas para merge en `docs/PROPUESTAS.md`.
