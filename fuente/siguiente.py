# «¿Y ahora qué?» (21/11/2026, noche): bajo cada calculadora, el siguiente paso según cómo salga el resultado.
# Lo ejecuta interior.py después de temas.py (antes de chequeo.py, que usa SIGUE). Solo enlaza a páginas que ya existen (guías, perfiles de Empieza aquí,
# otras herramientas, mitos, glosario, Puesta a punto, Programas, Pauta Activa); no añade datos nuevos.
# Zonas: z-alto (verde), z-medio (ámbar), z-bajo (rojo); 'def' es lo que sale si la herramienta no tiene zonas o aún no la hay.
_SG_EA = 'empieza-aqui.html#'
_SG_P = {
    'pp': ('Con Pelayo', 'Un plan revisado por un médico: Puesta a punto', 'puesta-a-punto.html'),
    'prog': ('Con Pelayo', 'Un programa que se ajusta cada semana', 'programas.html'),
    'mr': ('Mis resultados', 'Guárdalo y repítelo dentro de unas semanas', 'mis-resultados.html'),
    'pa': ('Pauta Activa', 'Qué vigilar al entrenar con tu medicación', 'pauta-activa.html'),
}
SIGUE = {
    'test-silla.html': {
        'z-bajo': [('Empieza aquí', 'Ruta para mayores de 60 (o para tus padres)', _SG_EA + 'mayores'), ('Herramienta', 'Mide también equilibrio y marcha: test SPPB', 'test-sppb.html'), _SG_P['pp']],
        'z-medio': [('Herramienta', 'Complétalo con el test SPPB', 'test-sppb.html'), ('Empieza aquí', 'Empieza con fuerza dos días por semana', _SG_EA + 'cero'), _SG_P['mr']],
        'z-alto': [('Herramienta', 'Mide tu fuerza de prensión', 'prension.html'), ('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html'), _SG_P['mr']]},
    'calculadora-1rm.html': {
        'def': [('Herramienta', 'Cuenta tus series de la semana', 'volumen-semanal.html'), ('Mito', '¿Hay que llegar al fallo para crecer?', 'mitos.html#fallo'), _SG_P['prog']]},
    'volumen-semanal.html': {
        'def': [('Glosario', 'Qué cuenta como volumen de entrenamiento', 'glosario.html#volumen'), ('Mito', '¿Cada músculo dos o tres veces por semana?', 'mitos.html#frecuencia'), ('Herramienta', 'Calcula tus cargas con el 1RM', 'calculadora-1rm.html')]},
    'cafeina.html': {
        'z-alto': [('Herramienta', 'Suplementos con evidencia', 'suplementos.html'), ('Glosario', 'Cafeína: cuánto y hasta cuándo', 'glosario.html#cafeina'), _SG_P['mr']],
        'z-medio': [('Glosario', 'Cafeína: cuánto y hasta cuándo', 'glosario.html#cafeina'), ('Guías', 'Sueño, estrés y rendimiento', 'guias.html'), _SG_P['pa']],
        'z-bajo': [('Guías', 'Sueño, estrés y rendimiento', 'guias.html'), _SG_P['pa'], ('Glosario', 'Cafeína: cuánto y hasta cuándo', 'glosario.html#cafeina')]},
    'revision-medica.html': {
        'z-alto': [('Empieza aquí', 'Tu ruta si nunca has entrenado fuerza', _SG_EA + 'cero'), ('Herramienta', 'Tus zonas de pulso', 'zonas-pulso.html'), ('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html')],
        'z-medio': [_SG_P['pa'], ('Empieza aquí', 'Ruta si tomas medicación o tienes una enfermedad crónica', _SG_EA + 'medicacion'), _SG_P['pp']],
        'z-bajo': [_SG_P['pa'], ('Empieza aquí', 'Ruta si tomas medicación o tienes una enfermedad crónica', _SG_EA + 'medicacion'), _SG_P['pp']]},
    'zonas-pulso.html': {
        'z-alto': [('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html'), ('Glosario', 'Escala de Borg', 'glosario.html#borg'), _SG_P['mr']],
        'z-medio': [_SG_P['pa'], ('Glosario', 'Escala de Borg: guiarte sin pulsómetro', 'glosario.html#borg'), ('Empieza aquí', 'Ruta si tomas medicación', _SG_EA + 'medicacion')],
        'z-bajo': [_SG_P['pa'], ('Glosario', 'Escala de Borg: guiarte sin pulsómetro', 'glosario.html#borg'), ('Empieza aquí', 'Ruta si tomas medicación', _SG_EA + 'medicacion')]},
    'semaforo-dolor.html': {
        'z-alto': [('Herramienta', 'Sigue progresando: calcula tus cargas', 'calculadora-1rm.html'), ('Mito', '¿Con artrosis de rodilla mejor no cargar?', 'mitos.html#artrosis'), _SG_P['mr']],
        'z-medio': [('Empieza aquí', 'Ruta si te duele algo al entrenar', _SG_EA + 'dolor'), ('Mito', '¿Con artrosis de rodilla mejor no cargar?', 'mitos.html#artrosis'), _SG_P['prog']],
        'z-bajo': [('Empieza aquí', 'Ruta si te duele algo al entrenar', _SG_EA + 'dolor'), _SG_P['pp'], ('Herramienta', '¿Necesito revisión médica?', 'revision-medica.html')]},
    'test-sppb.html': {
        'z-alto': [('Herramienta', 'Test de la silla en 30 segundos', 'test-silla.html'), ('Herramienta', 'Fuerza de prensión', 'prension.html'), _SG_P['mr']],
        'z-medio': [('Empieza aquí', 'Ruta para mayores de 60', _SG_EA + 'mayores'), ('Mito', '¿A partir de los 60 ya no se gana músculo?', 'mitos.html#sesenta'), _SG_P['mr']],
        'z-bajo': [('Empieza aquí', 'Ruta para mayores de 60', _SG_EA + 'mayores'), ('Herramienta', '¿Necesita revisión médica antes de empezar?', 'revision-medica.html'), _SG_P['pp']]},
    'paron.html': {
        'z-alto': [('Empieza aquí', 'Vuelvo después de un parón', _SG_EA + 'paron'), ('Mito', '¿Cuántas veces por semana hay que entrenar?', 'mitos.html#frecuencia'), _SG_P['mr']],
        'z-medio': [('Empieza aquí', 'Vuelvo después de un parón', _SG_EA + 'paron'), ('Glosario', 'Dosis mínima de mantenimiento', 'glosario.html'), _SG_P['prog']],
        'z-bajo': [('Empieza aquí', 'Vuelvo después de un parón', _SG_EA + 'paron'), ('Glosario', 'Dosis mínima de mantenimiento', 'glosario.html'), _SG_P['prog']]},
    'suplementos.html': {
        'z-alto': [('Mito', '¿La creatina es un esteroide y daña el riñón?', 'mitos.html#creatina'), ('Herramienta', 'Calcula tu proteína', CALC), ('Herramienta', 'Cafeína y sueño', 'cafeina.html')],
        'z-medio': [_SG_P['pa'], ('Herramienta', 'Cafeína y sueño', 'cafeina.html'), ('Mito', '¿La creatina es un esteroide y daña el riñón?', 'mitos.html#creatina')],
        'z-bajo': [_SG_P['pa'], ('Mito', '¿La creatina es un esteroide y daña el riñón?', 'mitos.html#creatina'), ('Herramienta', 'Calcula tu proteína', CALC)]},
    'actividad-oms.html': {
        'z-alto': [('Herramienta', 'Cuenta tus series de fuerza', 'volumen-semanal.html'), ('Herramienta', 'Tus zonas de pulso', 'zonas-pulso.html'), _SG_P['mr']],
        'z-medio': [('Empieza aquí', 'Tu ruta si nunca has entrenado fuerza', _SG_EA + 'cero'), ('Herramienta', 'Tus zonas de pulso', 'zonas-pulso.html'), _SG_P['prog']],
        'z-bajo': [('Empieza aquí', 'Tu ruta si nunca has entrenado fuerza', _SG_EA + 'cero'), ('Herramienta', '¿Necesito revisión médica?', 'revision-medica.html'), _SG_P['prog']]},
    'cintura-altura.html': {
        'z-alto': [('Herramienta', 'Calorías de mantenimiento', 'calorias.html'), ('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html'), _SG_P['mr']],
        'z-medio': [('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html'), ('Mito', '¿El cardio en ayunas quema más grasa?', 'mitos.html#ayunas'), _SG_P['prog']],
        'z-bajo': [('Herramienta', '¿Llegas a lo mínimo de la OMS?', 'actividad-oms.html'), ('Herramienta', '¿Necesito revisión médica?', 'revision-medica.html'), _SG_P['pp']]},
    'prension.html': {
        'z-alto': [('Herramienta', 'Test de la silla en 30 segundos', 'test-silla.html'), ('Herramienta', 'Test SPPB', 'test-sppb.html'), _SG_P['mr']],
        'z-medio': [('Glosario', 'Qué es la sarcopenia', 'glosario.html#sarcopenia'), ('Empieza aquí', 'Ruta para mayores de 60', _SG_EA + 'mayores'), _SG_P['pp']],
        'z-bajo': [('Glosario', 'Qué es la sarcopenia', 'glosario.html#sarcopenia'), ('Empieza aquí', 'Ruta para mayores de 60', _SG_EA + 'mayores'), _SG_P['pp']]},
    'calorias.html': {
        'def': [('Herramienta', 'Calcula tu proteína', CALC), ('Herramienta', 'Cintura y altura', 'cintura-altura.html'), _SG_P['prog']]},
}
_YA_TIT = {'z-alto': 'Vas bien. Para seguir:', 'z-medio': 'Para mejorarlo:', 'z-bajo': 'Por dónde empezaría yo:', 'def': 'Para seguir:'}
_YA_JS = r"""(function(){var s=document.getElementById('ya'),res=document.querySelector('.tool-res');if(!s||!res)return;
var cp=res.querySelector('.copiar-t:not(.guardar)'),rs=[].slice.call(s.querySelectorAll('.ya-rej'));
function pinta(){var z=['z-alto','z-medio','z-bajo'].filter(function(c){return res.classList.contains(c)})[0]||'def',hay=z!=='def'||(cp?!cp.hidden:true);
var r=rs.filter(function(x){return x.dataset.z===z})[0]||rs.filter(function(x){return x.dataset.z==='def'})[0]||null;
s.hidden=!(hay&&r);rs.forEach(function(x){x.hidden=x!==r});s.dataset.z=z}
var mo=new MutationObserver(pinta);mo.observe(res,{attributes:true,attributeFilter:['class']});if(cp)mo.observe(cp,{attributes:true,attributeFilter:['hidden']});pinta();})();"""
def _ya_tarj(e, t, u):
    ext = u.startswith('http')
    return f'<a class="ya-t" href="{u}"{" rel=\"noopener\"" if ext else ""}><small>{e}</small><b>{t}</b></a>'
def _ya_html(arch):
    zs = SIGUE[arch]
    rej = ''.join(f'<div class="ya-rej" data-z="{z}" hidden><p class="ya-st">{_YA_TIT[z]}</p><div class="ya-ts">' + ''.join(_ya_tarj(*x) for x in L) + '</div></div>' for z, L in zs.items())
    return (f'<section class="ya-s" id="ya" hidden aria-labelledby="ya-h"><div class="in"><div class="ya-caja">'
            f'<h2 class="ya-h" id="ya-h">¿Y ahora qué?</h2>{rej}</div></div></section><script>{_YA_JS}</script>\n')
for _arch in SIGUE:
    _t = open(f'{SAL}/{_arch}', encoding='utf-8').read()
    _i = _t.find('<section class="tool-s">'); _j = _t.find('</section>', _i)
    assert _i > 0 and _j > 0, _arch
    if 'id="ya"' not in _t:
        _t = _t[:_j + len('</section>')] + '\n' + _ya_html(_arch) + _t[_j + len('</section>'):]
        open(f'{SAL}/{_arch}', 'w', encoding='utf-8').write(_t)
