// Menu con desplegables: seccion marcada, raton, teclado, Escape, movil y que el desplegable quepa en pantalla
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
const s = await servir(RAIZ, 4399); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
for (const tema of ['dark', 'light']) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, colorScheme: tema }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:4399/calculadora-1rm.html'); await p.waitForTimeout(400);
  ok(await p.evaluate(() => document.querySelector('.nav-b[aria-controls="nm-herr"]').classList.contains('aqui')), 'Herramientas marcado como sección actual');
  await p.hover('.nav-b[aria-controls="nm-herr"]'); await p.waitForTimeout(350);
  ok(await p.isVisible('#nm-herr'), 'se abre al pasar el ratón'); await p.screenshot({ path: `${SALIDA}/menu-herr-${tema}.png`, clip: { x: 0, y: 0, width: 1280, height: 560 } });
  await p.mouse.move(640, 800); await p.waitForTimeout(400); ok(!(await p.isVisible('#nm-herr')), 'se cierra al salir');
  await p.focus('.nav-b[aria-controls="nm-aprende"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(200);
  ok(await p.isVisible('#nm-aprende'), 'Enter lo abre'); await p.keyboard.press('ArrowDown'); ok(await p.evaluate(() => document.activeElement.closest('#nm-aprende') !== null), 'flecha abajo entra en los enlaces');
  await p.screenshot({ path: `${SALIDA}/menu-ap-${tema}.png`, clip: { x: 0, y: 0, width: 1280, height: 480 } });
  await p.keyboard.press('Escape'); await p.waitForTimeout(150); ok(!(await p.isVisible('#nm-aprende')) && await p.evaluate(() => document.activeElement.matches('.nav-b')), 'Escape cierra y devuelve el foco');
  ok(errs.length === 0, 'sin errores ' + errs.join('|')); await p.close();
}
const m = await b.newPage({ viewport: { width: 390, height: 844 } }); await m.goto('http://localhost:4399/index.html'); await m.waitForTimeout(400);
await m.click('.menu summary'); await m.waitForTimeout(400); await m.screenshot({ path: `${SALIDA}/menu-movil.png` });
ok(await m.evaluate(() => [...document.querySelectorAll('.menu .mm-h')].map(x => x.textContent).join('|')) === 'Asesoría|Aprende|Herramientas|Por tema|Ayuda', 'menú del móvil con cinco secciones (Asesoría, Aprende, Herramientas, Por tema, Ayuda)');
for (const w of [1000, 1100, 1180, 1400]) { const q = await b.newPage({ viewport: { width: w, height: 800 } }); await q.goto('http://localhost:4399/index.html'); await q.waitForTimeout(300); await q.click('.nav-b[aria-controls="nm-herr"]'); await q.waitForTimeout(300); const r = await q.evaluate(() => { const x = document.getElementById('nm-herr').getBoundingClientRect(); return [Math.round(x.left), Math.round(x.right), document.documentElement.scrollWidth]; }); ok(r[0] >= 0 && r[1] <= w && r[2] <= w, `desplegable dentro de la pantalla a ${w} px ${r}`); await q.close(); }
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
