/* app.js (22/11/2026): la web como app. Historial, favoritos, Mis datos, logros, avisos, acciones rapidas y modo instalada.
   Todo se guarda en este dispositivo (localStorage fbe-visto, fbe-favoritos, fbe-perfil, fbe-logros, fbe-vistas). */
(function () {
  var D = document, R = D.documentElement;
  function lee(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function pon(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  var PAG = location.pathname.split('/').pop() || 'index.html'; if (PAG.indexOf('.') < 0) PAG += '.html';
  var APP = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  if (APP) R.classList.add('es-app');
  var SIN = /^(index|mi-panel|404|gracias|gracias-plaza|gracias-boletin|esencial-gracias|pedir-plaza|privacidad|sin-conexion)\.html$/;
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
