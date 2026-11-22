// Ejecuta todas las pruebas y resume. Uso: node fuente/pruebas/todas.mjs [rapidas]
import { spawnSync } from 'child_process'; import path from 'path'; import { fileURLToPath } from 'url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const LISTA = [
  ['calculadoras-1.mjs', 'Cinco primeras calculadoras'], ['calculadoras-1-extra.mjs', 'Mejoras de las cinco primeras'], ['calculadoras-2.mjs', 'Segunda tanda de calculadoras'],
  ['calculadoras-3.mjs', 'OMS, cintura/altura, prensión y ajustes'], ['diez-mejoras.mjs', 'Calorías, test de mitos, plan, Mis resultados'], ['extras.mjs', 'Buscador, glosario, archivo, Mis resultados, sin conexión'],
  ['mitos.mjs', 'Mitos'], ['resaltado.mjs', 'Resaltado y letras del glosario'], ['secciones.mjs', 'Secciones nuevas'], ['enlaces.mjs', 'Enlaces, anclas, imágenes y sitemap'], ['menu.mjs', 'Menú con desplegables'], ['herramientas-hub.mjs', 'Herramientas por objetivo'], ['siguiente.mjs', '¿Y ahora qué? bajo cada resultado'], ['fuentes.mjs', 'Fuentes comprobadas'], ['autoria.mjs', 'Firma y Cómo trabajo la evidencia'], ['temas.mjs', 'Páginas de tema'], ['n404.mjs', '404 con sugerencias'], ['evolucion.mjs', 'Mi evolución e informe para el médico'], ['chequeo.mjs', 'Chequeo de 10 minutos'], ['compartir.mjs', 'Compartir resultado (imagen)'], ['recetas.mjs', 'Recetas con proteína'], ['boletin-cta.mjs', 'El boletín, por tema'], ['datos.mjs', 'Datos estructurados'], ['videos.mjs', 'Vídeos en cuadrícula'], ['calculadoras-4.mjs', 'Temporizador, semana activa, pasos, tensión y equilibrio'], ['app.mjs', 'La web como app'],
  ['desbordes.mjs', 'Nada se sale de la pantalla (todas las páginas)'], ['cajas.mjs', 'Nada se sale de su tarjeta (todas las páginas)'], ['accesibilidad.mjs', 'Accesibilidad (axe)'],
];
const rapidas = process.argv[2] === 'rapidas'; let mal = 0;
for (const [f, t] of LISTA) {
  if (rapidas && ['desbordes.mjs', 'cajas.mjs', 'accesibilidad.mjs'].includes(f)) continue;
  const ini = Date.now(); const r = spawnSync(process.execPath, [path.join(dir, f)], { encoding: 'utf8', timeout: 30 * 60 * 1000 });
  const sal = (r.stdout || '') + (r.stderr || ''); const fin = sal.trim().split('\n').pop();
  const bien = /todo correcto|sin problemas|nada se sale|rotos: 0/.test(sal) && !/FALLOS|PROBLEMA|salen: \d|con problemas/.test(fin) && r.status === 0;
  if (!bien) mal++;
  console.log(`${bien ? '✔' : '✘'} ${t} (${Math.round((Date.now() - ini) / 1000)} s)${bien ? '' : '\n' + sal.split('\n').filter(l => /✘|FALLOS|PROBLEMA|Error|salen/.test(l)).slice(0, 12).join('\n')}`);
}
console.log(mal ? `\n${mal} pruebas con fallos` : '\nTodas las pruebas pasan'); process.exit(mal ? 1 : 0);
