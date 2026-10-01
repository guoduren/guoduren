/* render hooks: deterministic frame seeking for video export */
window.RENDER=true;
window.seekTo=function(t){
  document.getElementById('start').style.transition='none';
  document.getElementById('start').classList.add('hide');
  stage.classList.remove('paused');
  let i=starts.findIndex((s,k)=>t>=s&&(k===SCENES.length-1||t<starts[k+1]));
  const local=t-starts[i];
  SCENES.forEach((s,k)=>{
    const el=document.getElementById(s.id);
    const show=(k===i)||(k===i-1&&local<0.9);
    el.style.transition='none';
    el.classList.toggle('active',show);
    el.style.zIndex=k===i?2:1;
    el.style.opacity=show?(k===i&&i>0?Math.min(1,local/0.9):1):0;
    el.style.visibility=show?'visible':'hidden';
    if(show){const at=(k===i)?local:s.dur;
      el.getAnimations({subtree:true}).forEach(a=>{a.pause();a.currentTime=at*1000})}
  });
  let txt='';
  SCENES[i].lines.forEach((L,n)=>{const end=(SCENES[i].lines[n+1]||[SCENES[i].dur-0.4])[0];if(local>=L[0]&&local<end-0.1)txt=L[1]});
  if(txt){subEl.textContent=txt;subEl.classList.add('on')}else subEl.classList.remove('on');
  subEl.style.transition='none';
  barI.style.width=(t/TOTAL*100)+'%';
};
window.TOTAL_S=TOTAL;
