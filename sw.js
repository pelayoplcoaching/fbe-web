// Service worker de Fuerza Basada en Evidencia: guarda las calculadoras para usarlas sin conexion.
const V = 'fbe-ebfa12862a';
const PRE = ["./","fbe.js?v=29c28555","img/archivo.woff2","favicon.svg","icono-192.png","manifest.webmanifest","buscar.json","herramientas.html","mis-resultados.html","glosario.html","test-silla.html","calculadora-1rm.html","volumen-semanal.html","cafeina.html","revision-medica.html","zonas-pulso.html","semaforo-dolor.html","test-sppb.html","paron.html","suplementos.html","actividad-oms.html","cintura-altura.html","prension.html","calorias.html","temporizador.html","semana-activa.html","pasos.html","tension.html","equilibrio.html","mi-panel.html","aprende.html","ayuda.html","sin-conexion.html","chequeo.html","empieza-aqui.html","css/p-b2440d2882.css","css/p-f3356d9666.css","css/p-5fdf13997d.css","css/p-747e28884b.css","css/p-5a9919d1e9.css","css/p-c0393d7780.css","css/p-dd6d324d35.css","css/p-fe0e32648f.css","css/p-89b0badc11.css","css/p-2347e6964b.css","css/p-e2a2304bd9.css","css/p-3759d83923.css","css/p-7421a20379.css","css/p-7aa4e8230c.css","css/p-546ca491c7.css","css/p-3d11d47d8f.css","css/p-37755e4737.css","css/p-098c6b7b2c.css","css/p-af217fee4d.css","css/p-3f3392b3c8.css","css/p-01a7fffad7.css","css/p-d5320ebfb2.css","css/p-d11992d50b.css","css/p-e945c510fc.css","css/p-91d3687d6b.css","css/p-47bdff502b.css","css/p-164eace03b.css","css/p-81f1703e07.css","css/p-7486140529.css"];
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
