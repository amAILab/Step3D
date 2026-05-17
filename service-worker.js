const CACHE_NAME = 'step3d-pwa-v6';
const BASE = '/Step3D/';
const PRECACHE = [
  BASE,
  `${BASE}index.html`,
  `${BASE}app/`,
  `${BASE}account/`,
  `${BASE}account/demo/`,
  `${BASE}gallery/`,
  `${BASE}assets/site.webmanifest`,
  `${BASE}assets/favicon.svg`,
  `${BASE}assets/step3d-logo-192.png`,
  `${BASE}assets/step3d-logo-512.png`,
  `${BASE}assets/pwa-install.js`,
  `${BASE}assets/mobile-readability.css`,
  `${BASE}assets/minimal-ui.css`,
  `${BASE}assets/ux-ui-100.css`,
  `${BASE}assets/step3d-design-system.css`,
  `${BASE}assets/ux-ui-10.css`,
  `${BASE}assets/step3d-premium-system.css`,
  `${BASE}assets/step3d-common.css`,
  `${BASE}assets/step3d-common.js`,
  `${BASE}assets/step3d-minimal.css`
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => Promise.allSettled(PRECACHE.map((url) => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== location.origin || !url.pathname.startsWith(BASE)) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        return response;
      }).catch(() => caches.match(request).then((cached) => cached || caches.match(BASE)))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((response) => {
      if (response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
      }
      return response;
    }))
  );
});
