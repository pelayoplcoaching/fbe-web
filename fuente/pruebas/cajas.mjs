// Busca textos que se salen de su tarjeta (no solo de la pantalla)
import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
await servir(RAIZ, 4380);
const pags = process.argv.slice(2).length ? process.argv.slice(2) : paginas(); const b = await chromium.launch(); let total = 0;
for (const pag of pags) for (const w of [1280, 1100, 390]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
  await p.goto(`http://localhost:4380/${pag}.html`); await p.addStyleTag({ content: 'section.lenta{content-visibility:visible!important}.js .sube{opacity:1!important;transform:none!important}' + (process.env.EXTRA || '') }); await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const out = [];
    const caja = (e) => { for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const cs = getComputedStyle(a); if (['SECTION', 'MAIN', 'HEADER', 'FOOTER', 'NAV', 'FORM'].includes(a.tagName) && !a.className) continue; const bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.backgroundImage !== 'none'; const bd = parseFloat(cs.borderLeftWidth) > 0 && parseFloat(cs.borderRightWidth) > 0; if ((bg || bd) && parseFloat(cs.borderTopLeftRadius) > 4) return a; } return null; };
    for (const e of document.querySelectorAll('main *, .hero *, footer *')) {
      if (e.closest('[aria-hidden="true"],[hidden],.cinta,.carril,.recetas,.tabla-t-caja,.tabla-marco,svg,dialog,.sr,.oculto')) continue;
      const hasText = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!hasText) continue;
      const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
      const c = caja(e); if (!c) continue; const cs = getComputedStyle(c); if (cs.overflowX !== 'visible') continue;
      const rc = c.getBoundingClientRect();
      if (r.right > rc.right + 2 || r.left < rc.left - 2) out.push({ t: e.tagName.toLowerCase() + '.' + [...e.classList].join('.'), txt: e.textContent.trim().slice(0, 40), caja: c.tagName.toLowerCase() + '.' + [...c.classList].join('.'), sale: Math.round(Math.max(r.right - rc.right, rc.left - r.left)) });
    }
    return out;
  });
  if (r.length) { total += r.length; console.log(pag, w, JSON.stringify(r.slice(0, 6))); }
  await p.close();
}
console.log(total ? 'salen: ' + total : 'nada se sale de su tarjeta'); await b.close(); process.exit(0);
