# Guía para crear nuevas URLs de servicio (Plomero Culiacán Pro)

Esta guía resume la estructura, tono y elementos visuales que deben replicarse cada vez que levantemos una landing nueva (por ejemplo, `servicios/nuevo-servicio/`). Sigue los pasos para mantener coherencia de marca, SEO y performance.

---

## 1. Fundamentos de marca y estilo
- **Tipografía:** usa las fuentes ya autohospedadas (`Inter` para texto, `Montserrat` para encabezados). No agregues nuevas familias.
- **Paleta:** base en `--brand` (`#E36414`) y `--brand-dark`. Fondea secciones alternas con `#f8fafc` para ritmo visual.
- **Voz y tono:** directo, profesional y orientado a urgencias; menciona colonias/localizaciones concretas de Culiacán y promesas de tiempo de llegada (30‑60 min).
- **Iconografía/emoji:** admite íconos simples (⚡, 💬, 🔧) dentro de beneficios y CTAs, nunca abusar.

## 2. Estructura mínima de la página
1. **Head SEO**
   - `<title>` = `Servicio + en Culiacán | Beneficio clave`.
   - `<meta name="description">` resalta urgencia + cobertura + contacto.
   - `<link rel="canonical">` apuntando a la URL final.
   - OG/Twitter tags replican título, descripción e imagen destacada.
   - `lang="es-MX"` en `<html>`.
   - Preloads apuntando a `assets/fonts/...`.
2. **JSON-LD**
   - Bloque base `WebSite` + `BreadcrumbList`.
   - `HomeAndConstructionBusiness` con `aggregateRating`.
   - Agrega `Service` específico del tema y `FAQPage` si hay preguntas.
3. **Hero**
   - Imagen WebP 1200×800 con `fetchpriority="high"`, `loading="eager"` y `alt` descriptivo (menciona acción + ubicación).
   - `h1` con keyword exacta + promesa (“Plomero 24/7 en XYZ”).
   - Subtítulo que mencione síntomas y cobertura por colonias.
   - CTA primaria (`btn-primary`) hacia WhatsApp/Contacto y contacto textual (tel + WhatsApp).
   - Badge visible con rating (`★★★★★ 4.8/5 (150+ reseñas)`).
4. **Bloque de beneficios**
   - Grid de 4‑5 tarjetas con ícono, `h3`, texto corto y lista de bullets.
   - Incluir elementos de confianza: diagnóstico gratis, garantía, facturación, soporte por WhatsApp.
5. **Contenido principal**
   - Sección “Nuestros Servicios” (cards con imagen responsiva, `srcset`, `width/height` e `alt` orientado a acción + ubicación).
   - Texto de apoyo (párrafo largo) para LSI/semántica local.
6. **CTA secundaria / Emergencias**
   - Bloque destacado con botón a WhatsApp, recordatorio de cerrar llave, etc.
7. **SEO Links / interlinking**
   - Grid “Más opciones de plomería” con `<a class="seo-card">` apuntando a otras landings (usa datos `data-card-name` si se requieren para tracking).
8. **Zonas de servicio**
   - Listado de colonias + llamado a contacto si no aparece.
9. **Testimonios / Social proof**
   - 2‑3 testimonios con nombre + colonia.
10. **Contacto + Formulario**
    - Bloque con datos NAP y formulario igual al de la home (envío a WhatsApp + fallback server-side si existe).
    - Mapa embebido (iframe Google Maps) y texto corto con cobertura.
11. **Footer / Nav complementario**
    - Copia de los enlaces globales (`Inicio, Servicios, Blog, Contacto`) y mini-nav adicional si aplica.
12. **Scripts finales**
    - Toggle del menú móvil, handler del formulario y eventos de tracking (WhatsApp, CTA flotante, scroll depth). Valida que dependencias estén encapsuladas en IIFEs para no contaminar el scope global.

## 3. Estándares visuales de imágenes
- Formato principal: WebP, con fallback en `<picture>` si es necesario.
- Define `width` y `height` en cada `<img>` para evitar CLS.
- Usa `loading="lazy"` y `decoding="async"` excepto en la imagen hero (que va eager).
- `alt` debe contener **acción + servicio + ubicación** e incluir palabra clave cuando se justifique.
- Mantén rutas absolutas (`https://plomeroculiacanpro.mx/assets/...`) para que OG/Twitter lean las mismas imágenes.

## 4. SEO on-page y copywriting
- **Keywords principales:** “plomero en Culiacán”, “plomería + [servicio]”, variantes de colonias (Las Quintas, Tres Ríos, Chapultepec, Centro).
- **Keywords secundarias:** tiempos de llegada, 24/7, diagnóstico gratis, garantía 6 meses, facturación SAT.
- **Estructura de encabezados:** un solo `h1`, subsecciones con `h2` y `h3`. `h2` para bloques principales (beneficios, servicios, FAQ, contacto).
- **Preguntas frecuentes (mín. 8):** redacta en formato pregunta/respuesta clara; agrega `itemprop="name"`/`acceptedAnswer` si usas microdatos o `FAQPage` en JSON-LD.
- **Enlaces internos contextualizados:** menciona otras páginas con anchor text descriptivo (ej. “Ver tarifas completas de plomería”).
- **CTA consistente:** repite teléfonos/WhatsApp en hero, secciones intermedias y footer.

## 5. Performance y accesibilidad
- Evita CSS inline salvo casos muy puntuales. Añade reglas a `styles.css` y aprovecha clases existentes.
- Minimiza JS: usa `requestIdleCallback` solo como mejora, nunca como requisito para cargar GTM o CTAs críticos; implementa fallback (`setTimeout`).
- Usa etiquetas semánticas (`section`, `header`, `nav`, `footer`) y atributos `aria` cuando el componente lo necesite (ej. `aria-label` en CTA flotante).
- Verifica contraste (texto oscuro sobre fondo claro) y tamaño mínimo de fuente (≥16 px).

## 6. Checklist previo al deploy
1. Actualiza `lastmod` en `sitemaps/main_sitemap.xml` con la fecha real y agrega entrada para la nueva URL.
2. Ejecuta validación de schema (Rich Results Test) y Lighthouse para confirmar LCP/CLS < threshold.
3. Comprueba que el formulario y CTAs funcionen sin JS bloqueando (al menos un fallback).
4. Corrección ortográfica y uso consistente de acentos (“plomería”, “Culiacán”).
5. Añade anotación en GA4/Search Console con la fecha de publicación.

Con esta guía, cualquier nueva URL mantendrá la identidad visual, tono y optimización técnica de Plomero Culiacán Pro, garantizando resultados coherentes y escalables.
