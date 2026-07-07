#!/bin/bash
set -uo pipefail

# ════════════════════════════════════════════════════════════════════════════
#  CRITICO-SISTEMA — meta-pase 3×/semana (Lun/Mié/Vie). Observa el SISTEMA y deja
#  PROPUESTAS con su draft listo en PROPUESTAS.md. NO publica nada, NO arregla: solo propone.
# ════════════════════════════════════════════════════════════════════════════

export NODE_OPTIONS="--dns-result-order=ipv4first"
cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
RUTA_CLAUDE="/Users/openclaw/.npm-global/bin/claude"
LOG="$LOG_DIR/meta-$STAMP.log"

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

# Meta-pase (auto-permiso; solo propone, no publica).
if "$RUTA_CLAUDE" --permission-mode auto -p "$(cat .pipeline/meta-prompt.txt)" >> "$LOG" 2>&1; then
  echo "[$STAMP] meta-pase OK." >> "$LOG"
else
  echo "[$STAMP] meta-pase terminó con error (continúo para enviar el resumen)." >> "$LOG"
fi

# Resumen por email (reusa el emisor; si el agente no dejó ultima-meta.md, send-report alerta).
/usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-meta.md" \
  "Crítico-Sistema (propuestas)" "meta" >> "$LOG" 2>&1 \
  || echo "[$STAMP] No se pudo enviar el email del meta-pase." >> "$LOG"
