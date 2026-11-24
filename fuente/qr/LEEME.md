# QR de las direcciones cortas

- `/nivel` -> guía «¿Cuánta fuerza deberías tener a los 40, 50 y 60?» (`guia-fuerza-segun-nivel/`) y `/dosdias` -> guía «Dos días de gimnasio» (`guia-dos-dias/`). Las páginas de desvío las escribe interior.py (`CORTAS`), con utm_source=youtube, utm_medium=qr.
- `python3 hacer.py`: QR sencillos (`qr-<corta>.png` y `.svg`, oscuro sobre blanco).
- `python3 futurista.py`: tarjeta vertical con fondo transparente alrededor (`qr-<corta>-tarjeta.png`) y pantalla 1920 x 1080 (`qr-<corta>-pantalla.png`), al estilo de la landing de Fuerza según nivel (Space Grotesk y Space Mono; la de Dos días en naranja). Necesita las letras en /tmp/sp:
  `mkdir -p /tmp/sp && cd /tmp/sp && npm i @fontsource/space-grotesk@5 @fontsource/space-mono@5` y convertir los woff2 de 500/700 y 400/700 a sg500.ttf, sg700.ttf, sm400.ttf y sm700.ttf con fontTools (flavor = None).
- Comprobados con OpenCV: se leen a tamaño completo, al 30 % y la tarjeta al 15 %.
