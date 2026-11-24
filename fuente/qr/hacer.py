# QR de las direcciones cortas (24/11/2026): python3 hacer.py -> qr-<corta>.svg, qr-<corta>.png y qr-<corta>-tarjeta.png
import segno, io, os
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
NOCHE, MARCA = '#140B3A', '#593EDE'
CORTAS = {'nivel': 'Guía gratuita · ¿Cuánta fuerza deberías tener?', 'dosdias': 'Guía gratuita · Dos días de gimnasio', 'semanas': 'Guía gratuita · Cómo empezar: las primeras 4 semanas'}
if not os.path.exists('/tmp/archivo.ttf'):
    f = TTFont('../ext/archivo.woff2'); f.flavor = None; f.save('/tmp/archivo.ttf')
def letra(tam, peso):
    ft = ImageFont.truetype('/tmp/archivo.ttf', tam)
    try: ft.set_variation_by_axes([peso if 'eight' in str(x.get('name', '')) else 100 for x in ft.get_variation_axes()])  # peso y anchura normal
    except Exception: pass
    return ft
for c, rotulo in CORTAS.items():
    url = f'https://fuerzabasadaenevidencia.com/{c}'
    q = segno.make(url, error='q')
    q.save(f'qr-{c}.svg', scale=10, border=4, dark=NOCHE, light='#FFFFFF')
    q.save(f'qr-{c}.png', scale=40, border=4, dark=NOCHE, light='#FFFFFF')
    # Tarjeta para el vídeo: QR, dirección y rótulo, sobre blanco con esquinas redondeadas y fondo transparente
    b = io.BytesIO(); q.save(b, kind='png', scale=28, border=2, dark=NOCHE, light='#FFFFFF'); b.seek(0)
    im = Image.open(b).convert('RGBA'); W = im.width + 160; H = im.height + 330
    t = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=64, fill='#FFFFFF')
    f1 = letra(54, 700); tw = d.textlength(rotulo, font=f1)
    if tw > W - 120: f1 = letra(int(54 * (W - 120) / tw), 700); tw = d.textlength(rotulo, font=f1)
    d.text(((W - tw) / 2, 58), rotulo, font=f1, fill=MARCA)
    t.paste(im, (80, 150))
    dire = f'fuerzabasadaenevidencia.com/{c}'; f2 = letra(60, 800); tw = d.textlength(dire, font=f2)
    if tw > W - 100: f2 = letra(int(60 * (W - 100) / tw), 800); tw = d.textlength(dire, font=f2)
    d.text(((W - tw) / 2, 150 + im.height + 50), dire, font=f2, fill=NOCHE)
    t.save(f'qr-{c}-tarjeta.png')
    print(c, url, q.version, q.error, t.size)
