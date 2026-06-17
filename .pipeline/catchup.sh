#!/bin/bash
# catchup.sh — Recupera la corrida diaria si se saltó (Mac apagada/dormida a la hora).
# Lo dispara el LaunchAgent com.plomeroculiacan.catchup con RunAtLoad (al iniciar sesión/boot).
# Regla: si la última corrida fue hace >= 20h, se saltó al menos una diaria -> recuperar ahora.
# El lock de mantener-diario.sh evita doble corrida si la programada está activa.
set -uo pipefail

LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
SCRIPT="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/mantener-diario.sh"
STAMP=$(date "+%Y-%m-%d %H:%M:%S")

NEWEST=$(ls -t "$LOG_DIR"/run-*.log 2>/dev/null | head -1)
if [ -n "$NEWEST" ]; then
  AGE_H=$(( ( $(date +%s) - $(stat -f %m "$NEWEST") ) / 3600 ))
else
  AGE_H=999
fi

# La última corrida FALLÓ si su log trae el marcador de error de claude
# (mantener-diario.sh escribe "terminó con error" si claude sale != 0).
FAILED=0
[ -n "$NEWEST" ] && grep -qiE "termin. con error|API Error" "$NEWEST" && FAILED=1

if [ "$AGE_H" -ge 20 ]; then
  echo "[$STAMP] catch-up: última corrida hace ${AGE_H}h (>=20, ausente) -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up: terminado" >> "$LOG_DIR/catchup.log"
elif [ "$FAILED" = 1 ]; then
  echo "[$STAMP] catch-up: última corrida (hace ${AGE_H}h) FALLÓ -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up: terminado" >> "$LOG_DIR/catchup.log"
else
  echo "[$STAMP] catch-up: última corrida hace ${AGE_H}h, OK -> sin acción" >> "$LOG_DIR/catchup.log"
fi
