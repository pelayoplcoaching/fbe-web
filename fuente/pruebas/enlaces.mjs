// Enlaces internos de todas las paginas: archivos que existen, anclas (#) que existen, imagenes que existen y sitemap coherente.
import { RAIZ, paginas } from './comun.mjs';
import fs from 'fs'; import path from 'path';
const rotos = []; const cache = {};
const lee = f => cache[f] ??= (fs.existsSync(path.join(RAIZ, f)) ? fs.readFileSync(path.join(RAIZ, f), 'utf8') : null);
const tieneId = (html, id) => html.includes(`id="${id}"`) || html.includes(`data-p="${id}"`) || html.includes(`name="${id}"`);
for (const pag of paginas()) {
  const html = lee(pag + '.html').replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '');
  for (const m of html.matchAll(/(?:href|src)="([^"#:?]*)(#[^"]*)?"/g)) {
    const [_, f, ancla] = m; if (/^(mailto|tel|data|javascript)/.test(f)) continue;
    const dest = f === '' ? pag + '.html' : f.replace(/^\.\//, '');
    if (dest && !fs.existsSync(path.join(RAIZ, dest))) { rotos.push(`${pag}: ${dest}`); continue; }
    if (ancla && ancla.length > 1 && dest.endsWith('.html')) { const d = lee(dest); if (d && !tieneId(d, decodeURIComponent(ancla.slice(1)))) rotos.push(`${pag}: ${dest}${ancla}`); }
  }
  for (const m of html.matchAll(/srcset="([^"]+)"/g)) for (const parte of m[1].split(',')) { const u = parte.trim().split(/\s+/)[0]; if (u && !/^https?:/.test(u) && !fs.existsSync(path.join(RAIZ, u))) rotos.push(`${pag}: srcset ${u}`); }
}
const sm = lee('sitemap.xml') || ''; const enSm = [...sm.matchAll(/<loc>[^<]*\/([^/<]*)<\/loc>/g)].map(m => m[1] || 'index.html');
for (const f of enSm) if (!fs.existsSync(path.join(RAIZ, f))) rotos.push('sitemap: ' + f);
const u = [...new Set(rotos)]; u.slice(0, 40).forEach(r => console.log('  ✘ ' + r));
console.log(`${paginas().length} páginas, ${enSm.length} en el sitemap`);
console.log(u.length ? 'FALLOS ' + u.length : 'todo correcto'); process.exit(0);
