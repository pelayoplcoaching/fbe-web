# «Chequeo de 10 minutos» (21/11/2026, noche). Lo ejecuta interior.py después de siguiente.py (usa SIGUE) y antes de autoria.py.
# Una ruta guiada por cuatro herramientas que ya existen, en orden, y un resumen por áreas. No calcula nada nuevo: cada
# resultado sale de su herramienta (con sus cifras y fuentes) y se lee de Mis resultados (localStorage fbe-resultados).
# - chequeo.html: qué necesitas, los cuatro pasos con su estado, dos pruebas opcionales, el resumen y por qué estas cuatro.
# - En cada herramienta del chequeo, si llega con ?chequeo=1: barra de pasos arriba y «Guardar y seguir» junto a «Guardar».
# - El inicio del chequeo se guarda en localStorage fbe-chequeo ({inicio}): cuenta lo guardado desde ese día; «Empezar de
#   nuevo» lo pone en este momento (los resultados siguen en Mis resultados).
CHQ_PAGS = ['chequeo.html']
CHQ_PASOS = [
    {'u': 'revision-medica.html', 'a': 'Seguridad', 'q': '¿Conviene pasar antes por el médico?',
     'd': 'Tres preguntas del cribado del ACSM: si ya haces ejercicio, si tienes alguna enfermedad diagnosticada y si notas síntomas. Primero, porque decide cómo empezar.'},
    {'u': 'actividad-oms.html', 'a': 'Actividad', 'q': '¿Llegas a lo mínimo de la OMS?',
     'd': 'Apunta los minutos de una semana normal, moderados y vigorosos, y los días de fuerza. Sale cuánto te falta, si te falta algo.'},
    {'u': 'test-silla.html', 'a': 'Fuerza de piernas', 'q': 'Test de la silla en 30 segundos',
     'd': 'Cuántas veces te levantas de una silla en 30 segundos con los brazos cruzados. La web lleva el tiempo y la cuenta.'},
    {'u': 'cintura-altura.html', 'a': 'Grasa abdominal', 'q': 'Cintura y altura',
     'd': 'Mide tu cintura con una cinta métrica, como dice la guía de NICE, y escribe tu altura. Sale tu índice y su rango.'},
]
CHQ_OPC = [
    {'u': 'test-sppb.html', 'a': 'Equilibrio y marcha', 'q': 'Test SPPB', 'cuando': 'Para personas mayores, o si te cuesta moverte.'},
    {'u': 'prension.html', 'a': 'Fuerza de agarre', 'q': 'Fuerza de prensión', 'cuando': 'Si tienes un dinamómetro de mano.'},
]
# Por qué estas cuatro: lo mismo que ya dicen sus herramientas, con su ficha en Fuentes
CHQ_POR = [
    ('Seguridad', 'El cribado del ACSM separa a quien puede empezar sin más de quien conviene que pase antes por su médico, según el ejercicio que ya hace, sus enfermedades y sus síntomas.', [('riebe2015', 'Riebe y cols., 2015')]),
    ('Actividad', 'La OMS recomienda de 150 a 300 minutos a la semana de actividad moderada (o de 75 a 150 de vigorosa) y fuerza al menos dos días.', [('bull2020', 'Bull y cols., 2020')]),
    ('Fuerza de piernas', 'Levantarse de una silla es fuerza de piernas en estado puro. El test tiene valores de referencia de 60 a 94 años y un umbral relacionado con mantener la autonomía.', [('rikli1999', 'Rikli y Jones, 1999'), ('rikli2013', 'Rikli y Jones, 2013')]),
    ('Grasa abdominal', 'La cinta métrica dice más que la báscula sobre la grasa que rodea tus órganos. Rangos de la guía de NICE: saludable de 0,4 a 0,49.', [('nice2025', 'NICE, 2025')]),
]
for _i, _p in enumerate(CHQ_PASOS + CHQ_OPC):
    assert _p['u'] in HM, _p['u']
    _p['t'] = HM[_p['u']][2]; _p['i'] = HM[_p['u']][1]
_FU_IDS = {f['id']: f for f in FUENTES}
for _a, _t, _ids in CHQ_POR:
    for _id, _et in _ids: assert _id in _FU_IDS, _id
# Siguiente paso de cada área: los mismos enlaces que «¿Y ahora qué?» bajo cada herramienta (SIGUE de siguiente.py)
CHQ_SG = {p['u']: {z: [list(x) for x in L] for z, L in SIGUE[p['u']].items()} for p in CHQ_PASOS + CHQ_OPC if p['u'] in SIGUE}
_CHQ_D = json.dumps({'P': [{k: p[k] for k in ('u', 'a', 'q', 't')} for p in CHQ_PASOS], 'O': [{k: p[k] for k in ('u', 'a', 'q', 't')} for p in CHQ_OPC]}, ensure_ascii=False)

# ---- Barra de pasos y «Guardar y seguir» en las herramientas del chequeo (solo si llegan con ?chequeo=1) ----
CHQ_TOOL_JS = r"""(function(){var q;try{q=new URLSearchParams(location.search)}catch(e){return}if(!q.has('chequeo'))return;
var C=__D__,P=C.P,u=location.pathname.split('/').pop()||'index.html',i=-1,op=null,D=document;P.forEach(function(p,j){if(p.u===u)i=j});if(i<0)C.O.forEach(function(p){if(p.u===u)op=p});if(i<0&&!op)return;
var fin=op||i+1>=P.length,sig=fin?'chequeo.html#resumen':P[i+1].u+'?chequeo=1',m=D.querySelector('main');if(!m)return;
var nav=D.createElement('nav');nav.className='chq-barra';nav.setAttribute('aria-label','Chequeo de 10 minutos');
nav.innerHTML='<div class="in"><div class="chq-caja"><a class="chq-volver" href="chequeo.html"><span>Chequeo de 10 minutos</span></a>'+(op?'<p class="chq-et">Prueba opcional: '+op.a.toLowerCase()+'</p>':'<ol class="chq-mini">'+P.map(function(p,j){return '<li class="'+(j<i?'antes':j===i?'ahora':'')+'"'+(j===i?' aria-current="step"':'')+'><span>'+(j+1)+'</span><b>'+p.a+'</b></li>'}).join('')+'</ol><p class="chq-et">Paso '+(i+1)+' de '+P.length+'</p>')+'<a class="chq-saltar" href="'+sig+'">'+(op?'Volver al chequeo':fin?'Saltar y ver el resumen':'Saltar este paso')+'</a></div></div>';
m.insertBefore(nav,m.firstChild);
var r=D.querySelector('.tool-res'),g=r&&r.querySelector('.guarda-r');if(!g)return;
var b=D.createElement('button');b.type='button';b.className='btn peq chq-sig';b.textContent=fin?'Guardar y ver el resumen':'Guardar y seguir: '+P[i+1].a.toLowerCase();
var vv=r.querySelector('.guarda-ver');(vv||g).insertAdjacentElement('afterend',b);
function mira(){b.hidden=g.hidden}mira();new MutationObserver(mira).observe(g,{attributes:true,attributeFilter:['hidden']});
b.addEventListener('click',function(){g.click();var s=g.querySelector('span');if(s&&/^Guardado/.test(s.textContent))location.href=sig})})();""".replace('__D__', _CHQ_D)
for _p in CHQ_PASOS + CHQ_OPC:
    _parchea(_p['u'], '</main>', f'<script>{CHQ_TOOL_JS}</script></main>')

# ---- La página del chequeo ----
def _chq_paso(n, p):
    return (f'<li class="chq-paso sube" data-u="{p["u"]}"><span class="chq-num" aria-hidden="true">{n}</span>'
            f'<div class="chq-txt"><p class="chq-a"><i class="ic">{ico(p["i"])}</i>{p["a"]} · unos 2 minutos</p><h3>{p["q"]}</h3><p>{p["d"]}</p>'
            f'<p class="chq-est" data-est>Pendiente</p></div>'
            f'<a class="btn peq chq-b" href="{p["u"]}?chequeo=1" data-ir>Empezar<span class="oculto"> {p["a"].lower()}</span></a></li>')
def _chq_opc(p):
    return (f'<article class="chq-o sube" data-u="{p["u"]}"><p class="chq-a"><i class="ic">{ico(p["i"])}</i>{p["a"]}</p>'
            f'<h3><a href="{p["u"]}?chequeo=1" data-ir>{p["q"]}</a></h3><p>{p["cuando"]} {HM[p["u"]][3]}</p><p class="chq-est" data-est></p></article>')
def _chq_por(a, t, ids):
    fs = ' · '.join(f'<a href="fuentes.html#f-{i}">{et}</a>' for i, et in ids)
    return f'<div class="chq-por-c sube"><p class="chq-a">{a}</p><p>{t}</p><p class="chq-por-f">Fuente: {fs}</p></div>'
CHQ_JS = r"""(function(){var C=__D__,SG=__SG__,D=document,K='fbe-resultados',KC='fbe-chequeo',L=D.getElementById('chq-lista');if(!L)return;
function lee(k){try{var o=JSON.parse(localStorage.getItem(k)||'{}');return o&&typeof o==='object'?o:{}}catch(e){return {}}}
function pon(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function p2(x){return (x<10?'0':'')+x}function dm(t){var d=new Date(t||0);return p2(d.getDate())+'/'+p2(d.getMonth()+1)+'/'+d.getFullYear()}
function hoy(){var d=new Date();d.setHours(0,0,0,0);return d.getTime()}
function ultimo(o,u){var x=o[u];return x&&x.h&&x.h[0]?x.h[0]:null}
function arranca(){var c=lee(KC);if(!c.inicio){c.inicio=hoy();pon(KC,c)}}
function zona(e){return e&&e.z?'<p class="evo-zc z-'+esc(e.z)+'"><i aria-hidden="true"></i>'+esc(e.zt||'')+'</p>':''}
function linea(e){if(!e)return '';if(typeof e.v==='number')return esc(e.vt||'')+(e.u?' '+esc(e.u):'');return esc(e.zt||String(e.texto||'').split('\n')[0])}
function pinta(){var o=lee(K),c=lee(KC),ini=c.inicio||Infinity,hechos=0,prim=null,todos=C.P.concat(C.O),res=[];
  todos.forEach(function(p,j){var el=D.querySelector('[data-u="'+p.u+'"]');if(!el)return;var e=ultimo(o,p.u),h=e&&(e.t||0)>=ini,st=el.querySelector('[data-est]'),bt=el.querySelector('.chq-b');el.classList.toggle('hecho',!!h);
    if(j<C.P.length){if(h)hechos++;else if(prim===null)prim=j}
    st.innerHTML=h?'<b>Hecho el '+dm(e.t)+'</b> · '+linea(e):(e?'Último resultado: '+dm(e.t)+(c.inicio?', antes de este chequeo':'')+' · '+linea(e):(j<C.P.length?'Pendiente':''));
    if(bt)bt.firstChild.textContent=h?'Repetir':(e?'Hacer':'Empezar');
    if(h)res.push({p:p,e:e,op:j>=C.P.length})});
  D.getElementById('chq-hechos').textContent=hechos;D.getElementById('chq-rel').style.width=(hechos/C.P.length*100)+'%';
  var ir=D.getElementById('chq-ir'),rs=D.getElementById('chq-reset');
  if(hechos>=C.P.length){ir.textContent='Ver tu resumen';ir.href='#resumen';ir.removeAttribute('data-ir')}else{ir.textContent=hechos?'Seguir: paso '+(prim+1)+' de '+C.P.length:'Empezar el chequeo';ir.href=C.P[prim].u+'?chequeo=1';ir.setAttribute('data-ir','')}
  rs.hidden=!c.inicio;
  var S=D.getElementById('resumen'),R=D.getElementById('chq-rej');S.hidden=!res.length;
  R.innerHTML=res.map(function(x){var e=x.e,z=e.z?'z-'+e.z:'def',ls=(SG[x.p.u]||{})[z]||(SG[x.p.u]||{}).def||(SG[x.p.u]||{})['z-alto']||[];
    return '<article class="chq-r'+(x.op?' opc':'')+(e.z?' z-'+esc(e.z):'')+'"><p class="chq-a">'+esc(x.p.a)+(x.op?' · opcional':'')+'</p><h3><a href="'+esc(x.p.u)+'">'+esc(x.p.t)+'</a></h3>'
      +(typeof e.v==='number'?'<p class="chq-r-v"><b>'+esc(e.vt||'')+'</b>'+(e.u?'<span>'+esc(e.u)+'</span>':'')+'</p>'+zona(e):(e.z?zona(e):'<p class="chq-r-t">'+linea(e)+'</p>'))
      +'<p class="chq-r-f">'+dm(e.t)+(e.n?' · '+esc(e.n):'')+'</p>'
      +(ls.length?'<p class="chq-r-h">Qué hacer ahora</p><ul class="chq-r-l">'+ls.map(function(l){return '<li><a class="chq-r-a" href="'+esc(l[2])+'"'+(/^https?:/.test(l[2])?' rel="noopener"':'')+'><small>'+esc(l[0])+'</small>'+esc(l[1])+'</a></li>'}).join('')+'</ul>':'')+'</article>'}).join('');
  D.getElementById('chq-res-n').textContent=hechos>=C.P.length?'Has hecho las cuatro pruebas.':'Llevas '+hechos+' de '+C.P.length+'. Puedes seguir cuando quieras: se queda guardado en este navegador.'}
D.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-ir]');if(a)arranca()});
D.getElementById('chq-reset').addEventListener('click',function(){var c=lee(KC);c.inicio=Date.now();pon(KC,c);pinta();var t=D.getElementById('chq-av');t.textContent='Chequeo nuevo: los resultados anteriores siguen en Mis resultados.';setTimeout(function(){t.textContent=''},4000)});
pinta();window.addEventListener('pageshow',pinta);window.addEventListener('storage',pinta)})();"""
CHQ_JS = CHQ_JS.replace('__D__', _CHQ_D).replace('__SG__', json.dumps(CHQ_SG, ensure_ascii=False))
_CHQ_NEC = [('reloj', 'Unos 10 minutos y ropa cómoda'), ('silla', 'Una silla sin brazos, de unos 43 cm de alto, apoyada contra la pared'),
            ('cinta', 'Una cinta métrica'), ('check', 'Nada más: el cronómetro y las cuentas los pone la web')]
I.setdefault('silla', '<rect x="8" y="3" width="8" height="7" rx="1.5"/><path d="M6 13h12M8 10v3M16 10v3M7 13v8M17 13v8"/>')
_chq_cuerpo = f'''
<section class="chq-s"><div class="in">
  <div class="chq-cab sube">
    <div class="chq-nec"><h2 class="chq-h">Qué necesitas</h2><ul>{''.join(f'<li><i class="ic">{ico(i)}</i><span>{t}</span></li>' for i, t in _CHQ_NEC)}</ul></div>
    <div class="chq-prog"><p class="chq-n"><b id="chq-hechos">0</b> de {len(CHQ_PASOS)} pruebas</p><div class="chq-pista" aria-hidden="true"><i id="chq-rel"></i></div>
      <a class="btn" id="chq-ir" href="{CHQ_PASOS[0]['u']}?chequeo=1" data-ir>Empezar el chequeo</a>
      <button type="button" class="enl-b" id="chq-reset" hidden>Empezar de nuevo</button><p class="chq-av" id="chq-av" role="status"></p></div>
  </div>
  <h2 class="chq-h chq-h-pasos">Los cuatro pasos</h2>
  <ol class="chq-lista" id="chq-lista">{''.join(_chq_paso(n + 1, p) for n, p in enumerate(CHQ_PASOS))}</ol>
  <div class="chq-opc"><h2 class="chq-h">Si quieres, dos pruebas más</h2><div class="chq-opc-rej">{''.join(_chq_opc(p) for p in CHQ_OPC)}</div></div>
</div></section>
<section class="hoja chq-res-s" id="resumen" hidden aria-labelledby="chq-res-h"><div class="in">
  <div class="entrada sube"><h2 id="chq-res-h">Tu resumen</h2><p id="chq-res-n"></p><p>Cada resultado sale de su herramienta, con sus fuentes. Es orientativo, no un diagnóstico: si algo sale en la zona más baja, coméntalo con tu médico.</p></div>
  <div class="chq-rej" id="chq-rej"></div>
  <p class="chq-bots"><a class="btn" href="mis-resultados.html#mr-inf">Informe para tu médico</a><a class="btn hueco" href="mis-resultados.html">Ver Mis resultados</a></p>
</div></section>
<section class="hoja" id="chq-por" aria-labelledby="chq-por-h"><div class="in">
  <div class="entrada sube"><h2 id="chq-por-h">Por qué estas cuatro</h2><p>Son rápidas, se hacen en casa y cada una mira una cosa distinta. Lo que dice cada herramienta, en una frase:</p></div>
  <div class="chq-por-rej">{''.join(_chq_por(a, t, ids) for a, t, ids in CHQ_POR)}</div>
  <p class="sec-enl sube"><b>Más</b><a href="herramientas.html">Todas las herramientas</a><a href="empieza-aqui.html">Empieza aquí</a><a href="fuentes.html">Fuentes</a></p>
</div></section>
<script>{CHQ_JS}</script>'''
pagina('chequeo.html', 'Chequeo de 10 minutos',
       'Cuatro pruebas cortas: si conviene pasar antes por el médico, cuánto te mueves, la fuerza de tus piernas y tu grasa abdominal. Al final, un resumen.',
       'Chequeo de 10 minutos',
       'Cuatro pruebas cortas, en orden: si conviene pasar antes por el médico, cuánto te mueves, la fuerza de tus piernas y tu grasa abdominal. Al final tienes un resumen por áreas con el siguiente paso de cada una. Todo se queda en tu navegador.',
       _chq_cuerpo, padre=('herramientas.html', 'Herramientas'))
SEC_PAGS.append('chequeo.html')

# ---- Enlaces al chequeo ----
_CHQ_TARJ = (f'<aside class="chq-tarj sube" aria-labelledby="chq-tarj-h"><div class="chq-tarj-t"><p class="herr-et">¿No sabes por dónde empezar?</p><h2 id="chq-tarj-h">Chequeo de 10 minutos</h2>'
             f'<p>Cuatro pruebas en orden, con un resumen por áreas al final.</p></div><ol class="chq-tarj-p">{"".join(f"<li><span>{n + 1}</span>{p['a']}</li>" for n, p in enumerate(CHQ_PASOS))}</ol>'
             f'<a class="btn" href="chequeo.html">Hacer el chequeo</a></aside>\n  ')
_parchea('herramientas.html', '<section><div class="in herr-lista">\n  ', '<section><div class="in herr-lista">\n  ' + _CHQ_TARJ)
_parchea('empieza-aqui.html', '<p>Elige uno. Puedes cambiar cuando quieras.</p>', '<p>Elige uno. Puedes cambiar cuando quieras.</p><p class="ea-chq">¿Prefieres medirte antes? <a href="chequeo.html">Chequeo de 10 minutos</a></p>')
_parchea('mis-resultados.html', 'Si repites una prueba, se guardan las anteriores (hasta 12 por herramienta) para que veas tu evolución.</p>',
         'Si repites una prueba, se guardan las anteriores (hasta 12 por herramienta) para que veas tu evolución.</p><p class="mr-chq">¿No sabes por cuál empezar? <a class="btn peq" href="chequeo.html">Chequeo de 10 minutos</a></p>')
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_ix.append({'t': 'Chequeo de 10 minutos', 'u': 'chequeo.html', 'd': 'Cuatro pruebas en orden y un resumen por áreas: revisión médica, actividad, fuerza de piernas y grasa abdominal.',
            'k': 'chequeo empezar evaluar forma fisica test pruebas resumen por donde empiezo', 'y': 'Herramienta'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
