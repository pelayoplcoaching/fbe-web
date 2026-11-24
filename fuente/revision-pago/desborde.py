import sys, asyncio, os, mimetypes
from playwright.async_api import async_playwright
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
async def main():
    src, w = sys.argv[1], int(sys.argv[2])
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': w, 'height': 900})
        async def ruta(route):
            rel = route.request.url.split('?')[0].replace('https://fuerzabasadaenevidencia.com/', '')
            f = os.path.join(RAIZ, rel)
            if os.path.isfile(f): await route.fulfill(path=f, headers={'Access-Control-Allow-Origin': '*', 'Content-Type': mimetypes.guess_type(f)[0] or 'application/octet-stream'})
            else: await route.fulfill(status=404, body='')
        await pg.route('https://fuerzabasadaenevidencia.com/**', ruta)
        await pg.goto('file://' + os.path.abspath(src), wait_until='load')
        r = await pg.evaluate('''(w) => { const out = []; document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.right > w + 1 && r.width > 0) { const p = e.parentElement; const pr = p ? p.getBoundingClientRect().right : 0; if (pr <= w + 1 || out.length < 3) out.push(e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '') + ' right=' + Math.round(r.right) + ' w=' + Math.round(r.width) + ' txt=' + (e.textContent||'').trim().slice(0,30)); } }); return [document.documentElement.scrollWidth, out.slice(0, 15)]; }''', w)
        print(r[0]); print('\n'.join(r[1]))
        await b.close()
asyncio.run(main())
