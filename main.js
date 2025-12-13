// Main JavaScript - Plomero Culiacán Pro
// Loaded with defer for optimal performance
// Last updated: 2025-11-21

// Mobile menu toggle with scroll position preservation
(function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    if (!mobileMenuBtn || !navMenu) return;

    let scrollY = 0;

    function openMenu() {
        scrollY = window.scrollY;
        document.body.style.top = '-' + scrollY + 'px';
        document.body.classList.add('menu-open');
        navMenu.classList.add('active');
        mobileMenuBtn.classList.add('active');
        mobileMenuBtn.setAttribute('aria-expanded', 'true');
        mobileMenuBtn.setAttribute('aria-label', 'Cerrar menú de navegación');
    }

    function closeMenu() {
        const savedScrollY = scrollY;
        document.body.classList.remove('menu-open');
        document.body.style.top = '';
        navMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        mobileMenuBtn.setAttribute('aria-label', 'Abrir menú de navegación');
        window.scrollTo(0, savedScrollY);
    }

    mobileMenuBtn.addEventListener('click', () => {
        if (document.body.classList.contains('menu-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMenu);
    });
})();

// Real-time form validation
(function() {
    const form = document.getElementById('contact-form');
    if (!form) return; // Exit if form doesn't exist

    const nombreField = document.getElementById('nombre');
    const telefonoField = document.getElementById('telefono');
    const emailField = document.getElementById('email');
    const mensajeField = document.getElementById('mensaje');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Validation functions
    const validators = {
        nombre: (value) => value.trim().length >= 2,
        telefono: (value) => /^[0-9]{10}$/.test(value.replace(/\s/g, '')),
        email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        mensaje: (value) => value.trim().length >= 10
    };

    // Validate single field
    function validateField(field, validatorKey) {
        const value = field.value;
        const fieldWrapper = field.closest('.form-field');
        const isValid = validators[validatorKey](value);

        if (value.length === 0) {
            // Empty: neutral state
            fieldWrapper.classList.remove('valid', 'invalid');
        } else if (isValid) {
            // Valid: green checkmark
            fieldWrapper.classList.remove('invalid');
            fieldWrapper.classList.add('valid');
        } else {
            // Invalid: red X
            fieldWrapper.classList.remove('valid');
            fieldWrapper.classList.add('invalid');
        }

        updateSubmitButton();
        return isValid;
    }

    // Check if form is completely valid
    function isFormValid() {
        return validators.nombre(nombreField.value) &&
               validators.telefono(telefonoField.value) &&
               validators.email(emailField.value) &&
               validators.mensaje(mensajeField.value);
    }

    // Enable/disable submit button based on form validity
    function updateSubmitButton() {
        if (isFormValid()) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            submitBtn.style.cursor = 'not-allowed';
        }
    }

    // Add real-time validation listeners
    nombreField.addEventListener('input', () => validateField(nombreField, 'nombre'));
    nombreField.addEventListener('blur', () => validateField(nombreField, 'nombre'));

    telefonoField.addEventListener('input', () => {
        // Only allow numbers
        telefonoField.value = telefonoField.value.replace(/\D/g, '');
        validateField(telefonoField, 'telefono');
    });
    telefonoField.addEventListener('blur', () => validateField(telefonoField, 'telefono'));

    emailField.addEventListener('input', () => validateField(emailField, 'email'));
    emailField.addEventListener('blur', () => validateField(emailField, 'email'));

    mensajeField.addEventListener('input', () => validateField(mensajeField, 'mensaje'));
    mensajeField.addEventListener('blur', () => validateField(mensajeField, 'mensaje'));

    // Initial state: button disabled
    updateSubmitButton();
})();

// Multi-layer lead capture: Netlify Forms + localStorage + GA4 + WhatsApp
(function() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const nombre = formData.get('nombre');
        const telefono = formData.get('telefono');
        const email = formData.get('email');
        const mensaje = formData.get('mensaje');

        const leadData = {
            timestamp: new Date().toISOString(),
            nombre: nombre,
            telefono: telefono,
            email: email,
            mensaje: mensaje,
            source: 'homepage_form',
            url: window.location.href
        };

        // 1. Track lead in GA4 via GTM dataLayer (immediate)
        if (window.dataLayer) {
            window.dataLayer.push({
                'event': 'generate_lead',
                'form_name': 'contact_form_homepage',
                'method': 'netlify_forms',
                'value': 1,
                'currency': 'MXN'
            });
        }

        // 2. Store in localStorage as backup (immediate)
        try {
            const leads = JSON.parse(localStorage.getItem('plomero_leads') || '[]');
            leads.push(leadData);
            localStorage.setItem('plomero_leads', JSON.stringify(leads));
        } catch (e) {
            // console.error('Error storing lead in localStorage:', e);
        }

        // 3. Submit to Netlify Forms (primary backend)
        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData).toString()
            });

            if (response.ok) {
                // Success: show thank you and open WhatsApp
                const whatsappMessage = `Hola! Solicito cotización de servicios de plomería:\n\n` +
                                      `Nombre: ${nombre}\n` +
                                      `Teléfono: ${telefono}\n` +
                                      `Email: ${email}\n` +
                                      `Mensaje: ${mensaje}`;
                const whatsappURL = `https://wa.me/526673922273?text=${encodeURIComponent(whatsappMessage)}`;

                // Open WhatsApp in new tab
                window.open(whatsappURL, '_blank');

                // Redirect to thank you page
                window.location.href = '/gracias';
            } else {
                throw new Error('Netlify form submission failed');
            }
        } catch (error) {
            // console.error('Error submitting to Netlify:', error);

            // Fallback: open WhatsApp directly
            alert('Formulario enviado. Te redirigiremos a WhatsApp.');
            const whatsappMessage = `Hola! Solicito cotización de servicios de plomería:\n\n` +
                                  `Nombre: ${nombre}\n` +
                                  `Teléfono: ${telefono}\n` +
                                  `Email: ${email}\n` +
                                  `Mensaje: ${mensaje}`;
            const whatsappURL = `https://wa.me/526673922273?text=${encodeURIComponent(whatsappMessage)}`;
            window.location.href = whatsappURL;
        }
    });
})();

// CTA fijo con tracking (progressive enhancement: funciona sin JS)
(function(){
  // Progressive Enhancement: hrefs ya funcionan, JS solo agrega tracking
  var PATH = location.pathname;
  var wa = document.getElementById("cta-whatsapp");
  var tl = document.getElementById("cta-llamar");

  // Tracking de clics en GA4 via dataLayer
  window.dataLayer = window.dataLayer || [];
  function pushEvt(type, label) {
    try {
      window.dataLayer.push({
        event: "cta_click",
        cta_type: type,
        cta_label: label,
        page: PATH
      });
    } catch(e) {}
  }

  if (wa) {
    wa.addEventListener("click", function() {
      pushEvt("whatsapp", "cta_floating");
    });
  }
  if (tl) {
    tl.addEventListener("click", function() {
      pushEvt("llamar", "cta_floating");
    });
  }
})();

// Mini footer nav tracking
(function(){
  window.dataLayer=window.dataLayer||[];
  document.querySelectorAll(".site-mini-nav a").forEach(function(a){
    if(a.dataset.navBound==="1") return; a.dataset.navBound="1";
    a.addEventListener("click", function(){
      try{ dataLayer.push({event:"nav_click", nav_label:a.textContent.trim(), nav_href:a.getAttribute("href"), page:location.pathname}); }catch(e){}
    });
  });
})();

// Tracking de tarjetas SEO - diferido con requestIdleCallback
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
  // Tracking de clics en tarjetas "Más opciones de plomería"
  document.querySelectorAll('.seo-card[data-event="click_seo_card"]').forEach(function(card) {
    card.addEventListener('click', function(e) {
      var cardName = this.getAttribute('data-card-name');
      var cardPosition = this.getAttribute('data-card-position');
      var cardHref = this.getAttribute('href');

      try {
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
          'event': 'click_seo_card',
          'card_name': cardName,
          'card_position': cardPosition,
          'card_url': cardHref,
          'page_location': window.location.pathname
        });
      } catch(e) {
        // console.error('Error tracking seo card:', e);
      }
    });
  });

  // Tracking de scroll depth para medir engagement
  var scrollDepths = [25, 50, 75, 90];
  var scrollTracked = {};

  window.addEventListener('scroll', function() {
    var scrollPercent = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);

    scrollDepths.forEach(function(depth) {
      if (scrollPercent >= depth && !scrollTracked[depth]) {
        scrollTracked[depth] = true;
        try {
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            'event': 'scroll_depth',
            'scroll_percentage': depth,
            'page_location': window.location.pathname
          });
        } catch(e) {}
      }
    });
  });
})();

// Exit-Intent Popup - diferido con requestIdleCallback para no bloquear render
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    var popup = document.getElementById('exit-intent-popup');
    if (!popup) return; // Exit if popup doesn't exist

    var closeBtn = document.querySelector('.exit-popup-close');
    var whatsappBtn = document.getElementById('exit-popup-whatsapp');
    var phoneBtn = document.getElementById('exit-popup-phone');
    var hasShown = localStorage.getItem('exitPopupShown');
    var previousActiveElement = null; // For restoring focus on close

    // Get all focusable elements in popup for focus trap
    var focusableElements = popup.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    var firstFocusable = focusableElements[0];
    var lastFocusable = focusableElements[focusableElements.length - 1];
    var isExiting = false;
    var mouseY = 0;
    var timeOnPage = 0;
    var minTimeBeforePopup = 2000; // 2 seconds minimum on page (desktop)
    var minTimeBeforePopupMobile = 7000; // 7 seconds minimum on page (mobile)

    // Mobile detection and scroll tracking
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    var lastScrollY = 0;
    var scrollingUp = false;

    // Check if popup should be shown (only once per session)
    if (hasShown) {
        // console.log('[Exit-Intent] Ya se mostró anteriormente. Para re-probar: localStorage.removeItem("exitPopupShown")');
        return;
    }

    if (isMobile) {
        // console.log('[Exit-Intent] Modo MÓVIL activado. Espera 10+ segundos y haz scroll hacia arriba para activar.');
    } else {
        // console.log('[Exit-Intent] Modo DESKTOP activado. Espera 2+ segundos y mueve mouse hacia arriba para activar.');
    }

    // Track time on page
    var pageLoadTime = Date.now();

    // DESKTOP: Track mouse position continuously
    if (!isMobile) {
        document.addEventListener('mousemove', function(e) {
            mouseY = e.clientY;
        });

        // Detect exit intent - ONLY when mouse leaves through TOP of viewport
        document.addEventListener('mouseout', function(e) {
            // Ignore if already shown
            if (isExiting) return;

            // Get the element the mouse is leaving TO
            var toElement = e.relatedTarget || e.toElement;

            // Check if mouse is leaving the document (null = left viewport)
            // AND mouse Y position is near top (< 10px)
            // AND minimum time on page has passed
            timeOnPage = Date.now() - pageLoadTime;

            // Debug logging
            if (!toElement && mouseY < 10) {
                // console.log('[Exit-Intent] Detectado intento de salida. Tiempo en página:', Math.round(timeOnPage / 1000) + 's');
            }

            if (!toElement &&
                mouseY < 10 &&
                timeOnPage >= minTimeBeforePopup &&
                !isExiting) {
                isExiting = true;
                // console.log('[Exit-Intent] ✅ Mostrando popup (Desktop)!');
                showPopup();
            } else if (!toElement && mouseY < 10 && timeOnPage < minTimeBeforePopup) {
                // console.log('[Exit-Intent] ⏱️  Muy pronto. Necesitas ' + Math.ceil((minTimeBeforePopup - timeOnPage) / 1000) + 's más.');
            }
        });
    }

    // MOBILE: Detect scroll up (exit intent alternative)
    if (isMobile) {
        window.addEventListener('scroll', function() {
            if (isExiting) return;

            var currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
            scrollingUp = currentScrollY < lastScrollY;

            timeOnPage = Date.now() - pageLoadTime;

            // Trigger if: scrolling up + at top 20% of page + 10+ seconds on page
            if (scrollingUp &&
                currentScrollY < (document.documentElement.scrollHeight * 0.2) &&
                timeOnPage >= minTimeBeforePopupMobile &&
                !isExiting) {
                isExiting = true;
                // console.log('[Exit-Intent] ✅ Mostrando popup (Mobile - scroll up)!');
                showPopup();
            } else if (scrollingUp && currentScrollY < (document.documentElement.scrollHeight * 0.2) && timeOnPage < minTimeBeforePopupMobile) {
                // console.log('[Exit-Intent Mobile] ⏱️  Necesitas ' + Math.ceil((minTimeBeforePopupMobile - timeOnPage) / 1000) + 's más.');
            }

            lastScrollY = currentScrollY;
        });
    }

    // Elements to make inert when popup is open (accessibility)
    var mainContent = document.querySelector('main');
    var footer = document.querySelector('footer');
    var floatingBtns = document.querySelectorAll('.floating-btn');

    function setBackgroundInert(inert) {
        if (mainContent) mainContent.inert = inert;
        if (footer) footer.inert = inert;
        floatingBtns.forEach(function(btn) { btn.inert = inert; });
    }

    function showPopup() {
        // Save current focus to restore later
        previousActiveElement = document.activeElement;

        // Block background content for screen readers
        setBackgroundInert(true);

        popup.style.display = 'flex';
        localStorage.setItem('exitPopupShown', 'true');

        // Move focus to first focusable element (close button)
        if (firstFocusable) {
            firstFocusable.focus();
        }

        // Track popup shown event
        try {
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'exit_intent_shown',
                'page_location': window.location.pathname,
                'time_on_page': Math.round(timeOnPage / 1000) + 's'
            });
        } catch(e) {}
    }

    function hidePopup() {
        popup.style.display = 'none';

        // Restore background content accessibility
        setBackgroundInert(false);

        // Restore focus to previously focused element
        if (previousActiveElement && previousActiveElement.focus) {
            previousActiveElement.focus();
        }

        // Track popup close event
        try {
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'exit_intent_closed',
                'page_location': window.location.pathname
            });
        } catch(e) {}
    }

    // Close popup on X button click
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            hidePopup();
        });
    }

    // Close popup on overlay click
    popup.addEventListener('click', function(e) {
        if (e.target === popup) {
            hidePopup();
        }
    });

    // Close popup on ESC key + Focus trap on Tab
    document.addEventListener('keydown', function(e) {
        if (popup.style.display !== 'flex') return;

        // ESC to close
        if (e.key === 'Escape') {
            hidePopup();
            return;
        }

        // Focus trap: Tab key cycles within popup
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                // Shift+Tab: if on first element, go to last
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                }
            } else {
                // Tab: if on last element, go to first
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        }
    });

    // Track WhatsApp CTA click
    if (whatsappBtn) {
        whatsappBtn.addEventListener('click', function() {
            try {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'exit_intent_whatsapp_click',
                    'page_location': window.location.pathname
                });
            } catch(e) {}
        });
    }

    // Track Phone CTA click
    if (phoneBtn) {
        phoneBtn.addEventListener('click', function() {
            try {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'exit_intent_phone_click',
                    'page_location': window.location.pathname
                });
            } catch(e) {}
        });
    }
})();

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                // console.log('SW registered:', registration.scope);
            })
            .catch(err => {
                // console.log('SW registration failed:', err);
            });
    });
}

// Bottom Sheet Cotización Móvil - diferido con requestIdleCallback
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    var trigger = document.getElementById('quote-trigger');
    var overlay = document.getElementById('quote-overlay');
    var sheet = document.getElementById('quote-sheet');
    var closeBtn = document.querySelector('.quote-sheet-close');
    var form = document.getElementById('quote-form');
    var chips = document.querySelectorAll('.quote-chip');

    if (!trigger || !sheet) return;

    var selectedService = '';
    var scrollY = 0;

    // Get focusable elements for focus trap
    var focusableElements = sheet.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    var firstFocusable = focusableElements[0];
    var lastFocusable = focusableElements[focusableElements.length - 1];

    function openSheet() {
        scrollY = window.scrollY;
        document.body.classList.add('quote-sheet-open');
        overlay.classList.add('active');
        sheet.classList.add('active');
        sheet.setAttribute('aria-hidden', 'false');
        overlay.setAttribute('aria-hidden', 'false');

        // Focus first input
        var firstInput = sheet.querySelector('input');
        if (firstInput) {
            setTimeout(function() { firstInput.focus(); }, 100);
        }

        // Track event
        try {
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'quote_sheet_open',
                'page_location': window.location.pathname
            });
        } catch(e) {}
    }

    function closeSheet() {
        document.body.classList.remove('quote-sheet-open');
        overlay.classList.remove('active');
        sheet.classList.remove('active');
        sheet.setAttribute('aria-hidden', 'true');
        overlay.setAttribute('aria-hidden', 'true');
        window.scrollTo(0, scrollY);

        // Return focus to trigger
        trigger.focus();
    }

    // Open on trigger click
    trigger.addEventListener('click', openSheet);

    // Close on overlay click
    overlay.addEventListener('click', closeSheet);

    // Close on X button
    if (closeBtn) {
        closeBtn.addEventListener('click', closeSheet);
    }

    // Handle swipe down to close
    var touchStartY = 0;
    var touchCurrentY = 0;
    var handle = sheet.querySelector('.quote-sheet-handle');

    if (handle) {
        handle.addEventListener('touchstart', function(e) {
            touchStartY = e.touches[0].clientY;
        }, { passive: true });

        handle.addEventListener('touchmove', function(e) {
            touchCurrentY = e.touches[0].clientY;
            var deltaY = touchCurrentY - touchStartY;
            if (deltaY > 0) {
                sheet.style.transform = 'translateY(' + deltaY + 'px)';
            }
        }, { passive: true });

        handle.addEventListener('touchend', function() {
            var deltaY = touchCurrentY - touchStartY;
            if (deltaY > 100) {
                closeSheet();
            }
            sheet.style.transform = '';
            touchStartY = 0;
            touchCurrentY = 0;
        });
    }

    // ESC to close + Focus trap
    document.addEventListener('keydown', function(e) {
        if (!sheet.classList.contains('active')) return;

        if (e.key === 'Escape') {
            closeSheet();
            return;
        }

        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        }
    });

    // Chip selection (single)
    chips.forEach(function(chip) {
        chip.addEventListener('click', function() {
            chips.forEach(function(c) { c.classList.remove('selected'); });
            this.classList.add('selected');
            selectedService = this.getAttribute('data-service');
        });
    });

    // Form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            var nombre = document.getElementById('quote-nombre').value.trim();
            var whatsapp = document.getElementById('quote-whatsapp').value.trim();
            var mensaje = document.getElementById('quote-mensaje').value.trim();

            if (!nombre || !whatsapp) {
                alert('Por favor completa los campos obligatorios.');
                return;
            }

            // Build WhatsApp message
            var msg = '¡Hola! Solicito cotización:\n\n';
            msg += 'Nombre: ' + nombre + '\n';
            msg += 'WhatsApp: ' + whatsapp + '\n';
            if (selectedService) {
                msg += 'Servicio: ' + selectedService + '\n';
            }
            if (mensaje) {
                msg += 'Detalle: ' + mensaje + '\n';
            }

            var whatsappURL = 'https://wa.me/526673922273?text=' + encodeURIComponent(msg);

            // Track lead
            try {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'generate_lead',
                    'form_name': 'quote_sheet_mobile',
                    'method': 'whatsapp',
                    'service': selectedService || 'no_especificado',
                    'value': 1,
                    'currency': 'MXN'
                });
            } catch(e) {}

            // Store lead in localStorage
            try {
                var leads = JSON.parse(localStorage.getItem('plomero_leads') || '[]');
                leads.push({
                    timestamp: new Date().toISOString(),
                    nombre: nombre,
                    whatsapp: whatsapp,
                    servicio: selectedService,
                    mensaje: mensaje,
                    source: 'quote_sheet_mobile',
                    url: window.location.href
                });
                localStorage.setItem('plomero_leads', JSON.stringify(leads));
            } catch(e) {}

            // Open WhatsApp
            window.open(whatsappURL, '_blank');

            // Close sheet and reset form
            closeSheet();
            form.reset();
            chips.forEach(function(c) { c.classList.remove('selected'); });
            selectedService = '';
        });
    }

    // Only allow numbers in WhatsApp field
    var whatsappInput = document.getElementById('quote-whatsapp');
    if (whatsappInput) {
        whatsappInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '');
        });
    }
})();

// Hide floating buttons in critical sections - diferido con requestIdleCallback
(typeof requestIdleCallback === 'function' ? requestIdleCallback : setTimeout)(function() {
    var floatingBtns = document.querySelectorAll('.floating-btn');
    var quoteTrigger = document.getElementById('quote-trigger');
    if (!floatingBtns.length) return;

    // Sections where floating buttons should hide
    var criticalSections = document.querySelectorAll('#contacto, .footer, .contact-form, .map-embed');
    if (!criticalSections.length) return;

    var observer = new IntersectionObserver(function(entries) {
        var anyVisible = entries.some(function(entry) {
            return entry.isIntersecting && entry.intersectionRatio > 0.3;
        });

        floatingBtns.forEach(function(btn) {
            if (anyVisible) {
                btn.style.opacity = '0';
                btn.style.pointerEvents = 'none';
            } else if (!document.body.classList.contains('menu-open')) {
                btn.style.opacity = '1';
                btn.style.pointerEvents = 'auto';
            }
        });

        // Also hide quote trigger in critical sections
        if (quoteTrigger) {
            if (anyVisible) {
                quoteTrigger.style.opacity = '0';
                quoteTrigger.style.pointerEvents = 'none';
            } else if (!document.body.classList.contains('quote-sheet-open')) {
                quoteTrigger.style.opacity = '1';
                quoteTrigger.style.pointerEvents = 'auto';
            }
        }
    }, {
        threshold: [0, 0.3, 0.5],
        rootMargin: '0px 0px -100px 0px'
    });

    criticalSections.forEach(function(section) {
        observer.observe(section);
    });
})();
