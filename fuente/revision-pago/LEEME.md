# Página de pago de la Revisión de evidencia FBE (MailerLite)

La página «Revisión de evidencia FBE · suscripción» está en MailerLite (página 205028375716169269, sitio 205028375621797384), no en esta web. Su diseño va en bloques «Código» del editor de MailerLite; aquí está la fuente.

- `estilo.css`: toda la capa de estilo (va dentro del primer bloque, `top.html`, en un `<style>`). Restila también los bloques propios de MailerLite: el botón de compra (bloque «Productos», que no se toca), las condiciones (acordeón con el NIF, que escribe Pelayo) y el pie.
- `bloques.py`: escribe `salida/top.html` (estilo + cabecera), `hero.html` (portada, columna izquierda), `cab.html` y `pie.html` (encima y debajo del botón de compra, columna derecha), `cuerpo.html` (el resto) y `mock.html` (maqueta con la misma estructura que MailerLite para probar en local).
- Probar en local: `python3 bloques.py && python3 captura.py salida/mock.html /tmp/m.png 1280` (o 390) y `python3 desborde.py salida/mock.html 390`.
- Pasar a MailerLite: subir los cambios a GitHub y, en el editor de la página (Chrome de Pelayo), leer cada bloque de https://fuerzabasadaenevidencia.com/fuente/revision-pago/salida/<bloque>.html con fetch, ponerlo en el textarea de su bloque «Código» y pulsar «Guardar» de ese bloque. Nunca publicar la página sin su visto bueno (se publica el 1/1/2027).
- MailerLite quita los `<svg>` y no ejecuta `<script>` dentro de los bloques «Código»: los iconos van en el CSS (máscaras con SVG codificado) y nada depende de JavaScript.
