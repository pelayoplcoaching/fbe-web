import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
await servir(RAIZ, 4260);
const b = await chromium.launch(); const U = 'http://localhost:4260/'; let fallos = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) fallos++; };
async function pag(f, w = 1280) { const ctx = await b.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce', permissions: ['clipboard-read', 'clipboard-write'] }); const p = await ctx.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message)); await p.goto(U + f); await p.waitForTimeout(300); return p; }
const tx = (p, s) => p.textContent(s);
const set = async (p, s, v) => { await p.fill(s, String(v)); await p.dispatchEvent(s, 'input'); };
const radio = (p, n, v) => p.$eval(`input[name="${n}"][value="${v}"]`, e => e.click());
// pulso
console.log('Zonas de pulso'); let p = await pag('zonas-pulso.html');
ok((await tx(p, '#z-max-n')) === '177', 'edad 45: máximo Tanaka 177');
ok((await tx(p, '#z-lista')).includes('113–135'), 'moderada por % del máximo: 113–135 lpm');
ok((await tx(p, '#z-txt')).includes('175'), 'compara con 220 − edad = 175');
await set(p, '#z-rep', 60); ok((await tx(p, '#z-lista')).includes('107–129') && (await tx(p, '#z-metodo')).includes('Karvonen'), 'con reposo 60: moderada 107–129 (Karvonen)');
await set(p, '#z-max', 185); ok((await tx(p, '#z-max-n')) === '185' && (await tx(p, '#z-metodo')).includes('medido'), 'máximo medido 185');
await p.check('#z-bb'); ok((await tx(p, '#z-max-n')) === '12–13' && !(await tx(p, '#z-lista')).includes('lpm'), 'fármaco que cambia el pulso: Borg 12–13, sin lpm');
ok(!p.errs.length, 'sin errores ' + p.errs.join('|')); await p.context().close();
// dolor
console.log('Semáforo del dolor'); p = await pag('semaforo-dolor.html');
await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(300);
ok((await tx(p, '#d-tit')).startsWith('Sin dolor'), 'sin dolor: verde');
await set(p, '#d-dur', 4); await set(p, '#d-des', 3); await radio(p, 'd-man', 'igual'); ok((await tx(p, '#d-tit')) === 'Puedes seguir' && (await p.getAttribute('#d-luces', 'data-k')) === 'v', '4 y 3, mañana bien: puedes seguir');
await radio(p, 'd-man', 'peor'); ok((await p.getAttribute('#d-luces', 'data-k')) === 'a', 'mañana peor: ámbar');
await set(p, '#d-dur', 6); ok((await tx(p, '#d-tit')).includes('pasado') && (await tx(p, '#d-txt')).includes('6'), 'durante 6: rojo, te has pasado');
await p.check('input[name="d-flag"][value="pecho"]'); ok((await tx(p, '#d-tit')).includes('Para y consulta') && (await tx(p, '#d-lista')).includes('112'), 'dolor en el pecho: consulta y 112');
await p.uncheck('input[name="d-flag"][value="pecho"]'); await set(p, '#d-zona', 'Rodilla <b>'); await p.click('#d-guardar'); await p.click('#d-guardar');
ok((await p.locator('#d-entradas li').count()) === 2 && (await tx(p, '#d-entradas')).includes('Rodilla <b>'), 'diario: guarda dos entradas (y escapa el texto)');
await p.reload(); await p.waitForTimeout(300); ok(await p.isVisible('#d-diario'), 'el diario sigue al recargar');
await p.click('#d-borrar'); ok((await p.locator('#d-entradas li').count()) === 0, 'borrar el diario'); await p.click('#d-deshacer'); ok((await p.locator('#d-entradas li').count()) === 2, 'deshacer recupera el diario');
ok(!p.errs.length, 'sin errores ' + p.errs.join('|')); await p.context().close();
// sppb
console.log('Test SPPB'); p = await pag('test-sppb.html', 390);
ok((await tx(p, '#p-tit')).includes('Haz las tres'), 'sin datos: pide las pruebas');
ok(await p.isDisabled('input[name="p-semi"][value="10"]'), 'semitándem bloqueado hasta hacer pies juntos');
await radio(p, 'p-lado', '10'); await radio(p, 'p-semi', '10'); await radio(p, 'p-tan', '2'); await set(p, '#p-m1', 4.5); await radio(p, 'p-s1', 'si'); await set(p, '#p-s5', 11);
ok((await tx(p, '#p-total')) === '12' && (await tx(p, '#p-tit')) === 'Rendimiento alto' && (await tx(p, '#p-txt')).includes('Vivifrail: D'), '4+4+4 = 12, alto, Vivifrail D');
ok((await tx(p, '#p-vel')).includes('0,89'), 'velocidad 4/4,5 = 0,89 m/s');
await radio(p, 'p-tan', '0'); await set(p, '#p-m1', 5); await set(p, '#p-s5', 14);
ok((await tx(p, '#p-total')) === '7' && (await tx(p, '#p-txt')).includes('8 o menos'), '2+3+2 = 7, intermedio con aviso EWGSOP2');
await radio(p, 'p-tan', '1'); await set(p, '#p-s5', 12); ok((await tx(p, '#p-total')) === '9' && !(await tx(p, '#p-txt')).includes('8 o menos'), '3+3+3 = 9, sin aviso');
await radio(p, 'p-semi', '0'); ok(await p.isDisabled('input[name="p-tan"][value="2"]'), 'semitándem fallido bloquea el tándem');
await set(p, '#p-m1', 7); await radio(p, 'p-s1', 'no'); ok((await tx(p, '#p-total')) === '3' && (await tx(p, '#p-txt')).includes('Vivifrail: A') && await p.isDisabled('#p-s5'), '1+2+0 = 3, bajo, Vivifrail A');
await set(p, '#p-m1', 6.21); ok((await tx(p, '#p-partes')).includes('2/4'), 'marcha 6,21 s = 2 puntos');
await set(p, '#p-m2', 6.2); ok((await tx(p, '#p-partes')).includes('3/4'), 'cuenta el intento más rápido (6,20 s = 3)');
await p.click('.cronom[data-dest="p-m1"]'); await p.waitForTimeout(700); await p.click('.cronom[data-dest="p-m1"]'); const vm = parseFloat(await p.inputValue('#p-m1')); ok(vm > 0.5 && vm < 1.2, 'cronómetro escribe el tiempo (' + vm + ' s)');
await p.click('#p-reset'); ok((await tx(p, '#p-total')) === '–', 'empezar de nuevo');
ok(!p.errs.length, 'sin errores ' + p.errs.join('|')); await p.context().close();
// paron
console.log('Parón'); p = await pag('paron.html');
ok((await tx(p, '#o-items')).includes('Fuerza: apenas cambia') && (await tx(p, '#o-items')).includes('Cardio: empieza a bajar'), '3 semanas sin nada: fuerza igual, cardio baja');
await set(p, '#o-sem', 8); await radio(p, 'o-edad', 'm'); await radio(p, 'o-tipo', 'f');
ok((await tx(p, '#o-items')).includes('empieza a bajar') && (await tx(p, '#o-items')).includes('más del doble'), '8 semanas, 65+: baja, más del doble');
await radio(p, 'o-hago', '1'); ok((await tx(p, '#o-items')).includes('2-3 series'), '65+ con 1 sesión: puede quedarse corto');
await radio(p, 'o-edad', 'j'); await radio(p, 'o-tipo', 'a'); await radio(p, 'o-hago', '2'); await set(p, '#o-sem', 10);
ok((await tx(p, '#o-tit')).startsWith('Tranquilidad'), '10 semanas con 2 sesiones: se mantiene todo');
await set(p, '#o-sem', 40); ok((await tx(p, '#o-items')).includes('32 semanas no hay datos') && (await tx(p, '#o-items')).includes('15 semanas no hay datos'), '40 semanas: avisa de que no hay datos');
ok(!p.errs.length, 'sin errores ' + p.errs.join('|')); await p.context().close();
// suplementos
console.log('Suplementos'); p = await pag('suplementos.html');
ok((await tx(p, '#u-n')).startsWith('Creatina') && (await tx(p, '#u-g-l')) === 'Grupo A', 'por defecto, la creatina (grupo A)');
await set(p, '#u-q', 'omega'); ok((await tx(p, '#u-n')).includes('omega-3') && (await tx(p, '#u-g-l')) === 'Grupo B', 'buscar «omega» abre el aceite de pescado (B)');
await set(p, '#u-q', 'remolacha'); ok((await tx(p, '#u-n')).startsWith('Nitrato'), '«remolacha» encuentra el nitrato');
await set(p, '#u-q', 'ashwagandha'); ok(await p.isVisible('#u-nada') && (await tx(p, '#u-nada')).includes('no está'), 'lo que no está en el AIS lo dice');
await set(p, '#u-q', ''); await set(p, '#u-peso', 80); await p.click('.supl-it[data-id="cafeina"]'); ok((await tx(p, '#u-calc')).includes('240-480 mg') && (await tx(p, '#u-calc')).includes('EFSA'), 'cafeína para 80 kg: 240-480 mg y aviso EFSA');
await set(p, '#u-peso', 75); await p.click('.supl-it[data-id="betaalanina"]'); ok((await tx(p, '#u-calc')).includes('4,9 g'), 'beta-alanina 75 kg: 4,9 g al día');
await p.click('.supl-it[data-id="bicarbonato"]'); ok((await tx(p, '#u-calc')).includes('15-30 g'), 'bicarbonato 75 kg: 15-30 g');
await radio(p, 'u-g', 'D'); ok((await p.locator('.supl-it').count()) === 9, 'filtro D: 9 entradas');
ok(!p.errs.length, 'sin errores ' + p.errs.join('|')); await p.context().close();
// herramientas
p = await pag('herramientas.html'); ok((await p.locator('.herr-mini').count()) === 14, 'Herramientas: 14 tarjetas'); await p.context().close();
console.log(fallos ? fallos + ' FALLOS' : 'todo correcto'); await b.close(); process.exit(0);
