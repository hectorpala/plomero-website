#!/usr/bin/env node

/**
 * Script de Optimización Masiva para Plomero Culiacán Pro
 *
 * Optimiza todas las páginas HTML del sitio aplicando:
 * - Security headers
 * - SEO meta tags
 * - hreflang
 * - Open Graph
 * - ARIA accessibility
 * - Performance optimizations
 *
 * Uso: node optimize-all-pages.js [--dry-run] [--filter=pattern]
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// ============================================
// CONFIGURACIÓN
// ============================================

const CONFIG = {
    baseUrl: 'https://plomeroculiacanpro.mx',
    rootDir: path.join(__dirname, '../..'),
    partialsDir: path.join(__dirname, '../partials'),
    excludePatterns: [
        '**/node_modules/**',
        '**/templates/**',
        '**/gracias/**',
        '**/.git/**'
    ],
    dryRun: process.argv.includes('--dry-run'),
    filter: process.argv.find(arg => arg.startsWith('--filter='))?.split('=')[1]
};

// ============================================
// CARGAR PARTIALS
// ============================================

const PARTIALS = {
    headOptimized: fs.readFileSync(
        path.join(CONFIG.partialsDir, 'head-optimized.html'),
        'utf8'
    )
};

// ============================================
// UTILIDADES
// ============================================

function log(message, type = 'info') {
    const colors = {
        info: '\x1b[36m',    // Cyan
        success: '\x1b[32m', // Green
        warning: '\x1b[33m', // Yellow
        error: '\x1b[31m',   // Red
        reset: '\x1b[0m'
    };
    console.log(`${colors[type]}${message}${colors.reset}`);
}

function extractMetaData(html) {
    const titleMatch = html.match(/<title>(.*?)<\/title>/);
    const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]+)"/);

    return {
        title: titleMatch ? titleMatch[1] : 'Plomero en Culiacán 24/7',
        description: descMatch ? descMatch[1] : 'Servicio de plomería profesional en Culiacán'
    };
}

function getPageUrl(filePath) {
    const relativePath = path.relative(CONFIG.rootDir, filePath);
    const urlPath = relativePath
        .replace(/index\.html$/, '')
        .replace(/\.html$/, '')
        .replace(/\\/g, '/');

    return `${CONFIG.baseUrl}/${urlPath}`;
}

// ============================================
// OPTIMIZACIONES
// ============================================

function optimizePage(html, filePath) {
    const url = getPageUrl(filePath);
    const { title, description } = extractMetaData(html);

    // 1. Inyectar head optimizado
    let optimized = html;

    // Buscar si ya tiene security headers
    if (!html.includes('X-Content-Type-Options')) {
        // Preparar partial con variables reemplazadas
        let headContent = PARTIALS.headOptimized
            .replace(/\{\{URL\}\}/g, url)
            .replace(/\{\{TITLE\}\}/g, title)
            .replace(/\{\{DESCRIPTION\}\}/g, description);

        // Inyectar después de la descripción original o antes de </head>
        const descRegex = /<meta\s+name="description"[^>]*>/;
        if (descRegex.test(optimized)) {
            optimized = optimized.replace(
                descRegex,
                match => `${match}\n\n${headContent}`
            );
        } else {
            optimized = optimized.replace(
                '</head>',
                `\n${headContent}\n</head>`
            );
        }
    }

    // 2. Agregar ARIA al formulario (si existe)
    if (html.includes('<form') && !html.includes('aria-labelledby')) {
        optimized = addARIAToForm(optimized);
    }

    // 3. Eliminar estilos inline (preservar críticos)
    optimized = removeInlineStyles(optimized);

    // 4. Optimizar imágenes (agregar loading="lazy")
    optimized = optimizeImages(optimized);

    return optimized;
}

function addARIAToForm(html) {
    // Agregar aria-labelledby si no existe
    if (html.includes('<form') && !html.includes('aria-labelledby')) {
        html = html.replace(
            /<form([^>]*)>/,
            '<form$1 aria-labelledby="form-title">'
        );
    }

    // Agregar labels visually-hidden a inputs
    html = html.replace(
        /<input\s+type="text"\s+id="nombre"([^>]*)>/,
        '<label for="nombre" class="visually-hidden">Nombre completo</label>\n<input type="text" id="nombre" aria-required="true"$1>'
    );

    return html;
}

function removeInlineStyles(html) {
    // Eliminar style="" pero preservar algunos críticos
    const preservePatterns = [
        /style="display:\s*none"/gi,
        /style="width:\s*\d+px;\s*height:\s*\d+px"/gi
    ];

    let result = html;

    // Marcar estilos a preservar
    preservePatterns.forEach((pattern, i) => {
        result = result.replace(pattern, `PRESERVE_STYLE_${i}`);
    });

    // Eliminar estilos inline restantes
    result = result.replace(/\s+style="[^"]*"/gi, '');

    // Restaurar estilos preservados
    preservePatterns.forEach((pattern, i) => {
        const matches = html.match(pattern);
        if (matches) {
            matches.forEach(match => {
                result = result.replace(`PRESERVE_STYLE_${i}`, match);
            });
        }
    });

    return result;
}

function optimizeImages(html) {
    // Agregar loading="lazy" a imágenes que no lo tienen (excepto hero)
    let result = html;
    const imgRegex = /<img\s+(?![^>]*loading=)([^>]*)>/gi;

    result = result.replace(imgRegex, (match, attrs) => {
        // No agregar lazy loading a imágenes hero o con fetchpriority="high"
        if (attrs.includes('hero') || attrs.includes('fetchpriority="high"')) {
            return match;
        }
        return `<img ${attrs} loading="lazy">`;
    });

    return result;
}

// ============================================
// PROCESAMIENTO PRINCIPAL
// ============================================

function processFiles() {
    const pattern = CONFIG.filter || '**/*.html';
    const options = {
        cwd: CONFIG.rootDir,
        ignore: CONFIG.excludePatterns,
        absolute: true
    };

    log('🚀 Iniciando optimización masiva...', 'info');
    log(`📁 Patrón: ${pattern}`, 'info');
    if (CONFIG.dryRun) {
        log('🔍 Modo DRY-RUN (no se guardarán cambios)', 'warning');
    }

    const files = glob.sync(pattern, options);

    log(`\n📄 Encontradas ${files.length} páginas HTML\n`, 'info');

    let processed = 0;
    let optimized = 0;
    let errors = 0;

    files.forEach((filePath, index) => {
        try {
            const relativePath = path.relative(CONFIG.rootDir, filePath);
            process.stdout.write(`[${index + 1}/${files.length}] ${relativePath}... `);

            const originalHtml = fs.readFileSync(filePath, 'utf8');
            const optimizedHtml = optimizePage(originalHtml, filePath);

            if (originalHtml !== optimizedHtml) {
                if (!CONFIG.dryRun) {
                    fs.writeFileSync(filePath, optimizedHtml, 'utf8');
                }
                log('✅ OPTIMIZADO', 'success');
                optimized++;
            } else {
                log('⏭️  Sin cambios', 'info');
            }

            processed++;

        } catch (error) {
            log(`❌ ERROR: ${error.message}`, 'error');
            errors++;
        }
    });

    // Resumen final
    log('\n' + '='.repeat(60), 'info');
    log('📊 RESUMEN DE OPTIMIZACIÓN', 'info');
    log('='.repeat(60), 'info');
    log(`Total procesadas: ${processed}`, 'info');
    log(`Optimizadas: ${optimized}`, 'success');
    log(`Sin cambios: ${processed - optimized}`, 'info');
    log(`Errores: ${errors}`, errors > 0 ? 'error' : 'info');
    log('='.repeat(60) + '\n', 'info');

    if (CONFIG.dryRun) {
        log('⚠️  Modo DRY-RUN: Los cambios NO se guardaron', 'warning');
        log('💡 Ejecuta sin --dry-run para aplicar cambios', 'info');
    } else {
        log('✅ Optimización completada exitosamente!', 'success');
        log('📝 Recuerda hacer git commit y push de los cambios', 'info');
    }
}

// ============================================
// EJECUCIÓN
// ============================================

// Verificar que glob esté disponible
try {
    require.resolve('glob');
    processFiles();
} catch (e) {
    log('❌ Error: El módulo "glob" no está instalado', 'error');
    log('💡 Ejecuta: npm install glob', 'info');
    log('💡 O usa: npx glob (sin instalación)', 'info');
    process.exit(1);
}
