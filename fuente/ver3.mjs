import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import { servir } from '/home/claude/app-atletas/test/servidor.mjs';
await servir((process.env.FBE_SAL || '..'), 4196);
const b = await chromium.launch();
const pags = ['index', 'quien-soy', 'programas', 'puesta-a-punto', 'guias', 'newsletter', 'dudas', '404'];
for (const [w, h, pre] of [[1280, 900, 'x'], [390, 800, 'y']]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }); const errs = []; p.on('pageerror', (e) => errs.push(e.message)); p.on('requestfailed', (r) => { if (!/fonts|mlcdn|mailerlite/.test(r.url())) errs.push('falla ' + r.url().slice(-40)); });
  for (const n of pags) {
    await p.goto(`http://localhost:4196/${n}.html`); await p.waitForTimeout(700);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    console.log(w, n, 'alto', H, 'desborde', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth), 'rotos', await p.evaluate(() => [...document.querySelectorAll('a[href]')].filter((a) => !a.getAttribute('href') || a.getAttribute('href') === '#').length), errs.splice(0).join(' | ').slice(0, 200));
    if (n !== 'index') await p.screenshot({ path: `${pre}3-${n}.png`, fullPage: true });
  }
  if (w === 1280) {
    await p.goto('http://localhost:4196/programas.html'); await p.click('.elige [data-g="n"] [data-v="0"]'); await p.click('.elige [data-g="r"] [data-v="0"]');
    console.log('elige:', await p.textContent('#elige-t'), '| top:', await p.evaluate(() => document.querySelector('.plan.top').id), '| col yo:', await p.evaluate(() => document.querySelectorAll('.compara.ancha .yo').length));
    await p.click('.elige [data-g="r"] [data-v="2"]'); console.log('elige:', await p.textContent('#elige-t'));
    await p.goto('http://localhost:4196/guias.html'); await p.click('#filtro [data-t="salud"]'); console.log('filtro:', await p.textContent('#cuantas'), await p.evaluate(() => [...document.querySelectorAll('.guia')].filter((g) => g.offsetParent).length));
    await p.goto('http://localhost:4196/dudas.html'); await p.fill('#busca', 'creatína'); console.log('marcas:', await p.evaluate(() => document.querySelectorAll('mark').length)); console.log('busca:', await p.textContent('#halla'), await p.evaluate(() => [...document.querySelectorAll('.faq details')].filter((g) => g.offsetParent).length)); await p.fill('#busca', 'zzzz'); console.log('vacio visible:', await p.evaluate(() => !document.getElementById('vacio').hidden));
    await p.fill('#busca', ''); await p.click('#todas'); console.log('abiertas:', await p.evaluate(() => document.querySelectorAll('.lista-d details[open]').length)); await p.goto('http://localhost:4196/dudas.html#debo-pesarme-todos-los-dias'); await p.waitForTimeout(300); console.log('hash abre:', await p.evaluate(() => document.getElementById('debo-pesarme-todos-los-dias').open)); await p.goto('http://localhost:4196/guias.html'); await p.click('#emp [data-g="4"]'); console.log('empieza:', await p.textContent('#emp-t')); await p.goto('http://localhost:4196/index.html'); await p.waitForTimeout(800); console.log('img rotas portada:', await p.evaluate(async () => { const r = []; for (const i of document.querySelectorAll('img[src^="img/"]')) { i.loading = 'eager'; try { await i.decode(); } catch (e) { r.push(i.src); } } return r.length + ' de ' + document.querySelectorAll('img[src^="img/"]').length; })); await p.goto('http://localhost:4196/puesta-a-punto.html'); await p.click('#copia'); await p.waitForTimeout(300); console.log('copia:', await p.textContent('#copia-ok'));
    const q = await b.newPage({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark' }); for (const n of ['programas', 'guias']) { await q.goto(`http://localhost:4196/${n}.html`); await q.waitForTimeout(600); await q.evaluate(() => document.querySelectorAll('.sube').forEach((e) => e.classList.add('ya'))); await q.screenshot({ path: `o3-${n}.png`, fullPage: true }); } await q.close();
  }
  await p.close();
}
await b.close(); process.exit(0);
