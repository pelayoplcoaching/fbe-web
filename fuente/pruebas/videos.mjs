// Vídeos en cuadrícula: el último arriba, todos abajo con filtro por tema, búsqueda y orden; reproducir arriba; enlaces #v-<id> y ?t=<tema>
import { chromium, servir, RAIZ } from './comun.mjs';
import fs from 'fs';
const s = await servir(RAIZ, 4419); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
await ctx.route(/ytimg\.com|youtube/, r => r.abort());
await ctx.addInitScript(() => document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.scrollBehavior = 'auto'; }));
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
const U = 'http://localhost:4419/';
const V = JSON.parse(fs.readFileSync(RAIZ + '/fuente/videos.json', 'utf8')).sort((a, b) => b.f.localeCompare(a.f));
await p.goto(U + 'videos.html'); await p.waitForTimeout(300);
const vis = () => p.$$eval('#vid-rej .vc', ls => ls.filter(l => !l.hidden).map(l => ({ id: l.querySelector('a').dataset.v, f: l.dataset.f, s: +l.dataset.s, g: l.dataset.g, t: l.querySelector('b').textContent })));
let v = await vis();
ok(v.length === V.length && (await p.textContent('#vid-n')) === V.length + ' vídeos', `los ${V.length} vídeos a la vista`);
ok(v.every((x, i) => x.id === V[i].id && x.t === V[i].t), 'mismo orden (más reciente primero) y mismos títulos que videos.json');
ok((await p.getAttribute('#vid', 'data-v')) === V[0].id && (await p.textContent('#vid b')) === V[0].t, 'arriba, el último vídeo');
// Filtro por tema
await p.click('#vid-chips button[data-g="suplementos"]'); v = await vis();
const nSup = V.filter(x => x.g.includes('suplementos')).length;
ok(v.length === nSup && v.every(x => x.g.split(' ').includes('suplementos')), `tema Suplementos: ${nSup}`);
ok((await p.textContent('#vid-chips button[data-g="suplementos"] span')) === String(nSup), 'el contador del tema coincide');
// Búsqueda sin tildes dentro del tema y luego en todos
await p.fill('#vid-f', 'creatina'); v = await vis();
ok(v.length === 2 && v.every(x => /creatina/i.test(x.t)), 'buscar «creatina» dentro de Suplementos');
await p.click('#vid-chips button[data-g=""]'); await p.fill('#vid-f', 'azucar'); v = await vis();
ok(v.length === V.filter(x => /azúcar/i.test(x.t)).length && v.length > 0, 'buscar «azucar» encuentra «azúcar»');
await p.fill('#vid-f', 'zzzz'); v = await vis();
ok(v.length === 0 && !(await p.$eval('#vid-nada', e => e.hidden)) && (await p.getAttribute('#vid-nada a', 'href')).endsWith('query=zzzz'), 'sin resultados: aviso y búsqueda en el canal');
await p.fill('#vid-f', '');
// Orden
await p.selectOption('#vid-o', 'c'); v = await vis();
ok(v.every((x, i) => !i || v[i - 1].s <= x.s), 'más cortos primero');
await p.selectOption('#vid-o', 'a'); v = await vis();
ok(v[0].id === V[V.length - 1].id, 'más antiguos primero');
await p.selectOption('#vid-o', 'n');
// Reproducir una tarjeta arriba
const elegido = V[5];
await p.click(`#vid-rej a[data-v="${elegido.id}"]`); await p.waitForTimeout(150);
const src = await p.evaluate(() => { const f = document.querySelector('#vid-dest iframe'); return f ? f.src : ''; });
ok(src.startsWith('https://www.youtube-nocookie.com/embed/' + elegido.id) && src.includes('autoplay=1'), 'al pulsar una tarjeta, se reproduce arriba (youtube-nocookie)');
ok(await p.evaluate(() => document.querySelector('#vid-dest iframe').title) === elegido.t, 'el reproductor lleva el título del vídeo');
ok((await p.getAttribute(`#vid-rej a[data-v="${elegido.id}"]`, 'aria-current')) === 'true' && p.url().endsWith('#v-' + elegido.id), 'tarjeta marcada y dirección con #v-');
ok(await p.evaluate(() => !document.querySelector('iframe[src*="youtube"]:not(#vid-dest iframe)')), 'ningún otro reproductor cargado');
// Sin pulsar no se carga YouTube
const p2 = await ctx.newPage(); const pedidas = []; p2.on('request', r => { if (/youtube/.test(r.url())) pedidas.push(r.url()); });
await p2.goto(U + 'videos.html#v-' + V[10].id); await p2.waitForTimeout(300);
ok((await p2.getAttribute('#vid', 'data-v')) === V[10].id && (await p2.textContent('#vid .vid-chip')) === 'Elegido', '#v-<id> pone ese vídeo arriba');
ok(pedidas.length === 0, 'sin pulsar, no se pide nada a youtube.com');
await p2.click('#vid'); await p2.waitForTimeout(150);
ok(await p2.evaluate(id => !!document.querySelector(`#vid-dest iframe[src*="${id}"]`), V[10].id), 'pulsar el grande lo reproduce');
await p2.goto(U + 'videos.html?t=envejecer#todos'); await p2.waitForTimeout(300);
ok((await p2.getAttribute('#vid-chips button[data-g="envejecer"]', 'aria-pressed')) === 'true' && (await p2.$$eval('#vid-rej .vc:not([hidden])', l => l.length)) === V.filter(x => x.g.includes('envejecer')).length, '?t=envejecer filtra al cargar');
// Páginas de tema
await p2.goto(U + 'tema-envejecer.html'); await p2.waitForTimeout(200);
const tv = await p2.$$eval('.tm-vids .vc a', as => as.map(a => a.getAttribute('href')));
const env = V.filter(x => x.g.includes('envejecer'));
ok(tv.length === Math.min(4, env.length) && tv[0] === 'videos.html#v-' + env[0].id, 'tema Envejecer: sus vídeos más recientes, enlazados a la página Vídeos');
ok(await p2.$eval('#videos-tema', e => !!e.querySelector('a[href="videos.html?t=envejecer#todos"]')), 'y «Verlos todos» con el filtro');
for (const t of ['medicacion', 'dolor', 'nutricion', 'poco-tiempo']) { await p2.goto(U + `tema-${t}.html`); ok((await p2.$$eval('.tm-vids .vc', l => l.length)) > 0, `tema ${t}: con vídeos`); }
// Buscador y datos
const idx = JSON.parse(fs.readFileSync(RAIZ + '/buscar.json', 'utf8')).filter(e => e.y === 'Vídeo');
ok(idx.length === V.length && idx.every(e => e.u.startsWith('videos.html#v-')), 'los vídeos están en el buscador');
const ld = await p.$$eval('script[type="application/ld+json"]', ss => ss.map(s => JSON.parse(s.textContent)).find(j => j['@type'] === 'ItemList'));
ok(ld && ld.itemListElement.length === V.length && ld.itemListElement[0].item['@type'] === 'VideoObject' && /^PT\d+M\d+S$/.test(ld.itemListElement[0].item.duration), 'datos para buscadores: VideoObject de cada vídeo');
ok(ld && ld.itemListElement.every(x => /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d$/.test(x.item.uploadDate) && (x.item.description || '').length > 20), 'datos para buscadores: cada vídeo con fecha, hora y zona, y con descripción (avisos de Search Console del 25/11/2026)');
ok(errs.length === 0, 'sin errores de JS' + (errs.length ? ': ' + errs.join(' | ') : ''));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto');
await b.close(); s.close(); process.exit(mal ? 1 : 0);
