import base64
def img(n): return 'data:image/webp;base64,' + base64.b64encode(open(n + '.webp', 'rb').read()).decode()
CONTACTO = '#contacto-pendiente'   # aquí va el enlace del formulario de NoteForms
APP = 'https://atletas.fuerzabasadaenevidencia.com'
I = {  # iconos de línea, 24 px
 'video': '<path d="M4 6h11v12H4z"/><path d="m15 10 5-3v10l-5-3"/>', 'cambio': '<path d="M4 8h13l-3-3"/><path d="M20 16H7l3 3"/>',
 'reloj': '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>', 'grafica': '<path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/>',
 'check': '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="m8 12 3 3 5-6"/>', 'plato': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/>',
 'cesta': '<path d="M5 9h14l-1.5 10h-11z"/><path d="M9 9l3-5 3 5"/>', 'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
 'medalla': '<circle cx="12" cy="14" r="5"/><path d="M9 9 7 3h10l-2 6"/>', 'casa': '<path d="M4 11 12 4l8 7"/><path d="M6 10v9h12v-9"/>',
 'candado': '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>', 'libro': '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>',
}
def ico(n): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{I[n]}</svg>'
ANILLOS = '<svg class="anillos" viewBox="0 0 600 600" aria-hidden="true">' + ''.join(f'<circle cx="300" cy="300" r="{r}"/>' for r in (60, 110, 165, 225, 290)) + '<circle class="punto" cx="465" cy="300" r="7"/><circle class="punto p2" cx="300" cy="75" r="5"/></svg>'
bento = [('video', 'Vídeo de cada ejercicio', 'Técnica explicada, sin buscar en YouTube.'), ('cambio', 'Alternativas al momento', 'Máquina ocupada, casa o viaje: la app te da el cambio.'),
 ('reloj', 'Sesiones que se ajustan', '¿Solo 25 minutos? La sesión se recorta por lo que menos importa.'), ('grafica', 'Progreso a la vista', 'Peso, récords, tonelaje y racha de semanas.'),
 ('check', 'Check-in semanal', 'Dos minutos para contarme cómo ha ido.'), ('plato', 'Menú y macros', 'Objetivos por día y un menú que puedes cambiar.'),
 ('libro', 'Más de 500 recetas', 'Con macros, medidas caseras y filtros por dieta.'), ('cesta', 'Lista de la compra', 'Sale sola de tu menú de la semana.'),
 ('chat', 'Mensajes con tu coach', 'Dudas y vídeos de técnica, dentro de la app.'), ('medalla', 'Medallas y rachas', 'Pequeños hitos para no soltarlo.'),
 ('casa', 'Gimnasio, casa o viaje', 'Cada sesión se adapta al material que tengas.'), ('candado', 'Tus datos, tuyos', 'Fotos y medidas solo las vemos tú y yo.')]
faq = [('¿Necesito ir a un gimnasio?', 'No es obligatorio. Programo para gimnasio, para casa con poco material o para una mezcla de los dos, y la app te propone alternativas si un día no tienes lo que toca.'),
 ('¿Puedo apuntarme solo a la nutrición, o solo al entrenamiento?', 'Sí. Hay atletas que solo llevan entrenamiento, otros solo nutrición y otros las dos cosas. La app enseña únicamente lo que tengas contratado.'),
 ('¿Tengo que descargar algo?', 'No hace falta ir a ninguna tienda de aplicaciones. La app se abre desde el navegador del móvil y se añade a la pantalla de inicio en dos toques; funciona en iPhone y en Android.'),
 ('Tomo medicación o tengo una lesión. ¿Puedo entrenar?', 'En la mayoría de los casos sí, y adaptarlo es parte del trabajo. Lo vemos en la valoración inicial. La asesoría no sustituye a tu médico ni a tu tratamiento.'),
 ('¿Cuánto cuesta?', 'Depende de si quieres entrenamiento, nutrición o las dos cosas. Te lo detallo al responder a tu formulario, sin compromiso.')]
html = '''<meta name="claude:viewport-fit-sides" content="cover">
<title>Web FBE Equipo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&display=swap">
<style>
:root { --noche:#140B3A; --noche-2:#241665; --noche-3:#2f2470; --marca:#593EDE; --marca-h:#462ABF; --marca-clara:#A49CFF; --sobre:#FFFFFF; --lavanda:#D4D0F5;
  --fondo:#F6F6F9; --sup:#FFFFFF; --lila:#EEECFF; --tinta:#151423; --tinta-2:#55546A; --linea:#DDDCE6; --acento:#593EDE; --sombra: 0 1.2rem 3rem rgba(36,22,101,.16); --sombra-s: 0 .3rem 1rem rgba(36,22,101,.08); color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --fondo:#0E0D15; --sup:#181626; --lila:#211F32; --tinta:#EEECFF; --tinta-2:#A9A7BD; --linea:#343249; --acento:#A49CFF; --sombra: 0 1.2rem 3rem rgba(0,0,0,.5); --sombra-s: 0 .3rem 1rem rgba(0,0,0,.35); color-scheme: dark; } }
:root[data-theme="dark"] { --fondo:#0E0D15; --sup:#181626; --lila:#211F32; --tinta:#EEECFF; --tinta-2:#A9A7BD; --linea:#343249; --acento:#A49CFF; --sombra: 0 1.2rem 3rem rgba(0,0,0,.5); --sombra-s: 0 .3rem 1rem rgba(0,0,0,.35); color-scheme: dark; }
html { scroll-behavior: smooth; scroll-padding-top: 5rem; }
body { background: var(--fondo); color: var(--tinta); font: 400 1.0625rem/1.6 Archivo, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
.in { max-width: 70rem; margin: 0 auto; padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-stretch: 120%; font-weight: 760; line-height: 1.04; margin: 0; text-wrap: balance; letter-spacing: -.02em; }
h1 { font-size: clamp(2.5rem, 6.6vw, 4.9rem); } h2 { font-size: clamp(1.9rem, 4.2vw, 3.1rem); } h3 { font-size: 1.2rem; line-height: 1.2; letter-spacing: -.01em; }
p { margin: 0; text-wrap: pretty; } a { color: inherit; }
svg { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.btn { display: inline-flex; align-items: center; gap: .6rem; background: var(--marca); color: var(--sobre); font-weight: 680; text-decoration: none; padding: 1rem 1.6rem; border-radius: 99px; transition: transform .18s, background .18s, box-shadow .18s; box-shadow: 0 .6rem 1.6rem rgba(89,62,222,.35); }
.btn::after { content: ""; width: .5rem; height: .5rem; border-top: 2px solid; border-right: 2px solid; transform: rotate(45deg); transition: transform .18s; }
.btn:hover { background: var(--marca-h); transform: translateY(-2px); } .btn:hover::after { transform: translateX(3px) rotate(45deg); }
.btn.claro { background: var(--sobre); color: var(--noche); box-shadow: 0 .6rem 2rem rgba(0,0,0,.3); } .btn.claro:hover { background: #EEECFF; }
.btn.peq { padding: .6rem 1.1rem; font-size: .95rem; box-shadow: none; }
:focus-visible { outline: 3px solid var(--marca-clara); outline-offset: 3px; border-radius: 6px; }

/* cabecera fija */
.cab { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20; background: rgba(20,11,58,.94); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); color: var(--sobre); border-bottom: 1px solid rgba(164,156,255,.18); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--noche); }
.cab .in { display: flex; align-items: center; gap: 1.5rem; height: 4rem; }
.logo { font-stretch: 122%; font-weight: 780; text-decoration: none; display: flex; align-items: center; gap: .6rem; margin-right: auto; letter-spacing: -.01em; }
.logo i { width: 1.9rem; height: 1.9rem; border-radius: .6rem; background: linear-gradient(140deg, #7C6AFD, #462ABF); display: grid; place-items: center; font-style: normal; font-size: .8rem; }
.cab nav { display: flex; gap: 1.6rem; } .cab nav a { text-decoration: none; color: var(--lavanda); font-size: .96rem; } .cab nav a:hover { color: var(--sobre); }

/* portada */
.hero { background: radial-gradient(52rem 32rem at 82% 30%, #3b2ba6 0%, transparent 62%), radial-gradient(40rem 24rem at 0% 100%, #2a1b78 0%, transparent 60%), var(--noche); color: var(--sobre); overflow: hidden; position: relative; margin-top: -4rem; padding-top: 4rem; }
.anillos { position: absolute; right: -6rem; top: 50%; width: 52rem; transform: translateY(-50%); stroke: rgba(164,156,255,.2); stroke-width: 1; pointer-events: none; }
.anillos .punto { fill: var(--marca-clara); stroke: none; transform-origin: 300px 300px; animation: orbita 26s linear infinite; } .anillos .p2 { animation-duration: 40s; animation-direction: reverse; fill: #F0C674; }
@keyframes orbita { to { transform: rotate(360deg); } }
.hero .in { position: relative; display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr); gap: 2rem; align-items: center; padding-block: clamp(3rem, 8vw, 6.5rem) 0; }
.hero h1 span { display: block; } .hero h1 span:last-child { color: var(--marca-clara); }
.hero .sub { color: var(--lavanda); font-size: clamp(1.1rem, 1.6vw, 1.3rem); margin: 1.6rem 0 2.2rem; max-width: 33rem; }
.cta { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem 1.4rem; } .cta small { color: var(--marca-clara); font-size: .95rem; }
.escena { position: relative; justify-self: center; padding: 0 2.5rem; align-self: end; }
.tel { width: min(19.5rem, 72vw); aspect-ratio: 585 / 1180; border-radius: 2.6rem 2.6rem 0 0; border: .55rem solid #0a0520; border-bottom: 0; background: #0a0520; overflow: hidden; box-shadow: 0 0 0 1px rgba(164,156,255,.35), 0 2rem 6rem rgba(8,4,30,.7); position: relative; }
.tel::before { content: ""; position: absolute; top: .55rem; left: 50%; width: 5.2rem; height: 1.25rem; border-radius: 99px; background: #0a0520; transform: translateX(-50%); z-index: 2; }
.tel img { display: block; width: 100%; }
.flota { position: absolute; background: rgba(255,255,255,.96); color: #151423; border-radius: 1rem; padding: .7rem .9rem; font-size: .88rem; line-height: 1.35; box-shadow: 0 1rem 2.5rem rgba(8,4,30,.45); max-width: 14.5rem; animation: flotar 7s ease-in-out infinite; }
.flota b { display: block; font-size: .78rem; color: #593EDE; margin-bottom: .15rem; } .flota.a { left: -7rem; top: 30%; } .flota.b { right: -3rem; top: 52%; animation-delay: -3.5s; }
.flota.b strong { font-stretch: 120%; font-size: 1.25rem; display: block; }
@keyframes flotar { 50% { transform: translateY(-10px); } }

/* franja de confianza */
.franja { background: var(--noche); color: var(--sobre); border-top: 1px solid var(--noche-3); }
.franja ul { list-style: none; margin: 0; padding: 1.5rem 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.5rem; }
.franja li { display: grid; gap: .1rem; padding-left: 1.2rem; border-left: 2px solid var(--marca); } .franja b { font-stretch: 118%; font-size: 1.15rem; } .franja span { color: var(--lavanda); font-size: .95rem; }

section { padding-block: clamp(4rem, 10vw, 8rem); }
.entrada { display: grid; gap: 1.1rem; margin-bottom: clamp(2.5rem, 6vw, 4.5rem); max-width: 46rem; } .entrada p { color: var(--tinta-2); font-size: 1.18rem; }
.centro { text-align: center; margin-inline: auto; justify-items: center; }

/* bloques con pantallas */
.fila { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(2rem, 7vw, 6rem); align-items: center; margin-bottom: clamp(3.5rem, 9vw, 7rem); }
.fila:last-of-type { margin-bottom: 0; } .fila.inv .pant { order: 2; }
.pant { position: relative; background: linear-gradient(160deg, var(--lila), color-mix(in srgb, var(--lila) 40%, var(--fondo))); border-radius: 2rem; height: 33rem; overflow: hidden; display: flex; justify-content: center; gap: 1.2rem; padding: 2.5rem 2rem 0; border: 1px solid var(--linea); }
.pant .m { width: min(15.5rem, 46%); align-self: flex-start; border-radius: 1.7rem 1.7rem 0 0; border: .35rem solid #0a0520; border-bottom: 0; overflow: hidden; box-shadow: var(--sombra); background: #0a0520; }
.pant .m img { display: block; width: 100%; } .pant .m + .m { margin-top: 4rem; }
.num { font-stretch: 122%; font-weight: 780; font-size: .95rem; color: var(--acento); display: inline-flex; align-items: center; gap: .6rem; margin-bottom: 1rem; }
.num i { font-style: normal; width: 2.4rem; height: 2.4rem; border-radius: .8rem; display: grid; place-items: center; background: var(--marca); color: var(--sobre); } .num svg { width: 1.3rem; height: 1.3rem; }
.fila h3 { font-size: clamp(1.6rem, 3vw, 2.3rem); line-height: 1.08; margin-bottom: 1rem; letter-spacing: -.02em; }
.fila p { color: var(--tinta-2); max-width: 31rem; } .fila ul { margin: 1.4rem 0 0; padding: 0; list-style: none; display: grid; gap: .7rem; max-width: 31rem; }
.fila li { padding-left: 2rem; position: relative; } .fila li::before { content: ""; position: absolute; left: 0; top: .28em; width: 1.2rem; height: 1.2rem; border-radius: 50%; background: var(--lila); }
.fila li::after { content: ""; position: absolute; left: .38rem; top: .55em; width: .42rem; height: .22rem; border-left: 2px solid var(--acento); border-bottom: 2px solid var(--acento); transform: rotate(-45deg); }

/* conversación */
.charla { background: var(--sup); border-block: 1px solid var(--linea); }
.charla .in { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(2rem, 6vw, 5rem); align-items: center; }
.charla p.t { color: var(--tinta-2); font-size: 1.15rem; margin-top: 1.1rem; max-width: 30rem; }
.hilo { display: grid; gap: .7rem; max-width: 30rem; justify-self: center; width: 100%; }
.b { padding: .85rem 1.1rem; border-radius: 1.3rem; max-width: 86%; font-size: 1rem; line-height: 1.45; box-shadow: var(--sombra-s); }
.b.tu { justify-self: end; background: var(--marca); color: var(--sobre); border-bottom-right-radius: .4rem; } .b.co { background: var(--lila); border-bottom-left-radius: .4rem; }
.b small { display: block; font-size: .76rem; opacity: .75; margin-bottom: .15rem; font-weight: 650; } .hilo .nota { text-align: center; color: var(--tinta-2); font-size: .85rem; margin-top: .4rem; }

/* cuadrícula */
.bento { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
.caja { background: var(--sup); border: 1px solid var(--linea); border-radius: 1.3rem; padding: 1.4rem; display: grid; gap: .5rem; align-content: start; transition: transform .2s, box-shadow .2s, border-color .2s; }
.caja:hover { transform: translateY(-4px); box-shadow: var(--sombra); border-color: var(--marca-clara); }
.caja i { width: 2.6rem; height: 2.6rem; border-radius: .9rem; background: var(--lila); color: var(--acento); display: grid; place-items: center; margin-bottom: .5rem; } .caja svg { width: 1.4rem; height: 1.4rem; }
.caja p { color: var(--tinta-2); font-size: .96rem; line-height: 1.45; }

/* galería */
.galeria { display: flex; gap: 1.2rem; overflow-x: auto; scroll-snap-type: x mandatory; padding: 1rem max(20px, calc((100vw - 70rem) / 2 + 20px)) 2rem; scrollbar-width: thin; }
.galeria figure { margin: 0; flex: 0 0 min(15rem, 62vw); scroll-snap-align: center; } .galeria .m { border-radius: 1.7rem; border: .35rem solid #0a0520; overflow: hidden; box-shadow: var(--sombra); aspect-ratio: 585 / 1180; background: #0a0520; }
.galeria img { display: block; width: 100%; } .galeria figcaption { text-align: center; margin-top: .8rem; color: var(--tinta-2); font-size: .95rem; font-weight: 600; }

/* pasos */
.pasos { background: var(--noche); color: var(--sobre); position: relative; overflow: hidden; } .pasos .entrada p { color: var(--lavanda); }
.pasos ol { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.2rem; counter-reset: p; position: relative; }
.pasos li { counter-increment: p; background: rgba(255,255,255,.05); border: 1px solid rgba(164,156,255,.22); border-radius: 1.4rem; padding: 1.6rem; }
.pasos li::before { content: "0" counter(p); font-stretch: 122%; font-weight: 780; font-size: 3.2rem; line-height: 1; display: block; margin-bottom: 1.2rem; color: transparent; -webkit-text-stroke: 1.5px var(--marca-clara); }
.pasos li p { color: var(--lavanda); margin-top: .6rem; font-size: 1rem; }

/* quién */
.ficha { background: var(--sup); border: 1px solid var(--linea); border-radius: 2rem; padding: clamp(1.5rem, 4vw, 3rem); display: grid; grid-template-columns: auto minmax(0, 1fr); gap: clamp(1.5rem, 4vw, 3rem); box-shadow: var(--sombra-s); }
.retrato { width: clamp(7rem, 16vw, 11rem); aspect-ratio: 4 / 5; border-radius: 1.4rem; background: linear-gradient(150deg, #7C6AFD, #241665); display: grid; place-items: center; color: #fff; font-stretch: 122%; font-weight: 780; font-size: clamp(2rem, 5vw, 3.4rem); }
.ficha h2 { font-size: clamp(1.7rem, 3.4vw, 2.5rem); } .ficha .rol { color: var(--acento); font-weight: 650; margin: .5rem 0 1.2rem; } .ficha p { color: var(--tinta-2); max-width: 40rem; margin-bottom: .9rem; }
.sellos { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.2rem; padding: 0; list-style: none; } .sellos li { background: var(--lila); border-radius: 99px; padding: .35rem .9rem; font-size: .9rem; font-weight: 600; }
.encaje { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin-top: 1rem; }
.encaje div { border-radius: 1.4rem; padding: 1.5rem; border: 1px solid var(--linea); background: var(--sup); } .encaje ul { margin: .8rem 0 0; padding-left: 1.1rem; color: var(--tinta-2); display: grid; gap: .4rem; }
.encaje .no { background: transparent; border-style: dashed; }

/* preguntas */
.faq { max-width: 48rem; margin: 0 auto; display: grid; gap: .6rem; }
.faq details { background: var(--sup); border: 1px solid var(--linea); border-radius: 1.1rem; } .faq details[open] { border-color: var(--marca-clara); box-shadow: var(--sombra-s); }
.faq summary { list-style: none; cursor: pointer; padding: 1.1rem 3.2rem 1.1rem 1.3rem; font-weight: 650; position: relative; font-size: 1.08rem; } .faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: ""; position: absolute; right: 1.4rem; top: 50%; width: .6rem; height: .6rem; border-right: 2px solid var(--acento); border-bottom: 2px solid var(--acento); transform: translateY(-70%) rotate(45deg); transition: transform .2s; }
.faq details[open] summary::after { transform: translateY(-30%) rotate(225deg); } .faq details p { padding: 0 1.3rem 1.3rem; color: var(--tinta-2); }

/* cierre y pie */
.cierre { background: radial-gradient(40rem 22rem at 50% 0%, #3b2ba6 0%, transparent 70%), var(--noche); color: var(--sobre); text-align: center; position: relative; overflow: hidden; }
.cierre .anillos { right: 50%; transform: translate(50%, -50%); width: 60rem; opacity: .7; } .cierre .in { position: relative; }
.cierre h2 { font-size: clamp(2.2rem, 6vw, 4.2rem); } .cierre p { margin: 1.3rem auto 2.2rem; color: var(--lavanda); font-size: 1.2rem; max-width: 30rem; }
footer { background: var(--noche); color: var(--lavanda); font-size: .95rem; border-top: 1px solid var(--noche-3); padding-block: 2.5rem calc(2.5rem + env(safe-area-inset-bottom, 0px)); }
footer .in { display: grid; grid-template-columns: minmax(0, 1.4fr) repeat(2, minmax(0, 1fr)); gap: 2rem; } footer b { color: #fff; display: block; margin-bottom: .6rem; font-stretch: 118%; }
footer a { display: block; text-decoration: none; padding: .2rem 0; } footer a:hover { color: #fff; } footer p { max-width: 22rem; }

/* botón fijo en el móvil */
.fijo { display: none; }
/* entrada al hacer scroll */
.js .sube { opacity: 0; transform: translateY(24px); transition: opacity .7s cubic-bezier(.2,.7,.2,1), transform .7s cubic-bezier(.2,.7,.2,1); } .js .sube.ya { opacity: 1; transform: none; }
.js .hero .txt > * { animation: entra .8s cubic-bezier(.2,.7,.2,1) both; } .js .hero .txt > :nth-child(2) { animation-delay: .12s; } .js .hero .txt > :nth-child(3) { animation-delay: .24s; } .js .hero .escena { animation: entra 1s .2s cubic-bezier(.2,.7,.2,1) both; }
@keyframes entra { from { opacity: 0; transform: translateY(28px); } }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } *, *::before, *::after { animation: none !important; transition: none !important; } .js .sube { opacity: 1; transform: none; } }
@media (max-width: 900px) { .bento { grid-template-columns: repeat(2, minmax(0, 1fr)); } .cab nav { display: none; } .flota.a { left: -1rem; } .flota.b { right: -1rem; } }
@media (max-width: 760px) {
  .hero .in, .fila, .charla .in, .ficha, .encaje, footer .in { grid-template-columns: 1fr; } .hero .in { padding-top: 2.5rem; } .escena { margin-top: 1.5rem; padding: 0 1rem; }
  .fila.inv .pant { order: 0; } .pant { height: 24rem; padding: 1.5rem 1.2rem 0; border-radius: 1.5rem; } .pasos ol, .franja ul { grid-template-columns: 1fr; } .franja ul { gap: 1rem; }
  .anillos { width: 36rem; right: -14rem; top: 70%; } .flota { font-size: .8rem; max-width: 11.5rem; } .flota.a { top: 14%; } .flota.b { top: 58%; }
  .cab .btn { display: none; } .fijo { display: block; position: fixed; inset: auto 0 0; z-index: 25; padding: .7rem max(16px, env(safe-area-inset-right, 0px)) calc(.7rem + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); background: rgba(20,11,58,.9); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); transform: translateY(110%); transition: transform .3s; }
  .fijo.ver { transform: none; } .fijo .btn { width: 100%; justify-content: center; } footer { padding-bottom: calc(6rem + env(safe-area-inset-bottom, 0px)); }
}
</style>
<script>document.documentElement.classList.add('js');</script>

<div class="cab"><div class="in">
  <a class="logo" href="#inicio"><i>FBE</i>Fuerza Basada en Evidencia</a>
  <nav aria-label="Secciones"><a href="#app">La app</a><a href="#como">Cómo empezamos</a><a href="#quien">Quién te lleva</a><a href="#dudas">Dudas</a></nav>
  <a class="btn peq claro" href="__C__">Pedir plaza</a>
</div></div>

<header class="hero" id="inicio">__ANILLOS__<div class="in">
  <div class="txt">
    <h1><span>Tu plan.</span><span>Tu comida.</span><span>Tu coach.</span></h1>
    <p class="sub">Asesoría online de fuerza y nutrición con un médico internista que también te entrena. Todo en una app: cada semana sabes qué toca, lo apuntas en el móvil y yo lo reviso.</p>
    <div class="cta"><a class="btn claro" href="__C__">Pedir plaza</a><small>Sin compromiso: primero hablamos<br>y vemos si encaja.</small></div>
  </div>
  <div class="escena">
    <div class="tel"><img src="__HOY__" width="585" height="1266" alt="Pantalla de inicio de la app: la sesión de hoy, el aviso del coach y los anillos de constancia, carga, comida y sueño"></div>
    <div class="flota a" aria-hidden="true"><b>Tu coach</b>Si notas el hombro, cambia el press militar por press con mancuernas sentado.</div>
    <div class="flota b" aria-hidden="true"><b>Racha</b><strong>3 semanas</strong>completas seguidas</div>
  </div>
</div></header>

<div class="franja"><div class="in"><ul>
  <li><b>Médico internista</b><span>Hospital Universitario La Paz, Madrid</span></li>
  <li><b>Más de 15 años</b><span>entrenando fuerza</span></li>
  <li><b>Desde 2020</b><span>llevando atletas en FBE</span></li>
</ul></div></div>

<section id="app"><div class="in">
  <div class="entrada sube"><h2>Lo que tienes desde el primer día</h2><p>Una app hecha para mis atletas, no una plantilla en PDF ni un grupo de mensajes. Estas pantallas son de la app real, con atletas de ejemplo.</p></div>
  <div class="fila sube"><div class="pant"><div class="m"><img loading="lazy" src="__PORTADA__" width="585" height="1266" alt="Portada de la sesión Torso B con duración, ejercicios y la nota del coach"></div><div class="m"><img loading="lazy" src="__SESION__" width="585" height="1266" alt="Sesión en marcha: series apuntadas y temporizador de descanso"></div></div>
    <div><span class="num"><i>__I_reloj__</i>Entrenamiento</span><h3>Un plan escrito para ti, serie a serie</h3><p>Abres la app y ves la sesión de hoy: ejercicios, series, repeticiones y cuánto esfuerzo toca. Apuntas los kilos y el descanso arranca solo.</p>
    <ul><li>Vídeo y técnica de cada ejercicio</li><li>Alternativas si el gimnasio está lleno, entrenas en casa o estás de viaje</li><li>Si un día tienes 25 minutos, la sesión se ajusta</li></ul></div></div>
  <div class="fila inv sube"><div class="pant"><div class="m"><img loading="lazy" src="__PROGRESO__" width="585" height="1266" alt="Pantalla de progreso: peso, récords, tonelaje y racha de semanas"></div><div class="m"><img loading="lazy" src="__CHECKIN__" width="585" height="1266" alt="Check-in semanal con las respuestas del atleta"></div></div>
    <div><span class="num"><i>__I_grafica__</i>Seguimiento</span><h3>Ves si avanzas, sin hacer cuentas</h3><p>Tu peso, tus récords y tu constancia, semana a semana. Y cada semana un check-in corto: cómo has dormido, cómo vas de energía, qué te ha costado.</p>
    <ul><li>Con eso decido qué cambia la semana siguiente</li><li>Fotos y medidas, solo si quieres y solo las vemos tú y yo</li></ul></div></div>
  <div class="fila sube"><div class="pant"><div class="m"><img loading="lazy" src="__COMIDAS__" width="585" height="1266" alt="Pantalla de comidas: calorías y proteína del día y el menú de la semana"></div><div class="m"><img loading="lazy" src="__MENSAJES__" width="585" height="1266" alt="Conversación con el coach dentro de la app"></div></div>
    <div><span class="num"><i>__I_plato__</i>Nutrición</span><h3>Comer bien sin vivir a dieta</h3><p>Objetivos de calorías y proteína, un menú semanal que puedes cambiar y un recetario con más de 500 recetas con sus macros. Si comes fuera, la app te dice cómo cuadrarlo.</p>
    <ul><li>Lista de la compra hecha a partir de tu menú</li><li>Recetas veganas, sin gluten y sin lactosa</li></ul></div></div>
</div></section>

<section class="charla"><div class="in">
  <div class="sube"><h2>Alguien al otro lado</h2><p class="t">No es un programa que se rellena solo. Reviso tus sesiones y tu check-in cada semana, y me escribes cuando algo no cuadra.</p></div>
  <div class="hilo sube" role="img" aria-label="Ejemplo de conversación entre un atleta y su coach">
    <div class="b tu"><small>Tú</small>Hoy el press militar me ha molestado en el hombro. ¿Lo quito?</div>
    <div class="b co"><small>Tu coach</small>No lo quites: cámbialo por press con mancuernas sentado y baja un punto de esfuerzo. Te lo dejo ya puesto en la sesión del jueves.</div>
    <div class="b tu"><small>Tú</small>Perfecto. Te mando vídeo de la sentadilla, que no sé si bajo lo suficiente.</div>
    <div class="b co"><small>Tu coach</small>Mándalo desde la propia sesión y te lo devuelvo comentado.</div>
    <p class="nota">Conversación de ejemplo</p>
  </div>
</div></section>

<section><div class="in">
  <div class="entrada centro sube"><h2>Todo lo que lleva dentro</h2><p>Lo que usarás cada semana, sin ir saltando entre cinco aplicaciones.</p></div>
  <div class="bento">__BENTO__</div>
</div></section>

<section style="padding-top:0"><div class="in"><div class="entrada sube" style="margin-bottom:1rem"><h2>Míralo por dentro</h2></div></div>
  <div class="galeria" tabindex="0" aria-label="Galería de pantallas de la app">__GALERIA__</div>
</section>

<section class="pasos" id="como"><div class="in">
  <div class="entrada sube"><h2>Cómo empezamos</h2><p>De escribirme a tu primera sesión, tres pasos.</p></div>
  <ol>
    <li class="sube"><h3>Me escribes</h3><p>Rellenas el formulario: qué buscas, cómo entrenas ahora y de cuánto tiempo dispones.</p></li>
    <li class="sube"><h3>Valoración inicial</h3><p>Repasamos tu punto de partida, tu historial y, si tomas medicación o tienes alguna lesión, cómo tenerlo en cuenta.</p></li>
    <li class="sube"><h3>Tu plan, en tu móvil</h3><p>Recibes tu código, activas la app y ya tienes tu primera semana. A partir de ahí, revisión cada semana.</p></li>
  </ol>
</div></section>

<section id="quien"><div class="in">
  <div class="ficha sube">
    <div class="retrato" aria-hidden="true">PF</div>
    <div><h2>Pelayo Fernández Cidón</h2><p class="rol">Médico internista y entrenador</p>
      <p>Soy médico especialista en medicina interna en el Hospital Universitario La Paz (Madrid). Llevo más de quince años entrenando fuerza y desde 2020 dirijo FBE, Fuerza Basada en Evidencia.</p>
      <p>Programo con lo que dice la evidencia y con lo que cabe en tu semana. Si algo no está demostrado, te lo digo.</p>
      <ul class="sellos"><li>Medicina interna</li><li>Fuerza e hipertrofia</li><li>Nutrición</li><li>Basado en evidencia</li></ul></div>
  </div>
  <div class="encaje sube">
    <div><h3>Es para ti si…</h3><ul><li>Quieres ganar fuerza, perder grasa o las dos cosas</li><li>Tienes poco tiempo y no quieres improvisar</li><li>Empiezas de cero o llevas años y te has estancado</li></ul></div>
    <div class="no"><h3>No es lo que buscas si…</h3><ul><li>Quieres un plan cerrado sin seguimiento</li><li>Buscas resultados en dos semanas</li><li>Necesitas un tratamiento médico: eso es cosa de tu médico</li></ul></div>
  </div>
</div></section>

<section id="dudas" style="padding-top:0"><div class="in">
  <div class="entrada centro sube"><h2>Dudas habituales</h2></div>
  <div class="faq sube">__FAQ__</div>
</div></section>

<section class="cierre">__ANILLOS__<div class="in sube"><h2>¿Hablamos?</h2><p>Cuéntame tu caso en el formulario. Te respondo yo.</p><a class="btn claro" href="__C__">Pedir plaza</a></div></section>
<footer><div class="in">
  <div><b>FBE · Fuerza Basada en Evidencia</b><p>Asesoría online de fuerza y nutrición. La asesoría no sustituye a tu médico ni a un tratamiento.</p></div>
  <div><b>La página</b><a href="#app">La app</a><a href="#como">Cómo empezamos</a><a href="#quien">Quién te lleva</a><a href="#dudas">Dudas</a></div>
  <div><b>¿Ya eres atleta?</b><a href="__APP__">Entrar en la app</a><a href="__C__">Pedir plaza</a></div>
</div></footer>
<div class="fijo" id="fijo"><a class="btn claro" href="__C__">Pedir plaza</a></div>
<script>
(function () {
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ya'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' }) : null;
  document.querySelectorAll('.sube').forEach(function (el, i) { if (io) io.observe(el); else el.classList.add('ya'); });
  setTimeout(function () { document.querySelectorAll('.sube').forEach(function (el) { el.classList.add('ya'); }); }, 4000);
  var fijo = document.getElementById('fijo'), cierre = document.querySelector('.cierre');
  function mirar() { var y = window.scrollY || 0, fin = cierre.getBoundingClientRect().top < innerHeight; fijo.classList.toggle('ver', y > 600 && !fin); }
  addEventListener('scroll', mirar, { passive: true }); mirar();
})();
</script>
'''
html = html.replace('__BENTO__', ''.join(f'<div class="caja sube"><i>{ico(i)}</i><h3>{t}</h3><p>{d}</p></div>' for i, t, d in bento))
html = html.replace('__FAQ__', ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq))
gal = [('hoy', 'Hoy'), ('portada', 'Tu sesión'), ('sesion', 'Serie a serie'), ('progreso', 'Progreso'), ('comidas', 'Comidas'), ('checkin', 'Check-in'), ('mensajes', 'Mensajes')]
html = html.replace('__GALERIA__', ''.join(f'<figure><div class="m"><img loading="lazy" src="__{k.upper()}__" width="585" height="1266" alt="Pantalla de la app: {c}"></div><figcaption>{c}</figcaption></figure>' for k, c in gal))
for k in I: html = html.replace(f'__I_{k}__', ico(k))
for k in ('hoy', 'portada', 'sesion', 'progreso', 'checkin', 'comidas', 'mensajes'): html = html.replace('__' + k.upper() + '__', img(k))
html = html.replace('__ANILLOS__', ANILLOS).replace('__C__', CONTACTO).replace('__APP__', APP)
open('web-fbe-equipo.html', 'w', encoding='utf-8').write(html); print(len(html) // 1024, 'KB')
