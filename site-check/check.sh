#!/usr/bin/env bash
URL="https://plomeroculiacanpro.mx/"
LOGDIR="$(pwd)/site-check/logs"
mkdir -p "$LOGDIR"
STAMP=$(date +%F-%H%M)

echo "=== Lighthouse Check: $URL ==="
echo ""

# --- DESKTOP ---
echo "Desktop..."
OUT_DESKTOP="$LOGDIR/$STAMP-desktop"
lighthouse "$URL" --quiet --chrome-flags="--headless" --output=json --output-path="$OUT_DESKTOP.json" \
  --only-categories=performance --preset=desktop

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCORE_D=$(jq -r '.categories.performance.score' "$OUT_DESKTOP.json")
LCP_D=$(jq -r '.audits["largest-contentful-paint"].numericValue' "$OUT_DESKTOP.json")
SI_D=$(jq -r '.audits["speed-index"].numericValue' "$OUT_DESKTOP.json")
TBT_D=$(jq -r '.audits["total-blocking-time"].numericValue' "$OUT_DESKTOP.json")

echo "$TIMESTAMP,desktop,$SCORE_D,$LCP_D,$SI_D,$TBT_D" >> "$LOGDIR/history.csv"
echo "  Score: $(echo "$SCORE_D * 100" | bc)%  LCP: ${LCP_D}ms"

# --- MOBILE ---
echo "Mobile..."
OUT_MOBILE="$LOGDIR/$STAMP-mobile"
lighthouse "$URL" --quiet --chrome-flags="--headless" --output=json --output-path="$OUT_MOBILE.json" \
  --only-categories=performance

SCORE_M=$(jq -r '.categories.performance.score' "$OUT_MOBILE.json")
LCP_M=$(jq -r '.audits["largest-contentful-paint"].numericValue' "$OUT_MOBILE.json")
SI_M=$(jq -r '.audits["speed-index"].numericValue' "$OUT_MOBILE.json")
TBT_M=$(jq -r '.audits["total-blocking-time"].numericValue' "$OUT_MOBILE.json")

echo "$TIMESTAMP,mobile,$SCORE_M,$LCP_M,$SI_M,$TBT_M" >> "$LOGDIR/history.csv"
echo "  Score: $(echo "$SCORE_M * 100" | bc)%  LCP: ${LCP_M}ms"

# --- ALERTAS ---
if (( $(echo "$SCORE_D < 0.7" | bc -l) )) || (( $(echo "$SCORE_M < 0.5" | bc -l) )); then
  echo "ALERTA: Desktop=$SCORE_D Mobile=$SCORE_M $(date)" >> "$LOGDIR/alerts.log"
  echo ""
  echo "ALERTA: Performance baja detectada"
fi

echo ""
echo "=== Resumen ==="
echo "Desktop: $(echo "$SCORE_D * 100" | bc)%"
echo "Mobile:  $(echo "$SCORE_M * 100" | bc)%"
echo ""
echo "Logs guardados en: $LOGDIR"
