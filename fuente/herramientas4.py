# Cuarta tanda de herramientas (22/11/2026): temporizador, Mi semana activa, pasos al día, tensión en casa y equilibrio.
# La ejecuta herramientas.py después de herramientas3.py (antes de poner las tarjetas). Estilos en app.css. Pruebas: pruebas/calculadoras-4.mjs.
# Cifras y fuentes (comprobadas el 22/11/2026; fichas en fuentes.json):
#  - Semana activa: OMS 2020 (Bull y cols.): 150 min moderados o 75 vigorosos (el vigoroso cuenta doble) y fuerza 2 días.
#  - Pasos: Paluch 2022 (de 6000 a 8000 con 60 años o más; de 8000 a 10000 con menos de 60) y cadencia de Tudor-Locke 2018 (100 pasos/min o más = moderada).
#  - Tensión en casa: guía ESC 2024 (McEvoy): <120/70 no elevada; 120/70 a <135/85 elevada; >=135/85 umbral de hipertensión;
#    3 a 7 días, mañana y tarde-noche, dos tomas separadas 1-2 min, se promedian todas; >=180/110, descartar una emergencia.
#  - Equilibrio: Araujo 2022 (10 s a una pierna, hasta tres intentos; 1.702 personas de 51 a 75 años; 20,4 % no lo completó; HR 1,84).
#  - Temporizador: sin cifras de salud (no recomienda descansos; los marca tu plan).
I.update({
    'crono': '<circle cx="12" cy="13.5" r="7.5"/><path d="M12 9.5v4l2.5 2M9.5 3h5M12 3v3"/>',
    'anillos': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 3a9 9 0 0 1 9 9"/>',
    'pasos': '<path d="M8 4c1.7 0 2.6 1.6 2.6 4S10 13 8.4 13 6 10.5 6 8s.3-4 2-4zM7 15.5h3v2a1.5 1.5 0 0 1-3 0zM16 8c1.7 0 2.6 1.6 2.6 4s-.6 5-2.2 5-2.4-2.5-2.4-5 .3-4 2-4zM15 19.5h3v1a1.5 1.5 0 0 1-3 0z"/>',
    'tension': '<path d="M12 20s-7-4.3-7-9.5A4 4 0 0 1 12 8a4 4 0 0 1 7 2.5c0 5.2-7 9.5-7 9.5z"/><path d="M3 13h4l1.5-2.5 2.5 5 2-3.5h8"/>',
    'equilibrio': '<circle cx="12" cy="4.5" r="1.8"/><path d="M12 7v7M12 9l-4 2M12 9l4 2M12 14v7M12 14l3.5 2-1.5 3"/>',
})

# ---------------------------------------------------------------------------------------------
# 15. Temporizador de descansos e intervalos (sin cifras de salud)
TMP_FORM = (seg('t-modo', 'Modo', [('d', 'Descanso entre series'), ('i', 'Intervalos')], 'd', 'tmp-modo')
    + f'''<div id="t-pd"><div class="tmp-chips" role="group" aria-label="Descanso">{"".join(f'<button type="button" data-s="{s}">{t}</button>' for s, t in [(45, "45 s"), (60, "1 min"), (90, "1:30"), (120, "2 min"), (180, "3 min"), (300, "5 min")])}</div>
{campo_num("t-seg", "Descanso", 90, 5, 900, 5, "El que marque tu plan. El temporizador solo lo cuenta.", ud="s")}</div>
<div id="t-pi" hidden><div class="tool-fila">{campo_num("t-tr", "Trabajo", 30, 5, 900, 5, ud="s")}{campo_num("t-ds", "Descanso", 30, 0, 900, 5, ud="s")}</div>{campo_num("t-ro", "Rondas", 8, 1, 60, 1)}</div>
<div class="tmp-ops"><label><input type="checkbox" id="t-son" checked><span>Sonido</span></label><label><input type="checkbox" id="t-vib" checked><span>Vibración</span></label><label><input type="checkbox" id="t-luz" checked><span>Pantalla encendida</span></label></div>
<p class="tool-nota">Funciona sin conexión. Si instalas la web en el móvil, lo tienes a un toque.</p>''')
TMP_RES = '''<p class="tool-et" id="t-et">Listo</p>
<div class="tmp-reloj" id="t-reloj"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="tmp-pista" cx="60" cy="60" r="52"/><circle class="tmp-arco" id="t-arco" cx="60" cy="60" r="52" pathLength="100" transform="rotate(-90 60 60)"/></svg>
<div class="tmp-num"><b id="t-num" role="timer">1:30</b><span id="t-fase"></span></div></div>
<p class="tmp-serie" id="t-serie"></p>
<div class="tmp-bot"><button type="button" class="tmp-ir" id="t-ir">Empezar</button><button type="button" class="tmp-b2" id="t-mas">+15 s</button><button type="button" class="tmp-b2" id="t-cero">Reiniciar</button></div>
<button type="button" class="tmp-gym" id="t-gym" aria-pressed="false">Pantalla completa</button>
<p class="oculto" id="t-voz" aria-live="assertive"></p>'''
TMP_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},K='fbe-temporizador',cfg={m:'d',s:90,tr:30,ds:30,ro:8,son:1,vib:1,luz:1};
try{var g=JSON.parse(localStorage.getItem(K)||'{}')||{};Object.keys(cfg).forEach(function(k){if(g[k]!=null)cfg[k]=g[k]})}catch(e){}
var est='listo',fin=0,queda=0,total=0,fase='',ronda=0,series=0,tic=0,ac=null,wl=null,ult=-1,tit=document.title,caja=document.querySelector('.tool');
function guarda(){try{localStorage.setItem(K,JSON.stringify(cfg))}catch(e){}}
function mmss(s){s=Math.max(0,Math.ceil(s-0.05));return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function pita(f,d){if(!cfg.son)return;try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();if(ac.state==='suspended')ac.resume();var o=ac.createOscillator(),gn=ac.createGain(),t=ac.currentTime;o.frequency.value=f;o.connect(gn);gn.connect(ac.destination);gn.gain.setValueAtTime(.0001,t);gn.gain.exponentialRampToValueAtTime(.35,t+.02);gn.gain.exponentialRampToValueAtTime(.0001,t+d);o.start(t);o.stop(t+d+.03)}catch(e){}}
function vibra(p){if(cfg.vib&&navigator.vibrate){try{navigator.vibrate(p)}catch(e){}}}
function luz(on){if(!('wakeLock' in navigator))return;if(on&&cfg.luz){navigator.wakeLock.request('screen').then(function(l){wl=l},function(){})}else if(wl){try{wl.release()}catch(e){}wl=null}}
function durDe(f){return cfg.m==='d'?cfg.s:(f==='descanso'?cfg.ds:cfg.tr)}
function lee(){var n=function(id,mn,mx){var x=parseInt($(id).value,10);return isNaN(x)?mn:Math.max(mn,Math.min(mx,x))};cfg.m=document.querySelector('input[name="t-modo"]:checked').value;cfg.s=n('t-seg',5,900);cfg.tr=n('t-tr',5,900);cfg.ds=n('t-ds',0,900);cfg.ro=n('t-ro',1,60);cfg.son=$('t-son').checked?1:0;cfg.vib=$('t-vib').checked?1:0;cfg.luz=$('t-luz').checked?1:0;guarda()}
function pon(){$('t-seg').value=cfg.s;$('t-tr').value=cfg.tr;$('t-ds').value=cfg.ds;$('t-ro').value=cfg.ro;$('t-son').checked=!!cfg.son;$('t-vib').checked=!!cfg.vib;$('t-luz').checked=!!cfg.luz;var r=document.querySelector('input[name="t-modo"][value="'+cfg.m+'"]');if(r)r.checked=true}
function chips(){[].forEach.call(document.querySelectorAll('.tmp-chips button'),function(b){b.setAttribute('aria-pressed',String(+b.dataset.s===cfg.s))})}
function pinta(){
  $('t-pd').hidden=cfg.m!=='d';$('t-pi').hidden=cfg.m!=='i';chips();
  var q=est==='listo'?durDe(cfg.m==='d'?'descanso':'trabajo'):queda,t=est==='listo'?q:total;
  $('t-num').textContent=mmss(q);$('t-arco').style.strokeDashoffset=(t>0?100-Math.max(0,Math.min(1,q/t))*100:0);
  caja.dataset.est=est;caja.dataset.fase=fase;
  $('t-et').textContent=est==='listo'?'Listo':est==='pausa'?'En pausa':est==='fin'?(cfg.m==='d'?'¡A por la siguiente serie!':'¡Terminado!'):(fase==='trabajo'?'Trabajo':'Descanso');
  $('t-fase').textContent=cfg.m==='i'&&est!=='listo'?'Ronda '+Math.min(ronda,cfg.ro)+' de '+cfg.ro:(cfg.m==='i'?cfg.ro+' rondas':'');
  $('t-serie').textContent=cfg.m==='d'&&series?(series===1?'1 descanso hecho':series+' descansos hechos'):'';
  $('t-ir').textContent=est==='corre'?'Pausa':est==='pausa'?'Seguir':est==='fin'?(cfg.m==='d'?'Otro descanso':'Repetir'):'Empezar';
  $('t-mas').hidden=!(cfg.m==='d'&&(est==='corre'||est==='pausa'));$('t-cero').hidden=est==='listo';
  document.title=est==='corre'||est==='pausa'?mmss(q)+' · '+$('t-et').textContent:tit;
}
function faseNueva(f){fase=f;total=durDe(f);queda=total;fin=Date.now()+total*1000;ult=-1;$('t-voz').textContent=cfg.m==='i'?(f==='trabajo'?'Trabajo, ronda '+ronda:'Descanso'):'';}
function acaba(){est='fin';clearInterval(tic);tic=0;queda=0;luz(false);pita(1320,.7);vibra([300,120,300]);$('t-voz').textContent=cfg.m==='d'?'Descanso terminado':'Intervalos terminados';pinta()}
function paso(){
  if(est!=='corre')return;queda=(fin-Date.now())/1000;var s=Math.ceil(queda-0.05);
  if(s!==ult){ult=s;if(s<=3&&s>=1){pita(880,.12);vibra(40)}}
  if(queda<=0){
    if(cfg.m==='d'){acaba();return}
    if(fase==='trabajo'&&cfg.ds>0&&ronda<cfg.ro){pita(660,.4);vibra(200);faseNueva('descanso')}
    else if(ronda<cfg.ro){ronda++;pita(1100,.4);vibra(200);faseNueva('trabajo')}
    else{acaba();return}
  }
  pinta();
}
function empieza(){lee();est='corre';if(cfg.m==='d'){series++;faseNueva('descanso')}else{ronda=1;faseNueva('trabajo')}luz(true);pita(1100,.15);clearInterval(tic);tic=setInterval(paso,200);pinta()}
$('t-ir').addEventListener('click',function(){
  if(est==='corre'){est='pausa';queda=(fin-Date.now())/1000;clearInterval(tic);tic=0;luz(false);pinta()}
  else if(est==='pausa'){est='corre';fin=Date.now()+queda*1000;luz(true);tic=setInterval(paso,200);pinta()}
  else empieza();
});
$('t-mas').addEventListener('click',function(){if(est==='corre'){fin+=15000;total+=15}else if(est==='pausa'){queda+=15;total+=15}paso();pinta()});
$('t-cero').addEventListener('click',function(){est='listo';fase='';clearInterval(tic);tic=0;luz(false);ronda=0;series=0;lee();pinta()});
document.querySelector('.tmp-chips').addEventListener('click',function(e){var b=e.target.closest('button[data-s]');if(!b)return;$('t-seg').value=b.dataset.s;lee();if(est==='listo'||est==='fin'){est='listo';pinta()}else pinta()});
document.querySelector('.tool-form').addEventListener('input',function(){lee();if(est==='listo')pinta();else chips()});
document.querySelector('.tool-form').addEventListener('change',function(){lee();if(est==='listo'||est==='fin'){est='listo';fase='';pinta()}});
document.addEventListener('visibilitychange',function(){if(!document.hidden&&est==='corre'){luz(true);paso()}});
document.addEventListener('keydown',function(e){if(e.code==='Space'&&!/INPUT|BUTTON|TEXTAREA|SELECT|A/.test(e.target.tagName)){e.preventDefault();$('t-ir').click()}});
var gym=$('t-gym');function sal(){caja.classList.remove('tmp-full');document.documentElement.classList.remove('tmp-abierto');gym.setAttribute('aria-pressed','false');gym.textContent='Pantalla completa'}
gym.addEventListener('click',function(){var on=!caja.classList.contains('tmp-full');if(on){caja.classList.add('tmp-full');document.documentElement.classList.add('tmp-abierto');gym.setAttribute('aria-pressed','true');gym.textContent='Salir de pantalla completa';if(caja.requestFullscreen)caja.requestFullscreen().catch(function(){})}else{sal();if(document.fullscreenElement&&document.exitFullscreen)document.exitFullscreen().catch(function(){})}});
document.addEventListener('fullscreenchange',function(){if(!document.fullscreenElement&&caja.classList.contains('tmp-full'))sal()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&caja.classList.contains('tmp-full')&&!document.fullscreenElement)sal()});
var p=new URLSearchParams(location.search),ps=parseInt(p.get('s'),10);pon();if(ps>=5&&ps<=900){cfg.m='d';cfg.s=ps;pon();guarda()}
pinta();window.fbeTmp={estado:function(){return{est:est,fase:fase,queda:queda,ronda:ronda,series:series}}};
})();'''
tool_pagina('temporizador.html', 'Temporizador de descansos e intervalos',
    'Temporizador para el gimnasio: descanso entre series o intervalos de trabajo y descanso, con pantalla siempre encendida, sonido y vibración. Funciona sin conexión.',
    'El descanso, contado por ti',
    'Un temporizador grande para el gimnasio: descanso entre series o intervalos por rondas. Con aviso de sonido y vibración, y sin que se apague la pantalla.',
    TMP_FORM, TMP_RES,
    '''<p><b>Descanso entre series.</b> Elige el tiempo que marque tu plan, pulsa «Empezar» al soltar la barra y vuelve cuando suene. Lleva la cuenta de los descansos que has hecho. Si necesitas un poco más, «+15 s».</p>
<p><b>Intervalos.</b> Pon los segundos de trabajo, los de descanso y las rondas. Avisa en cada cambio y en los tres últimos segundos.</p>
<p><b>Pantalla encendida.</b> Mientras cuenta, el móvil no se bloquea (si tu navegador lo permite). En «Pantalla completa» los números se ven desde lejos.</p>
<p>No recomienda cuánto descansar: eso depende de tu plan y de tu objetivo. Si quieres que lo ajustemos a tu caso, lo vemos en la <a href="programas.html">asesoría</a>.</p>''',
    [], TMP_JS, slug='temporizador', tira=('Elige el descanso', 'Suelta la barra y pulsa', 'Vuelve cuando suene'))

# ---------------------------------------------------------------------------------------------
# 16. Mi semana activa (OMS 2020): registro de la semana, anillos, racha y doce semanas
_DIAS_S = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
_DIAS_L = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
SEM_FORM = (f'''<div class="sem-nav"><button type="button" id="s-ant" aria-label="Semana anterior">‹</button><p id="s-sem" aria-live="polite">Esta semana</p><button type="button" id="s-sig" aria-label="Semana siguiente">›</button></div>
<fieldset class="tool-campo sem-dias"><legend>Día</legend><div>{"".join(f'<label><input type="radio" name="s-dia" value="{i}"><span title="{_DIAS_L[i]}">{d}<span class="oculto"> ({_DIAS_L[i]})</span></span></label>' for i, d in enumerate(_DIAS_S))}</div></fieldset>'''
    + seg('s-tipo', 'Qué has hecho', [('m', 'Moderada'), ('v', 'Vigorosa'), ('f', 'Fuerza')], 'm', 'sem-tipo')
    + f'''{campo_num("s-min", "Minutos", 30, 5, 600, 5, "Moderada: puedes hablar, pero no cantar. Vigorosa: solo te salen frases cortas.", ud="min")}
<button type="button" class="sem-add" id="s-add">Añadir</button>
<ul class="sem-lista" id="s-lista" aria-label="Lo apuntado esta semana"></ul>
<p class="tool-nota">Se guarda solo en este dispositivo. La fuerza cuenta por días, no por minutos.</p>''')
SEM_RES = f'''<p class="tool-et">Tu semana, frente al mínimo de la OMS</p>
<div class="sem-anillos" aria-hidden="true"><svg viewBox="0 0 120 120"><circle class="an-p" cx="60" cy="60" r="50"/><circle class="an-a an-1" id="s-a1" cx="60" cy="60" r="50" pathLength="100" transform="rotate(-90 60 60)"/><circle class="an-p" cx="60" cy="60" r="36"/><circle class="an-a an-2" id="s-a2" cx="60" cy="60" r="36" pathLength="100" transform="rotate(-90 60 60)"/></svg></div>
<div class="res-grande"><b id="s-r">0</b><span>min equivalentes</span></div>
<ul class="sem-ley"><li class="k1"><b id="s-l1">0 de 150 min</b> de actividad aeróbica</li><li class="k2"><b id="s-l2">0 de 2 días</b> de fuerza</li></ul>
<p class="res-veredicto" id="s-tit"></p>
<p class="res-texto" id="s-txt"></p>
<p class="sem-racha" id="s-racha" hidden></p>
<div class="sem-12" id="s-12" hidden><p class="tool-et">Últimas doce semanas</p><div class="sem-barras" id="s-barras" role="img" aria-label=""></div></div>
{copiar_b("s-copiar", "Copiar mi semana")}'''
SEM_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},K='fbe-semana',D={},copia='',off=0,DL=['lunes','martes','miércoles','jueves','viernes','sábado','domingo'],MS=['ene','feb','mar','abr','may','jun','jul','ago','sept','oct','nov','dic'];
try{D=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){}
function lunes(d){var x=new Date(d.getFullYear(),d.getMonth(),d.getDate());x.setDate(x.getDate()-((x.getDay()+6)%7));return x}
function clave(d){return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
function sem(o){var l=lunes(new Date());l.setDate(l.getDate()+o*7);return l}
function suma(k){var L=D[k]||[],m=0,v=0,f={};L.forEach(function(e){if(e.t==='m')m+=e.n;else if(e.t==='v')v+=e.n;else f[e.d]=1});return{m:m,v:v,eq:m+2*v,f:Object.keys(f).length,n:L.length}}
function cumple(s){return s.eq>=150&&s.f>=2}
function guarda(){try{localStorage.setItem(K,JSON.stringify(D))}catch(e){}}
function pinta(){
  var l=sem(off),k=clave(l),s=suma(k),res=document.querySelector('.tool-res'),fin=new Date(l);fin.setDate(fin.getDate()+6);
  $('s-sem').textContent=off===0?'Esta semana':off===-1?'La semana pasada':'Semana del '+l.getDate()+' '+MS[l.getMonth()];$('s-sig').disabled=off>=0;
  var L=(D[k]||[]).slice().sort(function(a,b){return a.d-b.d});
  $('s-lista').innerHTML=L.length?L.map(function(e){var i=(D[k]||[]).indexOf(e);return '<li><span><b>'+DL[e.d]+'</b> · '+(e.t==='f'?'fuerza':(e.t==='m'?'moderada':'vigorosa')+', '+e.n+' min')+'</span><button type="button" data-i="'+i+'" aria-label="Quitar: '+DL[e.d]+', '+(e.t==='f'?'fuerza':e.n+' minutos')+'">×</button></li>'}).join(''):'<li class="sem-vacia">Todavía no has apuntado nada esta semana.</li>';
  $('s-r').textContent=fmt(s.eq);$('s-a1').style.strokeDashoffset=100-Math.min(100,s.eq/150*100);$('s-a2').style.strokeDashoffset=100-Math.min(100,s.f/2*100);
  $('s-l1').textContent=fmt(s.eq)+' de 150 min';$('s-l2').textContent=s.f+' de 2 días';
  res.classList.remove('z-alto','z-medio','z-bajo');var tit,txt;
  if(!s.n){tit='Apunta lo que vayas haciendo.';txt='Cada minuto vigoroso cuenta como dos moderados. El mínimo de la OMS para adultos: 150 minutos moderados a la semana (o 75 vigorosos) y fuerza al menos 2 días.'}
  else if(cumple(s)){res.classList.add('z-alto');tit='Semana cumplida';txt=s.eq>=300?'Has pasado de 300 minutos equivalentes: es la franja en la que la OMS sitúa beneficios adicionales.':'Llegas al mínimo de la OMS en aeróbico y en fuerza. Entre 150 y 300 minutos hay más beneficio todavía.'}
  else if(s.eq>=150||s.f>=2){res.classList.add('z-medio');tit=s.eq>=150?'Aeróbico cumplido; falta fuerza':'Fuerza cumplida; falta aeróbico';txt=s.eq>=150?'Te '+(2-s.f===1?'falta 1 día':'faltan 2 días')+' de fuerza para el mínimo de la OMS.':'Te faltan '+fmt(150-s.eq)+' minutos equivalentes para el mínimo. '+fmt(Math.ceil((150-s.eq)/2))+' si son vigorosos.'}
  else{res.classList.add(s.eq>=75||s.f>=1?'z-medio':'z-bajo');tit='Vas sumando';txt='Te faltan '+fmt(Math.max(0,150-s.eq))+' minutos equivalentes y '+(2-s.f===1?'1 día':(2-s.f)+' días')+' de fuerza. Algo de actividad siempre es mejor que nada, y más es mejor.'}
  $('s-tit').textContent=tit;$('s-txt').textContent=txt;
  var r=0,o=cumple(suma(clave(sem(0))))?0:-1;while(cumple(suma(clave(sem(o))))){r++;o--}
  $('s-racha').hidden=r<1;$('s-racha').textContent=r===1?'1 semana cumplida seguida':r+' semanas cumplidas seguidas';
  var hay=0,bs='',mx=300,et=[];for(var i=-11;i<=0;i++){var ss=suma(clave(sem(i)));if(ss.n)hay++;bs+='<i class="'+(cumple(ss)?'ok':'')+(i===off?' act':'')+'" style="--h:'+Math.min(100,ss.eq/mx*100).toFixed(1)+'%"><b></b>'+(ss.f?'<em>'+ss.f+'</em>':'')+'</i>';et.push(ss.eq)}
  $('s-12').hidden=hay<2;$('s-barras').innerHTML=bs+'<span class="sem-150"></span>';$('s-barras').setAttribute('aria-label','Minutos equivalentes de las últimas doce semanas: '+et.join(', ')+'. La línea marca 150.');
  $('s-copiar').hidden=!s.n;
  copia='Mi semana activa (FBE), semana del '+l.getDate()+' '+MS[l.getMonth()]+': '+fmt(s.eq)+' min equivalentes (mínimo de la OMS: 150) · fuerza '+s.f+(s.f===1?' día':' días')+' (mínimo: 2)\nModerada '+fmt(s.m)+' min · vigorosa '+fmt(s.v)+' min';
  try{window.dispatchEvent(new Event('fbe-semana'))}catch(e){}
}
$('s-add').addEventListener('click',function(){var k=clave(sem(off)),d=+document.querySelector('input[name="s-dia"]:checked').value,t=document.querySelector('input[name="s-tipo"]:checked').value,n=Math.max(5,Math.min(600,parseInt($('s-min').value,10)||0));D[k]=D[k]||[];
  if(t==='f'){if(D[k].some(function(e){return e.t==='f'&&e.d===d}))return pinta();D[k].push({d:d,t:'f',n:0})}else D[k].push({d:d,t:t,n:n});
  var ks=Object.keys(D).sort();while(ks.length>60)delete D[ks.shift()];guarda();pinta();destella($('s-r'))});
$('s-lista').addEventListener('click',function(e){var b=e.target.closest('button[data-i]');if(!b)return;var k=clave(sem(off));D[k].splice(+b.dataset.i,1);if(!D[k].length)delete D[k];guarda();pinta()});
$('s-ant').addEventListener('click',function(){if(off>-11){off--;pinta()}});$('s-sig').addEventListener('click',function(){if(off<0){off++;pinta()}});
function tipo(){$('s-min').closest('.tool-campo').hidden=document.querySelector('input[name="s-tipo"]:checked').value==='f'}
document.querySelector('.tool-form').addEventListener('change',tipo);
var hoy=(new Date().getDay()+6)%7;document.querySelector('input[name="s-dia"][value="'+hoy+'"]').checked=true;
$('s-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return $('s-copiar').hidden?'':copia};
tipo();pinta();
})();'''
tool_pagina('semana-activa.html', 'Mi semana activa',
    'Apunta tu actividad de la semana y mira con dos anillos si llegas al mínimo de la OMS: 150 minutos moderados (el vigoroso cuenta doble) y fuerza dos días. Con racha y tus últimas doce semanas.',
    'Tu semana, en dos anillos',
    'Apunta lo que haces cada día y mira de un vistazo si llegas al mínimo de la OMS: aeróbico y fuerza. Con tu racha de semanas cumplidas.',
    SEM_FORM, SEM_RES,
    '''<p>El <b>anillo de fuera</b> es la actividad aeróbica: la OMS recomienda a los adultos entre 150 y 300 minutos de actividad moderada a la semana, o entre 75 y 150 de vigorosa. Por eso cada minuto vigoroso cuenta aquí como dos: son tus «minutos equivalentes».</p>
<p>El <b>anillo de dentro</b> es la fuerza: al menos 2 días a la semana con ejercicios que trabajen los grandes grupos musculares.</p>
<p>La <b>racha</b> cuenta las semanas seguidas en las que cierras los dos anillos. Si esta semana aún no los has cerrado, la racha se mantiene hasta el domingo.</p>
<p>Si tienes 65 años o más, la OMS añade ejercicios de equilibrio y fuerza combinados al menos 3 días: lo tienes en <a href="actividad-oms.html">¿Llegas a lo mínimo de la OMS?</a></p>''',
    ['Bull FC y cols. World Health Organization 2020 guidelines on physical activity and sedentary behaviour. Br J Sports Med. 2020;54(24):1451-62.',
     'Organización Mundial de la Salud. Directrices de la OMS sobre actividad física y hábitos sedentarios. Ginebra: OMS; 2020.'],
    SEM_JS, slug='semana', tira=('Apunta lo que haces', 'El vigoroso cuenta doble', 'Fuerza, dos días'))

# ---------------------------------------------------------------------------------------------
# 17. Pasos al día (Paluch 2022) y cadencia (Tudor-Locke 2018)
PAS_FORM = (f'''<div class="tool-fila">{campo_num("p-edad", "Edad", 45, 18, 95, 1, ud="años")}{campo_num("p-pasos", "Pasos al día, de media", 5000, 0, 40000, 500, "Mira la media de la última semana en tu móvil o tu reloj.")}</div>
<div class="pas-cad"><p class="tool-et">¿A qué ritmo andas?</p><p class="tool-nota">Camina a tu paso de «voy con algo de prisa» y toca el botón a cada paso, al menos diez veces.</p>
<button type="button" class="pas-toca" id="p-toca">Toca a cada paso</button>
<p class="pas-cad-r" id="p-cad" aria-live="polite">Sin medir</p><button type="button" class="pas-borra" id="p-borra" hidden>Medir otra vez</button></div>''')
PAS_RES = f'''<p class="tool-et">Tus pasos al día</p>
<div class="res-grande"><b id="p-r">–</b><span>pasos al día</span></div>
<p class="res-chip" id="p-cat" hidden></p>
<div class="pas-escala" aria-hidden="true"><i class="pas-franja" id="p-fr"></i><i class="pas-marca" id="p-m"></i><span class="pas-e0">0</span><span class="pas-e1">12.000</span></div>
<p class="res-veredicto" id="p-tit"></p>
<p class="res-texto" id="p-txt"></p>
<p class="res-texto pas-cad-t" id="p-ctx" hidden></p>
{copiar_b("p-copiar", "Copiar resultado")}'''
PAS_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},copia='',ts=[],cad=0;
function num(id){var x=parseFloat(String($(id).value).replace(',','.'));return isNaN(x)?null:x}
function pinta(){
  var e=num('p-edad'),p=num('p-pasos'),res=document.querySelector('.tool-res');res.classList.remove('z-alto','z-medio','z-bajo');
  if(!e||e<18||p===null||p<0){$('p-r').textContent='–';$('p-cat').hidden=true;$('p-tit').textContent='Escribe tu edad y tus pasos de media.';$('p-txt').textContent='';$('p-copiar').hidden=true;return}
  var a=e>=60?6000:8000,b=e>=60?8000:10000,gr=e>=60?'60 años o más':'menos de 60 años';
  $('p-r').textContent=fmt(p);destella($('p-r'));$('p-fr').style.left=(a/12000*100)+'%';$('p-fr').style.width=((b-a)/12000*100)+'%';$('p-m').style.left=Math.min(100,p/12000*100)+'%';
  var tit,txt,cat;
  if(p>=a){res.classList.add('z-alto');cat=p>b?'Por encima de '+fmt(b):'Dentro de '+fmt(a)+'-'+fmt(b);tit='Estás en la franja de tu edad';txt='En el metaanálisis, el riesgo de muerte bajaba con cada paso de más hasta los '+fmt(a)+'-'+fmt(b)+' pasos al día en personas de '+gr+'. A partir de ahí, la curva se aplana: más pasos no hacen daño, pero suman poco.'}
  else{res.classList.add('z-medio');cat='Por debajo de '+fmt(a);var sig=Math.min(a,Math.ceil((p+1000)/500)*500);tit='Cada paso de más cuenta';txt='Con '+gr+', el beneficio sigue creciendo hasta los '+fmt(a)+'-'+fmt(b)+' pasos al día. No hace falta llegar de golpe: tu siguiente objetivo, '+fmt(sig)+'. Mil pasos son unos 10 minutos andando a buen ritmo.'}
  $('p-cat').hidden=false;$('p-cat').textContent=cat;$('p-tit').textContent=tit;$('p-txt').textContent=txt;$('p-copiar').hidden=false;
  $('p-ctx').hidden=!cad;if(cad)$('p-ctx').textContent=cad>=100?'Tu ritmo, '+cad+' pasos por minuto: a partir de 100, andar ya cuenta como actividad moderada.':'Tu ritmo, '+cad+' pasos por minuto: por debajo de 100, que es el ritmo que suele corresponder a una intensidad moderada.';
  copia='Pasos al día (FBE): '+fmt(p)+' · '+cat+' (franja para '+gr+': '+fmt(a)+'-'+fmt(b)+', Paluch 2022)'+(cad?'\nCadencia: '+cad+' pasos/min':'');
}
$('p-toca').addEventListener('click',function(){var t=performance.now();if(ts.length&&t-ts[ts.length-1]>3000)ts=[];ts.push(t);if(ts.length>24)ts.shift();
  if(ts.length>=10){var d=[];for(var i=1;i<ts.length;i++)d.push(ts[i]-ts[i-1]);d.sort(function(a,b){return a-b});var md=d[Math.floor(d.length/2)];cad=Math.round(60000/md);$('p-cad').textContent=cad+' pasos por minuto';$('p-borra').hidden=false;pinta()}
  else $('p-cad').textContent='Sigue: '+ts.length+' de 10';});
$('p-borra').addEventListener('click',function(){ts=[];cad=0;$('p-cad').textContent='Sin medir';this.hidden=true;pinta()});
$('p-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return $('p-copiar').hidden?'':copia};
document.querySelector('.tool-form').addEventListener('input',pinta);pinta();
})();'''
tool_pagina('pasos.html', 'Pasos al día: cuántos necesitas',
    'Cuántos pasos al día necesitas según tu edad, con el metaanálisis de 15 cohortes: de 6.000 a 8.000 con 60 años o más y de 8.000 a 10.000 con menos de 60. Y mide a qué ritmo andas.',
    '¿Cuántos pasos necesitas de verdad?',
    'No son 10.000 para todo el mundo. Mira la franja que corresponde a tu edad según el mayor estudio sobre pasos y mortalidad, y comprueba si andas a ritmo de actividad moderada.',
    PAS_FORM, PAS_RES,
    '''<p>El número sale de un <b>metaanálisis de 15 cohortes</b> con más de 47.000 adultos seguidos unos 7 años. Cuantos más pasos, menos riesgo de muerte por cualquier causa, pero solo hasta un punto: de <b>6.000 a 8.000 pasos</b> al día en personas de 60 años o más, y de <b>8.000 a 10.000</b> en menores de 60. Más allá, la curva se aplana.</p>
<p>Es un estudio de observación: dice que quien más anda vive más, no demuestra que sea solo por andar. Aun así, es la mejor estimación que hay hoy, y coincide en las 15 cohortes que reúne.</p>
<p>El <b>ritmo</b> también cuenta. Andar a <b>100 pasos por minuto o más</b> suele corresponder a una intensidad moderada, la que piden las recomendaciones de actividad física. Por eso mil pasos a ese ritmo son unos 10 minutos de actividad moderada.</p>
<p>Los pasos no sustituyen a la fuerza: la OMS pide además dos días de fuerza a la semana. Lo tienes en <a href="semana-activa.html">Mi semana activa</a>.</p>''',
    ['Paluch AE y cols. Daily steps and all-cause mortality: a meta-analysis of 15 international cohorts. Lancet Public Health. 2022;7(3):e219-e228.',
     'Tudor-Locke C y cols. How fast is fast enough? Walking cadence (steps/min) as a practical estimate of intensity in adults: a narrative review. Br J Sports Med. 2018;52(12):776-788.'],
    PAS_JS, slug='pasos', tira=('Mira tu media', 'Tu franja por edad', 'A buen ritmo'))

# ---------------------------------------------------------------------------------------------
# 18. Tensión en casa: tu semana de tomas (guía ESC 2024)
TEN_FORM = (seg('x-mom', 'Momento', [('m', 'Mañana'), ('n', 'Tarde-noche')], 'm', 'ten-mom')
    + f'''<div class="ten-tomas"><p class="tool-et">Primera toma</p><div class="tool-fila">{campo_num("x-s1", "Alta (sistólica)", "", 60, 260, 1, ud="mmHg")}{campo_num("x-d1", "Baja (diastólica)", "", 30, 160, 1, ud="mmHg")}</div>
<p class="tool-et">Segunda toma, 1 o 2 minutos después</p><div class="tool-fila">{campo_num("x-s2", "Alta (sistólica)", "", 60, 260, 1, ud="mmHg")}{campo_num("x-d2", "Baja (diastólica)", "", 30, 160, 1, ud="mmHg")}</div></div>
<p class="tool-aviso" id="x-err" role="alert" hidden></p>
<button type="button" class="sem-add" id="x-add">Apuntar estas tomas</button>
<details class="rev-det"><summary>Cómo medirte bien</summary><ul class="ten-como"><li>Sentado 5 minutos antes, en una habitación tranquila, con la espalda y el brazo apoyados.</li><li>Sin ejercicio, café ni tabaco en los 30 minutos de antes. Con la vejiga vacía.</li><li>Por la mañana, antes de desayunar y de tomar la medicación, pero no nada más despertarte. Y otra vez por la tarde o la noche.</li><li>Dos tomas cada vez, separadas 1 o 2 minutos.</li><li>Al menos 3 días seguidos; lo ideal, 7. A la misma hora.</li></ul></details>
<ul class="sem-lista ten-lista" id="x-lista" aria-label="Tomas apuntadas"></ul>
<p class="tool-nota">Se guarda solo en este dispositivo. No sustituye a tu médico: es para que llegues a su consulta con las tomas apuntadas.</p>''')
TEN_RES = f'''<p class="tool-et" id="x-et">Tu media en casa</p>
<div class="res-grande"><b id="x-r">–</b><span>mmHg</span></div>
<p class="res-chip" id="x-cat" hidden></p>
<p class="ten-prog" id="x-prog"></p>
<p class="res-veredicto" id="x-tit"></p>
<p class="res-texto" id="x-txt"></p>
<p class="ten-alerta" id="x-alerta" role="alert" hidden></p>
<div class="ten-bot">{copiar_b("x-copiar", "Copiar para mi médico")}<button type="button" class="copiar-t" id="x-impr" hidden><span>Imprimir la hoja</span></button><button type="button" class="copiar-t ten-nueva" id="x-nueva" hidden><span>Empezar otra semana</span></button></div>'''
TEN_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},K='fbe-tension',L=[],copia='',MS=['ene','feb','mar','abr','may','jun','jul','ago','sept','oct','nov','dic'];
try{L=JSON.parse(localStorage.getItem(K)||'[]')||[]}catch(e){}if(!Array.isArray(L))L=[];
function guarda(){try{localStorage.setItem(K,JSON.stringify(L))}catch(e){}}
function dia(t){var d=new Date(t);return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
function fecha(k){var p=k.split('-');return (+p[2])+' '+MS[+p[1]-1]}
function tanda(){if(!L.length)return[];var ult=Math.max.apply(null,L.map(function(x){return x.t})),lim=ult-7*864e5;return L.filter(function(x){return x.t>lim})}
function pinta(){
  var T=tanda(),res=document.querySelector('.tool-res');res.classList.remove('z-alto','z-medio','z-bajo');
  var dias={};T.forEach(function(x){(dias[dia(x.t)]=dias[dia(x.t)]||[]).push(x)});var ks=Object.keys(dias).sort(),nd=ks.length;
  $('x-lista').innerHTML=T.length?ks.slice().reverse().map(function(k){return '<li class="ten-dia"><span><b>'+fecha(k)+'</b> · '+dias[k].sort(function(a,b){return a.t-b.t}).map(function(x){return (x.m==='m'?'mañana ':'tarde ')+x.s+'/'+x.d}).join(' · ')+'</span><button type="button" data-k="'+k+'" aria-label="Quitar las tomas del '+fecha(k)+'">×</button></li>'}).join(''):'<li class="sem-vacia">Todavía no has apuntado ninguna toma.</li>';
  $('x-copiar').hidden=$('x-impr').hidden=$('x-nueva').hidden=!T.length;
  if(!T.length){$('x-r').textContent='–';$('x-cat').hidden=true;$('x-prog').textContent='';$('x-tit').textContent='Apunta tus tomas de la mañana y de la tarde-noche.';$('x-txt').textContent='Con 3 días ya hay una media orientativa; lo ideal son 7.';$('x-alerta').hidden=true;return}
  var s=Math.round(T.reduce(function(a,x){return a+x.s},0)/T.length),d=Math.round(T.reduce(function(a,x){return a+x.d},0)/T.length);
  $('x-r').textContent=s+'/'+d;destella($('x-r'));
  $('x-prog').textContent=nd+(nd===1?' día':' días')+' con tomas · '+T.length+' tomas'+(nd<3?' · faltan '+(3-nd)+(3-nd===1?' día':' días')+' para el mínimo':nd<7?' · lo ideal, 7 días':'');
  var cat,tit,txt;
  if(nd<3){cat='Media provisional';tit='Sigue apuntando';txt='La guía europea pide al menos 3 días de tomas, mañana y tarde-noche, para dar una media por buena. De momento es solo orientativa.'}
  else if(s>=135||d>=85){res.classList.add('z-bajo');cat='135/85 o más';tit='En el umbral de hipertensión';txt='Una media en casa de 135/85 o más es el umbral que la guía europea usa para la hipertensión. El diagnóstico y el tratamiento los decide tu médico: llévale estas tomas.'}
  else if(s>=120||d>=70){res.classList.add('z-medio');cat='De 120/70 a 134/84';tit='Tensión elevada';txt='Entre 120/70 y 134/84 de media en casa, la guía europea habla de «tensión elevada»: no es hipertensión, pero conviene comentarlo con tu médico, sobre todo si tienes otros factores de riesgo.'}
  else{res.classList.add('z-alto');cat='Por debajo de 120/70';tit='Tensión no elevada';txt='Una media en casa por debajo de 120/70 es lo que la guía europea considera tensión no elevada.'}
  if(nd>=3&&nd<7&&((s>=130&&s<140)||(d>=80&&d<90)))txt+=' Tu media queda cerca del umbral: la guía recomienda completar los 7 días.';
  $('x-cat').hidden=false;$('x-cat').textContent=cat;$('x-tit').textContent=tit;$('x-txt').textContent=txt;
  var alta=T.some(function(x){return x.s>=180||x.d>=110});$('x-alerta').hidden=!alta;
  if(alta)$('x-alerta').textContent='Tienes alguna toma de 180/110 o más. Repítela tras 5 minutos sentado. Si se mantiene, consulta hoy con un médico. Y si además hay dolor en el pecho, falta de aire, dolor de cabeza intenso, visión borrosa, debilidad o dificultad para hablar, llama al 112.';
  copia='Tensión en casa (FBE). Media de '+T.length+' tomas en '+nd+(nd===1?' día':' días')+': '+s+'/'+d+' mmHg'+(nd>=3?' · '+tit:' (provisional)')+'\n'+ks.map(function(k){return fecha(k)+': '+dias[k].map(function(x){return (x.m==='m'?'mañana ':'tarde ')+x.s+'/'+x.d}).join(', ')}).join('\n')+'\nUmbrales en casa de la guía ESC 2024: menos de 120/70, no elevada; de 120/70 a 134/84, elevada; 135/85 o más, hipertensión.';
}
function val(id){var x=parseInt($(id).value,10);return isNaN(x)?null:x}
$('x-add').addEventListener('click',function(){var m=document.querySelector('input[name="x-mom"]:checked').value,P=[[val('x-s1'),val('x-d1')],[val('x-s2'),val('x-d2')]].filter(function(p){return p[0]!==null||p[1]!==null}),err='';
  if(!P.length)err='Escribe al menos la primera toma.';
  P.forEach(function(p){if(p[0]===null||p[1]===null)err='A cada toma le hacen falta las dos cifras.';else if(p[0]<60||p[0]>260||p[1]<30||p[1]>160)err='Revisa las cifras: la alta suele estar entre 60 y 260, y la baja, entre 30 y 160.';else if(p[1]>=p[0])err='La alta tiene que ser mayor que la baja.'});
  $('x-err').hidden=!err;$('x-err').textContent=err;if(err)return;
  var t=Date.now();P.forEach(function(p,i){L.push({t:t+i,m:m,s:p[0],d:p[1]})});L=L.slice(-120);guarda();['x-s1','x-d1','x-s2','x-d2'].forEach(function(i){$(i).value=''});
  var o=document.querySelector('input[name="x-mom"][value="'+(m==='m'?'n':'m')+'"]');if(o)o.checked=true;pinta()});
$('x-lista').addEventListener('click',function(e){var b=e.target.closest('button[data-k]');if(!b)return;L=L.filter(function(x){return dia(x.t)!==b.dataset.k});guarda();pinta()});
$('x-nueva').addEventListener('click',function(){if(this.dataset.seguro){L=[];guarda();delete this.dataset.seguro;this.querySelector('span').textContent='Empezar otra semana';pinta()}else{this.dataset.seguro='1';this.querySelector('span').textContent='Pulsa otra vez para borrar las tomas';var b=this;setTimeout(function(){delete b.dataset.seguro;b.querySelector('span').textContent='Empezar otra semana'},4000)}});
$('x-impr').addEventListener('click',function(){window.print()});
$('x-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return $('x-copiar').hidden?'':copia};
if(new Date().getHours()>=14){var n=document.querySelector('input[name="x-mom"][value="n"]');if(n)n.checked=true}
pinta();
})();'''
tool_pagina('tension.html', 'Tensión en casa: tu semana de tomas',
    'Apunta tus tomas de tensión en casa como pide la guía europea (ESC 2024): mañana y tarde-noche, dos tomas, de 3 a 7 días. Calcula tu media, la compara con los umbrales y prepara la hoja para tu médico.',
    'Tu tensión, la de mañana por la mañana',
    'La tensión que cuenta es la de reposo, día tras día. Apunta tus tomas como pide la guía europea, mira tu media y llévasela a tu médico.',
    TEN_FORM, TEN_RES,
    f'''<p>Una toma suelta dice poco: la tensión cambia de un minuto a otro. Por eso la <b>guía europea de 2024</b> pide medirla en casa <b>dos veces al día</b> (mañana y tarde-noche), con <b>dos tomas cada vez</b>, durante <b>3 a 7 días</b>, y hacer la media de todas.</p>
<p>Con esa media en casa, la guía distingue tres tramos: <b>menos de 120/70</b>, tensión no elevada; <b>de 120/70 a 134/84</b>, tensión elevada; y <b>135/85 o más</b>, el umbral de hipertensión (equivale a 140/90 en la consulta). Basta con que una de las dos cifras llegue al tramo.</p>
<p>Si alguna toma sale en <b>180/110 o más</b>, la guía pide descartar una emergencia: repítela en reposo y consulta.</p>
<p>¿Y entrenar con la tensión alta? Lo explico en el vídeo <a href="videos.html#v-9Dy_ncFGwK8">«Tengo la tensión alta: ¿puedo levantar pesas?»</a>, con el semáforo de cuándo entrenar y cuándo no. Y si tomas medicación para la tensión, <a href="pauta-activa.html">Pauta Activa</a> te dice qué tener en cuenta.</p>''',
    ['McEvoy JW y cols. 2024 ESC Guidelines for the management of elevated blood pressure and hypertension. Eur Heart J. 2024;45(38):3912-4018 (umbrales en casa, tabla 5; cómo medirse, apartado 5.2.3).'],
    TEN_JS, slug='tension', tira=('Cinco minutos sentado', 'Dos tomas cada vez', 'Mañana y tarde-noche'))

# ---------------------------------------------------------------------------------------------
# 19. Equilibrio a una pierna, 10 segundos (Araujo 2022)
EQ_FORM = (f'''<p class="tool-aviso">Hazlo cerca de una pared o de una silla firme, y mejor con alguien al lado. Si te mareas o tienes una lesión reciente, no lo hagas.</p>
<ol class="eq-pasos"><li>De pie, apoya el empeine del pie libre en la parte de atrás de la otra pierna.</li><li>Brazos pegados al cuerpo y la mirada al frente.</li><li>Aguanta 10 segundos sin mover el pie de apoyo ni soltar el otro.</li><li>Tienes hasta tres intentos, con la pierna que quieras.</li></ol>
<div class="eq-ctl"><button type="button" class="sem-add" id="e-ir">Empezar (cuenta atrás de 3)</button><button type="button" class="eq-fallo" id="e-fallo" hidden>He apoyado el pie</button></div>
<p class="eq-int" id="e-int" aria-live="polite">Intento 1 de 3</p>
<button type="button" class="pas-borra" id="e-cero" hidden>Empezar de nuevo</button>''')
EQ_RES = f'''<p class="tool-et">Equilibrio a una pierna</p>
<div class="tmp-reloj eq-reloj"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="tmp-pista" cx="60" cy="60" r="52"/><circle class="tmp-arco" id="e-arco" cx="60" cy="60" r="52" pathLength="100" transform="rotate(-90 60 60)"/></svg><div class="tmp-num"><b id="e-num" role="timer">10</b><span id="e-fase">segundos</span></div></div>
<div class="res-grande eq-grande" hidden><b id="e-r">–</b><span>segundos</span></div>
<p class="res-chip" id="e-cat" hidden></p>
<p class="res-veredicto" id="e-tit">Lee los pasos y pulsa «Empezar».</p>
<p class="res-texto" id="e-txt"></p>
<p class="oculto" id="e-voz" aria-live="assertive"></p>
{copiar_b("e-copiar", "Copiar resultado")}'''
EQ_JS = r'''(function(){
var $=function(i){return document.getElementById(i)},est='listo',n=1,ini=0,tic=0,mejor=0,copia='',ac=null,res=document.querySelector('.tool-res');
function pita(f,d){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();if(ac.state==='suspended')ac.resume();var o=ac.createOscillator(),g=ac.createGain(),t=ac.currentTime;o.frequency.value=f;o.connect(g);g.connect(ac.destination);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.3,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.start(t);o.stop(t+d+.03)}catch(e){}}
function fin(ok,seg){clearInterval(tic);tic=0;mejor=Math.max(mejor,seg);$('e-fallo').hidden=true;
  if(ok){est='hecho';res.classList.add('z-alto');$('e-r').textContent='10';$('e-cat').hidden=false;$('e-cat').textContent='Conseguido'+(n>1?' al intento '+n:'');$('e-tit').textContent='Diez segundos a una pierna';$('e-txt').textContent='En el estudio, 8 de cada 10 personas de 51 a 75 años lo consiguieron. Repítelo cada pocos meses: el equilibrio empeora deprisa a partir de mediados de los 50, y se entrena.';$('e-ir').hidden=true;$('e-int').textContent='';pita(1320,.6);if(navigator.vibrate)try{navigator.vibrate([200,100,200])}catch(e){}}
  else if(n>=3){est='hecho';res.classList.add('z-bajo');$('e-r').textContent=fmt(mejor,1);$('e-cat').hidden=false;$('e-cat').textContent='No completado en tres intentos';$('e-tit').textContent='Una señal para trabajar el equilibrio';$('e-txt').textContent='En el estudio, no completar los 10 segundos se asoció a más riesgo de muerte en los 7 años siguientes, también tras tener en cuenta la edad, el sexo, el peso y las enfermedades. Es una asociación, no una condena: la fuerza y el equilibrio se entrenan a cualquier edad. Coméntalo con tu médico si además te has caído en el último año.';$('e-ir').hidden=true;$('e-int').textContent=''}
  else{est='listo';n++;$('e-int').textContent='Intento '+n+' de 3 · has aguantado '+fmt(seg,1)+' s';$('e-ir').textContent='Otro intento (cuenta atrás de 3)';$('e-ir').hidden=false;$('e-num').textContent='10';$('e-arco').style.strokeDashoffset=0;$('e-tit').textContent='Descansa un momento y prueba otra vez.';return}
  $('e-cero').hidden=false;document.querySelector('.eq-grande').hidden=false;$('e-copiar').hidden=false;$('e-voz').textContent=$('e-tit').textContent;
  copia='Equilibrio a una pierna (FBE): '+(ok?'10 segundos conseguidos'+(n>1?' al intento '+n:''):'no completado en tres intentos (mejor: '+fmt(mejor,1)+' s)')+' · prueba de Araujo 2022';
}
function corre(){est='corre';ini=performance.now();$('e-fallo').hidden=false;$('e-tit').textContent='Aguanta…';pita(1100,.2);tic=setInterval(function(){var s=(performance.now()-ini)/1000;$('e-num').textContent=Math.max(0,Math.ceil(10-s));$('e-arco').style.strokeDashoffset=Math.min(100,s*10);if(s>=10)fin(true,10)},100)}
$('e-ir').addEventListener('click',function(){if(est!=='listo')return;est='prep';this.hidden=true;var c=3;$('e-num').textContent=c;$('e-fase').textContent='prepárate';$('e-tit').textContent='Colócate…';pita(660,.12);
  tic=setInterval(function(){c--;if(c>0){$('e-num').textContent=c;pita(660,.12)}else{clearInterval(tic);$('e-fase').textContent='segundos';$('e-num').textContent='10';corre()}},1000)});
$('e-fallo').addEventListener('click',function(){if(est==='corre')fin(false,Math.round((performance.now()-ini)/100)/10)});
$('e-cero').addEventListener('click',function(){clearInterval(tic);est='listo';n=1;mejor=0;copia='';res.classList.remove('z-alto','z-bajo');this.hidden=true;$('e-ir').hidden=false;$('e-ir').textContent='Empezar (cuenta atrás de 3)';$('e-int').textContent='Intento 1 de 3';$('e-cat').hidden=true;$('e-copiar').hidden=true;document.querySelector('.eq-grande').hidden=true;$('e-num').textContent='10';$('e-arco').style.strokeDashoffset=0;$('e-tit').textContent='Lee los pasos y pulsa «Empezar».';$('e-txt').textContent=''});
$('e-copiar').addEventListener('click',function(){copiar(this,copia)});window.fbeCopia=function(){return copia};
})();'''
tool_pagina('equilibrio.html', 'Equilibrio a una pierna: la prueba de los 10 segundos',
    'La prueba de equilibrio de 10 segundos a una pierna, con cronómetro. En un estudio con 1.702 personas de 51 a 75 años, no completarla se asoció a más riesgo de muerte en los 7 años siguientes.',
    '¿Aguantas 10 segundos a una pierna?',
    'Una prueba de diez segundos, sin material. En un estudio con 1.702 personas de 51 a 75 años, una de cada cinco no la completó, y eso se asoció a peor pronóstico.',
    EQ_FORM, EQ_RES,
    '''<p>La prueba viene de un estudio de la clínica CLINIMEX (Río de Janeiro) con <b>1.702 personas de 51 a 75 años</b>, seguidas unos 7 años. Tenían hasta tres intentos para aguantar 10 segundos sobre una pierna.</p>
<p>Un <b>20,4 %</b> no lo consiguió. En ese grupo, el riesgo de muerte por cualquier causa fue más alto (<b>1,84 veces</b>) después de ajustar por edad, sexo, índice de masa corporal y enfermedades.</p>
<p>Es un estudio de observación: el equilibrio no es la causa, sino una señal del estado general (fuerza, sistema nervioso, actividad). Y no incluyó a personas de menos de 51 ni de más de 75 años, así que fuera de esas edades la cifra no se aplica igual.</p>
<p>Si no te sale, es una razón para entrenar fuerza y equilibrio, no para asustarse. Para una valoración más completa en mayores, tienes el <a href="test-sppb.html">test SPPB</a>.</p>''',
    ['Araujo CG y cols. Successful 10-second one-legged stance performance predicts survival in middle-aged and older individuals. Br J Sports Med. 2022;56(17):975-980.'],
    EQ_JS, slug='equilibrio', tira=('Cerca de una pared', 'El empeine, detrás', 'Diez segundos'))

HERR_MAS += [('temporizador.html', 'temporizador', 'crono', 'Temporizador de descansos', 'Descanso entre series o intervalos, con sonido, vibración y la pantalla siempre encendida.'),
    ('semana-activa.html', 'semana', 'anillos', 'Mi semana activa', 'Apunta tu semana y cierra los dos anillos de la OMS: aeróbico y fuerza. Con racha.'),
    ('pasos.html', 'pasos', 'pasos', 'Pasos al día', 'Cuántos pasos necesitas según tu edad, y a qué ritmo andas.'),
    ('tension.html', 'tension', 'tension', 'Tensión en casa', 'Tu semana de tomas como pide la guía europea, con tu media y la hoja para tu médico.'),
    ('equilibrio.html', 'equilibrio', 'equilibrio', 'Equilibrio a una pierna', 'La prueba de los 10 segundos, con cronómetro y lo que dice el estudio.')]
SEC_PAGS_H4 = ['temporizador.html', 'semana-activa.html', 'pasos.html', 'tension.html', 'equilibrio.html']  # entran en el sitemap desde extras.py
