import re, json, os, shutil
src = open('landing5.py', encoding='utf-8').read()
src = src[:src.rindex("open('web-fbe-equipo.html'")]
exec(src)
SAL = os.environ.get('FBE_SAL', '..')
FORM = 'https://noteforms.com/forms/formulario-inicial-fbe-coaching-online-snl8tn'
STRIPE = 'https://buy.stripe.com/9B6bJ0ccQ4exeMxcsKbV601'
CALC = 'https://calculadoradeproteina.fuerzabasadaenevidencia.com/'
PRIV = 'privacidad.html' if os.environ.get('FBE_CORREO') else 'https://fbe-politica_de_privacidad.mailerpage.io'
TERM = 'https://storage.googleapis.com/mailerlite-uploads-prod/1626427/HiBsw8Jed1HGMWBAioHtfU42FmBM9BSXBGOiafMN.pdf'
REDES = [('Instagram', 'https://www.instagram.com/fuerzabasadaenevidencia/'), ('YouTube', 'https://www.youtube.com/@FuerzaBasadaEnEvidencia'), ('X', 'https://x.com/PelayoPLcoach'), ('Threads', 'https://www.threads.com/@fuerzabasadaenevidencia')]
PAGS = [('quien-soy.html', 'Quién soy'), ('programas.html', 'Programas'), ('puesta-a-punto.html', 'Puesta a punto'), ('guias.html', 'Guías'), ('newsletter.html', 'Newsletter'), ('dudas.html', 'Dudas')]
def nav(act=''): return ''.join(f'<a href="{u}"{" class=\"aqui\" aria-current=\"page\"" if u == act else ""}>{t}</a>' for u, t in PAGS)
def cabecera(act=''):
    return f'''<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="avance" aria-hidden="true"><i id="avance"></i></div>
<div class="cab"><div class="in">
  <a class="logo" href="index.html"><i>{LOBO}</i><span>Fuerza Basada en Evidencia</span></a>
  <nav aria-label="Páginas" id="nav">{nav(act)}</nav>
  <button class="tema" id="tema" type="button" aria-label="Cambiar entre tema claro y oscuro"><span class="sol">{ico("sol")}</span><span class="luna">{ico("luna")}</span></button>
  <a class="btn peq claro" href="{FORM}">Pedir plaza</a>
  <details class="menu"><summary aria-label="Abrir el menú"><span></span></summary><div><a href="index.html">Inicio</a>{nav(act)}<a class="app" href="{APP}">Ya soy atleta: entrar</a></div></details>
</div></div>'''
ESCRIBE = ('mailto:' + os.environ['FBE_CORREO']) if os.environ.get('FBE_CORREO') else FORM
PIE = f'''<footer><div class="in">
  <div><div class="marca"><i>{LOBO}</i>Fuerza Basada en Evidencia</div><p>Asesoría online de fuerza y nutrición, por Pelayo Fernández Cidón. La asesoría no sustituye a tu médico ni a un tratamiento.</p><div class="redes">{''.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in REDES)}</div></div>
  <div><b>El sitio</b><a href="index.html">Inicio</a>{''.join(f'<a href="{u}">{t}</a>' for u, t in PAGS[:3])}</div>
  <div><b>Recursos</b><a href="guias.html">Guías</a><a href="newsletter.html">Newsletter</a><a href="{CALC}">Calculadora de proteína</a><a href="dudas.html">Dudas</a></div>
  <div><b>¿Ya eres atleta?</b><a href="{APP}">Entrar en la app</a><a href="{FORM}">Pedir plaza</a><a href="{ESCRIBE}">Escribirme</a></div>
  <div class="legal"><span>© 2026 Fuerza Basada en Evidencia, por Pelayo Fernández Cidón</span><span><a href="{PRIV}" style="display:inline">Privacidad</a> · <a href="{TERM}" style="display:inline">Términos y condiciones</a></span></div>
</div></footer>'''
def cierre(t='¿Hablamos?', s='Cuéntame tu caso en el formulario. Te respondo yo.'): return f'<section class="cierre">{ANILLOS}<div class="marca-agua">{LOBO}</div><div class="in sube"><h2>{t}</h2><p>{s}</p><a class="btn claro" href="{FORM}">Pedir plaza</a></div></section>'
FIJO = f'<a class="arriba" id="arriba" href="#contenido" aria-label="Volver arriba">{ico("sube")}</a>\n<div class="fijo" id="fijo"><a class="sec" href="programas.html">Programas</a><a class="btn claro" href="{FORM}">Pedir plaza</a></div>'

# ---------- inicio ----------
h = html.replace('#contacto-pendiente', FORM)
def cam(a, b):
    global h
    assert a in h, a[:70]
    h = h.replace(a, b)
i0 = h.index('<a class="salto"'); i1 = h.index('<header class="hero"')
h = h[:i0] + cabecera().replace('href="#contenido"', 'href="#semana"') + '\n\n' + h[i1:]
i0 = h.index('<footer>'); i1 = h.index('</footer>') + 9
h = h[:i0] + PIE + h[i1:]
cam('Sin compromiso: primero hablamos y vemos si encaja.', 'Trabajo con un grupo pequeño: si no hay plaza, entras en la lista de espera. Sin compromiso.')
i0 = h.index('<ol>\n    <li class="sube"><h3>Me escribes</h3>'); i1 = h.index('</ol>', i0) + 5
h = h[:i0] + '''<ol class="cuatro">
    <li class="sube"><h3>Rellenas el formulario</h3><p>Qué buscas, cómo entrenas ahora y de cuánto tiempo dispones.</p></li>
    <li class="sube"><h3>Videollamada gratuita</h3><p>Treinta minutos para ver tu punto de partida, tu historial y si te puedo ayudar.</p></li>
    <li class="sube"><h3>Tu plan, a medida</h3><p>Entrenamiento y nutrición pensados para tu horario, tu material y tu salud.</p></li>
    <li class="sube"><h3>Empiezas, y yo sigo ahí</h3><p>Activas la app y ya tienes tu primera semana. Seguimiento, respuesta y ajustes.</p></li>
  </ol>''' + h[i1:]
cam('<section class="pasos" id="como">', '''<section class="sin-arriba"><div class="in"><div class="entrada sube"><h2>Historias reales de profesionales con poco tiempo y muchos turnos</h2></div><div class="testi"><figure class="voz sube" style="margin:0"><blockquote>Todo está explicado con claridad. Sabes qué hacer y por qué hacerlo, eso motiva.</blockquote><figcaption class="quien"><span class="cara">JF<img loading="lazy" src="https://storage.mlcdn.com/account_image/1626427/3je0AlzZzJLdHR2hPlfUXueSQEJEHFpvY5eFyeAt.png" alt="" onerror="this.remove()"></span><span><b>Javier Fernández</b><span>Doctor en Química Inorgánica. Profesor en la Universidad de Oviedo.</span></span></figcaption></figure><figure class="voz sube" style="margin:0"><blockquote>Mi composición corporal ha mejorado y me siento más fuerte en el día a día.</blockquote><figcaption class="quien"><span class="cara">CO<img loading="lazy" src="https://storage.mlcdn.com/account_image/1626427/ajzi9PZ5DTcNkLwOoU3EKzZOxN2VHYzvYVbqc9ec.png" alt="" onerror="this.remove()"></span><span><b>Carlos Oñoro</b><span>Facultativo especialista adjunto en Medicina Interna, Hospital Universitario La Paz.</span></span></figcaption></figure><figure class="voz sube" style="margin:0"><blockquote>Llevaba años en el gimnasio sin rumbo. Por fin tengo una estructura que se adapta a mí.</blockquote><figcaption class="quien"><span class="cara">AD<img loading="lazy" src="https://storage.mlcdn.com/account_image/1626427/LuzGk6tGMePRMD6ztBbq2imqMxj9EZ7Fbl0TiHKN.jpg" alt="" onerror="this.remove()"></span><span><b>Adrián De Vera</b><span>Gestor de la Administración Civil del Estado. Periodista.</span></span></figcaption></figure><figure class="voz sube" style="margin:0"><blockquote>Por fin un enfoque realista para los que trabajamos a turnos.</blockquote><figcaption class="quien"><span class="cara">GB<img loading="lazy" src="https://storage.mlcdn.com/account_image/1626427/wSMCiT5opec4pxkPz5J4STaO49qJP0MM5l9BUprp.jpg" alt="" onerror="this.remove()"></span><span><b>Guillermo Bazarra</b><span>Residente de Neurocirugía, Hospital Universitario La Princesa.</span></span></figcaption></figure></div></div></section>

''' + '<section class="pasos" id="como">')
cam('De escribirme a tu primera sesión, tres pasos.', 'De escribirme a tu primera sesión, cuatro pasos.')
viejo = 'Sí. Hay atletas que solo llevan entrenamiento, otros solo nutrición y otros las dos cosas. La app enseña únicamente lo que tengas contratado.'
assert h.count(viejo) == 2
h = h.replace(viejo, 'El entrenamiento se puede contratar solo. La nutrición por separado es poco habitual: casi siempre va junto al entrenamiento, que es donde más rinde.')
cam('Llevo más de quince años entrenando fuerza y desde 2020 dirijo FBE, Fuerza Basada en Evidencia.</p>', 'Tengo un experto universitario en entrenamiento de fuerza y un máster en nutrición clínica. Llevo más de quince años entrenando y desde 2020 dirijo FBE, Fuerza Basada en Evidencia.</p>\n      <p><a href="quien-soy.html">Mi historia, entera</a></p>')
cam('<li><b>Te escribo yo</b>Con lo que te propondría y lo que cuesta.</li>', '<li><b>Hacemos una videollamada</b>Treinta minutos, gratis, para ver tu caso.</li>')
cam('<small>Orientativo, para adultos sanos que entrenan fuerza. Si tienes enfermedad renal u otra patología, consulta antes con tu médico.</small></div>', f'<small>Orientativo y para riñones sanos. Con enfermedad renal, diabetes de años o dudas, consúltalo antes con una analítica. <a href="{CALC}">Abre la calculadora completa</a>, con edad y reparto por comidas.</small></div>')
cam('<p>Mueve el peso y mira el rango que se usa como referencia al entrenar fuerza: de 1,6 a 2,2 g por kilo y día.</p>', '<p>Elige tu fase, mueve el peso y mira tu rango diario.</p>')
cam('<div><label for="peso">', '<div><div class="fases" role="group" aria-label="Fase"><button type="button" data-a="1.4" data-b="1.6" aria-pressed="false">Mantenimiento</button><button type="button" data-a="1.6" data-b="2.2" aria-pressed="true">Volumen</button><button type="button" data-a="1.8" data-b="2.4" aria-pressed="false">Definición</button></div><label for="peso">')
h += '''<script>(function(){var D=document,p=D.getElementById('peso'),A=1.6,B=2.2;if(!p)return;function r(v){return Math.round(v/5)*5}function pinta(){var k=+p.value,a=r(k*A),b=r(k*B);D.getElementById('peso-o').textContent=k+' kg';D.getElementById('prot').textContent=a+'–'+b+' g';D.getElementById('toma').textContent=r(a/4)+'–'+r(b/4)+' g'}
[].forEach.call(D.querySelectorAll('.fases button'),function(b){b.addEventListener('click',function(){[].forEach.call(D.querySelectorAll('.fases button'),function(x){x.setAttribute('aria-pressed',x===b)});A=+b.dataset.a;B=+b.dataset.b;pinta()})});p.addEventListener('input',pinta);pinta()})();</script>'''
cam('<div class="retrato" aria-hidden="true">PF</div>', '<div class="retrato">PF<img loading="lazy" src="' + ('img/foto-pelayo.webp' if os.path.exists('web-img/foto-pelayo.webp') else 'https://storage.mlcdn.com/account_image/1626427/9IMbm5EtFHhfSdYJ65FBb9koyf2wl2C5kufOmYtZ.png') + '" alt="Pelayo Fernández Cidón" onerror="this.remove()"></div>')
cam('<title>Web FBE Equipo</title>', '<title>Sitio FBE</title>')
cam('</style>\n<script>document.documentElement', open('sitio.css', encoding='utf-8').read() + open('futuro.css', encoding='utf-8').read() + '</style>\n<script>document.documentElement')
open('sitio-inicio.html', 'w', encoding='utf-8').write(h)
CSS = css + open('sitio.css', encoding='utf-8').read() + open('futuro.css', encoding='utf-8').read()
os.makedirs(SAL, exist_ok=True)
open(f'{SAL}/fbe.css', 'w', encoding='utf-8').write(CSS); shutil.copy('mini.js', f'{SAL}/fbe.js')
open(f'{SAL}/index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + h.replace('<title>Sitio FBE</title>', '<title>FBE · Tu plan, tu comida, tu coach</title>').replace('<style>', '</head><body style="margin:0"><style>', 1) + '</body></html>')

