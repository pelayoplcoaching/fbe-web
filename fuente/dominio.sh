#!/usr/bin/env bash
# Paso al dominio (preparado el 23/11/2026). Ejecutar SOLO cuando Pelayo haya verificado el dominio en GitHub
# y justo antes de que cambie el A y el www en IONOS. No toca IONOS ni MailerLite: solo la web.
#  1. CNAME con el dominio (GitHub Pages lo lee y empieza a servir la web en fuerzabasadaenevidencia.com;
#     la direccion de pruebas pelayoplcoaching.github.io/fbe-web pasa a redirigir al dominio).
#  2. Genera la web en modo publicado: sin noindex (salvo las paginas que lo llevan siempre: gracias, pedir plaza,
#     tarifas, Mi panel, Mis resultados, sin conexion, 404 y los desvios viejos) y robots.txt que deja entrar.
#  3. Landings de guias: quita el noindex de index.html (gracias.html lo conserva).
# Despues: node fuente/pruebas/todas.mjs rapidas, commit y push.
set -e
cd "$(dirname "$0")/.."
printf 'fuerzabasadaenevidencia.com\n' > CNAME
FBE_PUBLICAR=1 bash fuente/generar.sh
for f in guia-*/index.html; do sed -i 's#<meta name="robots" content="noindex">##' "$f"; done
echo "Con noindex: $(grep -l 'name="robots" content="noindex"' *.html | tr '\n' ' ')"
echo "Guias con noindex en index.html: $(grep -l 'content="noindex"' guia-*/index.html | wc -l) (debe ser 0)"
cat robots.txt
