# videos.html (secciones.py lo ejecuta en su sitio): los vídeos del canal, en fuente/videos.json,
# leídos del canal el 22/11/2026 con sus títulos tal cual (id, fecha, duración, título y temas).
# Arriba, el último en grande; debajo, todos en cuadrícula con filtro por tema, búsqueda y orden.
# Al pulsar una tarjeta se reproduce arriba (youtube-nocookie, solo al pulsar). Las miniaturas vienen de i.ytimg.com.
# Enlazable: videos.html#v-<id> (lo pone arriba) y videos.html?t=<tema>#todos (filtra).
# Para añadir un vídeo nuevo: una línea más en videos.json (se ordena solo por fecha).
import json as _jsv
import html as _html
import unicodedata as _ud
VIDS = sorted(_jsv.load(open('videos.json', encoding='utf-8')), key=lambda v: v['f'], reverse=True)
VID_G = [('fuerza', 'Fuerza y entreno'), ('envejecer', 'Envejecer con fuerza'), ('nutricion', 'Nutrición'), ('suplementos', 'Suplementos'),
         ('salud', 'Salud y análisis'), ('cardio', 'Cardio y pasos'), ('mitos', 'Mitos'), ('dolor', 'Dolor')]
VID_GD = dict(VID_G)
VID_TEMAS = ['Fuerza', 'Proteína', 'Creatina', 'Suplementos', 'Alcohol', 'Sueño', 'Colesterol', 'Cardio', 'Perder grasa', 'Mayores', 'Mujer', 'Mitos']
_MES_V = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sept', 'oct', 'nov', 'dic']
_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.5 5.8v12.4L19 12z"/></svg>'
_CAMPANA = '<svg class="vid-mini" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20a2 2 0 0 0 4 0"/></svg>'
_LUPA = '<svg class="vid-mini" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>'


def vid_fecha(f): return f'{int(f[8:])} {_MES_V[int(f[5:7]) - 1]} {f[:4]}'


def vid_seg(d):
    n = [int(x) for x in d.split(':')]
    return n[0] * 3600 + n[1] * 60 + n[2] if len(n) == 3 else n[0] * 60 + n[1]


def vid_iso(d):
    t = vid_seg(d)
    return f'PT{t // 60}M{t % 60}S'


def _vnorm(t): return ''.join(c for c in _ud.normalize('NFD', t.lower()) if _ud.category(c) != 'Mn')


def vid_mini(i, q='mq'): return f'https://i.ytimg.com/vi/{i}/{q}default.jpg'


def vid_card(v, href=None, ancla=True):
    """Tarjeta de un vídeo. Sin href enlaza a YouTube (en la página Vídeos el guion lo reproduce arriba)."""
    u = href or f'https://www.youtube.com/watch?v={v["id"]}'
    ext = '' if href else ' target="_blank" rel="noopener"'
    g = ' · '.join(VID_GD[x] for x in v['g'])
    ida = f' id="v-{v["id"]}"' if ancla else ''
    nv = ' data-nuevo="1"' if v['id'] == max(VIDS, key=lambda x: x['f'])['id'] else ''
    return (f'<li class="vc"{nv} data-g="{" ".join(v["g"])}" data-f="{v["f"]}" data-s="{vid_seg(v["d"])}" data-t="{_html.escape(_vnorm(v["t"] + " " + g))}">'
            f'<a class="vc-a"{ida} href="{u}" data-v="{v["id"]}"{ext}>'
            f'<span class="vc-img"><img src="{vid_mini(v["id"])}" alt="" width="320" height="180" loading="lazy" decoding="async" referrerpolicy="no-referrer"><span class="vc-dur">{v["d"]}</span><span class="vc-play">{_PLAY}</span></span>'
            f'<span class="vc-tx"><time datetime="{v["f"]}">{vid_fecha(v["f"])}</time><b>{_html.escape(v["t"])}</b><span class="vc-g">{g}</span></span></a></li>')


# Capítulos, guía y páginas relacionadas de cada vídeo (videos-extra.json: lo de la descripción de YouTube, leído el 22/11/2026)
_VXJ = _jsv.load(open('videos-extra.json', encoding='utf-8'))
_REL_T = {u: (t, 'Herramienta') for u, _sl, _i, t, _d in HERR_MAS}
_REL_T.update({'pauta-activa.html': ('Pauta Activa', 'Herramienta'), 'chequeo.html': ('Chequeo de 10 minutos', 'Herramienta'), 'mitos.html': ('Mitos y evidencia', 'Mitos'),
               'mitos.html#artrosis': ('El mito de la artrosis de rodilla', 'Mito'), 'mitos.html#creatina': ('El mito de la creatina', 'Mito'), 'mitos.html#proteina-rinon': ('El mito de la proteína y el riñón', 'Mito'),
               'recetas.html': ('Recetas con proteína', 'Recetas'), 'CALC': ('Calculadora de proteína', 'Herramienta')})
_REL_T.update({u: (t, 'Tema') for u, t in TEMAS_MENU})
def vid_rel(i):
    """Páginas de la web relacionadas con un vídeo: [(url, título, tipo)]."""
    return [(CALC if u == 'CALC' else u,) + _REL_T[u] for u in _VXJ.get(i, {}).get('r', []) if u in _REL_T]
def vid_caps(v):
    out = []
    for c in _VXJ.get(v['id'], {}).get('c', []):
        t, _, ti = c.partition(' '); sg = vid_seg(t)
        if sg < vid_seg(v['d']): out.append([sg, t.lstrip('0').replace(':', ':', 1) if not t.startswith('00:') else '0:' + t[3:], ti.rstrip('.')])
    return out
def vid_guia(i):
    e = _VXJ.get(i, {})
    if not e.get('g'): return None
    # g = subdominio antiguo de la guía (https://<g>.fuerzabasadaenevidencia.com/) o, en las guías nuevas, su dirección completa o relativa
    g = e['g']; u = g if g.startswith('http') or '/' in g else f'https://{g}.fuerzabasadaenevidencia.com/'
    return [u, e.get('gt', 'La guía del vídeo')]
VID_X = {v['id']: {k: x for k, x in (('c', vid_caps(v)), ('g', vid_guia(v['id'])), ('r', [list(r) for r in vid_rel(v['id'])])) if x} for v in VIDS}
_V0 = VIDS[0]
_VH = sum(vid_seg(v['d']) for v in VIDS)
_VCNT = {k: sum(k in v['g'] for v in VIDS) for k, _ in VID_G}
VID_JS = r"""(function(){
var dest=document.getElementById('vid-dest'),rej=document.getElementById('vid-rej');if(!dest||!rej)return;
var PLAY='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.5 5.8v12.4L19 12z"/></svg>';
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function datos(id){var a=rej.querySelector('a[data-v="'+id+'"]');if(!a)return null;return{id:id,t:a.querySelector('b').textContent,f:a.querySelector('time').textContent,d:a.querySelector('.vc-dur').textContent};}
function marca(id){[].forEach.call(rej.querySelectorAll('a[data-v]'),function(a){if(a.dataset.v===id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});}
function juega(v,s){var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+v.id+'?rel=0&autoplay=1'+(s?'&start='+s:'');f.title=v.t;f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';var d=document.createElement('div');d.className='vid-marco vid-on';d.id='vid';d.appendChild(f);document.getElementById('vid').replaceWith(d);}
var X={},fx=document.getElementById('vid-ficha');try{X=JSON.parse(document.getElementById('vid-x').textContent)}catch(e){}
function ficha(id){if(!fx)return;var v=datos(id),x=X[id]||{},h='';if(!v){fx.hidden=true;return}
 if(x.r&&x.r.length)h+='<div class="vf-rel"><p class="vf-et">Pruébalo tú</p><div class="vf-chips">'+x.r.map(function(r){return '<a class="vf-chip" href="'+esc(r[0])+'"'+(/^http/.test(r[0])?' rel="noopener"':'')+'><i class="pn-ki" data-k="'+esc(r[2])+'" aria-hidden="true"></i><small>'+esc(r[2])+'</small><b>'+esc(r[1])+'</b></a>'}).join('')+'</div></div>';
 if(x.g)h+='<a class="vf-guia" href="'+esc(x.g[0])+'" target="_blank" rel="noopener"><small>La guía de este vídeo</small><b>'+esc(x.g[1])+'</b></a>';
 if(x.c&&x.c.length)h+='<details class="vf-caps"'+(x.c.length<=9?' open':'')+'><summary>Capítulos <span>'+x.c.length+'</span></summary><ol>'+x.c.map(function(c){return '<li><button type="button" data-s="'+c[0]+'"><time>'+esc(c[1])+'</time><span>'+esc(c[2])+'</span></button></li>'}).join('')+'</ol></details>';
 fx.dataset.v=id;fx.innerHTML=h;fx.hidden=!h}
if(fx)fx.addEventListener('click',function(e){var b=e.target.closest('button[data-s]');if(!b)return;var v=datos(fx.dataset.v);if(!v)return;marca(v.id);juega(v,+b.dataset.s);[].forEach.call(fx.querySelectorAll('button[data-s]'),function(x){x.classList.toggle('act',x===b)});var r=dest.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)dest.scrollIntoView({block:'center'})});
function pon(id,auto,chip){var v=datos(id);if(!v)return;marca(id);ficha(id);
 dest.innerHTML='<a class="vid-marco vid-real" id="vid" href="https://www.youtube.com/watch?v='+v.id+'" data-v="'+v.id+'" target="_blank" rel="noopener"><img class="vid-fondo" src="https://i.ytimg.com/vi/'+v.id+'/maxresdefault.jpg" alt="" width="1280" height="720" referrerpolicy="no-referrer"><span class="vid-chip">'+esc(chip)+'</span><span class="vid-boton">'+PLAY+'</span><span class="vid-txt"><b>'+esc(v.t)+'</b><small>'+esc(v.f)+' · '+esc(v.d)+'</small></span></a>';
 if(auto)juega(v);}
dest.addEventListener('error',function(e){var i=e.target;if(i.tagName==='IMG'&&/maxres/.test(i.src))i.src=i.src.replace('maxresdefault','hqdefault');},true);
dest.addEventListener('click',function(e){var a=e.target.closest('#vid[data-v]');if(!a)return;e.preventDefault();var v=datos(a.dataset.v);if(v){marca(v.id);juega(v);}});
rej.addEventListener('click',function(e){var a=e.target.closest('a[data-v]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.button)return;e.preventDefault();pon(a.dataset.v,true,'Reproduciendo');try{history.replaceState(null,'','#v-'+a.dataset.v);}catch(_){}
 var r=dest.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)dest.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches||document.documentElement.classList.contains('quieto')?'auto':'smooth',block:'center'});});
ficha(dest.querySelector('#vid[data-v]').dataset.v);
var m=location.hash.match(/^#v-([\w-]{11})$/);if(m&&datos(m[1])){pon(m[1],false,'Elegido');setTimeout(function(){dest.scrollIntoView({block:'center'});},60);}
var lis=[].slice.call(rej.children),g='',q='',o='n',chips=document.getElementById('vid-chips'),inp=document.getElementById('vid-f'),sel=document.getElementById('vid-o'),cnt=document.getElementById('vid-n'),nada=document.getElementById('vid-nada');
function norm(t){return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
function aplica(){var ps=norm(q).split(/\s+/).filter(Boolean),n=0;
 var orden=lis.slice().sort(function(a,b){return o==='a'?a.dataset.f.localeCompare(b.dataset.f):o==='c'?a.dataset.s-b.dataset.s:b.dataset.f.localeCompare(a.dataset.f);});
 orden.forEach(function(li){var ok=(!g||(' '+li.dataset.g+' ').indexOf(' '+g+' ')>-1)&&ps.every(function(p){return li.dataset.t.indexOf(p)>-1;});li.hidden=!ok;if(ok)n++;rej.appendChild(li);});
 cnt.textContent=n===1?'1 vídeo':n+' vídeos';nada.hidden=n>0;var l=nada.querySelector('a');l.href=l.dataset.base+encodeURIComponent(q);}
chips.addEventListener('click',function(e){var b=e.target.closest('button[data-g]');if(!b)return;g=b.dataset.g;[].forEach.call(chips.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',String(x===b));});aplica();});
inp.addEventListener('input',function(){q=inp.value;aplica();});
sel.addEventListener('change',function(){o=sel.value;aplica();});
var t=new URLSearchParams(location.search).get('t');if(t){var b=chips.querySelector('button[data-g="'+t+'"]');if(b)b.click();}
})();"""
_VLD = '<script type="application/ld+json">' + _jsv.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Vídeos de Fuerza Basada en Evidencia',
    'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'item': {'@type': 'VideoObject', 'name': v['t'], 'uploadDate': v['f'], 'duration': vid_iso(v['d']), 'inLanguage': 'es',
        'thumbnailUrl': vid_mini(v['id'], 'hq'), 'embedUrl': f'https://www.youtube-nocookie.com/embed/{v["id"]}', 'contentUrl': f'https://www.youtube.com/watch?v={v["id"]}'}}
        for n, v in enumerate(VIDS)]}, ensure_ascii=False) + '</script>'
_CHIPS_V = f'<button type="button" data-g="" aria-pressed="true">Todos <span>{len(VIDS)}</span></button>' + ''.join(
    f'<button type="button" data-g="{k}" aria-pressed="false">{t} <span>{_VCNT[k]}</span></button>' for k, t in VID_G if _VCNT[k] >= 2)
_DEST_V = (f'<a class="vid-marco vid-real" id="vid" href="https://www.youtube.com/watch?v={_V0["id"]}" data-v="{_V0["id"]}" target="_blank" rel="noopener">'
           f'<img class="vid-fondo" src="https://i.ytimg.com/vi/{_V0["id"]}/maxresdefault.jpg" onerror="this.onerror=null;this.src=\'{vid_mini(_V0["id"], "hq")}\'" alt="" width="1280" height="720" referrerpolicy="no-referrer" fetchpriority="high">'
           f'<span class="vid-chip">Último vídeo</span><span class="vid-boton">{_PLAY}</span>'
           f'<span class="vid-txt"><b>{_html.escape(_V0["t"])}</b><small>{vid_fecha(_V0["f"])} · {_V0["d"]}</small></span></a>')
pagina('videos.html', 'Vídeos', 'Los vídeos de Fuerza Basada en Evidencia en YouTube: fuerza, nutrición y salud explicadas por un médico internista, por temas.',
       'Lo que publico en YouTube.', f'Fuerza, nutrición y salud, explicadas por un médico internista. Los {len(VIDS)} vídeos del canal, por temas, para verlos aquí mismo.', f'''
<section><div class="in">
  <div class="vid-dest sube" id="vid-dest">{_DEST_V}</div>
  <div class="vid-ficha sube" id="vid-ficha" hidden></div>
  <div class="vid-cta sube"><a class="btn vid-ir" href="#todos">Ver todos los vídeos</a><a class="btn hueco" href="{YT}"{_ext(YT)}>Ir al canal</a><a class="btn hueco vid-sus" href="{YT}?sub_confirmation=1"{_ext(YT)}>{_CAMPANA}Suscribirme</a></div>
</div></section>
<section class="hoja" id="todos"><div class="in"><div class="entrada sube"><h2>Todos los vídeos</h2><p>{len(VIDS)} vídeos, unas {round(_VH / 3600)} horas en total. Elige un tema o busca por palabras; al pulsar uno, se ve arriba, con sus capítulos.</p></div>
  <div class="vid-filtros sube">
    <div class="vid-chips" id="vid-chips" role="group" aria-label="Tema">{_CHIPS_V}</div>
    <div class="vid-fila"><div class="vid-q">{_LUPA}<label class="oculto" for="vid-f">Buscar entre los vídeos</label><input id="vid-f" type="search" placeholder="Rodilla, creatina, azúcar…" autocomplete="off"></div><label class="oculto" for="vid-o">Ordenar</label><select id="vid-o"><option value="n">Más recientes</option><option value="a">Más antiguos</option><option value="c">Más cortos</option></select></div>
    <p class="vid-cuenta" id="vid-n" aria-live="polite">{len(VIDS)} vídeos</p>
  </div>
  <ul class="vid-rej" id="vid-rej">{"".join(vid_card(v) for v in VIDS)}</ul>
  <p class="vid-nada" id="vid-nada" hidden>Ningún vídeo con esas palabras. <a data-base="{YT}/search?query=" href="{YT}/search"{_ext(YT)}>Búscalo en el canal</a></p>
  <p class="vid-priv">Las miniaturas se cargan desde YouTube. El reproductor, solo cuando pulsas un vídeo, en modo de privacidad mejorada.</p>
</div></section>
<section><div class="in"><div class="entrada sube"><h2>¿No lo encuentras? Busca en el canal</h2><p>Cada tema abre la búsqueda dentro del canal de YouTube. O escribe el tuyo.</p></div>
  <form class="vid-busca sube" action="{YT}/search" method="get" target="_blank" rel="noopener" role="search"><label class="oculto" for="vid-q">Buscar en el canal</label>{_LUPA}<input id="vid-q" name="query" type="search" placeholder="Rodilla, sueño, proteína…" autocomplete="off" required><button class="btn" type="submit">Buscar</button></form>
  <ul class="vid-temas sube">{"".join(f'<li><a href="{YT}/search?query={_up.quote(t)}"{_ext(YT)}>{t}</a></li>' for t in VID_TEMAS)}</ul>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Del vídeo a tu semana</h2><p>Un vídeo te da la idea. Lo que cambia las cosas es aplicarla.</p></div>
  <ol class="pasos-g en-linea vid-pasos sube">
    <li>{sec_ic("video")}<b>Ves el vídeo</b><span>Una idea concreta sobre fuerza, nutrición o salud.</span></li>
    <li>{sec_ic("grafica")}<b>Lo pruebas en tu caso</b><span>Con las <a href="herramientas.html">herramientas de la web</a> o con una <a href="guias.html">guía</a>.</span></li>
    <li>{sec_ic("pesa")}<b>Si quieres, lo llevamos a tu semana</b><span>En la <a href="programas.html">asesoría</a> lo convierto en tu plan y lo reviso cada semana.</span></li>
  </ol>
  <div class="vid-redes sube"><b>También estoy en</b>{"".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in REDES if t != 'YouTube')}</div>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>¿Prefieres leerlo?</h3><p>En el boletín te llega una idea cada semana sobre fuerza, nutrición y salud.</p></div><div><a class="btn claro" href="newsletter.html">Ver el boletín</a></div></div></div></section>
<script type="application/json" id="vid-x">{_jsv.dumps(VID_X, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")}</script>
<script>{VID_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="#vid-dest">Ver el último</a><a class="enl" href="#todos">Todos, por temas</a></div>', extra=_VLD)
