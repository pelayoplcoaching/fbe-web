// Service worker de Fuerza Basada en Evidencia: guarda las calculadoras para usarlas sin conexion.
const V = 'fbe-97ee87e0be';
const PRE = ["./","fbe.js?v=65e350cd","img/archivo.woff2","favicon.svg","icono-192.png","manifest.webmanifest","buscar.json","herramientas.html","mis-resultados.html","glosario.html","test-silla.html","calculadora-1rm.html","volumen-semanal.html","cafeina.html","revision-medica.html","zonas-pulso.html","semaforo-dolor.html","test-sppb.html","paron.html","suplementos.html","actividad-oms.html","cintura-altura.html","prension.html","calorias.html","temporizador.html","semana-activa.html","pasos.html","tension.html","equilibrio.html","mi-panel.html","aprende.html","ayuda.html","sin-conexion.html","chequeo.html","empieza-aqui.html","css/p-675781b88c.css","css/p-4a765ad14d.css","css/p-5fdf13997d.css","css/p-747e28884b.css","css/p-63da5d23f2.css","css/p-6d8d66be5b.css","css/p-febcda6fe4.css","css/p-071f2ebb5a.css","css/p-5de574bb8e.css","css/p-deca4a3ad1.css","css/p-9824f13b99.css","css/p-60181e7f5f.css","css/p-f25be9b744.css","css/p-9e30903d16.css","css/p-4e357744a5.css","css/p-0bf4c8ab59.css","css/p-22399d90e6.css","css/p-dd265054da.css","css/p-b616227cb3.css","css/p-83e09523ef.css","css/p-c7fb67049e.css","css/p-73e6a5a79a.css","css/p-675f8e03e9.css","css/p-e945c510fc.css","css/p-7bcfb986df.css","css/p-47bdff502b.css","css/p-164eace03b.css","css/p-81f1703e07.css","css/p-aac5bc878c.css"];
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
