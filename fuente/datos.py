# Datos estructurados que faltaban (M4, 21/11/2026, noche). Lo ejecuta interior.py después de extras2.py.
# Solo datos que ya están en la web: nombre, redes, logo, formación de Quién soy, hospital (como lo dio Pelayo), mitos con
# su veredicto, herramientas y recetas. El canónico de cada página ya apunta al dominio final (WEB), listo para el cambio.
# - Portada: Organization y WebSite (junto a su FAQPage).
# - Quién soy: ProfilePage con la persona (credenciales de la lista «marcas», el hospital y las redes) en lugar de la
#   Person suelta que había.
# - Mitos: cada mito como ClaimReview (afirmación, veredicto y autor).
# - Herramientas y Recetas: lista de lo que contienen.
def _ld(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>'
_ORG = {'@type': 'Organization', '@id': WEB + '#org', 'name': 'Fuerza Basada en Evidencia', 'url': WEB, 'logo': WEB + 'icono-512.png',
        'sameAs': [u for _, u in REDES], 'founder': {'@id': WEB + 'quien-soy.html#pelayo'}}
_parchea('index.html', '</head>', _ld({'@context': 'https://schema.org', '@graph': [
    _ORG, {'@type': 'WebSite', '@id': WEB + '#web', 'url': WEB, 'name': 'Fuerza Basada en Evidencia', 'inLanguage': 'es', 'publisher': {'@id': WEB + '#org'}}]}) + '</head>')
_PER = {'@type': 'Person', '@id': WEB + 'quien-soy.html#pelayo', 'name': 'Pelayo Fernández Cidón', 'url': WEB + 'quien-soy.html',
        'image': WEB + 'img/foto-pelayo.webp', 'jobTitle': 'Médico especialista en Medicina Interna y entrenador',
        'worksFor': [{'@id': WEB + '#org', '@type': 'Organization', 'name': 'Fuerza Basada en Evidencia', 'url': WEB},
                     {'@type': 'Hospital', 'name': HOSPITAL, 'address': {'@type': 'PostalAddress', 'addressLocality': 'Madrid', 'addressCountry': 'ES'}}],
        'hasCredential': [{'@type': 'EducationalOccupationalCredential', 'name': n, **({'recognizedBy': {'@type': 'CollegeOrUniversity', 'name': o}} if o else {})} for n, o in FORM_LD]
                         + [{'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'Colegiación', 'name': f'Médico colegiado n.º {COLEGIADO}', 'identifier': COLEGIADO, 'recognizedBy': {'@type': 'Organization', 'name': COLEGIO}}],
        'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': 'Universidad de Oviedo'}],
        'knowsAbout': ['Medicina interna', 'Entrenamiento de fuerza', 'Nutrición clínica', 'Ejercicio y medicación'], 'sameAs': [u for _, u in REDES]}
_p = open(f'{SAL}/quien-soy.html', encoding='utf-8').read()
assert LDP in _p, 'quien-soy: no encuentro la Person de antes'
_p = _p.replace(LDP, _ld({'@context': 'https://schema.org', '@type': 'ProfilePage', 'url': WEB + 'quien-soy.html', 'inLanguage': 'es', 'mainEntity': _PER}), 1)
open(f'{SAL}/quien-soy.html', 'w', encoding='utf-8').write(_p)
_AUT = {'@type': 'Person', 'name': 'Pelayo Fernández Cidón', 'url': WEB + 'quien-soy.html'}
_parchea('mitos.html', '</head>', _ld({'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Mitos y evidencia', 'itemListElement': [
    {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'ClaimReview', 'url': f'{WEB}mitos.html#{m[0]}', 'claimReviewed': m[2], 'author': _AUT,
                                                       'datePublished': FECHAS['mitos.html'], 'inLanguage': 'es', 'reviewRating': {'@type': 'Rating', 'alternateName': MITO_VER[m[3]]},
                                                       'itemReviewed': {'@type': 'Claim', 'name': m[2]}}} for i, m in enumerate(MITOS)]}) + '</head>')
_parchea('herramientas.html', '</head>', _ld({'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Herramientas gratuitas', 'url': WEB + 'herramientas.html', 'inLanguage': 'es',
    'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': WEB + u, 'name': t} for i, (u, sl, ic, t, d) in enumerate([('pauta-activa.html', '', '', 'Pauta Activa', '')] + list(HERR_MAS) + [('chequeo.html', '', '', 'Chequeo de 10 minutos', '')])]}}) + '</head>')
_parchea('recetas.html', '</head>', _ld({'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Recetas con proteína', 'itemListElement': [
    {'@type': 'ListItem', 'position': i + 1, 'url': f'{WEB}recetas.html#r-{r["libro"]["codigo"].replace(".", "-")}', 'name': r['nombre']} for i, r in enumerate(REC)]}) + '</head>')
