// Service Worker para Plomero Culiacán Pro
// Última actualización: 2025-11-21
// Estrategia: Cache-First para assets, Network-First para HTML

const CACHE_NAME = 'plomero-culiacan-v7';
const RUNTIME_CACHE = 'plomero-runtime-v7';

// Assets críticos para cachear en instalación
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/styles.min.css',
  '/assets/fonts/inter-400.woff2',
  '/assets/fonts/montserrat-700.woff2',
  '/assets/icons/logo-blue.svg',
  '/assets/icons/icon-192.png',
  '/assets/icons/icon-512.png',
  '/assets/images/hero-plomero-visita-1200w.webp',
  '/assets/images/emergencia-24-7-nocturna-1200w.webp',
  '/manifest.json'
];

// Instalación: Pre-cachear assets críticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activación: Limpiar cachés antiguos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== RUNTIME_CACHE)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Estrategia según tipo de recurso
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Solo cachear requests del mismo origen
  if (url.origin !== location.origin) {
    return;
  }

  // Network-First para páginas HTML (contenido dinámico)
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const clonedResponse = response.clone();
          caches.open(RUNTIME_CACHE).then((cache) => {
            cache.put(request, clonedResponse);
          });
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // Cache-First para assets estáticos (CSS, JS, imágenes, fonts)
  if (
    request.url.includes('/assets/') ||
    request.url.endsWith('.css') ||
    request.url.endsWith('.js') ||
    request.url.endsWith('.webp') ||
    request.url.endsWith('.jpg') ||
    request.url.endsWith('.png') ||
    request.url.endsWith('.svg') ||
    request.url.endsWith('.woff2')
  ) {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request).then((response) => {
            // Solo cachear respuestas exitosas
            if (response.status === 200) {
              const clonedResponse = response.clone();
              caches.open(RUNTIME_CACHE).then((cache) => {
                cache.put(request, clonedResponse);
              });
            }
            return response;
          });
        })
    );
    return;
  }

  // Network-only para formularios y APIs externas
  event.respondWith(fetch(request));
});
