#!/bin/bash
set -euo pipefail

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

"$RUTA_CLAUDE" --permission-mode auto -p "$(cat .pipeline/mantener-prompt.txt)" >> "$LOG_DIR/run-$STAMP.log" 2>&1
