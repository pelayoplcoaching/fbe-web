// Datos estructurados: que todos se lean y que estén los de la portada, Quién soy, Mitos, Herramientas y Recetas
import { RAIZ } from './comun.mjs';
import fs from 'fs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ld = f => [...fs.readFileSync(RAIZ + '/' + f, 'utf8').matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m => JSON.parse(m[1]));
let n = 0, err = [];
for (const f of fs.readdirSync(RAIZ).filter(f => f.endsWith('.html'))) { try { n += ld(f).length; } catch (e) { err.push(f + ': ' + e.message); } }
ok(!err.length, n + ' bloques de datos, todos se leen ' + err.join(' | '));
const graph = ld('index.html').flatMap(o => o['@graph'] || [o]);
const org = graph.find(o => o['@type'] === 'Organization'), web = graph.find(o => o['@type'] === 'WebSite');
ok(org && org.logo.endsWith('icono-512.png') && org.sameAs.length >= 4 && web && web.publisher['@id'] === org['@id'], 'portada: organización y sitio web');
ok(graph.some(o => o['@type'] === 'FAQPage'), 'portada: sigue su FAQ');
const qs = ld('quien-soy.html'), prof = qs.find(o => o['@type'] === 'ProfilePage');
ok(prof && prof.mainEntity['@type'] === 'Person' && prof.mainEntity.worksFor.some(w => w['@type'] === 'Hospital' && w.name.includes('La Paz')) && prof.mainEntity.hasCredential.length >= 5 && prof.mainEntity.hasCredential.some(c => c.identifier === '282875610'), 'Quién soy: perfil con hospital, credenciales y número de colegiado');
ok(!qs.some(o => o['@type'] === 'Person'), 'Quién soy: sin la persona repetida');
const mi = ld('mitos.html').find(o => o['@type'] === 'ItemList');
ok(mi && mi.itemListElement.length === 9 && mi.itemListElement.every(x => x.item['@type'] === 'ClaimReview' && x.item.reviewRating.alternateName && x.item.url.includes('mitos.html#')), 'Mitos: nueve ClaimReview con veredicto');
const html = fs.readFileSync(RAIZ + '/mitos.html', 'utf8'); ok(mi.itemListElement.every(x => html.includes('id="' + x.item.url.split('#')[1] + '"')), 'Mitos: cada ancla existe');
const he = ld('herramientas.html').find(o => o['@type'] === 'CollectionPage');
ok(he && he.mainEntity.itemListElement.length >= 16 && he.mainEntity.itemListElement.every(x => fs.existsSync(RAIZ + '/' + x.url.split('/').pop())), 'Herramientas: lista de herramientas que existen');
const re = ld('recetas.html').find(o => o['@type'] === 'ItemList'); ok(re && re.itemListElement.length === 10, 'Recetas: lista de las diez');
const gu = ld('guias.html').find(o => o['@type'] === 'ItemList');
ok(gu && gu.itemListElement.every(x => /^https:\/\/fuerzabasadaenevidencia\.com\/img\/guia-[\w-]+\.webp$/.test(x.item.image || '') && fs.existsSync(RAIZ + '/' + x.item.image.replace('https://fuerzabasadaenevidencia.com/', ''))), 'Guías: cada producto con su imagen, que existe (aviso de Search Console del 25/11/2026)');
const can = fs.readdirSync(RAIZ).filter(f => f.endsWith('.html') && !fs.readFileSync(RAIZ + '/' + f, 'utf8').includes('http-equiv="refresh"')).filter(f => !/<link rel="canonical" href="https:\/\/fuerzabasadaenevidencia\.com\//.test(fs.readFileSync(RAIZ + '/' + f, 'utf8')));
ok(can.length <= 1, 'canónicos apuntando al dominio final (sin canónico: ' + can.join(', ') + ')');
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); process.exit(0);
