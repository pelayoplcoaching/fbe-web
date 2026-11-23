// Service worker de Fuerza Basada en Evidencia: guarda las calculadoras para usarlas sin conexion.
const V = 'fbe-08b8afb7bc';
const PRE = ["./", "fbe.css?v=00acec68", "fbe.js?v=00acec68", "img/archivo.woff2", "favicon.svg", "icono-192.png", "manifest.webmanifest", "buscar.json", "herramientas.html", "mis-resultados.html", "glosario.html", "test-silla.html", "calculadora-1rm.html", "volumen-semanal.html", "cafeina.html", "revision-medica.html", "zonas-pulso.html", "semaforo-dolor.html", "test-sppb.html", "paron.html", "suplementos.html", "actividad-oms.html", "cintura-altura.html", "prension.html", "calorias.html", "temporizador.html", "semana-activa.html", "pasos.html", "tension.html", "equilibrio.html", "mi-panel.html", "aprende.html", "ayuda.html", "sin-conexion.html", "chequeo.html", "empieza-aqui.html"];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(PRE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('fbe-') && k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url); if (u.origin !== location.origin) return;
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then(res => { if (res.ok) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); } return res; })
      .catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || caches.match('sin-conexion.html'))));
    return;
  }
  e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => {
    if (res.ok && /\.(css|js|json|woff2|webp|png|jpg|svg)$/.test(u.pathname)) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); }
    return res;
  })));
});
