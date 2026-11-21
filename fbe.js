(function () {
  var D = document, R = D.documentElement; R.classList.add('js');
  function $(s) { return D.querySelector(s); } function $$(s) { return [].slice.call(D.querySelectorAll(s)); }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ya'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' }) : null;
  $$('.sube').forEach(function (el) { if (io) io.observe(el); else el.classList.add('ya'); }); setTimeout(function () { $$('.sube').forEach(function (el) { el.classList.add('ya'); }); }, 5000);
  var bt = $('#tema'); try { var g = localStorage.getItem('fbe-web-tema'); if (g === 'dark' || g === 'light') R.dataset.theme = g; } catch (e) {}
  if (bt) bt.addEventListener('click', function () { var osc = R.dataset.theme ? R.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; function cambia() { R.dataset.theme = osc ? 'light' : 'dark'; try { localStorage.setItem('fbe-web-tema', R.dataset.theme); } catch (e) {} }
    if (!D.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches || R.classList.contains('quieto')) { cambia(); return; }
    var r = bt.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2, rad = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y)); R.classList.add('vt-tema');
    var t = D.startViewTransition(cambia); t.ready.then(function () { R.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + rad + 'px at ' + x + 'px ' + y + 'px)'] }, { duration: 600, easing: 'cubic-bezier(.2,.7,.2,1)', pseudoElement: '::view-transition-new(root)' }); }).catch(function () {}); t.finished.then(function () { R.classList.remove('vt-tema'); }, function () { R.classList.remove('vt-tema'); }); });
  var cab = $('.cab'), av = $('#avance'), fijo = $('#fijo'), cierre = $('.cierre'), arr = $('#arriba'), antes = 0;
  function mirar() { var y = window.scrollY || 0, alto = R.scrollHeight - innerHeight; if (av) av.style.transform = 'scaleX(' + (alto > 0 ? Math.min(1, y / alto) : 0) + ')'; cab.classList.toggle('fina', y > 80); if (!$('.menu[open]')) cab.classList.toggle('oculta', y > 500 && y > antes + 4); if (y < antes - 4) cab.classList.remove('oculta'); if (fijo) fijo.classList.toggle('ver', y > 500 && (!cierre || cierre.getBoundingClientRect().top > innerHeight)); if (arr) arr.classList.toggle('ver', y > 1400); antes = y; }
  addEventListener('scroll', mirar, { passive: true }); mirar();
  var menu = $('.menu'); if (menu) menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') menu.open = false; });
})();

(function () { var n = 0; [].forEach.call(document.querySelectorAll('.entrada'), function (e) { if (e.closest('.cierre, .lema-banda')) return; n++; e.setAttribute('data-n', (n < 10 ? '0' : '') + n); }); })();
(function () { if (!window.matchMedia || !matchMedia('(pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return; document.addEventListener('pointermove', function (e) { if (document.documentElement.classList.contains('quieto')) return; var c = e.target && e.target.closest && e.target.closest('.plan, .guia, .idea, .correo, .voz, .pegada'); if (!c) return; var r = c.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top; c.style.setProperty('--lx', x + 'px'); c.style.setProperty('--ly', y + 'px'); if (c.classList.contains('guia') || c.classList.contains('plan')) { c.style.setProperty('--ry', ((x / r.width - 0.5) * 4).toFixed(2) + 'deg'); c.style.setProperty('--rx', ((0.5 - y / r.height) * 4).toFixed(2) + 'deg'); } }, { passive: true }); })();
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
(function () {
  var D = document, R = D.documentElement;
  D.addEventListener('visibilitychange', function () { R.classList.toggle('pestana-oculta', D.hidden); });
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('quieta-z', !e.isIntersecting); }); }, { rootMargin: '120px 0px' });
  function vigilar() { if (!D.getAnimations) return; var cajas = []; D.getAnimations().forEach(function (an) { var t = an.effect && an.effect.target; if (!t || !an.effect.getComputedTiming || an.effect.getComputedTiming().iterations !== Infinity) return; var c = t.closest('section, header, footer, .cinta, aside') || t; if (cajas.indexOf(c) < 0) cajas.push(c); }); cajas.forEach(function (c) { io.observe(c); }); }
  if (D.readyState === 'complete') setTimeout(vigilar, 800); else addEventListener('load', function () { setTimeout(vigilar, 800); });
})();
/* Buscador de toda la web (indice buscar.json, Ctrl+K o /), service worker (calculadoras sin conexion) e instalacion */
(function () {
  var D = document, idx = null, carga = null, dlg, inp, lista, act = -1, res = [], LUPA = '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>';
  function norm(t) { return String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pide() { if (!carga) carga = fetch('buscar.json').then(function (r) { return r.json(); }).then(function (a) { idx = a.map(function (e) { e.nt = norm(e.t); e.nk = norm(e.k + ' ' + e.d + ' ' + e.y); return e; }); return idx; }).catch(function () { carga = null; return []; }); return carga; }
  var SUG = [['empieza-aqui.html', 'Empieza aquí'], ['herramientas.html', 'Herramientas'], ['programas.html', 'Programas'], ['dudas.html', 'Dudas'], ['glosario.html', 'Glosario'], ['mis-resultados.html', 'Mis resultados']];
  var PRI = { 'Herramienta': 0, 'Página': 1, 'Glosario': 2, 'Duda': 3, 'Mito': 4, 'Guía': 5, 'Empieza aquí': 6, 'Boletín': 7 };
  function marca(t, ps) { var s = esc(t), p = ps.filter(function (x) { return x.length > 1; })[0]; if (!p) return s; var i = norm(s).indexOf(p); return i < 0 ? s : s.slice(0, i) + '<mark>' + s.slice(i, i + p.length) + '</mark>' + s.slice(i + p.length); }
  function pinta(ps) {
    act = res.length ? 0 : -1;
    lista.innerHTML = res.length ? res.map(function (e, i) { return '<li role="option" id="bo-' + i + '" aria-selected="' + (i === act) + '"><a href="' + esc(e.u) + '"' + (e.x ? ' target="_blank" rel="noopener"' : '') + '><span class="bo-y">' + esc(e.y) + '</span><b>' + marca(e.t, ps) + '</b>' + (e.d ? '<small>' + esc(e.d.length > 110 ? e.d.slice(0, 108) + '…' : e.d) + '</small>' : '') + '</a></li>'; }).join('') : '<li class="bo-nada">Nada con esas palabras. Prueba con otra o mira las <a href="dudas.html">dudas</a>.</li>';
    inp.setAttribute('aria-activedescendant', act >= 0 ? 'bo-0' : ''); D.getElementById('bo-n').textContent = ps.length ? res.length + (res.length === 1 ? ' resultado' : ' resultados') : 'Atajos';
  }
  function busca(q) {
    var ps = norm(q).trim().split(/\s+/).filter(Boolean);
    if (!ps.length) { res = SUG.map(function (s) { return { t: s[1], u: s[0], d: '', y: 'Atajo' }; }); return pinta([]); }
    res = (idx || []).map(function (e) { var sc = 0; for (var i = 0; i < ps.length; i++) { var p = ps[i], a = e.nt.indexOf(p), b = e.nk.indexOf(p); if (a < 0 && b < 0) return null; sc += a === 0 ? 10 : a > 0 ? (e.nt.charAt(a - 1) === ' ' ? 7 : 4) : 1; } return { e: e, s: sc - (PRI[e.y] || 0) * 0.3 }; }).filter(Boolean).sort(function (x, y) { return y.s - x.s; }).slice(0, 24).map(function (x) { return x.e; });
    pinta(ps);
  }
  function mueve(d) { if (!res.length) return; act = (act + d + res.length) % res.length; [].forEach.call(lista.children, function (li, i) { li.setAttribute('aria-selected', i === act); }); var li = lista.children[act]; inp.setAttribute('aria-activedescendant', li.id); li.scrollIntoView({ block: 'nearest' }); }
  function crea() {
    dlg = D.createElement('dialog'); dlg.className = 'busca-d'; dlg.setAttribute('aria-label', 'Buscar en la web');
    dlg.innerHTML = '<div class="bd-cab"><svg viewBox="0 0 24 24" aria-hidden="true">' + LUPA + '</svg><input type="search" id="bo-q" placeholder="Busca: creatina, rodilla, proteína…" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="bo-l" aria-label="Buscar en la web"><button type="button" class="bd-x" aria-label="Cerrar">Esc</button></div>' + ((D.documentElement.getAttribute('data-fbe-img') || '').indexOf('busca') >= 0 ? '<div class="bd-ilus" aria-hidden="true"><img src="img/web-buscador.webp" alt="" decoding="async"></div>' : '') + '<p class="bd-n" id="bo-n" role="status"></p><ul class="bd-l" id="bo-l" role="listbox" aria-label="Resultados"></ul><p class="bd-pie"><span><kbd>↑</kbd><kbd>↓</kbd> moverte</span><span><kbd>Intro</kbd> abrir</span><span><kbd>Esc</kbd> cerrar</span></p>';
    D.body.appendChild(dlg); inp = dlg.querySelector('input'); lista = dlg.querySelector('ul');
    inp.addEventListener('input', function () { pide().then(function () { busca(inp.value); }); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); mueve(1); } else if (e.key === 'ArrowUp') { e.preventDefault(); mueve(-1); } else if (e.key === 'Enter' && act >= 0) { e.preventDefault(); var a = lista.children[act].querySelector('a'); if (a) a.click(); } else if (e.key === 'Escape') { e.preventDefault(); dlg.close(); } });
    dlg.querySelector('.bd-x').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); else if (e.target.closest('a')) setTimeout(function () { dlg.close(); }, 0); });
  }
  function abre(q) { if (!dlg) crea(); if (!dlg.open) dlg.showModal(); inp.value = q || ''; pide().then(function () { busca(inp.value); }); inp.focus(); inp.select(); }
  window.fbeBusca = abre;
  var cab = D.querySelector('.cab .in'), tema = D.getElementById('tema');
  if (cab) { var b = D.createElement('button'); b.type = 'button'; b.className = 'busca-b'; b.setAttribute('aria-label', 'Buscar en la web'); b.title = 'Buscar (Ctrl+K)'; b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + LUPA + '</svg>'; cab.insertBefore(b, tema && tema.parentNode === cab ? tema : null); b.addEventListener('click', function () { abre(''); }); b.addEventListener('pointerenter', pide, { once: true }); }
  D.addEventListener('keydown', function (e) { var t = e.target, escr = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)); if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) { e.preventDefault(); abre(''); } else if (e.key === '/' && !escr && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); abre(''); } });
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  var dif = null, ins = function (v) { [].forEach.call(D.querySelectorAll('.instala'), function (x) { x.hidden = !v; }); };
  if (matchMedia('(display-mode: standalone)').matches || navigator.standalone) ins(false);
  else {
    addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); dif = e; ins(true); });
    if (/iphone|ipad|ipod/i.test(navigator.userAgent)) [].forEach.call(D.querySelectorAll('.instala'), function (x) { x.hidden = false; var bb = x.querySelector('.instala-b'), p = x.querySelector('.instala-ios'); if (bb) bb.hidden = true; if (p) p.hidden = false; });
  }
  [].forEach.call(D.querySelectorAll('.instala-b'), function (bb) { bb.addEventListener('click', function () { if (!dif) return; dif.prompt(); dif.userChoice.then(function () { dif = null; ins(false); }); }); });
  addEventListener('appinstalled', function () { ins(false); });
})();
/* Ajustes de lectura: tamano del texto, contraste alto y sin animaciones (localStorage fbe-lectura; la clase se pone antes en la cabecera de cada pagina) */
(function () {
  var D = document, R = D.documentElement, K = 'fbe-lectura', a = {}, b, p;
  try { a = JSON.parse(localStorage.getItem(K) || '{}') || {}; } catch (e) {}
  function aplica() { R.classList.toggle('letra-1', a.l === 1); R.classList.toggle('letra-2', a.l === 2); R.classList.toggle('contraste', !!a.c); R.classList.toggle('quieto', !!a.q); }
  function pinta() { if (!p) return; [].forEach.call(p.querySelectorAll('[data-l]'), function (x) { x.setAttribute('aria-pressed', String((a.l || 0) === +x.dataset.l)); }); [].forEach.call(p.querySelectorAll('[data-k]'), function (x) { x.checked = !!a[x.dataset.k]; }); b.classList.toggle('activo', !!(a.l || a.c || a.q)); }
  function guarda() { try { if (a.l || a.c || a.q) localStorage.setItem(K, JSON.stringify(a)); else localStorage.removeItem(K); } catch (e) {} aplica(); pinta(); }
  aplica();
  var cab = D.querySelector('.cab .in'); if (!cab) return;
  b = D.createElement('button'); b.type = 'button'; b.className = 'ajustes-b'; b.setAttribute('aria-label', 'Ajustes de lectura'); b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', 'ajustes-p'); b.title = 'Ajustes de lectura'; b.innerHTML = '<span aria-hidden="true">Aa</span>';
  var tema = D.getElementById('tema'); cab.insertBefore(b, tema && tema.parentNode === cab ? tema : null);
  var img = (R.getAttribute('data-fbe-img') || '').indexOf('ajustes') >= 0 ? '<img class="aj-img" src="img/web-ajustes.webp" alt="" loading="lazy" decoding="async">' : '';
  p = D.createElement('div'); p.className = 'ajustes-p'; p.id = 'ajustes-p'; p.setAttribute('role', 'dialog'); p.setAttribute('aria-label', 'Ajustes de lectura'); p.hidden = true;
  p.innerHTML = img + '<p class="aj-t">Ajustes de lectura</p><div class="aj-fila"><span id="aj-l">Tamaño del texto</span><div class="aj-seg" role="group" aria-labelledby="aj-l"><button type="button" data-l="0">A</button><button type="button" data-l="1">A+</button><button type="button" data-l="2">A++</button></div></div><label class="aj-fila"><span>Contraste alto</span><input type="checkbox" role="switch" data-k="c"></label><label class="aj-fila"><span>Sin animaciones</span><input type="checkbox" role="switch" data-k="q"></label><div class="aj-pie"><button type="button" class="enl-b aj-reset">Volver a lo normal</button><span>Se guardan en este navegador.</span></div>';
  D.body.appendChild(p);
  function abre(v) { p.hidden = !v; b.setAttribute('aria-expanded', String(v)); if (v) { var r = b.getBoundingClientRect(); p.style.top = Math.round(r.bottom + 10) + 'px'; var w = p.offsetWidth; p.style.right = Math.round(Math.min(Math.max(8, innerWidth - r.right - 8), Math.max(8, innerWidth - w - 8))) + 'px'; } }
  b.addEventListener('click', function () { abre(p.hidden); if (!p.hidden) { var f = p.querySelector('[aria-pressed="true"]') || p.querySelector('button'); if (f) f.focus(); } });
  p.addEventListener('click', function (e) { var l = e.target.closest('[data-l]'); if (l) { a.l = +l.dataset.l; guarda(); } if (e.target.closest('.aj-reset')) { a = {}; guarda(); } });
  p.addEventListener('change', function (e) { var k = e.target.dataset.k; if (k) { a[k] = e.target.checked; guarda(); } });
  D.addEventListener('click', function (e) { if (!p.hidden && !p.contains(e.target) && !b.contains(e.target)) abre(false); });
  D.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !p.hidden) { abre(false); b.focus(); } });
  addEventListener('resize', function () { if (!p.hidden) abre(true); });
  pinta();
})();
