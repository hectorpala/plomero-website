#!/bin/bash
set -euo pipefail

# ════════════════════════════════════════════════════════════════════════════
#  AUTO AGENTE PLOMERO — corrida diaria autónoma (todo el sistema junto):
#  CORRIGE errores (mecánicos + humanos) · CRECE +3 páginas/día según GSC ·
#  VERIFICA que todo quedó bien · APRENDE cada error · publica solo si pasa candados.
#  Reemplaza a mantener-diario.sh (lo incluye y le suma crecimiento, verificación y aprendizaje).
# ════════════════════════════════════════════════════════════════════════════

# Forzar IPv4: si IPv6 está roto en la red, node (MCP + send-report) falla
# (EHOSTUNREACH). Preferir IPv4 evita que se caigan la corrida y el correo.
export NODE_OPTIONS="--dns-result-order=ipv4first"
export PATH="/Users/openclaw/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

# Chrome para los checkers headless (perf, e2e, producción, tracking). Puppeteer 21 espera
# Chrome 121 y su caché local tiene otra versión, así que sin esta ruta explícita el lanzamiento
# falla ("Failed to launch the browser process") y el checker se reporta como verificación
# CIEGA. Se exporta aquí para que la hereden todos los pasos de la corrida.
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
fi

cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
CODEX_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-codex.py"
CODEX_BIN=$(python3 "$CODEX_FINDER" 2>/dev/null || true)
NODE_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-node.py"
NODE_BIN=$(python3 "$NODE_FINDER" 2>/dev/null || true)
AUTH_CHECK="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/codex-login-preflight.py"
AUTH_TIMEOUT_SECONDS=30

# Los pasos auxiliares no deben intentar ejecutar una cadena vacía si Node falta.
# El preflight aborta Codex; esta función deja además una salida controlada para costo/correo.
run_node() {
  [ -n "$NODE_BIN" ] && [ -x "$NODE_BIN" ] || return 127
  "$NODE_BIN" "$@"
}
# Log NAMESPACEADO por proyecto: el Electricista escribe en el MISMO LOG_DIR con el
# mismo prefijo "auto-agente-*"; catchup.sh y check-infra.mjs miran "el log más nuevo"
# y veían el del otro sitio → el plomero muerto pasaba por vivo (auditoría 2026-07-07).
LOG="$LOG_DIR/auto-agente-plomero-$STAMP.log"
NO_RETRY_DAY_FILE="$LOG_DIR/auto-agente-plomero-no-retry-day"

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
# visto en auto-agente-launchd.err.log) chocaría con la FASE 1. La limpieza valida
# puerto + comando + cwd: nunca debe matar el servidor 8080 de otro proyecto.
python3 .pipeline/limpiar-servidor-local.py "$PWD" 8080 /tmp/plomero-http-server.pid >> "$LOG" 2>&1 \
  || echo "[$STAMP] No pude comprobar el servidor local huérfano; continúo y FASE 1 validará el puerto." >> "$LOG"

# Guard "ya corrió hoy": si una corrida YA terminó OK hoy (marca datada), no repetir — evita el
# doble cuando un disparo MANUAL coincide con el job programado de las 18:25. Una corrida FALLIDA
# NO deja marca, así que la de las 18:25 sí la recupera (no rompe el recovery).
# Forzar una corrida extra a propósito:  FORCE_RUN=1 bash .pipeline/crecer-diario.sh
TODAY=$(date +%Y%m%d)
if [ "${FORCE_RUN:-0}" != "1" ] && [ "$(cat "$LOG_DIR/auto-agente-plomero-last-run-day" 2>/dev/null || echo "")" = "$TODAY" ]; then
  echo "[$STAMP] Ya hubo una corrida exitosa hoy ($TODAY); no repito (FORCE_RUN=1 para forzar)." >> "$LOG"
  exit 0
fi
if [ "${FORCE_RUN:-0}" != "1" ] && [ "$(cat "$NO_RETRY_DAY_FILE" 2>/dev/null || echo "")" = "$TODAY" ]; then
  echo "[$STAMP] Hoy quedó una publicación posible/no verificable; no repito para evitar duplicarla (FORCE_RUN=1 para forzar)." >> "$LOG"
  exit 0
fi

# Corrida autónoma del sistema completo con Codex. El prompt orquesta las 10 fases.
RUN_START=$(date +%s)   # para atribuir el consumo de ESTA corrida
# Deadline de RELOJ DE PARED para los reintentos. `sleep` se pausa cuando la Mac
# duerme; sin este límite, un backoff de 2–4 minutos puede despertar horas después
# y competir con la corrida siguiente. El intento activo conserva su timeout propio.
RETRY_DEADLINE=$((RUN_START + 3 * 3600))

# ── Clasificación de errores (NO confundir red con cuota) ────────────────────
# TRANSITORIO = se cayó la conexión / el servidor falló a media respuesta. Se REINTENTA:
#   no perdimos cuota, solo se cortó el stream (el caso del 2026-06-24: "Connection closed mid-response").
# LIMITE = de verdad se agotó el uso del plan. NO se reintenta (sería inútil hasta que reinicie la cuota).
# El match se hace SOLO sobre lo que imprimió ESE intento (por offset de bytes), así la línea de
# estadística "📊 Uso de la corrida (cuota de suscripción)" —que se anexa DESPUÉS— nunca cuenta como motivo.
TRANSIENT_RE='Connection closed mid-response|API Error|Connection error|overloaded|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|fetch failed|socket hang up|terminated|Internal server error|HTTP 5[0-9][0-9]|\b5(00|02|03|29)\b|may be incomplete'
LIMIT_RE='session limit|usage limit|hit your (usage|limit)|rate limit|límite de uso|quota exceeded|resets? at|your limit will reset'
# PERMANENTE = error de configuración/acceso que NO se cura reintentando.
PERM_RE='disabled|invalid.*api.*key|unauthorized|forbidden|revoked|suspended|billing|not logged in|login required|authentication'

# Busca SOLO dentro de la salida del intento actual, sin cargar el JSONL completo en una
# variable de shell. Una corrida grande puede producir cientos de MB; almacenarla entera
# para buscar una marca podía agotar memoria justo después de que Codex terminara bien.
attempt_has_fixed() {
  local rc
  set +o pipefail
  tail -c "+$((OFF + 1))" "$LOG" 2>/dev/null | grep -qF -- "$1"
  rc=${PIPESTATUS[1]}
  set -o pipefail
  return "$rc"
}

attempt_has_regex() {
  local rc
  set +o pipefail
  tail -c "+$((OFF + 1))" "$LOG" 2>/dev/null | grep -qiE -- "$1"
  rc=${PIPESTATUS[1]}
  set -o pipefail
  return "$rc"
}

# Espera a que ChatGPT vuelva antes de cada intento. NordVPN (kill switch) puede
# bloquear la salida al reconectar; solo un error de RED hace fallar curl.
wait_for_net() {
  local i
  for i in $(seq 1 32); do
    curl -sS -o /dev/null --max-time 6 https://chatgpt.com/ 2>/dev/null && return 0
    echo "[$STAMP] red caída (¿NordVPN reconectando?); espero 15s ($i/32)…" >> "$LOG"
    sleep 15
  done
  return 1
}

MAX_ATTEMPTS=3
CODEX_OK=0
FAIL_KIND=""          # transitorio | limite | desconocido
TIMEOUT_MIN=90
PUBLICATION_STATE="sin_ejecucion"
PROTECT_TODAY=0
PUB_CHECK="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/detectar-publicacion.py"
LOCAL_MAIN_BEFORE=$(git rev-parse refs/heads/main 2>/dev/null || echo "")
REMOTE_MAIN_BEFORE=$(python3 "$PUB_CHECK" baseline 2>/dev/null || echo "")

# Solo autoriza un reintento si GitHub Y la main local siguen exactamente como al inicio.
# Cualquier cambio o imposibilidad de consultar el remoto falla cerrado: repetir toda la
# corrida podría volver a publicar algo que alcanzó a subir antes de cortarse el stream.
check_publication_before_retry() {
  local out rc
  if out=$(python3 "$PUB_CHECK" check \
      --remote-antes "$REMOTE_MAIN_BEFORE" --local-antes "$LOCAL_MAIN_BEFORE" 2>&1); then
    PUBLICATION_STATE="no_detectada"
    echo "[$STAMP] idempotencia: $out" >> "$LOG"
    return 0
  else
    rc=$?
  fi
  echo "[$STAMP] idempotencia: $out" >> "$LOG"
  case "$rc" in
    10) PUBLICATION_STATE="origin_cambio"; FAIL_KIND="publicacion_detectada" ;;
    11) PUBLICATION_STATE="main_local_cambio"; FAIL_KIND="main_local_modificada" ;;
    *)  PUBLICATION_STATE="no_verificable"; FAIL_KIND="publicacion_no_verificable" ;;
  esac
  PROTECT_TODAY=1
  return 1
}

if [ -z "$NODE_BIN" ] || [ ! -x "$NODE_BIN" ]; then
  FAIL_KIND="permanente"
  echo "[$STAMP] No encontré un ejecutable de Node; MCP, costos y reportes no pueden iniciar." >> "$LOG"
elif [ -z "$CODEX_BIN" ] || [ ! -x "$CODEX_BIN" ]; then
  FAIL_KIND="permanente"
  echo "[$STAMP] No encontré el binario de Codex CLI; la corrida no puede iniciar." >> "$LOG"
elif python3 "$AUTH_CHECK" "$CODEX_BIN" "$AUTH_TIMEOUT_SECONDS" >> "$LOG" 2>&1; then
  : # autenticación presente
else
  AUTH_RC=$?
  FAIL_KIND="permanente"
  if [ "$AUTH_RC" -eq 124 ]; then
    echo "[$STAMP] El preflight de autenticación de Codex excedió ${AUTH_TIMEOUT_SECONDS}s; aborto para liberar el lock." >> "$LOG"
  else
    echo "[$STAMP] Codex CLI no está autenticado; ejecuta 'codex login'." >> "$LOG"
  fi
fi

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  [ -z "$FAIL_KIND" ] || break
  echo "[$STAMP] >>> intento $attempt/$MAX_ATTEMPTS de la corrida @ $(date +%H:%M:%S)" >> "$LOG"
  OFF=$(wc -c < "$LOG")   # byte-offset: leeremos SOLO lo que agregue este intento
  wait_for_net || echo "[$STAMP] red no volvió tras ~8 min; intento igual (puede fallar)." >> "$LOG"
  # TIMEOUT DURO: el prompt ordena MINUTOS_MAX=35 pero nada lo imponía — 3 corridas
  # desbocadas históricas de 600-654M tokens (~$1,300-1,420 equiv-API c/u). 90 min de
  # tope da holgura para días pesados y corta lo desbocado el MISMO día, no al siguiente.
  # Configuración aislada: ignora integraciones globales y carga SOLO GSC + local-seo.
  # --approve-for-me conserva autonomía dentro del sandbox workspace-write; nunca desactiva el sandbox.
  ATTEMPT_DEADLINE=$(( $(date +%s) + TIMEOUT_MIN * 60 ))
  "$CODEX_BIN" exec --cd "/Users/openclaw/Sitios Web/Plomero Culiacán" \
    --approve-for-me --ephemeral --ignore-user-config --strict-config \
    --json \
    -c agents.enabled=false \
    -c sandbox_workspace_write.network_access=true \
    -c "mcp_servers.gsc.command=\"$NODE_BIN\"" \
    -c 'mcp_servers.gsc.args=["/Users/openclaw/gsc-mcp/server.js"]' \
    -c "mcp_servers.local-seo.command=\"$NODE_BIN\"" \
    -c 'mcp_servers.local-seo.args=["/Users/openclaw/Sitios Web/Plomero Culiacán/mcp-local-seo/index.js"]' \
    -c 'mcp_servers.local-seo.cwd="/Users/openclaw/Sitios Web/Plomero Culiacán"' \
    - < .pipeline/crecer-diario-prompt.txt >> "$LOG" 2>&1 &
  CPID=$!
  # Watchdog de RELOJ DE PARED: `sleep 90m` se pausa durante el reposo y dejaba
  # revivir al día siguiente una corrida vieja. El sondeo corto compara epoch real.
  (
    while kill -0 "$CPID" 2>/dev/null; do
      if [ "$(date +%s)" -ge "$ATTEMPT_DEADLINE" ]; then
        echo "[$STAMP] TIMEOUT ${TIMEOUT_MIN}min: matando corrida desbocada (pid $CPID)." >> "$LOG"
        kill "$CPID" 2>/dev/null || true
        sleep 10
        kill -0 "$CPID" 2>/dev/null && kill -9 "$CPID" 2>/dev/null || true
        break
      fi
      sleep 15
    done
  ) &
  WPID=$!
  if wait "$CPID"; then
    kill "$WPID" 2>/dev/null || true
    wait "$WPID" 2>/dev/null || true
    # Una terminación por señal normalmente es !=0, pero no confiar en eso: si
    # el CLI maneja SIGTERM y sale 0, el marcador del watchdog sigue mandando.
    if attempt_has_fixed "TIMEOUT ${TIMEOUT_MIN}min"; then
      FAIL_KIND="timeout"
      echo "[$STAMP] Corrida cortada por timeout; NO se acepta como éxito." >> "$LOG"
      break
    fi
    # Código 0 sin turn.completed indica una salida incompleta del protocolo JSONL.
    if ! attempt_has_fixed '"type":"turn.completed"'; then
      FAIL_KIND="incompleta"
      echo "[$STAMP] Codex salió con código 0 pero sin turn.completed; no cuenta como éxito." >> "$LOG"
      check_publication_before_retry || true
      break
    fi
    CODEX_OK=1; FAIL_KIND=""; break
  fi
  kill "$WPID" 2>/dev/null || true
  wait "$WPID" 2>/dev/null || true
  if ! check_publication_before_retry; then
    echo "[$STAMP] No reintento: no pude demostrar que el intento anterior terminó sin publicar." >> "$LOG"
    break
  fi
  if attempt_has_fixed "TIMEOUT ${TIMEOUT_MIN}min"; then
    FAIL_KIND="timeout"
    echo "[$STAMP] Corrida cortada por timeout; NO se reintenta (volvería a desbocarse)." >> "$LOG"
    break
  fi
  if attempt_has_regex "$LIMIT_RE"; then
    FAIL_KIND="limite"
    echo "[$STAMP] Falla por LÍMITE DE USO real del plan; no tiene caso reintentar." >> "$LOG"
    break
  fi
  if attempt_has_regex "$PERM_RE"; then
    FAIL_KIND="permanente"
    echo "[$STAMP] Error PERMANENTE de configuración/acceso; no tiene caso reintentar." >> "$LOG"
    break
  fi
  if attempt_has_regex "$TRANSIENT_RE"; then
    FAIL_KIND="transitorio"
  else
    FAIL_KIND="desconocido"
  fi
  if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
    WAIT=$((attempt * 120))   # backoff: 120s, luego 240s
    if [ "$(date +%s)" -gt "$RETRY_DEADLINE" ]; then
      FAIL_KIND="deadline_reintentos"
      echo "[$STAMP] Fuera de la ventana de reintentos (>3h desde el inicio); no inicio otro intento. El catch-up o la corrida de mañana lo recuperan." >> "$LOG"
      break
    fi
    echo "[$STAMP] Error $FAIL_KIND (NO de cuota); reintento en ${WAIT}s." >> "$LOG"
    sleep "$WAIT"
    # Comprobar DESPUÉS del sleep es indispensable: macOS pausa `sleep` durante
    # el reposo y puede reanudarlo muchas horas más tarde.
    if [ "$(date +%s)" -gt "$RETRY_DEADLINE" ]; then
      FAIL_KIND="deadline_reintentos"
      echo "[$STAMP] La Mac despertó fuera de la ventana de reintentos (>3h desde el inicio); abandono. El catch-up o la corrida de mañana lo recuperan." >> "$LOG"
      break
    fi
  else
    echo "[$STAMP] Agotados los $MAX_ATTEMPTS intentos; la corrida no completó." >> "$LOG"
  fi
done
[ "$CODEX_OK" = 1 ] || echo "[$STAMP] La corrida de Codex terminó con error ($FAIL_KIND); continúo para enviar el parte." >> "$LOG"

# Registro de consumo de la corrida Codex desde el JSONL de este log.
run_node "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/registrar-costo.mjs" \
  "$LOG" "$RUN_START" \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/costos.jsonl" "auto-agente $STAMP" >> "$LOG" 2>&1 \
  || echo "[$STAMP] No pude registrar el costo de la corrida (sigo)." >> "$LOG"

# Cuadre del parte (red de seguridad INDEPENDIENTE del LLM): verifica que el correo cuadre con los
# cambios reales (conteos del encabezado == ítems listados, y ninguna URL "arreglada" inventada).
# Si NO cuadra, antepone un AVISO automático al cuerpo del correo para que el humano SIEMPRE lo vea
# (el agente no puede esconder una discrepancia). No bloquea el envío.
PARTE="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ultima-corrida.md"

# CANDADO DE FRESCURA (independiente del LLM): el parte solo vale si lo escribió ESTA corrida.
# Si su fecha de modificación es anterior al arranque, la corrida murió antes de la FASE 10 y
# mandarlo sería un correo FALSO (caso 2026-07-26: llegó el parte del 25 diciendo "publicado"
# mientras el trabajo del 26 seguía sin commitear). En ese caso se degrada a corrida fallida.
if [ "${CODEX_OK:-0}" = 1 ]; then
  PARTE_MTIME=$(stat -f %m "$PARTE" 2>/dev/null || echo 0)
  if [ "$PARTE_MTIME" -lt "$RUN_START" ]; then
    echo "[$STAMP] El parte no se reescribió en esta corrida (mtime $PARTE_MTIME < inicio $RUN_START): la corrida no llegó a la FASE 10; NO mando el parte viejo." >> "$LOG"
    CODEX_OK=0; FAIL_KIND="incompleta"
  fi
fi

# Solo cuadrar un parte NUEVO y COMPLETO. Si Codex falló o el candado de frescura
# rechazó el archivo, tocar el parte viejo lo convertiría en un cambio local falso
# que la corrida siguiente podría adoptar o publicar por accidente.
if [ "${CODEX_OK:-0}" = 1 ] && [ -f "$PARTE" ]; then
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

# Parte por email. Si la corrida de Codex tuvo ÉXITO → parte nuevo. Si FALLÓ
# (cuota/error) → NO mandes el parte viejo (correo engañoso "encontré N" de otra corrida); aviso honesto.
if [ "${CODEX_OK:-0}" = 1 ]; then
  ETIQUETA="18:25 · Codex"
  run_node /Users/openclaw/gsc-mcp/send-report.mjs \
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
      SUGERENCIA="Revisa el inicio de sesión de Codex (`codex login status`); el agente no puede resolver credenciales solo." ;;
    timeout)
      MOTIVO="la corrida excedió el tope duro de tiempo y fue cortada (posible corrida desbocada)"
      SUGERENCIA="Revisa el log para ver en qué fase se atoró: $LOG" ;;
    deadline_reintentos)
      MOTIVO="la Mac despertó fuera de la ventana segura de reintentos (más de 3 horas desde el inicio)"
      SUGERENCIA="No requiere acción: se canceló el reintento atrasado para no cruzarlo con otra automatización; el catch-up o la corrida de mañana lo recuperan." ;;
    incompleta)
      MOTIVO="la corrida hizo trabajo pero NO llegó a terminarlo (se cortó en la revisión final, antes de publicar y de escribir el parte del día)"
      SUGERENCIA="El trabajo NO se perdió: quedó guardado en la rama de la corrida. La próxima corrida lo retoma. Log: $LOG" ;;
    publicacion_detectada)
      MOTIVO="origin/main CAMBIÓ durante el intento: la publicación pudo completarse antes de que se cortara la respuesta de Codex"
      SUGERENCIA="El sistema NO reintentó para evitar publicar dos veces. Revisa el último commit remoto y el log: $LOG" ;;
    main_local_modificada)
      MOTIVO="la main local cambió durante el intento, aunque origin/main no cambió; quedó una integración incompleta"
      SUGERENCIA="El sistema NO reintentó para no duplicar/mezclar la integración. Revisa la main local y la rama automática: $LOG" ;;
    publicacion_no_verificable)
      MOTIVO="no pude consultar origin/main después del fallo, así que no es seguro afirmar si el push ocurrió"
      SUGERENCIA="El sistema NO reintentó para evitar una publicación duplicada. Comprueba GitHub y revisa: $LOG" ;;
    *)
      MOTIVO="error no reconocido de la corrida"
      SUGERENCIA="Revisa el log: $LOG" ;;
  esac
  case "$PUBLICATION_STATE" in
    origin_cambio) PUBLICATION_NOTE="**Publicación:** origin/main cambió durante el intento; pudo haberse publicado. No se reintentó." ;;
    main_local_cambio) PUBLICATION_NOTE="**Publicación:** origin/main no cambió, pero main local sí; no se publicó al remoto y quedó una integración local." ;;
    no_detectada) PUBLICATION_NOTE="**Publicación:** comprobé origin/main y main local; no cambiaron durante el intento." ;;
    sin_ejecucion) PUBLICATION_NOTE="**Publicación:** Codex no llegó a iniciar; no hubo intento de publicación." ;;
    *) PUBLICATION_NOTE="**Publicación:** estado NO verificable; no afirmo que el push haya ocurrido ni que no haya ocurrido." ;;
  esac
  printf '# Auto Agente Plomero — corrida NO completada\n**Motivo:** %s.\n**Evidencia (del log):** `%s`\n**Qué sigue:** %s\n\n%s\n' \
    "$MOTIVO" "$ERRLINE" "$SUGERENCIA" "$PUBLICATION_NOTE" > "$FAILNOTE"
  # TRABAJO SIN PUBLICAR: si la corrida alcanzó a editar el sitio y murió antes de publicar, dilo
  # en el correo. Antes eso quedaba invisible y el trabajo huérfano se descubría días después
  # (rama del 07-23 rescatada hasta el 07-25; trabajo del 07-26 abandonado sin aviso).
  SUCIOS=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  RAMA_ACTUAL=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
  if [ "${SUCIOS:-0}" -gt 0 ] || [ "$RAMA_ACTUAL" != "main" ]; then
    printf '\n**Trabajo sin publicar:** quedaron %s archivo(s) con cambios en la rama `%s`. No se perdió nada; la próxima corrida lo retoma y lo verifica antes de publicar.\n' \
      "$SUCIOS" "$RAMA_ACTUAL" >> "$FAILNOTE"
  fi
  run_node /Users/openclaw/gsc-mcp/send-report.mjs \
    "$FAILNOTE" "Auto Agente Plomero" "no completada" >> "$LOG" 2>&1 \
    || echo "[$STAMP] No se pudo enviar el aviso de falla (Auto Agente Plomero)." >> "$LOG"
fi

# Marca que YA corrió hoy SOLO si la corrida de Codex tuvo éxito. Si falló, NO se
# marca → el catch-up sí podrá recuperarla hoy (si se marcara siempre, quedaría sin recuperar).
if [ "${CODEX_OK:-0}" = 1 ]; then
  date +%Y%m%d > "$LOG_DIR/auto-agente-plomero-last-run-day"
elif [ "${PROTECT_TODAY:-0}" = 1 ]; then
  # No llamarlo "éxito": es una barrera separada que evita que catch-up repita una
  # corrida cuyo estado remoto es posible o no verificable.
  date +%Y%m%d > "$NO_RETRY_DAY_FILE"
fi
# Sentinel del DRIVER, separado del stream JSONL de Codex. Su ausencia con el lock
# libre significa que el proceso murió abruptamente; catchup.sh debe recuperarlo en
# vez de confundir un log reciente pero truncado con una corrida sana.
if [ "${CODEX_OK:-0}" = 1 ]; then
  echo "[$STAMP] DRIVER_RESULT=success" >> "$LOG"
else
  echo "[$STAMP] DRIVER_RESULT=failure:${FAIL_KIND:-desconocido}" >> "$LOG"
fi
# Exit 0 explícito: antes el script salía con 1 en toda corrida fallida (el && de arriba
# como última línea) y launchctl mostraba status 1 sin distinguir "driver roto" de
# "corrida fallida ya notificada por email".
exit 0
