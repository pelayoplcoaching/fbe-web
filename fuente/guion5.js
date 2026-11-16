(function () {
  var D = document, R = D.documentElement, reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, r) { return (r || D).querySelector(s); } function $$(s, r) { return [].slice.call((r || D).querySelectorAll(s)); }
  // Imágenes repetidas: se cargan una vez y se reutilizan
  $$('img[data-de]').forEach(function (i) { var o = $('img[data-k="' + i.dataset.de + '"]'); if (o) i.src = o.src; });
  // Tema claro u oscuro
  var bt = $('#tema'); try { var g = localStorage.getItem('fbe-web-tema'); if (g === 'dark' || g === 'light') R.dataset.theme = g; } catch (e) {}
  if (bt) bt.addEventListener('click', function () { var osc = R.dataset.theme ? R.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; R.dataset.theme = osc ? 'light' : 'dark'; try { localStorage.setItem('fbe-web-tema', R.dataset.theme); } catch (e) {} });
  // La cabecera se esconde al bajar y vuelve al subir
  var cab = $('.cab'), antes = 0, arr = $('#arriba');
  addEventListener('scroll', function () { var y = window.scrollY || 0; cab.classList.toggle('fina', y > 80); if (!$('.menu[open]')) cab.classList.toggle('oculta', y > 500 && y > antes + 4); if (y < antes - 4) cab.classList.remove('oculta'); if (arr) arr.classList.toggle('ver', y > 1400); antes = y; }, { passive: true });
  // Alternativas
  var ALT = { ocupada: ['Press con mancuernas en banco plano', 'Misma función, otro material'], casa: ['Flexiones con lastre o con banda', 'Sin banco ni barra'], viaje: ['Flexiones lentas: 3 segundos de bajada', 'Con tu peso, en cualquier sitio'] };
  var altN = $('#alt-n'); $$('.alt-b button').forEach(function (b) { b.addEventListener('click', function () { $$('.alt-b button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); altN.innerHTML = '<small>' + ALT[b.dataset.a][1] + '</small>' + ALT[b.dataset.a][0]; altN.classList.remove('cambia'); void altN.offsetWidth; altN.classList.add('cambia'); }); });
  // Recetas: se suman al día y el anillo de proteína se llena
  var arco = $('.hoy-p .a'), META = 140;
  function sumar() { var p = 0, k = 0; $$('.rc.en').forEach(function (c) { p += +c.dataset.p; k += +c.dataset.k; }); $('#hoy-b').textContent = Math.round(p) + ' / ' + META + ' g'; $('#hoy-s').textContent = p >= META ? 'Proteína del día, cumplida · ' + k + ' kcal' : (k ? k + ' kcal · te faltan ' + Math.round(META - p) + ' g' : 'Añade recetas a tu día'); if (arco) arco.style.strokeDashoffset = (213.6 * (1 - Math.min(1, p / META))).toFixed(1); }
  $$('.rc button').forEach(function (b) { b.addEventListener('click', function () { var c = b.closest('.rc'), en = c.classList.toggle('en'); b.setAttribute('aria-pressed', en); b.textContent = en ? 'En tu día' : 'Añadir a mi día'; sumar(); }); });
  // Test: ¿encaja contigo?
  var test = $('#test');
  if (test) test.addEventListener('change', function () { var r = $$('input:checked', test); if (r.length < 3) return; var si = r.filter(function (i) { return i.value === 's'; }).length, v = $('.veredicto', test), T = si === 3 ? ['Encaja', 'Es justo para lo que está pensada la asesoría. Cuéntame tu caso y lo vemos.'] : si === 2 ? ['Probablemente sí', 'Hay algo que conviene hablar antes. Cuéntamelo en el formulario y te digo con sinceridad si te puedo ayudar.'] : ['Puede que ahora no sea el momento', 'Y no pasa nada. Si cambia, aquí estaré; mientras tanto, tienes mi contenido en redes.']; $('b', v).textContent = T[0]; $('p', v).textContent = T[1]; $('a', v).hidden = si < 2; v.hidden = false; });
})();
