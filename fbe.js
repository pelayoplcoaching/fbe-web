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
  function vigilar() { if (!D.getAnimations) return; var cajas = []; D.getAnimations().forEach(function (an) { var t = an.effect && an.effect.target; if (!t || !an.effect.getComputedTiming || an.effect.getComputedTiming().iterations !== Infinity) return; var c = t.closest('section, header, footer, .cinta, aside, .hero') || t; if (cajas.indexOf(c) < 0) cajas.push(c); }); cajas.forEach(function (c) { io.observe(c); }); }
  if (D.readyState === 'complete') setTimeout(vigilar, 800); else addEventListener('load', function () { setTimeout(vigilar, 800); });
})();
/* Buscador de toda la web (indice buscar.json, Ctrl+K o /), service worker (calculadoras sin conexion) e instalacion */
(function () {
  var D = document, idx = null, carga = null, dlg, inp, lista, act = -1, res = [], LUPA = '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>';
  function norm(t) { return String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pide() { if (!carga) carga = fetch('buscar.json').then(function (r) { return r.json(); }).then(function (a) { idx = a.map(function (e) { e.nt = norm(e.t); e.nk = norm(e.k + ' ' + e.d + ' ' + e.y); return e; }); return idx; }).catch(function () { carga = null; return []; }); return carga; }
  var SUG = [['empieza-aqui.html', 'Empieza aquí'], ['herramientas.html', 'Herramientas'], ['programas.html', 'Programas'], ['dudas.html', 'Dudas'], ['mi-panel.html', 'Mi panel'], ['temporizador.html', 'Temporizador'], ['mis-resultados.html', 'Mis resultados']];
  var PRI = { 'Herramienta': 0, 'Página': 1, 'Glosario': 2, 'Duda': 3, 'Mito': 4, 'Guía': 5, 'Empieza aquí': 6, 'Boletín': 7, 'Fuente': 8, 'Receta': 9, 'Vídeo': 10, 'Acción': -1 };
  function marca(t, ps) { var s = esc(t), p = ps.filter(function (x) { return x.length > 1; })[0]; if (!p) return s; var i = norm(s).indexOf(p); return i < 0 ? s : s.slice(0, i) + '<mark>' + s.slice(i, i + p.length) + '</mark>' + s.slice(i + p.length); }
  function pinta(ps) {
    act = res.length ? 0 : -1;
    lista.innerHTML = res.length ? res.map(function (e, i) { return '<li role="option" data-k="' + ({ 'Herramienta': 'h', 'Página': 'p', 'Glosario': 'g', 'Duda': 'd', 'Mito': 'm', 'Guía': 'u', 'Empieza aquí': 'e', 'Boletín': 'b', 'Fuente': 'f', 'Atajo': 'a', 'Receta': 'r', 'Vídeo': 'v', 'Acción': 'x' }[e.y] || 'p') + '" id="bo-' + i + '" aria-selected="' + (i === act) + '"><a href="' + esc(e.u) + '"' + (e.x ? ' target="_blank" rel="noopener"' : '') + '><span class="bo-y">' + esc(e.y) + '</span><b>' + marca(e.t, ps) + '</b>' + (e.d ? '<small>' + esc(e.d.length > 110 ? e.d.slice(0, 108) + '…' : e.d) + '</small>' : '') + '</a></li>'; }).join('') : '<li class="bo-nada">Nada con esas palabras. Prueba con otra o mira las <a href="dudas.html">dudas</a>.</li>';
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
  var D = document, R = D.documentElement, K = 'fbe-lectura', a = {}, b, p, OIR = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
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
  p.innerHTML = img + '<p class="aj-t">Ajustes de lectura</p><div class="aj-fila"><span id="aj-l">Tamaño del texto</span><div class="aj-seg" role="group" aria-labelledby="aj-l"><button type="button" data-l="0">A</button><button type="button" data-l="1">A+</button><button type="button" data-l="2">A++</button></div></div><label class="aj-fila"><span>Contraste alto</span><input type="checkbox" role="switch" data-k="c"></label><label class="aj-fila"><span>Sin animaciones</span><input type="checkbox" role="switch" data-k="q"></label>' + (OIR ? '<button type="button" class="aj-oir" aria-pressed="false"><span>Escuchar esta página</span></button>' : '') + '<div class="aj-pie"><button type="button" class="enl-b aj-reset">Volver a lo normal</button><span>Se guardan en este navegador.</span></div>';
  D.body.appendChild(p);
  function abre(v) { p.hidden = !v; b.setAttribute('aria-expanded', String(v)); if (v) { var r = b.getBoundingClientRect(); p.style.top = Math.round(r.bottom + 10) + 'px'; var w = p.offsetWidth; p.style.right = Math.round(Math.min(Math.max(8, innerWidth - r.right - 8), Math.max(8, innerWidth - w - 8))) + 'px'; } }
  b.addEventListener('click', function () { abre(p.hidden); if (!p.hidden) { var f = p.querySelector('[aria-pressed="true"]') || p.querySelector('button'); if (f) f.focus(); } });
  p.addEventListener('click', function (e) { var l = e.target.closest('[data-l]'); if (l) { a.l = +l.dataset.l; guarda(); } if (e.target.closest('.aj-reset')) { a = {}; guarda(); } });
  p.addEventListener('change', function (e) { var k = e.target.dataset.k; if (k) { a[k] = e.target.checked; guarda(); } });
  function texto() { var m = D.querySelector('main') || D.body, h = D.querySelector('h1'), s = D.querySelector('.hero .sub'), c = m.cloneNode(true); [].forEach.call(c.querySelectorAll('script, style, svg, button, nav, form, .fuentes-t, .oculto, [aria-hidden="true"], [hidden]'), function (x) { x.remove(); }); return [h ? h.innerText : '', s ? s.innerText : '', c.innerText].join('. ').replace(/\s+/g, ' ').trim(); }
  function para(o) { try { speechSynthesis.cancel(); } catch (e) {} if (o) { o.setAttribute('aria-pressed', 'false'); o.querySelector('span').textContent = 'Escuchar esta página'; } }
  p.addEventListener('click', function (e) { var o = e.target.closest('.aj-oir'); if (!o) return; if (o.getAttribute('aria-pressed') === 'true') { para(o); return; }
    var ss = speechSynthesis, vs = ss.getVoices().filter(function (v) { return /^es/i.test(v.lang); }), voz = vs.filter(function (v) { return /es-ES/i.test(v.lang); })[0] || vs[0], fr = texto().match(/[^.!?;:]+[.!?;:]*\s*/g) || [], tr = [], cur = '';
    fr.forEach(function (f) { if ((cur + f).length > 220 && cur) { tr.push(cur); cur = f; } else cur += f; }); if (cur) tr.push(cur);
    ss.cancel(); tr.forEach(function (t, i) { var u = new SpeechSynthesisUtterance(t.trim()); u.lang = 'es-ES'; if (voz) u.voice = voz; if (i === tr.length - 1) u.onend = function () { para(o); }; ss.speak(u); });
    o.setAttribute('aria-pressed', 'true'); o.querySelector('span').textContent = 'Parar la lectura'; });
  addEventListener('pagehide', function () { if (OIR) para(null); });
  D.addEventListener('click', function (e) { if (!p.hidden && !p.contains(e.target) && !b.contains(e.target)) abre(false); });
  D.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !p.hidden) { abre(false); b.focus(); } });
  addEventListener('resize', function () { if (!p.hidden) abre(true); });
  pinta();
})();
/* Compartir la pagina (menu del movil o copiar el enlace) */
(function () {
  var D = document, t = D.querySelector('.hero.mini .txt'); if (!t || !(navigator.share || (navigator.clipboard && navigator.clipboard.writeText))) return;
  var b = D.createElement('button'); b.type = 'button'; b.className = 'compartir-b'; b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg><span>Compartir</span>';
  var c = t.querySelector('.cta'); (c || t).appendChild(b);
  b.addEventListener('click', function () { var u = location.href.split('#')[0], s = b.querySelector('span'); if (navigator.share) navigator.share({ title: D.title, url: u }).catch(function () {}); else navigator.clipboard.writeText(u).then(function () { s.textContent = 'Enlace copiado'; setTimeout(function () { s.textContent = 'Compartir'; }, 1600); }, function () {}); });
})();
/* Menu con desplegables (Aprende y Herramientas): clic o teclado lo abren y cierran; con raton tambien al pasar.
   Escape, clic fuera o salir con el tabulador lo cierran. La seccion actual se marca en el boton. */
(function () {
  var gs = [].slice.call(document.querySelectorAll('.nav-g')); if (!gs.length) return;
  function cierra(g, foco) { var b = g.querySelector('.nav-b'), m = g.querySelector('.nav-m'); if (b.getAttribute('aria-expanded') !== 'true') return; b.setAttribute('aria-expanded', 'false'); m.hidden = true; g.classList.remove('abierto'); if (foco) b.focus(); }
  function abre(g) { gs.forEach(function (x) { if (x !== g) cierra(x); }); g.querySelector('.nav-b').setAttribute('aria-expanded', 'true'); g.querySelector('.nav-m').hidden = false; g.classList.add('abierto'); }
  gs.forEach(function (g) {
    var b = g.querySelector('.nav-b'), m = g.querySelector('.nav-m'), t, porRaton = 0;
    if (m.querySelector('[aria-current="page"]')) b.classList.add('aqui');
    b.addEventListener('click', function () { if (Date.now() - porRaton < 700) return; b.getAttribute('aria-expanded') === 'true' ? cierra(g) : abre(g); });
    g.addEventListener('pointerenter', function (e) { if (e.pointerType !== 'mouse') return; clearTimeout(t); if (b.getAttribute('aria-expanded') !== 'true') { porRaton = Date.now(); abre(g); } });
    g.addEventListener('pointerleave', function (e) { if (e.pointerType !== 'mouse') return; t = setTimeout(function () { cierra(g); }, 220); });
    g.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { cierra(g, true); return; }
      if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && b.getAttribute('aria-expanded') === 'true') {
        var ls = [].slice.call(m.querySelectorAll('a')), i = ls.indexOf(document.activeElement); e.preventDefault();
        var j = e.key === 'ArrowDown' ? (i + 1) % ls.length : (i <= 0 ? ls.length - 1 : i - 1); ls[j].focus();
      } else if (e.key === 'ArrowDown' && document.activeElement === b) { e.preventDefault(); abre(g); var p = m.querySelector('a'); if (p) p.focus(); }
    });
    g.addEventListener('focusout', function (e) { if (!g.contains(e.relatedTarget)) cierra(g); });
  });
  document.addEventListener('click', function (e) { gs.forEach(function (g) { if (!g.contains(e.target)) cierra(g); }); });
})();

/* app.js (22/11/2026): la web como app. Historial, favoritos, Mis datos, logros, avisos, acciones rapidas y modo instalada.
   Todo se guarda en este dispositivo (localStorage fbe-visto, fbe-favoritos, fbe-perfil, fbe-logros, fbe-vistas). */
(function () {
  var D = document, R = D.documentElement;
  function lee(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function pon(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  var PAG = location.pathname.split('/').pop() || 'index.html'; if (PAG.indexOf('.') < 0) PAG += '.html';
  var APP = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  if (APP) R.classList.add('es-app');
  var SIN = /^(index|mi-panel|404|gracias|gracias-plaza|gracias-boletin|pedir-plaza|privacidad|sin-conexion)\.html$/;
  var ESTRELLA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/></svg>';
  var h1 = D.querySelector('h1'), TIT = (h1 ? h1.textContent : D.title).replace(/\s+/g, ' ').trim();
  var miga = D.querySelector('.hero.mini .miga'), NOM = miga ? miga.textContent.split('/').pop().trim() : TIT;
  var TIPO = D.querySelector('.tool-res') ? 'Herramienta' : 'Página';

  /* ---- avisos (toast) ---- */
  var caja = null;
  var AV_IC = { logro: '<path d="M8 3h8v5a4 4 0 0 1-8 0zM8 5H5a3 3 0 0 0 3 4M16 5h3a3 3 0 0 1-3 4M12 12v4M8.5 20h7M10 16h4v4h-4z"/>', fav: '<path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
    red: '<path d="M3 3l18 18M8.5 16.5a5 5 0 0 1 7 0M5 13a10 10 0 0 1 3.5-2.3M19 13a10 10 0 0 0-5-2.7M2 9.5a15 15 0 0 1 4-2.8M22 9.5a15 15 0 0 0-11-4.3"/><circle cx="12" cy="20" r=".6"/>',
    ok: '<path d="M5 12.5l4.5 4.5L19 7.5"/>', nueva: '<path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v5h-5"/>', info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.6v.1"/>' };
  function quieto() { return R.classList.contains('quieto') || !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }
  function confeti(t) {
    if (quieto()) return; var c = D.createElement('span'); c.className = 'confeti'; c.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 16; i++) { var p = D.createElement('i'), a = (i / 16) * Math.PI * 2 + (i % 2 ? .22 : -.16), r = 44 + (i * 37 % 42); p.style.setProperty('--x', Math.round(Math.cos(a) * r) + 'px'); p.style.setProperty('--y', Math.round(Math.sin(a) * r * .7 - 34) + 'px'); p.style.setProperty('--g', (120 + i * 97 % 360) + 'deg'); p.style.animationDelay = (i % 4) * 30 + 'ms'; p.dataset.c = i % 4; c.appendChild(p); }
    t.appendChild(c); setTimeout(function () { c.remove(); }, 1500);
  }
  function toast(txt, bt, fn, ms, k, tit) {
    if (!caja) { caja = D.createElement('div'); caja.className = 'aviso-app'; caja.setAttribute('role', 'status'); caja.setAttribute('aria-live', 'polite'); D.body.appendChild(caja); }
    var t = D.createElement('div'); t.className = 'aviso-t'; k = AV_IC[k] ? k : 'info'; t.dataset.k = k;
    var ic = D.createElement('i'); ic.className = 'aviso-ic'; ic.setAttribute('aria-hidden', 'true'); ic.innerHTML = '<svg viewBox="0 0 24 24">' + AV_IC[k] + '</svg>'; t.appendChild(ic);
    var s = D.createElement('span'); if (tit) { var sm = D.createElement('small'); sm.textContent = tit; s.appendChild(sm); } s.appendChild(D.createTextNode(txt)); t.appendChild(s);
    if (bt) { var b = D.createElement('button'); b.type = 'button'; b.textContent = bt; b.addEventListener('click', function () { t.remove(); if (fn) fn(); }); t.appendChild(b); }
    caja.appendChild(t); if (ms !== 0) { t.classList.add('con-tiempo'); t.style.setProperty('--ms', (ms || 4500) + 'ms'); setTimeout(function () { t.remove(); }, ms || 4500); }
    if (k === 'logro') confeti(t); return t;
  }

  /* ---- historial: seguir donde lo dejaste ---- */
  if (!SIN.test(PAG)) {
    var V = lee('fbe-visto', []).filter(function (x) { return x && x.u !== PAG; }); V.unshift({ u: PAG, t: NOM, k: TIPO, f: Date.now() }); pon('fbe-visto', V.slice(0, 12));
    if (TIPO === 'Herramienta') { var hv = lee('fbe-vistas', []); if (hv.indexOf(PAG) < 0) { hv.push(PAG); pon('fbe-vistas', hv); } }
  }

  /* ---- favoritos ---- */
  function favs() { return lee('fbe-favoritos', []); }
  function esFav(u) { return favs().some(function (x) { return x.u === u; }); }
  function cambiaFav(u, t, k) { var F = favs(), i = -1; F.forEach(function (x, n) { if (x.u === u) i = n; }); if (i >= 0) F.splice(i, 1); else F.unshift({ u: u, t: t, k: k, f: Date.now() }); pon('fbe-favoritos', F.slice(0, 60)); logros(); return i < 0; }
  function botonFav(u, t, k, clase, largo) {
    var b = D.createElement('button'); b.type = 'button'; b.className = clase; b.innerHTML = ESTRELLA + '<span' + (largo ? '' : ' class="oculto"') + '></span>';
    function pinta() { var on = esFav(u); b.setAttribute('aria-pressed', String(on)); b.querySelector('span').textContent = largo ? (on ? 'Guardado' : 'Guardar') : (on ? 'Quitar de favoritos: ' : 'Guardar en favoritos: ') + t; }
    b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); var on = cambiaFav(u, t, k); pinta(); b.classList.remove('late'); void b.offsetWidth; b.classList.add('late'); if (on && !lee('fbe-fav-visto', 0)) { pon('fbe-fav-visto', 1); toast('Tus favoritos están en Mi panel.', 'Ver', function () { location.href = 'mi-panel.html#pn-fav'; }, 4500, 'fav', 'Guardado'); } });
    pinta(); return b;
  }
  var txt = D.querySelector('.hero.mini .txt');
  if (txt && !SIN.test(PAG)) { var cta = txt.querySelector('.cta') || txt; cta.appendChild(botonFav(PAG, NOM, TIPO, 'compartir-b fav-b', true)); }
  function favItems() {
    [].forEach.call(D.querySelectorAll('#vid-rej .vc'), function (li) { if (li.querySelector('.fav-i')) return; var a = li.querySelector('a[data-v]'), b = li.querySelector('b'); if (a && b) li.appendChild(botonFav('videos.html#v-' + a.dataset.v, b.textContent, 'Vídeo', 'fav-i')); });
    [].forEach.call(D.querySelectorAll('.mito[id]'), function (m) { var c = m.querySelector('.mito-acc'), h = m.querySelector('.mito-frase'); if (c && h && !c.querySelector('.fav-i')) c.appendChild(botonFav('mitos.html#' + m.id, h.textContent.replace(/[«»]/g, '').trim(), 'Mito', 'fav-i fav-linea')); });
    [].forEach.call(D.querySelectorAll('.rec[id]'), function (r) { var h = r.querySelector('h3'); if (h && !r.querySelector('.fav-i')) r.appendChild(botonFav('recetas.html#' + r.id, h.textContent.trim(), 'Receta', 'fav-i')); });
  }
  favItems();

  /* ---- Mis datos: rellenan solas las calculadoras ---- */
  (function () {
    var f = D.querySelector('.tool-form'); if (!f) return; var P = lee('fbe-perfil', {}), usados = 0, campos = [];
    [].forEach.call(f.querySelectorAll('.tool-campo'), function (c) {
      var l = c.querySelector('label, legend'); if (!l) return; var t = l.textContent.trim().toLowerCase();
      var k = /^edad/.test(t) ? 'edad' : /^sexo/.test(t) ? 'sexo' : /^(tu )?peso(,| corporal|$)/.test(t) ? 'peso' : /^altura/.test(t) ? 'altura' : ''; if (!k) return; campos.push(c);
      if (P[k] == null || P[k] === '') return;
      if (k === 'sexo') { var r = c.querySelector('input[type="radio"][value="' + P.sexo + '"]'); if (r) { usados++; if (!r.checked) { r.checked = true; r.dispatchEvent(new Event('change', { bubbles: true })); r.dispatchEvent(new Event('input', { bubbles: true })); } } }
      else { var i = c.querySelector('input'); if (i) { usados++; if (String(i.value) !== String(P[k])) { i.value = P[k]; i.dispatchEvent(new Event('input', { bubbles: true })); } } }
    });
    if (!campos.length) return;
    var n = D.createElement('p'); n.className = 'perfil-n';
    if (usados) { n.innerHTML = 'Rellenado con <a href="mi-panel.html#pn-datos">Mis datos</a>.'; f.insertBefore(n, f.firstChild); }
    else { var visto = false; campos.forEach(function (c) { c.addEventListener('change', function () { if (visto) return; visto = true; n.innerHTML = '¿Siempre los mismos datos? Guárdalos una vez en <a href="mi-panel.html#pn-datos">Mis datos</a> y se rellenan solos.'; f.appendChild(n); }); }); }
  })();

  /* ---- logros ---- */
  var LOGROS = [['resultado', 'Primer resultado', 'Guarda el resultado de una herramienta.'], ['chequeo', 'Chequeo completo', 'Las cuatro pruebas del chequeo de 10 minutos, guardadas.'],
    ['semana', 'Semana cumplida', 'Cierra los dos anillos de Mi semana activa.'], ['racha3', 'Tres semanas seguidas', 'Tres semanas cumplidas una detrás de otra.'],
    ['mitos', 'Nueve mitos leídos', 'Lee los nueve mitos, con su estudio.'], ['ruta', 'Ruta terminada', 'Marca todos los pasos de tu ruta en Empieza aquí.'],
    ['favoritos', 'Tu biblioteca', 'Guarda tres favoritos.'], ['datos', 'Mis datos, a punto', 'Guarda tu edad en Mis datos para no repetirla.'],
    ['explorador', 'Explorador', 'Prueba ocho herramientas distintas.'], ['instalada', 'En tu pantalla de inicio', 'Instala la web como app.']];
  function semOk(L) { var m = 0, v = 0, f = {}; (L || []).forEach(function (e) { if (e.t === 'm') m += e.n; else if (e.t === 'v') v += e.n; else f[e.d] = 1; }); return m + 2 * v >= 150 && Object.keys(f).length >= 2; }
  function estado() {
    var r = lee('fbe-resultados', {}), s = lee('fbe-semana', {}), ks = Object.keys(s).filter(function (k) { return semOk(s[k]); }).sort(), racha = 0, mejor = 0, ant = 0;
    ks.forEach(function (k) { var t = new Date(k + 'T12:00:00').getTime(); racha = ant && Math.round((t - ant) / 864e5) === 7 ? racha + 1 : 1; mejor = Math.max(mejor, racha); ant = t; });
    var ru = lee('fbe-rutas', {});
    return { resultado: Object.keys(r).length > 0, chequeo: ['revision-medica.html', 'actividad-oms.html', 'test-silla.html', 'cintura-altura.html'].every(function (u) { return r[u]; }),
      semana: ks.length > 0, racha3: mejor >= 3, mitos: lee('fbe-mitos', []).length >= 9, ruta: Object.keys(ru).some(function (k) { return ru[k] && ru[k].ok; }),
      favoritos: favs().length >= 3, datos: !!lee('fbe-perfil', {}).edad, explorador: lee('fbe-vistas', []).length >= 8, instalada: APP };
  }
  function punto() { var tp = D.querySelector('#tabs [data-t="panel"]'); if (!tp) return; if (PAG === 'mi-panel.html') { try { localStorage.removeItem('fbe-punto'); } catch (e) { } tp.classList.remove('punto'); } else tp.classList.toggle('punto', !!lee('fbe-punto', 0)); }
  punto();
  function logros() {
    var e = estado(), G = lee('fbe-logros', {}), nuevos = [];
    LOGROS.forEach(function (l) { if (e[l[0]] && !G[l[0]]) { G[l[0]] = Date.now(); nuevos.push(l[1]); } });
    if (nuevos.length) { pon('fbe-logros', G); if (PAG !== 'mi-panel.html') { pon('fbe-punto', 1); punto(); toast(nuevos[0] + (nuevos.length > 1 ? ' y ' + (nuevos.length - 1) + ' más' : ''), 'Ver', function () { location.href = 'mi-panel.html#pn-logros'; }, 6000, 'logro', nuevos.length > 1 ? 'Logros conseguidos' : 'Logro conseguido'); } }
    return G;
  }
  setTimeout(logros, 900); addEventListener('fbe-semana', function () { setTimeout(logros, 50); });
  D.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.guarda-r, #pn-guarda, .ea-hecho')) setTimeout(logros, 300); });

  /* ---- acciones rapidas (buscador): enlaces #accion=... ---- */
  function lectura(fn) { var a = lee('fbe-lectura', {}) || {}; fn(a); pon('fbe-lectura', a); var c = R.classList; c.toggle('letra-1', a.l === 1); c.toggle('letra-2', a.l === 2); c.toggle('contraste', !!a.c); c.toggle('quieto', !!a.q); }
  var ACC = {
    tema: function () { var b = D.getElementById('tema'); if (b) b.click(); },
    'texto-mas': function () { lectura(function (a) { a.l = Math.min(2, (a.l || 0) + 1); }); toast('Texto más grande.'); },
    'texto-normal': function () { lectura(function (a) { a.l = 0; }); toast('Texto en su tamaño normal.'); },
    contraste: function () { lectura(function (a) { a.c = a.c ? 0 : 1; }); toast('Contraste alto: cambiado.'); },
    quieto: function () { lectura(function (a) { a.q = a.q ? 0 : 1; }); toast('Animaciones: cambiado.'); },
    favorito: function () { var b = D.querySelector('.fav-b'); if (b) b.click(); else toast('Esta página no se puede guardar.'); },
    compartir: function () { var b = D.querySelector('.compartir-b:not(.fav-b)'); if (b) b.click(); },
    instalar: function () { location.href = 'ayuda.html#instalar'; }
  };
  function accion() {
    var m = location.hash.match(/^#accion=([a-z-]+)$/); if (!m) return; var d = D.querySelector('dialog.busca-d[open]'); if (d) d.close();
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) { } if (ACC[m[1]]) setTimeout(ACC[m[1]], 60);
  }
  addEventListener('hashchange', accion); accion();

  /* ---- pestanas de abajo y modo instalada ---- */
  var tabs = D.getElementById('tabs');
  if (tabs) {
    var bq = tabs.querySelector('[data-t="buscar"]'); if (bq) bq.addEventListener('click', function (e) { var b = D.querySelector('.busca-b'); if (b) { e.preventDefault(); b.click(); } });
    if (navigator.vibrate) tabs.addEventListener('click', function (e) { if (e.target.closest('a')) { try { navigator.vibrate(8); } catch (x) { } } });
  }
  if (APP) {
    var cab = D.querySelector('.cab .in'), ini = /^(mi-panel|index)\.html$/.test(PAG);
    if (cab && !ini && history.length > 1) { var at = D.createElement('button'); at.type = 'button'; at.className = 'app-atras'; at.setAttribute('aria-label', 'Volver'); at.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'; at.addEventListener('click', function () { history.back(); }); cab.insertBefore(at, cab.firstChild); }
    [].forEach.call(D.querySelectorAll('.cab .logo'), function (a) { a.setAttribute('href', 'mi-panel.html'); });
  }

  /* ---- el titulo de la pagina sube a la barra al bajar (movil) ---- */
  (function () {
    var ci = D.querySelector('.cab .in'), lg = ci && ci.querySelector('.logo'); if (!lg || !h1 || !D.querySelector('.hero.mini') || !('IntersectionObserver' in window) || !(APP || D.body.classList.contains('con-tabs'))) return;
    var b = D.createElement('b'); b.className = 'cab-tit'; b.setAttribute('aria-hidden', 'true'); b.textContent = NOM.split(/[:·]/)[0].trim(); lg.insertAdjacentElement('afterend', b);
    new IntersectionObserver(function (es) { var e = es[0]; R.classList.toggle('tit-ver', !e.isIntersecting && e.boundingClientRect.top < 80); }, { rootMargin: '-70px 0px 0px 0px' }).observe(h1);
  })();

  /* ---- sin conexion y version nueva ---- */
  var sinRed = null;
  function red() { if (!navigator.onLine && !sinRed) sinRed = toast('Las herramientas siguen funcionando.', '', null, 0, 'red', 'Sin conexión'); else if (navigator.onLine && sinRed) { sinRed.remove(); sinRed = null; toast('Vuelves a tener conexión.', '', null, 2500, 'ok'); } R.classList.toggle('sin-red', !navigator.onLine); }
  addEventListener('offline', red); addEventListener('online', red); if (navigator.onLine === false) red();
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) { var avisado = false; navigator.serviceWorker.addEventListener('controllerchange', function () { if (avisado) return; avisado = true; toast('Hay una versión nueva de la web.', 'Actualizar', function () { location.reload(); }, 0, 'nueva'); }); }

  window.fbe = { lee: lee, pon: pon, pag: PAG, app: APP, toast: toast, favs: favs, esFav: esFav, cambiaFav: cambiaFav, botonFav: botonFav, favItems: favItems, LOGROS: LOGROS, logros: logros, estado: estado, semOk: semOk };
})();
