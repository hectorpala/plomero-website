#!/bin/bash
# IndexNow - Notificación instantánea a Bing/Yandex
# Uso: ./scripts/indexnow.sh "https://plomeroculiacanpro.mx/servicios/nueva-pagina/"
# O para múltiples URLs: ./scripts/indexnow.sh url1 url2 url3

KEY="f7648833b7167b4e80927a493e8e3a45"
HOST="plomeroculiacanpro.mx"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

if [ $# -eq 0 ]; then
    echo "Uso: $0 <url1> [url2] [url3] ..."
    echo "Ejemplo: $0 https://plomeroculiacanpro.mx/servicios/nueva-pagina/"
    exit 1
fi

# Construir array de URLs
URLS=""
for url in "$@"; do
    if [ -z "$URLS" ]; then
        URLS="\"$url\""
    else
        URLS="$URLS, \"$url\""
    fi
done

# Enviar a IndexNow (Bing)
echo "Enviando ${#} URL(s) a IndexNow..."
RESPONSE=$(curl -s -X POST "https://api.indexnow.org/indexnow" \
    -H "Content-Type: application/json" \
    -d "{
        \"host\": \"${HOST}\",
        \"key\": \"${KEY}\",
        \"keyLocation\": \"${KEY_LOCATION}\",
        \"urlList\": [${URLS}]
    }")

if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "OK" ] || echo "$RESPONSE" | grep -q "200"; then
    echo "✓ URLs enviadas exitosamente a Bing/Yandex"
    echo "  Las páginas serán indexadas en minutos/horas"
else
    echo "Respuesta: $RESPONSE"
fi
