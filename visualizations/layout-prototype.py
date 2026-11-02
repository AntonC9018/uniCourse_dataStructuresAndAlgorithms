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
const ease='calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"';
const transferSeconds=1.85;
function fade(from,to,duration=0.5,begin=0) {
 return `<animate attributeName="opacity" from="${from}" to="${to}" `
  +`dur="${duration}s" begin="${begin}s" ${ease} fill="freeze"/>`;
}
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
// Preserve shared glyphs; gather outgoing glyphs and grow the evaluated result in place.
function transformExpression(x,y,before,after,trace) {
 const advance=30*.602, used=new Set(), center=after.length*advance/2;
 let out='<g data-expression-transform="matching-glyphs">';
 for(let i=0;i<before.length;i++) {
  let match=-1;
  for(let j=0;j<after.length;j++) {
   if(!used.has(j) && before[i]===after[j]) {match=j;used.add(j);break;}
  }
  const destination=match<0?center:match*advance;
  out+=`<g transform="translate(${x+i*advance} ${y})">`
   +`<animateTransform attributeName="transform" type="translate" `
   +`from="${x+i*advance} ${y}" to="${x+destination} ${y}" dur="0.65s" ${ease} fill="freeze"/>`;
  out+='<g>';
  if(match<0) out+=fade(1,0,0.4)
   +`<animateTransform attributeName="transform" type="scale" from="1" to="0.15" `
   +`dur="0.45s" ${ease} fill="freeze"/>`;
  out+=colored(0,0,before[i],trace,30)+'</g></g>';
 }
 for(let j=0;j<after.length;j++) if(!used.has(j)) {
  out+=`<g transform="translate(${x+j*advance} ${y})"><g opacity="0">`
   +fade(0,1,0.4,0.25)
   +`<animateTransform attributeName="transform" type="scale" from="0.15" to="1" `
   +`begin="0.25s" dur="0.4s" ${ease} fill="freeze"/>`
   +colored(0,0,after[j],trace,30)+'</g></g>';
 }
 return out+'</g>';
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
   +`to="${g.code[3]}" dur="0.5s" ${ease} fill="freeze"/></rect>`);
 }
 out+=code;
 // Retain a fading evaluation row while the space closes, instead of removing it abruptly.
 if(move && old?.open && !evaluationOpen) {
  out+='<g>'+fade(1,0,0.35)+rect(...old.eval,'#202e42')
   +(step.write ? '' : colored(old.eval[0]+24,old.eval[1]+old.eval[3]-22,
     old.expression,trace,30))+'</g>';
 }
 trace.source.forEach((source,i)=>{
  const y=0, active=i===step.line;
  out+=`<g transform="translate(0 ${rows[i]})">`;
  if(move && old && old.rows[i]!==rows[i]) {
   out+=`<animateTransform attributeName="transform" type="translate" `
    +`from="0 ${old.rows[i]}" to="0 ${rows[i]}" dur="0.5s" ${ease} fill="freeze"/>`;
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
   +'to="1" dur="0.5s" ${ease} fill="freeze"/>';
  out+=rect(ex,ey,ew,eh,'#202e42');
  if(variant!=='A') out+=text(ex+22,ey+32,'Expression evaluation',18,'#a0afc2');
 }
 const tx=ex+24, ty=ey+eh-22;
 const copySource=move && evaluationOpen && !transfer && (!old?.open || old.line!==step.line);
 if(evaluationOpen) {
  if(transfer && step.read) {
   const [start,end]=step.read_span;
   out+=colored(tx,ty,previous.expression.slice(0,start),trace,30);
   out+='<g>'+fade(1,0,0.2,1.15)
    +colored(tx+start*30*.602,ty,previous.expression.slice(start,end),trace,30)+'</g>';
   out+=colored(tx+end*30*.602,ty,previous.expression.slice(end),trace,30);
  } else if(copySource) {
   // The code stays in place while its copy moves into the newly opened row.
   const start=trace.expression_spans[step.line][0];
   const sourceX=g.code[0]+62+start*25*.602, sourceY=rows[step.line];
   out+='<g opacity="0">'+fade(0,1,0.12,0.85)
    +colored(tx,ty,step.expression,trace,30)+'</g>';
   out+=`<g data-source-copy="expression" transform="translate(${sourceX} ${sourceY})">`
    +`<animateTransform attributeName="transform" type="translate" `
    +`from="${sourceX} ${sourceY}" to="${tx} ${ty}" begin="0.2s" dur="0.65s" `
    +`${ease} fill="freeze"/><g>`
    +`<animateTransform attributeName="transform" type="scale" from="1" to="1.2" `
    +`begin="0.2s" dur="0.65s" ${ease} fill="freeze"/>`
    +fade(1,0,0.12,0.85)+colored(0,0,step.expression,trace,25)+'</g></g>';
  } else {
   const changed=move && old?.open && old.expression!==step.expression;
   if(changed) out+=transformExpression(tx,ty,old.expression,step.expression,trace);
   else out+='<g>'+(transfer && step.write ? fade(1,0,0.25) : '')
    +colored(tx,ty,step.expression,trace,30)+'</g>';
  }
 }
 if(evaluationOpen) out+='</g>';
 trace.variables.forEach((v,i)=>{
  const [x,y,w,h]=g.slots[i], live=values[i]!==null || step.declared.includes(v.name)
   || (transfer && step.write===v.name);
  const active=step.transfer!==null && [step.read,step.write].includes(v.name);
  out+=text(x,y-16,v.address,18,live?'#a0afc2':'#697382');
  out+=text(x+w/2,y+h+34,v.name,26,live?v.color:'#697382','middle');
  out+=rect(x,y,w,h,live?'#192331':'#171d27',live?
   (active?(step.write?'#f5e58b':'#9cbaff'):v.color):'#47515f',0);
  if(live) {
   const pulse=transfer && active;
   const centerX=x+w/2, centerY=y+h/2;
   out+=`<g transform="translate(${centerX} ${centerY})"><g>`;
   if(pulse) {
    const begin=step.write ? 1.2 : 0;
    out+=`<animateTransform attributeName="transform" type="scale" `
     +`values="1;1.14;1" keyTimes="0;0.45;1" calcMode="spline" `
     +`keySplines="0.4 0 0.2 1;0.4 0 0.2 1" begin="${begin}s" dur="0.65s" fill="freeze"/>`;
   }
   if(transfer && step.write===v.name) {
    if(previous.values[i]!==null) out+='<g>'+fade(1,0,0.25)
     +text(0,11,previous.values[i],30,'#eef3fa','middle')+'</g>';
    // The arriving glyph hands off to the slot value at the exact same coordinates.
    out+='<g opacity="0">'+fade(0,1,0.2,1.55)
     +text(0,11,step.values[i],30,'#eef3fa','middle')+'</g>';
   } else out+=text(0,11,values[i]===null?'?':values[i],30,
    values[i]===null?'#a0afc2':'#eef3fa','middle');
   out+='</g></g>';
  }
 });
 if(transfer) {
  const name=step.read || step.write, vi=trace.variables.findIndex(v=>v.name===name);
  const [mx,my,mw,mh]=g.slots[vi];
  let sx,sy,dx,dy,path,arrow;
  const operand=step.read ? step.read_span[0] : 0;
  const cx=tx+(operand+String(step.transfer).length/2)*30*.602, cy=ty-11;
  // A smooth curve joins the actual glyph centers, avoiding a final positional jump.
  sx=mx+mw/2; sy=my+mh/2;
  dx=cx; dy=cy;
  if(variant==='C') {
   path=step.write ? `M ${dx} ${dy} C ${dx} ${sy+125}, ${sx} ${dy}, ${sx} ${sy}`
    : `M ${sx} ${sy} C ${sx} ${dy}, ${dx} ${sy+125}, ${dx} ${dy}`;
  } else {
   const lane=Math.max(my+mh+110,dy+70), gutter=ex+ew+65;
   // The side port passes beside the centered label below the cell.
   const port=sx+(step.write?72:-72);
   const memoryPart=`M ${sx} ${sy} C ${port} ${sy}, ${port} ${lane}, ${gutter+40} ${lane} `
    +`Q ${gutter} ${lane}, ${gutter} ${lane-40} `;
   const evalPart=`C ${gutter} ${dy+20}, ${gutter} ${dy}, ${dx} ${dy}`;
   path=step.write
    ? `M ${dx} ${dy} C ${gutter} ${dy}, ${gutter} ${dy+20}, ${gutter} ${lane-40} `
      +`Q ${gutter} ${lane}, ${gutter+40} ${lane} `
      +`C ${port} ${lane}, ${port} ${sy}, ${sx} ${sy}`
    : memoryPart+evalPart;
  }
  const color=step.write?'#f5e58b':'#9cbaff';
  arrow=`<path d="${path}" fill="none" stroke="${color}" stroke-width="3" `
   +`marker-end="url(#tip)"/>`;
  out+='<g opacity="0">'+fade(0,0.65,0.25)+fade(0.65,0,0.25,1.5)+arrow+'</g>';
  out+=`<g opacity="0">`+fade(0,1,0.18)+fade(1,0,0.2,1.55)
   +rect(-Math.max(28,String(step.transfer).length*30*.602/2+12),-25,
     Math.max(56,String(step.transfer).length*30*.602+24),50,'#192331',color,9)
   +text(0,11,step.transfer,30,'#eef3fa','middle')
   +`<animateMotion dur="1.55s" path="${path}" `
   +`keyPoints="0;1" ${ease} fill="freeze"/></g>`;
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
 previousLayout={key,rows,height:g.code[3],open:evaluationOpen,eval:g.eval,
  expression:step.expression,line:step.line};
 if(transfer) transferTimer=setTimeout(()=>draw(false,true),transferSeconds*1000);
}
function stop() {playing=false; clearTimeout(timer); $('play').textContent='Play';}
function advance(delta) {stop();index=Math.max(0,Math.min(traces[scenario].steps.length-1,index+delta));draw(true);}
function tick() {
 if(!playing)return;
 if(index===traces[scenario].steps.length-1){stop();return;}
 index++;draw(true);timer=setTimeout(tick,(traces[scenario].steps[index].transfer!==null
  ? transferSeconds+traces[scenario].steps[index].hold : traces[scenario].steps[index].hold)*1000);
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
