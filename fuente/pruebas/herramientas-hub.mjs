// Herramientas por objetivo: grupos, filtro por objetivo y buscador
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
const s = await servir(RAIZ, 4400); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const p = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://localhost:4400/herramientas.html'); await p.waitForTimeout(400);
const vis = () => p.evaluate(() => [...document.querySelectorAll('.hb-grupo .herr-mini')].filter(a => !a.hidden && !a.closest('.hb-grupo').hidden).length);
const total = await vis(); ok(total >= 14, 'todas visibles al entrar: ' + total);
ok(await p.evaluate(() => document.querySelectorAll('.hb-grupo').length) === 4, 'cuatro grupos');
await p.click('#hb-f button[data-g="evalua"]'); ok(await vis() === 5, 'filtro Evalúa: 5');
await p.click('#hb-f button[data-g=""]'); await p.fill('#hb-q', 'mayores'); await p.waitForTimeout(100);
const n = await vis(); ok(n >= 1 && n < total, 'buscar «mayores» filtra: ' + n);
await p.fill('#hb-q', 'cafeina'); ok(await vis() === 1, 'buscar sin tilde encuentra Cafeína');
await p.fill('#hb-q', 'xyzzy'); ok(await p.isVisible('#hb-nada'), 'sin resultados: aviso');
await p.fill('#hb-q', ''); ok(await vis() === total, 'al borrar vuelven todas');
await p.evaluate(() => document.querySelector('.hb-barra').scrollIntoView()); await p.screenshot({ path: `${SALIDA}/hub.png` });
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
