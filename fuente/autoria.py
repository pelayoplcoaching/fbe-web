# Firma, fecha y «Cómo trabajo la evidencia» (21/11/2026, noche). Lo ejecuta interior.py después de fuentes.py y antes de extras2.py.
# 1. evidencia.html: qué fuentes se usan, cómo se comprueban y qué no es esta web. Solo lo que ya es verdad en la web
#    (formación de Quién soy, fuentes de fuentes.json, aviso del pie). Sin declaración de conflictos de interés ni de
#    cómo se escriben los textos: eso solo lo puede decir Pelayo (pendiente de preguntarle).
# 2. Firma bajo la entradilla de las páginas de salud: autor de la web, fecha de la última actualización del contenido
#    y, si la página cita estudios, fecha de comprobación de sus fuentes. No dice «revisado por»: nadie más revisa los textos.
# FECHAS: cambiar la de una página cuando cambie su contenido (no al regenerar).
_MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
def fecha_es(iso): a, m, d = iso.split('-'); return f'{int(d)} de {_MESES[int(m) - 1]} de {a}'
FECHAS = {u: '2026-11-21' for u in [u for u, *_ in HERR_MAS] + ['pauta-activa.html', 'mitos.html', 'glosario.html', 'empieza-aqui.html', 'fuentes.html', 'profesionales.html', 'evidencia.html'] + globals().get('TEMAS_PAGS', []) + globals().get('CHQ_PAGS', [])}
PERSONA = {'@type': 'Person', 'name': 'Pelayo Fernández Cidón', 'url': WEB + 'quien-soy.html', 'jobTitle': 'Médico especialista en Medicina Interna y entrenador'}

# ---- Foto pequeña para la firma (sale de la foto real de Quién soy; si no está, la firma va sin foto) ----
_FOTO = 'web-img/foto-pelayo.webp'
FIRMA_FOTO = ''
if os.path.exists(_FOTO):
    from PIL import Image as _Im
    _f = _Im.open(_FOTO).convert('RGB'); _w, _h = _f.size; _l = round(_w * .65)
    _cx, _cy = _w // 2, round(_h * .37)
    _f.crop((_cx - _l // 2, max(0, _cy - _l // 2), _cx + _l // 2, max(0, _cy - _l // 2) + _l)).resize((112, 112), _Im.LANCZOS).save(f'{SAL}/img/firma-pelayo.webp', 'WEBP', quality=84, method=6)
    FIRMA_FOTO = '<img class="firma-foto" src="img/firma-pelayo.webp" alt="" width="56" height="56" decoding="async">'

# ---- 1. Cómo trabajo la evidencia ----
_EV_T = [(k, FU_T[k][0], FU_N[k]) for k in FU_ORDEN if FU_N[k]]
_EV_ORG = 'la OMS, el ACSM, la EFSA, el NICE, el COI y el consenso europeo de sarcopenia'
SEC_SIG['evidencia.html'] = (('quien-soy.html', 'Quién soy'), ('fuentes.html', 'Fuentes'))
pagina('evidencia.html', 'Cómo trabajo la evidencia', 'Qué fuentes usa la web de Fuerza Basada en Evidencia, cómo se comprueba cada cifra y qué no es esta web.',
       'Cómo trabajo la evidencia.', 'Qué fuentes uso, cómo compruebo cada cifra y qué no es esta web. Para que sepas de dónde sale lo que lees y lo que calculas aquí.', f'''
<section><div class="in dos">
  <div class="sube"><div class="entrada"><h2>Quién está detrás</h2><p>Esta web es mía. Soy Pelayo Fernández Cidón, médico especialista en Medicina Interna y entrenador.</p></div>
    <ul class="marcas"><li>Especialista en Medicina Interna</li><li>Experto universitario en entrenamiento de fuerza</li><li>Máster en nutrición clínica</li><li>Más de 15 años entrenando fuerza</li></ul>
    <p class="sec-enl"><b>Más sobre mí</b><a href="quien-soy.html">Quién soy</a><a href="medios.html">En los medios</a></p></div>
  <aside class="ev-foto sube">{ilus("foto-pelayo", "ev-retrato") if os.path.exists(_FOTO) else ""}</aside>
</div></section>
<section class="hoja" id="cifras"><div class="in"><div class="entrada sube"><h2>De dónde salen las cifras</h2><p>Cada número de las herramientas, de los mitos y de la portada lleva su fuente al pie. Están todas juntas, {len(FUENTES)}, en <a href="fuentes.html">Fuentes</a>.</p></div>
  <ul class="ev-tipos sube">{"".join(f'<li class="t-{k}"><b>{n}</b><span>{t}</span></li>' for k, t, n in _EV_T)}</ul>
  <div class="ev-dos sube">
    <div><h3>Primero, lo que junta muchos estudios</h3><p>Un metaanálisis o una revisión sistemática pesa más que un estudio suelto. Cuando hay donde elegir, la cifra sale de ahí.</p></div>
    <div><h3>Después, las guías de quien revisa toda la evidencia</h3><p>Para límites y recomendaciones uso las guías y los consensos de {_EV_ORG}.</p></div>
    <div><h3>Y la fuente, siempre a la vista</h3><p>Una cifra y su fuente van juntas. Si cambia una, cambia la otra.</p></div>
  </div>
</div></section>
<section id="comprobar"><div class="in"><div class="entrada sube"><h2>Cómo compruebo cada fuente</h2><p>Las {len(FUENTES)}, una por una, el {fecha_es(_FU["comprobado"])}.</p></div>
  <ol class="pasos-g en-linea sube">
    <li><b>Se busca en PubMed</b><span>Con el autor, la revista, el año, el volumen y la primera página. {FU_PM} de las {len(FUENTES)} están en PubMed y se enlazan con su número.</span></li>
    <li><b>Se coteja con la web</b><span>Título, año, volumen y páginas tienen que coincidir con lo citado. Un estudio citado como preprint pasa a su versión publicada.</span></li>
    <li><b>Si no está en PubMed</b><span>Las guías, los libros y los informes se enlazan a la página oficial de quien los publica o a su DOI.</span></li>
  </ol>
  <p class="ev-ej sube"><b>Un ejemplo de este mes:</b> el análisis de Pelland y cols. sobre cuántas series hacer se citaba como preprint (2024). Ya está publicado en Sports Medicine y la web cita esa versión, que mantiene el recuento que usa el <a href="volumen-semanal.html">contador de volumen</a>.</p>
  <p class="sec-enl sube"><b>Compruébalo tú</b><a href="fuentes.html">Las {len(FUENTES)} fuentes</a><a href="mitos.html">Mitos y evidencia</a></p>
</div></section>
<section class="hoja" id="limites"><div class="in"><div class="entrada sube"><h2>Qué no es esta web</h2></div>
  <ul class="ev-no sube">
    <li><b>No sustituye a tu médico</b><span>Ni la web ni la asesoría sustituyen a tu médico ni a un tratamiento.</span></li>
    <li><b>Las herramientas no diagnostican</b><span>Estiman y orientan. Úsalas para saber por dónde empezar y para ver si progresas.</span></li>
    <li><b>Lo que calculas es tuyo</b><span>Las calculadoras funcionan en tu navegador: lo que escribes no se envía a ningún sitio.</span></li>
    <li><b>Si tomas medicación o tienes una enfermedad</b><span>Empieza por el <a href="revision-medica.html">cribado de revisión médica</a> o por <a href="pauta-activa.html">Pauta Activa</a>.</span></li>
  </ul>
  <p class="fu-error sube">¿Ves una cifra que no cuadra con su fuente, o un error? <a href="{_FU_ESC}">Escríbeme</a>.</p>
</div></section>''', cta='<div class="cta"><a class="btn claro" href="#cifras">De dónde salen las cifras</a><a class="enl" href="fuentes.html">Ver las fuentes</a></div>',
       cierre_t=('¿Quieres un plan hecho así?', 'Cuéntame tu caso en el formulario. Te respondo yo.'))
SEC_PAGS += ['evidencia.html']
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_ix.append({'t': 'Cómo trabajo la evidencia', 'u': 'evidencia.html', 'd': 'Qué fuentes uso, cómo compruebo cada cifra y qué no es esta web.', 'k': 'evidencia metodo fuentes politica editorial quien escribe', 'y': 'Página'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
_parchea('quien-soy.html', '<a href="medios.html">Prensa, podcasts y formación</a></p>', '<a href="medios.html">Prensa, podcasts y formación</a><b>Mi método</b><a href="evidencia.html">Cómo trabajo la evidencia</a></p>')
_parchea('fuentes.html', '<p class="sec-enl sube"><b>Sigue por aquí</b>', '<p class="sec-enl sube"><b>Sigue por aquí</b><a href="evidencia.html">Cómo trabajo la evidencia</a>')

# ---- 2. Firma en las páginas de salud ----
def _dmy(iso): a, m, d = iso.split('-'); return f'{d}/{m}/{a}'
def firma(arch, fuentes_f=None):
    f = FECHAS[arch]
    fu = f'<a class="firma-c" href="{fuentes_f}" title="Comprobadas en PubMed el {fecha_es(_FU["comprobado"])}">Fuentes comprobadas</a>' if fuentes_f else ''
    return (f'<p class="firma">{FIRMA_FOTO}<span class="firma-t"><span class="firma-q">Por <a href="quien-soy.html">Pelayo Fernández Cidón</a>, médico internista</span>'
            f'<span class="firma-m"><span class="firma-f">Actualizado el <time datetime="{f}" title="{fecha_es(f)}">{_dmy(f)}</time></span>{fu}{"" if arch == "evidencia.html" else '<a class="firma-e" href="evidencia.html">Cómo trabajo la evidencia</a>'}</span></span></p>')
_FI_N = 0
for _a in FECHAS:
    _p = f'{SAL}/{_a}'
    if not os.path.exists(_p): continue
    _h = open(_p, encoding='utf-8').read()
    _ff = '#fuentes' if 'class="fuentes-t"' in _h else ('#lista' if _a == 'mitos.html' else ('#fu-lista' if _a == 'fuentes.html' else ('#fuentes-tema' if 'id="fuentes-tema"' in _h else ('#chq-por' if 'id="chq-por"' in _h else None))))
    _m = re.search(r'(<header class="hero mini[^>]*>.*?<p class="sub">.*?</p>)', _h, re.S)
    if not _m: continue
    _ld = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'WebPage', 'url': WEB + _a, 'inLanguage': 'es', 'dateModified': FECHAS[_a], 'author': PERSONA,
        'publisher': {'@type': 'Organization', 'name': 'Fuerza Basada en Evidencia', 'url': WEB}}, ensure_ascii=False) + '</script>'
    _h = _h[:_m.end()] + firma(_a, _ff) + _h[_m.end():]
    _h = _h.replace('</head>', _ld + '</head>', 1)
    open(_p, 'w', encoding='utf-8').write(_h); _FI_N += 1
print('firma:', _FI_N, 'páginas')
