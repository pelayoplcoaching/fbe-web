// Capturas para el aviso de instalar (manifest.webmanifest > screenshots). Uso: node app-capturas/hacer.mjs (tras generar la web).
// La semana que se ve en la tercera es un ejemplo sembrado para la captura, no datos de nadie.
import { chromium, servir, RAIZ } from '../pruebas/comun.mjs';
import { execFileSync } from 'child_process';
const s = await servir(RAIZ, 4441); const b = await chromium.launch(); const U = 'http://localhost:4441/';
async function cap(n, u, { w = 390, h = 693, esc = 1080 / 390, sel, y = 0, pre } = {}) {
  const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: esc, reducedMotion: 'reduce', colorScheme: 'light' });
  await c.route(/ytimg\.com|youtube|mlcdn|mailerlite/, r => r.abort()); if (pre) await c.addInitScript(pre);
  const p = await c.newPage(); await p.goto(U + u); await p.waitForTimeout(500);
  await p.evaluate(([sel, y]) => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.sube').forEach(e => e.classList.add('ya')); if (sel) { const e = document.querySelector(sel); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); } else scrollTo(0, y); }, [sel, y]);
  await p.waitForTimeout(500); const png = `/tmp/cap-${n}.png`; await p.screenshot({ path: png });
  execFileSync('python3', ['-c', `from PIL import Image; Image.open('${png}').convert('RGB').save('${RAIZ}/fuente/app-capturas/${n}.jpg', 'JPEG', quality=84, optimize=True)`]); await c.close();
}
const semana = () => { const l = new Date(); l.setDate(l.getDate() - ((l.getDay() + 6) % 7)); const k = l.getFullYear() + '-' + ('0' + (l.getMonth() + 1)).slice(-2) + '-' + ('0' + l.getDate()).slice(-2); localStorage.setItem('fbe-logros', JSON.stringify({ semana: Date.now(), resultado: Date.now() })); localStorage.setItem('fbe-semana', JSON.stringify({ [k]: [{ d: 0, t: 'm', n: 40 }, { d: 1, t: 'f', n: 0 }, { d: 2, t: 'v', n: 30 }, { d: 3, t: 'f', n: 0 }, { d: 5, t: 'm', n: 60 }] })); };
await cap('1-herramientas', 'herramientas.html', { sel: '#hb-f' });
await cap('2-temporizador', 'temporizador.html', { sel: '.tool-res' });
await cap('3-semana', 'semana-activa.html', { sel: '.tool-res', pre: semana });
await cap('4-aprende', 'aprende.html', { y: 330 });
await cap('5-ordenador', 'herramientas.html', { w: 1280, h: 720, esc: 1.5, sel: '#hb-f' });
await b.close(); s.close();
