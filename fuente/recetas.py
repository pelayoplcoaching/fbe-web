# «Recetas con proteína» (21/11/2026, noche). Lo ejecuta interior.py después de compartir.py.
# recetas.html: las diez recetas de muestra del recetario de la app FBE Equipo (ext/recetas.json, las mismas de la portada),
# con lo que trae cada ficha: capítulo, descripción, etiquetas, calorías, proteína, minutos, dificultad, si aguanta en táper
# y el truco. Los ingredientes y los pasos no se publican (solo están las medidas caseras, sin el ingrediente, y el
# recetario completo es de la app). Lo único calculado aquí es la proteína por cada 100 kcal.
# Filtros (vegetariana, vegana, sin gluten, sin lactosa, rápida, microondas, para táper), orden y «Tu día» (suma de
# proteína y calorías con tu objetivo; se recuerda en localStorage fbe-recetas). Capturas reales de la app (w3/).
import shutil as _sh
REC = json.load(open('ext/recetas.json', encoding='utf-8'))
_REC_F = [('', 'Todas'), ('vegetariana', 'Vegetariana'), ('vegana', 'Vegana'), ('sin-gluten', 'Sin gluten'), ('sin-lactosa', 'Sin lactosa'),
          ('rapida', 'Rápidas'), ('microondas', 'Microondas'), ('taper', 'Para táper')]
def _rec_k(t): return _norm(t).replace(' ', '-')
def _rec_taper(b):
    m = re.match(r'S[ií]\s*\((.*)\)', b or '')
    return m.group(1) if m else ('' if (b or 'No').startswith('No') else b)
def _rec_tarj(r):
    L = r['libro']; tp = _rec_taper(L.get('batch')); ks = [_rec_k(e) for e in r['etiquetas']] + (['taper'] if tp else [])
    pk = r['proteina_g'] / r['kcal'] * 100
    et = ''.join(f'<li>{e}</li>' for e in r['etiquetas'])
    x = f'<span>{fmt_es(pk, 1)} g de proteína por 100 kcal</span><span>{L["dificultad"]}</span>' + (f'<span>Para táper: {tp}</span>' if tp else '')
    return (f'<article class="rec sube" id="r-{L["codigo"].replace(".", "-")}" data-c="{L["codigo"]}" data-t="{" ".join(ks)}" data-p="{r["proteina_g"]}" data-k="{r["kcal"]}" data-m="{r["minutos"]}">'
            f'<p class="rec-cap">{L["capitulo"]} · {L["bloque"]}</p><h3>{r["nombre"]}</h3><p class="rec-d">{L["descripcion"]}</p><ul class="rec-et">{et}</ul>'
            f'<div class="mc"><div><b>{r["kcal"]}</b><span>kcal</span></div><div><b>{round(r["proteina_g"])} g</b><span>proteína</span></div><div><b>{r["minutos"]}</b><span>min</span></div></div>'
            f'<p class="rec-x">{x}</p>' + (f'<p class="rec-tr"><b>Truco</b>{L["nota"]}</p>' if L.get('nota') else '') +
            f'<button type="button" class="rec-b" aria-pressed="false">Añadir a mi día</button></article>')
def fmt_es(x, d=0): return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
for _n in ('recetario', 'receta'):
    _sh.copy(f'w3/{_n}.webp', f'{SAL}/img/app-{_n}.webp')
REC_JS = r"""(function(){var D=document,R=D.getElementById('rec-rej');if(!R)return;var K='fbe-recetas',st={sel:[],meta:140};try{var o=JSON.parse(localStorage.getItem(K)||'{}');if(o&&Array.isArray(o.sel))st.sel=o.sel;if(o&&o.meta>0)st.meta=o.meta}catch(e){}
function guarda(){try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
var cards=[].slice.call(R.querySelectorAll('.rec')),F=[].slice.call(D.querySelectorAll('#rec-f button')),O=D.getElementById('rec-o'),N=D.getElementById('rec-n'),V=D.getElementById('rec-vacio');
function nf(x){return Math.round(x).toLocaleString('es-ES')}
function filtra(){var act=F.filter(function(b){return b.dataset.f&&b.getAttribute('aria-pressed')==='true'}).map(function(b){return b.dataset.f}),n=0;
  cards.forEach(function(c){var ts=c.dataset.t.split(' '),ok=act.every(function(f){return ts.indexOf(f)>=0});c.hidden=!ok;if(ok)n++});
  F[0].setAttribute('aria-pressed',act.length?'false':'true');N.textContent=(n===1?'1 receta':n+' recetas')+(act.length?' con esos filtros':'');V.hidden=n>0}
function ordena(){var f={p:function(c){return -c.dataset.p},pk:function(c){return -(c.dataset.p/c.dataset.k)},k:function(c){return +c.dataset.k},t:function(c){return +c.dataset.m}}[O.value]||function(){return 0};cards.sort(function(a,b){return f(a)-f(b)});cards.forEach(function(c){R.appendChild(c)})}
F.forEach(function(b){b.addEventListener('click',function(){if(!b.dataset.f)F.forEach(function(x){x.setAttribute('aria-pressed','false')});else b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');filtra()})});
O.addEventListener('change',ordena);
var M=D.getElementById('rec-meta'),A=D.querySelector('.rec-anillo .a'),P=D.getElementById('rec-p'),S=D.getElementById('rec-sum'),L=D.getElementById('rec-lista'),VA=D.getElementById('rec-vaciar'),MT=D.getElementById('rec-meta-t');
function suma(){var p=0,k=0,li='';cards.forEach(function(c){var en=st.sel.indexOf(c.dataset.c)>=0,b=c.querySelector('.rec-b');c.classList.toggle('en',en);b.setAttribute('aria-pressed',en?'true':'false');b.textContent=en?'En tu día':'Añadir a mi día';if(en){p+=+c.dataset.p;k+=+c.dataset.k;li+='<li><a href="#'+c.id+'">'+c.querySelector('h3').textContent+'</a><b>'+nf(c.dataset.p)+' g</b></li>'}});
  var m=Math.max(20,Math.min(400,+st.meta||140));MT.textContent=nf(m);P.textContent=nf(p)+' g';if(A)A.style.strokeDashoffset=(213.6*(1-Math.min(1,p/m))).toFixed(1);
  S.textContent=!st.sel.length?'Añade recetas a tu día y mira cómo se llena.':(p>=m?'Proteína del día, cumplida · '+nf(k)+' kcal':nf(k)+' kcal · te faltan '+nf(m-p)+' g');L.innerHTML=li;VA.hidden=!st.sel.length}
cards.forEach(function(c){c.querySelector('.rec-b').addEventListener('click',function(){var i=st.sel.indexOf(c.dataset.c);if(i>=0)st.sel.splice(i,1);else st.sel.push(c.dataset.c);guarda();suma()})});
M.value=st.meta;M.addEventListener('input',function(){var v=parseFloat(String(M.value).replace(',','.'));if(v>0){st.meta=v;guarda();suma()}});
VA.addEventListener('click',function(){st.sel=[];guarda();suma();VA.blur()});
ordena();filtra();suma()})();"""
_rec_cuerpo = f'''
<section class="rec-s"><div class="in">
  <div class="rec-barra sube"><div class="rec-f fases claras" id="rec-f" role="group" aria-label="Filtrar las recetas">{''.join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if not k else "false"}">{t}</button>' for k, t in _REC_F)}</div>
    <label class="rec-o"><span>Ordenar</span><select id="rec-o"><option value="p">Más proteína</option><option value="pk">Más proteína por caloría</option><option value="k">Menos calorías</option><option value="t">Menos tiempo</option></select></label></div>
  <div class="rec-lay">
    <div><h2 class="oculto">Las recetas</h2><p class="rec-n" id="rec-n" role="status">{len(REC)} recetas</p>
      <div class="rec-rej" id="rec-rej">{''.join(_rec_tarj(r) for r in REC)}</div>
      <p class="rec-vacio" id="rec-vacio" hidden>Ninguna de estas diez cumple todo eso a la vez. Quita algún filtro: en la app hay más de 500.</p></div>
    <aside class="rec-dia" aria-labelledby="rec-dia-h"><h2 id="rec-dia-h">Tu día</h2>
      <div class="rec-anillo"><svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="34" class="f"/><circle cx="40" cy="40" r="34" class="a"/></svg><div><b id="rec-p">0 g</b><small>de <span id="rec-meta-t">140</span> g de proteína</small></div></div>
      <p class="rec-sum" id="rec-sum" role="status"></p>
      <ul class="rec-lista" id="rec-lista"></ul><button type="button" class="enl-b" id="rec-vaciar" hidden>Vaciar el día</button>
      <label class="rec-meta"><span>Tu objetivo de proteína</span><span class="rec-meta-c"><input id="rec-meta" type="number" inputmode="numeric" min="20" max="400" step="5" value="140"><i>g al día</i></span></label>
      <p class="rec-nota">140 g es un ejemplo. El tuyo sale de tu plan o de la <a href="{CALC}" rel="noopener">calculadora de proteína</a>.</p></aside>
  </div>
</div></section>
<section class="hoja rec-app" aria-labelledby="rec-app-h"><div class="in">
  <div class="rec-app-g">
    <div class="entrada sube" style="margin:0"><h2 id="rec-app-h">El recetario completo está en la app</h2><p>Estas diez son una muestra. Con los programas tienes la app FBE Equipo y, dentro, el recetario entero.</p>
      <ul class="rec-app-l"><li>Más de 500 recetas con macros y medidas caseras, también veganas, sin gluten y sin lactosa</li><li>Lista de la compra hecha a partir de tu menú</li><li>¿Comes fuera? La app te dice cómo cuadrarlo</li><li>¿No te apetece apuntar? Haz una foto al plato y cuenta como hecha</li></ul>
      <p class="rec-app-b"><a class="btn" href="programas.html">Ver los programas</a><a class="btn hueco" href="index.html#semana">Mira la app por dentro</a></p></div>
    <div class="rec-pant sube"><figure><img src="img/app-recetario.webp" alt="El recetario de la app FBE Equipo, con las recetas por capítulos" width="702" height="1519" loading="lazy" decoding="async"></figure><figure><img src="img/app-receta.webp" alt="La ficha de una receta en la app, con macros, ingredientes y pasos" width="702" height="1519" loading="lazy" decoding="async"></figure></div>
  </div>
  <p class="sec-enl sube"><b>Relacionado</b><a href="{CALC}" rel="noopener">Calculadora de proteína</a><a href="calorias.html">Calorías de mantenimiento</a><a href="mitos.html#proteina-rinon">¿La proteína daña el riñón?</a><a href="glosario.html#proteina">Proteína, en el glosario</a><a href="tema-nutricion.html">Nutrición y suplementos</a></p>
</div></section>
<script>{REC_JS}</script>'''
SEC_SIG['recetas.html'] = (('tema-nutricion.html', 'Nutrición y suplementos'), ('programas.html', 'Programas'))
pagina('recetas.html', 'Recetas con proteína',
       'Diez recetas del recetario de la app FBE Equipo con sus calorías, su proteína y el tiempo que llevan, con filtros por dieta y una suma de tu día.',
       'Recetas con proteína',
       'Diez recetas del recetario de la app FBE Equipo, con sus calorías, su proteína y el tiempo que llevan. Filtra por lo que comes y suma las que te comerías hoy.',
       _rec_cuerpo)
SEC_PAGS.append('recetas.html')
# Enlaces: portada (bajo el carrusel), tema de nutrición, menú Aprende y móvil (APRENDE en sitio-cab.py) y buscador
_parchea('index.html', '<p style="color:var(--tinta-2);font-size:.9rem">El objetivo de 140 g es un ejemplo; el tuyo sale de tu plan.</p>',
         '<p style="color:var(--tinta-2);font-size:.9rem">El objetivo de 140 g es un ejemplo; el tuyo sale de tu plan. <a href="recetas.html">Las diez, con filtros</a></p>')
_top = sorted(REC, key=lambda r: -r['proteina_g'] / r['kcal'])[:3]
_parchea('tema-nutricion.html', '<section class="tm-vid" id="videos-tema">',
         '<section class="tm-rec" id="recetas-tema"><div class="in"><div class="entrada sube"><h2>Recetas con proteína</h2><p>Tres del recetario de la app, de las que más proteína dan por caloría.</p></div>'
         '<ul class="tm-rec-l sube">' + ''.join(f'<li><a href="recetas.html#r-{r["libro"]["codigo"].replace(".", "-")}"><b>{r["nombre"]}</b><small>{round(r["proteina_g"])} g de proteína · {r["kcal"]} kcal · {r["minutos"]} min</small></a></li>' for r in _top) +
         '</ul><p class="sec-enl sube"><b>Hay diez</b><a href="recetas.html">Ver todas, con filtros</a></p></div></section>\n<section class="tm-vid" id="videos-tema">')
_ix = json.load(open(f'{SAL}/buscar.json', encoding='utf-8'))
_ix.append({'t': 'Recetas con proteína', 'u': 'recetas.html', 'd': 'Diez recetas del recetario de la app, con calorías, proteína y tiempo, y filtros por dieta.', 'k': 'recetas comida proteina desayuno cena vegana vegetariana sin gluten taper microondas', 'y': 'Página'})
for r in REC:
    _ix.append({'t': r['nombre'], 'u': f'recetas.html#r-{r["libro"]["codigo"].replace(".", "-")}', 'd': f'{round(r["proteina_g"])} g de proteína · {r["kcal"]} kcal · {r["minutos"]} min. {r["libro"]["descripcion"]}', 'k': 'receta ' + r['libro']['capitulo'] + ' ' + ' '.join(r['etiquetas']), 'y': 'Receta'})
open(f'{SAL}/buscar.json', 'w', encoding='utf-8').write(json.dumps(_ix, ensure_ascii=False, separators=(',', ':')))
