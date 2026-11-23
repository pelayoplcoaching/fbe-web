import base64, re
exec(open('landing2.py', encoding='utf-8').read().split("def ico(n)")[0].split('I = {', 1)[0])   # img(), CONTACTO, APP
def img(n): return 'data:image/webp;base64,' + base64.b64encode(open('w3/' + n + '.webp', 'rb').read()).decode()
I = {
 'video': '<path d="M4 6h11v12H4z"/><path d="m15 10 5-3v10l-5-3"/>', 'cambio': '<path d="M4 8h13l-3-3"/><path d="M20 16H7l3 3"/>',
 'reloj': '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>', 'grafica': '<path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/>',
 'check': '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="m8 12 3 3 5-6"/>', 'plato': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/>',
 'cesta': '<path d="M5 9h14l-1.5 10h-11z"/><path d="M9 9l3-5 3 5"/>', 'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
 'medalla': '<circle cx="12" cy="14" r="5"/><path d="M9 9 7 3h10l-2 6"/>', 'casa': '<path d="M4 11 12 4l8 7"/><path d="M6 10v9h12v-9"/>',
 'candado': '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>', 'libro': '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>',
 'camara': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>', 'pesa': '<path d="M3 10v4M6 7v10M18 7v10M21 10v4M6 12h12"/>',
 'ojo': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>', 'baja': '<path d="M12 4v11"/><path d="m7 11 5 5 5-5"/><path d="M5 20h14"/>',
 'si': '<path d="m5 12 4.5 4.5L19 7"/>', 'no': '<path d="M6 6l12 12M18 6 6 18"/>', 'medio': '<path d="M6 12h12"/>',
}
def ico(n): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'
ANILLOS = '<svg class="anillos" viewBox="0 0 600 600" aria-hidden="true">' + ''.join(f'<circle cx="300" cy="300" r="{r}"/>' for r in (60, 110, 165, 225, 290)) + '<circle class="punto" cx="465" cy="300" r="7"/><circle class="punto p2" cx="300" cy="75" r="5"/></svg>'
def m(n, alt, lazy=True, cls=''): return f'<div class="m {cls}"><img {"loading=\"lazy\" " if lazy else ""}src="{img(n)}" width="702" height="1519" alt="{alt}"></div>'

TOUR = [('semana', 'Lunes', 'Tu semana, ya montada', 'Abres la app y está todo: qué días entrenas, qué toca en cada uno y la nota que te he dejado.', 'Pantalla de la semana con las sesiones de cada día'),
 ('sesion', 'Entrenas', 'Apuntas cada serie en dos toques', 'Kilos, repeticiones y esfuerzo. La app recuerda lo de la semana pasada y te avisa cuando bates un récord.', 'Sesión en marcha con las series apuntadas'),
 ('descanso', 'Descansas', 'El descanso arranca solo', 'Marcas la serie y empieza la cuenta atrás, con lo que viene después a la vista. Sin mirar el reloj.', 'Temporizador de descanso entre series'),
 ('comidas', 'Comes', 'Sabes cuánto llevas y cuánto te queda', 'Calorías y proteína del día, tu menú de la semana y la lista de la compra hecha.', 'Pantalla de comidas con calorías, proteína y el menú del día'),
 ('check-in', 'Domingo', 'Me cuentas la semana en dos minutos', 'Sueño, energía, hambre, molestias. Es lo que leo antes de decidir tu semana siguiente.', 'Check-in semanal con las respuestas del atleta'),
 ('progreso', 'Y avanzas', 'El progreso, a la vista', 'Peso, fuerza, tonelaje y racha de semanas, en gráficas que se entienden sin hacer cuentas.', 'Pantalla de progreso con peso, récords y racha')]
GUIAS = ['Tipos de rutina', 'La semana de descarga', 'Volver tras un parón', 'Cardio y fuerza', 'Qué hacer si te estancas', 'Dieta flexible', 'Composición corporal', 'Suplementación', 'Sueño', 'Motivación', 'Salud cardiometabólica', 'Colesterol y lípidos', 'Entrenamiento y mujer', 'Mitos del fitness']
COMPARA = [('Plan hecho para ti, no una plantilla', 'si', 'no', 'medio'), ('Alguien revisa tu semana y la ajusta', 'si', 'no', 'no'), ('Un médico detrás de las decisiones', 'si', 'no', 'no'),
 ('Registro serie a serie con descansos', 'si', 'si', 'no'), ('Entrenamiento y nutrición en el mismo sitio', 'si', 'medio', 'medio'), ('Corrección de tu técnica en vídeo', 'si', 'no', 'no'), ('Se adapta si viajas, te lesionas o cambia tu horario', 'si', 'no', 'no')]
faq = [('¿Necesito ir a un gimnasio?', 'No es obligatorio. Programo para gimnasio, para casa con poco material o para una mezcla de los dos, y la app te propone alternativas si un día no tienes lo que toca.'),
 ('¿Cuánto tiempo necesito a la semana?', 'El que tengas. El plan se monta sobre tus días y tus minutos reales, no al revés; y si un día vas justo, la sesión se recorta por lo menos importante.'),
 ('¿Puedo apuntarme solo a la nutrición, o solo al entrenamiento?', 'Sí. Hay atletas que solo llevan entrenamiento, otros solo nutrición y otros las dos cosas. La app enseña únicamente lo que tengas contratado.'),
 ('Nunca he entrenado fuerza. ¿Es para mí?', 'Sí. Cada ejercicio lleva su vídeo y su explicación, empezamos con cargas que puedas controlar y me puedes mandar vídeo de tu técnica para que te la corrija.'),
 ('¿Tengo que descargar algo?', 'No hace falta ir a ninguna tienda de aplicaciones. La app se abre desde el navegador del móvil y se añade a la pantalla de inicio en dos toques; funciona en iPhone y en Android.'),
 ('Tomo medicación o tengo una lesión. ¿Puedo entrenar?', 'En la mayoría de los casos sí, y adaptarlo es parte del trabajo. Lo vemos en la valoración inicial. La asesoría no sustituye a tu médico ni a tu tratamiento.'),
 ('¿Qué pasa con mis fotos y mis datos de salud?', 'Solo se guardan con tu permiso, solo los vemos tú y yo, y puedes descargar todo lo tuyo desde la propia app.'),
 ('¿Cuánto cuesta?', f'Depende de si quieres entrenamiento, nutrición o las dos cosas. Desde {DESDE} € al trimestre. Te lo detallo al responder a tu formulario, sin compromiso.')]
def marca(v): return {'si': f'<span class="v si">{ico("si")}<b>Sí</b></span>', 'no': f'<span class="v no">{ico("no")}<b>No</b></span>', 'medio': f'<span class="v me">{ico("medio")}<b>A medias</b></span>'}[v]
def anillo(pct, color, txt, sub): 
    c = 2 * 3.1416 * 34
    return f'<div class="an"><svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="34" class="f"/><circle cx="40" cy="40" r="34" class="a" style="stroke:{color};stroke-dasharray:{c:.1f};--fin:{c * (1 - pct):.1f}"/></svg><strong>{txt}</strong><span>{sub}</span></div>'

css = open('estilo3.css', encoding='utf-8').read()
html = f'''<meta name="claude:viewport-fit-sides" content="cover">
<title>Web FBE Equipo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap">
<style>{css}</style>
<script>document.documentElement.classList.add('js');</script>
<div class="avance" aria-hidden="true"><i id="avance"></i></div>
<div class="cab"><div class="in">
  <a class="logo" href="#inicio"><i>FBE</i><span>Fuerza Basada en Evidencia</span></a>
  <nav aria-label="Secciones" id="nav"><a href="#semana">Tu semana</a><a href="#app">La app</a><a href="#como">Cómo empezamos</a><a href="#quien">Quién te lleva</a><a href="#dudas">Dudas</a></nav>
  <a class="btn peq claro" href="{CONTACTO}">Pedir plaza</a>
  <details class="menu"><summary aria-label="Abrir el menú"><span></span></summary><div><a href="#semana">Tu semana</a><a href="#app">La app</a><a href="#como">Cómo empezamos</a><a href="#quien">Quién te lleva</a><a href="#dudas">Dudas</a><a href="{APP}">Ya soy atleta: entrar</a></div></details>
</div></div>

<header class="hero" id="inicio">{ANILLOS}<div class="in">
  <div class="txt">
    <p class="sobre"><i></i>Asesoría online de fuerza y nutrición</p>
    <h1><span>Tu plan.</span><span>Tu comida.</span><span>Tu coach.</span></h1>
    <p class="sub">Soy médico internista y también entreno. Cada semana sabes qué toca, lo apuntas en el móvil y yo lo reviso y lo ajusto.</p>
    <div class="cta"><a class="btn claro" href="{CONTACTO}">Pedir plaza</a><a class="enl" href="#semana">Ver la app por dentro</a></div>
    <p class="nota-cta">Sin compromiso: primero hablamos y vemos si encaja.</p>
  </div>
  <div class="escena" id="escena">
    <div class="tel" id="tel"><img src="{img('hoy')}" width="702" height="1519" alt="Pantalla de inicio de la app: la sesión de hoy, el aviso del coach y los anillos de constancia, carga, comida y sueño"></div>
    <div class="flota a" aria-hidden="true"><b>Tu coach</b>Si notas el hombro, cambia el press militar por press con mancuernas sentado.</div>
    <div class="flota b" aria-hidden="true"><b>Racha</b><strong>3 semanas</strong>completas seguidas</div>
    <div class="flota c" aria-hidden="true"><i>{ico('medalla')}</i><span><b>Récord</b>Press inclinado · 17 kg × 10</span></div>
  </div>
</div></header>

<div class="franja"><div class="in"><ul>
  <li><b>Médico internista</b><span>Hospital Universitario La Paz, Madrid</span></li>
  <li><b>Más de 15 años</b><span>entrenando fuerza</span></li>
  <li><b>Desde 2020</b><span>llevando atletas en FBE</span></li>
</ul></div></div>

<section class="lema"><div class="in sube"><p>Entrenar bien no es hacer más.<br><em>Es saber qué toca hoy, y por qué.</em></p></div></section>

<section id="semana" class="sin-arriba"><div class="in">
  <div class="entrada sube"><h2>Una semana con la app</h2><p>Recorre cada momento y mira cómo cambia la pantalla. Son capturas de la app real, con atletas de ejemplo.</p></div>
  <div class="tour sube">
    <div class="tour-lista" role="tablist" aria-label="Momentos de la semana">{''.join(f'<button role="tab" id="t{i}" aria-controls="p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><small>{d}</small><b>{t}</b><span>{x}</span></button>' for i, (_, d, t, x, _a) in enumerate(TOUR))}</div>
    <div class="tour-tel"><div class="tel plano">{''.join(f'<img id="p{i}" role="tabpanel" aria-labelledby="t{i}" {"" if i == 0 else "hidden "}loading="lazy" src="{img(k)}" width="702" height="1519" alt="{a}">' for i, (k, _d, _t, _x, a) in enumerate(TOUR))}</div></div>
  </div>
</div></section>

<section id="app" class="hoja"><div class="in">
  <div class="entrada sube"><h2>Hecha para que lo cumplas</h2><p>No es una plantilla en PDF ni un grupo de mensajes. Es una app pensada para mis atletas, y se nota en los detalles.</p></div>
  <div class="fila sube"><div class="pant">{m('portada', 'Portada de la sesión Torso B con duración, ejercicios y la nota del coach')}{m('fuerza', 'Gráficas de fuerza estimada y tonelaje por semana', cls='dos')}</div>
    <div><span class="num"><i>{ico('pesa')}</i>Entrenamiento</span><h3>Un plan escrito para ti, serie a serie</h3><p>Cada sesión te dice qué ejercicios, cuántas series y cuánto esfuerzo. Y por qué: arriba del todo tienes para qué sirve la sesión de hoy.</p>
    <ul><li>Vídeo y técnica de cada uno de los más de 300 ejercicios</li><li>Alternativas si la máquina está ocupada, entrenas en casa o estás de viaje</li><li>¿Solo 25 minutos? La sesión se recorta por lo menos importante</li><li>Tu fuerza estimada y tus récords, ejercicio a ejercicio</li></ul></div></div>
  <div class="fila inv sube"><div class="pant">{m('recetario', 'Recetario del equipo con recetas por capítulos')}{m('receta', 'Ficha de una receta con macros, ingredientes y pasos', cls='dos')}</div>
    <div><span class="num"><i>{ico('plato')}</i>Nutrición</span><h3>Comer bien sin vivir a dieta</h3><p>Objetivos de calorías y proteína y un menú semanal que puedes cambiar. Sin pesar cada gramo si no quieres.</p>
    <ul><li>Más de 500 recetas con macros y medidas caseras, también veganas, sin gluten y sin lactosa</li><li>¿No te apetece apuntar? Haz una foto al plato y cuenta como hecha</li><li>¿Comes fuera? La app te dice cómo cuadrarlo</li><li>Lista de la compra hecha a partir de tu menú</li></ul></div></div>
</div></section>

<section class="sigo"><div class="in">
  <div class="entrada sube"><h2>Y al otro lado, alguien mirando</h2><p>Esto es lo que veo yo cada semana: quién ha entrenado, quién tiene una molestia, quién me ha escrito. Con eso ajusto tu plan antes de que empiece el lunes.</p></div>
  <div class="mesa sube">
    <div class="nav-marco"><div class="nav-barra"><i></i><i></i><i></i><span>Revisión semanal · vista del coach</span></div><img loading="lazy" src="{img('coach')}" width="1600" height="1000" alt="Panel del coach: revisión semanal con las sesiones, molestias y check-in de cada atleta (datos de ejemplo)"></div>
    <div class="hilo" role="img" aria-label="Ejemplo de conversación entre un atleta y su coach">
      <div class="b tu"><small>Tú</small>Hoy el press militar me ha molestado en el hombro. ¿Lo quito?</div>
      <div class="b co"><small>Pelayo</small>Lo he visto en tu sesión: un 2 sobre 10. Con eso no hace falta parar. Para la próxima sesión lo ajustamos con un punto menos de esfuerzo y el rango de recorrido que no te genere molestias, y avanzamos desde ahí.</div>
      <div class="b tu"><small>Tú</small>Perfecto. Te mando vídeo de la sentadilla para que la revises.</div>
      <p class="nota">Conversación de ejemplo</p>
    </div>
  </div>
  <ul class="tres sube"><li><i>{ico('ojo')}</i><b>Revisión cada semana</b><span>Miro tus sesiones y tu check-in y ajusto lo que haga falta.</span></li><li><i>{ico('chat')}</i><b>Mensajes dentro de la app</b><span>Me escribes cuando algo no cuadra, sin cambiar de aplicación.</span></li><li><i>{ico('video')}</i><b>Tu técnica, corregida</b><span>Me mandas vídeo desde la sesión y te lo devuelvo comentado.</span></li></ul>
</div></section>

<section class="cifras"><div class="in"><ul>
  <li class="sube"><b><span data-n="300">300</span>+</b><span>ejercicios con vídeo y técnica</span></li>
  <li class="sube"><b><span data-n="500">500</span>+</b><span>recetas con sus macros</span></li>
  <li class="sube"><b><span data-n="15">15</span>+</b><span>guías para entender lo que haces</span></li>
  <li class="sube"><b><span data-n="1">1</span></b><span>revisión mía cada semana</span></li>
</ul></div></section>

<section><div class="in">
  <div class="entrada centro sube"><h2>Los detalles que hacen que sigas</h2><p>Lo que usarás cada semana, sin saltar entre cinco aplicaciones</p></div>
  <div class="bento">
    <div class="caja g2 sube"><h3>Tu día, de un vistazo</h3><p>Constancia, carga, comida y sueño en anillos que se llenan.</p><div class="ans">{anillo(.66, '#7C6AFD', '2/3', 'Constancia')}{anillo(.9, '#2E9E6B', '118 %', 'Carga')}{anillo(.55, '#D99A2B', '6:35 h', 'Sueño')}</div></div>
    <div class="caja oscura sube"><h3>El descanso arranca solo</h3><p>Marcas la serie y cuenta atrás.</p><div class="crono" aria-hidden="true"><svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="34" class="f"/><circle cx="40" cy="40" r="34" class="a"/></svg><strong>1:55</strong></div></div>
    <div class="caja sube"><h3>Progreso a la vista</h3><p>Tonelaje, fuerza y racha.</p><div class="barras" aria-hidden="true"><i style="--h:38%"></i><i style="--h:52%"></i><i style="--h:47%"></i><i style="--h:66%"></i><i style="--h:74%"></i><i style="--h:92%"></i></div></div>
    <div class="caja sube"><i class="ic">{ico('cambio')}</i><h3>Alternativas al momento</h3><p>Máquina ocupada, casa o viaje: la app te da el cambio.</p></div>
    <div class="caja sube"><i class="ic">{ico('camara')}</i><h3>Foto del plato</h3><p>Una foto y la comida cuenta como hecha.</p></div>
    <div class="caja sube"><i class="ic">{ico('cesta')}</i><h3>Lista de la compra</h3><p>Sale sola de tu menú de la semana.</p></div>
    <div class="caja sube"><i class="ic">{ico('medalla')}</i><h3>Medallas y rachas</h3><p>Pequeños hitos para no soltarlo.</p></div>
    <div class="caja g2 dorada sube"><i class="ic">{ico('medalla')}</i><h3>Cada récord se celebra</h3><p>Cuando levantas más que nunca, la app lo sabe antes que tú y te lo dice en el momento.</p></div>
    <div class="caja sube"><i class="ic">{ico('casa')}</i><h3>Gimnasio, casa o viaje</h3><p>La sesión se adapta al material que tengas.</p></div>
    <div class="caja sube"><i class="ic">{ico('candado')}</i><h3>Tus datos, tuyos</h3><p>Fotos y medidas solo las vemos tú y yo.</p></div>
  </div>
</div></section>

<section class="sin-arriba"><div class="in"><div class="entrada sube" style="margin-bottom:1rem"><h2>Y todavía hay más</h2></div></div>
  <div class="galeria" id="galeria" tabindex="0" aria-label="Más pantallas de la app">
    <figure>{m('hoy-oscuro', 'La pantalla de inicio en modo oscuro')}<figcaption><b>Modo oscuro</b>Para entrenar de noche o porque te gusta más.</figcaption></figure>
    <figure>{m('logros', 'Medallas conseguidas y objetivos')}<figcaption><b>Medallas</b>Constancia, récords, toneladas, check-ins.</figcaption></figure>
    <figure>{m('perfil', 'Perfil del atleta con su carné y sus cifras')}<figcaption><b>Tu carné de atleta</b>Tus cifras, tu nivel y tu racha.</figcaption></figure>
    <figure>{m('aprende', 'Sección Aprende con las guías del coach')}<figcaption><b>Aprende</b>Las guías, para leer y para buscar.</figcaption></figure>
    <figure>{m('mensajes', 'Conversación con el coach dentro de la app')}<figcaption><b>Mensajes</b>Tu coach, a un toque.</figcaption></figure>
  </div>
</section>

<section class="aprende"><div class="in">
  <div class="sube"><h2>No solo te digo qué hacer. Te explico por qué.</h2><p class="t">Dentro de la app tienes mis guías, escritas para que entiendas lo que haces y puedas decidir tú cuando yo no esté.</p></div>
  <ul class="chips sube">{''.join(f'<li>{g}</li>' for g in GUIAS)}</ul>
</div></section>

<section><div class="in">
  <div class="entrada centro sube"><h2>No es lo mismo que una app cualquiera</h2><p>Ni que un plan en PDF. La diferencia es quién está detrás.</p></div>
  <div class="tabla-marco sube"><table class="compara"><thead><tr><th scope="col"><span class="oculto">Qué incluye</span></th><th scope="col" class="yo">Asesoría FBE</th><th scope="col">App genérica</th><th scope="col">Plan en PDF</th></tr></thead>
  <tbody>{''.join(f'<tr><th scope="row">{t}</th><td class="yo">{marca(a)}</td><td>{marca(b)}</td><td>{marca(c)}</td></tr>' for t, a, b, c in COMPARA)}</tbody></table></div>
</div></section>

<section class="pasos" id="como">{ANILLOS}<div class="in">
  <div class="entrada sube"><h2>Cómo empezamos</h2><p>De escribirme a tu primera sesión, tres pasos.</p></div>
  <ol>
    <li class="sube"><h3>Me escribes</h3><p>Rellenas el formulario: qué buscas, cómo entrenas ahora y de cuánto tiempo dispones.</p></li>
    <li class="sube"><h3>Valoración inicial</h3><p>Repasamos tu punto de partida, tu historial y, si tomas medicación o tienes alguna lesión, cómo tenerlo en cuenta.</p></li>
    <li class="sube"><h3>Tu plan, en tu móvil</h3><p>Recibes tu código, activas la app y ya tienes tu primera semana. A partir de ahí, revisión cada semana.</p></li>
  </ol>
  <div class="ciclo sube" aria-label="Así es cada semana después"><b>Y después, cada semana</b><ol><li>Lunes: tu semana lista</li><li>Entrenas y apuntas</li><li>Domingo: check-in</li><li>Reviso y ajusto</li></ol></div>
</div></section>

<section id="quien"><div class="in">
  <div class="ficha sube">
    <div class="retrato" aria-hidden="true">PF</div>
    <div><h2>Pelayo Fernández Cidón</h2><p class="rol">Médico internista y prescriptor de ejercicio físico</p>
      <p>Soy médico especialista en medicina interna en el Hospital Universitario La Paz (Madrid). Llevo más de quince años entrenando fuerza y desde 2020 dirijo FBE, Fuerza Basada en Evidencia.</p>
      <blockquote>Programo con lo que dice la evidencia y con lo que cabe en tu semana. Si algo no está demostrado, te lo digo.</blockquote>
      <ul class="sellos"><li>Medicina interna</li><li>Fuerza e hipertrofia</li><li>Nutrición</li><li>Basado en evidencia</li></ul></div>
  </div>
  <div class="encaje sube">
    <div><h3>Es para ti si…</h3><ul><li>Quieres ganar fuerza, perder grasa o las dos cosas</li><li>Tienes poco tiempo y no quieres improvisar</li><li>Empiezas de cero o llevas años y te has estancado</li><li>Te importa entender lo que haces</li></ul></div>
    <div class="no"><h3>No es lo que buscas si…</h3><ul><li>Quieres un plan cerrado sin seguimiento</li><li>Buscas resultados en dos semanas</li><li>Necesitas un tratamiento médico: eso es cosa de tu médico</li></ul></div>
  </div>
  <ul class="tres priv sube"><li><i>{ico('candado')}</i><b>Solo con tu permiso</b><span>Tus datos de salud se guardan únicamente si tú lo autorizas.</span></li><li><i>{ico('ojo')}</i><b>Solo tú y yo</b><span>Fotos, medidas y check-ins no los ve nadie más.</span></li><li><i>{ico('baja')}</i><b>Te los llevas cuando quieras</b><span>Puedes descargar todo lo tuyo desde la app.</span></li></ul>
</div></section>

<section id="dudas" class="sin-arriba"><div class="in">
  <div class="entrada centro sube"><h2>Dudas habituales</h2></div>
  <div class="faq sube">{''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))}</div>
</div></section>

<section class="cierre">{ANILLOS}<div class="in sube"><h2>¿Hablamos?</h2><p>Cuéntame tu caso en el formulario. Te respondo yo.</p><a class="btn claro" href="{CONTACTO}">Pedir plaza</a>
  <ul class="resumen"><li>{ico('si')}Plan hecho para ti</li><li>{ico('si')}Revisión cada semana</li><li>{ico('si')}Sin compromiso</li></ul></div></section>
<footer><div class="in">
  <div><b>FBE · Fuerza Basada en Evidencia</b><p>Asesoría online de fuerza y nutrición. La asesoría no sustituye a tu médico ni a un tratamiento.</p></div>
  <div><b>La página</b><a href="#semana">Tu semana</a><a href="#app">La app</a><a href="#como">Cómo empezamos</a><a href="#quien">Quién te lleva</a><a href="#dudas">Dudas</a></div>
  <div><b>¿Ya eres atleta?</b><a href="{APP}">Entrar en la app</a><a href="{CONTACTO}">Pedir plaza</a><a href="#inicio">Volver arriba</a></div>
</div></footer>
<div class="fijo" id="fijo"><a class="btn claro" href="{CONTACTO}">Pedir plaza</a></div>
<script>{open('guion3.js', encoding='utf-8').read()}</script>
'''
open('web-fbe-equipo.html', 'w', encoding='utf-8').write(html); print(len(html) // 1024, 'KB')
