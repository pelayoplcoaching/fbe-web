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
  var caja = null, cola = [];
  function toast(txt, bt, fn, ms) {
    if (!caja) { caja = D.createElement('div'); caja.className = 'aviso-app'; caja.setAttribute('role', 'status'); caja.setAttribute('aria-live', 'polite'); D.body.appendChild(caja); }
    var t = D.createElement('div'); t.className = 'aviso-t'; var s = D.createElement('span'); s.textContent = txt; t.appendChild(s);
    if (bt) { var b = D.createElement('button'); b.type = 'button'; b.textContent = bt; b.addEventListener('click', function () { t.remove(); if (fn) fn(); }); t.appendChild(b); }
    caja.appendChild(t); if (ms !== 0) setTimeout(function () { t.remove(); }, ms || 4500); return t;
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
    b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); var on = cambiaFav(u, t, k); pinta(); b.classList.remove('late'); void b.offsetWidth; b.classList.add('late'); if (on && !lee('fbe-fav-visto', 0)) { pon('fbe-fav-visto', 1); toast('Guardado. Tus favoritos están en Mi panel.', 'Ver', function () { location.href = 'mi-panel.html#pn-fav'; }); } });
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
  function logros() {
    var e = estado(), G = lee('fbe-logros', {}), nuevos = [];
    LOGROS.forEach(function (l) { if (e[l[0]] && !G[l[0]]) { G[l[0]] = Date.now(); nuevos.push(l[1]); } });
    if (nuevos.length) { pon('fbe-logros', G); if (PAG !== 'mi-panel.html') toast('Logro: ' + nuevos[0] + (nuevos.length > 1 ? ' y ' + (nuevos.length - 1) + ' más' : ''), 'Ver', function () { location.href = 'mi-panel.html#pn-logros'; }, 6000); }
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

  /* ---- sin conexion y version nueva ---- */
  var sinRed = null;
  function red() { if (!navigator.onLine && !sinRed) sinRed = toast('Sin conexión. Las herramientas siguen funcionando.', '', null, 0); else if (navigator.onLine && sinRed) { sinRed.remove(); sinRed = null; toast('Vuelves a tener conexión.', '', null, 2500); } R.classList.toggle('sin-red', !navigator.onLine); }
  addEventListener('offline', red); addEventListener('online', red); if (navigator.onLine === false) red();
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) { var avisado = false; navigator.serviceWorker.addEventListener('controllerchange', function () { if (avisado) return; avisado = true; toast('Hay una versión nueva de la web.', 'Actualizar', function () { location.reload(); }, 0); }); }

  window.fbe = { lee: lee, pon: pon, pag: PAG, app: APP, toast: toast, favs: favs, esFav: esFav, cambiaFav: cambiaFav, botonFav: botonFav, favItems: favItems, LOGROS: LOGROS, logros: logros, estado: estado, semOk: semOk };
})();
