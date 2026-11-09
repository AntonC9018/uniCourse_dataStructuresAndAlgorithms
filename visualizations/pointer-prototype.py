"""THROWAWAY pointer-category study for #59: three ways to draw pointers, ?variant=A/B/C.

DECIDED: variant A (arcs above memory); B and C are rejected comparisons.
Question: how should a pointer, the address it stores, and dereference chains look so that
`**pp = 7` stays legible? Same under-memory (B) language as #57; manual traces, no compiler.

Run from the course root: python3 visualizations/pointer-prototype.py
Then open visualizations/pointer-prototype.html.
"""
import json
import re
from pathlib import Path

COLORS = {'a': '#61d4c4', 'b': '#ffbd69', 'p': '#c39bff', 'pp': '#ff8fb1', 'q': '#a6e06b'}


class Trace:
    """Builds evaluation states the way the lesson explains them: `**pp` → `**72` → `*p`…"""

    def __init__(self, name, title, source, cells):
        self.name, self.title, self.source = name, title, source
        self.cells = [dict(name=n, address=a, size=s, kind=k, color=COLORS[n])
                      for n, a, s, k in cells]
        self.values = {cell['name']: None for cell in self.cells}
        self.steps, self.pane, self.line, self.stdout = [], '', 0, ''

    def _add(self, op=None, hold=1.0):
        self.steps.append(dict(line=self.line, pane=self.pane, values=dict(self.values),
                               op=op, stdout=self.stdout, hold=hold))

    def _replace(self, token, new):
        pattern = re.escape(token) + (r'\b' if token[-1].isalnum() else '')
        if token[0].isalpha():
            pattern = r'\b' + pattern
        start = re.search(pattern, self.pane).start()
        self.pane = self.pane[:start] + new + self.pane[start + len(token):]
        return [start, start + len(token)]

    def _cell(self, address):
        return next(c for c in self.cells if c['address'] == address)

    def statement(self, line):
        # Brace initialization reads as an assignment of the evaluated value, as in #57.
        pane = self.source[line].rstrip(';')
        self.line, self.pane = line, re.sub(r'(\w)\{\s*(.*?)\s*\}$', r'\1 = \2', pane)
        self._add()
        return self

    def read(self, name):
        value = self.values[name]
        self._add(dict(kind='read', name=name, value=value,
                       span=self._replace(name, str(value))))
        return self

    def address(self, name):
        value = next(c['address'] for c in self.cells if c['name'] == name)
        self._add(dict(kind='addr', name=name, value=value,
                       span=self._replace('&' + name, str(value))))
        return self

    def deref(self, address, via):
        target = self._cell(address)['name']
        self._add(dict(kind='deref', address=address, target=target, via=via,
                       span=self._replace('*' + str(address), target)))
        return self

    def write(self, name, hold=1.2):
        value = int(self.pane.rsplit('= ', 1)[1])
        self.values[name] = value
        target = re.search(r'\b' + name + r'\b(?=\s*=)', self.pane).start()
        self._add(dict(kind='write', name=name, value=value, target=target), hold)
        return self

    def print(self, name, hold=1.2):
        self.read(name)
        value = str(self.values[name])
        start = self.pane.index('<< ') + 3
        self.stdout += value + ('\n' if 'endl' in self.pane else '')
        self._add(dict(kind='print', value=value, span=[start, start + len(value)]), hold)
        return self

    def json(self):
        self.steps[-1]['hold'] = 3
        return dict(name=self.name, title=self.title, source=self.source,
                    cells=self.cells, steps=self.steps)


def write_through():
    t = Trace('write-through', 'Write through a pointer',
              ['int a{ 1 };', 'int* b{ &a };', '*b = 2;', 'std::cout << a;'],
              [('a', 64, 4, 'int'), ('b', 72, 8, 'ptr')])
    t.statement(0).write('a')
    t.statement(1).address('a').write('b')
    t.statement(2).read('b').deref(64, 'b').write('a')
    t.statement(3).print('a')
    return t.json()


def reassign():
    t = Trace('reassign', 'Reassigning a pointer',
              ['int a = 5;', 'int* p = &a;', '*p = 6;', 'int b = 7;', 'p = &b;', '*p = 8;',
               'std::cout << a << std::endl;', 'std::cout << b << std::endl;'],
              [('a', 64, 4, 'int'), ('b', 68, 4, 'int'), ('p', 72, 8, 'ptr')])
    t.statement(0).write('a')
    t.statement(1).address('a').write('p')
    t.statement(2).read('p').deref(64, 'p').write('a')
    t.statement(3).write('b')
    t.statement(4).address('b').write('p', hold=1.6)
    t.statement(5).read('p').deref(68, 'p').write('b')
    t.statement(6).print('a')
    t.statement(7).print('b')
    return t.json()


def shared_target():
    t = Trace('shared-target', 'Two pointers to one variable',
              ['int a = 5;', 'int* p = &a;', 'int* q = p;', '*q = 6;',
               'std::cout << *p << std::endl;'],
              [('a', 64, 4, 'int'), ('p', 72, 8, 'ptr'), ('q', 80, 8, 'ptr')])
    t.statement(0).write('a')
    t.statement(1).address('a').write('p')
    t.statement(2).read('p').write('q')
    t.statement(3).read('q').deref(64, 'q').write('a')
    t.statement(4).read('p').deref(64, 'p').print('a')
    return t.json()


def double_pointer():
    t = Trace('double-pointer', 'Pointer to a pointer',
              ['int a = 5;', 'int b = 6;', 'int* p = &a;', 'int** pp = &p;', '**pp = 7;',
               '*pp = &b;', '**pp = 8;', 'std::cout << a << std::endl;',
               'std::cout << b << std::endl;'],
              [('a', 64, 4, 'int'), ('b', 68, 4, 'int'), ('p', 72, 8, 'ptr'),
               ('pp', 80, 8, 'ptr')])
    t.statement(0).write('a')
    t.statement(1).write('b')
    t.statement(2).address('a').write('p')
    t.statement(3).address('p').write('pp')
    t.statement(4).read('pp').deref(72, 'pp').read('p').deref(64, 'p').write('a')
    t.statement(5).address('b').read('pp').deref(72, 'pp').write('p', hold=1.6)
    t.statement(6).read('pp').deref(72, 'pp').read('p').deref(68, 'p').write('b')
    t.statement(7).print('a')
    t.statement(8).print('b')
    return t.json()


PAGE = r'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pointer visualization study</title>
<style>
:root {color-scheme:dark; font-family:system-ui; color:#eef3fa; background:#0c121b}
body {margin:0 auto; max-width:1280px; padding:12px 16px 84px}
button,select {font:inherit; color:inherit; background:#233044; border:1px solid #47515f;
 border-radius:8px; padding:8px 12px; cursor:pointer}
button:focus-visible,select:focus-visible,input:focus-visible {outline:3px solid #9cbaff}
p {line-height:1.5; margin:10px 0; color:#a0afc2}
.controls {display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:12px 0}
svg {display:block; width:100%; background:#101722; border-radius:12px}
input[type=range] {flex:1; min-width:120px; accent-color:#9cbaff}
#switcher {position:fixed; bottom:12px; left:50%; transform:translateX(-50%);
 display:flex; align-items:center; gap:8px; padding:8px; border-radius:14px; background:#fff;
 color:#111; box-shadow:0 4px 20px #0009; white-space:nowrap}
#switcher button {background:#eee; color:#111; border-color:#bbb}
#variantName {font-size:14px; min-width:220px; text-align:center}
#state {font-family:monospace; font-size:13px; min-height:36px}
</style>
<p><strong>Prototype #59.</strong> Pointers as 8-byte cells holding addresses; ints 4 bytes;
addresses from 64. Variants differ only in how the pointer→pointee link is drawn.</p>
<div class="controls">
 <label>Example <select id="scenario"></select></label>
 <button id="play">Play</button><button id="back">← Step</button><button id="next">Step →</button>
 <input id="scrub" aria-label="Trace step" type="range" min="0" value="0"><span id="count"></span>
</div>
<svg id="stage" viewBox="0 0 1280 720" role="img" aria-label="Code, memory and pointers"></svg>
<p id="description"></p><div id="state" aria-live="polite"></div>
<nav id="switcher" aria-label="Prototype variant">
 <button id="prevVariant" aria-label="Previous variant">←</button><span id="variantName"></span>
 <button id="nextVariant" aria-label="Next variant">→</button>
</nav>
<script>
const traces=__TRACES__;
const variants=['A','B','C'], variantNames=['Arcs above memory','Lanes below memory','Address lookup'];
const descriptions=[
 'A · Arcs above memory: every live pointer keeps an arrow from its cell, over the address row, '
 +'onto the pointee\'s address label. Dereference lights the arrow from the pointer to the target.',
 'B · Lanes below memory: arrows leave the bottom of the pointer cell, run in their own lane under '
 +'the names, and enter the pointee from below. Address labels stay free above memory.',
 'C · Address lookup: no persistent arrows. The pointer cell shows only the address; dereference '
 +'carries the address from the expression to the matching address label, which selects the target.'];
let variant=new URLSearchParams(location.search).get('variant')||'A';
if(!variants.includes(variant)) variant='A';
let scenario=0,index=0,playing=false,timer,settleTimer;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mono='DejaVu Sans Mono,monospace', ease='calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"';
const FG='#eef3fa', MUTED='#a0afc2', GREY='#697382', READ='#9cbaff', WRITE='#f5e58b', CONTEXT='#6f7c8f';
const BYTE=24, MEMX=648, BASE=64, codeChar=25*.602, evalChar=30*.602;
const T={prepare:0.55,travel:1.1,replace:0.2,settle:0.6,follow:0.9,writeHold:0.8,copyBegin:0.15,copyTravel:1.0};
const KEYWORDS=new Set(['int','std','cout','endl']);
const departure=op=>op.kind==='write'?T.writeHold:op.kind==='print'?0.2:T.prepare;
function arrival(op) {
 if(op.kind==='deref' && variant!=='C') return T.prepare+T.follow;
 if(op.kind==='print') return 0.9;
 return departure(op)+T.travel;
}
const opSeconds=op=>arrival(op)+T.settle+(op.kind==='write'?0.5:0);
const copySeconds=T.copyBegin+T.copyTravel+0.2;
function copies(i){const s=traces[scenario].steps; return i===0||s[i-1].line!==s[i].line;}
function stepSeconds(i){const s=traces[scenario].steps[i]; return s.hold+(s.op?opSeconds(s.op):copies(i)?copySeconds:0);}

function hide(at){return `<set attributeName="opacity" to="0" begin="${at}s" fill="freeze"/>`;}
function fade(from,to,dur=0.5,begin=0){return `<animate attributeName="opacity" from="${from}" to="${to}" dur="${dur}s" begin="${begin}s" ${ease} fill="freeze"/>`;}
function animateAttr(name,from,to,dur=0.45,begin=0){return `<animate attributeName="${name}" from="${from}" to="${to}" dur="${dur}s" begin="${begin}s" ${ease} fill="freeze"/>`;}
function animated(el,anims){return anims?el.replace(/\/>$/,'>'+anims+'</'+el.match(/^<(\w+)/)[1]+'>'):el;}
function text(x,y,value,size=26,color=FG,anchor='start'){
 return `<text x="${x}" y="${y}" font-family="${mono}" font-size="${size}" fill="${color}" text-anchor="${anchor}" xml:space="preserve">${esc(value)}</text>`;}
function rect(x,y,w,h,fill='#192331',stroke='none',radius=8,width=3){
 return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;}
function pulse(begin){return `<animateTransform attributeName="transform" type="scale" values="1;1.14;1" keyTimes="0;0.45;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" begin="${begin}s" dur="0.65s" fill="freeze"/>`;}
function markBox(x,y,len,stroke,fill){return `<rect x="${x-3}" y="${y-32}" width="${len*evalChar+6}" height="42" rx="6" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;}
// Starts `from` pixels right of its place and slides home after `begin`.
function settle(markup,from,begin){return from?`<g transform="translate(${from} 0)"><animateTransform attributeName="transform" type="translate" from="${from} 0" to="0 0" begin="${begin}s" dur="0.3s" ${ease} fill="freeze"/>${markup}</g>`:markup;}
function glide(markup,dx,begin,dur){
 return dx?`<g><animateTransform attributeName="transform" type="translate" from="0 0" to="${dx} 0" begin="${begin}s" dur="${dur}s" ${ease} fill="freeze"/>${markup}</g>`:markup;}
function colored(x,y,value,trace,size=30,muteKeywords=true){
 let out='';
 for(const token of value.split(/(\b[a-zA-Z_]\w*\b)/)){
  const cell=trace.cells.find(c=>c.name===token);
  out+=text(x,y,token,size,cell?cell.color:muteKeywords&&KEYWORDS.has(token)?CONTEXT:FG);
  x+=token.length*size*.602;
 }
 return out;
}
function geometry(trace){
 const lh=56, h=44+trace.source.length*lh, top=Math.max(24,Math.round((720-h)/2));
 const g={code:[40,top,540,h],lh,cy:top+50};
 const layout={A:{memY:290,pane:430,out:566},B:{memY:118,pane:372,out:510},C:{memY:200,pane:372,out:510}}[variant];
 g.memY=layout.memY; g.pane=[640,layout.pane,592,76]; g.out=[664,layout.out];
 g.tx=664; g.ty=layout.pane+38+11;
 g.cells=trace.cells.map(c=>({...c,x:MEMX+(c.address-BASE)*BYTE,y:g.memY,w:c.size*BYTE,h:64}));
 return g;
}
const lineY=(g,i)=>g.cy+i*g.lh;
const cellNamed=(g,name)=>g.cells.find(c=>c.name===name);
const cellAt=(g,address)=>g.cells.find(c=>c.address===address);
const labelWidth=c=>String(c.address).length*18*.602;
const labelCenter=c=>[c.x+labelWidth(c)/2,c.y-22];
const valueCenter=c=>[c.x+c.w/2,c.y+32];

// Persistent pointer links, one per live pointer, for variants A and B.
function links(g,values){
 if(variant==='C') return [];
 const list=g.cells.filter(c=>c.kind==='ptr'&&values[c.name]!==null)
  .map(c=>({from:c,to:cellAt(g,values[c.name])})).filter(l=>l.to);
 if(variant==='A') {
  // Arcs start and end near the centre of their cells. When a cell carries several arc ends
  // (several pointers to it, or its own pointer plus incoming ones), the ends spread around
  // the centre without crossing: ends leading left sit left of ends leading right, and on
  // each side the arc reaching farther sits nearer the centre, so it encloses the shorter one.
  const centre=c=>c.x+c.w/2, ports=new Map();
  for(const l of list) for(const [cell,other,key] of [[l.from,l.to,'sx'],[l.to,l.from,'ex']]) {
   if(!ports.has(cell)) ports.set(cell,[]);
   ports.get(cell).push({l,key,other:centre(other)});
  }
  for(const [cell,ends] of ports) {
   const side=end=>end.other<centre(cell)?0:1;
   ends.sort((p,q)=>side(p)-side(q)||q.other-p.other);
   ends.forEach((end,i)=>end.l[end.key]=centre(cell)+(i-(ends.length-1)/2)*20);
  }
  const range=l=>[Math.min(l.sx,l.ex),Math.max(l.sx,l.ex)];
  for(const l of list) {
   const [a,b]=range(l), {sx,ex}=l;
   l.level=list.filter(o=>o!==l&&range(o)[0]>=a&&range(o)[1]<=b).length;
   const sy=l.from.y-2, ey=l.to.y-3, apex=l.to.y-112-l.level*40;
   l.d=`M ${sx} ${sy} C ${sx} ${apex}, ${ex} ${apex}, ${ex} ${ey-9}`; l.head=[ex,ey,90];
  }
 } else {
  // Each link owns a lane below the names; it enters the pointee's first byte from below.
  list.sort((p,q)=>p.from.x-q.from.x).forEach((l,lane)=>{
   const sx=l.from.x+30, sy=l.from.y+l.from.h, ex=l.to.x+16, ey=l.to.y+l.to.h+2;
   const ly=sy+56+lane*22, d=Math.sign(ex-sx)||1;
   l.d=`M ${sx} ${sy} V ${ly-8} Q ${sx} ${ly} ${sx+8*d} ${ly} H ${ex-8*d} Q ${ex} ${ly} ${ex} ${ly-8} V ${ey+9}`;
   l.head=[ex,ey,-90];
  });
 }
 return list;
}
function linkMarkup(l,{grow=null,fadeOut=null}={}) {
 const [x,y,angle]=l.head, color=l.from.color;
 const head=`<path d="M -11 -6.5 L 0 0 L -11 6.5 Z" fill="${color}" transform="translate(${x} ${y}) rotate(${angle})"/>`;
 return `<g data-link="${l.from.name}"${grow!==null?' opacity="1"':''}>`
  +(fadeOut!==null?fade(1,0,0.3,fadeOut):'')
  // A background halo separates arcs from the labels and from each other where they meet.
  +`<path d="${l.d}" fill="none" stroke="#101722" stroke-width="9"`+(grow!==null?` data-grow="${grow}"`:'')+'/>'
  +`<path d="${l.d}" fill="none" stroke="${color}" stroke-width="2.5"`
  +(grow!==null?` data-grow="${grow}"`:'')+'/>'
  +(grow!==null?`<g opacity="0">${fade(0,1,0.15,grow+0.5)}${head}</g>`:head)+'</g>';
}
function arrows(g,step,prev,op){
 if(variant==='C') return '';
 const now=links(g,step.values);
 if(op?.kind==='write' && g.cells.find(c=>c.name===op.name).kind==='ptr') {
  const at=arrival(op), before=links(g,prev.values);
  let out='';
  for(const l of before) out+=linkMarkup(l,l.from.name===op.name?{fadeOut:at}:{});
  for(const l of now) if(l.from.name===op.name) out+=linkMarkup(l,{grow:at+0.1});
  return out;
 }
 let out=now.map(l=>linkMarkup(l)).join('');
 if(op?.kind==='deref') {
  const l=now.find(l=>l.from.name===op.via);
  // The followed link brightens from pointer to pointee.
  if(l) out+=`<path d="${l.d}" fill="none" stroke="${l.from.color}" stroke-width="7" stroke-linecap="round" data-follow="${T.prepare}"/>`;
 }
 return out;
}
function memory(trace,g,step,prev,op){
 const values=op?.kind==='write'?prev.values:step.values, at=op?arrival(op):0;
 let out='';
 const cells=[...g.cells].sort((a,b)=>a.address-b.address);
 for(let i=1;i<cells.length;i++){
  const end=cells[i-1].address+cells[i-1].size;
  if(cells[i].address>end) out+=`<rect x="${MEMX+(end-BASE)*BYTE+3}" y="${g.memY+3}" width="${(cells[i].address-end)*BYTE-6}" height="58" fill="none" stroke="#2c3442" stroke-dasharray="5 5"/>`;
 }
 for(const c of g.cells){
  const writing=op?.kind==='write'&&op.name===c.name, live=values[c.name]!==null||writing;
  const target=op?.kind==='deref'&&op.address===c.address;
  if(op?.kind==='addr'&&op.name===c.name)
   out+=`<g opacity="0">${fade(0,1,0.15)}${fade(1,0,0.2,at+0.1)}${rect(c.x-5,c.y-39,labelWidth(c)+10,26,'#2c4775',READ,5,2)}</g>`;
  if(target && variant==='C')
   out+=`<g opacity="0">${fade(0,1,0.15,at)}${rect(c.x-5,c.y-39,labelWidth(c)+10,26,'#3a4658',FG,5,2)}</g>`;
  out+=text(c.x,c.y-20,c.address,18,live?MUTED:GREY);
  out+=text(c.x+c.w/2,c.y+c.h+34,c.name,26,live?c.color:GREY,'middle');
  out+=rect(c.x,c.y,c.w,c.h,live?'#192331':'#171d27','none',0);
  out+=rect(c.x+1.5,c.y+1.5,c.w-3,c.h-3,'none',live?c.color:'#47515f',0,3);
  const active=(op?.kind==='read'&&op.name===c.name)||writing;
  if(active) out+=`<g>${fade(1,0,0.35,at+0.15)}${rect(c.x+4.5,c.y+4.5,c.w-9,c.h-9,'none',writing?WRITE:READ,0,3)}</g>`;
  // Dereference selects a location; it does not read it, so the outline is neutral.
  if(target) out+=`<g opacity="0">${fade(0,1,0.2,at-0.15)}${rect(c.x+4.5,c.y+4.5,c.w-9,c.h-9,'none',FG,0,3)}</g>`;
  if(!live) continue;
  const [cx,cy]=[c.x+c.w/2,c.y+c.h/2];
  out+=`<g transform="translate(${cx} ${cy})"><g>`+(writing?pulse(at-0.2):active?pulse(0):'');
  if(writing) {
   if(prev.values[c.name]!==null) out+=`<g>${hide(at)}${text(0,11,prev.values[c.name],30,FG,'middle')}</g>`;
   out+=`<g opacity="0">${fade(0,1,T.replace,at)}${text(0,11,step.values[c.name],30,FG,'middle')}</g>`;
  } else out+=text(0,11,values[c.name],30,FG,'middle');
  out+='</g></g>';
 }
 return out;
}
function valueBox(value,color,path,begin,travel,end){
 const half=Math.max(28,String(value).length*evalChar/2+12);
 return `<g opacity="0">${fade(0,0.55,0.25,begin)}${fade(0.55,0,0.2,end-0.2)}<path d="${path}" fill="none" stroke="${color}" stroke-width="3"/></g>`
  +`<g opacity="0">${fade(0,1,0.12,begin)}${fade(1,0,T.replace,end)}`
  +rect(-half,-25,2*half,50,'#192331',color,9)+text(0,11,value,30,FG,'middle')
  +`<animateMotion begin="${begin}s" dur="${travel}s" path="${path}" keyPoints="0;1" ${ease} fill="freeze"/></g>`;
}
function transfers(g,step,prev,op){
 if(!op) return '';
 const at=arrival(op), begin=departure(op), ty=g.ty-11;
 const spanCenter=(s,len)=>g.tx+(s+len/2)*evalChar;
 if(op.kind==='read'){
  const [sx,sy]=valueCenter(cellNamed(g,op.name)), dx=spanCenter(op.span[0],op.span[1]-op.span[0]);
  const port=sx-50, mid=(g.memY+64+ty)/2;
  return valueBox(op.value,READ,`M ${sx} ${sy} C ${port} ${sy}, ${port} ${mid}, ${port} ${mid} C ${port} ${ty}, ${dx} ${mid}, ${dx} ${ty}`,begin,T.travel,at);
 }
 if(op.kind==='addr'){
  // The address comes from the label above storage: taking an address reads no value.
  const c=cellNamed(g,op.name), [sx,sy]=labelCenter(c), dx=spanCenter(op.span[0],op.span[1]-op.span[0]);
  const side=c.x-28;
  return valueBox(op.value,READ,`M ${sx} ${sy} C ${side} ${sy}, ${side} ${g.memY+64}, ${side} ${(g.memY+64+ty)/2} C ${side} ${ty}, ${dx} ${ty-60}, ${dx} ${ty}`,begin,T.travel,at);
 }
 if(op.kind==='write'){
  const sx=spanCenter(step.pane.lastIndexOf('= ')+2,String(op.value).length);
  const [ex,ey]=valueCenter(cellNamed(g,op.name)), port=ex+50, mid=(g.memY+64+ty)/2;
  return valueBox(op.value,WRITE,`M ${sx} ${ty} C ${sx} ${mid}, ${port} ${ty}, ${port} ${mid} C ${port} ${mid}, ${port} ${ey}, ${ex} ${ey}`,begin,T.travel,at);
 }
 if(op.kind==='deref' && variant==='C'){
  const value=String(op.address), sx=spanCenter(op.span[0]+1,value.length), [ex,ey]=labelCenter(cellAt(g,op.address));
  return valueBox(value,FG,`M ${sx} ${ty} C ${sx} ${ty-120}, ${ex} ${ey+150}, ${ex} ${ey}`,begin,T.travel,at);
 }
 return '';
}
function pane(trace,g,step,prev,op,copying,lineChanged){
 const [px,py,pw,ph]=g.pane, tx=g.tx, ty=g.ty;
 let out=rect(px,py,pw,ph,'#202e42');
 if(copying){
  const sx=g.code[0]+62, sy=lineY(g,step.line), begin=lineChanged?0.3:T.copyBegin, total=begin+T.copyTravel;
  if(prev && prev.line!==step.line) out+=`<g>${fade(1,0,0.3,begin+0.2)}${colored(tx,ty,prev.pane,trace)}</g>`;
  out+=`<g><animateMotion dur="${total}s" path="M ${sx} ${sy} L ${tx} ${ty}" keyPoints="0;0;1" keyTimes="0;${(begin/total).toFixed(4)};1" calcMode="spline" keySplines="0 0 1 1;0.4 0 0.2 1" fill="freeze"/>`
   +`<g transform="scale(${25/30})"><animateTransform attributeName="transform" type="scale" from="${25/30}" to="1" begin="${begin}s" dur="${T.copyTravel}s" ${ease} fill="freeze"/>`
   +`<g opacity="0">${fade(0,1,0.15,begin-0.15)}${fade(1,0,0.12,total)}<rect x="-8" y="-36" width="${step.pane.length*evalChar+16}" height="48" rx="7" fill="#2e4059" stroke="${READ}" stroke-width="2"/></g>`
   +colored(0,0,step.pane,trace)+'</g></g>';
  return out;
 }
 if(op && ['read','addr','deref'].includes(op.kind)){
  const before=prev.pane, [s,e]=op.span, len=step.pane.length-before.length+(e-s);
  const at=arrival(op), dx=(len-(e-s))*evalChar;
  const [stroke,fill]=op.kind==='deref'?[FG,'#3a4658']:[READ,'#2c4775'];
  out+=`<g opacity="0">${fade(0,1,0.15)}${fade(1,0,0.2,at-0.1)}${markBox(tx+s*evalChar,ty,e-s,stroke,fill)}</g>`;
  out+=colored(tx,ty,before.slice(0,s),trace);
  out+=`<g>${hide(at)}${colored(tx+s*evalChar,ty,before.slice(s,e),trace)}</g>`;
  out+=`<g opacity="0">${fade(0,1,T.replace,at)}${settle(colored(tx+s*evalChar,ty,step.pane.slice(s,s+len),trace),(e-s-len)/2*evalChar,at+0.1)}</g>`;
  // The rest of the line slides with the settling value, so the two never overlap.
  return out+glide(colored(tx+e*evalChar,ty,before.slice(e),trace),dx,at+0.1,0.3);
 }
 if(op?.kind==='write'){
  const at=arrival(op), v=step.pane.lastIndexOf('= ')+2;
  out+=`<g opacity="0">${fade(0,1,0.15)}${fade(1,0,0.2,at+0.15)}${markBox(tx+v*evalChar,ty,step.pane.length-v,WRITE,'#4a4630')}</g>`;
  out+=`<g opacity="0">${fade(0,1,0.15)}${fade(1,0,0.3,at+0.4)}<rect x="${tx+op.target*evalChar-3}" y="${ty-32}" width="${op.name.length*evalChar+6}" height="42" rx="6" fill="none" stroke="${WRITE}" stroke-width="2"/></g>`;
 }
 return out+colored(tx,ty,step.pane,trace);
}
function output(g,step,prev,op){
 const [ox,oy]=g.out, label='Output: ', vx=ox+label.length*26*.602;
 const printing=op?.kind==='print', shown=printing?prev.stdout:step.stdout;
 if(!step.stdout) return '';
 let out=(printing&&!prev.stdout?`<g opacity="0">${fade(0,1,0.25)}`:'<g>')+text(ox,oy,label,26,MUTED)+'</g>';
 shown.split('\n').forEach((line,i)=>out+=text(vx,oy+i*36,line,30));
 if(printing){
  const lines=shown.split('\n'), x=vx+lines[lines.length-1].length*evalChar, y=oy+(lines.length-1)*36;
  const sx=g.tx+(op.span[0]+op.value.length/2)*evalChar, w=op.value.length*evalChar;
  out+=valueBox(op.value,MUTED,`M ${sx} ${g.ty-11} C ${sx} ${y-30}, ${x+w/2} ${g.ty+20}, ${x+w/2} ${y-11}`,0.2,0.7,0.9);
  out+=`<g opacity="0">${fade(0,1,0.15,0.9)}${text(x,y,op.value,30)}</g>`;
 }
 return out;
}
function code(trace,g,step,op,oldLine){
 let out=rect(...g.code);
 const y=lineY(g,step.line), len=trace.source[step.line].replace(/;\s*$/,'').length;
 const color=op?.kind==='write'?WRITE:READ;
 let stripe=rect(g.code[0]+8,y-32,4,44,color,'none',0), span=rect(g.code[0]+59,y-30,len*codeChar+6,40,'#2e4059','none',6);
 if(oldLine!==null){
  const oy=lineY(g,oldLine), oldLen=trace.source[oldLine].replace(/;\s*$/,'').length;
  stripe=animated(stripe,animateAttr('y',oy-32,y-32));
  span=animated(span,animateAttr('y',oy-30,y-30)+animateAttr('width',oldLen*codeChar+6,len*codeChar+6));
 }
 out+=stripe+span;
 trace.source.forEach((src,i)=>{out+=text(g.code[0]+22,lineY(g,i),i+1,18,MUTED)+colored(g.code[0]+62,lineY(g,i),src,trace,25,false);});
 return out;
}
function describe(step,i){
 const op=step.op;
 if(!op) return 'Copy line '+(step.line+1)+' into evaluation';
 return {read:()=>`Read ${op.name}: its cell holds ${op.value}`,
  addr:()=>`Take the address of ${op.name}: ${op.value} (no value is read)`,
  deref:()=>`Follow address ${op.address}: the location is ${op.target}`,
  write:()=>`Store ${op.value} in ${op.name}`,
  print:()=>`Print ${op.value}`}[op.kind]();
}
function finishPaths(){
 const svg=$('stage');
 for(const p of svg.querySelectorAll('[data-grow],[data-follow]')){
  const L=p.getTotalLength(), grow=p.dataset.grow!==undefined;
  const begin=Number(grow?p.dataset.grow:p.dataset.follow), dur=grow?0.6:T.follow;
  p.setAttribute('stroke-dasharray',`${L} ${L}`); p.setAttribute('stroke-dashoffset',L);
  const a=document.createElementNS(svg.namespaceURI,'animate');
  for(const [k,v] of Object.entries({attributeName:'stroke-dashoffset',from:L,to:0,begin:begin+'s',dur:dur+'s',
   calcMode:'spline',keyTimes:'0;1',keySplines:'0.4 0 0.2 1',fill:'freeze'})) a.setAttribute(k,v);
  p.append(a);
  if(!grow){
   const f=document.createElementNS(svg.namespaceURI,'animate');
   for(const [k,v] of Object.entries({attributeName:'opacity',from:1,to:0,begin:(begin+dur+0.25)+'s',dur:'0.4s',fill:'freeze'})) f.setAttribute(k,v);
   p.append(f);
  }
 }
}
function draw(animate=false){
 clearTimeout(settleTimer);
 const trace=traces[scenario], step=trace.steps[index], prev=index?trace.steps[index-1]:null;
 const g=geometry(trace), op=animate?step.op:null;
 const copying=animate&&copies(index), lineChanged=animate&&prev&&prev.line!==step.line;
 let out=code(trace,g,step,op,lineChanged?prev.line:null);
 out+=`<path d="M ${g.code[0]+g.code[2]+5} ${lineY(g,step.line)-10} H ${g.code[0]+g.code[2]+40} V ${g.pane[1]+38} H ${g.pane[0]}" fill="none" stroke="#697d99" stroke-width="2"/>`;
 out+=arrows(g,step,prev,op)+memory(trace,g,step,prev,op)+pane(trace,g,step,prev,op,copying,lineChanged)
  +output(g,step,prev,op)+transfers(g,step,prev,op);
 const svg=$('stage'); svg.innerHTML=out; finishPaths(); svg.setCurrentTime(0);
 $('description').textContent=descriptions[variants.indexOf(variant)];
 $('variantName').textContent=variant+' · '+variantNames[variants.indexOf(variant)];
 $('scrub').max=trace.steps.length-1; $('scrub').value=index;
 $('count').textContent=`${index+1} / ${trace.steps.length}`;
 $('state').textContent=describe(step,index)+' · '+trace.cells.map(c=>c.name+' = '
  +(step.values[c.name]===null?'unallocated':step.values[c.name])).join(' · ')
  +' · evaluation: '+step.pane+(step.stdout?' · output: '+JSON.stringify(step.stdout):'');
 if(op) settleTimer=setTimeout(()=>draw(false),opSeconds(op)*1000);
}
function stop(){playing=false;clearTimeout(timer);$('play').textContent='Play';}
function advance(d){stop();index=Math.max(0,Math.min(traces[scenario].steps.length-1,index+d));draw(d>0);}
function tick(){if(!playing)return;if(index===traces[scenario].steps.length-1){stop();return;}
 index++;draw(true);timer=setTimeout(tick,stepSeconds(index)*1000);}
$('play').onclick=()=>{if(playing){stop();return;}if(index===traces[scenario].steps.length-1)index=0;
 playing=true;$('play').textContent='Pause';draw(true);timer=setTimeout(tick,stepSeconds(index)*1000);};
$('next').onclick=()=>advance(1);$('back').onclick=()=>advance(-1);
$('scrub').oninput=e=>{stop();index=Number(e.target.value);draw();};
traces.forEach((t,i)=>$('scenario').add(new Option(t.title,i)));
$('scenario').onchange=e=>{stop();scenario=Number(e.target.value);index=0;draw();};
function changeVariant(d){variant=variants[(variants.indexOf(variant)+d+3)%3];
 const url=new URL(location.href);url.searchParams.set('variant',variant);
 try{history.replaceState(null,'',url);}catch(error){if(error.name!=='SecurityError')throw error;}
 draw();}
$('prevVariant').onclick=()=>changeVariant(-1);$('nextVariant').onclick=()=>changeVariant(1);
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select,[contenteditable]'))return;
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();changeVariant(e.key==='ArrowLeft'?-1:1);}});
draw();
</script>
</html>'''

TRACES = [write_through(), reassign(), double_pointer(), shared_target()]

if __name__ == '__main__':
    target = Path(__file__).with_name('pointer-prototype.html')
    target.write_text(PAGE.replace('__TRACES__', json.dumps(TRACES).replace('<', '\\u003c')))
    print(target)
