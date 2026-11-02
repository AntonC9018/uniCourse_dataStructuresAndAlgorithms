"""Throwaway layout comparison for #57, using the existing manual traces.

Three variants on one page, switchable with ?variant=A, B, or C.
Run from the course root: python3 visualizations/layout-prototype.py.
"""
from dataclasses import asdict
import json
from pathlib import Path

from model import TIMELINES

PAGE = r'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Expression layout alternatives</title>
<style>
:root {color-scheme:dark; font-family:var(--font-sans,system-ui); color:var(--foreground,#eef3fa)}
body {margin:0; padding-bottom:76px}
button,select {font:inherit; color:inherit; background:var(--secondary,#233044);
 border:1px solid var(--border,#47515f); border-radius:8px; padding:8px 12px; cursor:pointer}
button:focus-visible,select:focus-visible,input:focus-visible {outline:3px solid #9cbaff}
button[aria-pressed=true] {border-color:#9cbaff; background:#2e4059}
p {line-height:1.5; margin:10px 0; color:var(--muted-foreground,#a0afc2)}
.controls {display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:12px 0}
svg {display:block; width:100%; background:#101722; border-radius:12px}
input[type=range] {flex:1; min-width:120px; accent-color:#9cbaff}
#switcher {position:fixed; bottom:12px; left:50%; transform:translateX(-50%);
 display:flex; align-items:center; gap:8px; padding:8px; border-radius:14px;
 background:var(--popover,#192331); border:1px solid var(--border,#47515f);
 box-shadow:0 4px 20px #0007; white-space:nowrap}
#variantName {font-size:14px; min-width:155px; text-align:center}
#state {font-family:var(--font-mono,monospace); font-size:13px; min-height:36px}
</style>
<p>Three layout studies · same expression and failed-swap traces · grey storage until allocation.</p>
<div class="controls">
 <label>Example <select id="scenario"><option value="0">Expression</option>
 <option value="1">Failed swap</option></select></label>
 <button id="play">Play</button><button id="back" aria-label="Previous step">← Step</button>
 <button id="next" aria-label="Next step">Step →</button>
 <input id="scrub" aria-label="Trace step" type="range" min="0" value="0">
 <span id="count"></span>
</div>
<svg id="stage" viewBox="0 0 1280 720" role="img" aria-label="Code evaluation and memory"></svg>
<p id="description"></p><div id="state" aria-live="polite"></div>
<nav id="switcher" aria-label="Layout variant">
 <button id="prevVariant" aria-label="Previous layout">←</button>
 <span id="variantName"></span>
 <button id="nextVariant" aria-label="Next layout">→</button>
</nav>
<script>
const traces = __TRACES__;
const variants = ['A','B','C'];
const names = ['Inline evaluation','Central workspace','Memory first'];
const descriptions = [
 'A · Open a temporary evaluation row beneath the active line. Later lines move down '
 + 'while evaluating, then close up after the value is stored or printed. Memory stays fixed.',
 'B · Code → evaluation → memory. A fixed central workspace gives reads and writes '
 + 'short routes. Three columns leave less room for long code or large memory layouts.',
 'C · Memory spans the top; code and evaluation sit below. More horizontal room for '
 + 'contiguous storage, with vertical read/write paths. The eye travels between two levels.'
];
let variant = new URLSearchParams(location.search).get('variant') || 'A';
if (!variants.includes(variant)) variant='A';
let scenario=0, index=0, playing=false, timer, transferTimer, previousLayout;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',
 '"':'&quot;',"'":'&#39;'}[c]));
const mono='DejaVu Sans Mono,monospace';
function text(x,y,value,size=26,color='#eef3fa',anchor='start') {
 return `<text x="${x}" y="${y}" font-family="${mono}" font-size="${size}" `
 + `fill="${color}" text-anchor="${anchor}" xml:space="preserve">${esc(value)}</text>`;
}
function rect(x,y,w,h,fill='#192331',stroke='none',radius=8) {
 return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" `
 + `fill="${fill}" stroke="${stroke}" stroke-width="3"/>`;
}
function colored(x,y,value,trace,size=25) {
 let out='';
 for (const token of value.split(/(\b[a-zA-Z_]\w*\b)/)) {
  out+=text(x,y,token,size,trace.variables.find(v=>v.name===token)?.color || '#eef3fa');
  x+=token.length*size*.602;
 }
 return out;
}
function geometry(evaluationOpen) {
 if (variant==='A') return {code:[40,60,550,48+traces[scenario].source.length*58
   +(evaluationOpen?88:0)], line:58, cy:112, gap:evaluationOpen?88:0,
  eval:[100,132+indexLine()*58,440,64], slots:[[710,140,224,64],[934,140,224,64]]};
 if (variant==='B') return {code:[28,70,435,480], line:86, cy:145,
  eval:[488,255,270,120], slots:[[792,265,224,64],[1016,265,224,64]]};
 return {code:[40,292,560,350], line:66, cy:350,
  eval:[692,350,520,150], slots:[[430,112,224,64],[654,112,224,64]]};
}
function indexLine() { return traces[scenario].steps[index].line; }
function draw(animate=false, shift=false) {
 clearTimeout(transferTimer);
 const trace=traces[scenario], step=trace.steps[index];
 const previous=trace.steps[Math.max(0,index-1)];
 const transfer=animate && step.transfer!==null;
 // A result remains visible until consumed, including during a write animation.
 const evaluationOpen=variant!=='A' || Boolean(step.expression &&
  (transfer || (!step.write && !step.stdout)));
 const g=geometry(evaluationOpen), key=variant+scenario;
 const old=previousLayout?.key===key ? previousLayout : null;
 const move=animate || shift;
 const rows=trace.source.map((_,i)=>g.cy+i*g.line+(i>step.line?(g.gap || 0):0));
 const values=transfer && step.write ? previous.values : step.values;
 let out='<defs><marker id="tip" markerWidth="10" markerHeight="10" refX="8" refY="5" '
  +'orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L10 5 L0 10" '
  +'fill="context-stroke"/></marker></defs>';
 let code=rect(...g.code);
 if(move && old && old.height!==g.code[3]) {
  code=code.replace('/>',`><animate attributeName="height" from="${old.height}" `
   +`to="${g.code[3]}" dur="0.22s" fill="freeze"/></rect>`);
 }
 out+=code;
 trace.source.forEach((source,i)=>{
  const y=0, active=i===step.line;
  out+=`<g transform="translate(0 ${rows[i]})">`;
  if(move && old && old.rows[i]!==rows[i]) {
   out+=`<animateTransform attributeName="transform" type="translate" `
    +`from="0 ${old.rows[i]}" to="0 ${rows[i]}" dur="0.22s" fill="freeze"/>`;
  }
  if(active) out+=rect(g.code[0]+8,y-32,4,44,step.write?'#f5e58b':'#9cbaff','none',0);
  out+=text(g.code[0]+22,y,i+1,18,'#a0afc2');
  if(active) {
   const [start,end]=trace.expression_spans[i];
   out+=rect(g.code[0]+62+start*25*.602-3,y-30,(end-start)*25*.602+6,40,'#2e4059');
  }
  out+=colored(g.code[0]+62,y,source,trace);
  out+='</g>';
 });
 let [ex,ey,ew,eh]=g.eval;
 if(evaluationOpen) {
  out+='<g data-evaluation="open">';
  if(move && old && !old.open) out+='<animate attributeName="opacity" from="0" '
   +'to="1" dur="0.22s" fill="freeze"/>';
  out+=rect(ex,ey,ew,eh,'#202e42');
  if(variant!=='A') out+=text(ex+22,ey+32,'Expression evaluation',18,'#a0afc2');
 }
 const tx=ex+24, ty=ey+eh-22;
 if(evaluationOpen && !(transfer && step.write)) {
  out+=colored(tx,ty,transfer && step.read ? previous.expression : step.expression,trace,30);
 }
 if(evaluationOpen) out+='</g>';
 trace.variables.forEach((v,i)=>{
  const [x,y,w,h]=g.slots[i], live=values[i]!==null || step.declared.includes(v.name)
   || (transfer && step.write===v.name);
  const active=step.transfer!==null && [step.read,step.write].includes(v.name);
  out+=text(x,y-48,v.address,18,live?'#a0afc2':'#697382');
  out+=text(x+w/2,y-18,v.name,26,live?v.color:'#697382','middle');
  out+=rect(x,y,w,h,live?'#192331':'#171d27',live?
   (active?(step.write?'#f5e58b':'#9cbaff'):v.color):'#47515f',0);
  if(live && !(transfer && step.write===v.name)) out+=text(x+w/2,y+43,
   values[i]===null?'?':values[i],30,values[i]===null?'#a0afc2':'#eef3fa','middle');
 });
 if(transfer) {
  const name=step.read || step.write, vi=trace.variables.findIndex(v=>v.name===name);
  const [mx,my,mw,mh]=g.slots[vi];
  let sx,sy,dx,dy,path,arrow;
  const operand=step.read ? step.read_span[0] : 0;
  const cx=tx+(operand+String(step.transfer).length/2)*30*.602, cy=ty-11;
  if(variant==='C') {
   sx=mx+mw/2; sy=my+mh+18; dx=cx; dy=ey-16;
   path=`M ${sx} ${sy} C ${sx} ${sy+90}, ${dx} ${dy-90}, ${dx} ${dy}`;
  } else {
   sx=mx+mw/2; sy=my+mh+18; dx=ex+ew+16; dy=cy;
   // A bottom lane clears all contiguous memory cells and their labels.
   const lane=Math.max(my+mh+70,dy+70);
   path=`M ${sx} ${sy} L ${sx} ${lane} `
    +`L ${dx+25} ${lane} Q ${dx} ${lane} ${dx} ${dy}`;
  }
  if(step.write) {
   // Reversing the SVG path changes direction without duplicating a stationary result.
   const temp=document.createElementNS('http://www.w3.org/2000/svg','path');
   temp.setAttribute('d',path);
   const length=temp.getTotalLength(), points=[];
   for(let t=1;t>=0;t-=1/80) { const p=temp.getPointAtLength(t*length);points.push(`${p.x} ${p.y}`); }
   const p=temp.getPointAtLength(0);points.push(`${p.x} ${p.y}`);
   path='M '+points.join(' L ');
  }
  const color=step.write?'#f5e58b':'#9cbaff';
  arrow=`<path d="${path}" fill="none" stroke="${color}" stroke-width="3" `
   +`marker-end="url(#tip)"/>`;
  out+=arrow;
  out+=`<g><rect x="-28" y="-24" width="56" height="44" rx="8" fill="#101722"/>`
   +text(0,10,step.transfer,30,color,'middle')
   +`<animateMotion dur="0.9s" path="${path}" fill="freeze"/></g>`;
 }
 if(step.stdout) out+=text(62,687,'Output: '+step.stdout,26);
 $('stage').innerHTML=out;
 $('description').textContent=descriptions[variants.indexOf(variant)];
 $('variantName').textContent=variant+' · '+names[variants.indexOf(variant)];
 $('scrub').max=trace.steps.length-1; $('scrub').value=index;
 $('count').textContent=`${index+1} / ${trace.steps.length}`;
 $('state').textContent=trace.variables.map((v,i)=>v.name+' = '+(step.values[i]===null?
  (step.declared.includes(v.name)?'uninitialized':'unallocated'):step.values[i])).join(' · ')
  +' · expression: '+step.expression+(step.stdout?' · output: '+step.stdout:'');
 previousLayout={key,rows,height:g.code[3],open:evaluationOpen};
 if(transfer) transferTimer=setTimeout(()=>draw(false,true),1000);
}
function stop() {playing=false; clearTimeout(timer); $('play').textContent='Play';}
function advance(delta) {stop();index=Math.max(0,Math.min(traces[scenario].steps.length-1,index+delta));draw(true);}
function tick() {
 if(!playing)return;
 if(index===traces[scenario].steps.length-1){stop();return;}
 index++;draw(true);timer=setTimeout(tick,1800);
}
$('play').onclick=()=>{
 if(playing){stop();return;}
 if(index===traces[scenario].steps.length-1)index=0;
 playing=true;$('play').textContent='Pause';draw();timer=setTimeout(tick,1000);
};
$('next').onclick=()=>advance(1); $('back').onclick=()=>advance(-1);
$('scrub').oninput=e=>{stop();index=Number(e.target.value);draw();};
$('scenario').onchange=e=>{stop();scenario=Number(e.target.value);index=0;draw();};
function changeVariant(delta) {
 variant=variants[(variants.indexOf(variant)+delta+3)%3];
 const url=new URL(location.href);url.searchParams.set('variant',variant);
 try { history.replaceState(null,'',url); } catch (error) {
  if(error.name!=='SecurityError') throw error;
 }
 draw();
}
$('prevVariant').onclick=()=>changeVariant(-1);$('nextVariant').onclick=()=>changeVariant(1);
document.addEventListener('keydown',e=>{
 if(e.target.closest('input,textarea,select,[contenteditable]'))return;
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();changeVariant(e.key==='ArrowLeft'?-1:1);}
});
draw();
</script>
</html>'''

if __name__ == '__main__':
    target = Path(__file__).with_name('layout-prototype.html')
    target.write_text(PAGE.replace('__TRACES__', json.dumps([asdict(t) for t in TIMELINES])))
    print(target)
