#!/bin/bash
# Script para actualizar sitemaps con fechas reales de git commits
# Uso: bash update-sitemaps.sh

set -e

echo "=== Updating sitemaps with real git commit dates ==="

# Función para obtener fecha del último commit de un archivo
get_lastmod() {
    local file=$1
    if [ -f "$file" ]; then
        git log -1 --format=%cI -- "$file" 2>/dev/null || echo "2025-11-21T21:52:06-07:00"
    else
        echo "2025-11-21T21:52:06-07:00"
    fi
}

# Obtener fechas
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
INDEX_DATE=$(get_lastmod "index.html")
BLOG_INDEX_DATE=$(get_lastmod "blog/index.html")
EMERGENCIA_DATE=$(get_lastmod "servicios/emergencia-24-7/index.html")
REPARACION_FUGAS_DATE=$(get_lastmod "servicios/reparacion-de-fugas/index.html")

echo "Current date: $CURRENT_DATE"
echo "Index.html: $INDEX_DATE"
echo "Emergencia 24/7: $EMERGENCIA_DATE"
echo "Reparación fugas: $REPARACION_FUGAS_DATE"

# Actualizar sitemap.xml (índice)
cat > sitemap.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://plomeroculiacanpro.mx/sitemaps/main_sitemap.xml</loc>
    <lastmod>$CURRENT_DATE</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://plomeroculiacanpro.mx/sitemaps/images_sitemap.xml</loc>
    <lastmod>$CURRENT_DATE</lastmod>
  </sitemap>
</sitemapindex>
EOF

echo "✓ sitemap.xml updated"

# Actualizar main_sitemap.xml con fechas reales
cat > sitemaps/main_sitemap.xml << 'EOF'
<?xml version='1.0' encoding='UTF-8'?>
<ns0:urlset xmlns:ns0="http://www.sitemaps.org/schemas/sitemap/0.9">
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/</ns0:loc>
    <ns0:lastmod>INDEX_DATE_PLACEHOLDER</ns0:lastmod>
    <ns0:changefreq>weekly</ns0:changefreq>
    <ns0:priority>1.0</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/servicios/emergencia-24-7/</ns0:loc>
    <ns0:lastmod>EMERGENCIA_DATE_PLACEHOLDER</ns0:lastmod>
    <ns0:changefreq>monthly</ns0:changefreq>
    <ns0:priority>0.9</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/servicios/reparacion-de-fugas/</ns0:loc>
    <ns0:lastmod>REPARACION_FUGAS_DATE_PLACEHOLDER</ns0:lastmod>
    <ns0:changefreq>monthly</ns0:changefreq>
    <ns0:priority>0.9</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/servicios/destape-de-drenajes/</ns0:loc>
    <ns0:lastmod>2025-11-20T21:29:43+00:00</ns0:lastmod>
    <ns0:changefreq>monthly</ns0:changefreq>
    <ns0:priority>0.9</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/servicios/instalacion-de-sanitarios/</ns0:loc>
    <ns0:lastmod>2025-11-20T21:29:43+00:00</ns0:lastmod>
    <ns0:changefreq>monthly</ns0:changefreq>
    <ns0:priority>0.8</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/servicios/mantenimiento-de-boiler/</ns0:loc>
    <ns0:lastmod>2025-11-20T21:29:43+00:00</ns0:lastmod>
    <ns0:changefreq>monthly</ns0:changefreq>
    <ns0:priority>0.8</ns0:priority>
  </ns0:url>
  <ns0:url>
    <ns0:loc>https://plomeroculiacanpro.mx/blog/</ns0:loc>
    <ns0:lastmod>BLOG_INDEX_DATE_PLACEHOLDER</ns0:lastmod>
    <ns0:changefreq>weekly</ns0:changefreq>
    <ns0:priority>0.7</ns0:priority>
  </ns0:url>
</ns0:urlset>
EOF

# Reemplazar placeholders
sed -i '' "s|INDEX_DATE_PLACEHOLDER|$INDEX_DATE|g" sitemaps/main_sitemap.xml
sed -i '' "s|EMERGENCIA_DATE_PLACEHOLDER|$EMERGENCIA_DATE|g" sitemaps/main_sitemap.xml
sed -i '' "s|REPARACION_FUGAS_DATE_PLACEHOLDER|$REPARACION_FUGAS_DATE|g" sitemaps/main_sitemap.xml
sed -i '' "s|BLOG_INDEX_DATE_PLACEHOLDER|$BLOG_INDEX_DATE|g" sitemaps/main_sitemap.xml

echo "✓ sitemaps/main_sitemap.xml updated"
echo ""
echo "=== Sitemap update complete ==="
echo "Run 'git add sitemap.xml sitemaps/main_sitemap.xml && git commit' to save changes"
