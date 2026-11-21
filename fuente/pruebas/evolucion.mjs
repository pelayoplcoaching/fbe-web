// «Mi evolución» (gráficas) e «Informe para tu médico» en Mis resultados, y lo que guarda «Guardar en Mis resultados»
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
const s = await servir(RAIZ, 4403); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
const U = 'http://localhost:4403/';
const lee = () => p.evaluate(() => JSON.parse(localStorage.getItem('fbe-resultados') || '{}'));
// 1. Guardar desde las herramientas: cifra, unidad, zona y su titular; en el 1RM, el ejercicio
await p.goto(U + 'prension.html'); await p.waitForTimeout(250);
await p.fill('#g-1', '30'); await p.waitForTimeout(200); await p.click('.guarda-r'); await p.waitForTimeout(150);
let o = await lee(), e = o['prension.html'] && o['prension.html'].h[0];
ok(e && e.v === 30 && e.vt === '30' && e.u === 'kg' && ['alto', 'medio', 'bajo'].includes(e.z) && e.zt && e.zt.length > 5, 'prensión: guarda 30 kg con zona «' + (e && e.zt) + '»');
await p.goto(U + 'calculadora-1rm.html'); await p.waitForTimeout(250);
await p.fill('#r-peso', '100'); await p.fill('#r-reps', '5'); await p.fill('#r-ej', 'Sentadilla'); await p.waitForTimeout(200);
ok((await p.textContent('#r-serie')).startsWith('Sentadilla:'), '1RM: el ejercicio sale en la serie');
await p.click('.guarda-r'); await p.waitForTimeout(150); o = await lee(); e = o['calculadora-1rm.html'] && o['calculadora-1rm.html'].h[0];
ok(e && e.s === 'Sentadilla' && typeof e.v === 'number' && e.u === 'kg' && e.texto.startsWith('Tabla de cargas · Sentadilla') && !e.z, '1RM: guarda ejercicio y cifra (' + (e && e.vt) + ' kg), sin zona');
await p.goto(U + 'calorias.html'); await p.waitForTimeout(250);
await p.fill('#k-edad', '40'); await p.fill('#k-peso', '80'); await p.fill('#k-alt', '180'); await p.waitForTimeout(200); await p.click('.guarda-r'); await p.waitForTimeout(150);
o = await lee(); e = o['calorias.html'] && o['calorias.html'].h[0];
ok(e && e.vt.includes('–') && Math.abs(e.v - e.vt.split('–').map(x => parseFloat(x.replace(/\./g, ''))).reduce((a, x) => a + x / 2, 0)) < 1, 'calorías: un rango se guarda como su punto medio (' + (e && e.vt) + ' → ' + (e && e.v) + ')');
// 2. Datos de ejemplo: varias pruebas con historial
const D = (d) => new Date(d + 'T10:00:00').getTime();
const datos = {
  'test-silla.html': { titulo: 'Test de la silla en 30 segundos', h: [
    { t: D('2026-11-20'), texto: 'Test de la silla: 15 veces', v: 15, vt: '15', u: 'veces en 30 s', z: 'alto', zt: 'Dentro de lo normal para tu edad' },
    { t: D('2026-09-01'), texto: 'Test de la silla: 14 veces', v: 14, vt: '14', u: 'veces en 30 s', z: 'alto', zt: 'Dentro de lo normal para tu edad', n: 'Tras el verano' },
    { t: D('2026-06-01'), texto: 'Test de la silla: 12 veces', v: 12, vt: '12', u: 'veces en 30 s', z: 'medio', zt: 'En el límite bajo' },
    { t: D('2026-03-01'), texto: 'Test de la silla: 11 veces', v: 11, vt: '11', u: 'veces en 30 s', z: 'bajo', zt: 'Por debajo de lo normal' }] },
  'cintura-altura.html': { titulo: 'Cintura y altura: tu grasa abdominal', h: [
    { t: D('2026-11-01'), texto: 'Índice 0,51', v: 0.51, vt: '0,51', u: '', z: 'medio', zt: 'Grasa abdominal aumentada' },
    { t: D('2026-08-01'), texto: 'Índice 0,53', v: 0.53, vt: '0,53', u: '', z: 'medio', zt: 'Grasa abdominal aumentada' },
    { t: D('2026-05-01'), texto: 'Índice 0,56', v: 0.56, vt: '0,56', u: '', z: 'medio', zt: 'Grasa abdominal aumentada' }] },
  'calculadora-1rm.html': { titulo: 'Calculadora de 1RM y cargas', h: [
    { t: D('2026-11-10'), texto: 'Tabla de cargas · Sentadilla (1RM estimado 110 kg, Epley)', v: 110, vt: '110', u: 'kg', s: 'Sentadilla' },
    { t: D('2026-11-09'), texto: 'Tabla de cargas · Press de banca (1RM estimado 82,5 kg, Epley)', v: 82.5, vt: '82,5', u: 'kg', s: 'Press de banca' },
    { t: D('2026-10-10'), texto: 'Tabla de cargas · Sentadilla (1RM estimado 102,5 kg, Epley)', v: 102.5, vt: '102,5', u: 'kg', s: 'Sentadilla' },
    { t: D('2026-10-09'), texto: 'Tabla de cargas · Press de banca (1RM estimado 80 kg, Epley)', v: 80, vt: '80', u: 'kg', s: 'Press de banca' },
    { t: D('2026-09-01'), texto: 'Tabla de cargas (1RM estimado 60 kg, Epley)', v: 60, vt: '60', u: 'kg' }] },
  'calorias.html': { titulo: 'Calorías de mantenimiento', h: [
    { t: D('2026-11-15'), texto: 'Mantenimiento 2200–2500 kcal', v: 2350, vt: '2200–2500', u: 'kcal' },
    { t: D('2026-07-15'), texto: 'Mantenimiento 2300–2650 kcal', v: 2475, vt: '2300–2650', u: 'kcal' }] },
  'volumen-semanal.html': { titulo: 'Volumen semanal por músculo', h: [{ t: D('2026-11-12'), texto: 'Pecho: 12 series\nEspalda: 14 series' }] },
  'revision-medica.html': { titulo: '¿Necesito revisión médica antes de empezar?', h: [
    { t: D('2026-11-11'), texto: 'Puedes empezar\nSin síntomas' }, { t: D('2026-04-11'), texto: 'Consulta antes\nCon síntomas', n: 'Ya lo vio mi médico' }] } };
await p.evaluate(d => localStorage.setItem('fbe-resultados', JSON.stringify(d)), datos);
await p.goto(U + 'mis-resultados.html'); await p.waitForTimeout(500);
const cards = await p.$$eval('#mr-evo .evo-c', cs => cs.map(c => ({ t: c.querySelector('h3').textContent, d: c.querySelector('.evo-d').className.replace('evo-d ', ''), dt: c.querySelector('.evo-d').textContent, pts: c.querySelectorAll('.evo-p').length, zc: c.querySelector('.evo-zc') ? c.querySelector('.evo-zc').textContent : '' })));
ok(await p.isVisible('#mr-evo'), 'Mi evolución se ve con datos');
ok(cards.length === 5, 'cinco gráficas: silla, cintura, 1RM por ejercicio (dos) y calorías (' + cards.map(c => c.t).join(' | ') + ')');
const c = t => cards.find(x => x.t.includes(t)) || {};
ok(c('silla').d === 'mejor' && c('silla').pts === 4 && c('silla').dt.startsWith('↑ +4 veces') && c('silla').dt.includes('mejora'), 'silla: +4 veces, mejora, 4 puntos');
ok(c('Cintura').d === 'mejor' && c('Cintura').dt.startsWith('↓ −0,05'), 'cintura/altura: baja 0,05 y es mejora');
ok(c('Sentadilla').d === 'mejor' && c('Sentadilla').dt.startsWith('↑ +7,5 kg') && c('Press de banca').pts === 2, '1RM: una gráfica por ejercicio (sentadilla +7,5 kg)');
ok(c('Calorías').d === 'neutro' && !/mejora|empeora/.test(c('Calorías').dt), 'calorías: cambio sin juicio');
ok(c('silla').zc.includes('Dentro de lo normal'), 'la zona del último resultado sale con su texto');
// 3. Ratón y teclado
const g = await p.$('#mr-evo .evo-c:has-text("silla") .evo-graf'); await g.evaluate(x => { document.documentElement.style.scrollBehavior = 'auto'; x.scrollIntoView({ block: 'center', behavior: 'instant' }); }); await p.waitForTimeout(150); const bb = await g.boundingBox();
await p.mouse.move(bb.x + bb.width * 0.15, bb.y + bb.height * 0.5); await p.waitForTimeout(120);
let tip = await g.$eval('.evo-tip', t => ({ t: t.textContent, o: getComputedStyle(t).opacity }));
ok(tip.o === '1' && tip.t.includes('01/03/2026') && tip.t.includes('11 veces'), 'al pasar el ratón: fecha, cifra y zona (' + tip.t + ')');
await p.mouse.move(5, 5); await p.waitForTimeout(80);
await g.focus(); await p.keyboard.press('Home'); tip = await g.$eval('.evo-tip', t => t.textContent);
ok(tip.includes('01/03/2026'), 'teclado: Inicio va al primero');
await p.keyboard.press('ArrowRight'); tip = await g.$eval('.evo-tip', t => t.textContent);
ok(tip.includes('01/06/2026') && tip.includes('En el límite bajo'), 'teclado: flecha a la derecha, el siguiente');
await p.keyboard.press('End'); tip = await g.$eval('.evo-tip', t => t.textContent);
ok(tip.includes('20/11/2026'), 'teclado: Fin va al último');
ok(await g.$eval('.evo-p.act', x => x.dataset.i) === '3', 'el punto activo se agranda');
await p.keyboard.press('Tab'); ok(!(await g.evaluate(x => x.classList.contains('on'))), 'al salir, se apaga');
const filas = await p.$eval('#mr-evo .evo-c:has-text("silla") details', d => { d.open = true; return d.querySelectorAll('tbody tr').length; });
ok(filas === 4, 'Ver en tabla: cuatro filas');
await p.screenshot({ path: `${SALIDA}/evo-escritorio.png`, fullPage: true });
// 4. Informe para tu médico
await p.click('#mr-inf-b'); await p.waitForTimeout(400);
ok(await p.isVisible('#mr-inf') && await p.evaluate(() => document.activeElement.id) === 'mr-inf-h', 'el informe se abre y lleva el foco a su título');
let inf = await p.evaluate(() => ({ sec: document.querySelectorAll('#mr-inf-doc .inf-it').length, res: document.querySelectorAll('#mr-inf-doc .inf-res tbody tr').length, svgs: document.querySelectorAll('#mr-inf-doc svg').length, fu: document.querySelectorAll('#mr-inf-doc .inf-fu li').length, txt: document.getElementById('mr-inf-doc').textContent, chk: document.querySelectorAll('#mr-inf-sel input:checked').length }));
ok(inf.sec === 6 && inf.chk === 6, 'seis apartados, todos marcados');
ok(inf.res === 5 && inf.svgs === 5, 'resumen y cinco gráficas');
ok(inf.fu >= 6 && inf.txt.includes('Rikli'), 'fuentes de cada prueba');
ok(inf.txt.includes('Ya lo vio mi médico') && inf.txt.includes('Tras el verano') === false, 'anteriores con su nota (la del último resultado de la silla no aplica)');
ok(!/Pelayo/.test(inf.txt), 'la hoja no lleva el nombre de Pelayo (no la ha revisado él)');
await p.fill('#mr-inf-nombre', 'Ana Prueba'); await p.waitForTimeout(80);
ok((await p.textContent('#mr-inf-doc')).includes('Nombre: Ana Prueba'), 'el nombre sale en la hoja');
await p.uncheck('#mr-inf-sel input[value="volumen-semanal.html"]'); await p.waitForTimeout(80);
ok(await p.$$eval('#mr-inf-doc .inf-it', x => x.length) === 5, 'quitar una prueba la saca de la hoja');
ok(!JSON.stringify(await p.evaluate(() => ({ ...localStorage }))).includes('Ana Prueba'), 'el nombre no se guarda');
// Imprimir: solo la hoja (sin abrir el diálogo de verdad)
await p.evaluate(() => { window.print = () => { window.__imp = 1 } }); await p.click('#mr-inf-imp'); await p.waitForTimeout(150);
ok(await p.evaluate(() => window.__imp === 1 && !!document.getElementById('inf-print') && document.documentElement.classList.contains('imprime-inf')), 'imprimir prepara la hoja');
await p.emulateMedia({ media: 'print' });
const imp = await p.evaluate(() => ({ hoja: getComputedStyle(document.getElementById('inf-print')).display, otros: [...document.body.children].filter(x => x.id !== 'inf-print' && getComputedStyle(x).display !== 'none').length, color: getComputedStyle(document.querySelector('#inf-print h2')).color }));
ok(imp.hoja === 'block' && imp.otros === 0 && imp.color === 'rgb(21, 20, 35)', 'al imprimir solo sale la hoja, con tinta oscura');
await p.pdf({ path: `${SALIDA}/informe-medico.pdf`, format: 'A4', printBackground: true });
await p.emulateMedia({ media: 'screen' }); await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));
ok(await p.evaluate(() => !document.getElementById('inf-print') && !document.documentElement.classList.contains('imprime-inf')), 'después de imprimir se recoge');
await p.click('#mr-inf-x'); ok(!(await p.isVisible('#mr-inf')) && await p.evaluate(() => document.activeElement.id) === 'mr-inf-b', 'cerrar devuelve el foco al botón');
// 5. Borrar todo: la evolución desaparece
await p.evaluate(() => { localStorage.setItem('fbe-resultados', '{}'); }); await p.reload(); await p.waitForTimeout(300);
ok(!(await p.isVisible('#mr-evo')), 'sin datos, no hay evolución');
// 6. Móvil y oscuro: nada se sale
const m = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: 'dark' }); const q = await m.newPage(); q.on('pageerror', e => errs.push(e.message));
await q.goto(U + 'mis-resultados.html'); await q.evaluate(d => localStorage.setItem('fbe-resultados', JSON.stringify(d)), datos); await q.reload(); await q.waitForTimeout(400);
await q.click('#mr-inf-b'); await q.waitForTimeout(300);
const sale = await q.evaluate(() => { const w = document.documentElement.clientWidth; return [...document.querySelectorAll('#mr-evo *, #mr-inf *')].filter(x => { const r = x.getBoundingClientRect(); return r.width && (r.right > w + 1 || r.left < -1) && !x.closest('.evo-tip'); }).map(x => x.tagName + '.' + x.className).slice(0, 5); });
ok(sale.length === 0, 'móvil: nada se sale de la pantalla ' + sale.join(' '));
await q.screenshot({ path: `${SALIDA}/evo-movil-oscuro.png`, fullPage: true });
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
