# La web como app (22/11/2026), parte 2: lo que se añade a páginas ya hechas. La ejecuta interior.py después de datos.py.
#  1. Pestañas de abajo en el móvil (Inicio, Herramientas, Aprende, Mi panel, Plaza). En el navegador salen en las páginas
#     de herramientas y de aprender (las de venta conservan su barra «Pedir plaza»); con la web instalada, en todas.
#  2. Vídeos enlazados: «Te lo explico en vídeo» en cada herramienta y cada mito (según «r» de videos-extra.json).
#  3. Portada: bloque «Esta semana» (último vídeo, su herramienta y el último envío del boletín). Se actualiza solo.
#  4. Empieza aquí: pasos que se marcan, con progreso (localStorage fbe-rutas).
#  5. Buscador: acciones rápidas (tipo «Acción») y Mi panel. Canal RSS enlazado en todas las páginas.
#  6. Manifiesto (inicio en Mi panel, atajos, capturas para el aviso de instalar) y service worker (página propia sin conexión).
import json as _jp, glob as _gp, re as _rp, hashlib as _hp, os as _op, shutil as _sp

# ---------------------------------------------------------------------------------------------
# 1. Pestañas
TAB_VENTA = {'index.html', 'programas.html', 'puesta-a-punto.html', 'quien-soy.html', 'pedir-plaza.html', 'gracias.html', 'gracias-plaza.html', 'gracias-boletin.html', 'pauta-activa.html'}
_T_HERR = {u for u, *_ in HERR_MAS} | {'herramientas.html', 'chequeo.html', 'mis-resultados.html', 'pauta-activa.html'}
_T_APR = {u for u, *_ in APRENDE} | {u for u, _ in TEMAS_MENU} | {'aprende.html', 'fuentes.html', 'evidencia.html', 'novedades.html', 'medios.html', 'dudas.html'}
def _tab_de(arch):
    if arch == 'index.html': return 'inicio'
    if arch in _T_HERR: return 'herr'
    if arch in _T_APR: return 'aprende'
    if arch in ('mi-panel.html', 'ayuda.html', 'sin-conexion.html'): return 'panel'
    if arch in ('pedir-plaza.html', 'programas.html', 'puesta-a-punto.html'): return 'plaza'
    return ''
_TABS = [('inicio', 'index.html', 'casa', 'Inicio'), ('herr', 'herramientas.html', 'cajas', 'Herramientas'), ('aprende', 'aprende.html', 'birrete', 'Aprende'), ('panel', 'mi-panel.html', 'panel', 'Mi panel'), ('plaza', FORM, 'mas', 'Pedir plaza')]
def tabs_html(arch):
    act = _tab_de(arch)
    return ('<nav class="tabs" id="tabs" aria-label="Secciones">' + ''.join(
        f'<a href="{u}" data-t="{k}"{" class=\"tabs-plaza\"" if k == "plaza" else ""}{" aria-current=\"true\"" if k == act else ""}>{ico(i)}<span>{t}</span></a>' for k, u, i, t in _TABS) + '</nav>')
_RSS = '<link rel="alternate" type="application/rss+xml" title="Fuerza Basada en Evidencia: novedades" href="feed.xml">'
for _f in _gp.glob(f'{SAL}/*.html'):
    _b = _op.path.basename(_f); _t = open(_f, encoding='utf-8').read()
    if '</body>' not in _t or 'http-equiv="refresh"' in _t or 'id="tabs"' in _t: continue
    _n = _t.replace('</body>', tabs_html(_b) + '</body>', 1)
    if _b not in TAB_VENTA: _n = _rp.sub(r'<body class="', '<body class="con-tabs ', _n, count=1) if '<body class="' in _n else _n.replace('<body', '<body class="con-tabs"', 1)
    if _RSS not in _n: _n = _n.replace('</head>', _RSS + '</head>', 1)
    open(_f, 'w', encoding='utf-8').write(_n)

# ---------------------------------------------------------------------------------------------
# 2. «Te lo explico en vídeo» en herramientas y mitos
_VD = {v['id']: v for v in VIDS}
_VREL = {}
for _v in VIDS:  # del más reciente al más antiguo
    for _u in _VXJ.get(_v['id'], {}).get('r', []): _VREL.setdefault(_u, []).append(_v)
def _tv_html(vs):
    return ('<section class="tv-s" id="en-video" aria-labelledby="tv-h"><div class="in"><div class="entrada sube"><h2 id="tv-h">Te lo explico en vídeo</h2><p>' + ('El vídeo en el que lo cuento, con sus capítulos.' if len(vs) == 1 else 'Los vídeos en los que lo cuento, con sus capítulos.') + '</p></div>'
            '<ul class="vid-rej tm-vids tv-vids sube">' + ''.join(vid_card(v, href=f'videos.html#v-{v["id"]}', ancla=False) for v in vs) + '</ul></div></section>\n')
_tv_n = 0
for _u, _vs in _VREL.items():
    if '#' in _u or _u == 'CALC' or not _u.endswith('.html') or _u.startswith('tema-') or _u in ('mitos.html', 'recetas.html', 'chequeo.html', 'pauta-activa.html'): continue
    _p = f'{SAL}/{_u}'
    if not _op.path.exists(_p): continue
    _t = open(_p, encoding='utf-8').read()
    if 'id="en-video"' in _t: continue
    _i = _t.find('<section class="bol-cta-s"')
    if _i < 0: _i = _t.find('<section class="cierre"')
    if _i < 0: continue
    open(_p, 'w', encoding='utf-8').write(_t[:_i] + _tv_html(_vs[:2]) + _t[_i:]); _tv_n += 1
_m = open(f'{SAL}/mitos.html', encoding='utf-8').read(); _mv_n = 0
for _u, _vs in _VREL.items():
    if not _u.startswith('mitos.html#'): continue
    _id = _u.split('#')[1]; _a = _m.find(f'<article class="mito sube" id="{_id}"'); _b = _m.find('<div class="mito-pie">', _a)
    if _a < 0 or _b < 0 or f'mito-video" href="videos.html#v-{_vs[0]["id"]}"' in _m: continue
    _m = _m[:_b] + f'<a class="mito-enl mito-video" href="videos.html#v-{_vs[0]["id"]}">En vídeo: {_ha.escape(_vs[0]["t"])}</a>' + _m[_b:]; _mv_n += 1
open(f'{SAL}/mitos.html', 'w', encoding='utf-8').write(_m)
print('vídeos enlazados:', _tv_n, 'herramientas y', _mv_n, 'mitos')

# ---------------------------------------------------------------------------------------------
# 3. Portada: «Esta semana»
_x = open(f'{SAL}/index.html', encoding='utf-8').read()
_rel = [r for r in vid_rel(_UV['id']) if r[2] == 'Herramienta'][:1]
_HD = {u: (t, d, i) for u, sl, i, t, d in HERR_MAS}
_sem_h = ''
if _rel:
    _ru, _rt, _rk = _rel[0]; _rd = _HD.get(_ru, (_rt, '', 'check'))
    _sem_h = f'<a class="es-t es-herr" href="{_ru}"><small>La herramienta del vídeo</small><i class="ic">{_aic(_rd[2])}</i><b>{_rd[0]}</b><span>{_rd[1]}</span></a>'
_g = vid_guia(_UV['id'])
_ES = (f'<section class="esta-semana lenta" id="esta-semana"><div class="in"><div class="entrada sube"><h2>Esta semana</h2><p>Lo último que he publicado, para verlo, probarlo y leerlo.</p></div>'
       f'<div class="es-rej sube"><div class="es-vid">{_ULT_V}</div>{_sem_h}{_ULT_B}</div>'
       f'<p class="sec-enl sube"><b>Hay más</b><a href="videos.html">Todos los vídeos</a><a href="novedades.html">Novedades</a><a href="herramientas.html">Herramientas</a></p></div></section>\n')
_i = _x.find('<section class="aprende lenta">'); _j = _x.find('</section>', _i)
if _i > 0 and _j > 0 and 'id="esta-semana"' not in _x:
    _x = _x[:_j + len('</section>')] + '\n' + _ES + _x[_j + len('</section>'):]
    open(f'{SAL}/index.html', 'w', encoding='utf-8').write(_x)

# ---------------------------------------------------------------------------------------------
# 4. Empieza aquí: pasos que se marcan
EA_PROG_JS = r'''(function(){var K='fbe-rutas',F=window.fbe,R={},res={};try{R=JSON.parse(localStorage.getItem(K)||'{}')||{};res=JSON.parse(localStorage.getItem('fbe-resultados')||'{}')||{}}catch(e){}
var rutas=[].slice.call(document.querySelectorAll('.ea-ruta[data-p]'));
function guarda(){try{localStorage.setItem(K,JSON.stringify(R))}catch(e){}}
function pinta(r){var p=r.dataset.p,e=R[p]||{h:[]},bs=[].slice.call(r.querySelectorAll('.ea-hecho')),n=bs.length,he=0;
 bs.forEach(function(b,i){var on=e.h.indexOf(i)>=0;if(on)he++;b.setAttribute('aria-pressed',String(on));b.closest('li').classList.toggle('hecho',on)});
 var t=r.querySelector('.ea-prog');t.querySelector('span').textContent=he===n?'Ruta terminada':he+' de '+n+' pasos';t.querySelector('b').style.width=Math.round(he/n*100)+'%';t.classList.toggle('fin',he===n);return he===n}
rutas.forEach(function(r){var p=r.dataset.p,cam=false;R[p]=R[p]||{h:[]};
 [].forEach.call(r.querySelectorAll('.ea-hecho'),function(b,i){var u=b.dataset.u;if(res[u]&&R[p].h.indexOf(i)<0){R[p].h.push(i);cam=true}});
 if(cam){R[p].t=R[p].t||Date.now()}if(!R[p].h.length&&!R[p].t)delete R[p];pinta(r)});guarda();
document.addEventListener('click',function(e){var b=e.target.closest('.ea-hecho');if(!b)return;var r=b.closest('.ea-ruta'),p=r.dataset.p,i=+b.dataset.i;R[p]=R[p]||{h:[]};var k=R[p].h.indexOf(i);if(k>=0)R[p].h.splice(k,1);else R[p].h.push(i);R[p].t=Date.now();var fin=pinta(r);if(fin&&!R[p].ok&&window.fbe)window.fbe.toast('Ruta terminada. Buen trabajo.');R[p].ok=fin?1:0;guarda()});
})();'''
_e = open(f'{SAL}/empieza-aqui.html', encoding='utf-8').read()
if 'class="ea-hecho"' not in _e:
    def _ea_ol(m):
        n = [0]
        def li(mm):
            i = n[0]; n[0] += 1; tit = _rp.search(r'<b>(.*?)</b>', mm.group(0)); u = _rp.search(r'href="([^"]+)"', mm.group(0)).group(1)
            return mm.group(0)[:-5] + f'<button type="button" class="ea-hecho" data-i="{i}" data-u="{u}" aria-pressed="false" aria-label="Hecho: {_ha.escape(_rp.sub("<[^>]+>", "", tit.group(1)) if tit else "paso")}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></button></li>'
        cuerpo = _rp.sub(r'<li><a class="ea-paso".*?</a></li>', li, m.group(2), flags=_rp.S)
        return '<p class="ea-prog"><span></span><i aria-hidden="true"><b></b></i></p>' + m.group(1) + cuerpo + '</ol>'
    _e = _rp.sub(r'(<ol class="ea-pasos">)(.*?)</ol>', _ea_ol, _e, flags=_rp.S)
    _e = _e.replace('<script src="fbe.js"></script>', f'<script src="fbe.js"></script><script>{EA_PROG_JS}</script>', 1)
    open(f'{SAL}/empieza-aqui.html', 'w', encoding='utf-8').write(_e)

# Aviso «Instalar» también en Mi panel (el mismo de Herramientas y Mis resultados)
_pn = open(f'{SAL}/mi-panel.html', encoding='utf-8').read()
if 'class="instala' not in _pn and '<p class="pn-pie' in _pn:
    open(f'{SAL}/mi-panel.html', 'w', encoding='utf-8').write(_pn.replace('<p class="pn-pie', INSTALA + '<p class="pn-pie', 1))

# ---------------------------------------------------------------------------------------------
# 5. Buscador: Mi panel y acciones rápidas
_ACC = [('Cambiar entre tema claro y oscuro', '#accion=tema', 'modo oscuro noche dark claro luz'), ('Texto más grande', '#accion=texto-mas', 'letra tamano aumentar grande leer'),
        ('Texto a su tamaño normal', '#accion=texto-normal', 'letra tamano normal reducir pequeno'), ('Contraste alto: poner o quitar', '#accion=contraste', 'contraste accesibilidad ver'),
        ('Animaciones: poner o quitar', '#accion=quieto', 'animaciones movimiento quieto'), ('Guardar esta página en favoritos', '#accion=favorito', 'guardar favorito estrella marcar'),
        ('Compartir esta página', '#accion=compartir', 'compartir enviar enlace'), ('Empezar el chequeo de 10 minutos', 'chequeo.html', 'chequeo empezar pruebas'),
        ('Temporizador: 1 minuto', 'temporizador.html?s=60', 'descanso cronometro 60'), ('Temporizador: 1 minuto y medio', 'temporizador.html?s=90', 'descanso cronometro 90'),
        ('Temporizador: 2 minutos', 'temporizador.html?s=120', 'descanso cronometro 120'), ('Temporizador: 3 minutos', 'temporizador.html?s=180', 'descanso cronometro 180'),
        ('Apuntar mi actividad de hoy', 'semana-activa.html', 'apuntar registrar entreno semana minutos'), ('Apuntar una toma de tensión', 'tension.html', 'tension apuntar toma'),
        ('Instalar la web como app', 'ayuda.html#instalar', 'instalar app movil pantalla inicio'), ('Copia de seguridad de mis datos', 'ayuda.html#datos', 'copia seguridad exportar borrar datos privacidad')]
_idx = _jp.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_idx = [e for e in _idx if e.get('y') != 'Acción' and e.get('u') != 'mi-panel.html']
_idx += [{'t': 'Mi panel', 'u': 'mi-panel.html', 'd': 'Tu inicio personal: dónde lo dejaste, tu semana, resultados, favoritos y Mis datos.', 'k': 'panel perfil inicio favoritos logros mis datos', 'y': 'Página'}]
_idx += [{'t': t, 'u': u, 'd': 'Acción rápida', 'k': k, 'y': 'Acción'} for t, u, k in _ACC]
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(_jp.dumps(_idx, ensure_ascii=False, separators=(',', ':')))

# ---------------------------------------------------------------------------------------------
# 6. Manifiesto y service worker
_CAP = sorted(_gp.glob('app-capturas/*.jpg'))
if _CAP:
    _op.makedirs(f'{SAL}/img/app', exist_ok=True)
    for _c in _CAP: _sp.copy(_c, f'{SAL}/img/app/{_op.path.basename(_c)}')
def _cap(c):
    from PIL import Image as _Im
    w, h = _Im.open(c).size; n = _op.path.basename(c)
    return {'src': f'img/app/{n}', 'sizes': f'{w}x{h}', 'type': 'image/jpeg', 'form_factor': 'wide' if w > h else 'narrow', 'label': {'1': 'Herramientas con su fuente', '2': 'Temporizador para el gimnasio', '3': 'Mi semana activa', '4': 'Aprende, por temas', '5': 'La web en el ordenador'}.get(n[:1], 'Fuerza Basada en Evidencia')}
open(f'{SAL}/manifest.webmanifest', 'w', encoding='utf-8').write(_jp.dumps({
    'name': 'Fuerza Basada en Evidencia', 'short_name': 'FBE', 'lang': 'es', 'dir': 'ltr', 'id': './',
    'description': 'Herramientas de fuerza y salud con su fuente, temporizador, tu semana activa y los vídeos de un médico internista que también entrena. Funciona sin conexión y todo se guarda en tu dispositivo.',
    'start_url': 'mi-panel.html', 'scope': './', 'display': 'standalone', 'orientation': 'any', 'background_color': '#140B3A', 'theme_color': '#140B3A', 'categories': ['health', 'fitness', 'education'],
    'icons': [{'src': 'icono-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icono-512.png', 'sizes': '512x512', 'type': 'image/png'},
              {'src': 'icono-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
    'shortcuts': [{'name': 'Temporizador', 'url': 'temporizador.html'}, {'name': 'Mi semana activa', 'url': 'semana-activa.html'}, {'name': 'Herramientas', 'url': 'herramientas.html'}, {'name': 'Mis resultados', 'url': 'mis-resultados.html'}],
    **({'screenshots': [_cap(c) for c in _CAP]} if _CAP else {}),
}, ensure_ascii=False, indent=1))
_PRE_APP = list(dict.fromkeys(_PRE_SW + ['mi-panel.html', 'aprende.html', 'ayuda.html', 'sin-conexion.html', 'chequeo.html', 'empieza-aqui.html']))
SW_APP = SW_JS.replace("m || caches.match('herramientas.html')", "m || caches.match('sin-conexion.html')")
assert "caches.match('sin-conexion.html')" in SW_APP
_ver2 = _hp.sha1((_lee('fbe.css') + _lee('fbe.js') + _lee('buscar.json') + ''.join(_lee(u) for u in _PRE_APP if u.endswith('.html'))).encode('utf-8')).hexdigest()[:10]
open(f'{SAL}/sw.js', 'w', encoding='utf-8').write(SW_APP.replace('__V__', _ver2).replace('__PRE__', _jp.dumps(_PRE_APP)))
