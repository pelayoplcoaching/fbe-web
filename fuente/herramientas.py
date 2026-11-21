# ===== herramientas: cinco calculadoras (21/11/2026) =====
# Se concatena detrás de interior.py (antes del sitemap). Todo funciona en el navegador, sin guardar datos fuera del dispositivo.
# Fuentes de cada cifra al pie de cada página; no cambiar números sin cambiar la fuente.
PADRE_H = ('herramientas.html', 'Herramientas')

def fuentes_t(items):
    return '<ol class="fuentes-t">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

def campo_num(id_, etiqueta, valor, mn, mx, paso, ayuda='', ud=''):
    return (f'<div class="tool-campo"><label for="{id_}">{etiqueta}</label><div class="num-paso"' + (f' data-ud="{ud}"' if ud else '') + '>'
            f'<button type="button" data-paso="-{paso}" data-para="{id_}" aria-label="Restar">−</button>'
            f'<input id="{id_}" type="number" inputmode="decimal" min="{mn}" max="{mx}" step="{paso}" value="{valor}">'
            f'<button type="button" data-paso="{paso}" data-para="{id_}" aria-label="Sumar">+</button></div>'
            + (f'<small>{ayuda}</small>' if ayuda else '') + '</div>')

def copiar_b(id_, texto, oculto=True):
    return f'<button type="button" class="copiar-t" id="{id_}"{" hidden" if oculto else ""}><span>{texto}</span></button>'

def seg(nombre, etiqueta, opciones, sel=None, clase=''):
    return (f'<fieldset class="tool-campo seg-t {clase}"><legend>{etiqueta}</legend><div>'
            + ''.join(f'<label><input type="radio" name="{nombre}" value="{v}"{" checked" if v == sel else ""}><span>{t}</span></label>' for v, t in opciones)
            + '</div></fieldset>')

def tool_pagina(arch, titulo, desc, h1, sub, form, res, explica, fuentes, js, extra_sec='', slug='', tira=()):
    figs = ''.join(f'<figure class="tool-fig">{ilus(f"{slug}-{i + 1}", "tool-tira-img").replace("alt=\"\"", f"alt=\"{t}\"", 1)}<figcaption><b>{i + 1:02d}</b>{t}</figcaption></figure>' for i, t in enumerate(tira) if os.path.exists(f'web-img/{slug}-{i + 1}.webp'))
    todas = bool(tira) and all(os.path.exists(f'web-img/{slug}-{i + 1}.webp') for i in range(len(tira)))
    tira_h = f'<div class="tool-tira sube">{figs}</div>' if todas else ''
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
window.copiar=function(b,t){var s=b.querySelector('span');b.dataset.t=b.dataset.t||s.textContent;function ok(){b.classList.add('hecho');s.textContent='Copiado';setTimeout(function(){b.classList.remove('hecho');s.textContent=b.dataset.t},1800)}if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,function(){})}else{var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy');ok()}catch(e){}a.remove()}};
window.destella=function(el){if(!el)return;el.classList.remove('destello');void el.offsetWidth;el.classList.add('destello')};
'''

# ---------------------------------------------------------------------------------------------
# 1. Test de la silla en 30 segundos (Rikli y Jones)
_M = __import__('math')
_TICKS = ''.join(f'<line x1="{60 + (38.5 if i % 5 == 0 else 41) * _M.cos(2 * _M.pi * i / 30):.2f}" y1="{60 + (38.5 if i % 5 == 0 else 41) * _M.sin(2 * _M.pi * i / 30):.2f}" x2="{60 + 44 * _M.cos(2 * _M.pi * i / 30):.2f}" y2="{60 + 44 * _M.sin(2 * _M.pi * i / 30):.2f}"{" class=\"may\"" if i % 5 == 0 else ""}/>' for i in range(30))
SILLA_FORM = f'''
<details class="tool-como" open><summary>Cómo se hace</summary><ol>
  <li>Una silla firme sin brazos, de unos 43 cm de alto, apoyada contra la pared.</li>
  <li>Sentado en el centro, la espalda recta, los pies apoyados en el suelo y los brazos cruzados sobre el pecho.</li>
  <li>Al «ya», levántate del todo y vuelve a sentarte, tantas veces como puedas en 30 segundos.</li>
  <li>Cuenta cada vez que te pones de pie del todo. Si al acabar el tiempo estás más de medio camino arriba, cuenta.</li>
  <li>Si hacen falta los brazos para levantarse, se para: el resultado es 0.</li>
</ol><p class="tool-aviso">Mejor con alguien al lado. Si aparece mareo, dolor en el pecho o falta de aire, para. No es para quien no pueda levantarse sin ayuda.</p></details>
<div class="crono-t" id="s-crono">
  <svg class="crono-anillo" viewBox="0 0 120 120" aria-hidden="true"><defs><linearGradient id="s-grad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="g1"/><stop offset=".6" class="g2"/><stop offset="1" class="g3"/></linearGradient></defs><g class="marcas-t">{_TICKS}</g><circle cx="60" cy="60" r="52" class="pista"/><circle cx="60" cy="60" r="52" class="valor" id="s-arco" pathLength="100"/></svg>
  <div class="crono-num"><b id="s-seg">30</b><small id="s-estado">segundos</small></div>
</div>
<div class="crono-bots"><button type="button" class="btn" id="s-empezar">Empezar el test</button><button type="button" class="crono-mas" id="s-mas" disabled>+1 de pie <b id="s-mas-n">0</b></button></div>
<p class="crono-hint" id="s-hint">Al pulsar «Empezar» tienes 3 segundos para prepararte.</p>
{campo_num("s-reps", "Veces que te levantas", "", 0, 50, 1, "Lo rellena el contador; también puedes escribirlo o corregirlo.")}
<div class="tool-fila">{campo_num("s-edad", "Edad", 70, 40, 100, 1, ud="años")}{seg("s-sexo", "Sexo", [("m", "Mujer"), ("h", "Hombre")], "m")}</div>
<p class="tool-chip" id="s-grupo"></p>'''

SILLA_RES = f'''<p class="tool-et">Tu resultado</p>
<div class="res-grande"><b id="s-r-num">–</b><span>veces en 30 s</span></div>
<p class="res-veredicto" id="s-r-tit">Haz el test o escribe cuántas veces te has levantado.</p>
<p class="res-chip" id="s-pct" hidden></p>
<div class="medidor" id="s-medidor" hidden><div class="medidor-pista"><span class="medidor-banda" id="s-banda"></span><i class="medidor-umbral" id="s-umbral"></i><i class="medidor-marca" id="s-marca" data-n=""></i></div><div class="medidor-esc" id="s-esc" aria-hidden="true"></div><div class="medidor-ley"><span><i class="ley-banda"></i>Rango normal para la edad</span><span><i class="ley-umbral"></i>Umbral de autonomía</span></div></div>
<p class="res-texto" id="s-r-txt"></p>
{copiar_b("s-copiar", "Copiar resultado")}'''

SILLA_JS = r'''(function(){
var N={m:[[60,12,17,15],[65,11,16,15],[70,10,15,14],[75,10,15,13],[80,9,14,12],[85,8,13,11],[90,4,11,9]],h:[[60,14,19,17],[65,12,18,16],[70,12,17,15],[75,11,17,14],[80,10,15,13],[85,8,14,11],[90,7,12,9]]};
var $=function(i){return document.getElementById(i)};
var reps=$('s-reps'),edad=$('s-edad'),cr=$('s-crono'),corre=false,t0=0,raf=0,prev=0,copia='';
function sexo(){var r=document.querySelector('input[name="s-sexo"]:checked');return r?r.value:'m'}
function pinta(){
  var n=parseInt(reps.value,10),e=parseInt(edad.value,10),s=sexo();
  var tit=$('s-r-tit'),txt=$('s-r-txt'),med=$('s-medidor'),pct=$('s-pct'),cp=$('s-copiar');
  $('s-r-num').textContent=isNaN(n)?'–':n;$('s-mas-n').textContent=isNaN(n)?0:n;
  var res=document.querySelector('.tool-res');res.classList.remove('z-bajo','z-medio','z-alto');pct.hidden=true;cp.hidden=true;
  var g=N[s][0];N[s].forEach(function(f){if(e>=f[0])g=f});
  var gr=e>94?'90 a 94':g[0]+' a '+(g[0]+4),quien=(s==='m'?'mujeres':'hombres')+' de '+gr+' años';
  $('s-grupo').textContent=!isNaN(e)&&e>=60?'Se compara con '+quien+'.':'';
  if(isNaN(n)){tit.textContent='Haz el test o escribe cuántas veces te has levantado.';txt.textContent='';med.hidden=true;return}
  if(isNaN(e)||e<60){tit.textContent='Los valores de referencia de este test son para 60 a 94 años.';txt.textContent='Para menores de 60 no hay rangos comparables de este mismo estudio. Puedes usarlo para seguir tu propia evolución: repítelo cada pocas semanas y compara contigo.';med.hidden=true;return}
  var a=g[1],b=g[2],u=g[3];
  var max=Math.max(25,n+3,b+5),pc=function(x){return Math.max(0,Math.min(100,x/max*100))+'%'};
  med.hidden=false;$('s-banda').style.left=pc(a);$('s-banda').style.width='calc('+pc(b)+' - '+pc(a)+')';$('s-umbral').style.left=pc(u);$('s-marca').style.left=pc(n);$('s-marca').setAttribute('data-n',n);
  $('s-esc').innerHTML='<span style="left:0">0</span><span style="left:'+pc(a)+'">'+a+'</span><span style="left:'+pc(b)+'">'+b+'</span><span class="ult" style="left:100%">'+max+'</span>';
  var extra=e>94?' (con más de 94 años se usa el grupo de 90 a 94).':'.',p='';
  if(n===0){res.classList.add('z-bajo');tit.textContent='0: no ha podido levantarse sin los brazos';txt.textContent='Si hacen falta los brazos para levantarse, el resultado cuenta como 0. Merece la pena comentarlo con el médico y empezar con ejercicios de fuerza adaptados.';p='Por debajo del 25 % de su grupo'}
  else if(n<a){res.classList.add('z-bajo');tit.textContent='Por debajo de lo normal para la edad';txt.textContent='El rango normal para '+quien+' es de '+a+' a '+b+' veces'+extra+' Por debajo de ese rango, la campaña STEADI de los CDC lo asocia a más riesgo de caídas. La fuerza de piernas se puede entrenar a cualquier edad: coméntalo con el médico y empieza con ejercicios de fuerza adaptados.';p='Por debajo del 25 % de su grupo'}
  else if(n<=b){res.classList.add('z-medio');tit.textContent='Dentro de lo normal para la edad';txt.textContent='El rango normal para '+quien+' es de '+a+' a '+b+' veces'+extra+' '+(n<u?'Aún está por debajo del umbral que Rikli y Jones proponen para mantener la autonomía hasta edades avanzadas ('+u+' veces): hay margen para ganar fuerza.':'Y llega al umbral que Rikli y Jones proponen para mantener la autonomía hasta edades avanzadas ('+u+' veces).');p='En el 50 % central de su grupo'}
  else{res.classList.add('z-alto');tit.textContent='Por encima de lo normal para la edad';txt.textContent='Mejor que 3 de cada 4 '+quien+' (rango normal: de '+a+' a '+b+' veces)'+extra+' Mantenerlo es cosa de seguir entrenando la fuerza.';p='Por encima del 75 % de su grupo'}
  pct.textContent=p;pct.hidden=false;
  copia='Test de la silla en 30 segundos: '+n+' veces ('+quien+'). '+tit.textContent+'. Rango normal: '+a+' a '+b+'; umbral de autonomía: '+u+' (Rikli y Jones).';cp.hidden=false;
}
function arco(f){$('s-arco').style.strokeDashoffset=String(100-f*100)}
function para(fin){corre=false;cancelAnimationFrame(raf);$('s-mas').disabled=true;$('s-empezar').textContent='Repetir el test';$('s-seg').textContent=fin?'0':'30';$('s-estado').textContent=fin?'¡tiempo!':'segundos';arco(fin?1:0);cr.className='crono-t'+(fin?' acabado':'');$('s-hint').textContent=fin?'Si te has equivocado al contar, corrige el número aquí debajo.':'Al pulsar «Empezar» tienes 3 segundos para prepararte.';if(fin&&navigator.vibrate)navigator.vibrate(300);pinta()}
function tic(){var t=(performance.now()-t0)/1000;
  if(t<0){var c=Math.ceil(-t);if(c!==prev){prev=c;$('s-seg').textContent=c;$('s-estado').textContent='preparados';destella($('s-seg'))}cr.className='crono-t prep';arco(0);raf=requestAnimationFrame(tic);return}
  if($('s-mas').disabled){$('s-mas').disabled=false;$('s-mas').focus();cr.className='crono-t corre';$('s-hint').textContent='Pulsa «+1 de pie» cada vez que se ponga de pie del todo.';if(navigator.vibrate)navigator.vibrate(120)}
  var q=Math.max(0,30-t);$('s-seg').textContent=Math.ceil(q);$('s-estado').textContent='¡ya!';arco(Math.min(1,t/30));if(q<=5)cr.classList.add('final');
  if(q<=0){para(true);return}raf=requestAnimationFrame(tic)}
$('s-empezar').addEventListener('click',function(){if(corre){para(false);return}corre=true;prev=0;reps.value=0;pinta();t0=performance.now()+3000;$('s-empezar').textContent='Parar';tic()});
$('s-mas').addEventListener('click',function(){if(!corre)return;reps.value=(parseInt(reps.value,10)||0)+1;pinta();var b=$('s-mas');b.classList.remove('toque');void b.offsetWidth;b.classList.add('toque')});
$('s-copiar').addEventListener('click',function(){copiar(this,copia)});
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
<div class="tool-fila">{campo_num("r-peso", "Peso de la serie", 60, 1, 500, 2.5, ud="kg")}{campo_num("r-reps", "Repeticiones hechas", 8, 1, 15, 1, ud="rep.")}</div>
{seg("r-rir", "¿Cuántas te quedaban?", [("0", "Ninguna"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], "2", clase="rir")}
{seg("r-red", "Redondear las cargas a", [("2.5", "2,5 kg"), ("1", "1 kg"), ("0", "Sin redondeo")], "2.5")}
<p class="tool-nota">No hace falta ir al fallo para estimarlo: haz una serie de 3 a 10 repeticiones dejando 1 o 2 en reserva y apunta cuántas te quedaban.</p>'''

RM_RES = '''<p class="tool-et">Tu 1RM estimado</p>
<div class="res-grande"><b id="r-r-num">–</b><span>kg</span></div>
<p class="rm-serie" id="r-serie"></p>
<div class="rm-escala" aria-hidden="true"><div class="rm-pista"><span class="rm-fiable"></span><i id="r-n-marca"></i></div><div class="rm-esc-l"><span>1</span><span>10</span><span>20</span></div><p class="rm-esc-t">Repeticiones hasta el fallo · la estimación es fiable hasta 10</p></div>
<p class="res-veredicto" id="r-r-tit"></p>
<p class="res-texto" id="r-r-txt"></p>
<div class="discos-caja"><p class="tool-et" id="r-discos-et">Discos para el 1RM</p><svg class="discos" id="r-discos" viewBox="0 0 320 120" role="img" aria-label="Discos por lado de la barra"></svg><p class="res-texto discos-t" id="r-discos-t"></p></div>'''

RM_TABLA = f'''<section class="tool-s"><div class="in"><div class="entrada sube"><h2>Con qué peso trabajar</h2><p>Busca la fila de las repeticiones que quieres hacer y la columna de las que quieres dejar en reserva. La casilla marcada es tu serie; toca cualquier otra para ver sus discos.</p></div>
<div class="tabla-t-cab sube"><p class="tabla-t-cap" id="r-cap"></p>{copiar_b("r-copiar", "Copiar tabla", False)}</div>
<div class="tabla-t-caja sube"><table class="tabla-t" id="r-tabla"><thead><tr><th scope="col">Repeticiones</th><th scope="col">Al fallo<small>RIR 0</small></th><th scope="col">1 en reserva<small>RIR 1</small></th><th scope="col">2 en reserva<small>RIR 2</small></th><th scope="col">3 en reserva<small>RIR 3</small></th></tr></thead><tbody></tbody></table></div></div></section>'''

RM_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},sel=null,ultimo='',copia='';
function val(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?parseFloat(r.value):0}
function pct(n){return n<=1?1:1/(1+n/30)}
function red(x,r){return r>0?Math.round(x/r)*r:Math.round(x*10)/10}
function f1(x){return fmt(x,Math.abs(x%1)>1e-9?1:0)}
function discos(carga){var svg=$('r-discos'),t=$('r-discos-t');
  if(!(carga>0)){svg.innerHTML='';t.textContent='';return}
  if(carga<20){svg.innerHTML='';t.textContent='Menos que la barra olímpica de 20 kg: usa mancuernas o una barra más ligera.';return}
  var lado=(carga-20)/2,P=[25,20,15,10,5,2.5,1.25],u=[];P.forEach(function(p){while(lado>=p-1e-9){u.push(p);lado-=p}});
  var H={25:100,20:92,15:82,10:70,5:54,2.5:44,1.25:36},W={25:15,20:13,15:12,10:10,5:8,2.5:7,1.25:6},x=82,pl='';
  u.forEach(function(p){if(x>290)return;var hh=H[p],w=W[p];pl+='<rect class="d d'+String(p).replace('.','_')+'" x="'+x+'" y="'+(60-hh/2)+'" width="'+w+'" height="'+hh+'" rx="2.5"><title>'+fp(p)+' kg</title></rect>';x+=w+2});
  var fin=Math.min(316,x+24),dx=Math.max(0,(320-fin)/2);
  svg.innerHTML='<g transform="translate('+dx.toFixed(1)+' 0)"><rect class="barra" x="4" y="57.5" width="70" height="5" rx="2.5"/><rect class="manga" x="76" y="55" width="'+(fin-76)+'" height="10" rx="3"/><rect class="tope" x="72" y="46" width="9" height="28" rx="2"/>'+pl+'</g>';
  t.textContent=u.length?'Por lado: '+u.map(fp).join(' + ')+' kg, con barra de 20 kg'+(lado>0.01?' (sobran '+fp(lado*2)+' kg que no salen con discos)':'')+'.':'Solo la barra de 20 kg.'}
function fp(x){return fmt(x,Math.abs(x*10%1)>1e-6?2:(Math.abs(x%1)>1e-6?1:0))}
function pinta(){
  var w=parseFloat($('r-peso').value),k=parseInt($('r-reps').value,10),rir=val('r-rir'),r=val('r-red');
  var tb=document.querySelector('#r-tabla tbody');
  if(!(w>0)||!(k>=1)){$('r-r-num').textContent='–';$('r-r-tit').textContent='Escribe el peso y las repeticiones.';$('r-r-txt').textContent='';$('r-serie').textContent='';tb.innerHTML='';discos(0);return}
  var n=k+rir,rm=w/pct(n),bz=n<37?w*36/(37-n):NaN,v=f1(red(rm,r));
  $('r-r-num').textContent=v;if(v!==ultimo){destella($('r-r-num'));ultimo=v}
  $('r-serie').textContent='Tu serie: '+f1(w)+' kg × '+k+' · '+(rir?rir+' en reserva':'al fallo');
  $('r-n-marca').style.left=Math.min(100,(n-1)/19*100)+'%';$('r-n-marca').className=n>10?'fuera':'';
  $('r-r-tit').textContent=n===1?'Una repetición al fallo: tu 1RM es ese peso.':'Equivale a unas '+n+' repeticiones hasta el fallo.';
  $('r-r-txt').textContent=(isNaN(bz)||n===1?'':'Con la fórmula de Brzycki saldría '+f1(red(bz,r))+' kg. ')+(n>10?'Con más de 10 repeticiones hasta el fallo la estimación pierde precisión: mejor una serie más pesada.':'Hasta unas 10 repeticiones hasta el fallo, las dos fórmulas dan valores parecidos.');
  var h='',lin=['Repeticiones; al fallo; 1 en reserva; 2 en reserva; 3 en reserva'];
  for(var f=1;f<=12;f++){var l=[f];h+='<tr'+(f===k?' class="fila-tu"':'')+'><th scope="row">'+f+'</th>';for(var c=0;c<=3;c++){var m=f===k&&c===rir,s=sel&&sel[0]===f&&sel[1]===c,p=pct(f+c),cg=red(rm*p,r);l.push(f1(cg)+' kg');h+='<td tabindex="0" data-f="'+f+'" data-c="'+c+'" style="--a:'+Math.max(0,Math.min(.32,(p-.62)/.38*.32)).toFixed(3)+'" class="'+(m?'tu':'')+(s?' sel':'')+'">'+f1(cg)+'<small>'+fmt(p*100,0)+' %</small></td>'}h+='</tr>';lin.push(l.join('; '))}
  tb.innerHTML=h;
  $('r-cap').textContent='1RM '+v+' kg · Epley · '+(r>0?'redondeo a '+f1(r)+' kg':'sin redondeo');
  copia='Tabla de cargas (1RM estimado '+v+' kg, Epley)\n'+lin.join('\n');
  if(sel){var cg2=red(rm*pct(sel[0]+sel[1]),r);$('r-discos-et').textContent='Discos para '+sel[0]+' repeticiones '+(sel[1]?'con '+sel[1]+' en reserva':'al fallo')+': '+f1(cg2)+' kg';discos(cg2)}
  else{$('r-discos-et').textContent='Discos para el 1RM: '+v+' kg';discos(red(rm,r))}
}
var tabla=$('r-tabla');
function cruz(td){[].forEach.call(tabla.querySelectorAll('.cruz'),function(x){x.classList.remove('cruz')});if(!td)return;var c=td.cellIndex;[].forEach.call(td.parentNode.children,function(x){x.classList.add('cruz')});[].forEach.call(tabla.rows,function(tr){if(tr.cells[c])tr.cells[c].classList.add('cruz')})}
tabla.addEventListener('mouseover',function(e){cruz(e.target.closest('td'))});tabla.addEventListener('mouseleave',function(){cruz(null)});
tabla.addEventListener('focusin',function(e){cruz(e.target.closest('td'))});
function elige(td){if(!td)return;var f=+td.dataset.f,c=+td.dataset.c;sel=sel&&sel[0]===f&&sel[1]===c?null:[f,c];pinta();var n=tabla.querySelector('td[data-f="'+f+'"][data-c="'+c+'"]');if(n)n.focus()}
tabla.addEventListener('click',function(e){elige(e.target.closest('td'))});
tabla.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();elige(e.target.closest('td'))}});
$('r-copiar').addEventListener('click',function(){copiar(this,copia)});
document.querySelector('.tool-form').addEventListener('input',function(){sel=null;pinta()});document.querySelector('.tool-form').addEventListener('change',function(){sel=null;pinta()});pinta();
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
<div class="caf-rapidos vol-rapidos" id="v-rapidos" role="group" aria-label="Añadir rápido"></div>
<div class="vol-filas" id="v-filas"></div>
<p class="vol-vacio" id="v-vacio" hidden>Todavía no hay ejercicios. Añade uno con los botones de arriba o carga el ejemplo.</p>
<div class="vol-bots"><button type="button" class="btn" id="v-mas">Añadir ejercicio</button><button type="button" class="enl-b" id="v-ejemplo">Cargar un ejemplo</button><button type="button" class="enl-b" id="v-vaciar">Vaciar</button></div>
<p class="vol-aviso" id="v-aviso" role="status"></p>
<p class="tool-nota">Cuenta las series de toda la semana (si haces 3 series dos días, son 6). Solo las exigentes, las que acabas a pocas repeticiones del fallo; los calentamientos no cuentan. Se guarda en este navegador.</p>'''
VOL_RES = f'''<p class="tool-et">Series por músculo a la semana</p>
<div class="vol-tiles"><div class="t2"><b id="v-t2">0</b><span>músculos con 10 o más</span></div><div class="t1"><b id="v-t1">0</b><span>de 5 a 9</span></div><div class="t0"><b id="v-t0">0</b><span>menos de 5</span></div><div class="tt"><b id="v-tot">0</b><span>series anotadas</span></div></div>
<div class="vol-cab"><button type="button" class="enl-b claro" id="v-orden" aria-pressed="false">Ordenar por series</button></div>
<div class="vol-barras" id="v-barras"></div>
<div class="vol-ley"><span><i class="z0"></i>Menos de 5</span><span><i class="z1"></i>De 5 a 9</span><span><i class="z2"></i>10 o más</span></div>
<p class="res-texto" id="v-resumen"></p>
{copiar_b("v-copiar", "Copiar resumen")}'''
VOL_JS = r'''(function(){
var M=__MUSC__,G=__EJ__,E={},MN={};G.forEach(function(g){g[1].forEach(function(e){E[e[0]]=e})});M.forEach(function(m){MN[m[0]]=m[1]});
var GR=[['Tren superior',['pecho','espalda','hombros','biceps','triceps']],['Tren inferior',['cuadriceps','isquios','gluteos','gemelos']],['Tronco',['abdomen']]];
var $=function(i){return document.getElementById(i)},filas=$('v-filas'),K='fbe-volumen',porSeries=false,copia='',deshacer=null,tAviso=0;
var quieto=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var opts=G.map(function(g){return '<optgroup label="'+g[0]+'">'+g[1].map(function(e){return '<option value="'+e[0]+'">'+e[1]+'</option>'}).join('')+'</optgroup>'}).join('');
$('v-rapidos').innerHTML=['sentadilla','banca','remo','dominadas','rumano','militar','hipthrust','curl'].map(function(k){return '<button type="button" class="chip-b" data-e="'+k+'">+ '+E[k][1].replace(/ \(.*$/,'').replace(/ o .*$/,'')+'</button>'}).join('');
var nid=0;
function fila(ej,s,nueva){var id='v-s'+(nid++),d=document.createElement('div');d.className='vol-fila'+(nueva?' nueva':'');
  d.innerHTML='<span class="vol-i" aria-hidden="true"></span><label class="sr" for="'+id+'e">Ejercicio</label><select id="'+id+'e">'+opts+'</select><div class="num-paso" data-ud="series"><button type="button" data-paso="-1" data-para="'+id+'" aria-label="Restar">−</button><input id="'+id+'" type="number" inputmode="numeric" min="0" max="40" step="1" value="'+(s==null?3:s)+'" aria-label="Series a la semana"><button type="button" data-paso="1" data-para="'+id+'" aria-label="Sumar">+</button></div><button type="button" class="vol-quita" aria-label="Quitar este ejercicio">×</button><p class="vol-musc"></p>';
  if(ej)d.querySelector('select').value=ej;filas.appendChild(d);return d}
function lee(){return [].map.call(filas.querySelectorAll('.vol-fila'),function(d){return [d.querySelector('select').value,parseFloat(d.querySelector('input').value)||0]})}
function guarda(){try{localStorage.setItem(K,JSON.stringify(lee()))}catch(e){}}
function aviso(h){var a=$('v-aviso');a.innerHTML=h;clearTimeout(tAviso);if(h)tAviso=setTimeout(function(){a.innerHTML='';deshacer=null},8000)}
function pinta(){var t={};M.forEach(function(m){t[m[0]]=0});
  [].forEach.call(filas.querySelectorAll('.vol-fila'),function(d,i){var e=E[d.querySelector('select').value];d.querySelector('.vol-i').textContent=String(i+1).padStart(2,'0');d.querySelector('.vol-musc').textContent=e?Object.keys(e[2]).map(function(m){return MN[m]+' ×'+fmt(e[2][m],e[2][m]%1?1:0)}).join(' · '):''});
  var tot=0;lee().forEach(function(r){var e=E[r[0]];tot+=r[1];if(!e)return;for(var m in e[2])t[m]+=e[2][m]*r[1]});
  var max=Math.max(20,Math.max.apply(null,M.map(function(m){return t[m[0]]}))),c=[0,0,0],h='<div class="vol-eje" aria-hidden="true"><span></span><span class="vol-pista-eje"><em style="left:'+(5/max*100)+'%">5</em><em style="left:'+(10/max*100)+'%">10</em></span><span></span></div>';
  function barra(k){var v=t[k],z=v>=10?2:(v>=5?1:0);if(v>0)c[z]++;
    return '<div class="vol-b z'+(v>0?z:'n')+'" data-m="'+k+'" tabindex="0"><span class="vol-n">'+MN[k]+'</span><span class="vol-pista"><i style="left:'+(5/max*100)+'%"></i><i style="left:'+(10/max*100)+'%"></i><b style="width:'+Math.min(100,v/max*100)+'%"></b></span><span class="vol-v">'+fmt(v,v%1?1:0)+'</span></div>'}
  if(porSeries)M.map(function(m){return m[0]}).sort(function(a,b){return t[b]-t[a]}).forEach(function(k){h+=barra(k)});
  else GR.forEach(function(g){h+='<p class="vol-grupo">'+g[0]+'</p>';g[1].forEach(function(k){h+=barra(k)})});
  $('v-barras').innerHTML=h;
  $('v-t2').textContent=c[2];$('v-t1').textContent=c[1];$('v-t0').textContent=c[0];$('v-tot').textContent=fmt(tot);
  var n=lee().length;$('v-vacio').hidden=n>0;$('v-copiar').hidden=!n;
  $('v-resumen').textContent=n?('Músculos con 10 o más series: '+c[2]+'. Entre 5 y 9: '+c[1]+'. Por debajo de 5: '+c[0]+'. Las series que trabajan un músculo de forma indirecta cuentan la mitad.'):'Añade los ejercicios de tu semana para ver el reparto.';
  copia='Series por músculo a la semana (FBE)\n'+M.map(function(m){return m[1]+': '+fmt(t[m[0]],t[m[0]]%1?1:0)}).join('\n');
  guarda()}
function marca(k){[].forEach.call(filas.querySelectorAll('.vol-fila'),function(d){var e=E[d.querySelector('select').value];d.classList.toggle('aporta',!!(k&&e&&e[2][k]))})}
$('v-barras').addEventListener('mouseover',function(e){var b=e.target.closest('.vol-b');marca(b?b.dataset.m:null)});
$('v-barras').addEventListener('mouseleave',function(){marca(null)});
$('v-barras').addEventListener('focusin',function(e){var b=e.target.closest('.vol-b');marca(b?b.dataset.m:null)});
$('v-barras').addEventListener('focusout',function(){marca(null)});
filas.addEventListener('input',pinta);filas.addEventListener('change',pinta);
filas.addEventListener('click',function(e){if(e.target.classList.contains('vol-quita')){var d=e.target.closest('.vol-fila');if(quieto){d.remove();pinta()}else{d.classList.add('sale');setTimeout(function(){d.remove();pinta()},180)}}});
$('v-mas').addEventListener('click',function(){var d=fila(null,null,true);d.querySelector('select').focus();pinta()});
$('v-rapidos').addEventListener('click',function(e){var b=e.target.closest('[data-e]');if(!b)return;fila(b.dataset.e,3,true);pinta()});
$('v-ejemplo').addEventListener('click',function(){filas.innerHTML='';[['sentadilla',9],['banca',9],['remo',9],['rumano',6],['militar',6],['jalon',6],['curl',6],['triceps',6],['gemelos',6],['plancha',6]].forEach(function(r){fila(r[0],r[1])});pinta();aviso('Ejemplo cargado: cuerpo completo, 3 días por semana.')});
$('v-vaciar').addEventListener('click',function(){var antes=lee();if(!antes.length)return;filas.innerHTML='';pinta();deshacer=antes;aviso('Semana vaciada. <button type="button" class="enl-b" id="v-deshacer">Deshacer</button>')});
$('v-aviso').addEventListener('click',function(e){if(e.target.id==='v-deshacer'&&deshacer){deshacer.forEach(function(r){fila(r[0],r[1])});deshacer=null;pinta();aviso('Recuperada.')}});
$('v-orden').addEventListener('click',function(){porSeries=!porSeries;this.setAttribute('aria-pressed',porSeries);this.textContent=porSeries?'Ordenar por zonas del cuerpo':'Ordenar por series';pinta()});
$('v-copiar').addEventListener('click',function(){copiar(this,copia)});
var g=null;try{g=JSON.parse(localStorage.getItem(K)||'null')}catch(e){}
if(Array.isArray(g)&&g.length)g.forEach(function(r){if(E[r[0]])fila(r[0],r[1])});else if(!Array.isArray(g)){fila('sentadilla',6);fila('banca',6);fila('remo',6)}
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
<div class="caf-rapidos" id="c-rapidos" role="group" aria-label="Añadir rápido"></div>
<div class="caf-filas" id="c-filas"></div>
<p class="vol-vacio" id="c-vacio" hidden>Todavía no hay tomas. Añade la primera con los botones de arriba.</p>
<div class="tool-fila"><div class="tool-campo caf-dormir"><label for="c-dormir">Me acuesto a las</label><input id="c-dormir" type="time" value="23:00"></div>
<div class="tool-campo"><span class="tool-et">Situación</span><label class="caf-check interruptor"><input type="checkbox" id="c-embarazo" role="switch"><span>Embarazo o lactancia</span></label></div></div>
<p class="tool-nota">Los miligramos son valores orientativos de la EFSA; cada marca y cada taza cambian. Si tu preentreno o tu bebida dice otra cantidad en la etiqueta, usa «Preentreno u otro» y escríbela.</p>'''
CAF_RES = f'''<p class="tool-et">Cafeína del día</p>
<div class="res-grande"><b id="c-r-total">0</b><span>mg</span></div>
<div class="medidor caf-med"><div class="medidor-pista"><b class="medidor-relleno" id="c-relleno"></b></div><div class="medidor-esc" id="c-esc" aria-hidden="true"></div><div class="medidor-ley"><span id="c-limite-t">Límite EFSA: 400 mg al día</span></div></div>
<div class="caf-curva-caja"><svg class="caf-curva" id="c-curva" viewBox="0 0 480 200" role="img" aria-label="Cafeína estimada en el cuerpo a lo largo del día"></svg><p class="caf-lectura" id="c-lectura" aria-live="off"></p></div>
<div class="caf-limites" id="c-limites"></div>
<p class="res-veredicto" id="c-r-tit"></p>
<ul class="res-lista" id="c-r-lista"></ul>
{copiar_b("c-copiar", "Copiar resumen")}'''
CAF_JS = r'''(function(){
var B=__BEB__,BB={};B.forEach(function(b){BB[b[0]]=b});
var $=function(i){return document.getElementById(i)},filas=$('c-filas'),K='fbe-cafeina',VM=5,copia='',ultQ=null;
var opts=B.map(function(b){return '<option value="'+b[0]+'">'+b[1]+'</option>'}).join('');
function corto(b){return BB[b]?BB[b][1].replace(/ \(.*$/,''):'Toma'}
$('c-rapidos').innerHTML=B.filter(function(b){return b[0]!=='choco-leche'}).map(function(b){return '<button type="button" class="chip-b" data-b="'+b[0]+'">+ '+corto(b[0])+' <b>'+(b[0]==='otro'?'mg':b[2])+'</b></button>'}).join('');
function mins(t){var p=(t||'').split(':');return p.length<2?NaN:parseInt(p[0],10)*60+parseInt(p[1],10)}
function hhmm(m){m=((Math.round(m)%1440)+1440)%1440;return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0')}
var nid=0;
function fila(b,h,mg,nueva){var id='c-t'+(nid++),d=document.createElement('div');d.className='caf-fila'+(nueva?' nueva':'');
  d.innerHTML='<label class="sr" for="'+id+'b">Bebida</label><select id="'+id+'b">'+opts+'</select><span class="caf-mgt"></span><input class="caf-mg" type="number" inputmode="numeric" min="0" max="1000" step="10" aria-label="Miligramos de cafeína" value="'+(mg||BB[b][2])+'"><label class="sr" for="'+id+'h">Hora</label><input id="'+id+'h" type="time" value="'+h+'"><button type="button" class="vol-quita" aria-label="Quitar">×</button>';
  d.querySelector('select').value=b;filas.appendChild(d);ajusta(d);return d}
function ajusta(d){var b=d.querySelector('select').value,mg=d.querySelector('.caf-mg'),t=d.querySelector('.caf-mgt');mg.hidden=b!=='otro';t.hidden=b==='otro';if(b!=='otro'){mg.value=BB[b][2];t.textContent=BB[b][2]+' mg'}}
function ordena(){var ds=[].slice.call(filas.querySelectorAll('.caf-fila'));ds.sort(function(a,b){return (mins(a.querySelector('input[type=time]').value)||0)-(mins(b.querySelector('input[type=time]').value)||0)});ds.forEach(function(d){filas.appendChild(d)})}
function lee(){return [].map.call(filas.querySelectorAll('.caf-fila'),function(d){var b=d.querySelector('select').value;return {b:b,mg:parseFloat(d.querySelector('.caf-mg').value)||0,h:d.querySelector('input[type=time]').value}})}
function guarda(){try{localStorage.setItem(K,JSON.stringify({t:lee(),d:$('c-dormir').value,e:$('c-embarazo').checked}))}catch(e){}}
function pinta(){
  var T=lee().filter(function(t){return !isNaN(mins(t.h))}).map(function(t){return {b:t.b,mg:t.mg,m:mins(t.h)}}).sort(function(a,b){return a.m-b.m});
  var tot=T.reduce(function(s,t){return s+t.mg},0),lim=$('c-embarazo').checked?200:400;
  $('c-r-total').textContent=fmt(tot);$('c-limite-t').textContent='Límite EFSA: '+lim+' mg al día'+(lim===200?' en embarazo o lactancia':'');
  $('c-esc').innerHTML='<span style="left:0">0</span><span style="left:50%">'+(lim/2)+'</span><span class="ult" style="left:100%">'+lim+'</span>';
  $('c-relleno').style.width=Math.min(100,tot/lim*100)+'%';$('c-relleno').className='medidor-relleno'+(tot>lim?' pasa':'');
  var res=document.querySelector('.tool-res');res.classList.remove('z-bajo','z-medio','z-alto');
  var dm=mins($('c-dormir').value),li=[];$('c-vacio').hidden=T.length>0;$('c-copiar').hidden=!T.length;
  if(isNaN(dm))dm=23*60;
  var lc=dm-8.8*60,lp=dm-13.2*60;
  $('c-limites').innerHTML='<span class="chip-l"><b>'+hhmm(lc)+'</b>último café de unos 107 mg</span><span class="chip-l"><b>'+hhmm(lp)+'</b>último preentreno de unos 217 mg</span>';
  if(!T.length){$('c-r-tit').textContent='Añade tus cafés, tés o refrescos con su hora.';$('c-r-lista').innerHTML='';$('c-curva').innerHTML='';$('c-lectura').textContent='';ultQ=null;guarda();return}
  var ult=T[T.length-1].m;if(dm<=ult)dm+=1440;
  var q=function(x){return T.reduce(function(s,t){return x>=t.m?s+t.mg*Math.pow(.5,(x-t.m)/60/VM):s},0)};ultQ=q;
  var cama=q(dm),may=Math.max.apply(null,T.map(function(t){return t.mg})),hora=false;
  li.push([tot>lim?'mal':'ok',tot>lim?'Pasas el límite de la EFSA ('+lim+' mg al día) en '+fmt(tot-lim)+' mg.':'Estás dentro del límite de la EFSA ('+lim+' mg al día).']);
  if(may>200)li.push(['at','Tu toma más grande tiene '+fmt(may)+' mg; la EFSA considera seguras tomas de hasta 200 mg de una vez.']);
  li.push([cama>=100?'mal':'ok','Al acostarte te quedarían unos '+fmt(cama)+' mg en el cuerpo (cálculo aproximado: el cuerpo elimina la mitad cada '+VM+' horas de media, aunque en cada persona va de 1,5 a 9,5).']);
  T.forEach(function(t){var hs=(dm-t.m)/60,n=corto(t.b);
    if(t.mg>=150&&hs<13.2){hora=true;li.push(['at',n+' de las '+hhmm(t.m)+' ('+fmt(t.mg)+' mg): queda a '+fmt(hs,1)+' h de dormir. Para un preentreno de unos 217 mg, Gardiner y cols. proponen tomarlo al menos 13,2 h antes.'])}
    else if(t.mg>=60&&t.mg<150&&hs<8.8){hora=true;li.push(['at',n+' de las '+hhmm(t.m)+': queda a '+fmt(hs,1)+' h de dormir. Para un café de unos 107 mg, Gardiner y cols. proponen al menos 8,8 h antes de acostarse.'])}});
  var dosis=may>200;
  res.classList.add(cama>=100||tot>lim?'z-bajo':(hora||dosis?'z-medio':'z-alto'));
  $('c-r-tit').textContent=cama>=100?'Te acuestas con 100 mg o más: puede costarte dormir':(tot>lim?'Te pasas del límite diario':(hora?'Revisa la hora de algún café':(dosis?'Alguna toma pasa de 200 mg':'Buena pinta para tu sueño')));
  $('c-r-lista').innerHTML=li.map(function(x){return '<li class="'+x[0]+'">'+x[1]+'</li>'}).join('');
  copia='Cafeína del día: '+fmt(tot)+' mg (límite EFSA '+lim+' mg). Al acostarme ('+hhmm(dm)+'): unos '+fmt(cama)+' mg.\n'+T.map(function(t){return hhmm(t.m)+' · '+corto(t.b)+' · '+fmt(t.mg)+' mg'}).join('\n');
  // curva
  var x0=T[0].m-60,x1=dm+120,ymax=Math.max(150,Math.max.apply(null,T.map(function(t){return q(t.m)}))*1.15),W=480,H=200,L=36,R=10,Tp=14,Bt=26;
  var X=function(m){return L+(m-x0)/(x1-x0)*(W-L-R)},Y=function(v){return Tp+(1-v/ymax)*(H-Tp-Bt)};
  var p='';for(var m=x0;m<=x1;m+=5){p+=(m===x0?'M':'L')+X(m).toFixed(1)+' '+Y(q(m)).toFixed(1)}
  var a=p+'L'+X(x1).toFixed(1)+' '+Y(0)+'L'+X(x0).toFixed(1)+' '+Y(0)+'Z',ej='';
  for(var hh=Math.ceil(x0/120)*120;hh<=x1;hh+=120)ej+='<line class="g" x1="'+X(hh)+'" x2="'+X(hh)+'" y1="'+Tp+'" y2="'+Y(0)+'"/><text class="t" x="'+X(hh)+'" y="'+(H-8)+'" text-anchor="middle">'+hhmm(hh).slice(0,2)+'h</text>';
  var tomas=T.map(function(t){return '<circle class="toma" cx="'+X(t.m)+'" cy="'+Y(q(t.m))+'" r="3.5"/><text class="t tm" x="'+X(t.m)+'" y="'+(Y(q(t.m))-8)+'" text-anchor="middle">'+fmt(t.mg)+'</text>'}).join('');
  $('c-curva').innerHTML='<defs><linearGradient id="c-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="c1"/><stop offset="1" class="c2"/></linearGradient></defs><rect class="noche" x="'+X(dm)+'" y="'+Tp+'" width="'+(W-R-X(dm))+'" height="'+(Y(0)-Tp)+'"/>'+ej+'<line class="cien" x1="'+L+'" x2="'+(W-R)+'" y1="'+Y(100)+'" y2="'+Y(100)+'"/><text class="t" x="'+(L-4)+'" y="'+(Y(100)+4)+'" text-anchor="end">100</text><path class="area" d="'+a+'"/><path class="linea" d="'+p+'"/>'+tomas+'<line class="cama" x1="'+X(dm)+'" x2="'+X(dm)+'" y1="'+Tp+'" y2="'+Y(0)+'"/><circle class="punto" cx="'+X(dm)+'" cy="'+Y(cama)+'" r="5"/><text class="t cama-t" x="'+(X(dm)-6)+'" y="'+(Tp+12)+'" text-anchor="end">a dormir</text><g class="scrub" id="c-scrub" style="display:none"><line class="sl" y1="'+Tp+'" y2="'+Y(0)+'"/><circle class="sp" r="4"/></g>';
  $('c-curva').dataset.x0=x0;$('c-curva').dataset.x1=x1;$('c-curva').dataset.ymax=ymax;
  $('c-lectura').textContent='Pasa el dedo o el ratón por la curva para ver la cafeína a cada hora.';
  guarda()}
var cv=$('c-curva');
function lectura(e){if(!ultQ)return;var r=cv.getBoundingClientRect(),W=480,L=36,R=10,Tp=14,H=200,Bt=26,vx=(e.clientX-r.left)/r.width*W;if(vx<L||vx>W-R)return;
  var x0=+cv.dataset.x0,x1=+cv.dataset.x1,ym=+cv.dataset.ymax,m=x0+(vx-L)/(W-L-R)*(x1-x0),v=ultQ(m),y=Tp+(1-v/ym)*(H-Tp-Bt),s=$('c-scrub');
  if(!s)return;s.style.display='';s.querySelector('.sl').setAttribute('x1',vx);s.querySelector('.sl').setAttribute('x2',vx);s.querySelector('.sp').setAttribute('cx',vx);s.querySelector('.sp').setAttribute('cy',y);
  $('c-lectura').textContent='A las '+hhmm(m)+': unos '+fmt(v)+' mg en el cuerpo.'}
cv.addEventListener('pointermove',lectura);cv.addEventListener('pointerdown',lectura);
cv.addEventListener('pointerleave',function(){var s=$('c-scrub');if(s)s.style.display='none'});
filas.addEventListener('change',function(e){if(e.target.tagName==='SELECT')ajusta(e.target.closest('.caf-fila'));if(e.target.type==='time')ordena();pinta()});
filas.addEventListener('input',pinta);
filas.addEventListener('click',function(e){if(e.target.classList.contains('vol-quita')){e.target.closest('.caf-fila').remove();pinta()}});
$('c-rapidos').addEventListener('click',function(e){var b=e.target.closest('[data-b]');if(!b)return;var T=lee().map(function(t){return mins(t.h)}).filter(function(m){return !isNaN(m)}),h=T.length?Math.min(Math.max.apply(null,T)+120,22*60):8*60;fila(b.dataset.b,hhmm(h),null,true);ordena();pinta()});
$('c-dormir').addEventListener('input',pinta);$('c-embarazo').addEventListener('change',pinta);
$('c-copiar').addEventListener('click',function(){copiar(this,copia)});
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
REV_FORM = ('<div class="rev-pasos" id="q-pasos" aria-hidden="true"><span>1</span><i></i><span>2</span><i></i><span>3</span></div>'
    + seg('q-regular', '1. ¿Haces ejercicio con regularidad? Al menos 30 minutos de intensidad moderada, 3 días por semana, en los últimos 3 meses.', [('si', 'Sí'), ('no', 'No')], clase='rev-q')
    + '<details class="rev-det"><summary>¿Qué es intensidad moderada?</summary><p>La que te deja hablar, pero no cantar: caminar a paso rápido, ir en bici sin prisa o nadar tranquilo.</p></details>'
    + seg('q-enf', '2. ¿Te han diagnosticado una enfermedad del corazón o de las arterias, diabetes o una enfermedad del riñón?', [('si', 'Sí'), ('no', 'No')], clase='rev-q')
    + '<fieldset class="tool-campo rev-sint rev-q"><legend>3. ¿Notas alguno de estos síntomas? <b class="rev-n" id="q-n" hidden></b></legend>'
    + ''.join(f'<label class="caf-check"><input type="checkbox" name="q-sint" value="{i}"><span>{t}</span></label>' for i, t in REV_SINT)
    + '<label class="caf-check ninguno"><input type="checkbox" id="q-ninguno"><span>Ninguno de estos</span></label></fieldset>'
    + '<div class="vol-bots rev-bots"><button type="button" class="ver-res" id="q-ver" hidden>Ver el resultado ↓</button><button type="button" class="enl-b" id="q-reset">Empezar de nuevo</button></div>'
    + '<p class="tool-aviso rev-112">Si tienes dolor en el pecho en reposo, que no cede, o con sudor frío o falta de aire, no esperes: llama al 112. <a class="tel-112" href="tel:112">Llamar al 112</a></p>')
REV_RES = f'''<div class="rev-icono" aria-hidden="true"></div>
<p class="tool-et">Resultado</p>
<p class="res-veredicto grande-t" id="q-r-tit">Responde a las tres preguntas.</p>
<p class="res-texto" id="q-r-txt">Son las del algoritmo de cribado del ACSM (2015). No es un examen ni bloquea nada: solo orienta.</p>
<div class="rev-camino" id="q-camino"></div>
<p class="tool-et rev-que" id="q-que" hidden>Qué hacer ahora</p>
<ul class="res-lista" id="q-r-lista"></ul>
<div class="rev-int" id="q-int" hidden><p class="tool-et">Cómo saber la intensidad</p><div><b>Ligera</b><span>Puedes hablar y hasta cantar</span></div><div><b>Moderada</b><span>Puedes hablar, pero no cantar</span></div><div><b>Vigorosa</b><span>Solo puedes decir frases cortas</span></div></div>
{copiar_b("q-copiar", "Copiar para mi médico")}'''
REV_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='';
var T={empezar:['z-alto','Puedes empezar','No hace falta una valoración médica previa. Empieza a intensidad ligera o moderada y súbela poco a poco.',['Ligera o moderada: puedes hablar mientras lo haces, aunque no cantar.','Sube la intensidad o el tiempo poco a poco, semana a semana.','Si aparece alguno de los síntomas de la lista, para y consulta.']],
continuar:['z-alto','Puedes seguir como hasta ahora','Puedes continuar con ejercicio moderado o vigoroso y progresar como venías haciendo.',['Si aparece alguno de los síntomas de la lista, para y consulta.']],
valoracion_vigoroso:['z-medio','Sigue, pero consulta antes de apretar más','Puedes seguir con ejercicio moderado; antes de pasar a intensidad vigorosa conviene una valoración médica.',['Moderado: puedes hablar, aunque no cantar. Vigoroso: solo puedes decir frases cortas.','Comenta con tu médico que quieres subir la intensidad.']],
valoracion_antes:['z-medio','Mejor una valoración médica antes de empezar','Conviene que te valore tu médico antes de empezar a entrenar; mientras tanto, actividad ligera, como caminar a paso cómodo.',['Lleva a la consulta tu lista de medicación y qué tipo de ejercicio quieres hacer.','Tras la valoración, empieza suave y progresa poco a poco.']],
valoracion_sint:['z-bajo','Con estos síntomas, consulta antes de empezar','Esos síntomas hay que valorarlos antes de empezar a entrenar. Pide cita con tu médico y cuéntaselos.',['Mientras tanto, nada de ejercicio intenso.','Tras la valoración, empieza suave y progresa poco a poco.']],
parar:['z-bajo','Para y consulta antes de seguir','Tienes síntomas que hay que valorar: deja el ejercicio moderado o intenso y consulta con tu médico antes de retomarlo.',['Cuéntale cuándo aparecen los síntomas y con qué esfuerzo.','Vuelve a entrenar cuando te lo indique.']]};
function radio(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
var nin=$('q-ninguno'),sint=[].slice.call(document.querySelectorAll('input[name="q-sint"]')),fs=[].slice.call(document.querySelectorAll('.rev-q'));
sint.forEach(function(c){c.addEventListener('change',function(){if(c.checked)nin.checked=false})});
nin.addEventListener('change',function(){if(nin.checked)sint.forEach(function(c){c.checked=false})});
function pinta(){var reg=radio('q-regular'),enf=radio('q-enf'),s=sint.filter(function(c){return c.checked}),res=document.querySelector('.tool-res'),hechas=[!!reg,!!enf,s.length>0||nin.checked];
  fs.forEach(function(f,i){f.classList.toggle('hecha',hechas[i])});
  [].forEach.call($('q-pasos').querySelectorAll('span'),function(x,i){x.classList.toggle('on',hechas[i])});
  $('q-n').hidden=!s.length;$('q-n').textContent=s.length===1?'1 marcado':s.length+' marcados';
  res.classList.remove('z-bajo','z-medio','z-alto');
  var listo=hechas.every(Boolean);$('q-ver').hidden=!listo;$('q-copiar').hidden=!listo;$('q-que').hidden=!listo;
  if(!listo){$('q-r-tit').textContent='Responde a las tres preguntas.';$('q-r-txt').textContent='Son las del algoritmo de cribado del ACSM (2015). No es un examen ni bloquea nada: solo orienta.';$('q-r-lista').innerHTML='';$('q-camino').innerHTML='';$('q-int').hidden=true;return}
  var k=s.length?(reg==='si'?'parar':'valoracion_sint'):(reg==='no'?(enf==='si'?'valoracion_antes':'empezar'):(enf==='si'?'valoracion_vigoroso':'continuar'));
  var t=T[k],extra=enf==='si'?['Si tomas medicación, mira también qué tener en cuenta al entrenar en <a href="pauta-activa.html">Pauta Activa</a>.']:[];
  res.classList.add(t[0]);$('q-r-tit').textContent=t[1];$('q-r-txt').textContent=t[2];$('q-r-lista').innerHTML=t[3].concat(extra).map(function(x){return '<li>'+x+'</li>'}).join('');
  var si=function(v){return v==='si'?'sí':'no'},sl=s.length?s.length+(s.length===1?' síntoma':' síntomas'):'ninguno';
  $('q-camino').innerHTML='<span>Ejercicio regular: <b>'+si(reg)+'</b></span><i>→</i><span>Enfermedad: <b>'+si(enf)+'</b></span><i>→</i><span>Síntomas: <b>'+sl+'</b></span>';
  $('q-int').hidden=!(k==='empezar'||k==='continuar'||k==='valoracion_vigoroso');
  copia='Cribado antes de entrenar (algoritmo ACSM 2015, Riebe y cols.)\nEjercicio regular: '+si(reg)+'. Enfermedad cardiovascular, metabólica o renal diagnosticada: '+si(enf)+'. Síntomas: '+(s.length?s.map(function(c){return c.parentNode.textContent.trim()}).join('; '):'ninguno')+'.\nResultado: '+t[1]+'. '+t[2]}
document.querySelector('.tool-form').addEventListener('change',pinta);
$('q-reset').addEventListener('click',function(){[].forEach.call(document.querySelectorAll('.tool-form input'),function(i){i.checked=false});pinta();document.querySelector('.tool-form').scrollIntoView({block:'start'})});
$('q-ver').addEventListener('click',function(){document.querySelector('.tool-res').scrollIntoView({block:'start'})});
$('q-copiar').addEventListener('click',function(){copiar(this,copia)});
pinta();
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
