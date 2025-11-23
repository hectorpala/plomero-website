#!/usr/bin/env python3
"""
Expande todas las páginas de colonias con la estructura completa de Las Quintas.
Mantiene schemas existentes, reemplaza contenido del body con estructura expandida.
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("servicios/plomero-colonias-culiacan")

# Colonias premium (precios diferentes)
colonias_premium = [
    'las-quintas', 'tres-rios', 'country-tres-rios', 'campestre',
    'colinas-de-san-miguel', 'lomas-del-boulevard', 'chapultepec'
]

# Características específicas por tipo de colonia
def get_caracteristicas(slug, es_premium):
    """Retorna características personalizadas según tipo de colonia"""
    if es_premium:
        return {
            'tipo': 'Residencias Premium',
            'icon': '🏡',
            'descripcion': 'Cientos de trabajos en ' + slug.replace('-', ' ').title(),
            'llegada': '20-30 Minutos',
            'sistemas': 'Sistemas de Alta Presión',
            'sistemas_desc': 'Hidroneumáticos y múltiples niveles',
            'materiales': 'Materiales Premium',
            'materiales_desc': 'Helvex, Grival, Moen, Noritz',
            'garantia': 'Garantía Escrita 6 Meses',
            'garantia_desc': 'Respaldamos nuestro trabajo'
        }
    else:
        return {
            'tipo': 'Zona Establecida',
            'icon': '🏘️',
            'descripcion': 'Experiencia en ' + slug.replace('-', ' ').title(),
            'llegada': '25-35 Minutos',
            'sistemas': 'Todos los Sistemas',
            'sistemas_desc': 'Instalaciones tradicionales y modernas',
            'materiales': 'Materiales de Calidad',
            'materiales_desc': 'Helvex, Grival, marcas nacionales',
            'garantia': 'Garantía 6 Meses',
            'garantia_desc': 'Trabajo respaldado'
        }

def generate_expanded_body(slug, es_premium):
    """Genera el contenido completo del body personalizado por colonia"""

    name = slug.replace('-', ' ').title()
    name_url = slug
    caract = get_caracteristicas(slug, es_premium)

    # Texto personalizado para el hero
    if es_premium:
        hero_subtitle = f"Servicio especializado en residencias premium de {name}. Más de 10 años trabajando en el fraccionamiento. Conocemos sistemas de alta presión, hidroneumáticos, instalaciones de lujo. Llegada en {caract['llegada'].lower()}. Atención 24/7."
        precios_texto = "Los costos pueden ser mayores debido al uso de materiales premium y la complejidad de los sistemas en residencias de lujo."
        why_text = "Acceso Controlado: Conocemos protocolos de la caseta, llegamos identificados profesionalmente."
    else:
        hero_subtitle = f"Servicio confiable de plomería en {name}, Culiacán. Conocemos la zona, sus accesos y características. Llegada en {caract['llegada'].lower()}. Atención 24/7 todos los días del año."
        precios_texto = "El precio incluye diagnóstico, mano de obra, materiales y garantía de 6 meses."
        why_text = "Conocemos la Zona: Calles, accesos, características específicas de cada sector."

    body = f'''<body>
<!-- Google Tag Manager -->
<script>
window.dataLayer = window.dataLayer || [];
if (window.requestIdleCallback) {{
  requestIdleCallback(() => {{
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-W75CRTX5';
    document.head.appendChild(script);
  }});
}}
</script>
<!-- Google Tag Manager (noscript) -->
<noscript>
  <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W75CRTX5"
          height="0" width="0" style="display:none;visibility:hidden"></iframe>
</noscript>

    <nav class="nav">
        <div class="container">
            <div class="nav-wrapper">
                <a href="../../../" class="logo">
                    <img src="../../../logo-plomero-culiacan-pro.webp" alt="Plomero Culiacán Pro - Logo">
                </a>
                <button class="mobile-menu-btn" aria-label="Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
                <ul class="nav-menu">
                    <li><a href="../../../#inicio" class="nav-link">Inicio</a></li>
                    <li><a href="../../../#servicios" class="nav-link">Servicios</a></li>
                    <li><a href="../../../#sobre-nosotros" class="nav-link">Sobre Nosotros</a></li>
                    <li><a href="../../../blog/" class="nav-link">Blog</a></li>
                    <li><a href="../../../#contacto" class="nav-link">Contacto</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header id="inicio" class="hero">
        <div class="container">
            <div class="hero-content">
                <h1 class="fade-in">Plomero Certificado en {name} Culiacán</h1>
                <p class="hero-subtitle fade-in">{hero_subtitle}</p>

    <div style="background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 24px 0; border-left: 4px solid #0066cc;">
        <p style="margin: 0; font-size: 15px; line-height: 1.6;">
            <strong>Nuestros servicios principales:</strong>
            <a href="../../emergencia-24-7/" style="color: #0066cc;">Emergencias 24/7</a>,
            <a href="../../destape-de-drenajes/" style="color: #0066cc;">destape de drenajes</a>,
            <a href="../../reparacion-de-fugas/" style="color: #0066cc;">reparación de fugas</a> y
            <a href="../../deteccion-de-fugas/" style="color: #0066cc;">detección de fugas</a>.
        </p>
    </div>
<p class="hero-contact">WhatsApp: 52 667 163 1231 · Llamadas: 667 163 1231</p>
                <a href="#contacto" class="btn-primary hover-lift">Solicitar Servicio en {name}</a>
            </div>
        </div>
    </header>

    <section class="section section-alt">
        <div class="container">
            <h2>¿Por qué somos el plomero preferido de {name}?</h2>
            <div class="benefits-grid">
                <div class="benefit">
                    <div class="benefit-icon">{caract['icon']}</div>
                    <h3>{caract['tipo']}</h3>
                    <p>{caract['descripcion']}</p>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">⚡</div>
                    <h3>Llegada en {caract['llegada']}</h3>
                    <p>Conocemos accesos y protocolos</p>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">🔧</div>
                    <h3>{caract['sistemas']}</h3>
                    <p>{caract['sistemas_desc']}</p>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">💎</div>
                    <h3>{caract['materiales']}</h3>
                    <p>{caract['materiales_desc']}</p>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">✅</div>
                    <h3>{caract['garantia']}</h3>
                    <p>{caract['garantia_desc']}</p>
                </div>
            </div>
        </div>
    </section>

    <section id="servicios" class="section">
        <div class="container">
            <h2>Servicios Especializados en {name}</h2>
            <div class="grid">
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/reparacion-fugas-420w.webp 420w, ../../../assets/images/reparacion-fugas-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/reparacion-fugas-420w.png"
                                     srcset="../../../assets/images/reparacion-fugas-420w.png 420w, ../../../assets/images/reparacion-fugas-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Plomero reparando fuga en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Reparación de Fugas</h3>
                    <p>Fugas en muros, techos, tuberías. Detección y reparación rápida.</p>
                </div>
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/arreglando-boiler-420w.webp 420w, ../../../assets/images/arreglando-boiler-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/arreglando-boiler-420w.png"
                                     srcset="../../../assets/images/arreglando-boiler-420w.png 420w, ../../../assets/images/arreglando-boiler-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Mantenimiento de boiler en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Mantenimiento de Boilers</h3>
                    <p>Reparación y mantenimiento de boilers de paso y tanque.</p>
                </div>
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/taza-de-baño-420w.webp 420w, ../../../assets/images/taza-de-baño-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/taza-de-baño-420w.png"
                                     srcset="../../../assets/images/taza-de-baño-420w.png 420w, ../../../assets/images/taza-de-baño-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Instalación de grifería en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Instalación de Grifería</h3>
                    <p>Instalación de sanitarios, llaves, regaderas y accesorios.</p>
                </div>
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/destapandodrenaje-420w.webp 420w, ../../../assets/images/destapandodrenaje-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/destapandodrenaje-420w.png"
                                     srcset="../../../assets/images/destapandodrenaje-420w.png 420w, ../../../assets/images/destapandodrenaje-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Destape de drenajes en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Destape de Drenajes</h3>
                    <p>Equipos especializados para destape profesional sin daños.</p>
                </div>
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/reivicion-bajapresion-420w.webp 420w, ../../../assets/images/reivicion-bajapresion-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/reivicion-bajapresion-420w.png"
                                     srcset="../../../assets/images/reivicion-bajapresion-420w.png 420w, ../../../assets/images/reivicion-bajapresion-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Corrección de presión en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Corrección de Presión</h3>
                    <p>Ajuste y optimización de presión de agua.</p>
                </div>
                <div class="card card--img">
                    <div class="service-card">
                        <figure class="media-box">
                            <picture>
                                <source type="image/webp"
                                        srcset="../../../assets/images/emergencia-24-7-nocturna-420w.webp 420w, ../../../assets/images/emergencia-24-7-nocturna-800w.webp 800w"
                                        sizes="(max-width:768px) 100vw, 420px">
                                <img src="../../../assets/images/emergencia-24-7-nocturna-420w.png"
                                     srcset="../../../assets/images/emergencia-24-7-nocturna-420w.png 420w, ../../../assets/images/emergencia-24-7-nocturna-800w.png 800w"
                                     sizes="(max-width:768px) 100vw, 420px"
                                     alt="Emergencias 24/7 en {name}"
                                     width="420" height="420"
                                     loading="lazy" decoding="async">
                            </picture>
                        </figure>
                    </div>
                    <h3>Emergencias 24/7 en {name}</h3>
                    <p>Atención inmediata fugas, inundaciones, drenajes tapados.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="seo-links" aria-labelledby="seo-links-title">
      <h2 id="seo-links-title">Otros servicios en {name}</h2>
      <div class="seo-grid">
        <a class="seo-card" href="../../reparacion-de-fugas/"><span>Reparación de Fugas</span></a>
        <a class="seo-card" href="../../destape-de-drenajes/"><span>Destape de Drenajes</span></a>
        <a class="seo-card" href="../../mantenimiento-de-boiler/"><span>Mantenimiento de Boiler</span></a>
        <a class="seo-card" href="../../emergencia-24-7/"><span>Emergencias 24/7</span></a>
      </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <h2>Conocimiento Específico de {name}</h2>
            <div class="pricing-content">
                <div class="pricing-box">
                    <h3>¿Por qué nos eligen en {name}?</h3>
                    <p><strong>✓ {why_text}</strong></p>
                    <p><strong>✓ Experiencia Local:</strong> Más de 10 años trabajando en {name} y alrededores.</p>
                    <p><strong>✓ Conocemos la Zona:</strong> Calles, accesos, características específicas del área.</p>
                    <p><strong>✓ Materiales de Calidad:</strong> Trabajamos con marcas reconocidas y confiables.</p>
                    <p><strong>✓ Detección Profesional:</strong> Equipos especializados para localizar fugas sin daños.</p>
                    <p><strong>✓ Respeto a tu Hogar:</strong> Trabajamos con protección, limpieza y cuidado.</p>
                    <p><strong>✓ Precios Transparentes:</strong> Cotización clara antes de iniciar el trabajo.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <h2>Ubicación y Tiempo de Llegada</h2>
            <div class="emergency-content">
                <p class="emergency-text">{name} es una de las zonas donde más trabajamos. Conocemos perfectamente la ubicación, los accesos principales y las características del área.</p>
                <p><strong>Tiempo promedio de llegada:</strong> {caract['llegada'].lower()} desde cualquier punto de Culiacán.</p>
                <p><strong>Disponibilidad:</strong> 24 horas, 7 días a la semana (incluyendo fines de semana y festivos).</p>
                <a href="https://wa.me/526671631231?text=Hola,%20necesito%20un%20plomero%20en%20{name.replace(' ', '%20')}" target="_blank" class="btn-primary emergency-btn">WhatsApp: 52 667 163 1231</a>
            </div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <h2>Testimonios de Vecinos de {name}</h2>
            <div class="testimonials">
                <div class="testimonial">
                    <p>"Excelente servicio. Llegaron rápido a {name} y solucionaron la fuga. Muy profesionales y con buen precio."</p>
                    <cite>— Cliente de {name}</cite>
                </div>
                <div class="testimonial">
                    <p>"Ya los he contratado varias veces en {name}. Siempre llegan a tiempo, trabajan limpio y dan garantía. Los recomiendo."</p>
                    <cite>— Residente de {name}</cite>
                </div>
                <div class="testimonial">
                    <p>"Muy contentos con el trabajo. Arreglaron el drenaje que otros no pudieron. Conocen bien la zona y son honestos."</p>
                    <cite>— Familia de {name}</cite>
                </div>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <h2>Preguntas Frecuentes - {name}</h2>
            <div class="faq">
                <div class="faq-item">
                    <h3>¿Cuánto cobran por servicio en {name}?</h3>
                    <p>Los precios son transparentes y justos. Reparación de fuga desde $600, destape desde $400, cambio de WC desde $800. {precios_texto} Te damos presupuesto exacto antes de iniciar.</p>
                </div>
                <div class="faq-item">
                    <h3>¿Cuánto tardan en llegar a {name}?</h3>
                    <p>Llegamos en {caract['llegada'].lower()} a {name}. Conocemos la zona y tenemos disponibilidad 24/7 todos los días del año.</p>
                </div>
                <div class="faq-item">
                    <h3>¿Traen refacciones o hay que comprarlas aparte?</h3>
                    <p>Traemos las refacciones más comunes en nuestra unidad. Si se requiere algo especial, lo conseguimos el mismo día o máximo en 24 horas con proveedores autorizados.</p>
                </div>
                <div class="faq-item">
                    <h3>¿Dan garantía en los trabajos?</h3>
                    <p>Sí, todos nuestros trabajos en {name} incluyen garantía escrita de 6 meses en mano de obra y materiales. Si hay algún problema relacionado con la reparación, regresamos sin costo.</p>
                </div>
                <div class="faq-item">
                    <h3>¿Pueden detectar fugas sin romper?</h3>
                    <p>Sí, usamos equipos profesionales (geófono y termografía) para detectar fugas ocultas sin dañar pisos o muros. Solo abrimos donde está la fuga exacta.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <h2>Cómo Solicitar Servicio en {name}</h2>
            <div class="process-steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Contáctanos por WhatsApp</h3>
                    <p>667 163 1231</p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Dinos tu dirección en {name}</h3>
                    <p>Calle y número</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Describenos el problema</h3>
                    <p>Fuga, drenaje tapado, etc.</p>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>Llegamos en {caract['llegada']}</h3>
                    <p>Identificados y equipados</p>
                </div>
            </div>
        </div>
    </section>

    <section id="sobre-nosotros" class="section">
        <div class="container">
            <h2>Plomeros Especializados en {name}</h2>
            <div class="about-content">
                <p>Llevamos más de 10 años trabajando en {name} y somos el plomero preferido de cientos de residentes. Conocemos las particularidades de la zona y brindamos servicio profesional, rápido y con garantía.</p>
                <p>Llegamos identificados profesionalmente, con unidad rotulada, herramientas especializadas y respeto absoluto a tu hogar. Trabajamos con protección de pisos, limpieza durante el servicio y garantía escrita de 6 meses.</p>
                <div class="features">
                    <div class="feature">
                        <h3>+10 Años</h3>
                        <p>De experiencia</p>
                    </div>
                    <div class="feature">
                        <h3>{caract['llegada']}</h3>
                        <p>Tiempo de llegada</p>
                    </div>
                    <div class="feature">
                        <h3>Garantía 6 Meses</h3>
                        <p>Por escrito</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section aria-label="Servicios relacionados">
        <div class="container">
            <h2>Otras Colonias Donde Trabajamos</h2>
            <ul>
                <li><a href="../las-quintas/">Plomero en Las Quintas</a></li>
                <li><a href="../tres-rios/">Plomero en Tres Ríos</a></li>
                <li><a href="../centro/">Plomero en Centro Culiacán</a></li>
                <li><a href="../../plomero-colonias-culiacan/">Ver todas las colonias</a></li>
            </ul>
        </div>
    </section>

    <section id="contacto" class="section section-alt">
        <div class="container">
            <h2>¿Necesitas Plomero en {name} Ahora?</h2>
            <div class="final-cta">
                <p class="cta-text">Contáctanos por WhatsApp al <strong>667 163 1231</strong> y llegamos en {caract['llegada'].lower()} a {name}.</p>
                <p class="cta-subtitle">Servicio profesional, garantía escrita, materiales de calidad.</p>
                <div class="cta-buttons">
                    <a href="https://wa.me/526671631231?text=Hola,%20necesito%20un%20plomero%20en%20{name.replace(' ', '%20')}" target="_blank" class="btn-primary btn-whatsapp">WhatsApp: 52 667 163 1231</a>
                    <a href="tel:6671631231" class="btn-secondary">Llamar: 667 163 1231</a>
                </div>
            </div>
        </div>
    </section>


        <!-- Mapa Interactivo de la Zona -->
        <section style="margin: 40px 0; padding: 30px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">
            <h2 style="color: #2c3e50; margin-bottom: 20px; font-size: 1.8em; text-align: center;">
                📍 Ubicación y Zona de Servicio en {name}
            </h2>

            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 50%; margin: 0 auto;">
                <p style="color: #555; margin-bottom: 20px; line-height: 1.6;">
                    Nuestro equipo de plomeros profesionales brinda servicio en toda la colonia <strong>{name}</strong>
                    y áreas circundantes. El mapa a continuación muestra nuestra zona de cobertura principal.
                </p>

                <!-- Google Maps Embed -->
                <div style="position: relative; padding-bottom: 28%; height: 0; overflow: hidden; border-radius: 8px;">
                    <iframe src="https://www.google.com/maps?q={name.replace(' ', '+')},+Culiacán,+Sinaloa,+México&output=embed"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                        allowfullscreen=""
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade"
                        title="Mapa de {name}, Culiacán">
                    </iframe>
                </div>

                <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">
                    <p style="margin: 0; color: #2e7d32; font-weight: 600;">
                        ⚡ Tiempo de llegada promedio a {name}: {caract['llegada'].lower()}
                    </p>
                </div>

                <div style="margin-top: 15px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="padding: 15px; background: #fff3e0; border-radius: 6px;">
                        <p style="margin: 0; color: #e65100; font-weight: 600;">📞 Llamada</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Respuesta inmediata 24/7</p>
                    </div>
                    <div style="padding: 15px; background: #e3f2fd; border-radius: 6px;">
                        <p style="margin: 0; color: #1565c0; font-weight: 600;">🚗 Llegada</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Unidad equipada lista</p>
                    </div>
                    <div style="padding: 15px; background: #f3e5f5; border-radius: 6px;">
                        <p style="margin: 0; color: #6a1b9a; font-weight: 600;">🔧 Servicio</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Solución profesional</p>
                    </div>
                </div>
            </div>
        </section>

        <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Plomero Culiacán Pro. Servicio especializado en {name}.</p>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navMenu = document.querySelector('.nav-menu');

        mobileMenuBtn.addEventListener('click', () => {{
            navMenu.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        }});

        // Close mobile menu when clicking a link
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', () => {{
                navMenu.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            }});
        }});
    </script>

<!-- CTA fijo con tracking -->
<style>
  .cta-bar{{position:fixed;right:16px;bottom:16px;display:flex;gap:10px;z-index:9999}}
  .cta-btn{{font:600 15px/1.1 system-ui,-apple-system,Segoe UI,Roboto; padding:12px 14px;border-radius:12px;color:#fff;text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.15)}}
  .cta-wa{{background:#25D366}}
  .cta-tel{{background:#1E40AF}}
</style>
<div class="cta-bar" aria-label="Contacto rápido">
  <a id="cta-whatsapp" class="cta-btn cta-wa" href="#" rel="noopener">💬 WhatsApp</a>
  <a id="cta-llamar"  class="cta-btn cta-tel" href="#" rel="noopener">📞 Llamar</a>
</div>
<script>
(function(){{
  var WA="526671631231", TEL="+52 667 163 1231", PATH=location.pathname;
  var waMsg="Hola, necesito un plomero en {name}, Culiacán";
  var waHref="https://wa.me/"+WA+"?text="+encodeURIComponent(waMsg);
  var telHref="tel:"+TEL.replace(/\\s+/g,'');
  var wa=document.getElementById("cta-whatsapp"); if(wa) wa.href=waHref;
  var tl=document.getElementById("cta-llamar");   if(tl) tl.href=telHref;
  window.dataLayer=window.dataLayer||[];
  function pushEvt(type,label){{try{{window.dataLayer.push({{event:"cta_click",cta_type:type,cta_label:label,page:PATH,colonia:"{name_url}"}});}}catch(e){{}}}}
  if(wa){{ wa.addEventListener("click", function(){{ pushEvt("whatsapp","cta_floating_{name_url}"); }}); }}
  if(tl){{ tl.addEventListener("click", function(){{ pushEvt("llamar","cta_floating_{name_url}"); }}); }}
}})();
</script>
</body>
</html>'''

    return body

# Obtener todas las colonias
colonias = [d for d in base_dir.iterdir() if d.is_dir()]

print(f"🏗️  Expandiendo estructura completa en {len(colonias)} colonias\n")
print(f"📋 Mantendremos los schemas existentes (BreadcrumbList, FAQPage, Service)")
print(f"📄 Expandiremos todo el contenido del body con estructura completa\n")

contador_exitosos = 0

for colonia_dir in sorted(colonias):
    index_file = colonia_dir / "index.html"

    if not index_file.exists():
        print(f"⚠️  {colonia_dir.name} - archivo index.html no encontrado")
        continue

    # Leer contenido actual
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer datos
    colonia_slug = colonia_dir.name
    colonia_name = colonia_slug.replace('-', ' ').title()
    es_premium = colonia_slug in colonias_premium

    # Extraer todo el HEAD (incluyendo schemas)
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if not head_match:
        print(f"⚠️  {colonia_name} - No se pudo extraer el <head>")
        continue

    head_content = head_match.group(1)

    # Generar nuevo body expandido
    new_body = generate_expanded_body(colonia_slug, es_premium)

    # Construir nuevo HTML completo
    new_html = f'''<!DOCTYPE html>
<html lang="es-MX">
<head>{head_content}</head>
{new_body}'''

    # Escribir archivo actualizado
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    tipo = "Premium" if es_premium else "Estándar"
    print(f"✅ {colonia_name} ({tipo}) - Estructura expandida completa")
    contador_exitosos += 1

print(f"\n{'='*70}")
print(f"📊 RESUMEN:")
print(f"  ✅ Páginas expandidas: {contador_exitosos}")
print(f"  📄 Total procesados: {len(colonias)}")
print(f"{'='*70}")
print(f"\n✨ ESTRUCTURA APLICADA:")
print(f"  • Hero con descripción personalizada")
print(f"  • Sección de beneficios (5 items)")
print(f"  • Servicios con imágenes (6 servicios)")
print(f"  • SEO links internos")
print(f"  • Conocimiento específico de la zona")
print(f"  • Ubicación y tiempo de llegada")
print(f"  • Testimonios (3)")
print(f"  • FAQs (5 preguntas)")
print(f"  • Proceso de solicitud (4 pasos)")
print(f"  • Sobre nosotros")
print(f"  • Enlaces a otras colonias")
print(f"  • CTA final")
print(f"  • Mapa interactivo (50% ancho, 28% alto, centrado)")
print(f"  • CTA flotante con tracking")
print(f"\n💎 PERSONALIZACIÓN:")
print(f"  • Premium: sistemas alta presión, materiales premium")
print(f"  • Estándar: sistemas tradicionales, materiales calidad")
print(f"  • Cada colonia con nombre, características únicas")
print(f"\n📐 ESTRUCTURA:")
print(f"  • Las Quintas: 713 líneas (referencia)")
print(f"  • Otras colonias: ahora ~700 líneas cada una")
print(f"  • Contenido 100% consistente y profesional")
