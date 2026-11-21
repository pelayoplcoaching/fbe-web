# «Mi evolución» e «Informe para tu médico» en Mis resultados (21/11/2026, noche). Lo ejecuta interior.py después de autoria.py.
# Desde esta fecha, «Guardar en Mis resultados» guarda también la cifra grande del resultado (v, su texto vt y su unidad u),
# la zona (z: alto, medio o bajo, con su titular en zt) y, en el 1RM, el ejercicio (s). Con dos o más cifras de una
# herramienta (o de un ejercicio) sale su gráfica. Todo sigue en el navegador: nada se envía.
# Gráfica: una serie (sin leyenda; el título dice qué es), línea de 2 px, puntos de 8 px con anillo del color del fondo,
# rejilla fina, la última cifra rotulada y la primera y la última fecha. Al pasar el ratón o el dedo, o con las flechas del
# teclado, una línea vertical y una etiqueta con la fecha, la cifra y la zona. Debajo, «Ver en tabla».
# m: 1 si subir es mejorar, -1 si bajar es mejorar, 0 si ninguna de las dos (entonces el cambio no lleva color).
# min: por debajo de esa cifra, bajar ya no es mejorar (cintura/altura < 0,4 no es el rango saludable de NICE).
# du: cómo se nombra la unidad en el cambio (singular, plural) cuando la de la herramienta no sirve («+2 de 12»).
# Las zonas de pulso no entran: su cifra (la FC máxima) solo cambia con la edad.
EVO_CFG = {'test-silla.html': {'m': 1, 'du': ['vez', 'veces']}, 'calculadora-1rm.html': {'m': 1}, 'prension.html': {'m': 1},
           'test-sppb.html': {'m': 1, 'du': ['punto', 'puntos']}, 'actividad-oms.html': {'m': 1},
           'cintura-altura.html': {'m': -1, 'min': 0.4}, 'calorias.html': {'m': 0}, 'cafeina.html': {'m': 0}}
# Fuentes de cada herramienta para el informe (las de su lista «De dónde salen los números», desde fuentes.json)
EVO_FU = {}
for _f in FU_L:
    for _u, _et in FU_USO[_f['id']]:
        _k = _u.split('#')[0]
        if _k in HM or _k in ('test-silla.html', 'calculadora-1rm.html', 'volumen-semanal.html', 'cafeina.html', 'revision-medica.html'):
            _c = f'{_f["au"]} {_f["ti"]}. {_f["rev"]}.'
            if _c not in EVO_FU.setdefault(_k, []):
                EVO_FU[_k].append(_c)
EVO_JS = r"""(function(){var K='fbe-resultados',D=document,E=D.getElementById('mr-evo'),G=D.getElementById('mr-evo-rej'),L=D.getElementById('mr-lista');if(!E||!G||!L)return;
var CFG=__CFG__,FU=__FU__,R=[];
function lee(){try{var o=JSON.parse(localStorage.getItem(K)||'{}');return o&&typeof o==='object'?o:{}}catch(e){return {}}}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function p2(x){return (x<10?'0':'')+x}
function dm(t){var d=new Date(t||0);return p2(d.getDate())+'/'+p2(d.getMonth()+1)+'/'+d.getFullYear()}
function nf(x,n){return Number(x).toLocaleString('es-ES',{minimumFractionDigits:n,maximumFractionDigits:n})}
function decs(s){var m=String(s||'').match(/,(\d+)/);return m?Math.min(2,m[1].length):0}
function series(h){var g={};(h||[]).forEach(function(e){if(e&&typeof e.v==='number'&&isFinite(e.v)){var s=e.s||'';(g[s]=g[s]||[]).push(e)}});Object.keys(g).forEach(function(s){g[s].sort(function(a,b){return (a.t||0)-(b.t||0)})});return g}
function marcas(a,b){if(a===b){var d=Math.abs(a)*.1||1;a-=d;b+=d}var r=b-a,st=Math.pow(10,Math.floor(Math.log(r/2)/Math.LN10)),q=(r/2)/st;if(q>=5)st*=5;else if(q>=2)st*=2;var lo=Math.floor(a/st+1e-9)*st,hi=Math.ceil(b/st-1e-9)*st,t=[];for(var v=lo;v<=hi+st/2;v+=st)t.push(+v.toFixed(6));return {t:t,d:st<1?Math.min(2,Math.round(-Math.log(st)/Math.LN10+.499)):0}}
function val(e,u){return (e.vt||nf(e.v,decs(e.vt)))+(u?' '+u:'')}
function cfg(k){var c=CFG[k];return c&&typeof c==='object'?c:{m:0}}
function grafica(s,n,inter){var W=320,H=158,ml=42,mr=52,mt=16,mb=28,iw=W-ml-mr,ih=H-mt-mb,vs=s.map(function(e){return e.v}),m=marcas(Math.min.apply(0,vs),Math.max.apply(0,vs)),y0=m.t[0],y1=m.t[m.t.length-1],t0=s[0].t||0,t1=s[s.length-1].t||0,porT=(t1-t0)>432e5,mismoA=new Date(t0).getFullYear()===new Date(t1).getFullYear();
  function X(e,i){return ml+(porT?((e.t||0)-t0)/(t1-t0):(s.length>1?i/(s.length-1):.5))*iw}
  function Y(v){return mt+ih-(v-y0)/((y1-y0)||1)*ih}
  function fx(t){var d=new Date(t||0);return d.getDate()+'/'+(d.getMonth()+1)+(mismoA?'':'/'+String(d.getFullYear()).slice(2))}
  var P=s.map(function(e,i){return [+X(e,i).toFixed(1),+Y(e.v).toFixed(1)]}),lp=P[P.length-1],ul=s[s.length-1];
  var g=m.t.map(function(v){var y=Y(v).toFixed(1);return '<line class="evo-g" x1="'+ml+'" x2="'+(W-mr+8)+'" y1="'+y+'" y2="'+y+'"/><text class="evo-ty" x="'+(ml-8)+'" y="'+y+'" dy=".34em">'+nf(v,m.d)+'</text>'}).join('');
  var d=P.map(function(p,i){return (i?'L':'M')+p[0]+' '+p[1]}).join(''),a=d+'L'+lp[0]+' '+(mt+ih)+'L'+P[0][0]+' '+(mt+ih)+'Z';
  var pt=P.map(function(p,i){return '<circle class="evo-p" data-i="'+i+'" cx="'+p[0]+'" cy="'+p[1]+'" r="4"/>'}).join('');
  var et=inter?' aria-hidden="true"':' role="img" aria-label="'+esc('Evolución: '+s.length+' resultados, del '+dm(t0)+' al '+dm(t1))+'"';
  return {W:W,H:H,P:P,svg:'<svg class="evo-svg" viewBox="0 0 '+W+' '+H+'" focusable="false"'+et+'>'+g+'<line class="evo-x" x1="0" x2="0" y1="'+(mt-6)+'" y2="'+(mt+ih)+'"/><path class="evo-a" d="'+a+'"/><path class="evo-l" d="'+d+'"/>'+pt
    +'<text class="evo-lab" x="'+(lp[0]+10)+'" y="'+lp[1]+'" dy=".34em">'+esc(ul.vt&&!/[–-]/.test(ul.vt)?ul.vt:nf(ul.v,n))+'</text>'
    +'<text class="evo-tx" x="'+P[0][0]+'" y="'+(H-8)+'" text-anchor="start">'+fx(t0)+'</text><text class="evo-tx" x="'+lp[0]+'" y="'+(H-8)+'" text-anchor="end">'+fx(t1)+'</text></svg>'}}
function tabla(s,u){var zt=s.some(function(e){return e.zt});return '<table><thead><tr><th scope="col">Fecha</th><th scope="col">Resultado</th>'+(zt?'<th scope="col">Zona</th>':'')+'</tr></thead><tbody>'+s.slice().reverse().map(function(e){return '<tr><td>'+dm(e.t)+'</td><td>'+esc(val(e,u))+'</td>'+(zt?'<td>'+(e.zt?'<span class="evo-zt z-'+esc(e.z||'')+'"><i aria-hidden="true"></i>'+esc(e.zt)+'</span>':'—')+'</td>':'')+'</tr>'}).join('')+'</tbody></table>'}
function cambio(k,s,n,u){var c=cfg(k),f=s[0],l=s[s.length-1],m=c.m||0;if(c.min!=null&&(f.v<c.min||l.v<c.min))m=0;var dif=+(l.v-f.v).toFixed(6),ad=Math.abs(dif),cl=!dif?'igual':(m?((dif>0)===(m>0)?'mejor':'peor'):'neutro'),ud=c.du?c.du[ad===1?0:1]:u;
  return {cl:cl,t:dif?((dif>0?'↑ +':'↓ −')+nf(ad,n)+(ud?' '+ud:'')+' desde el '+dm(f.t)+(cl==='mejor'?' · mejora':cl==='peor'?' · empeora':'')):'= Igual que el '+dm(f.t)}}
function datos(o){var out=[];Object.keys(o).sort().forEach(function(k){if(!CFG[k]||!o[k])return;var g=series(o[k].h);Object.keys(g).sort().forEach(function(sn){var s=g[sn];if(s.length<2)return;var l=s[s.length-1],u=l.u||'',n=Math.max(decs(l.vt),decs(s[0].vt));out.push({k:k,o:o[k],sn:sn,s:s,u:u,n:n,c:cambio(k,s,n,u)})})});return out}
function tarjeta(x,i){var l=x.s[x.s.length-1],gr=grafica(x.s,x.n,true);R[i]={P:gr.P,W:gr.W,H:gr.H,tx:x.s.map(function(e){return '<b>'+dm(e.t)+' · '+esc(val(e,x.u))+'</b>'+(e.zt?'<span>'+esc(e.zt)+'</span>':'')})};
  return '<article class="evo-c"><div class="evo-cab"><div>'+(x.sn?'<p class="evo-k">'+esc(x.o.titulo||x.k)+'</p>':'')+'<h3><a href="'+esc(x.k)+'">'+esc(x.sn||x.o.titulo||x.k)+'</a></h3></div><span class="evo-n">'+x.s.length+' resultados</span></div>'
    +'<div class="evo-fila"><p class="evo-v'+((l.vt||'').length>7?' largo':'')+'"><b>'+esc(l.vt||nf(l.v,x.n))+'</b>'+(x.u?'<span>'+esc(x.u)+'</span>':'')+'</p>'+(l.zt?'<p class="evo-zc z-'+esc(l.z||'')+'"><i aria-hidden="true"></i>'+esc(l.zt)+'</p>':'')+'</div>'
    +'<p class="evo-d '+x.c.cl+'">'+esc(x.c.t)+'</p>'
    +'<div class="evo-graf" tabindex="0" role="group" data-i="'+i+'" aria-label="'+esc('Gráfica de '+(x.o.titulo||'')+(x.sn?' ('+x.sn+')':'')+': '+x.s.length+' resultados. Recórrelos con las flechas.')+'">'+gr.svg+'<p class="evo-tip" role="status"></p></div>'
    +'<details class="evo-t"><summary>Ver en tabla</summary>'+tabla(x.s,x.u)+'</details>'
    +(x.k==='calculadora-1rm.html'&&!x.sn?'<p class="evo-pista">¿Mezclas ejercicios? Escribe cuál es en la calculadora y aquí saldrá cada uno por separado.</p>':'')+'</article>'}
function activa(g,i){var r=R[+g.dataset.i];if(!r)return;i=Math.max(0,Math.min(r.P.length-1,i));g.dataset.a=i;var p=r.P[i],sv=g.querySelector('svg'),x=sv.querySelector('.evo-x'),tip=g.querySelector('.evo-tip');x.setAttribute('x1',p[0]);x.setAttribute('x2',p[0]);
  [].forEach.call(sv.querySelectorAll('.evo-p'),function(c){c.classList.toggle('act',+c.dataset.i===i)});g.classList.add('on');tip.innerHTML=r.tx[i];
  var w=g.clientWidth,h=sv.getBoundingClientRect().height,tw=tip.offsetWidth,th=tip.offsetHeight,cx=p[0]/r.W*w,cy=p[1]/r.H*h;tip.style.left=Math.max(0,Math.min(w-tw,cx-tw/2))+'px';tip.style.top=Math.max(-th-4,cy-th-14)+'px'}
function apaga(g){g.classList.remove('on');var t=g.querySelector('.evo-tip');if(t)t.innerHTML='';[].forEach.call(g.querySelectorAll('.evo-p.act'),function(c){c.classList.remove('act')})}
function cerca(g,cx){var r=R[+g.dataset.i],b=g.getBoundingClientRect(),x=(cx-b.left)/b.width*r.W,m=0;r.P.forEach(function(p,i){if(Math.abs(p[0]-x)<Math.abs(r.P[m][0]-x))m=i});return m}
function liga(g){g.addEventListener('pointermove',function(e){activa(g,cerca(g,e.clientX))});g.addEventListener('pointerdown',function(e){activa(g,cerca(g,e.clientX))});g.addEventListener('pointerleave',function(){if(D.activeElement!==g)apaga(g)});
  g.addEventListener('focus',function(){activa(g,g.dataset.a!=null?+g.dataset.a:R[+g.dataset.i].P.length-1)});g.addEventListener('blur',function(){apaga(g)});
  g.addEventListener('keydown',function(e){var r=R[+g.dataset.i],a=g.dataset.a!=null?+g.dataset.a:r.P.length-1,k=e.key,n=k==='ArrowLeft'||k==='ArrowDown'?a-1:k==='ArrowRight'||k==='ArrowUp'?a+1:k==='Home'?0:k==='End'?r.P.length-1:null;if(n===null)return;e.preventDefault();activa(g,n)})}
function pinta(){var xs=datos(lee());R=[];E.hidden=!xs.length;G.innerHTML=xs.map(tarjeta).join('');[].forEach.call(G.querySelectorAll('.evo-graf'),liga);
  D.getElementById('mr-evo-n').textContent=xs.length===1?'Una gráfica: sale cuando guardas dos o más resultados de una misma prueba.':xs.length+' gráficas: salen cuando guardas dos o más resultados de una misma prueba.';if(I&&!I.hidden)informe()}
// Informe para tu médico: en pantalla para revisar, y al imprimir solo la hoja
var IB=D.getElementById('mr-inf-b'),I=D.getElementById('mr-inf'),ID=D.getElementById('mr-inf-doc'),IN=D.getElementById('mr-inf-nombre'),IL=D.getElementById('mr-inf-sel'),SEL={};
function herrs(o){return Object.keys(o).filter(function(k){return o[k]&&o[k].h&&o[k].h.length}).sort(function(a,b){return (o[b].h[0].t||0)-(o[a].h[0].t||0)})}
function opciones(o){var ks=herrs(o);IL.innerHTML=ks.map(function(k){if(SEL[k]==null)SEL[k]=true;return '<label><input type="checkbox" value="'+esc(k)+'"'+(SEL[k]?' checked':'')+'> '+esc(o[k].titulo||k)+'</label>'}).join('');return ks}
function informe(){var o=lee(),ks=herrs(o).filter(function(k){return SEL[k]!==false}),xs=datos(o).filter(function(x){return ks.indexOf(x.k)>=0}),nom=(IN.value||'').replace(/\s+/g,' ').trim();
  var res=xs.length?'<div class="inf-res"><p class="inf-et">Resumen de lo que tiene evolución</p><table><thead><tr><th scope="col">Prueba</th><th scope="col">Último</th><th scope="col">Fecha</th><th scope="col">Cambio</th></tr></thead><tbody>'+xs.map(function(x){var l=x.s[x.s.length-1];return '<tr><td data-l="Prueba"><span>'+esc(x.o.titulo||x.k)+(x.sn?' · '+esc(x.sn):'')+'</span></td><td data-l="Último"><span>'+esc(val(l,x.u))+(l.zt?'<br><small>'+esc(l.zt)+'</small>':'')+'</span></td><td data-l="Fecha"><span>'+dm(l.t)+'</span></td><td data-l="Cambio"><span>'+esc(x.c.t)+'</span></td></tr>'}).join('')+'</tbody></table></div>':'';
  ID.innerHTML='<header class="inf-cab"><p class="inf-marca">Fuerza Basada en Evidencia · Calculadoras</p><h2>Resultados de pruebas y calculadoras</h2><p class="inf-meta"><span>Fecha del informe: <b>'+dm(Date.now())+'</b></span>'+(nom?'<span>Nombre: <b>'+esc(nom)+'</b></span>':'')+'</p><p class="inf-aviso">Resultados que he apuntado yo en las calculadoras gratuitas de fuerzabasadaenevidencia.com. Son estimaciones orientativas, no un diagnóstico. Las fuentes de cada prueba van al final de su apartado.</p></header>'
   +(ks.length?res+ks.map(function(k){var x=o[k],h=x.h,u0=h[0],ev=xs.filter(function(z){return z.k===k});
     return '<div class="inf-it"><div class="inf-it-cab"><h3>'+esc(x.titulo||k)+'</h3><time datetime="'+new Date(u0.t||0).toISOString().slice(0,10)+'">'+dm(u0.t)+'</time></div><pre>'+esc(u0.texto||'')+'</pre>'+(u0.n?'<p class="inf-nota"><b>Nota:</b> '+esc(u0.n)+'</p>':'')
       +(ev.length?ev.map(function(z){return '<div class="inf-evo"><p class="inf-et">Evolución'+(z.sn?' · '+esc(z.sn):'')+' ('+z.s.length+' resultados)</p><div class="inf-evo-c">'+grafica(z.s,z.n,false).svg+tabla(z.s,z.u)+'</div></div>'}).join('')
         :(h.length>1?'<p class="inf-et">Anteriores</p><ul class="inf-ant">'+h.slice(1).map(function(e){return '<li>'+dm(e.t)+': '+esc(String(e.texto||'').split('\n')[0])+(e.n?' <i>('+esc(e.n)+')</i>':'')+'</li>'}).join('')+'</ul>':''))
       +(FU[k]?'<div class="inf-fu"><p class="inf-et">Fuentes</p><ol>'+FU[k].map(function(f){return '<li>'+esc(f)+'</li>'}).join('')+'</ol></div>':'')+'</div>'}).join('')
     :'<p class="inf-vacio">Marca al menos una prueba para incluirla.</p>')
   +'<footer class="inf-pie">Calculadoras de fuerzabasadaenevidencia.com · Hecho en tu navegador: no se ha enviado a ningún sitio.</footer>'}
function imprime(){informe();var c=D.getElementById('inf-print');if(c)c.remove();c=D.createElement('div');c.id='inf-print';c.className='inf-doc';c.innerHTML=ID.innerHTML;D.body.appendChild(c);D.documentElement.classList.add('imprime-inf');
  var fin=function(){D.documentElement.classList.remove('imprime-inf');var x=D.getElementById('inf-print');if(x)x.remove();window.removeEventListener('afterprint',fin)};window.addEventListener('afterprint',fin);window.print()}
if(IB&&I){IB.addEventListener('click',function(){SEL={};opciones(lee());informe();I.hidden=false;I.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches||D.documentElement.classList.contains('quieto')?'auto':'smooth',block:'start'});D.getElementById('mr-inf-h').focus({preventScroll:true})});
  IN.addEventListener('input',informe);IL.addEventListener('change',function(e){if(e.target&&e.target.value)SEL[e.target.value]=e.target.checked;informe()});
  D.getElementById('mr-inf-imp').addEventListener('click',imprime);
  D.getElementById('mr-inf-x').addEventListener('click',function(){I.hidden=true;IB.focus()});}
pinta();new MutationObserver(function(){pinta();if(I&&!I.hidden)opciones(lee())}).observe(L,{childList:true});
if(/^#(informe|mr-inf)$/.test(location.hash)&&IB)setTimeout(function(){if(herrs(lee()).length)IB.click()},60);
})();"""
EVO_JS = EVO_JS.replace('__CFG__', json.dumps(EVO_CFG)).replace('__FU__', json.dumps(EVO_FU, ensure_ascii=False))
_EVO_HTML = '''<section class="mr-evo sube" id="mr-evo" hidden aria-labelledby="mr-evo-h"><div class="entrada"><h2 id="mr-evo-h">Mi evolución</h2><p id="mr-evo-n"></p></div>
    <div class="evo-rej" id="mr-evo-rej"></div></section>
  <section class="mr-inf" id="mr-inf" hidden aria-labelledby="mr-inf-h"><div class="inf-barra"><h2 id="mr-inf-h" tabindex="-1">Informe para tu médico</h2>
    <p>Una hoja con tus resultados, su evolución y de dónde salen los números, para imprimir o guardar en PDF. Elige qué incluir; tu nombre solo sale en la hoja y no se guarda.</p>
    <label class="inf-nom"><span>Nombre (opcional)</span><input id="mr-inf-nombre" type="text" autocomplete="name" maxlength="80"></label>
    <fieldset class="inf-sel"><legend>Incluir</legend><div id="mr-inf-sel"></div></fieldset>
    <div class="inf-bots"><button type="button" class="btn peq" id="mr-inf-imp">Imprimir o guardar en PDF</button><button type="button" class="enl-b" id="mr-inf-x">Cerrar</button></div></div>
    <div class="inf-doc" id="mr-inf-doc"></div></section>
  '''
_p = open(f'{SAL}/mis-resultados.html', encoding='utf-8').read()
_a = '<div class="mr-lista" id="mr-lista"></div>'
assert _a in _p, 'mis-resultados: no encuentro la lista'
_p = _p.replace(_a, _EVO_HTML + _a, 1)
_a = '<button type="button" class="btn peq" id="mr-imp">Imprimir o guardar en PDF</button>'
assert _a in _p
_p = _p.replace(_a, '<button type="button" class="btn peq" id="mr-inf-b">Informe para tu médico</button>' + _a.replace('class="btn peq"', 'class="btn peq hueco"'), 1)
_p = _p.replace('</main>', f'<script>{EVO_JS}</script></main>', 1)
open(f'{SAL}/mis-resultados.html', 'w', encoding='utf-8').write(_p)
import sys as _sys
print('evolución: fuentes para el informe de', len(EVO_FU), 'herramientas', file=_sys.stderr)
