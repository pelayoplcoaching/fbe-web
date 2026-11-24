import sys, asyncio, os, mimetypes
from playwright.async_api import async_playwright
# uso: python3 captura.py pagina.html salida.png ancho [full|vista] [js]
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
async def main():
    src, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
    full = len(sys.argv) < 5 or sys.argv[4] == 'full'
    js = sys.argv[5] if len(sys.argv) > 5 else ''
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=1)
        async def ruta(route):
            u = route.request.url.split('?')[0]
            rel = u.replace('https://fuerzabasadaenevidencia.com/', '')
            f = os.path.join(RAIZ, rel)
            if os.path.isfile(f):
                await route.fulfill(path=f, headers={'Access-Control-Allow-Origin': '*', 'Content-Type': mimetypes.guess_type(f)[0] or 'application/octet-stream'})
            else:
                await route.fulfill(status=404, body='')
        await pg.route('https://fuerzabasadaenevidencia.com/**', ruta)
        await pg.goto('file://' + os.path.abspath(src), wait_until='load')
        await pg.add_style_tag(content='*{animation:none!important;transition:none!important} .fbe-sube{opacity:1!important;transform:none!important}')
        if js:
            await pg.evaluate(js)
            await pg.wait_for_timeout(1200)
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
asyncio.run(main())
