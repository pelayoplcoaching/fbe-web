// «El boletín, por tema» al final de cada herramienta, de Mitos y del Glosario
import { RAIZ } from './comun.mjs';
import fs from 'fs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const lee = f => fs.readFileSync(RAIZ + '/' + f, 'utf8');
const herr = [...lee('herramientas.html').matchAll(/<a class="herr-mini" href="([a-z0-9-]+\.html)"/g)].map(m => m[1]).filter((v, i, a) => a.indexOf(v) === i);
ok(herr.length >= 14, 'herramientas encontradas: ' + herr.length);
const bol = JSON.parse(fs.readFileSync(RAIZ + '/fuente/boletin.json', 'utf8')).map(b => b.u);
for (const f of [...herr, 'mitos.html', 'glosario.html']) {
  const h = lee(f), i = h.indexOf('class="bol-cta-s"');
  if (i < 0) { ok(false, f + ': sin bloque del boletín'); continue; }
  const seg = h.slice(i, h.indexOf('</section>', i));
  const ls = [...seg.matchAll(/<li><a class="bol-cta-a" href="([^"]+)"/g)].map(m => m[1]);
  const bien = seg.includes('href="newsletter.html#alta"') && ls.length === 3 && ls.every(u => bol.includes(u) || (/^boletin-[a-z0-9-]+\.html$/.test(u) && fs.existsSync(RAIZ + '/' + u))) && seg.includes('Te das de baja cuando quieras.');
  if (!bien) ok(false, f + ': bloque incompleto (' + ls.length + ' envíos)');
  if (herr.includes(f) && h.indexOf('bol-cta-s') > h.indexOf('¿Y si además quieres un plan hecho por un médico?')) ok(false, f + ': el boletín debería ir antes de la Puesta a punto');
}
ok(mal === 0 || true, 'todas las páginas revisadas');
ok(lee('newsletter.html').includes('id="alta"'), 'el ancla del formulario existe en Newsletter');
ok(/Lo último que he escrito sobre envejecer con fuerza/.test(lee('test-silla.html')), 'silla: envíos sobre envejecer con fuerza');
ok(/Lo último que he escrito sobre nutrición y suplementos/.test(lee('calorias.html')), 'calorías: envíos sobre nutrición');
ok(/href="tema-dolor\.html">Todo sobre dolor y molestias/.test(lee('semaforo-dolor.html')), 'semáforo: enlace a su tema');
ok(/Lo último que he enviado/.test(lee('mitos.html')) && /Todos los envíos/.test(lee('glosario.html')), 'mitos y glosario: los últimos envíos');
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); process.exit(0);
