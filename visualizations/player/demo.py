#!/usr/bin/env python3
"""Write `demo.html`: the player inside a lesson-like page, for checking the engine locally.

It traces a few examples from `en/labs/cpp/02_variables.md` with the compiler-backed tracer and
adds the pointer and struct fixtures. Each player sits in a collapsed `<details>`, as on the
site; the buttons in the header switch `<html data-theme>` and `lang`, as Starlight does.
Run from the course root, inside the default shell (Clang and GDB):
  nix develop --command python3 visualizations/player/demo.py
Then open visualizations/player/demo.html (git-ignored).
"""
from html import escape
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from trace_format import from_timeline, validate  # noqa: E402
from tracing import trace  # noqa: E402

# Lesson 02 examples 4, 5, 10 and 18.
EXAMPLES = {
    'Assigning one variable to another':
        'int a = 5;\nint b = 6;\na = b;\nb = 7;\nstd::cout << a << std::endl;\n',
    'Literals, variables and operators are expressions':
        'int a = 5;\nint b = a;\nint c = a + 6;\nstd::cout << b << std::endl;\nstd::cout << c << std::endl;\n',
    'Empty initialization': 'int a{};\nstd::cout << a << std::endl;\n',
    'Swapping variables':
        'int a { 1 };\nint b { 2 };\na = b;\nb = a;\nstd::cout << a << std::endl;\nstd::cout << b << std::endl;\n',
}

PAGE = '''<!doctype html>
<html lang="en" data-theme="dark">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Player demo</title>
<script>
// Starlight sets these before paint; ?theme= and ?lang= let screenshots pick them.
const query = new URLSearchParams(location.search);
document.documentElement.dataset.theme = query.get('theme') || 'dark';
document.documentElement.lang = query.get('lang') || 'en';
</script>
<link rel="stylesheet" href="player.css">
<script defer src="player.js"></script>
<style>
:root {color-scheme: dark; --page: #17181c; --text: #dfe3ea; --muted: #9aa1ae; --code: #23262e;
 --line: #353945}
:root[data-theme=light] {color-scheme: light; --page: #ffffff; --text: #23262f; --muted: #5d6573;
 --code: #f4f5f8; --line: #dde1e8}
* {box-sizing: border-box}
body {margin: 0; background: var(--page); color: var(--text);
 font: 16px/1.6 system-ui, -apple-system, 'Segoe UI', sans-serif}
header {position: sticky; top: 0; z-index: 2; display: flex; gap: 8px; align-items: center;
 padding: 10px 16px; border-bottom: 1px solid var(--line); background: var(--page)}
header strong {margin-right: auto}
header button {font: inherit; font-size: 14px; color: inherit; background: var(--code);
 border: 1px solid var(--line); border-radius: 6px; padding: 4px 10px; cursor: pointer}
main {max-width: 45rem; margin: 0 auto; padding: 1rem 1rem 4rem}
h2 {font-size: 1.35rem; margin: 2.2rem 0 .8rem}
pre {background: var(--code); border: 1px solid var(--line); border-radius: 6px;
 padding: .8rem 1rem; overflow-x: auto; font-size: .875rem}
details {border-left: 3px solid var(--line); padding: .2rem 0 .2rem 1rem; margin: 1rem 0}
summary {cursor: pointer; font-weight: 600}
p {color: var(--muted)}
</style>
<header><strong>Player demo</strong>
 <button id="theme" type="button">Theme</button><button id="lang" type="button">Language</button></header>
<main>
<p>Compiler-traced examples from lesson 2, then the manual pointer and struct fixtures.
The first trace is already open; the others initialize when opened.</p>
__SECTIONS__
</main>
<script>
document.getElementById('theme').onclick = () => {
  const root = document.documentElement;
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
};
document.getElementById('lang').onclick = () => {
  const url = new URL(location.href);
  url.searchParams.set('lang', document.documentElement.lang === 'en' ? 'ru' : 'en');
  url.searchParams.set('theme', document.documentElement.dataset.theme);
  location.href = url;
};
</script>
</html>
'''


def section(index: int, title: str, data: dict, opened: bool) -> str:
    validate(data)
    payload = json.dumps(data, sort_keys=True).replace('<', '\\u003c')
    source = escape('\n'.join(data['source']))
    return (f'<h2 id="trace-{index}">{index}. {escape(title)}</h2>\n<pre><code>{source}</code></pre>\n'
            f'<details{" open" if opened else ""}><summary>Execution trace</summary>\n'
            f'<div class="course-visualization"><script type="application/json">{payload}</script></div>\n'
            '</details>')


def main() -> None:
    traces = [(title, from_timeline(trace(source))) for title, source in EXAMPLES.items()]
    for path in sorted((HERE / 'fixtures').glob('*.json')):
        data = json.loads(path.read_text())
        traces.append((data.get('title', path.stem), data))
    sections = [section(i, title, data, i == 1) for i, (title, data) in enumerate(traces, 1)]
    target = HERE / 'demo.html'
    target.write_text(PAGE.replace('__SECTIONS__', '\n\n'.join(sections)))
    print(target)


if __name__ == '__main__':
    main()
