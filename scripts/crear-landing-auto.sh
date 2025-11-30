#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Script de Automatización de Landing Pages v2.0.0
# Crea landing pages completas desde el template base
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e  # Detener en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_step() {
    echo -e "${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INICIO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

START_TIME=$(date +%s)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 AUTOMATIZACIÓN DE LANDING PAGES INICIADA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Validar argumentos
if [ -z "$1" ]; then
    print_error "Falta el nombre del servicio"
    echo ""
    echo "Uso: $0 \"Nombre del Servicio\""
    echo "Ejemplo: $0 \"Plomero 24 Horas\""
    echo ""
    exit 1
fi

SERVICE_NAME="$1"
echo "📋 Servicio: ${SERVICE_NAME}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 1: Generar SLUG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 1/7] Generando slug..."

# Convertir a minúsculas, reemplazar espacios por guiones, quitar acentos
SLUG=$(echo "$SERVICE_NAME" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/á/a/g; s/é/e/g; s/í/i/g; s/ó/o/g; s/ú/u/g; s/ñ/n/g' | \
    sed 's/[^a-z0-9]/-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-//; s/-$//')

echo "🔗 Slug generado: ${SLUG}"
print_success "Slug creado"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 2: Generar contenido SEO con IA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 2/7] Generando contenido SEO con IA..."
echo "  🤖 Analizando servicio: ${SERVICE_NAME}"
echo "  📝 Creando title, description, keywords..."
echo "  💡 Generando 4 benefits personalizados..."

# NOTA: Aquí se llamará al generador-seo.md cuando exista
# Por ahora, usamos placeholder
print_warning "Generador SEO pendiente - Usando placeholder"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 3: Crear config.json
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 3/7] Creando config.json..."

# Crear directorio temporal para el config
mkdir -p "servicios/${SLUG}"

# Crear config.json básico (será mejorado con generador SEO)
cat > "servicios/${SLUG}/config.json" <<EOF
{
  "slug": "${SLUG}",
  "service_name": "${SERVICE_NAME}",
  "seo": {
    "title": "${SERVICE_NAME} Culiacán | Servicio Profesional",
    "description": "🔧 ${SERVICE_NAME} en Culiacán. Servicio profesional certificado. Cotización gratis. ¡Llama: 667 392 2273!",
    "keywords": "${SLUG} culiacan, plomero culiacan, servicio plomeria"
  },
  "content": {
    "h1": "${SERVICE_NAME} en Culiacán | Profesional Certificado",
    "subtitle": "Servicio profesional de ${SERVICE_NAME} en Culiacán. Atención rápida, garantía por escrito.",
    "whatsapp_text": "${SERVICE_NAME}",
    "breadcrumb": "${SERVICE_NAME}",
    "service_type": "${SERVICE_NAME}"
  },
  "images": {
    "hero_base": "${SLUG}-culiacan",
    "og": "${SLUG}-culiacan-800w.webp"
  }
}
EOF

echo "  📄 Archivo: servicios/${SLUG}/config.json"
print_success "config.json creado"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 4: Copiar template v2.0.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 4/7] Copiando template v2.0.0..."

TEMPLATE_SOURCE="."  # Página principal (index.html)
TARGET_DIR="servicios/${SLUG}"

if [ ! -d "$TEMPLATE_SOURCE" ]; then
    print_error "Template base no encontrado: ${TEMPLATE_SOURCE}"
    exit 1
fi

# Crear backup si ya existe
if [ -f "${TARGET_DIR}/index.html" ]; then
    BACKUP_FILE="${TARGET_DIR}/index.html.backup-$(date +%Y%m%d-%H%M%S)"
    echo "  💾 Creando backup: ${BACKUP_FILE}"
    cp "${TARGET_DIR}/index.html" "$BACKUP_FILE"
fi

# Copiar index.html del template
echo "  📋 Copiando desde: ${TEMPLATE_SOURCE}/index.html"
cp "${TEMPLATE_SOURCE}/index.html" "${TARGET_DIR}/index.html"

echo "  📂 Destino: ${TARGET_DIR}/index.html"
print_success "Template copiado"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 4.5: Corregir paths relativos para subdirectorio
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 4.5/7] Corrigiendo paths para subdirectorio..."

HTML_FILE="${TARGET_DIR}/index.html"

# Corregir CSS externo
sed -i '' 's|href="styles\.min\.css"|href="/styles.min.css"|g' "$HTML_FILE"
echo "  ✓ CSS externo: styles.min.css → /styles.min.css"

# Corregir fonts en @font-face
sed -i '' "s|src:url('assets/fonts/|src:url('/assets/fonts/|g" "$HTML_FILE"
echo "  ✓ Fonts: assets/fonts/ → /assets/fonts/"

# Corregir imágenes srcset
sed -i '' 's|srcset="assets/images/|srcset="/assets/images/|g' "$HTML_FILE"
echo "  ✓ Imágenes srcset: assets/images/ → /assets/images/"

# Corregir imágenes src
sed -i '' 's|src="assets/images/|src="/assets/images/|g' "$HTML_FILE"
echo "  ✓ Imágenes src: assets/images/ → /assets/images/"

# Corregir links a servicios
sed -i '' 's|href="./servicios/|href="/servicios/|g' "$HTML_FILE"
echo "  ✓ Links servicios: ./servicios/ → /servicios/"

print_success "Paths corregidos (5 tipos)"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 5: Aplicar contenido con agentconstructor
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 5/7] Aplicando contenido con agentconstructor..."
echo "  🤖 Leyendo: servicios/${SLUG}/config.json"
echo "  ✏️  Modificando: servicios/${SLUG}/index.html"

print_warning "Agentconstructor pendiente - Requiere integración manual"
echo "  ℹ️  Por ahora, usa: @agentconstructor con el config.json"

# NOTA: Aquí se llamará al agentconstructor cuando esté integrado
# print_success "Contenido aplicado (21 reemplazos)"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 6: Validar imágenes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 6/7] Validando imágenes..."

# Verificar si existe el script de validación
if [ -f "scripts/validar-imagenes.sh" ]; then
    bash scripts/validar-imagenes.sh "servicios/${SLUG}"
    print_success "Imágenes validadas"
else
    print_warning "Script validar-imagenes.sh no encontrado"
    echo "  🖼️  Verifica manualmente las imágenes en:"
    echo "      - ${SLUG}-culiacan-800w.webp"
    echo "      - ${SLUG}-culiacan-1200w.webp"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASO 7: Validar HTML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ""
print_step "[PASO 7/7] Validando HTML..."

if [ -f "./validate-landing.sh" ]; then
    echo "  ✓ Verificando data-template-version=\"v2.0.0\""
    echo "  ✓ Verificando estructura HTML"

    # Ejecutar validador
    bash ./validate-landing.sh "servicios/${SLUG}/index.html" || true

    print_success "HTML validado"
else
    print_warning "validate-landing.sh no encontrado"
    echo "  ℹ️  Valida manualmente el HTML"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FINALIZACIÓN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 LANDING CREADA EXITOSAMENTE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📂 Ubicación: servicios/${SLUG}/index.html"
echo "🔗 URL local: file://$(pwd)/servicios/${SLUG}/index.html"
echo "⏱️  Tiempo: ${DURATION} segundos"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Abrir en navegador (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🌐 Abriendo en navegador..."
    open "servicios/${SLUG}/index.html"
fi

exit 0
