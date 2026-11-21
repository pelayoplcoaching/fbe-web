// Página de Fuentes y enlaces a PubMed en herramientas, mitos y portada
import fs from 'fs';
import { chromium, servir, RAIZ } from './comun.mjs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const datos = JSON.parse(fs.readFileSync(RAIZ + '/fuente/fuentes.json', 'utf8')).fuentes;
const pm = datos.filter(f => f.pmid).map(f => f.pmid);
ok(new Set(pm).size === pm.length, `sin PMID repetidos (${pm.length} en PubMed)`);
ok(datos.every(f => f.pmid || f.doi || f.url || /Libro|libro/.test(f.nota + f.ti + f.rev) || f.id === 'epley1985' || f.id === 'acsm2021'), 'cada ficha tiene enlace o es un libro sin enlace');
const html = fs.readFileSync(RAIZ + '/fuentes.html', 'utf8');
const ids = [...html.matchAll(/<article class="fu[^"]*" id="f-([^"]+)"/g)].map(m => m[1]);
ok(ids.length === datos.length, `fuentes.html tiene las ${datos.length} fichas (${ids.length})`);
// Herramientas: cada cita con su ficha
const herr = fs.readdirSync(RAIZ).filter(f => f.endsWith('.html')).filter(f => fs.readFileSync(RAIZ + '/' + f, 'utf8').includes('class="fuentes-t"'));
let citas = 0, sin = [];
for (const f of herr) {
  const h = fs.readFileSync(RAIZ + '/' + f, 'utf8'); const ol = h.match(/<ol class="fuentes-t">([\s\S]*?)<\/ol>/)[1];
  for (const li of ol.match(/<li>[\s\S]*?<\/li>/g)) { citas++; const m = li.match(/href="fuentes\.html#f-([^"]+)"/); if (!m || !ids.includes(m[1])) sin.push(f); }
  ok(h.includes('id="fuentes"') && h.includes('class="f-todas"'), `${f}: ancla #fuentes y enlace a todas`);
}
ok(sin.length === 0, `${citas} citas de ${herr.length} herramientas con su ficha ${sin.join(', ')}`);
// Mitos y portada
const mi = fs.readFileSync(RAIZ + '/mitos.html', 'utf8');
const mf = mi.match(/<p class="mito-fuente">[\s\S]*?<\/p>/g) || [];
ok(mf.length >= 9 && mf.every(p => p.includes('class="f-enl"') && p.includes('pubmed.ncbi.nlm.nih.gov')), `los ${mf.length} mitos enlazan a PubMed`);
const ix = fs.readFileSync(RAIZ + '/index.html', 'utf8');
ok(/<section id="evidencia" class="ciencia/.test(ix) && ix.includes('href="fuentes.html"'), 'portada: #evidencia y enlace a Fuentes');
ok(fs.readFileSync(RAIZ + '/sitemap.xml', 'utf8').includes('fuentes.html'), 'en el sitemap');
ok(JSON.parse(fs.readFileSync(RAIZ + '/buscar.json', 'utf8')).filter(e => e.y === 'Fuente').length === datos.length, 'el buscador tiene una entrada por ficha');
// En el navegador: filtro y búsqueda
const s = await servir(RAIZ, 4408); const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://localhost:4408/fuentes.html'); await p.waitForTimeout(300);
await p.fill('#fu-q', 'schoenfeld'); ok((await p.textContent('#fu-n')) === '3 fuentes', 'buscar «schoenfeld»: 3 fuentes');
await p.fill('#fu-q', 'cafeina'); const nc = parseInt(await p.textContent('#fu-n')); ok(nc >= 3, `buscar «cafeina» (sin tilde): ${nc} fuentes`);
await p.fill('#fu-q', 'zzzz'); ok(!(await p.isHidden('#fu-nada')), 'sin resultados: aviso');
await p.fill('#fu-q', ''); await p.click('#fu-f button[data-t="ensayo"]');
const ne = await p.$$eval('.fu:not([hidden])', a => a.map(x => x.dataset.t)); ok(ne.length > 0 && ne.every(t => t === 'ensayo'), `filtro «Ensayo»: ${ne.length}`);
await p.goto('http://localhost:4408/fuentes.html?q=1RM'); await p.waitForTimeout(300);
ok(parseInt(await p.textContent('#fu-n')) >= 3, 'fuentes.html?q=1RM filtra al cargar');
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
await b.close(); s.close();
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); process.exit(0);
