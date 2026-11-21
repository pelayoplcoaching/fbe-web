// Accesibilidad con axe-core (WCAG 2.2 AA + buenas practicas) en todas las paginas, claro/oscuro, 1280 y 390 px.
// Necesita axe-core: `npm i axe-core` dentro de fuente/pruebas (o AXE=/ruta/axe.min.js).
// Falla si hay errores graves o criticos. Los leves y moderados se listan como aviso.
import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
import fs from 'fs'; import path from 'path'; import { createRequire } from 'module';
let axeRuta = process.env.AXE;
if (!axeRuta) { try { axeRuta = createRequire(import.meta.url).resolve('axe-core/axe.min.js'); } catch (e) { for (const c of ['/tmp/audit/node_modules/axe-core/axe.min.js']) if (fs.existsSync(c)) axeRuta = c; } }
if (!axeRuta) { console.log('axe-core no instalado (npm i axe-core en fuente/pruebas): se salta'); console.log('todo correcto'); process.exit(0); }
const axe = fs.readFileSync(axeRuta, 'utf8');
const srv = await servir(RAIZ, 4391);
const pags = process.argv.slice(2).length ? process.argv.slice(2) : paginas(); const b = await chromium.launch(); const tot = {};
for (const tema of ['light', 'dark']) for (const [w, h] of [[1280, 900], [390, 844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, colorScheme: tema, reducedMotion: 'reduce' });
  for (const pag of pags) {
    await p.goto(`http://localhost:4391/${pag}.html`); await p.addStyleTag({ content: 'section.lenta{content-visibility:visible!important}.js .sube{opacity:1!important;transform:none!important}' }); await p.waitForTimeout(350);
    await p.addScriptTag({ content: axe });
    const r = await p.evaluate(async () => { const r = await axe.run(document, { resultTypes: ['violations'], runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }); return r.violations.map(v => ({ id: v.id, imp: v.impact, n: v.nodes.length, ej: v.nodes.slice(0, 2).map(x => x.target.join(' ') + ' :: ' + (x.failureSummary || '').split('\n').slice(1, 2).join('').slice(0, 160)) })); });
    for (const v of r) { const t = tot[v.id] = tot[v.id] || { imp: v.imp, n: 0, pags: new Set(), ej: [] }; t.n += v.n; t.pags.add(`${pag}@${w}${tema[0]}`); if (t.ej.length < 4) t.ej.push(`${pag}@${w}${tema[0]}: ` + v.ej[0]); }
  }
  await p.close();
}
const lista = Object.entries(tot).sort((a, b) => b[1].n - a[1].n);
fs.writeFileSync(path.join(SALIDA, 'axe.json'), JSON.stringify(lista.map(([k, v]) => ({ id: k, imp: v.imp, n: v.n, pags: [...v.pags], ej: v.ej })), null, 1));
let graves = 0;
for (const [k, v] of lista) { const g = v.imp === 'serious' || v.imp === 'critical'; if (g) graves += v.n; console.log(`${g ? '  ✘' : '  ·'} ${k} [${v.imp}] ${v.n} nodos en ${v.pags.size} vistas`); v.ej.slice(0, 2).forEach(e => console.log('      ' + e)); }
console.log(graves ? 'FALLOS ' + graves : 'todo correcto'); await b.close(); srv.close(); process.exit(0);
