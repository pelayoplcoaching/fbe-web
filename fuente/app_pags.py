# La web como app (22/11/2026), parte 1: páginas nuevas. La ejecuta interior.py justo después de secciones.py
# (antes de extras.py, para que reciban el manifiesto, los ajustes de lectura, el buscador y el sitemap como las demás).
#  - aprende.html: todo lo de aprender en una pantalla (pestaña «Aprende» del móvil).
#  - mi-panel.html: inicio personal (seguir donde lo dejaste, tu semana, resultados, favoritos, ruta, Mis datos, logros). Siempre noindex.
#  - novedades.html y feed.xml: lo último (vídeos, envíos del boletín y cambios de la web), con canal RSS.
#  - ayuda.html: cómo instalar la web, qué funciona sin conexión, dónde se guardan tus datos, copia de seguridad y borrado.
#  - sin-conexion.html: lo que enseña el service worker cuando no hay red y la página no está guardada. Siempre noindex.
# Lo que parchea páginas ya hechas (pestañas, vídeos enlazados, portada, rutas, manifiesto y service worker) está en app.py.
import json as _ja, html as _ha
from email.utils import format_datetime as _rfc
from datetime import datetime as _dt, timezone as _tz
I.update({
    'casa': '<path d="M4 11l8-7 8 7v8a1 1 0 0 1-1 1h-4v-6h-6v6H5a1 1 0 0 1-1-1z"/>',
    'cajas': '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    'birrete': '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5V16c1.5 1.5 3.5 2 5.5 2s4-.5 5.5-2v-4.5M21.5 9.5v5"/>',
    'panel': '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.5-4 3.5-6 7-6s6.5 2 7 6"/>',
    'estrella': '<path d="M12 3.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
    'rayo': '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
    'mas': '<path d="M12 5v14M5 12h14"/>',
})
def _aic(n): return ico(n if n in I else 'libro')
_BOLJ = sorted(_ja.load(open('boletin.json', encoding='utf-8')), key=lambda b: b['f'], reverse=True)
_RECN = len(_ja.load(open('ext/recetas.json', encoding='utf-8')))
def _fl(f): return f'{int(f[8:10])} {_MES_V[int(f[5:7]) - 1]} {f[:4]}'
_UV = VIDS[0]; _UB = _BOLJ[0]
_ULT_V = f'<ul class="vid-rej ap-vid">{vid_card(_UV, href=f"videos.html#v-{_UV["id"]}", ancla=False)}</ul>'
_ULT_B = f'<a class="ap-bol" href="{_UB["u"]}" target="_blank" rel="noopener"><small>Boletín · {_fl(_UB["f"])}</small><b>{_ha.escape(_UB["asunto"])}</b><span>Leer el envío</span></a>'

# ---------------------------------------------------------------------------------------------
# aprende.html
AP_SEC = [('empieza-aqui.html', 'brujula', 'Empieza aquí', 'Seis rutas según tu caso, con sus pasos.'),
          ('videos.html', 'play', 'Vídeos', f'Los {len(VIDS)} vídeos del canal, por temas y con capítulos.'),
          ('mitos.html', 'bombilla', 'Mitos y evidencia', f'{len(MITOS)} mitos, cada uno con su estudio y su veredicto.'),
          ('glosario.html', 'libro', 'Glosario', 'Cada término, explicado en dos líneas.'),
          ('recetas.html', 'plato', 'Recetas con proteína', f'{_RECN} recetas del recetario de la app.'),
          ('guias.html', 'carpeta', 'Guías', 'Para descargar y aplicar.'),
          ('newsletter.html', 'sobre', 'Newsletter', 'Una idea cada semana, en tu correo.'),
          ('boletin.html', 'calendario', 'Archivo del boletín', f'Los {len(_BOLJ)} envíos, para leer cuando quieras.'),
          ('fuentes.html', 'lupa', 'Fuentes', 'De dónde sale cada número de la web.'),
          ('evidencia.html', 'fonendo', 'Cómo trabajo la evidencia', 'Cómo elijo y compruebo los estudios.'),
          ('novedades.html', 'rayo', 'Novedades', 'Lo último: vídeos, envíos y herramientas.')] + ([('medios.html', 'micro', 'En los medios', 'Entrevistas y pódcast.')] if len(MEDIOS) >= 2 else [])
def _ap_tema(u, t):
    i = ilus('web-' + u[:-5], 'ap-tema-img')
    return f'<a class="ap-tema" href="{u}">{i}<b>{t}</b></a>'
SEC_SIG['aprende.html'] = (('index.html', 'Inicio'), ('herramientas.html', 'Herramientas'))
pagina('aprende.html', 'Aprende', 'Todo lo que hay para aprender en Fuerza Basada en Evidencia: rutas para empezar, vídeos con capítulos, mitos con su estudio, glosario, recetas, guías y el boletín, ordenado por temas.',
       'Aprende, a tu ritmo.', 'Rutas para empezar, vídeos, mitos con su estudio, glosario, recetas y el boletín. Todo lo de aprender, en una pantalla.', f'''
<section><div class="in"><div class="entrada sube"><h2>¿Por dónde empiezo?</h2><p>Elige tu caso y te marco los pasos.</p></div>
  <div class="ap-rutas sube">{"".join(f'<a class="ap-ruta" href="empieza-aqui.html#{p}"><i class="ea-bi">{ico(EA_ICO[p])}</i><b>{t}</b><span>{len(xs)} pasos</span></a>' for p, t, _, xs in EA_PERF)}</div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Lo último</h2><p>El vídeo y el envío más recientes.</p></div>
  <div class="ap-ult sube">{_ULT_V}{_ULT_B}</div>
  <p class="sec-enl sube"><b>¿Quieres ver todo lo nuevo?</b><a href="novedades.html">Novedades</a><a href="videos.html">Todos los vídeos</a></p>
</div></section>
<section><div class="in"><div class="entrada sube"><h2>Todo lo que hay</h2><p>Cada sección, a un toque.</p></div>
  <div class="ap-rej sube">{"".join(f'<a class="ap-t" href="{u}"><i class="ic">{_aic(i)}</i><b>{t}</b><span>{d}</span></a>' for u, i, t, d in AP_SEC)}</div>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Por tema</h2><p>Lo que hay sobre cada asunto, junto: herramientas, mitos, vídeos y lecturas.</p></div>
  <div class="ap-temas sube">{"".join(_ap_tema(u, t) for u, t in TEMAS_MENU)}</div>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>Aprender haciendo</h3><p>Las herramientas te dan tu número, con su fuente. El chequeo de 10 minutos junta cuatro en una sola pasada.</p></div><div><a class="btn claro" href="herramientas.html">Ver las herramientas</a></div></div></div></section>''',
       cta='<div class="cta"><a class="btn claro" href="empieza-aqui.html">Empieza aquí</a><a class="enl" href="videos.html">Ver los vídeos</a></div>')

# ---------------------------------------------------------------------------------------------
# mi-panel.html
_PN_DATA = {'rutas': {p: {'t': t, 'pasos': [[u, tt] for u, _, tt, _ in xs]} for p, t, _, xs in EA_PERF}}
_PN_ACC = [('chequeo.html', 'check', 'Chequeo de 10 minutos'), ('temporizador.html', 'crono', 'Temporizador'), ('semana-activa.html', 'anillos', 'Mi semana activa'), ('herramientas.html', 'cajas', 'Todas las herramientas')]
PN_JS = r'''(function(){
var F=window.fbe;if(!F)return;var $=function(i){return document.getElementById(i)},S=JSON.parse($('pn-data').textContent),MS=['ene','feb','mar','abr','may','jun','jul','ago','sept','oct','nov','dic'];
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fecha(t){var d=new Date(t);return d.getDate()+' '+MS[d.getMonth()]}
var h=new Date().getHours();$('pn-saludo').textContent=h<6?'Buenas noches':h<14?'Buenos días':h<21?'Buenas tardes':'Buenas noches';
var V=F.lee('fbe-visto',[]).slice(0,4);$('pn-sigue').hidden=!V.length;$('pn-sigue-l').innerHTML=V.map(function(x){return '<li><a href="'+esc(x.u)+'"><small>'+esc(x.k||'Página')+'</small><b>'+esc(x.t)+'</b></a></li>'}).join('');
(function(){var d=new Date(),l=new Date(d.getFullYear(),d.getMonth(),d.getDate());l.setDate(l.getDate()-((l.getDay()+6)%7));var k=l.getFullYear()+'-'+('0'+(l.getMonth()+1)).slice(-2)+'-'+('0'+l.getDate()).slice(-2),L=(F.lee('fbe-semana',{})||{})[k]||[],m=0,v=0,f={};
 L.forEach(function(e){if(e.t==='m')m+=e.n;else if(e.t==='v')v+=e.n;else f[e.d]=1});var eq=m+2*v,nf=Object.keys(f).length;
 $('pn-a1').style.strokeDashoffset=100-Math.min(100,eq/150*100);$('pn-a2').style.strokeDashoffset=100-Math.min(100,nf/2*100);
 $('pn-sem-t').innerHTML=L.length?'<b>'+eq+' de 150 min</b> de aeróbico<br><b>'+nf+' de 2 días</b> de fuerza':'Apunta lo que hagas esta semana y cierra los dos anillos.';$('pn-sem-b').textContent=L.length?(eq>=150&&nf>=2?'Semana cumplida':'Apuntar más'):'Empezar la semana'})();
(function(){var R=F.lee('fbe-resultados',{})||{},L=Object.keys(R).map(function(u){var e=R[u],x=(e.h&&e.h[0])||(e.texto?{t:e.t,texto:e.texto}:null);return x?{u:u,ti:e.titulo||u,x:x}:null}).filter(Boolean).sort(function(a,b){return (b.x.t||0)-(a.x.t||0)});
 $('pn-res-l').innerHTML=L.slice(0,3).map(function(r){return '<li class="pn-z-'+esc(r.x.z||'')+'"><a href="'+esc(r.u)+'"><b>'+esc(r.ti)+'</b><span>'+esc(r.x.vt?r.x.vt+(r.x.u?' '+r.x.u:'')+(r.x.zt?' · '+r.x.zt:''):String(r.x.texto||'').split('\n')[0].slice(0,90))+'</span><small>'+(r.x.t?fecha(r.x.t):'')+'</small></a></li>'}).join('');
 $('pn-res-v').hidden=L.length>0;$('pn-res-m').hidden=!L.length;
 var C=['revision-medica.html','actividad-oms.html','test-silla.html','cintura-altura.html'],n=C.filter(function(u){return R[u]}).length;$('pn-chq').innerHTML=n===4?'Chequeo de 10 minutos: <b>completo</b>. <a href="chequeo.html">Ver el resumen</a>':'Chequeo de 10 minutos: <b>'+n+' de 4</b> pruebas. <a href="chequeo.html">'+(n?'Seguir':'Empezar')+'</a>'})();
function favs(){var L=F.favs();$('pn-fav-v').hidden=L.length>0;$('pn-fav-l').innerHTML=L.map(function(x,i){return '<li><a href="'+esc(x.u)+'"><small>'+esc(x.k||'Página')+'</small><b>'+esc(x.t)+'</b></a><button type="button" data-u="'+esc(x.u)+'" aria-label="Quitar de favoritos: '+esc(x.t)+'">×</button></li>'}).join('')}
$('pn-fav-l').addEventListener('click',function(e){var b=e.target.closest('button[data-u]');if(!b)return;var L=F.favs().filter(function(x){return x.u!==b.dataset.u});F.pon('fbe-favoritos',L);favs()});favs();
(function(){var ru=F.lee('fbe-rutas',{})||{},ks=Object.keys(ru).filter(function(k){return S.rutas[k]&&ru[k]&&ru[k].h&&ru[k].h.length}).sort(function(a,b){return (ru[b].t||0)-(ru[a].t||0)}),c=$('pn-ruta-c');
 if(!ks.length){c.innerHTML='<p class="pn-vacio">Elige tu caso y marca los pasos según los vayas haciendo.</p><a class="pn-mas" href="empieza-aqui.html">Elegir mi ruta</a>';return}
 var k=ks[0],r=S.rutas[k],h=ru[k].h,n=r.pasos.length,he=h.filter(function(i){return i<n}).length,sig=-1;for(var i=0;i<n;i++)if(h.indexOf(i)<0){sig=i;break}
 c.innerHTML='<p class="pn-ruta-t"><b>'+esc(r.t)+'</b><span>'+he+' de '+n+' pasos</span></p><div class="pn-barra"><i style="width:'+Math.round(he/n*100)+'%"></i></div>'+(sig>=0?'<p class="pn-sig">Siguiente: <a href="'+esc(r.pasos[sig][0])+'"'+(/^http/.test(r.pasos[sig][0])?' rel="noopener"':'')+'>'+esc(r.pasos[sig][1])+'</a></p>':'<p class="pn-sig">Ruta terminada.</p>')+'<a class="pn-mas" href="empieza-aqui.html#'+k+'">Ver mi ruta</a>'})();
(function(){var P=F.lee('fbe-perfil',{})||{},m=$('pn-msg');function pinta(){$('pn-edad').value=P.edad||'';$('pn-peso').value=P.peso||'';$('pn-alt').value=P.altura||'';[].forEach.call(document.querySelectorAll('input[name="pn-sexo"]'),function(r){r.checked=r.value===P.sexo});$('pn-borra').hidden=!Object.keys(P).length}
 function num(id,mn,mx){var v=String($(id).value).replace(',','.').trim();if(v==='')return null;var x=parseFloat(v);return isNaN(x)||x<mn||x>mx?NaN:x}
 $('pn-guarda').addEventListener('click',function(){var e=num('pn-edad',14,100),p=num('pn-peso',30,250),a=num('pn-alt',120,220),s=document.querySelector('input[name="pn-sexo"]:checked');
  if([e,p,a].some(function(x){return x!==null&&isNaN(x)})){m.textContent='Revisa los números: edad de 14 a 100, peso de 30 a 250 kg y altura de 120 a 220 cm.';m.className='pn-msg mal';return}
  P={};if(e!==null)P.edad=Math.round(e);if(p!==null)P.peso=p;if(a!==null)P.altura=Math.round(a);if(s)P.sexo=s.value;F.pon('fbe-perfil',P);m.textContent=Object.keys(P).length?'Guardado en este dispositivo. Las calculadoras se rellenarán solas.':'No hay nada que guardar.';m.className='pn-msg ok';pinta();setTimeout(logros,200)});
 $('pn-borra').addEventListener('click',function(){P={};try{localStorage.removeItem('fbe-perfil')}catch(e){}m.textContent='Datos borrados.';m.className='pn-msg ok';pinta()});pinta()})();
function logros(){var G=F.logros(),n=0;$('pn-log-l').innerHTML=F.LOGROS.map(function(l){var ok=G[l[0]];if(ok)n++;return '<li class="'+(ok?'ok':'')+'"><i aria-hidden="true"></i><b>'+esc(l[1])+'</b><span>'+esc(l[2])+'</span>'+(ok?'<small>Conseguido el '+fecha(ok)+'</small>':'')+'</li>'}).join('');$('pn-log-n').textContent=n+' de '+F.LOGROS.length}
logros();
if(location.hash&&document.querySelector(location.hash))setTimeout(function(){document.querySelector(location.hash).scrollIntoView({block:'start'})},80);
})();'''
SEC_SIG['mi-panel.html'] = (('herramientas.html', 'Herramientas'), ('aprende.html', 'Aprende'))
pagina('mi-panel.html', 'Mi panel', 'Tu inicio personal en Fuerza Basada en Evidencia: sigue donde lo dejaste, tu semana, tus resultados, tus favoritos y tus datos. Todo guardado solo en tu dispositivo.',
       'Tu panel.', 'Lo tuyo, en un sitio: dónde lo dejaste, tu semana, tus resultados y tus favoritos. Se guarda solo en este dispositivo.', f'''
<section class="pn-s"><div class="in">
  <div class="pn-hola sube"><p class="pn-saludo" id="pn-saludo">Hola</p><h2 class="pn-h">¿Qué toca hoy?</h2>
    <div class="pn-acc">{"".join(f'<a href="{u}"><i class="ic">{_aic(i)}</i><b>{t}</b></a>' for u, i, t in _PN_ACC)}</div></div>
  <div class="pn-rej">
    <article class="pn-t sube" id="pn-sigue" hidden><h3>Sigue donde lo dejaste</h3><ul class="pn-l" id="pn-sigue-l"></ul></article>
    <article class="pn-t pn-sem sube" id="pn-semana"><h3>Tu semana</h3><div class="pn-sem-c"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="pn-ap" cx="60" cy="60" r="50"/><circle class="pn-aa pn-a1" id="pn-a1" cx="60" cy="60" r="50" pathLength="100" transform="rotate(-90 60 60)"/><circle class="pn-ap" cx="60" cy="60" r="36"/><circle class="pn-aa pn-a2" id="pn-a2" cx="60" cy="60" r="36" pathLength="100" transform="rotate(-90 60 60)"/></svg><p id="pn-sem-t"></p></div><a class="pn-mas" href="semana-activa.html" id="pn-sem-b">Apuntar</a></article>
    <article class="pn-t sube" id="pn-res"><h3>Tus resultados</h3><ul class="pn-l pn-res-l" id="pn-res-l"></ul><p class="pn-vacio" id="pn-res-v">Cuando guardes el resultado de una herramienta, lo verás aquí.</p><p class="pn-chq" id="pn-chq"></p><a class="pn-mas" href="mis-resultados.html" id="pn-res-m" hidden>Ver todos y mi evolución</a></article>
    <article class="pn-t sube" id="pn-fav"><h3>Favoritos</h3><ul class="pn-l pn-fav-l" id="pn-fav-l"></ul><p class="pn-vacio" id="pn-fav-v">Toca la estrella de cualquier página, vídeo, mito o receta y lo tendrás aquí.</p></article>
    <article class="pn-t sube" id="pn-ruta"><h3>Tu ruta</h3><div id="pn-ruta-c"></div></article>
    <article class="pn-t sube" id="pn-datos"><h3>Mis datos</h3><p class="pn-nota">Escríbelos una vez y las calculadoras se rellenan solas. No salen de este dispositivo.</p>
      <div class="pn-form"><div class="pn-campo"><label for="pn-edad">Edad</label><input id="pn-edad" type="number" inputmode="numeric" min="14" max="100" autocomplete="off"></div>
      <fieldset class="pn-campo pn-sexo"><legend>Sexo</legend><label><input type="radio" name="pn-sexo" value="h"><span>Hombre</span></label><label><input type="radio" name="pn-sexo" value="m"><span>Mujer</span></label></fieldset>
      <div class="pn-campo"><label for="pn-peso">Peso (kg)</label><input id="pn-peso" type="number" inputmode="decimal" min="30" max="250" step="0.5" autocomplete="off"></div>
      <div class="pn-campo"><label for="pn-alt">Altura (cm)</label><input id="pn-alt" type="number" inputmode="numeric" min="120" max="220" autocomplete="off"></div></div>
      <div class="pn-bots"><button type="button" class="pn-b" id="pn-guarda">Guardar</button><button type="button" class="pn-b2" id="pn-borra" hidden>Borrar mis datos</button></div><p class="pn-msg" id="pn-msg" role="status"></p></article>
    <article class="pn-t pn-logros sube" id="pn-logros"><h3>Logros <small id="pn-log-n"></small></h3><ul class="pn-log" id="pn-log-l"></ul></article>
    <article class="pn-t pn-ult sube" id="pn-ult"><h3>Lo último</h3>{_ULT_V}{_ULT_B}<a class="pn-mas" href="novedades.html">Todas las novedades</a></article>
  </div>
  <p class="pn-pie sube">Todo lo de esta página vive solo en tu navegador. <a href="ayuda.html#datos">Cómo hacer una copia o borrarlo</a>.</p>
</div></section>
<script type="application/json" id="pn-data">{_ja.dumps(_PN_DATA, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>document.addEventListener('DOMContentLoaded',function(){{{PN_JS}}});</script>''',
       cta='<div class="cta"><a class="btn claro" href="herramientas.html">Herramientas</a><a class="enl" href="aprende.html">Aprende</a></div>', extra='<meta name="robots" content="noindex">')

# ---------------------------------------------------------------------------------------------
# novedades.html y feed.xml
NOV_WEB = [('2026-11-22', 'Cinco herramientas nuevas: temporizador, Mi semana activa, pasos al día, tensión en casa y equilibrio', 'herramientas.html'),
           ('2026-11-22', 'Mi panel, favoritos y Mis datos: la web, como una app', 'mi-panel.html'),
           ('2026-11-22', 'Los vídeos, con capítulos y enlazados con su herramienta', 'videos.html'),
           ('2026-11-21', 'Chequeo de 10 minutos: cuatro pruebas en una pasada', 'chequeo.html'),
           ('2026-11-21', 'Recetas con proteína', 'recetas.html'),
           ('2026-11-21', 'Fuentes: de dónde sale cada número', 'fuentes.html'),
           ('2026-11-21', 'Mitos y evidencia, con test', 'mitos.html'),
           ('2026-11-21', 'Glosario y archivo del boletín', 'glosario.html'),
           ('2026-11-21', 'Catorce herramientas con su fuente', 'herramientas.html')]
_NOV = ([{'f': v['f'], 'k': 'v', 'y': 'Vídeo', 't': v['t'], 'u': f'videos.html#v-{v["id"]}', 'x': v['d']} for v in VIDS]
        + [{'f': b['f'], 'k': 'b', 'y': 'Boletín', 't': b['asunto'], 'u': b['u'], 'x': b['tema']} for b in _BOLJ]
        + [{'f': f, 'k': 'w', 'y': 'Web', 't': t, 'u': u, 'x': ''} for f, t, u in NOV_WEB])
_NOV.sort(key=lambda x: (x['f'], {'w': 2, 'v': 1, 'b': 0}[x['k']]), reverse=True)
_MES_L = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
def _nov_li(x, n):
    ext = x['u'].startswith('http')
    return (f'<li class="nov-i" data-k="{x["k"]}"{" hidden" if n >= 30 else ""}><time datetime="{x["f"]}">{int(x["f"][8:10])} {_MES_V[int(x["f"][5:7]) - 1]}</time>'
            f'<a href="{x["u"]}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}><small>{x["y"]}{" · " + _ha.escape(x["x"]) if x["x"] else ""}</small><b>{_ha.escape(x["t"])}</b></a></li>')
def _nov_html():
    out = []; mes = ''
    for n, x in enumerate(_NOV):
        m = x['f'][:7]
        if m != mes: mes = m; out.append(f'<li class="nov-mes"{" hidden" if n >= 30 else ""}>{_MES_L[int(m[5:7]) - 1]} de {m[:4]}</li>')
        out.append(_nov_li(x, n))
    return ''.join(out)
NOV_JS = r'''(function(){var L=document.getElementById('nov-l'),C=document.getElementById('nov-f'),M=document.getElementById('nov-mas'),N=document.getElementById('nov-n');if(!L)return;var k='',ver=30,is=[].slice.call(L.querySelectorAll('.nov-i')),ms=[].slice.call(L.querySelectorAll('.nov-mes'));
function pinta(){var n=0,tot=0;is.forEach(function(li){var ok=!k||li.dataset.k===k;if(ok)tot++;li.hidden=!(ok&&n<ver);if(ok&&n<ver)n++});
 ms.forEach(function(m){var e=m.nextElementSibling,hay=false;while(e&&!e.classList.contains('nov-mes')){if(!e.hidden)hay=true;e=e.nextElementSibling}m.hidden=!hay});
 M.hidden=n>=tot;N.textContent=n+' de '+tot}
C.addEventListener('click',function(e){var b=e.target.closest('button[data-k]');if(!b)return;k=b.dataset.k;ver=30;[].forEach.call(C.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',String(x===b))});pinta()});
M.addEventListener('click',function(){ver+=30;pinta()});pinta()})();'''
_NC = {k: sum(1 for x in _NOV if x['k'] == k) for k in 'vbw'}
SEC_SIG['novedades.html'] = (('aprende.html', 'Aprende'), ('videos.html', 'Vídeos'))
pagina('novedades.html', 'Novedades', 'Lo último de Fuerza Basada en Evidencia: vídeos nuevos, envíos del boletín y herramientas y secciones de la web, por fecha. Con canal RSS.',
       'Lo último.', 'Vídeos nuevos, envíos del boletín y cambios de la web, del más reciente al más antiguo.', f'''
<section><div class="in">
  <div class="nov-cab sube"><div class="vid-chips" id="nov-f" role="group" aria-label="Tipo"><button type="button" data-k="" aria-pressed="true">Todo <span>{len(_NOV)}</span></button><button type="button" data-k="v" aria-pressed="false">Vídeos <span>{_NC["v"]}</span></button><button type="button" data-k="b" aria-pressed="false">Boletín <span>{_NC["b"]}</span></button><button type="button" data-k="w" aria-pressed="false">Web <span>{_NC["w"]}</span></button></div>
    <p class="vid-cuenta" aria-live="polite">Mostrando <span id="nov-n">30 de {len(_NOV)}</span></p></div>
  <ol class="nov-l sube" id="nov-l">{_nov_html()}</ol>
  <button type="button" class="nov-mas" id="nov-mas">Ver más</button>
  <div class="calc sube nov-rss"><div><h3>Síguelo con un lector RSS</h3><p>Si usas un lector de noticias, añade el canal y te llega cada vídeo y cada envío.</p></div><div><a class="btn claro" href="feed.xml">Canal RSS</a></div></div>
</div></section>
<script>{NOV_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="videos.html">Ver los vídeos</a><a class="enl" href="newsletter.html">Recibir el boletín</a></div>')
def _xml(t): return _ha.escape(t, quote=False)
def _pub(f): return _rfc(_dt(int(f[:4]), int(f[5:7]), int(f[8:10]), 9, 0, tzinfo=_tz.utc))
_FEED = [x for x in _NOV if x['k'] in 'vb'][:40]
open(f'{SAL}/feed.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>\n'
    f'<title>Fuerza Basada en Evidencia: novedades</title><link>{WEB}novedades.html</link><description>Vídeos y envíos del boletín de Pelayo Fernández Cidón, médico internista.</description><language>es</language>'
    f'<atom:link href="{WEB}feed.xml" rel="self" type="application/rss+xml"/><lastBuildDate>{_pub(_FEED[0]["f"])}</lastBuildDate>\n'
    + ''.join(f'<item><title>{_xml(x["t"])}</title><link>{_xml(x["u"] if x["u"].startswith("http") else WEB + x["u"])}</link><guid isPermaLink="false">fbe-{x["k"]}-{_xml(x["u"].split("/")[-1].split("#")[-1])}</guid><category>{x["y"]}</category><pubDate>{_pub(x["f"])}</pubDate></item>\n' for x in _FEED)
    + '</channel></rss>\n')

# ---------------------------------------------------------------------------------------------
# ayuda.html
AY_JS = r'''(function(){var $=function(i){return document.getElementById(i)},m=$('ay-msg');function claves(){var ks=[];try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf('fbe-')===0)ks.push(k)}}catch(e){}return ks}
function di(t,ok){m.textContent=t;m.className='pn-msg '+(ok?'ok':'mal')}
function cuenta(){var n=claves().length;$('ay-n').textContent=n?(n===1?'Hay 1 apartado guardado en este dispositivo.':'Hay '+n+' apartados guardados en este dispositivo.'):'Ahora mismo no hay nada guardado en este dispositivo.';$('ay-baja').disabled=!n;$('ay-borra').disabled=!n}
$('ay-baja').addEventListener('click',function(){var o={_fbe:'copia',_fecha:new Date().toISOString()};claves().forEach(function(k){o[k]=localStorage.getItem(k)});var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(o,null,1)],{type:'application/json'}));a.download='fbe-mis-datos-'+new Date().toISOString().slice(0,10)+'.json';document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href)},2000);di('Copia descargada. Guárdala donde quieras.',1)});
$('ay-sube').addEventListener('change',function(){var f=this.files&&this.files[0];if(!f)return;var r=new FileReader();r.onload=function(){try{var o=JSON.parse(r.result),n=0;if(!o||o._fbe!=='copia')throw 0;Object.keys(o).forEach(function(k){if(k.indexOf('fbe-')===0&&typeof o[k]==='string'){localStorage.setItem(k,o[k]);n++}});di('Recuperados '+n+' apartados. Ya están en este dispositivo.',1);cuenta()}catch(e){di('Ese archivo no es una copia de esta web.',0)}};r.readAsText(f);this.value=''});
$('ay-borra').addEventListener('click',function(){if(!this.dataset.seguro){this.dataset.seguro='1';this.textContent='Pulsa otra vez para borrarlo todo';var b=this;setTimeout(function(){delete b.dataset.seguro;b.textContent='Borrar todo lo guardado'},4000);return}claves().forEach(function(k){try{localStorage.removeItem(k)}catch(e){}});delete this.dataset.seguro;this.textContent='Borrar todo lo guardado';di('Borrado. Este dispositivo ya no guarda nada tuyo de esta web.',1);cuenta()});
cuenta()})();'''
SEC_SIG['ayuda.html'] = (('mi-panel.html', 'Mi panel'), ('dudas.html', 'Dudas'))
pagina('ayuda.html', 'Cómo usar la app', 'Cómo instalar Fuerza Basada en Evidencia en el móvil, qué funciona sin conexión, dónde se guardan tus datos y cómo hacer una copia o borrarlos.',
       'La web, en tu móvil como una app.', 'Cómo instalarla, qué funciona sin conexión y qué pasa con lo que guardas: se queda en tu dispositivo.', f'''
<section id="instalar"><div class="in"><div class="entrada sube"><h2>Instalarla</h2><p>No pasa por ninguna tienda y no ocupa casi nada. Se abre a pantalla completa, con su icono.</p></div>
  <div class="ay-tres sube">
    <div class="ay-c"><h3>iPhone y iPad</h3><ol><li>Abre la web en Safari.</li><li>Toca «Compartir».</li><li>Elige «Añadir a pantalla de inicio».</li></ol></div>
    <div class="ay-c"><h3>Android</h3><ol><li>Abre la web en Chrome.</li><li>Toca el menú de los tres puntos.</li><li>Elige «Instalar aplicación» o «Añadir a pantalla de inicio».</li></ol></div>
    <div class="ay-c"><h3>Ordenador</h3><ol><li>Abre la web en Chrome o Edge.</li><li>Pulsa el icono de instalar de la barra de direcciones.</li><li>Confirma con «Instalar».</li></ol></div>
  </div>
</div></section>
<section class="hoja" id="sin-conexion"><div class="in"><div class="entrada sube"><h2>Sin conexión</h2><p>En el gimnasio no siempre hay cobertura. Por eso las herramientas se quedan guardadas.</p></div>
  <ul class="ay-lista sube"><li><b>Funcionan sin conexión:</b> todas las calculadoras y pruebas, el temporizador, Mi semana activa, Mi panel, Mis resultados, el glosario y el buscador.</li>
  <li><b>Necesitan conexión:</b> los vídeos (se ven desde YouTube), los envíos del boletín y los formularios.</li>
  <li><b>Lo demás:</b> las páginas que ya has abierto se quedan guardadas y se pueden releer sin red.</li></ul>
</div></section>
<section id="datos"><div class="in"><div class="entrada sube"><h2>Tus datos son tuyos</h2><p>Resultados, favoritos, Mis datos, tu semana, tus tomas de tensión: todo se guarda solo en el navegador de este dispositivo.</p></div>
  <ul class="ay-lista sube"><li><b>No se envía nada.</b> Las herramientas calculan en tu dispositivo y la web no usa analítica.</li>
  <li><b>Solo sale lo que tú mandas:</b> el formulario de «Pedir plaza» y el alta en el boletín. Y si pulsas un vídeo, lo sirve YouTube.</li>
  <li><b>Si borras los datos del navegador</b> o cambias de móvil, lo guardado no viaja contigo. Para eso está la copia.</li></ul>
  <div class="ay-copia sube"><h3>Copia de seguridad</h3><p id="ay-n"></p>
    <div class="pn-bots"><button type="button" class="pn-b" id="ay-baja">Descargar una copia</button><label class="pn-b2 ay-sube-l">Recuperar una copia<input type="file" id="ay-sube" accept="application/json,.json" class="oculto"></label><button type="button" class="pn-b2 ay-rojo" id="ay-borra">Borrar todo lo guardado</button></div>
    <p class="pn-msg" id="ay-msg" role="status"></p></div>
</div></section>
<section class="hoja" id="atajos"><div class="in"><div class="entrada sube"><h2>Atajos</h2><p>Para moverte más rápido.</p></div>
  <ul class="ay-lista sube"><li><b>Buscar:</b> la lupa de arriba, o las teclas <kbd>Ctrl</kbd> + <kbd>K</kbd> o <kbd>/</kbd>. Busca páginas, herramientas, mitos, vídeos, recetas y términos.</li>
  <li><b>Acciones rápidas:</b> en el buscador, escribe «oscuro», «texto» o «guardar» y hazlo desde ahí.</li>
  <li><b>Favoritos:</b> la estrella de cada página, vídeo, mito o receta. Los tienes en <a href="mi-panel.html#pn-fav">Mi panel</a>.</li>
  <li><b>Ajustes de lectura:</b> el botón «Aa»: tamaño del texto, contraste alto, sin animaciones y escuchar la página.</li>
  <li><b>Novedades:</b> en <a href="novedades.html">Novedades</a>, o con el <a href="feed.xml">canal RSS</a>.</li></ul>
</div></section>
<script>{AY_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="mi-panel.html">Abrir Mi panel</a><a class="enl" href="#datos">Tus datos</a></div>')

# ---------------------------------------------------------------------------------------------
# sin-conexion.html
SEC_SIG['sin-conexion.html'] = (('mi-panel.html', 'Mi panel'), ('herramientas.html', 'Herramientas'))
pagina('sin-conexion.html', 'Sin conexión', 'Ahora no hay conexión. Las herramientas de Fuerza Basada en Evidencia siguen funcionando.',
       'Ahora no hay conexión.', 'Esta página no estaba guardada en tu dispositivo. Las herramientas sí: funcionan sin red.', f'''
<section><div class="in"><div class="entrada sube"><h2>Lo que puedes usar ahora</h2></div>
  <div class="ap-rej sube">{"".join(f'<a class="ap-t" href="{u}"><i class="ic">{_aic(i)}</i><b>{t}</b><span>{d}</span></a>' for u, i, t, d in [("temporizador.html", "crono", "Temporizador", "Descansos e intervalos."), ("semana-activa.html", "anillos", "Mi semana activa", "Apunta lo de hoy."), ("herramientas.html", "cajas", "Todas las herramientas", "Calculadoras y pruebas."), ("mi-panel.html", "panel", "Mi panel", "Lo tuyo."), ("mis-resultados.html", "grafica", "Mis resultados", "Tus resultados guardados."), ("glosario.html", "libro", "Glosario", "Cada término, en dos líneas.")])}</div>
  <p class="sec-enl sube"><b>¿Ya tienes red?</b><button type="button" class="pn-b" onclick="location.reload()">Volver a intentarlo</button></p>
</div></section>''', extra='<meta name="robots" content="noindex">')
SEC_PAGS += ['aprende.html', 'novedades.html', 'ayuda.html']
