# «El boletín, por tema» (21/11/2026, noche). Lo ejecuta interior.py después de recetas.py (usa TEMAS y _tm_bol de temas.py).
# Al final de cada herramienta (antes de la Puesta a punto), de Mitos y del Glosario: invitación al boletín con las frases
# de la página Newsletter («Un correo a la semana. Te das de baja cuando quieras.») y los tres últimos envíos sobre el tema
# de esa página (el primer tema de TEMAS que incluye la herramienta; si no, los tres últimos). Lleva a newsletter.html#alta,
# donde está el formulario: aquí no se carga nada de MailerLite.
def _bc_tema(u):
    for x in TEMAS:
        if u in x['herr']: return x
    return None
def _bc_dmy(iso): a, m, d = iso.split('-'); return f'{d}/{m}/{a}'
def _bc_bloque(x):
    L = (_tm_bol(x)[0] if x else [])[:3] or BOL[:3]
    sobre = x['corto'].lower() if x else 'entrenamiento, nutrición y salud'
    lst = ''.join(f'<li><a class="bol-cta-a" href="{b["u"]}" target="_blank" rel="noopener"><time datetime="{b["f"]}">{_bc_dmy(b["f"])}</time><b>{b["asunto"]}</b></a></li>' for b in L)
    mas = f'<a class="enl" href="tema-{x["id"]}.html">Todo sobre {sobre}</a>' if x else '<a class="enl" href="boletin.html">Todos los envíos</a>'
    return (f'<section class="bol-cta-s" aria-labelledby="bol-cta-h"><div class="in"><div class="bol-cta sube">'
            f'<div class="bol-cta-t"><p class="bol-cta-e">El boletín</p><h2 id="bol-cta-h">Lo que sí funciona, cada semana en tu correo</h2>'
            f'<p>Entrenamiento, nutrición y salud con base científica. Un correo a la semana. Te das de baja cuando quieras.</p>'
            f'<p class="bol-cta-b"><a class="btn" href="newsletter.html#alta">Apuntarme</a>{mas}</p></div>'
            f'<div class="bol-cta-l"><p class="bol-cta-h">{"Lo último que he escrito sobre " + sobre if x and _tm_bol(x)[0] else "Lo último que he enviado"}</p><ul>{lst}</ul></div>'
            f'</div></div></section>')
BC_N = 0
for _u, *_r in HERR_MAS:
    _parchea(_u, CTA_PP, _bc_bloque(_bc_tema(_u)) + CTA_PP); BC_N += 1
for _u in ('mitos.html', 'glosario.html'):
    _parchea(_u, '</main>', _bc_bloque(None) + '</main>'); BC_N += 1
