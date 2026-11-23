# Fuentes (21/11/2026, noche): todas las referencias de la web en una página, cada una comprobada el 21/11/2026 en PubMed
# (autor, revista, año, volumen y primera página) o, si no está en PubMed, en la web oficial o por su DOI. Datos en fuentes.json.
# Lo ejecuta interior.py después de extras.py y antes de extras2.py (así entra en el sitemap, la imagen para compartir y los datos estructurados).
# «Se usa en» se calcula solo: busca el patrón (pat) de cada referencia en las listas «De dónde salen los números» de las
# herramientas, en la fuente de cada mito, en el bloque «Basada en evidencia» de la portada y en las definiciones del glosario.
# Si se cita una referencia nueva en una herramienta o un mito, hay que añadirla a fuentes.json (el generador avisa y la prueba fuentes.mjs falla).
_FU = json.load(open('fuentes.json', encoding='utf-8'))
FUENTES = _FU['fuentes']
FU_T = {  # tipo: (etiqueta, qué es)
    'meta': ('Metaanálisis o revisión sistemática', 'Junta todos los estudios sobre la misma pregunta con un método explícito.'),
    'ensayo': ('Ensayo aleatorizado', 'Compara grupos repartidos al azar. Si es pequeño o corto, la conclusión es más provisional.'),
    'obs': ('Estudio de observación o validación', 'Mide a muchas personas o comprueba que una prueba o una fórmula funciona.'),
    'guia': ('Guía, consenso o informe oficial', 'Recomendaciones de un grupo de expertos o de un organismo que revisa la evidencia.'),
    'rev': ('Revisión narrativa', 'Expertos que resumen lo publicado, sin un método sistemático.'),
    'otro': ('Libro, manual o herramienta', 'Material de referencia práctico: una tabla, una hoja de prueba, un programa.'),
}
FU_ORDEN = ['meta', 'ensayo', 'obs', 'guia', 'rev', 'otro']
_FU_RX = {f['id']: re.compile(f['pat']) for f in FUENTES}
def _fu_txt(h): return _html.unescape(re.sub(r'<[^>]+>', ' ', h))
def _fu_busca(texto):
    """Referencias citadas en un texto, en el orden en que aparecen."""
    t = _fu_txt(texto); hits = []
    for f in FUENTES:
        m = _FU_RX[f['id']].search(t)
        if m: hits.append((m.start(), f))
    return [f for _, f in sorted(hits, key=lambda x: x[0])]
def _fu_enl(f, et=''):
    """Enlaces de una referencia: PubMed y DOI, o la web oficial; et añade el año cuando hay varias juntas."""
    a = ' target="_blank" rel="noopener"'
    s = ''
    if f['pmid']: s += f'<a class="f-pm" href="https://pubmed.ncbi.nlm.nih.gov/{f["pmid"]}/"{a}>PubMed{et}</a>'
    if f['doi'] and not (et and f['pmid']): s += f'<a class="f-doi" href="https://doi.org/{f["doi"]}"{a}>DOI{et}</a>'
    if f['url']: s += f'<a class="f-web" href="{f["url"]}"{a}>{f["url_t"] or "Web oficial"}{et}</a>'
    return s
_FU_SIN = []
def _fu_decora(html_lista, et_anio=False):
    """Añade los enlaces al final de cada cita (li o párrafo)."""
    fs = _fu_busca(html_lista)
    if not fs: return html_lista, []
    multi = et_anio and len(fs) > 1
    enl = ''.join(_fu_enl(f, f' {f["a"]}' if multi and f['a'] else '') for f in fs)
    return html_lista + f'<span class="f-enl">{enl}<a class="f-ver" href="fuentes.html#f-{fs[0]["id"]}">Ficha</a></span>', fs

# ---- «Se usa en» y enlaces en las páginas que citan ----
FU_USO = {f['id']: [] for f in FUENTES}
def _fu_uso(fs, u, et):
    for f in fs:
        if (u, et) not in FU_USO[f['id']]: FU_USO[f['id']].append((u, et))
# 1. Herramientas: lista «De dónde salen los números»
for _u, _sl, _i, _t, _d in HERR_MAS:
    _p = f'{SAL}/{_u}'
    if not os.path.exists(_p): continue
    _h = open(_p, encoding='utf-8').read()
    _m = re.search(r'(<h3 class="fuentes-h sube")(>De dónde salen los números</h3>)<ol class="fuentes-t">(.*?)</ol>', _h, re.S)
    if not _m: continue
    _lis = []
    for _li in re.findall(r'<li>(.*?)</li>', _m.group(3), re.S):
        _n, _fs = _fu_decora(_li)
        if not _fs: _FU_SIN.append(f'{_u}: {_fu_txt(_li)[:90]}')
        _fu_uso(_fs, f'{_u}#fuentes', _t)
        _lis.append(f'<li>{_n}</li>')
    _nuevo = (f'{_m.group(1)} id="fuentes"{_m.group(2)}<ol class="fuentes-t">{"".join(_lis)}</ol>'
              f'<p class="f-todas"><a href="fuentes.html">Todas las fuentes de la web, comprobadas una a una</a></p>')
    open(_p, 'w', encoding='utf-8').write(_h[:_m.start()] + _nuevo + _h[_m.end():])
# 2. Mitos: el párrafo «Fuente» de cada uno (con el año en cada enlace si cita dos estudios)
_h = open(f'{SAL}/mitos.html', encoding='utf-8').read()
def _fu_mito(m):
    _id = m.group(1)
    def _p(mm):
        _n, _fs = _fu_decora(mm.group(2), et_anio=True)
        if not _fs: _FU_SIN.append(f'mitos.html#{_id}: {_fu_txt(mm.group(2))[:90]}')
        _fu_uso(_fs, f'mitos.html#{_id}', f'Mito: {MITO_CORTO.get(_id, _id)}')
        return mm.group(1) + _n + '</p>'
    return re.sub(r'(<p class="mito-fuente"><b>Fuente</b> )(.*?)</p>', _p, m.group(0), count=1, flags=re.S)
_h = re.sub(r'<article class="mito sube" id="([a-z-]+)".*?</article>', _fu_mito, _h, flags=re.S)
_h = _h.replace('<p class="sec-enl sube"><b>¿Tienes otra duda?</b>', '<p class="sec-enl sube"><b>¿Tienes otra duda?</b><a href="fuentes.html">Todas las fuentes</a>', 1)
open(f'{SAL}/mitos.html', 'w', encoding='utf-8').write(_h)
# 3. Portada: «Basada en evidencia» (ya enlaza al DOI de cada estudio)
_h = open(f'{SAL}/index.html', encoding='utf-8').read()
_m = re.search(r'<section class="ciencia( lenta)?">(.*?)</section>', _h, re.S)
assert _m, 'portada: no encuentro la sección «Basada en evidencia»'
_fu_uso(_fu_busca(_m.group(2)), 'index.html#evidencia', 'Portada: Basada en evidencia')
_blk = _m.group(0).replace('<section class="ciencia', '<section id="evidencia" class="ciencia', 1)
_blk = re.sub(r'(</article>\s*</div>)(\s*<div class="calc sube">)', r'\1\n  <p class="f-todas sube"><a href="fuentes.html">Todas las fuentes de la web, comprobadas una a una</a></p>\2', _blk, count=1)
open(f'{SAL}/index.html', 'w', encoding='utf-8').write(_h[:_m.start()] + _blk + _h[_m.end():])
# 4. Glosario: definiciones que nombran una fuente
_h = open(f'{SAL}/glosario.html', encoding='utf-8').read()
_GN = {g[0]: g[1] for g in GLOS}
for _id, _cuerpo in re.findall(r'<article class="term[^"]*" id="([^"]+)"[^>]*>(.*?)</article>', _h, re.S):
    _fu_uso(_fu_busca(_cuerpo), f'glosario.html#{_id}', f'Glosario: {_GN.get(_id, _id)}')
# 5. Herramientas y Profesionales: enlace a la página
_parchea('herramientas.html', '<a href="glosario.html">Glosario</a></p>', '<a href="glosario.html">Glosario</a><a href="fuentes.html">Fuentes</a></p>')
_h = open(f'{SAL}/profesionales.html', encoding='utf-8').read()
_a = '</div>\n</div></section>\n<section id="pacientes">'
assert _a in _h, 'profesionales: no encuentro el final de «Herramientas con la fuente al pie»'
_h = _h.replace(_a, f'</div>\n  <p class="sec-enl sube"><b>Todas juntas</b><a href="fuentes.html">Las {len(FUENTES)} fuentes de la web, comprobadas una a una</a></p>\n</div></section>\n<section id="pacientes">', 1)
open(f'{SAL}/profesionales.html', 'w', encoding='utf-8').write(_h)
import sys as _sys
for _s in _FU_SIN: print('AVISO fuentes: cita sin ficha en fuentes.json ->', _s, file=_sys.stderr)
_FU_NOUSO = [f['id'] for f in FUENTES if not FU_USO[f['id']]]
if _FU_NOUSO: print('AVISO fuentes: fichas que ya no cita ninguna página ->', ', '.join(_FU_NOUSO), file=_sys.stderr)

# ---- La página ----
SEC_SIG['fuentes.html'] = (('mitos.html', 'Mitos y evidencia'), ('glosario.html', 'Glosario'))
def _fu_orden(f): return (_norm(re.split(r'[ ,.(]', f['au'])[0]), f['a'] or 0, f['id'])
FU_L = sorted(FUENTES, key=_fu_orden)
FU_N = {k: sum(1 for f in FUENTES if f['t'] == k) for k in FU_ORDEN}
FU_PM = sum(1 for f in FUENTES if f['pmid'])
FU_HERR = len({u for L in FU_USO.values() for u, _ in L if not u.startswith(('mitos', 'index', 'glosario'))})
def _fu_ok(f):
    if f['pmid']: return '<span class="fu-ok">En PubMed</span>'
    if f['doi'] or f['url']: return '<span class="fu-ok fu-ok-w">Fuera de PubMed</span>'
    return '<span class="fu-ok fu-ok-l">Libro</span>'
def _fu_ficha(f):
    usos = FU_USO[f['id']]
    donde = ''.join(f'<a href="{u}">{et}</a>' for u, et in usos)
    q = _norm(' '.join([f['au'], f['ti'], f['rev'], FU_T[f['t']][0], f['nota'], str(f['a'] or ''), f['pmid']] + [et for _, et in usos]))
    enl = _fu_enl(f) or '<span class="f-sin">Libro: sin enlace en abierto</span>'
    anio = f'<span class="fu-a">{f["a"]}</span>' if f['a'] else ''
    lang = '' if f['id'] in ('ais', 'vivifrail2017') else ' lang="en"'
    return (f'<article class="fu sube" id="f-{f["id"]}" data-t="{f["t"]}" data-q="{_html.escape(q)}">'
            f'<div class="fu-top"><span class="fu-tipo">{FU_T[f["t"]][0]}</span>{anio}{_fu_ok(f)}</div>'
            f'<h3 class="fu-ti"{lang}>{f["ti"]}</h3>'
            f'<p class="fu-au">{f["au"]} <i>{f["rev"]}.</i></p>'
            + (f'<p class="fu-nota">{f["nota"]}</p>' if f['nota'] else '')
            + (f'<p class="fu-donde"><b>Se usa en</b>{donde}</p>' if donde else '')
            + f'<p class="fu-enl">{enl}</p></article>')
FU_JS = r"""(function(){var f=document.getElementById('fu-f'),q=document.getElementById('fu-q'),n=document.getElementById('fu-n'),L=[].slice.call(document.querySelectorAll('.fu')),t='',nada=document.getElementById('fu-nada');if(!f)return;
function norm(s){return String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function pinta(){var v=norm(q.value).trim().split(/\s+/).filter(Boolean),k=0;L.forEach(function(a){var ok=(!t||a.dataset.t===t)&&v.every(function(p){return a.dataset.q.indexOf(p)>=0});a.hidden=!ok;if(ok)k++});n.textContent=k+(k===1?' fuente':' fuentes');nada.hidden=k>0}
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(f.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b)});t=b.dataset.t;pinta()});
q.addEventListener('input',pinta);
var h=location.hash.slice(1);if(h&&h.indexOf('f-')!==0&&document.getElementById(h)===null){q.value=decodeURIComponent(h);}
var u=new URLSearchParams(location.search).get('q');if(u){q.value=u}pinta();})();"""
_FU_ESC = ESCRIBE + ('?subject=Fuentes%20de%20la%20web' if ESCRIBE.startswith('mailto:') else '')
_FU_LD = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Fuentes', 'url': WEB + 'fuentes.html', 'inLanguage': 'es',
    'about': 'Referencias científicas de las herramientas, los mitos y la portada de Fuerza Basada en Evidencia', 'dateModified': _FU['comprobado'],
    'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(FU_L), 'itemListElement': [
        {'@type': 'ListItem', 'position': k, 'item': {'@type': 'ScholarlyArticle' if f['t'] in ('meta', 'ensayo', 'obs', 'rev') else 'CreativeWork', 'name': f['ti'], 'author': f['au'].rstrip('.'),
         **({'datePublished': str(f['a'])} if f['a'] else {}), **({'sameAs': [x for x in [f'https://pubmed.ncbi.nlm.nih.gov/{f["pmid"]}/' if f['pmid'] else '', f'https://doi.org/{f["doi"]}' if f['doi'] else '', f['url']] if x]} if (f['pmid'] or f['doi'] or f['url']) else {})}}
        for k, f in enumerate(FU_L, 1)]}}, ensure_ascii=False) + '</script>'
pagina('fuentes.html', 'Fuentes', f'Las {len(FUENTES)} referencias científicas que hay detrás de las herramientas, los mitos y la portada, comprobadas una a una en PubMed o en la web oficial de quien las publica.',
       'De dónde sale cada número.', f'Las {len(FUENTES)} referencias que hay detrás de las herramientas, los mitos y la portada. Cada una, comprobada en PubMed o en la web oficial de quien la publica.', f'''
<section><div class="in">
  <ul class="fu-cif sube"><li><b>{len(FUENTES)}</b>referencias</li><li class="c-pm"><b>{FU_PM}</b>en PubMed</li><li class="c-meta"><b>{FU_N["meta"]}</b>metaanálisis o revisiones sistemáticas</li><li class="c-guia"><b>{FU_N["guia"]}</b>guías, consensos e informes</li></ul>
  <div class="hb-barra fu-barra sube"><label class="oculto" for="fu-q">Buscar una fuente</label><span class="lupa glos-busca hb-busca"><input id="fu-q" type="search" placeholder="Ej.: Schoenfeld, cafeína, 1RM" autocomplete="off"></span>
    <div class="fases claras" id="fu-f" role="group" aria-label="Filtrar por tipo de fuente"><button type="button" data-t="" aria-pressed="true">Todas<em>{len(FUENTES)}</em></button>{"".join(f'<button type="button" data-t="{k}" aria-pressed="false">{FU_T[k][0].split(" o ")[0].split(",")[0]}<em>{FU_N[k]}</em></button>' for k in FU_ORDEN if FU_N[k])}</div>
    <p class="hb-n" id="fu-n" aria-live="polite">{len(FUENTES)} fuentes</p></div>
  <h2 class="oculto">Las {len(FUENTES)} fuentes</h2>
  <div class="fu-lista" id="fu-lista">{"".join(_fu_ficha(f) for f in FU_L)}</div>
  <p class="vol-vacio hb-nada" id="fu-nada" hidden>Ninguna fuente con esa palabra. Prueba con el <button type="button" class="enl-b" onclick="window.fbeBusca&&window.fbeBusca(document.getElementById('fu-q').value)">buscador de toda la web</button>.</p>
</div></section>
<section class="hoja" id="metodo"><div class="in"><div class="entrada sube"><h2>Cómo se han comprobado</h2><p>Una por una, el {int(_FU["comprobado"][8:])} de noviembre de {_FU["comprobado"][:4]}.</p></div>
  <ol class="pasos-g en-linea sube">
    <li><b>Se busca en PubMed</b><span>Con el autor, la revista, el año, el volumen y la primera página. Si aparece, se enlaza con su número de PubMed.</span></li>
    <li><b>Se coteja con la web</b><span>Título, año, volumen y páginas tienen que coincidir con lo citado. Un estudio citado como preprint pasa a su versión publicada.</span></li>
    <li><b>Si no está en PubMed</b><span>Las guías, los libros y los informes de la OMS, la EFSA, la FAO o el NICE se enlazan a su página oficial o a su DOI.</span></li>
  </ol>
  <h3 class="mitos-sub sube">Qué es cada tipo de fuente</h3>
  <ul class="fu-leyenda sube">{"".join(f'<li class="t-{k}"><b>{FU_T[k][0]}</b><span>{FU_T[k][1]}</span></li>' for k in FU_ORDEN)}</ul>
  <p class="fu-error sube">¿Ves una cifra que no cuadra con su fuente? <a href="{_FU_ESC}">Escríbeme</a>.</p>
  <p class="sec-enl sube"><b>Sigue por aquí</b><a href="mitos.html">Mitos y evidencia</a><a href="herramientas.html">Herramientas</a><a href="glosario.html">Glosario</a></p>
</div></section>
<script>{FU_JS}</script>''', cta='<div class="cta"><a class="btn claro" href="#fu-lista">Ver las fuentes</a><a class="enl" href="#metodo">Cómo se han comprobado</a></div>',
       cierre_t=('¿Quieres un plan con esta base?', 'Cuéntame tu caso en el formulario. Te respondo yo.'), extra=_FU_LD)
SEC_PAGS += ['fuentes.html']
# Buscador: la página y cada ficha (las fichas, al final de la lista de resultados)
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_ix.append({'t': 'Fuentes', 'u': 'fuentes.html', 'd': f'Las {len(FUENTES)} referencias de la web, comprobadas en PubMed.', 'k': 'fuentes referencias estudios bibliografia pubmed evidencia', 'y': 'Página'})
for f in FU_L:
    _ix.append({'t': f['ti'], 'u': f'fuentes.html#f-{f["id"]}', 'd': f'{f["au"]} {f["rev"]}', 'k': FU_T[f['t']][0] + ' ' + ' '.join(et for _, et in FU_USO[f['id']]), 'y': 'Fuente'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
print('fuentes:', len(FUENTES), 'referencias,', FU_PM, 'en PubMed;', FU_HERR, 'herramientas las citan')
