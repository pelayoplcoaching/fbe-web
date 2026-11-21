// «Compartir resultado»: imagen hecha en el navegador con la cifra y la zona, sin datos de la persona; o solo la herramienta
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
import fs from 'fs';
const s = await servir(RAIZ, 4405); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce', acceptDownloads: true }); await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
await ctx.addInitScript(() => document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.scrollBehavior = 'auto'; }));
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(p.url() + ' ' + e.message));
const U = 'http://localhost:4405/';
let antes = ''; const img = async () => { const r = await p.waitForFunction((a) => { const i = document.querySelector('.comp-img'); return i && i.complete && i.naturalWidth === 1080 && i.dataset.u && i.src === i.dataset.u && i.dataset.u !== a; }, antes, { timeout: 5000 }).then(() => true, () => false); antes = await p.evaluate(() => (document.querySelector('.comp-img') || {}).src || ''); return r; };
const guarda = async (n) => { const b64 = await p.evaluate(async () => { const r = await fetch(document.querySelector('.comp-img').src); const bl = await r.blob(); return await new Promise(res => { const f = new FileReader(); f.onload = () => res(f.result.split(',')[1]); f.readAsDataURL(bl); }); }); fs.writeFileSync(`${SALIDA}/${n}.png`, Buffer.from(b64, 'base64')); };
// 1. Prensión: sin resultado no hay botón; con resultado, sí
await p.goto(U + 'prension.html'); await p.waitForTimeout(300);
ok(!(await p.isVisible('.comp-r')), 'sin resultado no hay «Compartir resultado»');
await p.fill('#g-1', '30'); await p.waitForTimeout(200);
ok(await p.isVisible('.comp-r'), 'con resultado aparece el botón');
await p.click('.comp-r'); ok(await p.isVisible('dialog.comp-d[open]'), 'se abre el cuadro de compartir');
ok(await img(), 'la imagen se dibuja (1080 × 1350)');
let alt = await p.getAttribute('.comp-img', 'alt');
ok(await p.isChecked('input[name="comp-q"][value="res"]') && alt.includes('30 kg') && alt.includes('Fuerza de prensión'), 'por defecto, con el resultado: ' + alt);
await guarda('compartir-prension-resultado');
// Descargar con el resultado
let [dw] = await Promise.all([p.waitForEvent('download'), p.click('.comp-dl')]);
ok(dw.suggestedFilename() === 'fbe-prension-resultado.png', 'descarga: ' + dw.suggestedFilename());
// Solo la herramienta
await p.check('input[name="comp-q"][value="herr"]'); await p.waitForTimeout(100); ok(await img(), 'solo la herramienta: imagen nueva');
alt = await p.getAttribute('.comp-img', 'alt'); ok(!alt.includes('30 kg') && alt.includes('dinamómetro'), 'solo la herramienta: sin la cifra, con la descripción');
await guarda('compartir-prension-herramienta');
[dw] = await Promise.all([p.waitForEvent('download'), p.click('.comp-dl')]); ok(dw.suggestedFilename() === 'fbe-prension.png', 'descarga sin resultado: ' + dw.suggestedFilename());
await p.click('.comp-ln'); await p.waitForTimeout(150);
ok((await p.evaluate(() => navigator.clipboard.readText())) === U + 'prension.html' && (await p.textContent('.comp-av')) === 'Enlace copiado', 'copiar enlace: la dirección de la herramienta');
await p.keyboard.press('Escape'); await p.waitForTimeout(100);
ok(!(await p.isVisible('dialog.comp-d[open]')) && await p.evaluate(() => document.activeElement.classList.contains('comp-r')), 'Escape cierra y el foco vuelve al botón');
// 2. Silla: la edad no sale en la imagen
await p.goto(U + 'test-silla.html'); await p.waitForTimeout(250); await p.fill('#s-edad', '72'); await p.fill('#s-reps', '12'); await p.waitForTimeout(200);
await p.click('.comp-r'); await img(); alt = await p.getAttribute('.comp-img', 'alt');
ok(alt.includes('12 veces en 30 s') && !alt.includes('72') && !/mujer|hombre/i.test(alt), 'silla: cifra y zona, sin edad ni sexo (' + alt + ')');
await guarda('compartir-silla');
// 3. 1RM con ejercicio
await p.goto(U + 'calculadora-1rm.html'); await p.waitForTimeout(250); await p.fill('#r-ej', 'Press de banca'); await p.waitForTimeout(150);
await p.click('.comp-r'); await img(); alt = await p.getAttribute('.comp-img', 'alt'); ok(alt.includes('Press de banca') && alt.includes('80 kg'), '1RM: con el ejercicio (' + alt + ')');
await guarda('compartir-1rm');
// 4. Calorías: cifra larga (rango) cabe
await p.goto(U + 'calorias.html'); await p.waitForTimeout(250); await p.fill('#k-edad', '40'); await p.fill('#k-peso', '80'); await p.fill('#k-alt', '180'); await p.waitForTimeout(150);
await p.click('.comp-r'); ok(await img(), 'calorías: imagen con un rango'); await guarda('compartir-calorias');
// 5. Accesibilidad básica del cuadro y móvil
const m = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, reducedMotion: 'reduce' }); const q = await m.newPage(); q.on('pageerror', e => errs.push(e.message));
await q.goto(U + 'cintura-altura.html'); await q.waitForTimeout(300); await q.evaluate(() => document.querySelector('.comp-r').scrollIntoView({ block: 'center', behavior: 'instant' })); await q.click('.comp-r'); await q.waitForTimeout(600);
const dlg = await q.evaluate(() => { const d = document.querySelector('dialog.comp-d'); const r = d.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: innerWidth, h: innerHeight, lab: d.getAttribute('aria-labelledby') }; });
ok(dlg.l >= 0 && dlg.r <= dlg.w && dlg.t >= 0 && dlg.b <= dlg.h && dlg.lab === 'comp-h', 'móvil: el cuadro cabe en la pantalla');
await q.screenshot({ path: `${SALIDA}/compartir-movil.png` });
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
