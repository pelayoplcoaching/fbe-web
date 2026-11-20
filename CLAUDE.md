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
- `foto-playa.webp` (foto real de Pelayo en la playa): bloque «Quien te escribe» bajo «Que te llega» en Newsletter.
- La letra Archivo se sirve desde la propia web (`fuente/ext/archivo.woff2` -> `img/archivo.woff2`), recortada el 20/11/2026 a latin basico + espanol + signos tipograficos (57 KB; si aparece un caracter raro sin estilo, rehacer el recorte desde @fontsource-variable/archivo con fontTools.subset); el final de interior.py sustituye el enlace de Google Fonts en todas las paginas generadas. Las landings de guias siguen cargando sus letras de Google.
- `privacidad.html`: texto de su politica de MailerLite (sept. 2026), con el alojamiento cambiado a GitHub (20/11/2026). Se genera con el correo de `FBE_CORREO`. Las landings de guias enlazan a `../privacidad.html` desde el 20/11/2026 (antes, a la de MailerLite).
- `futuro.css`: capa de estilo tecnologico y futurista (desde 20/11/2026), 11 tandas de 20 mejoras (1-220); la 11 es de limpieza: no volver a meter animaciones continuas sin quitar otra. Se anade despues de `sitio.css` tanto en `fbe.css` como en la portada (sitio-cab.py). Usa `--mono` (letra de sistema monoespaciada, sin Google), `--rejilla` y `--hilo`.
- `luz.js`: guion pequeno que se anade a `fbe.js` y al final de la portada: numera las secciones (`data-n`, salta `.cierre` y `.lema-banda`), foco de luz e inclinacion de tarjetas (solo raton), respuestas al usar (filtro de guias, test de Programas, copiar analitica, calculadora, indice de Dudas, menu con Escape), fundido de imagenes de tarjeta y pausa de toda animacion continua cuya seccion no se ve o si la pestana esta oculta.
- `ilus()` de interior.py pone `width`/`height` reales a cada imagen y carga con prioridad las de cabecera (`ilus`). El final de interior.py anade `preconnect` a MailerLite, `speculationrules` (prefetch al pasar) y quita los comentarios de `fbe.css`.
- Boletin: formulario nuevo de MailerLite «Boletín · Newsletter (web)» (id 204678811842774100, `data-form="IpOp9n"`, grupo «Atletas PL coaching»), creado el 20/11/2026 como borrador para que Pelayo lo termine en el editor. Redirige a `gracias-boletin.html` (siempre noindex, fuera del sitemap). Desde el 20/11/2026 la pagina Newsletter usa este formulario (Pelayo lo confirmo en funcionamiento); el antiguo `9jHHlI` sigue en su web vieja de MailerLite. La bienvenida automatica («Email de bienvenida simple») se dispara por formulario: hay que anadirle el nuevo. Al pasar al dominio, cambiar la redireccion del formulario a fuerzabasadaenevidencia.com/gracias-boletin.html.
- `gracias.html`: pagina a la que vuelve Stripe tras pagar la Puesta a punto (en la web vieja era /gracias; comprobado en Stripe el 20/11/2026: el enlace de pago redirige a https://fuerzabasadaenevidencia.com/gracias, y su casilla de consentimiento enlaza a la privacidad vieja de MailerLite, a cambiar por la nueva tras el dominio). Texto copiado de la web vieja el 20/11/2026, con su Gmail cambiado por el correo publico. Enlaces: cuestionario https://tally.so/r/J94Voz y cita https://calendly.com/pelayoplcoaching/puesta-a-punto-videollamada. Siempre noindex.
- Desvios de la web vieja (MailerLite, sin .html): `faq.html` -> dudas, `newsletter-semanal.html` -> newsletter, `programas-copy.html` -> guias, `quien_soy.html` -> quien-soy (GitHub Pages sirve /faq como faq.html). /programas, /puesta-a-punto y /gracias coinciden con las nuevas.
- `og.mjs` necesita la letra Archivo. Si no hay acceso a Google Fonts: `npm i @fontsource-variable/archivo` y `FBE_FUENTE=<ruta>/files/archivo-latin-wdth-normal.woff2 node og.mjs`.
- `ver3.mjs` importa `servir` de `/home/claude/app-atletas/test/servidor.mjs` (repo fbe-equipo); si no está, usar cualquier servidor estático.

## Reglas
- Responder a Pelayo en español llano (no es programador), resultado primero.
- Mientras esté en pruebas: todas las páginas llevan `<meta name="robots" content="noindex">` y `robots.txt` con `Disallow: /`. Tras regenerar hay que reponerlos (el generador escribe la versión indexable). Quitarlos al pasar al dominio.
- Correo publico aprobado por Pelayo el 20/11/2026: pelayofbe@fuerzabasadaenevidencia.com (buzon de IONOS). Va por defecto en `FBE_CORREO` (sitio-cab.py), escrito con entidades HTML para despistar a los robots. Su Gmail personal no se publica nunca.
- No cambiar DNS ni nada en IONOS o MailerLite sin su visto bueno expreso. Nunca tocar los registros MX ni los subdominios `atletas.` y `calculadoradeproteina.`.
- No inventar datos (precios, plazos, cifras, testimonios). Los textos de testimonios son extractos de su web actual.
- CSS nuevo: solo ASCII, colores por tokens (`--noche`, `--marca`, `--marca-clara`, `--oro`, `--sup`, `--fondo`, `--tinta`, `--lila`...) con versión oscura, movimiento respetando `prefers-reduced-motion`.
- La clase `.tema` es el botón claro/oscuro: no reutilizarla. Fuera de un artifact hace falta `[hidden]{display:none!important}` e `img{height:auto}`.
- Las fotos de personas reales (retrato, testimonios) deben ser fotos reales, nunca generadas.

## Calculadora de proteína (subdominio calculadoradeproteina., en Netlify)
- No la publica GitHub Pages: va en Netlify (proyecto `calculadoraproteinafbe`, id e38619c9-9c99-4e59-890e-8e6a99f13f40), subida a mano arrastrando carpeta. No tocar su DNS.
- Fuente en `fuente/calculadora/`: `plantilla.html` (estilo de la web en 3 tandas de 20 mejoras, 20/11/2026) -> `python3 hacer.py` escribe `netlify/` (index.html con el lobo, archivo.woff2, favicon.svg, icono-180.png) y `node og.mjs` hace `netlify/og.jpg`. `original-netlify.html` es la versión anterior (con el PNG del logo quitado).
- Cálculos y textos sin cambiar (comprobado contra la versión anterior en 42 combinaciones y 6 casos del paso 0). Arreglado el fallo de la anterior: salía «NaN – NaN» al cargar y tras usar el paso 0 (cogía también los botones del paso 0 como fases).
- Publicar solo con el visto bueno de Pelayo.

## Formulario propio «Pedir plaza» (sustituye a NoteForms; 20/11/2026)
- `pedir-plaza.html` y `gracias-plaza.html` (interior.py; noindex y fuera del sitemap). Mismas preguntas que el NoteForms y mismas opciones que la base de Notion «Leads – Nuevos contactos» (database a5c4e10c-7a3f-4155-9384-ab91a3a0b12a).
- Se envía como formulario normal a `PLAZA_ENVIO` (sitio-cab.py) = función de Netlify `fuente/formularios/funciones/plaza.mjs`, proyecto de Netlify `fbe-formularios` (id bfa7cb8d-f56e-4d0e-a01d-d97845ae9573, creado sin protección de acceso). La función crea la fila en Notion con «Estado del Lead» = «🆕 Nuevo (formulario enviado)» y redirige a gracias-plaza.html, o a pedir-plaza.html?error=1 (datos) / ?error=2 (fallo técnico; la página recupera lo escrito). Trampas para robots: campo oculto `web` y envío en menos de 3 s.
- Necesita en Netlify la variable `NOTION_TOKEN` (integración interna de Notion «Web FBE» con acceso a esa base; la pone Pelayo, nunca en el código) y el proyecto enlazado al repo con base directory `fuente/formularios`.
- Mientras no se haya probado de verdad, los botones «Pedir plaza» (`FORM` en sitio-cab.py) siguen yendo a NoteForms. Al probarlo: cambiar `FORM = 'pedir-plaza.html'`.
- Ojo: su resumen diario de correo detecta los leads por el aviso de nuevo formulario en Gmail; si ese aviso lo mandaba NoteForms, hay que sustituirlo.

## Landings de guias (carpetas sueltas)
- `guia-dos-dias/` (landing de la guia «Dos dias de gimnasio»): NO sale de `fuente/`. Es una carpeta autocontenida (index.html, gracias.html, img/ y el PDF) con su propia paleta de campana; se edita a mano y el generador no la toca.
- Su formulario es el insertado de MailerLite «Guía · Dos días de gimnasio (web)» (`data-form="rE4kdS"`), grupo «Atletas PL coaching». Debe redirigir a `guia-dos-dias/gracias.html`.
- `guia-fuerza-segun-nivel/` (landing de la guia «Fuerza segun nivel», la de «¿Cuanta fuerza deberias tener a los 40, 50 y 60?»): igual que la anterior, carpeta autocontenida; desde el 19/11/2026 con estilo futurista (fondo oscuro, neon violeta, letras Space Grotesk y Space Mono de Google Fonts) e imagenes 3D sin personas. Formulario insertado de MailerLite «Guía · Fuerza según nivel (web)» (`data-form="p6ityX"`), grupo «Atletas PL coaching». Debe redirigir a `guia-fuerza-segun-nivel/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-plan-navidad/` (landing de la guia «El plan minimo para no perder musculo en Navidad», video del 13/12/2026): carpeta autocontenida como las anteriores, con paleta morado, lila, blanco, gris y negro, y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Plan Navidad (web)» (`data-form="Jy4YWB"`), grupo «Atletas PL coaching». Debe redirigir a `guia-plan-navidad/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-fuerza-padres/` (landing de la guia «La fuerza de tus padres: una prueba y cuatro ejercicios», video del 20/12/2026): carpeta autocontenida, con cabecera lila clara y texto negro, y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Fuerza padres (web)» (`data-form="QwaWyM"`), grupo «Atletas PL coaching». Debe redirigir a `guia-fuerza-padres/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-mes-a-mes/` (landing de la guia «Un ano de fuerza: que cambia mes a mes», video del 27/12/2026): carpeta autocontenida, con cabecera negra y acentos morados, linea de tiempo de los cuatro tramos y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Mes a mes (web)» (`data-form="sv6HEi"`), grupo «Atletas PL coaching». Debe redirigir a `guia-mes-a-mes/gracias.html`. No esta enlazada desde la pagina de Guias.
- `guia-primeras-semanas/` (landing de la guia «Como empezar: las primeras 4 semanas», video del 3/1/2027): carpeta autocontenida, con cabecera blanca de papel cuadriculado y acentos morados, fichas de las cuatro semanas y sus propios `extra.css` y `extra.js`. Formulario insertado de MailerLite «Guía · Primeras semanas (web)» (`data-form="GdLzWU"`), grupo «Atletas PL coaching». Debe redirigir a `guia-primeras-semanas/gracias.html`. No esta enlazada desde la pagina de Guias.
- Llevan `noindex` como el resto mientras la web este en pruebas; al pasar al dominio se quita de `index.html` y se deja en `gracias.html`.
