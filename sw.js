/*═══════════════════════════════════════════════════════════════════════════
  GymOS · App móvil — Service worker
  Hace la app instalable, guarda la carcasa para que abra rápido incluso sin
  señal, y muestra los avisos del cronómetro en la barra de notificaciones.
  ══════════════════════════════════════════════════════════════════════════*/

const CACHE = 'gymos-carcasa-v3';
const ARCHIVOS = [
  './',
  './index.html',
  './config.js',
  './manifest.json',
  './icons/icono-192.png',
  './icons/icono-512.png',
  './icons/badge-96.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ARCHIVOS).catch(() => {}))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ll => Promise.all(ll.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Solo se cachea la carcasa propia. Todo lo de Google va siempre a la red. */
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.origin !== self.location.origin) return;

  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copia = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copia)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});

/* Al tocar el aviso se vuelve a la app en vez de abrir otra ventana. */
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(lista => {
      for (const c of lista) {
        if ('focus' in c) return c.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow('./index.html');
    })
  );
});
