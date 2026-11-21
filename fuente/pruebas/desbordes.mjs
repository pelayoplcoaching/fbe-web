// Uso: node g.mjs pag1 pag2 ...  -> capturas <salida>/g-<pag>-<w>-<tema>.png y avisos de desbordes/errores
import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
await servir(RAIZ, 4291);
const pags = process.argv.slice(2).length ? process.argv.slice(2) : paginas(); const b = await chromium.launch(); let mal = 0;
for (const pag of pags) for (const [w, h] of [[1280, 900], [390, 844]]) for (const tema of ['light', 'dark']) {
  const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce', colorScheme: tema });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => { if (r.url().includes('localhost')) errs.push('falla ' + r.url()); });
  await p.goto(`http://localhost:4291/${pag}.html`); await p.addStyleTag({ content: 'section.lenta{content-visibility:visible!important}' }); await p.waitForTimeout(300);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } scrollTo(0, 0); });
  await p.waitForTimeout(250);
  const r = await p.evaluate(() => { const W = document.documentElement.clientWidth; const fuera = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); if (!b.width || e.closest('[aria-hidden="true"],.tabla-t-caja,.carril,.marquee,.cinta,[hidden]')) return false; let a = e.parentElement, cl = false; while (a && a !== document.body) { const cs = getComputedStyle(a); if (/(auto|scroll|hidden|clip)/.test(cs.overflowX)) { cl = true; break; } a = a.parentElement; } return !cl && (b.right > W + 1 || b.left < -1); }).slice(0, 4).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 30)); return { sw: document.documentElement.scrollWidth, W, fuera }; });
  if (r.sw > r.W || r.fuera.length || errs.length) { mal++; console.log('PROBLEMA', pag, w, tema, JSON.stringify(r), errs.join('|')); }
  if (tema === 'light' || w === 1280) await p.screenshot({ path: `${SALIDA}/g-${pag}-${w}-${tema}.png`, fullPage: true });
  await p.close();
}
console.log(mal ? 'con problemas: ' + mal : 'sin problemas'); await b.close(); process.exit(0);
