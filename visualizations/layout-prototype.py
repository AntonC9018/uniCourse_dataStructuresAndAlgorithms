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
const names = ['Bridge row','Under memory','Code above memory'];
const descriptions = [
 '1 · Bridge row: evaluation stays attached to the active line and reaches toward compact '
 + 'memory. The expression copies diagonally to the end of the row; later source lines move down.',
 '2 · Under memory: source and memory stay fixed. A bracket links the active line to a fixed '
 + 'evaluation strip; reads and writes make short vertical hops.',
 '3 · Code above memory: an inline evaluation row sits above a full-width memory band. '
 + 'Transfers run vertically through the open space beside the source; longer code scrolls.'
];
// Layout 2 (B) is the selected direction; A and C stay available for reference.
let variant = new URLSearchParams(location.search).get('variant') || 'B';
if (!variants.includes(variant)) variant='B';
let scenario=0, index=0, playing=false, timer, transferTimer, previousLayout;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',
 '"':'&quot;',"'":'&#39;'}[c]));
const mono='DejaVu Sans Mono,monospace';
const ease='calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"';
const transferTiming={prepare:0.55,travel:1.55,replace:0.2,settle:0.7};
const arrivalTime=transferTiming.prepare+transferTiming.travel;
const transferSeconds=arrivalTime+transferTiming.settle;
// Every non-transfer transition (line glide, source copy, transformation, print) ends by then.
const stepAnimationSeconds=1.05;
const charWidth=25*.602, evalWidth=30*.602;
function animateAttr(name,from,to,duration=0.45,begin=0) {
 return `<animate attributeName="${name}" from="${from}" to="${to}" `
  +`dur="${duration}s" begin="${begin}s" ${ease} fill="freeze"/>`;
}
function animated(element,animations) {
 return animations ? element.replace(/\/>$/,'>'+animations+'</'+element.match(/^<(\w+)/)[1]+'>')
  : element;
}
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
// Glyphs scale around their own centers, and the result starts growing before the old
// glyphs vanish, so the row is never empty mid-transformation.
function transformExpression(x,y,before,after,trace) {
 const used=new Set(), center=after.length*evalWidth/2, middle=-11;
 const glyph=(ch,animations)=>`<g transform="translate(${evalWidth/2} ${middle})"><g>`
  +animations+colored(-evalWidth/2,-middle,ch,trace,30)+'</g></g>';
 let out='<g data-expression-transform="matching-glyphs">';
 for(let i=0;i<before.length;i++) {
  let match=-1;
  for(let j=0;j<after.length;j++) {
   if(!used.has(j) && before[i]===after[j]) {match=j;used.add(j);break;}
  }
  const destination=match<0?center-evalWidth/2:match*evalWidth;
  out+=`<g transform="translate(${x+i*evalWidth} ${y})">`
   +`<animateTransform attributeName="transform" type="translate" `
   +`from="${x+i*evalWidth} ${y}" to="${x+destination} ${y}" dur="0.55s" `
   +`${ease} fill="freeze"/>`
   +glyph(before[i],match<0 ? fade(1,0,0.25,0.35)
    +`<animateTransform attributeName="transform" type="scale" from="1" to="0.45" `
    +`dur="0.55s" ${ease} fill="freeze"/>` : '')+'</g>';
 }
 for(let j=0;j<after.length;j++) if(!used.has(j)) {
  out+=`<g transform="translate(${x+j*evalWidth} ${y})" opacity="0">`+fade(0,1,0.2,0.2)
   +glyph(after[j],`<animateTransform attributeName="transform" type="scale" from="0.3" `
    +`to="1" begin="0.2s" dur="0.45s" ${ease} fill="freeze"/>`)+'</g>';
 }
 return out+'</g>';
}
function geometry(evaluationOpen) {
 const count=traces[scenario].variables.length;
 const slots=(x,y)=>traces[scenario].variables.map((_,i)=>[x+i*112,y,112,64]);
 const height=48+traces[scenario].source.length*58;
 if (variant==='A') return {code:[40,60,560,height+(evaluationOpen?88:0)], line:58, cy:112,
  gap:evaluationOpen?88:0, eval:[100,132+indexLine()*58,600,64], tx:600,
  slots:slots(720,230)};
 // B centers the composition vertically; output sits right under evaluation.
 if (variant==='B') return {code:[40,160,520,height], line:58, cy:212,
  eval:[640,392,540,88], tx:688, slots:slots(660,236), tether:true, copyBend:610,
  port:50, output:[664,544], printFromEvaluation:true};
 const scroll=Math.max(0,indexLine()-3)*58;
 return {code:[40,28,1200,410], line:58, cy:86-scroll, gap:evaluationOpen?88:0,
  eval:[100,106+indexLine()*58-scroll,1080,64], tx:560,
  slots:slots((1280-count*112)/2,520), viewport:true};
}
function indexLine() { return traces[scenario].steps[index].line; }
function spanBox(trace,g,line,y) {
 const [start,end]=trace.expression_spans[line];
 return [g.code[0]+62+start*charWidth-3,y-30,(end-start)*charWidth+6,40];
}
function tetherPath(g,y) {
 const [ex,ey,,eh]=g.eval;
 return `M ${g.code[0]+g.code[2]+5} ${y-10} H ${g.copyBend} V ${ey+eh/2} H ${ex}`;
}
// Export and scenario starts behave as if the page had just shown an empty, settled layout.
function resetLayout() {
 const g=geometry(variant==='B');
 previousLayout={key:variant+scenario, open:variant==='B', height:g.code[3],
  rows:traces[scenario].source.map((_,i)=>g.cy+i*g.line), eval:g.eval, expression:'', tx:g.tx};
}
function draw(animate=false, shift=false) {
 clearTimeout(transferTimer);
 const trace=traces[scenario], step=trace.steps[index];
 const previous=trace.steps[Math.max(0,index-1)];
 const transfer=animate && step.transfer!==null;
 // A result remains visible until consumed, including during a write animation.
 const evaluationOpen=variant==='B' || Boolean(step.expression &&
  (transfer || (!step.write && !step.stdout)));
 const g=geometry(evaluationOpen), key=variant+scenario;
 const old=previousLayout?.key===key ? previousLayout : null;
 const move=animate || shift;
 const rows=trace.source.map((_,i)=>g.cy+i*g.line+(i>step.line?(g.gap || 0):0));
 const values=transfer && step.write ? previous.values : step.values;
 const lineChanged=move && old?.rows && old.line!==undefined && old.line!==step.line;
 const output=g.output || [62,687];
 const printing=g.printFromEvaluation && move && step.stdout && old?.stdout!==step.stdout;
 // In B the strip persists, so a written or printed result must leave it explicitly.
 const consumed=variant==='B' && !transfer && Boolean(step.write || step.stdout);
 let out='<defs><marker id="tip" markerWidth="10" markerHeight="10" refX="8" refY="5" '
  +'orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L10 5 L0 10" '
  +'fill="context-stroke"/></marker></defs>';
 let code=rect(...g.code);
 if(move && old && old.height!==g.code[3]) {
  code=animated(code,animateAttr('height',old.height,g.code[3],0.5));
 }
 out+=code;
 // Retain a fading evaluation row while the space closes, instead of removing it abruptly.
 if(move && old?.open && !evaluationOpen) {
  out+='<g>'+fade(1,0,0.35)+rect(...old.eval,'#202e42')
   +(step.write ? '' : colored(old.tx,old.eval[1]+old.eval[3]-22,
     old.expression,trace,30))+'</g>';
 }
 if(g.viewport) out+='<defs><clipPath id="code-viewport">'
  +rect(...g.code)+'</clipPath></defs><g clip-path="url(#code-viewport)">';
 // The active-line stripe and span highlight glide between lines instead of jumping.
 {
  const y=rows[step.line], box=spanBox(trace,g,step.line,y);
  let stripe=rect(g.code[0]+8,y-32,4,44,step.write?'#f5e58b':'#9cbaff','none',0);
  let span=rect(...box,'#2e4059','none',6);
  if(lineChanged) {
   const oldY=old.rows[old.line], oldBox=spanBox(trace,g,old.line,oldY);
   stripe=animated(stripe,animateAttr('y',oldY-32,y-32));
   span=animated(span,animateAttr('x',oldBox[0],box[0])+animateAttr('y',oldBox[1],box[1])
    +animateAttr('width',oldBox[2],box[2]));
  }
  out+='<g data-active-line="highlight">'+stripe+span+'</g>';
 }
 trace.source.forEach((source,i)=>{
  out+=`<g transform="translate(0 ${rows[i]})">`;
  if(move && old && old.rows[i]!==rows[i]) {
   out+=`<animateTransform attributeName="transform" type="translate" `
    +`from="0 ${old.rows[i]}" to="0 ${rows[i]}" dur="0.5s" ${ease} fill="freeze"/>`;
  }
  out+=text(g.code[0]+22,0,i+1,18,'#a0afc2');
  out+=colored(g.code[0]+62,0,source,trace);
  out+='</g>';
 });
 if(g.viewport) out+='</g>';
 let tether;
 if(g.tether) {
  tether=tetherPath(g,rows[step.line]);
  out+=animated(`<path data-code-tether="bracket" d="${tether}" `
   +`fill="none" stroke="#697d99" stroke-width="2"/>`,
   lineChanged && old.tether ? animateAttr('d',old.tether,tether) : '');
 }
 if(variant==='C') out+=rect(40,488,1200,158,'#141e2b');
 let [ex,ey,ew,eh]=g.eval;
 if(evaluationOpen) {
  out+='<g data-evaluation="open">';
  if(move && old && !old.open) out+=fade(0,1,0.5);
  out+=rect(ex,ey,ew,eh,'#202e42');
  if(variant==='B') out+=text(ex+ew-16,ey+24,'Expression evaluation',16,'#a0afc2','end');
 }
 const tx=g.tx, ty=ey+eh-22;
 const copySource=move && evaluationOpen && !transfer && (!old?.open || old.line!==step.line);
 if(evaluationOpen) {
  if(transfer && step.read) {
   const [start,end]=step.read_span;
   out+=colored(tx,ty,previous.expression.slice(0,start),trace,30);
   // Preparation links the operand to its memory cell before the copy departs.
   out+='<g data-read-highlight="operand" opacity="0">'+fade(0,1,0.15)
    +fade(1,0,transferTiming.replace,arrivalTime)
    +rect(tx+start*evalWidth-8,ty-34,(end-start)*evalWidth+16,46,'none','#9cbaff',6)
    +'</g>';
   out+='<g data-replacement-old="operand">'+fade(1,0,transferTiming.replace,arrivalTime)
    +colored(tx+start*evalWidth,ty,previous.expression.slice(start,end),trace,30)+'</g>';
   out+='<g data-replacement-new="operand" opacity="0">'
    +fade(0,1,transferTiming.replace,arrivalTime)
    +colored(tx+start*evalWidth,ty,String(step.transfer),trace,30)+'</g>';
   out+=colored(tx+end*evalWidth,ty,previous.expression.slice(end),trace,30);
  } else if(transfer && step.write) {
   // The result is outlined with its destination, then hands off to the moving box.
   const width=step.expression.length*evalWidth;
   out+='<g data-write-source="result">'+fade(1,0,0.12,transferTiming.prepare)
    +colored(tx,ty,step.expression,trace,30)
    +'<g opacity="0">'+fade(0,1,0.15)
    +rect(tx-8,ty-34,width+16,46,'none','#f5e58b',6)+'</g></g>';
  } else if(copySource) {
   // The highlighted span lifts off as a boxed copy and follows the bracket into the strip;
   // the source line stays intact underneath. The copy itself becomes the evaluation text.
   const start=trace.expression_spans[step.line][0];
   const sourceX=g.code[0]+62+start*charWidth, sourceY=rows[step.line];
   const begin=lineChanged ? 0.3 : 0.15, travel=0.6, total=begin+travel;
   const path=g.copyBend
    ? `M ${sourceX} ${sourceY} C ${g.copyBend} ${sourceY}, ${g.copyBend} ${ty}, ${tx} ${ty}`
    : `M ${sourceX} ${sourceY} L ${tx} ${ty}`;
   const width=step.expression.length*charWidth;
   out+=`<g data-source-copy="expression">`
    +`<animateMotion dur="${total}s" path="${path}" keyPoints="0;0;1" `
    +`keyTimes="0;${(begin/total).toFixed(4)};1" calcMode="spline" `
    +`keySplines="0 0 1 1;0.4 0 0.2 1" fill="freeze"/><g>`
    +`<animateTransform attributeName="transform" type="scale" from="1" to="1.2" `
    +`begin="${begin}s" dur="${travel}s" ${ease} fill="freeze"/>`
    +'<g opacity="0">'+fade(0,1,0.15,begin-0.15)+fade(1,0,0.12,total)
    +`<rect x="-5" y="-29" width="${width+10}" height="38" rx="6" fill="#2e4059" `
    +`stroke="#9cbaff" stroke-width="2"/></g>`
    +colored(0,0,step.expression,trace,25)+'</g></g>';
  } else if(consumed) {
   if(printing) {
    // The printed value leaves evaluation and settles after the output label.
    out+='<g>'+fade(1,0,0.12,0.2)+colored(tx,ty,step.expression,trace,30)+'</g>';
   }
  } else {
   const changed=move && !transfer && old?.open && old.expression!==step.expression;
   if(changed) out+=transformExpression(tx,ty,old.expression,step.expression,trace);
   else out+=colored(tx,ty,step.expression,trace,30);
  }
 }
 if(evaluationOpen) out+='</g>';
 trace.variables.forEach((v,i)=>{
  const [x,y,w,h]=g.slots[i], live=values[i]!==null || step.declared.includes(v.name)
   || (transfer && step.write===v.name);
  // Only the transfer itself highlights memory; the border settles back after arrival.
  const active=transfer && [step.read,step.write].includes(v.name);
  const highlight=step.write?'#f5e58b':'#9cbaff';
  out+=text(x,y-16,v.address,18,live?'#a0afc2':'#697382');
  out+=text(x+w/2,y+h+34,v.name,26,live?v.color:'#697382','middle');
  out+=animated(rect(x,y,w,h,live?'#192331':'#171d27',live?
   (active?highlight:v.color):'#47515f',0),
   active ? `<animate attributeName="stroke" from="${highlight}" to="${v.color}" `
    +`begin="${arrivalTime+0.15}s" dur="0.35s" fill="freeze"/>` : '');
  if(live) {
   const centerX=x+w/2, centerY=y+h/2;
   out+=`<g transform="translate(${centerX} ${centerY})"><g>`;
   if(active) {
    const begin=step.write ? arrivalTime-0.2 : 0;
    out+=`<animateTransform attributeName="transform" type="scale" `
     +`values="1;1.14;1" keyTimes="0;0.45;1" calcMode="spline" `
     +`keySplines="0.4 0 0.2 1;0.4 0 0.2 1" begin="${begin}s" dur="0.65s" fill="freeze"/>`;
   }
   if(transfer && step.write===v.name) {
    if(previous.values[i]!==null) out+='<g data-replacement-old="memory">'
     +fade(1,0,transferTiming.replace,arrivalTime)
     +text(0,11,previous.values[i],30,'#eef3fa','middle')+'</g>';
    // The arriving glyph hands off to the slot value at the exact same coordinates.
    out+='<g data-replacement-new="memory" opacity="0">'
     +fade(0,1,transferTiming.replace,arrivalTime)
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
  const cx=tx+(operand+String(step.transfer).length/2)*evalWidth, cy=ty-11;
  // A smooth curve joins the actual glyph centers, avoiding a final positional jump.
  sx=mx+mw/2; sy=my+mh/2;
  dx=cx; dy=cy;
  let readPath,writePath;
  if(variant==='A') {
   // Route beside the names, through the short gap at the end of the bridge.
   const above=dy<sy, lane=above?my-48:my+mh+64;
   const port=above?sx:sx+(step.write?36:-36);
   readPath=`M ${sx} ${sy} C ${port} ${sy}, ${port} ${lane}, 710 ${lane} `
    +`C 680 ${lane}, 680 ${dy}, ${dx} ${dy}`;
   writePath=`M ${dx} ${dy} C 680 ${dy}, 680 ${lane}, 710 ${lane} `
    +`C ${port} ${lane}, ${port} ${sy}, ${sx} ${sy}`;
  } else if(variant==='B') {
   // Names sit below memory; side ports keep the boxed value clear of their glyphs.
   const port=sx+(step.write?g.port:-g.port), middle=(my+mh+dy)/2;
   readPath=`M ${sx} ${sy} C ${port} ${sy}, ${port} ${middle}, ${port} ${middle} `
    +`C ${port} ${dy}, ${dx} ${middle}, ${dx} ${dy}`;
   writePath=`M ${dx} ${dy} C ${dx} ${middle}, ${port} ${dy}, ${port} ${middle} `
    +`C ${port} ${middle}, ${port} ${sy}, ${sx} ${sy}`;
  } else {
   // The centered memory band aligns with the evaluation work area beside the code.
   const middle=(sy+dy)/2;
   readPath=`M ${sx} ${sy} C ${sx} ${middle}, ${dx} ${middle}, ${dx} ${dy}`;
   writePath=`M ${dx} ${dy} C ${dx} ${middle}, ${sx} ${middle}, ${sx} ${sy}`;
  }
  path=step.write?writePath:readPath;
  const color=step.write?'#f5e58b':'#9cbaff';
  arrow=`<path d="${path}" fill="none" stroke="${color}" stroke-width="3" `
   +`marker-end="url(#tip)"/>`;
  out+='<g opacity="0">'+fade(0,0.65,0.25,transferTiming.prepare)
   +fade(0.65,0,0.25,arrivalTime)+arrow+'</g>';
  out+=valueBox(name,step.transfer,color,path,transferTiming.prepare,transferTiming.travel,
   arrivalTime);
 }
 if(step.stdout) {
  const [ox,oy]=output, label='Output: ';
  if(g.printFromEvaluation) {
   const vx=ox+label.length*26*.602, width=step.stdout.length*evalWidth;
   out+='<g>'+(printing?'<g opacity="0">'+fade(0,1,0.25):'<g>')
    +text(ox,oy,label,26,'#a0afc2')+'</g>';
   if(printing) {
    const path=`M ${tx+width/2} ${ty-11} C ${tx+width/2} ${oy-30}, ${vx+width/2} ${ty+20}, `
     +`${vx+width/2} ${oy-11}`;
    out+=valueBox('stdout',step.stdout,'#a0afc2',path,0.2,0.6,0.8);
    out+='<g opacity="0">'+fade(0,1,0.15,0.8)+text(vx,oy,step.stdout,30)+'</g>';
   } else out+=text(vx,oy,step.stdout,30);
   out+='</g>';
  } else out+=text(ox,oy,label+step.stdout,26);
 }
 $('stage').innerHTML=out;
 $('description').textContent=descriptions[variants.indexOf(variant)];
 $('variantName').textContent=variant+' · '+names[variants.indexOf(variant)];
 $('scrub').max=trace.steps.length-1; $('scrub').value=index;
 $('count').textContent=`${index+1} / ${trace.steps.length}`;
 $('state').textContent=trace.variables.map((v,i)=>v.name+' = '+(step.values[i]===null?
  (step.declared.includes(v.name)?'uninitialized':'unallocated'):step.values[i])).join(' · ')
  +' · expression: '+step.expression+(step.stdout?' · output: '+step.stdout:'');
 previousLayout={key,rows,height:g.code[3],open:evaluationOpen,eval:g.eval,
  expression:consumed?'':step.expression,line:step.line,tx,tether,stdout:step.stdout};
 if(transfer) transferTimer=setTimeout(()=>draw(false,true),transferSeconds*1000);
}
// A boxed value fades in at departure, travels along the route, and vanishes on arrival.
function valueBox(name,value,color,path,begin,travel,arrival) {
 const width=String(value).length*evalWidth;
 return `<g data-transfer-value="${name}" opacity="0">`
  +fade(0,1,0.12,begin)+fade(1,0,transferTiming.replace,arrival)
  +rect(-Math.max(28,width/2+12),-25,Math.max(56,width+24),50,'#192331',color,9)
  +text(0,11,value,30,'#eef3fa','middle')
  +`<animateMotion begin="${begin}s" dur="${travel}s" path="${path}" `
  +`keyPoints="0;1" ${ease} fill="freeze"/></g>`;
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
$('scenario').onchange=e=>{stop();scenario=Number(e.target.value);index=0;resetLayout();draw();};
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
