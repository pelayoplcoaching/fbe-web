// Comun a todas las pruebas: raiz del sitio, Playwright y un servidor parecido a GitHub Pages (gzip y cache de 10 min).
import http from 'http'; import fs from 'fs'; import path from 'path'; import zlib from 'zlib'; import os from 'os';
import { fileURLToPath } from 'url';
export const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
export const SALIDA = path.join(os.tmpdir(), 'fbe-pruebas'); fs.mkdirSync(SALIDA, { recursive: true });
let pw;
try { pw = await import('playwright'); } catch (e) { pw = await import('/opt/npm-tools/node_modules/playwright/index.mjs'); }
export const chromium = pw.chromium;
const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.webmanifest': 'application/manifest+json', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.xml': 'text/xml', '.txt': 'text/plain', '.ics': 'text/calendar', '.pdf': 'application/pdf' };
const COMP = new Set(['.html', '.css', '.js', '.json', '.svg', '.xml', '.txt', '.webmanifest']);
// servir(dir, puerto): sirve una carpeta; devuelve el servidor (se puede cerrar con .close()). Como GitHub Pages: /pagina sirve pagina.html y lo que no existe, 404.html con estado 404.
export function servir(dir, port) {
  return new Promise(r => { const s = http.createServer((q, res) => { let u = decodeURIComponent(q.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html'; let f = path.join(dir, u); if (!fs.existsSync(f) && !path.extname(f) && fs.existsSync(f + '.html')) f += '.html'; fs.readFile(f, (e, d) => { if (e) { const n4 = path.join(dir, '404.html'); res.writeHead(404, { 'content-type': 'text/html; charset=utf-8' }); res.end(fs.existsSync(n4) ? fs.readFileSync(n4) : 'no'); return; } const ext = path.extname(f); const h = { 'content-type': T[ext] || 'application/octet-stream', 'cache-control': 'max-age=600' }; if (COMP.has(ext) && /gzip/.test(q.headers['accept-encoding'] || '')) { d = zlib.gzipSync(d); h['content-encoding'] = 'gzip'; } res.writeHead(200, h); res.end(d); }); }); s.listen(port, () => r(s)); });
}
// Paginas del sitio (sin los desvios de la web vieja)
export function paginas() { return fs.readdirSync(RAIZ).filter(f => f.endsWith('.html') && !['faq.html', 'newsletter-semanal.html', 'programas-copy.html', 'quien_soy.html'].includes(f)).map(f => f.slice(0, -5)).sort(); }
