# Genera la calculadora de proteina para Netlify (carpeta netlify/), desde plantilla.html.
# Uso: cd fuente/calculadora && python3 hacer.py   (luego arrastrar netlify/ a Netlify o desplegar con su conector)
import os, re, shutil
AQUI = os.path.dirname(os.path.abspath(__file__)); FUENTE = os.path.dirname(AQUI); RAIZ = os.path.dirname(FUENTE)
SAL = os.environ.get('CALC_SAL', os.path.join(AQUI, 'netlify')); os.makedirs(SAL, exist_ok=True)
lt = open(os.path.join(FUENTE, 'ext', 'lobo-trazo.js'), encoding='utf-8').read()
CAJA = re.search(r"LOBO_CAJA = '([^']+)'", lt).group(1); LD = re.search(r"LOBO_D = '([^']+)'", lt).group(1)
h = open(os.path.join(AQUI, 'plantilla.html'), encoding='utf-8').read().replace('__LOBO_CAJA__', CAJA).replace('__LOBO_D__', LD)
open(os.path.join(SAL, 'index.html'), 'w', encoding='utf-8').write(h)
shutil.copy(os.path.join(FUENTE, 'ext', 'archivo.woff2'), os.path.join(SAL, 'archivo.woff2'))
open(os.path.join(SAL, 'favicon.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 1254"><rect width="1254" height="1254" rx="280" fill="#593EDE"/><g transform="translate(627 627) scale(.82) translate(-627 -628)"><path fill="#fff" fill-rule="evenodd" d="{LD}"/></g></svg>')
shutil.copy(os.path.join(RAIZ, 'icono-180.png'), os.path.join(SAL, 'icono-180.png'))
print('ok', SAL, len(h))
