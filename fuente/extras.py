# ===== extras (21/11/2026): glosario, archivo del boletin, Mis resultados, buscador y web instalable =====
# Se ejecuta desde interior.py justo despues de secciones.py (antes del sitemap).
# - glosario.html: terminos de la web explicados en dos lineas, con enlace a su herramienta, mito o guia.
# - boletin.html: archivo de los envios del boletin (boletin.json, sacado de MailerLite en modo lectura el 21/11/2026;
#   cada envio enlaza a su vista web de MailerLite). Para anadir envios nuevos, anadir una linea a boletin.json.
# - mis-resultados.html: junta lo que se guarda con «Guardar en Mis resultados» en las calculadoras (localStorage fbe-resultados).
# - buscar.json: indice del buscador (lo usa luz.js). manifest.webmanifest y sw.js: web instalable y calculadoras sin conexion.
import json as _json, hashlib as _hl, unicodedata as _ud, glob, os, re, shutil, html as _html

I.update({
    'lupa': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    'carpeta': '<path d="M3.5 7.5A2 2 0 0 1 5.5 5.5h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/><path d="M8.5 13.5l2.2 2.2 4.8-4.8"/>',
    'sobre': '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
})
def _norm(t):
    t = _ud.normalize('NFD', str(t).lower())
    return ''.join(c for c in t if _ud.category(c) != 'Mn')

# ---------------------------------------------------------------------------------------------
# Glosario. Definiciones coherentes con las cifras de las herramientas y los mitos (mismas fuentes).
GLOS_G = [('', 'Todos'), ('entreno', 'Entrenamiento'), ('nutri', 'Nutrición y suplementos'), ('salud', 'Salud y medición'), ('evid', 'Evidencia')]
GLOS = [
    # id, termino, grupo, definicion, enlace (url, texto) o None, busqueda en el archivo del boletin
    ('1rm', '1RM (repetición máxima)', 'entreno', 'El peso máximo con el que puedes hacer una sola repetición con buena técnica. No hace falta probarlo: se puede estimar a partir de una serie de varias repeticiones.', ('calculadora-1rm.html', 'Calcula tu 1RM'), ''),
    ('rir', 'RIR (repeticiones en reserva)', 'entreno', 'Las repeticiones que te quedan antes de no poder hacer otra con buena técnica. Con RIR 2 podrías haber hecho dos más.', ('calculadora-1rm.html', 'Cargas según el RIR'), ''),
    ('rpe', 'RPE (esfuerzo percibido)', 'entreno', 'Escala del 1 al 10 para puntuar lo dura que ha sido una serie. En fuerza se usa junto al RIR: un RPE 8 equivale a dejar unas dos repeticiones en reserva.', None, 'RPE'),
    ('borg', 'Escala de Borg', 'salud', 'Escala de esfuerzo percibido de 6 a 20 que se usa en el ejercicio aeróbico. Para el ACSM, moderado es 12-13 y vigoroso, 14-17.', ('zonas-pulso.html', 'Tus zonas de esfuerzo'), ''),
    ('fallo', 'Fallo muscular', 'entreno', 'El punto en el que no puedes completar otra repetición con buena técnica. Acercarse ayuda a ganar músculo; llegar en cada serie añade poco.', ('mitos.html#fallo', 'Qué dicen los estudios'), 'fallo'),
    ('volumen', 'Volumen de entrenamiento', 'entreno', 'Cuánto entrenas en total, contado normalmente como series de trabajo por músculo y semana.', ('volumen-semanal.html', 'Cuenta tus series'), ''),
    ('serie-trabajo', 'Serie de trabajo', 'entreno', 'Una serie hecha cerca del fallo, la que cuenta para el volumen. Las series de calentamiento no cuentan.', ('volumen-semanal.html', 'Cuenta tus series'), ''),
    ('frecuencia', 'Frecuencia', 'entreno', 'Cuántas veces a la semana entrenas un músculo. Con las mismas series semanales, repartirlas en uno, dos o tres días da un crecimiento parecido.', ('mitos.html#frecuencia', 'Qué dicen los estudios'), ''),
    ('intensidad', 'Intensidad de carga', 'entreno', 'El peso con relación a tu máximo, normalmente en porcentaje del 1RM. No es lo mismo que el esfuerzo: un mismo porcentaje puede ser fácil o muy duro según las repeticiones que hagas.', ('calculadora-1rm.html', 'Tabla de cargas'), ''),
    ('sobrecarga', 'Sobrecarga progresiva', 'entreno', 'Subir poco a poco el estímulo (peso, repeticiones o series) para que el cuerpo siga adaptándose.', ('programas.html', 'Entrena con un plan'), ''),
    ('descarga', 'Descarga', 'entreno', 'Unos días o una semana con menos series o menos peso para recuperar la fatiga acumulada sin dejar de entrenar.', None, 'descanso'),
    ('tempo', 'Tempo', 'entreno', 'La velocidad de cada fase de la repetición: bajar, pausa y subir. A veces se escribe con cuatro números, como 3-1-1-0.', None, 'tempo'),
    ('hipertrofia', 'Hipertrofia', 'entreno', 'El aumento del tamaño del músculo. Depende sobre todo de las series de trabajo semanales, de lo cerca del fallo que acabes cada serie y de comer suficiente proteína.', ('volumen-semanal.html', 'Cuenta tus series'), ''),
    ('desentrenamiento', 'Desentrenamiento', 'entreno', 'Lo que se pierde al dejar de entrenar. La fuerza máxima casi no cambia hasta unas 4 semanas; la forma aeróbica baja antes.', ('paron.html', '¿Cuánto pierdo si paro?'), ''),
    ('dosis-minima', 'Dosis mínima de mantenimiento', 'entreno', 'Lo mínimo para no perder lo ganado. En adultos jóvenes, 1 sesión a la semana con 1 serie por ejercicio, manteniendo el peso, conservó la fuerza hasta 32 semanas.', ('paron.html', 'Tu plan mínimo'), ''),
    ('recomposicion', 'Recomposición corporal', 'nutri', 'Perder grasa y ganar músculo a la vez. Es más fácil si empiezas a entrenar o vuelves después de un parón.', ('guias.html', 'Guías'), 'recomposición'),
    ('deficit', 'Déficit calórico', 'nutri', 'Comer menos energía de la que gastas. Es lo que hace perder grasa, sea cual sea el tipo de dieta.', ('guias.html', 'Guías'), 'definición'),
    ('superavit', 'Superávit calórico', 'nutri', 'Comer algo más de lo que gastas. Ayuda a ganar músculo, pero si es grande también se gana bastante grasa.', None, 'volumen'),
    ('proteina', 'Proteína diaria', 'nutri', 'Para ganar músculo entrenando fuerza, el beneficio se estabiliza en torno a 1,6 g por kilo de peso y día (metaanálisis de Morton y cols., 2018).', (CALC, 'Calcula tu proteína'), 'proteína'),
    ('creatina', 'Creatina', 'nutri', 'El suplemento con más pruebas para ganar fuerza y músculo junto con el entrenamiento: 3-5 g al día. Está en el grupo A del Instituto Australiano del Deporte.', ('suplementos.html', 'Ficha de la creatina'), 'creatina'),
    ('cafeina', 'Cafeína', 'nutri', 'Mejora el rendimiento y reduce la sensación de esfuerzo. Para la EFSA, en adultos sanos son seguras tomas de hasta 200 mg y hasta 400 mg al día.', ('cafeina.html', 'Calcula tu cafeína'), 'cafeína'),
    ('ais', 'Grupos A-D del AIS', 'nutri', 'La clasificación de suplementos del Instituto Australiano del Deporte según su evidencia: A, sólida; B, emergente; C, sin beneficio demostrado; D, prohibido o de riesgo.', ('suplementos.html', 'Busca un suplemento'), 'suplementos'),
    ('sarcopenia', 'Sarcopenia', 'salud', 'Pérdida de fuerza y de masa muscular que reduce la capacidad física, sobre todo con la edad. El consenso europeo (EWGSOP2) la busca primero por la falta de fuerza.', ('test-sppb.html', 'Haz el test SPPB'), 'sarcopenia'),
    ('sppb', 'SPPB', 'salud', 'Batería de tres pruebas (equilibrio, marcha de 4 metros y levantarse de la silla) que puntúa de 0 a 12. Se usa para valorar la función física de las personas mayores.', ('test-sppb.html', 'Haz el test SPPB'), ''),
    ('test-silla', 'Test de la silla en 30 segundos', 'salud', 'Cuántas veces te levantas de una silla en 30 segundos con los brazos cruzados. Mide la fuerza de piernas y tiene valores de referencia de 60 a 94 años.', ('test-silla.html', 'Hazlo con cronómetro'), ''),
    ('pulso-max', 'Pulso máximo', 'salud', 'Las pulsaciones más altas que alcanzas en un esfuerzo máximo. Se estima con la fórmula de Tanaka (208 − 0,7 × edad), con un error típico de unos 10 latidos.', ('zonas-pulso.html', 'Calcula el tuyo'), ''),
    ('karvonen', 'Pulso de reserva (Karvonen)', 'salud', 'La diferencia entre tu pulso máximo y el de reposo. Las zonas calculadas sobre ella se ajustan mejor a tu forma física.', ('zonas-pulso.html', 'Tus zonas con el pulso en reposo'), ''),
    ('habla', 'Prueba del habla', 'salud', 'La forma más sencilla de medir la intensidad: si puedes hablar pero no cantar, vas a intensidad moderada; si solo te salen frases cortas, vigorosa.', ('zonas-pulso.html', 'Zonas de esfuerzo'), ''),
    ('betabloqueantes', 'Betabloqueantes', 'salud', 'Fármacos que bajan el pulso, como el bisoprolol. Con ellos, las zonas de pulso del reloj no sirven y hay que guiarse por el esfuerzo percibido.', ('pauta-activa.html', 'Pauta Activa'), 'medicación'),
    ('cribado', 'Cribado antes de hacer ejercicio', 'salud', 'Unas preguntas para saber si conviene una revisión médica antes de empezar o de subir la intensidad. La web usa el algoritmo del ACSM de 2015.', ('revision-medica.html', 'Haz el cribado'), 'valoración'),
    ('tendinopatia', 'Tendinopatía', 'salud', 'Dolor y peor tolerancia a la carga en un tendón, normalmente por sobrecarga. Suele mejorar dosificando la carga, no con reposo completo.', ('semaforo-dolor.html', 'Semáforo del dolor'), ''),
    ('control-dolor', 'Modelo de control del dolor', 'salud', 'Permite entrenar con un dolor de hasta 5 sobre 10 durante y después del ejercicio, si a la mañana siguiente ha vuelto a como estaba y no empeora de una semana a otra.', ('semaforo-dolor.html', 'Semáforo del dolor'), 'rodilla'),
    ('metaanalisis', 'Metaanálisis', 'evid', 'Un estudio que junta los resultados de muchos estudios sobre la misma pregunta. Pesa más que un estudio suelto.', ('mitos.html#leer', 'Cómo leer la evidencia'), ''),
    ('ensayo', 'Ensayo aleatorizado', 'evid', 'Un estudio que compara grupos asignados al azar. Es la mejor forma de saber si algo causa un efecto; si es pequeño o corto, la conclusión es más provisional.', ('mitos.html#leer', 'Cómo leer la evidencia'), ''),
    ('guia-clinica', 'Guía clínica', 'evid', 'Recomendaciones de un grupo de expertos que revisa toda la evidencia disponible sobre un problema de salud.', ('mitos.html#artrosis', 'Un ejemplo: la artrosis de rodilla'), ''),
    ('placebo', 'Efecto placebo', 'evid', 'La mejoría que aparece solo por creer que se recibe un tratamiento. Por eso los buenos ensayos comparan con una pastilla sin nada dentro.', None, ''),
]
GLOS.sort(key=lambda g: _norm(g[1]))
_GN = dict(GLOS_G)
def _glos_html(g):
    id_, t, gr, d, enl, q = g
    a = f'<a class="term-enl" href="{enl[0]}"{_ext(enl[0])}>{enl[1]}</a>' if enl else ''
    b = f'<a class="term-bol" href="boletin.html?q={_up.quote(q)}">Lo que he escrito</a>' if q else ''
    return (f'<article class="term sube" id="{id_}" data-g="{gr}" data-q="{_norm(t + " " + d)}"><p class="term-g">{_GN[gr]}</p><h3>{t}</h3><p>{d}</p>'
            f'<div class="term-pie">{a}{b}<button type="button" class="term-copia" data-u="glosario.html#{id_}" aria-label="Copiar el enlace a {t}">#</button></div></article>')
_letras = []
for g in GLOS:
    l = _norm(g[1])[0].upper()
    if l.isdigit(): l = '#'
    if l not in [x[0] for x in _letras]: _letras.append((l, g[0]))
GLOS_JS = r'''(function(){var f=document.getElementById('glos-f'),q=document.getElementById('glos-q'),ts=[].slice.call(document.querySelectorAll('.term')),n=document.getElementById('glos-n'),g='';
function norm(t){return String(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function res(el,ws){if(!el)return;if(el.dataset.o==null)el.dataset.o=el.textContent;var o=el.dataset.o,nn=norm(o),r=[];if(nn.length===o.length)ws.forEach(function(w){if(w.length<2)return;var i=0;while((i=nn.indexOf(w,i))>=0){r.push([i,i+w.length]);i+=w.length}});if(!r.length){if(el.firstElementChild||el.textContent!==o)el.textContent=o;return}r.sort(function(a,b){return a[0]-b[0]});var fr=document.createDocumentFragment(),j=0;r.forEach(function(x){if(x[0]<j)return;fr.appendChild(document.createTextNode(o.slice(j,x[0])));var m=document.createElement('mark');m.className='res';m.textContent=o.slice(x[0],x[1]);fr.appendChild(m);j=x[1]});fr.appendChild(document.createTextNode(o.slice(j)));el.textContent='';el.appendChild(fr)}
function pinta(){var v=norm(q.value).trim(),k=0;ts.forEach(function(t){var ok=(!g||t.dataset.g===g)&&(!v||t.dataset.q.indexOf(v)>=0);t.hidden=!ok;if(ok){k++;res(t.querySelector('h3'),v?[v]:[]);res(t.querySelector('p:not(.term-g)'),v?[v]:[])}});document.querySelector('.glos-rej').classList.toggle('filtrado',!!(v||g));n.textContent=k+(k===1?' término':' términos');document.getElementById('glos-nada').hidden=k>0}
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});g=b.dataset.g;pinta()});
q.addEventListener('input',pinta);
document.querySelectorAll('.term-copia').forEach(function(b){b.addEventListener('click',function(){var u=new URL(b.dataset.u,location.href).href;if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){b.classList.add('hecho');b.textContent='Copiado';setTimeout(function(){b.classList.remove('hecho');b.textContent='#'},1500)},function(){})})});
document.querySelectorAll('.glos-letras a').forEach(function(a){a.addEventListener('click',function(){if(q.value||g){q.value='';g='';f.querySelectorAll('button').forEach(function(x,i){x.setAttribute('aria-pressed',i===0)});pinta()}})});
if('IntersectionObserver' in window){var ls={};document.querySelectorAll('.glos-letras a').forEach(function(a){ls[a.getAttribute('href').slice(1)]=a});var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){Object.keys(ls).forEach(function(k){ls[k].classList.toggle('aqui',k===e.target.id)});var a=ls[e.target.id],nv=a&&a.parentNode;if(nv&&nv.scrollWidth>nv.clientWidth+4)nv.scrollTo({left:a.offsetLeft-nv.clientWidth/2+a.offsetWidth/2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}})},{rootMargin:'-25% 0px -65% 0px'});Object.keys(ls).forEach(function(k){var t=document.getElementById(k);if(t)io.observe(t)})}
pinta();})();'''
SEC_SIG['glosario.html'] = (('mitos.html', 'Mitos y evidencia'), ('herramientas.html', 'Herramientas'))
pagina('glosario.html', 'Glosario de fuerza', f'{len(GLOS)} términos de fuerza, nutrición y salud explicados en dos líneas: RIR, RPE, 1RM, volumen, sarcopenia, escala de Borg, metaanálisis y más, con su herramienta para probarlo.',
       'Glosario de fuerza.', f'{len(GLOS)} palabras que salen por toda la web, explicadas en dos líneas y con un enlace para probarlo o leer más.', f'''
<section><div class="in">
  <div class="empieza sube glos-caja"><div><h2>Busca un término</h2><p id="glos-n" role="status">{len(GLOS)} términos</p>
    <label class="oculto" for="glos-q">Buscar en el glosario</label><span class="lupa glos-busca"><input id="glos-q" type="search" placeholder="Por ejemplo: RIR, Borg, creatina" autocomplete="off"></span></div>
    <div><div class="fases claras" id="glos-f" role="group" aria-label="Filtrar por tema">{"".join(f'<button type="button" data-g="{v}" aria-pressed="{"true" if not v else "false"}">{t}<em>{len(GLOS) if not v else sum(1 for x in GLOS if x[2] == v)}</em></button>' for v, t in GLOS_G)}</div></div></div>
  <nav class="glos-letras sube" aria-label="Por letra">{"".join(f'<a href="#{i}">{l}</a>' for l, i in _letras)}</nav>
  <div class="glos-rej">{"".join(_glos_html(g) for g in GLOS)}</div>
  <p class="vol-vacio glos-nada" id="glos-nada" hidden>No hay ningún término con esa palabra. Prueba con el <button type="button" class="enl-b" onclick="window.fbeBusca&&window.fbeBusca(document.getElementById('glos-q').value)">buscador de toda la web</button>.</p>
  <p class="sec-enl sube"><b>Sigue por aquí</b><a href="mitos.html">Mitos y evidencia</a><a href="herramientas.html">Herramientas</a><a href="boletin.html">Archivo del boletín</a></p>
</div></section>
<script>{GLOS_JS}</script>''', cierre_t=('¿Prefieres que te lo explique yo?', 'Cuéntame tu caso en el formulario. Te respondo yo.'))

# ---------------------------------------------------------------------------------------------
# Archivo del boletin
BOL = _json.load(open('boletin.json', encoding='utf-8'))
BOL.sort(key=lambda b: b['f'], reverse=True)
BOL_T = [('', 'Todos'), ('entreno', 'Entrenamiento'), ('nutri', 'Nutrición'), ('suple', 'Suplementos'), ('salud', 'Salud')]
_BK = {
    'suple': ['creatina', 'suplement', 'cafeina'],
    'nutri': ['recomposicion', 'definicion', 'volumen', 'alimentacion', 'comer', 'dieta', 'proteina', 'alcohol', 'caloria', 'grasa', 'alimentos'],
    'salud': ['salud', 'diabetes', 'sarcopenia', 'longevidad', 'edad biologica', 'marcador', 'analitica', 'hospital', 'medic', 'cronobiologia', 'duermes', 'dormi',
              'sueno', 'pasos', 'caminar', 'imc', 'bascula', 'fc ', 'hrv', 'pulsacion', 'calor', 'mioquina', 'prension', 'visceral', 'miostatina', 'mortalidad', 'morir',
              'cerebro', 'corazon', 'envejecimiento', 'rodilla', 'span-mace'],
    'entreno': ['tecnica', 'repeticion', 'fallo', 'series', 'tempo', 'rpe', 'cardio', 'squat', 'sentadilla', 'gluteo', 'espalda', 'empuje', 'flexiones', 'gym',
                'gimnasio', 'fuerza', 'precision', 'movimiento', 'futbol', 'musica', 'rodilla', 'mitos', 'protocolo', 'ejercicio', 'entrena', 'descanso'],
}
def _bol_t(b):
    t = _norm(b['tema'] + ' ' + b['asunto']).replace('lipoproteina', 'lipo')
    r = [k for k in ('entreno', 'nutri', 'suple', 'salud') if any(w in t for w in _BK[k])]
    return r or ['entreno']
for b in BOL: b['t'] = _bol_t(b)
_BTN = dict(BOL_T)
_MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
_MC = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
def _bol_html():
    s, mes = '', ''
    for b in BOL:
        y, m, d = b['f'].split('-'); km = f'{_MES[int(m) - 1]} de {y}'
        if km != mes:
            s += f'<h3 class="bol-mes" data-m="{y}-{m}">{km}</h3>'; mes = km
        tags = ''.join(f'<span class="bt-{t}">{_BTN[t]}</span>' for t in b['t'])
        s += (f'<a class="bol-it" href="{b["u"]}" target="_blank" rel="noopener" data-t="{" ".join(b["t"])}" data-m="{y}-{m}" data-q="{_html.escape(_norm(b["tema"] + " " + b["asunto"]))}">'
              f'<time datetime="{b["f"]}"><b>{int(d)}</b>{_MC[int(m) - 1]}</time><span class="bol-txt"><b>{_html.escape(b["asunto"])}</b><small>{_html.escape(b["tema"])}</small></span>'
              f'<span class="bol-tags">{tags}</span><span class="oculto"> (se abre en una pestaña nueva)</span></a>')
    return s
BOL_JS = r'''(function(){var f=document.getElementById('bol-f'),q=document.getElementById('bol-q'),its=[].slice.call(document.querySelectorAll('.bol-it')),ms=[].slice.call(document.querySelectorAll('.bol-mes')),n=document.getElementById('bol-n'),t='';
function norm(x){return String(x||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function res(el,ws){if(!el)return;if(el.dataset.o==null)el.dataset.o=el.textContent;var o=el.dataset.o,nn=norm(o),r=[];if(nn.length===o.length)ws.forEach(function(w){if(w.length<2)return;var i=0;while((i=nn.indexOf(w,i))>=0){r.push([i,i+w.length]);i+=w.length}});if(!r.length){if(el.firstElementChild||el.textContent!==o)el.textContent=o;return}r.sort(function(a,b){return a[0]-b[0]});var fr=document.createDocumentFragment(),j=0;r.forEach(function(x){if(x[0]<j)return;fr.appendChild(document.createTextNode(o.slice(j,x[0])));var m=document.createElement('mark');m.className='res';m.textContent=o.slice(x[0],x[1]);fr.appendChild(m);j=x[1]});fr.appendChild(document.createTextNode(o.slice(j)));el.textContent='';el.appendChild(fr)}
function pinta(){var v=norm(q.value).trim().split(/\s+/).filter(Boolean),k=0,vis={};its.forEach(function(a){var ok=(!t||(' '+a.dataset.t+' ').indexOf(' '+t+' ')>=0)&&v.every(function(p){return a.dataset.q.indexOf(p)>=0});a.hidden=!ok;if(ok){k++;vis[a.dataset.m]=(vis[a.dataset.m]||0)+1;res(a.querySelector('.bol-txt b'),v);res(a.querySelector('.bol-txt small'),v)}});ms.forEach(function(m){var c=vis[m.dataset.m]||0,e=m.querySelector('.bol-c');if(!e){e=document.createElement('span');e.className='bol-c';e.setAttribute('aria-hidden','true');m.appendChild(e)}e.textContent=c});ms.forEach(function(m){m.hidden=!vis[m.dataset.m]});n.textContent=k+(k===1?' envío':' envíos');document.getElementById('bol-nada').hidden=k>0}
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});t=b.dataset.t;pinta()});
q.addEventListener('input',pinta);
try{var p=new URLSearchParams(location.search).get('q');if(p){q.value=p}}catch(e){}
pinta();})();'''
_bn = {k: sum(1 for b in BOL if k in b['t']) for k, _ in BOL_T if k}
_b0 = BOL[-1]['f'].split('-')
pagina('boletin.html', 'Archivo del boletín', f'Los {len(BOL)} envíos del boletín semanal de Fuerza Basada en Evidencia desde {_MES[int(_b0[1]) - 1]} de {_b0[0]}: entrenamiento, nutrición, suplementos y salud, con buscador por tema.',
       'Archivo del boletín.', f'{len(BOL)} correos desde {_MES[int(_b0[1]) - 1]} de {_b0[0]}. Busca un tema y ábrelo tal como llegó.', f'''
<section><div class="in">
  <div class="empieza sube bol-caja"><div><h2 id="bol-n" aria-live="polite">{len(BOL)} envíos</h2>
    <label class="oculto" for="bol-q">Buscar en el archivo</label><span class="lupa glos-busca"><input id="bol-q" type="search" placeholder="Por ejemplo: creatina, sueño, rodilla" autocomplete="off"></span></div>
    <div class="fases claras" id="bol-f" role="group" aria-label="Filtrar por tema">{"".join(f'<button type="button" data-t="{v}" aria-pressed="{"true" if not v else "false"}">{tt}<em>{len(BOL) if not v else _bn[v]}</em></button>' for v, tt in BOL_T)}</div></div>
  <div class="bol-lista" id="lista">{_bol_html()}</div>
  <p class="vol-vacio" id="bol-nada" hidden>No hay ningún envío con esa palabra. Prueba con otra o con el <button type="button" class="enl-b" onclick="window.fbeBusca&&window.fbeBusca(document.getElementById('bol-q').value)">buscador de toda la web</button>.</p>
  <p class="bol-nota sube">Cada correo se abre en su versión web, tal como llegó a los suscriptores.</p>
  <div class="calc sube bol-calc">{sec_ic("sobre")}<div><h3>Recibe el siguiente</h3><p>Un correo a la semana. Te das de baja cuando quieras.</p></div><div><a class="btn claro" href="newsletter.html">Apuntarme</a></div></div>
</div></section>
<script>{BOL_JS}</script>''', padre=('newsletter.html', 'Boletín'), cierre_t=('¿Quieres que lo apliquemos a tu caso?', 'Cuéntame tu caso en el formulario. Te respondo yo.'))
_p = open(f'{SAL}/newsletter.html', encoding='utf-8').read()
_i = _p.index('<div class="boletin">'); _j = _p.index('</div>\n</div></section>', _i) + len('</div>')
open(f'{SAL}/newsletter.html', 'w', encoding='utf-8').write(_p[:_j] + f'\n  <p class="sec-enl sube"><b>Todos los envíos</b><a href="boletin.html">Archivo del boletín ({len(BOL)})</a></p>' + _p[_j:])

# ---------------------------------------------------------------------------------------------
# Mis resultados
INSTALA = '<div class="instala sube" hidden><div>' + (ilus('web-instala', 'instala-img') or sec_ic('carpeta')) + '<p><b>Llévate las herramientas en el móvil.</b> Instala la web como una app: funcionan también sin cobertura.</p></div><button type="button" class="btn peq instala-b">Instalar</button><p class="instala-ios" hidden>En iPhone: botón <b>Compartir</b> y después <b>Añadir a pantalla de inicio</b>.</p></div>'
MR_JS = r'''(function(){var copiar=window.copiar||function(b,t){var s=b.querySelector('span'),o=s.textContent;function ok(){b.classList.add('hecho');s.textContent='Copiado';setTimeout(function(){b.classList.remove('hecho');s.textContent=o},1600)}if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(ok,function(){})};
var K='fbe-resultados',L=document.getElementById('mr-lista'),V=document.getElementById('mr-vacio'),B=document.getElementById('mr-bots'),av=document.getElementById('mr-aviso'),des=null,tN=0;
function ent(v){return v&&v.h?v:{titulo:v&&v.titulo,h:v&&v.texto?[{t:v.t,texto:v.texto}]:[]}}
function lee(){try{var o=JSON.parse(localStorage.getItem(K)||'{}');if(!o||typeof o!=='object')return {};Object.keys(o).forEach(function(k){o[k]=ent(o[k]);if(!o[k].h.length)delete o[k]});return o}catch(e){return {}}}
function escribe(o){try{if(Object.keys(o).length)localStorage.setItem(K,JSON.stringify(o));else localStorage.removeItem(K);return true}catch(e){return false}}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fecha(t){var d=new Date(t||0);return d.toLocaleDateString('es-ES',{day:'numeric',month:'long',year:'numeric'})+' · '+d.toLocaleTimeString('es-ES',{hour:'2-digit',minute:'2-digit'})}
function todo(){var o=lee();return Object.keys(o).map(function(k){return [k,o[k]]}).sort(function(a,b){return (b[1].h[0].t||0)-(a[1].h[0].t||0)})}
function txt(x){return (x[1].titulo||x[0])+' ('+new Date(x[1].h[0].t||0).toLocaleDateString('es-ES')+')\n'+x[1].h[0].texto+(x[1].h[0].n?'\nNota: '+x[1].h[0].n:'')}
function pinta(){var a=todo(),n=0;a.forEach(function(x){n+=x[1].h.length});V.hidden=a.length>0;B.hidden=!a.length;
  L.innerHTML=a.map(function(x){var h=x[1].h,u=h[0];return '<article class="mr-it sube ya"><div class="mr-cab"><h3><a href="'+esc(x[0])+'">'+esc(x[1].titulo||x[0])+'</a></h3><time datetime="'+new Date(u.t||0).toISOString()+'">'+fecha(u.t)+'</time></div><pre>'+esc(u.texto||'')+'</pre>'
    +'<label class="mr-nota"><span>Tu nota</span><textarea rows="2" data-nota="'+esc(x[0])+'" placeholder="Por ejemplo: con molestias en la rodilla, o después de una semana de guardias">'+esc(u.n||'')+'</textarea></label>'
    +(h.length>1?'<details class="mr-hist"><summary>Anteriores <em>'+(h.length-1)+'</em></summary><ol>'+h.slice(1).map(function(e,i){return '<li><time>'+fecha(e.t)+'</time><pre>'+esc(e.texto||'')+'</pre>'+(e.n?'<p class="mr-n">'+esc(e.n)+'</p>':'')+'<button type="button" class="enl-b" data-borra-h="'+esc(x[0])+'" data-i="'+(i+1)+'">Borrar este</button></li>'}).join('')+'</ol></details>':'')
    +'<div class="mr-pie"><a class="enl-h" href="'+esc(x[0])+'">Repetir</a><button type="button" class="copiar-t" data-k="'+esc(x[0])+'"><span>Copiar</span></button><button type="button" class="enl-b" data-rec="'+esc(x[0])+'">Recordármelo en 3 meses</button><button type="button" class="enl-b" data-borra="'+esc(x[0])+'">Borrar</button></div></article>'}).join('');
  document.getElementById('mr-n').textContent=a.length?(n===1?'1 resultado guardado':n+' resultados guardados'):'Aún no has guardado nada'}
function baja(nom,tipo,cont){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([cont],{type:tipo}));a.download=nom;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
function p2(x){return (x<10?'0':'')+x}
function ics(k,o){var d=new Date();d.setMonth(d.getMonth()+3);d.setHours(10,0,0,0);var f=function(z){return z.getFullYear()+p2(z.getMonth()+1)+p2(z.getDate())+'T'+p2(z.getHours())+p2(z.getMinutes())+'00'},e=new Date(d.getTime()+15*60000),st=new Date().toISOString().replace(/[-:]/g,'').replace(/\.\d+/,''),url=new URL(k,location.href).href,t='Repetir: '+(o.titulo||k)+' (FBE)';
  return ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Fuerza Basada en Evidencia//Recordatorio//ES','BEGIN:VEVENT','UID:'+Date.now()+'@fuerzabasadaenevidencia.com','DTSTAMP:'+st,'DTSTART:'+f(d),'DTEND:'+f(e),'SUMMARY:'+t,'DESCRIPTION:Repite la prueba y compárala con la anterior en Mis resultados. '+url,'URL:'+url,'BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+t,'TRIGGER:PT0M','END:VALARM','END:VEVENT','END:VCALENDAR'].join('\r\n')+'\r\n'}
L.addEventListener('click',function(e){var c=e.target.closest('.copiar-t'),b=e.target.closest('[data-borra]'),bh=e.target.closest('[data-borra-h]'),r=e.target.closest('[data-rec]'),o=lee();
  if(c&&o[c.dataset.k]){var h=o[c.dataset.k].h;copiar(c,txt([c.dataset.k,o[c.dataset.k]])+(h.length>1?'\n\nAnteriores:\n'+h.slice(1).map(function(x){return new Date(x.t||0).toLocaleDateString('es-ES')+'\n'+x.texto+(x.n?'\nNota: '+x.n:'')}).join('\n\n'):''))}
  if(r&&o[r.dataset.rec]){baja('recordatorio-fbe.ics','text/calendar;charset=utf-8',ics(r.dataset.rec,o[r.dataset.rec]));r.textContent='Descargado: ábrelo para añadirlo'}
  if(b){des=JSON.parse(JSON.stringify(o));delete o[b.dataset.borra];escribe(o);aviso('Borrado.');pinta()}
  if(bh&&o[bh.dataset.borraH]){des=JSON.parse(JSON.stringify(o));o[bh.dataset.borraH].h.splice(+bh.dataset.i,1);escribe(o);aviso('Borrado.');pinta()}});
L.addEventListener('input',function(e){var t=e.target.closest('[data-nota]');if(!t)return;clearTimeout(tN);tN=setTimeout(function(){var o=lee(),k=t.dataset.nota;if(o[k]){o[k].h[0].n=t.value.slice(0,300);escribe(o)}},350)});
function aviso(t,sinDes){av.innerHTML=t+(sinDes?'':' <button type="button" class="enl-b claro" id="mr-des">Deshacer</button>')}
av.addEventListener('click',function(e){if(e.target.id==='mr-des'&&des){escribe(des);des=null;av.textContent='';pinta()}});
document.getElementById('mr-imp').addEventListener('click',function(){window.print()});
document.getElementById('mr-cop').addEventListener('click',function(){copiar(this,todo().map(txt).join('\n\n'))});
document.getElementById('mr-todo').addEventListener('click',function(){des=lee();escribe({});aviso('Todo borrado.');pinta()});
document.getElementById('mr-exp').addEventListener('click',function(){var d=new Date();baja('mis-resultados-fbe-'+d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate())+'.json','application/json',JSON.stringify({fbe:'resultados',v:1,fecha:d.toISOString(),datos:lee()},null,1));aviso('Copia descargada. Guárdala donde quieras: con «Recuperar» la cargas en otro móvil u ordenador.',true)});
document.getElementById('mr-imp-f').addEventListener('change',function(){var f=this.files&&this.files[0],inp=this;if(!f)return;var r=new FileReader();r.onload=function(){try{var j=JSON.parse(r.result),dd=j&&j.datos;if(!dd||typeof dd!=='object')throw 0;var o=lee(),k=0;des=JSON.parse(JSON.stringify(o));Object.keys(dd).forEach(function(key){var x=ent(dd[key]);if(!x.h.length)return;var y=o[key]||{titulo:x.titulo,h:[]},vistos={};y.h=y.h.concat(x.h).filter(function(e){var c=e.t+'|'+e.texto;if(vistos[c])return false;vistos[c]=1;return true}).sort(function(a,b){return (b.t||0)-(a.t||0)}).slice(0,12);y.titulo=y.titulo||x.titulo;o[key]=y;k++});escribe(o);aviso('Recuperados '+k+(k===1?' resultado.':' resultados.'));pinta()}catch(e){aviso('Ese archivo no es una copia de Mis resultados.',true)}inp.value=''};r.readAsText(f)});
addEventListener('storage',function(e){if(e.key===K)pinta()});
pinta();})();'''
_MR_H = ''.join(f'<a class="herr-mini" href="{u}">{ilus(f"herr-{sl}", "herr-mini-img")}<b>{t}</b><span>{d}</span></a>' for u, sl, i, t, d in HERR_MAS)
pagina('mis-resultados.html', 'Mis resultados', 'Tus resultados de las calculadoras, juntos en una hoja para imprimir o enseñar a tu médico o entrenador. Se guardan solo en tu navegador.',
       'Mis resultados.', 'Lo que guardas en las calculadoras, junto en una hoja para imprimir o enseñar a tu médico o a tu entrenador.', f'''
<section><div class="in">
  <div class="empieza sube mr-caja"><div><h2 id="mr-n" aria-live="polite">Aún no has guardado nada</h2><p class="mr-priv">{ico("candado")}Se guarda solo en este navegador: no sale de tu dispositivo ni me llega a mí.</p></div>
    <div class="mr-bots" id="mr-bots" hidden><button type="button" class="btn peq" id="mr-imp">Imprimir o guardar en PDF</button><button type="button" class="copiar-t" id="mr-cop"><span>Copiar todo</span></button><button type="button" class="enl-b" id="mr-todo">Borrar todo</button></div></div>
  <div class="mr-copia sube"><p><b>Copia de seguridad.</b> Tus resultados viven en este navegador. Descárgalos en un archivo para guardarlos o pasarlos a otro dispositivo.</p><div><button type="button" class="copiar-t" id="mr-exp"><span>Descargar copia</span></button><label class="copiar-t mr-rec"><span>Recuperar copia</span><input type="file" id="mr-imp-f" accept="application/json,.json" class="oculto"></label></div></div>
  <p class="vol-aviso" id="mr-aviso" role="status"></p>
  <div class="mr-lista" id="mr-lista"></div>
  <div class="mr-vacio" id="mr-vacio">{ilus('mr-vacio', 'mr-vacio-img')}<p>Usa cualquier calculadora y pulsa «Guardar en Mis resultados», junto a «Copiar». Aparecerá aquí con la fecha. Si repites una prueba, se guardan las anteriores (hasta 12 por herramienta) para que veas tu evolución.</p><div class="herr-mas-rej">{_MR_H}</div></div>
  {INSTALA}
</div></section>
<script>{MR_JS}</script>''', padre=('herramientas.html', 'Herramientas'), extra='<meta name="robots" content="noindex">')  # datos de cada persona: fuera de los buscadores
_p = open(f'{SAL}/herramientas.html', encoding='utf-8').read()
_a = '<p class="herr-nota sube">'
assert _a in _p
_p = _p.replace(_a, f'<p class="sec-enl sube"><b>Lo tuyo</b><a href="mis-resultados.html">Mis resultados</a><a href="glosario.html">Glosario</a></p>\n  {INSTALA}\n  ' + _a, 1)
open(f'{SAL}/herramientas.html', 'w', encoding='utf-8').write(_p)

SEC_PAGS += ['glosario.html', 'boletin.html'] + SEC_PAGS_H3 + SEC_PAGS_H4

# ---------------------------------------------------------------------------------------------
# Indice del buscador (buscar.json): paginas y, dentro de ellas, dudas, mitos, guias, perfiles, terminos y envios del boletin
def _txt(h): return _html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))).strip()
def _lee(f):
    try: return open(f'{SAL}/{f}', encoding='utf-8').read()
    except OSError: return ''
_HERR_U = {u for u, *_ in HERR_MAS} | {'pauta-activa.html'}
_IDX = []
_PAGS_B = ['index.html'] + [u for u, _ in PAGS] + ['pauta-activa.html'] + [u for u, *_ in HERR_MAS] + SEC_PAGS + ['mis-resultados.html', 'pedir-plaza.html']
for _f in dict.fromkeys(_PAGS_B):
    _h = _lee(_f)
    if not _h: continue
    _t = _txt(re.search(r'<title>(.*?)</title>', _h, re.S).group(1)).split(' · ')[0].split(' | ')[0]
    _d = re.search(r'<meta name="description" content="([^"]*)"', _h)
    _h1 = re.search(r'<h1[^>]*>(.*?)</h1>', _h, re.S)
    _h2 = ' '.join(_txt(x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', _h, re.S))[:400]
    _IDX.append({'t': 'Inicio' if _f == 'index.html' else _t, 'u': _f, 'd': _html.unescape(_d.group(1)) if _d else '', 'k': (_txt(_h1.group(1)) if _h1 else '') + ' ' + _h2,
                 'y': 'Herramienta' if _f in _HERR_U else 'Página'})
for _id, _q, _r in re.findall(r'<details id="([^"]+)"><summary>(.*?)</summary><p>(.*?)</p>', _lee('dudas.html'), re.S):
    _IDX.append({'t': _txt(_q), 'u': f'dudas.html#{_id}', 'd': _txt(_r)[:150], 'k': '', 'y': 'Duda'})
for _m in MITOS:
    _IDX.append({'t': f'«{_m[2]}»', 'u': f'mitos.html#{_m[0]}', 'd': (_m[4] or MITO_VER[_m[3]]) + '. ' + _m[6][:120], 'k': _m[5], 'y': 'Mito'})
for _id, _h3, _p1 in re.findall(r'<article class="guia[^"]*" id="(g\d+)"[^>]*>.*?<h3>(.*?)</h3><p>(.*?)</p>', _lee('guias.html'), re.S):
    _IDX.append({'t': _txt(_h3), 'u': f'guias.html#{_id}', 'd': _txt(_p1), 'k': '', 'y': 'Guía'})
for _id, _h3 in re.findall(r'<div class="ea-ruta[^"]*" data-p="([a-z]+)">.*?<h3[^>]*>(.*?)</h3>', _lee('empieza-aqui.html'), re.S):
    _IDX.append({'t': _txt(_h3), 'u': f'empieza-aqui.html#{_id}', 'd': 'Por dónde empezar si es tu caso.', 'k': '', 'y': 'Empieza aquí'})
for _g in GLOS:
    _IDX.append({'t': _g[1], 'u': f'glosario.html#{_g[0]}', 'd': _g[3], 'k': '', 'y': 'Glosario'})
for _b in BOL:
    _IDX.append({'t': _b['asunto'], 'u': _b['u'], 'd': _b['tema'], 'k': '', 'y': 'Boletín', 'x': 1})
for _v in VIDS:
    _IDX.append({'t': _v['t'], 'u': f'videos.html#v-{_v["id"]}', 'd': f'{vid_fecha(_v["f"])} · {_v["d"]} · ' + ' · '.join(VID_GD[g] for g in _v['g']), 'k': 'video youtube ' + ' '.join(c[2] for c in VID_X.get(_v['id'], {}).get('c', [])), 'y': 'Vídeo'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(_json.dumps(_IDX, ensure_ascii=False, separators=(',', ':')))
print('buscador:', len(_IDX), 'entradas')

# ---------------------------------------------------------------------------------------------
# Web instalable: manifiesto, service worker y enlace en todas las paginas
open(f'{SAL}/manifest.webmanifest', 'w', encoding='utf-8').write(_json.dumps({
    'name': 'Fuerza Basada en Evidencia', 'short_name': 'FBE', 'lang': 'es', 'dir': 'ltr',
    'description': 'Fuerza y nutrición con un médico internista que también entrena. Herramientas que funcionan sin conexión.',
    'start_url': './', 'scope': './', 'display': 'standalone', 'background_color': '#140B3A', 'theme_color': '#140B3A',
    'icons': [{'src': 'icono-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icono-512.png', 'sizes': '512x512', 'type': 'image/png'},
              {'src': 'icono-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
    'shortcuts': [{'name': 'Herramientas', 'url': 'herramientas.html'}, {'name': 'Mis resultados', 'url': 'mis-resultados.html'}, {'name': 'Glosario', 'url': 'glosario.html'}],
}, ensure_ascii=False, indent=1))
_PRE_SW = ['./', 'fbe.css', 'fbe.js', 'img/archivo.woff2', 'favicon.svg', 'icono-192.png', 'manifest.webmanifest', 'buscar.json', 'herramientas.html', 'mis-resultados.html', 'glosario.html'] + [u for u, *_ in HERR_MAS]
SW_JS = r'''// Service worker de Fuerza Basada en Evidencia: guarda las calculadoras para usarlas sin conexion.
const V = 'fbe-__V__';
const PRE = __PRE__;
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(PRE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('fbe-') && k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url); if (u.origin !== location.origin) return;
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then(res => { if (res.ok) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); } return res; })
      .catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || caches.match('herramientas.html'))));
    return;
  }
  e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => {
    if (res.ok && /\.(css|js|json|woff2|webp|png|jpg|svg)$/.test(u.pathname)) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); }
    return res;
  })));
});
'''
_ver = _hl.sha1((_lee('fbe.css') + _lee('fbe.js') + _lee('buscar.json') + ''.join(_lee(u) for u in _PRE_SW if u.endswith('.html'))).encode('utf-8')).hexdigest()[:10]
open(f'{SAL}/sw.js', 'w', encoding='utf-8').write(SW_JS.replace('__V__', _ver).replace('__PRE__', _json.dumps(_PRE_SW)))
# Ilustraciones opcionales que pinta luz.js (buscador y ajustes de lectura): se copian si existen y se avisa con data-fbe-img
_IMG_JS = [k for k, n in (('busca', 'web-buscador'), ('ajustes', 'web-ajustes')) if os.path.exists(f'web-img/{n}.webp')]
for _k, _n in (('busca', 'web-buscador'), ('ajustes', 'web-ajustes')):
    if _k in _IMG_JS: shutil.copy(f'web-img/{_n}.webp', f'{SAL}/img/{_n}.webp')
# Ajustes de lectura antes de pintar (sin salto al cargar) y enlace al manifiesto en todas las paginas
_LECT = "<script>try{var _a=JSON.parse(localStorage.getItem('fbe-lectura')||'{}')||{},_c=document.documentElement.classList;if(_a.l===1)_c.add('letra-1');if(_a.l===2)_c.add('letra-2');if(_a.c)_c.add('contraste');if(_a.q)_c.add('quieto')}catch(e){}</script>"
_MAN = '<link rel="manifest" href="manifest.webmanifest">'
for _f in glob.glob(f'{SAL}/*.html'):
    _t = open(_f, encoding='utf-8').read()
    if '</head>' not in _t or 'http-equiv="refresh"' in _t: continue
    _n = _t
    if _MAN not in _n: _n = _n.replace('</head>', _MAN + _LECT + '</head>', 1)
    if _IMG_JS and 'data-fbe-img=' not in _n: _n = re.sub(r'<html(\s|>)', lambda m: f'<html data-fbe-img="{" ".join(_IMG_JS)}"' + m.group(1), _n, count=1)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
