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
CLASSIFIER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/clasificar-log-corrida.py"
STAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Anti doble-corrida: si YA hubo una corrida HOY (marca datada que escribe el driver al
# terminar bien), no dispares otra aunque hayan pasado >=20h (evita 1 por reinicio + 1 por launchd).
TODAY=$(date +%Y%m%d)
LAST_RUN_DAY=$(cat "$LOG_DIR/auto-agente-plomero-last-run-day" 2>/dev/null || echo "")
if [ "$LAST_RUN_DAY" = "$TODAY" ]; then
  echo "[$STAMP] catch-up plomero: ya corrió hoy ($TODAY) -> sin acción" >> "$LOG_DIR/catchup.log"
  exit 0
fi

# Un log sin sentinel puede ser una corrida TODAVÍA activa. Consultar primero el
# lock compartido evita lanzar una recuperación mientras el driver sigue trabajando.
LOCK_DIR="/tmp/plomero-mantener-sitio.lock"
ACTIVE_PID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
if [ -n "$ACTIVE_PID" ] && kill -0 "$ACTIVE_PID" 2>/dev/null; then
  echo "[$STAMP] catch-up plomero: corrida activa (pid $ACTIVE_PID) -> sin acción" >> "$LOG_DIR/catchup.log"
  exit 0
fi
if [ "$(cat "$LOG_DIR/auto-agente-plomero-no-retry-day" 2>/dev/null || echo "")" = "$TODAY" ]; then
  echo "[$STAMP] catch-up plomero: publicación posible/no verificable hoy; no repito para evitar duplicarla" >> "$LOG_DIR/catchup.log"
  exit 0
fi

# SOLO logs del PLOMERO (namespaceados): los globs viejos (auto-agente-2*.log/run-2*.log)
# matcheaban también los del ELECTRICISTA (mismo LOG_DIR y prefijo) → con el plomero
# muerto y el electricista vivo, el catch-up veía "log fresco, OK" y NO recuperaba
# (así pasó del 04 al 07-jul-2026).
NEWEST=$(ls -t "$LOG_DIR"/auto-agente-plomero-2*.log "$LOG_DIR"/run-2*.log 2>/dev/null | head -1)
if [ -n "$NEWEST" ]; then
  AGE_H=$(( ( $(date +%s) - $(stat -f %m "$NEWEST") ) / 3600 ))
else
  AGE_H=999
fi

# El sentinel nuevo distingue éxito, fallo e interrupción abrupta. Para logs legados,
# se conserva el marcador textual de fallo. Un log posterior al último día exitoso
# y SIN sentinel es truncado (SIGKILL/corte de luz), no una corrida sana.
FAILED=0
INCOMPLETE=0
LOG_STATE="sin_log"
if [ -n "$NEWEST" ]; then
  LOG_STATE=$(python3 "$CLASSIFIER" "$NEWEST" "$LAST_RUN_DAY" 2>/dev/null || echo "incompleta")
  [ "$LOG_STATE" = "fallida" ] && FAILED=1
  [ "$LOG_STATE" = "incompleta" ] && INCOMPLETE=1
  [ "$LOG_STATE" = "legado" ] && grep -qiE "termin. con error" "$NEWEST" && FAILED=1
fi

if [ "$AGE_H" -ge 20 ]; then
  echo "[$STAMP] catch-up plomero: última corrida hace ${AGE_H}h (>=20, ausente) -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up plomero: terminado" >> "$LOG_DIR/catchup.log"
elif [ "$FAILED" = 1 ]; then
  echo "[$STAMP] catch-up plomero: última corrida (hace ${AGE_H}h) FALLÓ -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up plomero: terminado" >> "$LOG_DIR/catchup.log"
elif [ "$INCOMPLETE" = 1 ]; then
  echo "[$STAMP] catch-up plomero: log nuevo INCOMPLETO y sin proceso activo -> RECUPERANDO" >> "$LOG_DIR/catchup.log"
  bash "$SCRIPT"
  echo "[$STAMP] catch-up plomero: terminado" >> "$LOG_DIR/catchup.log"
else
  echo "[$STAMP] catch-up plomero: última corrida hace ${AGE_H}h, OK -> sin acción" >> "$LOG_DIR/catchup.log"
fi
