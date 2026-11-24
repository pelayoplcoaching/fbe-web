// Mejoras de movimiento de la landing. Sin esto la pagina se ve entera igualmente.
(function(){
  var d=document,h=d.documentElement,w=window;
  var quieto=w.matchMedia&&w.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var hayIO='IntersectionObserver' in w;
  var prog=d.querySelector('.fx-prog i'),top=d.querySelector('.fx-top'),bot=d.querySelector('.fx-bot');
  var hero=d.querySelector('.fbe-hero'),form=d.querySelector('.fbe-form');
  var formVisible=false,pend=false;
  function mide(){
    pend=false;
    var y=w.scrollY||h.scrollTop,max=h.scrollHeight-w.innerHeight;
    if(prog)prog.style.transform='scaleX('+(max>0?Math.min(1,y/max):0)+')';
    var pasado=hero?y>hero.offsetTop+hero.offsetHeight-90:false,on=pasado&&!formVisible;
    if(top)top.classList.toggle('on',on);
    if(bot)bot.classList.toggle('on',on);
  }
  w.addEventListener('scroll',function(){if(!pend){pend=true;w.requestAnimationFrame(mide);}},{passive:true});
  w.addEventListener('resize',mide);
  if(hayIO&&form){new IntersectionObserver(function(e){formVisible=e[0].isIntersecting;mide();},{rootMargin:'-60px 0px 0px 0px'}).observe(form);}
  mide();
  if(!hayIO||quieto)return;
  h.classList.add('fx');

  var sel='.fbe-formintro,.fbe-form,.fbe-trust,.fbe-sec__head,.fbe-stat,.fbe-curve,.fbe-index li,.fbe-day,.fbe-specs span,.fbe-note,.fbe-fit,.fbe-quote,.fbe-card,.fbe-refs li,.fbe-faq details,.fbe-final,.fbe-ok__steps li,.fbe-steps li,.fbe-warn,.fbe-wk>li';
  var ver=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      var el=e.target;ver.unobserve(el);
      var n=0,p=el.previousElementSibling;
      while(p&&p.classList.contains('rv')&&n<7){n++;p=p.previousElementSibling;}
      el.style.transitionDelay=(n*70)+'ms';
      el.classList.add('in');
      setTimeout(function(){el.style.transitionDelay='';},900+n*70);
    });
  },{rootMargin:'0px 0px -8% 0px',threshold:.08});
  [].forEach.call(d.querySelectorAll(sel),function(el){el.classList.add('rv');ver.observe(el);});

  var svg=d.querySelector('.fbe-curve svg');
  if(svg){new IntersectionObserver(function(e,o){if(e[0].isIntersecting){svg.classList.add('in');o.disconnect();}},{threshold:.35}).observe(svg);}

  var cuenta=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      var el=e.target,fin=+el.getAttribute('data-n'),t0=null;cuenta.unobserve(el);
      function paso(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1100);k=1-Math.pow(1-k,3);el.textContent=Math.round(fin*k);if(k<1)w.requestAnimationFrame(paso);}
      el.textContent='0';w.requestAnimationFrame(paso);
    });
  },{threshold:.6});
  [].forEach.call(d.querySelectorAll('[data-n]'),function(el){cuenta.observe(el);});
})();

// Bloque 'Y en la semana 5?' (FBE Esencial, 24/11/2026): del 3 al 10/1/2027 ensena el enlace; despues, 'plazas cerradas'.
// Vista previa: ?esencial=abierto o ?esencial=cerrado. Si se llenan antes, poner data-lleno="1" en el bloque.
(function(){
  var q=location.search.match(/[?&]esencial=(abierto|cerrado)/);
  [].forEach.call(document.querySelectorAll('.fbe-esen[data-abre]'),function(b){
    var t=Date.now(),abre=new Date(b.getAttribute('data-abre')).getTime(),cierra=new Date(b.getAttribute('data-cierra')).getTime();
    var est=q?q[1]:(t<abre?'':(t>cierra||b.getAttribute('data-lleno')==='1'?'cerrado':'abierto'));
    if(!est)return;
    var a=b.querySelector('.fbe-esen__abierto'),c=b.querySelector('.fbe-esen__cerrado');
    if(a)a.hidden=est!=='abierto';
    if(c)c.hidden=est!=='cerrado';
    b.hidden=false;
  });
})();
