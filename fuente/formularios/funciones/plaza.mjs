// Recibe el formulario «Pedir plaza» de la web (pedir-plaza.html) y crea una fila en la base de Notion
// «Leads – Nuevos contactos», con las mismas columnas que rellenaba NoteForms.
// Direccion: https://fbe-formularios.netlify.app/.netlify/functions/plaza
// Necesita la variable de entorno NOTION_TOKEN (clave de la integracion interna de Notion «Web FBE»,
// con acceso a esa base). La clave la pone Pelayo en Netlify; no va nunca en el codigo.
//
// El formulario se envia como un formulario normal (sin depender de JavaScript): esta funcion responde
// con una redireccion a la pagina de gracias o, si algo falla, de vuelta al formulario con ?error=1 o 2.

const BASE_NOTION = 'a5c4e10c-7a3f-4155-9384-ab91a3a0b12a'; // Leads – Nuevos contactos

// Webs desde las que se acepta el formulario, y a donde se vuelve despues
const WEBS = {
  'https://pelayoplcoaching.github.io': 'https://pelayoplcoaching.github.io/fbe-web/',
  'https://fuerzabasadaenevidencia.com': 'https://fuerzabasadaenevidencia.com/',
  'https://www.fuerzabasadaenevidencia.com': 'https://fuerzabasadaenevidencia.com/',
};

// Opciones exactas de las columnas de Notion
const OBJETIVOS = ['Hipertrofia', 'Fuerza', 'Pérdida de grasa corporal', 'Recomposición Corporal', 'Salud general', 'Prevención de lesiones/Rehabilitación'];
const CONOCIDO = ['Instagram', 'Referido', 'YouTube', 'Web', 'Otro'];  // en la web, «Referido» se muestra como «Recomendación»
const COL_NOTA = 'Muchas gracias por llegar hasta el final! Algo que añadir o algo más que tenga que saber?';
const NUEVO = '🆕 Nuevo (formulario enviado)';

const linea = (v, n) => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, n);

export function webDeVuelta(req) {
  const origen = req.headers.get('origin') || '';
  if (WEBS[origen]) return WEBS[origen];
  const ref = req.headers.get('referer') || '';
  for (const o of Object.keys(WEBS)) if (ref.startsWith(o + '/')) return WEBS[o];
  return null;
}

export function leeFormulario(datos) {
  const nombre = linea(datos.get('nombre'), 200);
  const correo = linea(datos.get('correo'), 200).toLowerCase();
  const telefono = linea(datos.get('telefono'), 40);
  const objetivos = [...new Set(datos.getAll('objetivos').map(String))].filter((o) => OBJETIVOS.includes(o));
  const c = String(datos.get('conocido') ?? '');
  const conocido = CONOCIDO.includes(c) ? c : null;
  const nota = String(datos.get('nota') ?? '').trim().slice(0, 1900);
  const okCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(correo);
  const okTel = /^[+()\d\s.\-]+$/.test(telefono) && telefono.replace(/\D/g, '').length >= 6;
  const okPriv = datos.get('privacidad') === 'si';
  return { ok: Boolean(nombre && okCorreo && okTel && okPriv), nombre, correo, telefono, objetivos, conocido, nota };
}

export function propiedades(f) {
  const p = {
    'Nombre y apellidos': { title: [{ text: { content: f.nombre } }] },
    'Correo electrónico': { email: f.correo },
    'Teléfono de contacto': { phone_number: f.telefono },
    'Objetivos:': { multi_select: f.objetivos.map((name) => ({ name })) },
    'Estado del Lead': { select: { name: NUEVO } },
  };
  if (f.conocido) p['¿Cómo me has conocido?'] = { select: { name: f.conocido } };
  if (f.nota) p[COL_NOTA] = { rich_text: [{ text: { content: f.nota } }] };
  return p;
}

export default async (req) => {
  if (req.method !== 'POST') return new Response('Este formulario solo acepta envíos.', { status: 405 });
  const web = webDeVuelta(req);
  if (!web) return new Response('Origen no permitido.', { status: 403 });
  const ir = (pag) => new Response(null, { status: 303, headers: { Location: web + pag } });

  let datos;
  try { datos = await req.formData(); } catch { return ir('pedir-plaza.html?error=1'); }

  // Trampas para robots: campo invisible relleno, o envio en menos de 3 segundos desde que se abrio la pagina
  if (linea(datos.get('web'), 200)) return ir('gracias-plaza.html');
  const t0 = Number(datos.get('t0')) || 0;
  if (t0 && Date.now() - t0 < 3000) return ir('gracias-plaza.html');

  const f = leeFormulario(datos);
  if (!f.ok) return ir('pedir-plaza.html?error=1');

  const clave = Netlify.env.get('NOTION_TOKEN');
  if (!clave) { console.error('Falta la variable NOTION_TOKEN'); return ir('pedir-plaza.html?error=2'); }

  try {
    let r = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: { Authorization: `Bearer ${clave}`, 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json' },
      body: JSON.stringify({ parent: { database_id: BASE_NOTION }, properties: propiedades(f) }),
    });
    if (!r.ok && r.status === 400 && f.conocido) {
      // Si Notion no acepta la opcion de «¿Cómo me has conocido?» (por ejemplo, una nueva como YouTube), se guarda igual: va a la nota
      console.error('Notion respondio 400 con la opcion', f.conocido, (await r.text()).slice(0, 300));
      const g = { ...f, conocido: null, nota: `${f.nota ? f.nota + '\n\n' : ''}Cómo me conoció: ${f.conocido}`.slice(0, 1990) };
      r = await fetch('https://api.notion.com/v1/pages', {
        method: 'POST',
        headers: { Authorization: `Bearer ${clave}`, 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json' },
        body: JSON.stringify({ parent: { database_id: BASE_NOTION }, properties: propiedades(g) }),
      });
    }
    if (!r.ok) { console.error('Notion respondio', r.status, (await r.text()).slice(0, 500)); return ir('pedir-plaza.html?error=2'); }
  } catch (e) {
    console.error('No se pudo hablar con Notion', e);
    return ir('pedir-plaza.html?error=2');
  }
  return ir('gracias-plaza.html');
};
