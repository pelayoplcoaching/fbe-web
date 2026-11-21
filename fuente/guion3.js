(function () {
  var D = document, reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Entrada de cada bloque y contadores
  function contar(el) { var fin = +el.dataset.n, t0 = performance.now(); if (reducido || fin < 5) { el.textContent = fin; return; } (function paso(t) { var k = Math.min(1, (t - t0) / 1100), v = Math.round(fin * (1 - Math.pow(1 - k, 3))); el.textContent = v; if (k < 1) requestAnimationFrame(paso); })(t0); }
  function ya(el) { el.classList.add('ya'); el.querySelectorAll('[data-n]:not(.entrada)').forEach(contar); }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { ya(e.target); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' }) : null;
  var subes = D.querySelectorAll('.sube'); subes.forEach(function (el) { if (io) io.observe(el); else ya(el); });
  setTimeout(function () { subes.forEach(function (el) { if (!el.classList.contains('ya')) ya(el); }); }, 6000);
  // Recorrido de la semana
  var tabs = [].slice.call(D.querySelectorAll('.tour-lista [role=tab]')), tocado = false, turno = 0, reloj;
  function elegir(i, foco) { tabs.forEach(function (t, k) { var s = k === i; t.setAttribute('aria-selected', s); t.tabIndex = s ? 0 : -1; D.getElementById('p' + k).hidden = !s; }); turno = i; if (foco) tabs[i].focus(); if (matchMedia('(max-width: 760px)').matches && tocado) tabs[i].scrollIntoView({ inline: 'center', block: 'nearest', behavior: reducido ? 'auto' : 'smooth' }); }
  tabs.forEach(function (t, i) { t.addEventListener('click', function () { tocado = true; clearInterval(reloj); elegir(i); });
    t.addEventListener('keydown', function (e) { var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key]; if (!d) return; e.preventDefault(); tocado = true; clearInterval(reloj); elegir((i + d + tabs.length) % tabs.length, true); }); });
  if (!reducido && io && tabs.length) { var visto = new IntersectionObserver(function (es) { es.forEach(function (e) { clearInterval(reloj); if (e.isIntersecting && !tocado) reloj = setInterval(function () { elegir((turno + 1) % tabs.length); }, 4200); }); }, { threshold: .35 }); visto.observe(D.querySelector('.tour')); }
  // Barra de lectura, botón fijo y sección activa
  var av = D.getElementById('avance'), fijo = D.getElementById('fijo'), cierre = D.querySelector('.cierre'), pend = false;
  function mirar() { pend = false; var y = window.scrollY || 0, alto = D.documentElement.scrollHeight - innerHeight; av.style.transform = 'scaleX(' + (alto > 0 ? Math.min(1, y / alto) : 0) + ')'; fijo.classList.toggle('ver', y > 600 && cierre.getBoundingClientRect().top > innerHeight); }
  addEventListener('scroll', function () { if (!pend) { pend = true; requestAnimationFrame(mirar); } }, { passive: true }); mirar();
  var enlaces = [].slice.call(D.querySelectorAll('#nav a[href^="#"]'));
  if (io) { var sec = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) enlaces.forEach(function (a) { a.classList.toggle('aqui', a.getAttribute('href') === '#' + e.target.id); }); }); }, { rootMargin: '-45% 0px -50% 0px' }); enlaces.forEach(function (a) { var s = D.querySelector(a.getAttribute('href')); if (s) sec.observe(s); }); }
  // El menú del móvil se cierra al elegir
  var menu = D.querySelector('.menu'); if (menu) menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') menu.open = false; });
  // El móvil de la portada se inclina un poco con el ratón
  var esc = D.getElementById('escena'), tel = D.getElementById('tel');
  if (esc && tel && !reducido && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    D.querySelector('.hero').addEventListener('pointermove', function (e) { var r = esc.getBoundingClientRect(), x = (e.clientX - r.left - r.width / 2) / r.width, y = (e.clientY - r.top - r.height / 2) / r.height; tel.style.transform = 'rotateY(' + (x * 7).toFixed(2) + 'deg) rotateX(' + (-y * 4).toFixed(2) + 'deg)'; });
    D.querySelector('.hero').addEventListener('pointerleave', function () { tel.style.transform = ''; });
  }
})();
