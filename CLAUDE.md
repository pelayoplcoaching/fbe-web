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
- Fotos reales de Pelayo en `web-img/`: `foto-pelayo.webp` (retrato 4:5 de Quien soy y de la portada; sale de su foto redonda, con las esquinas rellenadas con el fondo morado; si falta, se usa la de MailerLite) y `foto-banner.webp` (banda en Puesta a punto, tras «Que incluye»).
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

## Landings de guias (carpetas sueltas)
- `guia-dos-dias/` (landing de la guia «Dos dias de gimnasio»): NO sale de `fuente/`. Es una carpeta autocontenida (index.html, gracias.html, img/ y el PDF) con su propia paleta de campana; se edita a mano y el generador no la toca.
- Su formulario es el insertado de MailerLite «Guía · Dos días de gimnasio (web)» (`data-form="rE4kdS"`), grupo «Atletas PL coaching». Debe redirigir a `guia-dos-dias/gracias.html`.
- `guia-fuerza-segun-nivel/` (landing de la guia «Fuerza segun nivel», la de «¿Cuanta fuerza deberias tener a los 40, 50 y 60?»): igual que la anterior, carpeta autocontenida; desde el 19/11/2026 con estilo futurista (fondo oscuro, neon violeta, letras Space Grotesk y Space Mono de Google Fonts) e imagenes 3D sin personas. Formulario insertado de MailerLite «Guía · Fuerza según nivel (web)» (`data-form="p6ityX"`), grupo «Atletas PL coaching». Debe redirigir a `guia-fuerza-segun-nivel/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-plan-navidad/` (landing de la guia «El plan minimo para no perder musculo en Navidad», video del 13/12/2026): carpeta autocontenida como las anteriores, con paleta morado, lila, blanco, gris y negro, y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Plan Navidad (web)» (`data-form="Jy4YWB"`), grupo «Atletas PL coaching». Debe redirigir a `guia-plan-navidad/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-fuerza-padres/` (landing de la guia «La fuerza de tus padres: una prueba y cuatro ejercicios», video del 20/12/2026): carpeta autocontenida, con cabecera lila clara y texto negro, y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Fuerza padres (web)» (`data-form="QwaWyM"`), grupo «Atletas PL coaching». Debe redirigir a `guia-fuerza-padres/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-mes-a-mes/` (landing de la guia «Un ano de fuerza: que cambia mes a mes», video del 27/12/2026): carpeta autocontenida, con cabecera negra y acentos morados, linea de tiempo de los cuatro tramos y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Mes a mes (web)» (`data-form="sv6HEi"`), grupo «Atletas PL coaching». Debe redirigir a `guia-mes-a-mes/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-primeras-semanas/` (landing de la guia «Como empezar: las primeras 4 semanas», video del 3/1/2027): carpeta autocontenida, con cabecera blanca de papel cuadriculado y acentos morados, fichas de las cuatro semanas y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Primeras semanas (web)» (`data-form="GdLzWU"`), grupo «Atletas PL coaching». Debe redirigir a `guia-primeras-semanas/gracias.html`. No esta enlazada desde la pagina de Guias.
- Llevan `noindex` como el resto mientras la web este en pruebas; al pasar al dominio se quita de `index.html` y se deja en `gracias.html`.
