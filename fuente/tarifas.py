# ===== tarifas.html (23/11/2026) =====
# Precios de los tres programas. Sustituye a la pagina vieja planesytarifas.fuerzabasadaenevidencia.com.
# NO se enlaza desde ninguna pagina, lleva noindex siempre y queda fuera del sitemap, del buscador y de la cache sin conexion:
# Pelayo pasa el enlace a quien pide informacion. Cifras: TARIFA (interior.py), las de su pagina vieja; no cambiarlas sin que el lo diga.
# Semestral = dos trimestres con un 10 % menos; anual = cuatro trimestres con un 20 % menos (igual que en la pagina vieja).
TF_VIG = 'del 1 de septiembre de 2026 al 31 de agosto de 2027'
TF_PP = 250                                   # Puesta a punto, pago unico (el mismo precio de puesta-a-punto.html)
TF_PER = [('t', 'Trimestral', '', 1, 1.0, 3, 'al trimestre'), ('s', 'Semestral', '−10 %', 2, .9, 6, 'al semestre'), ('a', 'Anual', '−20 %', 4, .8, 12, 'al año')]
TF_PARA = {'performance': 'Para quien quiere progresar en el entrenamiento con alguien que lo revise cada semana.',
           'elite': 'Entrenamiento y nutrición llevados a la vez, con revisión semanal de los dos planes.',
           'eliteplus': 'Todo lo de Elite y una videollamada semanal de 20 minutos para repasar y ajustar.'}
def _eur(n):
    n = int(round(n)); return f'{n:,}'.replace(',', '.') + ' €'
def _tf_precio(k, per):
    q = TARIFA[k]; return q * per[3] * per[4], q * per[3]
_TF_IMG = _todas('tarifa-performance', 'tarifa-elite', 'tarifa-eliteplus')
def tf_plan(p):
    k, g, n, r, c, items = p
    niv = {'performance': 1, 'elite': 2, 'eliteplus': 3}[k]
    barras = '<span class="nivel" aria-hidden="true">' + ''.join(f'<i{" class=\"on\"" if j < niv else ""}></i>' for j in range(3)) + '</span>'
    img = ilus(f'tarifa-{k}', 'tf-img') if _TF_IMG else ''
    return (f'<article class="plan tf n{niv}{" oro" if k == "eliteplus" else ""} sube" id="{k}" data-q="{TARIFA[k]}">{img}<h3>{n}{barras}</h3>'
            f'<p class="ritmo"><span>{g}</span><span>Revisión semanal</span></p><p class="tf-para">{TF_PARA[k]}</p>'
            f'<p class="tf-eur"><b class="tf-v">{_eur(TARIFA[k])}</b><small class="tf-u">al trimestre</small></p>'
            f'<p class="tf-mas"><s class="tf-s" hidden></s><span class="tf-m">IVA incluido</span></p>'
            f'<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><a class="btn peq" href="{FORM}">Empezar con {n}</a></article>')
def _tf_celda(k, per):
    v, lleno = _tf_precio(k, per)
    return f'<td data-p="{per[0]}"><b>{_eur(v)}</b>' + (f'<s>{_eur(lleno)}</s>' if v != lleno else '') + '</td>'
TF_TABLA = ('<div class="tabla-marco sube" tabindex="0" role="region" aria-label="Todas las tarifas"><table class="tf-tabla" id="tf-tabla" data-p="t"><thead><tr><td></td>'
            + ''.join(f'<th scope="col" data-p="{per[0]}">{per[1]}' + (f' <small>{per[2]}</small>' if per[2] else '') + '</th>' for per in TF_PER) + '</tr></thead><tbody>'
            + ''.join(f'<tr><th scope="row">{p[2]}<small>{p[1]}</small></th>' + ''.join(_tf_celda(p[0], per) for per in TF_PER) + '</tr>' for p in P)
            + '</tbody></table></div>')
TF_JS = '''<script>(function(){var D=document,P={t:[1,1,3,'al trimestre'],s:[2,.9,6,'al semestre'],a:[4,.8,12,'al año']},g=D.getElementById('tf-per'),tb=D.getElementById('tf-tabla');if(!g)return;
function eur(n){return String(Math.round(n)).replace(/\\B(?=(\\d{3})+$)/g,'.')+' €'}
function pinta(k){var p=P[k];[].forEach.call(g.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',b.dataset.p===k)});
[].forEach.call(D.querySelectorAll('.plan.tf'),function(c){var q=+c.dataset.q,lleno=q*p[0],v=lleno*p[1],s=c.querySelector('.tf-s');c.querySelector('.tf-v').textContent=eur(v);c.querySelector('.tf-u').textContent=p[3];s.hidden=v===lleno;s.textContent=eur(lleno);c.classList.remove('tf-cambia');void c.offsetWidth;c.classList.add('tf-cambia')});
if(tb)tb.dataset.p=k;var a=D.getElementById('tf-aviso');if(a)a.textContent=k==='t'?'':(k==='s'?'Semestral: un 10 % menos que dos trimestres.':'Anual: un 20 % menos que cuatro trimestres.')}
g.addEventListener('click',function(e){var b=e.target.closest('button');if(b)pinta(b.dataset.p)})})();</script>'''
_tf_cuerpo = f'''
<section><div class="in">
  <div class="tf-barra sube"><div><h2>Elige cada cuánto pagas</h2><p>El programa es el mismo; cambia el precio.</p></div>
    <div class="tf-per" id="tf-per" role="group" aria-label="Periodo de pago">{"".join(f'<button type="button" data-p="{per[0]}" aria-pressed="{"true" if per[0] == "t" else "false"}">{per[1]}' + (f'<small>{per[2]}</small>' if per[2] else '') + '</button>' for per in TF_PER)}</div></div>
  <p class="tf-aviso" id="tf-aviso" aria-live="polite"></p>
  <div class="planes tres-p">{"".join(tf_plan(p) for p in P)}</div>
  <p class="tf-nota sube">Todos los precios llevan el IVA incluido. Tarifas vigentes {TF_VIG}.</p>
</div></section>
<section class="hoja" id="tabla"><div class="in"><div class="entrada sube"><h2>Todas las tarifas, en una tabla</h2></div>{TF_TABLA}
  <p class="tf-nota sube">El precio tachado es lo que costarían esos mismos meses pagados trimestre a trimestre.</p>
</div></section>
<section><div class="in"><div class="entrada sube"><h2>Lo que llevan los tres</h2></div>
  <ul class="tres sube" style="margin-top:0"><li>{PROG_IMG('prog-plan', 'pesa')}<b>Plan a medida y revisión semanal</b><span>Hecho para tu horario, tu material y tu punto de partida. Lo reviso cada semana.</span></li><li>{PROG_IMG('prog-app', 'video')}<b>La app FBE Equipo</b><span>Sesiones, registro serie a serie, vídeos, recetario y progreso. <a href="index.html#semana">Mírala por dentro</a>.</span></li><li>{PROG_IMG('prog-guias', 'libro')}<b>Las guías</b><span>Para entender lo que haces y por qué.</span></li></ul>
  <p class="sube" style="text-align:center;margin-top:1.5rem"><a href="programas.html#lado">Comparar los tres programas</a></p>
</div></section>
<section class="hoja"><div class="in"><div class="entrada sube"><h2>Cómo se empieza</h2></div>
  <ol class="tf-pasos sube"><li><b>Rellenas el formulario</b><span>Me cuentas tu caso y qué programa te interesa.</span></li><li><b>Hablamos 30 minutos</b><span>Una videollamada gratuita para ver tu punto de partida.</span></li><li><b>Preparo tu plan</b><span>Si encaja, lo tienes en la app y empezamos.</span></li></ol>
</div></section>
<section><div class="in"><div class="calc sube"><div><h3>¿Solo quieres un plan, sin seguimiento?</h3><p>La Puesta a punto es una consulta y un plan de 12 semanas, con lectura de tu analítica. <b>{TF_PP} €, pago único, IVA incluido.</b></p></div><div><a class="btn claro" href="puesta-a-punto.html">Ver la Puesta a punto</a></div></div></div></section>{TF_JS}'''
_tf_cta = BTN + datos(('3', 'programas'), (f'{DESDE} €', 'al trimestre, el más sencillo'), ('30 min', 'de videollamada inicial, gratis'))
open(f'{SAL}/tarifas.html', 'w', encoding='utf-8').write(f'''{cabeza('tarifas.html', 'Tarifas', 'Tarifas de los programas de Fuerza Basada en Evidencia.', '<meta name="robots" content="noindex">')}
{cabecera('programas.html')}
<header class="hero mini t-tarifas" id="inicio">{ANILLOS}{ilus("web-tarifas") or f'<div class="marca-agua">{LOBO}</div>'}<div class="in"><div class="txt"><span class="miga"><a href="index.html">Inicio</a> / <a href="programas.html">Programas</a> / Tarifas</span><h1>Programas y tarifas.</h1><p class="sub">Tres programas, todos con revisión semanal. Precios con el IVA incluido, vigentes {TF_VIG}.</p>{_tf_cta}</div></div></header>
<main id="contenido">{_tf_cuerpo}</main>
{cierre('¿Empezamos?', 'Cuéntame tu caso en el formulario y te digo con cuál empezaría yo.')}
{PIE}
{FIJO}
<script src="fbe.js"></script></body></html>''')
