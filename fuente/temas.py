# Cinco páginas de tema (21/11/2026, noche): todo lo de la web sobre un asunto en una sola página, como las páginas por
# tema de Examine o de Peter Attia. No añaden contenido de salud nuevo: juntan lo que ya hay (ruta de Empieza aquí,
# herramientas, mitos, glosario, guías, envíos del boletín, vídeos y fuentes) con textos cortos de enlace.
# Lo ejecuta interior.py después de fuentes.py y antes de autoria.py (que les pone la firma). Estilos al final de futuro.css («TEMAS»).
# Para cambiar qué sale en un tema, tocar su línea en TEMAS. Los envíos del boletín salen por palabras (bol), los más recientes primero.
_EA_D = {p: (t, d, xs) for p, t, d, xs in EA_PERF}
_PROG = ('programas.html', 'pesa', 'Un plan con revisión semanal', 'Un plan a tu medida dentro de la app, revisado cada semana.')
_PP = ('puesta-a-punto.html', 'check', 'Un plan hecho por un médico', 'Consulta y plan de 12 semanas, con lectura de tu analítica.')
_PAS = ('pauta-activa.html', 'capsula', 'Revisa tu medicación con Pauta Activa', 'Qué tener en cuenta con tus fármacos al hacer ejercicio, con la fuente de cada regla.')
def _paso_h(u, t=None, d=None):
    sl, i, tt, dd = HM[u]
    return (u, i, t or tt, d or dd)
TEMAS = [
    dict(id='envejecer', t='Envejecer con fuerza', corto='Envejecer con fuerza', ea='mayores',
         sub='Medir cómo estás hoy, empezar desde ahí y no perder lo que ganas. Todo lo de la web para quien tiene más de 60 años, o lo busca para sus padres.',
         herr=['test-sppb.html', 'test-silla.html', 'prension.html', 'actividad-oms.html', 'revision-medica.html', 'paron.html'],
         mitos=['sesenta', 'artrosis', 'estirar'], glos=['sarcopenia', 'sppb', 'test-silla', 'desentrenamiento', 'dosis-minima', 'cribado'], guias=[5],
         bol=['sarcopenia', 'envejec', 'longevidad', 'edad biologica', 'prension', 'mortalidad', 'morir', 'miostatina', 'mioquina', 'caida', 'mayores', 'padres', 'abuel'],
         vid=['Mayores', 'Fuerza', 'Mitos'], cta=_PP),
    dict(id='medicacion', t='Entrenar con medicación o una enfermedad crónica', corto='Medicación y enfermedad', ea='medicacion',
         sub='Antes de pensar en la intensidad, mira qué cambia tu medicación durante el ejercicio. Todo lo de la web para entrenar con un tratamiento o una enfermedad crónica.',
         herr=['revision-medica.html', 'zonas-pulso.html', 'actividad-oms.html', 'suplementos.html', 'cafeina.html'], pa=True,
         mitos=['proteina-rinon', 'creatina', 'artrosis'], glos=['betabloqueantes', 'cribado', 'borg', 'habla', 'pulso-max', 'karvonen'], guias=[5, 0],
         bol=['farmac', 'receto', 'paciente', 'diabetes', 'hospital', 'analitica', 'marcador', 'colesterol', 'lipo', 'corazon', 'tension', 'presion', 'enfermedad', 'rinon'],
         vid=['Colesterol', 'Cardio', 'Suplementos'], cta=_PP, extra=('profesionales.html', 'Si eres sanitario', 'Pauta Activa en consulta, herramientas con su fuente y recursos para tus pacientes.')),
    dict(id='dolor', t='Entrenar con dolor', corto='Dolor y molestias', ea='dolor',
         sub='Molestia no siempre significa parar. Lo importante es saber dosificar. Las herramientas, los mitos y las lecturas de la web para entrenar cuando algo duele.',
         herr=['semaforo-dolor.html', 'revision-medica.html', 'paron.html', 'volumen-semanal.html'],
         mitos=['artrosis', 'estirar', 'fallo'], glos=['control-dolor', 'tendinopatia', 'sobrecarga', 'descarga', 'rpe', 'rir'], guias=[],
         bol=['dolor', 'doler', 'duele', 'lesion', 'rodilla', 'tendon', 'tendin', 'hombro', 'molestia'],
         vid=['Fuerza', 'Mitos'], cta=_PP),
    dict(id='nutricion', t='Nutrición y suplementos', corto='Nutrición y suplementos', ea=None,
         pasos=[_paso_h('calorias.html'), (CALC, 'plato', 'Calcula tu proteína', 'Tu rango diario según tu peso y tu fase, con reparto por comidas.'), _paso_h('suplementos.html'), _PROG],
         sub='Calorías, proteína y suplementos con la evidencia delante: cuánto te toca, qué tiene pruebas y qué no. Todo lo de la web sobre comer para entrenar.',
         herr=['calorias.html', 'suplementos.html', 'cafeina.html', 'cintura-altura.html'], calc=True,
         mitos=['proteina-rinon', 'creatina', 'ayunas'], glos=['proteina', 'creatina', 'cafeina', 'ais', 'deficit', 'superavit', 'recomposicion'], guias=[1, 3, 4, 6, 8],
         bol=[], bol_t=['nutri', 'suple'], vid=['Proteína', 'Creatina', 'Suplementos', 'Alcohol', 'Perder grasa'], cta=_PROG),
    dict(id='poco-tiempo', t='Fuerza con poco tiempo', corto='Poco tiempo', ea=None,
         pasos=[('guias.html#g2', 'libro', 'Una rutina de 45 minutos o menos', 'Base de dos días por semana, ampliable a tres o cinco.'), _paso_h('paron.html'), _paso_h('volumen-semanal.html'), _PROG],
         sub='Cuando hay poco tiempo, lo que cuenta es lo mínimo que funciona. Rutinas cortas, la dosis mínima para no perder lo ganado y cómo encajarlo en tu semana.',
         herr=['paron.html', 'volumen-semanal.html', 'actividad-oms.html', 'calculadora-1rm.html'],
         mitos=['frecuencia', 'fallo'], glos=['dosis-minima', 'frecuencia', 'volumen', 'serie-trabajo', 'rir', 'desentrenamiento'], guias=[2, 0],
         bol=['sesenta minutos', '10 minutos', 'minim', 'rapid', 'habito', 'descanso entre series', 'volver al gimnasio', 'poco tiempo'],
         vid=['Fuerza', 'Cardio'], cta=_PROG),
]
TEMAS_PAGS = [f'tema-{x["id"]}.html' for x in TEMAS]
assert [u for u, _ in TEMAS_MENU] == TEMAS_PAGS, 'TEMAS_MENU (sitio-cab.py) no coincide con TEMAS (temas.py)'
_GL = {g[0]: g for g in GLOS}
_MI = {m[0]: m for m in MITOS}
def _tm_herr_pa(): return f'<a class="herr-mini" href="pauta-activa.html">{ilus("pa-vistazo", "herr-mini-img")}<b>Pauta Activa</b><span>Qué tener en cuenta con tus fármacos al hacer ejercicio, con la fuente de cada regla.</span></a>'
def _tm_herr_calc(): return f'<a class="herr-mini" href="{CALC}" rel="noopener">{ilus("web-calculadora", "herr-mini-img")}<b>Calculadora de proteína</b><span>Tu rango diario según tu peso y tu fase, con reparto por comidas.</span></a>'
def _tm_mito(i):
    m = _MI[i]
    return (f'<a class="tm-mito" data-ver="{m[3]}" href="mitos.html#{i}"><span class="tm-ver">{m[4] or MITO_VER[m[3]]}</span>'
            f'<b>«{m[2]}»</b><small>{m[5]}</small></a>')
def _tm_glos(i):
    g = _GL[i]
    return f'<a class="tm-term" href="glosario.html#{i}"><b>{g[1]}</b><span>{g[3]}</span></a>'
def _tm_guia(k):
    return f'<a class="tm-guia" href="guias.html#g{k}"><small>Guía</small><b>{G[k][0]}</b><span>{CORTA[k]}</span></a>'
def _tm_bol(x):
    if x.get('bol_t'): L = [b for b in BOL if any(t in b['t'] for t in x['bol_t'])]
    else: L = [b for b in BOL if any(w in _norm(b['tema'] + ' ' + b['asunto']) for w in x['bol'])]
    return L[:6], len(L)
def _tm_fuentes(x):
    pags = set(x['herr']) | {f'mitos.html#{i}' for i in x['mitos']}
    fs = [f for f in FU_L if any(u.split('#')[0] in pags or u in pags for u, _ in FU_USO[f['id']])]
    return fs
def _tm_dmy(iso): a, m, d = iso.split('-'); return f'{d}/{m}/{a}'
def _tm_pagina(x):
    ea = _EA_D.get(x['ea']) if x['ea'] else None
    pasos = ea[2] if ea else x['pasos']
    bol, nbol = _tm_bol(x)
    fs = _tm_fuentes(x)
    herr = (_tm_herr_pa() if x.get('pa') else '') + ''.join(_hb_tarj(u) for u in x['herr']) + (_tm_herr_calc() if x.get('calc') else '')
    otros = ''.join(f'<a href="tema-{y["id"]}.html">{y["corto"]}</a>' for y in TEMAS if y is not x)
    q_bol = (x['bol'][0] if x['bol'] else '')
    bol_html = ''
    if bol:
        bol_html = (f'<section class="hoja" id="boletin"><div class="in"><div class="entrada sube"><h2>Lo que he escrito sobre esto</h2><p>Envíos del boletín, del más reciente al más antiguo.</p></div>'
                    f'<ul class="tm-bol sube">' + ''.join(f'<li><a class="tm-b" href="{b["u"]}" target="_blank" rel="noopener"><time datetime="{b["f"]}">{_tm_dmy(b["f"])}</time><b>{_html.escape(b["asunto"])}</b><small>{_html.escape(b["tema"])}</small></a></li>' for b in bol) + '</ul>'
                    + (f'<p class="sec-enl sube"><b>Hay {nbol}</b><a href="boletin.html{"?q=" + _up.quote(q_bol) if q_bol else ""}">Ver todos en el archivo</a></p>' if nbol > len(bol) else '')
                    + '</div></section>')
    guias = ''.join(_tm_guia(k) for k in x['guias'])
    extra = f'<p class="sec-enl sube"><b>{x["extra"][1]}</b><a href="{x["extra"][0]}">{x["extra"][2]}</a></p>' if x.get('extra') else ''
    cuerpo = f'''
<section><div class="in">
  <nav class="tm-indice sube" aria-label="En esta página"><b>En esta página</b><a href="#empieza">Por dónde empezar</a><a href="#herramientas">Herramientas</a><a href="#mitos">Mitos</a><a href="#palabras">Palabras</a>{'<a href="#guias">Guías</a>' if guias else ''}{'<a href="#boletin">Boletín</a>' if bol else ''}<a href="#fuentes-tema">Fuentes</a></nav>
  <div class="entrada sube" id="empieza"><h2>Por dónde empezar</h2>{f"<p>{ea[1]}</p>" if ea else ""}</div>
  <ol class="ea-pasos tm-pasos sube">{"".join(ea_paso(n + 1, *p) for n, p in enumerate(pasos))}</ol>
  {f'<p class="sec-enl sube"><b>Es tu caso</b><a href="empieza-aqui.html#{x["ea"]}">Tu ruta en Empieza aquí</a></p>' if ea else ''}
</div></section>
<section class="hoja" id="herramientas"><div class="in"><div class="entrada sube"><h2>Herramientas</h2><p>Gratis, en tu navegador y con la fuente al pie.</p></div>
  <div class="herr-mas-rej sube">{herr}</div>{extra}
</div></section>
<section id="mitos"><div class="in"><div class="entrada sube"><h2>Mitos que conviene conocer</h2><p>Lo que dicen los estudios, con el tipo de estudio de cada respuesta.</p></div>
  <div class="tm-mitos sube">{"".join(_tm_mito(i) for i in x["mitos"])}</div>
</div></section>
<section class="hoja" id="palabras"><div class="in"><div class="entrada sube"><h2>Palabras que vas a ver</h2><p>Explicadas en dos líneas. Toca una para ir al glosario.</p></div>
  <div class="tm-terms sube">{"".join(_tm_glos(i) for i in x["glos"])}</div>
</div></section>
{f'<section id="guias"><div class="in"><div class="entrada sube"><h2>Guías para ir más lejos</h2></div><div class="tm-guias sube">{guias}</div></div></section>' if guias else ''}
{bol_html}
<section class="tm-vid" id="videos-tema"><div class="in"><div class="entrada sube"><h2>En el canal de YouTube</h2><p>Búsquedas en el canal sobre este tema.</p></div>
  <ul class="vid-temas sube">{"".join(f'<li><a href="{YT}/search?query={_up.quote(v)}" target="_blank" rel="noopener">{v}</a></li>' for v in x["vid"])}</ul>
</div></section>
<section class="hoja" id="fuentes-tema"><div class="in"><div class="entrada sube"><h2>Las fuentes de este tema</h2><p>Las {len(fs)} referencias que usan las herramientas y los mitos de esta página, comprobadas en PubMed o en la web oficial.</p></div>
  <ol class="tm-fu sube">{"".join(f'<li><a class="tm-f" href="fuentes.html#f-{f["id"]}"><span class="fu-tipo">{FU_T[f["t"]][0].split(" o ")[0].split(",")[0]}</span><b lang="en">{f["ti"]}</b><small>{f["au"]} {f["a"] or ""}</small></a></li>' for f in fs)}</ol>
  <div class="calc sube tm-cta"><div><h3>{x["cta"][2]}</h3><p>{x["cta"][3]}</p></div><div><a class="btn claro" href="{x["cta"][0]}">Ver cómo funciona</a></div></div>
  <p class="sec-enl sube tm-otros"><b>Otros temas</b>{otros}</p>
</div></section>'''
    arch = f'tema-{x["id"]}.html'
    ld = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': x['t'], 'url': WEB + arch, 'inLanguage': 'es', 'description': x['sub'],
        'hasPart': [{'@type': 'WebPage', 'url': WEB + u} for u in x['herr']] + [{'@type': 'WebPage', 'url': f'{WEB}mitos.html#{i}'} for i in x['mitos']]}, ensure_ascii=False) + '</script>'
    SEC_SIG[arch] = (('empieza-aqui.html', 'Empieza aquí'), (f'tema-{TEMAS[(TEMAS.index(x) + 1) % len(TEMAS)]["id"]}.html', TEMAS[(TEMAS.index(x) + 1) % len(TEMAS)]['corto']))
    pagina(arch, x['t'], x['sub'], x['t'] + '.', x['sub'], cuerpo, cta='<div class="cta"><a class="btn claro" href="#empieza">Por dónde empezar</a><a class="enl" href="#herramientas">Ver las herramientas</a></div>',
           cierre_t=('¿Lo vemos juntos?', 'Cuéntame tu caso en el formulario. Te respondo yo.'), extra=ld)
for _x in TEMAS: _tm_pagina(_x)
SEC_PAGS += TEMAS_PAGS
# Enlaces a los temas: menú Aprende (se hace en sitio-cab.py con TEMAS_MENU), Empieza aquí, Herramientas y portada
_EA_TEMA = {'mayores': 'envejecer', 'medicacion': 'medicacion', 'dolor': 'dolor', 'paron': 'poco-tiempo'}
_h = open(f'{SAL}/empieza-aqui.html', encoding='utf-8').read()
for _p, _t in _EA_TEMA.items():
    _a = f'<div class="ea-ruta sube" data-p="{_p}">'
    _i = _h.find(_a)
    if _i < 0: continue
    _j = _h.find('<a class="ea-volver"', _i)
    _tt = next(y for y in TEMAS if y['id'] == _t)
    _h = _h[:_j] + f'<a class="ea-tema" href="tema-{_t}.html">Todo sobre «{_tt["corto"]}»</a>' + _h[_j:]
open(f'{SAL}/empieza-aqui.html', 'w', encoding='utf-8').write(_h)
_TM_FILA = '<p class="sec-enl sube tm-fila"><b>Por tema</b>' + ''.join(f'<a href="tema-{y["id"]}.html">{y["corto"]}</a>' for y in TEMAS) + '</p>'
_parchea('herramientas.html', '<p class="herr-nota sube">', _TM_FILA + '\n  <p class="herr-nota sube">')
_parchea('mitos.html', '<p class="sec-enl sube"><b>¿Tienes otra duda?</b>', _TM_FILA + '\n  <p class="sec-enl sube"><b>¿Tienes otra duda?</b>')
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
for _x in TEMAS:
    _ix.append({'t': _x['t'], 'u': f'tema-{_x["id"]}.html', 'd': _x['sub'], 'k': 'tema ' + _x['corto'] + ' ' + ' '.join(_x['vid']), 'y': 'Página'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
print('temas:', len(TEMAS), 'páginas')
