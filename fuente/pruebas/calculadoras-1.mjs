import { chromium, servir, RAIZ, SALIDA, paginas } from './comun.mjs';
await servir(RAIZ, 4250);
const b = await chromium.launch(); const U = 'http://localhost:4250/'; let fallos = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) fallos++; };
async function pag(f, w = 1280) { const ctx = await b.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message)); await p.goto(U + f); await p.waitForTimeout(300); return p; }
const txt = (p, s) => p.locator(s).innerText();
const set = async (p, s, v) => { await p.fill(s, String(v)); await p.dispatchEvent(s, 'input'); };
// 1 silla
console.log('Test de la silla'); let p = await pag('test-silla.html');
await set(p, '#s-edad', 72); await set(p, '#s-reps', 9); ok((await txt(p, '#s-r-tit')).startsWith('Por debajo'), 'mujer 72, 9 veces: por debajo');
await set(p, '#s-reps', 12); ok((await txt(p, '#s-r-tit')).startsWith('Dentro') && (await txt(p, '#s-r-txt')).includes('(14 veces)'), 'mujer 72, 12: dentro y por debajo del umbral 14');
await set(p, '#s-reps', 16); ok((await txt(p, '#s-r-tit')).startsWith('Por encima'), 'mujer 72, 16: por encima');
await p.check('input[name="s-sexo"][value="h"]', { force: true }); await set(p, '#s-edad', 66); await set(p, '#s-reps', 12); ok((await txt(p, '#s-r-txt')).includes('de 12 a 18') && (await txt(p, '#s-r-txt')).includes('(16 veces)'), 'hombre 66, 12: rango 12-18, umbral 16');
await set(p, '#s-edad', 55); ok((await txt(p, '#s-r-tit')).includes('60 a 94'), 'menor de 60: aviso de rango');
await set(p, '#s-edad', 97); await set(p, '#s-reps', 8); ok((await txt(p, '#s-r-txt')).includes('90 a 94'), 'mayor de 94: usa 90-94');
await p.click('#s-empezar'); await p.waitForTimeout(3400); for (let i = 0; i < 3; i++) await p.click('#s-mas'); await p.click('#s-empezar');
ok((await p.inputValue('#s-reps')) === '3', 'cronómetro: tres toques cuentan 3 y se puede parar');
await p.click('#s-empezar'); await p.waitForTimeout(34000); ok((await txt(p, '#s-estado')).toLowerCase().includes('tiempo') && await p.isDisabled('#s-mas'), 'cronómetro completo: a los 30 s se para solo');
ok(!p.errs.length, 'sin errores JS ' + p.errs.join('|')); await p.context().close();
// 2 1RM
console.log('1RM'); p = await pag('calculadora-1rm.html');
await set(p, '#r-peso', 100); await set(p, '#r-reps', 5); await p.check('input[name="r-rir"][value="0"]', { force: true });
ok((await txt(p, '#r-r-num')) === '117,5', '100 kg x 5 al fallo: 117,5 (Epley 116,7 redondeado a 2,5)');
ok((await txt(p, '#r-r-txt')).includes('112,5'), 'Brzycki 112,5');
ok((await p.locator('#r-tabla td.tu').innerText()).startsWith('100'), 'la casilla de la serie vuelve a dar 100');
await set(p, '#r-reps', 1); ok((await txt(p, '#r-r-num')) === '100', '1 repetición al fallo: 100');
await p.check('input[name="r-red"][value="0"]', { force: true }); await set(p, '#r-reps', 10); await p.check('input[name="r-rir"][value="2"]', { force: true });
ok((await txt(p, '#r-r-num')) === '140', '100 x 10 con 2 en reserva sin redondeo: 133,3');
ok((await txt(p, '#r-r-txt')).includes('pierde precisión'), 'aviso con más de 10 hasta el fallo');
ok(!p.errs.length, 'sin errores JS ' + p.errs.join('|')); await p.context().close();
// 3 volumen
console.log('Volumen'); p = await pag('volumen-semanal.html');
await p.click('#v-ejemplo'); await p.waitForTimeout(200);
const vol = await p.evaluate(() => Object.fromEntries([...document.querySelectorAll('.vol-b')].map(e => [e.querySelector('.vol-n').textContent, e.querySelector('.vol-v').textContent])));
const esp = { 'Pecho': '9', 'Tríceps': '13,5', 'Hombros': '15', 'Espalda': '15', 'Bíceps': '13,5', 'Cuádriceps': '9', 'Glúteos': '7,5', 'Isquiotibiales': '6', 'Gemelos': '6', 'Abdomen': '6' };
ok(Object.entries(esp).every(([k, v]) => vol[k] === v), 'ejemplo: series por músculo ' + JSON.stringify(vol));
await p.reload(); await p.waitForTimeout(300); ok((await p.locator('.vol-fila').count()) === 10, 'se guarda en el navegador al recargar');
await p.click('.vol-fila .vol-quita'); ok((await p.locator('.vol-fila').count()) === 9, 'quitar una fila');
await p.click('#v-vaciar'); ok((await txt(p, '#v-resumen')).includes('Añade'), 'vaciar');
ok(!p.errs.length, 'sin errores JS ' + p.errs.join('|')); await p.context().close();
// 4 cafeina
console.log('Cafeína'); p = await pag('cafeina.html');
ok((await txt(p, '#c-r-total')) === '250', 'ejemplo: 250 mg');
const l = await txt(p, '#c-r-lista'); ok(l.includes('unos 60 mg'), 'quedan unos 60 mg a las 23:00'); ok(l.includes('16:30') && l.includes('8,8'), 'aviso del café de las 16:30 (Gardiner 8,8 h)');
ok((await txt(p, '#c-r-tit')).includes('hora'), 'título: revisa la hora');
await p.check('#c-embarazo'); ok((await txt(p, '#c-r-lista')).includes('200 mg al día') && (await txt(p, '#c-r-tit')).includes('límite'), 'embarazo: límite 200 y se pasa');
await p.uncheck('#c-embarazo'); await p.click('[data-b="otro"]'); await p.waitForTimeout(150);
const t2 = await txt(p, '#c-r-total'); ok(t2 === '450', 'añadir preentreno 200 mg: 450 ' + t2);
ok((await txt(p, '#c-r-tit')).includes('100 mg') || (await txt(p, '#c-r-tit')).includes('límite'), 'con preentreno tarde: aviso fuerte');
ok((await p.locator('#c-curva path.linea').count()) === 1, 'dibuja la curva');
ok(!p.errs.length, 'sin errores JS ' + p.errs.join('|')); await p.context().close();
// 5 revision
console.log('Revisión médica'); p = await pag('revision-medica.html');
const r = async (reg, enf, sint) => { await p.check(`input[name="q-regular"][value="${reg}"]`, { force: true }); await p.check(`input[name="q-enf"][value="${enf}"]`, { force: true }); if (sint) await p.check('input[name="q-sint"][value="disnea"]'); else await p.check('#q-ninguno'); await p.waitForTimeout(80); return txt(p, '#q-r-tit'); };
ok((await txt(p, '#q-r-tit')).includes('Responde'), 'sin responder: pide responder');
ok((await r('no', 'no', false)) === 'Puedes empezar', 'no regular, sin enfermedad ni síntomas');
ok((await r('si', 'no', false)) === 'Puedes seguir como hasta ahora', 'regular, sin enfermedad');
ok((await r('si', 'si', false)).startsWith('Sigue, pero consulta'), 'regular con enfermedad: consulta antes de vigoroso');
ok((await r('no', 'si', false)).startsWith('Mejor una valoración'), 'no regular con enfermedad: valoración antes');
ok((await r('no', 'no', true)).startsWith('Con estos síntomas'), 'no regular con síntomas');
ok(!(await p.isChecked('#q-ninguno')), 'marcar un síntoma desmarca «Ninguno»');
ok((await r('si', 'no', true)).startsWith('Para y consulta'), 'regular con síntomas: para');
ok(!p.errs.length, 'sin errores JS ' + p.errs.join('|')); await p.context().close();
console.log(fallos ? `${fallos} FALLOS` : 'todo correcto'); await b.close(); process.exit(0);
