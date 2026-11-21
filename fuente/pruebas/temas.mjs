// Páginas de tema: existen, juntan lo que deben y están enlazadas
import fs from 'fs';
import { RAIZ } from './comun.mjs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const temas = ['envejecer', 'medicacion', 'dolor', 'nutricion', 'poco-tiempo'];
const mapa = fs.readFileSync(RAIZ + '/sitemap.xml', 'utf8');
for (const t of temas) {
  const f = `tema-${t}.html`; const h = fs.existsSync(RAIZ + '/' + f) ? fs.readFileSync(RAIZ + '/' + f, 'utf8') : '';
  const n = (re) => (h.match(re) || []).length;
  ok(h && n(/class="ea-paso"/g) >= 3 && n(/class="herr-mini"/g) >= 3 && n(/class="tm-mito"/g) >= 2 && n(/class="tm-term"/g) >= 4 && n(/class="tm-f"/g) >= 3 && h.includes('class="firma"') && mapa.includes(f),
    `${f}: ${n(/class="ea-paso"/g)} pasos, ${n(/class="herr-mini"/g)} herramientas, ${n(/class="tm-mito"/g)} mitos, ${n(/class="tm-term"/g)} palabras, ${n(/class="tm-b"/g)} envíos, ${n(/class="tm-f"/g)} fuentes`);
}
const ix = fs.readFileSync(RAIZ + '/index.html', 'utf8');
ok(temas.every(t => ix.includes(`href="tema-${t}.html"`)), 'el menú (Aprende y móvil) enlaza los cinco temas');
const ea = fs.readFileSync(RAIZ + '/empieza-aqui.html', 'utf8');
ok((ea.match(/class="ea-tema"/g) || []).length === 4, 'Empieza aquí enlaza cuatro perfiles con su tema');
ok(fs.readFileSync(RAIZ + '/herramientas.html', 'utf8').includes('tm-fila'), 'Herramientas tiene la fila «Por tema»');
ok(JSON.parse(fs.readFileSync(RAIZ + '/buscar.json', 'utf8')).filter(e => /^tema-/.test(e.u)).length === 5, 'los cinco temas en el buscador');
console.log(mal ? 'FALLOS ' + mal : 'todo correcto');
