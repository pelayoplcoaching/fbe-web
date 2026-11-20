// Imagen para compartir de la calculadora (netlify/og.jpg, 1200x630). Uso: node og.mjs (tras python3 hacer.py)
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs'; import path from 'path'; import url from 'url';
const aqui = path.dirname(url.fileURLToPath(import.meta.url));
const lt = fs.readFileSync(path.join(aqui, '..', 'ext', 'lobo-trazo.js'), 'utf8');
const caja = lt.match(/LOBO_CAJA = '([^']+)'/)[1], d = lt.match(/LOBO_D = '([^']+)'/)[1];
const fuente = fs.readFileSync(path.join(aqui, '..', 'ext', 'archivo.woff2')).toString('base64');
const lobo = (c) => `<svg class="${c}" viewBox="${caja}"><path fill-rule="evenodd" d="${d}"/></svg>`;
const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:A;src:url(data:font/woff2;base64,${fuente}) format("woff2");font-weight:400 800;font-stretch:75% 125%}
body{margin:0;width:1200px;height:630px;overflow:hidden;font-family:A;color:#fff;background:radial-gradient(900px 560px at 85% 30%,#3b2ba6,transparent 62%),radial-gradient(700px 420px at 0% 100%,#2a1b78,transparent 60%),#140B3A;position:relative}
.r{position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,rgba(164,156,255,.1) 0 1px,transparent 1px 44px),repeating-linear-gradient(90deg,rgba(164,156,255,.1) 0 1px,transparent 1px 44px);-webkit-mask-image:radial-gradient(75% 95% at 72% 40%,#000,transparent 78%)}
.an{position:absolute;right:-170px;top:50%;width:760px;transform:translateY(-50%);fill:none;stroke:rgba(164,156,255,.22)}
.an .p{fill:#F0C674;stroke:none}
.agua{position:absolute;right:70px;bottom:-60px;width:360px;fill:rgba(164,156,255,.12)}
.c{position:absolute;left:84px;top:86px;right:380px}
.m{display:flex;align-items:center;gap:18px;font-weight:780;font-stretch:122%;font-size:28px}
.m i{width:56px;height:56px;border-radius:16px;background:linear-gradient(140deg,#7C6AFD,#462ABF);display:grid;place-items:center}
.m i svg{width:38px;height:38px;fill:#fff}
.e{margin-top:70px;font-family:monospace;font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:#D4D0F5}.e b{color:#F0C674;font-weight:400}
h1{margin:18px 0 22px;font-size:96px;line-height:1;font-stretch:120%;font-weight:760;letter-spacing:-.02em}
p{margin:0;font-size:30px;line-height:1.35;color:#D4D0F5;max-width:640px}
.h{position:absolute;left:0;right:0;bottom:0;height:3px;background:linear-gradient(90deg,transparent,#A49CFF 30%,#F0C674 70%,transparent)}
</style></head><body><div class="r"></div>
<svg class="an" viewBox="0 0 600 600">${[60,110,165,225,290].map(r=>`<circle cx="300" cy="300" r="${r}"/>`).join('')}<circle class="p" cx="465" cy="300" r="7"/></svg>${lobo('agua')}
<div class="c"><div class="m"><i>${lobo('')}</i>Fuerza Basada en Evidencia</div>
<div class="e"><b>&gt;</b> Calculadora / Proteína</div><h1>Tu número de proteína</h1>
<p>Tu rango diario y su reparto por comidas, desde metaanálisis revisados.</p></div><div class="h"></div></body></html>`;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.setContent(html); await p.waitForTimeout(400);
await p.screenshot({ path: path.join(aqui, 'netlify', 'og.jpg'), type: 'jpeg', quality: 86 }); await b.close(); console.log('og.jpg hecho');
