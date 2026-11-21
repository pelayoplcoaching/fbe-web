import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
import fs from 'fs';
await servir(RAIZ, 4262);
const b = await chromium.launch(); let problemas = 0;
const U = 'http://localhost:4262/';
for (const pag of ['empieza-aqui', 'videos', 'profesionales', 'mitos', 'medios', 'index', 'herramientas', 'guias', 'quien-soy', 'pauta-activa']) for (const [w, h] of [[1280, 900], [390, 844]]) for (const tema of ['light', 'dark']) {
  const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce', colorScheme: tema });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => { if (r.url().includes('localhost')) errs.push('falla ' + r.url()); });
  await p.goto(`${U}${pag}.html`); await p.waitForTimeout(400);
  if (pag === 'mitos') await p.click('#mitos-todos');
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
  await p.waitForTimeout(300);
  const r = await p.evaluate(() => { const W = document.documentElement.clientWidth; const fuera = [...document.querySelectorAll('main *, footer *')].filter(e => { const b = e.getBoundingClientRect(); if (!(b.width && (b.right > W + 1 || b.left < -1)) || e.closest('.tabla-t-caja,[aria-hidden="true"],.tour,.mesa,.carril,.marquee') || getComputedStyle(e).position === 'fixed') return false; for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(a).overflowX)) return false; return true; }).slice(0, 5).map(e => e.tagName + '.' + String(e.className).slice(0, 25)); return { sw: document.documentElement.scrollWidth, W, fuera }; });
  if (r.sw > r.W || r.fuera.length || errs.length) problemas++, console.log('PROBLEMA', pag, w, tema, JSON.stringify(r), errs.join(' '));
  if (['empieza-aqui', 'videos', 'profesionales', 'mitos', 'medios', 'pauta-activa'].includes(pag)) await p.screenshot({ path: `${SALIDA}/s-${pag}-${w}-${tema}.png`, fullPage: true });
  await p.close();
}
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
const vis = () => p.evaluate(() => [...document.querySelectorAll('.ea-ruta')].filter(r => !r.hidden).map(r => r.dataset.p).join(','));
await p.goto(U + 'empieza-aqui.html'); console.log('empieza inicial:', await vis());
await p.click('#ea-perfil button[data-p="medicacion"]'); console.log('tras medicacion:', await vis(), new URL(p.url()).hash, await p.getAttribute('#ea-perfil button[data-p="medicacion"]', 'aria-pressed'));
await p.goto(U + 'empieza-aqui.html#dolor'); console.log('con #dolor:', await vis());
await p.goto(U + 'mitos.html'); const n = () => p.evaluate(() => [...document.querySelectorAll('.mito')].filter(m => !m.hidden).length + ' / ' + document.getElementById('mitos-n').textContent);
console.log('mitos todos:', await n());
await p.click('#mitos-f button[data-t="nutri"]'); console.log('nutri:', await n());
await p.click('#mitos-f button[data-t="mayores"]'); console.log('mayores:', await n());
await p.click('#mitos-f button[data-t=""]'); await p.click('#mitos-todos'); console.log('abiertas:', await p.evaluate(() => document.querySelectorAll('.mito details[open]').length), await p.textContent('#mitos-todos'));
await p.goto(U + 'mitos.html#artrosis'); console.log('artrosis abierta:', await p.evaluate(() => document.querySelector('#artrosis details').open));
await p.goto(U + 'videos.html'); await p.click('#vid'); await p.waitForTimeout(200); console.log('iframe:', await p.evaluate(() => { const f = document.querySelector('.vid-on iframe'); return f ? f.src.slice(0, 80) : 'NO'; }));
// enlaces locales de las paginas nuevas y del pie
const rotos = [];
for (const pag of ['empieza-aqui', 'videos', 'profesionales', 'mitos', 'medios', 'index', 'herramientas', 'guias', 'quien-soy', 'pauta-activa']) {
  const html = fs.readFileSync(`${RAIZ}/${pag}.html`, 'utf8');
  for (const m of html.matchAll(/href="([^"#:?]+\.html)(#[^"]*)?"/g)) { if (!fs.existsSync(RAIZ + '/' + m[1])) rotos.push(pag + ' -> ' + m[1]); if (m[2] && m[2].length > 1) { const d = fs.readFileSync(RAIZ + '/' + m[1], 'utf8'); if (!d.includes(`id="${m[2].slice(1)}"`) && !d.includes(`data-p="${m[2].slice(1)}"`)) rotos.push(pag + ' -> ' + m[1] + m[2]); } }
}
console.log('rotos:', rotos.length ? [...new Set(rotos)].join(' | ') : 0);
{ const q = await b.newPage(); await q.goto(U + 'medios.html'); const k = () => q.evaluate(() => [...document.querySelectorAll('.medio')].filter(m => !m.hidden).length);
console.log('medios todos:', await k()); await q.click('#medios-f button[data-t="Podcast"]'); console.log('podcasts:', await k()); await q.click('#medios-f button[data-t="Formación"]'); console.log('formacion:', await k());
console.log('pie con medios:', (await q.$$('footer a[href="medios.html"]')).length, '| sitemap:', fs.readFileSync(RAIZ + '/sitemap.xml', 'utf8').includes('medios.html')); await q.close(); }
console.log(problemas || rotos.length ? 'FALLOS ' + (problemas + rotos.length) : 'todo correcto'); await b.close(); process.exit(0);
