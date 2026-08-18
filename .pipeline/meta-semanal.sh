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
CODEX_BIN="/Users/openclaw/.local/bin/codex"
LOG="$LOG_DIR/meta-plomero-$STAMP.log"

# Cortesía con la corrida diaria: si el pipeline principal está corriendo (lock con pid
# vivo), NO correr en paralelo — dos agentes en el mismo repo pueden pisarse (el meta
# escribe PROPUESTAS.md/ultima-meta.md a mitad de un commit/checkout del diario).
MAIN_LOCK="/tmp/plomero-mantener-sitio.lock"
MAIN_PID=$(cat "$MAIN_LOCK/pid" 2>/dev/null || echo "")
if [ -n "$MAIN_PID" ] && kill -0 "$MAIN_PID" 2>/dev/null; then
  echo "[$STAMP] corrida diaria activa (pid $MAIN_PID); pospongo el meta-pase." >> "$LOG"
  exit 0
fi

# Lock propio (NO comparte con la corrida diaria: el meta-pase solo lee + escribe PROPUESTAS.md).
LOCK_DIR="/tmp/plomero-meta.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  OLDPID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "[$STAMP] meta-pase ya activo (pid $OLDPID); saliendo." >> "$LOG"; exit 0
  fi
  rm -rf "$LOCK_DIR"; mkdir "$LOCK_DIR" 2>/dev/null || exit 0
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT

# Meta-pase con Codex y CERO MCP: ignora la configuración global porque solo lee el repo
# y escribe propuestas locales; nunca necesita integraciones externas.
CODEX_OK=0
if [ -x "$CODEX_BIN" ] && "$CODEX_BIN" login status >> "$LOG" 2>&1; then
  if "$CODEX_BIN" exec --cd "/Users/openclaw/Sitios Web/Plomero Culiacán" \
      --approve-for-me --ephemeral --ignore-user-config --strict-config --json \
      - < .pipeline/meta-prompt.txt >> "$LOG" 2>&1 \
      && grep -q '"type":"turn.completed"' "$LOG"; then
    CODEX_OK=1
    echo "[$STAMP] meta-pase Codex OK." >> "$LOG"
  fi
else
  echo "[$STAMP] Codex no está instalado o autenticado." >> "$LOG"
fi

# Resumen por email, solo si Codex escribió un archivo fresco en ESTA corrida.
META="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-meta.md"
META_MTIME=$(stat -f %m "$META" 2>/dev/null || echo 0)
if [ "$CODEX_OK" != 1 ] || [ "$META_MTIME" -lt "$RUN_START" ]; then
  META="$LOG_DIR/meta-plomero-fail-$STAMP.md"
  printf '# Crítico-Sistema Plomero — corrida no completada\nCodex no terminó el meta-pase o no escribió un resumen nuevo. Revisa: %s\n' "$LOG" > "$META"
fi
/usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
  "$META" \
  "Crítico-Sistema (propuestas)" "meta" >> "$LOG" 2>&1 \
  || echo "[$STAMP] No se pudo enviar el email del meta-pase." >> "$LOG"
