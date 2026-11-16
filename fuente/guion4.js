(function () {
  var D = document, reducido = matchMedia('(prefers-reduced-motion: reduce)').matches, fino = matchMedia('(hover: hover) and (pointer: fine)').matches;
  function $(s, r) { return (r || D).querySelector(s); } function $$(s, r) { return [].slice.call((r || D).querySelectorAll(s)); }
  // Portada: luz que sigue al ratón, pase de pantallas, burbuja que se escribe, metas
  var hero = $('.hero');
  if (fino && !reducido) hero.addEventListener('pointermove', function (e) { var r = hero.getBoundingClientRect(); hero.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%'); hero.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%'); });
  var pases = $$('#tel .pase'), pts = $$('#tel .puntos i'), k = 0;
  function pase(i) { pases.forEach(function (p, j) { p.classList.toggle('on', j === i); }); pts.forEach(function (p, j) { p.classList.toggle('on', j === i); }); k = i; }
  if (pases.length > 1 && !reducido) setInterval(function () { if (!D.hidden) pase((k + 1) % pases.length); }, 3400);
  var burb = $('#escribe');
  if (burb && !reducido) { var txt = burb.textContent, n = 0; burb.textContent = ''; var cur = D.createElement('span'); cur.className = 'cur'; burb.after(cur); setTimeout(function esc() { burb.textContent = txt.slice(0, ++n); if (n < txt.length) setTimeout(esc, 28); else setTimeout(function () { cur.remove(); }, 1500); }, 1500); }
  var META = { fuerza: 'Progresión planificada semana a semana y cada récord apuntado. Yo decido cuándo toca subir y cuándo descargar.', grasa: 'Un déficit que puedas sostener, proteína suficiente y fuerza para no perder músculo por el camino.', cero: 'Vídeo de cada ejercicio, cargas que controlas y alguien que te corrige la técnica desde el primer día.', volver: 'Volvemos sin prisa y sin culpa: cargas ajustadas a cómo estás hoy, no a cómo estabas.' };
  var sub = $('#sub'), base = sub.textContent, metas = $$('.metas button');
  metas.forEach(function (b) { b.addEventListener('click', function () { var on = b.getAttribute('aria-pressed') === 'true'; metas.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); if (!on) b.setAttribute('aria-pressed', 'true'); sub.textContent = on ? base : META[b.dataset.m]; sub.classList.remove('cambia'); void sub.offsetWidth; sub.classList.add('cambia'); }); });
  // Recorrido: en pantallas grandes, el móvil se queda fijo y cambia al pasar cada momento
  var tabs = $$('.tour-lista [role=tab]'), puntos = $$('.tour-puntos i');
  function marcar() { tabs.forEach(function (t, i) { if (puntos[i]) puntos[i].classList.toggle('on', t.getAttribute('aria-selected') === 'true'); }); }
  tabs.forEach(function (t) { new MutationObserver(marcar).observe(t, { attributes: true, attributeFilter: ['aria-selected'] }); }); marcar();
  if ('IntersectionObserver' in window && matchMedia('(min-width: 981px)').matches) { var ver = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && e.target.getAttribute('aria-selected') !== 'true') e.target.click(); }); }, { rootMargin: '-48% 0px -48% 0px' }); tabs.forEach(function (t) { ver.observe(t); }); }
  // Pruébalo: tres series, descanso y récord
  var ses = $('#sesion');
  if (ses) {
    var filas = $$('.serie', ses), desc = $('.desc', ses), arco = $('.desc .a', ses), cuenta = $('.desc b', ses), fin = $('.fin', ses), brindis = $('.brindis', ses), conf = $('.conf', ses), reloj, quedan, MEJOR = 16 * 10;
    function parar() { clearInterval(reloj); desc.hidden = true; }
    function descansar() { quedan = 12; desc.hidden = false; arco.style.transition = 'none'; arco.style.strokeDashoffset = 0; cuenta.textContent = '0:12'; void arco.getBoundingClientRect(); arco.style.transition = ''; reloj = setInterval(function () { quedan--; cuenta.textContent = '0:' + (quedan < 10 ? '0' : '') + quedan; arco.style.strokeDashoffset = (213.6 * (1 - quedan / 12)).toFixed(1); if (quedan <= 0) parar(); }, 1000); }
    function num(i) { return Math.max(0, parseFloat(String(i.value).replace(',', '.')) || 0); }
    filas.forEach(function (f, i) { $('button', f).addEventListener('click', function () {
      if (f.classList.contains('hecha')) return; var kg = num($$('input', f)[0]), reps = num($$('input', f)[1]); f.classList.add('hecha'); $('button', f).setAttribute('aria-pressed', 'true');
      if (kg * reps > MEJOR) { f.classList.add('record'); brindis.classList.remove('on'); void brindis.offsetWidth; brindis.classList.add('on'); if (!reducido) { conf.classList.remove('on'); void conf.offsetWidth; conf.classList.add('on'); } }
      var hechas = filas.filter(function (x) { return x.classList.contains('hecha'); });
      if (hechas.length === filas.length) { parar(); var tot = hechas.reduce(function (s, x) { var v = $$('input', x); return s + num(v[0]) * num(v[1]); }, 0); $('.fin b', ses).textContent = 'Sesión apuntada: ' + Math.round(tot) + ' kg movidos'; fin.hidden = false; } else descansar(); }); });
    $('.desc button', ses).addEventListener('click', parar);
    $('.fin button', ses).addEventListener('click', function () { filas.forEach(function (f) { f.classList.remove('hecha', 'record'); $('button', f).setAttribute('aria-pressed', 'false'); }); fin.hidden = true; parar(); });
    $$('.conf i', ses).forEach(function (c, i) { var a = i / 18 * 6.283; c.style.setProperty('--x', Math.round(Math.cos(a) * (90 + i % 5 * 22)) + 'px'); c.style.setProperty('--y', Math.round(Math.sin(a) * (90 + i % 4 * 26) - 40) + 'px'); c.style.setProperty('--r', (i * 67 % 360) + 'deg'); c.style.background = ['#7C6AFD', '#F0C674', '#5FD3A0', '#FF6B81'][i % 4]; });
  }
  // Foco que sigue al cursor en las tarjetas
  if (fino) $$('.caja').forEach(function (c) { c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(); c.style.setProperty('--cx', (e.clientX - r.left) + 'px'); c.style.setProperty('--cy', (e.clientY - r.top) + 'px'); }); });
  // Galería con flechas
  var gal = $('#galeria'); $$('.gal-btn button').forEach(function (b) { b.addEventListener('click', function () { gal.scrollBy({ left: (b.dataset.d === 'sig' ? 1 : -1) * Math.min(540, gal.clientWidth * .8), behavior: reducido ? 'auto' : 'smooth' }); }); });
  // Calculadora de proteína
  var peso = $('#peso');
  if (peso) { var pinta = function () { var p = +peso.value, a = Math.round(p * 1.6 / 5) * 5, b = Math.round(p * 2.2 / 5) * 5; $('#peso-o').textContent = p + ' kg'; $('#prot').textContent = a + '–' + b + ' g'; $('#toma').textContent = Math.round(a / 4 / 5) * 5 + '–' + Math.round(b / 4 / 5) * 5 + ' g'; }; peso.addEventListener('input', pinta); pinta(); }
})();
