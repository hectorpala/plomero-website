#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Validador de Imágenes para Landing Pages
# Verifica y crea imágenes faltantes automáticamente
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e  # Detener en caso de error

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}    ✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}    ⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}    ❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}    ℹ️  $1${NC}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VALIDACIÓN DE ARGUMENTOS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if [ -z "$1" ]; then
    print_error "Falta el directorio de la landing"
    echo ""
    echo "Uso: $0 servicios/[slug]"
    echo "Ejemplo: $0 servicios/plomero-24-horas"
    echo ""
    exit 1
fi

LANDING_DIR="$1"
HTML_FILE="$LANDING_DIR/index.html"

# Verificar que exista el archivo HTML
if [ ! -f "$HTML_FILE" ]; then
    print_error "No se encontró: $HTML_FILE"
    exit 1
fi

echo "  🔍 Buscando imágenes referenciadas en HTML..."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXTRAER IMÁGENES DEL HTML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Buscar todas las imágenes hero en el HTML
# Patrón: [slug]-culiacan-[800w|1200w].webp
IMAGES=$(grep -o '[a-z0-9-]*-culiacan-[0-9]*w\.webp' "$HTML_FILE" 2>/dev/null | sort -u)

if [ -z "$IMAGES" ]; then
    print_warning "No se encontraron imágenes hero en el HTML"
    exit 0
fi

echo "  📋 Imágenes encontradas en HTML:"
for img in $IMAGES; do
    echo "      - $img"
done
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERIFICAR EXISTENCIA DE IMÁGENES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo "  ✓ Verificando existencia en assets/images/optimizadas/..."

MISSING_IMAGES=0
IMAGES_DIR="assets/images/optimizadas"

for img in $IMAGES; do
    IMG_PATH="$IMAGES_DIR/$img"

    if [ ! -f "$IMG_PATH" ]; then
        print_warning "Falta: $img"
        MISSING_IMAGES=$((MISSING_IMAGES + 1))

        # Intentar crear desde la versión 800w
        if [[ "$img" == *"-1200w.webp" ]]; then
            # Extraer el nombre base sin el tamaño
            BASE_NAME=$(echo "$img" | sed 's/-1200w\.webp$//')
            SOURCE_IMG="${IMAGES_DIR}/${BASE_NAME}-800w.webp"

            if [ -f "$SOURCE_IMG" ]; then
                echo "      📋 Copiando desde: ${BASE_NAME}-800w.webp"
                cp "$SOURCE_IMG" "$IMG_PATH"
                print_success "Creada: $img (desde 800w)"
            else
                print_error "No se puede crear: falta imagen base 800w"
                echo "      ℹ️  Necesitas crear manualmente:"
                echo "         $SOURCE_IMG"
            fi
        elif [[ "$img" == *"-800w.webp" ]]; then
            print_error "Falta imagen base 800w: $img"
            echo "      ℹ️  Esta imagen debe crearse manualmente"
            echo "      📍 Ubicación esperada: $IMG_PATH"
        fi
    else
        print_success "Existe: $img"
    fi
done

echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESUMEN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if [ $MISSING_IMAGES -eq 0 ]; then
    print_success "Todas las imágenes existen ✓"
else
    print_warning "Se encontraron $MISSING_IMAGES imagen(es) faltante(s)"
    echo ""
    print_info "Revisa que todas las imágenes 800w existan manualmente"
fi

exit 0
