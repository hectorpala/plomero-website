#!/bin/bash
# Reconstruye el sitemap eliminando todas las páginas con noindex
BASE="/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán"
SITEMAP="$BASE/sitemaps/main_sitemap.xml"
TEMP="$BASE/sitemaps/main_sitemap_new.xml"

# Leer el encabezado del sitemap actual
HEAD=$(head -3 "$SITEMAP")

echo "$HEAD" > "$TEMP"

KEPT=0
REMOVED=0

# Extraer cada bloque <url>...</url> y decidir si lo conserva
while IFS= read -r url; do
  PATH_REL=$(echo "$url" | sed 's|https://plomeroculiacanpro.mx||')
  FILE="$BASE${PATH_REL}index.html"

  # Homepage especial
  if [ "$PATH_REL" = "/" ]; then
    FILE="$BASE/index.html"
  fi

  if [ -f "$FILE" ]; then
    IS_NOINDEX=$(grep -c 'content="noindex' "$FILE" 2>/dev/null)
    if [ "$IS_NOINDEX" -gt 0 ]; then
      REMOVED=$((REMOVED+1))
      continue
    fi
  fi

  # Conservar: extraer el bloque completo del sitemap
  echo "  <url>" >> "$TEMP"
  grep -A 4 "<loc>$url</loc>" "$SITEMAP" | head -5 >> "$TEMP"
  KEPT=$((KEPT+1))
done < <(grep '<loc>' "$SITEMAP" | sed 's/<[^>]*>//g' | tr -d ' \t')

echo "</urlset>" >> "$TEMP"

mv "$TEMP" "$SITEMAP"
echo "✅ Sitemap reconstruido: $KEPT URLs conservadas · $REMOVED eliminadas"
