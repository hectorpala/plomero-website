#!/bin/bash
# IndexNow - Notificar URLs a buscadores (Bing, Yandex, Seznam, Naver)
# Uso: ./scripts/indexnow.sh [URL o "sitemap"]

KEY="013f798d7b51dcbc05f3926fb27c9d65"
HOST="plomeroculiacanpro.mx"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

notify_url() {
    local url=$1
    echo -e "${YELLOW}Notificando:${NC} $url"
    response=$(curl -s -w "%{http_code}" -o /tmp/indexnow_response.txt \
        "https://api.indexnow.org/indexnow?url=${url}&key=${KEY}&keyLocation=${KEY_LOCATION}")
    if [ "$response" = "200" ] || [ "$response" = "202" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
    else
        echo -e "${RED}✗ Error${NC} (HTTP $response)"
    fi
}

notify_batch() {
    local urls=("$@")
    local json_urls=""
    for url in "${urls[@]}"; do
        json_urls="${json_urls}\"${url}\","
    done
    json_urls="${json_urls%,}"

    echo -e "${YELLOW}Notificando ${#urls[@]} URLs en batch...${NC}"
    response=$(curl -s -w "%{http_code}" -o /tmp/indexnow_response.txt \
        -X POST "https://api.indexnow.org/indexnow" \
        -H "Content-Type: application/json" \
        -d "{\"host\":\"${HOST}\",\"key\":\"${KEY}\",\"keyLocation\":\"${KEY_LOCATION}\",\"urlList\":[${json_urls}]}")
    if [ "$response" = "200" ] || [ "$response" = "202" ]; then
        echo -e "${GREEN}✓ Batch OK${NC} (HTTP $response)"
    else
        echo -e "${RED}✗ Batch Error${NC} (HTTP $response)"
    fi
}

if [ -z "$1" ]; then
    echo "Uso:"
    echo "  $0 <URL>     - Notificar una URL"
    echo "  $0 sitemap   - Notificar todas las URLs del sitemap"
    exit 1
fi

if [ "$1" = "sitemap" ]; then
    echo -e "${YELLOW}Extrayendo URLs del sitemap...${NC}"
    urls=($(curl -s "https://${HOST}/sitemaps/main_sitemap.xml" | grep -oP '(?<=<loc>)[^<]+'))
    echo "Encontradas ${#urls[@]} URLs"
    notify_batch "${urls[@]}"
else
    if [ $# -eq 1 ]; then
        notify_url "$1"
    else
        notify_batch "$@"
    fi
fi

echo -e "\n${GREEN}Listo.${NC} Buscadores procesarán en minutos/horas."
