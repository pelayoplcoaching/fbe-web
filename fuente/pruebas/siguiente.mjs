// «¿Y ahora qué?»: aparece con el resultado y cambia según la zona (verde, ámbar, rojo)
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
const s = await servir(RAIZ, 4402); const b = await chromium.launch(); let mal = 0;
const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const p = await b.newPage({ viewport: { width: 1280, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
const estado = () => p.evaluate(() => { const s = document.getElementById('ya'); const r = [...s.querySelectorAll('.ya-rej')].find(x => !x.hidden); return { visible: !s.hidden, z: s.dataset.z, enlaces: r ? [...r.querySelectorAll('a')].map(a => a.getAttribute('href')) : [] }; });
// Prensión: sin intentos no hay resultado; con 15 kg (hombre) sale bajo; con 40 kg, por encima
await p.goto('http://localhost:4402/prension.html'); await p.waitForTimeout(300);
ok(!(await estado()).visible, 'prensión: oculto sin resultado');
await p.fill('#g-1', '15'); await p.waitForTimeout(200); let e = await estado();
ok(e.visible && e.z === 'z-bajo' && e.enlaces.includes('glosario.html#sarcopenia'), 'prensión baja: sarcopenia, ruta mayores y Puesta a punto');
await p.fill('#g-1', '40'); await p.waitForTimeout(200); e = await estado();
ok(e.visible && e.z === 'z-alto' && e.enlaces.includes('test-silla.html'), 'prensión alta: siguiente prueba');
await p.screenshot({ path: `${SALIDA}/ya-prension.png`, fullPage: false });
// Revisión médica: con una respuesta de riesgo sale la ruta de medicación
await p.goto('http://localhost:4402/calculadora-1rm.html'); await p.waitForTimeout(300); e = await estado();
ok(e.visible && e.z === 'def' && e.enlaces.includes('volumen-semanal.html'), '1RM (sin zonas): siguiente paso por defecto');
await p.goto('http://localhost:4402/calorias.html'); await p.waitForTimeout(300); e = await estado();
ok(e.visible && e.enlaces.some(u => u.includes('calculadoradeproteina')), 'calorías: proteína');
// Todas las paginas con el bloque: enlaces internos existentes
const fs = await import('fs');
for (const f of fs.readdirSync(RAIZ).filter(f => f.endsWith('.html'))) { const h = fs.readFileSync(RAIZ + '/' + f, 'utf8'); if (!h.includes('id="ya"')) continue; for (const m of h.matchAll(/class="ya-t" href="([^"#]+)/g)) if (!m[1].startsWith('http') && !fs.existsSync(RAIZ + '/' + m[1])) { ok(false, f + ' enlaza a ' + m[1]); } }
ok(errs.length === 0, 'sin errores ' + errs.join('|'));
console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); await b.close(); s.close(); process.exit(0);
