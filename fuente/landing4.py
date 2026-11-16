import re
src = open('landing3.py', encoding='utf-8').read()
src = src.replace("css = open('estilo3.css', encoding='utf-8').read()", "css = open('estilo3.css', encoding='utf-8').read() + open('estilo4.css', encoding='utf-8').read()")
src = src.replace("{open('guion3.js', encoding='utf-8').read()}", "{open('guion3.js', encoding='utf-8').read()}</script><script>{open('guion4.js', encoding='utf-8').read()}")
src = src[:src.rindex("open('web-fbe-equipo.html'")]
exec(src)
lt = open('ext/lobo-trazo.js', encoding='utf-8').read()
CAJA = re.search(r"LOBO_CAJA = '([^']+)'", lt).group(1); LD = re.search(r"LOBO_D = '([^']+)'", lt).group(1)
LOBO = f'<svg class="lobo" viewBox="{CAJA}" aria-hidden="true"><path fill-rule="evenodd" d="{LD}"/></svg>'
def cambia(a, b, n=1):
    global html
    assert html.count(a) >= 1, a[:80]
    html = html.replace(a, b, n)
cambia('<a class="logo" href="#inicio"><i>FBE</i>', f'<a class="logo" href="#inicio"><i>{LOBO}</i>')
cambia("<div class=\"avance\"", '<a class="salto" href="#semana">Saltar al contenido</a>\n<div class="avance"')
# portada
i = html.index('<div class="tel" id="tel">'); j = html.index('</div>', i) + 6
pases = [('hoy', 'Pantalla de inicio de la app: la sesión de hoy, el aviso del coach y los anillos del día'), ('portada', 'Portada de la sesión de hoy'), ('sesion', 'Sesión en marcha, serie a serie'), ('descanso', 'Descanso entre series con cuenta atrás')]
tel = '<div class="tel atras" aria-hidden="true"><img src="' + img('hoy-oscuro') + '" width="702" height="1519" alt=""></div><div class="tel" id="tel">' + ''.join(f'<img class="pase{" on" if k == 0 else ""}" src="{img(n)}" width="702" height="1519" alt="{a}"{"" if k == 0 else " aria-hidden=\"true\""}>' for k, (n, a) in enumerate(pases)) + '<div class="puntos" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i></div></div>'
html = html[:i] + tel + html[j:]
cambia('<p class="sub">', '<div class="metas" role="group" aria-label="Qué buscas"><span>¿Qué buscas?</span><button type="button" data-m="fuerza" aria-pressed="false">Ganar fuerza</button><button type="button" data-m="grasa" aria-pressed="false">Perder grasa</button><button type="button" data-m="cero" aria-pressed="false">Empezar de cero</button><button type="button" data-m="volver" aria-pressed="false">Volver tras un parón</button></div>\n    <p class="sub" id="sub" aria-live="polite">')
cambia('<b>Tu coach</b>Si notas el hombro, cambia el press militar por press con mancuernas sentado.</div>', '<b>Tu coach</b><span id="escribe">Si notas el hombro, cambia el press militar por press con mancuernas sentado.</span></div>')
PAL = ['Fuerza', 'Hipertrofia', 'Pérdida de grasa', 'Nutrición flexible', 'Técnica', 'Descarga', 'Sueño', 'Constancia', 'Evidencia']
ul = '<ul>' + ''.join(f'<li>{p}</li>' for p in PAL) + '</ul>'
cambia('\n\n<section class="lema">', f'\n<div class="cinta" aria-hidden="true"><div>{ul}{ul}{ul}{ul}</div></div>\n\n<section class="lema">')
PRUEBA = f'''<section class="prueba"><div class="in">
  <div class="sube"><h2>Pruébalo aquí mismo</h2><p class="t">Así se apunta una serie en la app. Cambia los kilos o las repeticiones y márcala como hecha.</p>
    <ol class="ayuda"><li>Marca la primera serie: el descanso arranca solo.</li><li>Sube los kilos o las repeticiones en otra.</li><li>Si mueves más que la vez anterior, la app lo celebra.</li></ol></div>
  <div class="sesion sube" id="sesion" aria-label="Demostración de una sesión">
    <div class="brindis" role="status">{ico('medalla')}Récord en press inclinado</div><div class="conf" aria-hidden="true">{'<i></i>' * 18}</div>
    <header><h3>Press inclinado con mancuernas</h3><small>Torso B</small></header><p class="pauta">3 series · 8–10 repeticiones · la última vez: 16 kg × 10</p>
    {''.join(f'<div class="serie"><span>{n}</span><label><small>kg</small><input inputmode="decimal" value="{kg}" aria-label="Kilos de la serie {n}"></label><label><small>reps</small><input inputmode="numeric" value="10" aria-label="Repeticiones de la serie {n}"></label><button type="button" aria-pressed="false" aria-label="Marcar la serie {n} como hecha">{ico("si")}</button></div>' for n, kg in ((1, 16), (2, 16), (3, 17)))}
    <div class="desc" hidden><svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="34" class="f"/><circle cx="40" cy="40" r="34" class="a"/></svg><div><b>0:12</b><small>Descanso (aquí, acortado)</small></div><button type="button">Saltar</button></div>
    <div class="fin" hidden><div><b>Sesión apuntada</b><small>En la app, esto me llega a mí al momento.</small></div><button type="button">Repetir</button></div>
  </div>
</div></section>'''
cambia('</div></div>\n  </div>\n</div></section>\n\n<section id="app" class="hoja">', '</div></div>\n  </div>\n  <div class="tour-puntos" aria-hidden="true">' + '<i></i>' * 6 + '</div>\n</div></section>\n\n' + PRUEBA + '\n\n<section id="app" class="hoja">')
# panel del coach con puntos
k = html.index('alt="Panel del coach'); i = html.rindex('<img', 0, k); j = html.index('>', k) + 1
html = html[:i] + '<div class="pos">' + html[i:j] + '<span class="pin" style="left:38.5%;top:35%" aria-hidden="true">1</span><span class="pin" style="left:22%;top:47%" aria-hidden="true">2</span><span class="pin" style="left:41%;top:47%" aria-hidden="true">3</span></div>' + html[j:]
cambia('<ul class="tres sube"><li><i>', '<ol class="leyenda sube"><li><b>1</b>Cuántas sesiones llevas esta semana</li><li><b>2</b>Si has apuntado una molestia, y cuánto</li><li><b>3</b>Si ya me has enviado el check-in</li></ol>\n  <ul class="tres sube"><li><i>')
FL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m{0}"/></svg>'
cambia('<div class="entrada sube" style="margin-bottom:1rem"><h2>Y todavía hay más</h2></div>', '<div class="entrada gal-cab sube" style="margin-bottom:1rem;max-width:none;grid-template-columns:1fr auto"><h2>Y todavía hay más</h2><div class="gal-btn"><button type="button" data-d="ant" aria-label="Pantallas anteriores">' + FL.format('15 6-6 6 6 6') + '</button><button type="button" data-d="sig" aria-label="Pantallas siguientes">' + FL.format('9 6 6 6-6 6') + '</button></div></div>')
CIENCIA = f'''<section class="ciencia"><div class="in">
  <div class="entrada sube"><h2>Basada en evidencia, de verdad</h2><p>Tres ideas que están detrás de cada plan, con el estudio que las sostiene. Sin dogmas: si la evidencia cambia, cambia el plan.</p></div>
  <div class="rej">
    <article class="idea sube"><span class="n">01</span><h3>El volumen se dosifica</h3><p>Más series semanales por músculo dan más ganancia, de forma gradual. Por eso tu volumen sube poco a poco y se descarga cuando toca.</p><a href="https://doi.org/10.1080/02640414.2016.1210197" target="_blank" rel="noopener">Schoenfeld, Ogborn y Krieger. J Sports Sci. 2017;35(11):1073-82.</a></article>
    <article class="idea sube"><span class="n">02</span><h3>No todo va al fallo</h3><p>La fuerza mejora parecido en un rango amplio de esfuerzo; el músculo, algo más cerca del fallo. Por eso cada serie lleva su esfuerzo objetivo.</p><a href="https://doi.org/10.1007/s40279-024-02069-2" target="_blank" rel="noopener">Robinson y cols. Sports Med. 2024;54(9):2209-31.</a></article>
    <article class="idea sube"><span class="n">03</span><h3>Proteína: la suficiente</h3><p>Por encima de unos 1,6 g por kilo y día, suplementar más proteína no añade masa magra. Suficiente, no infinita.</p><a href="https://doi.org/10.1136/bjsports-2017-097608" target="_blank" rel="noopener">Morton y cols. Br J Sports Med. 2018;52(6):376-84.</a></article>
  </div>
  <div class="calc sube"><div><h3>¿Cuánta proteína te toca?</h3><p>Mueve el peso y mira el rango que se usa como referencia al entrenar fuerza: de 1,6 a 2,2 g por kilo y día.</p><small>Orientativo, para adultos sanos que entrenan fuerza. Si tienes enfermedad renal u otra patología, consulta antes con tu médico.</small></div>
    <div><label for="peso">Tu peso <output id="peso-o" for="peso">75 kg</output></label><input type="range" id="peso" min="45" max="130" step="1" value="75"><div class="res"><div><b id="prot">120–165 g</b><span>de proteína al día</span></div><div><b id="toma">30–40 g</b><span>por comida, en cuatro tomas</span></div></div></div></div>
</div></section>

'''
cambia('<section class="aprende">', CIENCIA + '<section class="aprende">')
ESPERA = '''<section class="espera"><div class="in">
  <div class="entrada sube"><h2>Qué puedes esperar</h2><p>Sin promesas de antes y después. Esto es lo que suele pasar cuando se hace bien.</p></div>
  <ol>
    <li class="sube"><small>Semana 1</small><h3>Aprendes el camino</h3><p>La app, los ejercicios y tu menú. Cargas cómodas y la técnica por delante.</p></li>
    <li class="sube"><small>Mes 1</small><h3>La rutina ya es tuya</h3><p>Primeras subidas de carga, el menú rodando y los check-ins con datos para ajustar.</p></li>
    <li class="sube"><small>Mes 3</small><h3>Cierras tu primer bloque</h3><p>Miramos tus números, tus fotos si quieres, y decidimos juntos el siguiente.</p></li>
  </ol>
</div></section>

'''
cambia('<section id="quien">', ESPERA + '<section id="quien" class="sin-arriba">')
cambia('<section class="cierre">', f'<section class="cierre"><div class="marca-agua">{LOBO}</div>')
cambia('<li>' + ico('si') + 'Sin compromiso</li></ul></div></section>', '<li>' + ico('si') + 'Sin compromiso</li></ul>\n  <ol class="luego"><li><b>Rellenas el formulario</b>Qué buscas y cómo entrenas ahora.</li><li><b>Te escribo yo</b>Con lo que te propondría y lo que cuesta.</li><li><b>Decides tú</b>Sin compromiso y sin prisa.</li></ol></div></section>')
cambia('<div><b>FBE · Fuerza Basada en Evidencia</b><p>', f'<div><div class="marca"><i>{LOBO}</i>Fuerza Basada en Evidencia</div><p>')
cambia('</div></footer>', '<div class="legal"><span>© 2026 FBE · Fuerza Basada en Evidencia</span><span>Las pantallas son de la app real, con atletas de ejemplo.</span></div>\n</div></footer>')
cambia(f'<div class="fijo" id="fijo"><a class="btn claro" href="{CONTACTO}">Pedir plaza</a></div>', f'<div class="fijo" id="fijo"><a class="sec" href="#semana">Ver la app</a><a class="btn claro" href="{CONTACTO}">Pedir plaza</a></div>')
html = html.replace('loading="lazy" ', 'loading="lazy" decoding="async" ')
open('web-fbe-equipo.html', 'w', encoding='utf-8').write(html); print(len(html) // 1024, 'KB')
