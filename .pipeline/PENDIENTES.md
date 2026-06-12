# Pendientes del pipeline de agentes

Estado actualizado para el modo autónomo.

## Hecho
- Memoria activa: `CLAUDE.md`, `REGLAS.md`, `HISTORIAL.jsonl`, `ESTADO.md`.
- 6 revisores: `revisor-seo`, `revisor-movil`, `revisor-a11y`, `revisor-perf`, `revisor-links`, `revisor-gsc`.
- Crítico semanal de completitud: `.claude/agents/critico-completitud.md`.
- Comando de enseñanza: `.claude/skills/ensenar/SKILL.md`.
- Runner headless: `.pipeline/mantener-diario.sh`.
- LaunchAgent creado: `~/Library/LaunchAgents/com.plomeroculiacan.mantener.plist` a las 20:00.
- Primera corrida autónoma publicada y documentada en `.pipeline/ultima-corrida.md`.

## Pendiente inmediato
- Confirmar la primera corrida real de `launchd` después de las 20:00 revisando `~/Library/Logs/mantener-sitio/launchd.err.log`, `launchd.out.log` y el log `run-*.log`.
- Confirmar que en la próxima corrida `revisor-gsc` usa las herramientas nativas `mcp__local-seo__*` (la config se movió a `.mcp.json` en la raíz el 2026-06-12; la corrida anterior improvisó un cliente MCP propio porque el servidor no cargaba).
- Verificar que `mcp-local-seo/client_secret.json` y `mcp-local-seo/gsc-token.json` existen y renuevan token en modo headless.
- Revisar los pendientes humanos en `ESTADO.md` antes de permitir que el modo automático toque estrategia SEO, copy, navegación o colores de marca.

## Pendientes humanos del sitio
- `gsc-201`: decidir consolidación de `/precios/` vs `/servicios/plomero-precios/`.
- `gsc-202`: decidir enlace real al hub `/servicios/` en navegación/footer.
- `gsc-203`: reenviar sitemap en Search Console si el log confirma copia rancia.
- `a11y-201`: decidir color accesible para "Disponibles ahora".
