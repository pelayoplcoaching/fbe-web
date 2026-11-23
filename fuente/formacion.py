# Trayectoria y formacion completa en Quien soy (23/11/2026).
# Sale del CV de Pelayo (CVN de enero de 2026), del diploma de Experto universitario en Nutricion clinica
# (Universidad Europea de Madrid, curso 2025-2026, expedido el 14/10/2026) y de su carnet del Colegio de Medicos de Madrid.
# Solo lo que tiene que ver con la salud o el entrenamiento. Fuera a proposito: datos personales del CV, comunicaciones a
# congresos sobre infecciosas, el voluntariado, el TFG, cursos cortos (2 h), lo que esta pendiente (Comision de Nutricion)
# el curso de RCP para atletas y los estudios en marcha (ecografia nutricional, programa de ejercicio en miopatias):
# Pelayo pidio el 23/11/2026 que no salgan. Tampoco el articulo de 2022 (trombosis y COVID-19, J Ultrasound Med): no es relevante ahora.
# Se ejecuta despues de app_pags.py (usa los iconos fonendo y birrete) y antes de datos.py (que usa FORM_LD).
import html as _html_f

TRAY = [
    ('fonendo', 'Medicina', [
        ('2016', 'Grado en Medicina', 'Universidad de Oviedo'),
        ('Colegiado', f'Médico colegiado n.º {COLEGIADO}', COLEGIO),
        ('2017-2022', 'Residencia (MIR) en Medicina Interna', 'Hospital Universitario La Paz, Madrid'),
        ('Desde 2022', 'Médico adjunto de Medicina Interna', 'Planta de hospitalización del Hospital Carlos III y consulta externa (Hospital Universitario La Paz), con guardias en urgencias y en planta'),
    ]),
    ('pesa', 'Entrenamiento de fuerza', [
        ('2022', 'Experto universitario en prescripción, metodología y bases del entrenamiento de fuerza', 'Universidad Tecnológica de México · 450 horas'),
        ('2023', 'Programación del entrenamiento de fuerza mediante estrategias emergentes', 'RTS · 300 horas'),
        ('2023', 'El músculo como órgano endocrino', 'Actualización en medicina clínica · Medical Practice Group'),
        ('15+ años', 'Entrenando fuerza', 'Desde primero de Medicina'),
    ]),
    ('plato', 'Nutrición clínica', [
        ('2023-2024', 'Máster en nutrición clínica en medicina', 'Universidad Tecnológica de México · título propio'),
        ('2025-2026', 'Experto universitario en nutrición clínica', 'Universidad Europea de Madrid · título propio'),
    ]),
    ('birrete', 'Docencia', [
        ('Actual', 'Colaborador docente de la Facultad de Medicina', 'Universidad Autónoma de Madrid'),
        ('Actual', 'Docente y referente de ecografía clínica', 'Hospital Carlos III'),
    ]),
]
# Otra formacion clinica: aparte y plegada (Pelayo, 23/11/2026: no es lo relevante para FBE ahora)
TRAY_OTROS = [('2025-2026', 'Experto universitario en el manejo integral de la ventilación mecánica no invasiva', 'Universidad Católica de Ávila'),
              ('2018-2019', 'Máster en enfermedades infecciosas y tratamiento antimicrobiano', 'Universidad CEU Cardenal Herrera')]
# Para los datos de buscadores (datos.py): titulo y quien lo expide
FORM_LD = [('Grado en Medicina', 'Universidad de Oviedo'), ('Especialista en Medicina Interna', None),
           ('Experto universitario en prescripción, metodología y bases del entrenamiento de fuerza', 'Universidad Tecnológica de México'),
           ('Máster en nutrición clínica en medicina', 'Universidad Tecnológica de México'),
           ('Experto universitario en nutrición clínica', 'Universidad Europea de Madrid'),
           ('Experto universitario en el manejo integral de la ventilación mecánica no invasiva', 'Universidad Católica de Ávila'),
           ('Máster en enfermedades infecciosas y tratamiento antimicrobiano', 'Universidad CEU Cardenal Herrera')]


def _tray_li(a, t, d):
    return f'<li><span class="tray-a">{a}</span><div><b>{t}</b><small>{d}</small></div></li>'



def _tray_g(n):  # dos columnas (Medicina y Nutricion | Fuerza y Docencia); en movil, en el orden de TRAY
    i, t, items = TRAY[n]
    return f'<article class="tray-g sube" style="order:{n}"><h3>{sec_ic(i)}{t}</h3><ol>{"".join(_tray_li(*x) for x in items)}</ol></article>'


TRAY_HTML = (f'''<section class="hoja" id="formacion"><div class="in"><div class="entrada sube"><h2>Trayectoria y formación</h2><p>La medicina, la fuerza y la nutrición que hay detrás de cada plan. Solo lo que tiene que ver con tu salud o con tu entrenamiento.</p></div>
  <div class="tray">''' + ''.join(
    '<div class="tray-c">' + ''.join(_tray_g(n) for n in col) + '</div>' for col in ((0, 2), (1, 3)))
    + f'''</div>
  <details class="tray-mas sube"><summary>Otra formación clínica <small>{len(TRAY_OTROS)}</small></summary><ol>{"".join(_tray_li(*x) for x in TRAY_OTROS)}</ol></details>
  <p class="sec-enl sube"><b>Cómo trabajo</b><a href="evidencia.html">Cómo trabajo la evidencia</a><a href="medios.html">En los medios</a></p>
</div></section>
''')

_qs = open(f'{SAL}/quien-soy.html', encoding='utf-8').read()
assert _qs.count('<section class="lema-banda">') == 1, 'quien-soy: no encuentro la banda del lema'
assert 'id="formacion"' not in _qs
_qs = _qs.replace('<section class="lema-banda">', TRAY_HTML + '<section class="lema-banda">', 1)
open(f'{SAL}/quien-soy.html', 'w', encoding='utf-8').write(_qs)
