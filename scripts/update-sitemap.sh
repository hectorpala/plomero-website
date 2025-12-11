#!/bin/bash
# Actualizar lastmod en sitemap basado en archivos modificados
# Uso: ./scripts/update-sitemap.sh

HOST="plomeroculiacanpro.mx"
SITEMAP="sitemaps/main_sitemap.xml"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$ROOT_DIR"

echo -e "${YELLOW}Actualizando sitemap...${NC}"

# Obtener fecha actual en formato ISO 8601
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")

# Contador de actualizaciones
updated=0

# Buscar archivos HTML modificados en los últimos 7 días
while IFS= read -r file; do
    # Obtener la URL correspondiente
    relative_path="${file#./}"
    
    # Convertir path a URL
    if [[ "$relative_path" == "index.html" ]]; then
        url="https://${HOST}/"
    elif [[ "$relative_path" == */index.html ]]; then
        dir=$(dirname "$relative_path")
        url="https://${HOST}/${dir}/"
    else
        continue
    fi
    
    # Obtener fecha de modificación del archivo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        file_date=$(stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%S" "$file")
    else
        file_date=$(stat -c "%y" "$file" | cut -d'.' -f1 | tr ' ' 'T')
    fi
    file_date="${file_date}-07:00"
    
    # Actualizar lastmod en sitemap si la URL existe
    if grep -q "<loc>${url}</loc>" "$SITEMAP"; then
        # Usar sed compatible con macOS
        sed -i '' "/<loc>${url//\//\\/}<\/loc>/,/<\/url>/ s/<lastmod>[^<]*<\/lastmod>/<lastmod>${file_date}<\/lastmod>/" "$SITEMAP"
        echo -e "  ${GREEN}✓${NC} $url"
        ((updated++))
    fi
done < <(find . -name "index.html" -mtime -7 -type f)

# Actualizar fecha del sitemap index
sed -i '' "s/<lastmod>[^<]*<\/lastmod>/<lastmod>${NOW}<\/lastmod>/g" sitemap.xml

echo -e "\n${GREEN}Listo.${NC} $updated URLs actualizadas en sitemap."
echo -e "Ejecuta ${YELLOW}git add && git commit && git push${NC} para publicar."
