// «Recetas con proteína»: diez recetas de muestra, filtros, orden y «Tu día»
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
import fs from 'fs';
const s = await servir(RAIZ, 4406); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' }); await ctx.addInitScript(() => document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.scrollBehavior = 'auto'; }));
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
const U = 'http://localhost:4406/';
const datos = JSON.parse(fs.readFileSync(RAIZ + '/fuente/ext/recetas.json', 'utf8'));
await p.goto(U + 'recetas.html'); await p.waitForTimeout(300);
const vis = () => p.$$eval('#rec-rej .rec', cs => cs.filter(c => !c.hidden).map(c => ({ c: c.dataset.c, p: +c.dataset.p, k: +c.dataset.k, m: +c.dataset.m, t: c.dataset.t })));
let v = await vis();
ok(v.length === 10 && (await p.textContent('#rec-n')) === '10 recetas', 'diez recetas a la vista');
ok(v.every((x, i) => !i || v[i - 1].p >= x.p), 'por defecto, de más a menos proteína');
// Los datos de cada tarjeta son los del recetario
const t0 = await p.$eval('.rec[data-c="03.17"]', c => ({ h: c.querySelector('h3').textContent, mc: [...c.querySelectorAll('.mc b')].map(b => b.textContent), x: c.querySelector('.rec-x').textContent, tr: (c.querySelector('.rec-tr') || {}).textContent || '' }));
const r0 = datos.find(r => r.libro.codigo === '03.17');
ok(t0.h === r0.nombre && t0.mc[0] === String(r0.kcal) && t0.mc[1] === Math.round(r0.proteina_g) + ' g' && t0.mc[2] === String(r0.minutos), 'ficha: nombre, kcal, proteína y minutos del recetario');
ok(t0.x.includes('7,4 g de proteína por 100 kcal') && t0.tr.includes(r0.libro.nota), 'proteína por 100 kcal calculada (30/403) y el truco');
ok(await p.$eval('.rec[data-c="04.50"] .rec-x', e => e.textContent.includes('Para táper: 4 días o congelado')), 'táper: el texto del recetario');
// Filtros
await p.click('#rec-f button[data-f="vegana"]'); v = await vis();
ok(v.length === datos.filter(r => r.etiquetas.includes('vegana')).length && v.every(x => x.t.includes('vegana')), 'filtro vegana: ' + v.length);
await p.click('#rec-f button[data-f="sin-gluten"]'); v = await vis();
ok(v.length === datos.filter(r => r.etiquetas.includes('vegana') && r.etiquetas.includes('sin gluten')).length, 'vegana y sin gluten a la vez: ' + v.length);
await p.click('#rec-f button[data-f="microondas"]'); v = await vis();
ok(v.length === 0 && await p.isVisible('#rec-vacio'), 'sin coincidencias: aviso');
await p.click('#rec-f button[data-f=""]'); v = await vis();
ok(v.length === 10 && (await p.getAttribute('#rec-f button[data-f=""]', 'aria-pressed')) === 'true', '«Todas» quita los filtros');
await p.click('#rec-f button[data-f="taper"]'); v = await vis();
ok(v.length === datos.filter(r => !String(r.libro.batch).startsWith('No')).length, 'para táper: ' + v.length);
await p.click('#rec-f button[data-f=""]');
// Orden
await p.selectOption('#rec-o', 't'); v = await vis(); ok(v.every((x, i) => !i || v[i - 1].m <= x.m), 'orden: menos tiempo primero');
await p.selectOption('#rec-o', 'pk'); v = await vis(); ok(v.every((x, i) => !i || v[i - 1].p / v[i - 1].k >= x.p / x.k), 'orden: proteína por caloría');
// Tu día
await p.click('.rec[data-c="09.01"] .rec-b'); await p.click('.rec[data-c="04.a04"] .rec-b');
const pr = Math.round(27.3 + 48.1), kc = 276 + 570;
ok((await p.textContent('#rec-p')) === pr + ' g' && (await p.textContent('#rec-sum')).includes(kc + ' kcal') && (await p.textContent('#rec-sum')).includes('te faltan ' + (140 - pr) + ' g'), 'tu día: suma ' + pr + ' g y ' + kc + ' kcal, faltan ' + (140 - pr));
ok(await p.$$eval('#rec-lista li', l => l.length) === 2 && (await p.getAttribute('.rec[data-c="09.01"] .rec-b', 'aria-pressed')) === 'true', 'lista del día y botones marcados');
await p.fill('#rec-meta', '70'); await p.waitForTimeout(80);
ok((await p.textContent('#rec-sum')).startsWith('Proteína del día, cumplida'), 'con objetivo 70 g: cumplida');
await p.reload(); await p.waitForTimeout(300);
ok((await p.textContent('#rec-p')) === pr + ' g' && (await p.inputValue('#rec-meta')) === '70', 'se recuerda al volver');
await p.click('#rec-vaciar'); ok((await p.textContent('#rec-p')) === '0 g' && !(await p.isVisible('#rec-vaciar')), 'vaciar el día');
// Enlaces de entrada
await p.goto(U + 'index.html'); ok(await p.$('a[href="recetas.html"]') !== null, 'portada enlaza a recetas');
await p.goto(U + 'tema-nutricion.html'); ok(await p.$$eval('#recetas-tema a[href^="recetas.html#r-"]', a => a.length) === 3, 'tema de nutrición: tres recetas');
const ancla = await p.$eval('#recetas-tema a[href^="recetas.html#r-"]', a => a.getAttribute('href').split('#')[1]);
await p.goto(U + 'recetas.html#' + ancla); await p.waitForTimeout(300); ok(await p.$('#' + ancla) !== null, 'las anclas de cada receta existen');
ok(await p.$('#nm-aprende a[href="recetas.html"]') !== null && await p.$('.mm a[href="recetas.html"]') !== null, 'menú Aprende y móvil');
// Móvil
const m = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const q = await m.newPage(); q.on('pageerror', e => errs.push(e.message));
await q.goto(U + 'recetas.html'); await q.addStyleTag({ content: '.js .sube{opacity:1!important;transform:none!important}' }); await q.waitForTimeout(300);
const sale = await q.evaluate(() => { const w = document.documentElement.clientWidth; return [...document.querySelectorAll('main *')].filter(x => { const r = x.getBoundingClientRect(); return r.width && (r.right > w + 1 || r.left < -1); }).map(x => x.tagName + '.' + x.className).slice(0, 4); });
ok(sale.length === 0, 'móvil: nada se sale ' + sale.join(' '));
await q.screenshot({ path: `${SALIDA}/recetas-movil.png`, fullPage: true });
await p.goto(U + 'recetas.html'); await p.addStyleTag({ content: '.js .sube{opacity:1!important;transform:none!important}' }); await p.waitForTimeout(300); await p.screenshot({ path: `${SALIDA}/recetas-escritorio.png`, fullPage: true });
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
