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
def datos(*xs): return '<ul class="datos">' + ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in xs) + '</ul>'
def sigue(arch):
    i = [u for u, _ in PAGS].index(arch); a = PAGS[i - 1] if i else ('index.html', 'Inicio'); b = PAGS[i + 1] if i + 1 < len(PAGS) else ('index.html', 'Inicio')
    return f'<nav class="sigue" aria-label="Seguir leyendo"><div class="in"><a href="{a[0]}"><small>Anterior</small><b>{a[1]}</b></a><a class="der" href="{b[0]}"><small>Siguiente</small><b>{b[1]}</b></a></div></nav>'
def cabeza(arch, titulo, desc, extra=''):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo} · Fuerza Basada en Evidencia</title><meta name="description" content="{desc}">
<link rel="canonical" href="{WEB}{arch}"><meta name="theme-color" content="#140B3A"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="icono-180.png">
<meta property="og:image" content="{WEB}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="Fuerza Basada en Evidencia"><meta property="og:title" content="{titulo} · Fuerza Basada en Evidencia"><meta property="og:description" content="{desc}"><meta property="og:url" content="{WEB}{arch}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap"><link rel="stylesheet" href="fbe.css">{extra}</head><body class="pag-{arch[:-5]}" style="margin:0">'''
def pagina(arch, titulo, desc, h1, sub, cuerpo, cta='', cierre_t=None, fijo=None, extra='', lado=''):
    doc = f'''{cabeza(arch, titulo, desc, extra)}
{cabecera(arch)}
<header class="hero mini t-{arch[:-5]}{" foto" if lado else ""}" id="inicio">{ANILLOS}{"" if lado else (ilus("web-" + arch[:-5]) or f"<div class=\"marca-agua\">{LOBO}</div>")}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / {titulo}</span><h1>{h1}</h1><p class="sub">{sub}</p>{cta}</div>{lado}</div></header>
<main id="contenido">{cuerpo}</main>
{sigue(arch)}
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
pagina('quien-soy.html', 'Quién soy', 'Pelayo Fernández Cidón, médico internista y entrenador: cómo trabajo y con quién.', 'Médico de día. Entrenador el resto.', 'Soy Pelayo Fernández Cidón, especialista en medicina interna. Prescribo ejercicio de fuerza y nutrición a gente con poco tiempo que quiere un plan claro y con base científica.', f'''
<section><div class="in dos">
  <div class="sube"><div class="entrada"><h2>Cómo empezó</h2></div>
    <ol class="linea">
      <li><h3>Primero de Medicina</h3><p>Había dejado el fútbol, había cogido peso y los estudios se me hacían cuesta arriba. Empecé a entrenar fuerza y recuperé la energía y la cabeza despejada. Ese año lo aprobé todo.</p></li>
      <li><h3>La preparación del MIR</h3><p>Seguí entrenando mientras estudiaba. No volví a suspender un examen.</p></li>
      <li><h3>Medicina interna</h3><p>Trabajo en un hospital de alta complejidad, con pacientes con enfermedad crónica, varias patologías a la vez, dolor persistente y limitación funcional. Ahí aprendí algo que no viene en los libros: <strong>todo el mundo sabe que el ejercicio es bueno, pero casi nunca se prescribe bien</strong>. Y la fuerza, menos todavía, sobre todo en quien ya tiene una enfermedad.</p></li>
      <li><h3>2020: nace FBE</h3><p>Para llevar a la vida real lo que la evidencia dice desde hace años.</p></li>
    </ol></div>
  <aside class="pegada sube"><h3>Formación</h3><ul class="marcas"><li>Especialista en Medicina Interna</li><li>Experto universitario en entrenamiento de fuerza</li><li>Máster en nutrición clínica</li><li>Más de 15 años entrenando fuerza</li></ul><a class="btn" href="{FORM}">Pedir plaza</a><div class="redes claras">{''.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in REDES)}</div></aside>
</div></section>
<section class="lema-banda">{ilus("web-frase", "lema-fondo")}<div class="in sube"><blockquote>Lo que no puedes sostener en tu día a día, no sirve.</blockquote><p>Pelayo Fernández Cidón</p></div></section>
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
    <a class="caja sube" href="guias.html"><i class="ic">{ico('libro')}</i><h3>Guías</h3><p>Nueve guías prácticas para descargar.</p></a>
    <a class="caja sube" href="newsletter.html"><i class="ic">{ico('chat')}</i><h3>Newsletter</h3><p>Un correo a la semana.</p></a>
    <a class="caja sube" href="{CALC}"><i class="ic">{ico('plato')}</i><h3>Calculadora de proteína</h3><p>Gratis, con reparto por comidas.</p></a>
    <a class="caja sube" href="{dict(REDES)['YouTube']}" target="_blank" rel="noopener"><i class="ic">{ico('video')}</i><h3>YouTube</h3><p>Vídeos sobre fuerza, nutrición y salud.</p></a>
  </div></div></section>''', BTN + datos(('15+', 'años entrenando fuerza'), ('2020', 'el año en que nace FBE')), extra=LDP, lado=f'<div class="retrato xl">PF<img src="{FOTO}" alt="Pelayo Fernández Cidón" width="720" height="900" fetchpriority="high" decoding="async" onerror="this.remove()"></div>')

# ===== programas =====
P = [('essential', 'Entrenamiento', 'Essential', 'Mensual', 'Correo', ['Revisión del plan cada 4 semanas', 'Seguimiento semanal por correo', 'Programación basada en evidencia', 'Adaptada a tu energía, tu horario y tu estrés']),
 ('performance', 'Entrenamiento', 'Performance', 'Semanal', 'WhatsApp', ['Revisión y actualización del plan cada semana', 'Contacto directo por WhatsApp, respuesta en 48 h', 'Ajustes sobre la marcha: horarios, viajes, molestias, cansancio', 'Para semanas que no se parecen entre sí']),
 ('complete', 'Entrenamiento y nutrición', 'Complete', 'Mensual', 'Correo', ['Revisión mensual de los dos planes', 'Contacto semanal por correo', 'Ajustes flexibles en semanas de mucho estrés o cambios de horario']),
 ('elite', 'Entrenamiento y nutrición', 'Elite', 'Semanal', 'WhatsApp', ['Revisión semanal de los dos planes', 'WhatsApp con respuesta en 48 h', 'Ajustes continuos: horario, estado físico y mental, viajes, carga de trabajo', 'Nuevos objetivos cuando toque']),
 ('eliteplus', 'Entrenamiento y nutrición', 'Elite Plus', 'Semanal', 'WhatsApp y videollamada', ['Todo lo de Elite', 'Videollamada semanal de 20 minutos', 'Para repasar el progreso, ajustar la estrategia y planificar'])]
def plan(p):
    k, g, n, r, c, items = p
    niv, tope = {'essential': (1, 2), 'performance': (2, 2), 'complete': (1, 3), 'elite': (2, 3), 'eliteplus': (3, 3)}[k]
    barras = '<span class="nivel" aria-hidden="true">' + ''.join(f'<i{" class=\"on\"" if j < niv else ""}></i>' for j in range(tope)) + '</span>'
    return f'<article class="plan n{niv}{" oro" if k == "eliteplus" else ""} sube" id="{k}"><span class="eti" hidden>Te encaja</span><h3>{n}{barras}</h3><p class="ritmo"><span>Revisión {r.lower()}</span><span>{c}</span></p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><a class="btn peq" href="{FORM}">Empezar con {n}</a><a class="comp" href="#lado">Comparar con los demás</a></article>'
fila = lambda t, f: f'<tr><th scope="row">{t}</th>' + ''.join(f'<td>{f(p)}</td>' for p in P) + '</tr>'
TABLA = '<div class="tabla-marco ancha sube" tabindex="0" role="region" aria-label="Comparativa de programas"><table class="compara ancha"><thead><tr><td></td>' + ''.join(f'<th scope="col"><a href="#{p[0]}">{p[2]}</a></th>' for p in P) + '</tr></thead><tbody>' + fila('Entrenamiento a medida', lambda p: SI) + fila('Plan de nutrición', lambda p: SI if 'nutrición' in p[1] else NO) + fila('Cada cuánto reviso tu plan', lambda p: 'Cada 4 semanas' if p[3] == 'Mensual' else 'Cada semana') + fila('Por dónde hablamos', lambda p: p[4].split(' y ')[0]) + fila('Videollamada semanal', lambda p: SI if p[0] == 'eliteplus' else NO) + fila('App FBE Equipo y guías', lambda p: SI) + '</tbody></table></div>'
ELIGE = '''<div class="elige sube" id="elige"><div><h2>¿Cuál te encaja?</h2><p>Dos respuestas y te señalo por dónde empezaría.</p></div>
  <div class="elige-p"><p id="e1">¿Quieres también la nutrición?</p><div class="fases claras" role="group" aria-labelledby="e1" data-g="n"><button type="button" data-v="0" aria-pressed="false">Solo entrenamiento</button><button type="button" data-v="1" aria-pressed="true">Entrenamiento y nutrición</button></div>
  <p id="e2">¿Cómo de cerca quieres que esté?</p><div class="fases claras" role="group" aria-labelledby="e2" data-g="r"><button type="button" data-v="0" aria-pressed="false">Una revisión al mes</button><button type="button" data-v="1" aria-pressed="true">Cada semana</button><button type="button" data-v="2" aria-pressed="false">Cada semana y con videollamada</button></div></div>
  <p class="elige-r" aria-live="polite"><span id="elige-t"></span> <a href="#elite" id="elige-a">Ver el programa</a></p></div>'''
JS_P = '''<script>(function(){var D=document,O=['essential','performance','complete','elite','eliteplus'],M={'00':'essential','01':'performance','02':'eliteplus','10':'complete','11':'elite','12':'eliteplus'},N={essential:'Essential',performance:'Performance',complete:'Complete',elite:'Elite',eliteplus:'Elite Plus'},v={n:'1',r:'1'};try{var g=JSON.parse(localStorage.getItem('fbe-web-plan'));if(g&&/^[01]$/.test(g.n)&&/^[012]$/.test(g.r))v=g}catch(e){}
[].forEach.call(D.querySelectorAll('.elige .fases'),function(gr){[].forEach.call(gr.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x.dataset.v===v[gr.dataset.g])})});
function pinta(){var k=M[v.n+v.r],t='Yo empezaría con '+N[k]+'.';if(v.n==='0'&&v.r==='2')t='La videollamada semanal va con Elite Plus, que también incluye nutrición.';D.getElementById('elige-t').textContent=t;D.getElementById('elige-a').setAttribute('href','#'+k);[].forEach.call(D.querySelectorAll('.plan'),function(p){var s=p.id===k;p.classList.toggle('top',s);p.querySelector('.eti').hidden=!s});[].forEach.call(D.querySelectorAll('.compara.ancha tr'),function(tr){[].forEach.call(tr.children,function(c,i){c.classList.toggle('yo',i>0&&O[i-1]===k)})})}
[].forEach.call(D.querySelectorAll('.elige .fases'),function(g){g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b)});v[g.dataset.g]=b.dataset.v;try{localStorage.setItem('fbe-web-plan',JSON.stringify(v))}catch(e){}pinta()})});pinta()})();</script>'''
pagina('programas.html', 'Programas', 'Programas de seguimiento de entrenamiento y nutrición: Essential, Performance, Complete, Elite y Elite Plus.', 'Elige cuánto quieres que te acompañe.', 'Todos los programas son a medida y se llevan desde la app. Cambia cada cuánto reviso tu plan y por dónde hablamos.', f'''
<section><div class="in">
  {ELIGE}
  <p class="grupo-t sube">Solo entrenamiento</p>
  <div class="planes">{plan(P[0])}{plan(P[1])}</div>
  <p class="grupo-t sube">Entrenamiento y nutrición</p>
  <div class="planes">{plan(P[2])}{plan(P[3])}{plan(P[4])}</div>
  <div class="aviso sube" style="margin:2.5rem 0 0"><span><b>Trabajo con un grupo pequeño.</b> Si ahora no hay plaza, entras en la lista de espera al rellenar el formulario.</span><a class="btn peq" href="puesta-a-punto.html">¿No quieres esperar? Puesta a punto</a></div>
</div></section>
<section class="hoja" id="lado"><div class="in"><div class="entrada sube"><h2>Los cinco, lado a lado</h2></div><p class="desliza">Desliza la tabla para ver los cinco.</p>{TABLA}</div></section>
<section><div class="in"><div class="entrada sube"><h2>Lo que llevan todos</h2></div>
  <ul class="tres sube" style="margin-top:0"><li><i>{ico('pesa')}</i><b>Plan a medida</b><span>Hecho para tu horario, tu material y tu punto de partida.</span></li><li><i>{ico('video')}</i><b>La app FBE Equipo</b><span>Sesiones, registro serie a serie, vídeos, recetario y progreso. <a href="index.html#semana">Mírala por dentro</a>.</span></li><li><i>{ico('libro')}</i><b>Las guías</b><span>Para entender lo que haces y por qué.</span></li></ul>
</div></section>
{voz_banda(3)}
<section class="hoja"><div class="in"><div class="entrada sube centro"><h2>Antes de pedir plaza</h2></div>
  <div class="faq sube"><details><summary>¿Cómo empiezo?</summary><p>Rellenas el formulario, hacemos una videollamada gratuita de 30 minutos para ver tu punto de partida y, si encaja, preparo tu plan.</p></details><details><summary>¿Puedo contratar solo el entrenamiento?</summary><p>Sí: Essential y Performance son solo entrenamiento. La nutrición por separado es poco habitual.</p></details><details><summary>¿Cada cuánto revisas mi progreso?</summary><p>Cada semana o cada mes, según el programa.</p></details><details><summary>¿Y si me lesiono o me duele algo?</summary><p>Me lo dices cuanto antes y ajusto el plan. Si el dolor es agudo o no cede, te derivo a quien deba verlo.</p></details></div>
  <p class="sube" style="text-align:center;margin-top:1.5rem"><a href="dudas.html">Todas las dudas</a></p>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>¿Solo quieres un plan, sin seguimiento?</h3><p>La Puesta a punto es una consulta y un plan de 12 semanas, con lectura de tu analítica. Sin lista de espera.</p></div><div><a class="btn claro" href="puesta-a-punto.html">Ver la Puesta a punto</a></div></div></div></section>{JS_P}''', BTN + datos(('5', 'programas'), ('30 min', 'de videollamada inicial, gratis'), ('1', 'app para llevarlo todo')), ('¿Sigues dudando?', 'Cuéntame tu caso y te digo con cuál empezaría yo.'))

# ===== puesta a punto =====
FQ = [('¿Incluye seguimiento?', 'No. Es una consulta y un plan. Tienes una ronda de dudas por correo en los 7 días siguientes a la entrega.'), ('¿Cuánto tarda en llegar el plan?', 'Menos de 7 días desde la videollamada.'), ('¿Qué analítica necesito?', 'Una de los últimos 12 meses. En esta página tienes la lista de lo que conviene que incluya.'), ('¿Cómo te envío mis pruebas?', 'Por un formulario seguro, con tu consentimiento expreso. Nunca por WhatsApp.'), ('¿Se puede regalar?', 'Sí.'), ('¿Sustituye a mi médico?', 'No. No es un diagnóstico ni un tratamiento médico.')]
LDS = '<script type="application/ld+json">' + json.dumps([{'@context': 'https://schema.org', '@type': 'Service', 'name': 'Puesta a punto', 'provider': {'@type': 'Person', 'name': 'Pelayo Fernández Cidón'}, 'description': 'Consulta por videollamada, lectura de analítica y plan de entrenamiento y nutrición para 12 semanas.', 'offers': {'@type': 'Offer', 'price': '250', 'priceCurrency': 'EUR', 'url': STRIPE}}, {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FQ]}], ensure_ascii=False) + '</script>'
ANA = ['Hemograma', 'Ferritina', 'Glucosa o HbA1c', 'Perfil lipídico', 'TSH', 'Vitamina D', 'Creatinina', 'Transaminasas', 'B12 y folato']
FIJO_P = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="programas.html">Programas</a><a class="btn claro" href="{STRIPE}">Reservar por 250 €</a></div>'
BANNER = ilus('foto-banner', 'banner sube').replace('alt=""', 'alt="Pelayo Fernández Cidón, médico internista"')
if BANNER: BANNER = f'<section class="sin-arriba"><div class="in">{BANNER}</div></section>'
pagina('puesta-a-punto.html', 'Puesta a punto', 'Una consulta, un plan de 12 semanas y la lectura de tu analítica por un médico internista. Sin seguimiento. 250 €.', 'Una consulta, un plan, sin seguimiento.', 'Un médico internista lee tu analítica y tu historial, hablamos 30 minutos por videollamada y en menos de 7 días tienes tu plan de entrenamiento y nutrición para 12 semanas.', f'''
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
<section class="pasos">{ANILLOS}<div class="in"><div class="entrada sube"><h2>Cómo va</h2><p>De la reserva al plan, en cuatro pasos.</p></div>
  <ol class="cuatro">
    <li class="sube"><h3>Reservas</h3><p>Pagas con tarjeta y tu plaza queda guardada.</p></li>
    <li class="sube"><h3>Me envías tus datos</h3><p>Analítica e historial, por un formulario seguro.</p></li>
    <li class="sube"><h3>Hablamos 30 minutos</h3><p>Por videollamada: tu objetivo, tu horario y lo que dice tu analítica.</p></li>
    <li class="sube"><h3>Recibes tu plan</h3><p>En menos de 7 días, para 12 semanas. Y una ronda de dudas por correo.</p></li>
  </ol></div></section>
<section><div class="in"><div class="encaje sube" style="margin:0">
  <div><h3>Es para ti si…</h3><ul><li>Quieres un plan hecho por un médico, sin compromiso mensual</li><li>Tienes una analítica y no sabes qué hacer con ella</li><li>Te organizas bien por tu cuenta una vez sabes qué toca</li></ul></div>
  <div class="no"><h3>No es para ti si…</h3><ul><li>Tienes una enfermedad activa sin controlar</li><li>Estás embarazada o eres menor de edad</li><li>Compites y buscas la preparación de una prueba concreta</li><li>Esperas corregir un valor alterado solo con entrenamiento y dieta</li><li>Quieres acompañamiento semanal: para eso están los <a href="programas.html">programas</a></li></ul></div>
</div><p class="sube" style="color:var(--tinta-2);margin-top:1.5rem;max-width:46rem">No es un diagnóstico ni un tratamiento médico, y no sustituye a tu médico habitual.</p></div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Puesta a punto o programa</h2></div>
  <div class="tabla-marco sube"><table class="compara dosc"><thead><tr><td></td><th scope="col" class="yo">Puesta a punto</th><th scope="col">Programas</th></tr></thead><tbody>
    <tr><th scope="row">Qué es</th><td class="yo">Una consulta y un plan</td><td>Acompañamiento continuo</td></tr>
    <tr><th scope="row">Ajustes del plan</th><td class="yo">Una ronda de dudas por correo</td><td>Cada semana o cada mes</td></tr>
    <tr><th scope="row">Plaza</th><td class="yo">Sin lista de espera</td><td>Grupo pequeño, puede haber espera</td></tr>
  </tbody></table></div>
  <p class="sube" style="text-align:center;margin-top:1.5rem"><a href="programas.html">Ver los programas</a></p>
</div></section>
<section><div class="in"><div class="entrada sube centro"><h2>Antes de reservar</h2></div>
  <div class="faq sube">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FQ)}</div>
  <div class="llama sube" style="max-width:48rem;margin-inline:auto"><b>¿Es para regalar?</b><span style="flex:1;min-width:12rem;color:var(--tinta-2)">Se puede. Cuéntamelo antes de reservar.</span><a class="btn peq" href="{ESCRIBE}">Escribirme</a></div>
</div></section>
<script>(function(){{var b=document.getElementById('copia'),o=document.getElementById('copia-ok');if(!b)return;b.addEventListener('click',function(){{var t=b.dataset.t;function ok(){{o.textContent='Copiada.'}}function mal(){{var r=document.createRange();r.selectNodeContents(document.getElementById('ana'));var s=getSelection();s.removeAllRanges();s.addRange(r);o.textContent='Seleccionada: copia con tu teclado.'}}try{{navigator.clipboard.writeText(t).then(ok,mal)}}catch(e){{mal()}}}})}})();</script>''', f'<div class="cta"><a class="btn claro" href="{STRIPE}">Reservar por 250 €</a></div>' + datos(('30 min', 'de videollamada'), ('7 días', 'como mucho, y tienes el plan'), ('12 semanas', 'de plan')), ('¿Prefieres seguimiento?', 'Los programas incluyen revisión y ajustes cada semana o cada mes.'), fijo=FIJO_P, extra=LDS)

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
LDG = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Product', 'name': g[0], 'description': g[1], 'brand': 'Fuerza Basada en Evidencia', 'offers': {'@type': 'Offer', 'price': g[3].replace(',', '.'), 'priceCurrency': 'EUR', 'availability': 'https://schema.org/InStock', 'url': 'https://checkout.mailerlite.com/checkout/' + g[4]}}} for i, g in enumerate(G)]}, ensure_ascii=False) + '</script>'
JS_G = '''<script>(function(){var D=document,g=D.getElementById('filtro'),n=D.getElementById('cuantas');if(!g)return;g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.t,c=0;[].forEach.call(D.querySelectorAll('.guia'),function(a){var s=!t||(' '+a.dataset.t+' ').indexOf(' '+t+' ')>=0;a.hidden=!s;if(s){c++;a.classList.add('ya')}});n.textContent=c+(c===1?' guía':' guías')});var em=D.getElementById('emp');em.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;g.querySelector('[data-t=""]').click();[].forEach.call(D.querySelectorAll('.guia'),function(a){a.classList.remove('senal')});var a=D.getElementById('g'+b.dataset.g);a.classList.add('senal','ya');D.getElementById('emp-t').textContent='Empieza por: '+a.querySelector('h3').textContent+'.';a.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})})();</script>'''
pagina('guias.html', 'Guías', 'Guías prácticas y descargables sobre entrenamiento, fuerza y nutrición con respaldo científico.', 'Ciencia útil, lista para descargar.', 'Nueve guías prácticas sobre entrenamiento, fuerza y nutrición, con respaldo científico y pensadas para aplicarlas.', '<section><div class="in"><div class="empieza sube"><div><h2>¿Por cuál empiezo?</h2><p id="emp-t" role="status">Dime qué buscas y te señalo una.</p></div><div class="fases claras" id="emp" role="group" aria-label="Qué buscas"><button type="button" data-g="0">Tengo guardias o turnos</button><button type="button" data-g="1">Perder grasa</button><button type="button" data-g="4">Ganar músculo</button><button type="button" data-g="2">Tengo poco tiempo</button><button type="button" data-g="5">Cuidar mi salud</button></div></div><div class="barra-f sube"><div class="fases claras" id="filtro" role="group" aria-label="Filtrar por tema"><button type="button" data-t="" aria-pressed="true">Todas</button><button type="button" data-t="entreno" aria-pressed="false">Entrenamiento</button><button type="button" data-t="nutri" aria-pressed="false">Nutrición</button><button type="button" data-t="salud" aria-pressed="false">Salud</button></div><span id="cuantas" role="status">9 guías</span></div><div class="guias">' + ''.join(guia(i, g) for i, g in enumerate(G)) + f'</div><div class="calc sube" style="margin-top:3rem"><div><h3>Gratis: calculadora de proteína</h3><p>Tu rango diario según tu peso y tu fase, con reparto por comidas.</p></div><div><a class="btn claro" href="{CALC}">Abrir la calculadora</a></div></div></div></section>' + JS_G + LDG, datos(('9', 'guías'), ('5,99 €', 'la mayoría'), ('3', 'temas: entrenar, comer y salud')), ('¿Quieres que lo aplique contigo?', 'Las guías explican el porqué. En la asesoría lo llevo a tu semana.'))

# ===== newsletter =====
PLAYA = ilus('foto-playa', 'foto-p').replace('alt=""', 'alt="Pelayo en la playa"')
if PLAYA: PLAYA = f'<figure class="autor-foto">{PLAYA}<figcaption><b>Quién te escribe</b>Pelayo, fuera del hospital y del gimnasio.</figcaption></figure>'
BIMG = ['boletin-habito', 'boletin-cafeina', 'boletin-pulsaciones']
ENV = [('El hábito que movió mis marcadores', 'Lo que descubrí que les afectaba más que entrenar más duro.'), ('700 mg de cafeína sin darme cuenta', 'Cómo un médico llega ahí, y qué hice después.'), ('46 pulsaciones en reposo', 'Sin ser perfecto en nada. Qué hice y qué no.')]
pagina('newsletter.html', 'Newsletter', 'El boletín semanal de Fuerza Basada en Evidencia: entrenamiento, nutrición y salud, sin mitos.', 'Lo que sí funciona. Cada semana, en tu correo.', 'Entrenamiento, nutrición y salud con base científica. Sin mitos y sin adornos, para entrenar mejor, comer con cabeza y vivir con energía.', f'''
<section><div class="in dos alta">
  <div class="sube" id="alta"><div class="entrada" style="margin-bottom:1.5rem"><h2>Apúntate</h2><p>Un correo a la semana. Te das de baja cuando quieras.</p></div>
    <div class="ml-caja"><div class="ml-embedded" data-form="9jHHlI"></div><noscript>Activa JavaScript para ver el formulario.</noscript><p style="margin-top:.8rem;font-size:.92rem;color:var(--tinta-2)">¿No ves el formulario? <a href="https://preview.mailerlite.io/forms/1626427/158927974439061023/share">Ábrelo en otra pestaña</a>.</p></div><p style="margin-top:1rem;font-size:.92rem;color:var(--tinta-2)">Uso tu correo solo para enviarte el boletín. <a href="{PRIV}">Política de privacidad</a>.</p></div>
  <div class="sube"><h3 style="margin-bottom:1.2rem">Qué te llega</h3><ul class="marcas" style="font-size:1.08rem;gap:.9rem"><li><strong>Una idea por correo</strong>, para aplicarla esa semana.</li><li><strong>Lo que me pasa a mí</strong>: lo que pruebo, lo que mido y en qué me equivoco.</li><li><strong>La evidencia detrás</strong>, sin tecnicismos de más.</li></ul>{PLAYA}</div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Lo último que he enviado</h2></div>
  <div class="boletin">{''.join(f'<article class="correo sube">{ilus(BIMG[ENV.index((t, d))], "foto-b")}<p class="de"><span class="cara peq">PF</span><span><b>Pelayo, de FBE</b><small>Asunto</small></span></p><h3>{t}</h3><p>{d}</p></article>' for t, d in ENV)}</div>
</div></section>
<script>(function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[]).push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');ml('account','1626427');</script>''', f'<div class="cta"><a class="btn claro" href="#alta">Suscribirme</a></div>')

# ===== dudas =====
D = [('Cómo funciona', [('¿En qué consiste el servicio?', 'Planes de entrenamiento y nutrición a medida que se llevan desde la app, con contacto directo conmigo, corrección de tu técnica en vídeo, check-ins semanales y guías para entender lo que haces. Antes de empezar hacemos una videollamada gratuita.'), ('¿Puedo contratar solo una parte?', 'El entrenamiento se puede contratar solo. La nutrición por separado es poco habitual.'), ('¿Qué formación tiene Pelayo?', 'Especialista en Medicina Interna, experto universitario en entrenamiento de fuerza y máster en nutrición clínica.')]),
 ('Entrenamiento', [('¿Cuántos días a la semana debo entrenar?', 'Depende de tu disponibilidad, tu nivel y tu objetivo. La mayoría de mis atletas entrena entre 3 y 5 días.'), ('¿Por qué no hago siempre los mismos ejercicios?', 'Se cambian con criterio, cada 12 a 16 semanas o cuando dejan de darte resultado.'), ('¿Por qué repito algunos ejercicios varias semanas?', 'Porque mantenerlos permite progresar en carga y medir de forma objetiva si avanzas.'), ('¿Hay que llegar al fallo en cada serie?', 'No. Lo habitual es quedarse a entre 1 y 3 repeticiones del fallo.'), ('¿Tengo que calentar siempre?', 'Sí, pero poco: algo de movilidad y series progresivas del primer ejercicio.'), ('¿Y si un día no puedo completar el entrenamiento?', 'Se mueve, se acorta o se salta. La constancia importa más que una sesión suelta.')]),
 ('Nutrición', [('¿Debo seguir un menú fijo?', 'No. Prefiero pautas flexibles y hábitos, porque son los que se sostienen.'), ('¿Qué suplementos debería tomar?', 'Para la mayoría: cafeína en dosis controladas, proteína en polvo si no llegas con la comida y creatina monohidrato. El resto, caso a caso.'), ('¿Cómo cuento las calorías si como fuera?', 'Con estimaciones visuales y estrategias de ración. La app te da además una pauta para cuadrar el día.'), ('¿Qué como en una guardia, un turno de noche o un viaje?', 'Comidas planificadas, tentempiés ricos en proteína, alimentos que aguanten sin nevera y cafeína bien colocada.'), ('¿Debo pesarme todos los días?', 'No. El peso es una herramienta más, junto con las fotos, la fuerza, las medidas y cómo te encuentras.')]),
 ('Motivación', [('¿Y si no tengo ganas de entrenar?', 'Empieza por el calentamiento, o baja el volumen o la intensidad ese día. El hábito gana a la motivación.'), ('¿Y si no veo resultados rápido?', 'Los resultados piden tiempo y constancia. Trabajamos con expectativas realistas y con el foco en el proceso.')]),
 ('Soporte y cambios', [('¿Cómo me comunico contigo?', 'Según tu programa: por la app, por correo o por WhatsApp, con respuesta en 24 a 48 horas.'), ('¿Cada cuánto revisas mi progreso?', 'Cada semana o cada mes, según el programa.'), ('¿Qué hago si me lesiono o me duele algo?', 'Me lo dices cuanto antes y ajusto el plan. Si el dolor es agudo o no cede, te derivo a quien deba verlo.'), ('¿Puedo cambiar el orden de los ejercicios o el día?', 'Sí, dentro de un margen. Un cambio puntual no es problema; si se repite, lo revisamos juntos.'), ('¿Cómo sé si progreso?', 'Por las cargas, las repeticiones, la técnica, la recuperación, cómo te notas y tus medidas.')])]
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
open(f'{SAL}/favicon.svg', 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 1254"><rect width="1254" height="1254" rx="280" fill="#593EDE"/><g transform="translate(627 627) scale(.82) translate(-627 -628)"><path fill="#fff" fill-rule="evenodd" d="{LD}"/></g></svg>')
open(f'{SAL}/404.html', 'w', encoding='utf-8').write(f'''{cabeza('404.html', 'Página no encontrada', 'Esta página no existe.', '<meta name="robots" content="noindex">')}
{cabecera()}
<header class="hero mini t-404" id="inicio">{ANILLOS}{ilus("web-404")}<div class="in"><div class="txt"><p class="num404" aria-hidden="true">404</p><h1>Aquí no hay nada.</h1><p class="sub">La página que buscas no existe o ha cambiado de sitio. Estas sí están:</p><div class="cta"><a class="btn claro" href="index.html">Ir al inicio</a><a class="enl" href="programas.html">Programas</a><a class="enl" href="guias.html">Guías</a><a class="enl" href="dudas.html">Dudas</a></div></div></div></header>
<main id="contenido"></main>
{PIE}
<script src="fbe.js"></script></body></html>''')
# Politica de privacidad propia: texto de su pagina de MailerLite (sept. 2026); el 20/11/2026 Pelayo pidio cambiar el alojamiento de la web a GitHub. Solo se genera si hay FBE_CORREO.
if os.environ.get('FBE_CORREO'):
    C = os.environ['FBE_CORREO']; CM = f'<a href="mailto:{C}">{C}</a>'
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
<p>No compartimos tus datos con terceros con fines comerciales. Trabajamos únicamente con proveedores tecnológicos que actúan como encargados del tratamiento y cumplen el RGPD (como MailerLite para email, GitHub para alojar esta web, Calendly para reservas y Stripe para pagos). Algunos de estos proveedores pueden alojar datos fuera del Espacio Económico Europeo; en esos casos, el tratamiento se ampara en garantías adecuadas como las cláusulas contractuales tipo aprobadas por la Comisión Europea.</p>
<h2>Tus derechos</h2>
<p>Puedes ejercer en cualquier momento tus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar tu consentimiento, escribiendo a {CM}. También tienes derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es">aepd.es</a>) si consideras que el tratamiento no se ajusta a la normativa.</p>
<h2>Seguridad</h2>
<p>Aplicamos medidas técnicas y organizativas para proteger tu información, incluido el almacenamiento de la documentación clínica en sistemas con acceso restringido.</p>
<p><small>Última actualización: noviembre de 2026.</small></p>
</div></div></section>"""
    open(f'{SAL}/privacidad.html', 'w', encoding='utf-8').write(f"""{cabeza('privacidad.html', 'Política de privacidad', 'Qué datos trata Fuerza Basada en Evidencia, para qué, cuánto tiempo y cómo ejercer tus derechos.')}
{cabecera()}
<header class="hero mini t-privacidad" id="inicio">{ANILLOS}<div class="marca-agua">{LOBO}</div><div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / Privacidad</span><h1>Política de privacidad</h1><p class="sub">Qué datos trato, para qué, cuánto tiempo los guardo y cómo ejercer tus derechos.</p></div></div></header>
<main id="contenido">{PRIV_TXT}</main>
{PIE}
<script src="fbe.js"></script></body></html>""")
open(f'{SAL}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{WEB}{u}</loc></url>\n' for u in [''] + [u for u, _ in PAGS] + (['privacidad.html'] if os.environ.get('FBE_CORREO') else [])) + '</urlset>\n')
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
_FF = '<link rel="preload" href="img/archivo.woff2" as="font" type="font/woff2" crossorigin><style>@font-face{font-family:"Archivo";src:url(img/archivo.woff2) format("woff2");font-weight:400 800;font-stretch:75% 125%;font-display:swap}</style>'
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
# CSS sin comentarios (mas ligero)
_c = open(f'{SAL}/fbe.css', encoding='utf-8').read()
_c2 = _re.sub(r'/\*.*?\*/', '', _c, flags=_re.S)
_c2 = _re.sub(r'\n\s*\n+', '\n', _c2)
open(f'{SAL}/fbe.css', 'w', encoding='utf-8').write(_c2)
