#!/bin/bash
# ════════════════════════════════════════════════════════════════════════════
#  MODO MARATÓN — corre el Auto Agente en BUCLE hasta cumplir un tiempo:
#  una UNIDAD de trabajo por pasada (un arreglo, una mejora o UNA página nueva),
#  y al terminar una se pasa a la siguiente, hasta que se acabe el tiempo o se
#  quede sin trabajo bueno (anti-doorway: no fuerza páginas malas por llenar).
#  Cada pasada publica SOLA solo lo que pasa los candados (sin autorización humana).
#
#  Uso:  bash .pipeline/maraton.sh [segundos] [max_pasadas]
#        bash .pipeline/maraton.sh 3600 20    # 1 hora, máx 20 pasadas (default)
#        bash .pipeline/maraton.sh 600 2      # prueba corta
# ════════════════════════════════════════════════════════════════════════════
set -uo pipefail
export NODE_OPTIONS="--dns-result-order=ipv4first"   # IPv6 roto no tumba la corrida/correo
export PATH="/Users/openclaw/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"; mkdir -p "$LOG_DIR"
CODEX_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-codex.py"
if [ -n "${MARATON_CODEX:-}" ]; then
  CODEX_BIN="$MARATON_CODEX"  # override explícito para pruebas controladas
else
  CODEX_BIN=$(python3 "$CODEX_FINDER" 2>/dev/null || true)
fi
AUTH_CHECK="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/codex-login-preflight.py"
AUTH_TIMEOUT_SECONDS=30
NODE_FINDER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/encontrar-node.py"
NODE_BIN=$(python3 "$NODE_FINDER" 2>/dev/null || true)
DEADLINE_RUNNER="/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/ejecutar-hasta.py"
PASS_TIMEOUT_SECONDS=${MARATON_PASS_TIMEOUT_SECONDS:-1200}

DUR=${1:-3600}            # segundos (default 1 h)
MAX_PASS=${2:-20}         # tope duro de pasadas
STAMP0=$(date +%Y%m%d-%H%M%S)
MLOG="$LOG_DIR/maraton-$STAMP0.log"

# Lock COMPARTIDO con el pipeline diario (mismo nombre): nunca dos a la vez sobre el repo.
# Resistente a cuelgues: roba el lock si el dueño ya murió.
LOCK_DIR="/tmp/plomero-mantener-sitio.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  OLDPID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "")
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "[$(date)] Ya hay una corrida activa (pid $OLDPID); salgo." | tee -a "$MLOG"; exit 0
  fi
  # Lock sin pid pero recién creado = otra corrida arrancando (ventana mkdir→pid); no robar.
  if [ -z "$OLDPID" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0) ))
    [ "$LOCK_AGE" -lt 120 ] && { echo "[$(date)] Lock sin pid recién creado; salgo." | tee -a "$MLOG"; exit 0; }
  fi
  # Robo ATÓMICO vía mv (solo un proceso se lo lleva; evita el doble robo simultáneo).
  if mv "$LOCK_DIR" "$LOCK_DIR.stale.$$" 2>/dev/null; then
    rm -rf "$LOCK_DIR.stale.$$"
  else
    echo "[$(date)] Otro proceso robó el lock primero; salgo." | tee -a "$MLOG"; exit 0
  fi
  mkdir "$LOCK_DIR" 2>/dev/null || { echo "No tomé el lock; salgo." | tee -a "$MLOG"; exit 0; }
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT
RUN_START=$(date +%s)   # para atribuir el consumo de cuota del maratón al ledger

# Espera a que ChatGPT sea alcanzable (NordVPN puede estar reconectando y
# bloqueando la salida con el kill switch). Devuelve 0 si vuelve la red, 1 si no en ~8 min.
wait_for_net() {
  local i
  for i in $(seq 1 32); do
    if curl -sS -o /dev/null --max-time 6 https://chatgpt.com/ 2>/dev/null; then return 0; fi
    echo "[$(date)] red caída (¿NordVPN reconectando?); espero 15s ($i/32)…" >> "$MLOG"
    sleep 15
  done
  return 1
}

END=$(( $(date +%s) + DUR ))
PASS=0; DRY=0; HECHAS=0
echo "[$(date)] === MARATÓN inicio · dura ${DUR}s · máx ${MAX_PASS} pasadas ===" | tee -a "$MLOG"

if [ -z "$NODE_BIN" ] || [ ! -x "$NODE_BIN" ]; then
  echo "[$(date)] Node no está instalado; maratón cancelado porque los MCP no pueden iniciar." | tee -a "$MLOG"
  exit 0
fi
if [ -z "$CODEX_BIN" ] || [ ! -x "$CODEX_BIN" ]; then
  echo "[$(date)] No encontré un ejecutable de Codex; maratón cancelado." | tee -a "$MLOG"
  "$NODE_BIN" /Users/openclaw/gsc-mcp/send-report.mjs "$MLOG" "Plomero Culiacán (MARATÓN)" "no inició" >> "$MLOG" 2>&1 || true
  exit 0
fi
AUTH_RC=0
python3 "$AUTH_CHECK" "$CODEX_BIN" "$AUTH_TIMEOUT_SECONDS" >> "$MLOG" 2>&1 || AUTH_RC=$?
if [ "$AUTH_RC" -ne 0 ]; then
  if [ "$AUTH_RC" -eq 124 ]; then
    echo "[$(date)] El preflight de Codex excedió ${AUTH_TIMEOUT_SECONDS}s; maratón cancelado y lock liberado." | tee -a "$MLOG"
  else
    echo "[$(date)] Codex no está autenticado; maratón cancelado." | tee -a "$MLOG"
  fi
  "$NODE_BIN" /Users/openclaw/gsc-mcp/send-report.mjs "$MLOG" "Plomero Culiacán (MARATÓN)" "no inició" >> "$MLOG" 2>&1 || true
  exit 0
fi

while [ "$(date +%s)" -lt "$END" ] && [ "$PASS" -lt "$MAX_PASS" ]; do
  PASS=$((PASS+1)); ST=$(date +%Y%m%d-%H%M%S)
  PLOG="$LOG_DIR/maraton-pasada-$ST.log"
  LAST_FILE="/tmp/plomero-maraton-last-$ST.txt"
  REST=$(( END - $(date +%s) ))
  echo "[$(date)] --- pasada $PASS (quedan ${REST}s) -> $PLOG" | tee -a "$MLOG"

  # Resiliencia a NordVPN: no quemar una unidad si la red está caída; espera a que vuelva.
  if ! wait_for_net; then
    echo "[$(date)] la red no volvió tras ~8 min -> termino el maratón (el catch-up/diario lo retoma)." | tee -a "$MLOG"
    break
  fi

  # El tiempo de red también consume el presupuesto. Nunca iniciar una pasada nueva
  # si el maratón ya venció; cada pasada tiene además un máximo de 20 minutos.
  PASS_START=$(date +%s)
  if [ "$PASS_START" -ge "$END" ]; then
    echo "[$(date)] terminó el tiempo del maratón durante la espera de red; no inicio otra pasada." | tee -a "$MLOG"
    break
  fi
  PASS_DEADLINE=$((PASS_START + PASS_TIMEOUT_SECONDS))
  [ "$PASS_DEADLINE" -gt "$END" ] && PASS_DEADLINE="$END"

  # Codex aislado: SOLO GSC + local-seo, sin integraciones globales del usuario.
  PASS_RC=0
  python3 "$DEADLINE_RUNNER" "$PASS_DEADLINE" "$CODEX_BIN" exec \
    --cd "/Users/openclaw/Sitios Web/Plomero Culiacán" \
    --approve-for-me --ephemeral --ignore-user-config --strict-config --json \
    -c sandbox_workspace_write.network_access=true \
    -c "mcp_servers.gsc.command=\"$NODE_BIN\"" \
    -c 'mcp_servers.gsc.args=["/Users/openclaw/gsc-mcp/server.js"]' \
    -c "mcp_servers.local-seo.command=\"$NODE_BIN\"" \
    -c 'mcp_servers.local-seo.args=["/Users/openclaw/Sitios Web/Plomero Culiacán/mcp-local-seo/index.js"]' \
    -c 'mcp_servers.local-seo.cwd="/Users/openclaw/Sitios Web/Plomero Culiacán"' \
    --output-last-message "$LAST_FILE" - < .pipeline/maraton-prompt.txt >> "$PLOG" 2>&1 \
    || PASS_RC=$?
  if [ "$PASS_RC" -eq 124 ]; then
    echo "[$(date)] pasada $PASS cortada por deadline; Codex y sus procesos hijos fueron terminados." | tee -a "$MLOG"
  elif [ "$PASS_RC" -ne 0 ]; then
    echo "[$(date)] pasada $PASS terminó con código $PASS_RC." | tee -a "$MLOG"
  fi
  grep '"type":"turn.completed"' "$PLOG" >> "$MLOG" 2>/dev/null || true

  LAST=$(grep -E '^(HECHO|SIN TRABAJO):' "$LAST_FILE" 2>/dev/null | tail -1)
  echo "    -> ${LAST:-(sin línea de cierre — pasada incompleta)}" | tee -a "$MLOG"
  if echo "$LAST" | grep -q '^SIN TRABAJO'; then
    DRY=$((DRY+1))
  elif [ -z "$LAST" ]; then
    # Pasada SIN línea de cierre (Codex falló) cuenta como seca: antes reseteaba
    # DRY=0 y un CLI roto quemaba las 20 pasadas sin que el corte "2 secas" actuara.
    DRY=$((DRY+1))
  else
    DRY=0; HECHAS=$((HECHAS+1))
  fi
  if [ "$DRY" -ge 2 ]; then
    echo "[$(date)] 2 pasadas SIN TRABAJO seguidas -> fin anticipado (sin huecos buenos que hacer)." | tee -a "$MLOG"
    break
  fi
done

echo "[$(date)] === MARATÓN fin · ${PASS} pasada(s) · ${HECHAS} unidad(es) hecha(s) ===" | tee -a "$MLOG"
# Registro de consumo de cuota en el ledger (antes el maratón era invisible para
# costos.jsonl y para el tripwire de check-costos.py).
"$NODE_BIN" "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/registrar-costo.mjs" \
  "$MLOG" "$RUN_START" \
  "/Users/openclaw/Sitios Web/Plomero Culiacán/.pipeline/costos.jsonl" "maraton $STAMP0" >> "$MLOG" 2>&1 \
  || echo "[$(date)] No pude registrar el consumo del maratón (sigo)." >> "$MLOG"
# Correo resumen del maratón (mismo IPv4 fix; no bloquea si falla)
"$NODE_BIN" /Users/openclaw/gsc-mcp/send-report.mjs "$MLOG" "Plomero Culiacán (MARATÓN)" "maratón" >> "$MLOG" 2>&1 || true
