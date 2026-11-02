"""Build a self-contained, disposable review page from the rendered artifacts."""
import base64
import json
from pathlib import Path

from drawing import frame, svg
from model import TIMELINES

ROOT = Path(__file__).parent


def review_html():
    examples = {}
    for timeline in TIMELINES:
        examples[timeline.name] = {
            "frames": [svg(frame(timeline, i), timeline.title)
                       for i in range(len(timeline.steps))],
            "video": "data:video/mp4;base64," + base64.b64encode(
                (ROOT / "renders" / f"{timeline.name}.mp4").read_bytes()).decode(),
        }
    return '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Expression timeline · prototype #57</title>
<style>
:root { color-scheme: light dark; }
body { margin:0; font:15px/1.5 var(--font-sans,system-ui); color:var(--foreground); }
p { margin:0 0 12px; }
nav, .controls { display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin:12px 0; }
button { padding:8px 12px; border:1px solid var(--border,#65758b); border-radius:6px;
 background:var(--secondary,#263549); color:var(--secondary-foreground,#eef3fa); cursor:pointer; }
button[aria-pressed=true] { outline:2px solid var(--primary,#61d4c4); }
video, svg { display:block; width:100%; height:auto; border-radius:8px; }
input { flex:1; min-width:160px; }
label { display:flex; flex:1; gap:12px; }
summary { cursor:pointer; margin-top:16px; }
small { color:var(--muted-foreground,#8b9bb0); }
</style>
<body>
<p>Prototype #57: can the same visual language explain copying an expression result
and losing a value during a failed swap?</p>
<nav aria-label="Example">
<button data-case="expression" aria-pressed="true">Expression</button>
<button data-case="swap" aria-pressed="false">Failed swap</button>
</nav>
<video id="movie" controls playsinline preload="metadata" aria-label="Execution animation"></video>
<details open><summary>Inspect individual states</summary>
<div class="controls"><button id="back" aria-label="Previous state">←</button>
<label>State <input id="step" type="range" min="0" value="0"></label>
<output id="counter"></output><button id="next" aria-label="Next state">→</button></div>
<div id="snapshot"></div></details>
<p><small>Illustrative ABI: 4-byte int, 8-byte pointer, little-endian; synthetic decimal
addresses start at 64. Each int occupies one slot; byte detail is reserved for byte-level
examples. ? marks an unknown value, including a declaration that has not executed.
Variable names are below their slots; starting addresses are above. Slots wrap as whole integers.
Blue outlines mark reads; yellow outlines mark writes. Expression evaluation shows temporary
results; a copied value moves into the subexpression it replaces.
Fixed dark media background is provisional. No automatic C++ tracing or maintenance integration.</small></p>
<script>
const examples = EXAMPLES;
let selected = 'expression';
const movie=document.querySelector('#movie'), step=document.querySelector('#step');
function draw() {
 const frames=examples[selected].frames;
 document.querySelector('#snapshot').innerHTML=frames[+step.value];
 document.querySelector('#counter').textContent=`${+step.value+1} / ${frames.length}`;
 document.querySelector('#back').disabled=+step.value===0;
 document.querySelector('#next').disabled=+step.value===frames.length-1;
}
function choose(name) {
 movie.pause(); selected=name; movie.src=examples[name].video;
 step.max=examples[name].frames.length-1; step.value=0;
 document.querySelectorAll('[data-case]').forEach(button=>
  button.setAttribute('aria-pressed',button.dataset.case===name));
 draw();
}
document.querySelectorAll('[data-case]').forEach(button=>
 button.onclick=()=>choose(button.dataset.case));
step.oninput=draw;
document.querySelector('#back').onclick=()=>{step.value=Math.max(0,+step.value-1);draw();};
document.querySelector('#next').onclick=()=>{step.value=Math.min(+step.max,+step.value+1);draw();};
choose(selected);
</script></body></html>'''.replace('EXAMPLES', json.dumps(examples))


if __name__ == "__main__":
    path = ROOT / "review.html"
    path.write_text(review_html())
    print(path)
