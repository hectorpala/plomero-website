#!/usr/bin/env bash
URL="https://plomeroculiacanpro.mx/"  # cámbiala a tu web real
DIR="$(cd "$(dirname "$0")" && pwd)"
LOGDIR="$DIR/logs"
mkdir -p "$LOGDIR"
STAMP=$(date +%F-%H%M)

run_profile() {
  local profile="$1"           # etiqueta: desktop|mobile
  local preset_flag=("${@:2}") # flags opcionales para lighthouse
  local out="$LOGDIR/${STAMP}-${profile}"
  lighthouse "$URL" --quiet --port=9333 --chrome-flags="--headless=new --no-sandbox --disable-dev-shm-usage --remote-debugging-address=127.0.0.1" \
    --output=json --output-path="$out.json" --only-categories=performance "${preset_flag[@]}"

  if [[ ! -f "$out.json" ]]; then
    echo "Error ($profile): no se generó reporte Lighthouse $(date)" >> "$LOGDIR/alerts.log"
    return
  fi

  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq -r --arg ts "$ts" --arg profile "$profile" '[$ts,
        $profile,
        .categories.performance.score,
        .audits["largest-contentful-paint"].numericValue,
        .audits["interactive"].numericValue,
        .audits["speed-index"].numericValue,
        .audits["total-blocking-time"].numericValue] | @csv' "$out.json" >> "$LOGDIR/history.csv"

  local score lcp
  score=$(jq -r '.categories.performance.score' "$out.json")
  lcp=$(jq -r '.audits["largest-contentful-paint"].numericValue' "$out.json")
  if (( $(echo "$score < 0.7" | bc -l) )) || (( $(echo "$lcp > 3000" | bc -l) )); then
    echo "Alerta ($profile): score=$score LCP=${lcp}ms $(date)" >> "$LOGDIR/alerts.log"
  fi
}

run_profile desktop --preset=desktop
run_profile mobile
