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

# SOLO logs del PLOMERO (namespaceados): los globs viejos (auto-agente-2*.log/run-2*.log)
# matcheaban también los del ELECTRICISTA (mismo LOG_DIR y prefijo) → con el plomero
# muerto y el electricista vivo, el catch-up veía "log fresco, OK" y NO recuperaba
# (así pasó del 04 al 07-jul-2026).
NEWEST=$(ls -t "$LOG_DIR"/auto-agente-plomero-2*.log 2>/dev/null | head -1)
if [ -n "$NEWEST" ]; then
  AGE_H=$(( ( $(date +%s) - $(stat -f %m "$NEWEST") ) / 3600 ))
else
  AGE_H=999
fi

# La última corrida FALLÓ si trae el marcador propio del DRIVER ("terminó con error").
# Antes también grepeaba "API Error", que aparece en el STREAM de corridas exitosas
# (reintentos internos relatados por claude) → falso FAILED → corrida extra en el boot.
FAILED=0
[ -n "$NEWEST" ] && grep -qiE "termin. con error" "$NEWEST" && FAILED=1

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
