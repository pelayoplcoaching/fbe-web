import re, sys
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_BREAK
R='/home/claude/fbe-web/'
GR=[('1. Para vender', ['index','quien-soy','programas','tarifas','puesta-a-punto','guias','newsletter','dudas','pedir-plaza','gracias-plaza','gracias-boletin','gracias']),
 ('2. Para aprender', ['aprende','empieza-aqui','mitos','videos','recetas','evidencia','profesionales','medios','tema-envejecer','tema-medicacion','tema-dolor','tema-nutricion','tema-poco-tiempo']),
 ('3. Herramientas', ['herramientas','chequeo','pauta-activa','revision-medica','actividad-oms','test-silla','cintura-altura','test-sppb','prension','equilibrio','zonas-pulso','semaforo-dolor','paron','calculadora-1rm','volumen-semanal','semana-activa','pasos','tension','calorias','cafeina','suplementos','temporizador']),
 ('4. La web como app', ['mi-panel','mis-resultados','ayuda','sin-conexion','404'])]
SALTA={'script','style','svg','template','noscript','nav','img','picture','iframe','canvas','select','input','textarea','datalist','dialog'}
BLOQ={'p','li','ul','ol','div','section','article','table','h1','h2','h3','h4','h5','details','summary','dl','dt','dd','figure','figcaption','blockquote','aside','header','footer','form','label','fieldset','legend','tr','td','th','thead','tbody','main','button'}
def txt(e): return re.sub(r'\s+',' ',e.get_text(' ',strip=True)).replace(' ,',',').replace(' .','.').replace(' :',':').replace(' ;',';').replace('( ','(').replace(' )',')').strip()
def hoja(e): return not any(isinstance(c,Tag) and c.name in BLOQ for c in e.descendants)
d=Document()
st=d.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(11)
for s in d.sections: s.left_margin=s.right_margin=Cm(2.2); s.top_margin=s.bottom_margin=Cm(2.2)
for n,sz in (('Title',24),('Heading 1',20),('Heading 2',15),('Heading 3',12.5),('Heading 4',11.5)):
    f=d.styles[n].font; f.name='Arial'; f.size=Pt(sz); f.color.rgb=RGBColor(0x2A,0x1A,0x6E); f.bold=True
    d.styles[n].element.rPr.rFonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia','Arial')
cuenta={'pal':0,'pag':0}
def par(t,estilo=None,gris=False,neg=False):
    if not t: return
    p=d.add_paragraph(style=estilo) if estilo else d.add_paragraph()
    r=p.add_run(t); r.bold=neg
    if gris: r.font.color.rgb=RGBColor(0x77,0x77,0x88); r.font.size=Pt(9.5)
    cuenta['pal']+=len(t.split())
def tabla(e):
    filas=[[txt(c) for c in tr.find_all(['th','td'],recursive=False)] for tr in e.find_all('tr')]
    filas=[f for f in filas if f]
    if not filas: return
    n=max(len(f) for f in filas); t=d.add_table(rows=0,cols=n); t.style='Table Grid'
    for i,f in enumerate(filas):
        c=t.add_row().cells
        for j,x in enumerate(f):
            c[j].text=x
            for p in c[j].paragraphs:
                for r in p.runs: r.font.size=Pt(9.5); r.bold=(i==0 or j==0)
            cuenta['pal']+=len(x.split())
    d.add_paragraph()
def anda(e,visto):
    for c in e.children:
        if isinstance(c,NavigableString):
            t=re.sub(r'\s+',' ',str(c)).strip()
            if len(t)>1: par(t)
            continue
        if c.name in SALTA or 'oculto' in (c.get('class') or []) or c.get('aria-hidden')=='true': continue
        cl=' '.join(c.get('class') or [])
        if c.name=='table': tabla(c); continue
        if c.name in ('h2','h3','h4','h5'):
            t=txt(c)
            if t: d.add_heading(t, level={'h2':2,'h3':3,'h4':4,'h5':4}[c.name]); cuenta['pal']+=len(t.split())
            continue
        if hoja(c):
            t=txt(c)
            if not t or len(t)<2: continue
            k=(c.name,t)
            if k in visto and len(t)>40: continue
            visto.add(k)
            if c.name=='li': par(t,'List Bullet')
            elif c.name=='summary': par(t,neg=True)
            elif c.name in ('button','label','legend','dt') or 'btn' in cl.split(): par('['+('Botón' if c.name=='button' or 'btn' in cl.split() else 'Etiqueta')+'] '+t,gris=True)
            else: par(t)
        else: anda(c,visto)
d.add_heading('Web FBE · Todos los textos para revisar',0)
par('Versión del 23 de noviembre de 2026. Sacado tal cual de la web publicada en pruebas, página por página.')
d.add_heading('Cómo usarlo',2)
for x in ['Corrige encima de cada texto. Lo que dejes sin tocar lo doy por bueno.',
 'Si algo sobra entero, bórralo o escribe «quitar» al lado.',
 'Cuando termines, devuélveme este mismo archivo: comparo tu versión con esta y aplico todos los cambios de una vez.',
 'Las líneas en gris que empiezan por [Botón] o [Etiqueta] son textos de botones y de campos: también se pueden corregir.',
 'No cambies cifras de estudios sin decirme la fuente nueva: cada cifra de las herramientas y de los mitos va ligada a su referencia.']: par(x,'List Bullet')
d.add_heading('Qué no está aquí',2)
for x in ['Las listas de referencias al pie de cada herramienta, las tarjetas de las diez recetas (salen de tu app), la cuadrícula de vídeos (tus títulos de YouTube) y, en las páginas de tema, lo que solo repite cosas de otras páginas.',
 'Fuentes (la lista de 48 referencias, comprobadas en PubMed), el archivo del boletín (tus asuntos de MailerLite) y Novedades (se escribe sola con tus vídeos y envíos).',
 'Glosario: aprobaste sus definiciones el 22 de noviembre.',
 'Privacidad: es tu política de MailerLite, con el alojamiento cambiado.',
 'Las landings de las guías de los vídeos: se llevan en la otra conversación.',
 'Los mensajes que escriben las calculadoras al dar un resultado («Cumples el mínimo», avisos…): los genera el programa y no salen en la página hasta usarla. Si quieres revisarlos también, te los saco en un segundo documento.',
 'El menú, el pie y los avisos comunes a todas las páginas van una sola vez, al final.']: par(x,'List Bullet')
indice=[]
for g,ps in GR:
    d.add_page_break(); d.add_heading(g,1)
    for n in ps:
        s=BeautifulSoup(open(R+n+'.html',encoding='utf-8').read(),'html.parser')
        tit=s.title.get_text().split(' · ')[0] if n!='index' else 'Portada'
        d.add_heading(f'{tit}  ·  /{n}.html',2); cuenta['pag']+=1; indice.append((g,tit))
        md=s.find('meta',attrs={'name':'description'})
        if md and md.get('content'): par('Descripción para Google: '+md['content'],gris=True)
        visto=set()
        h=s.find(class_='hero') or s.find('header',class_='hero')
        if h:
            h1=h.find('h1')
            if h1: par('Título: '+txt(h1),neg=True)
            hh=BeautifulSoup(str(h),'html.parser')
            for x in hh.find_all('h1'): x.decompose()
            for x in hh.find_all(class_='miga'): x.decompose()
            for x in hh.find_all(class_='marca-agua'): x.decompose()
            anda(hh,visto)
        m=s.find('main')
        if m:
            mm=BeautifulSoup(str(m),'html.parser')
            for x in mm.find_all(class_='hero'): x.decompose()
            for sel in ('.bol-cta-s','#en-video','.tm-vid','#fuentes-tema','#palabras','ol.fuentes-t','.firma','article.rec','#vid-rej','.recetas','.chq-barra'):
                for x in mm.select(sel): x.decompose()
            if n.startswith('tema-'):
                for x in mm.select('#boletin'): x.decompose()
            for x in mm.find_all(id=['fuentes','en-video']): pass
            anda(mm,visto)
d.add_page_break(); d.add_heading('5. Comunes a todas las páginas',1)
s=BeautifulSoup(open(R+'programas.html',encoding='utf-8').read(),'html.parser')
e=BeautifulSoup(open(R+'tension.html',encoding='utf-8').read(),'html.parser').select_one('.bol-cta-s')
if e:
    d.add_heading('Invitación al boletín (al final de cada herramienta, de Mitos y del Glosario)',2)
    for x in e.select('ul,ol'): x.decompose()
    anda(BeautifulSoup(str(e),'html.parser'),set())
e=BeautifulSoup(open(R+'tension.html',encoding='utf-8').read(),'html.parser').select_one('.firma')
if e: d.add_heading('Firma (bajo la entradilla de las páginas de salud)',2); par(txt(e))
for sel,tit in (('section.cierre','Cierre de página (cambia el título según la página)'),('footer','Pie'),):
    e=s.select_one(sel)
    if e: d.add_heading(tit,2); anda(BeautifulSoup(str(e),'html.parser'),set())
d.save(sys.argv[1]); print(cuenta, len(indice))
