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
  var SUG = [['empieza-aqui.html', 'Empieza aquí'], ['herramientas.html', 'Herramientas'], ['programas.html', 'Programas'], ['dudas.html', 'Dudas'], ['glosario.html', 'Glosario'], ['mis-resultados.html', 'Mis resultados']];
  var PRI = { 'Herramienta': 0, 'Página': 1, 'Glosario': 2, 'Duda': 3, 'Mito': 4, 'Guía': 5, 'Empieza aquí': 6, 'Boletín': 7, 'Fuente': 8, 'Receta': 9, 'Vídeo': 10 };
  function marca(t, ps) { var s = esc(t), p = ps.filter(function (x) { return x.length > 1; })[0]; if (!p) return s; var i = norm(s).indexOf(p); return i < 0 ? s : s.slice(0, i) + '<mark>' + s.slice(i, i + p.length) + '</mark>' + s.slice(i + p.length); }
  function pinta(ps) {
    act = res.length ? 0 : -1;
    lista.innerHTML = res.length ? res.map(function (e, i) { return '<li role="option" data-k="' + ({ 'Herramienta': 'h', 'Página': 'p', 'Glosario': 'g', 'Duda': 'd', 'Mito': 'm', 'Guía': 'u', 'Empieza aquí': 'e', 'Boletín': 'b', 'Fuente': 'f', 'Atajo': 'a', 'Receta': 'r', 'Vídeo': 'v' }[e.y] || 'p') + '" id="bo-' + i + '" aria-selected="' + (i === act) + '"><a href="' + esc(e.u) + '"' + (e.x ? ' target="_blank" rel="noopener"' : '') + '><span class="bo-y">' + esc(e.y) + '</span><b>' + marca(e.t, ps) + '</b>' + (e.d ? '<small>' + esc(e.d.length > 110 ? e.d.slice(0, 108) + '…' : e.d) + '</small>' : '') + '</a></li>'; }).join('') : '<li class="bo-nada">Nada con esas palabras. Prueba con otra o mira las <a href="dudas.html">dudas</a>.</li>';
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
