/**
 * SCRIPT DE VERIFICACIÓN AUTOMÁTICA DE TRACKING
 *
 * Ejecuta este script en la consola del navegador para verificar
 * que todos los eventos de tracking están funcionando correctamente.
 *
 * CÓMO USAR:
 * 1. Abre https://plomeroculiacanpro.mx
 * 2. Abre la consola del navegador (F12 o clic derecho → Inspeccionar)
 * 3. Pega este script completo y presiona Enter
 * 4. Sigue las instrucciones en la consola
 */

(function() {
  console.log('%c🔍 VERIFICACIÓN DE TRACKING - INICIO', 'background: #0066cc; color: white; font-size: 16px; padding: 10px;');
  console.log('');

  const results = {
    dataLayer: false,
    gtm: false,
    tracking_script: false,
    seo_cards: 0,
    seo_cards_with_tracking: 0,
    scroll_tracking: false,
    events_detected: []
  };

  // 1. Verificar dataLayer
  console.log('%c1️⃣ Verificando dataLayer...', 'color: #0066cc; font-weight: bold;');
  if (typeof window.dataLayer !== 'undefined') {
    results.dataLayer = true;
    console.log('✅ dataLayer existe');
    console.log('   Elementos en dataLayer:', window.dataLayer.length);
  } else {
    console.log('❌ dataLayer NO existe - GTM no está cargando');
  }
  console.log('');

  // 2. Verificar GTM
  console.log('%c2️⃣ Verificando Google Tag Manager...', 'color: #0066cc; font-weight: bold;');
  if (typeof window.google_tag_manager !== 'undefined') {
    results.gtm = true;
    const gtmId = Object.keys(window.google_tag_manager)[0];
    console.log('✅ GTM cargado correctamente');
    console.log('   Container ID:', gtmId);
  } else {
    console.log('❌ GTM NO está cargado');
  }
  console.log('');

  // 3. Verificar script de tracking
  console.log('%c3️⃣ Verificando script de tracking...', 'color: #0066cc; font-weight: bold;');
  const scripts = document.querySelectorAll('script');
  let foundTrackingScript = false;
  scripts.forEach(script => {
    if (script.textContent.includes('click_seo_card')) {
      foundTrackingScript = true;
    }
  });
  if (foundTrackingScript) {
    results.tracking_script = true;
    console.log('✅ Script de tracking encontrado');
  } else {
    console.log('❌ Script de tracking NO encontrado');
  }
  console.log('');

  // 4. Verificar tarjetas SEO
  console.log('%c4️⃣ Verificando tarjetas SEO...', 'color: #0066cc; font-weight: bold;');
  const seoCards = document.querySelectorAll('.seo-card');
  results.seo_cards = seoCards.length;
  console.log('   Total de tarjetas .seo-card:', seoCards.length);

  const cardsWithTracking = document.querySelectorAll('.seo-card[data-event="click_seo_card"]');
  results.seo_cards_with_tracking = cardsWithTracking.length;

  if (cardsWithTracking.length > 0) {
    console.log('✅ Tarjetas con tracking:', cardsWithTracking.length);
    cardsWithTracking.forEach((card, index) => {
      const cardName = card.getAttribute('data-card-name');
      const cardPosition = card.getAttribute('data-card-position');
      console.log(`   ${index + 1}. ${cardName} (posición ${cardPosition})`);
    });
  } else {
    console.log('❌ NO se encontraron tarjetas con atributos de tracking');
  }
  console.log('');

  // 5. Verificar listeners de scroll
  console.log('%c5️⃣ Verificando tracking de scroll...', 'color: #0066cc; font-weight: bold;');
  // Simular scroll para verificar
  const originalScrollY = window.scrollY;
  window.scrollTo(0, 100);
  setTimeout(() => {
    window.scrollTo(0, originalScrollY);
  }, 100);
  console.log('✅ Listener de scroll debería estar activo');
  console.log('   (Verificar en dataLayer después de hacer scroll)');
  console.log('');

  // 6. Listener temporal para capturar eventos
  console.log('%c6️⃣ Configurando listener de eventos...', 'color: #0066cc; font-weight: bold;');
  console.log('   Ahora haz clic en una tarjeta SEO para probar...');
  console.log('');

  const originalPush = window.dataLayer.push;
  window.dataLayer.push = function() {
    const data = arguments[0];

    if (data && data.event === 'click_seo_card') {
      results.events_detected.push('click_seo_card');
      console.log('%c🎉 EVENTO DETECTADO: click_seo_card', 'background: #00cc66; color: white; font-size: 14px; padding: 5px;');
      console.log('   Datos del evento:', data);
      console.log('');
    }

    if (data && data.event === 'scroll_depth') {
      if (!results.events_detected.includes('scroll_depth')) {
        results.events_detected.push('scroll_depth');
      }
      console.log('%c📏 EVENTO DETECTADO: scroll_depth', 'background: #cc6600; color: white; font-size: 14px; padding: 5px;');
      console.log('   Profundidad:', data.scroll_percentage + '%');
      console.log('');
    }

    return originalPush.apply(this, arguments);
  };

  // Mostrar resumen inicial
  console.log('%c📊 RESUMEN DE VERIFICACIÓN', 'background: #333; color: white; font-size: 16px; padding: 10px;');
  console.log('');
  console.table({
    'dataLayer': results.dataLayer ? '✅ Sí' : '❌ No',
    'GTM cargado': results.gtm ? '✅ Sí' : '❌ No',
    'Script tracking': results.tracking_script ? '✅ Sí' : '❌ No',
    'Tarjetas totales': results.seo_cards,
    'Tarjetas con tracking': results.seo_cards_with_tracking
  });
  console.log('');

  // Instrucciones finales
  console.log('%c📝 PRÓXIMOS PASOS:', 'color: #0066cc; font-weight: bold; font-size: 14px;');
  console.log('');
  console.log('1. 🖱️  Haz clic en una tarjeta de "Más opciones de plomería"');
  console.log('2. 📜 Haz scroll hasta el 50% de la página');
  console.log('3. 👀 Observa los eventos que aparecen arriba');
  console.log('');
  console.log('Para ver el dataLayer actual, ejecuta:');
  console.log('%cdataLayer', 'background: #f0f0f0; color: #333; padding: 2px 5px; font-family: monospace;');
  console.log('');
  console.log('Para ver el último evento, ejecuta:');
  console.log('%cdataLayer[dataLayer.length - 1]', 'background: #f0f0f0; color: #333; padding: 2px 5px; font-family: monospace;');
  console.log('');

  // Función auxiliar para mostrar resumen final
  window.mostrarResumenTracking = function() {
    console.log('%c📊 RESUMEN FINAL DE TRACKING', 'background: #0066cc; color: white; font-size: 16px; padding: 10px;');
    console.log('');
    console.log('Eventos detectados:', results.events_detected.length);
    results.events_detected.forEach(event => {
      console.log('  ✅', event);
    });
    console.log('');

    if (results.events_detected.includes('click_seo_card') && results.events_detected.includes('scroll_depth')) {
      console.log('%c🎉 ¡TODO FUNCIONA PERFECTAMENTE!', 'background: #00cc66; color: white; font-size: 18px; padding: 10px;');
      console.log('');
      console.log('✅ Tracking de clics: FUNCIONANDO');
      console.log('✅ Tracking de scroll: FUNCIONANDO');
      console.log('');
      console.log('Ahora puedes verificar en Google Analytics:');
      console.log('1. GA4 > Informes > Tiempo real');
      console.log('2. Busca los eventos: click_seo_card y scroll_depth');
    } else if (results.events_detected.includes('click_seo_card')) {
      console.log('%c⚠️ TRACKING PARCIAL', 'background: #cc6600; color: white; font-size: 16px; padding: 10px;');
      console.log('');
      console.log('✅ Tracking de clics: FUNCIONANDO');
      console.log('❌ Tracking de scroll: Haz scroll para activarlo');
    } else if (results.events_detected.includes('scroll_depth')) {
      console.log('%c⚠️ TRACKING PARCIAL', 'background: #cc6600; color: white; font-size: 16px; padding: 10px;');
      console.log('');
      console.log('❌ Tracking de clics: Haz clic en una tarjeta SEO');
      console.log('✅ Tracking de scroll: FUNCIONANDO');
    } else {
      console.log('%c❌ NO SE DETECTARON EVENTOS', 'background: #cc0000; color: white; font-size: 16px; padding: 10px;');
      console.log('');
      console.log('Verifica:');
      console.log('1. ¿Hiciste clic en una tarjeta?');
      console.log('2. ¿Hiciste scroll?');
      console.log('3. ¿El script de tracking está en el HTML?');
    }
  };

  console.log('%c💡 TIP:', 'color: #cc6600; font-weight: bold;');
  console.log('Después de hacer clic y scroll, ejecuta:');
  console.log('%cmostrarResumenTracking()', 'background: #f0f0f0; color: #333; padding: 2px 5px; font-family: monospace;');
  console.log('');

})();
