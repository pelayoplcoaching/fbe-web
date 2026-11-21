# «Compartir resultado» (21/11/2026, noche): bajo cada herramienta, una imagen para compartir hecha en el propio navegador.
# Lo ejecuta interior.py después de chequeo.py. Con el resultado: el nombre de la herramienta, la cifra grande y su unidad,
# el titular de la zona (si hay) y la fecha; sin edad, sexo, peso ni ningún otro dato de la persona. O solo la herramienta.
# Se comparte con el menú del móvil (si deja compartir archivos) o se descarga; también «Copiar enlace». Nada se sube.
COMP_JS = r"""(function(){var D=document,r=D.querySelector('.tool-res');if(!r)return;var g=r.querySelector('.guarda-r');if(!g)return;
var TIT=r.dataset.titulo||'',DESC=__DESC__,SLUG=(location.pathname.split('/').pop()||'').replace(/\.html$/,''),URL0=location.href.split('#')[0].split('?')[0],ZC={alto:'#5FD3A0',medio:'#F0C674',bajo:'#FF8FA3'},LOGO=null,dl=null,modo='res',blob=null,n=0;
function dato(){var gb=r.querySelector('.res-grande b'),gu=r.querySelector('.res-grande span'),vt=gb?gb.textContent.replace(/\s+/g,' ').trim():'',z=['z-alto','z-medio','z-bajo'].filter(function(c){return r.classList.contains(c)})[0],vd=r.querySelector('.res-veredicto');if(!/\d/.test(vt))vt='';return {vt:vt,u:vt&&gu?gu.textContent.trim():'',z:z?z.slice(2):'',zt:z&&vd?vd.textContent.replace(/\s+/g,' ').trim():'',s:r.dataset.serie||''}}
var b=D.createElement('button');b.type='button';b.className='copiar-t comp-r';b.innerHTML='<span>Compartir resultado</span>';g.insertAdjacentElement('afterend',b);
function mira(){var d=dato();b.hidden=g.hidden||!(d.vt||d.zt)}mira();var mo=new MutationObserver(mira);mo.observe(g,{attributes:true,attributeFilter:['hidden']});mo.observe(r,{attributes:true,attributeFilter:['class'],childList:true,subtree:true,characterData:true});
(function(){var sv=D.querySelector('.cab .logo svg');if(!sv)return;var c=sv.cloneNode(true);c.setAttribute('xmlns','http://www.w3.org/2000/svg');c.setAttribute('width','128');c.setAttribute('height','147');c.removeAttribute('class');[].forEach.call(c.querySelectorAll('path'),function(p){p.setAttribute('fill','#ffffff')});var im=new Image();im.onload=function(){LOGO=im};im.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(c))})();
function p2(x){return (x<10?'0':'')+x}function hoy(){var d=new Date();return p2(d.getDate())+'/'+p2(d.getMonth()+1)+'/'+d.getFullYear()}
function lineas(c,t,w){var ps=String(t).split(/\s+/),ls=[],l='';ps.forEach(function(p){var x=l?l+' '+p:p;if(c.measureText(x).width>w&&l){ls.push(l);l=p}else l=x});if(l)ls.push(l);return ls}
function rr(c,x,y,w,h,ra){c.beginPath();c.moveTo(x+ra,y);c.arcTo(x+w,y,x+w,y+h,ra);c.arcTo(x+w,y+h,x,y+h,ra);c.arcTo(x,y+h,x,y,ra);c.arcTo(x,y,x+w,y,ra);c.closePath()}
function dibuja(){var W=1080,H=1350,M=84,cv=D.createElement('canvas');cv.width=W;cv.height=H;var c=cv.getContext('2d'),d=dato(),res=modo==='res'&&(d.vt||d.zt),F=' Archivo, system-ui, sans-serif',y=M;
  var gr=c.createLinearGradient(0,0,W,H);gr.addColorStop(0,'#140B3A');gr.addColorStop(1,'#2f2470');c.fillStyle=gr;c.fillRect(0,0,W,H);
  var rg=c.createRadialGradient(W*.86,H*.1,0,W*.86,H*.1,W*.75);rg.addColorStop(0,'rgba(89,62,222,.55)');rg.addColorStop(1,'rgba(89,62,222,0)');c.fillStyle=rg;c.fillRect(0,0,W,H);
  c.strokeStyle='rgba(255,255,255,.045)';c.lineWidth=1;for(var x=54;x<W;x+=54){c.beginPath();c.moveTo(x+.5,0);c.lineTo(x+.5,H);c.stroke()}for(var yy=54;yy<H;yy+=54){c.beginPath();c.moveTo(0,yy+.5);c.lineTo(W,yy+.5);c.stroke()}
  c.strokeStyle='rgba(164,156,255,.35)';c.lineWidth=2;rr(c,28,28,W-56,H-56,44);c.stroke();
  if(LOGO)c.drawImage(LOGO,M,y,62,71);c.fillStyle='#fff';c.textBaseline='middle';c.font='700 34px'+F;c.fillText('Fuerza Basada en Evidencia',M+(LOGO?84:0),y+36);
  c.textBaseline='alphabetic';y+=170;c.fillStyle='#A49CFF';c.font='700 26px'+F;c.fillText(res?'MI RESULTADO':'HERRAMIENTA GRATUITA',M,y);
  c.fillStyle='#fff';c.font='800 74px'+F;lineas(c,TIT,W-2*M).slice(0,3).forEach(function(l){y+=88;c.fillText(l,M,y)});
  if(res&&d.s){y+=62;c.fillStyle='#D4D0F5';c.font='600 42px'+F;c.fillText(d.s,M,y)}
  var py=H-M-170,yT=y,ops=[],h=0;
  if(res){if(d.vt){var fs=220;c.font='800 '+fs+'px'+F;while(c.measureText(d.vt).width>W-2*M&&fs>100){fs-=10;c.font='800 '+fs+'px'+F}var vw=c.measureText(d.vt).width,cap=Math.round(fs*.74),uw=0,ul=false;
      if(d.u){c.font='600 52px'+F;uw=c.measureText(d.u).width;ul=vw+28+uw>W-2*M}
      (function(fs,vw,cap,ul){ops.push(function(y0){c.font='800 '+fs+'px'+F;c.fillStyle='#fff';c.fillText(d.vt,M,y0+cap);if(d.u){c.font='600 52px'+F;c.fillStyle='#D4D0F5';if(!ul)c.fillText(d.u,M+vw+28,y0+cap);else c.fillText(d.u,M,y0+cap+70)}})})(fs,vw,cap,ul);h+=cap+(ul?70:0)}
    if(d.zt){c.font='600 38px'+F;var zl=lineas(c,d.zt,W-2*M-110).slice(0,3),ch=34+zl.length*50,cw=Math.min(W-2*M,Math.max.apply(0,zl.map(function(l){return c.measureText(l).width}))+112),col=ZC[d.z]||'#D4D0F5',gap=d.vt?60:0,top=h+gap;
      ops.push(function(y0){var yy=y0+top;c.fillStyle='rgba(255,255,255,.06)';rr(c,M,yy,cw,ch,ch>90?30:ch/2);c.fill();c.strokeStyle=col;c.lineWidth=3;c.stroke();c.fillStyle=col;c.beginPath();c.arc(M+44,yy+ch/2,13,0,Math.PI*2);c.fill();c.font='600 38px'+F;c.fillStyle='#fff';zl.forEach(function(l,i){c.fillText(l,M+76,yy+45+i*50)})});h=top+ch}
    var td=h+78;ops.push(function(y0){c.fillStyle='#D4D0F5';c.font='500 32px'+F;c.fillText('Resultado del '+hoy(),M,y0+td)});h=td}
  else{c.font='500 46px'+F;var dl2=lineas(c,DESC,W-2*M).slice(0,6);ops.push(function(y0){c.fillStyle='#E8E6FF';c.font='500 46px'+F;dl2.forEach(function(l,i){c.fillText(l,M,y0+46+i*64)});c.fillStyle='#A49CFF';c.font='700 30px'+F;c.fillText('Gratis · Sin cuentas · En tu navegador',M,y0+46+(dl2.length-1)*64+92)});h=46+(dl2.length-1)*64+92}
  var y0=Math.max(yT+70,Math.round((yT+py)/2-h/2-20));ops.forEach(function(f){f(y0)});
c.strokeStyle='rgba(255,255,255,.2)';c.lineWidth=2;c.beginPath();c.moveTo(M,py);c.lineTo(W-M,py);c.stroke();
  c.fillStyle='#D4D0F5';c.font='500 34px'+F;c.fillText(res?'Hazlo tú, gratis:':'Pruébala gratis:',M,py+66);
  var u='fuerzabasadaenevidencia.com/'+SLUG,us=46;c.font='700 '+us+'px'+F;while(c.measureText(u).width>W-2*M&&us>26){us-=2;c.font='700 '+us+'px'+F}c.fillStyle='#fff';c.fillText(u,M,py+124);
  c.fillStyle='rgba(212,208,245,.8)';c.font='500 26px'+F;c.fillText(res?'Estimación orientativa, no un diagnóstico.':'Hecha con las fuentes que cita cada herramienta.',M,py+178);
  return cv}
function pinta(){var k=++n,fin=function(){if(k!==n)return;var cv=dibuja(),im=dl.querySelector('.comp-img'),d=dato();cv.toBlob(function(bl){if(k!==n||!bl)return;blob=bl;if(im.dataset.u)URL.revokeObjectURL(im.dataset.u);var u=URL.createObjectURL(bl);im.dataset.u=u;im.src=u},'image/png');
    im.alt=modo==='res'&&(d.vt||d.zt)?'Imagen para compartir: '+TIT+(d.s?', '+d.s:'')+(d.vt?', '+d.vt+(d.u?' '+d.u:''):'')+(d.zt?', '+d.zt:'')+'.':'Imagen para compartir: '+TIT+'. '+DESC};
  if(D.fonts&&D.fonts.load)D.fonts.load('800 74px Archivo').then(fin,fin);else fin()}
function aviso(t){var a=dl.querySelector('.comp-av');a.textContent=t;clearTimeout(aviso.t);aviso.t=setTimeout(function(){a.textContent=''},2600)}
function texto(){var d=dato();return modo==='res'&&(d.vt||d.zt)?'Mi resultado en «'+TIT+'»'+(d.s?' ('+d.s+')':'')+': '+(d.vt?d.vt+(d.u?' '+d.u:''):d.zt)+'. Hazlo tú, gratis:':TIT+': '+DESC}
function abre(){if(!dl){dl=D.createElement('dialog');dl.className='comp-d';dl.setAttribute('aria-labelledby','comp-h');
    dl.innerHTML='<div class="comp-in"><div class="comp-cab"><h2 id="comp-h">Compartir</h2><button type="button" class="comp-x" aria-label="Cerrar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>'
      +'<fieldset class="comp-op"><legend class="oculto">Qué compartir</legend><label><input type="radio" name="comp-q" value="res"><span>Con mi resultado</span></label><label><input type="radio" name="comp-q" value="herr"><span>Solo la herramienta</span></label></fieldset>'
      +'<div class="comp-prev"><img class="comp-img" alt="" width="1080" height="1350"></div>'
      +'<p class="comp-nota">Sin tu nombre, tu edad ni otros datos tuyos: solo la cifra, su zona y el enlace a la herramienta. La imagen se hace en tu dispositivo y no se sube a ningún sitio.</p>'
      +'<div class="comp-bots"><button type="button" class="btn peq comp-sh">Compartir</button><button type="button" class="comp-b2 comp-dl">Descargar imagen</button><button type="button" class="comp-b2 comp-ln">Copiar enlace</button></div><p class="comp-av" role="status"></p></div>';
    D.body.appendChild(dl);
    dl.querySelector('.comp-x').addEventListener('click',function(){dl.close()});dl.addEventListener('close',function(){b.focus()});
    dl.addEventListener('click',function(e){if(e.target===dl)dl.close()});
    dl.querySelector('.comp-op').addEventListener('change',function(e){modo=e.target.value;pinta()});
    var sh=dl.querySelector('.comp-sh');sh.hidden=!navigator.share;
    sh.addEventListener('click',function(){if(!blob)return;var f=new File([blob],'fbe-'+SLUG+'.png',{type:'image/png'}),t=texto();if(navigator.canShare&&navigator.canShare({files:[f]}))navigator.share({files:[f],title:TIT,text:t+' '+URL0}).catch(function(){});else navigator.share({title:TIT,text:t,url:URL0}).catch(function(){})});
    dl.querySelector('.comp-dl').addEventListener('click',function(){if(!blob)return;var a=D.createElement('a');a.href=dl.querySelector('.comp-img').dataset.u;a.download='fbe-'+SLUG+(modo==='res'?'-resultado':'')+'.png';D.body.appendChild(a);a.click();a.remove();aviso('Imagen descargada')});
    dl.querySelector('.comp-ln').addEventListener('click',function(){var t=URL0;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){aviso('Enlace copiado')},function(){aviso(t)})})}
  var d=dato(),hay=!!(d.vt||d.zt),ri=dl.querySelector('input[value="res"]');ri.disabled=!hay;modo=hay?'res':'herr';dl.querySelector('input[value="'+modo+'"]').checked=true;
  if(dl.showModal)dl.showModal();else dl.setAttribute('open','');pinta()}
b.addEventListener('click',abre)})();"""
for _u, _sl, _i, _t, _d in HERR_MAS:
    _parchea(_u, '</main>', '<script>' + COMP_JS.replace('__DESC__', json.dumps(_d, ensure_ascii=False)) + '</script></main>')
