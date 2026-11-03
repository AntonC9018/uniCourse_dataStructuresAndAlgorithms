"""THROWAWAY: three control layouts inside a course lesson, ?variant=A/B/C.

Run: python3 visualizations/website-controls-prototype.py
Uses the existing SVG animation/export renderer, with a pausable browser clock.
Keep on the visualization prototype branch until a control design is selected.
"""
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path

from model import TIMELINES

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location('layout_prototype', ROOT / 'layout-prototype.py')
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)

BRIDGE = r'''<style>
html,body{margin:0!important;padding:0!important;overflow:hidden;background:#101722}
body>*{display:none!important}body>#stage{display:block!important;width:100%;height:auto;aspect-ratio:16/9;border-radius:0}
[data-source-line]{cursor:pointer;outline:none}
[data-source-line]:hover{fill:#9cbaff;fill-opacity:.1}
[data-source-line]:focus-visible{stroke:#9cbaff;stroke-width:2}
</style><script>
// The export renderer owns every glyph, path and expression transformation. This
// adapter replaces its wall-clock scheduling with one pausable SVG timeline.
stop(); clearTimeout(transferTimer); variant='B'; scenario=0; index=0;
let running=false, continuous=false, elapsed=0, duration=0, rate=1, last=0, announced=0, pristine=true;
function currentStage(){return document.getElementById('stage')}
function freeze(t){currentStage().pauseAnimations();currentStage().setCurrentTime(t)}
// Add interaction targets without changing the shared export renderer.
const drawScene=draw;
draw=function(...args){
 drawScene(...args);
 const g=geometry(true),svg=currentStage();
 svg.setAttribute('role','group');
 traces[scenario].source.forEach((source,line)=>{
  const hit=document.createElementNS(svg.namespaceURI,'rect');
  for(const [key,value] of Object.entries({x:g.code[0]+12,y:g.cy+line*g.line-34,
    width:g.code[2]-24,height:48,fill:'transparent',tabindex:0,role:'button',
    'data-source-line':line,'aria-label':'Jump to line '+(line+1)+': '+source}))
   hit.setAttribute(key,value);
  svg.append(hit);
 });
};
function describeStep(step,i){
 if(step.transfer!==null)return step.write?'Store '+step.transfer+' in '+step.write:'Copy '+step.read+' into the expression';
 if(step.stdout)return 'Print '+JSON.stringify(step.stdout);
 if(i && traces[scenario].steps[i-1].line===step.line)return 'Evaluate → '+step.expression;
 return 'Begin '+traces[scenario].source[step.line];
}
function snapshot(){
 const trace=traces[scenario], step=trace.steps[index], previous=trace.steps[Math.max(0,index-1)];
 const transferring=step.transfer!==null && elapsed<transferArrivalTime(step);
 const values=step.write && transferring?previous.values:step.values;
 return {kind:'course-player',scenario,index,running,continuous,speed:rate,time:elapsed,duration,
  phase:elapsed>=duration?'Settled':step.transfer!==null?(elapsed<transferDepartureTime(step)?'Prepare':elapsed<transferArrivalTime(step)?'Move':'Settle'):'Animate',
  source:trace.source,steps:trace.steps.map((s,i)=>({line:s.line,label:describeStep(s,i)})),
  line:step.line,expression:step.read && transferring?previous.expression:step.expression,action:describeStep(step,index),
  memory:trace.variables.map((v,i)=>({name:v.name,address:v.address,value:values[i]})),
  stdout:step.stdout!==previous.stdout && elapsed<0.8?previous.stdout:step.stdout};
}
function publish(){parent.postMessage(snapshot(),'*')}
function settle(i){
 running=false;continuous=false;index=Math.max(0,Math.min(traces[scenario].steps.length-1,i));
 resetLayout();draw(false);clearTimeout(transferTimer);duration=stepSeconds(index);elapsed=duration;
 freeze(duration);last=performance.now();publish();
}
function start(i,autoplay=false){
 continuous=autoplay;running=false;
 if(i>0){index=i-1;resetLayout();draw(false);clearTimeout(transferTimer);freeze(100)}
 else {index=0;resetLayout()}
 index=i;draw(true);clearTimeout(transferTimer);elapsed=0;duration=stepSeconds(i);freeze(0);
 pristine=false;running=true;last=performance.now();publish();
}
window.coursePlayer={
 state:snapshot,
 next(){if(index<traces[scenario].steps.length-1)start(index+1)},
 back(){pristine=false;settle(index-1)},
 jump(i){pristine=false;settle(i)},
 line(line){
  const i=traces[scenario].steps.findIndex(step=>step.line===Number(line));
  if(i>=0){pristine=false;settle(i)}
 },
 replay(){start(index)},
 reset(){pristine=true;settle(0)},
 play(){
  if(running){running=false;last=performance.now();publish();return}
  continuous=true;
  if(pristine || index===traces[scenario].steps.length-1 && elapsed>=duration)start(0,true);
  else if(elapsed>=duration)start(index+1,true);
  else {running=true;last=performance.now();publish()}
 },
 speed(value){rate=Number(value);last=performance.now();publish()},
 example(value){scenario=Number(value);pristine=true;settle(0)}
};
currentStage().addEventListener('click',e=>{
 const hit=e.target.closest('[data-source-line]');
 if(hit)window.coursePlayer.line(hit.dataset.sourceLine);
});
document.addEventListener('keydown',e=>{
 const hit=e.target.closest('[data-source-line]');
 // The embedded layout study has its own arrow shortcuts; keep its layout fixed here.
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){
  e.preventDefault();e.stopImmediatePropagation();return;
 }
 if(hit && (e.key==='Enter'||e.key===' ')){
  e.preventDefault();e.stopImmediatePropagation();
  window.coursePlayer.line(hit.dataset.sourceLine);
 }
},true);
function clock(now){
 if(running){
  elapsed=Math.min(duration,elapsed+(now-last)/1000*rate);freeze(elapsed);
  if(elapsed>=duration){
   running=false;
   if(continuous && index<traces[scenario].steps.length-1)start(index+1,true);
   else {continuous=false;publish()}
  }
 }
 last=now;
 if(now-announced>100){announced=now;publish()}
 requestAnimationFrame(clock);
}
settle(0);requestAnimationFrame(clock);
</script>'''

PAGE = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prototype · interactive course animation controls</title>
<style>
:root{color-scheme:dark;font:15px/1.55 var(--font-sans,system-ui),sans-serif;color:var(--foreground,#e6e9f1);background:transparent;--accent:var(--primary,#a8b4ff);--muted:var(--muted-foreground,#a4a7b5);--border:var(--border-color,#363944)}
*{box-sizing:border-box}body{margin:0;padding-bottom:90px;background:transparent}button,select,input{font:inherit}button,select{color:inherit;background:#262a35;border:1px solid #454a5d;border-radius:7px;padding:7px 11px;cursor:pointer}button:hover{background:#34394a}button:disabled{opacity:.4;cursor:default}button:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:2px}button.primary{background:#a8b4ff;color:#161a36;border-color:#a8b4ff;font-weight:650}a{color:var(--accent);text-decoration:none}.muted{color:var(--muted)}.small{font-size:12px}.topbar{height:64px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:22px;padding:0 28px;position:sticky;top:0;background:#202229;z-index:3}.brand{font-weight:700;letter-spacing:-.3px;font-size:18px;color:#a8b4ff}.search{margin-left:auto;padding:6px 16px;border:1px solid #454852;border-radius:8px;color:#9b9eac;min-width:210px}.sidebar{position:fixed;top:64px;bottom:0;width:240px;border-right:1px solid var(--border);padding:24px 17px;overflow:auto}.sidebar p{margin:0 12px 10px;color:#e6e9f1;font-size:13px;font-weight:700}.sidebar a{display:block;color:#b6b8c4;padding:7px 12px;border-radius:6px;font-size:13px}.sidebar a.active{background:#a8b4ff;color:#171b34;font-weight:650}.sidebar .group{margin-top:24px}main{margin-left:240px;max-width:1320px;padding:36px 48px 0;display:grid;grid-template-columns:minmax(0,1fr) 170px;gap:40px}article{min-width:0}h1{font-size:34px;line-height:1.15;letter-spacing:-1px;margin:14px 0 22px}h2{font-size:23px;line-height:1.3;letter-spacing:-.4px;margin:26px 0 14px}p{margin:12px 0;color:#c4c7d3}.breadcrumb{font-size:12px;color:#a0a4b5}.prototype-note{color:#f4cf86;background:#352e24;border:1px solid #64553a;border-radius:6px;padding:8px 11px;font-size:12px;margin-bottom:22px}.source{background:#242730;border:1px solid var(--border);border-radius:7px;padding:17px 20px;font:14px/1.8 ui-monospace,monospace;color:#dae3f6;white-space:pre;overflow:auto}.source .type{color:#d79ef1}.source .var{color:#70d8cb}.source .num{color:#f5bf7e}.toc{font-size:12px;position:sticky;top:90px;align-self:start;color:#979aa9}.toc strong{color:#e4e6ed;display:block;margin-bottom:14px}.toc div{padding:5px 0}.toc .selected{color:#a8b4ff}.trace-heading{font-size:14px;font-weight:700;display:flex;gap:8px;margin:23px 0 12px}.example-switch{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 14px}.example-switch label{font-size:12px;color:#a4a7b5}.example-switch select{margin-left:8px;font-size:13px;padding:5px 8px}.design-label{font-size:12px;color:var(--accent)}.demo{border:1px solid var(--border);border-radius:9px;background:#1e222c;overflow:hidden;display:grid}.viewport{grid-area:canvas;min-width:0;background:#101722;position:relative}iframe{display:block;border:0;width:100%;aspect-ratio:16/9;background:#101722}.readout{padding:12px 16px;border-top:1px solid var(--border);grid-area:readout;background:#1d212a}.readout strong{font-size:13px;font-weight:600}.readout .meta{font-size:11px;color:#9ca5ba;margin-top:3px;display:flex;gap:16px;flex-wrap:wrap}.controls{padding:13px 15px;gap:10px;align-items:center}.transport{display:flex;gap:7px;align-items:center;flex-wrap:wrap}.controls input[type=range]{accent-color:#a8b4ff;min-width:70px;flex:1}.speed{font-size:12px;padding:6px}.count{font:12px ui-monospace,monospace;color:#aeb8d1;white-space:nowrap}.progress-row{display:flex;gap:12px;align-items:center;margin-top:10px}.controls-a{grid-area:controls}.controls-b{grid-area:rail;padding:18px 12px;background:#252a36;border-right:1px solid var(--border);max-height:620px;overflow:auto}.controls-b .transport{gap:5px}.controls-b button{padding:6px 8px;font-size:12px}.rail-heading{font-size:13px;font-weight:700;margin:17px 0 8px}.steps{display:grid;gap:3px}.step{display:flex;gap:9px;text-align:left;width:100%;border:0;border-radius:5px;background:transparent;padding:8px!important;color:#aeb7cc;font-size:11px!important;line-height:1.4}.step.active{background:#3b4663;color:#fff}.step .n{color:#8491b0;min-width:17px;font:11px ui-monospace,monospace}.step.active .n{color:#bac9ff}.controls-c{grid-area:controls;border-bottom:1px solid var(--border);background:#242833;padding:11px 16px}.controls-c .transport{justify-content:space-between}.chapter-row{grid-area:chapters;display:flex;gap:0;background:#232733;overflow:auto}.chapter{flex:1;border:0;border-right:1px solid #414654;border-radius:0;text-align:left;padding:11px 12px;font-size:11px;line-height:1.4;background:transparent;color:#a4abc0;min-width:95px}.chapter.active{box-shadow:inset 0 -3px #a8b4ff;background:#30384c;color:#fff}.chapter strong{display:block;font-size:12px;margin-top:3px}.demo .controls-b,.demo .controls-c,.demo .chapter-row{display:none}body[data-variant=A] .demo{grid-template-areas:'canvas' 'controls' 'readout'}body[data-variant=B] .demo{grid-template-columns:200px minmax(0,1fr);grid-template-areas:'rail canvas' 'rail readout'}body[data-variant=B] .controls-b{display:block}body[data-variant=B] .controls-a{display:none}body[data-variant=B] main{max-width:1540px;grid-template-columns:minmax(0,1fr)}body[data-variant=B] .toc{display:none}body[data-variant=C] .demo{grid-template-areas:'controls' 'canvas' 'chapters' 'readout';border-radius:0;border-left:0;border-right:0}body[data-variant=C] .controls-a{display:none}body[data-variant=C] .controls-c{display:block}body[data-variant=C] .chapter-row{display:flex}body[data-variant=C] .trace-heading{margin-top:24px}.snapshot{font-size:11px;margin:12px 0 22px;color:#8e99b0}.snapshot summary{cursor:pointer}.snapshot pre{white-space:pre-wrap;background:#171a22;padding:12px;color:#aab6cf;border-radius:6px}.answer{border:1px solid var(--border);border-radius:7px;padding:12px 15px;margin:20px 0}.answer summary{font-size:14px;font-weight:600;cursor:pointer}.answer p{font-size:14px}.switcher{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:11px;background:#ecedf5;color:#242638;border:1px solid #fff9;border-radius:50px;padding:7px;box-shadow:0 8px 32px #0009;z-index:9}.switcher button{border:0;border-radius:50%;width:36px;height:36px;background:#d8dbe9;color:#242638;padding:0;font-size:20px}.switcher .label{min-width:220px;text-align:center;font-size:12px;font-weight:700}.switcher .label small{display:block;font-size:10px;font-weight:400;color:#646b81}.focus-note{font-size:12px;color:#a8b4ff;margin:8px 0 18px}body[data-variant=B] .focus-note{color:#9ccfc4}
@media(min-width:1700px){main{margin-left:270px;max-width:1550px}.sidebar{width:270px}}
@media(max-width:1150px){main{padding:28px 24px 0;grid-template-columns:minmax(0,1fr)}.toc{display:none}.sidebar{width:210px}main{margin-left:210px}.brand{max-width:520px;font-size:15px}.search{display:none}}
@media(max-width:760px){.sidebar{display:none}main{margin:0;padding:22px 0 0}.topbar{padding:0 16px;height:56px}.topbar .lang{display:none}.brand{font-size:14px}h1{font-size:29px}.demo{border-radius:6px}body[data-variant=B] .demo{grid-template-columns:140px minmax(0,1fr)}.controls-b{padding:10px 7px}.controls-b .transport{flex-direction:column;align-items:stretch}.controls-b .rail-heading{font-size:11px}.step{font-size:10px!important}.readout{padding:9px}.readout strong{font-size:11px}.example-switch{align-items:start}.switcher .label{min-width:180px}.source{font-size:12px;padding:12px}.controls{padding:10px}.transport button{padding:6px 8px}.controls-c .transport{justify-content:start}}
@media(max-width:520px){body[data-variant=B] .demo{grid-template-columns:minmax(0,1fr);grid-template-areas:'canvas' 'readout' 'rail'}.controls-b{border-right:0;border-top:1px solid var(--border);max-height:260px}.controls-b .transport{flex-direction:row}.steps{grid-template-columns:1fr 1fr}.topbar{padding:0 8px}.brand{font-size:12px}.example-switch{flex-wrap:wrap}.switcher{bottom:9px}}
.source{padding:10px 0;white-space:normal}
.source-line{display:flex;align-items:baseline;gap:16px;width:100%;border:0;border-radius:0;
 padding:4px 16px;text-align:left;background:transparent;color:inherit;font:inherit;white-space:pre}
.source-line code{font:inherit}.source-line:hover{background:#30394e}
.source-line.active{background:#303b54;box-shadow:inset 3px 0 #a8b4ff}
.line-number{color:#8c98b0;min-width:14px;text-align:right;font-size:11px}
</style>
<body data-variant="A">
<header class="topbar"><a class="brand" href="#">Programming Fundamentals and Data Structures</a><div class="search">Search lessons <span style="float:right">⌘ K</span></div><span class="lang small muted">Prototype　☾ Auto　 English ▾</span></header>
<aside class="sidebar"><p>PROGRAMMING FUNDAMENTALS</p><a href="#">Overview</a><a href="#">Concepts</a><p class="group">C++ · Labs</p><a href="#">1. Basic syntax: statements</a><a class="active" href="#">2. Variables and Types</a><a href="#">3. Numeric conversions</a><a href="#">4. Pointers</a><a href="#">5. Structures</a><a href="#">6. Functions</a><a href="#">7. Practice Modeling a Simple Problem</a><a href="#">8. Practice with Simple Problems</a><a href="#">9. C arrays</a><a href="#">10. C++ arrays</a><a href="#">11. Pointer arithmetic</a><a href="#">12. Array practice</a><a href="#">13. Objects</a><a href="#">14. References</a></aside>
<main><article><div class="breadcrumb">Labs / C++ / Variables and Types</div><h1>2. Variables and Types</h1>

<p>Predict the value of each variable after every statement. Open the trace to follow the expression and the memory together.</p>
<h2 id="example-heading">5. Evaluating an expression</h2>
<div class="source" id="lesson-code"></div>
<div class="trace-heading"><span>⌄</span> Execution trace</div>
<div class="example-switch"><span class="design-label" id="design-name"></span><label>Example<select id="example"><option value="0">Expression</option><option value="1">Failed swap</option></select></label></div>
<p class="focus-note" id="design-description"></p>
<section class="demo" aria-label="Interactive execution trace">
<div class="viewport"><iframe id="animation" title="Animated code evaluation and memory" tabindex="-1"></iframe></div>
<div class="controls controls-a"><div class="transport"><button class="primary play" data-action="play">▶ Play</button><button data-action="back" title="Previous settled step">← Back</button><button data-action="next">Next →</button><button data-action="replay" title="Animate this step again">↻</button><select class="speed" aria-label="Playback speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select><button data-action="reset" title="Reset trace" style="margin-left:auto">Reset</button></div><div class="progress-row"><input class="scrub" type="range" min="0" value="0" aria-label="Trace step"><span class="count"></span></div></div>
<div class="controls controls-b"><div class="transport"><button class="primary play" data-action="play">▶ Play</button><button data-action="back">←</button><button data-action="next">→</button><button data-action="replay" title="Replay step">↻</button><select class="speed" aria-label="Playback speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select><button data-action="reset">Reset</button></div><div class="rail-heading">Execution steps</div><div id="steps" class="steps"></div></div>
<div class="controls controls-c"><div class="transport"><button class="primary play" data-action="play">▶ Run</button><span class="count"></span><span><button data-action="back">← Step</button><button data-action="next">Step →</button><button data-action="replay">↻ Replay</button></span><span><select class="speed" aria-label="Playback speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select><button data-action="reset">Reset</button></span></div></div>
<div id="chapters" class="chapter-row"></div>
<div class="readout" aria-live="polite"><strong id="action">Ready</strong><div class="meta"><span id="phase"></span><span id="memory"></span><span id="output"></span></div></div>
</section>
<details class="snapshot"><summary>Inspect current playback state</summary><pre id="snapshot"></pre></details>
<details class="answer"><summary>Answer</summary><p id="answer-copy"></p></details>
<h2>6. Assigning an expression to a variable</h2><p>Assignment stores the computed value in the destination variable. Try changing a source variable afterward: values already copied to other variables remain the same.</p>
</article><aside class="toc"><strong>On this page</strong><div>Overview</div><div>Concepts</div><div>Understanding the examples</div><div>1. Variable definition</div><div>2. Variable declaration</div><div>3. Defining a variable twice</div><div>4. Assigning one variable to another</div><div class="selected">5. Evaluating an expression</div><div>6. Assigning an expression</div><div>7. String value</div><div>8. Reversing output</div><div>9. Uniform initialization</div><div>10. Empty initialization</div></aside></main>
<nav class="switcher" aria-label="Prototype variant"><button id="previous-variant" aria-label="Previous variant">←</button><span class="label" id="variant-label"></span><button id="next-variant" aria-label="Next variant">→</button></nav>
<script id="engine-source" type="application/json">__ENGINE__</script>
<script>
const frame=document.getElementById('animation');
const variants=['A','B','C'], names=['Compact transport','Step navigator','Lesson chapters'];
const descriptions=[
 'A · Click a code line to jump to the start of its execution. Next animates; Play continues from there.',
 'B · Every execution phase is visible beside the animation. Pick a step, then replay its transition to inspect the movement.',
 'C · Follow the source statement by statement. Chapters jump to a line; Step plays the smaller transitions within it.'
];
const $=id=>document.getElementById(id);
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let variant=new URLSearchParams(location.search).get('variant')||'A';
if(!variants.includes(variant))variant='A';
let state,previousScenario=-1;
function changeVariant(delta){
 variant=variants[(variants.indexOf(variant)+delta+3)%3];
 const url=new URL(location.href);url.searchParams.set('variant',variant);
 try{history.replaceState(null,'',url)}catch(e){}
 renderVariant();
}
function renderVariant(){
 document.body.dataset.variant=variant;
 $('design-name').textContent=names[variants.indexOf(variant)];
 $('design-description').textContent=descriptions[variants.indexOf(variant)];
 $('variant-label').innerHTML=variant+' · '+names[variants.indexOf(variant)]+'<small>Prototype controls · ← / → to compare</small>';
}
function update(s){
 state=s;
 if(s.scenario!==previousScenario){
  previousScenario=s.scenario;
  $('lesson-code').innerHTML=s.source.map((line,i)=>'<button class="source-line" data-line="'+i
   +'" aria-label="Jump to line '+(i+1)+'"><span class="line-number">'+(i+1)
   +'</span><code>'+escapeHTML(line)+'</code></button>').join('');
  $('example-heading').textContent=s.scenario===0?'5. Evaluating an expression':'18. Swapping variables';
  $('answer-copy').textContent=s.scenario===0?'b receives a copy of 5 + 6, so b becomes 11. Later, assigning 7 to a leaves b unchanged. The final output is 11.':'After a = b, both variables contain 2. The original value of a has been overwritten, so b = a copies 2 again. A temporary variable is needed to preserve the first value.';
  $('steps').innerHTML=s.steps.map((step,i)=>'<button class="step" data-jump="'+i+'"><span class="n">'+(i+1)+'</span><span>'+escapeHTML(step.label)+'</span></button>').join('');
  $('chapters').innerHTML=s.source.map((line,i)=>'<button class="chapter" data-jump="'+s.steps.findIndex(step=>step.line===i)+'">Line '+(i+1)+'<strong>'+escapeHTML(line)+'</strong></button>').join('');
 }
 document.querySelectorAll('.play').forEach(b=>b.textContent=s.running?'Ⅱ Pause':variant==='C'?'▶ Run':'▶ Play');
 document.querySelectorAll('[data-action=back]').forEach(b=>b.disabled=s.index===0);
 document.querySelectorAll('[data-action=next]').forEach(b=>b.disabled=s.index===s.steps.length-1);
 document.querySelectorAll('.count').forEach(e=>e.textContent=(s.index+1)+' / '+s.steps.length);
 document.querySelectorAll('.scrub').forEach(e=>{e.max=s.steps.length-1;e.value=s.index});
 document.querySelectorAll('.speed').forEach(e=>e.value=s.speed);
 document.querySelectorAll('.step').forEach((e,i)=>{e.classList.toggle('active',i===s.index);e.setAttribute('aria-current',i===s.index?'step':'false')});
 document.querySelectorAll('.chapter').forEach((e,i)=>e.classList.toggle('active',i===s.line));
 document.querySelectorAll('.source-line').forEach((e,i)=>{
  e.classList.toggle('active',i===s.line);e.setAttribute('aria-current',i===s.line?'step':'false');
 });
 $('action').textContent=s.action;
 $('phase').textContent=s.phase+' · '+s.time.toFixed(1)+' / '+s.duration.toFixed(1)+' s';
 $('memory').textContent=s.memory.map(v=>v.name+' = '+(v.value===null?'—':v.value)).join(' · ');
 $('output').textContent='Output: '+(s.stdout?JSON.stringify(s.stdout):'—');
 $('snapshot').textContent=JSON.stringify({variant,index:s.index,line:s.line+1,expression:s.expression,memory:s.memory,stdout:s.stdout,running:s.running,speed:s.speed,phase:s.phase,seconds:Number(s.time.toFixed(2))},null,2);
}
document.addEventListener('click',e=>{
 const action=e.target.closest('[data-action]'),jump=e.target.closest('[data-jump]'),line=e.target.closest('[data-line]');
 if(action)frame.contentWindow.coursePlayer?.[action.dataset.action]();
 if(jump)frame.contentWindow.coursePlayer?.jump(Number(jump.dataset.jump));
 if(line)frame.contentWindow.coursePlayer?.line(Number(line.dataset.line));
});
document.querySelectorAll('.scrub').forEach(e=>e.oninput=()=>frame.contentWindow.coursePlayer?.jump(Number(e.value)));
document.querySelectorAll('.speed').forEach(e=>e.onchange=()=>frame.contentWindow.coursePlayer?.speed(Number(e.value)));
$('example').onchange=e=>frame.contentWindow.coursePlayer?.example(Number(e.target.value));
$('previous-variant').onclick=()=>changeVariant(-1);$('next-variant').onclick=()=>changeVariant(1);
document.addEventListener('keydown',e=>{
 if(e.target.closest('input,textarea,select,[contenteditable]'))return;
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();changeVariant(e.key==='ArrowLeft'?-1:1)}
 if(e.code==='Space' && e.target===document.body){e.preventDefault();frame.contentWindow.coursePlayer?.play()}
});
window.addEventListener('message',e=>{if(e.source===frame.contentWindow && e.data?.kind==='course-player')update(e.data)});
renderVariant();frame.srcdoc=JSON.parse($('engine-source').textContent);
if(new URLSearchParams(location.search).get('production')==='1')document.querySelector('.switcher').hidden=true;
</script></html>'''


def main():
    engine = layout.PAGE.replace('__TRACES__', json.dumps([asdict(t) for t in TIMELINES]))
    engine = engine.replace('</html>', BRIDGE + '</html>')
    # JSON script data must not contain a literal closing script tag.
    page = PAGE.replace('__ENGINE__', json.dumps(engine).replace('<', r'\u003c'))
    target = ROOT / 'website-controls-prototype.html'
    target.write_text(page)
    print(target)


if __name__ == '__main__':
    main()
