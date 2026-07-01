# Meta-pase del Crítico-Sistema — 2026-06-29

Dejé **3 propuestas nuevas**, todas con su DRAFT ya escrito y listas para merge en `docs/PROPUESTAS.md`
(las nuevas van arriba). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto
1. **Detector de corrida DESBOCADA por costo** (impacto A) — 3 de las últimas ~11 corridas explotaron a 606–654M tokens (~$1300–1420 cada una) frente a una mediana de 26.6M. La firma real es un loop sin freno (output 2.1–2.3M y >1400 mensajes), que el tripwire actual no distingue de un día grande. El draft añade un aviso ALTA cuando output o mensajes pasan de ~5× la mediana.
2. **El over-budget de REGLAS.md se vuelve tarea drenable** (impacto M) — REGLAS lleva pegado al tope (3997/4000 tok) corrida tras corrida; hoy solo lo marca un exit-1 de la FASE 9 que se puede ignorar si la fase se salta. El draft es un sensor que emite el hallazgo para que el diario lo drene solo como consolidación.
3. **Gate proactivo de contrato de checkers en pre-push** (impacto M) — la clase "añadí un checker y rompí el sensor de salud" (infra-003/005) ya reincidió ≥3 veces y solo se caza en la corrida del día siguiente, con una ALTA falsa. El draft la bloquea al pushear, antes de que llegue a una corrida.

**Estado del sistema:** sano salvo el costo. Backlog sin tareas (0 pendientes, 0 bloqueadas); 0 hallazgos
marcados pendientes en HISTORIAL; pero el costo tiene picos reales sin vigilancia fina y REGLAS.md sigue
al borde del presupuesto. Esos son justo los dos huecos que cubren las propuestas 1 y 2.

Todas están listas para merge en `docs/PROPUESTAS.md`.
