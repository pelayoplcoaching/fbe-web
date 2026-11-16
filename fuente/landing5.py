import re, json
src = open('landing4.py', encoding='utf-8').read()
src = src.replace("open('estilo4.css', encoding='utf-8').read()\")", "open('estilo4.css', encoding='utf-8').read() + open('estilo5.css', encoding='utf-8').read()\")")
src = src.replace("{open('guion4.js', encoding='utf-8').read()}\")", "{open('guion4.js', encoding='utf-8').read()}</script><script>{open('guion5.js', encoding='utf-8').read()}\")")
assert 'estilo5' in src and 'guion5' in src
src = src[:src.rindex("open('web-fbe-equipo.html'")]
exec(src)
I.update({'sol': '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/>', 'luna': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>', 'flecha': '<path d="M5 12h14M13 6l6 6-6 6"/>', 'sube': '<path d="M12 19V5M6 11l6-6 6 6"/>', 'rayo': '<path d="M13 3 5 13h6l-1 8 8-10h-6z"/>'})
# titular por líneas
for t in ('Tu plan.', 'Tu comida.', 'Tu coach.'): cambia(f'<span>{t}</span>', f'<span><b>{t}</b></span>')
cambia('<a class="btn peq claro" href="' + CONTACTO + '">Pedir plaza</a>\n  <details class="menu">', f'<button class="tema" id="tema" type="button" aria-label="Cambiar entre tema claro y oscuro"><span class="sol">{ico("sol")}</span><span class="luna">{ico("luna")}</span></button>\n  <a class="btn peq claro" href="{CONTACTO}">Pedir plaza</a>\n  <details class="menu">')
cambia('<em>Es saber qué toca hoy, y por qué.</em></p></div></section>', f'<em>Es saber qué toca hoy, y por qué.</em></p>\n  <aside class="rapido"><b>Si vas con prisa</b><ul><li>{ico("pesa")}<span><strong>Un plan a tu medida</strong>, de entrenamiento, de nutrición o de las dos cosas.</span></li><li>{ico("ojo")}<span><strong>Yo lo reviso cada semana</strong> y lo ajusto con lo que me cuentas.</span></li><li>{ico("rayo")}<span><strong>Todo en una app</strong> que se abre desde el móvil, sin instalar nada.</span></li></ul></aside></div></section>')
# portátil y chat
cambia('<div class="hilo" role="img"', '<div class="base-pc" aria-hidden="true"></div>\n    <div class="hilo" role="img"')
cambia('<div class="b co"><small>Tu coach</small>No lo quites', '<div class="tecleo" aria-hidden="true"><i></i><i></i><i></i></div><div class="b co"><small>Tu coach</small>No lo quites')
# app viva
cambia('<section>\n<div class="in">\n  <div class="entrada centro sube"><h2>Los detalles' if False else '</ul></div></section>\n\n<section><div class="in">\n  <div class="entrada centro sube"><h2>Los detalles', '</ul>\n  <div class="viva sube"><svg viewBox="0 0 180 48" aria-hidden="true"><path d="M2 40 C20 38 26 30 40 31 S62 22 78 24 S100 14 118 15 S146 8 172 6"/><circle class="pt" cx="172" cy="6" r="4"/></svg><b>Una app viva</b><span>Más de 170 actualizaciones publicadas. Lo que piden mis atletas suele estar dentro en pocos días.</span></div></div></section>\n\n<section><div class="in">\n  <div class="entrada centro sube"><h2>Los detalles')
# alternativas interactivas en la cuadrícula
a0 = html.index('<div class="caja sube"><i class="ic">' + ico('cambio')); a1 = html.index('</div>', a0) + 6
html = html[:a0] + f'<div class="caja g2 sube"><h3>Alternativas al momento</h3><p>Elige qué te ha pasado y mira el cambio.</p><div class="alt"><div class="alt-b" role="group" aria-label="Situación"><button type="button" data-a="ocupada" aria-pressed="true">Máquina ocupada</button><button type="button" data-a="casa" aria-pressed="false">Entreno en casa</button><button type="button" data-a="viaje" aria-pressed="false">Estoy de viaje</button></div><div class="alt-r"><div><small>Te tocaba</small>Press de banca con barra</div>{ico("flecha")}<div class="n" id="alt-n" aria-live="polite"><small>Misma función, otro material</small>Press con mancuernas en banco plano</div></div></div></div>' + html[a1:]
cambia('<div class="caja sube"><i class="ic">' + ico('medalla') + '</i><h3>Medallas y rachas</h3><p>Pequeños hitos para no soltarlo.</p></div>', '')
# recetas reales
rs = {r['libro']['codigo']: r for r in json.load(open('ext/recetas.json', encoding='utf-8'))}
tarj = ''
for c in ['03.17', '04.29', '04.50', '05.19', '09.01', '10.13', '11.17', '12.01', '04.a04', '03.50']:
    r = rs[c]; et = [e for e in r['etiquetas'] if e in ('vegetariana', 'vegana', 'sin gluten', 'sin lactosa')][:3]
    tarj += f'<article class="rc" data-p="{r["proteina_g"]}" data-k="{r["kcal"]}"><small>{r["libro"]["capitulo"]}</small><h3>{r["nombre"]}</h3><ul>{"".join(f"<li>{e}</li>" for e in et)}</ul><div class="mc"><div><b>{r["kcal"]}</b><span>kcal</span></div><div><b>{round(r["proteina_g"])} g</b><span>proteína</span></div><div><b>{r["minutos"]}</b><span>min</span></div></div><button type="button" aria-pressed="false">Añadir a mi día</button></article>'
RECETAS = f'''<section class="sin-arriba lenta"><div class="in"><div class="rec-cab sube"><div class="entrada" style="margin:0"><h2>Del recetario, a tu día</h2><p>Diez de las más de 500 recetas. Añade las que te comerías hoy y mira cómo se llena la proteína.</p></div>
  <div class="hoy-p" aria-live="polite"><svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="34" class="f"/><circle cx="40" cy="40" r="34" class="a"/></svg><div><b id="hoy-b">0 / 140 g</b><small id="hoy-s">Añade recetas a tu día</small></div></div></div></div>
  <div class="recetas" tabindex="0" aria-label="Recetas del recetario">{tarj}</div>
  <div class="in"><p style="color:var(--tinta-2);font-size:.9rem">El objetivo de 140 g es un ejemplo; el tuyo sale de tu plan.</p></div>
</section>

'''
cambia('<section class="ciencia">', RECETAS + '<section class="ciencia lenta">')
# llamadas dentro de la página
k = html.index('<section class="sigo">'); k0 = html.rindex('</div></section>', 0, k)
html = html[:k0] + f'<div class="llama sube"><b>¿Te ves usándola?</b><a class="btn" href="{CONTACTO}">Pedir plaza</a></div>\n' + html[k0:]
k = html.index('<section class="aprende">'); k0 = html.rindex('</div></section>', 0, k)
html = html[:k0] + f'<div class="llama sube"><b>¿Quieres un plan hecho con este criterio?</b><a class="btn" href="{CONTACTO}">Contarme tu caso</a></div>\n' + html[k0:]
# test
def preg(n, t): return f'<fieldset><legend>{t}</legend><div class="sn"><label><input type="radio" name="q{n}" value="s"><span>Sí</span></label><label><input type="radio" name="q{n}" value="n"><span>No</span></label></div></fieldset>'
TEST = f'''<section class="encaja sin-arriba"><div class="in">
  <div class="entrada centro sube"><h2>¿Encaja contigo?</h2><p>Tres preguntas, diez segundos.</p></div>
  <form class="caja-t sube" id="test" onsubmit="return false">{preg(1, '¿Puedes entrenar al menos dos días por semana?')}{preg(2, '¿Quieres que alguien revise tu semana y te diga qué cambiar?')}{preg(3, '¿Te vale ir paso a paso, sin atajos?')}
    <div class="veredicto" hidden role="status"><b></b><p></p><a class="btn" href="{CONTACTO}">Pedir plaza</a></div></form>
</div></section>

'''
cambia('<section id="dudas" class="sin-arriba">', TEST + '<section id="dudas" class="sin-arriba">')
cambia('<div class="fijo" id="fijo">', f'<a class="arriba" id="arriba" href="#inicio" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo">')
# datos estructurados y descripción
ld = {'@context': 'https://schema.org', '@graph': [
  {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
  {'@type': 'Person', 'name': 'Pelayo Fernández Cidón', 'jobTitle': 'Médico internista y entrenador', 'worksFor': {'@type': 'Organization', 'name': 'FBE · Fuerza Basada en Evidencia'}}]}
cambia('<title>Web FBE Equipo</title>', '<title>Web FBE Equipo</title>\n<meta name="description" content="Asesoría online de fuerza y nutrición con un médico internista que también entrena. Tu plan, tu comida y tu coach en una app.">\n<meta property="og:title" content="FBE · Tu plan, tu comida, tu coach">\n<meta property="og:description" content="Asesoría online de fuerza y nutrición basada en evidencia, con revisión cada semana.">\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
for s in ('<section class="espera">', '<section class="aprende">'): cambia(s, s.replace('">', ' lenta">'))
# imágenes repetidas: una sola copia
vistos = {}; n = [0]
def una(m):
    u = m.group(1)
    if u not in vistos: vistos[u] = len(vistos); return f'src="{u}" data-k="{vistos[u]}"'
    n[0] += 1; return f'src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-de="{vistos[u]}"'
html = re.sub(r'src="(data:image/webp;base64,[^"]+)"', una, html)
html = html.replace('loading="lazy" decoding="async" src="data:image/gif', 'decoding="async" src="data:image/gif')
open('web-fbe-equipo.html', 'w', encoding='utf-8').write(html); print(len(html) // 1024, 'KB', 'repetidas quitadas:', n[0])
