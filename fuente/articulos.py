# Boletines como artículos de la web (24/11/2026). Lo ejecuta interior.py después de app.py y antes del sitemap.
# Cada archivo de articulos/*.md es un boletín ya enviado, con el texto de Pelayo tal cual salió en su versión web de
# MailerLite (leída desde su Chrome). Se quita solo lo que es de correo: el «Hola», la firma, el pie, la petición de
# responder al correo, los huecos de plantilla que se colaron en algún envío y el enlace directo al PDF de la guía
# (es para los suscriptores). Formato: cabecera entre --- (slug, fecha, u = versión web de MailerLite, titulo, corto,
# desc, video, rel, img) y el cuerpo en un markdown sencillo: párrafos, «## » títulos, «> » cita, «1. » lista numerada, «- » puntos, «### » subtítulo,
# **negrita** y [texto](enlace).
# Sale boletin-<slug>.html (subpágina del archivo del boletín) con firma, fecha, vídeo, «Pruébalo tú», invitación al
# boletín y datos para buscadores (BlogPosting). En toda la web, los enlaces a la versión de MailerLite de ese envío pasan
# a apuntar al artículo; entra en el sitemap, en el buscador (tipo «Artículo») y en Novedades no (ya está el envío).
import glob as _ag, html as _ah
def _art_lee(p):
    t = open(p, encoding='utf-8').read()
    _, cab, cuerpo = t.split('---', 2)
    m = {}
    for l in cab.strip().splitlines():
        k, v = l.split(':', 1); m[k.strip()] = v.strip()
    m['cuerpo'] = cuerpo.strip(); m['arch'] = f"boletin-{m['slug']}.html"
    m['rel'] = [x.strip() for x in m.get('rel', '').split(',') if x.strip()]
    return m
ART = sorted((_art_lee(p) for p in _ag.glob('articulos/*.md')), key=lambda a: a['fecha'], reverse=True)

def _art_inl(s):
    s = _ah.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    def _a(m):
        t, u = m.group(1), m.group(2)
        ext = u.startswith('http')
        return f'<a href="{u}"' + (' rel="noopener"' if ext else '') + f'>{t}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', _a, s)

def _art_html(md):
    out, lista = [], []
    def cierra():
        if lista: out.append('<ol class="art-lista">' + ''.join(f'<li>{_art_inl(x)}</li>' for x in lista) + '</ol>'); lista.clear()
    for b in re.split(r'\n\s*\n', md):
        b = b.strip()
        if not b: continue
        if re.match(r'\d+\.\s', b):
            for l in b.splitlines():
                l = l.strip()
                if re.match(r'\d+\.\s', l): lista.append(re.sub(r'^\d+\.\s+', '', l))
                elif lista: lista[-1] += ' ' + l
            continue
        cierra()
        if all(l.strip().startswith('- ') for l in b.splitlines()):
            out.append('<ul class="art-puntos">' + ''.join(f'<li>{_art_inl(l.strip()[2:])}</li>' for l in b.splitlines()) + '</ul>'); continue
        if b.startswith('### '): out.append(f'<h3>{_art_inl(b[4:])}</h3>')
        elif b.startswith('## '): out.append(f'<h2>{_art_inl(b[3:])}</h2>')
        elif b.startswith('> '): out.append(f'<blockquote class="art-cita"><p>{_art_inl(b[2:])}</p></blockquote>')
        else: out.append(f'<p>{_art_inl(" ".join(x.strip() for x in b.splitlines()))}</p>')
    cierra()
    return '\n'.join(out)

def _art_min(md): return max(2, round(len(re.findall(r'\w+', md)) / 200))
_ART_VID = {v['id']: v for v in json.load(open('videos.json', encoding='utf-8'))}
_ART_T = {u: (t, ic) for u, _s, ic, t, *_ in HERR_MAS}
def _art_rel(u):
    if u.startswith('http'): return ('Calcular mi número de proteína', 'balanza') if 'calculadoradeproteina' in u else (u, 'enlace')
    b = u.split('#')[0]
    if b in _ART_T: return _ART_T[b][0], _ART_T[b][1]
    for a in ART:
        if a['arch'] == b: return a.get('corto') or a['titulo'], 'libro'
    nombres = {'mitos.html': 'Mitos y evidencia', 'glosario.html': 'Glosario', 'recetas.html': 'Recetas con proteína', 'chequeo.html': 'Chequeo de 10 minutos',
               'empieza-aqui.html': 'Empieza aquí', 'pauta-activa.html': 'Pauta Activa', 'profesionales.html': 'Para profesionales sanitarios', 'medios.html': 'En los medios', 'boletin.html': 'Archivo del boletín'}
    for t in TEMAS:
        if b == f"tema-{t['id']}.html": return f"Todo sobre {t['corto'].lower()}", 'libro'
    if b == 'mitos.html' and '#' in u:
        mid = u.split('#')[1]
        for m in MITOS:
            if m[0] == mid: return f'Mito: {m[2]}', 'libro'
    return nombres.get(b, b), 'libro'

for a in ART:
    arch = a['arch']; f = a['fecha']
    corto = a.get('corto') or a['titulo']
    vid = _ART_VID.get(a.get('video', ''))
    v_html = ''
    if vid:
        v_html = (f'<a class="art-vid sube" href="videos.html#v-{vid["id"]}"><span class="art-vid-i"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg></span>'
                  f'<span><small>Te lo explico en vídeo · {vid["d"]}</small><b>{_ah.escape(vid["t"])}</b></span></a>')
    rel = ''.join(f'<li><a href="{u}"' + (' rel="noopener"' if u.startswith('http') else '') + f'>{_ah.escape(_art_rel(u)[0])}</a></li>' for u in a['rel'])
    tema = None
    for u in a['rel']:
        tema = _bc_tema(u.split('#')[0])
        if tema: break
    cuerpo = f'''<section class="art-s"><div class="in art-in">
<article class="art prosa">
{_art_html(a['cuerpo'])}
<p class="art-orig">Este texto salió en el boletín del {fecha_es(f)}. <a href="{a['u']}" rel="noopener">Ver el correo original</a>.</p>
</article>
<aside class="art-lado">{v_html}{f'<div class="art-rel sube"><p class="art-rel-t">Pruébalo tú</p><ul>{rel}</ul></div>' if rel else ''}
<p class="art-mas"><a class="enl" href="boletin.html">Todos los envíos del boletín</a></p></aside>
</div></section>
{_bc_bloque(tema)}'''
    pagina(arch, corto, a['desc'], _ah.escape(a['titulo']), f'Del boletín del {fecha_es(f)} · lectura de {_art_min(a["cuerpo"])} minutos', cuerpo,
           padre=('newsletter.html', 'Boletín'))
    p = f'{SAL}/{arch}'; h = open(p, encoding='utf-8').read()
    # miga Inicio / Boletín / Archivo / artículo, y «Anterior» al archivo
    h = h.replace('<a href="newsletter.html">Boletín</a> / ', '<a href="newsletter.html">Boletín</a> / <a href="boletin.html">Archivo</a> / ', 1)
    h = re.sub(r'(<nav class="sigue"[^>]*><div class="in"><a href=")newsletter\.html("><small>Anterior</small><b>)[^<]*', r'\1boletin.html\2Archivo del boletín', h, count=1)
    if a.get('img') and os.path.exists(f"web-img/{a['img']}.webp"):
        h = re.sub(r'<div class="marca-agua">.*?</svg></div>', ilus(a['img']), h, count=1, flags=re.S)
    fi = (f'<p class="firma">{FIRMA_FOTO}<span class="firma-t"><span class="firma-q">Por <a href="quien-soy.html">Pelayo Fernández Cidón</a>, médico internista</span>'
          f'<span class="firma-m"><span class="firma-f">Publicado el <time datetime="{f}" title="{fecha_es(f)}">{_dmy(f)}</time></span><a class="firma-e" href="evidencia.html">Cómo trabajo la evidencia</a></span></span></p>')
    h = re.sub(r'(<header class="hero mini[^>]*>.*?<p class="sub">.*?</p>)', lambda m: m.group(1) + fi, h, count=1, flags=re.S)
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': corto[:110], 'description': a['desc'], 'url': WEB + arch, 'mainEntityOfPage': WEB + arch,
          'datePublished': f, 'dateModified': f, 'inLanguage': 'es', 'author': PERSONA, 'image': WEB + 'og.png',
          'publisher': {'@type': 'Organization', 'name': 'Fuerza Basada en Evidencia', 'url': WEB, 'logo': {'@type': 'ImageObject', 'url': WEB + 'icono-512.png'}},
          'isPartOf': {'@type': 'Blog', 'name': 'Boletín de Fuerza Basada en Evidencia', 'url': WEB + 'boletin.html'}}
    h = h.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script></head>', 1)
    open(p, 'w', encoding='utf-8').write(h)

# En toda la web, el enlace a la versión de MailerLite de un envío con artículo pasa a ser el artículo
_ART_U = {a['u']: a['arch'] for a in ART}
for _f in _ag.glob(f'{SAL}/*.html'):
    if os.path.basename(_f).startswith('boletin-'): continue
    _t = open(_f, encoding='utf-8').read(); _n = _t
    for u, ar in _ART_U.items():
        if u in _n: _n = re.sub(r'href="' + re.escape(u) + r'"(\s+target="_blank")?(\s+rel="noopener")?', f'href="{ar}"', _n)
    if _n != _t: open(_f, 'w', encoding='utf-8').write(_n)
# buscador y sitemap
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_ix = [x for x in _ix if not x['u'].startswith('boletin-')]
for a in ART:
    _ix.append({'t': a.get('corto') or a['titulo'], 'u': a['arch'], 'd': a['desc'], 'k': 'boletin articulo ' + re.sub(r'[*\[\]()#>]', ' ', a['cuerpo'])[:600], 'y': 'Artículo'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
SEC_PAGS += [a['arch'] for a in ART]
print('artículos del boletín:', len(ART))
