import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const svg = fs.readFileSync((process.env.FBE_SAL || '..') + '/favicon.svg', 'utf8');
const lobo = svg.match(/ d="([^"]+)"/)[1];
const fi = 'web-img/web-compartir.webp'; const fondo = fs.existsSync(fi) ? 'data:image/webp;base64,' + fs.readFileSync(fi).toString('base64') : '';
const ff = process.env.FBE_FUENTE; const letra = ff && fs.existsSync(ff) ? `<style>@font-face{font-family:Archivo;src:url(data:font/woff2;base64,${fs.readFileSync(ff).toString('base64')});font-weight:100 900;font-stretch:62% 125%}</style>` : '';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.setContent(`${letra}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap"><body style="margin:0;width:1200px;height:630px;overflow:hidden;background:radial-gradient(900px 520px at 85% 25%,#3b2ba6 0%,transparent 62%),#140B3A;color:#fff;font-family:Archivo,Arial,sans-serif;position:relative">
${fondo ? `<img src="${fondo}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:right center">` : `<svg viewBox="0 0 600 600" style="position:absolute;right:-140px;top:-60px;width:760px;fill:none;stroke:rgba(164,156,255,.25)"><circle cx="300" cy="300" r="60"/><circle cx="300" cy="300" r="110"/><circle cx="300" cy="300" r="165"/><circle cx="300" cy="300" r="225"/><circle cx="300" cy="300" r="290"/></svg>
<svg viewBox="150 82 954 1092" style="position:absolute;right:120px;top:150px;width:300px;fill:rgba(164,156,255,.22)"><path fill-rule="evenodd" d="${lobo}"/></svg>`}
<div style="position:absolute;left:80px;top:80px;display:flex;align-items:center;gap:18px;font-size:30px;font-weight:700;font-stretch:118%"><span style="width:64px;height:64px;border-radius:16px;background:#593EDE;display:grid;place-items:center"><svg viewBox="150 82 954 1092" style="width:44px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></span>Fuerza Basada en Evidencia</div>
<div style="position:absolute;left:80px;bottom:${fondo ? 178 : 150}px;font-size:${fondo ? 80 : 86}px;line-height:1;font-weight:780;font-stretch:122%;letter-spacing:-1px;max-width:${fondo ? 640 : 800}px">Tu plan, tu comida, tu coach.</div>
<div style="position:absolute;left:80px;bottom:80px;font-size:30px;color:#D4D0F5;max-width:${fondo ? 640 : 1040}px">Fuerza y nutrición con un médico internista que también entrena.</div></body>`);
await p.waitForTimeout(1500); await p.screenshot({ path: (process.env.FBE_SAL || '..') + '/og.png' });
const q = await b.newPage({ viewport: { width: 180, height: 180 } }); await q.setContent(`<body style="margin:0;background:#593EDE"><svg viewBox="150 82 954 1092" style="width:124px;margin:28px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></body>`); await q.screenshot({ path: (process.env.FBE_SAL || '..') + '/icono-180.png' });
for (const n of [192, 512]) { const w = Math.round(n * 0.56), h = Math.round(w * 1092 / 954); const r = await b.newPage({ viewport: { width: n, height: n } }); await r.setContent(`<body style="margin:0;background:#593EDE;width:${n}px;height:${n}px;display:grid;place-items:center"><svg viewBox="150 82 954 1092" style="width:${w}px;height:${h}px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></body>`); await r.screenshot({ path: (process.env.FBE_SAL || '..') + `/icono-${n}.png` }); }
// Imagen para compartir de cada página (og/<pagina>.jpg), con su título; la lista la escribe extras2.py
const SAL = process.env.FBE_SAL || '..', LF = SAL + '/og/lista.json';
if (fs.existsSync(LF)) {
  const L = JSON.parse(fs.readFileSync(LF, 'utf8')), esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const pg = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const it of L) {
    const st = it.f.replace(/^og\//, '').replace(/\.jpg$/, ''), wi = `web-img/web-${st}.webp`;
    const im = fs.existsSync(wi) ? 'data:image/webp;base64,' + fs.readFileSync(wi).toString('base64') : fondo;
    await pg.setContent(`${letra}<body style="margin:0;width:1200px;height:630px;overflow:hidden;background:radial-gradient(900px 520px at 85% 25%,#3b2ba6 0%,transparent 62%),#140B3A;color:#fff;font-family:Archivo,Arial,sans-serif;position:relative">
${im ? `<img src="${im}" style="position:absolute;right:0;top:0;height:100%;width:60%;object-fit:cover;object-position:center;-webkit-mask-image:linear-gradient(90deg,transparent,#000 40%);mask-image:linear-gradient(90deg,transparent,#000 40%)">` : ''}
<div style="position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:16px;font-size:26px;font-weight:700;font-stretch:118%"><span style="width:56px;height:56px;border-radius:14px;background:#593EDE;display:grid;place-items:center"><svg viewBox="150 82 954 1092" style="width:38px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></span>Fuerza Basada en Evidencia</div>
<div style="position:absolute;left:80px;top:170px;bottom:64px;width:660px;display:flex;flex-direction:column;justify-content:center;gap:22px">
${it.e ? `<div style="font:700 20px/1 ui-monospace,Menlo,monospace;letter-spacing:3px;text-transform:uppercase;color:#F0C674">${esc(it.e)}</div>` : ''}
<div style="font-size:${it.t.length > 34 ? 60 : 72}px;line-height:1.03;font-weight:780;font-stretch:118%;letter-spacing:-1px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden">${esc(it.t)}</div>
${it.s ? `<div style="font-size:25px;line-height:1.38;color:#D4D0F5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden">${esc(it.s)}</div>` : ''}
</div></body>`);
    await pg.waitForTimeout(120); await pg.screenshot({ path: SAL + '/' + it.f, type: 'jpeg', quality: 82 });
  }
}
await b.close(); process.exit(0);
