# ===== diez mejoras más (21/11/2026) =====
# Se ejecuta desde interior.py justo despues de extras.py (antes del sitemap). Lo que va en el navegador esta al final de luz.js
# (escuchar la pagina y compartir) y en MR_JS de extras.py (notas, recordatorio y copia de seguridad de Mis resultados).
# Aqui: test «¿Mito o no?» en Mitos, planificador de la semana con archivo de calendario en la herramienta de la OMS,
# datos estructurados para buscadores (migas, herramientas y glosario) e imagen para compartir propia de cada pagina (og/*.jpg, la hace og.mjs).

# ---------------------------------------------------------------------------------------------
# «Ponte a prueba» en Mitos: los nueve mitos, uno a uno, y el veredicto con su fuente
_QZ = [{'id': m[0], 'f': m[2], 'v': m[3], 'vt': m[4] or MITO_VER[m[3]], 'tp': m[5]} for m in MITOS]
QUIZ_JS = r'''(function(){var Q=__Q__,V={f:'Falso',a:'A medias',n:'No demostrado'},i=0,bien=0,c=document.getElementById('qz');if(!c)return;
var fr=document.getElementById('qz-f'),pr=document.getElementById('qz-p'),bt=document.getElementById('qz-b'),rs=document.getElementById('qz-r'),sg=document.getElementById('qz-s'),bar=document.getElementById('qz-bar');
function pinta(){var q=Q[i];c.classList.remove('fin-qz','ok','mal');pr.textContent=(i+1)+' de '+Q.length;bar.style.width=(i/Q.length*100)+'%';fr.textContent='«'+q.f+'»';fr.classList.remove('nuevo');void fr.offsetWidth;fr.classList.add('nuevo');c.style.removeProperty('--acierto');rs.innerHTML='';sg.hidden=true;bt.hidden=false;[].forEach.call(bt.querySelectorAll('button'),function(b){b.disabled=false;b.className=''})}
bt.addEventListener('click',function(e){var b=e.target.closest('button');if(!b||b.disabled)return;var q=Q[i],ok=b.dataset.v===q.v;if(ok)bien++;c.classList.add(ok?'ok':'mal');[].forEach.call(bt.querySelectorAll('button'),function(x){x.disabled=true;if(x.dataset.v===q.v)x.className='es';else if(x===b)x.className='no-es'});
  rs.innerHTML='<b>'+(ok?'Bien visto.':'No exactamente.')+'</b> Veredicto: '+q.vt+'. Sale de: '+q.tp.toLowerCase()+'. <a href="#'+q.id+'">Ver la explicación</a>';sg.hidden=false;sg.textContent=i<Q.length-1?'Siguiente':'Ver mi resultado';sg.focus()});
sg.addEventListener('click',function(){if(i<Q.length-1){i++;pinta();return}c.classList.add('fin-qz');c.dataset.bien=bien;c.dataset.tot=Q.length;c.style.setProperty('--acierto',Math.round(bien/Q.length*100)+'%');var an=c.querySelector('.qz-anillo');if(an)an.dataset.x=bien+'/'+Q.length;bar.style.width='100%';pr.textContent='Resultado';fr.textContent='Has acertado '+bien+' de '+Q.length+'.';fr.classList.remove('nuevo');void fr.offsetWidth;fr.classList.add('nuevo');bt.hidden=true;rs.innerHTML=bien===Q.length?'Pleno. Ya sabes más que la mayoría del gimnasio.':bien>=6?'Muy bien: abre los que fallaste para ver por qué.':'Normal: son ideas muy repetidas. Abre las tarjetas de abajo para ver qué dicen los estudios.';sg.textContent='Repetir';sg.onclick=function(){sg.onclick=null;i=0;bien=0;pinta()}});
document.addEventListener('click',function(e){var a=e.target.closest('#qz-r a');if(!a)return;var d=document.querySelector(a.getAttribute('href')+' details');if(d)d.open=true});
pinta();})();'''.replace('__Q__', _json.dumps(_QZ, ensure_ascii=False))
_QUIZ = (f'<div class="qz sube" id="qz"><div class="qz-cab"><p class="qz-t">Ponte a prueba</p><p class="qz-p" id="qz-p">1 de {len(_QZ)}</p></div><div class="qz-barra" aria-hidden="true" style="--pasos:{len(_QZ)}"><i id="qz-bar"></i></div><span class="qz-anillo" aria-hidden="true"></span>'
         '<p class="qz-f" id="qz-f" aria-live="polite"></p><div class="qz-b" id="qz-b" role="group" aria-label="Tu respuesta"><button type="button" data-v="f">Falso</button><button type="button" data-v="a">A medias</button><button type="button" data-v="n">No demostrado</button></div>'
         f'<p class="qz-r" id="qz-r" role="status"></p><button type="button" class="btn peq qz-s" id="qz-s" hidden>Siguiente</button></div><script>{QUIZ_JS}</script>\n  ')
_parchea('mitos.html', '<div class="mitos-rej" id="lista">', _QUIZ + '<div class="mitos-rej" id="lista">')

# ---------------------------------------------------------------------------------------------
# Planificador de la semana en «¿Llegas a lo mínimo de la OMS?»: descarga un archivo .ics con eventos que se repiten cada semana
_DIAS = [('MO', 'L', 'Lunes'), ('TU', 'M', 'Martes'), ('WE', 'X', 'Miércoles'), ('TH', 'J', 'Jueves'), ('FR', 'V', 'Viernes'), ('SA', 'S', 'Sábado'), ('SU', 'D', 'Domingo')]
def _dias(n, sel):
    return '<div class="pl-dias" role="group" aria-label="Días">' + ''.join(f'<label title="{t}"><input type="checkbox" name="{n}" value="{c}"{" checked" if c in sel else ""}><span>{l}</span></label>' for c, l, t in _DIAS) + '</div>'
PLAN_JS = r'''(function(){var $=function(i){return document.getElementById(i)},D=['SU','MO','TU','WE','TH','FR','SA'];
function sel(n){return [].map.call(document.querySelectorAll('input[name="'+n+'"]:checked'),function(c){return c.value})}
function n(id){var x=parseInt($(id).value,10);return x>0?x:0}
function resumen(){var f=sel('pl-f'),c=sel('pl-c'),mf=f.length*n('pl-fm'),mc=c.length*n('pl-cm');$('pl-res').innerHTML='<b>'+f.length+'</b> '+(f.length===1?'día':'días')+' de fuerza y <b>'+mc+'</b> minutos de actividad aeróbica a la semana'+(mc>=150&&f.length>=2?' · <span class="si">llegas a lo mínimo de la OMS</span>':'');$('pl-baja').disabled=!(f.length||c.length)}
function p2(x){return (x<10?'0':'')+x}
function fecha(d){return d.getFullYear()+p2(d.getMonth()+1)+p2(d.getDate())}
function ev(dias,titulo,hora,min,desc){if(!dias.length)return '';var hm=hora.split(':'),h=+hm[0]||19,m=+hm[1]||0,hoy=new Date(),d=new Date(hoy);for(var k=0;k<8;k++){var x=new Date(hoy.getFullYear(),hoy.getMonth(),hoy.getDate()+k);if(dias.indexOf(D[x.getDay()])>=0&&(k>0||h*60+m>hoy.getHours()*60+hoy.getMinutes())){d=x;break}}
  var ini=new Date(d.getFullYear(),d.getMonth(),d.getDate(),h,m),fin=new Date(ini.getTime()+min*60000),t=function(z){return fecha(z)+'T'+p2(z.getHours())+p2(z.getMinutes())+'00'},st=new Date().toISOString().replace(/[-:]/g,'').replace(/\.\d+/,'');
  return ['BEGIN:VEVENT','UID:'+Date.now()+Math.random().toString(36).slice(2)+'@fuerzabasadaenevidencia.com','DTSTAMP:'+st,'DTSTART:'+t(ini),'DTEND:'+t(fin),'RRULE:FREQ=WEEKLY;BYDAY='+dias.join(','),'SUMMARY:'+titulo,'DESCRIPTION:'+desc,'BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+titulo,'TRIGGER:-PT30M','END:VALARM','END:VEVENT'].join('\r\n')+'\r\n'}
$('pl-baja').addEventListener('click',function(){var h=$('pl-h').value||'19:00',url=location.href.split('#')[0],ics='BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fuerza Basada en Evidencia//Plan semanal//ES\r\nCALSCALE:GREGORIAN\r\n'+ev(sel('pl-f'),'Fuerza (FBE)',h,n('pl-fm'),'Sesión de fuerza de tu plan semanal. '+url)+ev(sel('pl-c'),'Caminar o cardio (FBE)',$('pl-h2').value||h,n('pl-cm'),'Actividad aeróbica de tu plan semanal. '+url)+'END:VCALENDAR\r\n';
  var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([ics],{type:'text/calendar;charset=utf-8'}));a.download='mi-semana-fbe.ics';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500);$('pl-ok').hidden=false});
document.querySelector('.plan-sem').addEventListener('input',resumen);document.querySelector('.plan-sem').addEventListener('change',resumen);resumen();})();'''
PLAN_SEC = f'''<section class="hoja plan-s"><div class="in"><div class="entrada sube"><h2>Ponlo en tu calendario</h2><p>Elige tus días y te llevas un archivo para tu calendario (Google, Apple u Outlook), con un aviso media hora antes y repetido cada semana.</p></div>
  <form class="plan-sem sube" onsubmit="return false">
    <fieldset class="pl-g"><legend>Fuerza</legend>{_dias('pl-f', ('MO', 'TH'))}<div class="pl-h">{campo_num("pl-fm", "Minutos por sesión", 45, 10, 180, 5, ud="min")}<div class="tool-campo"><label for="pl-h">Hora</label><input type="time" id="pl-h" value="19:00"></div></div></fieldset>
    <fieldset class="pl-g"><legend>Caminar o cardio</legend>{_dias('pl-c', ('TU', 'WE', 'FR', 'SA'))}<div class="pl-h">{campo_num("pl-cm", "Minutos por sesión", 40, 10, 180, 5, ud="min")}<div class="tool-campo"><label for="pl-h2">Hora</label><input type="time" id="pl-h2" value="08:00"></div></div></fieldset>
    <p class="pl-res" id="pl-res" role="status"></p>
    <div class="pl-bots"><button type="button" class="btn" id="pl-baja">Descargar para mi calendario</button><span class="pl-ok" id="pl-ok" hidden>Abre el archivo descargado y acepta añadirlo a tu calendario.</span></div>
  </form>
</div></section>
<script>{PLAN_JS}</script>
'''
_parchea('actividad-oms.html', '<section class="hoja"><div class="in"><div class="entrada sube"><h2>Cómo se interpreta</h2>', PLAN_SEC + '<section class="hoja"><div class="in"><div class="entrada sube"><h2>Cómo se interpreta</h2>')

# ---------------------------------------------------------------------------------------------
# Datos estructurados para buscadores: migas de pan en las subpaginas, cada herramienta como aplicacion web y el glosario
def _ld(o): return '<script type="application/ld+json">' + _json.dumps(o, ensure_ascii=False) + '</script>'
_AUTOR = {'@type': 'Person', 'name': 'Pelayo Fernández Cidón', 'jobTitle': 'Médico especialista en Medicina Interna'}
_HERR_T = {u: (t, d) for u, sl, i, t, d in HERR_MAS}
for _f in glob.glob(f'{SAL}/*.html'):
    _b = os.path.basename(_f)
    if _b in ('index.html', '404.html') or _b.startswith(('gracias', 'pedir-plaza')): continue
    _t = open(_f, encoding='utf-8').read()
    if 'http-equiv="refresh"' in _t or '"BreadcrumbList"' in _t: continue
    _m = re.search(r'<span class="miga">(.*?)</span>', _t, re.S)
    _add = ''
    if _m:
        _els, _k = [], 1
        for _u, _n in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', _m.group(1)):
            _els.append({'@type': 'ListItem', 'position': _k, 'name': _txt(_n), 'item': WEB + ('' if _u == 'index.html' else _u)}); _k += 1
        _h1 = re.search(r'<h1[^>]*>(.*?)</h1>', _t, re.S)
        _tt = re.search(r'<title>(.*?) · ', _t)
        _els.append({'@type': 'ListItem', 'position': _k, 'name': _txt(_tt.group(1)) if _tt else _txt(_h1.group(1)), 'item': WEB + _b})
        _add += _ld({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': _els})
    if _b in _HERR_T:
        _add += _ld({'@context': 'https://schema.org', '@type': 'WebApplication', 'name': _HERR_T[_b][0], 'description': _HERR_T[_b][1], 'url': WEB + _b, 'applicationCategory': 'HealthApplication',
                     'operatingSystem': 'Web', 'inLanguage': 'es', 'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'EUR'}, 'author': _AUTOR})
    if _b == 'glosario.html':
        _add += _ld({'@context': 'https://schema.org', '@type': 'DefinedTermSet', 'name': 'Glosario de fuerza', 'url': WEB + _b, 'inLanguage': 'es',
                     'hasDefinedTerm': [{'@type': 'DefinedTerm', 'name': g[1], 'description': g[3], 'url': f'{WEB}glosario.html#{g[0]}'} for g in GLOS]})
    if _add: open(_f, 'w', encoding='utf-8').write(_t.replace('</head>', _add + '</head>', 1))

# ---------------------------------------------------------------------------------------------
# Imagen para compartir propia de cada pagina (WhatsApp, redes): og/<pagina>.jpg con su titulo. La lista la usa og.mjs.
os.makedirs(f'{SAL}/og', exist_ok=True)
_OG = []
for _b in dict.fromkeys([u for u, _ in PAGS] + ['pauta-activa.html', 'esencial.html'] + [u for u, *_ in HERR_MAS] + SEC_PAGS):
    _p = f'{SAL}/{_b}'
    if not os.path.exists(_p): continue
    _t = open(_p, encoding='utf-8').read()
    _h1 = re.search(r'<h1[^>]*>(.*?)</h1>', _t, re.S)
    _sub = re.search(r'<p class="sub">(.*?)</p>', _t, re.S)
    _mg = re.search(r'<span class="miga">(.*?)</span>', _t, re.S)
    _miga = re.findall(r'<a href="[^"]+"[^>]*>(.*?)</a>', _mg.group(1)) if _mg else []
    _tit = re.search(r'<title>(.*?) · ', _t); _tit = _txt(_tit.group(1)) if _tit else ''
    _et = 'Herramienta gratuita' if _b in _HERR_T else (_txt(_miga[-1]) if len(_miga) > 1 else (_tit if _h1 and _norm(_tit).strip('. ') not in _norm(_txt(_h1.group(1))) else ''))
    _s = _txt(_sub.group(1)) if _sub else ''
    if len(_s) > 150: _s = _s[:147].rsplit(' ', 1)[0] + '…'
    _img = f'og/{_b[:-5]}.jpg'
    _OG.append({'f': _img, 't': _txt(_h1.group(1)) if _h1 else _b, 's': _s, 'e': _et})
    _n = _t.replace(f'<meta property="og:image" content="{WEB}og.png">', f'<meta property="og:image" content="{WEB}{_img}">', 1)
    if _n != _t: open(_p, 'w', encoding='utf-8').write(_n)
open(f'{SAL}/og/lista.json', 'w', encoding='utf-8').write(_json.dumps(_OG, ensure_ascii=False))
