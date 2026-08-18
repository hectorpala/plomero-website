# Plomero Culiacán — instrucciones para Codex

Antes de trabajar, lee `CLAUDE.md` completo y trátalo como instrucciones obligatorias del proyecto. El nombre del
archivo es histórico: sus reglas de negocio, seguridad, SEO, verificación y publicación también aplican a Codex.

Compatibilidad de automatización:

- Los roles especializados siguen en `.claude/agents/*.md`. Cuando una tarea pida un rol, lee su archivo completo
  y aplícalo tú mismo como una pasada independiente, con evidencia y un resultado explícito. La automatización no
  depende de subagentes nativos: en modo no interactivo pueden terminar sin haber devuelto un resultado verificable.
- Las skills históricas siguen en `.claude/skills/*/SKILL.md`. Lee el `SKILL.md` completo antes de seguirlas.
- La fase final debe ser una pasada nueva, escéptica y estrictamente de solo lectura; descarta las conclusiones de
  las pasadas anteriores y vuelve a correr los candados desde cero.
- En una corrida automática, ante cualquier duda o candado fallido, no publiques.
