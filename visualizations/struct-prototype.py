"""THROWAWAY struct-layout study for #62: two static ways to show fields and padding, ?variant=A/C.

Question: how should struct layout and alignment look? It should replace the hand-made
`05_struct_alignment.svg`. DECIDED: static, not animated; either layout is acceptable.
Hovering or clicking a source row highlights its bytes, and hovering memory highlights the row.

Layouts come from the compiler: Clang's record-layout dump gives field offsets, sizeof and
alignment; a tiny compiled probe gives each field's size and alignment. Set CLANGXX when
clang++ is not on PATH. Without Clang, the last captured layouts in CAPTURED are used.

Run from the course root: python3 visualizations/struct-prototype.py
Then open visualizations/struct-prototype.html.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

STRUCTS = {
    'A': ['struct A', '{', '    uint8_t f1;', '    int f2;', '    uint8_t f3;', '};',
          'std::cout << sizeof(A);'],
    'B': ['struct B', '{', '    uint8_t f1;', '    int* p;', '    int f2;', '};',
          'std::cout << sizeof(B);'],
}
COLORS = ('#61d4c4', '#ffbd69', '#c39bff', '#ff8fb1')
# Output of compiler_layouts() on x86-64 Clang 21, used only when Clang is unavailable.
CAPTURED = {
    'A': dict(size=12, align=4, fields=[
        dict(type='uint8_t', name='f1', offset=0, size=1, align=1),
        dict(type='int', name='f2', offset=4, size=4, align=4),
        dict(type='uint8_t', name='f3', offset=8, size=1, align=1),
    ]),
    'B': dict(size=24, align=8, fields=[
        dict(type='uint8_t', name='f1', offset=0, size=1, align=1),
        dict(type='int*', name='p', offset=8, size=8, align=8),
        dict(type='int', name='f2', offset=16, size=4, align=4),
    ]),
}


def compiler_layouts() -> dict:
    """Ask Clang for each struct's layout; the renderer consumes only this data."""
    clang = os.environ.get('CLANGXX') or shutil.which('clang++')
    if not clang:
        raise FileNotFoundError('clang++')
    definitions = '\n'.join('\n'.join(lines[:-1]) for lines in STRUCTS.values())
    with tempfile.TemporaryDirectory(prefix='struct-layout-') as directory:
        source = Path(directory) / 'layout.cpp'
        source.write_text('#include <cstdint>\n' + definitions + '\n'
                          + ''.join(f'{name} instance{name};\n' for name in STRUCTS))
        dump = subprocess.run([clang, '-std=c++20', '-Xclang', '-fdump-record-layouts',
                               '-fsyntax-only', str(source)],
                              capture_output=True, text=True, check=True).stdout
        records = {}
        for block in dump.split('*** Dumping AST Record Layout')[1:]:
            rows = [line.split('|', 1) for line in block.strip().splitlines()]
            name = rows[0][1].split()[-1]
            if name not in STRUCTS:
                continue
            fields = []
            for offset, declaration in rows[1:]:
                match = re.fullmatch(r'\s+(.+?)\s*(\w+)', declaration)
                if offset.strip() and match:
                    fields.append(dict(type=match[1].replace(' *', '*'), name=match[2],
                                       offset=int(offset)))
            summary = dict(re.findall(r'(\w+)=(\d+)', block))
            records[name] = dict(fields=fields, size=int(summary['sizeof']),
                                 align=int(summary['align']))
        # The dump has offsets but not field sizes; a probe asks the compiler for those.
        probe = source.with_name('probe.cpp')
        probe.write_text('#include <iostream>\n' + source.read_text() + 'int main() {\n' + ''.join(
            f'    std::cout << sizeof(decltype({s}::{f["name"]})) << " "'
            f' << alignof(decltype({s}::{f["name"]})) << "\\n";\n'
            for s, record in records.items() for f in record['fields']) + '}\n')
        binary = probe.with_suffix('')
        subprocess.run([clang, '-std=c++20', str(probe), '-o', str(binary)],
                       capture_output=True, check=True)
        sizes = iter(subprocess.run([str(binary)], capture_output=True, text=True,
                                    check=True).stdout.split('\n'))
        for record in records.values():
            for field in record['fields']:
                field['size'], field['align'] = map(int, next(sizes).split())
    return records


def structs(layouts: dict) -> list[dict]:
    result = []
    for name, source in STRUCTS.items():
        record = layouts[name]
        for i, field in enumerate(record['fields']):
            field['color'] = COLORS[i]
            field['line'] = next(n for n, line in enumerate(source)
                                 if re.search(r'\b' + field['name'] + r';', line))
        result.append(dict(name=name, title=f'struct {name}', source=source, **record))
    return result


PAGE = r'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Struct layout study</title>
<style>
:root {color-scheme:dark; font-family:system-ui; color:#eef3fa; background:#0c121b}
body {margin:0 auto; max-width:1280px; padding:12px 16px 84px}
button,select {font:inherit; color:inherit; background:#233044; border:1px solid #47515f;
 border-radius:8px; padding:8px 12px; cursor:pointer}
button:disabled {opacity:.4; cursor:default}
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
.row, .item {cursor:pointer}
.row .mark {opacity:0}
.row.on .mark {opacity:1}
.item {transition:opacity .15s}
#stage.focus .item:not(.on) {opacity:.22}
.item .glow {opacity:0}
.item.on .glow {opacity:1}
</style>
<p><strong>Prototype #62.</strong> Field offsets, sizes, sizeof and alignment come from Clang
(<span id="origin"></span>). Hover or click a source row, or a part of memory, to link the two.</p>
<div class="controls">
 <label>Example <select id="scenario"></select></label>
</div>
<svg id="stage" viewBox="0 0 1280 720" role="img" aria-label="Struct definition and its layout"></svg>
<p id="description"></p><div id="state" aria-live="polite"></div>
<nav id="switcher" aria-label="Prototype variant">
 <button id="prevVariant" aria-label="Previous variant">←</button><span id="variantName"></span>
 <button id="nextVariant" aria-label="Next variant">→</button>
</nav>
<script>
const structs=__STRUCTS__, origin=__ORIGIN__;
const variants=['A','C'], variantNames=['Byte row','Slot grid'];
const descriptions=[
 'A · Byte row: one continuous row of bytes at a fixed scale, like stack memory. Fields keep their '
 +'colors, padding is hatched, offsets sit above and slot brackets mark the alignment unit.',
 'C · Slot grid: the lesson\'s slot model drawn literally. One row per alignment slot, offsets on '
 +'the left; a field that does not fit the rest of a row starts the next one.'];
let variant=new URLSearchParams(location.search).get('variant')||'A';
if(!variants.includes(variant)) variant='A';
let scenario=0,locked=null;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mono='DejaVu Sans Mono,monospace';
const FG='#eef3fa', MUTED='#a0afc2', GREY='#697382', READ='#9cbaff', WRITE='#f5e58b';
const codeChar=25*.602, evalChar=30*.602, BYTE=28, ROWX=520;
function text(x,y,value,size=26,color=FG,anchor='start'){
 return `<text x="${x}" y="${y}" font-family="${mono}" font-size="${size}" fill="${color}" text-anchor="${anchor}" xml:space="preserve">${esc(value)}</text>`;}
function rect(x,y,w,h,fill='#192331',stroke='none',radius=8,width=3){
 return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;}
function colored(x,y,value,s,size=25){
 let out='';
 for(const token of value.split(/(\b[a-zA-Z_]\w*\b)/)){
  const field=s.fields.find(f=>f.name===token);
  out+=text(x,y,token,size,field?field.color:FG); x+=token.length*size*.602;
 }
 return out;
}
const defs='<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
 +'<rect width="8" height="8" fill="#151c27"/><line x1="0" y1="0" x2="0" y2="8" stroke="#3a4554" stroke-width="3"/></pattern></defs>';
// Padding ranges between fields and at the tail, derived only from compiler offsets and sizes.
function gaps(s){
 const out=[]; let end=0;
 for(const f of s.fields){ if(f.offset>end) out.push({offset:end,size:f.offset-end,before:f}); end=f.offset+f.size; }
 if(s.size>end) out.push({offset:end,size:s.size-end,tail:true});
 return out;
}
// The source row that owns each part of memory: a field's own line, or the whole struct.
function rowKey(s,i){const f=s.fields.findIndex(f=>f.line===i); return f>=0?'f'+f:'all';}
function code(s){
 const h=44+s.source.length*56, top=Math.round((720-h)/2), g={x:40,y:top,w:440,h,cy:top+50};
 let out=rect(g.x,g.y,g.w,g.h);
 s.source.forEach((src,i)=>{
  const y=g.cy+i*56, len=src.trimEnd().replace(/;$/,'').length;
  out+=`<g class="row" data-key="${rowKey(s,i)}" tabindex="0" role="button" aria-label="Highlight ${esc(src.trim())}">`
   +`<rect x="${g.x}" y="${y-36}" width="${g.w}" height="52" fill="#000" fill-opacity="0"/>`
   +`<g class="mark">${rect(g.x+8,y-32,4,44,READ,'none',0)+rect(g.x+59,y-30,len*codeChar+6,40,'#2e4059','none',6)}</g>`
   +text(g.x+22,y,i+1,18,MUTED)+colored(g.x+62,y,src,s)+'</g>';
 });
 return {out,g};
}
// Wraps memory markup so hovering it and hovering its source row highlight each other.
const item=(key,markup)=>`<g class="item" data-key="${key}">${markup}</g>`;
// A continuous byte row at a fixed scale; shared by variants A and B.
function byteRow(s,y){
 let out='';
 const x=o=>ROWX+o*BYTE, h=64;
 out+=rect(x(0),y,s.size*BYTE,h,'#171d27','#47515f',0,2);
 for(let o=1;o<s.size;o++) out+=`<line x1="${x(o)}" y1="${y+h-10}" x2="${x(o)}" y2="${y+h}" stroke="#47515f" stroke-width="1"/>`;
 // Slot brackets above the offsets mark the alignment unit.
 for(let o=0;o<s.size;o+=s.align){
  const a=x(o)+3,b=x(o+s.align)-3,top=y-50;
  out+=`<path d="M ${a} ${top+8} V ${top} H ${b} V ${top+8}" fill="none" stroke="#47515f" stroke-width="2"/>`;
 }
 for(const gap of gaps(s)) out+=item('pad',rect(x(gap.offset)+2,y+2,gap.size*BYTE-4,h-4,'url(#hatch)','none',0)
  // The label sits inside the hatching, so it never competes with field names below.
  +(gap.size*BYTE>=80?rect(x(gap.offset)+gap.size*BYTE/2-38,y+22,76,24,'#151c27','none',4)
    +text(x(gap.offset)+gap.size*BYTE/2,y+40,'padding',16,MUTED,'middle'):'')
  +text(x(gap.offset),y-14,gap.offset,16,GREY));
 s.fields.forEach((f,i)=>out+=item('f'+i,rect(x(f.offset),y,f.size*BYTE,h,'#192331','none',0)
  +rect(x(f.offset)+1.5,y+1.5,f.size*BYTE-3,h-3,'none',f.color,0,3)
  +`<g class="glow">${rect(x(f.offset)+5,y+5,f.size*BYTE-10,h-10,'none',READ,0,3)}</g>`
  +Array.from({length:f.size-1},(_,k)=>`<line x1="${x(f.offset+k+1)}" y1="${y+h-12}" x2="${x(f.offset+k+1)}" y2="${y+h-3}" stroke="${f.color}" stroke-opacity=".5"/>`).join('')
  +text(x(f.offset)+f.size*BYTE/2,y+40,f.size*BYTE>=70?f.type:'',20,MUTED,'middle')
  +text(x(f.offset),y-14,f.offset,16,MUTED)+text(x(f.offset)+f.size*BYTE/2,y+h+30,f.name,24,f.color,'middle')));
 out+=text(x(s.size),y-14,s.size,16,MUTED);
 return out;
}
function sizeBracket(s,y){
 const a=ROWX, b=ROWX+s.size*BYTE;
 return item('size',`<path d="M ${a} ${y} V ${y+8} H ${b} V ${y}" fill="none" stroke="${MUTED}" stroke-width="2"/>`
  +text((a+b)/2,y+38,`sizeof(${s.name}) = ${s.size}`,24,FG,'middle'));
}
function variantA(s){
 const {out}=code(s), y=300;
 return out+byteRow(s,y)+sizeBracket(s,y+108);
}
function variantC(s){
 const {out}=code(s), cell=56, width=s.align*cell, x0=ROWX+60, rows=s.size/s.align;
 const top=Math.round((720-rows*72)/2)-30;
 let svg=out;
 for(let r=0;r<rows;r++){
  const y=top+r*72;
  svg+=text(x0-16,y+40,r*s.align,18,MUTED,'end')+rect(x0,y,width,56,'#171d27','#47515f',0,2);
  for(let b=1;b<s.align;b++) svg+=`<line x1="${x0+b*cell}" y1="${y+46}" x2="${x0+b*cell}" y2="${y+56}" stroke="#47515f"/>`;
 }
 const place=(offset,size)=>{
  // A field never straddles slots here; padding may span several rows.
  const parts=[]; let o=offset, left=size;
  while(left>0){const r=Math.floor(o/s.align), c=o%s.align, n=Math.min(left,s.align-c); parts.push([x0+c*cell,top+r*72,n*cell]); o+=n; left-=n;}
  return parts;
 };
 for(const gap of gaps(s)) for(const [x,y,w] of place(gap.offset,gap.size))
  svg+=item('pad',rect(x+2,y+2,w-4,52,'url(#hatch)','none',0)+(w>=150?text(x+w/2,y+35,'padding',18,GREY,'middle'):''));
 s.fields.forEach((f,i)=>{for(const [x,y,w] of place(f.offset,f.size))
  svg+=item('f'+i,rect(x,y,w,56,'#192331','none',0)+rect(x+1.5,y+1.5,w-3,53,'none',f.color,0,3)
   +`<g class="glow">${rect(x+5,y+5,w-10,46,'none',READ,0,3)}</g>`
   +text(x+w/2,y+36,w>=150?`${f.type} ${f.name}`:f.name,22,f.color,'middle'));});
 const y=top+rows*72+30;
 svg+=item('size',text(x0,y,`sizeof(${s.name}) = ${rows} slots × ${s.align} = ${s.size}`,24,FG));
 svg+=text(x0+width+28,top+40,`slot = ${s.align} bytes`,18,MUTED);
 return svg;
}
function focusKey(key){
 const svg=$('stage');
 svg.classList.toggle('focus',key!==null);
 // A struct-level row (the definition or sizeof) highlights every byte, padding included.
 for(const el of svg.querySelectorAll('.item')) el.classList.toggle('on',key==='all'||el.dataset.key===key);
 for(const el of svg.querySelectorAll('.row')) el.classList.toggle('on',key!==null&&(el.dataset.key===key||
  (key==='pad'||key==='size')&&el.dataset.key==='all'));
}
function draw(){
 const s=structs[scenario];
 const body={A:variantA,C:variantC}[variant](s);
 const svg=$('stage'); svg.innerHTML=defs+body; locked=null; focusKey(null);
 $('origin').textContent=origin;
 $('description').textContent=descriptions[variants.indexOf(variant)];
 $('variantName').textContent=variant+' · '+variantNames[variants.indexOf(variant)];
 $('state').textContent=s.fields.map(f=>`${f.type} ${f.name} @${f.offset} (${f.size} B, align ${f.align})`).join(' · ')
  +` · sizeof=${s.size}, align=${s.align}`;
}
const keyOf=e=>e.target.closest?.('.row,.item')?.dataset.key??null;
$('stage').addEventListener('pointerover',e=>{if(locked===null) focusKey(keyOf(e));});
$('stage').addEventListener('pointerleave',()=>focusKey(locked));
$('stage').addEventListener('click',e=>{const key=keyOf(e); locked=key===locked?null:key; focusKey(locked);});
$('stage').addEventListener('focusin',e=>focusKey(keyOf(e)));
$('stage').addEventListener('focusout',()=>focusKey(locked));
$('stage').addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();
 const key=keyOf(e); locked=key===locked?null:key; focusKey(locked);}});
structs.forEach((s,i)=>$('scenario').add(new Option(s.title,i)));
$('scenario').onchange=e=>{scenario=Number(e.target.value);draw();};
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

if __name__ == '__main__':
    try:
        layouts, origin = compiler_layouts(), 'live Clang record layouts'
    except (OSError, subprocess.CalledProcessError) as error:
        if CAPTURED is None:
            raise SystemExit(f'Clang is required (set CLANGXX): {error}')
        layouts, origin = CAPTURED, 'captured Clang layouts; Clang was unavailable'
    target = Path(__file__).with_name('struct-prototype.html')
    target.write_text(PAGE.replace('__STRUCTS__', json.dumps(structs(layouts)))
                      .replace('__ORIGIN__', json.dumps(origin)))
    print(target)
