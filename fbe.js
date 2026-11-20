(function () {
  var D = document, R = D.documentElement; R.classList.add('js');
  function $(s) { return D.querySelector(s); } function $$(s) { return [].slice.call(D.querySelectorAll(s)); }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ya'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' }) : null;
  $$('.sube').forEach(function (el) { if (io) io.observe(el); else el.classList.add('ya'); }); setTimeout(function () { $$('.sube').forEach(function (el) { el.classList.add('ya'); }); }, 5000);
  var bt = $('#tema'); try { var g = localStorage.getItem('fbe-web-tema'); if (g === 'dark' || g === 'light') R.dataset.theme = g; } catch (e) {}
  if (bt) bt.addEventListener('click', function () { var osc = R.dataset.theme ? R.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; R.dataset.theme = osc ? 'light' : 'dark'; try { localStorage.setItem('fbe-web-tema', R.dataset.theme); } catch (e) {} });
  var cab = $('.cab'), av = $('#avance'), fijo = $('#fijo'), cierre = $('.cierre'), arr = $('#arriba'), antes = 0;
  function mirar() { var y = window.scrollY || 0, alto = R.scrollHeight - innerHeight; if (av) av.style.transform = 'scaleX(' + (alto > 0 ? Math.min(1, y / alto) : 0) + ')'; cab.classList.toggle('fina', y > 80); if (!$('.menu[open]')) cab.classList.toggle('oculta', y > 500 && y > antes + 4); if (y < antes - 4) cab.classList.remove('oculta'); if (fijo) fijo.classList.toggle('ver', y > 500 && (!cierre || cierre.getBoundingClientRect().top > innerHeight)); if (arr) arr.classList.toggle('ver', y > 1400); antes = y; }
  addEventListener('scroll', mirar, { passive: true }); mirar();
  var menu = $('.menu'); if (menu) menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') menu.open = false; });
})();

(function () { var n = 0; [].forEach.call(document.querySelectorAll('.entrada'), function (e) { n++; e.setAttribute('data-n', (n < 10 ? '0' : '') + n); }); })();
(function () { if (!window.matchMedia || !matchMedia('(pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return; document.addEventListener('pointermove', function (e) { var c = e.target && e.target.closest && e.target.closest('.plan, .guia, .idea, .correo, .voz, .pegada'); if (!c) return; var r = c.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top; c.style.setProperty('--lx', x + 'px'); c.style.setProperty('--ly', y + 'px'); if (c.classList.contains('guia') || c.classList.contains('plan')) { c.style.setProperty('--ry', ((x / r.width - 0.5) * 4).toFixed(2) + 'deg'); c.style.setProperty('--rx', ((0.5 - y / r.height) * 4).toFixed(2) + 'deg'); } }, { passive: true }); })();
(function () {
  var D = document, quieto = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s) { return D.querySelector(s); } function $$(s) { return [].slice.call(D.querySelectorAll(s)); }
  function vuelve(el, c) { if (!el || quieto) return; el.classList.remove(c); void el.offsetWidth; el.classList.add(c); }
  function vigila(el, fn) { if (el && 'MutationObserver' in window) new MutationObserver(fn).observe(el, { childList: true, characterData: true, subtree: true }); }
  /* menu: Escape y clic fuera lo cierran */
  var menu = $('.menu');
  if (menu) { D.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.open) { menu.open = false; var s = menu.querySelector('summary'); if (s) s.focus(); } }); D.addEventListener('click', function (e) { if (menu.open && !menu.contains(e.target)) menu.open = false; }); }
  /* volver arriba: anillo de lectura */
  var arr = $('#arriba'); if (arr) { var mueve = function () { var h = D.documentElement.scrollHeight - innerHeight; arr.style.setProperty('--p', h > 0 ? Math.min(1, (window.scrollY || 0) / h).toFixed(3) : 0); }; addEventListener('scroll', mueve, { passive: true }); mueve(); }
  /* guias: entrada escalonada al filtrar */
  var fil = $('#filtro'); if (fil) fil.addEventListener('click', function (e) { if (!e.target.closest('button')) return; setTimeout(function () { var i = 0; $$('.guia').forEach(function (g) { if (!g.hidden) { g.style.setProperty('--i', i++); vuelve(g, 'entra'); } }); }, 0); });
  /* programas: la recomendacion y el plan recomendado avisan al cambiar */
  var et = $('#elige-t'); vigila(et, function () { vuelve(et, 'cambia'); var t = $('.plan.top'); vuelve(t, 'llega'); });
  /* copiar la analitica */
  var ok = $('#copia-ok'), cp = $('#copia'); vigila(ok, function () { if (cp) cp.classList.toggle('hecho', /Copiada/.test(ok.textContent)); });
  /* calculadora: salto de la cifra */
  ['#prot', '#toma'].forEach(function (s) { var el = $(s); vigila(el, function () { vuelve(el, 'salta'); }); });
  /* dudas: marcar el apartado visible del indice */
  var idx = $$('.indice a[href^="#"]');
  if (idx.length && 'IntersectionObserver' in window) { var mapa = {}; idx.forEach(function (a) { var t = D.getElementById(a.getAttribute('href').slice(1)); if (t) mapa[t.id] = a; });
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting && mapa[en.target.id]) { idx.forEach(function (a) { a.classList.remove('aqui'); }); mapa[en.target.id].classList.add('aqui'); } }); }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(mapa).forEach(function (id) { io.observe(D.getElementById(id)); }); }
})();
(function () { var imgs = [].slice.call(document.querySelectorAll('.foto-i, .foto-c, .foto-b, .foto-g, .foto-p, .banner')); function lista(i) { i.classList.add('cargada'); } imgs.forEach(function (i) { if (i.complete && i.naturalWidth) { i.classList.add('cargada'); i.style.animation = 'none'; } else { i.addEventListener('load', function () { lista(i); }, { once: true }); i.addEventListener('error', function () { lista(i); }, { once: true }); } }); setTimeout(function () { imgs.forEach(lista); }, 6000); })();
