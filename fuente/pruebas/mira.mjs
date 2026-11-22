// Capturas para repasar el diseño: página entera en móvil (o al ancho que se pida), troceada en columnas en una sola imagen.
// Uso: node pruebas/mira.mjs <pagina>[#ancla] ... [--oscuro] [--w=390] [--alto=1000] [--max=5] [--vacio] [--esc=0.62] [--vista=Y: solo la pantalla, bajada Y px]
// Sale en /tmp/mira/<pagina>-<claro|oscuro>.png. Siembra datos de ejemplo (no son de nadie) salvo con --vacio.
import { chromium, servir, RAIZ } from './comun.mjs';
import { execFileSync } from 'child_process';
import fs from 'fs';
const A = process.argv.slice(2); const op = k => { const a = A.find(x => x.startsWith('--' + k)); return a ? (a.includes('=') ? a.split('=')[1] : true) : null; };
const pags = A.filter(x => !x.startsWith('--')); const oscuro = !!op('oscuro'); const W = +(op('w') || 390); const ALTO = +(op('alto') || 1000); const MAX = +(op('max') || 5); const ESC = +(op('esc') || 0.62);
fs.mkdirSync('/tmp/mira', { recursive: true });
const s = await servir(RAIZ, 4455); const b = await chromium.launch(); const U = 'http://localhost:4455/';
const siembra = () => {
  const dia = n => { const d = new Date(); d.setDate(d.getDate() - n); return d; };
  const iso = d => d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  const lunes = d => { const l = new Date(d); l.setDate(l.getDate() - ((l.getDay() + 6) % 7)); return iso(l); };
  const sem = {}; for (let w = 0; w < 9; w++) { const d = dia(w * 7); const k = lunes(d); sem[k] = [{ d: 0, t: 'f', n: 1 }, { d: 1, t: 'm', n: 45 }, { d: 3, t: 'f', n: 1 }, { d: 4, t: 'v', n: w % 3 ? 30 : 10 }, { d: 5, t: 'm', n: w % 2 ? 60 : 20 }]; }
  const L = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  L('fbe-semana', sem); L('fbe-perfil', { edad: 52, sexo: 'm', peso: 68, altura: 164 });
  L('fbe-visto', [{ u: 'test-silla.html', t: 'Test de la silla', f: Date.now() - 3e6 }, { u: 'mitos.html', t: 'Mitos y evidencia', f: Date.now() - 8e6 }, { u: 'tension.html', t: 'Tensión en casa', f: Date.now() - 9e7 }, { u: 'videos.html', t: 'Vídeos', f: Date.now() - 2e8 }]);
  L('fbe-favoritos', [{ u: 'cafeina.html', t: 'Cafeína: cuánta y hasta qué hora', k: 'Herramienta', f: Date.now() - 1e6 }, { u: 'mitos.html#artrosis', t: 'Con artrosis de rodilla no se puede hacer fuerza', k: 'Mito', f: Date.now() - 5e6 }, { u: 'videos.html#v-9Dy_ncFGwK8', t: 'Tengo la tensión alta: ¿puedo levantar pesas?', k: 'Vídeo', f: Date.now() - 9e6 }]);
  L('fbe-resultados', { 'test-silla.html': { titulo: 'Test de la silla', h: [{ t: Date.now() - 6e9, texto: 'Test de la silla: 14 repeticiones', v: 14, vt: '14', u: 'repeticiones', z: 'z-medio', zt: 'En el rango normal' }, { t: Date.now() - 2e8, texto: 'Test de la silla: 17 repeticiones', v: 17, vt: '17', u: 'repeticiones', z: 'z-alto', zt: 'Por encima de lo normal' }] }, 'cintura-altura.html': { titulo: 'Cintura / altura', h: [{ t: Date.now() - 3e8, texto: 'Cintura/altura: 0,48', v: 0.48, vt: '0,48', u: '', z: 'z-alto', zt: 'Saludable' }] } });
  L('fbe-rutas', { cero: { h: [0, 1], t: Date.now() - 4e8 } }); L('fbe-vistas', ['test-silla.html', 'cafeina.html', 'tension.html']);
  const ten = []; for (let i = 0; i < 5; i++) { ten.push({ t: dia(i).setHours(8, 10), m: 'm', s: 128 - i, d: 82 - (i % 2) }); ten.push({ t: dia(i).setHours(21, 5), m: 'n', s: 124 + i, d: 79 }); } L('fbe-tension', ten);
};
for (const pg of pags) {
  const [nom, ancla] = pg.split('#');
  const c = await b.newContext({ viewport: { width: W, height: ALTO }, deviceScaleFactor: 1, reducedMotion: 'reduce', colorScheme: oscuro ? 'dark' : 'light' });
  await c.route(/ytimg\.com|youtube|mlcdn|mailerlite/, r => r.abort()); if (!op('vacio')) await c.addInitScript(siembra);
  await c.addInitScript(o => { try { localStorage.setItem('fbe-web-tema', o ? 'oscuro' : 'claro'); } catch (e) { } }, oscuro);
  const p = await c.newPage(); await p.goto(U + nom + (nom.includes('.') ? '' : '.html') + (ancla ? '#' + ancla : '')); await p.waitForTimeout(700);
  await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.sube').forEach(e => e.classList.add('ya')); document.querySelectorAll('section.lenta').forEach(e => { e.style.contentVisibility = 'visible'; }); document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; }); });
  await p.waitForTimeout(500);
  let y0 = 0; if (ancla) y0 = await p.evaluate(a => { const e = document.getElementById(a); return e ? Math.max(0, e.getBoundingClientRect().top + scrollY - 70) : 0; }, ancla);
  const png = `/tmp/mira/_${nom}.png`;
  if (op('vista') !== null) { const Y = +op('vista'); await p.evaluate(y => scrollTo(0, y), Y); await p.waitForTimeout(600); const sv = `/tmp/mira/${nom}-vista${Y}-${oscuro ? 'oscuro' : 'claro'}${W !== 390 ? '-' + W : ''}.png`; await p.screenshot({ path: sv }); console.log(sv); await c.close(); continue; }
  await p.screenshot({ path: png, fullPage: true });
  const sal = `/tmp/mira/${nom}${ancla ? '-' + ancla : ''}-${oscuro ? 'oscuro' : 'claro'}${W !== 390 ? '-' + W : ''}.png`;
  execFileSync('python3', ['-c', `
from PIL import Image
im = Image.open('${png}').convert('RGB'); W, H = im.size; y0 = ${y0}; alto = ${ALTO}; n = min(${MAX}, max(1, -(-(H - y0) // alto)))
sep = 14; hoja = Image.new('RGB', (n * W + (n - 1) * sep, alto), (120, 120, 130))
for i in range(n):
    t = im.crop((0, y0 + i * alto, W, min(H, y0 + (i + 1) * alto))); hoja.paste(t, (i * (W + sep), 0))
e = ${ESC}; hoja = hoja.resize((int(hoja.width * e), int(hoja.height * e)), Image.LANCZOS); hoja.save('${sal}', optimize=True)
print('${sal}', H, n)
`], { stdio: 'inherit' });
  await c.close();
}
await b.close(); s.close();
