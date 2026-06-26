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

cd "/Users/openclaw/Sitios Web/Plomero Culiacán" || exit 1
LOG_DIR="$HOME/Library/Logs/mantener-sitio"; mkdir -p "$LOG_DIR"
RUTA_CLAUDE="/Users/openclaw/.npm-global/bin/claude"
CLAUDE_CMD="${MARATON_CLAUDE:-$RUTA_CLAUDE}"          # override para pruebas (stub)

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
  rm -rf "$LOCK_DIR"; mkdir "$LOCK_DIR" 2>/dev/null || { echo "No tomé el lock; salgo." | tee -a "$MLOG"; exit 0; }
fi
echo "$$" > "$LOCK_DIR/pid"
trap 'rm -rf "$LOCK_DIR"' EXIT

# Espera a que la API de Claude sea alcanzable (NordVPN puede estar reconectando y
# bloqueando la salida con el kill switch). Devuelve 0 si vuelve la red, 1 si no en ~8 min.
# curl a /v1/messages da HTTP 405 (exit 0 = conectó); solo error de RED da exit != 0.
wait_for_net() {
  local i
  for i in $(seq 1 32); do
    if curl -sS -o /dev/null --max-time 6 https://api.anthropic.com/v1/messages 2>/dev/null; then return 0; fi
    echo "[$(date)] red caída (¿NordVPN reconectando?); espero 15s ($i/32)…" >> "$MLOG"
    sleep 15
  done
  return 1
}

END=$(( $(date +%s) + DUR ))
PASS=0; DRY=0; HECHAS=0
echo "[$(date)] === MARATÓN inicio · dura ${DUR}s · máx ${MAX_PASS} pasadas ===" | tee -a "$MLOG"

while [ "$(date +%s)" -lt "$END" ] && [ "$PASS" -lt "$MAX_PASS" ]; do
  PASS=$((PASS+1)); ST=$(date +%Y%m%d-%H%M%S)
  PLOG="$LOG_DIR/maraton-pasada-$ST.log"
  REST=$(( END - $(date +%s) ))
  echo "[$(date)] --- pasada $PASS (quedan ${REST}s) -> $PLOG" | tee -a "$MLOG"

  # Resiliencia a NordVPN: no quemar una unidad si la red está caída; espera a que vuelva.
  if ! wait_for_net; then
    echo "[$(date)] la red no volvió tras ~8 min -> termino el maratón (el catch-up/diario lo retoma)." | tee -a "$MLOG"
    break
  fi

  "$CLAUDE_CMD" --permission-mode auto -p "$(cat .pipeline/maraton-prompt.txt)" >> "$PLOG" 2>&1 || true

  LAST=$(grep -E '^(HECHO|SIN TRABAJO):' "$PLOG" | tail -1)
  echo "    -> ${LAST:-(sin línea de cierre — pasada incompleta)}" | tee -a "$MLOG"
  if echo "$LAST" | grep -q '^SIN TRABAJO'; then
    DRY=$((DRY+1))
  else
    DRY=0; [ -n "$LAST" ] && HECHAS=$((HECHAS+1))
  fi
  if [ "$DRY" -ge 2 ]; then
    echo "[$(date)] 2 pasadas SIN TRABAJO seguidas -> fin anticipado (sin huecos buenos que hacer)." | tee -a "$MLOG"
    break
  fi
done

echo "[$(date)] === MARATÓN fin · ${PASS} pasada(s) · ${HECHAS} unidad(es) hecha(s) ===" | tee -a "$MLOG"
# Correo resumen del maratón (mismo IPv4 fix; no bloquea si falla)
/usr/local/bin/node /Users/openclaw/gsc-mcp/send-report.mjs "$MLOG" "Plomero Culiacán (MARATÓN)" "maratón" >> "$MLOG" 2>&1 || true
