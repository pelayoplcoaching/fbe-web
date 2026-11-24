# Bloques «Código» de la página de pago de la Revisión de evidencia FBE (MailerLite).
# python3 bloques.py  -> escribe salida/top.html, hero.html, cab.html, pie.html, cuerpo.html y mock.html
import os
import re

WEB = "https://fuerzabasadaenevidencia.com"
IMG = WEB + "/revision/img"
PORTAL = "https://billing.stripe.com/p/login/eVq28q7WA8uNeMxakCbV600"
CORREO = "newsletter@pelayoplcoaching.com"
os.makedirs("salida", exist_ok=True)


def css_min(c):
    c = re.sub(r"/\*.*?\*/", "", c, flags=re.S)
    cadenas = []
    def guarda(m):
        cadenas.append(m.group(0))
        return f"\x00{len(cadenas) - 1}\x00"
    c = re.sub(r'"(?:[^"\\]|\\.)*"', guarda, c)
    c = re.sub(r"\s*\n\s*", "", c)
    c = re.sub(r"\s*([{};,>])\s*", r"\1", c)
    c = c.replace(";}", "}")
    c = re.sub(r"\x00(\d+)\x00", lambda m: cadenas[int(m.group(1))], c)
    return c.strip()


CSS = css_min(open("estilo.css", encoding="utf-8").read())
CSS_URL = WEB + "/revision/pago.css"
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "revision", "pago.css"), "w", encoding="utf-8").write(CSS + "\n")
LIMITE = 4500  # bytes por bloque: MailerLite descarta sin avisar lo que pasa de unos 5.000 caracteres

TOP = f"""<style>@import url({CSS_URL});body,.ml-site,.ml-landing-page,.ml-landing-page .ml-section-wrapper{{background:#F2EFE9!important}}</style>
<div id="fbe-top" class="fbe fbe-top">
<div class="fbe-barra"><a class="fbe-marca" href="{WEB}/"><img src="{WEB}/favicon.svg" width="38" height="38" alt=""><span>Fuerza Basada en Evidencia</span></a><a class="fbe-top-cta" href="#suscribirse">Suscribirme · <b>0,99&nbsp;€</b></a></div>
<div class="fbe-mast"><span>Revisión de evidencia FBE</span><span>Un número al mes · el último viernes</span><span>0,99&nbsp;€ al mes</span></div>
</div>"""

HERO = f"""<style>.fbe-hero{{min-width:0}}</style>
<div id="fbe-hero" class="fbe fbe-hero">
<p class="fbe-kick">Para curiosos y profesionales</p>
<h1 class="fbe-h1">Seis estudios del mes <em>y qué cambian en el gimnasio y en la&nbsp;consulta.</em></h1>
<p class="fbe-lead">Leídos por un internista y resumidos en fichas de un minuto: qué hicieron, qué encontraron, cuánto fiarse y qué&nbsp;cambia.</p>
<div class="fbe-cta"><a class="fbe-btn" href="#suscribirse">Suscribirme por 0,99&nbsp;€ al mes</a><p class="fbe-cta-nota">Un número al mes, el último viernes.<br>Sin permanencia. IVA incluido.</p></div>
<ul class="fbe-chips"><li>Seis estudios recientes</li><li>Cuánto fiarse de cada uno</li><li>El enlace a cada estudio</li></ul>
<div class="fbe-firma"><img src="{WEB}/img/firma-pelayo.webp" width="46" height="46" alt=""><p><b>Pelayo Fernández Cidón</b><span>Médico internista · prescriptor de ejercicio físico</span></p></div>
</div>"""

CAB = f"""<div id="fbe-cab" class="fbe fbe-cab">
<span id="suscribirse" class="fbe-ancla">&#8203;</span>
<div class="fbe-cab-img"><img src="{IMG}/portada.webp" width="1200" height="800" alt="Ilustración: tres libros, una lupa, una mancuerna y un fonendoscopio"><p class="fbe-sello" aria-hidden="true"><span>6<small>estudios al mes</small></span></p></div>
<p class="fbe-cab-kick">Suscripción mensual</p>
<p class="fbe-cab-tit">Revisión de evidencia FBE</p>
<p class="fbe-precio"><b>0,99&nbsp;€</b><span>al mes</span></p>
<p class="fbe-precio-nota">IVA incluido · sin permanencia · baja cuando quieras</p>
<ul class="fbe-incluye"><li>Un número al mes, el último viernes, en tu correo</li><li>Seis estudios recientes en fichas de un minuto</li><li>Cuánto fiarse de cada estudio, y el enlace para ir a la fuente</li><li>14 días para desistir: te devuelvo lo pagado</li></ul>
</div>"""

PIE = f"""<div id="fbe-pie" class="fbe fbe-pie">
<p class="fbe-seguro fbe-ic-candado">Pago con tarjeta a través de Stripe: yo no veo los datos de tu tarjeta.</p>
<p class="fbe-seguro fbe-ic-correo">Te llega un recibo por correo con cada cobro.</p>
<p class="fbe-ya">¿Ya estás suscrito? <a href="{PORTAL}">Gestionar mi suscripción</a></p>
</div>"""

N0 = [
    ("01", "Fármacos y ejercicio", "Tirzepatida", "entrenar fuerza supervisada tres días por semana conserva 1,1&nbsp;kg más de masa magra y cambia perder fuerza por ganarla.", "mod", "Moderada", "Nature Medicine", "ensayo aleatorizado"),
    ("02", "Salud mental", "Antipsicóticos", "el ejercicio supervisado mejora los síntomas negativos y, un poco, la grasa; no la tensión, la glucosa ni los lípidos.", "mod", "Moderada", "Journal of Affective Disorders", "metaanálisis"),
    ("03", "Hospital y mayores", "Ingreso hospitalario", "unas cuatro sesiones tipo Vivifrail en mayores de 70 dejan el SPPB al alta 3&nbsp;puntos por encima del cuidado habitual, en un ensayo pequeño.", "baja", "Baja", "Age and Ageing", "ensayo aleatorizado"),
    ("04", "Cardiovascular", "Tensión arterial", "los diez tipos de ejercicio estudiados la bajan; destacan el acuático, el mente-cuerpo y el isométrico, pero el orden entre ellos es poco fiable.", "alta", "Alta", "Maturitas", "metaanálisis en red"),
    ("05", "Actividad física", "Moverse más", "el coaching telefónico quincenal de un fisio suma unos 900&nbsp;pasos al día a los 6&nbsp;meses; una llamada inicial con SMS, bastante menos.", "alta", "Alta", "BMJ", "ensayo aleatorizado"),
    ("06", "Oncología", "Cáncer gastroesofágico", "entrenar durante la neoadyuvancia no hizo que más pacientes llegaran a la cirugía, y la supervivencia, un resultado secundario, fue peor.", "mod", "Moderada", "JAMA Network Open", "ensayo aleatorizado"),
]
N0_HTML = "".join(
    f'<li class="fbe-sube"><img src="{IMG}/n0-{int(n)}.webp" width="480" height="240" loading="lazy" alt=""><div>'
    f'<p class="fbe-n0-tema"><b>{n}</b>{tema}</p><p class="fbe-n0-frase"><strong>{tit}</strong>: {frase}</p>'
    f'<p class="fbe-n0-pie"><span class="fbe-niv fbe-{niv}">{niv_t}</span><span class="fbe-fuente"><em>{rev}</em> · {tipo}</span></p></div></li>'
    for n, tema, tit, frase, niv, niv_t, rev, tipo in N0)
MOSAICO = "".join(f'<img src="{IMG}/n0-{i}.webp" width="480" height="240" loading="lazy" alt="">' for i in range(1, 7))

FAQ = [
    ("¿Cuánto cuesta y cómo se paga?", "0,99&nbsp;€ al mes, IVA incluido. El cobro es automático, con tarjeta, a través de Stripe: el primero al suscribirte y después cada mes el mismo día. Yo no veo los datos de tu tarjeta, y te llega un recibo por correo con cada cobro."),
    ("¿Cuándo llega cada número?", "El último viernes de cada mes, en el correo con el que te suscribas. Si algún mes un número se retrasa, te aviso."),
    ("¿Puedo darme de baja cuando quiera?", f"Sí, no hay permanencia. Te das de baja desde <a href=\"{PORTAL}\">la página de gestión de tu suscripción</a> (te llega un código a tu correo para entrar) o escribiéndome. La baja se hace al final del mes ya pagado: hasta entonces sigues recibiendo la revisión."),
    ("¿Y si me arrepiento?", f"Tienes 14 días naturales desde que te suscribes para desistir sin dar explicaciones: escríbeme a <a href=\"mailto:{CORREO}\">{CORREO}</a> y te devuelvo lo pagado."),
    ("¿Necesito ser sanitario?", "No. Está escrita para sanitarios y entrenadores, con el lenguaje de los estudios, pero cada número trae un glosario con los términos técnicos."),
    ("¿La newsletter del domingo sigue siendo gratis?", "Sí. La revisión va aparte: la newsletter del domingo sigue igual."),
    ("¿Puedo reenviársela a un colega?", "Puedes reenviar un número suelto a un colega. Lo que no está permitido es redistribuirla de forma sistemática ni publicarla."),
    ("¿Sustituye a la valoración de un médico?", "No. Resume estudios publicados con fines divulgativos: no sustituye a la valoración de un médico, al juicio clínico ni a un plan de ejercicio individual."),
]
FAQ_HTML = "".join(
    f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))

CUERPO = f"""<div id="fbe-cuerpo" class="fbe fbe-cuerpo">
<section class="fbe-sec" aria-label="La revisión en cifras"><ul class="fbe-cifras fbe-sube"><li><b>6</b><span>estudios cada mes</span></li><li><b>1&nbsp;min</b><span>por ficha</span></li><li><b>4</b><span>preguntas por estudio</span></li><li><b>0,99&nbsp;€</b><span>al mes, IVA incluido</span></li></ul></section>
<section class="fbe-sec" id="por-dentro">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">Cómo es por dentro</p><h2 class="fbe-h2">Una ficha por estudio, de un minuto</h2><p>Cada ficha dice qué hicieron, qué encontraron, cuánto fiarse y qué cambia: lo que haría distinto mañana, o «nada todavía» si es el caso.</p></div>
<div class="fbe-ficha-grid"><div class="fbe-ficha-izq"><ol class="fbe-partes">
<li class="fbe-sube"><b>1</b><div><strong>Qué hicieron</strong><span>Arriba, la ficha técnica resume el estudio en cuatro datos: diseño, personas, duración y qué mide.</span></div></li>
<li class="fbe-sube"><b>2</b><div><strong>Qué encontraron</strong><span>La cifra que importa y, cuando ayuda, el gráfico del efecto con su intervalo.</span></div></li>
<li class="fbe-sube"><b>3</b><div><strong>Cuánto fiarse</strong><span>Certeza alta, moderada o baja, y por qué.</span></div></li>
<li class="fbe-sube"><b>4</b><div><strong>Qué cambia</strong><span>Lo que haría distinto mañana en consulta o en el gimnasio, o «nada todavía».</span></div></li>
</ol><div class="fbe-leyenda fbe-sube"><p>La certeza, de un vistazo</p><ul><li><span class="fbe-niv fbe-alta">Alta</span></li><li><span class="fbe-niv fbe-mod">Moderada</span></li><li><span class="fbe-niv fbe-baja">Baja</span></li></ul></div></div>
<figure class="fbe-capturas fbe-sube"><img class="fbe-cap-ficha" src="{IMG}/ficha.webp" width="760" height="1381" loading="lazy" alt="Captura de la ficha 01 del número 0: tirzepatida y fuerza, con su ficha técnica y la cifra de 1,1 kg menos de masa magra perdida"><img class="fbe-cap-efecto" src="{IMG}/efecto.webp" width="720" height="618" loading="lazy" alt="Captura de un gráfico del efecto: 3,1 puntos de mejora, con un intervalo de 1,7 a 4,5 y el umbral clínico en 3"><figcaption>Ficha 01 y gráfico del efecto de la ficha 02, del número 0</figcaption></figure></div>
</section>
<section class="fbe-sec">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">Un número de ejemplo</p><h2 class="fbe-h2">El número <span class="fbe-num">0</span>, en un minuto</h2><p>Seis estudios: cuatro ensayos aleatorizados y dos metaanálisis.</p></div>
<ol class="fbe-n0">{N0_HTML}</ol>
<blockquote class="fbe-cita fbe-sube"><p>Este número tiene un hilo: el ejercicio empieza a tratarse como parte del tratamiento, no como un consejo al final de la consulta.</p><p class="fbe-cita-pie">Del número 0</p></blockquote>
</section>
<section class="fbe-sec">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">En cada número</p><h2 class="fbe-h2">Qué trae cada número</h2></div>
<ul class="fbe-trae">
<li class="fbe-sube fbe-ic-lupa"><strong>Seis estudios recientes</strong><span>De entrenamiento, nutrición y fármacos con ejercicio.</span></li>
<li class="fbe-sube fbe-ic-ficha"><strong>Fichas de un minuto</strong><span>Qué hicieron, qué encontraron, cuánto fiarse y qué cambia.</span></li>
<li class="fbe-sube fbe-ic-grafico"><strong>El efecto, con su intervalo</strong><span>Gráficos para ver de un vistazo cuánto cambia y con cuánta precisión.</span></li>
<li class="fbe-sube fbe-ic-reloj"><strong>En un minuto</strong><span>Las seis conclusiones juntas, al principio.</span></li>
<li class="fbe-sube fbe-ic-libro"><strong>Glosario rápido</strong><span>Si un término no te suena, lo tienes al final.</span></li>
<li class="fbe-sube fbe-ic-enlace"><strong>El enlace a cada estudio</strong><span>Para ir a la fuente cuando quieras.</span></li>
</ul>
<div class="fbe-revistas fbe-sube"><p>Revistas del número 0</p><ul><li>Nature Medicine</li><li>BMJ</li><li>JAMA Network Open</li><li>Journal of Affective Disorders</li><li>Age and Ageing</li><li>Maturitas</li></ul></div>
</section>
<section class="fbe-sec">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">Cómo funciona</p><h2 class="fbe-h2">Una suscripción sin sorpresas</h2></div>
<ol class="fbe-pasos">
<li class="fbe-sube"><span class="fbe-paso-n fbe-ic-candado">Hoy</span><strong>Te suscribes aquí</strong><p>0,99&nbsp;€ al mes con tarjeta, a través de Stripe: el primer cobro al suscribirte y después cada mes el mismo día. Te llega un correo de bienvenida y un recibo con cada cobro.</p></li>
<li class="fbe-sube"><span class="fbe-paso-n fbe-ic-calendario">El último viernes</span><strong>Te llega cada número</strong><p>Seis estudios nuevos en tu correo, en fichas de un minuto y con el enlace a cada estudio.</p></li>
<li class="fbe-sube"><span class="fbe-paso-n fbe-ic-ajustes">Cuando quieras</span><strong>Lo gestionas tú</strong><p>Desde la página de gestión de tu suscripción ves tus recibos, cambias la tarjeta o te das de baja. Sin permanencia: sigues recibiendo la revisión hasta el final del mes pagado.</p></li>
</ol>
</section>
<section class="fbe-sec">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">Para quién es</p><h2 class="fbe-h2">Escrita para sanitarios y entrenadores, abierta a quien quiera aprender</h2></div>
<div class="fbe-quien">
<div class="fbe-q fbe-q-si fbe-sube"><h3>Es para ti si…</h3><ul><li>Prescribes, enseñas o practicas ejercicio y quieres saber qué dicen los estudios nuevos.</li><li>Te interesa cuánto fiarte de cada resultado, no solo el titular.</li><li>Te gusta aprender aunque no te dediques a esto: va con el lenguaje de los estudios, y con glosario.</li></ul></div>
<div class="fbe-q fbe-q-no fbe-sube"><h3>Lo que no es</h3><ul><li>Un plan de ejercicio individual.</li><li>Un sustituto de la valoración de un médico ni del juicio clínico.</li></ul></div>
</div>
</section>
<section class="fbe-sec">
<div class="fbe-autor fbe-sube">
<div class="fbe-autor-foto"><img src="{WEB}/img/foto-pelayo.webp" width="720" height="900" loading="lazy" alt="Pelayo Fernández Cidón, médico internista"></div>
<div class="fbe-autor-txt">
<p class="fbe-kick">Quién te escribe</p>
<h3>Pelayo Fernández Cidón</h3>
<p class="fbe-rol">Médico internista · prescriptor de ejercicio físico</p>
<p>Cada mes elijo seis estudios recientes de entrenamiento, nutrición y fármacos con ejercicio, y los resumo en fichas de un minuto. Cada número lo reviso yo antes de enviarlo, y cada ficha lleva el enlace al estudio para que puedas ir a la fuente.</p>
<ul class="fbe-cred"><li>Especialista en Medicina Interna en el Hospital Universitario La Paz</li><li>Médico colegiado n.º 282875610 (Colegio de Médicos de Madrid)</li><li>Máster y experto universitario en nutrición clínica</li><li>Experto universitario en entrenamiento de fuerza</li><li>Quince años entrenando fuerza y diez de guardias en urgencias</li></ul>
<p class="fbe-autor-links"><a href="{WEB}/evidencia.html">Cómo trabajo la evidencia →</a><a href="{WEB}/quien-soy.html">Quién soy →</a></p>
</div>
</div>
</section>
<section class="fbe-sec">
<div class="fbe-final fbe-sube">
<div><p class="fbe-kick">Suscripción mensual</p><h2 class="fbe-h2">Seis estudios nuevos, el último viernes de cada mes.</h2>
<p class="fbe-final-precio"><b>0,99&nbsp;€</b><span>al mes<br>IVA incluido</span></p>
<ul><li>Sin permanencia: te das de baja cuando quieras</li><li>14 días para desistir: te devuelvo lo pagado</li><li>Un recibo por correo con cada cobro</li></ul>
<a class="fbe-btn" href="#suscribirse">Suscribirme</a></div>
<div class="fbe-final-mos" aria-hidden="true">{MOSAICO}</div>
</div>
</section>
<section class="fbe-sec" id="preguntas">
<div class="fbe-sec-cab fbe-sube"><p class="fbe-kick">Preguntas</p><h2 class="fbe-h2">Antes de suscribirte</h2></div>
<div class="fbe-faq">{FAQ_HTML}</div>
</section>
<div class="fbe-barra-movil"><a class="fbe-btn" href="#suscribirse">Suscribirme · 0,99&nbsp;€ al mes</a></div>
</div>"""

def trocea(html):
    interior = html[html.index(">") + 1:html.rindex("</div>")].strip()
    partes = re.split(r"\n(?=<section |<div class=\"fbe-barra-movil)", interior)
    trozos, actual = [], ""
    for parte in partes:
        if actual and len((actual + "\n" + parte).encode("utf-8")) > LIMITE - 80:
            trozos.append(actual); actual = parte
        else:
            actual = (actual + "\n" + parte) if actual else parte
    trozos.append(actual)
    return [f'<div id="fbe-cuerpo-{i}" class="fbe fbe-cuerpo">\n{t}\n</div>' for i, t in enumerate(trozos, 1)]


TROZOS = trocea(CUERPO)
BLOQUES = {"top": TOP, "hero": HERO, "cab": CAB, "pie": PIE}
BLOQUES.update({f"cuerpo-{i}": t for i, t in enumerate(TROZOS, 1)})
for f in os.listdir("salida"):
    if f.startswith("cuerpo"):
        os.remove(os.path.join("salida", f))
for k, v in BLOQUES.items():
    open(f"salida/{k}.html", "w", encoding="utf-8").write(v)
    n = len(v.encode("utf-8"))
    print(k, n, "bytes", "<- DEMASIADO LARGO" if n > LIMITE else "")
print("css", len(CSS.encode("utf-8")), "bytes en revision/pago.css")

# ---- Maqueta local con la misma estructura que MailerLite (para capturas antes de pegarlo) ----
def seccion(sid, filas, fondo="#fff"):
    return (f'<div class="ml-section-wrapper" id="{sid}" style="background-color:{fondo}"><div class="max-w-6xl ml-animate mx-auto w-full px-4">'
            f'<div class="transition-all"><div class="gap-12 grid">{filas}</div></div></div></div>')


def fila(columnas, cards=True):
    cols = "".join(
        (f'<div class="grid relative group/card items-start border h-full" style="padding:32px;background:#F8F1FD;border-color:#9E58D3;border-radius:32px">' if cards else '<div class="ml-column">')
        + '<div class="list-group flex flex-col">' + "".join(f'<div class="list-group-item"><div>{m}</div></div>' for m in col) + '</div></div>'
        for col in columnas)
    n = len(columnas)
    return f'<div class="ml-desktop-layout relative"><div class="grid items-start ml-mobile-cols-1 gap-8 gap-x-16" style="grid-template-columns:repeat({n},minmax(0,1fr))">{cols}</div></div>'


PRODUCTO = """<div class="flex flex-col items-center space-y-8 justify-center place-items-center"><div class="flex-shrink-0 w-full"><div class="w-full flex gap-x-16 gap-y-8 flex-wrap flex-col">
<div class="relative w-auto overflow-hidden w-full"><a><div class="ml-mobile-flex flex w-full relative overflow-hidden aspect-square"><div class="flex w-full"><img class="w-full h-full object-cover" src="https://fuerzabasadaenevidencia.com/revision/img/portada.webp"></div></div></a></div>
<div class="w-full flex-1"><div class="items-center mb-12 flex flex-col"><div class="text-center"><div><h3 class="ml-content-heading">Revisión de evidencia FBE</h3></div></div><div class="text-center mt-3"><div><p class="ml-p text-base">Un número al mes...</p><p class="ml-p text-base"><strong>0,99 € al mes, IVA incluido</strong></p></div></div></div>
<div><div class="alert alert-danger hidden">Something went wrong</div><div class="items-center flex flex-col"><div class="flex w-full"><div class="ml-mobile-flex w-full flex justify-start"><div class="ml-btn-grid"><a class="ml-btn ml-btn-secondary" style="background:#391853;border:1.6px solid #93385F;border-radius:32px;padding:2px 21px;color:#fff">Suscribirme</a></div></div></div></div>
<div class="hidden items-center my-4"><div><h4 class="ml-content-heading"><strong>¡Gracias! Ya estás suscrito</strong></h4><p class="ml-p text-base">Te llega un correo...</p></div></div></div></div></div></div></div>"""

ACORDEON = "".join(
    f'<div><div class="relative{" item-active" if i == 0 else ""} ml-border"><div class="collapse overflow-visible collapse-arrow"><input type="radio" name="acc" class="hidden" {"checked" if i == 0 else ""}>'
    f'<label class="collapse-title cursor-pointer"><span class="block w-fit pr-1 text-xl font-medium"><div><h4 class="ml-content-heading">{t}</h4></div></span></label>'
    f'<div class="collapse-content"><p class="ml-p">Texto de ejemplo de la condición (en la página real, el de MailerLite).</p></div></div></div></div>'
    for i, t in enumerate(["Quién presta el servicio", "Qué recibes", "Precio y pago", "Baja", "Desistimiento", "Tus datos", "Uso del contenido", "Cambios y ley aplicable"]))

PIE_ML = """<div id="R5cV8xZ0tN2yH3uG" style="background-color:#E6D5FD"><div class="max-w-6xl mx-auto w-full px-4"><div class="gap-8 grid" style="padding:48px 0">
<div class="ml-desktop-layout relative"><div class="grid items-start ml-mobile-cols-1 gap-8" style="grid-template-columns:1fr 1fr">
<div class="ml-column"><div class="list-group"><div class="list-group-item"><h4 class="ml-content-heading">Un número al mes, el último viernes. Sin permanencia.</h4><p class="ml-p">Te das de baja cuando quieras desde la página de gestión de tu suscripción, y tienes 14 días para desistir.</p></div></div></div>
<div class="ml-column"><div class="list-group"><div class="list-group-item"><h4 class="ml-content-heading">¿Ya estás suscrito?</h4><a class="ml-btn ml-btn-primary">Gestionar mi suscripción</a></div></div></div></div></div>
<div class="ml-desktop-layout relative"><div class="grid items-start" style="grid-template-columns:1fr 1fr"><div class="ml-column"><div class="list-group"><div class="list-group-item"><p class="ml-p">© 2026 Pelayo Fernández Cidón. Todos los derechos reservados.</p><p class="ml-p"><a href="#">Política de privacidad</a></p></div></div></div><div class="ml-column"><div class="list-group"><div class="list-group-item"><p class="ml-p">[redes]</p></div></div></div></div></div>
</div></div></div>"""

MOCK = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maqueta</title>
<style>*,*::before,*::after{{box-sizing:border-box}}body{{margin:0;font-family:Inter,Arial,sans-serif}}h1,h2,h3,h4,p{{margin:0}}.hidden{{display:none}}.grid{{display:grid}}.flex{{display:flex}}.flex-col{{flex-direction:column}}.max-w-6xl{{max-width:72rem}}.mx-auto{{margin-left:auto;margin-right:auto}}.px-4{{padding-left:1rem;padding-right:1rem}}@media(min-width:768px){{.max-w-6xl{{padding-left:2rem!important;padding-right:2rem!important}}}}.gap-12{{gap:3rem}}.gap-8{{gap:2rem}}.gap-x-16{{column-gap:4rem}}.border{{border-style:solid;border-width:1px}}.relative{{position:relative}}.w-full{{width:100%}}.ml-section-wrapper{{padding:48px 0}}.aspect-square{{aspect-ratio:1/1}}.object-cover{{object-fit:cover}}.items-center{{align-items:center}}.text-center{{text-align:center}}.mb-12{{margin-bottom:3rem}}.space-y-8>*+*{{margin-top:2rem}}.list-group-item{{padding:8px 0}}.collapse{{position:relative;display:grid;overflow:hidden}}.collapse>input{{position:absolute;opacity:0}}.collapse-title{{position:relative;padding:1rem}}.collapse-content{{display:none;padding:0 1rem 1rem}}.collapse>input:checked~.collapse-content{{display:block}}.collapse-arrow>.collapse-title::after{{position:absolute;content:"";width:.5rem;height:.5rem;right:1.4rem;top:1.9rem;transform:rotate(45deg);border-right:2px solid;border-bottom:2px solid}}.divide-y>*+*{{border-top:1px solid #ccc}}@media(max-width:767px){{.ml-mobile-cols-1{{grid-template-columns:1fr!important}}}}.ml-site h1,.ml-site h2,.ml-site h3,.ml-site h4{{font-family:Inter,Arial;color:#391853}}.ml-site p{{margin-bottom:.5em}}</style></head>
<body><main class="ml-site"><div class="ml-landing-page">
{seccion("Hero-with-menu", fila([[TOP, HERO], [CAB, PRODUCTO, PIE]]))}
{seccion("Testimonio-Header", fila([TROZOS + ["", '<h2 class="ml-content-heading">Condiciones de la suscripción</h2>']], cards=False), "#EEEEEE")}
{seccion("One-column", fila([['<div class="flex w-full justify-center"><div class="w-full divide-y">' + ACORDEON + '</div></div>']], cards=False), "#EEEEEE")}
</div>{PIE_ML}</main></body></html>"""
open("salida/mock.html", "w", encoding="utf-8").write(MOCK)
print("mock", len(MOCK.encode("utf-8")), "bytes")
