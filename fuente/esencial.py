# ===== esencial.html (24/11/2026): FBE Esencial, la app sin seguimiento personal =====
# Planes en los docs del proyecto «claude/por-tu-cuenta-plan.md» y «claude/esencial-lanzamiento-enero.md».
# OCULTA hasta el vídeo del 3/1/2027: no se enlaza desde ninguna página de la web (solo desde la guía «Primeras semanas»,
# cuyo bloque se enseña a partir del 3/1), lleva noindex y queda fuera del sitemap, del buscador y de la caché sin conexión.
# Cifras: decisiones de Pelayo del 24/11/2026 (normal 19,99 y 29,99 € al mes, 199 y 299 € al año; fundador 14,99 y 19,99 € al
# mes y 149 y 199 € al año, mientras siga suscrito; 20 plazas; garantía de 14 días). Sin directos (decisión de Pelayo del 26/11/2026). No cambiarlas sin que él lo diga.
# Cobro (opción B, decidida por Pelayo el 24/11/2026): «Reservar plaza» lleva a la función de Netlify
# fuente/formularios/funciones/esencial.mjs, que cuenta las plazas y abre el pago de Stripe: se deja la tarjeta y no se cobra
# nada hasta el lunes 11 de enero; desde ahí se renueva solo, con el precio de fundador. La función devuelve aquí con
# ?esencial=pronto|casi|lleno|lleno-lista|cerrado|error y la página enseña su aviso (vista previa con ese mismo parámetro;
# ?esencial=abierto enseña los botones activos antes de abrir). Antes de ESEN_ABRE los botones salen desactivados; pasada la
# fecha de cierre (o con ESEN_LLENO = True), «plazas cerradas». Tras pagar, Stripe vuelve a esencial-gracias.html (noindex).
# Capturas: las de la app de los atletas (w3/) hasta tener las de la cuenta de demostración: si existen
# web-img/esencial-hoy.webp y web-img/esencial-progreso.webp (702 x 1519), entran solas.
# Plan B (si la app no llega al 31/12): ESEN_INICIO = date(2027, 1, 25) y ESEN_CIERRE = date(2027, 1, 24), y cambiar a mano
# las fechas del bloque de la guía (guia-primeras-semanas/index.html, gracias.html y extra.js).
import datetime as _dt, shutil as _sh
from PIL import Image as _Img
ESEN_INICIO = _dt.date(2027, 1, 11)      # lunes de la semana 1: empiezan todos
ESEN_CIERRE = _dt.date(2027, 1, 10)      # domingo: último día para reservar (o antes, si se llenan)
ESEN_ABRE = _dt.date(2026, 12, 15)      # martes: abren las reservas de la lista de espera (invitaciones de ese día)
ESEN_VIDEO = _dt.date(2027, 1, 3)        # domingo del vídeo: abren las 20 plazas del vídeo
ESEN_PLAZAS = 20                         # por ventana: 20 para la lista de espera y 20 para el vídeo (las cuenta la función)
ESEN_LLENO = False                       # True si se llenan antes del cierre
# Si cambian estas fechas, cambiarlas también en FECHAS de fuente/formularios/funciones/esencial.mjs
ESEN_FN = 'https://fbe-formularios.netlify.app/.netlify/functions/esencial'
ESEN_PAGO = {(k, p): f'{ESEN_FN}?n={k}&amp;p={p}' for k in ('ent', 'nut') for p in ('m', 'a')}
ESEN_PORTAL = 'https://billing.stripe.com/p/login/9B6bJ0ccQ4exeMxcsKbV601'   # portal de Stripe de FBE Esencial: baja y tarjeta
_ES_DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
_ES_MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
def _es_f(d, dia=True): return (f'{_ES_DIAS[d.weekday()]} ' if dia else '') + f'{d.day} de {_ES_MES[d.month - 1]}'
def _es_eur(x): return (f'{x:.2f}'.replace('.', ',') if x != int(x) else str(int(x))) + ' €'
_ES_ABRE = f'{ESEN_INICIO.day} {_ES_MES[ESEN_INICIO.month - 1][:3]}'
# nivel: clave, nombre, para quién, fundador al mes, fundador al año, normal al mes, normal al año, lo que lleva
ESEN_NIV = [
    ('ent', 'Entrenamiento', 'Tu plan de fuerza, que avanza solo semana a semana.', 14.99, 149, 19.99, 199,
     ['Plantilla según tu objetivo, tus días, tu material y tu nivel', 'Cada semana, la siguiente, con mis reglas de progresión y los cuatro frenos',
      'Tu progreso y tus récords, sacados de lo que apuntas', 'Comunidad, guías de Aprende y recetario para consultar', 'Respuestas a las dudas frecuentes, con buscador, en la app']),
    ('nut', 'Entrenamiento y nutrición', 'Lo mismo, con tu plan de nutrición y tu menú en la misma app.', 19.99, 199, 29.99, 299,
     ['Todo lo de Entrenamiento', 'Plan de nutrición con ajuste cada semana', 'Menú semanal con las recetas del recetario']),
]

def _es_cap(slot, w3, alt):
    # Captura de la cuenta de demostración (web-img/<slot>.webp) si existe; si no, la de la app de los atletas (w3/),
    # recortada a la columna de la app (las de w3 son de 702 px de ancho con márgenes a los lados) con forma de móvil.
    # Sale siempre como img/<slot>.webp: la usa también el bloque de la guía «Primeras semanas» (img/esencial-hoy.webp).
    if os.path.exists(f'web-img/{slot}.webp'):
        _sh.copy(f'web-img/{slot}.webp', f'{SAL}/img/{slot}.webp'); w, h = _Img.open(f'web-img/{slot}.webp').size
    else:
        im = _Img.open(f'w3/{w3}.webp').convert('RGB'); x0, x1 = 134, 568; im = im.crop((x0, 0, x1, round((x1 - x0) * 1519 / 702)))
        im.save(f'{SAL}/img/{slot}.webp', 'WEBP', quality=88, method=6); w, h = im.size
    return f'<figure class="pa-tel"><img class="pa-cap" src="img/{slot}.webp" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"></figure>'
_ES_HOY = _es_cap('esencial-hoy', 'portada', 'La app en el móvil: la sesión de hoy, con el calentamiento y los ejercicios que tocan')
_ES_PROG = _es_cap('esencial-progreso', 'fuerza', 'La app en el móvil: tu progreso de fuerza, con la gráfica de cada ejercicio y tus récords')

def _es_plan(n):
    k, nom, para, fm, fa, nm, na, items = n
    hm, ha = ESEN_PAGO[(k, 'm')], ESEN_PAGO[(k, 'a')]
    b = (f'<a class="btn peq es-b" href="{hm}" data-umami-event="Reservar FBE Esencial" data-umami-event-nivel="{k}" data-umami-event-pago="mensual">Reservar plaza</a>'
         if hm else '<a class="btn peq es-b" role="link" aria-disabled="true">Muy pronto</a>')
    return (f'<article class="plan tf es-plan n{1 if k == "ent" else 2} sube" id="{"entrenamiento" if k == "ent" else "nutricion"}" data-nivel="{k}" data-m="{_es_eur(fm)}" data-a="{_es_eur(fa)}" '
            f'data-mn="{_es_eur(nm)}" data-an="{_es_eur(na)}" data-hm="{hm}" data-ha="{ha}"><h3>{nom}</h3><p class="tf-para">{para}</p>'
            f'<p class="tf-eur"><b class="es-v">{_es_eur(fm)}</b><small class="es-u">al mes</small></p>'
            f'<p class="tf-mas"><span>Precio normal: <span class="es-n">{_es_eur(nm)} al mes</span></span><span>IVA incluido</span></p>'
            f'<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>{b}</article>')

ES_JS = '''<script>(function(){var D=document,g=D.getElementById('es-per'),s=D.getElementById('precios');if(!g||!s)return;
var T=Date.now(),A=new Date(s.getAttribute('data-abre')).getTime(),C=new Date(s.getAttribute('data-cierra')).getTime(),
q=(location.search.match(/[?&]esencial=([a-z-]+)/)||[])[1]||'',
est=/^(pronto|casi|lleno|lleno-lista|cerrado|error)$/.test(q)?q:q==='abierto'?'':(s.getAttribute('data-lleno')==='1'||T>C)?'cerrado':T<A?'pronto':'';
if(est){s.setAttribute('data-estado',est);var av=s.querySelector('[data-aviso="'+est+'"]');if(av)av.hidden=false}
function pinta(p){[].forEach.call(g.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-p')===p?'true':'false')});
[].forEach.call(s.querySelectorAll('.es-plan'),function(c){var d=c.dataset,b=c.querySelector('.es-b'),h=d['h'+p],u=p==='m'?'al mes':'al año';
c.querySelector('.es-v').textContent=d[p];c.querySelector('.es-u').textContent=u;c.querySelector('.es-n').textContent=d[p+'n']+' '+u;
if(h&&est!=='pronto'){b.setAttribute('href',h);b.removeAttribute('aria-disabled');b.removeAttribute('role');b.textContent='Reservar plaza';b.setAttribute('data-umami-event','Reservar FBE Esencial');b.setAttribute('data-umami-event-nivel',d.nivel);b.setAttribute('data-umami-event-pago',p==='m'?'mensual':'anual')}
else{b.removeAttribute('href');b.setAttribute('role','link');b.setAttribute('aria-disabled','true');b.textContent=h?s.getAttribute('data-pronto'):'Muy pronto';b.removeAttribute('data-umami-event')}})}
g.addEventListener('click',function(ev){var b=ev.target.closest('button');if(b)pinta(b.getAttribute('data-p'))});
pinta('m')})();</script>'''

_es_cierra = f'{ESEN_CIERRE.isoformat()}T23:59:59+01:00'
# Avisos de #precios: los enseña ES_JS según el estado (data-aviso). Ver la cabecera de este archivo.
def _es_aviso(k, t, u, boton=''):
    return f'<div class="es-cerrado es-aviso sube" data-aviso="{k}"{" id=" + chr(34) + "es-cerrado" + chr(34) if k == "cerrado" else ""} hidden><b>{t}</b><span>{u}</span>{boton}</div>'
_ES_BOL = '<a class="btn peq" href="newsletter.html#alta">Apuntarme al boletín</a>'
_ES_AVISOS = ''.join([
    _es_aviso('cerrado', 'Las plazas de esta tanda están cerradas.', 'Aviso en el boletín cuando abra la siguiente.', _ES_BOL),
    _es_aviso('pronto', f'Las reservas abren el {_es_f(ESEN_ABRE)}.', f'Ese día ya puedes reservar tu plaza. Empezamos todos el {_es_f(ESEN_INICIO)}.'),
    _es_aviso('casi', 'Ahora mismo no quedan plazas libres.', 'Hay reservas a medias: si alguna no se termina, su plaza vuelve a quedar libre en media hora.', '<a class="btn peq" href="esencial.html#precios">Volver a probar</a>'),
    _es_aviso('lleno', f'Las {ESEN_PLAZAS} plazas ya están reservadas.', 'Aviso en el boletín cuando abra la siguiente tanda.', _ES_BOL),
    _es_aviso('lleno-lista', f'Las {ESEN_PLAZAS} plazas de la lista de espera ya están reservadas.', f'El {_es_f(ESEN_VIDEO)}, con el vídeo, se abren {ESEN_PLAZAS} plazas más para empezar el mismo día. Lo aviso en el boletín.', _ES_BOL),
    _es_aviso('error', 'No se ha podido abrir el pago.', f'Vuelve a probar en unos minutos. Si sigue sin ir, escríbeme a {_CCM}.'),
])
_es_cuerpo = f'''
<section id="como"><div class="in"><div class="entrada sube"><h2>Cómo funciona</h2><p>Cuatro pasos. Desde ahí, cada semana la prepara la app.</p></div>
  <ol class="tf-pasos sube"><li><b>Reservas tu plaza</b><span>Eliges nivel y si pagas al mes o al año, y dejas tu tarjeta. No se cobra nada hasta el {_es_f(ESEN_INICIO)}, cuando empezamos todos.</span></li><li><b>Rellenas el cuestionario</b><span>Tu objetivo, tus días, tu material y unas preguntas de salud. Si en ellas sale que conviene consultar, no empiezas sin el visto bueno de tu médico o una <a href="puesta-a-punto.html">Puesta a punto</a> conmigo.</span></li><li><b>Empiezas el {_es_f(ESEN_INICIO)}</b><span>Si no entrenas, con las cuatro semanas de la guía <a href="guia-primeras-semanas/">«Cómo empezar»</a>. Si ya entrenas, con la plantilla de tu nivel.</span></li><li><b>Cada semana, la siguiente</b><span>Apuntas kilos y repeticiones y, con eso, la app te prepara la semana siguiente con mis reglas de progresión.</span></li></ol>
</div></section>
<section class="hoja pa-movil-s es-app"><div class="in">
  <div class="sube"><div class="entrada" style="text-align:left;margin-inline:0"><h2>Lo que ves en la app</h2><p>Qué toca hoy, con cada ejercicio, y al acabar, tu progreso: sale solo de lo que apuntas en cada sesión, sin rellenar nada aparte.</p></div>
    <p class="es-nota">Capturas de la app con la que trabajo con mis atletas.</p></div>
  <div class="pa-moviles sube">{_ES_HOY}{_ES_PROG}</div>
</div></section>
<section id="frenos"><div class="in"><div class="entrada sube"><h2>Como no reviso yo tu semana, la app lleva cuatro frenos</h2><p>Son reglas solo para FBE Esencial, para que la progresión sea prudente cuando nadie la mira.</p></div>
  <ol class="es-frenos sube"><li><b>Parte de lo que hiciste</b><span>Si un día mueves menos peso del previsto, la semana siguiente parte de lo que hiciste, no de lo previsto.</span></li><li><b>Pregunta si ve una errata</b><span>Si un dato parece mal apuntado, te pregunta antes de preparar la semana. Si lo confirmas, se usa.</span></li><li><b>No sube a costa de repeticiones</b><span>Si al subir el peso fueras a quedarte por debajo de tu mínimo de repeticiones, no lo sube: antes suma repeticiones.</span></li><li><b>Baja si te atascas</b><span>Si dos semanas seguidas te quedas por debajo de tu rango, baja un escalón el peso para volver a él.</span></li></ol>
</div></section>
<section class="hoja" id="precios" data-abre="{ESEN_ABRE.isoformat()}T00:00:00+01:00" data-cierra="{_es_cierra}" data-pronto="Desde el {_es_f(ESEN_ABRE, False)}"{' data-lleno="1"' if ESEN_LLENO else ''}><div class="in">
  <div class="tf-barra sube"><div><h2>Precio de fundador</h2><p>Lo mantienes mientras sigas suscrito. Si te das de baja y vuelves, pagas el normal.</p></div>
    <div class="tf-per" id="es-per" role="group" aria-label="Forma de pago"><button type="button" data-p="m" aria-pressed="true">Mensual</button><button type="button" data-p="a" aria-pressed="false">Anual<small>2 meses gratis</small></button></div></div>
  {_ES_AVISOS}
  <div class="planes es-planes">{"".join(_es_plan(n) for n in ESEN_NIV)}</div>
  <div class="es-seguros sube"><div class="es-garantia es-hoy"><i>{ico("candado")}</i><div><b>Hoy no pagas nada</b><span>Reservas con tu tarjeta y el primer cobro es el {_es_f(ESEN_INICIO)}. Si te das de baja antes, no se cobra nada.</span></div></div>
    <div class="es-garantia"><i>{ico("medalla")}</i><div><b>Garantía de 14 días</b><span>Si en los primeros 14 días no te convence, te devuelvo el dinero entero.</span></div></div></div>
  <p class="tf-nota sube" style="text-align:center">Todos los precios llevan el IVA incluido. {ESEN_PLAZAS} plazas, hasta el {_es_f(ESEN_CIERRE)} o hasta que se llenen. Para mayores de 18 años que vivan en España o en otro país de la UE.</p>
</div></section>
<section id="no-lleva"><div class="in"><div class="entrada sube"><h2>Lo que no lleva</h2><p>Para que sepas desde el principio qué es y qué no es.</p></div>
  <ul class="es-no sube"><li><i>{ico("no")}</i><b>Chat conmigo</b><span>No hay mensajes uno a uno.</span></li><li><i>{ico("no")}</i><b>Revisión semanal</b><span>Nadie mira tu semana antes de que llegue: la prepara la app.</span></li><li><i>{ico("no")}</i><b>Ajustes a medida</b><span>No cambio ejercicios ni pautas para tu caso concreto.</span></li></ul>
  <div class="calc sube" style="margin-top:2rem"><div><h3>¿Prefieres que lo revise yo cada semana?</h3><p>Eso son los programas con seguimiento: plan a medida, revisión semanal y contacto conmigo por la app. <b>Desde {DESDE} € al trimestre.</b></p></div><div><a class="btn claro" href="programas.html">Ver los programas</a></div></div>
</div></section>
<section class="hoja" id="fechas"><div class="in dos">
  <div class="entrada sube" style="text-align:left;margin-inline:0"><h2>Las fechas</h2><p>Empezamos todos a la vez: en la comunidad vais por la misma semana.</p></div>
  <ol class="es-fechas sube"><li><span class="es-cuando">Hasta el {_es_f(ESEN_CIERRE)}</span><b>Reservas</b><span>O hasta que se llenen las {ESEN_PLAZAS} plazas.</span></li><li><span class="es-cuando">{_es_f(ESEN_INICIO).capitalize()}</span><b>Semana 1</b><span>Todos empezamos el mismo día. Ese día se cobra la primera cuota.</span></li><li><span class="es-cuando">Cada semana</span><b>Tu semana siguiente</b><span>La prepara la app con lo que apuntas, con mis reglas de progresión y los cuatro frenos.</span></li></ol>
</div></section>
<section><div class="in"><div class="encaje sube" style="margin:0">
  <div><h3>Es para ti si…</h3><ul><li>Empiezas de cero o vuelves tras mucho tiempo: las cuatro primeras semanas son las de la guía</li><li>Ya entrenas y quieres que tu plan avance sin pensarlo cada semana</li><li>Tienes 18 años o más y vives en España o en otro país de la UE</li></ul></div>
  <div class="no"><h3>No es para ti si…</h3><ul><li>Quieres que alguien revise tu técnica o tu semana: para eso están los <a href="programas.html">programas</a></li><li>Necesitas que alguien supervise tus sesiones por una enfermedad o una lesión</li><li>Ya entrenas conmigo: ya tienes la app y mi seguimiento</li></ul></div>
</div></div></section>
<section class="hoja" id="preguntas"><div class="in"><div class="entrada sube"><h2>Preguntas</h2></div>
  <div class="faq sube"><details><summary>¿Necesito experiencia?</summary><p>No. Si empiezas de cero o vuelves tras mucho tiempo, las cuatro primeras semanas son las de la guía «Cómo empezar», en la app. Si ya entrenas, empiezas con la plantilla de tu nivel.</p></details><details><summary>¿Cuántos días a la semana?</summary><p>Si empiezas de cero, dos: las cuatro semanas de la guía y, desde la quinta, una plantilla de dos días. Si ya entrenas, los que pongas en el cuestionario.</p></details><details><summary>¿Qué material necesito?</summary><p>La plantilla se elige con el material que pongas en el cuestionario. Las cuatro semanas de la guía son de gimnasio, y cada ejercicio trae su alternativa.</p></details><details><summary>¿Hablo contigo?</summary><p>No hay chat conmigo ni reviso tu semana: eso lo llevan los <a href="programas.html">programas con seguimiento</a>. Para las dudas, la app trae respuestas a las más frecuentes, con buscador, y la comunidad.</p></details><details><summary>¿Y si tengo una enfermedad o tomo medicación?</summary><p>Antes de empezar contestas unas preguntas de salud. Si sale que conviene consultar, no empiezas sin el visto bueno de tu médico o una <a href="puesta-a-punto.html">Puesta a punto</a> conmigo. Si quieres saberlo ya, tienes la herramienta <a href="revision-medica.html">¿Necesito revisión médica antes de entrenar?</a></p></details><details><summary>¿Y si me duele algo?</summary><p>La app no valora el dolor. Si con el esfuerzo notas dolor u opresión en el pecho, falta de aire que no cuadra con lo que estás haciendo, mareos o palpitaciones, para y habla con tu médico. Para las molestias al entrenar tienes el <a href="semaforo-dolor.html">semáforo del dolor</a>.</p></details><details><summary>¿Es lo mismo que la guía gratis?</summary><p>La guía son las cuatro semanas en papel. En la app, además, apuntas kilos y repeticiones, guarda tus marcas en la cuarta semana y, desde la quinta, te prepara cada semana la siguiente.</p></details><details><summary>¿Cuándo se me cobra?</summary><p>Al reservar dejas tu tarjeta, pero no se cobra nada. La primera cuota se cobra el {_es_f(ESEN_INICIO)} y, desde ahí, cada mes o cada año, según lo que elijas, con el mismo precio de fundador.</p></details><details><summary>¿Puedo darme de baja?</summary><p>Sí, cuando quieras, desde <a href="{ESEN_PORTAL}" rel="noopener">tu suscripción</a>, con el correo con el que reservaste. Sigues dentro hasta el final del periodo que hayas pagado, y si te das de baja antes del {_es_f(ESEN_INICIO, False)}, no se cobra nada. Si vuelves más adelante, pagas el precio normal.</p></details><details><summary>¿Y si se llenan las plazas?</summary><p>Aviso en el <a href="newsletter.html#alta">boletín</a> cuando abra la siguiente tanda.</p></details></div>
</div></section>
{ES_JS}'''
_es_cta = (f'<div class="cta"><a class="btn claro" href="#precios">Ver precios</a><a class="enl" href="#como">Cómo funciona</a></div>'
           + datos((_es_eur(ESEN_NIV[0][3]), 'al mes, precio de fundador'), (str(ESEN_PLAZAS), 'plazas'), (_ES_ABRE, 'empezamos todos')))
FIJO_ES = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="#como">Cómo funciona</a><a class="btn claro" href="#precios">Ver precios</a></div>'
open(f'{SAL}/esencial.html', 'w', encoding='utf-8').write(f'''{cabeza('esencial.html', 'FBE Esencial', 'La app de Fuerza Basada en Evidencia sin seguimiento personal: tu plan de fuerza, preparado cada semana con las reglas de progresión de Pelayo. Plazas de fundador.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-esencial foto" id="inicio">{ANILLOS}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / FBE Esencial</span><h1>Entrena por tu cuenta, con mis reglas de progresión.</h1><p class="sub">FBE Esencial es la app con la que trabajo con mis atletas, sin seguimiento personal: te dice qué toca cada día, apuntas lo que haces y cada semana te prepara la siguiente. Plazas de fundador para empezar todos el {_es_f(ESEN_INICIO)}.</p>{_es_cta}</div><div class="pa-hero">{_ES_HOY.replace(' loading="lazy"', ' fetchpriority="high"')}</div></div></header>
<main id="contenido">{_es_cuerpo}</main>
<section class="cierre">{ANILLOS}<div class="marca-agua">{LOBO}</div><div class="in sube"><h2>¿Empezamos el {_es_f(ESEN_INICIO, False)}?</h2><p>Plazas de fundador hasta el {_es_f(ESEN_CIERRE)}, o hasta que se llenen.</p><a class="btn claro" href="#precios">Ver precios</a></div></section>
{PIE}
{FIJO_ES}
<script src="fbe.js"></script></body></html>''')

# ===== esencial-gracias.html: aquí vuelve Stripe tras reservar. noindex, fuera del sitemap, del buscador y de la caché. =====
open(f'{SAL}/esencial-gracias.html', 'w', encoding='utf-8').write(f'''{cabeza('esencial-gracias.html', 'Plaza reservada', 'Tu plaza de FBE Esencial está reservada.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-esencial" id="inicio">{ANILLOS}{ilus("web-esencial-gracias") or AGUA}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / <a href="esencial.html">FBE Esencial</a> / Plaza reservada</span>{SELLO}<h1>Plaza reservada.</h1><p class="sub">Gracias por apuntarte a FBE Esencial. Hoy no se te ha cobrado nada: el primer cobro es el {_es_f(ESEN_INICIO)}, el día que empezamos todos.</p></div></div></header>
<main id="contenido">
<section><div class="in"><div class="entrada sube"><h2>Cómo sigue</h2></div><div class="caja-s sube"><ol class="pasitos hecho1"><li>Has reservado tu plaza con tu tarjeta. Hoy no se ha cobrado nada.</li><li>Antes del {_es_f(ESEN_INICIO)} te escribo al correo que has dejado al reservar para darte acceso a la app.</li><li>En la app rellenas el cuestionario: tu objetivo, tus días, tu material y unas preguntas de salud.</li><li>El {_es_f(ESEN_INICIO)} se cobra la primera cuota y empiezas la semana 1.</li></ol></div></div></section>
<section class="hoja"><div class="in">
  <div class="calc sube"><div><h3>¿Te has equivocado o quieres darte de baja?</h3><p>Desde tu suscripción, con el correo con el que reservaste, puedes darte de baja o cambiar la tarjeta. Si te das de baja antes del {_es_f(ESEN_INICIO, False)}, no se cobra nada. Para cambiar de nivel o de forma de pago, escríbeme a {_CCM}.</p></div><div><a class="btn claro" href="{ESEN_PORTAL}" rel="noopener">Ir a mi suscripción</a></div></div>
  <div class="es-garantia sube"><i>{ico("medalla")}</i><div><b>Garantía de 14 días</b><span>Si en los primeros 14 días no te convence, te devuelvo el dinero entero.</span></div></div>
</div></section>
<section><div class="in"><div class="entrada sube"><h2>Mientras tanto</h2></div>
  <div class="tarj-g sube">{tarj_sigue("revision-medica.html", "herr-revision", "¿Necesito revisión médica antes de entrenar?")}{tarj_sigue("guia-primeras-semanas/", "web-guias", "La guía «Cómo empezar»")}{tarj_sigue("videos.html", "web-videos", "Mis vídeos")}</div>
</div></section>
</main>
{PIE}
<script src="fbe.js"></script></body></html>''')
