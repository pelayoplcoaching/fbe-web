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

(function () { if (!window.matchMedia || !matchMedia('(pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return; document.addEventListener('pointermove', function (e) { var c = e.target && e.target.closest && e.target.closest('.plan, .guia, .idea, .correo, .voz, .pegada'); if (!c) return; var r = c.getBoundingClientRect(); c.style.setProperty('--lx', (e.clientX - r.left) + 'px'); c.style.setProperty('--ly', (e.clientY - r.top) + 'px'); }, { passive: true }); })();
