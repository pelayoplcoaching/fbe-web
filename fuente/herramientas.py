# ===== herramientas: diez calculadoras (21/11/2026; segunda tanda de cinco el mismo día) =====
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
# ---------------------------------------------------------------------------------------------
# Segunda tanda de herramientas (21/11/2026): zonas de pulso, semáforo del dolor, SPPB, parón y suplementos.
# Fuentes al pie de cada página; no cambiar números sin cambiar la fuente.
I.update({
    'pulso': '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
    'semaforo': '<rect x="8" y="2.5" width="8" height="19" rx="3"/><circle cx="12" cy="7" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="17" r="1.5"/>',
    'andar': '<circle cx="13" cy="4.5" r="1.8"/><path d="M12 8.5l-2.5 5 3 2.5v5M12 8.5l3.5 1.5 2 3M9.5 13.5 7 20"/>',
    'pausa': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4M10 13.5v4M14 13.5v4"/>',
    'capsula': '<path d="M10.5 3.5a5 5 0 0 1 7 7l-7 7a5 5 0 0 1-7-7z"/><path d="M7 7l7 7"/>',
})

def rango(id_, etiqueta, val=0):
    return (f'<div class="tool-campo rango-t"><label for="{id_}">{etiqueta}</label><div class="rango-fila">'
            f'<input type="range" id="{id_}" min="0" max="10" step="1" value="{val}"><output id="{id_}-v" for="{id_}">{val}</output></div>'
            '<div class="rango-esc" aria-hidden="true"><span>0 · nada</span><span>5</span><span>10 · el peor</span></div></div>')

def crono_b(dest, que=''):
    return f'<button type="button" class="cronom" data-dest="{dest}" data-t="Cronometrar{(" " + que) if que else ""}"><i aria-hidden="true"></i><span>Cronometrar{(" " + que) if que else ""}</span></button>'

# ---------------------------------------------------------------------------------------------
# 6. Zonas de pulso (Tanaka 2001; tramos de Garber y cols. 2011, ACSM; fármacos que invalidan el pulso, de Pauta Activa / ACSM GETP 11.ª ed.)
PUL_FARM = 'Betabloqueantes (bisoprolol, atenolol, carvedilol, nebivolol, metoprolol, propranolol), verapamilo o diltiazem, digoxina, amiodarona, ivabradina, flecainida o propafenona, sotalol o dronedarona, metilfenidato, lisdexanfetamina, atomoxetina o modafinilo, y clozapina.'
PUL_FORM = f'''<div class="tool-fila">{campo_num("z-edad", "Edad", 45, 18, 95, 1, ud="años")}{campo_num("z-rep", "Pulso en reposo (opcional)", "", 35, 110, 1, "Por la mañana, sentado y tranquilo: cuenta las pulsaciones de un minuto.", ud="lpm")}</div>
{campo_num("z-max", "Pulso máximo medido (opcional)", "", 100, 220, 1, "Solo si te lo midieron en una prueba de esfuerzo. Si no, se estima con la edad.", ud="lpm")}
<label class="caf-check interruptor"><input type="checkbox" id="z-bb" role="switch"><span>Tomo un fármaco que cambia el pulso, o tengo fibrilación auricular o marcapasos</span></label>
<details class="rev-det"><summary>¿Qué fármacos cambian el pulso?</summary><p>{PUL_FARM} Si tomas medicación, <a href="pauta-activa.html">Pauta Activa</a> te lo dice fármaco a fármaco.</p></details>'''
PUL_RES = f'''<p class="tool-et" id="z-et">Tu pulso máximo estimado</p>
<div class="res-grande"><b id="z-max-n">–</b><span id="z-ud">lpm</span></div>
<p class="res-chip" id="z-metodo" hidden></p>
<p class="z-formulas" id="z-form" hidden></p>
<div class="zonas-barra" id="z-barra" aria-hidden="true"></div>
<div class="zonas-lista" id="z-lista"></div>
<div class="z-borg" aria-hidden="true"><p class="tool-et">Escala de Borg (6-20)</p><div>{''.join(f'<i class="zb-{("lig" if 9 <= n <= 11 else "mod" if n <= 13 else "vig" if n <= 17 else "max") if n >= 9 else "suave"}">{n}</i>' for n in range(6, 21))}</div><p><span>Muy suave</span><span>Máximo</span></p></div>
<p class="res-texto" id="z-txt"></p>
{copiar_b("z-copiar", "Copiar mis zonas")}'''
PUL_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='',ult='';
var Z=[['lig','Ligera',.30,.39,.57,.63,'9–11','Puedes hablar y hasta cantar',''],['mod','Moderada',.40,.59,.64,.76,'12–13','Puedes hablar, pero no cantar','≥150 min/semana'],['vig','Vigorosa',.60,.89,.77,.95,'14–17','Solo frases cortas','≥75 min/semana'],['max','Casi máxima',.90,1,.96,1,'18 o más','','']];
function pinta(){
  var e=parseFloat($('z-edad').value),r=parseFloat($('z-rep').value),mm=parseFloat($('z-max').value),bb=$('z-bb').checked,res=document.querySelector('.tool-res');
  res.classList.remove('z-alto','z-medio','z-bajo');
  if(!(e>=18&&e<=100)){$('z-max-n').textContent='–';$('z-metodo').hidden=true;$('z-barra').innerHTML='';$('z-lista').innerHTML='';$('z-txt').textContent='Escribe tu edad.';$('z-copiar').hidden=true;return}
  var est=Math.round(208-0.7*e),medido=mm>=100&&mm<=230,max=medido?Math.round(mm):est,hrr=!bb&&r>=35&&r<=max-30;
  var f=function(p){return Math.round(hrr?r+p*(max-r):p*max)};
  var filas=Z.map(function(z){return {z:z,lo:f(hrr?z[2]:z[4]),hi:z[0]==='max'?max:f(hrr?z[3]:z[5])}});
  var v=bb?'12–13':String(max);$('z-max-n').textContent=v;if(v!==ult){destella($('z-max-n'));ult=v}
  $('z-et').textContent=bb?'Tu objetivo para intensidad moderada':'Tu pulso máximo estimado';$('z-ud').textContent=bb?'en la escala de Borg':'lpm';
  $('z-metodo').hidden=false;$('z-metodo').textContent=bb?'Guíate por el esfuerzo, no por el pulso':(hrr?'Con tu pulso en reposo (método de Karvonen)':'Porcentaje del pulso máximo')+(medido?' · máximo medido':' · máximo estimado (Tanaka)');
  var b0=filas[0].lo,span=Math.max(1,max-b0);
  $('z-barra').innerHTML=bb?'':filas.map(function(x,i){var nx=i<filas.length-1?filas[i+1].lo:max;return '<span class="zb-'+x.z[0]+'" style="width:'+((nx-x.lo)/span*100).toFixed(2)+'%"><b>'+x.lo+'</b></span>'}).join('')+'<em>'+max+'</em>';
  $('z-form').hidden=bb;$('z-form').innerHTML='<span><small>Tanaka</small>'+est+'</span><span><small>220 − edad</small>'+(220-Math.round(e))+'</span>'+(medido?'<span class="on"><small>Medido</small>'+max+'</span>':'');
  $('z-lista').innerHTML=filas.map(function(x,i){return '<div class="zl zl-'+x.z[0]+'" data-z="'+x.z[0]+'"><i></i><b>'+x.z[1]+(x.z[8]?'<span class="zl-salud" title="Mínimo recomendado para la salud (ACSM)">'+x.z[8]+'</span>':'')+'</b>'+(bb?'':'<span class="zl-lpm">'+x.lo+'–'+x.hi+' lpm</span>')+'<small>Borg '+x.z[6]+(x.z[7]?' · '+x.z[7]:'')+'</small><em class="zl-int" aria-hidden="true">'+'<u></u><u></u><u></u><u></u>'.replace(/<u><\/u>/g,function(m,o){return o/7<=i?'<u class="si"></u>':m})+'</em></div>'}).join('');
  document.querySelector('.z-borg').dataset.bb=bb?'1':'';
  if(bb){res.classList.add('z-medio');$('z-txt').textContent='Con estos fármacos, con fibrilación auricular o con marcapasos, el pulso sube menos de lo normal o de forma irregular: no te fíes de las zonas de pulso del reloj. Guíate por el esfuerzo que notas (escala de Borg, de 6 a 20) y por la prueba del habla: para intensidad moderada, poder hablar pero no cantar.'}
  else{res.classList.add('z-alto');$('z-txt').textContent=(medido?'Usamos el máximo que te midieron. ':'Con la fórmula clásica (220 − edad) saldría '+(220-Math.round(e))+' lpm. Cualquier fórmula tiene un error típico de unos 10 latidos. ')+(hrr?'':'Si apuntas tu pulso en reposo, las zonas se ajustan mejor a tu forma física.')}
  $('z-copiar').hidden=false;
  copia='Mis zonas de esfuerzo (FBE)\n'+(bb?'El pulso no me sirve de guía: esfuerzo percibido y prueba del habla.\n':'Pulso máximo: '+max+' lpm ('+(medido?'medido':'estimado con Tanaka')+')'+(hrr?' · reposo '+r+' lpm':'')+'\n')+filas.map(function(x){return x.z[1]+': '+(bb?'':x.lo+'–'+x.hi+' lpm · ')+'Borg '+x.z[6]+(x.z[7]?' ('+x.z[7].toLowerCase()+')':'')}).join('\n');
}
$('z-copiar').addEventListener('click',function(){copiar(this,copia)});
function enlaza(e){var r=e.target.closest&&e.target.closest('.zl'),k=r?r.dataset.z:'';document.querySelectorAll('#z-barra span').forEach(function(sp){sp.classList.toggle('on',!!k&&sp.classList.contains('zb-'+k))});document.querySelectorAll('.z-borg i').forEach(function(c){c.classList.toggle('on',!!k&&c.classList.contains('zb-'+k))})}
$('z-lista').addEventListener('mouseover',enlaza);$('z-lista').addEventListener('mouseleave',enlaza);
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('zonas-pulso.html', 'Zonas de pulso y esfuerzo',
    'Calcula tu pulso máximo con la fórmula de Tanaka y tus zonas de entrenamiento según el ACSM, con o sin pulso en reposo. Si tomas medicación que cambia el pulso, te dice cómo guiarte sin él.',
    'Tus zonas de pulso, bien calculadas',
    'Tu pulso máximo con la fórmula de Tanaka y tus zonas de entrenamiento con los tramos del Colegio Americano de Medicina del Deporte. Si tomas medicación que cambia el pulso, te digo cómo guiarte sin él.',
    PUL_FORM, PUL_RES,
    '''<p>El pulso máximo se estima con la fórmula de <b>Tanaka</b> (208 − 0,7 × edad), más ajustada que la clásica 220 − edad, aunque cualquier fórmula tiene un error típico de unos 10 latidos. Si te lo midieron en una prueba de esfuerzo, usa ese.</p>
<p>Si apuntas el <b>pulso en reposo</b>, las zonas se calculan sobre la reserva de pulso (la diferencia entre el máximo y el de reposo), el método de Karvonen, que se ajusta mejor a tu forma física. Si no, se usan porcentajes del máximo.</p>
<p>Los tramos son los del <b>Colegio Americano de Medicina del Deporte (ACSM)</b>: moderada, del 40 al 59 % de la reserva (64-76 % del máximo); vigorosa, del 60 al 89 % (77-95 % del máximo). Para la salud recomienda al menos 150 minutos a la semana de intensidad moderada o 75 de vigorosa.</p>
<p>Algunos fármacos, la fibrilación auricular y el marcapasos hacen que el pulso no sirva para medir la intensidad. Entonces manda el <b>esfuerzo percibido</b> (escala de Borg, de 6 a 20) y la <b>prueba del habla</b>.</p>''',
    ['Tanaka H, Monahan KD, Seals DR. Age-predicted maximal heart rate revisited. J Am Coll Cardiol. 2001;37(1):153-6.',
     'Garber CE y cols. Quantity and quality of exercise for developing and maintaining cardiorespiratory, musculoskeletal, and neuromotor fitness in apparently healthy adults (Position Stand del ACSM). Med Sci Sports Exerc. 2011;43(7):1334-59 (tramos de intensidad y 150/75 minutos).',
     'American College of Sports Medicine. ACSM\'s Guidelines for Exercise Testing and Prescription. 11.ª ed. 2021 (fármacos que alteran el pulso; es la misma fuente que usa Pauta Activa).'],
    PUL_JS, slug='pulso', tira=('Calcula tu máximo', 'Ajusta con el pulso en reposo', 'Si el pulso no sirve, el esfuerzo'))

# ---------------------------------------------------------------------------------------------
# 7. Semáforo del dolor (modelo de control del dolor de Thomeé 1997 y Silbernagel 2007; Silbernagel 2020)
DOL_FLAGS = [('noche', 'Dolor que te despierta por la noche o que no cede en reposo'), ('hinchazon', 'Hinchazón, calor o enrojecimiento en la zona'), ('golpe', 'Empezó con un golpe, una caída o un chasquido'), ('nervio', 'Hormigueo, adormecimiento o pérdida de fuerza'), ('pecho', 'Dolor en el pecho, falta de aire o mareo con el esfuerzo')]
DOL_FORM = (f'<div class="tool-campo"><label for="d-zona">Zona (opcional)</label><input id="d-zona" type="text" maxlength="40" autocomplete="off" placeholder="Rodilla derecha, hombro, tendón de Aquiles…"></div>'
    + rango('d-dur', 'Dolor durante el ejercicio') + rango('d-des', 'Dolor al terminar o ese mismo día')
    + seg('d-man', 'A la mañana siguiente', [('igual', 'Como antes de entrenar'), ('peor', 'Más dolor o rigidez'), ('nose', 'Aún no lo sé')], 'nose')
    + seg('d-sem', 'Comparado con la semana pasada', [('igual', 'Igual o mejor'), ('peor', 'Peor'), ('nose', 'No lo sé')], 'nose')
    + '<fieldset class="tool-campo rev-sint d-banderas"><legend>Señales para consultar antes de seguir <em id="d-nflag" hidden></em></legend>'
    + ''.join(f'<label class="caf-check"><input type="checkbox" name="d-flag" value="{v}"><span>{t}</span></label>' for v, t in DOL_FLAGS)
    + '</fieldset><p class="tool-nota">Sirve para dolores por sobrecarga y tendones, no para golpes ni lesiones recientes. Lo que guardes en el diario se queda en este navegador.</p>')
DOL_RES = f'''<div class="semaforo" id="d-luces" data-k="v" aria-hidden="true"><i class="l-r"></i><i class="l-a"></i><i class="l-v"></i></div>
<p class="tool-et">Resultado</p>
<p class="res-veredicto grande-t" id="d-tit"></p>
<p class="res-texto" id="d-txt"></p>
<p class="tool-et rev-que">Qué hacer</p>
<ul class="res-lista" id="d-lista"></ul>
<div class="vol-bots"><button type="button" class="copiar-t guardar" id="d-guardar"><span>Guardar en mi diario</span></button>{copiar_b("d-copiar", "Copiar", False)}</div>
<div class="d-diario" id="d-diario" hidden><p class="tool-et">Tu diario</p><p class="d-resumen" id="d-resumen"></p><svg class="d-graf" id="d-graf" viewBox="0 0 300 86" role="img" aria-label="Dolor máximo de tus últimas anotaciones"></svg><ol class="d-entradas" id="d-entradas"></ol><button type="button" class="enl-b claro" id="d-borrar">Borrar el diario</button><p class="vol-aviso" id="d-aviso" role="status"></p></div>'''
DOL_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},K='fbe-dolor',copia='',estado='v',deshacer=null;
function val(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:'nose'}
function out(id){var i=$(id),o=$(id+'-v');o.textContent=i.value;o.dataset.z=+i.value>5?'r':'v';i.style.setProperty('--p',(i.value*10)+'%')}
function pinta(){
  out('d-dur');out('d-des');
  var du=+$('d-dur').value,de=+$('d-des').value,m=val('d-man'),s=val('d-sem'),fl=[].map.call(document.querySelectorAll('input[name="d-flag"]:checked'),function(c){return c.value}),res=document.querySelector('.tool-res'),k,tit,txt,li;
  if(fl.indexOf('pecho')>=0){k='r';tit='Para y consulta: no parece un dolor muscular';txt='El dolor en el pecho, la falta de aire o el mareo con el esfuerzo hay que valorarlos antes de seguir entrenando.';li=['Si aparece en reposo, no cede o va con sudor frío, llama al 112.','Si no, pide cita con tu médico antes de volver a entrenar.']}
  else if(fl.length){k='r';tit='Consulta antes de seguir';txt='Esa señal no entra en este semáforo: conviene que te valore un médico o un fisioterapeuta antes de seguir cargando la zona.';li=['Mientras tanto, entrena lo que no moleste.']}
  else if(du>5||de>5){k='r';tit='Te has pasado del límite';txt='El modelo admite hasta 5 sobre 10 durante y después del ejercicio, y has llegado a '+Math.max(du,de)+'.';li=['La próxima sesión, baja la carga: menos peso, menos series o menos recorrido, o cambia a una variante que moleste menos.','Parar del todo no suele ser la solución: en las tendinopatías, el reposo completo puede ser contraproducente.','Si sigue sin mejorar, consúltalo con un fisioterapeuta o con tu médico.']}
  else if(m==='peor'||s==='peor'){k='a';tit='Dentro del límite, pero tu cuerpo avisa';txt=(m==='peor'?'A la mañana siguiente, el dolor y la rigidez deberían estar como antes de entrenar. ':'')+(s==='peor'?'Y no deberían ir a más de una semana a otra.':'');li=['Mantén la carga sin subirla, o bájala un poco, hasta que a la mañana siguiente estés como antes de entrenar.','Vuelve a mirarlo después de la próxima sesión.']}
  else if(du===0&&de===0){k='v';tit='Sin dolor: entrena con normalidad';txt='Ni durante ni después. Sigue progresando como tenías previsto.';li=['Si aparece dolor, vuelve y apúntalo.']}
  else if(m==='nose'){k='v';tit='Por ahora, dentro del límite';txt='Hasta 5 sobre 10 durante y después está dentro del modelo. Falta un dato: a la mañana siguiente debería estar como antes de entrenar.';li=['Mañana, vuelve y marca cómo te has levantado.','Mientras, puedes mantener la carga.']}
  else{k='v';tit='Puedes seguir';txt='Dentro del modelo de control del dolor: no pasa de 5 sobre 10, se va a la mañana siguiente y no empeora de una semana a otra.';li=['Mantén la carga y, si se repite así, súbela poco a poco.','Sigue apuntándolo para ver la tendencia.']}
  var nf=$('d-nflag');nf.hidden=!fl.length;nf.textContent=fl.length+(fl.length===1?' marcada':' marcadas');
  ['d-dur','d-des'].forEach(function(id){$(id).closest('.rango-t').classList.toggle('pasa',+$(id).value>5)});
  document.querySelectorAll('input[name="d-flag"]').forEach(function(c){c.closest('label').classList.toggle('marcada',c.checked)});
  if(estado!==k){var lz=$('d-luces');lz.classList.remove('cambia');void lz.offsetWidth;lz.classList.add('cambia')}
  estado=k;res.classList.remove('z-alto','z-medio','z-bajo');res.classList.add(k==='v'?'z-alto':k==='a'?'z-medio':'z-bajo');$('d-luces').dataset.k=k;
  $('d-tit').textContent=tit;$('d-txt').textContent=txt;$('d-lista').innerHTML=li.map(function(x){return '<li>'+x+'</li>'}).join('');
  var z=$('d-zona').value.trim();
  copia='Semáforo del dolor (FBE)'+(z?' · '+z:'')+'\nDurante: '+du+'/10 · Después: '+de+'/10 · Mañana siguiente: '+{igual:'como antes',peor:'peor',nose:'sin dato'}[m]+' · Semana: '+{igual:'igual o mejor',peor:'peor',nose:'sin dato'}[s]+'\nResultado: '+tit;
}
function lee(){try{var a=JSON.parse(localStorage.getItem(K)||'[]');return Array.isArray(a)?a:[]}catch(e){return []}}
function escribe(a){try{if(a.length)localStorage.setItem(K,JSON.stringify(a));else localStorage.removeItem(K)}catch(e){}}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function diario(){var a=lee(),c=$('d-diario');c.hidden=!a.length&&!deshacer;$('d-graf').style.display=a.length?'':'none';$('d-borrar').hidden=!a.length;if(!a.length){$('d-entradas').innerHTML='';return}
  var u=a.slice(-12),W=300,H=86,L=18,B=8,X=function(i){return L+(u.length<2?(W-L-8)/2:i*(W-L-8)/(u.length-1))},Y=function(v){return 6+(1-v/10)*(H-6-B)};
  var p=u.map(function(e,i){return (i?'L':'M')+X(i).toFixed(1)+' '+Y(Math.max(e.d,e.s)).toFixed(1)}).join('');
  var ks={v:0,a:0,r:0};u.forEach(function(e){ks[e.k]=(ks[e.k]||0)+1});var mx=function(e){return Math.max(e.d,e.s)},tr=u.length>1?mx(u[u.length-1])-mx(u[u.length-2]):0;
  $('d-resumen').innerHTML='<span class="k-v"><b>'+ks.v+'</b> verde'+(ks.v===1?'':'s')+'</span><span class="k-a"><b>'+ks.a+'</b> ámbar</span><span class="k-r"><b>'+ks.r+'</b> roja'+(ks.r===1?'':'s')+'</span>'+(u.length>1?'<span class="d-tend '+(tr>0?'sube':tr<0?'baja':'igual')+'">'+(tr>0?'Más dolor que la vez anterior':tr<0?'Menos dolor que la vez anterior':'Igual que la vez anterior')+'</span>':'');
  var area=u.length>1?'<path class="area" d="'+p+'L'+X(u.length-1).toFixed(1)+' '+Y(0).toFixed(1)+'L'+X(0).toFixed(1)+' '+Y(0).toFixed(1)+'Z"/>':'';
  $('d-graf').innerHTML='<rect class="banda-v" x="'+L+'" y="'+Y(5)+'" width="'+(W-4-L)+'" height="'+(Y(0)-Y(5))+'"/><rect class="banda-r" x="'+L+'" y="'+Y(10)+'" width="'+(W-4-L)+'" height="'+(Y(5)-Y(10))+'"/>'+area+'<line class="cinco" x1="'+L+'" x2="'+(W-4)+'" y1="'+Y(5)+'" y2="'+Y(5)+'"/><text class="t" x="'+(L-5)+'" y="'+(Y(5)+3.5)+'" text-anchor="end">5</text>'+(u.length>1?'<path class="linea" d="'+p+'"/>':'')+u.map(function(e,i){return '<circle class="pt k-'+e.k+'" cx="'+X(i).toFixed(1)+'" cy="'+Y(Math.max(e.d,e.s)).toFixed(1)+'" r="4"/>'}).join('');
  $('d-entradas').innerHTML=a.slice(-6).reverse().map(function(e){var f=new Date(e.f);return '<li class="k-'+e.k+'"><i></i><b>'+f.toLocaleDateString('es-ES',{day:'numeric',month:'short'})+'</b><span>'+(e.z?esc(e.z)+' · ':'')+'durante '+e.d+' · después '+e.s+'</span></li>'}).join('')}
$('d-guardar').addEventListener('click',function(){var a=lee();a.push({f:new Date().toISOString(),z:$('d-zona').value.trim().slice(0,40),d:+$('d-dur').value,s:+$('d-des').value,m:val('d-man'),k:estado});escribe(a.slice(-60));deshacer=null;$('d-aviso').innerHTML='';diario();var b=this,sp=b.querySelector('span');b.classList.add('hecho');sp.textContent='Guardado';setTimeout(function(){b.classList.remove('hecho');sp.textContent='Guardar en mi diario'},1600)});
$('d-borrar').addEventListener('click',function(){deshacer=lee();escribe([]);$('d-aviso').innerHTML='Diario borrado. <button type="button" class="enl-b claro" id="d-deshacer">Deshacer</button>';diario()});
$('d-aviso').addEventListener('click',function(e){if(e.target.id==='d-deshacer'&&deshacer){escribe(deshacer);deshacer=null;$('d-aviso').innerHTML='';diario()}});
$('d-copiar').addEventListener('click',function(){copiar(this,copia)});
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();diario();
})();'''

tool_pagina('semaforo-dolor.html', 'Semáforo del dolor al entrenar',
    '¿Puedo entrenar con este dolor? Un semáforo basado en el modelo de control del dolor de Thomeé y Silbernagel: dolor durante, después y a la mañana siguiente, con diario para ver la tendencia.',
    '¿Puedo entrenar con este dolor?',
    'Un semáforo basado en el modelo de control del dolor que se usa en tendinopatías y dolores por sobrecarga: apuntas el dolor durante, después y a la mañana siguiente, y te dice si seguir, mantener o bajar la carga.',
    DOL_FORM, DOL_RES,
    '''<p>El semáforo sigue el <b>modelo de control del dolor</b> de Thomeé y Silbernagel: se puede seguir entrenando con dolor de hasta 5 sobre 10 durante y después del ejercicio, siempre que a la mañana siguiente se haya ido y que el dolor y la rigidez no vayan a más de una semana a otra.</p>
<p>En un ensayo con tendinopatía de Aquiles, seguir corriendo y saltando con este modelo no tuvo efectos negativos frente al reposo activo. Y en estos cuadros, el reposo completo puede ser contraproducente: el dolor guía cuánto cargar, no si parar.</p>
<p>No sirve para golpes, lesiones recientes ni dolores con señales de alarma. Si marcas alguna, consulta antes de seguir.</p>''',
    ['Silbernagel KG, Thomeé R, Eriksson BI, Karlsson J. Continued sports activity, using a pain-monitoring model, during rehabilitation in patients with Achilles tendinopathy: a randomized controlled study. Am J Sports Med. 2007;35(6):897-906.',
     'Thomeé R. A comprehensive treatment approach for patellofemoral pain syndrome in young women. Phys Ther. 1997;77(12):1690-703 (origen del modelo).',
     'Silbernagel KG, Hanlon S, Sprague A. Current clinical concepts: conservative management of Achilles tendinopathy. J Athl Train. 2020;55(5):438-47.'],
    DOL_JS, slug='dolor', tira=('Durante', 'Al terminar', 'A la mañana siguiente'))

# ---------------------------------------------------------------------------------------------
# 8. Test SPPB (Guralnik 1994 y 2000; EWGSOP2 2019; niveles Vivifrail 2017)
SPPB_FORM = (f'''<p class="tool-aviso">Hazlo con alguien al lado y una silla firme sin brazos apoyada en la pared. Si aparece mareo, dolor en el pecho o falta de aire, para. No es para quien no pueda estar de pie sin ayuda.</p>
<div class="sppb-paso"><p class="sppb-t"><b>1</b>Equilibrio <small>De pie, sin apoyarse, 10 segundos en cada postura</small></p>
<button type="button" class="cuenta10" id="p-c10"><i aria-hidden="true"></i><span>Contar 10 segundos</span></button>'''
    + seg('p-lado', 'Pies juntos, uno al lado del otro', [('10', 'Aguanta 10 s'), ('0', 'Menos de 10 s')], clase='sppb-q')
    + seg('p-semi', 'Semitándem: el talón de un pie junto al dedo gordo del otro', [('10', 'Aguanta 10 s'), ('0', 'Menos de 10 s')], clase='sppb-q')
    + seg('p-tan', 'Tándem: un pie justo delante del otro, talón con punta', [('2', '10 s'), ('1', 'De 3 a 9 s'), ('0', 'Menos de 3 s')], clase='sppb-q')
    + f'''</div>
<div class="sppb-paso"><p class="sppb-t"><b>2</b>Marcha de 4 metros <small>A su paso normal. Dos intentos; cuenta el más rápido</small></p>
<div class="tool-fila">{campo_num("p-m1", "Intento 1", "", 0.5, 120, 0.01, ud="s")}{campo_num("p-m2", "Intento 2", "", 0.5, 120, 0.01, ud="s")}</div>
<div class="crono-par">{crono_b("p-m1", "el 1")}{crono_b("p-m2", "el 2")}</div>
<label class="caf-check"><input type="checkbox" id="p-m-no"><span>No puede hacerlo</span></label></div>
<div class="sppb-paso"><p class="sppb-t"><b>3</b>Levantarse de la silla <small>Brazos cruzados sobre el pecho</small></p>'''
    + seg('p-s1', 'Primero, una vez: ¿se levanta sin usar los brazos?', [('si', 'Sí'), ('no', 'No, necesita los brazos')], clase='sppb-q')
    + f'''{campo_num("p-s5", "Tiempo para levantarse 5 veces, lo más rápido posible", "", 1, 120, 0.01, "Del «ya» hasta que queda de pie la quinta vez.", ud="s")}
<div class="crono-par">{crono_b("p-s5")}</div>
<label class="caf-check"><input type="checkbox" id="p-s-no"><span>No completa las 5 o tarda más de 60 segundos</span></label></div>
<div class="vol-bots rev-bots"><button type="button" class="ver-res" id="p-ver" hidden>Ver el resultado ↓</button><button type="button" class="enl-b" id="p-reset">Empezar de nuevo</button></div>''')
SPPB_RES = f'''<p class="tool-et">Puntuación SPPB</p>
<div class="res-grande"><b id="p-total">–</b><span>de 12</span></div>
<p class="res-chip" id="p-cat" hidden></p>
<div class="sppb-partes" id="p-partes"></div>
<p class="res-veredicto" id="p-tit">Haz las tres pruebas.</p>
<p class="res-texto" id="p-txt">Equilibrio, marcha y levantarse de la silla: cada una puntúa de 0 a 4.</p>
<p class="res-texto p-vel" id="p-vel"></p>
{copiar_b("p-copiar", "Copiar resultado")}'''
SPPB_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='',act=null,tm=0,t0=0,cd=0;
function v(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return x>0?x:null}
function grupo(n){return document.querySelector('input[name="'+n+'"]').closest('fieldset')}
function para(b,escribir){clearInterval(tm);if(escribir){var i=$(b.dataset.dest);i.value=((performance.now()-t0)/1000).toFixed(2);i.dispatchEvent(new Event('input',{bubbles:true}))}b.classList.remove('va');b.querySelector('span').textContent=b.dataset.t||'Cronometrar';act=null}
document.addEventListener('click',function(e){var b=e.target.closest('.cronom');if(!b)return;if(act===b){para(b,true);return}if(act)para(act,true);act=b;t0=performance.now();b.classList.add('va');tm=setInterval(function(){b.querySelector('span').textContent=fmt((performance.now()-t0)/1000,2)+' s · parar'},50)});
$('p-c10').addEventListener('click',function(){var b=this,s=b.querySelector('span'),f=performance.now()+10000;clearInterval(cd);b.classList.add('va');cd=setInterval(function(){var q=Math.ceil((f-performance.now())/1000);if(q<=0){clearInterval(cd);b.classList.remove('va');s.textContent='¡10 segundos! Contar otra vez';if(navigator.vibrate)navigator.vibrate(250);return}s.textContent=q+' s…'},100)});
function pinta(){
  var lado=v('p-lado'),semi=v('p-semi'),tan=v('p-tan'),res=document.querySelector('.tool-res');
  grupo('p-semi').disabled=lado!=='10';grupo('p-tan').disabled=lado!=='10'||semi!=='10';
  var eq=null;if(lado==='0')eq=0;else if(lado==='10'){if(semi==='0')eq=1;else if(semi==='10'&&tan!==null)eq=2+(+tan)}
  var mno=$('p-m-no').checked,ts=[num('p-m1'),num('p-m2')].filter(Boolean),mt=ts.length?Math.min.apply(null,ts):null,mp=null;
  if(mno)mp=0;else if(mt)mp=mt<4.82?4:mt<=6.2?3:mt<=8.7?2:1;
  var s1=v('p-s1'),sno=$('p-s-no').checked,s5=num('p-s5'),sp=null;
  $('p-s5').disabled=s1==='no';$('p-s-no').disabled=s1==='no';
  if(s1==='no')sp=0;else if(s1==='si'){if(sno)sp=0;else if(s5)sp=s5<=11.19?4:s5<=13.69?3:s5<=16.69?2:s5<=60?1:0}
  var P=[['Equilibrio',eq],['Marcha',mp],['Levantarse',sp]];
  $('p-partes').innerHTML=P.map(function(p){return '<div class="pp'+(p[1]===null?' falta':'')+'"><span>'+p[0]+'</span><i>'+[0,1,2,3].map(function(k){return '<b'+(p[1]!==null&&k<p[1]?' class="on"':'')+'></b>'}).join('')+'</i><em>'+(p[1]===null?'–':p[1]+'/4')+'</em></div>'}).join('');
  var hechas=P.filter(function(p){return p[1]!==null}).length,tot=(eq||0)+(mp||0)+(sp||0),listo=hechas===3;
  res.classList.remove('z-alto','z-medio','z-bajo');$('p-ver').hidden=!listo;$('p-copiar').hidden=!listo;
  $('p-total').textContent=hechas?tot:'–';$('p-vel').textContent=mt&&!mno?'Velocidad de marcha: '+fmt(4/mt,2)+' metros por segundo.':'';
  if(!listo){$('p-cat').hidden=!hechas;$('p-cat').textContent='Faltan '+(3-hechas)+(3-hechas===1?' prueba':' pruebas');$('p-tit').textContent=hechas?'Sigue con las pruebas que faltan.':'Haz las tres pruebas.';$('p-txt').textContent='Equilibrio, marcha y levantarse de la silla: cada una puntúa de 0 a 4.';return}
  var viv=tot<=3?'A':tot<=6?'B':tot<=9?'C':'D',cat,tit,txt;
  if(tot>=10){res.classList.add('z-alto');cat='Rendimiento alto (10-12)';tit='Rendimiento alto';txt='Buen equilibrio, buena marcha y buena fuerza de piernas. Lo que lo mantiene es seguir entrenando fuerza y equilibrio.'}
  else if(tot>=7){res.classList.add('z-medio');cat='Rendimiento intermedio (7-9)';tit='Rendimiento intermedio';txt='Hay margen de mejora, y el ejercicio de fuerza y equilibrio adaptado suele mejorarlo.'+(tot<=8?' Una puntuación de 8 o menos es la que el consenso europeo de sarcopenia considera bajo rendimiento físico: conviene comentarlo con el médico.':'')}
  else{res.classList.add('z-bajo');cat='Rendimiento bajo (0-6)';tit='Rendimiento bajo';txt='Conviene comentarlo con el médico y empezar con un programa de ejercicio adaptado, mejor supervisado.'}
  $('p-cat').hidden=false;$('p-cat').textContent=cat;$('p-tit').textContent=tit;
  $('p-txt').innerHTML=txt+' Nivel de los programas <a href="https://vivifrail.com/" rel="noopener">Vivifrail</a>: '+viv+'.';
  copia='SPPB (FBE): '+tot+'/12 · '+tit+'\nEquilibrio '+eq+'/4 · Marcha '+mp+'/4'+(mt&&!mno?' ('+fmt(mt,2)+' s)':'')+' · Levantarse '+sp+'/4'+(s5&&s1==='si'&&!sno?' ('+fmt(s5,2)+' s)':'')+'\nNivel Vivifrail: '+viv;
}
$('p-reset').addEventListener('click',function(){[].forEach.call(document.querySelectorAll('.tool-form input'),function(i){if(i.type==='radio'||i.type==='checkbox')i.checked=false;else i.value=''});if(act)para(act,false);pinta();document.querySelector('.tool-form').scrollIntoView({block:'start'})});
$('p-ver').addEventListener('click',function(){document.querySelector('.tool-res').scrollIntoView({block:'start'})});
$('p-copiar').addEventListener('click',function(){copiar(this,copia)});
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('test-sppb.html', 'Test SPPB: equilibrio, marcha y fuerza',
    'Test SPPB (Short Physical Performance Battery) con cronómetro: equilibrio, marcha de 4 metros y levantarse de la silla. Puntuación de 0 a 12, qué significa y nivel de los programas Vivifrail.',
    'La fuerza de tus padres, en 10 minutos',
    'El test SPPB que usamos los médicos para medir el equilibrio, la marcha y la fuerza de piernas en personas mayores. Hazlo con ellos: con cronómetro, puntuación de 0 a 12 y qué significa.',
    SPPB_FORM, SPPB_RES,
    '''<p>La <b>batería corta de rendimiento físico</b> (SPPB, de Guralnik y cols.) mide en unos 10 minutos tres cosas que predicen cómo se va a valer una persona mayor: el equilibrio, la velocidad al caminar y la fuerza de piernas. Cada prueba puntúa de 0 a 4 y el total va de 0 a 12.</p>
<p>Los tiempos de la marcha son los de la versión de 4 metros. Se suele leer así: de 10 a 12, rendimiento alto; de 7 a 9, intermedio; de 0 a 6, bajo. El consenso europeo de sarcopenia (EWGSOP2) considera bajo rendimiento físico una puntuación de 8 o menos.</p>
<p>Los programas de ejercicio <b>Vivifrail</b> usan el SPPB para elegir el nivel: A (0-3), B (4-6), C (7-9) y D (10-12).</p>
<p>No es un diagnóstico: orienta. Repetirlo cada pocos meses sirve para ver si el entrenamiento funciona. Si te interesa solo la fuerza de piernas, prueba también el <a href="test-silla.html">test de la silla en 30 segundos</a>.</p>''',
    ['Guralnik JM y cols. A short physical performance battery assessing lower extremity function: association with self-reported disability and prediction of mortality and nursing home admission. J Gerontol. 1994;49(2):M85-94.',
     'Guralnik JM y cols. Lower extremity function and subsequent disability: consistency across studies, predictive models, and value of gait speed alone compared with the short physical performance battery. J Gerontol A Biol Sci Med Sci. 2000;55(4):M221-31 (versión de 4 metros y categorías).',
     'Cruz-Jentoft AJ y cols. Sarcopenia: revised European consensus on definition and diagnosis (EWGSOP2). Age Ageing. 2019;48(1):16-31 (SPPB de 8 o menos).',
     'Izquierdo M (coord.). Vivifrail: programa multicomponente de ejercicio físico para la prevención de la fragilidad y el riesgo de caídas. 2017 (niveles A-D).'],
    SPPB_JS, slug='sppb', tira=('Equilibrio', 'Marcha de 4 metros', 'Levantarse 5 veces'))

# ---------------------------------------------------------------------------------------------
# 9. ¿Cuánto pierdo si paro? (Bosquet 2013; Spiering 2021; Mujika y Padilla 2000 y 2001; Ogasawara 2013)
PAR_FORM = (campo_num('o-sem', 'Semanas sin entrenar como siempre', 3, 1, 52, 1, 'Vacaciones, Navidad, una lesión, una época de mucho trabajo…', ud='sem.')
    + seg('o-edad', 'Edad', [('j', 'Menos de 65'), ('m', '65 o más')], 'j')
    + seg('o-tipo', 'Qué entrenas', [('f', 'Fuerza'), ('r', 'Resistencia (cardio)'), ('a', 'Las dos')], 'a')
    + seg('o-hago', 'Durante el parón podré hacer', [('0', 'Nada'), ('1', '1 sesión a la semana'), ('2', '2 sesiones a la semana')], '0'))
PAR_RES = f'''<p class="tool-et">Durante tu parón</p>
<p class="res-veredicto grande-t" id="o-tit"></p>
<div class="paron-linea" id="o-linea" aria-hidden="true"></div>
<div class="paron-items" id="o-items"></div>
<div class="paron-plan"><p class="tool-et rev-que">Tu plan mínimo</p><ul class="res-lista" id="o-plan"></ul></div>
<p class="res-texto" id="o-vuelta">Al volver, lo que se pierde se recupera antes de lo que costó ganarlo: con parones de 3 semanas cada 6 de entrenamiento, en 6 meses se ganó lo mismo que entrenando sin parar.</p>
{copiar_b("o-copiar", "Copiar mi plan", False)}'''
PAR_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='';
function v(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
var ORD={ok:0,at:1,baja:2},ETQ={ok:'Se mantiene',at:'Puede quedarse corto',baja:'Baja'};
function pinta(){
  var w=Math.round(parseFloat($('o-sem').value)),ed=v('o-edad'),ti=v('o-tipo'),h=+v('o-hago'),res=document.querySelector('.tool-res'),items=[],filas=[];
  if(!(w>=1)){$('o-tit').textContent='Escribe cuántas semanas vas a parar.';return}
  var W=Math.min(52,Math.max(16,Math.ceil((w+3)/4)*4));
  if(ti!=='r'){var e,t,d,seg;
    if(h===0){if(w<=4){e='ok';t='Fuerza: apenas cambia';d='Hasta unas 4 semanas sin entrenar, la fuerza máxima casi no cambia (metaanálisis de 103 estudios).'}else{e='baja';t='Fuerza: empieza a bajar';d='Pasadas unas 4 semanas, la fuerza baja, y más cuanto más dura el parón.'+(ed==='m'?' A partir de los 65 se pierde bastante más: en el metaanálisis, más del doble que en adultos más jóvenes.':'')+' La resistencia muscular (aguantar muchas repeticiones) baja antes y más que la fuerza máxima.'}seg=[[4,'ok'],[W,'baja']]}
    else if(ed==='j'){e='ok';t='Fuerza: se mantiene';d=(h===1?'Con 1 sesión a la semana, 1 serie por ejercicio y el mismo peso de siempre, la fuerza y el músculo se mantuvieron hasta 32 semanas (en adultos jóvenes).':'Con 1 sesión ya se mantenía en los estudios; con 2 tienes margen de sobra.')+(w>32?' Más allá de 32 semanas no hay datos.':'');seg=[[Math.min(32,W),'ok'],[W,'sin']]}
    else if(h===1){e='at';t='Fuerza: puede quedarse corto';d='En personas mayores, mantener el músculo puede requerir hasta 2 sesiones a la semana y 2-3 series por ejercicio. Una sesión es mucho mejor que nada, pero si puedes, haz 2.';seg=[[W,'at']]}
    else{e='ok';t='Fuerza: se mantiene';d='2 sesiones a la semana y 2-3 series por ejercicio, con el mismo peso: es lo que hizo falta en mayores para mantener el músculo.';seg=[[W,'ok']]}
    items.push([e,t,d]);filas.push(['Fuerza',seg])}
  if(ti!=='f'){var e2,t2,d2,s2;
    if(h===0){if(w<=4){e2='at';t2='Cardio: empieza a bajar pronto';d2='La forma aeróbica se pierde antes que la fuerza: en las primeras semanas sin entrenar ya baja la capacidad aeróbica máxima.'}else{e2='baja';t2='Cardio: se pierde parte de lo ganado';d2='Pasadas 4 semanas, quien llevaba poco tiempo entrenando pierde lo que había ganado de capacidad aeróbica; quien lleva años baja, pero sigue por encima de alguien que no entrena.'}s2=[[W,'baja']]}
    else if(h===1){e2='at';t2='Cardio: puede quedarse corto';d2='Para mantener la resistencia, los estudios usan al menos 2 sesiones a la semana. Con 1, mejor que nada.';s2=[[W,'at']]}
    else{e2='ok';t2='Cardio: se mantiene';d2='Con 2 sesiones a la semana, o recortando cada sesión entre un tercio y dos tercios (de 13 a 26 minutos), la resistencia se mantuvo hasta 15 semanas, siempre que no baje la intensidad.'+(w>15?' Más allá de 15 semanas no hay datos.':'');s2=[[Math.min(15,W),'ok'],[W,'sin']]}
    items.push([e2,t2,d2]);filas.push(['Cardio',s2])}
  var peor=items.reduce(function(a,x){return ORD[x[0]]>ORD[a]?x[0]:a},'ok');
  res.classList.remove('z-alto','z-medio','z-bajo');res.classList.add(peor==='ok'?'z-alto':peor==='at'?'z-medio':'z-bajo');
  $('o-tit').textContent=peor==='ok'?'Tranquilidad: vas a mantener casi todo':peor==='at'?'Vas a perder algo; con un poco más lo evitas':'Vas a perder parte de lo ganado, pero se recupera rápido';
  var X=function(s){return (s/W*100).toFixed(2)+'%'};
  $('o-linea').innerHTML=filas.map(function(f){var a=0;return '<div class="pl-fila"><span class="pl-n">'+f[0]+'</span><span class="pl-pista">'+f[1].map(function(sg){var h2='<b class="pl-'+sg[1]+'" style="left:'+X(a)+';width:'+X(sg[0]-a)+'"></b>';a=sg[0];return h2}).join('')+'<i style="left:'+X(Math.min(w,W))+'"></i></span></div>'}).join('')+'<div class="pl-eje"><span></span><span class="pl-pista">'+[0,4].concat(h>0&&ti!=='f'?[15]:[],h>0&&ti!=='r'&&ed==='j'?[32]:[]).filter(function(n){return n<=W&&Math.abs(n-Math.min(w,W))/W>0.16}).map(function(n){return '<em style="left:'+X(n)+'">'+n+'</em>'}).join('')+'<em class="tu" style="left:'+X(Math.min(w,W))+'">'+w+' sem.</em></span></div>';
  $('o-items').innerHTML=items.map(function(x){return '<div class="pi pi-'+x[0]+'"><p><b>'+x[1]+'</b><small>'+ETQ[x[0]]+'</small></p><span>'+x[2]+'</span></div>'}).join('');
  var plan=[];
  if(h===0)plan.push('Si puedes sacar un hueco, con esto basta para no perder:');
  if(ti!=='r')plan.push(ed==='j'?'Fuerza: 1 sesión a la semana, 1 serie de cada ejercicio principal, con el peso de siempre.':'Fuerza: 2 sesiones a la semana, 2-3 series de cada ejercicio, con el peso de siempre.');
  if(ti!=='f')plan.push('Cardio: 2 sesiones a la semana; pueden ser más cortas, de 13 a 26 minutos, si mantienes el ritmo.');
  plan.push('Lo que no puede bajar es la intensidad: el mismo peso y el mismo ritmo, aunque hagas menos.');
  $('o-plan').innerHTML=plan.map(function(x,i){return '<li'+(h===0&&i===0?' class="intro"':'')+'>'+x+'</li>'}).join('');
  copia='Mi parón de '+w+' semanas (FBE)\n'+items.map(function(x){return x[1]+'. '+x[2]}).join('\n')+'\nPlan mínimo:\n'+plan.filter(function(x,i){return !(h===0&&i===0)}).map(function(x){return '- '+x}).join('\n');
}
$('o-copiar').addEventListener('click',function(){copiar(this,copia)});
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''

tool_pagina('paron.html', '¿Cuánto pierdo si paro de entrenar?',
    '¿Cuánta fuerza y forma pierdes si paras de entrenar unas semanas? Y lo mínimo para mantener lo ganado, según el metaanálisis de Bosquet y la revisión de Spiering.',
    '¿Cuánto pierdo si paro de entrenar?',
    'Vacaciones, Navidad, una lesión o una época de mucho trabajo: dime cuántas semanas vas a parar y te digo qué se pierde, qué no, y lo mínimo para mantener lo ganado.',
    PAR_FORM, PAR_RES,
    '''<p>Lo que pasa con la fuerza sale del metaanálisis de <b>Bosquet y cols.</b> (103 estudios): hasta unas 4 semanas sin entrenar, la fuerza máxima casi no cambia; después baja, más en personas de 65 años o más, y la resistencia muscular baja antes y más que la fuerza máxima.</p>
<p>La dosis mínima para mantener sale de la revisión de <b>Spiering y cols.</b>: la fuerza y el músculo se mantuvieron hasta 32 semanas con 1 sesión a la semana y 1 serie por ejercicio (en adultos jóvenes), y la resistencia hasta 15 semanas con 2 sesiones. En mayores hizo falta más: hasta 2 sesiones y 2-3 series. En todos los casos, la clave fue mantener la intensidad.</p>
<p>La forma aeróbica se pierde antes: en deportistas entrenados baja en pocas semanas, y en quien empezó hace poco, lo ganado se pierde tras más de 4 semanas de parón (Mujika y Padilla).</p>
<p>Y al volver, lo perdido se recupera rápido: con parones de 3 semanas cada 6 de entrenamiento, en 6 meses se ganó la misma fuerza y el mismo músculo que entrenando sin parar (Ogasawara y cols.).</p>''',
    ['Bosquet L y cols. Effect of training cessation on muscular performance: a meta-analysis. Scand J Med Sci Sports. 2013;23(3):e140-9.',
     'Spiering BA, Mujika I, Sharp MA, Foulis SA. Maintaining physical performance: the minimal dose of exercise needed to preserve endurance and strength over time. J Strength Cond Res. 2021;35(5):1449-58.',
     'Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations. Part I: short term insufficient training stimulus. Sports Med. 2000;30(2):79-87.',
     'Mujika I, Padilla S. Cardiorespiratory and metabolic characteristics of detraining in humans. Med Sci Sports Exerc. 2001;33(3):413-21.',
     'Ogasawara R y cols. Comparison of muscle hypertrophy following 6-month of continuous and periodic strength training. Eur J Appl Physiol. 2013;113(4):975-85.'],
    PAR_JS, slug='paron', tira=('Hasta 4 semanas, casi nada', 'Mantén la intensidad', 'Se recupera rápido'))

# ---------------------------------------------------------------------------------------------
# 10. Suplementos con evidencia (clasificación ABCD del AIS; dosis del consenso del COI 2018; EFSA 2015)
_B = 'Hay estudios prometedores, pero no bastan para recomendarlo en general. El AIS solo lo contempla dentro de un estudio o con seguimiento de un profesional.'
_C = 'Los estudios no muestran beneficio para deportistas, o no hay estudios suficientes para opinar.'
_D = 'Prohibido en el deporte o con alto riesgo de estar contaminado con sustancias prohibidas. Aunque no compitas, no sabes qué te estás tomando.'
_MED = 'Corrige un déficit confirmado.'
_MEDD = 'No conviene tomarlo a ciegas: primero, un análisis, y la dosis, con tu médico.'
SUP = [
    # id, nombre, alias de búsqueda, grupo, subgrupo, para qué, dosis, ojo, cálculo, enlace
    ('creatina', 'Creatina (monohidrato)', 'creatine monohidrato', 'A', 'Rendimiento', 'Mejora la capacidad de repetir esfuerzos cortos e intensos y, con el entrenamiento, ayuda a ganar fuerza y músculo.', 'Opcional, carga: unos 20 g al día en 4 tomas durante 5-7 días. Mantenimiento: 3-5 g al día en una sola toma.', 'Tras la carga puede subir 1-2 kg de peso, sobre todo por agua.', '', ''),
    ('cafeina', 'Cafeína', 'cafe caffeine pastillas preentreno pre-entreno', 'A', 'Rendimiento', 'Mejora el rendimiento en esfuerzos de resistencia e intensos y reduce la sensación de esfuerzo.', '3-6 mg por kilo de peso, unos 60 minutos antes. También funcionan dosis menores (menos de 3 mg por kilo, unos 200 mg).', 'Dosis de 9 mg por kilo o más no mejoran más y dan más náuseas, ansiedad, insomnio e inquietud. La EFSA solo considera seguras tomas de hasta 200 mg de una vez y 400 mg al día.', 'caf', 'cafeina.html|Calcula tu cafeína del día'),
    ('betaalanina', 'Beta-alanina', 'beta alanina b-alanina', 'A', 'Rendimiento', 'Sube la carnosina del músculo, que amortigua la acidez en esfuerzos muy intensos.', 'Unos 65 mg por kilo al día, en tomas de 0,8-1,6 g cada 3-4 horas, durante 10-12 semanas.', 'Puede dar hormigueo pasajero en la piel o erupciones.', 'ba', ''),
    ('bicarbonato', 'Bicarbonato sódico', 'bicarbonato de sodio', 'A', 'Rendimiento', 'Amortigua la acidez en esfuerzos muy intensos.', '0,2-0,4 g por kilo en una toma, entre 60 y 150 minutos antes.', 'Las molestias digestivas son frecuentes. Lleva mucho sodio: si tienes la tensión alta o una enfermedad del riñón, consúltalo antes.', 'bic', ''),
    ('nitrato', 'Nitrato (zumo de remolacha)', 'remolacha beetroot zumo de remolacha nitratos', 'A', 'Rendimiento', 'Mejora la eficiencia en esfuerzos de resistencia.', '5-9 mmol (310-560 mg) de nitrato, 2-3 horas antes. Tomarlo varios días seguidos también puede ayudar.', 'Elige zumos o concentrados que indiquen los miligramos de nitrato.', '', ''),
    ('glicerol', 'Glicerol', 'glicerina', 'A', 'Rendimiento', 'Ayuda a retener líquido antes de pruebas largas con calor.', 'Protocolos concretos; mejor con un dietista-nutricionista deportivo.', 'No tiene sentido para el gimnasio.', '', ''),
    ('proteina', 'Proteína en polvo', 'proteina whey suero batido de proteina caseina proteina vegetal isolate', 'A', 'Alimento deportivo', 'Comodidad para llegar a la proteína del día cuando con la comida no llegas.', 'La que te falte para tu objetivo diario.', 'Es comida, no un atajo: si con la dieta llegas, no hace falta.', '', CALC + '|Calcula tu proteína del día'),
    ('deportivas', 'Bebidas, geles y barritas deportivas', 'isotonica bebida isotonica gel geles barrita barritas hidratos', 'A', 'Alimento deportivo', 'Energía en forma de hidratos fácil de tomar durante esfuerzos largos.', 'Según la duración y la intensidad del esfuerzo.', 'Para una sesión normal de gimnasio no suelen hacer falta.', '', ''),
    ('electrolitos', 'Electrolitos', 'sales sales minerales suero oral sodio potasio', 'A', 'Alimento deportivo', 'Reponer sodio y líquido cuando sudas mucho.', 'Según lo que sudes y el calor que haga.', '', '', ''),
    ('sustitutos', 'Sustitutos de comida', 'batido de comida barrita de comida', 'A', 'Alimento deportivo', 'Una comida práctica cuando no hay otra opción.', 'Como una comida más.', '', '', ''),
    ('vitaminad', 'Vitamina D', 'vitamina d d3 colecalciferol', 'A', 'Suplemento médico', _MED, 'No conviene tomarla a ciegas: primero, un análisis. Para mantener niveles en otoño e invierno se han usado 1.000 UI al día de vitamina D3.', 'Mejor con tu médico.', '', ''),
    ('hierro', 'Hierro', 'ferropenia anemia', 'A', 'Suplemento médico', _MED, _MEDD, 'Sin un análisis que lo justifique, mejor no tomarlo.', '', ''),
    ('calcio', 'Calcio', '', 'A', 'Suplemento médico', 'Cuando con la dieta no llegas.', _MEDD, '', '', ''),
    ('zinc', 'Zinc', 'cinc', 'A', 'Suplemento médico', _MED, _MEDD, '', '', ''),
    ('folato', 'Folato (ácido fólico)', 'acido folico vitamina b9', 'A', 'Suplemento médico', _MED, _MEDD, '', '', ''),
    ('polifenoles', 'Polifenoles de frutas', 'cereza cereza acida montmorency frutos rojos grosella negra granada', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('vitaminac', 'Vitamina C', 'acido ascorbico', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('mentol', 'Mentol', '', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('pepinillo', 'Zumo de pepinillo', 'pickle', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('quinina', 'Quinina', 'tonica', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('colageno', 'Colágeno', 'colageno gelatina', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('carnitina', 'Carnitina', 'l-carnitina l carnitina', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('cetonas', 'Cetonas', 'cetonas exogenas ketonas', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('omega3', 'Aceite de pescado (omega-3)', 'omega 3 omega3 aceite de pescado epa dha', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('nac', 'N-acetilcisteína', 'nac acetilcisteina', 'B', 'Evidencia emergente', _B, '', '', '', ''),
    ('magnesio', 'Magnesio', '', 'C', 'Sin beneficio demostrado', _C, '', 'Si tienes un déficit confirmado, es otra historia: eso lo trata tu médico.', '', ''),
    ('ala', 'Ácido alfa-lipoico', 'alfa lipoico', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('hmb', 'HMB', 'beta-hidroxi-beta-metilbutirato hidroximetilbutirato', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('bcaa', 'BCAA y leucina', 'aminoacidos ramificados bcaa leucina aminoacidos', 'C', 'Sin beneficio demostrado', _C, '', 'Si llegas a tu proteína del día, no aportan nada extra.', '', ''),
    ('fosfato', 'Fosfato', '', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('same', 'SAM-e', 'adenosilmetionina', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('vitaminae', 'Vitamina E', '', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('tirosina', 'Tirosina', 'l-tirosina', 'C', 'Sin beneficio demostrado', _C, '', '', '', ''),
    ('estimulantes', 'Estimulantes', 'quemagrasas quemador termogenico dmaa', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('prohormonas', 'Prohormonas y potenciadores hormonales', 'prohormona hormonas', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('peptidos', 'Liberadores de hormona del crecimiento y péptidos', 'peptidos gh hormona del crecimiento', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('beta2', 'Beta-2 agonistas', 'clembuterol beta 2', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('sarm', 'SARM', 'sarms moduladores selectivos del receptor de androgenos', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('moduladores', 'Moduladores metabólicos', '', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('calostro', 'Calostro', '', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('tribulus', 'Tribulus y otros potenciadores de testosterona', 'tribulus terrestris testosterona booster', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
    ('maca', 'Maca', 'raiz de maca', 'D', 'Prohibido o de riesgo', _D, '', '', '', ''),
]
SUP_G = {'A': 'Evidencia sólida para usos concretos, con protocolos basados en estudios.', 'B': 'Evidencia emergente, que merece más investigación.', 'C': 'Sin beneficio demostrado o sin estudios suficientes.', 'D': 'Prohibido o con alto riesgo de contaminación.'}
SUP_FORM = f'''<div class="tool-campo supl-busca"><label for="u-q">Busca un suplemento</label><input id="u-q" type="search" autocomplete="off" placeholder="Creatina, omega-3, magnesio, colágeno…"></div>
{seg("u-g", "Grupo de evidencia", [("", "Todos"), ("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], "", "supl-filtro")}
<div class="supl-lista" id="u-lista" role="list"></div>
<p class="tool-nota supl-cuenta" id="u-cuenta"></p>
<p class="vol-vacio" id="u-nada" hidden></p>
{campo_num("u-peso", "Tu peso, para calcular las dosis", 75, 30, 200, 1, ud="kg")}'''
SUP_RES = f'''<div class="supl-cab"><span class="supl-g" id="u-g-l">A</span><p class="tool-et" id="u-sub"></p></div>
<p class="res-veredicto grande-t" id="u-n"></p>
<p class="supl-gtxt" id="u-gtxt"></p>
<div class="supl-sec" id="u-s-para"><p class="tool-et">Para qué</p><p class="res-texto" id="u-para"></p></div>
<div class="supl-sec" id="u-s-dosis"><p class="tool-et">Dosis</p><p class="res-texto" id="u-dosis"></p><p class="res-chip" id="u-calc" hidden></p></div>
<div class="supl-sec" id="u-s-ojo"><p class="tool-et">Ojo</p><p class="res-texto" id="u-ojo"></p></div>
<p class="supl-enl" id="u-enl"></p>
{copiar_b("u-copiar", "Copiar ficha", False)}'''
SUP_JS = r'''(function(){
var S=__SUP__,G=__G__,$=function(i){return document.getElementById(i)},sel='creatina',copia='';
function norm(t){return String(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim()}
function g1(x){x=Math.round(x*10)/10;return fmt(x,x%1?1:0)}
function grupo(){var r=document.querySelector('input[name="u-g"]:checked');return r?r.value:''}
function lista(){var q=norm($('u-q').value),g=grupo(),L=S.filter(function(s){return (!g||s[3]===g)&&(!q||norm(s[1]+' '+s[2]).indexOf(q)>=0||q.split(' ').every(function(p){return norm(s[1]+' '+s[2]).indexOf(p)>=0}))});
  $('u-lista').innerHTML=L.map(function(s){return '<button type="button" role="listitem" class="supl-it g'+s[3]+(s[0]===sel?' sel':'')+'" data-id="'+s[0]+'"><b>'+s[3]+'</b>'+s[1]+'</button>'}).join('');
  $('u-nada').hidden=L.length>0;$('u-cuenta').textContent=L.length?(L.length===1?'1 suplemento':L.length+' suplementos')+' · toca uno para ver su ficha':'';if(!L.length)$('u-nada').textContent=q?'«'+$('u-q').value.trim()+'» no está en la clasificación del AIS. Eso no quiere decir que funcione ni que no: si te interesa, pregúntame.':'No hay suplementos en este grupo.';
  if(L.length===1&&L[0][0]!==sel){sel=L[0][0];ficha();lista()}}
function ficha(){var s=S.filter(function(x){return x[0]===sel})[0];if(!s)return;var kg=parseFloat($('u-peso').value),res=document.querySelector('.tool-res');
  res.classList.remove('z-alto','z-medio','z-bajo');res.classList.add(s[3]==='A'?'z-alto':s[3]==='D'?'z-bajo':'z-medio');
  $('u-g-l').textContent='Grupo '+s[3];$('u-g-l').className='supl-g g'+s[3];$('u-sub').textContent=s[4];$('u-n').textContent=s[1];$('u-gtxt').textContent=G[s[3]];
  $('u-para').textContent=s[5];$('u-s-dosis').hidden=!s[6];$('u-dosis').textContent=s[6];$('u-s-ojo').hidden=!s[7];$('u-ojo').textContent=s[7];
  var c='';if(kg>=30&&kg<=250){if(s[8]==='caf')c='Para tus '+fmt(kg)+' kg: '+fmt(kg*3)+'-'+fmt(kg*6)+' mg'+(kg*6>200?' · la EFSA da por seguras tomas de hasta 200 mg':'');if(s[8]==='ba')c='Para tus '+fmt(kg)+' kg: unos '+g1(kg*0.065)+' g al día';if(s[8]==='bic')c='Para tus '+fmt(kg)+' kg: '+g1(kg*0.2)+'-'+g1(kg*0.4)+' g'}
  $('u-calc').hidden=!c;$('u-calc').textContent=c;
  var l=s[9]?s[9].split('|'):null;$('u-enl').innerHTML=l?'<a class="btn claro" href="'+l[0]+'"'+(l[0].indexOf('http')===0?' rel="noopener"':'')+'>'+l[1]+'</a>':'';
  copia=s[1]+' · Grupo '+s[3]+' del AIS ('+G[s[3]].toLowerCase()+')\nPara qué: '+s[5]+(s[6]?'\nDosis: '+s[6]:'')+(c?'\n'+c:'')+(s[7]?'\nOjo: '+s[7]:'');}
$('u-lista').addEventListener('click',function(e){var b=e.target.closest('.supl-it');if(!b)return;sel=b.dataset.id;ficha();lista();if(window.innerWidth<960)document.querySelector('.tool-res').scrollIntoView({block:'start',behavior:'smooth'})});
$('u-q').addEventListener('input',lista);$('u-q').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();var b=$('u-lista').querySelector('.supl-it');if(b)b.click()}});
document.querySelector('.tool-form').addEventListener('change',function(e){if(e.target.name==='u-g')lista()});
$('u-peso').addEventListener('input',ficha);
$('u-copiar').addEventListener('click',function(){copiar(this,copia)});
lista();ficha();
})();'''.replace('__SUP__', json.dumps([list(s) for s in SUP], ensure_ascii=False)).replace('__G__', json.dumps(SUP_G, ensure_ascii=False))

tool_pagina('suplementos.html', 'Suplementos con evidencia',
    'Busca un suplemento y mira en qué grupo de evidencia lo pone el Instituto Australiano del Deporte (AIS), la dosis del consenso del Comité Olímpico Internacional calculada para tu peso y qué vigilar.',
    'Suplementos: cuáles tienen evidencia',
    'Busca un suplemento y mira en qué grupo lo pone el Instituto Australiano del Deporte, la dosis del Comité Olímpico Internacional calculada para tu peso y qué vigilar.',
    SUP_FORM, SUP_RES,
    '''<p>La clasificación es la del <b>Instituto Australiano del Deporte (AIS)</b>, que ordena los suplementos en cuatro grupos: A, evidencia sólida para usos concretos; B, evidencia emergente; C, sin beneficio demostrado o sin estudios suficientes; y D, prohibidos o con alto riesgo de contaminación.</p>
<p>Las dosis son las del <b>consenso del Comité Olímpico Internacional (2018)</b> y están pensadas para deportistas. Como recuerda el propio consenso, un suplemento solo aporta una contribución pequeña al lado de la alimentación y el entrenamiento.</p>
<p>Ningún producto está garantizado al 100 %: algunos suplementos llevan sustancias no declaradas. Los programas que analizan cada lote reducen el riesgo, pero no lo eliminan.</p>
<p>Si tomas medicación o tienes una enfermedad, consúltalo antes con tu médico.</p>''',
    ['Australian Institute of Sport. AIS Sports Supplement Framework: clasificación ABCD (versión vigente, consultada en noviembre de 2026).',
     'Maughan RJ y cols. IOC consensus statement: dietary supplements and the high-performance athlete. Br J Sports Med. 2018;52(7):439-55 (dosis y efectos secundarios).',
     'EFSA NDA Panel. Scientific opinion on the safety of caffeine. EFSA Journal. 2015;13(5):4102 (200 mg por toma y 400 mg al día).'],
    SUP_JS, slug='suplementos', tira=('Grupo A: evidencia sólida', 'La dosis, según tu peso', 'Cuidado con la contaminación'))

HERR_MAS += [('zonas-pulso.html', 'pulso', 'pulso', 'Zonas de pulso y esfuerzo', 'Tu pulso máximo y tus zonas, y cómo guiarte si tu medicación cambia el pulso.'),
    ('semaforo-dolor.html', 'dolor', 'semaforo', 'Semáforo del dolor', '¿Puedo entrenar con este dolor? Seguir, mantener o bajar la carga, con diario.'),
    ('test-sppb.html', 'sppb', 'andar', 'Test SPPB para tus padres', 'Equilibrio, marcha y levantarse de la silla, con cronómetro y puntuación de 0 a 12.'),
    ('paron.html', 'paron', 'pausa', '¿Cuánto pierdo si paro?', 'Qué se pierde en unas semanas sin entrenar y lo mínimo para mantenerlo.'),
    ('suplementos.html', 'suplementos', 'capsula', 'Suplementos con evidencia', 'Grupo de evidencia, dosis para tu peso y qué vigilar.')]

_h = open(f'{SAL}/herramientas.html', encoding='utf-8').read()
_mas = ('<div class="herr-mas sube"><h2 class="herr-mas-t">Más herramientas</h2><div class="herr-mas-rej">'
    + ''.join(f'<a class="herr-mini" href="{u}">{ilus(f"herr-{sl}", "herr-mini-img") or f"<i class=\"ic\">{ico(i)}</i>"}<b>{t}</b><span>{d}</span></a>' for u, sl, i, t, d in HERR_MAS)
    + '</div></div>\n  <p class="herr-nota sube">')
assert '<p class="herr-nota sube">' in _h
open(f'{SAL}/herramientas.html', 'w', encoding='utf-8').write(_h.replace('<p class="herr-nota sube">', _mas, 1))
