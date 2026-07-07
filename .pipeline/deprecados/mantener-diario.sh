#!/bin/bash
set -euo pipefail

# Forzar IPv4: el 2026-06-16 la corrida de claude (socket cerrado) y el correo
# (EHOSTUNREACH IPv6 a Gmail) fallaron por IPv6 roto en la red. Esto hace que node
# (claude CLI + send-report) prefiera IPv4 y evita ambos fallos.
export NODE_OPTIONS="--dns-result-order=ipv4first"

cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
RUTA_CLAUDE="/Users/openclaw/.npm-global/bin/claude"

LOCK_DIR="/tmp/plomero-mantener-sitio.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "[$STAMP] Ya hay una corrida de mantenimiento activa; saliendo." >> "$LOG_DIR/run-$STAMP.log"
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

"$RUTA_CLAUDE" --model sonnet --permission-mode auto -p "$(cat .pipeline/mantener-prompt.txt)" >> "$LOG_DIR/run-$STAMP.log" 2>&1 \
  || echo "[$STAMP] La corrida de claude terminó con error (continúo para enviar el parte)." >> "$LOG_DIR/run-$STAMP.log"

# Parte por email — SIEMPRE, aun si la corrida falló: send-report detecta resumen viejo/ausente y alerta.
/usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-corrida.md" \
  "Plomero Culiacán" "18:25" >> "$LOG_DIR/run-$STAMP.log" 2>&1 \
  || echo "[$STAMP] No se pudo enviar el email del parte." >> "$LOG_DIR/run-$STAMP.log"
