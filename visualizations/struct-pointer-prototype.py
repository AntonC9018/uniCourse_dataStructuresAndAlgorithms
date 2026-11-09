"""THROWAWAY study: structs in memory, copies, `.` and `->`, and pointers to structs. ?variant=A/B.

Question: how does a struct variable read in the player, and where does a pointer to a struct
land compared with a pointer to one of its fields? Builds on the locked pointer arcs (#59) and
the under-memory (B) player of #57. Traces are manual; production layouts come from Clang (#62).

Variants differ only in how a struct groups its fields:
A · flat fields with a bracket and the struct name underneath; a pointee bar marks the target.
B · a frame around the struct's fields; an arc to the struct lands on the frame.

The JavaScript is copied from pointer-prototype.py and adapted; it is not meant to be shared.
Run from the course root: python3 visualizations/struct-pointer-prototype.py
Then open visualizations/struct-pointer-prototype.html.
"""
import json
import re
from pathlib import Path

COLORS = ('#61d4c4', '#ffbd69', '#c39bff', '#ff8fb1', '#a6e06b')


def scalar(name, address, size, kind='int'):
    return dict(name=name, address=address, fields=None, size=size, kind=kind)


def struct(name, type_, address, fields, size=None):
    """fields: (name, offset, size, kind); size includes any tail padding."""
    size = size or max(offset + n for _, offset, n, _ in fields)
    return dict(name=name, type=type_, address=address, size=size,
                fields=[dict(name=f, offset=o, size=n, kind=k) for f, o, n, k in fields])


class Trace:
    """Evaluation states in the lesson's notation: `pa->f1 = 7` → `64->f1 = 7` → `a.f1 = 7`."""

    def __init__(self, name, title, source, variables):
        self.name, self.title, self.source = name, title, source
        self.leaves, self.groups = [], []
        for color, var in zip(COLORS, variables):
            if var['fields'] is None:
                self.leaves.append(dict(name=var['name'], label=var['name'], group=None,
                                        address=var['address'], size=var['size'],
                                        kind=var['kind'], color=color))
                continue
            names = []
            for f in var['fields']:
                names.append(var['name'] + '.' + f['name'])
                self.leaves.append(dict(name=names[-1], label=f['name'], group=var['name'],
                                        address=var['address'] + f['offset'], size=f['size'],
                                        kind=f['kind'], color=color))
            self.groups.append(dict(name=var['name'], type=var['type'], address=var['address'],
                                    size=var['size'], color=color, fields=names))
        self.values = {leaf['name']: None for leaf in self.leaves}
        self.targets = {}
        self.steps, self.pane, self.line, self.stdout, self.carry = [], '', 0, '', None

    def _fields(self, name):
        group = next((g for g in self.groups if g['name'] == name), None)
        return group['fields'] if group else [name]

    def _value(self, name):
        if name in self.values:
            return str(self.values[name])
        return '{' + ', '.join(str(self.values[f]) for f in self._fields(name)) + '}'

    def _add(self, op=None, hold=1.0):
        self.steps.append(dict(line=self.line, pane=self.pane, values=dict(self.values),
                               targets=dict(self.targets), op=op, stdout=self.stdout,
                               hold=hold))

    def _replace(self, token, new):
        pattern = re.escape(token)
        if token[0].isalnum():
            pattern = r'(?<![\w.>])' + pattern
        if token[-1].isalnum():
            pattern += r'(?![\w.])'
        start = re.search(pattern, self.pane).start()
        self.pane = self.pane[:start] + new + self.pane[start + len(token):]
        return [start, start + len(token)]

    def statement(self, line, pane=None):
        # Brace initialization reads as an assignment of the evaluated value, as in #57.
        self.line = line
        self.pane = pane or re.sub(r'(\w)\s*\{\s*(.*?)\s*\}$', r'\1 = \2',
                                   self.source[line].rstrip(';'))
        self._add()
        return self

    def declare(self, name):
        """An uninitialized object: its storage exists, but its value is unknown."""
        for field in self._fields(name):
            self.values[field] = '?'
        self.steps[-1]['values'] = dict(self.values)
        return self

    def read(self, name, token=None):
        value = self._value(name)
        self.carry = name
        self._add(dict(kind='read', name=name, value=value,
                       span=self._replace(token or name, value)))
        return self

    def address(self, name):
        value = str(self.leaves[[leaf['name'] for leaf in self.leaves].index(
            self._fields(name)[0])]['address'])
        self.carry = ('address', name)
        self._add(dict(kind='addr', name=name, value=value,
                       span=self._replace('&' + name, value)))
        return self

    def deref(self, token, target, via, new=None):
        self.carry = None
        self._add(dict(kind='deref', target=target, via=via,
                       span=self._replace(token, new or target)))
        return self

    def write(self, name, hold=1.2):
        text = self.pane.rsplit('= ', 1)[1]
        values = text.strip('{}').split(', ') if text.startswith('{') else [text]
        fields = self._fields(name)
        sources = self._fields(self.carry) if isinstance(self.carry, str) else [None] * len(fields)
        for field, value, source in zip(fields, values, sources):
            self.values[field] = int(value) if value.isdigit() else value
            self.targets.pop(field, None)
            if isinstance(self.carry, tuple):
                self.targets[field] = self.carry[1]
            elif source in self.targets:
                self.targets[field] = self.targets[source]
        self.carry = None
        target = re.search(r'(?<![\w.])' + re.escape(name) + r'(?=\s*=)', self.pane).start()
        self._add(dict(kind='write', name=name, value=text, target=target), hold)
        return self

    def print(self, name, hold=1.2):
        self.read(name)
        value = self._value(name)
        start = self.pane.index('<< ') + 3
        self.stdout += value + ('\n' if 'endl' in self.pane else '')
        self._add(dict(kind='print', value=value, span=[start, start + len(value)]), hold)
        return self

    def json(self):
        self.steps[-1]['hold'] = 3
        return dict(name=self.name, title=self.title, source=self.source,
                    leaves=self.leaves, groups=self.groups, steps=self.steps)


TWO_INTS = [('f1', 0, 4, 'int'), ('f2', 4, 4, 'int')]


def copy_assignment():
    # Lesson 05, example 9.
    t = Trace('copy', 'Assigning a structure',
              ['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'a.f2 = 6;', 'A b;',
               'b.f1 = 7;', 'b = a;', 'std::cout << b.f1 << std::endl;',
               'std::cout << b.f2 << std::endl;'],
              [struct('a', 'A', 64, TWO_INTS), struct('b', 'A', 72, TWO_INTS)])
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).write('a.f2')
    t.statement(4).declare('b')
    t.statement(5).write('b.f1')
    t.statement(6).read('a').write('b', hold=1.6)
    t.statement(7).print('b.f1')
    t.statement(8).print('b.f2')
    return t.json()


def arrow_operator():
    # Lesson 05, example 12.
    t = Trace('arrow', 'The -> operator',
              ['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'A* pa = &a;',
               '(*pa).f2 = 6;', 'pa->f1 = 7;', 'std::cout << a.f1 << std::endl;',
               'std::cout << a.f2 << std::endl;'],
              [struct('a', 'A', 64, TWO_INTS), scalar('pa', 72, 8, 'ptr')])
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).address('a').write('pa')
    t.statement(4).read('pa').deref('(*64)', 'a', 'pa').write('a.f2')
    t.statement(5).read('pa').deref('64->f1', 'a.f1', 'pa').write('a.f1')
    t.statement(6).print('a.f1')
    t.statement(7).print('a.f2')
    return t.json()


def copy_through_pointer():
    # Lesson 05, example 11.
    t = Trace('through-pointer', 'Copying through a structure address',
              ['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'a.f2 = 6;',
               'A* pa = &a;', 'a.f1 = 7;', 'A b = *pa;', 'std::cout << b.f1 << std::endl;'],
              [struct('a', 'A', 64, TWO_INTS), scalar('pa', 72, 8, 'ptr'),
               struct('b', 'A', 80, TWO_INTS)])
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).write('a.f2')
    t.statement(4).address('a').write('pa')
    t.statement(5).write('a.f1')
    t.statement(6).read('pa').deref('*64', 'a', 'pa').read('a').write('b', hold=1.6)
    t.statement(7).print('b.f1')
    return t.json()


def field_address():
    # Lesson 05, example 7, with a second field so the field address differs from the struct's.
    t = Trace('field-address', 'Field addresses',
              ['struct A { int f1; int f2; };', 'A a{};', 'int* b = &a.f2;', '*b = 5;',
               'std::cout << a.f2 << std::endl;'],
              [struct('a', 'A', 64, TWO_INTS), scalar('b', 72, 8, 'ptr')])
    t.statement(1, 'a = {0, 0}').write('a')
    t.statement(2).address('a.f2').write('b')
    t.statement(3).read('b').deref('*68', 'a.f2', 'b').write('a.f2')
    t.statement(4).print('a.f2')
    return t.json()


def shallow_copy():
    # Lesson 05, example 26. Clang: sizeof(A) = 16, with 4 bytes of tail padding.
    fields = [('pa', 0, 8, 'ptr'), ('a', 8, 4, 'int')]
    t = Trace('shallow-copy', 'Copying a structure with a pointer field',
              ['struct A { int* pa; int a; };', 'A s1 { .pa = nullptr, .a = 1 };',
               's1.pa = &s1.a;', 'A s2 { s1 };', '*s2.pa = 2;',
               'std::cout << s1.a << std::endl;', 'std::cout << s2.a << std::endl;'],
              [struct('s1', 'A', 64, fields, 16), struct('s2', 'A', 80, fields, 16)])
    t.statement(1, 's1 = {nullptr, 1}').write('s1')
    t.statement(2).address('s1.a').write('s1.pa')
    t.statement(3).read('s1').write('s2', hold=1.6)
    t.statement(4).read('s2.pa').deref('*72', 's1.a', 's2.pa').write('s1.a')
    t.statement(5).print('s1.a')
    t.statement(6).print('s2.a')
    return t.json()


PAGE = r'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Struct and pointer study</title>
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
<p><strong>Struct and pointer study.</strong> Struct variables, whole-struct copies, <code>.</code>
and <code>-&gt;</code>, and pointers to structs and to fields. Ints and fields 4 bytes, pointers 8,
addresses from 64. Variants differ only in how a struct groups its fields.</p>
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
const variants=['A','B'], variantNames=['Bracket below','Frame around'];
const descriptions=[
 'A · Bracket below: fields are ordinary cells in the struct\'s colour; a bracket and the struct name '
 +'sit under them. A pointer\'s arc ends on a bar spanning exactly what it points to: the whole struct, or one field.',
 'B · Frame around: a struct is a framed box holding its field cells. An arc to the struct lands on the '
 +'frame; an arc to a field lands on that field inside it.'];
let variant=new URLSearchParams(location.search).get('variant')||'A';
if(!variants.includes(variant)) variant='A';
let scenario=0,index=0,playing=false,timer,settleTimer;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mono='DejaVu Sans Mono,monospace', ease='calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"';
const FG='#eef3fa', MUTED='#a0afc2', GREY='#697382', READ='#9cbaff', WRITE='#f5e58b', CONTEXT='#6f7c8f';
const MEMX=640, BASE=64, codeChar=25*.602, evalChar=30*.602;
const T={prepare:0.55,travel:1.1,replace:0.2,settle:0.6,follow:0.9,writeHold:0.8,copyBegin:0.15,copyTravel:1.0};
const KEYWORDS=new Set(['int','std','cout','endl','struct','nullptr']);
const departure=op=>op.kind==='write'?T.writeHold:op.kind==='print'?0.2:T.prepare;
function arrival(op) {
 if(op.kind==='deref') return T.prepare+T.follow;
 if(op.kind==='print') return 0.9;
 return departure(op)+T.travel;
}
const opSeconds=op=>arrival(op)+T.settle+(op.kind==='write'?0.5:0);
const copySeconds=T.copyBegin+T.copyTravel+0.2;
function copies(i){const s=traces[scenario].steps; return i===0||s[i-1].line!==s[i].line;}
function stepSeconds(i){const s=traces[scenario].steps[i]; return s.hold+(s.op?opSeconds(s.op):copies(i)?copySeconds:0);}

function fade(from,to,dur=0.5,begin=0){return `<animate attributeName="opacity" from="${from}" to="${to}" dur="${dur}s" begin="${begin}s" ${ease} fill="freeze"/>`;}
function animateAttr(name,from,to,dur=0.45,begin=0){return `<animate attributeName="${name}" from="${from}" to="${to}" dur="${dur}s" begin="${begin}s" ${ease} fill="freeze"/>`;}
function animated(el,anims){return anims?el.replace(/\/>$/,'>'+anims+'</'+el.match(/^<(\w+)/)[1]+'>'):el;}
function text(x,y,value,size=26,color=FG,anchor='start'){
 return `<text x="${x}" y="${y}" font-family="${mono}" font-size="${size}" fill="${color}" text-anchor="${anchor}" xml:space="preserve">${esc(value)}</text>`;}
function rect(x,y,w,h,fill='#192331',stroke='none',radius=8,width=3){
 return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;}
function pulse(begin){return `<animateTransform attributeName="transform" type="scale" values="1;1.14;1" keyTimes="0;0.45;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" begin="${begin}s" dur="0.65s" fill="freeze"/>`;}
function markBox(x,y,len,stroke,fill){return `<rect x="${x-3}" y="${y-32}" width="${len*evalChar+6}" height="42" rx="6" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;}
function glide(markup,dx,begin,dur){return dx?`<g><animateTransform attributeName="transform" type="translate" from="0 0" to="${dx} 0" begin="${begin}s" dur="${dur}s" ${ease} fill="freeze"/>${markup}</g>`:markup;}
// Variables keep their colour; a field name after `.` or `->` stays neutral, like the lesson text.
function colored(x,y,value,trace,size=30,muteKeywords=true){
 let out='', member=false;
 for(const token of value.split(/(\b[a-zA-Z_]\w*\b)/)){
  const owner=!member&&(trace.groups.find(g=>g.name===token)||trace.leaves.find(l=>!l.group&&l.name===token));
  out+=text(x,y,token,size,owner?owner.color:muteKeywords&&KEYWORDS.has(token)?CONTEXT:FG);
  if(token) member=/(\.|->)$/.test(token);
  x+=token.length*size*.602;
 }
 return out;
}
function geometry(trace){
 const lh=56, h=44+trace.source.length*lh, top=Math.max(24,Math.round((720-h)/2));
 const g={code:[40,top,560,h],lh,cy:top+50,memY:262};
 g.pane=[640,462,600,76]; g.out=[664,598]; g.tx=664; g.ty=462+38+11;
 const end=Math.max(...trace.leaves.map(l=>l.address+l.size),...trace.groups.map(s=>s.address+s.size));
 const byte=Math.min(24,600/(end-BASE));
 const at=(address,size)=>({x:MEMX+(address-BASE)*byte,y:g.memY,w:size*byte,h:64});
 g.leaves=trace.leaves.map(l=>({...l,...at(l.address,l.size)}));
 g.groups=trace.groups.map(s=>({...s,...at(s.address,s.size),fieldsEnd:Math.max(...trace.leaves.filter(l=>l.group===s.name).map(l=>l.address+l.size))}));
 for(const s of g.groups) s.used=(s.fieldsEnd-s.address)*byte;
 return g;
}
const lineY=(g,i)=>g.cy+i*g.lh;
const leafNamed=(g,name)=>g.leaves.find(l=>l.name===name);
// A box is either one cell or a whole struct (its fields, without tail padding).
function box(g,name){
 const s=g.groups.find(s=>s.name===name);
 return s?{...s,w:s.used,group:true}:leafNamed(g,name);
}
const frameTop=c=>c.y-12;
function landingY(c){return variant==='B'&&c.group?frameTop(c)-2:c.y-9;}
const labelWidth=c=>String(c.address).length*16*.602;
const labelCenter=c=>[c.x+3+labelWidth(c)/2,c.y-(variant==='B'?28:20)-6];
const valueCenter=c=>[c.x+c.w/2,c.y+32];
function leavesOf(g,name){const s=g.groups.find(s=>s.name===name); return s?g.leaves.filter(l=>l.group===name):[leafNamed(g,name)];}

// Persistent pointer arcs, as locked in #59: both ends near the centre, spread when shared.
function links(g,step){
 const list=g.leaves.filter(l=>l.kind==='ptr'&&step.targets[l.name]).map(l=>({from:l,to:box(g,step.targets[l.name])}));
 const centre=c=>c.x+c.w/2, ports=new Map();
 const key=c=>c.name;
 for(const l of list) for(const [cell,other,k] of [[l.from,l.to,'sx'],[l.to,l.from,'ex']]) {
  if(!ports.has(key(cell))) ports.set(key(cell),{cell,ends:[]});
  ports.get(key(cell)).ends.push({l,k,other:centre(other)});
 }
 for(const {cell,ends} of ports.values()) {
  const side=end=>end.other<centre(cell)?0:1;
  ends.sort((p,q)=>side(p)-side(q)||q.other-p.other);
  ends.forEach((end,i)=>end.l[end.k]=centre(cell)+(i-(ends.length-1)/2)*20);
 }
 const range=l=>[Math.min(l.sx,l.ex),Math.max(l.sx,l.ex)];
 for(const l of list) {
  const [a,b]=range(l), {sx,ex}=l;
  l.level=list.filter(o=>o!==l&&range(o)[0]>=a&&range(o)[1]<=b).length;
  const sy=l.from.y-2, ey=landingY(l.to), apex=g.memY-112-l.level*40;
  l.d=`M ${sx} ${sy} C ${sx} ${apex}, ${ex} ${apex}, ${ex} ${ey-9}`; l.head=[ex,ey,90];
 }
 return list;
}
function linkMarkup(l,{grow=null,fadeOut=null}={}) {
 const [x,y,angle]=l.head, color=l.from.color;
 const head=`<path d="M -11 -6.5 L 0 0 L -11 6.5 Z" fill="${color}" transform="translate(${x} ${y}) rotate(${angle})"/>`;
 // Variant A: a bar spanning the pointee says how much the pointer designates.
 const bar=variant==='A'?`<rect x="${l.to.x+3}" y="${l.to.y-8}" width="${l.to.w-6}" height="3" rx="1.5" fill="${color}"/>`:'';
 return `<g data-link="${l.from.name}"${grow!==null?' opacity="1"':''}>`
  +(fadeOut!==null?fade(1,0,0.3,fadeOut):'')
  +`<path d="${l.d}" fill="none" stroke="#101722" stroke-width="9"`+(grow!==null?` data-grow="${grow}"`:'')+'/>'
  +`<path d="${l.d}" fill="none" stroke="${color}" stroke-width="2.5"`
  +(grow!==null?` data-grow="${grow}"`:'')+'/>'
  +(grow!==null?`<g opacity="0">${fade(0,1,0.15,grow+0.5)}${head}${bar}</g>`:head+bar)+'</g>';
}
function arrows(g,step,prev,op){
 const now=links(g,step);
 const writesPointer=op?.kind==='write'&&leavesOf(g,op.name).some(l=>l.kind==='ptr');
 if(writesPointer) {
  const at=arrival(op), before=links(g,prev), changed=new Set(leavesOf(g,op.name).map(l=>l.name));
  let out='';
  for(const l of before) out+=linkMarkup(l,changed.has(l.from.name)?{fadeOut:at}:{});
  for(const l of now) if(changed.has(l.from.name)) out+=linkMarkup(l,{grow:at+0.1});
  return out;
 }
 let out=now.map(l=>linkMarkup(l)).join('');
 if(op?.kind==='deref') {
  const l=now.find(l=>l.from.name===op.via);
  if(l) out+=`<path d="${l.d}" fill="none" stroke="${l.from.color}" stroke-width="7" stroke-linecap="round" data-follow="${T.prepare}"/>`;
 }
 return out;
}
function outline(c,color,inset=4.5){return rect(c.x+inset,c.y+inset,c.w-2*inset,c.h-2*inset,'none',color,0,3);}
function memory(trace,g,step,prev,op){
 const values=op?.kind==='write'?prev.values:step.values, at=op?arrival(op):0;
 const live=l=>values[l.name]!==null||(op?.kind==='write'&&leavesOf(g,op.name).includes(l));
 let out='';
 // Unused bytes (tail padding, gaps between variables) are dashed, as in the pointer study.
 const spans=g.leaves.map(l=>[l.address,l.address+l.size]).sort((a,b)=>a[0]-b[0]);
 const end=Math.max(...g.groups.map(s=>s.address+s.size),...spans.map(s=>s[1]));
 const byte=g.leaves[0].w/g.leaves[0].size;
 let cursor=BASE;
 for(const [a,b] of [...spans,[end,end]]){
  if(a>cursor) out+=`<rect x="${MEMX+(cursor-BASE)*byte+3}" y="${g.memY+3}" width="${(a-cursor)*byte-6}" height="58" fill="none" stroke="#2c3442" stroke-dasharray="5 5"/>`;
  cursor=Math.max(cursor,b);
 }
 for(const s of g.groups){
  const on=g.leaves.some(l=>l.group===s.name&&live(l)), color=on?s.color:'#47515f';
  if(variant==='A'){
   const y=s.y+s.h+46;
   out+=`<path d="M ${s.x+4} ${y-8} V ${y} H ${s.x+s.used-4} V ${y-8}" fill="none" stroke="${on?MUTED:GREY}" stroke-width="2"/>`;
   out+=text(s.x+s.used/2,y+32,s.name,26,on?s.color:GREY,'middle');
  } else {
   out+=rect(s.x-2,frameTop(s),s.used+4,s.h+24+30,'none',color,10,2.5);
   out+=text(s.x+s.used/2,s.y+s.h+76,s.name,26,on?s.color:GREY,'middle');
  }
 }
 if(op?.kind==='addr'){
  const c=leavesOf(g,op.name)[0], [lx,ly]=labelCenter(c);
  out+=`<g opacity="0">${fade(0,1,0.15)}${fade(1,0,0.2,at+0.1)}${rect(lx-labelWidth(c)/2-5,ly-13,labelWidth(c)+10,24,'#2c4775',READ,5,2)}</g>`;
 }
 for(const c of g.leaves){
  const on=live(c), changing=op?.kind==='write'&&leavesOf(g,op.name).includes(c);
  const addressY=c.y-(variant==='B'?28:20);
  out+=text(c.x+3,addressY,c.address,16,on?MUTED:GREY);
  out+=c.group?text(c.x+c.w/2,c.y+c.h+28,c.label,20,on?c.color:GREY,'middle')
   :text(c.x+c.w/2,c.y+c.h+34,c.label,26,on?c.color:GREY,'middle');
  out+=rect(c.x,c.y,c.w,c.h,on?'#192331':'#171d27','none',0);
  // In B the frame carries the struct colour, so its fields use a quieter outline.
  const border=!on?'#47515f':variant==='B'&&c.group?'#55657a':c.color;
  out+=rect(c.x+1.5,c.y+1.5,c.w-3,c.h-3,'none',border,0,variant==='B'&&c.group?2:3);
  if(!on) continue;
  const [cx,cy]=[c.x+c.w/2,c.y+c.h/2], value=values[c.name], size=String(value).length*18>c.w-12?22:30;
  const shown=v=>text(0,size/3+1,v,size,v==='?'?GREY:FG,'middle');
  out+=`<g transform="translate(${cx} ${cy})"><g>`+(changing?pulse(at-0.2):'');
  if(changing && prev.values[c.name]!==step.values[c.name]) {
   if(prev.values[c.name]!==null) out+=`<g>${fade(1,0,T.replace,at)}${shown(prev.values[c.name])}</g>`;
   out+=`<g opacity="0">${fade(0,1,T.replace,at)}${shown(step.values[c.name])}</g>`;
  } else out+=shown(changing?step.values[c.name]:value);
  out+='</g></g>';
 }
 // Highlights cover a whole struct for struct operations and one cell for field operations.
 if(op?.kind==='read'||op?.kind==='write'){
  const c=box(g,op.name), color=op.kind==='write'?WRITE:READ;
  out+=`<g>${fade(1,0,0.35,at+0.15)}${outline(c,color)}</g>`;
 }
 if(op?.kind==='deref')
  out+=`<g opacity="0">${fade(0,1,0.2,at-0.15)}${outline(box(g,op.target),FG)}</g>`;
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
 const at=arrival(op), begin=departure(op), ty=g.ty-11, below=g.memY+150;
 const spanCenter=(s,len)=>g.tx+(s+len/2)*evalChar;
 if(op.kind==='read'){
  const [sx,sy]=valueCenter(box(g,op.name)), dx=spanCenter(op.span[0],String(op.value).length);
  return valueBox(op.value,READ,`M ${sx} ${sy} C ${sx} ${below}, ${dx} ${below}, ${dx} ${ty}`,begin,T.travel,at);
 }
 if(op.kind==='addr'){
  // The address comes from the label above storage: taking an address reads no value.
  const c=leavesOf(g,op.name)[0], [sx,sy]=labelCenter(c), dx=spanCenter(op.span[0],op.value.length);
  const side=c.x-20;
  return valueBox(op.value,READ,`M ${sx} ${sy} C ${side} ${sy}, ${side} ${g.memY+64}, ${side} ${below} C ${side} ${ty}, ${dx} ${ty-60}, ${dx} ${ty}`,begin,T.travel,at);
 }
 if(op.kind==='write'){
  const sx=spanCenter(step.pane.lastIndexOf('= ')+2,op.value.length);
  const [ex,ey]=valueCenter(box(g,op.name));
  return valueBox(op.value,WRITE,`M ${sx} ${ty} C ${sx} ${below}, ${ex} ${below}, ${ex} ${ey}`,begin,T.travel,at);
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
  out+=`<g>${fade(1,0,T.replace,at)}${colored(tx+s*evalChar,ty,before.slice(s,e),trace)}</g>`;
  out+=`<g opacity="0">${fade(0,1,T.replace,at)}${colored(tx+s*evalChar,ty,step.pane.slice(s,s+len),trace)}</g>`;
  return out+glide(colored(tx+e*evalChar,ty,before.slice(e),trace),dx,at,T.replace);
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
 trace.source.forEach((src,i)=>{out+=text(g.code[0]+22,lineY(g,i),i+1,18,MUTED)+colored(g.code[0]+62,lineY(g,i),src,trace,25,i===0);});
 return out;
}
function describe(step){
 const op=step.op;
 if(!op) return 'Copy line '+(step.line+1)+' into evaluation';
 return {read:()=>`Read ${op.name}: ${op.value}`,
  addr:()=>`Take the address of ${op.name}: ${op.value} (no value is read)`,
  deref:()=>`Follow the address: the location is ${op.target}`,
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
 out+=`<path d="M ${g.code[0]+g.code[2]+5} ${lineY(g,step.line)-10} H ${g.code[0]+g.code[2]+20} V ${g.pane[1]+38} H ${g.pane[0]}" fill="none" stroke="#697d99" stroke-width="2"/>`;
 out+=arrows(g,step,prev,op)+memory(trace,g,step,prev,op)+pane(trace,g,step,prev,op,copying,lineChanged)
  +output(g,step,prev,op)+transfers(g,step,prev,op);
 const svg=$('stage'); svg.innerHTML=out; finishPaths(); svg.setCurrentTime(0);
 $('description').textContent=descriptions[variants.indexOf(variant)];
 $('variantName').textContent=variant+' · '+variantNames[variants.indexOf(variant)];
 $('scrub').max=trace.steps.length-1; $('scrub').value=index;
 $('count').textContent=`${index+1} / ${trace.steps.length}`;
 $('state').textContent=describe(step)+' · '+trace.leaves.map(c=>c.name+' = '
  +(step.values[c.name]===null?'unallocated':step.values[c.name])
  +(step.targets[c.name]?' → '+step.targets[c.name]:'')).join(' · ')
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
function changeVariant(d){variant=variants[(variants.indexOf(variant)+d+2)%2];
 const url=new URL(location.href);url.searchParams.set('variant',variant);
 try{history.replaceState(null,'',url);}catch(error){if(error.name!=='SecurityError')throw error;}
 draw();}
$('prevVariant').onclick=()=>changeVariant(-1);$('nextVariant').onclick=()=>changeVariant(1);
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select,[contenteditable]'))return;
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();changeVariant(e.key==='ArrowLeft'?-1:1);}});
draw();
</script>
</html>'''

TRACES = [copy_assignment(), arrow_operator(), copy_through_pointer(), field_address(),
          shallow_copy()]

if __name__ == '__main__':
    target = Path(__file__).with_name('struct-pointer-prototype.html')
    target.write_text(PAGE.replace('__TRACES__', json.dumps(TRACES).replace('<', '\\u003c')))
    print(target)
