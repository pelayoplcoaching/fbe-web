// Reserva de plaza de FBE Esencial (24/11/2026). La llaman los botones «Reservar plaza» de esencial.html:
//   https://fbe-formularios.netlify.app/.netlify/functions/esencial?n=ent|nut&p=m|a
// Cuenta las plazas de la ventana (lista de espera o vídeo) y, si queda sitio, abre el pago de Stripe.
//
// Opción B (decidida por Pelayo el 24/11/2026): al reservar se deja la tarjeta y no se cobra nada; el primer cobro es el
// lunes 11 de enero de 2027 y desde ahí se renueva solo (billing_cycle_anchor con proration_behavior none: Stripe no hace
// factura hasta ese día). El precio de fundador se mantiene al renovar. Ojo: Stripe solo acepta la fecha del primer cobro
// si cae dentro del primer periodo, así que las cuotas mensuales no se pueden reservar antes del 11 de diciembre.
//
// Necesita la variable de entorno STRIPE_KEY: una clave restringida de Stripe con «Checkout Sessions: escritura» y
// «Subscriptions: lectura». La pone Pelayo en Netlify; no va nunca en el código.
// Comprobación: ?comprobar=1 devuelve en JSON la ventana y las plazas ocupadas; antes de abrir las reservas, además abre
// un pago de prueba (anual) y lo cierra en el acto, para ver que la clave sirve.
// Las cuatro tarifas (precio de fundador) y el portal para darse de baja se crearon en Stripe el 24/11/2026.

const WEB = 'https://fuerzabasadaenevidencia.com/';
export const PRECIOS = {
  'ent-m': 'price_1UfNOsAf1PxT1FDlAoMslvo8',  // Entrenamiento, 14,99 € al mes
  'ent-a': 'price_1UfNOuAf1PxT1FDl5vZOLQrw',  // Entrenamiento, 149 € al año
  'nut-m': 'price_1UfNOwAf1PxT1FDlGq25pHX5',  // Entrenamiento y nutrición, 19,99 € al mes
  'nut-a': 'price_1UfNOxAf1PxT1FDleKe1AY3C',  // Entrenamiento y nutrición, 199 € al año
};
const NOMBRES = { ent: 'Entrenamiento', nut: 'Entrenamiento y nutrición' };
export const FECHAS = {
  abre: Date.parse('2026-12-15T00:00:00+01:00'),    // reservas de la lista de espera (invitaciones del martes 15/12)
  video: Date.parse('2027-01-03T00:00:00+01:00'),   // desde el vídeo del domingo 3 de enero, las plazas del vídeo
  cierra: Date.parse('2027-01-11T00:00:00+01:00'),  // último momento: domingo 10 de enero a las 23:59
  ancla: Date.parse('2027-01-11T09:00:00+01:00'),   // primer cobro: lunes 11 de enero (a las 9, para que sea día 11 en toda la UE)
};
export const PLAZAS = { lista: 20, video: 20 };
export const TANDA = 'fundador-2027-01';
const MUERTAS = ['canceled', 'incomplete_expired'];

export function ventana(ahora) {
  if (ahora < FECHAS.abre) return 'pronto';
  if (ahora >= FECHAS.cierra) return 'cerrado';
  return ahora < FECHAS.video ? 'lista' : 'video';
}

async function stripe(clave, metodo, ruta, cuerpo) {
  const r = await fetch('https://api.stripe.com' + ruta, {
    method: metodo,
    headers: { Authorization: `Bearer ${clave}`, ...(cuerpo ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}) },
    body: cuerpo ? cuerpo.toString() : undefined,
  });
  const datos = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Stripe ${r.status} en ${ruta.split('?')[0]}: ${(datos.error && datos.error.message) || ''}`);
  return datos;
}

// Plazas de una ventana: suscripciones vivas de la tanda («vivas») y pagos abiertos sin terminar («abiertos», caducan a
// los 31 minutos). La búsqueda de Stripe tarda hasta un minuto en ver una suscripción nueva: por eso se suman también las
// de los pagos terminados en las dos últimas horas, sin contar dos veces la misma.
export async function ocupadas(clave, v, ahora) {
  const vivas = new Set(), muertas = new Set();
  let pagina = null;
  do {
    const q = new URLSearchParams({ query: `metadata['tanda']:'${TANDA}' AND metadata['ventana']:'${v}'`, limit: '100' });
    if (pagina) q.set('page', pagina);
    const r = await stripe(clave, 'GET', '/v1/subscriptions/search?' + q);
    for (const s of r.data || []) (MUERTAS.includes(s.status) ? muertas : vivas).add(s.id);
    pagina = r.has_more ? r.next_page : null;
  } while (pagina);
  let abiertos = 0;
  for (const estado of ['complete', 'open']) {
    const q = new URLSearchParams({ status: estado, 'created[gte]': String(Math.floor(ahora / 1000) - 7200), limit: '100' });
    const r = await stripe(clave, 'GET', '/v1/checkout/sessions?' + q);
    for (const x of r.data || []) {
      if (!x.metadata || x.metadata.tanda !== TANDA || x.metadata.ventana !== v) continue;
      if (estado === 'open') abiertos++;
      else if (x.subscription && !muertas.has(x.subscription)) vivas.add(x.subscription);
    }
  }
  return { vivas: vivas.size, abiertos };
}

// Con plaza: null. Sin plaza: el aviso que enseña la página. «lleno-lista»: llena la lista de espera (el 3/1 se abren las
// del vídeo); «lleno»: llenas las del vídeo; «casi»: solo faltan pagos a medias, que pueden dejar la plaza libre.
export function sinPlaza(o, v) {
  if (o.vivas >= PLAZAS[v]) return v === 'lista' ? 'lleno-lista' : 'lleno';
  return o.vivas + o.abiertos >= PLAZAS[v] ? 'casi' : null;
}

export function datosPago(n, p, v, ahora) {
  const meta = { programa: 'esencial', tanda: TANDA, ventana: v, nivel: n, pago: p };
  const c = new URLSearchParams({
    mode: 'subscription',
    'line_items[0][price]': PRECIOS[`${n}-${p}`],
    'line_items[0][quantity]': '1',
    'subscription_data[billing_cycle_anchor]': String(Math.floor(FECHAS.ancla / 1000)),
    'subscription_data[proration_behavior]': 'none',
    'subscription_data[description]': `FBE Esencial · ${NOMBRES[n]} · precio de fundador`,
    payment_method_collection: 'always',
    locale: 'es',
    success_url: WEB + 'esencial-gracias.html',
    cancel_url: WEB + 'esencial.html#precios',
    expires_at: String(Math.floor(ahora / 1000) + 31 * 60),  // Stripe pide al menos 30 minutos
    'consent_collection[terms_of_service]': 'required',
    'custom_text[terms_of_service_acceptance][message]': 'Acepto la [política de privacidad](https://fuerzabasadaenevidencia.com/privacidad.html) y que el lunes 11 de enero de 2027 se cobre la primera cuota, que se renovará sola hasta que me dé de baja.',
    'custom_text[submit][message]': 'Hoy no se cobra nada. El primer cobro es el lunes 11 de enero de 2027, el día que empezamos todos. Puedes darte de baja cuando quieras.',
  });
  for (const [k, val] of Object.entries(meta)) { c.set(`subscription_data[metadata][${k}]`, val); c.set(`metadata[${k}]`, val); }
  return c;
}

const json = (o) => new Response(JSON.stringify(o), { headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } });

async function comprobar(clave, v, ahora) {
  if (!clave) return json({ ok: false, ventana: v, fallo: 'Falta la variable STRIPE_KEY en Netlify' });
  try {
    const r = { ok: true, ventana: v };
    if (v === 'pronto') {
      const s = await stripe(clave, 'POST', '/v1/checkout/sessions', datosPago('ent', 'a', 'prueba', ahora));
      await stripe(clave, 'POST', `/v1/checkout/sessions/${s.id}/expire`);
      r.pago_de_prueba = { abierto_y_cerrado: true, cobro_hoy: s.amount_total, estado: s.payment_status };
    }
    r.ocupadas = { lista: await ocupadas(clave, 'lista', ahora), video: await ocupadas(clave, 'video', ahora) };
    r.plazas = PLAZAS;
    return json(r);
  } catch (e) {
    return json({ ok: false, ventana: v, fallo: e.message });
  }
}

export default async (req) => {
  const u = new URL(req.url), ahora = Date.now(), v = ventana(ahora);
  const clave = Netlify.env.get('STRIPE_KEY');
  if (u.searchParams.has('comprobar')) return comprobar(clave, v, ahora);
  const ir = (estado) => new Response(null, { status: 303, headers: { Location: `${WEB}esencial.html?esencial=${estado}#precios` } });
  const n = u.searchParams.get('n'), p = u.searchParams.get('p');
  if (!PRECIOS[`${n}-${p}`]) return ir('error');
  if (v === 'pronto' || v === 'cerrado') return ir(v);
  if (!clave) { console.error('Falta la variable STRIPE_KEY'); return ir('error'); }
  try {
    const falta = sinPlaza(await ocupadas(clave, v, ahora), v);
    if (falta) return ir(falta);
    const s = await stripe(clave, 'POST', '/v1/checkout/sessions', datosPago(n, p, v, ahora));
    return new Response(null, { status: 303, headers: { Location: s.url } });
  } catch (e) {
    console.error('No se pudo abrir el pago:', e.message);
    return ir('error');
  }
};
