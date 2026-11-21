# ===== tercera tanda de herramientas (21/11/2026): actividad de la OMS, cintura y altura, fuerza de prension =====
# herramientas.py la ejecuta justo antes de poner las tarjetas «Más herramientas». Fuentes al pie de cada pagina;
# no cambiar cifras sin cambiar la fuente.
I.update({
    'calendario': '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="M8 14.5l2.5 2.5 5-5"/>',
    'cinta': '<path d="M4 8.5C4 6.6 7.6 5 12 5s8 1.6 8 3.5v7c0 1.9-3.6 3.5-8 3.5s-8-1.6-8-3.5z"/><path d="M4 8.5c0 1.9 3.6 3.5 8 3.5s8-1.6 8-3.5M9 12v2M12 12.2v3M15 12v2"/>',
    'mano': '<path d="M7 11V6.5a1.5 1.5 0 0 1 3 0V11M10 10V5a1.5 1.5 0 0 1 3 0v5M13 10V6a1.5 1.5 0 0 1 3 0v6"/><path d="M16 9.5a1.5 1.5 0 0 1 3 0V14a6 6 0 0 1-6 6h-1a6 6 0 0 1-5.4-3.4L4.8 13a1.5 1.5 0 0 1 2.6-1.5L9 14"/>',
})

# ---------------------------------------------------------------------------------------------
# 11. ¿Llegas a lo mínimo de la OMS? (Bull y cols. 2020, directrices de la OMS sobre actividad física)
OMS_FORM = (f'''<div class="tool-fila">{campo_num("a-mod", "Minutos a la semana de actividad moderada", 90, 0, 3000, 10, "Caminar rápido, bici suave, nadar tranquilo: puedes hablar, pero no cantar.", ud="min")}{campo_num("a-vig", "Minutos a la semana de actividad vigorosa", 0, 0, 2000, 5, "Correr, bici o natación intensas: solo frases cortas.", ud="min")}</div>
{campo_num("a-fza", "Días a la semana de fuerza", 1, 0, 7, 1, "Pesas, máquinas, bandas o tu peso, con los grupos musculares grandes.", ud="días")}'''
    + seg('a-edad', 'Edad', [('a', 'De 18 a 64 años'), ('m', '65 o más')], 'a')
    + f'''<div class="a-mayor" hidden>{campo_num("a-eq", "Días a la semana de equilibrio y fuerza combinados", 0, 0, 7, 1, "Ejercicio multicomponente: equilibrio, fuerza y marcha en la misma sesión.", ud="días")}</div>''')
OMS_RES = f'''<p class="tool-et">Tu semana, en minutos de actividad moderada</p>
<div class="res-grande"><b id="a-tot">–</b><span>min</span></div>
<div class="a-barra" id="a-barra" aria-hidden="true"><i id="a-rel"></i><span style="left:{150 / 450 * 100:.2f}%"><b>150</b></span><span style="left:{300 / 450 * 100:.2f}%"><b>300</b></span></div>
<ul class="a-checks" id="a-checks"></ul>
<p class="res-veredicto" id="a-tit"></p>
<p class="res-texto" id="a-txt"></p>
{copiar_b("a-copiar", "Copiar mi semana")}'''
OMS_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='';
function v(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return x>=0?x:0}
function pinta(){
  var mo=num('a-mod'),vi=num('a-vig'),fz=Math.round(num('a-fza')),ma=v('a-edad')==='m',eq=Math.round(num('a-eq')),tot=Math.round(mo+2*vi),res=document.querySelector('.tool-res');
  document.querySelector('.a-mayor').hidden=!ma;
  $('a-tot').textContent=tot;destella($('a-tot'));$('a-rel').style.width=Math.min(100,tot/450*100)+'%';
  var c1=tot>=150,c2=fz>=2,c3=!ma||eq>=3;
  var L=[[c1,'Actividad aeróbica: '+tot+' de al menos 150 minutos'+(vi?' (cada minuto vigoroso cuenta doble)':'')],[c2,'Fuerza: '+fz+(fz===1?' día':' días')+' de al menos 2']];
  if(ma)L.push([c3,'Equilibrio y fuerza combinados: '+eq+(eq===1?' día':' días')+' de al menos 3']);
  $('a-checks').innerHTML=L.map(function(x){return '<li class="'+(x[0]?'si':'no')+'">'+x[1]+'</li>'}).join('');
  res.classList.remove('z-alto','z-medio','z-bajo');
  var tit,txt;
  if(c1&&c2&&c3){res.classList.add('z-alto');tit=tot>300?'Cumples, y con beneficio extra':'Cumples las recomendaciones';txt=tot>300?'Pasar de 300 minutos de actividad moderada a la semana aporta beneficios adicionales para la salud.':'Llegas a lo mínimo de la OMS. Subir hacia los 300 minutos semanales aporta más beneficio.'}
  else if(c1||c2){res.classList.add('z-medio');tit='Vas por buen camino';txt='Te falta '+(!c1?'actividad aeróbica: '+(150-tot)+' minutos más a la semana':!c2?'un día más de fuerza'+(fz===0?' (o dos)':''):'el trabajo de equilibrio')+'. Cualquier cantidad cuenta: algo de actividad es mejor que nada.'}
  else{res.classList.add('z-bajo');tit='Aún por debajo';txt='Empieza por poco y ve subiendo: algo de actividad es mejor que nada, y cualquier intensidad suma. Si tienes una enfermedad o hace tiempo que no te mueves, mira antes el cribado de revisión médica.'}
  $('a-tit').textContent=tit;$('a-txt').textContent=txt+' Y reduce el tiempo que pasas sentado: sustitúyelo por actividad de cualquier intensidad.';
  $('a-copiar').hidden=false;
  copia='Mi semana frente a la OMS (FBE)\n'+L.map(function(x){return (x[0]?'Sí':'No')+' · '+x[1]}).join('\n')+'\nResultado: '+tit;
}
$('a-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return copia};
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''
tool_pagina('actividad-oms.html', '¿Llegas a lo mínimo de la OMS?',
    'Comprueba si tu semana cumple las recomendaciones de actividad física de la OMS: 150 a 300 minutos de actividad moderada, fuerza dos días y, a partir de los 65, equilibrio tres días.',
    '¿Llegas a lo mínimo de la OMS?',
    'Apunta lo que te mueves en una semana normal y mira si llegas a lo que recomienda la Organización Mundial de la Salud: actividad aeróbica, fuerza y, a partir de los 65, equilibrio.',
    OMS_FORM, OMS_RES,
    '''<p>Las directrices de la <b>OMS de 2020</b> recomiendan a los adultos de 18 a 64 años entre <b>150 y 300 minutos</b> a la semana de actividad aeróbica moderada, o entre 75 y 150 de vigorosa, o una combinación de las dos. Por eso aquí cada minuto vigoroso cuenta como dos moderados. Pasar de 300 minutos aporta beneficios adicionales.</p>
<p>Además, recomiendan actividades de <b>fuerza</b> que trabajen los grupos musculares grandes al menos <b>dos días</b> a la semana. A partir de los 65, añaden actividad <b>multicomponente</b> (equilibrio y fuerza) al menos <b>tres días</b> a la semana, para prevenir caídas.</p>
<p>Y dos mensajes que valen para todos: algo de actividad es mejor que nada, y conviene reducir el tiempo sentado y sustituirlo por actividad de cualquier intensidad.</p>''',
    ['Bull FC y cols. World Health Organization 2020 guidelines on physical activity and sedentary behaviour. Br J Sports Med. 2020;54(24):1451-62.',
     'Organización Mundial de la Salud. Directrices de la OMS sobre actividad física y hábitos sedentarios. Ginebra: OMS; 2020.'],
    OMS_JS, slug='oms', tira=('Moverte más', 'Fuerza dos días', 'Equilibrio a partir de los 65'))

# ---------------------------------------------------------------------------------------------
# 12. Cintura y altura (NICE NG246, 2025, que recoge los umbrales de 2022)
CIN_FORM = (f'''<div class="tool-fila">{campo_num("w-alt", "Altura", 170, 120, 220, 1, ud="cm")}{campo_num("w-cin", "Cintura", 84, 40, 200, 0.5, ud="cm")}</div>
<details class="rev-det" open><summary>Cómo medir la cintura</summary><p>Busca la parte de abajo de las costillas y la parte de arriba del hueso de la cadera. Rodea la cintura con la cinta justo a medio camino entre los dos puntos y mide después de soltar el aire con normalidad.</p></details>
<p class="tool-nota">Sirve para adultos con un índice de masa corporal por debajo de 35, de los dos sexos y de cualquier origen, también con mucha masa muscular. No sirve en el embarazo.</p>''')
CIN_RES = f'''<p class="tool-et">Tu índice cintura/altura</p>
<div class="res-grande"><b id="w-r">–</b></div>
<p class="res-chip" id="w-cat" hidden></p>
<div class="w-escala" aria-hidden="true"><span class="w-v">0,4-0,49</span><span class="w-a">0,5-0,59</span><span class="w-r">0,6 o más</span><i id="w-m"></i></div>
<p class="res-veredicto" id="w-tit"></p>
<p class="res-texto" id="w-txt"></p>
{copiar_b("w-copiar", "Copiar resultado")}'''
CIN_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='';
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return x>0?x:null}
function pinta(){
  var h=num('w-alt'),c=num('w-cin'),res=document.querySelector('.tool-res');res.classList.remove('z-alto','z-medio','z-bajo');
  if(!h||!c||h<100||c<30){$('w-r').textContent='–';$('w-cat').hidden=true;$('w-tit').textContent='Escribe tu altura y tu cintura.';$('w-txt').textContent='';$('w-copiar').hidden=true;$('w-m').style.left='0';return}
  var r=c/h,rr=Math.round(r*100)/100,lim=Math.floor(h*0.5*10)/10,cat,tit,txt;
  $('w-r').textContent=fmt(rr,2);destella($('w-r'));$('w-m').style.left=Math.max(0,Math.min(100,(r-0.35)/(0.75-0.35)*100))+'%';
  if(r<0.4){res.classList.add('z-medio');cat='Por debajo de 0,4';tit='Por debajo del rango de la guía';txt='La guía de NICE describe como saludable de 0,4 a 0,49. Un valor más bajo no se clasifica ahí: si además has perdido peso sin buscarlo, coméntalo con tu médico.'}
  else if(r<0.5){res.classList.add('z-alto');cat='Saludable (0,4 a 0,49)';tit='Grasa abdominal en rango saludable';txt='Sin aumento del riesgo para la salud por la grasa abdominal. Para tu altura, mantén la cintura por debajo de '+fmt(lim,lim%1?1:0)+' cm.'}
  else if(r<0.6){res.classList.add('z-medio');cat='Aumentada (0,5 a 0,59)';tit='Grasa abdominal aumentada';txt='Indica más riesgo para la salud (por ejemplo, de diabetes tipo 2 o enfermedad cardiovascular). Para tu altura, la cintura debería quedar por debajo de '+fmt(lim,lim%1?1:0)+' cm. Pide a tu médico que valore tus factores de riesgo.'}
  else{res.classList.add('z-bajo');cat='Alta (0,6 o más)';tit='Grasa abdominal alta';txt='Indica un riesgo para la salud más alto todavía. Conviene una valoración de tus factores de riesgo cardiometabólico con tu médico. Para tu altura, la cintura debería quedar por debajo de '+fmt(lim,lim%1?1:0)+' cm.'}
  $('w-cat').hidden=false;$('w-cat').textContent=cat;$('w-tit').textContent=tit;$('w-txt').textContent=txt;$('w-copiar').hidden=false;
  copia='Índice cintura/altura (FBE): '+fmt(rr,2)+' · '+cat+'\nCintura '+fmt(c,c%1?1:0)+' cm · altura '+fmt(h)+' cm (umbrales de NICE)';
}
$('w-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return copia};
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''
tool_pagina('cintura-altura.html', 'Cintura y altura: tu grasa abdominal',
    'Calcula tu índice cintura/altura y mira en qué rango de grasa abdominal estás según la guía de NICE: saludable de 0,4 a 0,49, aumentada de 0,5 a 0,59 y alta desde 0,6.',
    'Tu cintura, frente a tu altura',
    'Una cinta métrica dice más que la báscula sobre la grasa que rodea tus órganos. Divide tu cintura entre tu altura y mira en qué rango estás según la guía clínica de NICE.',
    CIN_FORM, CIN_RES,
    '''<p>El <b>índice cintura/altura</b> estima la grasa abdominal, la que más se relaciona con la diabetes tipo 2, la tensión alta y la enfermedad cardiovascular. La regla es sencilla: tu cintura debería medir menos de la mitad de tu altura.</p>
<p>Los rangos son los de la guía de <b>NICE</b> sobre sobrepeso, obesidad y grasa abdominal: de 0,4 a 0,49, grasa abdominal saludable, sin aumento del riesgo; de 0,5 a 0,59, aumentada; y 0,6 o más, alta, con un riesgo todavía mayor.</p>
<p>La guía lo recomienda junto al índice de masa corporal en adultos con un IMC por debajo de 35, de los dos sexos y de cualquier origen, también en personas con mucha masa muscular, en las que el IMC sobreestima la grasa. No sirve en el embarazo.</p>''',
    ['National Institute for Health and Care Excellence (NICE). Overweight, obesity and central adiposity: identifying, assessing and managing (NG246). 2025 (umbrales del índice cintura/altura de 2022 y cómo medir la cintura).'],
    CIN_JS, slug='cintura', tira=('Mide a medio camino', 'Divide entre tu altura', 'Menos de la mitad'))

# ---------------------------------------------------------------------------------------------
# 13. Fuerza de prension (EWGSOP2, Cruz-Jentoft 2019; protocolo de Southampton, Roberts 2011)
PRE_FORM = (seg('g-sexo', 'Sexo', [('h', 'Hombre'), ('m', 'Mujer')], 'h')
    + f'''<div class="tool-fila">{campo_num("g-1", "Intento 1", "", 1, 120, 0.1, ud="kg")}{campo_num("g-2", "Intento 2", "", 1, 120, 0.1, ud="kg")}</div>
{campo_num("g-3", "Intento 3", "", 1, 120, 0.1, "Apunta los intentos de las dos manos; cuenta el mejor.", ud="kg")}
<details class="rev-det"><summary>Cómo hacer la prueba</summary><p>Con un dinamómetro de mano. Siéntate en una silla con brazos, apoya los antebrazos, con el codo doblado a unos 90 grados y la muñeca recta. Aprieta lo más fuerte que puedas durante unos segundos. Haz tres intentos con cada mano y quédate con el mejor.</p></details>''')
PRE_RES = f'''<p class="tool-et">Tu mejor intento</p>
<div class="res-grande"><b id="g-max">–</b><span>kg</span></div>
<div class="g-barra" aria-hidden="true"><i id="g-rel"></i><span id="g-cor"><b></b></span></div>
<p class="res-veredicto" id="g-tit">Apunta al menos un intento.</p>
<p class="res-texto" id="g-txt">Con un dinamómetro de mano, sentado y con el codo doblado.</p>
{copiar_b("g-copiar", "Copiar resultado")}'''
PRE_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='';
function v(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:'h'}
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return x>0&&x<200?x:null}
function pinta(){
  var s=v('g-sexo'),cor=s==='h'?27:16,ts=['g-1','g-2','g-3'].map(num).filter(Boolean),res=document.querySelector('.tool-res'),top=s==='h'?70:45;
  $('g-cor').style.left=(cor/top*100)+'%';$('g-cor').querySelector('b').textContent=cor;res.classList.remove('z-alto','z-medio','z-bajo');
  if(!ts.length){$('g-max').textContent='–';$('g-rel').style.width='0';$('g-tit').textContent='Apunta al menos un intento.';$('g-txt').textContent='Con un dinamómetro de mano, sentado y con el codo doblado.';$('g-copiar').hidden=true;return}
  var m=Math.max.apply(null,ts),tit,txt;
  $('g-max').textContent=fmt(m,m%1?1:0);destella($('g-max'));$('g-rel').style.width=Math.min(100,m/top*100)+'%';
  if(m<cor){res.classList.add('z-bajo');tit='Fuerza de prensión baja';txt='Por debajo de '+cor+' kg en '+(s==='h'?'hombres':'mujeres')+', el punto de corte del consenso europeo de sarcopenia (EWGSOP2). Para ellos, una fuerza baja hace «probable» la sarcopenia: coméntalo con tu médico. El entrenamiento de fuerza es el tratamiento principal.'}
  else{res.classList.add('z-alto');tit='Por encima del punto de corte';txt='Estás por encima de '+cor+' kg, el umbral de fuerza baja del consenso europeo para '+(s==='h'?'hombres':'mujeres')+'. Repetirlo cada pocos meses sirve para ver la tendencia.'}
  if(ts.length<3)txt+=' Con tres intentos el resultado es más fiable.';
  $('g-tit').textContent=tit;$('g-txt').textContent=txt;$('g-copiar').hidden=false;
  copia='Fuerza de prensión (FBE): '+fmt(m,m%1?1:0)+' kg, mejor de '+ts.length+(ts.length===1?' intento':' intentos')+' ('+(s==='h'?'hombre':'mujer')+')\n'+tit+' · punto de corte EWGSOP2: '+cor+' kg';
}
$('g-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return copia};
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''
tool_pagina('prension.html', 'Fuerza de prensión con dinamómetro',
    'Compara tu fuerza de prensión con el punto de corte del consenso europeo de sarcopenia (EWGSOP2): menos de 27 kg en hombres y de 16 kg en mujeres. Con el protocolo de medida paso a paso.',
    'Tu fuerza de prensión',
    'La fuerza con la que aprietas la mano es una de las medidas de fuerza más usadas en medicina. Apunta tus intentos con un dinamómetro y compáralos con el punto de corte del consenso europeo de sarcopenia.',
    PRE_FORM, PRE_RES,
    '''<p>El consenso europeo de sarcopenia (<b>EWGSOP2</b>) usa la fuerza de prensión como primer paso: por debajo de <b>27 kg en hombres</b> y de <b>16 kg en mujeres</b>, la fuerza es baja y la sarcopenia se considera probable. Después se confirma midiendo la masa muscular y se valora su gravedad con pruebas como la velocidad de la marcha o el <a href="test-sppb.html">SPPB</a>.</p>
<p>La forma de medir sigue el <b>protocolo de Southampton</b>: sentado en una silla con brazos, antebrazos apoyados, codo a unos 90 grados, tres intentos con cada mano y se queda el mejor.</p>
<p>Si no tienes dinamómetro, el <a href="test-silla.html">test de la silla</a> también mide la fuerza de piernas en casa.</p>''',
    ['Cruz-Jentoft AJ y cols. Sarcopenia: revised European consensus on definition and diagnosis (EWGSOP2). Age Ageing. 2019;48(1):16-31 (puntos de corte de 27 y 16 kg).',
     'Roberts HC y cols. A review of the measurement of grip strength in clinical and epidemiological studies: towards a standardised approach. Age Ageing. 2011;40(4):423-9 (protocolo de Southampton).'],
    PRE_JS, slug='prension', tira=('Sentado, codo a 90 grados', 'Tres intentos por mano', 'Cuenta el mejor'))

# ---------------------------------------------------------------------------------------------
# 14. Calorías de mantenimiento (Mifflin-St Jeor 1990; niveles de actividad de FAO/OMS/UNU 2004; precisión, Frankenfield 2005)
I.update({'llama2': '<path d="M12 3c1 3 4 4.5 4 8.5a4 4 0 0 1-8 0c0-1.5.6-2.6 1.5-3.5.2 1.5 1 2.3 2 2.5-.5-2.5-.3-5 .5-7.5z"/><path d="M8 15.5a4 4 0 0 0 8 0"/>'})
CAL_FORM = (seg('k-sexo', 'Sexo', [('h', 'Hombre'), ('m', 'Mujer')], 'h')
    + f'''<div class="tool-fila">{campo_num("k-edad", "Edad", 40, 18, 100, 1, ud="años")}{campo_num("k-peso", "Peso", 75, 35, 250, 0.5, ud="kg")}</div>
{campo_num("k-alt", "Altura", 175, 130, 220, 1, ud="cm")}'''
    + seg('k-act', 'Tu día a día', [('1', 'Poco activo'), ('2', 'Activo'), ('3', 'Muy activo')], '1')
    + '<p class="tool-nota k-ayuda" id="k-ayuda"></p><p class="tool-nota">Si tienes o has tenido un trastorno de la conducta alimentaria, mejor no te guíes por calorías: háblalo con tu médico.</p>')
CAL_RES = f'''<p class="tool-et">Para mantener tu peso, al día</p>
<div class="res-grande"><b id="k-rango">–</b><span>kcal</span></div>
<p class="res-chip" id="k-bmr" hidden></p>
<div class="k-barra" aria-hidden="true"><i id="k-b1"></i><i id="k-b2"></i></div>
<p class="res-texto" id="k-txt"></p>
<p class="supl-enl"><a class="btn claro" href="{CALC}" rel="noopener">Calcula tu proteína</a></p>
{copiar_b("k-copiar", "Copiar resultado")}'''
CAL_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='',PAL={'1':[1.40,1.69,'Trabajo sentado y poco ejercicio, o algo de actividad suave.'],'2':[1.70,1.99,'Trabajo de pie o caminando, o ejercicio moderado casi todos los días.'],'3':[2.00,2.40,'Trabajo físico duro o entrenamiento intenso a diario.']};
function v(n){var r=document.querySelector('input[name="'+n+'"]:checked');return r?r.value:null}
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return x>0?x:null}
function r50(x){return Math.round(x/50)*50}
function pinta(){
  var s=v('k-sexo')||'h',e=num('k-edad'),w=num('k-peso'),h=num('k-alt'),a=PAL[v('k-act')||'1'];$('k-ayuda').textContent=a[2];
  if(!(e>=18&&e<=110&&w>=30&&w<=300&&h>=120&&h<=230)){$('k-rango').textContent='–';$('k-bmr').hidden=true;$('k-txt').textContent='Completa tus datos.';$('k-copiar').hidden=true;return}
  var bmr=10*w+6.25*h-5*e+(s==='h'?5:-161),lo=r50(bmr*a[0]),hi=r50(bmr*a[1]);
  $('k-rango').textContent=fmt(lo)+'–'+fmt(hi);destella($('k-rango'));$('k-bmr').hidden=false;$('k-bmr').textContent='En reposo: unas '+fmt(Math.round(bmr/10)*10)+' kcal (Mifflin-St Jeor)';
  $('k-b1').style.width=(lo/4500*100)+'%';$('k-b2').style.width=((hi-lo)/4500*100)+'%';
  $('k-txt').textContent='Es una estimación: la fórmula acierta con un margen del 10 % en la mayoría de los adultos, y el gasto real cambia con el sueño, el estrés o el ejercicio de cada semana. Lo que manda es cómo evoluciona tu peso durante unas semanas.';
  $('k-copiar').hidden=false;copia='Calorías de mantenimiento (FBE): '+fmt(lo)+'-'+fmt(hi)+' kcal al día\nEn reposo: unas '+fmt(Math.round(bmr/10)*10)+' kcal (Mifflin-St Jeor) · '+(s==='h'?'hombre':'mujer')+', '+e+' años, '+fmt(w,w%1?1:0)+' kg, '+fmt(h)+' cm · nivel de actividad '+a[0].toFixed(2).replace('.',',')+'-'+a[1].toFixed(2).replace('.',',');
}
$('k-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return copia};
document.querySelector('.tool-form').addEventListener('input',pinta);document.querySelector('.tool-form').addEventListener('change',pinta);pinta();
})();'''
tool_pagina('calorias.html', 'Calorías de mantenimiento',
    'Estima cuántas calorías gastas al día para mantener tu peso con la fórmula de Mifflin-St Jeor y los niveles de actividad de la FAO y la OMS. Una estimación con su margen de error.',
    'Tus calorías para mantener el peso',
    'Una estimación de lo que gastas al día con la fórmula más fiable para adultos (Mifflin-St Jeor) y tu nivel de actividad. Sirve de punto de partida, no de número exacto.',
    CAL_FORM, CAL_RES,
    '''<p>El gasto en reposo se calcula con la ecuación de <b>Mifflin-St Jeor</b>, la que mejor acierta en adultos según la revisión de Frankenfield y cols.: queda dentro de un margen del 10 % en la mayoría de las personas, aunque se equivoca más en algunas.</p>
<p>Ese gasto se multiplica por tu <b>nivel de actividad física</b>, con los tramos del informe de la FAO, la OMS y la Universidad de las Naciones Unidas: de 1,40 a 1,69 en una vida poco activa, de 1,70 a 1,99 en una activa y de 2,00 a 2,40 en una muy activa. Por eso el resultado es un rango y no un número.</p>
<p>Úsalo como punto de partida: si durante unas semanas tu peso se mantiene, estás en tu mantenimiento. Si tienes o has tenido un trastorno de la conducta alimentaria, no te guíes por calorías y háblalo con tu médico.</p>''',
    ['Mifflin MD, St Jeor ST, Hill LA y cols. A new predictive equation for resting energy expenditure in healthy individuals. Am J Clin Nutr. 1990;51(2):241-7.',
     'FAO, OMS y UNU. Human energy requirements: report of a joint FAO/WHO/UNU expert consultation. Roma: FAO; 2004 (niveles de actividad física).',
     'Frankenfield D, Roth-Yousey L, Compher C. Comparison of predictive equations for resting metabolic rate in healthy nonobese and obese adults: a systematic review. J Am Diet Assoc. 2005;105(5):775-89.'],
    CAL_JS, slug='calorias', tira=('Tu gasto en reposo', 'Por tu actividad', 'Ajusta con tu peso'))

HERR_MAS += [('actividad-oms.html', 'oms', 'calendario', '¿Llegas a lo mínimo de la OMS?', 'Tu semana de actividad frente a las recomendaciones de la OMS: aeróbica, fuerza y equilibrio.'),
    ('cintura-altura.html', 'cintura', 'cinta', 'Cintura y altura', 'Tu grasa abdominal con una cinta métrica, con los rangos de la guía de NICE.'),
    ('prension.html', 'prension', 'mano', 'Fuerza de prensión', 'Tu fuerza con un dinamómetro, frente al punto de corte del consenso europeo de sarcopenia.'),
    ('calorias.html', 'calorias', 'llama2', 'Calorías de mantenimiento', 'Lo que gastas al día para mantener tu peso, con su margen de error.')]

SEC_PAGS_H3 = ['actividad-oms.html', 'cintura-altura.html', 'prension.html', 'calorias.html']  # entran en el sitemap desde extras.py
