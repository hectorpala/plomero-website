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
# Log NAMESPACEADO por proyecto: el Electricista escribe en el MISMO LOG_DIR con el
# mismo prefijo "auto-agente-*"; catchup.sh y check-infra.mjs miran "el log más nuevo"
# y veían el del otro sitio → el plomero muerto pasaba por vivo (auditoría 2026-07-07).
LOG="$LOG_DIR/auto-agente-plomero-$STAMP.log"

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
  # Lock sin pid: puede ser un lock RECIÉN creado (ventana mkdir→echo-pid de otro proceso).
  # Solo se considera huérfano si además tiene >2 min de edad.
  if [ -z "$OLDPID" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0) ))
    if [ "$LOCK_AGE" -lt 120 ]; then
      echo "[$STAMP] Lock sin pid pero recién creado (${LOCK_AGE}s); asumo corrida arrancando y salgo." >> "$LOG"
      exit 0
    fi
  fi
  # Robo ATÓMICO: el mv solo se lo lleva UN proceso; el perdedor sale en vez de
  # borrar el lock que el ganador acaba de crear (carrera de doble robo).
  if mv "$LOCK_DIR" "$LOCK_DIR.stale.$$" 2>/dev/null; then
    echo "[$STAMP] Lock huérfano (pid '$OLDPID' ya no vive) -> lo robo y continúo." >> "$LOG"
    rm -rf "$LOCK_DIR.stale.$$"
  else
    echo "[$STAMP] Otro proceso robó el lock primero; saliendo." >> "$LOG"
    exit 0
  fi
  mkdir "$LOCK_DIR" 2>/dev/null || { echo "[$STAMP] No pude tomar el lock; saliendo." >> "$LOG"; exit 0; }
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT

# Server local :8080 huérfano de una corrida anterior muerta a medias (SIGKILL real
# visto en auto-agente-launchd.err.log) chocaría con la FASE 1 → limpieza defensiva.
pkill -f "http.server 8080" 2>/dev/null || true

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
# PERMANENTE = error de configuración/acceso que NO se cura reintentando (caso 2026-07-06:
# "Your organization has disabled Claude subscription access" → 3 reintentos inútiles, ~45 min).
PERM_RE='disabled|invalid.*api.*key|unauthorized|forbidden|revoked|suspended|billing'

# Espera a que la API de Claude vuelva antes de cada intento. NordVPN (kill switch)
# bloquea la salida al reconectar; sin esto, el intento se quema de inmediato (caso 06-25:
# 3 intentos fallaron por red caída, no por cuota). curl a /v1/messages da HTTP 405
# (exit 0 = conectó); solo un error de RED da exit != 0.
wait_for_net() {
  local i
  for i in $(seq 1 32); do
    curl -sS -o /dev/null --max-time 6 https://api.anthropic.com/v1/messages 2>/dev/null && return 0
    echo "[$STAMP] red caída (¿NordVPN reconectando?); espero 15s ($i/32)…" >> "$LOG"
    sleep 15
  done
  return 1
}

MAX_ATTEMPTS=3
CLAUDE_OK=0
FAIL_KIND=""          # transitorio | limite | desconocido
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "[$STAMP] >>> intento $attempt/$MAX_ATTEMPTS de la corrida @ $(date +%H:%M:%S)" >> "$LOG"
  OFF=$(wc -c < "$LOG")   # byte-offset: leeremos SOLO lo que agregue este intento
  wait_for_net || echo "[$STAMP] red no volvió tras ~8 min; intento igual (puede fallar)." >> "$LOG"
  # Orquestador en SONNET (~5x más barato; el gasto es 67% releer contexto). Los agentes
  # de juicio crítico (revisor-contenido/critico-completitud/decisor-negocio/fixer-autonomo)
  # declaran model:opus en su frontmatter -> NO se degradan. Ver MODELO-ROUTING.md.
  # TIMEOUT DURO: el prompt ordena MINUTOS_MAX=35 pero nada lo imponía — 3 corridas
  # desbocadas históricas de 600-654M tokens (~$1,300-1,420 equiv-API c/u). 90 min de
  # tope da holgura para días pesados y corta lo desbocado el MISMO día, no al siguiente.
  TIMEOUT_MIN=90
  # --strict-mcp-config con .pipeline/mcp-run.json (gsc + local-seo): SOLO los MCP que la
  # corrida necesita. Sin esto cargaba TODOS los del usuario (tradingview, facebook-ads
  # con ESCRITURA…) en un agente autónomo sin humano (hallazgo del port al electricista).
  "$RUTA_CLAUDE" --model sonnet --permission-mode auto --mcp-config .pipeline/mcp-run.json --strict-mcp-config -p "$(cat .pipeline/crecer-diario-prompt.txt)" >> "$LOG" 2>&1 &
  CPID=$!
  ( sleep $((TIMEOUT_MIN * 60))
    if kill -0 "$CPID" 2>/dev/null; then
      echo "[$STAMP] TIMEOUT ${TIMEOUT_MIN}min: matando corrida desbocada (pid $CPID)." >> "$LOG"
      kill "$CPID" 2>/dev/null; sleep 10; kill -9 "$CPID" 2>/dev/null
    fi ) &
  WPID=$!
  if wait "$CPID"; then
    kill "$WPID" 2>/dev/null || true
    CLAUDE_OK=1; FAIL_KIND=""; break
  fi
  kill "$WPID" 2>/dev/null || true
  TAIL=$(tail -c "+$((OFF + 1))" "$LOG" 2>/dev/null || echo "")
  if printf '%s' "$TAIL" | grep -q "TIMEOUT ${TIMEOUT_MIN}min"; then
    FAIL_KIND="timeout"
    echo "[$STAMP] Corrida cortada por timeout; NO se reintenta (volvería a desbocarse)." >> "$LOG"
    break
  fi
  if printf '%s' "$TAIL" | grep -qiE "$LIMIT_RE"; then
    FAIL_KIND="limite"
    echo "[$STAMP] Falla por LÍMITE DE USO real del plan; no tiene caso reintentar." >> "$LOG"
    break
  fi
  if printf '%s' "$TAIL" | grep -qiE "$PERM_RE"; then
    FAIL_KIND="permanente"
    echo "[$STAMP] Error PERMANENTE de configuración/acceso; no tiene caso reintentar." >> "$LOG"
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

# ── RESPALDO CODEX (solo falla por CUOTA): la corrida del día la intenta Codex CLI, que
# gasta cuota de ChatGPT (independiente de la de Claude). Alcance REDUCIDO a mantenimiento
# determinista (checkers + auto-fixers + candados), SIN crecimiento ni cambios de contenido
# — Codex no tiene los subagentes Task ni el MCP de GSC. Prompt: .pipeline/respaldo-codex-prompt.txt
CODEX_OK=0
CODEX_TRIED=0
if [ "$CLAUDE_OK" != 1 ] && [ "$FAIL_KIND" = "limite" ]; then
  # Binario: el CLI suelto si existe; si no, el que trae la extensión de VS Code de Codex
  # (su ruta cambia con cada update de la extensión → se resuelve al vuelo, la más nueva).
  CODEX_BIN=$(command -v codex 2>/dev/null || true)
  if [ -z "$CODEX_BIN" ]; then
    CODEX_BIN=$(ls -t "$HOME"/.vscode/extensions/openai.chatgpt-*/bin/macos-aarch64/codex 2>/dev/null | head -1 || true)
  fi
  if [ -n "$CODEX_BIN" ] && [ -x "$CODEX_BIN" ]; then
    CODEX_TRIED=1
    echo "[$STAMP] >>> RESPALDO CODEX: cuota de Claude agotada; mantenimiento reducido con $("$CODEX_BIN" --version 2>/dev/null | head -1)." >> "$LOG"
    # Sandbox workspace-write + red habilitada: puede editar el repo y hacer git push, pero
    # no escribir fuera del workspace. Mismo timeout duro que la corrida normal.
    "$CODEX_BIN" exec --cd "/Users/openclaw/Sitios Web/Plomero Culiacán" \
      --sandbox workspace-write -c sandbox_workspace_write.network_access=true \
      "$(cat .pipeline/respaldo-codex-prompt.txt)" >> "$LOG" 2>&1 &
    CPID=$!
    ( sleep $((TIMEOUT_MIN * 60))
      if kill -0 "$CPID" 2>/dev/null; then
        echo "[$STAMP] TIMEOUT ${TIMEOUT_MIN}min del respaldo Codex: lo mato (pid $CPID)." >> "$LOG"
        kill "$CPID" 2>/dev/null; sleep 10; kill -9 "$CPID" 2>/dev/null
      fi ) &
    WPID=$!
    if wait "$CPID"; then
      CODEX_OK=1
      echo "[$STAMP] Respaldo Codex terminó OK; el parte del día sale de esta corrida." >> "$LOG"
    else
      echo "[$STAMP] El respaldo con Codex TAMBIÉN falló; se manda el aviso de falla normal." >> "$LOG"
    fi
    kill "$WPID" 2>/dev/null || true
  else
    echo "[$STAMP] Cuota agotada y NO encontré el binario de codex (CLI ni extensión VS Code); sin respaldo." >> "$LOG"
  fi
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

# Parte por email. Si la corrida tuvo ÉXITO (Claude o respaldo Codex) → parte nuevo. Si FALLÓ
# (cuota/error) → NO mandes el parte viejo (correo engañoso "encontré N" de otra corrida); aviso honesto.
if [ "${CLAUDE_OK:-0}" = 1 ] || [ "${CODEX_OK:-0}" = 1 ]; then
  ETIQUETA="18:25"
  [ "${CODEX_OK:-0}" = 1 ] && ETIQUETA="18:25 · respaldo Codex"
  /usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
    "$PARTE" \
    "Auto Agente Plomero" "$ETIQUETA" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el email del parte (Auto Agente Plomero)." >> "$LOG"
else
  FAILNOTE="$LOG_DIR/fail-$STAMP.md"
  # Motivo HONESTO según el tipo de falla (no asumir cuota). La línea de evidencia se saca del
  # log EXCLUYENDO la estadística "📊 Uso ... (cuota de suscripción)" para no volver a confundirla con un error.
  # El "|| true" es VITAL: con set -eo pipefail, un grep sin match (exit 1) mataba el
  # script AQUÍ y el aviso de falla nunca se enviaba — exactamente en el caso
  # "desconocido", donde más importa avisar (así murió en silencio el 2026-07-06).
  ERRLINE=$(grep -iE "$TRANSIENT_RE|$LIMIT_RE|$PERM_RE" "$LOG" 2>/dev/null | grep -viE '📊 Uso|cuota de suscripción|equiv-API' | head -1 | sed 's/^[[:space:]]*//' || true)
  [ -n "$ERRLINE" ] || ERRLINE="(sin línea de error reconocible; revisa el log completo)"
  case "$FAIL_KIND" in
    transitorio)
      MOTIVO="se cayó la conexión con el servidor a media respuesta — error TRANSITORIO de red, NO de cuota (corrió con tu plan, no se facturó nada)"
      SUGERENCIA="El sistema ya reintentó $MAX_ATTEMPTS veces sin éxito. No requiere acción: el catch-up o la corrida de mañana lo recuperan." ;;
    limite)
      MOTIVO="se alcanzó el límite de uso del plan"
      SUGERENCIA="Reintenta cuando se restablezca la cuota." ;;
    permanente)
      MOTIVO="error PERMANENTE de configuración/acceso (p.ej. suscripción deshabilitada o credencial inválida) — reintentar no ayuda"
      SUGERENCIA="Revisa la suscripción/credenciales de Claude; el agente no puede resolver esto solo." ;;
    timeout)
      MOTIVO="la corrida excedió el tope duro de tiempo y fue cortada (posible corrida desbocada)"
      SUGERENCIA="Revisa el log para ver en qué fase se atoró: $LOG" ;;
    *)
      MOTIVO="error no reconocido de la corrida"
      SUGERENCIA="Revisa el log: $LOG" ;;
  esac
  printf '# Auto Agente Plomero — corrida NO completada\n**Motivo:** %s.\n**Evidencia (del log):** `%s`\n**Qué sigue:** %s\n\nNo se hizo ni publicó ningún cambio en esta corrida.\n' \
    "$MOTIVO" "$ERRLINE" "$SUGERENCIA" > "$FAILNOTE"
  # Si además se intentó el respaldo con Codex y también murió, que el correo lo diga.
  [ "${CODEX_TRIED:-0}" = 1 ] && printf '\n**Respaldo Codex:** también se intentó la corrida con Codex CLI y falló; revisa el log: %s\n' "$LOG" >> "$FAILNOTE"
  /usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs \
    "$FAILNOTE" "Auto Agente Plomero" "no completada" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el aviso de falla (Auto Agente Plomero)." >> "$LOG"
fi

# Marca que YA corrió hoy SOLO si la corrida tuvo éxito (Claude o respaldo Codex). Si falló, NO se
# marca → el catch-up sí podrá recuperarla hoy (si se marcara siempre, quedaría sin recuperar).
if [ "${CLAUDE_OK:-0}" = 1 ] || [ "${CODEX_OK:-0}" = 1 ]; then
  date +%Y%m%d > "$LOG_DIR/auto-agente-plomero-last-run-day"
fi
# Exit 0 explícito: antes el script salía con 1 en toda corrida fallida (el && de arriba
# como última línea) y launchctl mostraba status 1 sin distinguir "driver roto" de
# "corrida fallida ya notificada por email".
exit 0
