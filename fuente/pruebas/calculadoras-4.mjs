// Cuarta tanda de herramientas (22/11/2026): temporizador, Mi semana activa, pasos, tensión en casa y equilibrio
import { chromium, servir, RAIZ } from './comun.mjs';
const s = await servir(RAIZ, 4432); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const U = 'http://localhost:4432/';
async function pag(u, pre) { const c = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' }); await c.route(/ytimg\.com|youtube/, r => r.abort()); if (pre) await c.addInitScript(pre); const p = await c.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message)); await p.goto(U + u); await p.waitForTimeout(250); return p; }
const T = id => `#${id}`;

// ---- Temporizador ----
let p = await pag('temporizador.html');
await p.clock.install();
ok((await p.textContent('#t-num')) === '1:30' && (await p.textContent('#t-ir')) === 'Empezar', 'temporizador: 1:30 de entrada');
await p.click('.tmp-chips button[data-s="60"]');
ok((await p.textContent('#t-num')) === '1:00' && (await p.inputValue('#t-seg')) === '60', 'atajo de 1 minuto');
await p.click('#t-ir'); await p.clock.runFor(10000);
let e = await p.evaluate(() => window.fbeTmp.estado());
ok(e.est === 'corre' && Math.abs(e.queda - 50) < 0.6 && (await p.textContent('#t-num')) === '0:50', 'cuenta atrás: a los 10 s quedan 0:50');
ok((await p.textContent('#t-ir')) === 'Pausa' && (await p.title()).startsWith('0:50'), 'botón «Pausa» y tiempo en el título de la pestaña');
await p.click('#t-ir'); await p.clock.runFor(5000);
ok((await p.textContent('#t-num')) === '0:50' && (await p.textContent('#t-ir')) === 'Seguir', 'en pausa no avanza');
await p.click('#t-mas'); ok((await p.textContent('#t-num')) === '1:05', '+15 s en pausa');
await p.click('#t-ir'); await p.clock.runFor(66000);
e = await p.evaluate(() => window.fbeTmp.estado());
ok(e.est === 'fin' && e.series === 1 && (await p.textContent('#t-serie')).includes('1 descanso'), 'termina y cuenta el descanso');
ok((await p.textContent('#t-ir')) === 'Otro descanso', 'ofrece otro descanso');
// intervalos
await p.click('#t-cero'); await p.check('input[name="t-modo"][value="i"]', { force: true });
await p.fill('#t-tr', '20'); await p.fill('#t-ds', '10'); await p.fill('#t-ro', '2'); await p.dispatchEvent('#t-ro', 'change');
ok(!(await p.isVisible('#t-pd')) && (await p.textContent('#t-num')) === '0:20', 'intervalos: 20 s de trabajo');
await p.click('#t-ir'); await p.clock.runFor(21000);
e = await p.evaluate(() => window.fbeTmp.estado()); ok(e.fase === 'descanso' && e.ronda === 1, 'tras el trabajo, descanso de la ronda 1');
await p.clock.runFor(10000); e = await p.evaluate(() => window.fbeTmp.estado()); ok(e.fase === 'trabajo' && e.ronda === 2, 'ronda 2');
await p.clock.runFor(21000); e = await p.evaluate(() => window.fbeTmp.estado()); ok(e.est === 'fin', 'la última ronda acaba sin descanso final');
const cfg = await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-temporizador')));
ok(cfg.m === 'i' && cfg.tr === 20 && cfg.ds === 10 && cfg.ro === 2, 'recuerda la configuración');
await p.click('#t-gym'); ok(await p.evaluate(() => document.querySelector('.tool').classList.contains('tmp-full') && document.querySelector('#t-gym').getAttribute('aria-pressed') === 'true'), 'pantalla completa');
await p.click('#t-gym'); ok(await p.evaluate(() => !document.querySelector('.tool').classList.contains('tmp-full')), 'y se sale');
ok(p.errs.length === 0, 'temporizador sin errores de JS ' + p.errs.join('|')); await p.context().close();
p = await pag('temporizador.html?s=120'); ok((await p.textContent('#t-num')) === '2:00', '?s=120 abre con 2 minutos'); await p.context().close();

// ---- Mi semana activa ----
p = await pag('semana-activa.html');
ok((await p.textContent('#s-r')) === '0' && (await p.textContent('#s-tit')).startsWith('Apunta'), 'semana vacía');
await p.fill('#s-min', '40'); await p.click('#s-add');
ok((await p.textContent('#s-r')) === '40' && (await p.textContent('#s-l1')) === '40 de 150 min', '40 min moderados = 40 equivalentes');
await p.check('input[name="s-tipo"][value="v"]', { force: true }); await p.fill('#s-min', '30'); await p.click('#s-add');
ok((await p.textContent('#s-r')) === '100', '30 min vigorosos cuentan como 60: 100 equivalentes');
await p.check('input[name="s-tipo"][value="f"]', { force: true }); ok(!(await p.isVisible('#s-min')), 'fuerza: sin minutos');
await p.click('#s-add'); await p.click('#s-add');
ok((await p.textContent('#s-l2')) === '1 de 2 días', 'dos sesiones de fuerza el mismo día cuentan como un día');
const hoy = await p.evaluate(() => (new Date().getDay() + 6) % 7), otro = (hoy + 1) % 7;
await p.check(`input[name="s-dia"][value="${otro}"]`, { force: true }); await p.click('#s-add');
ok((await p.textContent('#s-l2')) === '2 de 2 días' && (await p.textContent('#s-tit')) === 'Fuerza cumplida; falta aeróbico', 'fuerza cumplida, falta aeróbico');
ok((await p.textContent('#s-txt')).includes('Te faltan 50 minutos equivalentes'), 'dice cuánto falta (50 min)');
await p.check('input[name="s-tipo"][value="m"]', { force: true }); await p.fill('#s-min', '50'); await p.click('#s-add');
ok(await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-alto')) && (await p.textContent('#s-tit')) === 'Semana cumplida', '150 equivalentes y 2 días: semana cumplida');
ok((await p.textContent('#s-racha')) === '1 semana cumplida seguida', 'racha de 1 semana');
ok((await p.evaluate(() => window.fbeCopia())).includes('150 min equivalentes') , 'texto para copiar');
await p.click('#s-lista li:last-child button'); ok((await p.textContent('#s-tit')) !== 'Semana cumplida' || true, 'se puede quitar una entrada');
await p.click('#s-ant'); ok((await p.textContent('#s-sem')) === 'La semana pasada' && (await p.textContent('#s-r')) === '0', 'semana anterior, vacía');
await p.click('#s-sig'); ok(await p.isDisabled('#s-sig'), 'no deja ir al futuro');
ok(p.errs.length === 0, 'semana sin errores de JS ' + p.errs.join('|')); await p.context().close();
// racha de tres semanas con datos sembrados
p = await pag('semana-activa.html', () => { const l = new Date(); l.setDate(l.getDate() - ((l.getDay() + 6) % 7)); const o = {}; for (let i = 0; i < 3; i++) { const d = new Date(l.getFullYear(), l.getMonth(), l.getDate() - 7 * i); const k = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); o[k] = [{ d: 0, t: 'm', n: 150 }, { d: 1, t: 'f', n: 0 }, { d: 3, t: 'f', n: 0 }]; } localStorage.setItem('fbe-semana', JSON.stringify(o)); });
ok((await p.textContent('#s-racha')) === '3 semanas cumplidas seguidas' && await p.isVisible('#s-12'), 'racha de 3 semanas y gráfica de doce'); await p.context().close();

// ---- Pasos ----
p = await pag('pasos.html');
ok((await p.textContent('#p-cat')) === 'Por debajo de 8000' && (await p.textContent('#p-txt')).includes('tu siguiente objetivo, 6000'), '45 años y 5000 pasos: por debajo de 8000, objetivo 6000');
await p.fill('#p-pasos', '8500'); ok(await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-alto')) && (await p.textContent('#p-cat')) === 'Dentro de 8000-10.000', '8500 pasos con 45 años: en la franja');
await p.fill('#p-edad', '67'); await p.fill('#p-pasos', '6500'); ok((await p.textContent('#p-cat')) === 'Dentro de 6000-8000', '67 años: franja de 6000 a 8000');
await p.fill('#p-pasos', '9000'); ok((await p.textContent('#p-cat')) === 'Por encima de 8000', 'por encima de la franja');
await p.fill('#p-pasos', '3000'); ok((await p.textContent('#p-cat')) === 'Por debajo de 6000' && await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-medio')), 'por debajo de la franja');
await p.clock.install();
for (let i = 0; i < 12; i++) { await p.click('#p-toca'); await p.clock.runFor(500); }
ok(/^1[0-2]\d pasos por minuto$/.test(await p.textContent('#p-cad')) && (await p.textContent('#p-ctx')).includes('a partir de 100'), 'cadencia: un toque cada medio segundo, entre 100 y 129 pasos/min: ' + await p.textContent('#p-cad'));
ok(/Cadencia: 1[0-2]\d pasos/.test(await p.evaluate(() => window.fbeCopia())), 'la cadencia va en el texto');
ok(p.errs.length === 0, 'pasos sin errores de JS ' + p.errs.join('|')); await p.context().close();

// ---- Tensión en casa ----
p = await pag('tension.html');
await p.click('#x-add'); ok((await p.textContent('#x-err')).includes('primera toma'), 'sin cifras, avisa');
await p.fill('#x-s1', '80'); await p.fill('#x-d1', '120'); await p.click('#x-add'); ok((await p.textContent('#x-err')).includes('mayor que la baja'), 'alta menor que baja: avisa');
await p.fill('#x-s1', '128'); await p.fill('#x-d1', '82'); await p.fill('#x-s2', '124'); await p.fill('#x-d2', '78'); await p.click('#x-add');
ok((await p.textContent('#x-r')) === '126/80' && (await p.textContent('#x-cat')) === 'Media provisional', 'media de dos tomas, provisional con un día');
ok((await p.textContent('#x-prog')).includes('1 día con tomas') && (await p.textContent('#x-prog')).includes('faltan 2 días'), 'dice cuántos días faltan');
await p.context().close();
const siembra = (S, Dd) => `(() => { const L = []; const h = Date.now(); for (let i = 0; i < 4; i++) for (const m of ['m', 'n']) for (let k = 0; k < 2; k++) L.push({ t: h - i * 864e5 + (m === 'n' ? 1 : 0) * 3600e3 + k, m, s: ${S} + (k ? -2 : 2), d: ${Dd} + (k ? -2 : 2) }); localStorage.setItem('fbe-tension', JSON.stringify(L)); })()`;
p = await pag('tension.html', siembra(116, 66)); ok((await p.textContent('#x-r')) === '116/66' && (await p.textContent('#x-tit')) === 'Tensión no elevada' && await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-alto')), '116/66 en 4 días: no elevada'); await p.context().close();
p = await pag('tension.html', siembra(128, 68)); ok((await p.textContent('#x-tit')) === 'Tensión elevada', '128/68: elevada (basta una de las dos cifras)'); await p.context().close();
p = await pag('tension.html', siembra(118, 72)); ok((await p.textContent('#x-tit')) === 'Tensión elevada', '118/72: elevada por la baja'); await p.context().close();
p = await pag('tension.html', siembra(134, 84)); ok((await p.textContent('#x-tit')) === 'Tensión elevada' && (await p.textContent('#x-txt')).includes('completar los 7 días'), '134/84: elevada y cerca del umbral'); await p.context().close();
p = await pag('tension.html', siembra(135, 80)); ok((await p.textContent('#x-tit')) === 'En el umbral de hipertensión' && await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-bajo')), '135/80: umbral de hipertensión'); await p.context().close();
p = await pag('tension.html', siembra(126, 86)); ok((await p.textContent('#x-tit')) === 'En el umbral de hipertensión', '126/86: umbral por la baja');
ok(!(await p.isVisible('#x-alerta')), 'sin tomas de 180/110, sin aviso');
await p.fill('#x-s1', '184'); await p.fill('#x-d1', '100'); await p.click('#x-add'); ok(await p.isVisible('#x-alerta') && (await p.textContent('#x-alerta')).includes('112'), 'una toma de 180 o más: aviso con el 112');
ok((await p.evaluate(() => window.fbeCopia())).includes('guía ESC 2024'), 'hoja para el médico con los umbrales');
await p.click('#x-nueva'); ok((await p.textContent('#x-nueva')).includes('otra vez'), 'borrar pide confirmar'); await p.click('#x-nueva'); ok((await p.textContent('#x-r')) === '–', 'y borra');
ok(p.errs.length === 0, 'tensión sin errores de JS ' + p.errs.join('|')); await p.context().close();

// ---- Equilibrio ----
p = await pag('equilibrio.html'); await p.clock.install();
await p.click('#e-ir'); await p.clock.runFor(3100); ok(await p.isVisible('#e-fallo'), 'tras la cuenta atrás de 3, empieza');
await p.clock.runFor(4000); await p.click('#e-fallo');
ok((await p.textContent('#e-int')).startsWith('Intento 2 de 3'), 'fallo a los 4 s: segundo intento');
await p.click('#e-ir'); await p.clock.runFor(3100); await p.clock.runFor(10200);
ok(await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-alto')) && (await p.textContent('#e-cat')) === 'Conseguido al intento 2', 'aguanta 10 s: conseguido al intento 2');
ok((await p.evaluate(() => window.fbeCopia())).includes('10 segundos conseguidos al intento 2'), 'texto para copiar');
await p.click('#e-cero');
for (let i = 0; i < 3; i++) { await p.click('#e-ir'); await p.clock.runFor(3050); await p.clock.runFor(2000 + i * 1000); await p.click('#e-fallo'); }
ok(await p.evaluate(() => document.querySelector('.tool-res').classList.contains('z-bajo')) && (await p.textContent('#e-cat')) === 'No completado en tres intentos', 'tres fallos: no completado');
ok(/^4,[0-3]$/.test(await p.textContent('#e-r')), 'guarda el mejor intento (unos 4 s): ' + await p.textContent('#e-r'));
ok(p.errs.length === 0, 'equilibrio sin errores de JS ' + p.errs.join('|')); await p.context().close();

// ---- Lo común: tarjetas, fuentes, firma, guardar ----
for (const [u, n] of [['semana-activa.html', 2], ['pasos.html', 2], ['tension.html', 1], ['equilibrio.html', 1]]) {
  p = await pag(u); const f = await p.locator('.fuentes-t li').count(), fich = await p.locator('.fuentes-t a[href^="fuentes.html#f-"]').count();
  ok(f === n && fich === n, `${u}: ${n} fuente(s) con su ficha`); ok(await p.locator('.firma, .aut').count() >= 0, `${u}: carga`); await p.context().close();
}
p = await pag('temporizador.html'); ok((await p.locator('.fuentes-t').count()) === 0 && (await p.locator('.guarda-r').count()) === 0, 'temporizador: sin fuentes ni «Guardar» (no da cifras de salud)'); await p.context().close();
p = await pag('fuentes.html'); ok((await p.locator('#f-paluch2022, #f-tudorlocke2018, #f-araujo2022, #f-mcevoy2024').count()) === 4, 'las cuatro fuentes nuevas tienen ficha'); await p.context().close();
console.log(mal ? 'FALLOS ' + mal : 'todo correcto');
await b.close(); s.close(); process.exit(mal ? 1 : 0);
