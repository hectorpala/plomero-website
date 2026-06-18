#!/bin/bash
set -euo pipefail

# ════════════════════════════════════════════════════════════════════════════
#  AUTO AGENTE PLOMERO — corrida diaria autónoma (todo el sistema junto):
#  CORRIGE errores (mecánicos + humanos) · CRECE +3 páginas/día según GSC ·
#  VERIFICA que todo quedó bien · APRENDE cada error · publica solo si pasa candados.
#  Reemplaza a mantener-diario.sh (lo incluye y le suma crecimiento, verificación y aprendizaje).
# ════════════════════════════════════════════════════════════════════════════

# Forzar IPv4: si IPv6 está roto en la red, node (claude CLI + send-report) falla
# (EHOSTUNREACH). Preferir IPv4 evita que se caigan la corrida y el correo.
export NODE_OPTIONS="--dns-result-order=ipv4first"

cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
RUTA_CLAUDE="/Users/openclaw/.npm-global/bin/claude"
LOG="$LOG_DIR/auto-agente-$STAMP.log"

# Lock por-REPO COMPARTIDO con mantener-diario.sh (mismo nombre) para que NUNCA corran
# dos pipelines a la vez sobre el mismo repo. Resistente a cuelgues: si el dueño del lock
# ya murió (SIGKILL/corte de luz/reboot), se roba el lock en vez de quedar apagado en silencio.
LOCK_DIR="/tmp/plomero-mantener-sitio.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  OLDPID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "[$STAMP] Ya hay una corrida activa (pid $OLDPID); saliendo." >> "$LOG"
    exit 0
  fi
  echo "[$STAMP] Lock huérfano (pid '$OLDPID' ya no vive) -> lo robo y continúo." >> "$LOG"
  rm -rf "$LOCK_DIR"
  mkdir "$LOCK_DIR" 2>/dev/null || { echo "[$STAMP] No pude tomar el lock; saliendo." >> "$LOG"; exit 0; }
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT

# Corrida autónoma del sistema completo (auto-permiso). El prompt orquesta las 10 fases.
RUN_START=$(date +%s)   # para atribuir el costo (tokens) de los transcripts de ESTA corrida
if "$RUTA_CLAUDE" --permission-mode auto -p "$(cat .pipeline/crecer-diario-prompt.txt)" >> "$LOG" 2>&1; then
  CLAUDE_OK=1
else
  CLAUDE_OK=0
  echo "[$STAMP] La corrida de claude terminó con error (continúo para enviar el parte)." >> "$LOG"
fi

# Registro de costo/tokens de la corrida (no bloqueante): suma los transcripts (sesión + subagentes)
# producidos desde RUN_START y los anexa a .pipeline/costos.jsonl. Da visibilidad del gasto diario.
/usr/local/bin/node "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/registrar-costo.mjs" \
  "$HOME/.claude/projects/-Users-openclaw-Sitios-Web-Plomero-Culiac-n" "$RUN_START" \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/costos.jsonl" "auto-agente $STAMP" >> "$LOG" 2>&1 \
  || echo "[$STAMP] No pude registrar el costo de la corrida (sigo)." >> "$LOG"

# Cuadre del parte (red de seguridad INDEPENDIENTE del LLM): verifica que el correo cuadre con los
# cambios reales (conteos del encabezado == ítems listados, y ninguna URL "arreglada" inventada).
# Si NO cuadra, antepone un AVISO automático al cuerpo del correo para que el humano SIEMPRE lo vea
# (el agente no puede esconder una discrepancia). No bloquea el envío.
PARTE="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-corrida.md"
if [ -f "$PARTE" ]; then
  if ! CUADRE=$(python3 "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/check-parte.py" "$PARTE" 2>&1); then
    {
      echo "## ⚠️ AVISO AUTOMÁTICO — el parte no cuadra con los cambios reales"
      echo "**Esto lo verificó el sistema, NO el agente.** Revisa el parte de abajo con ojo crítico — puede faltar o sobrar algo de lo reportado:"
      echo
      echo "$CUADRE"
      echo
      echo "---"
      echo
      cat "$PARTE"
    } > "$PARTE.tmp" && mv "$PARTE.tmp" "$PARTE"
    echo "[$STAMP] check-parte: el parte NO cuadra; antepuse aviso al correo." >> "$LOG"
  fi
fi

# Parte por email — SIEMPRE, aun si la corrida falló (send-report alerta si el resumen es viejo/ausente).
/usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-corrida.md" \
  "Auto Agente Plomero" "18:25" >> "$LOG" 2>&1 \
  || echo "[$STAMP] No se pudo enviar el email del parte (Auto Agente Plomero)." >> "$LOG"

# Marca que YA corrió hoy SOLO si la corrida tuvo éxito. Si falló, NO se marca → el
# catch-up sí podrá recuperarla hoy (si se marcara siempre, una corrida fallida quedaría sin recuperar).
[ "${CLAUDE_OK:-0}" = 1 ] && date +%Y%m%d > "$LOG_DIR/auto-agente-plomero-last-run-day"
