#!/bin/bash
cd "/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
RUTA_CLAUDE="/Users/openclaw/.npm-global/bin/claude"
"$RUTA_CLAUDE" --permission-mode auto -p "$(cat .pipeline/mantener-prompt.txt)" >> "$LOG_DIR/run-$STAMP.log" 2>&1
