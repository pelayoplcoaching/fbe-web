# ---------- páginas interiores (v3) ----------
import json
WEB = 'https://fuerzabasadaenevidencia.com/'
ML = 'https://storage.mlcdn.com/account_image/1626427/'
FOTO = ML + '9IMbm5EtFHhfSdYJ65FBb9koyf2wl2C5kufOmYtZ.png'
if os.path.exists('web-img/foto-pelayo.webp'):
    os.makedirs(f'{SAL}/img', exist_ok=True); shutil.copy('web-img/foto-pelayo.webp', f'{SAL}/img/foto-pelayo.webp'); FOTO = 'img/foto-pelayo.webp'
# testimonios: se leen de la portada ya montada (h), para no repetirlos aqui
VOCES = re.findall(r'<figure class="voz sube" style="margin:0">(.*?)</figure>', h, re.S)
assert len(VOCES) == 4
def voz_banda(i): return f'<section class="sin-arriba"><div class="in"><figure class="voz ancha sube">{VOCES[i]}</figure></div></section>'
def ilus(nombre, clase='ilus'):
    f = f'web-img/{nombre}.webp'
    if not os.path.exists(f): return ''
    os.makedirs(f'{SAL}/img', exist_ok=True); shutil.copy(f, f'{SAL}/img/{nombre}.webp')
    try:
        from PIL import Image as _I
        _w, _h = _I.open(f).size; _wh = f' width="{_w}" height="{_h}"'
    except Exception: _wh = ''
    _arriba = clase == 'ilus'
    _carga = 'loading="eager" fetchpriority="high"' if _arriba else 'loading="lazy"'
    return f'<img class="{clase}" src="img/{nombre}.webp" alt=""{_wh} {_carga} decoding="async">'
def _todas(*ns): return all(os.path.exists(f'web-img/{n}.webp') for n in ns)
PP_OK = _todas('pp-reservas', 'pp-datos', 'pp-hablamos', 'pp-plan')
def PP_IMG(n, t): return ilus(n, 'paso-img').replace('alt=""', f'alt="{t}"', 1) if PP_OK else ''
PROG_OK = _todas('prog-plan', 'prog-app', 'prog-guias')
PUB_OK = _todas('web-guias', 'web-newsletter', 'web-calculadora', 'pub-youtube')
def PUB_IMG(n, i): return ilus(n, 'pub-img') if PUB_OK else f'<i class="ic">{ico(i)}</i>'
def PROG_IMG(n, i): return ilus(n, 'tres-img') if PROG_OK else f'<i>{ico(i)}</i>'
_PA_P = ['pa-pacientes', 'pa-profesionales', 'pa-entrenadores']
def PA_PARA_IMG(i, l): return f'<div class="pa-para-img">{ilus(_PA_P[i], "pa-para-ilus")}</div>' if _todas(*_PA_P) else f'<span class="n" aria-hidden="true">{l}</span>'

def datos(*xs): return '<ul class="datos">' + ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in xs) + '</ul>'
def sigue(arch, padre=None):
    L = [u for u, _ in PAGS]; i = L.index(padre[0] if padre else arch)
    a = padre if padre else (PAGS[i - 1] if i else ('index.html', 'Inicio')); b = PAGS[i + 1] if i + 1 < len(PAGS) else ('index.html', 'Inicio')
    return f'<nav class="sigue" aria-label="Seguir leyendo"><div class="in"><a href="{a[0]}"><small>Anterior</small><b>{a[1]}</b></a><a class="der" href="{b[0]}"><small>Siguiente</small><b>{b[1]}</b></a></div></nav>'
def cabeza(arch, titulo, desc, extra=''):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo} · Fuerza Basada en Evidencia</title><meta name="description" content="{desc}">
<link rel="canonical" href="{WEB}{arch}"><meta name="theme-color" content="#140B3A"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="icono-180.png">
<meta property="og:image" content="{WEB}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="Fuerza Basada en Evidencia"><meta property="og:title" content="{titulo} · Fuerza Basada en Evidencia"><meta property="og:description" content="{desc}"><meta property="og:url" content="{WEB}{arch}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap"><link rel="stylesheet" href="fbe.css">{extra}</head><body class="pag-{arch[:-5]}" style="margin:0">'''
def pagina(arch, titulo, desc, h1, sub, cuerpo, cta='', cierre_t=None, fijo=None, extra='', lado='', padre=None):
    doc = f'''{cabeza(arch, titulo, desc, extra)}
{cabecera(padre[0] if padre else arch)}
<header class="hero mini t-{arch[:-5]}{" foto" if lado else ""}" id="inicio">{ANILLOS}{"" if lado else (ilus("web-" + arch[:-5]) or f"<div class=\"marca-agua\">{LOBO}</div>")}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / {f"<a href=\"{padre[0]}\">{padre[1]}</a> / " if padre else ""}{titulo}</span><h1>{h1}</h1><p class="sub">{sub}</p>{cta}</div>{lado}</div></header>
<main id="contenido">{cuerpo}</main>
{sigue(arch, padre)}
{cierre(*(cierre_t or ()))}
{PIE}
{fijo or FIJO}
<script src="fbe.js"></script></body></html>'''
    open(f'{SAL}/{arch}', 'w', encoding='utf-8').write(doc)
BTN = f'<div class="cta"><a class="btn claro" href="{FORM}">Pedir plaza</a></div>'
SI = f'<span class="v si">{ico("si")}<b>Sí</b></span>'; NO = f'<span class="v no">{ico("no")}<b>No</b></span>'

# ===== quién soy =====
LDP = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'Person', 'name': 'Pelayo Fernández Cidón', 'jobTitle': 'Médico especialista en Medicina Interna y entrenador', 'url': WEB + 'quien-soy.html', 'worksFor': {'@type': 'Organization', 'name': 'Fuerza Basada en Evidencia', 'url': WEB}, 'sameAs': [u for _, u in REDES]}, ensure_ascii=False) + '</script>'
def caja_i(n, i): return ilus(n, 'foto-c') or f'<i class="ic">{ico(i)}</i>'
pagina('quien-soy.html', 'Quién soy', 'Pelayo Fernández Cidón, médico internista y entrenador: cómo trabajo y con quién.', 'Médico internista. Prescriptor de ejercicio físico.', 'Soy Pelayo Fernández Cidón, especialista en medicina interna. Prescribo ejercicio de fuerza y nutrición a gente con poco tiempo que quiere un plan claro y con base científica.', f'''
<section><div class="in dos">
  <div class="sube"><div class="entrada"><h2>Cómo empezó</h2></div>
    <ol class="linea">
      <li><h3>Primero de Medicina</h3><p>Había dejado el fútbol, había cogido peso y los estudios se me hacían cuesta arriba. Empecé a entrenar fuerza y recuperé la energía y la cabeza despejada. Ese año lo aprobé todo.</p></li>
      <li><h3>La preparación del MIR</h3><p>Seguí entrenando mientras estudiaba. También durante mi periodo de médico interno residente en el Hospital Universitario La Paz, en Madrid.</p></li>
      <li><h3>Medicina interna</h3><p>Trabajo en un hospital de alta complejidad, con pacientes con enfermedad crónica, varias patologías a la vez, dolor persistente y limitación funcional. Ahí aprendí algo que no viene en los libros: <strong>todo el mundo sabe que el ejercicio es bueno, pero casi nunca se prescribe bien</strong>. Y la fuerza, menos todavía, sobre todo en quien ya tiene una enfermedad.</p></li>
      <li><h3>2020: nace FBE</h3><p>Para llevar a la vida real lo que la evidencia dice desde hace años.</p></li>
    </ol></div>
  <aside class="pegada sube"><h3>Formación</h3><ul class="marcas">{FORM_LI}</ul><p class="coleg">{ico("medalla")}<span>Médico colegiado n.º <b>{COLEGIADO}</b><small>{COLEGIO}</small></span></p><p class="tr-ver"><a href="#formacion">Toda mi trayectoria</a></p><a class="btn" href="{FORM}">Pedir plaza</a><div class="redes claras">{''.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in REDES)}</div></aside>
</div></section>
<section class="lema-banda">{ilus("web-frase", "lema-fondo")}<div class="in sube"><blockquote>Lo que no puedes sostener en tu día a día no sirve.</blockquote><p>Pelayo Fernández Cidón</p></div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Cómo trabajo</h2></div>
  <div class="ciencia"><div class="rej">
    <article class="idea sube">{ilus("web-contexto", "foto-i")}<h3>Primero, tu contexto</h3><p>El plan se ajusta a tu historial médico, tu dolor si lo hay, tu horario, tu estrés, tu sueño y lo que ya hayas probado.</p></article>
    <article class="idea sube">{ilus("web-fuerza-centro", "foto-i")}<h3>La fuerza, en el centro</h3><p>Con 45 a 60 minutos bien usados basta. Volumen, intensidad y progresión, decididos y por escrito.</p></article>
    <article class="idea sube">{ilus("web-evidencia", "foto-i")}<h3>Evidencia que cabe en tu vida</h3><p>Guías clínicas y consensos internacionales, aplicados a una semana que tiene guardias, niños o viajes.</p></article>
  </div></div></div></section>
<section><div class="in"><div class="entrada sube"><h2>Con quién trabajo</h2></div>
  <div class="bento">
    <div class="caja sube">{caja_i('web-poco-tiempo', 'reloj')}<h3>Profesionales con poco tiempo</h3><p>Jornadas largas, turnos rotatorios o guardias.</p></div>
    <div class="caja sube">{caja_i('web-dolor', 'cambio')}<h3>Dolor o lesiones previas</h3><p>Molestias musculoesqueléticas que condicionan cómo entrenar.</p></div>
    <div class="caja sube">{caja_i('web-cronica', 'candado')}<h3>Patología crónica controlada</h3><p>Quien quiere entrenar con seguridad y con alguien que entiende su tratamiento.</p></div>
    <div class="caja sube">{caja_i('web-genericas', 'grafica')}<h3>Hartos de rutinas genéricas</h3><p>Quien ya ha probado plantillas y quiere algo hecho para él.</p></div>
  </div></div></section>
{voz_banda(1)}
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Lo que publico</h2><p>Si todavía no quieres una asesoría, empieza por aquí.</p></div>
  <div class="bento">
    <a class="caja sube" href="guias.html">{PUB_IMG('web-guias', 'libro')}<h3>Guías</h3><p>Nueve guías prácticas para descargar.</p></a>
    <a class="caja sube" href="newsletter.html">{PUB_IMG('web-newsletter', 'chat')}<h3>Boletín</h3><p>Un correo a la semana.</p></a>
    <a class="caja sube" href="{CALC}">{PUB_IMG('web-calculadora', 'plato')}<h3>Calculadora de proteína</h3><p>Gratis, con reparto por comidas.</p></a>
    <a class="caja sube" href="{dict(REDES)['YouTube']}" target="_blank" rel="noopener">{PUB_IMG('pub-youtube', 'video')}<h3>YouTube</h3><p>Vídeos sobre fuerza, nutrición y salud.</p></a>
  </div></div></section>''', BTN + datos(('15+', 'años entrenando fuerza'), ('2020', 'el año en que nace FBE')), extra=LDP, lado=f'<div class="retrato xl">PF<img src="{FOTO}" alt="Pelayo Fernández Cidón" width="720" height="900" fetchpriority="high" decoding="async" onerror="this.remove()"></div>')

# ===== programas =====
# Desde el 23/11/2026 solo tres programas (fuera Essential y Complete): con la app, la revision es semanal en todos.
# Tarifas (pagina tarifas.html, sin enlazar): fuente/tarifas.py. DESDE = trimestre del mas barato (Performance).
# TARIFA y DESDE estan arriba de sitio-cab.py (la portada tambien dice «Desde ... al trimestre»)
P = [('performance', 'Entrenamiento', 'Performance', 'Semanal', 'La app', ['Revisión y actualización del plan cada semana', 'Mensajes conmigo en la app, respuesta en 48-72 h', 'Ajustes sobre la marcha: horarios, viajes, molestias, cansancio', 'Para semanas que no se parecen entre sí']),
 ('elite', 'Entrenamiento y nutrición', 'Elite', 'Semanal', 'La app', ['Revisión semanal de los dos planes', 'Mensajes conmigo en la app, respuesta en 48-72 h', 'Ajustes continuos: horario, estado físico y mental, viajes, carga de trabajo', 'Nuevos objetivos cuando toque']),
 ('eliteplus', 'Entrenamiento, nutrición y videollamada', 'Elite Plus', 'Semanal', 'La app y videollamada', ['Todo lo de Elite', 'Videollamada semanal de 20 minutos', 'Para repasar el progreso, ajustar la estrategia y planificar'])]
def plan(p):
    k, g, n, r, c, items = p
    niv, tope = {'performance': (1, 3), 'elite': (2, 3), 'eliteplus': (3, 3)}[k]
    barras = '<span class="nivel" aria-hidden="true">' + ''.join(f'<i{" class=\"on\"" if j < niv else ""}></i>' for j in range(tope)) + '</span>'
    return f'<article class="plan n{niv}{" oro" if k == "eliteplus" else ""} sube" id="{k}"><span class="eti" hidden>Te encaja</span><h3>{n}{barras}</h3><p class="ritmo"><span>{g}</span><span>Revisión semanal</span></p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><a class="btn peq" href="{FORM}">Empezar con {n}</a><a class="comp" href="#lado">Comparar con los demás</a></article>'
fila = lambda t, f: f'<tr><th scope="row">{t}</th>' + ''.join(f'<td>{f(p)}</td>' for p in P) + '</tr>'
TABLA = '<div class="tabla-marco ancha sube" tabindex="0" role="region" aria-label="Comparativa de programas"><table class="compara ancha"><thead><tr><td></td>' + ''.join(f'<th scope="col"><a href="#{p[0]}">{p[2]}</a></th>' for p in P) + '</tr></thead><tbody>' + fila('Entrenamiento a medida', lambda p: SI) + fila('Plan de nutrición', lambda p: SI if 'nutrición' in p[1] else NO) + fila('Videollamada semanal', lambda p: SI if p[0] == 'eliteplus' else NO) + fila('Cada cuánto reviso tu plan', lambda p: 'Cada semana') + fila('Por dónde hablamos', lambda p: 'Por la app') + fila('App FBE Equipo y guías', lambda p: SI) + '</tbody></table></div>'
ELIGE = '''<div class="elige sube" id="elige"><div><h2>¿Cuál te encaja?</h2><p>Dos respuestas y te señalo por dónde empezaría.</p></div>
  <div class="elige-p"><p id="e1">¿Quieres también la nutrición?</p><div class="fases claras" role="group" aria-labelledby="e1" data-g="n"><button type="button" data-v="0" aria-pressed="false">Solo entrenamiento</button><button type="button" data-v="1" aria-pressed="true">Entrenamiento y nutrición</button></div>
  <p id="e2">¿Quieres que nos veamos cada semana por videollamada?</p><div class="fases claras" role="group" aria-labelledby="e2" data-g="r"><button type="button" data-v="0" aria-pressed="true">No hace falta</button><button type="button" data-v="1" aria-pressed="false">Sí, cada semana</button></div></div>
  <p class="elige-r" aria-live="polite"><span id="elige-t"></span> <a href="#elite" id="elige-a">Ver el programa</a></p></div>'''
JS_P = '''<script>(function(){var D=document,O=['performance','elite','eliteplus'],M={'00':'performance','01':'eliteplus','10':'elite','11':'eliteplus'},N={performance:'Performance',elite:'Elite',eliteplus:'Elite Plus'},v={n:'1',r:'0'};try{var g=JSON.parse(localStorage.getItem('fbe-web-plan'));if(g&&/^[01]$/.test(g.n)&&/^[01]$/.test(g.r))v=g}catch(e){}
[].forEach.call(D.querySelectorAll('.elige .fases'),function(gr){[].forEach.call(gr.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v[gr.dataset.g])})});
function pinta(){var k=M[v.n+v.r],t='Yo empezaría con '+N[k]+'.';if(v.n==='0'&&v.r==='1')t='La videollamada semanal va con Elite Plus, que también incluye nutrición.';D.getElementById('elige-t').textContent=t;D.getElementById('elige-a').setAttribute('href','#'+k);[].forEach.call(D.querySelectorAll('.plan'),function(p){var s=p.id===k;p.classList.toggle('top',s);p.querySelector('.eti').hidden=!s});[].forEach.call(D.querySelectorAll('.compara.ancha tr'),function(tr){[].forEach.call(tr.children,function(c,i){c.classList.toggle('yo',i>0&&O[i-1]===k)})})}
[].forEach.call(D.querySelectorAll('.elige .fases'),function(g){g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b)});v[g.dataset.g]=b.dataset.v;try{localStorage.setItem('fbe-web-plan',JSON.stringify(v))}catch(e){}pinta()})});pinta()})();</script>'''
pagina('programas.html', 'Programas', 'Programas de seguimiento de entrenamiento y nutrición: Performance, Elite y Elite Plus.', 'Elige cuánto quieres que te acompañe.', 'Los tres son a medida, se llevan desde la app y los reviso cada semana. Cambia si llevan nutrición y videollamada.', f'''
<section><div class="in">
  {ELIGE}
  <div class="planes tres-p">{plan(P[0])}{plan(P[1])}{plan(P[2])}</div>
  <p class="desde sube"><b>Desde {DESDE} € al trimestre</b><span>IVA incluido. Es el precio de Performance.</span></p>
  <div class="aviso sube" style="margin:2.5rem 0 0"><span><b>Trabajo con un grupo pequeño.</b> Si ahora no hay plaza, entras en la lista de espera al rellenar el formulario.</span><a class="btn peq" href="puesta-a-punto.html">¿No quieres esperar? Puesta a punto</a></div>
</div></section>
<section class="hoja" id="lado"><div class="in"><div class="entrada sube"><h2>Los tres, lado a lado</h2></div><p class="desliza">Desliza la tabla para ver los tres.</p>{TABLA}</div></section>
<section><div class="in"><div class="entrada sube"><h2>Lo que llevan todos</h2></div>
  <ul class="tres sube" style="margin-top:0"><li>{PROG_IMG('prog-plan', 'pesa')}<b>Plan a medida</b><span>Hecho para tu horario, tu material y tu punto de partida.</span></li><li>{PROG_IMG('prog-app', 'video')}<b>La app FBE Equipo</b><span>Sesiones, registro serie a serie, vídeos, recetario y progreso. <a href="index.html#semana">Mírala por dentro</a>.</span></li><li>{PROG_IMG('prog-guias', 'libro')}<b>Las guías</b><span>Para entender lo que haces y por qué.</span></li></ul>
</div></section>
{voz_banda(3)}
<section class="hoja"><div class="in"><div class="entrada sube centro"><h2>Antes de pedir plaza</h2></div>
  <div class="faq sube"><details><summary>¿Cómo empiezo?</summary><p>Rellenas el formulario, hacemos una videollamada gratuita de 20 minutos para ver tu punto de partida y, si encaja, preparo tu plan.</p></details><details><summary>¿Puedo contratar solo el entrenamiento?</summary><p>Sí: Performance es solo entrenamiento. La nutrición por separado es poco habitual (individualizamos caso a caso).</p></details><details><summary>¿Cada cuánto revisas mi progreso?</summary><p>Cada semana, en los tres programas.</p></details><details><summary>¿Y si me lesiono o me duele algo?</summary><p>Me lo dices cuanto antes y ajusto el plan. Si el dolor es agudo o no cede, te derivo a quien deba verlo.</p></details></div>
  <p class="sube" style="text-align:center;margin-top:1.5rem"><a href="dudas.html">Todas las dudas</a></p>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>¿Solo quieres un plan, sin seguimiento?</h3><p>La Puesta a punto es una consulta y un plan de 12 semanas, con lectura de tu analítica. Sin lista de espera.</p></div><div><a class="btn claro" href="puesta-a-punto.html">Ver la Puesta a punto</a></div></div></div></section>{JS_P}''', BTN + datos(('3', 'programas'), ('20 min', 'de videollamada inicial, gratis'), ('1', 'app para llevarlo todo')), ('¿Sigues dudando?', 'Cuéntame tu caso y te digo con cuál empezaría yo.'))

# ===== puesta a punto =====
FQ = [('¿Incluye seguimiento?', 'No. Es una consulta y un plan. Tienes una ronda de dudas por correo en los 7 días siguientes a la entrega.'), ('¿Cuánto tarda en llegar el plan?', 'Menos de 7 días desde la videollamada.'), ('¿Qué analítica necesito?', 'Una de los últimos 12 meses. En esta página tienes la lista de lo que conviene que incluya.'), ('¿Cómo te envío mis pruebas?', 'Por un formulario seguro, con tu consentimiento expreso. Nunca por WhatsApp.'), ('¿Se puede regalar?', 'Sí.'), ('¿Sustituye a mi médico?', 'No. No es un diagnóstico ni un tratamiento médico.')]
LDS = '<script type="application/ld+json">' + json.dumps([{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Puesta a punto', 'provider': {'@type': 'Person', 'name': 'Pelayo Fernández Cidón'}, 'description': 'Consulta por videollamada, lectura de analítica y plan de entrenamiento y nutrición para 12 semanas.', 'offers': {'@type': 'Offer', 'price': '250', 'priceCurrency': 'EUR', 'url': STRIPE}}, {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FQ]}], ensure_ascii=False) + '</script>'
ANA = ['Hemograma', 'Ferritina', 'Glucosa o HbA1c', 'Perfil lipídico', 'TSH', 'Vitamina D', 'Creatinina', 'Transaminasas', 'B12 y folato']
FIJO_P = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="programas.html">Programas</a><a class="btn claro" href="{STRIPE}">Reservar por 250 €</a></div>'
BANNER = ilus('foto-banner', 'banner sube').replace('alt=""', 'alt="Pelayo Fernández Cidón, médico internista"')
if BANNER: BANNER = f'<section class="sin-arriba"><div class="in">{BANNER}</div></section>'
pagina('puesta-a-punto.html', 'Puesta a punto', 'Una consulta, un plan de 12 semanas y la lectura de tu analítica por un médico internista. Sin seguimiento. 250 €.', 'Una consulta, un plan, sin seguimiento.', 'Soy médico internista: leo tu analítica y tu historial, hablamos 30 minutos por videollamada y en menos de 7 días tienes tu plan de entrenamiento y nutrición para 12 semanas.', f'''
<section><div class="in dos">
  <div class="sube"><div class="entrada"><h2>Qué incluye</h2></div>
    <ul class="marcas" style="font-size:1.1rem;gap:1rem">
      <li><strong>Lectura de tu analítica</strong>, con lo que significa para entrenar y comer.</li>
      <li><strong>Prescripción de entrenamiento</strong>: estructura semanal, ejercicios, cargas y progresión.</li>
      <li><strong>Pautas de nutrición</strong> ajustadas a tu objetivo.</li>
      <li><strong>Suplementación, solo si está justificada.</strong> Muchas veces, ninguna.</li>
      <li><strong>Qué vigilar</strong> en tu próxima analítica.</li>
      <li><strong>Una ronda de dudas por correo</strong> en los 7 días siguientes a la entrega, con respuesta en 48 a 72 horas.</li>
    </ul>
    <div class="entrada" style="margin-top:3rem;margin-bottom:1.2rem"><h2>Qué necesito de ti</h2><p>Una analítica de los últimos 12 meses. Lo ideal es que incluya esto:</p></div>
    <ul class="chips" id="ana">{''.join(f'<li>{a}</li>' for a in ANA)}</ul>
    <p style="margin-top:1rem"><button class="btn peq hueco" id="copia" type="button" data-t="Analítica para la Puesta a punto: {', '.join(a.lower() for a in ANA)}.">Copiar la lista para pedirla</button> <span id="copia-ok" role="status" style="color:var(--tinta-2);margin-left:.6rem"></span></p>
    <p style="color:var(--tinta-2);margin-top:1.2rem;max-width:40rem">El historial y las pruebas se suben por un formulario seguro, con tu consentimiento expreso. Nunca por WhatsApp.</p>
  </div>
  <aside class="pegada sube"><p class="precio">250 € <small>pago único, IVA incluido</small></p><ul class="marcas"><li>Videollamada de 30 minutos</li><li>Plan entregado en menos de 7 días</li><li>Plan para 12 semanas</li><li>Se puede regalar</li></ul><a class="btn" href="{STRIPE}">Reservar mi plaza</a><small style="color:var(--tinta-2)">Pago con tarjeta por Stripe al reservar. Acepto una o dos consultas por semana.</small><a href="{ESCRIBE}">Tengo una duda antes</a></aside>
</div></section>
{BANNER}
<section class="pasos{" con-img" if PP_OK else ""}">{ANILLOS}<div class="in"><div class="entrada sube"><h2>Cómo va</h2><p>De la reserva al plan, en cuatro pasos.</p></div>
  <ol class="cuatro">
    <li class="sube">{PP_IMG("pp-reservas", "Reservas")}<h3>Reservas</h3><p>Pagas con tarjeta y tu plaza queda guardada.</p></li>
    <li class="sube">{PP_IMG("pp-datos", "Me envías tus datos")}<h3>Me envías tus datos</h3><p>Analítica e historial, por un formulario seguro.</p></li>
    <li class="sube">{PP_IMG("pp-hablamos", "Hablamos 30 minutos")}<h3>Hablamos 30 minutos</h3><p>Por videollamada: tu objetivo, tu horario y lo que dice tu analítica.</p></li>
    <li class="sube">{PP_IMG("pp-plan", "Recibes tu plan")}<h3>Recibes tu plan</h3><p>En menos de 7 días, para 12 semanas. Y una ronda de dudas por correo.</p></li>
  </ol></div></section>
<section><div class="in"><div class="encaje sube" style="margin:0">
  <div><h3>Es para ti si…</h3><ul><li>Quieres un plan hecho por un médico, sin compromiso mensual</li><li>Tienes una analítica y no sabes qué hacer con ella</li><li>Te organizas bien por tu cuenta una vez que sabes qué toca</li></ul></div>
  <div class="no"><h3>No es para ti si…</h3><ul><li>Tienes una enfermedad activa sin controlar</li><li>Estás embarazada o eres menor de edad</li><li>Compites y buscas la preparación de una prueba concreta</li><li>Esperas corregir un valor alterado solo con entrenamiento y dieta</li><li>Quieres acompañamiento semanal: para eso están los <a href="programas.html">programas</a></li></ul></div>
</div><p class="sube" style="color:var(--tinta-2);margin-top:1.5rem;max-width:46rem">No es un diagnóstico ni un tratamiento médico, y no sustituye a tu médico habitual.</p></div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Puesta a punto o programa</h2></div>
  <div class="tabla-marco sube"><table class="compara dosc"><thead><tr><td></td><th scope="col" class="yo">Puesta a punto</th><th scope="col">Programas</th></tr></thead><tbody>
    <tr><th scope="row">Qué es</th><td class="yo">Una consulta y un plan</td><td>Acompañamiento continuo</td></tr>
    <tr><th scope="row">Ajustes del plan</th><td class="yo">Una ronda de dudas por correo</td><td>Cada semana</td></tr>
    <tr><th scope="row">Plaza</th><td class="yo">Sin lista de espera</td><td>Grupo pequeño, puede haber espera</td></tr>
  </tbody></table></div>
  <p class="sube" style="text-align:center;margin-top:1.5rem"><a href="programas.html">Ver los programas</a></p>
</div></section>
<section><div class="in"><div class="entrada sube centro"><h2>Antes de reservar</h2></div>
  <div class="faq sube">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FQ)}</div>
  <div class="llama sube" style="max-width:48rem;margin-inline:auto"><b>¿Es para regalar?</b><span style="flex:1;min-width:12rem;color:var(--tinta-2)">Se puede. Cuéntamelo antes de reservar.</span><a class="btn peq" href="{ESCRIBE}">Escribirme</a></div>
</div></section>
<script>(function(){{var b=document.getElementById('copia'),o=document.getElementById('copia-ok');if(!b)return;b.addEventListener('click',function(){{var t=b.dataset.t;function ok(){{o.textContent='Copiada.'}}function mal(){{var r=document.createRange();r.selectNodeContents(document.getElementById('ana'));var s=getSelection();s.removeAllRanges();s.addRange(r);o.textContent='Seleccionada: copia con tu teclado.'}}try{{navigator.clipboard.writeText(t).then(ok,mal)}}catch(e){{mal()}}}})}})();</script>''', f'<div class="cta"><a class="btn claro" href="{STRIPE}">Reservar por 250 €</a></div>' + datos(('30 min', 'de videollamada'), ('&lt; 7 días', 'y tienes el plan'), ('12 semanas', 'de plan')), ('¿Prefieres seguimiento?', 'Los programas incluyen revisión y ajustes cada semana o cada mes.'), fijo=FIJO_P, extra=LDS)

# ===== guías =====
G = [('Entrenar, comer y descansar siendo médico', 'Guía práctica para turnos y guardias: plan de fuerza de 3 sesiones semanales de 60 minutos, 12 semanas de progresión, batch cooking, la mochila de guardia, sueño y cafeína.', 'Residentes, adjuntos y sanitarios con noches o guardias de 24 horas.', '5,99', '12528', 'Guardias', 'entreno nutri'),
 ('Recomposición corporal', 'El arte de perder grasa y ganar músculo a la vez: fundamentos, estrategia de fuerza, nutrición flexible, descanso y suplementación.', 'Quien empieza, quien tiene sobrepeso o quien vuelve a entrenar.', '5,99', '5573', 'Recomp', 'entreno nutri'),
 ('Rutina minimalista (45 minutos o menos)', 'Rutinas cortas con base de 2 días por semana, ampliable a 3-5: ejercicios compuestos, técnicas de intensidad y calentamiento.', 'Quien tiene poco tiempo.', '5,99', '12594', '45 min', 'entreno'),
 ('Cómo llegar al 10 % de grasa corporal', 'Metabolismo, NEAT, fuerza en déficit, un sistema de 16 reglas de nutrición y cómo mantenerlo después.', 'Quien quiere un proceso paso a paso y está dispuesto a seguirlo.', '5,99', '12595', '10 %', 'nutri entreno'),
 ('La ciencia del volumen', 'Superávit calórico, reparto de macronutrientes, suplementación, principios de hipertrofia y cómo seguir tu progreso.', 'Quien quiere ganar masa muscular con estrategia.', '5,99', '12596', 'Volumen', 'nutri entreno'),
 ('Actividad física y salud', 'Lo que todo el mundo debería saber: recomendaciones aeróbicas y de fuerza, riesgos del sedentarismo, cambio de hábitos y plantillas. Basada en las directrices de la OMS (2020).', 'Sanitarios y público general.', '9,99', '12597', 'Moverse', 'salud'),
 ('Alimentación y salud basada en evidencia', 'Qué pesa de verdad en la longevidad, errores frecuentes, patrones dietéticos, alimentos protectores, frecuencia de comidas y ayuno intermitente.', 'Público general y sanitarios.', '5,99', '12598', 'Comer', 'nutri salud'),
 ('Sueño, estrés y rendimiento', 'Biología del sueño, cómo afecta al rendimiento, higiene del sueño y gestión del estrés y el cortisol.', 'Deportistas recreativos, entrenadores y gente activa.', '5,99', '12599', 'Sueño', 'salud'),
 ('Creatina monohidrato: la última evidencia', 'Fundamentos, pautas de uso, beneficios según la población, efectos secundarios desmentidos y comparativa de formas.', 'Cualquiera que la tome o se lo esté pensando.', '5,99', '12601', 'Creatina', 'nutri')]
MOT = ['<circle cx="120" cy="100" r="88"/><path d="M128 40a62 62 0 1 0 38 104a50 50 0 0 1-38-104z"/><circle class="f" cx="60" cy="50" r="3"/><circle class="f" cx="92" cy="26" r="2"/><circle class="o f" cx="40" cy="104" r="2.5"/>', '<path d="M14 20v160h176"/><path d="M14 62C74 62 112 150 190 150"/><path class="o g" d="M14 150C74 150 112 62 190 62"/>', '<circle cx="110" cy="100" r="78"/><circle cx="110" cy="100" r="56"/><path class="o g" d="M110 22a78 78 0 1 1-78 78"/><path d="M110 100V50M110 100l38 22"/>', '<circle cx="110" cy="100" r="74"/><circle cx="110" cy="100" r="48"/><circle class="o g" cx="110" cy="100" r="74" pathLength="100" stroke-dasharray="10 90" transform="rotate(-90 110 100)"/>', '<path d="M20 180h170"/><rect x="34" y="140" width="24" height="40"/><rect x="70" y="112" width="24" height="68"/><rect x="106" y="84" width="24" height="96"/><rect class="o g" x="142" y="48" width="24" height="132"/>', '<circle cx="104" cy="100" r="84"/><circle cx="104" cy="100" r="60"/><path class="o g" d="M0 110h52l14-42 22 82 18-58 10 18h84"/>', '<circle cx="110" cy="100" r="82"/><circle cx="110" cy="100" r="60"/><path d="M110 40v120M110 100l52-30"/><path class="o g" d="M110 100l-52-30"/>', '<path d="M0 50q25-22 50 0t50 0t50 0t50 0"/><path d="M0 86q25-22 50 0t50 0t50 0t50 0"/><path class="o g" d="M0 122q25-22 50 0t50 0t50 0t50 0"/><path d="M0 158q25-22 50 0t50 0t50 0t50 0"/>', '<path d="M110 28l62 36v72l-62 36-62-36V64z"/><path d="M110 60l34 20v40l-34 20-34-20V80z"/><path class="o g" d="M110 28v32M172 136l-28-16M48 136l28-16"/>']
DENTRO = [['Plan de fuerza: 3 sesiones semanales de 60 minutos', '12 semanas de progresión', 'Batch cooking', 'La mochila de guardia', 'Sueño y cafeína'], ['Fundamentos', 'Estrategia de fuerza', 'Nutrición flexible', 'Descanso', 'Suplementación'], ['Base de 2 días por semana, ampliable a 3-5', 'Ejercicios compuestos', 'Técnicas de intensidad', 'Calentamiento'], ['Metabolismo y NEAT', 'Fuerza en déficit', 'Un sistema de 16 reglas de nutrición', 'Cómo mantenerlo después'], ['Superávit calórico', 'Reparto de macronutrientes', 'Suplementación', 'Principios de hipertrofia', 'Cómo seguir tu progreso'], ['Recomendaciones aeróbicas y de fuerza', 'Riesgos del sedentarismo', 'Cambio de hábitos', 'Plantillas'], ['Qué pesa de verdad en la longevidad', 'Errores frecuentes', 'Patrones dietéticos', 'Alimentos protectores', 'Frecuencia de comidas y ayuno intermitente'], ['Biología del sueño', 'Cómo afecta al rendimiento', 'Higiene del sueño', 'Gestión del estrés y el cortisol'], ['Fundamentos', 'Pautas de uso', 'Beneficios según la población', 'Efectos secundarios desmentidos', 'Comparativa de formas']]
CORTA = ['Guía práctica para turnos y guardias.', 'El arte de perder grasa y ganar músculo a la vez.', 'Rutinas cortas, de 45 minutos o menos.', 'Un proceso paso a paso, de la fuerza en déficit al mantenimiento.', 'Cómo comer y entrenar para ganar músculo.', 'Lo que todo el mundo debería saber. Basada en las directrices de la OMS (2020).', 'Qué comer para vivir más y mejor, según la evidencia.', 'Dormir mejor para rendir mejor.', 'Lo que dice la evidencia más reciente.']
GIMG = ['guia-guardias', 'guia-recomposicion', 'guia-minimalista', 'guia-10-grasa', 'guia-volumen', 'guia-actividad-salud', 'guia-alimentacion', 'guia-sueno', 'guia-creatina']
TEMA = {'entreno': 'Entrenamiento', 'nutri': 'Nutrición', 'salud': 'Salud'}
def guia(i, g):
    t, d, p, e, c, pal, tm = g
    return f'<article class="guia{" g2" if i == 0 else ""} sube" id="g{i}" data-t="{tm}"><div class="portada c{i}" aria-hidden="true">{ilus(GIMG[i], "foto-g") or f"<svg viewBox=\"0 0 200 200\">{MOT[i]}</svg>"}<b>{pal}</b><span>Guía FBE</span></div><div class="g-txt"><p class="temas-g">{"".join(f"<span class=\"tm-{x}\">{TEMA[x]}</span>" for x in tm.split())}</p><h3>{t}</h3><p>{CORTA[i]}</p><details class="dentro"><summary>Qué hay dentro</summary><ul>{"".join(f"<li>{x}</li>" for x in DENTRO[i])}</ul></details><p class="para"><b>Para:</b> {p}</p><a class="btn" href="https://checkout.mailerlite.com/checkout/{c}">Descargar <span>{e} €</span></a></div></article>'
LDG = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Product', 'name': g[0], 'description': g[1], 'brand': 'Fuerza Basada en Evidencia', **({'image': WEB + 'img/' + GIMG[i] + '.webp'} if os.path.exists(f'web-img/{GIMG[i]}.webp') else {}), 'offers': {'@type': 'Offer', 'price': g[3].replace(',', '.'), 'priceCurrency': 'EUR', 'availability': 'https://schema.org/InStock', 'url': 'https://checkout.mailerlite.com/checkout/' + g[4]}}} for i, g in enumerate(G)]}, ensure_ascii=False) + '</script>'
JS_G = '''<script>(function(){var D=document,g=D.getElementById('filtro'),n=D.getElementById('cuantas');if(!g)return;g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.t,c=0;[].forEach.call(D.querySelectorAll('.guia'),function(a){var s=!t||(' '+a.dataset.t+' ').indexOf(' '+t+' ')>=0;a.hidden=!s;if(s){c++;a.classList.add('ya')}});n.textContent=c+(c===1?' guía':' guías')});var em=D.getElementById('emp');em.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;g.querySelector('[data-t=""]').click();[].forEach.call(D.querySelectorAll('.guia'),function(a){a.classList.remove('senal')});var a=D.getElementById('g'+b.dataset.g);a.classList.add('senal','ya');D.getElementById('emp-t').textContent='Empieza por: '+a.querySelector('h3').textContent+'.';a.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})})();</script>'''
pagina('guias.html', 'Guías', 'Guías prácticas y descargables sobre entrenamiento, fuerza y nutrición con respaldo científico.', 'Ciencia útil, lista para descargar.', 'Nueve guías prácticas sobre entrenamiento, fuerza y nutrición, con respaldo científico y pensadas para aplicarlas.', '<section><div class="in"><div class="empieza sube"><div><h2>¿Por cuál empiezo?</h2><p id="emp-t" role="status">Dime qué buscas y te señalo una.</p></div><div class="fases claras" id="emp" role="group" aria-label="Qué buscas"><button type="button" data-g="0">Tengo guardias o turnos</button><button type="button" data-g="1">Perder grasa</button><button type="button" data-g="4">Ganar músculo</button><button type="button" data-g="2">Tengo poco tiempo</button><button type="button" data-g="5">Cuidar mi salud</button></div></div><div class="barra-f sube"><div class="fases claras" id="filtro" role="group" aria-label="Filtrar por tema"><button type="button" data-t="" aria-pressed="true">Todas</button><button type="button" data-t="entreno" aria-pressed="false">Entrenamiento</button><button type="button" data-t="nutri" aria-pressed="false">Nutrición</button><button type="button" data-t="salud" aria-pressed="false">Salud</button></div><span id="cuantas" role="status">9 guías</span></div><div class="guias">' + ''.join(guia(i, g) for i, g in enumerate(G)) + f'</div><div class="calc sube" style="margin-top:3rem"><div><h3>Gratis: calculadora de proteína</h3><p>Tu rango diario según tu peso y tu fase, con reparto por comidas.</p></div><div><a class="btn claro" href="{CALC}">Abrir la calculadora</a></div></div></div></section>' + JS_G + LDG, datos(('9', 'guías'), ('5,99 €', 'la mayoría'), ('3', 'temas: entrenar, comer y salud')), ('¿Quieres que lo aplique contigo?', 'Las guías explican el porqué. En la asesoría lo llevo a tu semana.'))

# ===== newsletter =====
PLAYA = ilus('foto-playa', 'foto-p').replace('alt=""', 'alt="Pelayo en la playa"')
if PLAYA: PLAYA = f'<figure class="autor-foto">{PLAYA}<figcaption><b>Quién te escribe</b>Pelayo, fuera del hospital y del gimnasio.</figcaption></figure>'
# «Lo ultimo que he enviado» (Boletin): los tres envios mas recientes de boletin.json (23/11/2026; antes, tres fijos).
# Imagen: web-img/boletin-<fecha>.webp si existe; si no, la ilustracion de su tema (BOL_IMG); si no hay, sin imagen.
BOL_IMG = {'2026-11-22': 'herr-tension', '2026-11-15': 'herr-dolor', '2026-11-08': 'revision-2'}
_ULT = sorted(json.load(open('boletin.json', encoding='utf-8')), key=lambda b: b['f'], reverse=True)[:3]
_MESC = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
def _ult_card(b):
    img = ilus(f"boletin-{b['f']}", 'foto-b') or (ilus(BOL_IMG[b['f']], 'foto-b') if b['f'] in BOL_IMG else '')
    y, m, dd = b['f'].split('-')
    return (f'<article class="correo sube">{img}<p class="de"><span class="cara peq">PF</span><span><b>Pelayo, de FBE</b>'
            f'<small>{int(dd)} {_MESC[int(m) - 1]} {y} · Asunto</small></span></p><h3>{b["asunto"]}</h3><p>{b["tema"]}</p>'
            f'<p class="leer"><a href="{b["u"]}" target="_blank" rel="noopener">Leer el correo</a></p></article>')
pagina('newsletter.html', 'Boletín', 'El boletín semanal de Fuerza Basada en Evidencia: entrenamiento, nutrición y salud, sin mitos.', 'Lo que sí funciona. Cada semana, en tu correo.', 'Entrenamiento, nutrición y salud con base científica. Sin mitos y sin adornos, para entrenar mejor, comer con cabeza y vivir con energía.', f'''
<section><div class="in dos alta">
  <div class="sube" id="alta"><div class="entrada" style="margin-bottom:1.5rem"><h2>Apúntate</h2><p>Un correo a la semana. Te das de baja cuando quieras.</p></div>
    <div class="ml-caja"><div class="ml-embedded" data-form="IpOp9n"></div><noscript>Activa JavaScript para ver el formulario.</noscript><p style="margin-top:.8rem;font-size:.92rem;color:var(--tinta-2)">¿No ves el formulario? <a href="https://preview.mailerlite.io/forms/1626427/204678811842774100/share">Ábrelo en otra pestaña</a>.</p></div><p style="margin-top:1rem;font-size:.92rem;color:var(--tinta-2)">Uso tu correo solo para enviarte el boletín. <a href="{PRIV}">Política de privacidad</a>.</p></div>
  <div class="sube"><h3 style="margin-bottom:1.2rem">Qué te llega</h3><ul class="marcas" style="font-size:1.08rem;gap:.9rem"><li><strong>Una idea por correo</strong>, para aplicarla esa semana.</li><li><strong>Lo que me pasa a mí</strong>: lo que pruebo, lo que mido y en qué me equivoco.</li><li><strong>La evidencia detrás</strong>, sin tecnicismos de más.</li></ul>{PLAYA}</div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Lo último que he enviado</h2></div>
  <div class="boletin">{''.join(_ult_card(b) for b in _ULT)}</div>
</div></section>
<script>(function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[]).push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');ml('account','1626427');</script>''', f'<div class="cta"><a class="btn claro" href="#alta">Suscribirme</a></div>')

# ===== dudas =====
D = [('Cómo funciona', [('¿En qué consiste el servicio?', 'Planes de entrenamiento y nutrición a medida que se llevan desde la app, con contacto directo conmigo, corrección de tu técnica en vídeo, check-ins semanales y guías para entender lo que haces. Antes de empezar hacemos una videollamada gratuita.'), ('¿Puedo contratar solo una parte?', 'El entrenamiento se puede contratar solo. La nutrición por separado es poco habitual (individualizamos caso a caso).'), ('¿Qué formación tiene Pelayo?', f'Especialista en Medicina Interna (médico colegiado n.º {COLEGIADO} en Madrid), experto universitario en entrenamiento de fuerza y, en nutrición clínica, máster y experto universitario. Toda su trayectoria está en Quién soy.')]),
 ('Entrenamiento', [('¿Cuántos días a la semana debo entrenar?', 'Depende de tu disponibilidad, tu nivel y tu objetivo. La mayoría de mis atletas entrena entre 2 y 5 días.'), ('¿Por qué no hago siempre los mismos ejercicios?', 'Se cambian con criterio, cada 12 a 16-20 semanas o cuando dejan de darte resultado.'), ('¿Por qué repito algunos ejercicios varias semanas?', 'Porque mantenerlos permite progresar en carga y medir de forma objetiva si avanzas.'), ('¿Hay que llegar al fallo en cada serie?', 'No. Lo habitual es parar entre 1 y 3 repeticiones antes del fallo.'), ('¿Tengo que calentar siempre?', 'Sí, pero poco: algo de movilidad y series progresivas del primer ejercicio.'), ('¿Y si un día no puedo completar el entrenamiento?', 'Se mueve, se acorta o se salta. La constancia importa más que una sesión suelta.')]),
 ('Nutrición', [('¿Debo seguir un menú fijo?', 'No. Prefiero pautas flexibles y hábitos, porque son los que se sostienen.'), ('¿Qué suplementos debería tomar?', 'Para la mayoría: cafeína en dosis controladas, proteína en polvo si no llegas con la comida y creatina monohidrato. El resto, caso a caso.'), ('¿Cómo cuento las calorías si como fuera?', 'Con estimaciones visuales y estrategias de ración. La app te da además una pauta para cuadrar el día.'), ('¿Qué como en una guardia, un turno de noche o un viaje?', 'Comidas planificadas, tentempiés ricos en proteína, alimentos que aguanten sin nevera y cafeína bien colocada.'), ('¿Debo pesarme todos los días?', 'No. El peso es una herramienta más, junto con las fotos, la fuerza, las medidas y cómo te encuentras.')]),
 ('Motivación', [('¿Y si no tengo ganas de entrenar?', 'Empieza por el calentamiento, o baja el volumen o la intensidad ese día. El hábito gana a la motivación.'), ('¿Y si no veo resultados rápido?', 'Los resultados piden tiempo y constancia. Trabajamos con expectativas realistas y con el foco en el proceso.')]),
 ('Soporte y cambios', [('¿Cómo me comunico contigo?', 'Por la app, con respuesta en 48-72 horas como máximo.'), ('¿Cada cuánto revisas mi progreso?', 'Cada semana, en los tres programas.'), ('¿Qué hago si me lesiono o me duele algo?', 'Me lo dices cuanto antes y ajusto el plan. Si el dolor es agudo o no cede, te derivo a quien deba verlo.'), ('¿Puedo cambiar el orden de los ejercicios o el día?', 'Sí, dentro de un margen. Un cambio puntual no es problema; si se repite, lo revisamos juntos.'), ('¿Cómo sé si progreso?', 'Por las cargas, las repeticiones, la técnica, la recuperación, cómo te notas y tus medidas.')])]
import unicodedata
def slug(t): return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFD', t.lower()).encode('ascii', 'ignore').decode()).strip('-')
MAS = {'Cómo funciona': ('programas.html', 'Ver los programas'), 'Entrenamiento': ('guias.html', 'Rutinas y progresión, en las guías'), 'Nutrición': ('CALC', 'Calcula tu proteína diaria'), 'Motivación': ('newsletter.html', 'Una idea cada semana, en el boletín')}
def mas(t):
    if t not in MAS: return ''
    u, x = MAS[t]; return f'<p class="mas-d"><a href="{CALC if u == "CALC" else u}">{x}</a></p>'
NQ = sum(len(q) for _, q in D)
LDF = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for _, qs in D for q, a in qs]}, ensure_ascii=False) + '</script>'
JS_D = '''<script>(function(){var D=document,b=D.getElementById('busca'),v=D.getElementById('vacio'),n=D.getElementById('halla'),bt=D.getElementById('todas');if(!b)return;function $$(q,r){return [].slice.call((r||D).querySelectorAll(q))}
function nc(s){return s.split('').map(function(c){var x=c.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');return x.length===1?x:c.toLowerCase()}).join('')}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
var T=$$('.lista-d summary, .lista-d details > p');T.forEach(function(e){e._t=e.textContent;e._n=nc(e._t)});
function marca(e,q){if(!q||q.length<2){e.textContent=e._t;return}var h='',i=0,j;while((j=e._n.indexOf(q,i))>=0){h+=esc(e._t.slice(i,j))+'<mark>'+esc(e._t.slice(j,j+q.length))+'</mark>';i=j+q.length}e.innerHTML=h+esc(e._t.slice(i))}
b.addEventListener('input',function(){var q=nc(b.value.trim()),c=0;$$('.grupo-d').forEach(function(t){var k=0;$$('details',t).forEach(function(d){var s=!q||nc(d.querySelector('summary')._t+' '+d.querySelector('p')._t).indexOf(q)>=0;d.hidden=!s;if(s)k++;d.open=!!q&&s&&q.length>2});t.hidden=!k;t.classList.add('ya');c+=k});T.forEach(function(e){marca(e,q)});v.hidden=c>0;n.textContent=q?(c+(c===1?' respuesta':' respuestas')):''});
bt.addEventListener('click',function(){var a=bt.getAttribute('aria-pressed')!=='true';bt.setAttribute('aria-pressed',a);bt.textContent=a?'Cerrar todas':'Abrir todas';$$('.lista-d details').forEach(function(d){d.open=a})});
function ir(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var d=D.getElementById(id);if(d&&d.tagName==='DETAILS'){d.open=true;d.closest('.grupo-d').classList.add('ya');d.scrollIntoView({block:'center'})}}addEventListener('hashchange',ir);ir();
if('IntersectionObserver' in window){var L=$$('.indice a'),o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)L.forEach(function(a){if(a.getAttribute('href')==='#'+e.target.id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')})})},{rootMargin:'-30% 0px -60% 0px'});$$('.grupo-d').forEach(function(g){o.observe(g)})}})();</script>'''
pagina('dudas.html', 'Dudas', 'Preguntas frecuentes sobre la asesoría de Fuerza Basada en Evidencia: funcionamiento, entrenamiento, nutrición y soporte.', 'Las dudas de siempre, respondidas.', 'Si la tuya no está, escríbeme y te contesto yo.', '<section><div class="in dudas"><nav class="indice sube" aria-label="Temas"><b>Temas</b>' + ''.join(f'<a href="#t{i}">{t}<span>{len(qs)}</span></a>' for i, (t, qs) in enumerate(D)) + '</nav><div class="lista-d"><div class="busca sube"><label for="busca">Busca en las ' + str(NQ) + ' respuestas</label><span class="lupa"><input id="busca" type="search" placeholder="Por ejemplo: guardia, creatina, fallo" autocomplete="off"></span><div class="busca-pie"><span id="halla" role="status"></span><button class="btn peq hueco" id="todas" type="button" aria-pressed="false">Abrir todas</button></div></div>' + ''.join(f'<div class="grupo-d sube" id="t{i}"><h2>{t}</h2><div class="faq">' + ''.join(f'<details id="{slug(q)}"><summary>{q}</summary><p>{a}</p><a class="ancla" href="#{slug(q)}">Enlace a esta respuesta</a></details>' for q, a in qs) + '</div>' + mas(t) + '</div>' for i, (t, qs) in enumerate(D)) + f'<p id="vacio" hidden>No hay ninguna respuesta con esas palabras. Prueba con otra o escríbeme.</p><div class="llama sube" style="margin-top:0"><b>¿No está tu pregunta?</b><a class="btn" href="{ESCRIBE}">Escribirme</a></div></div></div></section>' + JS_D, datos((str(NQ), 'respuestas'), (str(len(D)), 'temas')), extra=LDF)

# ===== publicar: icono, 404, mapa =====
N404_JS = r"""(function(){var D=document,L=D.getElementById('n4-lista'),S=D.getElementById('n4-sug'),q=D.getElementById('n4-q'),f=D.getElementById('n4-f');
function norm(t){return String(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var p=norm(decodeURIComponent(location.pathname)).replace(/^\/fbe-web\//,'/').replace(/\.(html?|php|aspx?)$/,'');
var NO={'www':1,'html':1,'index':1,'fbe':1,'web':1,'com':1,'pagina':1,'page':1,'the':1,'los':1,'las':1,'del':1,'para':1,'con':1};
var ws=p.split(/[^a-z0-9]+/).filter(function(w){return w.length>2&&!NO[w]});
q.value=ws.join(' ');
f.addEventListener('submit',function(e){e.preventDefault();if(window.fbeBusca)window.fbeBusca(q.value);});
if(!ws.length)return;
fetch('buscar.json').then(function(r){return r.json()}).then(function(ix){
  var PRI={'Herramienta':0,'Página':1,'Glosario':2,'Duda':3,'Mito':4,'Guía':5,'Empieza aquí':6,'Fuente':7,'Boletín':8};
  var res=ix.map(function(e){var t=norm(e.t),k=norm(e.k+' '+e.d+' '+e.u),s=0;ws.forEach(function(w){var w4=w.slice(0,Math.max(4,w.length-2));if(t.indexOf(w)>=0)s+=6;else if(t.indexOf(w4)>=0)s+=4;else if(k.indexOf(w)>=0)s+=2;else if(k.indexOf(w4)>=0)s+=1});return s?{e:e,s:s-(PRI[e.y]||0)*.25}:null}).filter(Boolean).sort(function(a,b){return b.s-a.s}).slice(0,6);
  if(!res.length)return;
  L.innerHTML=res.map(function(x){var e=x.e;return '<li><a class="n4-r" href="'+esc(e.u)+'"'+(e.x?' target="_blank" rel="noopener"':'')+'><small>'+esc(e.y)+'</small><b>'+esc(e.t)+'</b>'+(e.d?'<span>'+esc(e.d.length>120?e.d.slice(0,118)+'…':e.d)+'</span>':'')+'</a></li>'}).join('');
  S.hidden=false;
}).catch(function(){});})();"""

open(f'{SAL}/favicon.svg', 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 1254"><rect width="1254" height="1254" rx="280" fill="#593EDE"/><g transform="translate(627 627) scale(.82) translate(-627 -628)"><path fill="#fff" fill-rule="evenodd" d="{LD}"/></g></svg>')
open(f'{SAL}/404.html', 'w', encoding='utf-8').write(f'''{cabeza('404.html', 'Página no encontrada', 'Esta página no existe.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-404" id="inicio">{ANILLOS}{ilus("web-404")}<div class="in"><div class="txt"><p class="num404" aria-hidden="true">404</p><h1>Aquí no hay nada.</h1><p class="sub">La página que buscas no existe o ha cambiado de sitio. Estas sí están:</p><div class="cta"><a class="btn claro" href="index.html">Ir al inicio</a><a class="enl" href="programas.html">Programas</a><a class="enl" href="guias.html">Guías</a><a class="enl" href="dudas.html">Dudas</a></div></div></div></header>
<main id="contenido">
<section class="n4-s" id="n4-sug" hidden aria-labelledby="n4-h"><div class="in"><div class="entrada"><h2 id="n4-h">¿Buscabas esto?</h2><p id="n4-p">Por la dirección que has escrito, puede que sea una de estas páginas.</p></div>
  <ul class="n4-lista" id="n4-lista"></ul>
</div></section>
<section class="n4-s"><div class="in">
  <form class="n4-busca" id="n4-f" role="search"><label for="n4-q">Busca en toda la web</label><span class="lupa glos-busca hb-busca"><input id="n4-q" type="search" placeholder="Por ejemplo: creatina, rodilla, 1RM" autocomplete="off"></span><button class="btn" type="submit"><span>Buscar</span></button></form>
  <h2 class="n4-t">O empieza por aquí</h2>
  <div class="n4-rej">{"".join(f'<a class="n4-a" href="{u}"><b>{t}</b><span>{d}</span></a>' for u, t, d in [('empieza-aqui.html', 'Empieza aquí', 'Tu ruta según tu caso'), ('herramientas.html', 'Herramientas', 'Calculadoras y tests gratuitos'), ('mitos.html', 'Mitos y evidencia', 'Qué dicen los estudios'), ('guias.html', 'Guías', 'Para descargar y aplicar'), ('programas.html', 'Programas', 'Entrena con un plan'), ('dudas.html', 'Dudas', 'Preguntas frecuentes')])}</div>
  <p class="sec-enl n4-temas"><b>Por tema</b>{"".join(f'<a href="{u}">{t}</a>' for u, t in TEMAS_MENU)}</p>
</div></section>
</main>
{PIE}
<script src="fbe.js"></script>
<script>{N404_JS}</script></body></html>''')
# La 404 se sirve en cualquier dirección: si la dirección tiene subcarpetas, una <base> para que carguen el estilo y los enlaces (en la de pruebas, bajo /fbe-web/)
_n4 = open(f'{SAL}/404.html', encoding='utf-8').read()
open(f'{SAL}/404.html', 'w', encoding='utf-8').write(_n4.replace('<meta charset="utf-8">', '<meta charset="utf-8"><script>(function(){var p=location.pathname,r=p.indexOf("/fbe-web/")===0?"/fbe-web/":"/";if(p.slice(r.length).indexOf("/")>=0)document.write(\'<base href="\'+r+\'">\')})();</script>', 1))
# Tandas 12-14 (20/11/2026): sello de las paginas de gracias, tarjetas de «Mientras tanto» y pasos de «Cómo sigue»
SELLO = '<span class="sello" aria-hidden="true"><svg viewBox="0 0 52 52"><circle cx="26" cy="26" r="23"/><path d="M15.5 27.5l7 7 14-15"/></svg></span>'
def tarj_sigue(href, img, titulo):
    _i = ilus(img, 'tarj-img') or f'<span class="tarj-img vacia">{LOBO}</span>'
    return f'<a class="tarj-s" href="{href}">{_i}<span class="tarj-t"><b>{titulo}</b></span></a>'
PASITOS_G = '<ol class="pasitos{x}"><li>Ya me has contado tu caso.</li><li>Te respondo yo.</li><li>Antes de empezar hacemos una videollamada gratuita.</li></ol>'  # en gracias-plaza
PASITOS = '<ol class="pasitos{x}"><li>Me cuentas tu caso en este formulario.</li><li>Te respondo yo.</li><li>Antes de empezar hacemos una videollamada gratuita.</li></ol>'
# Gracias de la Puesta a punto: a /gracias vuelve Stripe tras el pago (copiada de su web vieja el 20/11/2026; su Gmail cambiado por el correo publico). Siempre noindex.
_TALLY = 'https://tally.so/r/J94Voz'; _CAL = 'https://calendly.com/pelayoplcoaching/puesta-a-punto-videollamada'
_CC = _ent(os.environ.get('FBE_CORREO', '')); _CCM = f'<a href="mailto:{_CC}">{_CC}</a>' if _CC else 'el formulario de contacto'
open(f'{SAL}/gracias.html', 'w', encoding='utf-8').write(f"""{cabeza('gracias.html', 'Gracias · Puesta a punto', 'Pago recibido: los dos pasos que quedan para tu Puesta a punto.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-puesta-a-punto" id="inicio">{ANILLOS}{ilus("web-gracias") or ilus("web-puesta-a-punto")}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / <a href="puesta-a-punto.html">Puesta a punto</a> / Gracias</span>{SELLO}<h1>Pago recibido.</h1><p class="sub">Tu Puesta a punto ya está en marcha. En unos minutos te llega el recibo de Stripe por correo.</p></div></div></header>
<main id="contenido">
<section><div class="in"><div class="entrada sube"><h2>Quedan dos pasos, y el orden importa</h2><p>Para que yo pueda revisar tu caso antes de que hablemos: primero el cuestionario, después la cita. Reserva la cita solo cuando hayas enviado el cuestionario con tu analítica. Si reservas antes, no podré preparar la consulta.</p></div>
  <ol class="pasos-g dos-pasos con-iconos sube">
    <li><em class="orden">Primero</em><b>Rellena el cuestionario y sube tu analítica</b><span>Historial médico, cómo entrenas, cómo comes y tu analítica de los últimos 12 meses en PDF. Es largo a propósito: es lo que me permite darte un plan que no sea genérico. Hazlo de una vez, con calma.</span><small>20–30 min · canal seguro</small><a class="btn" href="{_TALLY}">Abrir el cuestionario</a></li>
    <li><em class="orden">Después</em><b>Reserva tu videollamada de 30 minutos</b><span>Elige el hueco que mejor te venga. La agenda solo deja reservar con al menos 5 días de antelación: es el tiempo que necesito para leer tu analítica y tu historial antes de vernos.</span><small>30 min · Google Meet</small><a class="btn hueco" href="{_CAL}">Reservar la cita</a></li>
  </ol>
</div></section>
<section class="hoja"><div class="in dos">
  <div class="sube"><h3 style="margin-bottom:.8rem">¿Todavía no tienes analítica?</h3><p>Rellena igualmente el cuestionario (puedes dejar el archivo sin subir) y pide a tu médico o a un laboratorio:</p><ul class="chips analitica" style="margin:1rem 0"><li>Hemograma</li><li>Ferritina</li><li>Glucosa y HbA1c</li><li>Perfil lipídico</li><li>TSH</li><li>Vitamina D</li><li>Creatinina</li><li>Transaminasas</li><li>B12 y folato</li></ul><p>Cuando tengas los resultados, me los mandas por un formulario seguro y reservas la cita.</p></div>
  <div class="sube"><h3 style="margin-bottom:.8rem">Qué pasa después</h3><ul class="marcas linea-t"><li>Antes de la cita reviso tu analítica y tu historial. La llamada la dedicamos a lo que los datos no cuentan.</li><li>En menos de 7 días desde la consulta recibes tu plan de 12 semanas de entrenamiento y nutrición en PDF.</li><li>Tienes 7 días desde la entrega para mandarme un único correo con todas tus dudas. Respondo en 48–72 h.</li><li>La videollamada se transcribe para redactar tu plan con precisión; te lo confirmo al empezar la llamada.</li></ul>
  <p class="nota-g">Si necesitas cambiar la cita, hazlo desde el enlace del correo de confirmación de Calendly. Para cualquier otra cosa, escríbeme a {_CCM}. Tus datos se tratan según la <a href="{PRIV}">política de privacidad</a>.</p></div>
</div></section>
</main>
{PIE}
<script src="fbe.js"></script></body></html>""")
# Direcciones de la web vieja de MailerLite que cambian de nombre: paginas que redirigen al momento (/programas y /puesta-a-punto ya coinciden)
for _vieja, _nueva in [('faq', 'dudas.html'), ('newsletter-semanal', 'newsletter.html'), ('programas-copy', 'guias.html'), ('quien_soy', 'quien-soy.html')]:
    open(f'{SAL}/{_vieja}.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Fuerza Basada en Evidencia</title><link rel="canonical" href="{WEB}{_nueva}"><meta http-equiv="refresh" content="0; url={_nueva}"><script>location.replace("{_nueva}" + location.search + location.hash)</script></head><body><p><a href="{_nueva}">Esta página ha cambiado de sitio. Sigue aquí.</a></p></body></html>')
# Direcciones cortas para los QR y para decir en los vídeos (24/11/2026): /nivel, /dosdias, /navidad (vídeo del 13/12/2026, añadida el 25/11) y /semanas (vídeo del 3/1/2027) llevan a su landing con la marca de origen (utm) para el contador de visitas.
CORTAS = {'nivel': ('guia-fuerza-segun-nivel/', 'fuerza-segun-nivel'), 'dosdias': ('guia-dos-dias/', 'dos-dias'), 'navidad': ('guia-plan-navidad/', 'plan-navidad'), 'semanas': ('guia-primeras-semanas/', 'primeras-semanas')}
for _c, (_dest, _camp) in CORTAS.items():
    _u = f'{_dest}?utm_source=youtube&amp;utm_medium=qr&amp;utm_campaign={_camp}'
    open(f'{SAL}/{_c}.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Fuerza Basada en Evidencia</title><link rel="canonical" href="{WEB}{_dest}"><meta http-equiv="refresh" content="0; url={_u}"><script>location.replace("{_u.replace("&amp;", "&")}")</script></head><body><p><a href="{_u}">Ir a la guía</a></p></body></html>')
# Gracias del boletin: a esta pagina redirige el formulario de MailerLite «Boletín · Newsletter (web)». Siempre noindex y fuera del sitemap.
open(f'{SAL}/gracias-boletin.html', 'w', encoding='utf-8').write(f"""{cabeza('gracias-boletin.html', 'Ya estás dentro', 'Gracias por apuntarte al boletín de Fuerza Basada en Evidencia.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-newsletter" id="inicio">{ANILLOS}{ilus("web-gracias-boletin") or ilus("web-newsletter")}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / <a href="newsletter.html">Boletín</a> / Gracias</span>{SELLO}<h1>Ya estás dentro.</h1><p class="sub">Gracias por apuntarte. En unos minutos te llega mi correo de bienvenida.</p></div></div></header>
<main id="contenido">
<section><div class="in"><div class="entrada sube"><h2>Para que no se pierda</h2></div>
  <ol class="pasos-g en-linea sube">
    <li><b>Mira tu bandeja de entrada</b><span>Si no está, busca en Promociones o en Spam y márcalo como «No es spam».</span></li>
    <li><b>Guárdame en tus contactos</b><span>Así los siguientes correos llegan siempre a la bandeja principal.</span></li>
    <li><b>Contesta si quieres</b><span>Leo las respuestas. Si hay un tema que te interesa, cuéntamelo.</span></li>
  </ol>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Mientras tanto</h2></div>
  <div class="tarj-g sube">{tarj_sigue("guias.html", "web-guias", "Ver las guías")}{tarj_sigue(CALC, "web-calculadora", "Calculadora de proteína")}{tarj_sigue("quien-soy.html", "foto-pelayo", "Quién soy")}</div>
</div></section>
</main>
{PIE}
<script src="fbe.js"></script></body></html>""")
# Formulario propio «Pedir plaza» (20/11/2026): mismas preguntas que el de NoteForms y mismas opciones que las columnas de la base
# de Notion «Leads – Nuevos contactos». Se envia a PLAZA_ENVIO (funcion de Netlify, fuente/formularios/) como formulario normal;
# la funcion vuelve a gracias-plaza.html o a pedir-plaza.html?error=1|2. Las dos paginas, noindex y fuera del sitemap.
AGUA = f'<div class="marca-agua">{LOBO}</div>'  # cabecera sin ilustracion: el lobo de fondo
OBJ_P = ['Hipertrofia', 'Fuerza', 'Pérdida de grasa corporal', 'Recomposición Corporal', 'Salud general', 'Prevención de lesiones/Rehabilitación']
CON_P = ['Instagram', 'Referido', 'YouTube', 'Web', 'Otro']
# Lo que se ve en pantalla cuando no coincide con la opcion de Notion (el valor que se envia sigue siendo el de Notion)
ETQ_P = {'Recomposición Corporal': 'Recomposición corporal', 'Prevención de lesiones/Rehabilitación': 'Prevención de lesiones/rehabilitación', 'Referido': 'Recomendación'}
ICO_P = {'Hipertrofia': 'sube', 'Fuerza': 'pesa', 'Pérdida de grasa corporal': 'llama', 'Recomposición Corporal': 'balanza', 'Salud general': 'corazon', 'Prevención de lesiones/Rehabilitación': 'escudo', 'Instagram': 'camara', 'Referido': 'persona', 'YouTube': 'video', 'Web': 'globo', 'Otro': 'puntos'}
def chip_p(nombre, tipo, v): return f'<label data-i="{ICO_P.get(v, "")}"><input type="{tipo}" name="{nombre}" value="{v}"><span>{ETQ_P.get(v, v).replace("/", "/<wbr>")}</span></label>'
CORREO_P = (_ent(os.environ['FBE_CORREO'])) if os.environ.get('FBE_CORREO') else ''
FORM_P = f"""<form class="formu sube" id="plaza" action="{PLAZA_ENVIO}" method="post" accept-charset="utf-8">
  <div class="aviso-f" id="aviso" role="alert" hidden></div>
  <div class="progreso-f" aria-hidden="true"><span class="progreso-barra"><i id="f-barra"></i></span><span class="progreso-txt"><b id="f-listos">0</b> de 4 listos</span></div>
  <p class="bloque-f"><b>/01</b> Tus datos</p>
  <div class="campo"><label for="f-nombre">Nombre y apellidos<span class="oblig" aria-hidden="true">*</span></label><input class="ic ic-nombre" type="text" id="f-nombre" name="nombre" autocomplete="name" autocapitalize="words" enterkeyhint="next" maxlength="200" required><small class="ayuda-f">Escribe tu nombre y apellidos.</small></div>
  <div class="fila-f">
    <div class="campo"><label for="f-correo">Correo electrónico<span class="oblig" aria-hidden="true">*</span></label><input class="ic ic-correo" type="email" id="f-correo" name="correo" autocomplete="email" enterkeyhint="next" placeholder="tu@correo.com" maxlength="200" required><small class="ayuda-f">Revisa el correo: parece que falta algo.</small></div>
    <div class="campo"><label for="f-tel">Teléfono de contacto<span class="oblig" aria-hidden="true">*</span></label><input class="ic ic-tel" type="tel" id="f-tel" name="telefono" autocomplete="tel" inputmode="tel" enterkeyhint="next" placeholder="+34 600 000 000" maxlength="40" pattern="[+\\(\\)0-9 .\\-]{{6,}}" required><small class="ayuda-f">Revisa el teléfono: al menos 6 cifras.</small></div>
  </div>
  <p class="bloque-f"><b>/02</b> Qué buscas</p>
  <fieldset class="campo"><legend>Objetivos<small>puedes marcar varios</small></legend><div class="chips-f tarj">{"".join(chip_p("objetivos", "checkbox", o) for o in OBJ_P)}</div></fieldset>
  <fieldset class="campo"><legend>¿Cómo me has conocido?</legend><div class="chips-f uno">{"".join(chip_p("conocido", "radio", o) for o in CON_P)}</div></fieldset>
  <p class="bloque-f"><b>/03</b> Algo más</p>
  <div class="campo"><label for="f-nota">Gracias por llegar hasta el final. ¿Hay algo más que deba saber?</label><textarea id="f-nota" name="nota" rows="4" maxlength="1900"></textarea><small class="cuenta-f"><span id="f-cuenta">0</span> / 1.900</small></div>
  <div class="trampa" aria-hidden="true"><label>No rellenes este campo<input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="t0" id="f-t0" value="">
  <label class="acepta"><input type="checkbox" name="privacidad" value="si" required><span>He leído la <a href="privacidad.html">política de privacidad</a> y acepto que uses estos datos para responder a mi solicitud.<span class="oblig" aria-hidden="true">*</span></span></label>
  <div class="envio-f"><button class="btn grande" type="submit" id="f-enviar">Enviar</button><small><span class="oblig" aria-hidden="true">*</span> Obligatorio</small></div>
</form>"""
LADO_P = f"""<aside class="plaza-lado sube">
  <div class="tarjeta-p"><img class="foto-p" src="{FOTO}" alt="Pelayo Fernández Cidón" width="160" height="200" loading="lazy"><p><b>Pelayo Fernández Cidón</b> Médico internista y prescriptor de ejercicio físico.</p></div>
  <div class="tarjeta-p como-sigue"><p class="etq-p">Cómo sigue</p>{PASITOS.format(x="")}</div>
  <div class="tarjeta-p"><p><b>¿Dudas antes de pedir plaza?</b></p><p><a href="programas.html">Ver los programas</a> · <a href="dudas.html">Dudas frecuentes</a>{f' · <a href="mailto:{CORREO_P}">Escribirme</a>' if CORREO_P else ''}</p></div>
</aside>"""
JS_P = """<script>(function(){
var f = document.getElementById('plaza'); if (!f) return;
var t0 = document.getElementById('f-t0'), av = document.getElementById('aviso'), bt = document.getElementById('f-enviar'), K = 'fbe-plaza';
t0.value = Date.now();
var err = (location.search.match(/error=(\\d)/) || [])[1];
function caja(){ try { return window.sessionStorage; } catch (e) { return null; } }
if (err) {
  var c = caja(), d = null; try { d = JSON.parse(c && c.getItem(K) || 'null'); } catch (e) {}
  if (d) [].forEach.call(f.elements, function(el){ if (!el.name || el.name === 't0' || el.name === 'web') return; if (el.type === 'checkbox' || el.type === 'radio') el.checked = (d[el.name] || []).indexOf(el.value) > -1; else if (d[el.name]) el.value = d[el.name][0]; });
  av.textContent = err === '2' ? 'No he podido guardar tu solicitud por un fallo técnico. Prueba otra vez en un momento' + (f.dataset.correo ? ' o escríbeme a ' + f.dataset.correo + '.' : '.') : 'Revisa el formulario: falta algún dato obligatorio o hay uno que no cuadra.';
  av.hidden = false; av.scrollIntoView({ block: 'center' });
}
f.addEventListener('submit', function(){
  var d = {}; [].forEach.call(f.elements, function(el){ if (!el.name || el.name === 't0' || el.name === 'web' || el.name === 'privacidad') return; if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return; (d[el.name] = d[el.name] || []).push(el.value); });
  var c = caja(); try { c && c.setItem(K, JSON.stringify(d)); } catch (e) {}
  bt.disabled = true; bt.textContent = 'Enviando…';
});
window.addEventListener('pageshow', function(e){ if (e.persisted) { bt.disabled = false; bt.textContent = 'Enviar'; t0.value = Date.now() - 5000; } });
})();</script>"""
JS_P2 = """<script>(function(){
var f = document.getElementById('plaza'); if (!f) return;
var req = [f.nombre, f.correo, f.telefono, f.privacidad], barra = document.getElementById('f-barra'), listos = document.getElementById('f-listos');
function prog(){ var n = 0; req.forEach(function(el){ if (el.type === 'checkbox' ? el.checked : (el.value.trim() && el.checkValidity())) n++; }); listos.textContent = n; barra.style.width = (n * 25) + '%'; f.classList.toggle('completo', n === 4); }
var nota = f.nota, cuenta = document.getElementById('f-cuenta');
function crece(){ cuenta.textContent = String(nota.value.length).replace(/\B(?=(\d{3})+$)/g, '.'); nota.style.height = 'auto'; nota.style.height = Math.min(nota.scrollHeight + 2, 420) + 'px'; }
f.addEventListener('input', prog); f.addEventListener('change', prog); nota.addEventListener('input', crece);
prog(); crece();
if (/error=1/.test(location.search)) { for (var i = 0; i < req.length; i++) { if (!(req[i].type === 'checkbox' ? req[i].checked : (req[i].value.trim() && req[i].checkValidity()))) { req[i].focus({ preventScroll: true }); break; } } }
})();</script>"""
_correo_vis = os.environ.get('FBE_CORREO', '')
open(f'{SAL}/pedir-plaza.html', 'w', encoding='utf-8').write(f"""{cabeza('pedir-plaza.html', 'Pedir plaza', 'Formulario de contacto inicial de FBE Coaching Online: cuéntame tu caso y te respondo yo.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-pedir-plaza" id="inicio">{ANILLOS}{ilus("web-pedir-plaza") or AGUA}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / Pedir plaza</span><h1>Pedir plaza.</h1><p class="sub">Formulario de contacto inicial de Fuerza Basada en Evidencia. Cuéntame tu caso. Te respondo yo.</p></div></div></header>
<main id="contenido">
<section><div class="in"><div class="plaza-rejilla">
{FORM_P.replace('<form class="formu sube" id="plaza"', '<form class="formu sube" id="plaza" data-correo="' + _ent(_correo_vis) + '"' if _correo_vis else '<form class="formu sube" id="plaza"')}
{LADO_P}
</div></div></section>
</main>
{PIE}
<script src="fbe.js"></script>
{JS_P}{JS_P2}</body></html>""")
open(f'{SAL}/gracias-plaza.html', 'w', encoding='utf-8').write(f"""{cabeza('gracias-plaza.html', 'Recibido', 'Solicitud recibida en FBE Coaching Online.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-pedir-plaza" id="inicio">{ANILLOS}{ilus("web-recibido") or AGUA}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / Pedir plaza / Recibido</span>{SELLO}<h1>Recibido.</h1><p class="sub">Gracias por contarme tu caso. Te respondo yo.</p></div></div></header>
<main id="contenido">
<section><div class="in"><div class="entrada sube"><h2>Cómo sigue</h2></div><div class="caja-s sube">{PASITOS_G.format(x=" hecho1")}</div></div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Mientras tanto</h2></div>
  <div class="tarj-g sube">{tarj_sigue("programas.html", "web-programas", "Ver los programas")}{tarj_sigue("guias.html", "web-guias", "Guías")}{tarj_sigue(CALC, "web-calculadora", "Calculadora de proteína")}</div>
</div></section>
</main>
{PIE}
<script src="fbe.js"></script>
<script>try {{ sessionStorage.removeItem('fbe-plaza'); }} catch (e) {{}}</script></body></html>""")
# Politica de privacidad propia: texto de su pagina de MailerLite (sept. 2026); el 20/11/2026 Pelayo pidio cambiar el alojamiento de la web a GitHub. Solo se genera si hay FBE_CORREO.
if os.environ.get('FBE_CORREO'):
    C = _ent(os.environ['FBE_CORREO']); CM = f'<a href="mailto:{C}">{C}</a>'
    PRIV_TXT = f"""<section><div class="in"><div class="prosa">
<p><strong>Responsable del tratamiento:</strong> Pelayo Fernández Cidón, médico especialista en Medicina Interna, NIF 71777712W, con domicilio a efectos de notificaciones en Fernández de los Ríos 63, 28015, Madrid. Contacto: {CM}.</p>
<p>En Fuerza Basada en Evidencia nos tomamos muy en serio la protección de tus datos. Esta política explica qué información recogemos, con qué finalidad, durante cuánto tiempo la conservamos y qué derechos tienes sobre ella.</p>
<h2>Qué datos tratamos</h2>
<p>Según el servicio que contrates, podemos tratar:</p>
<ul class="marcas"><li><strong>Datos identificativos y de contacto:</strong> nombre, email, teléfono.</li><li><strong>Datos de salud (categoría especial, art. 9 RGPD):</strong> análisis de sangre, historial médico, medicación, lesiones, objetivos de salud e imágenes que nos facilites voluntariamente.</li><li><strong>Datos de facturación y pago</strong>, gestionados a través de proveedores de pago seguros.</li></ul>
<h2>Para qué los usamos</h2>
<ul class="marcas"><li>Revisar tu analítica e historial médico y elaborar tu prescripción personalizada de entrenamiento y nutrición (servicio Puesta a punto).</li><li>Diseñar tu plan y realizar el seguimiento y los ajustes correspondientes (programa de seguimiento).</li><li>Comunicarnos contigo de forma directa en relación con el servicio contratado.</li><li>Procesar pagos y emitir facturas.</li><li>Enviarte comunicaciones por email únicamente si te has suscrito a nuestra lista; puedes darte de baja en cualquier momento desde el propio correo.</li></ul>
<h2>Base legal</h2>
<p>Tratamos tus datos de salud sobre la base de tu consentimiento explícito, que prestas al reservar el servicio marcando la casilla correspondiente. Puedes retirar este consentimiento en cualquier momento, sin que ello afecte a la licitud del tratamiento previo. El resto de datos se tratan para la ejecución del contrato de servicios y el cumplimiento de obligaciones legales (fiscales y sanitarias).</p>
<h2>Cuánto tiempo los conservamos</h2>
<p>Al tratarse de un servicio prestado por un médico, la documentación clínica (analíticas, historial y prescripción) se conserva durante un mínimo de 5 años desde la finalización del servicio, conforme a la Ley 41/2002 de autonomía del paciente. Los datos de facturación se conservan durante los plazos exigidos por la normativa fiscal. El resto de datos se eliminan cuando dejan de ser necesarios o cuando lo solicitas.</p>
<h2>Con quién compartimos tus datos</h2>
<p>No compartimos tus datos con terceros con fines comerciales. Trabajamos únicamente con proveedores tecnológicos que actúan como encargados del tratamiento y cumplen el RGPD (como MailerLite para email, GitHub para alojar esta web, Netlify para recibir el formulario de contacto, Notion para gestionar las solicitudes, Calendly para reservas, Stripe para pagos y Umami para contar visitas). Algunos de estos proveedores pueden alojar datos fuera del Espacio Económico Europeo; en esos casos, el tratamiento se ampara en garantías adecuadas como las cláusulas contractuales tipo aprobadas por la Comisión Europea.</p>
<h2>Estadísticas de visitas</h2>
<p>Para saber cuántas personas visitan cada página y desde dónde llegan, esta web usa Umami, un contador de visitas que no usa cookies ni guarda nada en tu dispositivo. No recoge tu nombre ni tu email, no guarda tu dirección IP (solo la usa para saber el país) y no te sigue de una web a otra. Cuenta las páginas vistas, la web desde la que llegas, el tipo de dispositivo y de navegador, el país y algunos clics, como los de «Pedir plaza». Si tu navegador pide no ser rastreado, no cuenta tu visita. Lo que escribes en las calculadoras no se envía nunca: se queda en tu navegador.</p>
<h2>Tus derechos</h2>
<p>Puedes ejercer en cualquier momento tus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar tu consentimiento, escribiendo a {CM}. También tienes derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es">aepd.es</a>) si consideras que el tratamiento no se ajusta a la normativa.</p>
<h2>Seguridad</h2>
<p>Aplicamos medidas técnicas y organizativas para proteger tu información, incluido el almacenamiento de la documentación clínica en sistemas con acceso restringido.</p>
<p><small>Última actualización: noviembre de 2026.</small></p>
</div></div></section>"""
    import re as _rp, unicodedata as _ud
    def _slug(t): return _rp.sub(r'[^a-z0-9]+', '-', _ud.normalize('NFD', t).encode('ascii', 'ignore').decode().lower()).strip('-')
    _tits = _rp.findall(r'<h2>([^<]+)</h2>', PRIV_TXT)
    for _t in _tits: PRIV_TXT = PRIV_TXT.replace(f'<h2>{_t}</h2>', f'<h2 id="{_slug(_t)}">{_t}<a class="ancla" href="#{_slug(_t)}" aria-label="Enlace a este apartado">#</a></h2>', 1)
    _IND = '<nav class="indice-p" aria-label="En esta página"><p>En esta página</p><ol>' + ''.join(f'<li><a href="#{_slug(_t)}">{_t}</a></li>' for _t in _tits) + '</ol></nav>'
    PRIV_TXT = PRIV_TXT.replace('<section><div class="in"><div class="prosa">', '<section><div class="in priv-rejilla">' + _IND + '<div class="prosa prosa-priv">', 1)
    PRIV_TXT = PRIV_TXT.replace('<p><strong>Responsable del tratamiento:</strong>', '<p class="ficha-resp"><strong>Responsable del tratamiento:</strong>', 1)
    PRIV_TXT = PRIV_TXT.replace(f'Contacto: {CM}.</p>', f'Contacto: {CM}. <button type="button" class="copiar-c" data-c="{C}">Copiar</button></p>', 1)
    PRIV_TXT = PRIV_TXT.replace('<li><strong>Datos de salud', '<li class="ambar"><strong>Datos de salud', 1)
    PRIV_TXT = PRIV_TXT.replace('<p><small>Última actualización', '<p class="act"><small>Última actualización', 1)
    PRIV_TXT = PRIV_TXT.replace('<a href="https://www.aepd.es">', '<a class="fuera" href="https://www.aepd.es" rel="noopener">', 1)
    _JS_PRIV = """<script>(function(){
var b = document.querySelector('.copiar-c'); if (b) b.addEventListener('click', function(){ var t = b.getAttribute('data-c'); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function(){ b.textContent = 'Copiado'; b.classList.add('hecho'); setTimeout(function(){ b.textContent = 'Copiar'; b.classList.remove('hecho'); }, 1800); }).catch(function(){}); });
var links = document.querySelectorAll('.indice-p a'); if (!links.length || !('IntersectionObserver' in window)) return;
var mapa = {}; links.forEach(function(a){ mapa[a.getAttribute('href').slice(1)] = a; });
var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { links.forEach(function(a){ a.classList.remove('aqui'); a.removeAttribute('aria-current'); }); var a = mapa[e.target.id]; if (a) { a.classList.add('aqui'); a.setAttribute('aria-current', 'true'); } } }); }, { rootMargin: '-20% 0px -70% 0px' });
document.querySelectorAll('.prosa-priv h2[id]').forEach(function(h){ io.observe(h); });
})();</script>"""
    open(f'{SAL}/privacidad.html', 'w', encoding='utf-8').write(f"""{cabeza('privacidad.html', 'Política de privacidad', 'Qué datos trata Fuerza Basada en Evidencia, para qué, cuánto tiempo y cómo ejercer tus derechos.')}
{cabecera()}
<header class="hero mini t-privacidad" id="inicio">{ANILLOS}{ilus("web-privacidad") or AGUA}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / Privacidad</span><h1>Política de privacidad</h1><p class="sub">Qué datos trato, para qué, cuánto tiempo los guardo y cómo ejercer tus derechos.</p></div></div></header>
<main id="contenido">{PRIV_TXT}</main>
{PIE}
<script src="fbe.js"></script>{_JS_PRIV}</body></html>""")
# ===== herramientas: calculadora de proteina y Pauta Activa (app de otro repo, medicacion-y-ejercicio) =====
# Textos de Pauta Activa: de su presentacion (app/presentacion.html), pasados a tu. Las capturas (web-img/pa-*.webp) son reales de la app.
def _alt(html, t): return html.replace('alt=""', f'alt="{t}"', 1)
PA_LOGO = ilus('pa-logo', 'pa-logo')
PA_TEL = lambda n, t: f'<figure class="pa-tel">{_alt(ilus("pa-" + n, "pa-cap"), t)}</figure>'
def herr(clase, img, etiqueta, titulo, texto, chips, botones):
    return f'<article class="herr {clase} sube"><div class="herr-img">{img}</div><div class="herr-txt"><p class="herr-et">{etiqueta}</p><h2>{titulo}</h2><p>{texto}</p><ul class="herr-chips">{"".join(f"<li>{c}</li>" for c in chips)}</ul><div class="herr-bot">{botones}</div></div></article>'
CTA_PP = '<section><div class="in"><div class="calc sube"><div><h3>¿Y si además quieres un plan hecho por un médico?</h3><p>La Puesta a punto es una consulta y un plan de 12 semanas, con lectura de tu analítica. Sin lista de espera.</p></div><div><a class="btn claro" href="puesta-a-punto.html">Ver la Puesta a punto</a></div></div></div></section>'
pagina('herramientas.html', 'Herramientas', 'Herramientas gratuitas: Pauta Activa (medicación y ejercicio), calculadora de proteína, test de la silla, 1RM, volumen semanal, cafeína y cribado médico.', 'Herramientas gratuitas', 'Aplicaciones y calculadoras para resolver dudas concretas: qué tener en cuenta al entrenar si tomas medicación, cuánta proteína necesitas, con qué peso trabajar o si te conviene una revisión antes de empezar.', f'''
<section><div class="in herr-lista">
  {herr("pa", _alt(ilus("pa-consulta", "herr-cap"), "Pauta Activa en el ordenador: la medicación a la izquierda y el informe a la derecha"), f"{PA_LOGO}App web · Medicación y Ejercicio", "Pauta Activa", "Lee tu medicación habitual y tu situación clínica y te dice qué tener en cuenta al entrenar: aeróbico, fuerza y equilibrio, interacciones relevantes (también con suplementos y plantas) e informes para ti, tu médico y tu entrenador.", ["388 principios activos", "53 suplementos y plantas", "Sin cuentas", "Funciona sin conexión"], f'<a class="btn" href="pauta-activa.html">Ver qué es</a><a class="enl-h" href="{PA}" rel="noopener">Abrir la app</a>')}
  {herr("calc-h", ilus("web-calculadora", "herr-cap") or f'<span class="herr-vacia">{LOBO}</span>', "Calculadora", "Calculadora de proteína", "Calcula tu objetivo diario de proteína y su reparto por comidas, con rangos basados en metaanálisis revisados.", ["Objetivo diario", "Reparto por comidas", "La guía completa, en tu correo"], f'<a class="btn" href="{CALC}" rel="noopener">Abrir la calculadora</a>')}
  <p class="herr-nota sube">Son herramientas informativas: no diagnostican ni sustituyen a tu médico.</p>
</div></section>
{CTA_PP}''')

PA_LD = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'Pauta Activa', 'alternateName': 'Medicación y Ejercicio', 'url': PA, 'applicationCategory': 'HealthApplication', 'operatingSystem': 'Web', 'inLanguage': ['es', 'en', 'fr', 'pt', 'it'], 'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'}, 'author': {'@type': 'Person', 'name': 'Pelayo Fernández Cidón'}, 'license': 'https://opensource.org/licenses/MIT', 'sameAs': ['https://doi.org/10.5281/zenodo.23423114', 'https://github.com/pelayoplcoaching/medicacion-y-ejercicio']}, ensure_ascii=False) + '</script>'
PA_CIF = [('388', 'principios activos'), ('53', 'suplementos y plantas'), ('781', 'reglas con fuente y evidencia'), ('318', 'interacciones revisadas'), ('32', 'casos clínicos de validación'), ('5', 'idiomas de interfaz')]
PA_PARA = [('P', 'Pacientes y familias', 'Personas mayores o polimedicadas que quieren moverse con seguridad y saber qué preguntar a su médico.', ['Añades la medicación (y tus suplementos o plantas) buscando, con una foto de la hoja o de la caja, o dictándola.', '«Lo esencial» en cinco puntos, tu plan semanal y una sesión guiada con dibujos y cronómetro.', 'PDF de cuatro caras, tarjeta para la nevera y avisos los días de ejercicio.']),
 ('M', 'Médicos, enfermería y farmacia', 'Para prescribir ejercicio en la consulta con la medicación delante, en menos de cinco minutos.', ['Cribado ACSM, zona de intensidad individual (Karvonen o RPE), SPPB guiado, plantillas por perfil y varios pacientes por sesión.', 'Informe clínico, texto para la historia, exportación FHIR e informe de evolución para la reevaluación.', 'Estadísticas y CSV anonimizado de la consulta para la memoria del servicio.']),
 ('E', 'Entrenadores y fisioterapeutas', 'Para adaptar la sesión sin conocer el diagnóstico: solo los efectos que importan durante el entrenamiento.', ['Ficha del entrenador con lo que puede pasar en la sesión y cómo actuar.', 'Enlace de solo lectura del plan, compartido por el propio paciente.', 'Señales de alarma y prueba del habla cuando el pulso no sirve de guía.'])]
PA_HACE = [('camara', 'Medicación, suplementos y plantas', 'Buscador sobre el nomenclátor de la AEMPS (11.000 presentaciones) y 53 suplementos y plantas por su nombre común (creatina, hierba de San Juan, cola de caballo…); lectura de hojas de medicación y cajas con la cámara, PDF, texto pegado, dictado y código de barras.'),
 ('check', 'Veredicto y lo esencial', 'Una frase clara, cinco puntos prácticos y el detalle por tipo de ejercicio, con el nivel de evidencia y la fuente de cada regla a la vista.'),
 ('pesa', 'Un plan que se puede seguir', 'Semana tipo según la medicación y la forma física, sesión guiada con ejercicios ilustrados y cronómetro, diario con constantes y tendencia semanal.'),
 ('ojo', 'Pantalla de consulta', 'En escritorio o tablet, dos columnas sin pestañas: la medicación y los datos a la izquierda, el informe completo a la derecha, con el paciente delante.'),
 ('libro', 'Informes para cada persona', 'PDF para el paciente (cuatro caras, lo básico en la primera), resumen clínico, ficha del entrenador, tarjeta de nevera, texto para la historia, FHIR y versión en texto accesible.'),
 ('candado', 'Tus datos, solo en tu dispositivo', 'Sin cuentas ni servidores. Copia de seguridad cifrada con tu contraseña y paso de un dispositivo a otro por código QR. Las listas que se comparten nunca llevan nombre.')]
PA_NO = [('No es un producto sanitario ni sustituye a tu médico.', 'Organiza información pública (fichas técnicas de la AEMPS, monografías de plantas medicinales de la EMA, guías ACSM/OMS/ESC/ADA, AIS y COI para suplementos, criterios Beers y STOPP/START) para preparar una conversación con el profesional que te atiende. Las decisiones sobre tratamiento e intensidad son siempre suyas.'),
 ('No diagnostica ni ajusta dosis.', 'Señala precauciones e interacciones conocidas; no sabe lo que no está en tu lista ni lo que tu médico sí sabe de ti.'),
 ('No recoge datos.', 'Precisamente por eso no puede recordarte nada si cambias de dispositivo sin hacer copia, ni avisarte fuera de la aplicación salvo las notificaciones locales que tú actives.')]
PA_PASOS = [('Abre la aplicación', 'En el móvil o el ordenador. Si quieres, instálala desde el menú «Más» para usarla sin conexión y recibir avisos.'), ('Añade tu medicación', 'Y, si los sabes, tu edad, tu situación clínica y tu pulso en reposo. Un minuto.'), ('Llévalo a consulta', 'Lee «Lo esencial», descarga tu PDF y llévalo a la próxima consulta. El profesional puede marcar la prescripción y reevaluarla en seis semanas.')]
PA_ENL = [('https://github.com/pelayoplcoaching/medicacion-y-ejercicio', 'Código y base (GitHub)'), ('https://doi.org/10.5281/zenodo.23423114', 'DOI 10.5281/zenodo.23423114'), (PA + 'novedades.html', 'Novedades'), ('https://tally.so/r/5XK9YM', 'Sugerencias'), (PA + 'legal.html', 'Aviso legal y privacidad')]
_FOTO_A = ilus('foto-pelayo', 'pa-autor-foto').replace('alt=""', 'alt="Pelayo Fernández Cidón"')
FIJO_PA = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="herramientas.html">Herramientas</a><a class="btn claro" href="{PA}" rel="noopener">Abrir Pauta Activa</a></div>'
pagina('pauta-activa.html', 'Pauta Activa', 'Pauta Activa · Medicación y Ejercicio: de tu lista de medicación a un plan de ejercicio seguro. Gratuita, sin cuentas y sin enviar datos a ningún servidor.', 'De tu lista de medicación a un plan de ejercicio seguro', 'Pauta Activa lee tu medicación habitual y tu situación clínica y te dice qué tener en cuenta al entrenar: aeróbico, fuerza y equilibrio, con horario según las tomas, interacciones relevantes (también con los suplementos y plantas que tomas) e informes para ti, tu médico y tu entrenador. Gratuita, sin cuentas y sin enviar ningún dato a ningún servidor.', f'''
<section class="cifras pa-cifras"><div class="in"><ul>{"".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in PA_CIF)}</ul></div></section>
<section><div class="in"><div class="entrada sube"><h2>Para quién</h2><p>Dos modos en la misma herramienta: el del paciente, en lenguaje llano y letra grande, y el profesional, con los datos clínicos que cambian la prescripción.</p></div>
  <div class="ciencia"><div class="rej">{"".join(f'<article class="idea pa-para sube">{PA_PARA_IMG(i, l)}<h3>{t}</h3><p>{d}</p><ul class="marcas">{"".join(f"<li>{x}</li>" for x in xs)}</ul></article>' for i, (l, t, d, xs) in enumerate(PA_PARA))}</div></div>
</div></section>
<section class="hoja" id="que-hace"><div class="in"><div class="entrada sube"><h2>Qué hace</h2><p>Todo ocurre en el navegador. La base de conocimiento se descarga una vez y la aplicación funciona sin conexión e instalada en el móvil.</p></div>
  <figure class="pa-pantalla sube"><div class="pa-barra" aria-hidden="true"><i></i><i></i><i></i><span>medicacionyejercicio.fuerzabasadaenevidencia.com</span></div>{_alt(ilus("pa-consulta", "pa-cap"), "Pantalla de consulta de Pauta Activa: datos y medicación a la izquierda, «Qué tener en cuenta» a la derecha")}</figure>
  <div class="pa-hace">{"".join(f'<div class="caja sube"><i class="ic">{ico(i)}</i><h3>{t}</h3><p>{d}</p></div>' for i, t, d in PA_HACE)}</div>
</div></section>
<section class="pa-movil-s"><div class="in">
  <div class="pa-moviles sube">{PA_TEL("vistazo", "Pauta Activa en el móvil: de un vistazo, qué puedes hacer, con cuidado y qué evitar")}{PA_TEL("sesion", "Pauta Activa en el móvil: sesión guiada con ejercicios y nivel de dificultad")}</div>
  <div class="sube"><div class="entrada"><h2>En el móvil, como una app</h2><p>Lo esencial en cinco puntos, la semana tipo y una sesión guiada con ejercicios ilustrados y cronómetro.</p></div>
  <p><a class="btn" href="{PA}" rel="noopener">Abrir Pauta Activa</a></p><p class="pa-guia"><a href="{PA}guia.html" rel="noopener">Guía rápida en seis pasos</a></p></div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Lo que no es</h2></div>
  <ul class="pa-no sube">{"".join(f"<li><b>{a}</b> {b}</li>" for a, b in PA_NO)}</ul>
  <p class="pa-rev sube">El contenido clínico lo mantiene un médico con un muestreo de revisión continuo; cada actualización de la base avisa dentro de la aplicación de lo que cambia. Si encuentras un error, el formulario de sugerencias llega directamente al autor. Más detalle en <a href="{PA}legal.html#metodologia" rel="noopener">Metodología y limitaciones</a> y <a href="{PA}legal.html#regulatorio" rel="noopener">Posicionamiento regulatorio</a>.</p>
</div></section>
<section class="pasos">{ANILLOS}<div class="in"><div class="entrada sube"><h2>Cómo empezar</h2></div>
  <ol>{"".join(f'<li class="sube"><h3>{t}</h3><p>{d}</p></li>' for t, d in PA_PASOS)}</ol>
  <p class="pa-pasos-bot sube"><a class="btn claro" href="{PA}" rel="noopener">Abrir Pauta Activa</a></p></div></section>
<section><div class="in"><div class="pa-autor sube">{_FOTO_A}<div><p class="herr-et">{PA_LOGO}Quién la hace</p><p class="pa-autor-t">Pelayo Fernández Cidón, médico especialista en medicina interna y prescriptor de ejercicio físico.</p><p>Código abierto (MIT) y base de conocimiento publicada (CC BY-NC-SA 4.0): cualquier profesional puede revisar cada regla, proponer cambios y citar la base.</p>
  <ul class="herr-chips enl">{"".join(f'<li><a href="{u}" rel="noopener">{t}</a></li>' for u, t in PA_ENL)}</ul></div></div></div></section>
{CTA_PP}''', f'<div class="cta"><a class="btn claro" href="{PA}" rel="noopener">Abrir Pauta Activa</a><a class="enl" href="#que-hace">Qué hace</a></div>', fijo=FIJO_PA, extra=PA_LD, lado=f'<div class="pa-hero">{PA_TEL("vistazo", "Pauta Activa en el móvil")}</div>', padre=('herramientas.html', 'Herramientas'))
exec(open('herramientas.py', encoding='utf-8').read())  # cinco calculadoras de Herramientas (21/11/2026)
exec(open('secciones.py', encoding='utf-8').read())  # Empieza aquí, Vídeos, Para profesionales y Mitos y evidencia (21/11/2026)
exec(open('tarifas.py', encoding='utf-8').read())  # tarifas.html: precios de los tres programas; sin enlazar, noindex y fuera del sitemap (23/11/2026)
exec(open('esencial.py', encoding='utf-8').read())  # esencial.html: FBE Esencial; oculta hasta el 3/1/2027 (sin enlazar, noindex, fuera del sitemap y del buscador) (24/11/2026)
exec(open('app_pags.py', encoding='utf-8').read())  # la web como app (1): Aprende, Mi panel, Novedades y RSS, Ayuda y Sin conexión (22/11/2026)
exec(open('formacion.py', encoding='utf-8').read())  # «Trayectoria y formación» en Quién soy, del CV y del carnet de colegiado (23/11/2026)
exec(open('extras.py', encoding='utf-8').read())  # Glosario, archivo del boletín, Mis resultados, buscador y web instalable (21/11/2026)
exec(open('fuentes.py', encoding='utf-8').read())  # Fuentes: todas las referencias, comprobadas en PubMed, y enlaces en herramientas, mitos y portada (21/11/2026, noche)
exec(open('temas.py', encoding='utf-8').read())  # cinco páginas de tema: envejecer, medicación, dolor, nutrición y poco tiempo (21/11/2026, noche)
exec(open('siguiente.py', encoding='utf-8').read())  # «¿Y ahora qué?» bajo cada calculadora, según el resultado (21/11/2026, noche)
exec(open('chequeo.py', encoding='utf-8').read())  # «Chequeo de 10 minutos»: ruta guiada por cuatro herramientas y resumen por áreas (21/11/2026, noche)
exec(open('compartir.py', encoding='utf-8').read())  # «Compartir resultado»: imagen hecha en el navegador, sin datos personales (21/11/2026, noche)
exec(open('recetas.py', encoding='utf-8').read())  # «Recetas con proteína»: las diez de muestra del recetario, con filtros y «Tu día» (21/11/2026, noche)
exec(open('boletin_cta.py', encoding='utf-8').read())  # «El boletín, por tema» al final de herramientas, Mitos y Glosario (21/11/2026, noche)
exec(open('autoria.py', encoding='utf-8').read())  # firma y fecha en las páginas de salud y «Cómo trabajo la evidencia» (21/11/2026, noche)
exec(open('evolucion.py', encoding='utf-8').read())  # «Mi evolución» (gráficas) e «Informe para tu médico» en Mis resultados (21/11/2026, noche)
exec(open('extras2.py', encoding='utf-8').read())  # test de mitos, plan semanal con calendario, datos estructurados e imagen para compartir de cada página (21/11/2026)
exec(open('datos.py', encoding='utf-8').read())  # datos para buscadores que faltaban: organización, perfil, mitos (ClaimReview), herramientas y recetas (21/11/2026, noche)
exec(open('app.py', encoding='utf-8').read())  # la web como app (2): pestañas, vídeos enlazados, «Esta semana», rutas con progreso, acciones del buscador, manifiesto y service worker (22/11/2026)
exec(open('articulos.py', encoding='utf-8').read())  # boletines como artículos de la web (24/11/2026)
open(f'{SAL}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{WEB}{u}</loc></url>\n' for u in [''] + [u for u, _ in PAGS] + ['pauta-activa.html', 'test-silla.html', 'calculadora-1rm.html', 'volumen-semanal.html', 'cafeina.html', 'revision-medica.html', 'zonas-pulso.html', 'semaforo-dolor.html', 'test-sppb.html', 'paron.html', 'suplementos.html'] + SEC_PAGS + (['privacidad.html'] if os.environ.get('FBE_CORREO') else [])) + '</urlset>\n')
open(f'{SAL}/robots.txt', 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nSitemap: {WEB}sitemap.xml\n')
p = open(f'{SAL}/index.html', encoding='utf-8').read()
import base64, hashlib
os.makedirs(f'{SAL}/img', exist_ok=True); vistos = {}
def fuera(m):
    ext = {'jpeg': 'jpg'}.get(m.group(1), m.group(1)); b = base64.b64decode(m.group(2)); k = hashlib.sha1(b).hexdigest()[:10]
    if k not in vistos: vistos[k] = f'img/{k}.{ext}'; open(f'{SAL}/{vistos[k]}', 'wb').write(b)
    return f'src="{vistos[k]}"'
p = re.sub(r'src="data:image/(webp|png|jpeg);base64,([^"]+)"', fuera, p)
cuenta = [0]
def perezosa(m):
    cuenta[0] += 1
    return m.group(0) if cuenta[0] <= 2 or 'loading=' in m.group(0) else m.group(0).replace('<img ', '<img loading="lazy" decoding="async" ', 1)
p = re.sub(r'<img [^>]*>', perezosa, p)
print('imagenes fuera:', len(vistos))
p = p.replace('<meta charset="utf-8">', f'<meta charset="utf-8"><link rel="canonical" href="{WEB}"><meta name="theme-color" content="#140B3A"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="icono-180.png"><meta property="og:image" content="{WEB}og.png"><meta name="twitter:card" content="summary_large_image"><meta property="og:url" content="{WEB}"><meta property="og:type" content="website"><meta property="og:locale" content="es_ES">', 1)
open(f'{SAL}/index.html', 'w', encoding='utf-8').write(p)
print({f: os.path.getsize(f'{SAL}/{f}') // 1024 for f in sorted(os.listdir(SAL))})

# Letra Archivo servida desde la propia web (sin Google Fonts)
shutil.copy('ext/archivo.woff2', f'{SAL}/img/archivo.woff2')
import glob, re as _re
# Letra de reserva ajustada (24/11/2026): mientras llega Archivo se usa Arial (o Liberation Sans, igual de ancha) o, en Android, Roboto,
# agrandada o achicada para que ocupe lo mismo que Archivo y el texto no salte al cambiar. Medidas con fontTools sobre el texto de la web:
# cuerpo (peso 400, anchura 100), negrita (700, 100), texto ancho (600, 118) y titulares (760, 120).
def _fb(fam, reg, neg, medidas):
    out = ''
    for (pesos, anchos), (src, (sa, asc, des)) in zip([('100 600', '50% 110%'), ('601 1000', '50% 110%'), ('100 600', '111% 200%'), ('601 1000', '111% 200%')],
                                                      [(reg, medidas[0]), (neg, medidas[1]), (reg, medidas[2]), (neg, medidas[3])]):
        out += f'@font-face{{font-family:"{fam}";src:{src};font-weight:{pesos};font-stretch:{anchos};size-adjust:{sa}%;ascent-override:{asc}%;descent-override:{des}%;line-gap-override:0%}}'
    return out
_FB = (_fb('Archivo fb', 'local("Arial"),local("ArialMT"),local("Liberation Sans"),local("LiberationSans")', 'local("Arial Bold"),local("Arial-BoldMT"),local("Liberation Sans Bold"),local("LiberationSans-Bold")',
           [(98.1, 89.5, 21.4), (98.2, 89.4, 21.4), (122.6, 71.6, 17.1), (121.9, 72, 17.2)]) +
       _fb('Archivo fb2', 'local("Roboto"),local("Roboto-Regular")', 'local("Roboto Bold"),local("Roboto-Bold")',
           [(99.0, 88.7, 21.2), (104.4, 84.1, 20.1), (123.8, 70.9, 17.0), (129.5, 67.8, 16.2)]))
_FF = '<link rel="preload" href="img/archivo.woff2" as="font" type="font/woff2" crossorigin><style>@font-face{font-family:"Archivo";src:url(img/archivo.woff2) format("woff2");font-weight:400 800;font-stretch:75% 125%;font-display:swap}' + _FB + '</style>'
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read()
    _n = _re.sub(r'(<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>)?<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Archivo[^"]*">', _FF, _t)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)

# Conexion anticipada a MailerLite (caras de testimonios y formulario) y navegacion instantanea al pasar por un enlace
_PRE = '<link rel="preconnect" href="https://storage.mlcdn.com" crossorigin><script type="speculationrules">{"prefetch":[{"where":{"href_matches":"/*"},"eagerness":"moderate"}]}</script>'
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read()
    if 'speculationrules' not in _t and '</head>' in _t:
        open(_f, 'w', encoding='utf-8').write(_t.replace('</head>', _PRE + '</head>', 1))
# Contador de visitas sin cookies (Umami Cloud, 24/11/2026; Website ID que dio Pelayo). Solo cuenta en el dominio
# (data-domains: las pruebas en local no cuentan) y respeta «no rastrear». Clics que cuenta: Pedir plaza (con la pagina
# desde la que se pulsa), comprar la Puesta a punto y apuntarse al boletin. No va en las paginas de desvio.
UMAMI = '<script defer src="https://cloud.umami.is/script.js" data-website-id="afbc92fb-0c36-4ef4-aff9-def6810b8f79" data-domains="fuerzabasadaenevidencia.com" data-do-not-track="true"></script>'
_SIN_UMAMI = {'faq.html', 'newsletter-semanal.html', 'programas-copy.html', 'quien_soy.html'} | {f'{c}.html' for c in CORTAS}
for _f in glob.glob(f'{SAL}/*.html'):
    _b = os.path.basename(_f)
    if _b in _SIN_UMAMI or _b.startswith('google'): continue
    _t = open(_f, encoding='utf-8').read()
    if 'cloud.umami.is' in _t or '</head>' not in _t: continue
    _p = _b[:-5]
    _n = _t.replace('</head>', UMAMI + '</head>', 1)
    _n = _re.sub(r'<a href="pedir-plaza\.html"(?![^>]*data-umami-event)', f'<a href="pedir-plaza.html" data-umami-event="Pedir plaza" data-umami-event-desde="{_p}"', _n)
    _n = _re.sub(r'<a href="(https://buy\.stripe\.com/[^"]*)"(?![^>]*data-umami-event)', r'<a href="\1" data-umami-event="Comprar Puesta a punto"', _n)
    _n = _re.sub(r'<a href="newsletter\.html#alta"(?![^>]*data-umami-event)', f'<a href="newsletter.html#alta" data-umami-event="Quiero el boletín" data-umami-event-desde="{_p}"', _n)
    open(_f, 'w', encoding='utf-8').write(_n)
# Enlace a la propia pagina marcado como actual (pie y menu), para que se vea donde estas
for _f in glob.glob(f'{SAL}/*.html'):
    _b = os.path.basename(_f)
    if _b == 'index.html': continue
    _t = open(_f, encoding='utf-8').read()
    _n = _re.sub(r'<a href="' + _re.escape(_b) + r'"(?![^>]*aria-current)', f'<a href="{_b}" aria-current="page"', _t)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
# Accesibilidad (zonas): la barra superior es la cabecera del sitio (<header>), la cabecera de cada pagina
# pasa a ser una region con nombre (su h1), la portada tiene su <main>, y «Volver arriba» y la barra del movil
# quedan dentro de zonas. Asi un lector de pantalla salta por zonas sin que nada quede fuera.
def _cierre(t, ini, tag):
    d = 0
    for m in _re.finditer(r'<(/?)' + tag + r'\b[^>]*>', t[ini:]):
        d += -1 if m.group(1) else 1
        if d == 0: return ini + m.start()
    return -1
def _zonas(t, portada):
    i = t.find('<div class="cab">')
    if i >= 0:
        j = _cierre(t, i, 'div')
        if j > 0: t = t[:j] + '</header>' + t[j + 6:]; t = t[:i] + '<header class="cab">' + t[i + 17:]
    i = t.find('<header class="hero')
    if i >= 0:
        j = _cierre(t, i, 'header')
        if j > 0:
            seg = t[i:j]; m = _re.search(r'<h1\b([^>]*)>', seg); hid = 'titulo'
            if m:
                mi = _re.search(r'\bid="([^"]+)"', m.group(1))
                if mi: hid = mi.group(1)
                else: seg = seg[:m.start()] + '<h1 id="titulo"' + seg[m.start() + 3:]
            seg = '<div role="region" aria-labelledby="' + hid + '" class="hero' + seg[len('<header class="hero'):]
            t = t[:i] + seg + '</div>' + t[j + len('</header>'):]
    if portada:  # la portada usa la misma hoja que el resto (fbe.css, en cache) en lugar de 520 KB de estilos dentro del HTML
        t = _re.sub(r'<style>(?:(?!</style>).){100000,}</style>', '<link rel="stylesheet" href="fbe.css">', t, count=1, flags=_re.S)
        # el movil de atras de la portada no se ve en movil: que no se descargue hasta que haga falta
        t = _re.sub(r'(<div class="tel atras"[^>]*>(?:(?!<img).)*?<img)\b(?![^>]*loading=)', r'\1 loading="lazy"', t, count=1, flags=_re.S)
    if portada:  # paneles de la galeria de la app: el papel de panel va en un envoltorio, no en la imagen
        t = _re.sub(r'<img ([^>]*?)id="p(\d+)" role="tabpanel" aria-labelledby="t\2" (hidden )?([^>]*)>', lambda m: f'<div id="p{m.group(2)}" role="tabpanel" aria-labelledby="t{m.group(2)}" tabindex="0"{" hidden" if m.group(3) else ""}><img {m.group(1)}{m.group(4)}></div>', t)
    if portada:  # secciones de la portada bajo el pliegue: se pintan al acercarse (content-visibility), menos trabajo al cargar (24/11/2026)
        _o, _d, _k, _u = [], 0, 0, 0
        for _m in _re.finditer(r'<(/?)section\b([^>]*)>', t):
            _o.append(t[_u:_m.start()]); _u = _m.end(); _a = _m.group(2)
            if _m.group(1): _d -= 1; _o.append(_m.group(0)); continue
            if _d == 0:
                if _k >= 2 and 'lenta' not in _a and 'cierre' not in _a:
                    _a = _re.sub(r'class="', 'class="lenta ', _a, count=1) if 'class="' in _a else _a + ' class="lenta"'
                _k += 1
            _d += 1; _o.append(f'<section{_a}>')
        _o.append(t[_u:]); t = ''.join(_o)
    if portada and '<main' not in t:
        k = t.find('<div class="franja">'); f = t.find('<footer')
        if 0 < k < f: t = t[:k] + '<main id="contenido">' + t[k:f] + '</main>\n' + t[f:]
    t = _re.sub(r'(<a class="arriba"[^>]*>.*?</a>)', r'<nav class="arriba-n" aria-label="Volver arriba">\1</nav>', t, count=1, flags=_re.S) if 'class="arriba-n"' not in t else t
    i = t.find('<section class="cierre">')
    if i >= 0 and not portada:
        m = _re.compile(r'<h2\b([^>]*)>').search(t, i)
        if m and 'id="' not in m.group(1):
            t = t[:m.start()] + '<h2 id="cierre-t"' + t[m.start() + 3:]
            t = t[:i] + '<section class="cierre" aria-labelledby="cierre-t">' + t[i + len('<section class="cierre">'):]
    t = t.replace('<div class="fijo" id="fijo">', '<div class="fijo" id="fijo" role="navigation" aria-label="Accesos rápidos">', 1)
    return t
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read()
    _n = _zonas(_t, os.path.basename(_f) == 'index.html')
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
# Imagenes a la medida: versiones de 160, 360, 640 y 960 px (solo las menores que el original) y srcset/sizes
# segun el tamano real al que se pinta cada clase (medido en 390 y 1280 px). Asi el movil no baja imagenes de escritorio.
_TAM = {'tool-tira-img': (100, 280), 'ilus': (360, 600), 'herr-mini-img': (320, 340), 'tool-fondo': (360, 530), 'mito-img': (330, 340),
        'foto-g': (360, 400), 'ea-img': (360, 330), 'tarj-img': (130, 370), 'pa-cap': (360, 1120), 'paso-img': (300, 230), 'pub-img': (320, 240),
        'ev-ilus': (320, 320), 'pa-para-ilus': (320, 320), 'tres-img': (360, 360), 'foto-i': (320, 320), 'espera-img': (340, 360), 'foto-b': (320, 330),
        'herr-cap': (360, 600), 'pa-logo': (28, 28), 'foto-p': (360, 450), 'foto-c': (300, 230), 'pa-autor-foto': (110, 150), 'pro-logo': (66, 66),
        'pro-guia': (90, 115), 'pro-img': (360, 460), 'banner': (360, 1120), 'lema-fondo': (440, 1440), 'vid-fondo': (360, 1120), 'pase': (300, 330),
        'mr-vacio-img': (360, 420), 'instala-img': (150, 180), 'herr-img': (360, 620), 'ap-tema-img': (240, 240), 'ap-ruta-img': (96, 96), 'pn-cielo-img': (480, 960), 'ap-t-img': (240, 480)}
_TAM_P = {'retrato xl': (200, 370), 'retrato': (120, 180), 'tel atras': (310, 310), 'tel plano': (310, 310), 'tel': (310, 310), 'm dos': (80, 80), 'm': (240, 240), 'pos': (360, 900)}
_PORTADA_HTML = [False]
_VAR = {}
def _variantes(nombre):
    if nombre in _VAR: return _VAR[nombre]
    from PIL import Image as _I
    orig = f'{SAL}/img/{nombre}'; base = nombre[:-5]; res = []
    try: im = _I.open(orig); nw, nh = im.size
    except Exception: _VAR[nombre] = None; return None
    os.makedirs(f'{SAL}/img/v', exist_ok=True)
    for w in (96, 160, 360, 480, 640, 960):
        if w >= nw * 0.92: continue
        dest = f'{SAL}/img/v/{base}-{w}.webp'
        if not os.path.exists(dest) or os.path.getmtime(dest) < os.path.getmtime(orig):
            im2 = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB').resize((w, max(1, round(nh * w / nw))), _I.LANCZOS)
            im2.save(dest, 'WEBP', quality=80, method=6)
        res.append(w)
    _VAR[nombre] = (res, nw); return _VAR[nombre]
def _srcset(m):
    tag = m.group(0)
    if 'srcset=' in tag: return tag
    src = _re.search(r'\bsrc="img/([^"/]+\.webp)"', tag)
    if not src: return tag
    v = _variantes(src.group(1))
    if not v or not v[0]: return tag
    ws, nw = v; base = src.group(1)[:-5]
    cls = (_re.search(r'\bclass="([^"]*)"', tag) or [None, ''])[1].split()
    mv, dv = next((_TAM[c] for c in cls if c in _TAM), (None, None))
    if mv is None:  # sin clase propia: se mira la clase del contenedor (retrato, marcos de movil de la portada...)
        prev = _re.findall(r'<[a-z0-9]+\b[^>]*?class="([^"]*)"[^>]*>', m.string[max(0, m.start() - 400):m.start()])
        pc = prev[-1].strip() if prev else ''
        mv, dv = _TAM_P.get(pc, (None, None))
    if mv is None: mv, dv = (310, 310) if _PORTADA_HTML[0] else (min(nw, 400), min(nw, 1200))
    # en el movil hacen falta como poco 2 px de imagen por punto: se quitan las versiones que se quedarian cortas
    ws = [w for w in ws if w >= min(mv, dv) or w >= 96]
    sset = ', '.join(f'img/v/{base}-{w}.webp {w}w' for w in ws) + f', img/{base}.webp {nw}w'
    return tag[:-1].rstrip('/').rstrip() + f' srcset="{sset}" sizes="(max-width: 700px) {mv}px, {dv}px">'
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read(); _PORTADA_HTML[0] = os.path.basename(_f) == 'index.html'
    _n = _re.sub(r'<img\b[^>]*>', _srcset, _t)
    _n = _re.sub(r'(<img class="herr-cap"[^>]*?)loading="lazy"', r'\1loading="eager"', _n, count=1)
    # la primera imagen grande del contenido no se carga en diferido si la pagina no tiene ilustracion de cabecera (es la mayor que se ve al entrar)
    if 'class="ilus"' not in _n:
        _n = _re.sub(r'(<main id="contenido">(?:(?!<img).)*?<img\b[^>]*?)loading="lazy"', r'\1loading="eager"', _n, count=1, flags=_re.S)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
# CSS sin comentarios (mas ligero)
_c = open(f'{SAL}/fbe.css', encoding='utf-8').read()
_c2 = _re.sub(r'/\*.*?\*/', '', _c, flags=_re.S)
_c2 = _re.sub(r'\n\s*\n+', '\n', _c2)
# compactar espacios (unos 3 KB menos comprimido): saltos de linea, espacios junto a llaves y puntos y coma, y tras los dos puntos de cada declaracion
_c2 = _re.sub(r'\s*\n\s*', ' ', _c2)
_c2 = _re.sub(r'\s*([{};])\s*', r'\1', _c2)
_c2 = _c2.replace(';}', '}')
_c2 = _re.sub(r'([{;][\w-]+):\s+', r'\1:', _c2)
# la letra de reserva ajustada va detras de Archivo en todas las pilas de letra (ver _FB)
_c2 = _re.sub(r'Archivo,\s*(?!"Archivo fb)', 'Archivo,"Archivo fb","Archivo fb2",', _c2)
open(f'{SAL}/fbe.css', 'w', encoding='utf-8').write(_c2)
# Versión en la dirección de la hoja de estilos y del guion (22/11/2026): el service worker guarda fbe.css y fbe.js y los
# sirve de la caché; sin esto, quien ya tenía la web guardada veía la página nueva con el estilo viejo hasta recargar.
import hashlib as _hv
_VA = _hv.sha1((open(f'{SAL}/fbe.css', encoding='utf-8').read() + open(f'{SAL}/fbe.js', encoding='utf-8').read()).encode('utf-8')).hexdigest()[:8]
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read()
    _n = _re.sub(r'href="fbe\.css(\?v=[0-9a-f]+)?"', f'href="fbe.css?v={_VA}"', _t)
    _n = _re.sub(r'src="fbe\.js(\?v=[0-9a-f]+)?"', f'src="fbe.js?v={_VA}"', _n)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
_sw = open(f'{SAL}/sw.js', encoding='utf-8').read()
_sw = _sw.replace('"fbe.css"', f'"fbe.css?v={_VA}"').replace('"fbe.js"', f'"fbe.js?v={_VA}"')
assert f'fbe.css?v={_VA}' in _sw and f'fbe.js?v={_VA}' in _sw
open(f'{SAL}/sw.js', 'w', encoding='utf-8').write(_sw)
