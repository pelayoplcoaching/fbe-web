// La barra de arriba no se sale de la pantalla a ningun ancho de ordenador (el boton «Pedir plaza» se cortaba a ~1220 px).
import { RAIZ, chromium, servir, paginas } from './comun.mjs';
const s = await servir(RAIZ, 8791); const b = await chromium.launch(); let mal = 0;
const pags = process.argv.slice(2).length ? process.argv.slice(2) : ['index', 'pedir-plaza', 'programas', 'tension', 'mi-panel', 'tarifas'];
for (const w of [761, 800, 900, 980, 1024, 1100, 1160, 1224, 1280, 1366, 1400, 1440, 1600]) {
  const p = await b.newPage({ viewport: { width: w, height: 800 } });
  for (const n of pags) {
    await p.goto(`http://localhost:8791/${n}.html`); await p.waitForTimeout(250);
    const r = await p.evaluate(() => { const W = document.documentElement.clientWidth, c = document.querySelector('header.cab, .cab'); if (!c) return null;
      const f = [...c.querySelectorAll('a, button')].filter(e => e.offsetParent && e.getBoundingClientRect().width > 0).map(e => ({ t: (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 18), d: Math.round(e.getBoundingClientRect().right), i: Math.round(e.getBoundingClientRect().left) }));
      const ap = [...c.querySelectorAll('a, button')].filter(e => e.offsetParent && (e.scrollWidth > e.clientWidth + 4 || e.scrollHeight > e.clientHeight + 6) && !e.closest('.logo, .marca')).map(e => ({ t: e.textContent.trim().slice(0, 18), apretado: e.clientWidth + '<' + e.scrollWidth, alto: e.clientHeight }));
      return { W, fuera: f.filter(x => x.d > W + 1 || x.i < -1).concat(ap) }; });
    if (r && r.fuera.length) { mal++; console.log(`✘ ${n} a ${w}px:`, JSON.stringify(r.fuera)); }
  }
  await p.close();
}
await b.close(); s.close(); console.log(mal ? `${mal} fallos` : 'la barra de arriba cabe a todos los anchos'); process.exit(mal ? 1 : 0);
