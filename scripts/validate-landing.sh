#!/bin/bash
# validate-landing.sh - Valida que una landing de servicios de PLOMERÍA cumpla la
# estructura de la plantilla ESTÁNDAR del sitio.
# Referencia (esqueleto estándar): servicios/plomero-zona-oriente-culiacan/index.html
# Uso: ./validate-landing.sh servicios/[slug]/index.html
#
# Adaptado del sitio electricista. OJO: las páginas de servicio de plomero NO son
# 100% uniformes (hay varias generaciones de plantilla). Por eso este validador
# comprueba SOLO el denominador común que tiene el esqueleto estándar del que se
# generan las páginas NUEVAS (gen-landing copia ese esqueleto byte a byte): SEO core
# + estructura de hero + anti-fuga de la plantilla origen (electricista). No exige
# @font-face inline, botones flotantes inline ni exit-popup (la plantilla estándar
# de plomero los carga vía main.js / CSS externo, no inline).

FILE="$1"
ERRORS=0
WARNINGS=0

if [ -z "$FILE" ]; then
    echo "Uso: ./validate-landing.sh <ruta-a-index.html>"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "ERROR: Archivo no encontrado: $FILE"
    exit 1
fi

CONTENT=$(cat "$FILE")

# Las páginas noindex no son landings de ranking: se omite la validación.
if echo "$CONTENT" | grep -qE '<meta name="robots"[^>]*noindex'; then
    echo "Validando: $FILE"
    echo "-------------------------------------------"
    echo "  SKIP  Página noindex — validación de plantilla omitida"
    echo "-------------------------------------------"
    echo "RESULTADO: OMITIDO (noindex, no es landing de ranking)"
    exit 0
fi

pass() { echo "  OK  $1"; }
fail() { echo "  FAIL  $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  WARN  $1"; WARNINGS=$((WARNINGS + 1)); }

echo "Validando: $FILE"
echo "-------------------------------------------"

# 1. Canonical URL (universal en el sitio)
if echo "$CONTENT" | grep -q 'rel="canonical"'; then
    pass "Canonical URL presente"
else
    fail "Falta canonical URL"
fi

# 2. Open Graph tags
if echo "$CONTENT" | grep -q 'og:title' && echo "$CONTENT" | grep -q 'og:description'; then
    pass "Open Graph tags presentes"
else
    fail "Faltan Open Graph tags (og:title, og:description)"
fi

# 3. Schema JSON-LD
if echo "$CONTENT" | grep -q 'application/ld+json'; then
    pass "Schema JSON-LD presente"
else
    fail "Falta schema JSON-LD"
fi

# 4. Breadcrumb (schema o HTML)
if echo "$CONTENT" | grep -q 'BreadcrumbList' || echo "$CONTENT" | grep -q 'breadcrumb'; then
    pass "Breadcrumb presente"
else
    fail "Falta breadcrumb (schema o HTML)"
fi

# 5. Meta robots
if echo "$CONTENT" | grep -q '<meta name="robots"'; then
    pass "Meta robots presente"
else
    fail "Falta <meta name=\"robots\">"
fi

# 6. Hero
if echo "$CONTENT" | grep -q 'class="hero"' && echo "$CONTENT" | grep -q 'hero-content'; then
    pass "Hero (.hero + .hero-content) presente"
else
    fail "Falta estructura de hero (.hero / .hero-content)"
fi

# 7. H1
if echo "$CONTENT" | grep -q '<h1'; then
    pass "H1 presente"
else
    fail "Falta <h1>"
fi

# 8. Hoja de estilos del sitio
if echo "$CONTENT" | grep -q 'styles.min.css'; then
    pass "styles.min.css presente"
else
    fail "Falta /styles.min.css"
fi

# 9. theme-color
if echo "$CONTENT" | grep -q 'name="theme-color"'; then
    pass "theme-color presente"
else
    warn "Falta <meta name=\"theme-color\">"
fi

# 10. GTM (deferred)
if echo "$CONTENT" | grep -q 'GTM-W75CRTX5' || echo "$CONTENT" | grep -q 'googletagmanager'; then
    pass "GTM configurado"
else
    warn "No se encontró GTM"
fi

# 11. ANTI-FUGA de la plantilla origen (electricista). En un sitio de PLOMERÍA jamás
#     debe colarse "electricista" ni el GTM del electricista (sería copy-paste sucio).
if echo "$CONTENT" | grep -qi 'electricista'; then
    fail "FUGA: aparece 'electricista' (contaminación de la plantilla origen)"
else
    pass "Sin fuga 'electricista'"
fi
if echo "$CONTENT" | grep -q 'GTM-5Z2QRZ5Q'; then
    fail "FUGA: GTM del electricista (GTM-5Z2QRZ5Q)"
else
    pass "GTM correcto (sin fuga del electricista)"
fi

echo "-------------------------------------------"

if [ $ERRORS -gt 0 ]; then
    echo "RESULTADO: FALLO - $ERRORS errores, $WARNINGS advertencias"
    exit 1
else
    if [ $WARNINGS -gt 0 ]; then
        echo "RESULTADO: PASO con $WARNINGS advertencias"
    else
        echo "RESULTADO: PASO - Todas las validaciones OK"
    fi
    exit 0
fi
