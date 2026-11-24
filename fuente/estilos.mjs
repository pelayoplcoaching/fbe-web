// Estilos por página (24/11/2026). Lo ejecuta generar.sh justo después de generar la web.
// fbe.css lleva los estilos de TODA la web (unos 110 KB comprimidos) y cada página usaba menos de un tercio.
// Aquí, para cada página, se queda solo con las reglas que esa página puede necesitar y lo escribe en css/p-<huella>.css
// (páginas con los mismos estilos comparten archivo). Se conserva una regla si sus clases, ids, etiquetas y atributos
// aparecen en:
//   - el HTML de la página (con sus guiones en línea),
//   - fbe.js (lo común: buscador, Aa, menú, avisos, pestañas...) y buscar.json (el buscador pinta sus resultados),
//   - css-dinamicas.json: por página, clases y atributos que llegan a tener los elementos al USAR la web (resultados,
//     estados, avisos...). Se recogen pasando las pruebas con FBE_CLASES=<archivo> (ver pruebas/comun.mjs) y
//     node estilos.mjs --dinamicas <archivo>. Las de una página solo cuentan para esa página,
//   - y SEGURAS: prefijos de clases que los guiones construyen por partes ('z-' + zona, 'g' + grupo...).
// fbe.css se queda tal cual (por si algo lo pide). sw.js guarda también el CSS de cada página que se usa sin conexión.
// Si purgecss no está instalado, no hace nada y la web sigue con fbe.css.
import fs from 'fs'; import path from 'path'; import crypto from 'crypto'; import { createRequire } from 'module';
const AQUI = path.dirname(new URL(import.meta.url).pathname); const RAIZ = path.resolve(AQUI, '..');
const DIN = path.join(AQUI, 'css-dinamicas.json');
const SEGURAS = [/^z-/, /^zb-/, /^zl-/, /^pn-z-/, /^k-/, /^k[a-z]$/, /^pl-/, /^pi-/, /^bo-/, /^g[A-Z]$/, /^d\d+$/, /^t[a-z]$/];
const NO_PAGINA = new Set(['faq.html', 'newsletter-semanal.html', 'programas-copy.html', 'quien_soy.html', 'nivel.html', 'dosdias.html']);

function cargaPurge() {
  for (const d of [AQUI, '/tmp/purge']) { try { return createRequire(path.join(d, 'x.js'))('purgecss'); } catch (e) {} }
  return null;
}

// --dinamicas <archivo>: guarda en css-dinamicas.json, por página, las fichas recogidas por las pruebas que salen en fbe.css
// y que no están ya en el HTML de esa página (las demás ya cuentan).
if (process.argv[2] === '--dinamicas') {
  const css = fs.readFileSync(path.join(RAIZ, 'fbe.css'), 'utf8');
  const enCss = new Set(css.replace(/\{[^{}]*\}/g, ' ').match(/[A-Za-z_][\w-]*/g));
  const prev = fs.existsSync(DIN) ? JSON.parse(fs.readFileSync(DIN, 'utf8')) : {};
  const por = {};
  for (const l of fs.readFileSync(process.argv[3], 'utf8').split('\n')) {
    const i = l.indexOf('\t'); if (i < 0) continue;
    let pg = l.slice(0, i).replace(/^\//, '') || 'index.html'; if (!pg.endsWith('.html')) pg += '.html';
    (por[pg] = por[pg] || new Set(prev[pg] || []));
    for (const x of l.slice(i + 1).split(' ')) if (x && enCss.has(x)) por[pg].add(x);
  }
  const out = { ...prev };
  for (const [pg, set] of Object.entries(por)) {
    const f = path.join(RAIZ, pg); if (!fs.existsSync(f)) continue;
    const html = fs.readFileSync(f, 'utf8'); const est = new Set(html.match(/[A-Za-z_][\w-]*/g));
    out[pg] = [...set].filter(x => !est.has(x)).sort();
  }
  fs.writeFileSync(DIN, JSON.stringify(out, null, 0).replace(/\],/g, '],\n'));
  console.log('css-dinamicas.json:', Object.keys(out).length, 'páginas,', Object.values(out).reduce((a, v) => a + v.length, 0), 'fichas');
  process.exit(0);
}

const P = cargaPurge();
if (!P) { console.log('estilos por página: purgecss no está instalado, se queda fbe.css'); process.exit(0); }
const { PurgeCSS } = P;
const css = fs.readFileSync(path.join(RAIZ, 'fbe.css'), 'utf8');
const comun = [fs.readFileSync(path.join(RAIZ, 'fbe.js'), 'utf8'), fs.readFileSync(path.join(RAIZ, 'buscar.json'), 'utf8')].join('\n');
// Selectores de atributo ([data-theme="dark"], [aria-pressed="true"]...): sus valores los ponen los guiones al usar la página, así que se conservan todos.
const ATRIB = [...new Set([...css.matchAll(/\[([a-z][a-z-]*)\s*[\]=~^$*|]/g)].map(m => m[1]))];
const DINP = fs.existsSync(DIN) ? JSON.parse(fs.readFileSync(DIN, 'utf8')) : {};
const dir = path.join(RAIZ, 'css'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
const RE = /href="fbe\.css(\?v=[0-9a-f]+)?"/;
const pags = fs.readdirSync(RAIZ).filter(f => f.endsWith('.html') && !NO_PAGINA.has(f) && !/^google/.test(f) && !fs.readFileSync(path.join(RAIZ, f), 'utf8').includes('http-equiv="refresh"'));
const deCada = {}; let antes = 0, despues = 0, n = 0;
for (const f of pags) {
  const ruta = path.join(RAIZ, f); const html = fs.readFileSync(ruta, 'utf8');
  if (!RE.test(html)) continue;
  const r = await new PurgeCSS().purge({
    content: [{ raw: html, extension: 'html' }, { raw: comun, extension: 'js' }, { raw: (DINP[f] || []).join(' '), extension: 'js' }], css: [{ raw: css }],
    safelist: { standard: SEGURAS, deep: [], greedy: [] }, dynamicAttributes: ATRIB, keyframes: false, fontFace: false, variables: false, rejected: false,
  });
  const out = r[0].css;
  const h = crypto.createHash('sha1').update(out).digest('hex').slice(0, 10);
  const nom = `css/p-${h}.css`;
  if (!fs.existsSync(path.join(RAIZ, nom))) fs.writeFileSync(path.join(RAIZ, nom), out);
  fs.writeFileSync(ruta, html.replace(RE, `href="${nom}"`));
  deCada[f] = nom; antes += css.length; despues += out.length; n++;
}
// sw.js: el CSS de cada página que se guarda para usarse sin conexión, y versión nueva de la caché
const sw = path.join(RAIZ, 'sw.js');
if (fs.existsSync(sw)) {
  let t = fs.readFileSync(sw, 'utf8');
  const m = t.match(/const PRE = (\[.*?\]);/s);
  if (m) {
    const pre = JSON.parse(m[1]).filter(u => !/^fbe\.css/.test(u));
    const cssPre = [...new Set(pre.map(u => deCada[u === './' ? 'index.html' : u]).filter(Boolean))];
    const nuevo = [...pre, ...cssPre];
    const ver = crypto.createHash('sha1').update(nuevo.map(u => { const p = path.join(RAIZ, u === './' ? 'index.html' : u.split('?')[0]); return fs.existsSync(p) ? fs.readFileSync(p) : u; }).join('|')).digest('hex').slice(0, 10);
    t = t.replace(m[0], `const PRE = ${JSON.stringify(nuevo)};`).replace(/const V = '[^']*';/, `const V = 'fbe-${ver}';`);
    fs.writeFileSync(sw, t);
  }
}
const nArch = fs.readdirSync(dir).length;
console.log(`estilos por página: ${n} páginas, ${nArch} archivos, media ${Math.round(despues / n / 1024)} KB por página (antes ${Math.round(antes / n / 1024)} KB)`);
