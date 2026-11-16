import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const svg = fs.readFileSync((process.env.FBE_SAL || '..') + '/favicon.svg', 'utf8');
const lobo = svg.match(/ d="([^"]+)"/)[1];
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
await p.setContent(`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap"><body style="margin:0;width:1200px;height:630px;overflow:hidden;background:radial-gradient(900px 520px at 85% 25%,#3b2ba6 0%,transparent 62%),#140B3A;color:#fff;font-family:Archivo,Arial,sans-serif;position:relative">
<svg viewBox="0 0 600 600" style="position:absolute;right:-140px;top:-60px;width:760px;fill:none;stroke:rgba(164,156,255,.25)"><circle cx="300" cy="300" r="60"/><circle cx="300" cy="300" r="110"/><circle cx="300" cy="300" r="165"/><circle cx="300" cy="300" r="225"/><circle cx="300" cy="300" r="290"/></svg>
<svg viewBox="150 82 954 1092" style="position:absolute;right:120px;top:150px;width:300px;fill:rgba(164,156,255,.22)"><path fill-rule="evenodd" d="${lobo}"/></svg>
<div style="position:absolute;left:80px;top:80px;display:flex;align-items:center;gap:18px;font-size:30px;font-weight:700;font-stretch:118%"><span style="width:64px;height:64px;border-radius:16px;background:#593EDE;display:grid;place-items:center"><svg viewBox="150 82 954 1092" style="width:44px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></span>Fuerza Basada en Evidencia</div>
<div style="position:absolute;left:80px;bottom:150px;font-size:86px;line-height:1;font-weight:780;font-stretch:122%;letter-spacing:-1px;max-width:800px">Tu plan, tu comida, tu coach.</div>
<div style="position:absolute;left:80px;bottom:80px;font-size:30px;color:#D4D0F5">Fuerza y nutrición con un médico internista que también entrena.</div></body>`);
await p.waitForTimeout(1500); await p.screenshot({ path: (process.env.FBE_SAL || '..') + '/og.png' });
const q = await b.newPage({ viewport: { width: 180, height: 180 } }); await q.setContent(`<body style="margin:0;background:#593EDE"><svg viewBox="150 82 954 1092" style="width:124px;margin:28px;fill:#fff"><path fill-rule="evenodd" d="${lobo}"/></svg></body>`); await q.screenshot({ path: (process.env.FBE_SAL || '..') + '/icono-180.png' });
await b.close(); process.exit(0);
