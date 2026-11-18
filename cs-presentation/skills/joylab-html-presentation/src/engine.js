/* JoyLab HTML Presentation Engine V1.0 — engine.js (vanilla, 의존성 없음) */
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var slides=$$('.slide'), n=slides.length, cur=-1, stage=$('#stage');
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}

/* 16:9 고정 스테이지를 뷰포트에 맞춰 레터박스 스케일 */
function fit(){
  var s=Math.min(window.innerWidth/1920,window.innerHeight/1080);
  document.documentElement.style.setProperty('--s',String(s));
}
window.addEventListener('resize',fit);fit();

/* 목차 */
var toc=$('#toc');
slides.forEach(function(sl,i){
  var b=document.createElement('button');b.className='toc-item';b.type='button';b.dataset.i=i;
  b.innerHTML='<span>'+(i+1)+'</span><span></span><small>'+(sl.dataset.minutes||'')+'분</small>';
  b.children[1].textContent=sl.dataset.title||('슬라이드 '+(i+1));
  b.addEventListener('click',function(){go(i);setPanel('toc',false)});
  toc.appendChild(b);
});

function setPanel(name,on){
  var cls=name+'-on';
  if(on===undefined)on=!document.body.classList.contains(cls);
  document.body.classList.toggle(cls,on);
  var btn=$('#hud [data-act="'+name+'"]');if(btn)btn.setAttribute('aria-pressed',String(on));
  if(name==='notes')store('jl-notes',on?'1':'0');
}

function go(i){
  i=Math.max(0,Math.min(n-1,i));
  if(i===cur)return;
  if(cur>=0){slides[cur].classList.remove('active');slides[cur].setAttribute('aria-hidden','true')}
  cur=i;var sl=slides[cur];sl.classList.add('active');sl.removeAttribute('aria-hidden');
  $('#progress i').style.width=((cur+1)/n*100)+'%';
  var bar=$('#progress');bar.setAttribute('aria-valuenow',String(cur+1));bar.setAttribute('aria-valuemax',String(n));
  $('#hud .ctr').textContent=(cur+1)+' / '+n;
  $$('.toc-item').forEach(function(t,k){t.classList.toggle('cur',k===cur)});
  var nt=$('.notes',sl);
  $('#notes-panel p').textContent=nt?nt.textContent.trim():'(발표자 노트 없음)';
  $('#notes-panel h4').textContent='발표자 노트 · '+(cur+1)+'/'+n+' · 배정 '+(sl.dataset.minutes||'-')+'분';
  try{history.replaceState(null,'','#'+(cur+1))}catch(e){}
  document.title=(document.documentElement.dataset.deck||'JoyLab')+' · '+(cur+1)+'/'+n;
}
function next(){go(cur+1)} function prev(){go(cur-1)}

/* 전체화면 */
function fs(){
  var d=document,el=d.documentElement;
  try{
    if(!d.fullscreenElement){var p=el.requestFullscreen&&el.requestFullscreen();if(p&&p.catch)p.catch(function(){})}
    else{var q=d.exitFullscreen&&d.exitFullscreen();if(q&&q.catch)q.catch(function(){})}
  }catch(e){}
}
document.addEventListener('fullscreenchange',function(){
  var on=!!document.fullscreenElement;document.body.classList.toggle('is-fs',on);
  var b=$('#hud [data-act="fs"]');if(b)b.setAttribute('aria-pressed',String(on));
});

/* 애니메이션 ON/OFF */
function setAnim(on){
  var h=document.documentElement;h.classList.toggle('no-anim',!on);h.classList.toggle('force-anim',on);
  var b=$('#hud [data-act="anim"]');if(b){b.setAttribute('aria-pressed',String(on));b.textContent='애니메이션 '+(on?'ON':'OFF')}
  store('jl-anim',on?'1':'0');
}

/* 퀴즈 */
function answer(q,i){
  if(q.classList.contains('answered'))return;
  var ans=parseInt(q.dataset.answer,10);q.classList.add('answered');
  $$('.opt',q).forEach(function(o,k){o.disabled=true;
    if(k===ans)o.classList.add('correct'); if(k===i&&i!==ans)o.classList.add('wrong');});
  var v=$('.verdict',q);v.textContent=(i===ans)?'정답입니다.':'오답입니다. 정답은 '+['①','②','③','④'][ans]+'번입니다.';
  q.dataset.result=(i===ans)?'correct':'wrong';
}
function resetQuiz(){
  $$('.quiz').forEach(function(q){q.classList.remove('answered');delete q.dataset.result;
    $$('.opt',q).forEach(function(o){o.disabled=false;o.classList.remove('correct','wrong')});});
}
document.addEventListener('click',function(e){
  var o=e.target.closest('.opt');if(o){answer(o.closest('.quiz'),parseInt(o.dataset.i,10));return}
  var t=e.target.closest('.timer button');if(t){timer(t);return}
  var h=e.target.closest('#hud button');if(h){hud(h.dataset.act);h.blur()}
});

/* 실습 타이머 */
var tm={};
function fmt(s){var m=Math.floor(s/60),r=s%60;return (m<10?'0':'')+m+':'+(r<10?'0':'')+r}
function timer(btn){
  var box=btn.closest('.timer'),out=$('output',box),total=parseInt(box.dataset.seconds,10),act=btn.dataset.t;
  var st=tm[box.id]||(tm[box.id]={left:total,h:null});
  function stop(){if(st.h){clearInterval(st.h);st.h=null}}
  if(act==='start'){if(st.h)return;box.classList.add('run');
    st.h=setInterval(function(){st.left--;out.textContent=fmt(Math.max(0,st.left));
      if(st.left<=0){stop();box.classList.remove('run');box.classList.add('done')}},1000);}
  if(act==='pause'){stop();box.classList.remove('run')}
  if(act==='reset'){stop();st.left=total;out.textContent=fmt(total);box.classList.remove('run','done')}
}

function hud(a){
  if(a==='prev')prev(); else if(a==='next')next(); else if(a==='toc')setPanel('toc');
  else if(a==='notes')setPanel('notes'); else if(a==='fs')fs();
  else if(a==='anim')setAnim(document.documentElement.classList.contains('no-anim'));
  else if(a==='print')window.print(); else if(a==='help')setPanel('help');
}

document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  var k=e.key, inBtn=e.target.closest&&e.target.closest('button');
  if(inBtn&&(k===' '||k==='Enter'))return;
  var q=$('.quiz',slides[cur]);
  if(q&&/^[1-4]$/.test(k)){answer(q,parseInt(k,10)-1);e.preventDefault();return}
  switch(k){
    case 'ArrowRight':case 'ArrowDown':case 'PageDown':case ' ':case 'Enter':next();break;
    case 'ArrowLeft':case 'ArrowUp':case 'PageUp':case 'Backspace':prev();break;
    case 'Home':go(0);break; case 'End':go(n-1);break;
    case 'f':case 'F':fs();break; case 't':case 'T':setPanel('toc');break;
    case 'n':case 'N':setPanel('notes');break; case 'a':case 'A':hud('anim');break;
    case 'p':case 'P':window.print();break; case 'r':case 'R':resetQuiz();break;
    case '?':setPanel('help');break;
    case 'Escape':setPanel('toc',false);setPanel('notes',false);setPanel('help',false);break;
    default:return;
  }
  e.preventDefault();
});

/* 터치 스와이프 */
var tx=null;
document.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
document.addEventListener('touchend',function(e){
  if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;tx=null;
  if(Math.abs(dx)>60){dx<0?next():prev()}
},{passive:true});

/* HUD는 마우스가 움직일 때만 표시 */
var hudT=null;
document.addEventListener('mousemove',function(){
  document.body.classList.add('hud-on');clearTimeout(hudT);
  hudT=setTimeout(function(){document.body.classList.remove('hud-on')},2600);
});

/* 초기화 */
var sa=store('jl-anim');setAnim(sa===null?!window.matchMedia('(prefers-reduced-motion: reduce)').matches:sa==='1');
if(store('jl-notes')==='1')setPanel('notes',true);
var h=parseInt((location.hash||'').replace('#',''),10);
go(isNaN(h)?0:h-1);
window.addEventListener('hashchange',function(){var x=parseInt(location.hash.replace('#',''),10);if(!isNaN(x))go(x-1)});
window.JoyLab={go:go,next:next,prev:prev,count:function(){return n},current:function(){return cur},resetQuiz:resetQuiz};
})();
