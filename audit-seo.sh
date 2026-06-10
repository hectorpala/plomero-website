#!/bin/bash
SITIO="/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán"
echo "🔍 AUDITORÍA SEO COMPLETA"
echo "========================="
echo ""
find "$SITIO" -name "*.html" -type f ! -path "*/.*" ! -path "*/node_modules/*" | sort | while read f; do
  rel=$(echo "$f" | sed "s|$SITIO/||")
  echo "📄 $rel"
  grep -q "<title>" "$f" || echo "  ❌ Sin <title>"
  grep -q "name=\"description\"" "$f" || echo "  ❌ Sin meta description"
  h1=$(grep -o "<h1" "$f" | wc -l)
  [ $h1 -gt 1 ] && echo "  ❌ $h1 H1s (máx 1)"
  grep -E '<img[^>]*>' "$f" | grep -v 'alt=' >/dev/null && echo "  ❌ Imágenes sin alt"
  grep -q "og:image" "$f" || echo "  ❌ Sin og:image"
  grep -q "canonical" "$f" || echo "  ❌ Sin canonical"
done
echo ""
echo "✅ Auditoría completa"
