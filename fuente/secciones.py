# ===== secciones nuevas (21/11/2026): Empieza aquí, Vídeos, Para profesionales y Mitos y evidencia =====
# Se ejecuta desde interior.py justo después de herramientas.py (antes del sitemap). No van en el menú: se enlazan desde el pie,
# la portada, Herramientas, Guías, Quién soy y Pauta Activa. «En los medios» espera los enlaces reales (MEDIOS vacío = no se genera).
# Mitos: cada cifra lleva su fuente en la tarjeta; no cambiar números sin cambiar la fuente.
import urllib.parse as _up
import re as _re

I.update({
    'brujula': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    'play': '<rect x="2.5" y="5" width="19" height="14" rx="3.5"/><path d="M10 9v6l5-3z"/>',
    'micro': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/>',
    'fonendo': '<path d="M6 3v5a4 4 0 0 0 8 0V3"/><path d="M10 12v3a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/>',
    'bombilla': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
})

# «Anterior / Siguiente» de las paginas que no estan en el menu
SEC_SIG = {'empieza-aqui.html': (('index.html', 'Inicio'), ('quien-soy.html', 'Quién soy')),
           'mitos.html': (('guias.html', 'Guías'), ('newsletter.html', 'Newsletter')),
           'videos.html': (('newsletter.html', 'Newsletter'), ('herramientas.html', 'Herramientas')),
           'profesionales.html': (('herramientas.html', 'Herramientas'), ('pauta-activa.html', 'Pauta Activa')),
           'medios.html': (('quien-soy.html', 'Quién soy'), ('videos.html', 'Vídeos'))}
_sigue_h = sigue
def sigue(arch, padre=None):
    if arch in SEC_SIG and not padre:
        a, b = SEC_SIG[arch]
        return f'<nav class="sigue" aria-label="Seguir leyendo"><div class="in"><a href="{a[0]}"><small>Anterior</small><b>{a[1]}</b></a><a class="der" href="{b[0]}"><small>Siguiente</small><b>{b[1]}</b></a></div></nav>'
    return _sigue_h(arch, padre)

HM = {u: (sl, i, t, d) for u, sl, i, t, d in HERR_MAS}
YT = dict(REDES)['YouTube']
MAILTO = ('mailto:' + _ent(os.environ['FBE_CORREO'])) if os.environ.get('FBE_CORREO') else ''
def sec_ic(n): return f'<i class="sec-ic">{ico(n)}</i>'
def _ext(u): return ' target="_blank" rel="noopener"' if u.startswith('http') else ''

# En los medios (lista arriba porque Profesionales y Quién soy enlazan a la página si existe; la página se monta en el punto 5)
MEDIOS = [  # (medio, tipo: 'Prensa' | 'Podcast' | 'Formación', título, url, fecha o '')
    ('AS · Tikitakas', 'Prensa', 'Pelayo Fernández, médico: «Si no bebes alcohol, no empieces. No hay ninguna razón de salud para hacerlo»',
     'https://as.com/tikitakas/salud/pelayo-fernandez-medico-si-no-bebes-alcohol-no-empieces-no-hay-ninguna-razon-de-salud-para-hacerlo-f202611-n/', 'noviembre de 2026'),
    ('Vozpópuli', 'Prensa', 'Pelayo Fernández Cidón, médico: «Hay cuatro pruebas que predicen cómo vas a envejecer y la mayoría de las personas mayores de 40 no las pasa, y esto no sale en las analíticas»',
     'https://www.vozpopuli.com/bienestar/pelayo-fernandez-cidon-medico-hay-cuatro-pruebas-que-predicen-como-vas-a-envejecer-y-la-mayoria-de-las-personas-mayores-de-40-no-las-pasa-y-esto-no-sale-en-las-analiticas.html', 'noviembre de 2026'),
    ('Libertad Digital', 'Prensa', 'Esteroides, un cóctel letal: así destrozan el corazón, el hígado y los riñones de los culturistas',
     'https://www.libertaddigital.com/deportes/mas-deporte/2025-09-27/esteroides-un-coctel-letal-asi-destrozan-el-corazon-el-higado-y-los-rinones-de-los-culturistas-7299778/', '27/09/2025'),
    ('Podcast de Borja Bandera', 'Podcast', 'El PRIMER signo de envejecer mal NO está en la analítica (3 pruebas que casi nadie pasa a los 40)', 'https://www.youtube.com/watch?v=vkqBWbCNVOs', ''),
    ('Dr. Antitabaco (Dr. Paul Freund)', 'Podcast', 'Experto en ejercicio físico desmiente mitos sobre proteína y creatina', 'https://www.youtube.com/watch?v=N4uZ0dNjD4M', ''),
    ('SEMI · Grupo de Cronicidad y Pluripatología', 'Formación', 'Minipíldora «Beneficios de la prescripción de ejercicio físico»',
     'https://www.fesemi.org/nueva-minipildora-cargo-de-dr-pelayo-cidon-con-titulo-beneficios-de-la-prescripcion-de-ejercicio', ''),
    ('SEMI · Grupo de Cronicidad y Pluripatología', 'Formación', 'Minipíldora «Prescripción de ejercicio aeróbico»',
     'https://www.fesemi.org/nueva-minipildora-bajo-el-titulo-prescripcion-de-ejercicio-aerobico', ''),
]

# ---------------------------------------------------------------------------------------------
# 1. Empieza aquí: elige el perfil que se parece al tuyo y te marca tres o cuatro pasos por la web
def ea_paso(n, u, ic_, t, d):
    return f'<li><a class="ea-paso" href="{u}"{" rel=\"noopener\"" if u.startswith("http") else ""}><span class="ea-n">{n:02d}</span>{sec_ic(ic_)}<b>{t}</b><span>{d}</span></a></li>'
def _h(u): return HM[u][1]
EA_PERF = [
    ('cero', 'Nunca he entrenado fuerza', 'Lo básico, sin prisa. Primero, comprobar que puedes empezar por tu cuenta.', [
        ('revision-medica.html', _h('revision-medica.html'), '¿Necesito pasar por el médico?', 'Unas preguntas del algoritmo del ACSM y te dice si puedes empezar ya o conviene consultar antes.'),
        ('guias.html', 'libro', 'Elige una guía para empezar', 'La rutina minimalista parte de dos días por semana; la de recomposición está pensada para quien empieza.'),
        (CALC, 'plato', 'Calcula tu proteína', 'Tu rango diario según tu peso y tu fase, con reparto por comidas.'),
        ('programas.html', 'pesa', 'O que te lo monte yo', 'Un plan a tu medida dentro de la app, revisado cada semana.')]),
    ('sinplan', 'Ya entreno, pero sin plan', 'Pon números a lo que ya haces: cuánto mueves, cuántas series y si te sobra o te falta.', [
        ('calculadora-1rm.html', _h('calculadora-1rm.html'), 'Calcula tu 1RM', 'Con un peso y tus repeticiones: tu máximo estimado y la tabla de cargas.'),
        ('volumen-semanal.html', _h('volumen-semanal.html'), 'Cuenta tus series por músculo', 'Series semanales por músculo, contadas como en los estudios.'),
        ('mitos.html', 'bombilla', 'Quita lo que sobra', 'Nueve ideas de gimnasio contrastadas con los estudios.'),
        ('programas.html', 'pesa', 'Un plan con revisión semanal', 'Si quieres dejar de improvisar, lo montamos juntos.')]),
    ('medicacion', 'Tomo medicación o tengo una enfermedad crónica', 'Antes de pensar en la intensidad, mira qué cambia tu medicación durante el ejercicio.', [
        ('revision-medica.html', _h('revision-medica.html'), '¿Necesito pasar por el médico?', 'El cribado del ACSM, con un texto para copiar y llevar a tu consulta.'),
        ('pauta-activa.html', 'capsula', 'Revisa tu medicación con Pauta Activa', 'Qué tener en cuenta con tus fármacos al hacer ejercicio, con la fuente de cada regla.'),
        ('zonas-pulso.html', _h('zonas-pulso.html'), 'Tus zonas de pulso', 'Y cómo guiarte si tu medicación cambia el pulso.'),
        ('puesta-a-punto.html', 'check', 'Un plan hecho por un médico', 'La Puesta a punto: consulta y plan de 12 semanas, con lectura de tu analítica.')]),
    ('mayores', 'Tengo más de 60 años, o busco algo para mis padres', 'Mide cómo estás hoy para tener un punto de partida, y empieza desde ahí.', [
        ('test-sppb.html', _h('test-sppb.html'), 'Haz el test SPPB', 'Equilibrio, marcha y levantarse de la silla, con la puntuación y lo que significa.'),
        ('test-silla.html', _h('test-silla.html'), 'Test de la silla en 30 segundos', 'Con cronómetro, contador y los valores de referencia de 60 a 94 años.'),
        ('revision-medica.html', _h('revision-medica.html'), '¿Hace falta pasar por el médico?', 'Unas preguntas del algoritmo del ACSM antes de empezar.'),
        ('puesta-a-punto.html', 'check', 'Un plan hecho por un médico', 'Consulta y plan de 12 semanas, con lectura de la analítica.')]),
    ('dolor', 'Me duele algo al entrenar', 'Molestia no siempre significa parar. Lo importante es saber dosificar.', [
        ('semaforo-dolor.html', _h('semaforo-dolor.html'), 'El semáforo del dolor', 'Hasta dónde puedes seguir entrenando con molestias y cuándo conviene bajar.'),
        ('mitos.html#artrosis', 'bombilla', '¿Y si es artrosis?', 'Lo que dice la guía clínica sobre el ejercicio en la artrosis de rodilla.'),
        ('puesta-a-punto.html', 'check', 'Que lo mire un médico', 'Si quieres un plan individual con tu historia delante.')]),
    ('paron', 'Vuelvo después de un parón', 'Mira cuánto has podido perder y vuelve con cargas realistas.', [
        ('paron.html', _h('paron.html'), '¿Cuánto he perdido?', 'Lo que dicen los estudios según las semanas parado y tu edad.'),
        ('calculadora-1rm.html', _h('calculadora-1rm.html'), 'Recalcula tus cargas', 'Tu 1RM de hoy, no el de antes del parón.'),
        ('volumen-semanal.html', _h('volumen-semanal.html'), 'Ajusta tus series', 'Cuántas series por músculo para volver sin pasarte.'),
        ('programas.html', 'pesa', 'Vuelve con un plan', 'Lo ajusto cada semana según cómo responde tu cuerpo.')]),
]
EA_TRES = [('Aprender', 'libro', [('guias.html', 'Guías'), ('newsletter.html', 'Newsletter'), ('videos.html', 'Vídeos'), ('mitos.html', 'Mitos y evidencia'), ('dudas.html', 'Dudas')]),
           ('Medir', 'grafica', [('herramientas.html', 'Todas las herramientas'), ('pauta-activa.html', 'Pauta Activa'), (CALC, 'Calculadora de proteína'), ('test-sppb.html', 'Test SPPB'), ('calculadora-1rm.html', 'Calculadora de 1RM')]),
           ('Trabajar conmigo', 'chat', [('programas.html', 'Programas'), ('puesta-a-punto.html', 'Puesta a punto'), (FORM, 'Pedir plaza'), ('quien-soy.html', 'Quién soy')])]
EA_IMG_OK = _todas(*[f'ea-{p}' for p, _, _, _ in EA_PERF])  # bloque W10: una imagen por perfil, solo si estan las seis
EA_ICO = {'cero': 'pesa', 'sinplan': 'grafica', 'medicacion': 'capsula', 'mayores': 'andar', 'dolor': 'semaforo', 'paron': 'pausa'}  # 5x50 (1): icono por perfil
EA_JS = r'''(function(){var g=document.getElementById('ea-perfil');if(!g)return;var bs=[].slice.call(g.querySelectorAll('button')),rs=[].slice.call(document.querySelectorAll('.ea-ruta')),quieto=matchMedia('(prefers-reduced-motion: reduce)').matches;
function pon(p,url){if(!rs.some(function(r){return r.dataset.p===p}))return false;bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.p===p)});rs.forEach(function(r){var v=r.dataset.p===p;if(v&&r.hidden&&url){r.classList.remove('ea-entra');void r.offsetWidth;r.classList.add('ea-entra')}r.hidden=!v});if(url){try{history.replaceState(null,'','#'+p)}catch(e){}}return true}
bs.forEach(function(b){b.addEventListener('click',function(){pon(b.dataset.p,true);if(innerWidth<760){var r=document.querySelector('.ea-ruta[data-p="'+b.dataset.p+'"]');if(r&&r.getBoundingClientRect().top>innerHeight*.6)r.scrollIntoView({behavior:quieto?'auto':'smooth',block:'start'})}})});
document.querySelectorAll('.ea-volver').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();g.scrollIntoView({behavior:quieto?'auto':'smooth',block:'center'});var b=g.querySelector('[aria-pressed="true"]');if(b)b.focus({preventScroll:true})})});
if(!pon(location.hash.slice(1)))pon(bs[0].dataset.p);addEventListener('hashchange',function(){pon(location.hash.slice(1))});})();'''
pagina('empieza-aqui.html', 'Empieza aquí', 'Por dónde empezar en Fuerza Basada en Evidencia según tu caso: nunca has entrenado, entrenas sin plan, tomas medicación, tienes más de 60 años, te duele algo o vuelves de un parón.',
       'Empieza aquí.', 'Dime cuál se parece más a ti y te señalo qué mirar primero. Son tres o cuatro pasos, en orden.', f'''
<section><div class="in">
  <div class="empieza sube"><div><h2>¿Cuál se parece más a ti?</h2><p>Elige uno. Puedes cambiar cuando quieras.</p></div>
    <div class="fases claras" id="ea-perfil" role="group" aria-label="Tu caso">{"".join(f'<button type="button" data-p="{p}" aria-pressed="{"true" if k == 0 else "false"}"><i class="ea-bi">{ico(EA_ICO[p])}</i><span>{t}</span></button>' for k, (p, t, _, _) in enumerate(EA_PERF))}</div></div>
  {"".join(f'<div class="ea-ruta sube" data-p="{p}"><div class="ea-top"><div><span class="ea-kick">Tu ruta · {len(xs)} pasos</span><h3>{t}</h3><p>{d}</p></div>{ilus(f"ea-{p}", "ea-img") if EA_IMG_OK else ""}</div><ol class="ea-pasos">{"".join(ea_paso(n + 1, *x) for n, x in enumerate(xs))}</ol><a class="ea-volver" href="#ea-perfil">Elegir otro caso</a></div>' for p, t, d, xs in EA_PERF)}
</div></section>
<section class="hoja" id="ea-todo"><div class="in"><div class="entrada sube"><h2>Todo lo que hay en la web</h2><p>En tres verbos, por si prefieres ir a tu aire.</p></div>
  <div class="ea-tres">{"".join(f'<div class="ea-col sube" data-n="{len(xs)}">{sec_ic(i)}<h3>{t}</h3><ul>{"".join(f"<li><a href=\"{u}\"{_ext(u)}>{n}</a></li>" for u, n in xs)}</ul></div>' for t, i, xs in EA_TRES)}</div>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>Si solo vas a hacer una cosa</h3><p>Apúntate al boletín: una idea cada semana sobre fuerza, nutrición y salud.</p></div><div><a class="btn claro" href="newsletter.html">Ver el boletín</a></div></div></div></section>
<script>{EA_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="#ea-perfil">Elegir mi caso</a><a class="enl" href="#ea-todo">Ver todo lo que hay</a></div>')

# ---------------------------------------------------------------------------------------------
# 2. Vídeos: la lista «subidas» del canal (UC... -> UU...) tras una fachada; YouTube solo se carga al pulsar
VID_LISTA = 'UUiE1T4Z2KiaKSw88mg7k6CQ'
VID_SRC = f'https://www.youtube-nocookie.com/embed/videoseries?list={VID_LISTA}&amp;rel=0&amp;autoplay=1'
VID_TEMAS = ['Fuerza', 'Proteína', 'Creatina', 'Suplementos', 'Alcohol', 'Sueño', 'Colesterol', 'Cardio', 'Perder grasa', 'Mayores', 'Mujer', 'Mitos']
VID_JS = r'''(function(){var a=document.getElementById('vid');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src=a.dataset.src;f.title='Últimos vídeos de Fuerza Basada en Evidencia en YouTube';f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';var d=document.createElement('div');d.className='vid-marco vid-on';d.appendChild(f);a.replaceWith(d);});})();'''
_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.5 5.8v12.4L19 12z"/></svg>'
_CAMPANA = '<svg class="vid-mini" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20a2 2 0 0 0 4 0"/></svg>'
_LUPA = '<svg class="vid-mini" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>'
pagina('videos.html', 'Vídeos', 'Los vídeos de Fuerza Basada en Evidencia en YouTube: fuerza, nutrición y salud explicadas por un médico internista.',
       'Lo que publico en YouTube.', 'Fuerza, nutrición y salud, explicadas por un médico internista. Aquí tienes los últimos vídeos del canal y los temas para buscar.', f'''
<section><div class="in">
  <a class="vid-marco sube" id="vid" href="{YT}/videos" data-src="{VID_SRC}" target="_blank" rel="noopener">{ilus("videos-fondo", "vid-fondo")}<span class="vid-chip">Lista del canal</span><span class="vid-boton">{_PLAY}</span><span class="vid-txt"><b>Ver los últimos vídeos del canal</b><small>Al pulsar se carga el reproductor de YouTube, en modo de privacidad mejorada.</small></span></a>
  <div class="vid-cta sube"><a class="btn vid-ir" href="{YT}"{_ext(YT)}>Ir al canal</a><a class="btn hueco vid-sus" href="{YT}?sub_confirmation=1"{_ext(YT)}>{_CAMPANA}Suscribirme</a></div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Busca por tema</h2><p>Cada tema abre la búsqueda dentro del canal. O escribe el tuyo.</p></div>
  <form class="vid-busca sube" action="{YT}/search" method="get" target="_blank" rel="noopener" role="search"><label class="oculto" for="vid-q">Buscar en el canal</label>{_LUPA}<input id="vid-q" name="query" type="search" placeholder="Rodilla, sueño, proteína…" autocomplete="off" required><button class="btn" type="submit">Buscar</button></form>
  <ul class="vid-temas sube">{"".join(f'<li><a href="{YT}/search?query={_up.quote(t)}"{_ext(YT)}>{t}</a></li>' for t in VID_TEMAS)}</ul>
</div></section>
<section><div class="in"><div class="entrada sube"><h2>Del vídeo a tu semana</h2><p>Un vídeo te da la idea. Lo que cambia las cosas es aplicarla.</p></div>
  <ol class="pasos-g en-linea vid-pasos sube">
    <li>{sec_ic("video")}<b>Ves el vídeo</b><span>Una idea concreta sobre fuerza, nutrición o salud.</span></li>
    <li>{sec_ic("grafica")}<b>Lo pruebas en tu caso</b><span>Con las <a href="herramientas.html">herramientas de la web</a> o con una <a href="guias.html">guía</a>.</span></li>
    <li>{sec_ic("pesa")}<b>Si quieres, lo llevamos a tu semana</b><span>En la <a href="programas.html">asesoría</a> lo convierto en tu plan y lo reviso cada semana.</span></li>
  </ol>
  <div class="vid-redes sube"><b>También estoy en</b>{"".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in REDES if t != 'YouTube')}</div>
</div></section>
<section class="hoja"><div class="in"><div class="calc sube"><div><h3>¿Prefieres leerlo?</h3><p>En el boletín te llega una idea cada semana sobre fuerza, nutrición y salud.</p></div><div><a class="btn claro" href="newsletter.html">Ver el boletín</a></div></div></div></section>
<script>{VID_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="#vid">Ver los vídeos</a><a class="enl" href="#vid-q">Buscar un tema</a></div>')

# ---------------------------------------------------------------------------------------------
# 3. Para profesionales sanitarios: Pauta Activa en consulta, herramientas con fuente, recursos para pacientes y charlas
_PM = PA_PARA[1]
PRO_HERR = [('revision-medica.html', 'Cribado antes del ejercicio', 'Algoritmo del ACSM 2015 (Riebe), con texto para copiar y llevar al médico.', 'ACSM 2015'),
            ('test-sppb.html', 'Test SPPB guiado', 'Guralnik 1994 y 2000, punto de corte de EWGSOP2 y niveles de Vivifrail.', 'Guralnik · EWGSOP2'),
            ('test-silla.html', 'Test de la silla en 30 segundos', 'Valores normales de Rikli y Jones (1999) y umbral de autonomía (2013).', 'Rikli y Jones'),
            ('zonas-pulso.html', 'Zonas de pulso con medicación', 'Tanaka, tramos del ACSM y aviso cuando un fármaco invalida el pulso como guía.', 'Tanaka · ACSM'),
            ('semaforo-dolor.html', 'Semáforo del dolor', 'Modelo de Thomeé (1997) y Silbernagel (2007), con diario.', 'Thomeé · Silbernagel'),
            ('suplementos.html', 'Suplementos con evidencia', 'Grupos del AIS y dosis del consenso del COI de 2018.', 'AIS · COI 2018')]
PRO_FORMATOS = ['Sesión clínica', 'Curso', 'Jornadas']  # 5x50 (tanda 2): los mismos formatos que nombra el texto
_SOBRE = '<svg class="vid-mini" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>'
PRO_JS = r'''(function(){var q=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('.pro-copia').forEach(function(b){b.addEventListener('click',function(){var u=new URL(b.dataset.u,location.href).href,s=b.querySelector('span'),t=s.textContent;function ok(){b.classList.add('hecho');s.textContent='Copiado';setTimeout(function(){b.classList.remove('hecho');s.textContent=t},1600)}if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(ok,function(){prompt('Copia el enlace:',u)});else prompt('Copia el enlace:',u)})});
var cs=document.querySelectorAll('.pro-cif b[data-v]');if(q||!('IntersectionObserver' in window))return;cs.forEach(function(b){b.textContent='0'});var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var b=e.target,v=+b.dataset.v,t0=performance.now();(function paso(t){var k=Math.min(1,(t-t0)/900);b.textContent=Math.round(v*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(paso)})(t0)})},{threshold:.4});cs.forEach(function(b){io.observe(b)});})();'''
PRO_TEMAS = ['Fuerza en el paciente crónico y polimedicado: por dónde empezar.',
             'Fármacos y ejercicio: qué cambia el pulso, la tensión o la glucosa durante el esfuerzo.',
             'Valoración funcional en consulta: SPPB y test de la silla.',
             'Ejercicio en la persona mayor y prevención de la fragilidad.',
             'Proteína y masa muscular con la edad.',
             'Dolor persistente: cómo dosificar la carga.']
PRO_CRED = ['Especialista en Medicina Interna', 'Experto universitario en entrenamiento de fuerza', 'Máster en nutrición clínica', 'Más de 15 años entrenando fuerza']
_G0 = G[0]
_MAIL_S = (MAILTO + '?subject=' + _up.quote('Sesión o formación')) if MAILTO else FORM
_FIJO_PRO = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="pauta-activa.html">Pauta Activa</a><a class="btn claro" href="#charlas">Charlas</a></div>'
def pro_tarj(u, t, d, fu):
    sl, i, _, _ = HM[u]
    return f'<a class="herr-mini pro-herr" href="{u}">{ilus(f"herr-{sl}", "herr-mini-img") or f"<i class=\"ic\">{ico(i)}</i>"}<b>{t}</b><span>{d}</span><em class="pro-fuente">{fu}</em></a>'
def pro_li(u, n):
    return f'<li><a href="{u}">{n}</a><button type="button" class="pro-copia" data-u="{u}" aria-label="Copiar el enlace de {n}"><span>Copiar enlace</span></button></li>'
PRO_IND = [('#pauta', 'Pauta Activa'), ('#herramientas', 'Herramientas'), ('#pacientes', 'Para tus pacientes'), ('#charlas', 'Charlas y formación')]
pagina('profesionales.html', 'Para profesionales sanitarios', 'Para médicos, enfermería, farmacia y fisioterapia: Pauta Activa en consulta, herramientas con la fuente al pie y charlas sobre fuerza y medicación.',
       'Para profesionales sanitarios.', 'Soy médico internista. Esto es lo que te puede servir en la consulta, y cómo escribirme si quieres una sesión o una charla para tu equipo.', f'''
<section id="pauta"><div class="in"><nav class="pro-indice sube" aria-label="En esta página"><b>En esta página</b>{"".join(f'<a href="{h}">{t}</a>' for h, t in PRO_IND)}</nav></div><div class="in pro-dos">
  <div class="sube">{ilus("pa-logo", "pro-logo")}<div class="entrada"><h2>Pauta Activa en tu consulta</h2></div><p class="pro-lead">{_PM[2]}</p>
    <ul class="marcas pro-marcas">{"".join(f"<li>{x}</li>" for x in _PM[3])}</ul>
    <div class="vid-cta"><a class="btn" href="{PA}" rel="noopener">Abrir Pauta Activa</a><a class="btn hueco" href="pauta-activa.html">Ver qué hace</a></div></div>
  <div class="sube"><ul class="pro-cif">{"".join(f"<li><b data-v=\"{n}\">{n}</b><span>{t}</span></li>" for n, t in PA_CIF)}</ul><p class="pro-nota">{PA_NO[0][0]} {PA_NO[0][1]}</p></div>
</div></section>
<section class="hoja" id="herramientas"><div class="in"><div class="entrada sube"><h2>Herramientas con la fuente al pie</h2><p>Cada una cita de dónde salen sus números.</p></div>
  <p class="pro-priv sube">{ico("candado")}<span>Gratis y en el navegador: no se envía ningún dato del paciente.</span></p>
  <div class="herr-mas-rej sube">{"".join(pro_tarj(*x) for x in PRO_HERR)}</div>
</div></section>
<section id="pacientes"><div class="in"><div class="entrada sube"><h2>Para tus pacientes</h2><p>Lo que puedes recomendar en la consulta. Copia el enlace y pásaselo.</p></div>
  <div class="pro-pac">
    <div class="ea-col sube">{sec_ic("libro")}<h3>Para aprender por su cuenta</h3><ul class="pro-lista">{pro_li("herramientas.html", "Herramientas")}{pro_li("mitos.html", "Mitos y evidencia")}{pro_li("videos.html", "Vídeos")}{pro_li("newsletter.html", "Newsletter")}</ul></div>
    <div class="ea-col sube">{sec_ic("check")}<h3>Si necesitan un plan individual</h3><ul class="pro-planes"><li><a href="puesta-a-punto.html">Puesta a punto</a>: consulta y plan de 12 semanas, con lectura de su analítica.</li><li><a href="programas.html">Asesoría</a>: plan de fuerza y nutrición en la app, revisado cada semana.</li></ul></div>
  </div>
</div></section>
<section class="hoja"><div class="in"><div class="calc sube pro-guardias">{ilus(GIMG[0], "pro-guia")}<div><h3>¿Tú también haces guardias?</h3><p>La guía «{_G0[0]}» es para {_G0[2][0].lower() + _G0[2][1:-1]}: {_G0[1].split(": ", 1)[1]}</p></div><div><a class="btn claro" href="guias.html">Ver la guía</a></div></div></div></section>
<section id="charlas"><div class="in pro-dos">
  <div class="sube"><div class="entrada"><h2>Sesiones, charlas y formación</h2></div><p class="pro-lead">Si organizas una sesión clínica, un curso o unas jornadas, puedo hablar de fuerza y medicación con casos reales. Cuéntame el público, el formato y la fecha, y te digo si puedo.</p>
    <ul class="pro-formatos">{"".join(f"<li>{x}</li>" for x in PRO_FORMATOS)}</ul>
    <ul class="pro-cred">{"".join(f"<li>{x}</li>" for x in PRO_CRED)}</ul>
    <div class="vid-cta"><a class="btn" href="{_MAIL_S}">{_SOBRE}Escribirme</a></div>{'<p class="sec-enl"><b>Entrevistas y formación</b><a href="medios.html">En los medios</a></p>' if len(MEDIOS) >= 2 else ''}</div>
  <div class="sube">{ilus("pro-charlas", "pro-img")}<h3 class="pro-h3">{sec_ic("micro")}Algunos temas</h3><ul class="pro-temas">{"".join(f"<li>{x}</li>" for x in PRO_TEMAS)}</ul></div>
</div></section>
<script>{PRO_JS}</script>''', cta=f'<div class="cta"><a class="btn claro" href="{PA}" rel="noopener">Abrir Pauta Activa</a><a class="enl" href="#charlas">Charlas y formación</a></div>',
       cierre_t=('¿Y tú, entrenas?', 'Los sanitarios también tenemos guardias y poco tiempo. Cuéntame tu caso.'), fijo=_FIJO_PRO)

# ---------------------------------------------------------------------------------------------
# 4. Mitos y evidencia (fuentes comprobadas el 21/11/2026)
MITO_VER = {'f': 'Falso', 'a': 'A medias', 'n': 'No demostrado'}
MITO_T = [('', 'Todos'), ('entreno', 'Entrenamiento'), ('nutri', 'Nutrición'), ('salud', 'Salud'), ('mayores', 'Mayores')]
MITOS = [
    ('estirar', 'entreno salud', 'Estirar antes de entrenar evita lesiones.', 'f', '', 'Metaanálisis',
     'Un metaanálisis de 25 ensayos con más de 26 000 participantes no encontró que estirar previniera lesiones. Lo que sí las redujo fue el entrenamiento de fuerza: a menos de un tercio. Estirar puede servirte para ganar movilidad, no como seguro contra lesiones.',
     'Lauersen JB, Bertelsen DM, Andersen LB. Br J Sports Med. 2014;48:871-7.', ('volumen-semanal.html', 'Organiza tus series de fuerza')),
    ('proteina-rinon', 'nutri salud', 'Comer mucha proteína daña el riñón.', 'f', 'Falso en personas sanas', 'Metaanálisis',
     'En adultos sin enfermedad renal, las dietas altas en proteína (por ejemplo, 1,5 g por kilo al día o más) no cambiaron la función del riñón de forma distinta a las dietas normales. Si tienes enfermedad renal crónica es otra cosa: ahí la cantidad la decide tu nefrólogo.',
     'Devries MC, Sithamparapillai A, Brimble KS, et al. J Nutr. 2018;148:1760-75.', (CALC, 'Calcula tu proteína diaria')),
    ('fallo', 'entreno', 'Si no llegas al fallo, no creces.', 'a', '', 'Metaanálisis y ensayo',
     'Entrenar cerca del fallo ayuda a ganar músculo, pero llegar al fallo en cada serie añade poco: en el metaanálisis la ventaja fue trivial. En un ensayo de 8 semanas con personas entrenadas, terminar las series a una o dos repeticiones del fallo dio el mismo crecimiento del cuádriceps que llegar al fallo, con menos fatiga en cada sesión.',
     'Refalo MC, et al. Sports Med. 2023;53:649-65. Refalo MC, et al. J Sports Sci. 2024;42:85-101.', ('calculadora-1rm.html', 'Calcula tus cargas')),
    ('sesenta', 'mayores', 'A partir de los 60 ya no se gana músculo.', 'f', '', 'Metaanálisis',
     'En 49 estudios con 1328 personas de 50 años o más, el entrenamiento de fuerza sumó de media 1,1 kg de masa magra. Los de más edad ganaron algo menos y los programas con más volumen, algo más: razón para empezar cuanto antes, no para no empezar.',
     'Peterson MD, Sen A, Gordon PM. Med Sci Sports Exerc. 2011;43:249-58.', ('test-sppb.html', 'Mide tu punto de partida')),
    ('ayunas', 'nutri', 'El cardio en ayunas quema más grasa.', 'n', '', 'Ensayo',
     'En un ensayo con 20 mujeres jóvenes a dieta, que hicieron una hora de cardio tres días por semana durante 4 semanas, la pérdida de grasa fue la misma en ayunas que después de comer. Es un estudio pequeño y corto: si te sienta mejor entrenar en ayunas, hazlo, pero no esperes quemar más grasa por ello.',
     'Schoenfeld BJ, Aragon AA, Wilborn CD, et al. J Int Soc Sports Nutr. 2014;11:54.', ('guias.html', 'Guías para perder grasa')),
    ('creatina', 'nutri salud', 'La creatina es un esteroide y daña el riñón.', 'f', '', 'Revisión de expertos',
     'La creatina no es un esteroide anabolizante: es una sustancia que fabrica tu cuerpo y que está en la carne y el pescado. Una revisión de expertos concluyó que, a las dosis habituales (3-5 g al día), no daña el riñón en personas sanas, y que no hay pruebas de que haga caer el pelo. Si tienes enfermedad renal, consúltalo antes.',
     'Antonio J, Candow DG, Forbes SC, et al. J Int Soc Sports Nutr. 2021;18:13.', ('suplementos.html', 'Suplementos con y sin evidencia')),
    ('mujeres', 'entreno', 'Si levantas pesas siendo mujer, te pones enorme.', 'f', '', 'Metaanálisis',
     'Mujeres y hombres ganan músculo en proporción parecida a lo que ya tenían. Como ellas parten de menos masa muscular, en kilos ganan algo menos. Y en fuerza relativa del tren superior, ellas mejoraron incluso más.',
     'Roberts BM, Nuckols G, Krieger JW. J Strength Cond Res. 2020;34:1448-60. Refalo MC, Nuckols G, Galpin AJ, et al. PeerJ. 2025;13:e19042.', ('programas.html', 'Entrena con un plan')),
    ('artrosis', 'salud mayores', 'Con artrosis de rodilla, mejor no cargar la articulación.', 'f', '', 'Guía clínica',
     'La guía de la OARSI de 2019 pone el ejercicio estructurado, junto con la educación y, si hace falta, perder peso, como tratamiento central de la artrosis de rodilla: recomendado para la mayoría de los pacientes en cualquier momento de la enfermedad. La clave es dosificar la carga, no evitarla.',
     'Bannuru RR, Osani MC, Vaysbrot EE, et al. Osteoarthritis Cartilage. 2019;27:1578-89.', ('semaforo-dolor.html', 'Dosifica con el semáforo del dolor')),
    ('frecuencia', 'entreno', 'Hay que entrenar cada músculo dos o tres veces por semana.', 'a', '', 'Metaanálisis',
     'Con las mismas series a la semana, repartirlas en uno, dos o tres días da un crecimiento muy parecido (revisión de 25 estudios). Entrenar más días ayuda sobre todo porque facilita hacer más series. Elige la frecuencia que puedas sostener.',
     'Schoenfeld BJ, Grgic J, Krieger J. J Sports Sci. 2019;37:1286-95.', ('volumen-semanal.html', 'Cuenta tus series por músculo')),
]
MITO_IMG_OK = _todas(*[f'mito-{m[0]}' for m in MITOS])  # bloque W10: una imagen por mito, solo si estan las nueve
MITO_CORTO = {'estirar': 'Estirar', 'proteina-rinon': 'Proteína y riñón', 'fallo': 'Fallo', 'sesenta': 'Músculo a los 60', 'ayunas': 'Cardio en ayunas',
              'creatina': 'Creatina', 'mujeres': 'Mujeres y pesas', 'artrosis': 'Artrosis', 'frecuencia': 'Frecuencia'}
MITO_TN = dict(MITO_T)
MITO_NV = {k: sum(1 for m in MITOS if m[3] == k) for k in MITO_VER}
MITO_NT = {v: sum(1 for m in MITOS if v in m[1].split()) for v, _ in MITO_T if v}
MITO_REFS = sum(len(_re.findall(r'\d{4};', m[7])) for m in MITOS)
def mito_html(k, id_, t, frase, ver, ver_t, tipo, txt, fuente, enl):
    foto = f'<span class="mito-foto">{ilus(f"mito-{id_}", "mito-img")}<span class="mito-sello" aria-hidden="true">{MITO_VER[ver]}</span></span>' if MITO_IMG_OK else ''
    temas = ''.join(f'<span>{MITO_TN[x]}</span>' for x in t.split() if x in MITO_TN)
    return (f'<article class="mito sube" id="{id_}" data-t="{t}" data-ver="{ver}"><details><summary>{foto}<span class="mito-cab"><span class="mito-n">{k:02d}<small>/{len(MITOS):02d}</small></span><span class="mito-tipo">{tipo}</span><span class="mito-leido">Leído</span></span>'
            f'<span class="mito-frase">«{frase}»</span><span class="mito-abre">Qué dicen los estudios</span></summary>'
            f'<div class="mito-cuerpo"><p class="mito-ver"><b>{ver_t or MITO_VER[ver]}</b></p><p>{txt}</p><p class="mito-fuente"><b>Fuente</b> {fuente}</p>'
            f'<a class="mito-enl" href="{enl[0]}"{_ext(enl[0])}>{enl[1]}</a>'
            f'<div class="mito-pie"><span class="mito-temas">{temas}</span><span class="mito-acc"><button type="button" class="pro-copia mito-copia" data-u="mitos.html#{id_}" aria-label="Copiar el enlace a este mito"><span>Copiar enlace</span></button>'
            f'<button type="button" class="mito-sig">Siguiente</button></span></div></div></details></article>')
MITOS_JS = r'''(function(){var f=document.getElementById('mitos-f');if(!f)return;var ms=[].slice.call(document.querySelectorAll('.mito')),n=document.getElementById('mitos-n'),todo=document.getElementById('mitos-todos'),q=matchMedia('(prefers-reduced-motion: reduce)').matches,K='fbe-mitos',L=[];
try{L=JSON.parse(localStorage.getItem(K)||'[]')||[]}catch(e){}
var pl=document.getElementById('mitos-l'),pb=document.getElementById('mitos-pb');
function prog(){var k=ms.filter(function(m){return L.indexOf(m.id)>=0}).length;ms.forEach(function(m){m.classList.toggle('leido',L.indexOf(m.id)>=0)});if(pl)pl.textContent=k;if(pb)pb.style.width=(k/ms.length*100)+'%';var w=document.querySelector('.mitos-prog');if(w)w.classList.toggle('completo',k===ms.length)}
function vis(){return ms.filter(function(m){return!m.hidden})}
function cuenta(){var k=vis().length;n.textContent=k+(k===1?' mito':' mitos')}
function foco(m){m.classList.remove('mito-foco');void m.offsetWidth;m.classList.add('mito-foco')}
function abre(m,ir){var d=m.querySelector('details');d.open=true;if(ir){m.scrollIntoView({behavior:q?'auto':'smooth',block:'start'});foco(m);var s=m.querySelector('summary');if(s)s.focus({preventScroll:true})}}
ms.forEach(function(m){var d=m.querySelector('details');d.addEventListener('toggle',function(){if(d.open&&L.indexOf(m.id)<0){L.push(m.id);try{localStorage.setItem(K,JSON.stringify(L))}catch(e){}prog()}});
var sg=m.querySelector('.mito-sig');if(sg)sg.addEventListener('click',function(){var v=vis(),i=v.indexOf(m),x=v[(i+1)%v.length];if(x&&x!==m)abre(x,true)})});
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.t;ms.forEach(function(m){var o=!!t&&(' '+m.dataset.t+' ').indexOf(' '+t+' ')<0;if(!o&&m.hidden){m.classList.remove('mito-entra');void m.offsetWidth;m.classList.add('mito-entra')}m.hidden=o});cuenta()});
todo.addEventListener('click',function(){var ab=todo.getAttribute('aria-pressed')!=='true';todo.setAttribute('aria-pressed',ab);todo.querySelector('span').textContent=ab?'Cerrar todas':'Abrir todas';ms.forEach(function(m){m.querySelector('details').open=ab})});
var az=document.getElementById('mitos-azar');if(az)az.addEventListener('click',function(){var v=vis(),nl=v.filter(function(m){return L.indexOf(m.id)<0}),p=nl.length?nl:v;if(p.length)abre(p[Math.floor(Math.random()*p.length)],true)});
var rs=document.getElementById('mitos-reset');if(rs)rs.addEventListener('click',function(){L=[];try{localStorage.removeItem(K)}catch(e){}prog()});
document.querySelectorAll('.mito-copia').forEach(function(b){b.addEventListener('click',function(){var u=new URL(b.dataset.u,location.href).href,s=b.querySelector('span'),t=s.textContent;function ok(){b.classList.add('hecho');s.textContent='Copiado';setTimeout(function(){b.classList.remove('hecho');s.textContent=t},1600)}if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(ok,function(){});})});
function hash(){var h=decodeURIComponent(location.hash.slice(1)),d=h&&document.getElementById(h);if(d&&d.classList.contains('mito')){if(d.hidden){f.querySelector('button').click()}abre(d,false);foco(d)}}
addEventListener('hashchange',hash);addEventListener('beforeprint',function(){ms.forEach(function(m){m.querySelector('details').open=true})});
hash();prog();cuenta();})();'''
pagina('mitos.html', 'Mitos y evidencia', 'Nueve mitos de gimnasio y de consulta contrastados con revisiones, ensayos y guías clínicas: estiramientos, proteína y riñón, fallo, edad, ayunas, creatina, mujeres, artrosis y frecuencia.',
       'Mitos y evidencia.', f'{len(MITOS)} ideas que se repiten en el gimnasio y en la consulta, contrastadas con revisiones, ensayos y guías clínicas. Toca cada una para ver qué dicen los estudios.', f'''
<section><div class="in">
  <ul class="mitos-cif sube"><li class="v-f"><b>{MITO_NV["f"]}</b>falsos</li><li class="v-a"><b>{MITO_NV["a"]}</b>a medias</li><li class="v-n"><b>{MITO_NV["n"]}</b>sin demostrar</li><li class="v-r"><b>{MITO_REFS}</b>referencias citadas</li></ul>
  <nav class="mitos-indice sube" aria-label="Los mitos"><b>Ir a</b>{"".join(f'<a href="#{m[0]}"><i>{k:02d}</i>{MITO_CORTO[m[0]]}</a>' for k, m in enumerate(MITOS, 1))}</nav>
  <div class="empieza sube"><div><h2>Filtra por tema</h2><p id="mitos-n" role="status">{len(MITOS)} mitos</p>
    <div class="mitos-prog"><span>Has leído <b id="mitos-l">0</b> de {len(MITOS)}</span><i aria-hidden="true"><b id="mitos-pb"></b></i><button type="button" id="mitos-reset" class="mitos-reset">Empezar de cero</button></div></div>
    <div><div class="fases claras" id="mitos-f" role="group" aria-label="Filtrar por tema">{"".join(f'<button type="button" data-t="{v}" aria-pressed="{"true" if not v else "false"}">{t}<em>{len(MITOS) if not v else MITO_NT[v]}</em></button>' for v, t in MITO_T)}</div>
    <div class="mitos-botones"><button type="button" class="btn hueco mitos-todos" id="mitos-todos" aria-pressed="false"><span>Abrir todas</span></button><button type="button" class="btn hueco mitos-azar" id="mitos-azar"><span>Uno al azar</span></button></div></div></div>
  <div class="mitos-rej" id="lista">{"".join(mito_html(k, *m) for k, m in enumerate(MITOS, 1))}</div>
</div></section>
<section class="hoja" id="leer"><div class="in"><div class="entrada sube"><h2>Cómo leer la etiqueta de cada mito</h2><p>Arriba de cada tarjeta verás de qué tipo de estudio sale la respuesta.</p></div>
  <ol class="pasos-g en-linea sube">
    <li><b>Metaanálisis</b><span>Junta los resultados de muchos estudios sobre la misma pregunta. Pesa más que un estudio suelto.</span></li>
    <li><b>Ensayo</b><span>Compara dos grupos asignados al azar. Si es pequeño o corto, la conclusión es más provisional.</span></li>
    <li><b>Guía clínica</b><span>Recomendaciones de un grupo de expertos que revisa toda la evidencia disponible.</span></li>
  </ol>
  <h3 class="mitos-sub sube">Y el veredicto, en tres colores</h3>
  <ul class="mitos-leyenda sube"><li class="v-f"><b>Falso</b><span>Los estudios dicen lo contrario de lo que afirma el mito.</span></li><li class="v-a"><b>A medias</b><span>Tiene parte de verdad, pero con matices importantes.</span></li><li class="v-n"><b>No demostrado</b><span>No hay pruebas de que sea así; los estudios son pocos o pequeños.</span></li></ul>
  <p class="sec-enl sube"><b>¿Tienes otra duda?</b><a href="dudas.html">Dudas frecuentes</a><a href="suplementos.html">Suplementos</a><a href="videos.html">Vídeos</a></p>
</div></section>
<script>{MITOS_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="#lista">Ver los mitos</a><a class="enl" href="#leer">Cómo leer las etiquetas</a></div>', cierre_t=('¿Quieres un plan sin mitos?', 'Cuéntame tu caso en el formulario. Te respondo yo.'))

# ---------------------------------------------------------------------------------------------
# 5. En los medios: solo con enlaces reales que Pelayo ha aprobado (21/11/2026). Los títulos de los dos podcasts los dio Pelayo
#    (YouTube no se puede leer desde aquí); los de prensa y SEMI son los publicados (el de AS, comprobado con la captura que mandó Pelayo el 21/11/2026).
MEDIO_ACC = {'Prensa': ('libro', 'Leer la noticia'), 'Podcast': ('micro', 'Ver la entrevista'), 'Formación': ('fonendo', 'Ver la minipíldora')}
MEDIO_T = [('', 'Todo'), ('Prensa', 'Prensa'), ('Podcast', 'Podcasts'), ('Formación', 'Formación')]
MEDIOS_JS = r'''(function(){var f=document.getElementById('medios-f');if(!f)return;var ms=[].slice.call(document.querySelectorAll('.medio')),n=document.getElementById('medios-n');
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.t,k=0;ms.forEach(function(m){var v=!t||m.dataset.t===t;if(v&&m.hidden){m.classList.remove('medio-entra');void m.offsetWidth;m.classList.add('medio-entra')}m.hidden=!v;if(v)k++});if(n)n.textContent=k+(k===1?' aparici\u00f3n':' apariciones')});})();'''
MEDIO_K = {'Prensa': 'pr', 'Podcast': 'po', 'Formación': 'fo'}
def _dominio(u): return _up.urlparse(u).netloc.replace('www.', '')
def medio_html(m, tp, t, u, fch):
    i, acc = MEDIO_ACC[tp]
    return (f'<a class="medio sube k-{MEDIO_K[tp]}" data-t="{tp}" href="{u}" target="_blank" rel="noopener"><span class="medio-cab">{sec_ic(i)}<span class="mito-tipo">{tp}</span>{f"<span class=\"medio-fecha\">{fch}</span>" if fch else ""}</span>'
            f'<b>{t}</b><span class="medio-de">{m}<small>{_dominio(u)}</small></span><span class="medio-acc">{acc}<span class="oculto"> (se abre en una pestaña nueva)</span></span></a>')
if len(MEDIOS) >= 2:
    _nt = {k: sum(1 for x in MEDIOS if x[1] == k) for k in MEDIO_ACC}
    pagina('medios.html', 'En los medios', 'Prensa, podcasts y formación con Pelayo Fernández Cidón, médico internista y entrenador: AS, Vozpópuli, Libertad Digital, podcasts y minipíldoras de la SEMI.',
           'En los medios.', 'Noticias, entrevistas y formación en las que he participado, con el enlace a cada una.', f'''
<section><div class="in">
  <div class="empieza sube"><div><h2 id="medios-n" role="status">{len(MEDIOS)} apariciones</h2><ul class="medios-cif"><li><b>{_nt["Prensa"]}</b>en prensa</li><li><b>{_nt["Podcast"]}</b>podcasts</li><li><b>{_nt["Formación"]}</b>de formación</li></ul></div>
    <div class="fases claras" id="medios-f" role="group" aria-label="Filtrar por tipo">{"".join(f'<button type="button" data-t="{v}" aria-pressed="{"true" if not v else "false"}">{t}<em>{len(MEDIOS) if not v else _nt[v]}</em></button>' for v, t in MEDIO_T)}</div></div>
  <div class="medios" id="lista">{"".join(medio_html(*x) for x in MEDIOS)}</div>
</div></section>
<section class="hoja"><div class="in"><div class="calc sube medios-calc">{sec_ic("micro")}<div><h3>¿Quieres entrevistarme o que dé una charla?</h3><p>Escríbeme con el medio, el tema y la fecha. Para sanitarios, mira también la página de profesionales.</p></div><div><a class="btn claro" href="{(MAILTO + '?subject=' + _up.quote('Entrevista o charla')) if MAILTO else FORM}">Escribirme</a></div></div>
  <p class="sec-enl sube"><b>Sigue por aquí</b><a href="profesionales.html">Para profesionales</a><a href="videos.html">Mis vídeos</a><a href="quien-soy.html">Quién soy</a></p>
</div></section>
<script>{MEDIOS_JS}</script>''', cta=f'<div class="cta"><a class="btn claro" href="#lista">Ver las apariciones</a><a class="enl" href="{(MAILTO + '?subject=' + _up.quote('Entrevista o charla')) if MAILTO else FORM}">Escribirme</a></div>', cierre_t=('¿Y si lo aplicamos a tu caso?', 'Cuéntame tu caso en el formulario. Te respondo yo.'))
SEC_PAGS = ['empieza-aqui.html', 'videos.html', 'mitos.html', 'profesionales.html'] + (['medios.html'] if len(MEDIOS) >= 2 else [])

# ---------------------------------------------------------------------------------------------
# Enlaces desde otras paginas ya generadas
def _parchea(arch, a, b):
    p = open(f'{SAL}/{arch}', encoding='utf-8').read()
    assert a in p, (arch, a[:70])
    open(f'{SAL}/{arch}', 'w', encoding='utf-8').write(p.replace(a, b, 1))
_parchea('index.html', '<li>Mitos del fitness</li></ul>', '<li>Mitos del fitness</li></ul>\n  <p class="sec-enl sube"><b>¿Aún no eres atleta?</b><a href="empieza-aqui.html">Empieza aquí</a><a href="mitos.html">Mitos y evidencia</a><a href="videos.html">Vídeos</a></p>')
_parchea('herramientas.html', '<p class="herr-nota sube">', '<p class="sec-enl sube"><b>¿No sabes cuál usar?</b><a href="empieza-aqui.html">Empieza aquí</a><b>¿Eres sanitario?</b><a href="profesionales.html">Para profesionales</a></p>\n  <p class="herr-nota sube">')
_parchea('guias.html', '<div class="calc sube" style="margin-top:3rem">', '<p class="sec-enl sube" style="margin-top:2.5rem"><b>Gratis para aprender</b><a href="mitos.html">Mitos y evidencia</a><a href="videos.html">Vídeos</a><a href="newsletter.html">Newsletter</a></p><div class="calc sube" style="margin-top:3rem">')
_parchea('quien-soy.html', f'<a class="caja sube" href="{YT}" target="_blank" rel="noopener">', '<a class="caja sube" href="videos.html">')
_parchea('pauta-activa.html', f'{_PM[2]}</p>', f'{_PM[2]} <a href="profesionales.html">Más para profesionales</a></p>')
if len(MEDIOS) >= 2:
    _parchea('quien-soy.html', '<p>Vídeos sobre fuerza, nutrición y salud.</p></a>\n  </div>', '<p>Vídeos sobre fuerza, nutrición y salud.</p></a>\n  </div><p class="sec-enl sube"><b>También he salido en</b><a href="medios.html">Prensa, podcasts y formación</a></p>')
