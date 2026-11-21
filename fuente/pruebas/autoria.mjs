// Firma y fecha en las páginas de salud, «Cómo trabajo la evidencia» y datos de autor para buscadores
import fs from 'fs';
import { RAIZ } from './comun.mjs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const pags = fs.readdirSync(RAIZ).filter(f => f.endsWith('.html'));
const con = pags.filter(f => fs.readFileSync(RAIZ + '/' + f, 'utf8').includes('class="firma"'));
const deben = ['test-silla.html', 'calculadora-1rm.html', 'calorias.html', 'mitos.html', 'glosario.html', 'empieza-aqui.html', 'fuentes.html', 'profesionales.html', 'pauta-activa.html', 'evidencia.html'];
ok(deben.every(f => con.includes(f)), `firma en ${con.length} páginas (${deben.filter(f => !con.includes(f)).join(', ') || 'todas las esperadas'})`);
for (const f of con) {
  const h = fs.readFileSync(RAIZ + '/' + f, 'utf8'); const fi = h.match(/<p class="firma">[\s\S]*?<\/p>/)[0];
  const t = fi.match(/<time datetime="(\d{4}-\d{2}-\d{2})"/);
  const ld = [...h.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m => JSON.parse(m[1]));
  const wp = ld.find(x => x['@type'] === 'WebPage');
  const bien = t && wp && wp.dateModified === t[1] && wp.author && wp.author.name === 'Pelayo Fernández Cidón' && fi.includes('href="quien-soy.html"') && !/revisado por/i.test(fi);
  if (!bien) ok(false, f + ': firma o datos de autor incompletos');
  if (fi.includes('firma-c')) { const a = fi.match(/class="firma-c" href="(#[^"]+)"/)[1]; if (!h.includes(`id="${a.slice(1)}"`)) ok(false, `${f}: «Fuentes comprobadas» apunta a ${a}, que no existe`); }
}
ok(mal === 0, 'cada firma con fecha, autor, enlace a Quién soy y datos para buscadores (sin «revisado por»)');
const ev = fs.readFileSync(RAIZ + '/evidencia.html', 'utf8');
ok(['Quién está detrás', 'De dónde salen las cifras', 'Cómo compruebo cada fuente', 'Qué no es esta web'].every(x => ev.includes(x)), 'evidencia.html con sus cuatro partes');
// Declaraciones: solo las que hizo Pelayo el 21/11/2026, con sus palabras
ok(ev.includes('No cobro de marcas ni uso enlaces de afiliado') && ev.includes('Los preparo con ayuda de herramientas digitales y los reviso yo') && ev.includes('Hospital Universitario La Paz / Carlos III / Cantoblanco'), 'declaraciones de Pelayo (marcas y afiliados, cómo se preparan los textos, hospital)');
ok(!/conflicto|patrocin|revisado por/i.test(ev), 'sin otras declaraciones (conflictos, patrocinios, «revisado por»)');
ok(fs.readFileSync(RAIZ + '/index.html', 'utf8').includes('href="evidencia.html"'), 'enlazada desde el pie');
ok(fs.readFileSync(RAIZ + '/sitemap.xml', 'utf8').includes('evidencia.html'), 'en el sitemap');
console.log(mal ? 'FALLOS ' + mal : 'todo correcto');
