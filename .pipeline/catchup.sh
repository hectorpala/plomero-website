#!/bin/bash
# catchup.sh — Recupera la corrida diaria si se saltó (Mac apagada/dormida a la hora).
# Lo dispara el LaunchAgent com.plomeroculiacan.catchup con RunAtLoad (al iniciar sesión/boot).
# Regla: si la última corrida fue hace >= 20h, se saltó al menos una diaria -> recuperar ahora.
# Apunta al sistema unificado (Auto Agente Plomero), no al viejo de solo-mantenimiento.
# El lock de crecer-diario.sh (/tmp/plomero-mantener-sitio.lock) evita doble corrida.
set -uo pipefail

LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
SCRIPT="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/crecer-diario.sh"
STAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Anti doble-corrida: si YA hubo una corrida HOY (marca datada que escribe el driver al
# terminar bien), no dispares otra aunque hayan pasado >=20h (evita 1 por reinicio + 1 por launchd).
TODAY=$(date +%Y%m%d)
if [ "$(cat "$LOG_DIR/auto-agente-plomero-last-run-day" 2>/dev/null || echo "")" = "$TODAY" ]; then
  echo "[$STAMP] catch-up plomero: ya corrió hoy ($TODAY) -> sin acción" >> "$LOG_DIR/catchup.log"
  exit 0
fi

# Busca el log más reciente de cualquiera de los dos drivers (auto-agente nuevo o run-* viejo).
NEWEST=$(ls -t "$LOG_DIR"/auto-agente-2*.log "$LOG_DIR"/run-2*.log 2>/dev/null | head -1)
if [ -n "$NEWEST" ]; then
  AGE_H=$(( ( $(date +%s) - $(stat -f %m "$NEWEST") ) / 3600 ))
else
  AGE_H=999
fi

# La última corrida FALLÓ si su log trae el marcador de error de claude.
FAILED=0
[ -n "$NEWEST" ] && grep -qiE "termin. con error|API Error" "$NEWEST" && FAILED=1

if [ "$AGE_H" -ge 20 ]; then
  echo "[$STAMP] catch-up plomero: última corrida hace ${AGE_H}h (>=20, ausente) -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up plomero: terminado" >> "$LOG_DIR/catchup.log"
elif [ "$FAILED" = 1 ]; then
  echo "[$STAMP] catch-up plomero: última corrida (hace ${AGE_H}h) FALLÓ -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up plomero: terminado" >> "$LOG_DIR/catchup.log"
else
  echo "[$STAMP] catch-up plomero: última corrida hace ${AGE_H}h, OK -> sin acción" >> "$LOG_DIR/catchup.log"
fi
