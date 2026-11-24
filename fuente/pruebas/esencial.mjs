// FBE Esencial: la función de reserva (plazas, ventanas y pago de Stripe, con Stripe simulado) y los estados de la página
import { chromium, servir, RAIZ, SALIDA } from './comun.mjs';
import * as F from '../formularios/funciones/esencial.mjs';
let mal = 0; const ok = (c, m) => { console.log((c ? '  ✔ ' : '  ✘ ') + m); if (!c) mal++; };
const D = (t) => Date.parse(t);

// ---- La función, sin red: Stripe simulado ----
ok(['2026-12-14T23:59:59+01:00', '2026-12-15T00:00:00+01:00', '2027-01-02T23:59:59+01:00', '2027-01-03T00:00:00+01:00', '2027-01-10T23:59:59+01:00', '2027-01-11T00:00:00+01:00']
  .map(t => F.ventana(D(t))).join(' ') === 'pronto lista lista video video cerrado', 'ventanas: lista desde el 15/12, vídeo desde el 3/1, cierre el 10/1 a las 23:59');
const ahora = D('2026-12-20T12:00:00+01:00'), c = F.datosPago('nut', 'a', 'lista', ahora);
ok(c.get('subscription_data[billing_cycle_anchor]') === String(D('2027-01-11T09:00:00+01:00') / 1000) && c.get('subscription_data[proration_behavior]') === 'none', 'primer cobro el lunes 11/1 y sin cobro hasta entonces (proration none)');
ok(c.get('line_items[0][price]') === F.PRECIOS['nut-a'] && c.get('mode') === 'subscription', 'precio del nivel y la forma de pago elegidos');
ok(c.get('subscription_data[metadata][ventana]') === 'lista' && c.get('metadata[tanda]') === F.TANDA && c.get('subscription_data[metadata][nivel]') === 'nut', 'la suscripción y el pago llevan tanda, ventana y nivel');
ok(+c.get('expires_at') - ahora / 1000 >= 1800 && c.get('success_url').endsWith('/esencial-gracias.html') && c.get('cancel_url').endsWith('/esencial.html#precios'), 'el pago caduca a los 31 min y vuelve a gracias o a precios');
ok(/11 de enero de 2027/.test(c.get('custom_text[submit][message]')) && c.get('consent_collection[terms_of_service]') === 'required', 'Stripe avisa de la fecha del primer cobro y pide aceptar');
// El precio mensual solo se puede reservar si el 11/1 cae dentro del primer mes (lo exige Stripe)
ok(F.FECHAS.abre + 31 * 864e5 > F.FECHAS.ancla, 'el día que abren las reservas, el 11/1 está a menos de un mes');
ok(F.sinPlaza({ vivas: 20, abiertos: 0 }, 'lista') === 'lleno-lista' && F.sinPlaza({ vivas: 20, abiertos: 0 }, 'video') === 'lleno' && F.sinPlaza({ vivas: 19, abiertos: 1 }, 'video') === 'casi' && F.sinPlaza({ vivas: 19, abiertos: 0 }, 'lista') === null, 'llenas, casi (pagos a medias) o con plaza');

let llamadas = [];
function stripeFalso({ subs = [], completas = [], abiertas = [], falla = false } = {}) {
  llamadas = [];
  globalThis.fetch = async (url, op = {}) => {
    llamadas.push({ url, op }); const u = new URL(url); const r = (o, st = 200) => new Response(JSON.stringify(o), { status: st, headers: { 'Content-Type': 'application/json' } });
    if (falla) return r({ error: { message: 'Invalid API Key provided' } }, 401);
    if (u.pathname === '/v1/subscriptions/search') return r({ data: subs, has_more: false });
    if (u.pathname === '/v1/checkout/sessions' && op.method === 'GET') return r({ data: u.searchParams.get('status') === 'open' ? abiertas : completas, has_more: false });
    if (u.pathname === '/v1/checkout/sessions' && op.method === 'POST') return r({ id: 'cs_prueba', url: 'https://checkout.stripe.com/c/pay/cs_prueba', amount_total: 0, payment_status: 'unpaid' });
    if (/\/expire$/.test(u.pathname)) return r({ id: 'cs_prueba', status: 'expired' });
    return r({ error: { message: 'no simulado ' + u.pathname } }, 404);
  };
}
const M = { tanda: F.TANDA };
const sub = (id, v, status = 'active') => ({ id, status, metadata: { ...M, ventana: v } });
const llama = async (q, t, clave = 'rk_prueba') => {
  globalThis.Netlify = { env: { get: (k) => (k === 'STRIPE_KEY' ? clave : undefined) } };
  const real = Date.now; Date.now = () => D(t);
  try { return await F.default(new Request('https://fbe-formularios.netlify.app/.netlify/functions/esencial' + q)); } finally { Date.now = real; }
};
const a = (r) => r.headers.get('Location') || '';
stripeFalso();
ok(a(await llama('?n=ent&p=m', '2026-12-01T10:00:00+01:00')).endsWith('esencial.html?esencial=pronto#precios') && llamadas.length === 0, 'antes del 15/12: vuelve con «pronto» sin tocar Stripe');
ok(a(await llama('?n=ent&p=m', '2027-01-11T08:00:00+01:00')).endsWith('esencial=cerrado#precios'), 'tras el cierre: «cerrado»');
ok(a(await llama('?n=xx&p=m', '2026-12-20T10:00:00+01:00')).endsWith('esencial=error#precios'), 'nivel desconocido: «error»');
ok(a(await llama('?n=ent&p=m', '2026-12-20T10:00:00+01:00', '')).endsWith('esencial=error#precios'), 'sin la clave de Stripe en Netlify: «error»');
stripeFalso({ subs: [sub('sub_1', 'lista'), sub('sub_2', 'lista'), sub('sub_3', 'lista', 'canceled')] });
let r = await llama('?n=nut&p=a', '2026-12-20T10:00:00+01:00'); const post = llamadas.find(x => x.op.method === 'POST');
ok(r.status === 303 && a(r) === 'https://checkout.stripe.com/c/pay/cs_prueba', 'con plaza: va al pago de Stripe');
ok(post && new URLSearchParams(post.op.body).get('subscription_data[metadata][ventana]') === 'lista' && post.op.headers.Authorization === 'Bearer rk_prueba', 'el pago se abre en la ventana de la lista con la clave de Netlify');
ok(decodeURIComponent(llamadas[0].url).includes(`metadata['ventana']:'lista'`), 'cuenta solo las plazas de su ventana');
stripeFalso({ subs: Array.from({ length: 20 }, (_, i) => sub('sub_' + i, 'lista')) });
ok(a(await llama('?n=ent&p=m', '2026-12-28T10:00:00+01:00')).endsWith('esencial=lleno-lista#precios') && !llamadas.some(x => x.op.method === 'POST'), 'lista llena: «lleno-lista» y no abre pago');
stripeFalso({ subs: Array.from({ length: 20 }, (_, i) => sub('sub_' + i, 'video')) });
ok(a(await llama('?n=ent&p=m', '2027-01-05T10:00:00+01:00')).endsWith('esencial=lleno#precios'), 'vídeo lleno: «lleno»');
stripeFalso({ subs: Array.from({ length: 19 }, (_, i) => sub('sub_' + i, 'video')), abiertas: [{ id: 'cs_a', metadata: { ...M, ventana: 'video' } }, { id: 'cs_b', metadata: { ...M, ventana: 'lista' } }] });
ok(a(await llama('?n=ent&p=m', '2027-01-05T10:00:00+01:00')).endsWith('esencial=casi#precios'), '19 reservas y un pago a medias: «casi»');
// la búsqueda de Stripe aún no ve la suscripción recién creada: la cuenta por el pago terminado, sin repetirla
stripeFalso({ subs: [sub('sub_1', 'video')], completas: [{ id: 'cs_1', subscription: 'sub_1', metadata: { ...M, ventana: 'video' } }, { id: 'cs_2', subscription: 'sub_2', metadata: { ...M, ventana: 'video' } }, { id: 'cs_3', subscription: 'sub_9', metadata: { tanda: 'otra', ventana: 'video' } }] });
ok(JSON.stringify(await F.ocupadas('rk', 'video', D('2027-01-05T10:00:00+01:00'))) === '{"vivas":2,"abiertos":0}', 'suma los pagos terminados que la búsqueda aún no ve, sin contar dos veces');
stripeFalso({ falla: true });
ok(a(await llama('?n=ent&p=m', '2027-01-05T10:00:00+01:00')).endsWith('esencial=error#precios'), 'si Stripe falla: «error»');
stripeFalso({ subs: [sub('sub_1', 'lista')] });
let j = await (await llama('?comprobar=1', '2026-12-01T10:00:00+01:00')).json();
ok(j.ok && j.pago_de_prueba && j.pago_de_prueba.cobro_hoy === 0 && llamadas.some(x => /\/expire$/.test(x.url)) && j.ocupadas.lista.vivas === 1, 'comprobar antes de abrir: abre y cierra un pago de prueba y cuenta plazas');
stripeFalso({ subs: [sub('sub_1', 'lista')] }); j = await (await llama('?comprobar=1', '2026-12-20T10:00:00+01:00')).json();
ok(j.ok && !j.pago_de_prueba && !llamadas.some(x => x.op.method === 'POST'), 'comprobar con las reservas abiertas: solo cuenta, no abre pagos');
j = await (await llama('?comprobar=1', '2026-12-01T10:00:00+01:00', '')).json();
ok(!j.ok && /STRIPE_KEY/.test(j.fallo), 'comprobar sin clave: lo dice');

// ---- La página ----
const s = await servir(RAIZ, 4431); const b = await chromium.launch(); const errs = [];
async function pagina(q, { w = 1280, fecha = null } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
  if (fecha) await ctx.addInitScript(t => { const f = Date.parse(t); Date.now = () => f; }, fecha);
  await ctx.route(/umami|mlcdn|mailerlite|ytimg|youtube/, rr => rr.abort());
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); await p.goto('http://localhost:4431/esencial.html' + q); await p.waitForTimeout(400); return p;
}
const est = (p) => p.evaluate(() => {
  const s = document.getElementById('precios'), v = [...document.querySelectorAll('[data-aviso]')].filter(x => !x.hidden).map(x => x.dataset.aviso);
  const bs = [...document.querySelectorAll('.es-b')].map(x => ({ h: x.getAttribute('href') || '', t: x.textContent, dis: x.getAttribute('aria-disabled') === 'true', ver: getComputedStyle(x).display !== 'none' }));
  return { e: s.getAttribute('data-estado') || '', v: v.join(','), bs };
});
let p = await pagina('', { fecha: '2026-12-01T10:00:00+01:00' }); let e = await est(p);
ok(e.e === 'pronto' && e.v === 'pronto' && e.bs.every(x => x.dis && x.t === 'Desde el 15 de diciembre' && !x.h), 'antes del 15/12: aviso de cuándo abren y botones desactivados');
await p.locator('#precios').screenshot({ path: `${SALIDA}/esencial-pronto.png` }); await p.context().close();
p = await pagina('', { fecha: '2026-12-20T10:00:00+01:00' }); e = await est(p);
ok(e.e === '' && e.v === '' && e.bs.every(x => !x.dis && x.t === 'Reservar plaza' && /functions\/esencial\?n=(ent|nut)&p=m$/.test(x.h)), 'con las reservas abiertas: botones a la función, pago mensual');
await p.click('#es-per [data-p="a"]'); e = await est(p);
const precios = await p.$$eval('.es-v', x => x.map(y => y.textContent).join(' '));
ok(e.bs.every(x => /&p=a$/.test(x.h)) && precios === '149 € 199 €', 'al pasar a anual: enlaces con p=a y precios de 149 y 199 €');
ok(await p.$eval('.es-b', x => x.getAttribute('data-umami-event-pago')) === 'anual', 'Umami apunta la forma de pago');
await p.locator('#precios').screenshot({ path: `${SALIDA}/esencial-abierto.png` }); await p.context().close();
for (const [q, av, botones] of [['casi', 'casi', false], ['lleno', 'lleno', false], ['lleno-lista', 'lleno-lista', false], ['cerrado', 'cerrado', false], ['error', 'error', true]]) {
  p = await pagina('?esencial=' + q + '#precios', { fecha: '2026-12-20T10:00:00+01:00' }); e = await est(p);
  ok(e.e === q && e.v === av && e.bs.every(x => x.ver === botones), `?esencial=${q}: su aviso${botones ? ', y los botones siguen' : ' y sin botones'}`);
  if (q === 'casi' || q === 'error') await p.locator('#precios').screenshot({ path: `${SALIDA}/esencial-${q}.png` });
  await p.context().close();
}
p = await pagina('', { fecha: '2027-01-11T00:00:01+01:00' }); e = await est(p);
ok(e.e === 'cerrado' && e.v === 'cerrado' && e.bs.every(x => !x.ver), 'tras el cierre, sola: «plazas cerradas»'); await p.context().close();
p = await pagina('?esencial=abierto', { fecha: '2026-12-01T10:00:00+01:00' }); e = await est(p);
ok(e.e === '' && e.bs.every(x => !x.dis), '?esencial=abierto enseña los botones activos antes de abrir'); await p.context().close();
p = await pagina('', { w: 390, fecha: '2026-12-20T10:00:00+01:00' });
await p.locator('#precios').screenshot({ path: `${SALIDA}/esencial-movil.png` }); await p.context().close();
// Página de gracias
const ctx = await b.newContext({ viewport: { width: 390, height: 900 }, reducedMotion: 'reduce' }); await ctx.route(/umami/, rr => rr.abort());
p = await ctx.newPage(); p.on('pageerror', x => errs.push(x.message)); await p.goto('http://localhost:4431/esencial-gracias.html'); await p.waitForTimeout(400);
const g = await p.evaluate(() => ({ h1: document.querySelector('h1').textContent, portal: !!document.querySelector('a[href^="https://billing.stripe.com/p/login/"]'), robots: document.querySelector('meta[name=robots]')?.content, pasos: document.querySelectorAll('.pasitos li').length, tabs: document.body.classList.contains('con-tabs') }));
ok(g.h1 === 'Plaza reservada.' && g.portal && g.robots === 'noindex' && g.pasos === 4 && !g.tabs, 'gracias: título, enlace a la suscripción, noindex, cuatro pasos y sin pestañas de abajo');
await p.evaluate(() => document.querySelectorAll('.sube').forEach(x => x.classList.add('ya'))); await p.screenshot({ path: `${SALIDA}/esencial-gracias.png`, fullPage: true });
ok(errs.length === 0, 'sin errores de guion ' + errs.join(' | '));
await b.close(); s.close(); console.log(mal ? 'FALLOS ' + mal : 'todo correcto'); process.exit(0);
