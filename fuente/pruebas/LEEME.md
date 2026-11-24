# Pruebas automáticas

Todo se ejecuta contra la web ya generada (la carpeta raíz del repo), con un servidor local parecido a GitHub Pages.

```
bash fuente/generar.sh                 # regenera la web (modo pruebas: noindex)
node fuente/pruebas/todas.mjs rapidas  # pruebas de funciones y enlaces (~4 min)
node fuente/pruebas/todas.mjs          # además: desbordes, tarjetas y accesibilidad en todas las páginas (~20 min)
```

- `comun.mjs`: raíz del sitio, Playwright y servidor (gzip, caché de 10 min).
- `calculadoras-1*.mjs`, `calculadoras-2.mjs`, `calculadoras-3.mjs`, `diez-mejoras.mjs`: cálculos e interacción de las herramientas.
- `extras.mjs`, `mitos.mjs`, `resaltado.mjs`, `secciones.mjs`: buscador, glosario, archivo, Mis resultados, sin conexión, mitos y secciones nuevas.
- `enlaces.mjs`: enlaces internos, anclas, imágenes y sitemap.
- `esencial.mjs`: FBE Esencial. La función de reserva (`formularios/funciones/esencial.mjs`) con Stripe simulado: ventanas, plazas, pago y comprobación; y los estados de `esencial.html` (pronto, abierto, casi, lleno, cerrado, error) y la página de gracias.
- `desbordes.mjs`: nada se sale de la pantalla (1280 y 390 px, claro y oscuro). Acepta páginas sueltas: `node desbordes.mjs glosario mitos`.
- `cajas.mjs`: ningún texto se sale de su tarjeta (1280, 1100 y 390 px).
- `accesibilidad.mjs`: axe-core (WCAG 2.2 AA). Necesita `npm i` en esta carpeta. Falla si hay errores graves.
- Las capturas y el informe de axe van a la carpeta temporal del sistema (`fbe-pruebas`).
