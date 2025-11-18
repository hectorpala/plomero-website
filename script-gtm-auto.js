/**
 * SCRIPT SEMI-AUTOMÁTICO PARA GTM
 *
 * Este script te guiará paso a paso para crear la configuración.
 * Ejecuta esto en la consola de GTM (F12 en la página de GTM).
 *
 * IMPORTANTE: Este script NO puede crear etiquetas automáticamente
 * porque GTM no expone esas APIs en el frontend.
 *
 * Pero SÍ te mostrará exactamente qué hacer con instrucciones visuales.
 */

console.clear();
console.log('%c🚀 ASISTENTE DE CONFIGURACIÓN GTM', 'background: #0066cc; color: white; font-size: 20px; padding: 10px;');
console.log('');

const config = {
  measurementId: 'G-NSV2K9N2ZD',
  variables: [
    { name: 'DL - Card Name', dataLayerVar: 'card_name' },
    { name: 'DL - Card Position', dataLayerVar: 'card_position' },
    { name: 'DL - Card URL', dataLayerVar: 'card_url' },
    { name: 'DL - Scroll Percentage', dataLayerVar: 'scroll_percentage' }
  ],
  triggers: [
    { name: 'Click - SEO Card', eventName: 'click_seo_card' },
    { name: 'Scroll - Depth Milestone', eventName: 'scroll_depth' }
  ],
  tags: [
    {
      name: 'GA4 - Event - Click SEO Card',
      eventName: 'click_seo_card',
      parameters: [
        { name: 'card_name', variable: 'DL - Card Name' },
        { name: 'card_position', variable: 'DL - Card Position' },
        { name: 'card_url', variable: 'DL - Card URL' }
      ],
      trigger: 'Click - SEO Card'
    },
    {
      name: 'GA4 - Event - Scroll Depth',
      eventName: 'scroll_depth',
      parameters: [
        { name: 'scroll_percentage', variable: 'DL - Scroll Percentage' }
      ],
      trigger: 'Scroll - Depth Milestone'
    }
  ]
};

console.log('%c📋 CONFIGURACIÓN A CREAR:', 'color: #0066cc; font-weight: bold; font-size: 16px;');
console.log('');
console.log('Variables:', config.variables.length);
console.log('Activadores:', config.triggers.length);
console.log('Etiquetas:', config.tags.length);
console.log('ID de medición:', config.measurementId);
console.log('');

// PARTE 1: VARIABLES
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('%c📊 PARTE 1: CREAR VARIABLES (3 minutos)', 'background: #00cc66; color: white; font-size: 16px; padding: 5px;');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('');

console.log('👉 1. En GTM, ve a: %cVariables%c (menú izquierdo)', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;', '');
console.log('👉 2. Haz clic en: %cNueva%c (en "Variables definidas por el usuario")', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;', '');
console.log('');

config.variables.forEach((variable, index) => {
  console.log(`%c✓ Variable ${index + 1}/${config.variables.length}`, 'color: #00cc66; font-weight: bold;');
  console.log('   Nombre:', `%c${variable.name}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('   Tipo:', '%cVariable de capa de datos', 'font-style: italic;');
  console.log('   Nombre de la variable:', `%c${variable.dataLayerVar}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('');
});

console.log('%c💡 TIP:', 'color: #cc6600; font-weight: bold;');
console.log('Copia y pega los valores amarillos exactamente como aparecen.');
console.log('');

// PARTE 2: ACTIVADORES
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('%c⚡ PARTE 2: CREAR ACTIVADORES (2 minutos)', 'background: #cc6600; color: white; font-size: 16px; padding: 5px;');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('');

console.log('👉 1. En GTM, ve a: %cActivadores%c (menú izquierdo)', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;', '');
console.log('👉 2. Haz clic en: %cNuevo', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;');
console.log('');

config.triggers.forEach((trigger, index) => {
  console.log(`%c✓ Activador ${index + 1}/${config.triggers.length}`, 'color: #cc6600; font-weight: bold;');
  console.log('   Nombre:', `%c${trigger.name}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('   Tipo:', '%cEvento personalizado', 'font-style: italic;');
  console.log('   Nombre del evento:', `%c${trigger.eventName}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('');
});

// PARTE 3: ETIQUETAS
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('%c🏷️  PARTE 3: CREAR ETIQUETAS GA4 (5 minutos)', 'background: #0066cc; color: white; font-size: 16px; padding: 5px;');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('');

console.log('👉 1. En GTM, ve a: %cEtiquetas%c (menú izquierdo)', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;', '');
console.log('👉 2. Haz clic en: %cNueva', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;');
console.log('👉 3. Selecciona tipo: %cGoogle Analytics: Evento GA4', 'background: #f0f0f0; padding: 2px 5px; font-weight: bold;');
console.log('');

config.tags.forEach((tag, index) => {
  console.log(`%c✓ Etiqueta ${index + 1}/${config.tags.length}`, 'color: #0066cc; font-weight: bold;');
  console.log('   Nombre:', `%c${tag.name}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('   ID de medición:', `%c${config.measurementId}`, 'background: #ffcccc; padding: 2px 5px; font-weight: bold;');
  console.log('   Nombre del evento:', `%c${tag.eventName}`, 'background: #ffffcc; padding: 2px 5px;');
  console.log('');
  console.log('   Parámetros del evento:');
  tag.parameters.forEach(param => {
    console.log(`      • ${param.name}: %c{{${param.variable}}}`, 'background: #ccffcc; padding: 2px 5px;');
  });
  console.log('');
  console.log('   Activación:', `%c${tag.trigger}`, 'background: #ffcccc; padding: 2px 5px;');
  console.log('');
  console.log('%c   ─────────────────────────────────', 'color: #ccc;');
  console.log('');
});

// RESUMEN FINAL
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('%c📊 RESUMEN DE VALORES PARA COPY-PASTE', 'background: #333; color: white; font-size: 16px; padding: 5px;');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: #666;');
console.log('');

console.log('%cID DE MEDICIÓN (USA ESTE EN AMBAS ETIQUETAS):', 'font-weight: bold; color: #cc0000;');
console.log(`%c${config.measurementId}`, 'background: #ffcccc; padding: 5px 10px; font-size: 16px; font-weight: bold;');
console.log('');

console.log('%cNOMBRES DE VARIABLES DE CAPA DE DATOS:', 'font-weight: bold;');
config.variables.forEach(v => {
  console.log(`  ${v.dataLayerVar}`);
});
console.log('');

console.log('%cNOMBRES DE EVENTOS:', 'font-weight: bold;');
config.triggers.forEach(t => {
  console.log(`  ${t.eventName}`);
});
console.log('');

// FUNCIÓN HELPER
window.copiarValor = function(valor) {
  navigator.clipboard.writeText(valor).then(() => {
    console.log(`✅ Copiado: ${valor}`);
  });
};

console.log('%c💡 TIP ÚTIL:', 'color: #cc6600; font-weight: bold;');
console.log('Para copiar el ID de medición automáticamente, ejecuta:');
console.log(`%ccopiarValor('${config.measurementId}')`, 'background: #f0f0f0; padding: 2px 5px; font-family: monospace;');
console.log('');

console.log('%c✅ DESPUÉS DE CREAR TODO, EJECUTA:', 'color: #00cc66; font-weight: bold; font-size: 14px;');
console.log('%cverificarConfiguracion()', 'background: #f0f0f0; padding: 5px 10px; font-family: monospace; font-size: 14px;');
console.log('');

// Función de verificación
window.verificarConfiguracion = function() {
  console.clear();
  console.log('%c🔍 VERIFICACIÓN DE CONFIGURACIÓN', 'background: #0066cc; color: white; font-size: 18px; padding: 10px;');
  console.log('');
  console.log('Esta función solo muestra un checklist.');
  console.log('Verifica manualmente en GTM que creaste:');
  console.log('');
  console.log('Variables (4):');
  config.variables.forEach(v => {
    console.log(`  ☐ ${v.name}`);
  });
  console.log('');
  console.log('Activadores (2):');
  config.triggers.forEach(t => {
    console.log(`  ☐ ${t.name}`);
  });
  console.log('');
  console.log('Etiquetas (2):');
  config.tags.forEach(t => {
    console.log(`  ☐ ${t.name}`);
  });
  console.log('');
  console.log('%c👉 PRÓXIMO PASO: PUBLICAR', 'background: #00cc66; color: white; padding: 5px; font-weight: bold;');
  console.log('1. Haz clic en "Enviar" (esquina superior derecha)');
  console.log('2. Nombre: "Tracking tarjetas SEO"');
  console.log('3. Publicar');
};

console.log('%c🎯 ¡LISTO! Sigue las instrucciones arriba paso a paso.', 'background: #00cc66; color: white; font-size: 16px; padding: 10px;');
