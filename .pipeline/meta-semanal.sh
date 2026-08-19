#!/bin/bash
set -uo pipefail

# ════════════════════════════════════════════════════════════════════════════
#  CRITICO-SISTEMA — meta-pase 3×/semana (Lun/Mié/Vie). Observa el SISTEMA y deja
#  PROPUESTAS con su draft listo en PROPUESTAS.md. NO publica nada, NO arregla: solo propone.
# ════════════════════════════════════════════════════════════════════════════

export NODE_OPTIONS="--dns-result-order=ipv4first"
export PATH="/Users/openclaw/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"
cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
RUN_START=$(date +%s)
CODEX_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-codex.py"
CODEX_BIN=$(python3 "$CODEX_FINDER" 2>/dev/null || true)
NODE_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-node.py"
NODE_BIN=$(python3 "$NODE_FINDER" 2>/dev/null || true)
AUTH_CHECK="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/codex-login-preflight.py"
AUTH_TIMEOUT_SECONDS=30
LOG="$LOG_DIR/meta-plomero-$STAMP.log"

# Candado COMPARTIDO con la corrida diaria y el maratón. Antes el meta solo miraba
# el lock principal y luego adquiría otro distinto: la diaria podía arrancar en esa
# ventana y ambos escribían el repo a la vez. `mkdir` vuelve la exclusión atómica.
LOCK_DIR="/tmp/plomero-mantener-sitio.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  OLDPID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "[$STAMP] otro pipeline del repo está activo (pid $OLDPID); pospongo el meta-pase." >> "$LOG"
    exit 0
  fi
  # Un lock sin pid puede estar en la ventana mkdir→escritura del dueño. Solo se
  # considera huérfano después de 2 minutos, igual que en crecer-diario.sh.
  if [ -z "$OLDPID" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0) ))
    if [ "$LOCK_AGE" -lt 120 ]; then
      echo "[$STAMP] lock compartido sin pid pero recién creado (${LOCK_AGE}s); pospongo el meta-pase." >> "$LOG"
      exit 0
    fi
  fi
  # Robo atómico del lock huérfano: solo un contendiente puede moverlo.
  if mv "$LOCK_DIR" "$LOCK_DIR.stale.$$" 2>/dev/null; then
    rm -rf "$LOCK_DIR.stale.$$"
  else
    echo "[$STAMP] otro proceso recuperó el lock; pospongo el meta-pase." >> "$LOG"
    exit 0
  fi
  mkdir "$LOCK_DIR" 2>/dev/null || {
    echo "[$STAMP] no pude adquirir el lock compartido; pospongo el meta-pase." >> "$LOG"
    exit 0
  }
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT

# Meta-pase con Codex y CERO MCP: ignora la configuración global porque solo lee el repo
# y escribe propuestas locales; nunca necesita integraciones externas.
CODEX_OK=0
META_TIMEOUT_MIN=45
AUTH_OK=0
if [ -x "$CODEX_BIN" ]; then
  if python3 "$AUTH_CHECK" "$CODEX_BIN" "$AUTH_TIMEOUT_SECONDS" >> "$LOG" 2>&1; then
    AUTH_OK=1
  else
    AUTH_RC=$?
    if [ "$AUTH_RC" -eq 124 ]; then
      echo "[$STAMP] El preflight de autenticación excedió ${AUTH_TIMEOUT_SECONDS}s; libero el lock sin iniciar el meta-pase." >> "$LOG"
    else
      echo "[$STAMP] Codex no está autenticado." >> "$LOG"
    fi
  fi
else
  echo "[$STAMP] Codex no está instalado." >> "$LOG"
fi
if [ "$AUTH_OK" = 1 ]; then
  "$CODEX_BIN" exec --cd "/Users/openclaw/Sitios Web/Plomero Culiacán" \
      --approve-for-me --ephemeral --ignore-user-config --strict-config --json \
      - < .pipeline/meta-prompt.txt >> "$LOG" 2>&1 \
      &
  META_PID=$!
  META_DEADLINE=$((RUN_START + META_TIMEOUT_MIN * 60))
  # Reloj de pared: tras despertar del reposo, `date` detecta inmediatamente que
  # venció el plazo aunque los `sleep` del watchdog hayan quedado pausados.
  (
    while kill -0 "$META_PID" 2>/dev/null; do
      if [ "$(date +%s)" -ge "$META_DEADLINE" ]; then
        echo "[$STAMP] META_TIMEOUT ${META_TIMEOUT_MIN}min: termino Codex (pid $META_PID) para liberar el lock compartido." >> "$LOG"
        kill "$META_PID" 2>/dev/null || true
        sleep 10
        kill -9 "$META_PID" 2>/dev/null || true
        break
      fi
      sleep 15
    done
  ) &
  WATCHDOG_PID=$!
  META_RC=0
  wait "$META_PID" || META_RC=$?
  kill "$WATCHDOG_PID" 2>/dev/null || true
  wait "$WATCHDOG_PID" 2>/dev/null || true
  if [ "$META_RC" -eq 0 ] \
      && ! grep -q "META_TIMEOUT ${META_TIMEOUT_MIN}min" "$LOG" \
      && grep -q '"type":"turn.completed"' "$LOG"; then
    CODEX_OK=1
    echo "[$STAMP] meta-pase Codex OK." >> "$LOG"
  fi
fi

# Resumen por email, solo si Codex escribió un archivo fresco en ESTA corrida.
META="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-meta.md"
META_MTIME=$(stat -f %m "$META" 2>/dev/null || echo 0)
if [ "$CODEX_OK" != 1 ] || [ "$META_MTIME" -lt "$RUN_START" ]; then
  META="$LOG_DIR/meta-plomero-fail-$STAMP.md"
  if grep -q "META_TIMEOUT ${META_TIMEOUT_MIN}min" "$LOG"; then
    META_FAIL_REASON="Codex excedió el límite de ${META_TIMEOUT_MIN} minutos y fue terminado para no bloquear la corrida diaria."
  else
    META_FAIL_REASON="Codex no terminó el meta-pase o no escribió un resumen nuevo."
  fi
  printf '# Crítico-Sistema Plomero — corrida no completada\n%s Revisa: %s\n' "$META_FAIL_REASON" "$LOG" > "$META"
fi
if [ -n "$NODE_BIN" ] && [ -x "$NODE_BIN" ]; then
  "$NODE_BIN" /Users/openclaw/gsc-mcp/send-report.mjs \
    "$META" \
    "Crítico-Sistema (propuestas)" "meta" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el email del meta-pase." >> "$LOG"
else
  echo "[$STAMP] No encontré Node; no se pudo enviar el email del meta-pase." >> "$LOG"
fi
