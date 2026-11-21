#!/usr/bin/env bash
# Regenera toda la web (escribe en la carpeta de arriba) y repone el modo pruebas (noindex y robots).
# Uso: bash fuente/generar.sh        -> web en pruebas (noindex)
#      FBE_PUBLICAR=1 bash fuente/generar.sh  -> web indexable (solo al pasar al dominio)
set -e
cd "$(dirname "$0")"
cat sitio-cab.py interior.py > sitio.py && python3 sitio.py >/dev/null; rm -f sitio.py web-fbe-equipo.html sitio-inicio.html
F=${FBE_FUENTE:-/tmp/fnt/node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2}
if [ ! -f "$F" ]; then (mkdir -p /tmp/fnt && cd /tmp/fnt && npm i @fontsource-variable/archivo --silent >/dev/null 2>&1) || true; fi
if [ -f "$F" ]; then FBE_FUENTE="$F" node og.mjs; else node og.mjs; fi
cd ..
if [ "${FBE_PUBLICAR:-}" != "1" ]; then
  printf 'User-agent: *\nDisallow: /\n' > robots.txt
  for f in *.html; do grep -q 'name="robots" content="noindex"' "$f" || sed -i '0,/<meta charset="utf-8">/s//<meta charset="utf-8"><meta name="robots" content="noindex">/' "$f"; done
  echo "noindex: $(grep -l noindex *.html | wc -l) de $(ls *.html | wc -l)"
fi
cd fuente && node ver3.mjs > /tmp/fbe-ver.txt 2>&1 || true; rm -f x3-*.png y3-*.png o3-*.png
echo "limpias: $(grep -c 'desborde false rotos 0 $' /tmp/fbe-ver.txt) de 16"; grep -v 'desborde false rotos 0 $' /tmp/fbe-ver.txt | cut -c1-160 || true
