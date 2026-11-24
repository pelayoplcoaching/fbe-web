// Comun a todas las pruebas: raiz del sitio, Playwright y un servidor parecido a GitHub Pages (gzip y cache de 10 min).
import http from 'http'; import fs from 'fs'; import path from 'path'; import zlib from 'zlib'; import os from 'os';
import { fileURLToPath } from 'url';
export const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
export const SALIDA = path.join(os.tmpdir(), 'fbe-pruebas'); fs.mkdirSync(SALIDA, { recursive: true });
let pw;
try { pw = await import('playwright'); } catch (e) { pw = await import('/opt/npm-tools/node_modules/playwright/index.mjs'); }
// Con FBE_CLASES=<archivo>, cada pagina que abran las pruebas apunta las clases y atributos que llegan a tener sus
// elementos (tambien los que pone el guion al usarla) y el servidor los va anadiendo a ese archivo. Sirve para que los
// estilos por pagina no pierdan reglas de estados que solo aparecen al usar la web (ver fuente/estilos.mjs).
const CLASES_JS = `(() => { const S = new Set(); const pon = v => { for (const x of String(v).split(/\\s+/)) if (/^[\\w-]{1,40}$/.test(x)) S.add(x); };
  const add = el => { if (!el || el.nodeType !== 1) return; S.add(el.localName); for (const a of el.attributes) { if (a.name === 'class') pon(a.value); else if (/^(data-|aria-)|^(role|type|id|open|hidden)$/.test(a.name)) { S.add(a.name); pon(a.value); } } };
  const scan = r => { add(r); if (r.querySelectorAll) r.querySelectorAll('*').forEach(add); };
  const mo = new MutationObserver(ms => { for (const m of ms) { if (m.type === 'attributes') add(m.target); else m.addedNodes.forEach(n => { if (n.nodeType === 1) scan(n); }); } });
  const ini = () => { scan(document.documentElement); mo.observe(document.documentElement, { subtree: true, childList: true, attributes: true }); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ini); else ini();
  const manda = () => { if (!S.size) return; try { navigator.sendBeacon('/__clases', location.pathname + '\\t' + [...S].join(' ')); } catch (e) {} S.clear(); };
  setInterval(manda, 700); addEventListener('pagehide', manda); })();`;
function conClases(cr) {
  return { ...cr, launch: async o => { const b = await cr.launch(o); const nc = b.newContext.bind(b);
    b.newContext = async (...a) => { const c = await nc(...a); await c.addInitScript(CLASES_JS); return c; };
    b.newPage = async (...a) => { const c = await b.newContext(...a); const p = await c.newPage(); p.on('close', () => c.close().catch(() => {})); return p; };
    return b; } };
}
export const chromium = process.env.FBE_CLASES ? conClases(pw.chromium) : pw.chromium;
const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.webmanifest': 'application/manifest+json', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.xml': 'text/xml', '.txt': 'text/plain', '.ics': 'text/calendar', '.pdf': 'application/pdf' };
const COMP = new Set(['.html', '.css', '.js', '.json', '.svg', '.xml', '.txt', '.webmanifest']);
// servir(dir, puerto): sirve una carpeta; devuelve el servidor (se puede cerrar con .close()). Como GitHub Pages: /pagina sirve pagina.html y lo que no existe, 404.html con estado 404.
export function servir(dir, port) {
  return new Promise(r => { const s = http.createServer((q, res) => { if (q.method === 'POST' && q.url === '/__clases') { let d = ''; q.on('data', c => d += c); q.on('end', () => { if (process.env.FBE_CLASES) fs.appendFileSync(process.env.FBE_CLASES, d + '\n'); res.writeHead(204); res.end(); }); return; } let u = decodeURIComponent(q.url.split('?')[0]); if (u.endsWith('/')) u += 'index.html'; let f = path.join(dir, u); if (!fs.existsSync(f) && !path.extname(f) && fs.existsSync(f + '.html')) f += '.html'; fs.readFile(f, (e, d) => { if (e) { const n4 = path.join(dir, '404.html'); res.writeHead(404, { 'content-type': 'text/html; charset=utf-8' }); res.end(fs.existsSync(n4) ? fs.readFileSync(n4) : 'no'); return; } const ext = path.extname(f); const h = { 'content-type': T[ext] || 'application/octet-stream', 'cache-control': 'max-age=600' }; if (COMP.has(ext) && /gzip/.test(q.headers['accept-encoding'] || '')) { d = zlib.gzipSync(d); h['content-encoding'] = 'gzip'; } res.writeHead(200, h); res.end(d); }); }); s.listen(port, () => r(s)); });
}
// Paginas del sitio (sin los desvios de la web vieja)
// paginas(): todas las paginas de la raiz menos los desvios viejos, las direcciones cortas de los QR (nivel, dosdias) y el archivo de verificacion de Google Search Console (no es una pagina).
export function paginas() { return fs.readdirSync(RAIZ).filter(f => f.endsWith('.html') && !/^google[0-9a-f]+\.html$/.test(f) && !['faq.html', 'newsletter-semanal.html', 'programas-copy.html', 'quien_soy.html', 'nivel.html', 'dosdias.html'].includes(f)).map(f => f.slice(0, -5)).sort(); }
