# QR con marco futurista (24/11/2026), al estilo de la landing de Fuerza según nivel: fondo noche, rejilla,
# neón, esquinas de visor y letras Space Grotesk / Space Mono. El QR va siempre oscuro sobre claro (se lee con
# cualquier móvil). Uso: python3 futurista.py  (necesita /tmp/sp/*.ttf: ver fuente/qr/LEEME.md)
# Sale qr-<corta>-tarjeta.png (vertical, fondo transparente fuera de la tarjeta) y qr-<corta>-pantalla.png (1920 x 1080).
import io
import segno
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = {k: f'/tmp/sp/{k}.ttf' for k in ('sg700', 'sg500', 'sm400', 'sm700')}
BG, PAN, TXT, MUT = (13, 10, 20), (22, 16, 34), (239, 231, 247), (169, 157, 184)
GUIAS = {
    'nivel': dict(neon=(168, 85, 247), sec=(94, 234, 212), eti='// GUÍA GRATUITA · PDF', tit=['¿Cuánta fuerza', 'deberías tener a los', '40, 50 y 60?']),
    'dosdias': dict(neon=(255, 160, 60), sec=(168, 85, 247), eti='// GUÍA GRATUITA · PDF', tit=['Dos días de gimnasio', 'a la semana:', '¿es suficiente?']),
    'semanas': dict(neon=(184, 120, 245), sec=(216, 197, 241), eti='// GUÍA GRATUITA · PDF', tit=['Cómo empezar:', 'las primeras', '4 semanas']),
    'navidad': dict(neon=(160, 82, 232), sec=(216, 197, 241), eti='// GUÍA GRATUITA · PDF', tit=['El plan mínimo', 'para no perder', 'músculo en Navidad']),
    # tit_p: líneas de la pantalla, si no caben las de la tarjeta (allí el título va a 88 px junto al QR)
    'padres': dict(neon=(206, 168, 252), sec=(236, 226, 249), eti='// GUÍA GRATUITA · PDF', tit=['La fuerza de tus padres:', 'una prueba y', 'cuatro ejercicios'], tit_p=['La fuerza de', 'tus padres:', 'una prueba y', 'cuatro ejercicios']),
    'mesames': dict(neon=(146, 72, 228), sec=(216, 197, 241), eti='// GUÍA GRATUITA · PDF', tit=['Un año de fuerza:', 'qué cambia', 'mes a mes']),
}


def f(k, t):
    return ImageFont.truetype(F[k], t)


def rejilla(im, paso, col, a):
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    for x in range(0, im.width, paso): d.line([(x, 0), (x, im.height)], fill=col + (a,), width=1)
    for y in range(0, im.height, paso): d.line([(0, y), (im.width, y)], fill=col + (a,), width=1)
    # la rejilla se apaga hacia los bordes
    msk = Image.new('L', im.size, 0); ImageDraw.Draw(msk).ellipse([-im.width * .2, -im.height * .1, im.width * 1.2, im.height * 1.1], fill=255)
    capa.putalpha(Image.composite(capa.getchannel('A'), Image.new('L', im.size, 0), msk.filter(ImageFilter.GaussianBlur(im.width // 6))))
    im.alpha_composite(capa)


def brillo(base, caja, col, r, rad, a=170):
    capa = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle(caja, radius=rad, fill=col + (a,))
    base.alpha_composite(capa.filter(ImageFilter.GaussianBlur(r)))


def esquinas(d, caja, col, largo, grosor):
    x0, y0, x1, y1 = caja
    for (x, y, dx, dy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([(x, y), (x + dx * largo, y)], fill=col, width=grosor)
        d.line([(x, y), (x, y + dy * largo)], fill=col, width=grosor)


def panel_qr(url, lado):
    q = segno.make(url, error='q')
    n = q.symbol_size(border=4)[0]
    b = io.BytesIO(); q.save(b, kind='png', scale=max(1, lado // n), border=4, dark='#0D0A14', light='#F6F2FF'); b.seek(0)
    im = Image.open(b).convert('RGBA')
    return im.resize((lado, lado), Image.NEAREST)


def texto_centrado(d, y, t, ft, col, W, x0=0):
    w = d.textlength(t, font=ft); d.text((x0 + (W - w) / 2, y), t, font=ft, fill=col)


def url_partida(d, x, y, corta, ft, neon, centro=None):
    a, b = 'fuerzabasadaenevidencia.com', '/' + corta
    wa, wb = d.textlength(a, font=ft), d.textlength(b, font=ft)
    if centro is not None: x = centro - (wa + wb) / 2
    d.text((x, y), a, font=ft, fill=TXT); d.text((x + wa, y), b, font=ft, fill=neon)
    return wa + wb


def tarjeta(corta, g):
    W, H, M = 1200, 1545, 70
    lienzo = Image.new('RGBA', (W + 2 * M, H + 2 * M), (0, 0, 0, 0))
    brillo(lienzo, [M, M, M + W, M + H], g['neon'], 34, 64, 120)  # halo de neon alrededor de la tarjeta
    t = Image.new('RGBA', (W, H), BG + (255,))
    rejilla(t, 40, g['neon'], 34)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([W * .1, H * .32, W * .9, H * .86], fill=g['neon'] + (70,))
    t.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(t)
    d.text((80, 78), g['eti'], font=f('sm700', 34), fill=g['sec'])
    ImageDraw.Draw(t).line([(80, 132), (W - 80, 132)], fill=tuple(int(c * .55 + b * .45) for c, b in zip(g['neon'], BG)), width=2)
    y = 162
    for ln in g['tit']:
        d.text((80, y), ln, font=f('sg700', 74), fill=TXT); y += 84
    lado = 700; px, py = (W - lado) // 2, y + 100
    brillo(t, [px - 10, py - 10, px + lado + 10, py + lado + 10], g['neon'], 30, 36, 200)
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([px - 22, py - 22, px + lado + 22, py + lado + 22], radius=34, fill=(246, 242, 255, 255))
    t.alpha_composite(panel_qr(f'https://fuerzabasadaenevidencia.com/{corta}', lado), (px, py))
    d = ImageDraw.Draw(t)
    esquinas(d, [px - 52, py - 52, px + lado + 52, py + lado + 52], g['neon'] + (255,), 64, 7)
    yb = py + lado + 92
    texto_centrado(d, yb, '[ ESCANEA CON LA CÁMARA ]', f('sm400', 30), MUT, W)
    url_partida(d, 0, yb + 58, corta, f('sm700', 46), g['neon'] + (255,), centro=W / 2)
    # borde fino de neon y marca de esquina
    msk = Image.new('L', (W, H), 0); ImageDraw.Draw(msk).rounded_rectangle([0, 0, W - 1, H - 1], radius=56, fill=255)
    lienzo.paste(t, (M, M), msk)
    ImageDraw.Draw(lienzo).rounded_rectangle([M, M, M + W - 1, M + H - 1], radius=56, outline=g['neon'] + (170,), width=3)
    lienzo.save(f'qr-{corta}-tarjeta.png')
    return lienzo


def pantalla(corta, g):
    W, H = 1920, 1080
    t = Image.new('RGBA', (W, H), BG + (255,))
    rejilla(t, 48, g['neon'], 30)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([980, 120, 1820, 960], fill=g['neon'] + (80,))
    t.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(t)
    x = 140
    lineas = g.get('tit_p', g['tit'])
    dy = 0 if len(lineas) <= 3 else -50 * (len(lineas) - 3)  # con más líneas, todo el bloque sube para seguir centrado
    d.text((x, 250 + dy), g['eti'], font=f('sm700', 36), fill=g['sec'])
    d.line([(x, 312 + dy), (x + 640, 312 + dy)], fill=tuple(int(c * .6 + b * .4) for c, b in zip(g['neon'], BG)), width=2)
    y = 350 + dy
    for ln in lineas:
        d.text((x, y), ln, font=f('sg700', 88), fill=TXT); y += 100
    d.text((x, y + 50), '[ ESCANEA CON LA CÁMARA ]', font=f('sm400', 32), fill=MUT)
    url_partida(d, x, y + 104, corta, f('sm700', 40), g['neon'] + (255,))
    lado = 620; px, py = 1150, (H - lado) // 2
    brillo(t, [px - 10, py - 10, px + lado + 10, py + lado + 10], g['neon'], 34, 36, 210)
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([px - 22, py - 22, px + lado + 22, py + lado + 22], radius=34, fill=(246, 242, 255, 255))
    t.alpha_composite(panel_qr(f'https://fuerzabasadaenevidencia.com/{corta}', lado), (px, py))
    d = ImageDraw.Draw(t)
    esquinas(d, [px - 52, py - 52, px + lado + 52, py + lado + 52], g['neon'] + (255,), 60, 7)
    t.convert('RGB').save(f'qr-{corta}-pantalla.png')
    return t


for c, g in GUIAS.items():
    tarjeta(c, g); pantalla(c, g); print(c, 'hecho')
