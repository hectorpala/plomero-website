#!/bin/bash
set -euo pipefail

# Compatibilidad para accesos directos antiguos. Este archivo ya NO ejecuta Claude
# ni mantiene una segunda implementación: delega al único driver vigente de Codex,
# que aplica lock, timeouts, verificación, reporte y candados de publicación.
DRIVER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/crecer-diario.sh"
printf '[%s] Ruta heredada: delego al driver vigente de Codex.\n' "$(date +%Y%m%d-%H%M%S)"
exec /bin/bash "$DRIVER"
