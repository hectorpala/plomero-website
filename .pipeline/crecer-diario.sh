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

# Guard "ya corrió hoy": si una corrida YA terminó OK hoy (marca datada), no repetir — evita el
# doble cuando un disparo MANUAL coincide con el job programado de las 18:25. Una corrida FALLIDA
# NO deja marca, así que la de las 18:25 sí la recupera (no rompe el recovery).
# Forzar una corrida extra a propósito:  FORCE_RUN=1 bash .pipeline/crecer-diario.sh
TODAY=$(date +%Y%m%d)
if [ "${FORCE_RUN:-0}" != "1" ] && [ "$(cat "$LOG_DIR/auto-agente-plomero-last-run-day" 2>/dev/null || echo "")" = "$TODAY" ]; then
  echo "[$STAMP] Ya hubo una corrida exitosa hoy ($TODAY); no repito (FORCE_RUN=1 para forzar)." >> "$LOG"
  exit 0
fi

# Corrida autónoma del sistema completo (auto-permiso). El prompt orquesta las 10 fases.
RUN_START=$(date +%s)   # para atribuir el costo (tokens) de los transcripts de ESTA corrida

# ── Clasificación de errores (NO confundir red con cuota) ────────────────────
# TRANSITORIO = se cayó la conexión / el servidor falló a media respuesta. Se REINTENTA:
#   no perdimos cuota, solo se cortó el stream (el caso del 2026-06-24: "Connection closed mid-response").
# LIMITE = de verdad se agotó el uso del plan. NO se reintenta (sería inútil hasta que reinicie la cuota).
# El match se hace SOLO sobre lo que imprimió ESE intento (por offset de bytes), así la línea de
# estadística "📊 Uso de la corrida (cuota de suscripción)" —que se anexa DESPUÉS— nunca cuenta como motivo.
TRANSIENT_RE='Connection closed mid-response|API Error|Connection error|overloaded|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|fetch failed|socket hang up|terminated|Internal server error|HTTP 5[0-9][0-9]|\b5(00|02|03|29)\b|may be incomplete'
LIMIT_RE='session limit|usage limit|hit your (usage|limit)|rate limit|límite de uso|quota exceeded|resets? at|your limit will reset'

MAX_ATTEMPTS=3
CLAUDE_OK=0
FAIL_KIND=""          # transitorio | limite | desconocido
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "[$STAMP] >>> intento $attempt/$MAX_ATTEMPTS de la corrida @ $(date +%H:%M:%S)" >> "$LOG"
  OFF=$(wc -c < "$LOG")   # byte-offset: leeremos SOLO lo que agregue este intento
  if "$RUTA_CLAUDE" --permission-mode auto -p "$(cat .pipeline/crecer-diario-prompt.txt)" >> "$LOG" 2>&1; then
    CLAUDE_OK=1; FAIL_KIND=""; break
  fi
  TAIL=$(tail -c "+$((OFF + 1))" "$LOG" 2>/dev/null || echo "")
  if printf '%s' "$TAIL" | grep -qiE "$LIMIT_RE"; then
    FAIL_KIND="limite"
    echo "[$STAMP] Falla por LÍMITE DE USO real del plan; no tiene caso reintentar." >> "$LOG"
    break
  fi
  if printf '%s' "$TAIL" | grep -qiE "$TRANSIENT_RE"; then
    FAIL_KIND="transitorio"
  else
    FAIL_KIND="desconocido"
  fi
  if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
    WAIT=$((attempt * 120))   # backoff: 120s, luego 240s
    echo "[$STAMP] Error $FAIL_KIND (NO de cuota); reintento en ${WAIT}s." >> "$LOG"
    sleep "$WAIT"
  else
    echo "[$STAMP] Agotados los $MAX_ATTEMPTS intentos; la corrida no completó." >> "$LOG"
  fi
done
[ "$CLAUDE_OK" = 1 ] || echo "[$STAMP] La corrida de claude terminó con error ($FAIL_KIND); continúo para enviar el parte." >> "$LOG"

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

# Parte por email. Si la corrida tuvo ÉXITO → parte nuevo. Si FALLÓ (cuota/error) → NO mandes
# el parte viejo (correo engañoso "encontré N" de otra corrida); manda un aviso honesto.
if [ "${CLAUDE_OK:-0}" = 1 ]; then
  /usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
    "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-corrida.md" \
    "Auto Agente Plomero" "18:25" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el email del parte (Auto Agente Plomero)." >> "$LOG"
else
  FAILNOTE="$LOG_DIR/fail-$STAMP.md"
  # Motivo HONESTO según el tipo de falla (no asumir cuota). La línea de evidencia se saca del
  # log EXCLUYENDO la estadística "📊 Uso ... (cuota de suscripción)" para no volver a confundirla con un error.
  ERRLINE=$(grep -iE "$TRANSIENT_RE|$LIMIT_RE" "$LOG" 2>/dev/null | grep -viE '📊 Uso|cuota de suscripción|equiv-API' | head -1 | sed 's/^[[:space:]]*//')
  [ -n "$ERRLINE" ] || ERRLINE="(sin línea de error reconocible; revisa el log completo)"
  case "$FAIL_KIND" in
    transitorio)
      MOTIVO="se cayó la conexión con el servidor a media respuesta — error TRANSITORIO de red, NO de cuota (corrió con tu plan, no se facturó nada)"
      SUGERENCIA="El sistema ya reintentó $MAX_ATTEMPTS veces sin éxito. No requiere acción: el catch-up o la corrida de mañana lo recuperan." ;;
    limite)
      MOTIVO="se alcanzó el límite de uso del plan"
      SUGERENCIA="Reintenta cuando se restablezca la cuota." ;;
    *)
      MOTIVO="error no reconocido de la corrida"
      SUGERENCIA="Revisa el log: $LOG" ;;
  esac
  printf '# Auto Agente Plomero — corrida NO completada\n**Motivo:** %s.\n**Evidencia (del log):** `%s`\n**Qué sigue:** %s\n\nNo se hizo ni publicó ningún cambio en esta corrida.\n' \
    "$MOTIVO" "$ERRLINE" "$SUGERENCIA" > "$FAILNOTE"
  /usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
    "$FAILNOTE" "Auto Agente Plomero" "no completada" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el aviso de falla (Auto Agente Plomero)." >> "$LOG"
fi

# Marca que YA corrió hoy SOLO si la corrida tuvo éxito. Si falló, NO se marca → el
# catch-up sí podrá recuperarla hoy (si se marcara siempre, una corrida fallida quedaría sin recuperar).
[ "${CLAUDE_OK:-0}" = 1 ] && date +%Y%m%d > "$LOG_DIR/auto-agente-plomero-last-run-day"
