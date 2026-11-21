// «Chequeo de 10 minutos»: ruta por cuatro herramientas, barra de pasos, «Guardar y seguir» y resumen por áreas
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
const s = await servir(RAIZ, 4404); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' }); await ctx.addInitScript(() => document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.scrollBehavior = 'auto'; })); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(p.url() + ' ' + e.message));
const U = 'http://localhost:4404/';
const est = () => p.$$eval('#chq-lista .chq-paso', ls => ls.map(l => ({ u: l.dataset.u, h: l.classList.contains('hecho'), e: l.querySelector('[data-est]').textContent, b: l.querySelector('.chq-b').textContent })));
// 1. Sin nada hecho
await p.goto(U + 'chequeo.html'); await p.waitForTimeout(300);
let e = await est();
ok(e.length === 4 && e.every(x => !x.h && x.e === 'Pendiente' && x.b.startsWith('Empezar')), 'cuatro pasos pendientes');
ok((await p.textContent('#chq-hechos')) === '0' && (await p.textContent('#chq-ir')) === 'Empezar el chequeo' && (await p.getAttribute('#chq-ir', 'href')) === 'revision-medica.html?chequeo=1', 'botón: empezar por la revisión médica');
ok(!(await p.isVisible('#resumen')) && !(await p.isVisible('#chq-reset')), 'sin resumen ni «empezar de nuevo»');
ok(await p.$$eval('.chq-o h3 a', as => as.every(a => a.href.includes('?chequeo=1'))), 'las dos opcionales abren en modo chequeo');
ok(await p.$$eval('#chq-por a[href^="fuentes.html#f-"]', as => as.length) === 5, 'por qué estas cuatro: cinco fuentes enlazadas');
// 2. Paso 1: revisión médica
await p.click('#chq-ir'); await p.waitForURL(/revision-medica\.html\?chequeo=1/);
ok(await p.evaluate(() => { const c = JSON.parse(localStorage.getItem('fbe-chequeo') || '{}'); const d = new Date(); d.setHours(0, 0, 0, 0); return c.inicio === d.getTime(); }), 'al empezar se apunta el inicio (desde hoy)');
ok((await p.textContent('.chq-barra .chq-et')) === 'Paso 1 de 4' && (await p.$eval('.chq-mini li[aria-current="step"]', l => l.textContent)).includes('Seguridad'), 'barra: paso 1 de 4, seguridad');
ok((await p.getAttribute('.chq-saltar', 'href')) === 'actividad-oms.html?chequeo=1', '«Saltar este paso» lleva al siguiente');
ok(!(await p.isVisible('.chq-sig')), 'sin resultado no hay «Guardar y seguir»');
await p.check('input[name="q-regular"][value="no"]', { force: true }); await p.check('input[name="q-enf"][value="no"]', { force: true }); await p.check('#q-ninguno', { force: true }); await p.waitForTimeout(150);
ok(await p.isVisible('.chq-sig') && (await p.textContent('.chq-sig')) === 'Guardar y seguir: actividad', 'con resultado: «Guardar y seguir: actividad»');
await p.click('.chq-sig'); await p.waitForURL(/actividad-oms\.html\?chequeo=1/);
ok(await p.evaluate(() => { const o = JSON.parse(localStorage.getItem('fbe-resultados') || '{}'); const e = o['revision-medica.html'] && o['revision-medica.html'].h[0]; return e && e.z && e.zt === 'Puedes empezar'; }), 'se guardó la revisión con su zona');
// 3. Paso 2: actividad
ok((await p.textContent('.chq-barra .chq-et')) === 'Paso 2 de 4' && await p.$eval('.chq-mini li.antes', l => l.textContent.includes('Seguridad')), 'barra: paso 2, el 1 marcado');
await p.fill('#a-mod', '100'); await p.fill('#a-vig', '30'); await p.fill('#a-fza', '2'); await p.waitForTimeout(150);
await p.click('.chq-sig'); await p.waitForURL(/test-silla\.html\?chequeo=1/);
// 4. Paso 3: silla
await p.fill('#s-edad', '72'); await p.fill('#s-reps', '12'); await p.waitForTimeout(150);
ok((await p.textContent('.chq-sig')) === 'Guardar y seguir: grasa abdominal', 'silla: siguiente, grasa abdominal');
await p.click('.chq-sig'); await p.waitForURL(/cintura-altura\.html\?chequeo=1/);
// 5. Paso 4: cintura y altura
ok((await p.textContent('.chq-saltar')) === 'Saltar y ver el resumen', 'último paso: saltar y ver el resumen');
await p.fill('#w-cin', '90'); await p.waitForTimeout(150);
ok((await p.textContent('.chq-sig')) === 'Guardar y ver el resumen', 'último paso: «Guardar y ver el resumen»');
await p.click('.chq-sig'); await p.waitForURL(/chequeo\.html#resumen/); await p.waitForTimeout(300);
// 6. Resumen
e = await est();
ok(e.every(x => x.h && x.e.startsWith('Hecho el') && x.b.startsWith('Repetir')), 'los cuatro pasos hechos');
ok((await p.textContent('#chq-hechos')) === '4' && (await p.textContent('#chq-ir')) === 'Ver tu resumen', '4 de 4 y «Ver tu resumen»');
const rs = await p.$$eval('#chq-rej .chq-r', cs => cs.map(c => ({ a: c.querySelector('.chq-a').textContent, z: c.className, v: c.querySelector('.chq-r-v b') ? c.querySelector('.chq-r-v b').textContent : '', zt: c.querySelector('.evo-zc') ? c.querySelector('.evo-zc').textContent : '', l: c.querySelectorAll('.chq-r-l a').length })));
ok(rs.length === 4 && rs.every(r => r.l >= 2), 'cuatro tarjetas con «Qué hacer ahora»');
ok(rs[0].a === 'Seguridad' && rs[0].zt === 'Puedes empezar' && !rs[0].v, 'seguridad: «Puedes empezar»');
ok(rs[1].v === '160' && rs[2].v === '12' && rs[3].v === '0,53', 'actividad 160 min, silla 12 veces, índice 0,53 (' + rs.map(r => r.v).join(', ') + ')');
ok(rs[3].z.includes('z-medio') && rs[3].zt.length > 3, 'cintura/altura en zona media con su texto');
const lk = await p.$$eval('#chq-rej a', as => as.map(a => a.getAttribute('href')));
const fs = await import('fs'); ok(lk.every(h => /^https?:/.test(h) || fs.existsSync(RAIZ + '/' + h.split('#')[0])), 'los enlaces del resumen existen');
await p.screenshot({ path: `${SALIDA}/chequeo-escritorio.png`, fullPage: true });
// 7. Opcional: SPPB en modo chequeo
await p.click('.chq-o h3 a[href^="test-sppb"]'); await p.waitForURL(/test-sppb\.html\?chequeo=1/);
ok((await p.textContent('.chq-barra .chq-et')).startsWith('Prueba opcional') && (await p.textContent('.chq-saltar')) === 'Volver al chequeo', 'SPPB: prueba opcional con «Volver al chequeo»');
// 8. Empezar de nuevo
await p.goto(U + 'chequeo.html'); await p.waitForTimeout(250); await p.click('#chq-reset'); await p.waitForTimeout(150);
e = await est();
ok(e.every(x => !x.h && x.e.includes('antes de este chequeo') && x.b.startsWith('Hacer')), 'empezar de nuevo: lo anterior queda como «antes de este chequeo»');
ok(!(await p.isVisible('#resumen')) && (await p.textContent('#chq-av')).includes('Mis resultados'), 'sin resumen y aviso de que siguen en Mis resultados');
// 9. Accesos y el informe con #informe
await p.goto(U + 'herramientas.html'); ok(await p.isVisible('.chq-tarj a[href="chequeo.html"]'), 'Herramientas: tarjeta del chequeo');
ok(await p.$('#nm-herr a[href="chequeo.html"]') !== null && await p.$('.mm a[href="chequeo.html"]') !== null, 'menú y menú del móvil');
await p.goto(U + 'empieza-aqui.html'); ok(await p.$('.ea-chq a[href="chequeo.html"]') !== null, 'Empieza aquí: enlace al chequeo');
await p.goto(U + 'mis-resultados.html#mr-inf'); await p.waitForTimeout(500); ok(await p.isVisible('#mr-inf'), 'Mis resultados con #mr-inf abre el informe');
await p.evaluate(() => localStorage.clear()); await p.goto(U + 'mis-resultados.html'); await p.waitForTimeout(250); ok(await p.isVisible('.mr-chq a[href="chequeo.html"]'), 'Mis resultados vacío: sugiere el chequeo');
// 10. Móvil: nada se sale
const m = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const q = await m.newPage(); q.on('pageerror', e => errs.push(e.message));
await q.goto(U + 'test-silla.html?chequeo=1'); await q.waitForTimeout(300);
const sale = async () => q.evaluate(() => { const w = document.documentElement.clientWidth; return [...document.querySelectorAll('main *')].filter(x => { const r = x.getBoundingClientRect(); return r.width && (r.right > w + 1 || r.left < -1) && !x.closest('.tool-tira,.evo-tip,.oculto'); }).map(x => x.tagName + '.' + x.className).slice(0, 4); });
let sl = await sale(); ok(sl.length === 0, 'móvil, barra de pasos: nada se sale ' + sl.join(' '));
await q.screenshot({ path: `${SALIDA}/chequeo-barra-movil.png` });
await q.goto(U + 'chequeo.html'); await q.waitForTimeout(300); sl = await sale(); ok(sl.length === 0, 'móvil, chequeo: nada se sale ' + sl.join(' '));
await q.screenshot({ path: `${SALIDA}/chequeo-movil.png`, fullPage: true });
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
