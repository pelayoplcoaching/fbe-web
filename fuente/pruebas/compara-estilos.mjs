// Compara cómo se ve cada página con fbe.css entero (copia de la web en BASE) y con su CSS propio (la raíz).
// Uso: node pruebas/compara-estilos.mjs /tmp/fbe-base [pagina ...]   -> capturas en /tmp/compara y lista de diferencias
// Tres vistas por página: 1280 claro, 390 claro y 390 oscuro, sin animaciones y con todas las secciones pintadas.
import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
import { servir, RAIZ, chromium, paginas } from './comun.mjs';
const BASE = process.argv[2]; if (!BASE) { console.log('falta la carpeta base'); process.exit(1); }
const pags = process.argv.slice(3).length ? process.argv.slice(3) : paginas();
const OUT = '/tmp/compara'; fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT);
await servir(BASE, 4601); await servir(RAIZ, 4602);
const b = await chromium.launch();
const QUIETO = `*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}section.lenta,.lenta{content-visibility:visible!important}`;
const VISTAS = [['1280', 1280, 900, 'light'], ['390', 390, 844, 'light'], ['390o', 390, 844, 'dark']];
for (const p of pags) {
  for (const [n, w, h, tema] of VISTAS) {
    for (const [lado, port] of [['a', 4601], ['b', 4602]]) {
      const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce', deviceScaleFactor: 1 });
      await ctx.addInitScript(t => { try { localStorage.setItem('fbe-web-tema', t); localStorage.setItem('fbe-lectura', JSON.stringify({ q: 1 })); } catch (e) {} }, tema);
      await ctx.route(/^https?:\/\/(?!localhost)/, r => r.abort());
      const pg = await ctx.newPage();
      await pg.goto(`http://localhost:${port}/${p}.html`, { waitUntil: 'load' }).catch(() => {});
      await pg.addStyleTag({ content: QUIETO }).catch(() => {});
      await pg.evaluate(async () => { document.querySelectorAll('.sube').forEach(e => e.classList.add('ya')); await document.fonts.ready; window.scrollTo(0, 0); }).catch(() => {});
      await pg.waitForTimeout(350);
      await pg.screenshot({ path: `${OUT}/${p}-${n}-${lado}.png`, fullPage: true }).catch(e => console.log('error', p, n, e.message));
      await ctx.close();
    }
  }
}
await b.close();
// diferencias con Python (PIL): píxeles distintos de verdad (umbral 24 en algún canal)
const py = `
import sys, glob, os
from PIL import Image, ImageChops
out = sys.argv[1]; malas = []
for a in sorted(glob.glob(out + '/*-a.png')):
    bb = a[:-6] + '-b.png'
    A, B = Image.open(a).convert('RGB'), Image.open(bb).convert('RGB')
    if A.size != B.size:
        malas.append((os.path.basename(a)[:-6], 'tamano %sx%s -> %sx%s' % (A.size + B.size))); continue
    d = ImageChops.difference(A, B).convert('L').point(lambda v: 255 if v > 24 else 0)
    n = sum(1 for v in d.getdata() if v)
    if n > 40:
        box = d.getbbox(); malas.append((os.path.basename(a)[:-6], '%d px distintos en %s' % (n, box)))
        d.save(a[:-6] + '-dif.png')
print('vistas comparadas:', len(glob.glob(out + '/*-a.png')))
for m in malas: print('DIFERENTE', *m)
print('iguales' if not malas else '%d vistas con diferencias' % len(malas))
`;
console.log(execFileSync('python3', ['-c', py, OUT], { encoding: 'utf8' }));
process.exit(0);
