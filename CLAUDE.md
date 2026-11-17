# Web de Fuerza Basada en Evidencia (fbe-web)

Sitio estático de Pelayo Fernández Cidón (médico internista y entrenador). Se publica con GitHub Pages desde `main`, carpeta raíz. Dirección de prueba: https://pelayoplcoaching.github.io/fbe-web/ . Dominio final previsto: fuerzabasadaenevidencia.com (en IONOS, todavía sin apuntar).

## Cómo se genera
Los `.html`, `fbe.css`, `fbe.js` e `img/` de la raíz son SALIDA. No se editan a mano: se regeneran desde `fuente/`.

```
cd fuente
cat sitio-cab.py interior.py > sitio.py && python3 sitio.py   # escribe en .. (o en $FBE_SAL)
node og.mjs                                                    # og.png e icono-180.png (necesita Playwright)
node ver3.mjs                                                  # pruebas en 1280 y 390 px
rm sitio.py web-fbe-equipo.html sitio-inicio.html
```

- `sitio-cab.py`: portada. Encadena `landing5.py` -> `landing4.py` -> `landing3.py` -> `landing2.py` (cada uno parchea al anterior) con `estilo3/4/5.css` y `guion3/4/5.js`. Capturas de la app en `w3/`.
- `interior.py`: Quién soy, Programas, Puesta a punto, Guías, Newsletter, Dudas, 404, favicon, sitemap, robots.
- `sitio.css` y `mini.js`: estilos y guion comunes de las interiores (se añaden por tandas al final).
- `ext/`: el trazo del lobo (copiado de la app) y 10 recetas de muestra.
- `web-img/`: ilustraciones opcionales. Si existe `web-<pagina>.webp` sustituye al lobo de la cabecera; si existe `guia-<nombre>.webp` sustituye al dibujo de la portada (nombres en `GIMG` de interior.py).
- Otras ilustraciones de `web-img/`: `web-404.webp` (cabecera de la 404), `web-frase.webp` (fondo de la banda del lema en Quien soy) y `web-compartir.webp` (fondo de `og.png`). Los PNG de ChatGPT se recortan antes: cabeceras, el 64 % derecho; portadas de guias, el 72 % superior.
- Tambien en `web-img/`: `web-contexto`, `web-fuerza-centro`, `web-evidencia` (tarjetas de Como trabajo), `web-poco-tiempo`, `web-dolor`, `web-cronica`, `web-genericas` (Con quien trabajo; si falta, sale el icono) y `boletin-habito`, `boletin-cafeina`, `boletin-pulsaciones` (ultimos envios, lista `BIMG` en el mismo orden que `ENV`; cambiar cuando cambien los envios). Colocadas las 27 ilustraciones el 17/11/2026.
- `og.mjs` necesita la letra Archivo. Si no hay acceso a Google Fonts: `npm i @fontsource-variable/archivo` y `FBE_FUENTE=<ruta>/files/archivo-latin-wdth-normal.woff2 node og.mjs`.
- `ver3.mjs` importa `servir` de `/home/claude/app-atletas/test/servidor.mjs` (repo fbe-equipo); si no está, usar cualquier servidor estático.

## Reglas
- Responder a Pelayo en español llano (no es programador), resultado primero.
- Mientras esté en pruebas: todas las páginas llevan `<meta name="robots" content="noindex">` y `robots.txt` con `Disallow: /`. Tras regenerar hay que reponerlos (el generador escribe la versión indexable). Quitarlos al pasar al dominio.
- El correo de Pelayo NO va escrito en el código: `ESCRIBE` lo lee de la variable `FBE_CORREO`; sin ella enlaza al formulario. No publicarlo sin que él lo apruebe.
- No cambiar DNS ni nada en IONOS o MailerLite sin su visto bueno expreso. Nunca tocar los registros MX ni los subdominios `atletas.` y `calculadoradeproteina.`.
- No inventar datos (precios, plazos, cifras, testimonios). Los textos de testimonios son extractos de su web actual.
- CSS nuevo: solo ASCII, colores por tokens (`--noche`, `--marca`, `--marca-clara`, `--oro`, `--sup`, `--fondo`, `--tinta`, `--lila`...) con versión oscura, movimiento respetando `prefers-reduced-motion`.
- La clase `.tema` es el botón claro/oscuro: no reutilizarla. Fuera de un artifact hace falta `[hidden]{display:none!important}` e `img{height:auto}`.
- Las fotos de personas reales (retrato, testimonios) deben ser fotos reales, nunca generadas.
