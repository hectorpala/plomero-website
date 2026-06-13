#!/bin/bash
BASE="/Users/openclaw/Sitios Web/Plomero Culiacán/servicios/plomero-colonias-culiacan"

SKIP="tres-rios chapultepec centro guadalupe bachigualato humaya campestre montebello valle-alto zona-dorada country-tres-rios la-campina colinas-de-san-miguel lomas-del-boulevard cumbres-tres-rios infonavit-barrancos monaco real-del-valle hacienda-los-huertos bugambilias santa-fe las-palmas bosques-del-humaya amorada jardines-del-valle lomas-de-san-isidro altamira colinas-de-la-rivera villa-universidad isla-del-oeste nuevo-culiacan libertad barrancos fovissste praderas-del-humaya villas-del-humaya culiacan-tres-rios lomas-del-humaya balcones-del-humaya portales-del-rio jardines-tres-rios campestre-tres-rios floresta-tres-rios los-laureles hacienda-del-valle santa-clara residencial-san-jose index.html las-quintas"

OK=0
SKIP_COUNT=0

for dir in "$BASE"/*/; do
  slug=$(basename "$dir")
  FILE="$dir/index.html"
  [ ! -f "$FILE" ] && continue

  # Skip Tier 1 and Tier 2
  if echo " $SKIP " | grep -q " $slug "; then
    SKIP_COUNT=$((SKIP_COUNT+1))
    continue
  fi

  # Replace robots meta: index, follow → noindex, follow
  sed -i '' 's/name="robots" content="index, follow"/name="robots" content="noindex, follow"/g' "$FILE"
  OK=$((OK+1))
done

echo "✅ noindex aplicado: $OK colonias"
echo "⏭️  Saltadas (Tier 1+2): $SKIP_COUNT colonias"
