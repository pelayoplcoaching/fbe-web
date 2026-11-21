# ===== herramientas: cinco calculadoras (21/11/2026) =====
# Se concatena detrás de interior.py (antes del sitemap). Todo funciona en el navegador, sin guardar datos fuera del dispositivo.
# Fuentes de cada cifra al pie de cada página; no cambiar números sin cambiar la fuente.
PADRE_H = ('herramientas.html', 'Herramientas')

def fuentes_t(items):
    return '<ol class="fuentes-t">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

def campo_num(id_, etiqueta, valor, mn, mx, paso, ayuda=''):
    return (f'<div class="tool-campo"><label for="{id_}">{etiqueta}</label><div class="num-paso">'
            f'<button type="button" data-paso="-{paso}" data-para="{id_}" aria-label="Restar">−</button>'
            f'<input id="{id_}" type="number" inputmode="decimal" min="{mn}" max="{mx}" step="{paso}" value="{valor}">'
            f'<button type="button" data-paso="{paso}" data-para="{id_}" aria-label="Sumar">+</button></div>'
            + (f'<small>{ayuda}</small>' if ayuda else '') + '</div>')

def seg(nombre, etiqueta, opciones, sel=None, clase=''):
    return (f'<fieldset class="tool-campo seg-t {clase}"><legend>{etiqueta}</legend><div>'
            + ''.join(f'<label><input type="radio" name="{nombre}" value="{v}"{" checked" if v == sel else ""}><span>{t}</span></label>' for v, t in opciones)
            + '</div></fieldset>')

def tool_pagina(arch, titulo, desc, h1, sub, form, res, explica, fuentes, js, extra_sec='', slug='', tira=()):
    figs = ''.join(f'<figure class="tool-fig">{ilus(f"{slug}-{i + 1}", "tool-tira-img").replace("alt=\"\"", f"alt=\"{t}\"", 1)}<figcaption><b>{i + 1:02d}</b>{t}</figcaption></figure>' for i, t in enumerate(tira) if os.path.exists(f'web-img/{slug}-{i + 1}.webp'))
    tira_h = f'<div class="tool-tira sube">{figs}</div>' if figs else ''
    fondo = ilus(f'{slug}-fondo', 'tool-fondo') if slug else ''
    cuerpo = f'''
<section class="tool-s"><div class="in"><div class="tool sube">
  <form class="tool-form" onsubmit="return false" novalidate>{form}</form>
  <div class="tool-res" aria-live="polite">{fondo}{res}</div>
</div></div></section>
{extra_sec}
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Cómo se interpreta</h2></div>
  {tira_h}<div class="tool-explica sube">{explica}</div>
  <h3 class="fuentes-h sube">De dónde salen los números</h3>{fuentes_t(fuentes)}
</div></section>
{CTA_PP}
<script>{STEP_JS}{js}</script>'''
    pagina(arch, titulo, desc, h1, sub, cuerpo, padre=PADRE_H)

# Botones +/- de los campos numericos (delegado: vale para filas que se anaden despues) y formato es-ES
STEP_JS = r'''(function(){document.addEventListener('click',function(e){var b=e.target.closest('[data-paso]');if(!b)return;var i=document.getElementById(b.dataset.para)||b.parentNode.querySelector('input');if(!i)return;var p=parseFloat(b.dataset.paso),v=parseFloat(i.value);if(isNaN(v))v=parseFloat(i.min)||0;var mn=parseFloat(i.min),mx=parseFloat(i.max);v=Math.round((v+p)*100)/100;if(!isNaN(mn))v=Math.max(mn,v);if(!isNaN(mx))v=Math.min(mx,v);i.value=v;i.dispatchEvent(new Event('input',{bubbles:true}));});})();
window.fmt=function(x,d){return Number(x).toLocaleString('es-ES',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});};
'''

# ---------------------------------------------------------------------------------------------
# 1. Test de la silla en 30 segundos (Rikli y Jones)
SILLA_FORM = f'''
<details class="tool-como" open><summary>Cómo se hace</summary><ol>
  <li>Una silla firme sin brazos, de unos 43 cm de alto, apoyada contra la pared.</li>
  <li>Sentado en el centro, la espalda recta, los pies apoyados en el suelo y los brazos cruzados sobre el pecho.</li>
  <li>Al «ya», levántate del todo y vuelve a sentarte, tantas veces como puedas en 30 segundos.</li>
  <li>Cuenta cada vez que te pones de pie del todo. Si al acabar el tiempo estás más de medio camino arriba, cuenta.</li>
  <li>Si hacen falta los brazos para levantarse, se para: el resultado es 0.</li>
</ol><p class="tool-aviso">Mejor con alguien al lado. Si aparece mareo, dolor en el pecho o falta de aire, para. No es para quien no pueda levantarse sin ayuda.</p></details>
<div class="crono-t">
  <svg class="crono-anillo" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="pista"/><circle cx="60" cy="60" r="52" class="valor" id="s-arco" pathLength="100"/></svg>
  <div class="crono-num"><b id="s-seg">30</b><small id="s-estado">segundos</small></div>
</div>
<div class="crono-bots"><button type="button" class="btn" id="s-empezar">Empezar el test</button><button type="button" class="crono-mas" id="s-mas" disabled>+1 de pie</button></div>
{campo_num("s-reps", "Veces que te levantas", "", 0, 50, 1, "Lo rellena el contador; también puedes escribirlo.")}
<div class="tool-fila">{campo_num("s-edad", "Edad", 70, 40, 100, 1)}{seg("s-sexo", "Sexo", [("m", "Mujer"), ("h", "Hombre")], "m")}</div>'''

SILLA_RES = '''<p class="tool-et">Tu resultado</p>
<div class="res-grande"><b id="s-r-num">–</b><span>veces en 30 s</span></div>
<p class="res-veredicto" id="s-r-tit">Haz el test o escribe cuántas veces te has levantado.</p>
<div class="medidor" id="s-medidor" hidden><div class="medidor-pista"><span class="medidor-banda" id="s-banda"></span><i class="medidor-umbral" id="s-umbral"></i><i class="medidor-marca" id="s-marca"></i></div><div class="medidor-ley"><span><i class="ley-banda"></i>Rango normal para tu edad</span><span><i class="ley-umbral"></i>Umbral de autonomía</span></div></div>
<p class="res-texto" id="s-r-txt"></p>'''

SILLA_JS = r'''(function(){
var N={m:[[60,12,17,15],[65,11,16,15],[70,10,15,14],[75,10,15,13],[80,9,14,12],[85,8,13,11],[90,4,11,9]],h:[[60,14,19,17],[65,12,18,16],[70,12,17,15],[75,11,17,14],[80,10,15,13],[85,8,14,11],[90,7,12,9]]};
var $=function(i){return document.getElementById(i)};
var reps=$('s-reps'),edad=$('s-edad'),corre=false,t0=0,raf=0,prev=0;
function sexo(){var r=document.querySelector('input[name="s-sexo"]:checked');return r?r.value:'m'}
function pinta(){
  var n=parseInt(reps.value,10),e=parseInt(edad.value,10),s=sexo();
  var tit=$('s-r-tit'),txt=$('s-r-txt'),med=$('s-medidor');
  $('s-r-num').textContent=isNaN(n)?'–':n;
  var res=document.querySelector('.tool-res');res.classList.remove('z-bajo','z-medio','z-alto');
  if(isNaN(n)){tit.textContent='Haz el test o escribe cuántas veces te has levantado.';txt.textContent='';med.hidden=true;return}
  if(isNaN(e)||e<60){tit.textContent='Los valores de referencia de este test son para 60 a 94 años.';txt.textContent='Para menores de 60 no hay rangos comparables de este mismo estudio. Puedes usarlo para seguir tu propia evolución: repítelo cada pocas semanas y compara contigo.';med.hidden=true;return}
  var g=N[s][0];N[s].forEach(function(f){if(e>=f[0])g=f});
  var a=g[1],b=g[2],u=g[3],gr=e>94?'90 a 94':g[0]+' a '+(g[0]+4);
  var quien=(s==='m'?'mujeres':'hombres')+' de '+gr+' años';
  var max=Math.max(25,n+3,b+5),pc=function(x){return Math.max(0,Math.min(100,x/max*100))+'%'};
  med.hidden=false;$('s-banda').style.left=pc(a);$('s-banda').style.width='calc('+pc(b)+' - '+pc(a)+')';$('s-umbral').style.left=pc(u);$('s-marca').style.left=pc(n);
  var extra=e>94?' (con más de 94 años se usa el grupo de 90 a 94).':'.';
  if(n===0){res.classList.add('z-bajo');tit.textContent='0: no ha podido levantarse sin los brazos';txt.textContent='Si hacen falta los brazos para levantarse, el resultado cuenta como 0. Merece la pena comentarlo con el médico y empezar con ejercicios de fuerza adaptados.';return}
  if(n<a){res.classList.add('z-bajo');tit.textContent='Por debajo de lo normal para la edad';txt.textContent='El rango normal para '+quien+' es de '+a+' a '+b+' veces'+extra+' Por debajo de ese rango, la campaña STEADI de los CDC lo asocia a más riesgo de caídas. La fuerza de piernas se puede entrenar a cualquier edad: coméntalo con el médico y empieza con ejercicios de fuerza adaptados.'}
  else if(n<=b){res.classList.add('z-medio');tit.textContent='Dentro de lo normal para la edad';txt.textContent='El rango normal para '+quien+' es de '+a+' a '+b+' veces'+extra+' '+(n<u?'Aún está por debajo del umbral que Rikli y Jones proponen para mantener la autonomía hasta edades avanzadas ('+u+' veces): hay margen para ganar fuerza.':'Y llega al umbral que Rikli y Jones proponen para mantener la autonomía hasta edades avanzadas ('+u+' veces).')}
  else{res.classList.add('z-alto');tit.textContent='Por encima de lo normal para la edad';txt.textContent='Mejor que 3 de cada 4 '+quien+' (rango normal: de '+a+' a '+b+' veces)'+extra+' Mantenerlo es cosa de seguir entrenando la fuerza.'}
}
function arco(f){$('s-arco').style.strokeDashoffset=String(100-f*100)}
function para(fin){corre=false;cancelAnimationFrame(raf);$('s-mas').disabled=true;$('s-empezar').textContent='Repetir el test';$('s-seg').textContent=fin?'0':'30';$('s-estado').textContent=fin?'¡tiempo!':'segundos';arco(fin?1:0);if(fin&&navigator.vibrate)navigator.vibrate(300);pinta()}
function tic(){var t=(performance.now()-t0)/1000;
  if(t<0){var c=Math.ceil(-t);if(c!==prev){prev=c;$('s-seg').textContent=c;$('s-estado').textContent='preparados'}arco(0);raf=requestAnimationFrame(tic);return}
  if($('s-mas').disabled){$('s-mas').disabled=false;$('s-mas').focus();if(navigator.vibrate)navigator.vibrate(120)}
  var q=Math.max(0,30-t);$('s-seg').textContent=Math.ceil(q);$('s-estado').textContent='¡ya!';arco(Math.min(1,t/30));
  if(q<=0){para(true);return}raf=requestAnimationFrame(tic)}
$('s-empezar').addEventListener('click',function(){if(corre){para(false);return}corre=true;prev=0;reps.value=0;pinta();t0=performance.now()+3000;$('s-empezar').textContent='Parar';tic()});
$('s-mas').addEventListener('click',function(){if(!corre)return;reps.value=(parseInt(reps.value,10)||0)+1;pinta();var b=$('s-mas');b.classList.remove('toque');void b.offsetWidth;b.classList.add('toque')});
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('test-silla.html', 'Test de la silla en 30 segundos',
    'Test de la silla en 30 segundos: cronómetro, contador y comparación con los valores de referencia de Rikli y Jones para 60 a 94 años.',
    'La fuerza de piernas, en 30 segundos',
    'Cuántas veces te levantas de una silla en medio minuto dice mucho de la fuerza de las piernas a partir de los 60. Hazlo tú o hazlo con tus padres: cronómetro, contador y comparación con los valores de referencia.',
    SILLA_FORM, SILLA_RES,
    '''<p>El resultado se compara con el <b>rango normal</b> de su edad y sexo: el 50 % central de las personas de 60 a 94 años que viven en su casa, medidas en el estudio de referencia. Por debajo del rango, la campaña STEADI de los CDC lo asocia a más riesgo de caídas; por encima, está mejor que 3 de cada 4.</p>
<p>La línea dorada es el <b>umbral de autonomía</b> que proponen los mismos autores: el número de veces que conviene alcanzar a cada edad para mantener la capacidad de valerse por sí mismo en edades avanzadas.</p>
<p>No es un diagnóstico: orienta. Repetirlo cada pocas semanas es una buena forma de ver si el entrenamiento de fuerza está funcionando.</p>''',
    ['Rikli RE, Jones CJ. Functional fitness normative scores for community-residing older adults, ages 60-94. J Aging Phys Act. 1999 (rangos normales).',
     'Rikli RE, Jones CJ. Development and validation of criterion-referenced clinically relevant fitness standards for maintaining physical independence in later years. Gerontologist. 2013 (umbral de autonomía).',
     'CDC. STEADI: The 30-Second Chair Stand (resultado por debajo de la media y riesgo de caídas).'],
    SILLA_JS, slug='silla', tira=('Sentado, con los brazos cruzados', 'De pie del todo', 'Tantas veces como puedas en 30 segundos'))

# ---------------------------------------------------------------------------------------------
# 2. Calculadora de 1RM y cargas por esfuerzo (Epley y Brzycki)
RM_FORM = f'''
<div class="tool-fila">{campo_num("r-peso", "Peso de la serie (kg)", 60, 1, 500, 2.5)}{campo_num("r-reps", "Repeticiones hechas", 8, 1, 15, 1)}</div>
{seg("r-rir", "¿Cuántas te quedaban?", [("0", "Ninguna"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], "2")}
{seg("r-red", "Redondear las cargas a", [("2.5", "2,5 kg"), ("1", "1 kg"), ("0", "Sin redondeo")], "2.5")}
<p class="tool-nota">No hace falta ir al fallo para estimarlo: haz una serie de 3 a 10 repeticiones dejando 1 o 2 en reserva y apunta cuántas te quedaban.</p>'''

RM_RES = '''<p class="tool-et">Tu 1RM estimado</p>
<div class="res-grande"><b id="r-r-num">–</b><span>kg</span></div>
<p class="res-veredicto" id="r-r-tit"></p>
<p class="res-texto" id="r-r-txt"></p>'''

RM_TABLA = '''<section class="tool-s"><div class="in"><div class="entrada sube"><h2>Con qué peso trabajar</h2><p>Busca la fila de las repeticiones que quieres hacer y la columna de las que quieres dejar en reserva. La casilla marcada es tu serie.</p></div>
<div class="tabla-t-caja sube"><table class="tabla-t" id="r-tabla"><thead><tr><th scope="col">Repeticiones</th><th scope="col">Al fallo</th><th scope="col">1 en reserva</th><th scope="col">2 en reserva</th><th scope="col">3 en reserva</th></tr></thead><tbody></tbody></table></div></div></section>'''

RM_JS = r'''(function(){
var $=function(i){return document.getElementById(i)};
function val(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?parseFloat(r.value):0}
function pct(n){return n<=1?1:1/(1+n/30)}
function red(x,r){return r>0?Math.round(x/r)*r:Math.round(x*10)/10}
function f1(x){return fmt(x,Math.abs(x%1)>1e-9?1:0)}
function pinta(){
  var w=parseFloat($('r-peso').value),k=parseInt($('r-reps').value,10),rir=val('r-rir'),r=val('r-red');
  var tb=document.querySelector('#r-tabla tbody');
  if(!(w>0)||!(k>=1)){$('r-r-num').textContent='–';$('r-r-tit').textContent='Escribe el peso y las repeticiones.';$('r-r-txt').textContent='';tb.innerHTML='';return}
  var n=k+rir,rm=w/pct(n),bz=n<37?w*36/(37-n):NaN;
  $('r-r-num').textContent=f1(red(rm,r));
  $('r-r-tit').textContent=n===1?'Una repetición al fallo: tu 1RM es ese peso.':'Equivale a unas '+n+' repeticiones hasta el fallo.';
  $('r-r-txt').textContent=(isNaN(bz)||n===1?'':'Con la fórmula de Brzycki saldría '+f1(red(bz,r))+' kg. ')+(n>10?'Con más de 10 repeticiones hasta el fallo la estimación pierde precisión: mejor una serie más pesada.':'Hasta unas 10 repeticiones hasta el fallo, las dos fórmulas dan valores parecidos.');
  var h='';for(var f=1;f<=12;f++){h+='<tr><th scope="row">'+f+'</th>';for(var c=0;c<=3;c++){var m=f===k&&c===rir;h+='<td'+(m?' class="tu"':'')+'>'+f1(red(rm*pct(f+c),r))+'<small>'+fmt(pct(f+c)*100,0)+' %</small></td>'}h+='</tr>'}tb.innerHTML=h;
}
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('calculadora-1rm.html', 'Calculadora de 1RM y cargas',
    'Calculadora de 1RM: tu máximo estimado con las fórmulas de Epley y Brzycki y una tabla de cargas según las repeticiones que dejas en reserva.',
    'Tu máximo estimado, y con qué peso trabajar',
    'Mete el peso y las repeticiones de una serie, y cuántas te quedaban. Te calculo tu 1RM estimado y una tabla de cargas según cuántas repeticiones quieres dejar en reserva.',
    RM_FORM, RM_RES,
    '''<p>El <b>1RM</b> es el peso que podrías levantar una sola vez. No hace falta probarlo: se estima bien a partir de una serie, sumando las repeticiones hechas y las que te quedaban. La calculadora usa la fórmula de Epley para todo (así la tabla vuelve a dar tu serie) y enseña la de Brzycki como comparación.</p>
<p>Las repeticiones en reserva sirven para dosificar el esfuerzo. Según la revisión de Robinson y cols., la fuerza mejora parecido en un rango amplio de esfuerzo y el músculo crece algo más cuanto más cerca del fallo. Por eso no todas las series tienen que ir al fallo.</p>
<p>Es una estimación: el cansancio del día, la técnica y el ejercicio cambian el número. Úsala para orientarte y ajusta con lo que notas en la barra.</p>''',
    ['Epley B. Poundage chart. Boyd Epley Workout. 1985 (1RM = peso × (1 + repeticiones / 30)).',
     'Brzycki M. Strength testing: predicting a one-rep max from reps-to-fatigue. J Phys Educ Recreat Dance. 1993;64(1):88-90 (1RM = peso × 36 / (37 − repeticiones)).',
     'Robinson ZP y cols. Exploring the dose-response relationship between estimated resistance training proximity to failure, strength gain, and muscle hypertrophy. Sports Med. 2024;54(9):2209-31.'],
    RM_JS, extra_sec=RM_TABLA, slug='rm', tira=('Una serie de 3 a 10 repeticiones', 'Cuenta las que te quedaban', 'Elige la carga en la tabla'))

# ---------------------------------------------------------------------------------------------
# 3. Contador de volumen semanal (recuento fraccional de Pelland y cols.; zonas de Schoenfeld y cols. 2017)
VOL_MUSC = [('pecho', 'Pecho'), ('espalda', 'Espalda'), ('hombros', 'Hombros'), ('biceps', 'Bíceps'), ('triceps', 'Tríceps'), ('cuadriceps', 'Cuádriceps'), ('isquios', 'Isquiotibiales'), ('gluteos', 'Glúteos'), ('gemelos', 'Gemelos'), ('abdomen', 'Abdomen')]
VOL_EJ = [
 ('Pecho', [('banca', 'Press de banca', {'pecho': 1, 'triceps': .5, 'hombros': .5}), ('inclinado', 'Press inclinado', {'pecho': 1, 'hombros': .5, 'triceps': .5}), ('fondos', 'Fondos en paralelas', {'pecho': 1, 'triceps': .5, 'hombros': .5}), ('flexiones', 'Flexiones', {'pecho': 1, 'triceps': .5, 'hombros': .5}), ('aperturas', 'Aperturas o contractora', {'pecho': 1})]),
 ('Espalda', [('dominadas', 'Dominadas', {'espalda': 1, 'biceps': .5}), ('jalon', 'Jalón al pecho', {'espalda': 1, 'biceps': .5}), ('remo', 'Remo (barra, mancuerna o polea)', {'espalda': 1, 'biceps': .5, 'hombros': .5}), ('pullover', 'Pullover en polea', {'espalda': 1})]),
 ('Hombros y brazos', [('militar', 'Press militar', {'hombros': 1, 'triceps': .5}), ('laterales', 'Elevaciones laterales', {'hombros': 1}), ('pajaros', 'Pájaros o face pull', {'hombros': 1, 'espalda': .5}), ('curl', 'Curl de bíceps', {'biceps': 1}), ('triceps', 'Extensión de tríceps', {'triceps': 1})]),
 ('Pierna', [('sentadilla', 'Sentadilla', {'cuadriceps': 1, 'gluteos': .5}), ('prensa', 'Prensa de piernas', {'cuadriceps': 1, 'gluteos': .5}), ('zancadas', 'Zancadas o sentadilla búlgara', {'cuadriceps': 1, 'gluteos': .5}), ('extension', 'Extensión de cuádriceps', {'cuadriceps': 1}), ('muerto', 'Peso muerto', {'gluteos': 1, 'isquios': .5, 'cuadriceps': .5}), ('rumano', 'Peso muerto rumano', {'isquios': 1, 'gluteos': .5}), ('femoral', 'Curl femoral', {'isquios': 1}), ('hipthrust', 'Hip thrust o puente de glúteo', {'gluteos': 1, 'isquios': .5}), ('gemelos', 'Elevación de gemelos', {'gemelos': 1})]),
 ('Tronco', [('abdominal', 'Abdominales (crunch, rueda, elevaciones)', {'abdomen': 1}), ('plancha', 'Plancha y variantes', {'abdomen': 1})]),
]
VOL_FORM = '''<p class="tool-et">Tu semana</p>
<div class="vol-filas" id="v-filas"></div>
<div class="vol-bots"><button type="button" class="btn" id="v-mas">Añadir ejercicio</button><button type="button" class="enl-b" id="v-ejemplo">Cargar un ejemplo</button><button type="button" class="enl-b" id="v-vaciar">Vaciar</button></div>
<p class="tool-nota">Cuenta las series de toda la semana (si haces 3 series dos días, son 6). Solo las exigentes, las que acabas a pocas repeticiones del fallo; los calentamientos no cuentan. Se guarda en este navegador.</p>'''
VOL_RES = '''<p class="tool-et">Series por músculo a la semana</p>
<div class="vol-barras" id="v-barras"></div>
<div class="vol-ley"><span><i class="z0"></i>Menos de 5</span><span><i class="z1"></i>De 5 a 9</span><span><i class="z2"></i>10 o más</span></div>
<p class="res-texto" id="v-resumen"></p>'''
VOL_JS = r'''(function(){
var M=__MUSC__,G=__EJ__,E={};G.forEach(function(g){g[1].forEach(function(e){E[e[0]]=e})});
var $=function(i){return document.getElementById(i)},filas=$('v-filas'),K='fbe-volumen';
var opts=G.map(function(g){return '<optgroup label="'+g[0]+'">'+g[1].map(function(e){return '<option value="'+e[0]+'">'+e[1]+'</option>'}).join('')+'</optgroup>'}).join('');
var nid=0;
function fila(ej,s){var id='v-s'+(nid++),d=document.createElement('div');d.className='vol-fila';
  d.innerHTML='<label class="sr" for="'+id+'e">Ejercicio</label><select id="'+id+'e">'+opts+'</select><div class="num-paso"><button type="button" data-paso="-1" data-para="'+id+'" aria-label="Restar">−</button><input id="'+id+'" type="number" inputmode="numeric" min="0" max="40" step="1" value="'+(s==null?3:s)+'" aria-label="Series a la semana"><button type="button" data-paso="1" data-para="'+id+'" aria-label="Sumar">+</button></div><button type="button" class="vol-quita" aria-label="Quitar este ejercicio">×</button>';
  if(ej)d.querySelector('select').value=ej;filas.appendChild(d);return d}
function lee(){return [].map.call(filas.querySelectorAll('.vol-fila'),function(d){return [d.querySelector('select').value,parseFloat(d.querySelector('input').value)||0]})}
function guarda(){try{localStorage.setItem(K,JSON.stringify(lee()))}catch(e){}}
function pinta(){var t={};M.forEach(function(m){t[m[0]]=0});
  lee().forEach(function(r){var e=E[r[0]];if(!e)return;for(var m in e[2])t[m]+=e[2][m]*r[1]});
  var max=Math.max(20,Math.max.apply(null,M.map(function(m){return t[m[0]]}))),c=[0,0,0],h='';
  M.forEach(function(m){var v=t[m[0]],z=v>=10?2:(v>=5?1:0);if(v>0)c[z]++;
    h+='<div class="vol-b z'+(v>0?z:'n')+'"><span class="vol-n">'+m[1]+'</span><span class="vol-pista"><i style="left:'+(5/max*100)+'%"></i><i style="left:'+(10/max*100)+'%"></i><b style="width:'+Math.min(100,v/max*100)+'%"></b></span><span class="vol-v">'+fmt(v,v%1?1:0)+'</span></div>'});
  $('v-barras').innerHTML=h;
  var n=lee().length;$('v-resumen').textContent=n?('Músculos con 10 o más series: '+c[2]+'. Entre 5 y 9: '+c[1]+'. Por debajo de 5: '+c[0]+'. Las series que trabajan un músculo de forma indirecta cuentan la mitad.'):'Añade los ejercicios de tu semana para ver el reparto.';
  guarda()}
filas.addEventListener('input',pinta);filas.addEventListener('change',pinta);
filas.addEventListener('click',function(e){if(e.target.classList.contains('vol-quita')){e.target.closest('.vol-fila').remove();pinta()}});
$('v-mas').addEventListener('click',function(){var d=fila(null,null);d.querySelector('select').focus();pinta()});
$('v-ejemplo').addEventListener('click',function(){filas.innerHTML='';[['sentadilla',9],['banca',9],['remo',9],['rumano',6],['militar',6],['jalon',6],['curl',6],['triceps',6],['gemelos',6],['plancha',6]].forEach(function(r){fila(r[0],r[1])});pinta()});
$('v-vaciar').addEventListener('click',function(){filas.innerHTML='';pinta()});
var g=null;try{g=JSON.parse(localStorage.getItem(K)||'null')}catch(e){}
if(Array.isArray(g)&&g.length)g.forEach(function(r){if(E[r[0]])fila(r[0],r[1])});else{fila('sentadilla',6);fila('banca',6);fila('remo',6)}
pinta();
})();'''.replace('__MUSC__', json.dumps(VOL_MUSC, ensure_ascii=False)).replace('__EJ__', json.dumps([[g, [[i, n, d] for i, n, d in es]] for g, es in VOL_EJ], ensure_ascii=False))

tool_pagina('volumen-semanal.html', 'Contador de volumen semanal',
    'Contador de volumen semanal: apunta tus ejercicios y series y mira cuántas series haces por músculo, comparadas con lo que dice la evidencia.',
    '¿Cuántas series haces por músculo a la semana?',
    'Apunta los ejercicios de tu semana y cuántas series haces de cada uno. Te dibujo el volumen por músculo y lo comparo con lo que dice la evidencia.',
    VOL_FORM, VOL_RES,
    '''<p>En el metaanálisis de Schoenfeld, Ogborn y Krieger, el músculo crecía más con más series semanales, de forma gradual: menos de 5 series a la semana por músculo, de 5 a 9, y 10 o más. Por eso las bandas de las barras van en 5 y en 10.</p>
<p>Más series siguen sumando, pero cada vez menos: el análisis más reciente de Pelland y cols. encuentra rendimientos decrecientes. Si vas sobrado de volumen y te recuperas mal, quitar series suele ser mejor idea que añadir.</p>
<p>Cada ejercicio cuenta 1 serie para el músculo principal y media para los que ayudan (el press de banca suma 1 al pecho y 0,5 al tríceps y al hombro). Es el recuento «fraccional» que mejor predijo los resultados en ese análisis. El reparto de cada ejercicio es orientativo.</p>''',
    ['Schoenfeld BJ, Ogborn D, Krieger JW. Dose-response relationship between weekly resistance training volume and increases in muscle mass: a systematic review and meta-analysis. J Sports Sci. 2017;35(11):1073-82.',
     'Pelland JC y cols. The resistance training dose-response: meta-regressions exploring the effects of weekly volume and frequency on muscle hypertrophy and strength gain. SportRxiv. 2024 (recuento fraccional y rendimientos decrecientes).'],
    VOL_JS, slug='volumen', tira=('La serie directa cuenta 1', 'La indirecta cuenta media', 'Más series suman, cada vez menos'))

# ---------------------------------------------------------------------------------------------
# 4. Calculadora de cafeína y sueño (EFSA 2015; vida media IOM 2001; Gardiner y cols. 2023)
CAF_BEB = [('espresso', 'Espresso (60 ml)', 80), ('filtro', 'Café de filtro (200 ml)', 90), ('te', 'Té negro (220 ml)', 50), ('cola', 'Refresco de cola (lata, 355 ml)', 40), ('energetica', 'Bebida energética (lata, 250 ml)', 80), ('choco-negro', 'Chocolate negro (50 g)', 25), ('choco-leche', 'Chocolate con leche (50 g)', 10), ('otro', 'Preentreno u otro (mg)', 200)]
CAF_FORM = '''<p class="tool-et">Añade lo que tomas en un día</p>
<div class="caf-rapidos" id="c-rapidos"></div>
<div class="caf-filas" id="c-filas"></div>
<div class="tool-fila"><div class="tool-campo"><label for="c-dormir">Me acuesto a las</label><input id="c-dormir" type="time" value="23:00"></div>
<div class="tool-campo"><span class="tool-et">Situación</span><label class="caf-check"><input type="checkbox" id="c-embarazo"><span>Embarazo o lactancia</span></label></div></div>
<p class="tool-nota">Los miligramos son valores orientativos de la EFSA; cada marca y cada taza cambian. Si tu preentreno o tu bebida dice otra cantidad en la etiqueta, usa «Otro» y escríbela.</p>'''
CAF_RES = '''<p class="tool-et">Cafeína del día</p>
<div class="res-grande"><b id="c-r-total">0</b><span>mg</span></div>
<div class="medidor caf-med"><div class="medidor-pista"><b class="medidor-relleno" id="c-relleno"></b></div><div class="medidor-ley"><span id="c-limite-t">Límite EFSA: 400 mg al día</span></div></div>
<svg class="caf-curva" id="c-curva" viewBox="0 0 600 190" role="img" aria-label="Cafeína estimada en el cuerpo a lo largo del día"></svg>
<p class="res-veredicto" id="c-r-tit"></p>
<ul class="res-lista" id="c-r-lista"></ul>'''
CAF_JS = r'''(function(){
var B=__BEB__,BB={};B.forEach(function(b){BB[b[0]]=b});
var $=function(i){return document.getElementById(i)},filas=$('c-filas'),K='fbe-cafeina',VM=5;
var opts=B.map(function(b){return '<option value="'+b[0]+'">'+b[1]+'</option>'}).join('');
$('c-rapidos').innerHTML=B.filter(function(b){return b[0]!=='choco-leche'}).map(function(b){return '<button type="button" class="chip-b" data-b="'+b[0]+'">+ '+b[1].replace(/ \(.*$/,'').replace(/:.*$/,'')+'</button>'}).join('');
function mins(t){var p=(t||'').split(':');return p.length<2?NaN:parseInt(p[0],10)*60+parseInt(p[1],10)}
function hhmm(m){m=((m%1440)+1440)%1440;return String(Math.floor(m/60)).padStart(2,'0')+':'+String(Math.round(m%60)).padStart(2,'0')}
var nid=0;
function fila(b,h,mg){var id='c-t'+(nid++),d=document.createElement('div');d.className='caf-fila';
  d.innerHTML='<label class="sr" for="'+id+'b">Bebida</label><select id="'+id+'b">'+opts+'</select><input class="caf-mg" type="number" inputmode="numeric" min="0" max="1000" step="10" aria-label="Miligramos de cafeína" value="'+(mg||BB[b][2])+'"><label class="sr" for="'+id+'h">Hora</label><input id="'+id+'h" type="time" value="'+h+'"><button type="button" class="vol-quita" aria-label="Quitar">×</button>';
  d.querySelector('select').value=b;filas.appendChild(d);ajusta(d);return d}
function ajusta(d){var b=d.querySelector('select').value,mg=d.querySelector('.caf-mg');mg.hidden=b!=='otro';if(b!=='otro')mg.value=BB[b][2]}
function lee(){return [].map.call(filas.querySelectorAll('.caf-fila'),function(d){var b=d.querySelector('select').value;return {b:b,mg:parseFloat(d.querySelector('.caf-mg').value)||0,h:d.querySelector('input[type=time]').value}})}
function guarda(){try{localStorage.setItem(K,JSON.stringify({t:lee(),d:$('c-dormir').value,e:$('c-embarazo').checked}))}catch(e){}}
function pinta(){
  var T=lee().filter(function(t){return !isNaN(mins(t.h))}).map(function(t){return {b:t.b,mg:t.mg,m:mins(t.h)}}).sort(function(a,b){return a.m-b.m});
  var tot=T.reduce(function(s,t){return s+t.mg},0),lim=$('c-embarazo').checked?200:400;
  $('c-r-total').textContent=fmt(tot);$('c-limite-t').textContent='Límite EFSA: '+lim+' mg al día'+(lim===200?' en embarazo o lactancia':'');
  $('c-relleno').style.width=Math.min(100,tot/lim*100)+'%';$('c-relleno').className='medidor-relleno'+(tot>lim?' pasa':'');
  var res=document.querySelector('.tool-res');res.classList.remove('z-bajo','z-medio','z-alto');
  var dm=mins($('c-dormir').value),li=[];
  if(!T.length){$('c-r-tit').textContent='Añade tus cafés, tés o refrescos con su hora.';$('c-r-lista').innerHTML='';$('c-curva').innerHTML='';guarda();return}
  if(isNaN(dm))dm=23*60;var ult=T[T.length-1].m;if(dm<=ult)dm+=1440;
  var q=function(x){return T.reduce(function(s,t){return x>=t.m?s+t.mg*Math.pow(.5,(x-t.m)/60/VM):s},0)};
  var cama=q(dm),may=Math.max.apply(null,T.map(function(t){return t.mg}));
  li.push(tot>lim?'Pasas el límite de la EFSA ('+lim+' mg al día) en '+fmt(tot-lim)+' mg.':'Estás dentro del límite de la EFSA ('+lim+' mg al día).');
  if(may>200)li.push('Tu toma más grande tiene '+fmt(may)+' mg; la EFSA considera seguras tomas de hasta 200 mg de una vez.');
  li.push('Al acostarte te quedarían unos '+fmt(cama)+' mg en el cuerpo (cálculo aproximado: el cuerpo elimina la mitad cada '+VM+' horas de media, aunque en cada persona va de 1,5 a 9,5).');
  T.forEach(function(t){var hs=(dm-t.m)/60,n=BB[t.b]?BB[t.b][1].replace(/ \(.*$/,'').replace(/:.*$/,''):'Toma';
    if(t.mg>=150&&hs<13.2)li.push(n+' de las '+hhmm(t.m)+' ('+fmt(t.mg)+' mg): queda a '+fmt(hs,1)+' h de dormir. Para un preentreno de unos 217 mg, Gardiner y cols. proponen tomarlo al menos 13,2 h antes.');
    else if(t.mg>=60&&t.mg<150&&hs<8.8)li.push(n+' de las '+hhmm(t.m)+': queda a '+fmt(hs,1)+' h de dormir. Para un café de unos 107 mg, Gardiner y cols. proponen al menos 8,8 h antes de acostarse.')});
  var hora=li.some(function(x){return x.indexOf('Gardiner')>=0}),dosis=may>200;
  res.classList.add(cama>=100||tot>lim?'z-bajo':(hora||dosis?'z-medio':'z-alto'));
  $('c-r-tit').textContent=cama>=100?'Te acuestas con 100 mg o más: puede costarte dormir':(tot>lim?'Te pasas del límite diario':(hora?'Revisa la hora de algún café':(dosis?'Alguna toma pasa de 200 mg':'Buena pinta para tu sueño')));
  $('c-r-lista').innerHTML=li.map(function(x){return '<li>'+x+'</li>'}).join('');
  // curva
  var x0=T[0].m-60,x1=dm+120,ymax=Math.max(150,Math.max.apply(null,T.map(function(t){return q(t.m)}))*1.1),W=600,H=190,L=36,R=10,Tp=12,Bt=26;
  var X=function(m){return L+(m-x0)/(x1-x0)*(W-L-R)},Y=function(v){return Tp+(1-v/ymax)*(H-Tp-Bt)};
  var p='',a='';for(var m=x0;m<=x1;m+=5){var v=q(m);p+=(m===x0?'M':'L')+X(m).toFixed(1)+' '+Y(v).toFixed(1)}
  a=p+'L'+X(x1).toFixed(1)+' '+Y(0)+'L'+X(x0).toFixed(1)+' '+Y(0)+'Z';
  var ej='';for(var hh=Math.ceil(x0/120)*120;hh<=x1;hh+=120)ej+='<line class="g" x1="'+X(hh)+'" x2="'+X(hh)+'" y1="'+Tp+'" y2="'+Y(0)+'"/><text class="t" x="'+X(hh)+'" y="'+(H-8)+'" text-anchor="middle">'+hhmm(hh).slice(0,2)+'h</text>';
  $('c-curva').innerHTML=ej+'<line class="cien" x1="'+L+'" x2="'+(W-R)+'" y1="'+Y(100)+'" y2="'+Y(100)+'"/><text class="t" x="'+(L-4)+'" y="'+(Y(100)+4)+'" text-anchor="end">100</text><path class="area" d="'+a+'"/><path class="linea" d="'+p+'"/><line class="cama" x1="'+X(dm)+'" x2="'+X(dm)+'" y1="'+Tp+'" y2="'+Y(0)+'"/><circle class="punto" cx="'+X(dm)+'" cy="'+Y(cama)+'" r="5"/><text class="t cama-t" x="'+(X(dm)-6)+'" y="'+(Tp+12)+'" text-anchor="end">a dormir</text>';
  guarda()}
filas.addEventListener('change',function(e){if(e.target.tagName==='SELECT')ajusta(e.target.closest('.caf-fila'));pinta()});
filas.addEventListener('input',pinta);
filas.addEventListener('click',function(e){if(e.target.classList.contains('vol-quita')){e.target.closest('.caf-fila').remove();pinta()}});
$('c-rapidos').addEventListener('click',function(e){var b=e.target.closest('[data-b]');if(!b)return;var T=lee().map(function(t){return mins(t.h)}).filter(function(m){return !isNaN(m)}),h=T.length?Math.min(Math.max.apply(null,T)+120,22*60):8*60;fila(b.dataset.b,hhmm(h));pinta()});
$('c-dormir').addEventListener('input',pinta);$('c-embarazo').addEventListener('change',pinta);
var g=null;try{g=JSON.parse(localStorage.getItem(K)||'null')}catch(e){}
if(g&&Array.isArray(g.t)){g.t.forEach(function(t){if(BB[t.b])fila(t.b,t.h,t.mg)});if(g.d)$('c-dormir').value=g.d;$('c-embarazo').checked=!!g.e}else{fila('espresso','08:00');fila('filtro','11:00');fila('espresso','16:30')}
pinta();
})();'''.replace('__BEB__', json.dumps(CAF_BEB, ensure_ascii=False))

tool_pagina('cafeina.html', 'Calculadora de cafeína y sueño',
    'Calculadora de cafeína: suma la cafeína de tu día, compárala con el límite de la EFSA y mira cuánta te queda en el cuerpo al acostarte.',
    '¿Cuánta cafeína tomas, y cuánta te queda al acostarte?',
    'Apunta tus cafés, tés, refrescos o preentrenos con su hora. Te digo los miligramos del día, si pasas el límite de la EFSA y cuánta cafeína te queda en el cuerpo a la hora de dormir.',
    CAF_FORM, CAF_RES,
    '''<p>La <b>EFSA</b> considera seguras para adultos sanos hasta 400 mg de cafeína al día y tomas de hasta 200 mg de una vez; en embarazo y lactancia, hasta 200 mg al día. También señala que 100 mg cerca de la hora de dormir pueden alargar lo que tardas en dormirte y acortar el sueño en algunas personas.</p>
<p>La curva es una estimación sencilla: supone que el cuerpo elimina la mitad de la cafeína cada 5 horas, que es la media en adultos sanos. En cada persona va de 1,5 a 9,5 horas (influyen la genética, el tabaco, el embarazo o algunos fármacos), así que tómala como orientación.</p>
<p>En el metaanálisis de Gardiner y cols., para no perder sueño, un café (unos 107 mg) debería tomarse al menos 8,8 horas antes de acostarse y un preentreno (unos 217 mg), al menos 13,2 horas antes; para una taza de té no encontraron hora límite. La calculadora aplica esos cortes a las tomas de 60 a 149 mg y de 150 mg o más.</p>''',
    ['EFSA NDA Panel. Scientific opinion on the safety of caffeine. EFSA Journal. 2015;13(5):4102 (límites y cantidades orientativas por bebida).',
     'Institute of Medicine. Caffeine for the sustainment of mental task performance. National Academies Press; 2001 (vida media de unas 5 h, de 1,5 a 9,5 h).',
     'Gardiner C y cols. The effect of caffeine on subsequent sleep: a systematic review and meta-analysis. Sleep Med Rev. 2023;69:101764.'],
    CAF_JS, slug='cafeina', tira=('Cuánta tomas', 'A qué hora', 'Cuánta queda al dormir'))

# ---------------------------------------------------------------------------------------------
# 5. ¿Necesito revisión médica antes de empezar? (algoritmo ACSM 2015; textos de Pauta Activa, en tú)
REV_SINT = [('dolor_pecho', 'Dolor, opresión o molestia en el pecho, cuello, mandíbula o brazos con el esfuerzo'), ('disnea', 'Falta de aire en reposo o con esfuerzos pequeños'), ('sincope', 'Mareos intensos o desmayos'), ('ortopnea', 'Falta de aire al acostarte o que te despierta por la noche'), ('edema', 'Hinchazón de los tobillos'), ('palpitaciones', 'Palpitaciones o latidos rápidos o irregulares'), ('claudicacion', 'Dolor en las piernas al caminar que cede al parar'), ('soplo', 'Te han dicho que tienes un soplo cardíaco'), ('fatiga', 'Cansancio o falta de aire inusuales con actividades normales')]
REV_FORM = (seg('q-regular', '1. ¿Haces ejercicio con regularidad? Al menos 30 minutos de intensidad moderada, 3 días por semana, en los últimos 3 meses.', [('si', 'Sí'), ('no', 'No')], clase='rev-q')
    + seg('q-enf', '2. ¿Te han diagnosticado una enfermedad del corazón o de las arterias, diabetes o una enfermedad del riñón?', [('si', 'Sí'), ('no', 'No')], clase='rev-q')
    + '<fieldset class="tool-campo rev-sint rev-q"><legend>3. ¿Notas alguno de estos síntomas?</legend>'
    + ''.join(f'<label class="caf-check"><input type="checkbox" name="q-sint" value="{i}"><span>{t}</span></label>' for i, t in REV_SINT)
    + '<label class="caf-check ninguno"><input type="checkbox" id="q-ninguno"><span>Ninguno de estos</span></label></fieldset>'
    + '<p class="tool-aviso">Si tienes dolor en el pecho en reposo, que no cede, o con sudor frío o falta de aire, no esperes: llama al 112.</p>')
REV_RES = '''<p class="tool-et">Resultado</p>
<p class="res-veredicto grande-t" id="q-r-tit">Responde a las tres preguntas.</p>
<p class="res-texto" id="q-r-txt">Son las del algoritmo de cribado del ACSM (2015). No es un examen ni bloquea nada: solo orienta.</p>
<ul class="res-lista" id="q-r-lista"></ul>'''
REV_JS = r'''(function(){
var $=function(i){return document.getElementById(i)};
var T={empezar:['z-alto','Puedes empezar','No hace falta una valoración médica previa. Empieza a intensidad ligera o moderada y súbela poco a poco.',['Ligera o moderada: puedes hablar mientras lo haces, aunque no cantar.','Sube la intensidad o el tiempo poco a poco, semana a semana.','Si aparece alguno de los síntomas de la lista, para y consulta.']],
continuar:['z-alto','Puedes seguir como hasta ahora','Puedes continuar con ejercicio moderado o vigoroso y progresar como venías haciendo.',['Si aparece alguno de los síntomas de la lista, para y consulta.']],
valoracion_vigoroso:['z-medio','Sigue, pero consulta antes de apretar más','Puedes seguir con ejercicio moderado; antes de pasar a intensidad vigorosa conviene una valoración médica.',['Moderado: puedes hablar, aunque no cantar. Vigoroso: solo puedes decir frases cortas.','Comenta con tu médico que quieres subir la intensidad.']],
valoracion_antes:['z-medio','Mejor una valoración médica antes de empezar','Conviene que te valore tu médico antes de empezar a entrenar; mientras tanto, actividad ligera, como caminar a paso cómodo.',['Lleva a la consulta tu lista de medicación y qué tipo de ejercicio quieres hacer.','Tras la valoración, empieza suave y progresa poco a poco.']],
valoracion_sint:['z-bajo','Con estos síntomas, consulta antes de empezar','Esos síntomas hay que valorarlos antes de empezar a entrenar. Pide cita con tu médico y cuéntaselos.',['Mientras tanto, nada de ejercicio intenso.','Tras la valoración, empieza suave y progresa poco a poco.']],
parar:['z-bajo','Para y consulta antes de seguir','Tienes síntomas que hay que valorar: deja el ejercicio moderado o intenso y consulta con tu médico antes de retomarlo.',['Cuéntale cuándo aparecen los síntomas y con qué esfuerzo.','Vuelve a entrenar cuando te lo indique.']]};
function radio(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
var nin=$('q-ninguno'),sint=[].slice.call(document.querySelectorAll('input[name="q-sint"]'));
sint.forEach(function(c){c.addEventListener('change',function(){if(c.checked)nin.checked=false})});
nin.addEventListener('change',function(){if(nin.checked)sint.forEach(function(c){c.checked=false})});
function pinta(){var reg=radio('q-regular'),enf=radio('q-enf'),s=sint.filter(function(c){return c.checked}).length,res=document.querySelector('.tool-res');
  res.classList.remove('z-bajo','z-medio','z-alto');
  if(!reg||!enf||(!s&&!nin.checked)){$('q-r-tit').textContent='Responde a las tres preguntas.';$('q-r-txt').textContent='Son las del algoritmo de cribado del ACSM (2015). No es un examen ni bloquea nada: solo orienta.';$('q-r-lista').innerHTML='';return}
  var k=s?(reg==='si'?'parar':'valoracion_sint'):(reg==='no'?(enf==='si'?'valoracion_antes':'empezar'):(enf==='si'?'valoracion_vigoroso':'continuar'));
  var t=T[k];res.classList.add(t[0]);$('q-r-tit').textContent=t[1];$('q-r-txt').textContent=t[2];$('q-r-lista').innerHTML=t[3].map(function(x){return '<li>'+x+'</li>'}).join('')}
document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('revision-medica.html', '¿Necesito revisión médica antes de entrenar?',
    '¿Necesito revisión médica antes de empezar a entrenar? Tres preguntas del algoritmo de cribado del ACSM (2015) que te orientan en un minuto.',
    '¿Necesito revisión médica antes de empezar a entrenar?',
    'Tres preguntas del algoritmo de cribado del Colegio Americano de Medicina del Deporte (ACSM, 2015). No sustituye a tu médico: te orienta sobre si conviene una valoración antes de empezar o de subir la intensidad.',
    REV_FORM, REV_RES,
    f'''<p>El algoritmo del ACSM se fija en tres cosas: si ya haces ejercicio con regularidad, si tienes una enfermedad cardiovascular, metabólica (diabetes) o renal diagnosticada, y si tienes síntomas que la sugieran. Con eso decide si hace falta una valoración médica antes de empezar o antes de subir a intensidad vigorosa.</p>
<p>No pregunta por la edad ni por el colesterol: en la versión de 2015 se quitaron los factores de riesgo porque llevaban a mandar a revisión a mucha gente sin beneficio claro, y el ejercicio moderado es seguro para la mayoría.</p>
<p>Si tomas medicación, mira también <a href="pauta-activa.html">Pauta Activa</a>: incluye este mismo cribado y te dice qué tener en cuenta al entrenar con tus fármacos.</p>''',
    ['Riebe D y cols. Updating ACSM\'s recommendations for exercise preparticipation health screening. Med Sci Sports Exerc. 2015;47(11):2473-9.'],
    REV_JS, slug='revision', tira=('¿Haces ejercicio con regularidad?', '¿Alguna enfermedad diagnosticada?', '¿Síntomas con el esfuerzo?'))

# ---------------------------------------------------------------------------------------------
# Tarjetas de las cinco en Herramientas (las inserta el bloque de abajo antes de la nota final)
HERR_MAS = [('test-silla.html', 'silla', 'reloj', 'Test de la silla en 30 segundos', 'Cronómetro, contador y comparación con los valores de referencia de 60 a 94 años.'),
    ('calculadora-1rm.html', 'rm', 'pesa', 'Calculadora de 1RM', 'Tu máximo estimado y una tabla de cargas según las repeticiones en reserva.'),
    ('volumen-semanal.html', 'volumen', 'grafica', 'Contador de volumen semanal', 'Series por músculo a la semana, comparadas con la evidencia.'),
    ('cafeina.html', 'cafeina', 'luna', 'Cafeína y sueño', 'Miligramos del día, límite de la EFSA y cuánta te queda al acostarte.'),
    ('revision-medica.html', 'revision', 'check', '¿Necesito revisión médica?', 'Tres preguntas del cribado del ACSM antes de empezar a entrenar.')]
_h = open(f'{SAL}/herramientas.html', encoding='utf-8').read()
_mas = ('<div class="herr-mas sube"><h2 class="herr-mas-t">Más herramientas</h2><div class="herr-mas-rej">'
    + ''.join(f'<a class="herr-mini" href="{u}">{ilus(f"herr-{sl}", "herr-mini-img") or f"<i class=\"ic\">{ico(i)}</i>"}<b>{t}</b><span>{d}</span></a>' for u, sl, i, t, d in HERR_MAS)
    + '</div></div>\n  <p class="herr-nota sube">')
assert '<p class="herr-nota sube">' in _h
open(f'{SAL}/herramientas.html', 'w', encoding='utf-8').write(_h.replace('<p class="herr-nota sube">', _mas, 1))
