// La web como app (22/11/2026): pestañas, Mi panel, favoritos, Mis datos, logros, acciones del buscador, rutas con progreso,
// Aprende, Novedades y RSS, Ayuda (copia de seguridad), vídeos con capítulos y enlazados, «Esta semana», manifiesto y service worker
import { chromium, servir, RAIZ } from './comun.mjs';
import fs from 'fs';
const s = await servir(RAIZ, 4434); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const U = 'http://localhost:4434/';
async function ctx(w = 390, h = 844, pre) { const c = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce', acceptDownloads: true }); await c.route(/ytimg\.com|youtube|mlcdn|mailerlite/, r => r.abort()); await c.addInitScript(() => document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.scrollBehavior = 'auto'; })); if (pre) await c.addInitScript(pre); return c; }
async function abre(c, u) { const p = await c.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message)); await p.goto(U + u); await p.waitForTimeout(300); return p; }
const visible = (p, sel) => p.evaluate(q => { const e = document.querySelector(q); return !!e && getComputedStyle(e).display !== 'none'; }, sel);

// ---- Pestañas ----
let c = await ctx(); let p = await abre(c, 'test-silla.html');
ok(await visible(p, '#tabs') && !(await visible(p, '#fijo')), 'móvil, herramienta: pestañas a la vista y sin la barra «Pedir plaza»');
ok((await p.locator('#tabs a').count()) === 5 && (await p.getAttribute('#tabs a[aria-current="true"]', 'data-t')) === 'herr', 'cinco pestañas; marcada «Herramientas»');
ok((await p.getAttribute('#tabs .tabs-plaza', 'href')) === 'pedir-plaza.html', '«Plaza» lleva al formulario');
await p.goto(U + 'index.html'); await p.waitForTimeout(200);
ok(!(await visible(p, '#tabs')), 'portada en el navegador: sin pestañas (conserva su barra de «Pedir plaza»)');
await p.goto(U + 'mitos.html'); ok((await p.getAttribute('#tabs a[aria-current="true"]', 'data-t')) === 'aprende', 'Mitos: marcada «Aprende»');
await p.goto(U + 'mi-panel.html'); ok((await p.getAttribute('#tabs a[aria-current="true"]', 'data-t')) === 'panel', 'Mi panel: marcada «Mi panel»');
const sinB = await p.evaluate(() => { const t = document.getElementById('tabs').getBoundingClientRect(); return t.bottom <= innerHeight + 1 && t.width <= innerWidth && document.documentElement.scrollWidth <= innerWidth; });
ok(sinB, 'las pestañas caben en 390 px');
await c.close();
c = await ctx(1280, 900); p = await abre(c, 'test-silla.html'); ok(!(await visible(p, '#tabs')), 'en ordenador no hay pestañas'); await c.close();

// ---- Historial, favoritos y Mi panel ----
c = await ctx(); p = await abre(c, 'zonas-pulso.html'); await p.goto(U + 'glosario.html'); await p.waitForTimeout(200);
ok(await p.locator('.fav-b').count() === 1 && (await p.getAttribute('.fav-b', 'aria-pressed')) === 'false', 'botón «Guardar» en la cabecera');
await p.click('.fav-b'); ok((await p.getAttribute('.fav-b', 'aria-pressed')) === 'true' && (await p.textContent('.fav-b span')) === 'Guardado', 'guardar la página');
ok((await p.textContent('.aviso-t')).includes('Mi panel'), 'la primera vez avisa de dónde están');
await p.goto(U + 'mitos.html'); await p.waitForTimeout(200);
await p.evaluate(() => { document.querySelector('#artrosis details').open = true; }); await p.click('#artrosis .fav-i');
await p.goto(U + 'recetas.html'); await p.waitForTimeout(200); await p.click('.rec .fav-i >> nth=0');
await p.goto(U + 'videos.html'); await p.waitForTimeout(300); ok(await p.locator('#vid-rej .vc .fav-i').count() >= 40, 'estrella en cada vídeo');
await p.click('#vid-rej .vc .fav-i >> nth=1'); await p.waitForTimeout(200);
ok(await p.evaluate(() => !document.querySelector('#vid-dest iframe')), 'la estrella no reproduce el vídeo');
const F = await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-favoritos')));
ok(F.length === 4 && F.map(x => x.k).sort().join() === 'Mito,Página,Receta,Vídeo' && F.some(x => x.u === 'mitos.html#artrosis'), 'cuatro favoritos de cuatro tipos');
await p.goto(U + 'mi-panel.html'); await p.waitForTimeout(400);
ok(await p.locator('#pn-fav-l li').count() === 4 && !(await p.isVisible('#pn-fav-v')), 'Mi panel: los cuatro favoritos');
const sg = await p.$$eval('#pn-sigue-l a', as => as.map(a => a.getAttribute('href')));
ok(sg.join() === 'videos.html,recetas.html,mitos.html,glosario.html', 'seguir donde lo dejaste: las cuatro últimas, la más reciente primero');
ok(/Buen/.test(await p.textContent('#pn-saludo')), 'saludo según la hora');
await p.click('#pn-fav-l li button >> nth=0'); ok(await p.locator('#pn-fav-l li').count() === 3, 'quitar un favorito desde el panel');
const G = await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-logros') || '{}'));
ok(!!G.favoritos && await p.locator('#pn-log-l li.ok').count() >= 1 && (await p.textContent('#pn-log-n')).endsWith('de 10'), 'logro «Tu biblioteca» con tres favoritos');

// ---- Mis datos rellenan las calculadoras ----
await p.fill('#pn-edad', '9'); await p.click('#pn-guarda'); ok((await p.getAttribute('#pn-msg', 'class')).includes('mal'), 'Mis datos: edad fuera de rango, avisa');
await p.fill('#pn-edad', '58'); await p.check('input[name="pn-sexo"][value="m"]', { force: true }); await p.fill('#pn-peso', '64.5'); await p.fill('#pn-alt', '162'); await p.click('#pn-guarda');
ok(JSON.stringify(await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-perfil')))) === JSON.stringify({ edad: 58, peso: 64.5, altura: 162, sexo: 'm' }), 'Mis datos guardados');
await p.goto(U + 'calorias.html'); await p.waitForTimeout(300);
const cal = await p.evaluate(() => ({ e: document.querySelector('#k-edad').value, p: document.querySelector('#k-peso').value, a: document.querySelector('#k-alt').value, s: document.querySelector('input[name="k-sexo"]:checked').value, n: (document.querySelector('.perfil-n') || {}).textContent || '' }));
ok(cal.e === '58' && cal.p === '64.5' && cal.a === '162' && cal.s === 'm' && cal.n.includes('Mis datos'), 'Calorías: edad, peso, altura y sexo rellenados');
const kcal = await p.textContent('.res-grande b');
await p.evaluate(() => localStorage.removeItem('fbe-perfil')); await p.reload(); await p.waitForTimeout(300);
await p.fill('#k-edad', '58'); await p.fill('#k-peso', '64.5'); await p.fill('#k-alt', '162'); await p.check('input[name="k-sexo"][value="m"]', { force: true }); await p.waitForTimeout(100);
ok((await p.textContent('.res-grande b')) === kcal && kcal !== '–', 'el resultado con Mis datos es el mismo que escribiéndolos a mano: ' + kcal);
ok((await p.textContent('.perfil-n')).includes('Guárdalos una vez'), 'sin Mis datos, al escribir los ofrece');
await p.evaluate(() => localStorage.setItem('fbe-perfil', JSON.stringify({ edad: 67 }))); await p.goto(U + 'pasos.html'); await p.waitForTimeout(300);
ok((await p.inputValue('#p-edad')) === '67' && (await p.textContent('#p-cat')).includes('6000'), 'Pasos: usa la edad de Mis datos (franja de 60 o más)');
await p.goto(U + 'calculadora-1rm.html'); await p.waitForTimeout(200); ok(await p.locator('.perfil-n').count() === 0, '1RM: el «peso de la serie» no se toca');
await c.close();

// ---- Panel con datos: semana, resultados, chequeo y ruta ----
c = await ctx(390, 844, () => { if (localStorage.getItem('sembrado')) return; localStorage.setItem('sembrado', '1'); const l = new Date(); l.setDate(l.getDate() - ((l.getDay() + 6) % 7)); const k = l.getFullYear() + '-' + ('0' + (l.getMonth() + 1)).slice(-2) + '-' + ('0' + l.getDate()).slice(-2);
  localStorage.setItem('fbe-semana', JSON.stringify({ [k]: [{ d: 0, t: 'm', n: 90 }, { d: 1, t: 'v', n: 30 }, { d: 1, t: 'f', n: 0 }, { d: 3, t: 'f', n: 0 }] }));
  localStorage.setItem('fbe-resultados', JSON.stringify({ 'test-silla.html': { titulo: 'Test de la silla en 30 segundos', h: [{ t: Date.now() - 5e3, texto: 'Test de la silla: 16 veces', v: 16, vt: '16', u: 'veces', z: 'alto', zt: 'Dentro de lo normal' }] }, 'cintura-altura.html': { titulo: 'Cintura y altura', h: [{ t: Date.now(), texto: 'Índice 0,52', v: 0.52, vt: '0,52', u: '', z: 'medio', zt: 'Grasa abdominal aumentada' }] } })); });
p = await abre(c, 'mi-panel.html'); await p.waitForTimeout(300);
ok((await p.textContent('#pn-sem-t')).includes('150 de 150 min') && (await p.textContent('#pn-sem-t')).includes('2 de 2 días') && (await p.textContent('#pn-sem-b')) === 'Semana cumplida', 'panel: tu semana (90 + 2 × 30 = 150 y 2 días)');
const rs = await p.$$eval('#pn-res-l li', ls => ls.map(l => l.className + '|' + l.querySelector('b').textContent));
ok(rs.length === 2 && rs[0] === 'pn-z-medio|Cintura y altura' && rs[1].startsWith('pn-z-alto'), 'panel: resultados, el último primero, con su zona');
ok((await p.textContent('#pn-chq')).includes('2 de 4'), 'panel: chequeo 2 de 4');
const G2 = await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-logros') || '{}')); ok(G2.resultado && G2.semana && !G2.chequeo && !G2.racha3, 'logros: primer resultado y semana cumplida, no los que no tocan');
ok((await p.textContent('#pn-ruta-c')).includes('Elegir mi ruta'), 'panel: sin ruta empezada');
// ---- Rutas con progreso ----
await p.goto(U + 'empieza-aqui.html#mayores'); await p.waitForTimeout(400);
const ruta = '.ea-ruta[data-p="mayores"]';
const n = await p.locator(ruta + ' .ea-hecho').count(); const auto = await p.locator(ruta + ' .ea-hecho[aria-pressed="true"]').count();
ok(n >= 3 && (await p.textContent(ruta + ' .ea-prog span')) === auto + ' de ' + n + ' pasos', `ruta de mayores: ${n} pasos; ${auto} ya marcado(s) por tener resultado guardado`);
for (let i = 0; i < n; i++) if ((await p.getAttribute(`${ruta} .ea-hecho >> nth=${i}`, 'aria-pressed')) === 'false') await p.click(`${ruta} .ea-hecho >> nth=${i}`);
ok((await p.textContent(ruta + ' .ea-prog span')) === 'Ruta terminada' && (await p.evaluate(() => JSON.parse(localStorage.getItem('fbe-rutas')).mayores.ok)) === 1, 'todos los pasos marcados: ruta terminada');
ok(p.url().includes('empieza-aqui.html'), 'marcar un paso no navega');
await p.click(ruta + ' .ea-hecho >> nth=0'); ok((await p.textContent(ruta + ' .ea-prog span')) === (n - 1) + ' de ' + n + ' pasos', 'se puede desmarcar');
await p.goto(U + 'mi-panel.html'); await p.waitForTimeout(300); ok((await p.textContent('#pn-ruta-c')).includes((n - 1) + ' de ' + n + ' pasos') && (await p.textContent('#pn-ruta-c')).includes('Siguiente:'), 'panel: tu ruta con su progreso y el siguiente paso');
ok(p.errs.length === 0, 'sin errores de JS en el panel ' + p.errs.join('|'));
await c.close();

// ---- Acciones rápidas del buscador ----
c = await ctx(1280, 900); p = await abre(c, 'glosario.html');
await p.click('.busca-b'); await p.fill('#bo-q', 'oscuro'); await p.waitForTimeout(300);
ok((await p.textContent('.bd-l li >> nth=0')).includes('tema claro y oscuro') && (await p.getAttribute('.bd-l li >> nth=0', 'data-k')) === 'x', 'buscar «oscuro»: la acción sale la primera');
const antes = await p.evaluate(() => document.documentElement.dataset.theme || ''); await p.click('.bd-l li >> nth=0 >> a'); await p.waitForTimeout(400);
ok((await p.evaluate(() => document.documentElement.dataset.theme || '')) !== antes && !p.url().includes('accion') && !(await p.evaluate(() => !!document.querySelector('dialog.busca-d[open]'))), 'cambia el tema, cierra el buscador y limpia la dirección');
await p.goto(U + 'glosario.html#accion=texto-mas'); await p.waitForTimeout(300); ok(await p.evaluate(() => document.documentElement.classList.contains('letra-1')), 'acción «texto más grande»');
await p.goto(U + 'glosario.html#accion=favorito'); await p.waitForTimeout(300); ok((await p.getAttribute('.fav-b', 'aria-pressed')) === 'true', 'acción «guardar esta página»');
await p.click('.busca-b'); await p.fill('#bo-q', 'temporizador 2'); await p.waitForTimeout(300);
ok(await p.locator('.bd-l a[href="temporizador.html?s=120"]').count() === 1, 'buscar «temporizador 2»: acción de 2 minutos');
await c.close();

// ---- Aprende, Novedades, RSS y Ayuda ----
c = await ctx(); p = await abre(c, 'aprende.html');
ok(await p.locator('.ap-ruta').count() === 6 && await p.locator('.ap-t').count() >= 11 && await p.locator('.ap-tema').count() === 5, 'Aprende: seis rutas, las secciones y cinco temas');
const V = JSON.parse(fs.readFileSync(RAIZ + '/fuente/videos.json', 'utf8')).sort((a, b) => b.f.localeCompare(a.f));
const B = JSON.parse(fs.readFileSync(RAIZ + '/fuente/boletin.json', 'utf8')).sort((a, b) => b.f.localeCompare(a.f));
ok((await p.getAttribute('.ap-ult .vc a', 'href')) === 'videos.html#v-' + V[0].id && (await p.textContent('.ap-bol b')) === B[0].asunto, 'Aprende: el último vídeo y el último envío');
await p.goto(U + 'novedades.html'); await p.waitForTimeout(200);
const tot = V.length + B.length + await p.locator('.nov-i[data-k="w"]').count();
ok(await p.locator('.nov-i').count() === tot && await p.locator('.nov-i:not([hidden])').count() === 30, `Novedades: ${tot} entradas, 30 a la vista`);
const fechas = await p.$$eval('.nov-i time', ts => ts.map(t => t.getAttribute('datetime'))); ok(fechas.every((f, i) => !i || fechas[i - 1] >= f), 'de la más reciente a la más antigua');
await p.click('#nov-f button[data-k="v"]'); ok(await p.locator('.nov-i:not([hidden])').count() === 30 && (await p.textContent('#nov-n')) === '30 de ' + V.length, 'filtro Vídeos');
await p.click('#nov-mas'); ok(await p.locator('.nov-i:not([hidden])').count() === V.length && !(await p.isVisible('#nov-mas')), '«Ver más» enseña el resto');
const feed = fs.readFileSync(RAIZ + '/feed.xml', 'utf8');
ok(feed.startsWith('<?xml') && (feed.match(/<item>/g) || []).length === 40 && feed.includes('videos.html#v-' + V[0].id) && !/&(?!amp;|lt;|gt;|quot;|apos;)/.test(feed), 'feed.xml: 40 entradas, con el último vídeo y bien escapado');
ok((await p.locator('link[rel="alternate"][type="application/rss+xml"]').count()) === 1, 'canal RSS enlazado en la cabecera');
await p.goto(U + 'ayuda.html'); await p.waitForTimeout(200);
await p.evaluate(() => { localStorage.setItem('fbe-perfil', '{"edad":40}'); localStorage.setItem('otra-cosa', '1'); }); await p.reload(); await p.waitForTimeout(200);
ok(/Hay \d+ apartados? guardados?/.test(await p.textContent('#ay-n')), 'Ayuda: cuenta lo guardado');
const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#ay-baja')]); const ruta2 = await dl.path(); const copia = JSON.parse(fs.readFileSync(ruta2, 'utf8'));
ok(copia._fbe === 'copia' && copia['fbe-perfil'] === '{"edad":40}' && !('otra-cosa' in copia) && /^fbe-mis-datos-\d{4}-\d\d-\d\d\.json$/.test(dl.suggestedFilename()), 'copia de seguridad: solo lo de esta web');
await p.click('#ay-borra'); ok((await p.textContent('#ay-borra')).includes('otra vez'), 'borrar todo pide confirmar');
await p.click('#ay-borra'); ok(await p.evaluate(() => localStorage.getItem('fbe-perfil') === null && localStorage.getItem('otra-cosa') === '1'), 'borra lo de la web y nada más');
await p.setInputFiles('#ay-sube', ruta2); await p.waitForTimeout(300); ok(await p.evaluate(() => localStorage.getItem('fbe-perfil')) === '{"edad":40}', 'recuperar la copia');
await c.close();

// ---- Vídeos: ficha con capítulos, guía y «pruébalo»; vídeos en herramientas, mitos y portada ----
const X = JSON.parse(fs.readFileSync(RAIZ + '/fuente/videos-extra.json', 'utf8'));
c = await ctx(1280, 900); p = await abre(c, 'videos.html');
const x0 = X[V[0].id];
ok(await p.locator('#vid-ficha .vf-caps button').count() === x0.c.length && (await p.textContent('#vid-ficha .vf-caps button >> nth=1')).includes(x0.c[1].split(' ').slice(1).join(' ')), `ficha del último vídeo: ${x0.c.length} capítulos`);
ok((await p.getAttribute('#vid-ficha .vf-guia', 'href')) === `https://${x0.g}.fuerzabasadaenevidencia.com/` && await p.locator('#vid-ficha .vf-chip').count() === x0.r.length, 'con su guía y sus páginas relacionadas');
await p.evaluate(() => { document.querySelector('#vid-ficha .vf-caps').open = true; }); await p.click('#vid-ficha .vf-caps button >> nth=2'); await p.waitForTimeout(150);
const seg = x0.c[2].split(' ')[0].split(':').reduce((a, n) => a * 60 + +n, 0);
ok((await p.evaluate(() => document.querySelector('#vid-dest iframe').src)).includes('start=' + seg), 'pulsar un capítulo reproduce desde ese segundo (' + seg + ')');
await p.click(`#vid-rej a[data-v="${V[7].id}"]`); await p.waitForTimeout(150);
ok((await p.getAttribute('#vid-ficha', 'data-v')) === V[7].id && await p.locator('#vid-ficha .vf-caps button').count() === (X[V[7].id].c || []).length, 'al cambiar de vídeo cambia la ficha');
const sinCap = V.find(v => !(X[v.id].c || []).length && !(X[v.id].g)); await p.click(`#vid-rej a[data-v="${sinCap.id}"]`); await p.waitForTimeout(150);
ok(await p.locator('#vid-ficha .vf-caps').count() === 0, 'un vídeo sin capítulos no enseña la lista');
const mal2 = V.find(v => v.id === 'JCMV2c1fI_Y'); await p.click(`#vid-rej a[data-v="${mal2.id}"]`); await p.waitForTimeout(150);
ok(await p.locator('#vid-ficha .vf-caps button').count() === X[mal2.id].c.length - 2, 'los capítulos que pasan de la duración del vídeo no salen');
await p.goto(U + 'tension.html'); ok((await p.getAttribute('#en-video .vc a', 'href')) === 'videos.html#v-9Dy_ncFGwK8', 'Tensión en casa: «Te lo explico en vídeo» con el de la tensión');
await p.goto(U + 'zonas-pulso.html'); ok(await p.locator('#en-video .vc').count() === 2, 'Zonas de pulso: dos vídeos');
await p.goto(U + 'volumen-semanal.html'); ok(await p.locator('#en-video .vc').count() === 2 && await p.evaluate(() => { const a = document.getElementById('en-video'), b = document.querySelector('.bol-cta-s'); return !!(a.compareDocumentPosition(b) & 4); }), 'el bloque va antes de la invitación al boletín');
await p.goto(U + 'mitos.html'); ok(await p.locator('#artrosis .mito-video').count() === 1 && (await p.getAttribute('#artrosis .mito-video', 'href')) === 'videos.html#v-5_EvJpdr0LQ', 'mito de la artrosis: enlazado con el vídeo de la rodilla');
await p.goto(U + 'index.html'); await p.waitForTimeout(200);
ok((await p.getAttribute('#esta-semana .vc a', 'href')) === 'videos.html#v-' + V[0].id && (await p.textContent('#esta-semana .ap-bol b')) === B[0].asunto && (await p.getAttribute('#esta-semana .es-herr', 'href')) === 'tension.html', 'portada «Esta semana»: último vídeo, su herramienta y el último envío');
await c.close();

// ---- Manifiesto y service worker ----
const man = JSON.parse(fs.readFileSync(RAIZ + '/manifest.webmanifest', 'utf8'));
ok(man.start_url === 'mi-panel.html' && man.shortcuts.length === 4 && man.shortcuts.every(x => fs.existsSync(RAIZ + '/' + x.url)), 'manifiesto: empieza en Mi panel y los atajos existen');
ok(!man.screenshots || man.screenshots.every(x => fs.existsSync(RAIZ + '/' + x.src) && /^\d+x\d+$/.test(x.sizes)), 'capturas del aviso de instalar: ' + (man.screenshots ? man.screenshots.length : 0));
const sw = fs.readFileSync(RAIZ + '/sw.js', 'utf8'); const pre = JSON.parse(sw.match(/const PRE = (\[.*?\]);/)[1]);
ok(['mi-panel.html', 'sin-conexion.html', 'temporizador.html', 'semana-activa.html', 'tension.html'].every(u => pre.includes(u)) && pre.filter(u => u !== './').every(u => fs.existsSync(RAIZ + '/' + u)), 'service worker: guarda Mi panel, el temporizador y la página sin conexión, y todo existe');
c = await ctx(); p = await abre(c, 'herramientas.html'); await p.waitForFunction(() => navigator.serviceWorker && navigator.serviceWorker.controller, null, { timeout: 15000 }).catch(() => {});
await p.goto(U + 'temporizador.html'); await p.waitForTimeout(500); await c.setOffline(true);
await p.goto(U + 'temporizador.html').catch(() => {}); ok((await p.textContent('#t-num').catch(() => '')) === '1:30', 'sin conexión: el temporizador abre');
await p.goto(U + 'programas.html').catch(() => {}); await p.waitForTimeout(300);
ok(/no hay conexión/.test(await p.textContent('h1').catch(() => '')), 'sin conexión, una página no guardada: sale la página propia');
await c.close();
console.log(mal ? 'FALLOS ' + mal : 'todo correcto');
await b.close(); s.close(); process.exit(mal ? 1 : 0);
