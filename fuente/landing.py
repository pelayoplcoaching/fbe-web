import base64
def img(n): return 'data:image/webp;base64,' + base64.b64encode(open(n + '.webp', 'rb').read()).decode()
CONTACTO = '#contacto-pendiente'   # aquí va el enlace del formulario de NoteForms
html = '''<meta name="claude:viewport-fit-sides" content="cover">
<title>Web FBE Equipo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap">
<style>
:root { --noche:#140B3A; --noche-2:#241665; --marca:#593EDE; --marca-clara:#A49CFF; --lila:#EEECFF; --fondo:#F6F6F9; --sup:#FFFFFF; --tinta:#151423; --tinta-2:#55546A; --linea:#DDDCE6; --sobre:#FFFFFF; color-scheme: light; }
body { background: var(--fondo); color: var(--tinta); font: 400 1.0625rem/1.55 Archivo, system-ui, sans-serif; }
.in { max-width: 68rem; margin: 0 auto; padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-stretch: 118%; font-weight: 750; line-height: 1.08; margin: 0; text-wrap: balance; letter-spacing: -.01em; }
h1 { font-size: clamp(2.3rem, 6.2vw, 4.3rem); } h2 { font-size: clamp(1.7rem, 3.8vw, 2.6rem); } h3 { font-size: 1.25rem; line-height: 1.2; }
p { margin: 0; max-width: 34rem; }
.btn { display: inline-block; background: var(--marca); color: var(--sobre); font-weight: 650; text-decoration: none; padding: .95rem 1.5rem; border-radius: .9rem; }
.btn:hover { background: #462ABF; } .btn:focus-visible, a:focus-visible { outline: 3px solid var(--marca-clara); outline-offset: 3px; }
.hero { background: radial-gradient(60rem 30rem at 85% 10%, #3a2a9a 0%, transparent 60%), var(--noche); color: var(--sobre); overflow: hidden; }
.hero .in { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: 3rem; align-items: end; padding-top: 1.5rem; }
.marca { font-stretch: 118%; font-weight: 750; font-size: 1.05rem; padding-bottom: clamp(2.5rem, 7vw, 5rem); display: block; }
.hero p { color: #D4D0F5; font-size: 1.2rem; margin: 1.4rem 0 2rem; }
.hero .txt { padding-bottom: clamp(3rem, 8vw, 6rem); }
.hero small { display: block; margin-top: 1rem; color: var(--marca-clara); font-size: .95rem; }
.hero .btn { background: var(--sobre); color: var(--noche); } .hero .btn:hover { background: var(--lila); }
.movil { border-radius: 2.2rem 2.2rem 0 0; border: .5rem solid #0b0624; border-bottom: 0; overflow: hidden; max-width: 21rem; justify-self: center; height: 34rem; box-shadow: 0 2rem 5rem rgba(8, 4, 30, .6); }
.movil img { display: block; width: 100%; }
section { padding-block: clamp(3.5rem, 9vw, 7rem); }
.entrada { display: grid; gap: 1rem; margin-bottom: clamp(2.5rem, 6vw, 4.5rem); }
.entrada p { color: var(--tinta-2); font-size: 1.15rem; }
.fila { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(2rem, 6vw, 5rem); align-items: center; margin-bottom: clamp(3rem, 8vw, 6rem); }
.fila:last-child { margin-bottom: 0; }
.fila:nth-child(even) .pant { order: 2; }
.pant { background: var(--lila); border-radius: 1.6rem; padding: 2rem 2rem 0; display: flex; justify-content: center; gap: 1rem; overflow: hidden; height: 30rem; }
.pant img { width: min(15.5rem, 46%); align-self: flex-start; border-radius: 1.4rem 1.4rem 0 0; box-shadow: 0 1rem 2.5rem rgba(36, 22, 101, .22); }
.pant img + img { margin-top: 3rem; }
.fila h3 { font-size: clamp(1.4rem, 2.6vw, 1.9rem); margin-bottom: .9rem; }
.fila p { color: var(--tinta-2); } .fila ul { margin: 1.1rem 0 0; padding: 0; list-style: none; display: grid; gap: .55rem; max-width: 32rem; }
.fila li { padding-left: 1.5rem; position: relative; } .fila li::before { content: ""; position: absolute; left: 0; top: .55em; width: .6rem; height: .6rem; border-radius: 50%; background: var(--marca); }
.pasos { background: var(--sup); border-block: 1px solid var(--linea); }
.pasos ol { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2rem; counter-reset: p; }
.pasos li { counter-increment: p; border-top: 3px solid var(--marca); padding-top: 1.1rem; }
.pasos li::before { content: counter(p); font-stretch: 118%; font-weight: 750; font-size: 2.2rem; color: var(--marca); display: block; line-height: 1; margin-bottom: .7rem; }
.pasos li p { color: var(--tinta-2); margin-top: .5rem; }
.quien .in { display: grid; grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); gap: clamp(2rem, 6vw, 5rem); }
.quien p { margin-bottom: 1rem; max-width: 38rem; } .quien dl { margin: 1.5rem 0 0; display: grid; gap: .8rem; }
.quien dt { font-weight: 650; } .quien dd { margin: 0; color: var(--tinta-2); }
.cierre { background: var(--noche); color: var(--sobre); text-align: center; }
.cierre p { margin: 1.2rem auto 2rem; color: #D4D0F5; font-size: 1.15rem; } .cierre .btn { background: var(--sobre); color: var(--noche); }
footer { background: var(--noche); color: var(--marca-clara); font-size: .9rem; padding-block: 1.5rem 2.5rem; text-align: center; border-top: 1px solid #2f2470; }
footer p { margin: 0 auto; }
@media (max-width: 760px) {
  .hero .in, .fila, .quien .in { grid-template-columns: 1fr; } .hero .txt { padding-bottom: 0; } .movil { height: 26rem; }
  .fila:nth-child(even) .pant { order: 0; } .pant { height: 22rem; padding: 1.25rem 1.25rem 0; } .pasos ol { grid-template-columns: 1fr; }
}
</style>
<header class="hero"><div class="in">
  <div class="txt">
    <span class="marca">FBE · Fuerza Basada en Evidencia</span>
    <h1>Tu entrenamiento, tu comida y tu coach, en la misma app.</h1>
    <p>Asesoría online de fuerza y nutrición con un médico internista que también te entrena. Cada semana sabes qué toca, lo apuntas en el móvil y yo lo reviso.</p>
    <a class="btn" href="__C__">Pedir plaza</a>
    <small>Sin compromiso: primero hablamos y vemos si encaja.</small>
  </div>
  <div class="movil"><img src="__HOY__" alt="Pantalla de inicio de la app: la sesión de hoy, el aviso del coach y los anillos de constancia, carga, comida y sueño"></div>
</div></header>

<section><div class="in">
  <div class="entrada"><h2>Lo que tienes desde el primer día</h2><p>Una app hecha para mis atletas, no una plantilla en PDF ni un grupo de mensajes. Estas pantallas son de la app real, con atletas de ejemplo.</p></div>
  <div class="fila"><div class="pant"><img src="__PORTADA__" alt="Portada de la sesión Torso B con duración, ejercicios y la nota del coach"><img src="__SESION__" alt="Sesión en marcha: series apuntadas y temporizador de descanso"></div>
    <div><h3>Un plan escrito para ti, serie a serie</h3><p>Abres la app y ves la sesión de hoy: ejercicios, series, repeticiones y cuánto esfuerzo toca. Apuntas los kilos y el descanso arranca solo.</p>
    <ul><li>Vídeo y técnica de cada ejercicio</li><li>Alternativas si el gimnasio está lleno, entrenas en casa o estás de viaje</li><li>Si un día tienes 25 minutos, la sesión se ajusta</li></ul></div></div>
  <div class="fila"><div class="pant"><img src="__PROGRESO__" alt="Pantalla de progreso: peso, récords, tonelaje y racha de semanas"><img src="__CHECKIN__" alt="Check-in semanal con las respuestas del atleta"></div>
    <div><h3>Ves si avanzas, sin hacer cuentas</h3><p>Tu peso, tus récords y tu constancia, semana a semana. Y cada semana un check-in corto: cómo has dormido, cómo vas de energía, qué te ha costado.</p>
    <ul><li>Con eso decido qué cambia la semana siguiente</li><li>Fotos y medidas, solo si quieres y solo las vemos tú y yo</li></ul></div></div>
  <div class="fila"><div class="pant"><img src="__COMIDAS__" alt="Pantalla de comidas: calorías y proteína del día y el menú de la semana"><img src="__MENSAJES__" alt="Conversación con el coach dentro de la app"></div>
    <div><h3>Nutrición que se puede cumplir, y alguien al otro lado</h3><p>Objetivos de calorías y proteína, un menú semanal que puedes cambiar y un recetario con más de 500 recetas con sus macros. Si comes fuera, la app te dice cómo cuadrarlo.</p>
    <ul><li>Lista de la compra hecha a partir de tu menú</li><li>Mensajes conmigo dentro de la app, y vídeos de tu técnica para que te los corrija</li></ul></div></div>
</div></section>

<section class="pasos"><div class="in">
  <div class="entrada"><h2>Cómo empezamos</h2></div>
  <ol>
    <li><h3>Me escribes</h3><p>Rellenas el formulario: qué buscas, cómo entrenas ahora y de cuánto tiempo dispones.</p></li>
    <li><h3>Valoración inicial</h3><p>Repasamos tu punto de partida, tu historial y, si tomas medicación o tienes alguna lesión, cómo tenerlo en cuenta.</p></li>
    <li><h3>Tu plan, en tu móvil</h3><p>Recibes tu código, activas la app y ya tienes tu primera semana. A partir de ahí, revisión cada semana.</p></li>
  </ol>
</div></section>

<section class="quien"><div class="in">
  <h2>Quién te lleva</h2>
  <div>
    <p>Soy Pelayo Fernández Cidón, médico especialista en medicina interna en el Hospital Universitario La Paz (Madrid) y entrenador. Llevo más de quince años entrenando fuerza y desde 2020 dirijo FBE, Fuerza Basada en Evidencia.</p>
    <p>Programo con lo que dice la evidencia y con lo que cabe en tu semana. Si algo no está demostrado, te lo digo.</p>
    <dl><div><dt>Para quién es</dt><dd>Personas que quieren ganar fuerza, perder grasa o entrenar con cabeza teniendo poco tiempo, empiecen de cero o lleven años.</dd></div>
    <div><dt>Qué no es</dt><dd>La asesoría no sustituye a tu médico ni a un tratamiento. Si hay algo que valorar antes de entrenar, te lo diré.</dd></div></dl>
  </div>
</div></section>

<section class="cierre"><div class="in"><h2>¿Hablamos?</h2><p>Cuéntame tu caso en el formulario. Te respondo yo.</p><a class="btn" href="__C__">Pedir plaza</a></div></section>
<footer><div class="in"><p>FBE · Fuerza Basada en Evidencia</p></div></footer>
'''
for k in ('hoy', 'portada', 'sesion', 'progreso', 'checkin', 'comidas', 'mensajes'): html = html.replace('__' + k.upper() + '__', img(k))
html = html.replace('__C__', CONTACTO)
open('web-fbe-equipo.html', 'w', encoding='utf-8').write(html); print(len(html) // 1024, 'KB')
