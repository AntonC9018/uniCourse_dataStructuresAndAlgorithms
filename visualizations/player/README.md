# Course visualization player

`player.js` and `player.css` play execution traces inside lessons. They need no libraries and
make no network requests. The site loads both on every page:

```html
<link rel="stylesheet" href="…/player.css">
<script defer src="…/player.js"></script>
```

Each visualization is one element; the site emits it inside a lesson's `<details>`:

```html
<div class="course-visualization"><script type="application/json">TRACE_JSON</script></div>
```

`TRACE_JSON` is the output of `generate.py trace`, with `<` escaped as `<`.
Nothing else is required from the page.

## Behaviour

- **Discovery.** On load, and on Astro's `astro:page-load`, the engine finds every
  `div.course-visualization`. A player inside a closed `<details>` initializes when it opens;
  closing it pauses playback. A host that fails to parse shows a short message, not an exception.
- **One global.** `window.CourseVisualization` holds `version`, the live `players` and `scan()`.
  Each host element also gets `cvPlayer`; `cvPlayer.inspect(step, seconds)` freezes a step at
  a given animation time, for tests and screenshots.
- **Theme.** The player follows `<html data-theme="dark|light">` (Starlight's switch) live,
  falling back to `prefers-color-scheme`. Colours live in `player.css` as `--cv-*` properties;
  the script reads them, so a palette changes in one place.
- **Language.** Labels come from `<html lang>`: English and Russian, English otherwise.
- **Size.** The stage is an SVG sized by its content. It fills the lesson column but never
  draws code larger than 0.6 CSS pixels per unit, so short traces keep the common text size.
  Players narrower than 600 CSS pixels stack code above memory; the page never scrolls sideways.
- **Controls.** Compact transport: Play/Pause, Back, Next, Replay, speed (0.5×–2×), Reset and a
  scrub slider. Clicking a code line, or Enter/Space on it, jumps to the start of that line.
  With the player focused: ←/→ step, Space plays or pauses, Home/End jump to the ends.
  Next and Replay animate; Back, Reset and the slider show the settled state.
- **Focus.** Redraws replace only the drawing; code-line controls and buttons are created once,
  so steps, animations and theme changes keep keyboard focus. A focused button that becomes
  disabled hands focus to the player, where the arrow keys still step.
- **Reduced motion.** With `prefers-reduced-motion: reduce`, every step cuts to its end state.

## Visual language

Memory sits above an evaluation pane, right of the code (stacked on phones). Bytes are drawn to
scale, addresses start at 64, and alignment gaps are dashed. A struct is a frame hugging its
field cells; adjacent frames touch. Every live pointer keeps an arc above memory, in the
pointer's colour, from its cell to the pointee. Arcs to a whole struct end on its frame; arcs
to a field reach the field cell. Ends sharing a cell spread apart and never cross.

A step's operation animates from the previous pane to the new one. Reads are blue, writes
yellow; a dereference selects its target with a neutral outline, and that target brightens just
before the followed arc arrives. Values land in the centre of the token they replace and cut
over on arrival: the old text disappears in the same frame the new value appears. Variables the
current statement does not involve are dimmed.

## Palettes

The dark palette is the approved prototype palette (stage `#101722`, panels `#192331`). The
light palette keeps the same roles on a cool paper stage (`#f5f7fb`, white panels, a pale blue
pane). Variable and field colours are darker versions of their dark hues (teal `#0b8a7c`,
amber `#b86a00`, violet `#7448d0`, rose `#c42e66`, green `#4b8710`; fields olive, magenta,
red, blue), each at least 3:1 against the stage. Reads use `#2f64d6` on `#d9e5ff`; writes use
`#b07d00` on `#fbefc6`.

## Trace format, version 1

`../trace_format.py` defines the format, validates it (`validate(trace)`), builds traces by hand
(`Builder`) and converts the tracer's integer timelines (`from_timeline`).

```text
trace     = {format: 1, source: [line…], variables: [variable…], steps: [step…],
             title?: text, spans?: [span | null per source line]}
variable  = {name, address, size, kind: "int" | "ptr", color}
          | {name, address, size, kind: "struct", color, type, fields: [field…]}
field     = {name, offset, size, kind: "int" | "ptr", color}
step      = {line, pane, values, targets, stdout, hold, op, expr?}
span      = [start, end)  — character offsets
```

- `source` lists the example's lines; `spans[i]` is the evaluated part of line `i`, used for the
  code highlight (the whole line without `;` when absent). `title` is informational.
- `variables` are non-overlapping storage, in any order. `size` counts bytes, padding included.
  `color` indexes the palette's variable colours (fields: field colours) and wraps around.
- A *leaf* is a cell holding a value: a scalar by name, a struct field as `variable.field`.
- `line` is the zero-based source line. `pane` is the statement as currently evaluated, in the
  lessons' notation (`int b{ a };` appears as `int b = a`, `int a{};` as `int a = {}`);
  `expr` is the part of the pane that is being evaluated, the rest being muted context.
- `values` maps every leaf to an integer, `"?"` (declared, value unknown) or `null`
  (storage not yet in use). Pointers hold the address they store, `nullptr` being `0`.
- `targets` maps a pointer leaf to the variable or leaf it points to. A pointer with a target
  holds that target's address; a pointer holding a nonzero value has a target. `stdout` is everything printed so far. `hold` is the pause after the step,
  in seconds at 1×.

`op` describes what turned the previous step into this one. The first step and each new
statement have `op: null`; a new statement copies its pane from the code. Without an operation
a value may only change from `null` to `"?"` (a declaration).

| `kind` | Fields | Meaning |
| --- | --- | --- |
| `read` | `name`, `value`, `span` | `name`'s value replaces `span` of the previous pane. |
| `addr` | `name`, `value`, `span` | `&name`, at `span`, becomes the address `value`. |
| `deref` | `target`, `via`, `span` | `*…` at `span` becomes `target`, which `via` pointed to. |
| `eval` | `value`, `span` | An operator, parentheses or `{}` at `span` reduce to `value`. |
| `write` | `name`, `value`, `span`, `destination` | `value` (at `span`) is stored in `name`. |
| `print` | `value`, `span` | `value` (at `span`) is appended to `stdout`. |

- For `read`, `addr`, `deref` and `eval`, `span` indexes the previous pane, and the new pane is
  the previous one with that span replaced by `value` (`target` for `deref`).
- `write` and `print` leave the pane unchanged; their `span` covers `value` in it. A write's
  `destination` covers `name` in the pane.
- Only a write changes values or targets, and only of the cells its `name` covers (all fields of
  a struct). Only a print changes `stdout`, by its value plus optional whitespace.
- Values agree with memory. A value is an integer, `nullptr` (stored as `0`) or `"?"`; a struct
  is `{…}` of its fields' values, in order. A read's value is what `name` held before the step,
  a write's value what `name` holds after it, field by field, and an `addr` value is the
  address of `name`. A dereference's `target` is `via`'s target or one of its fields.

The double-pointer fixture shows a full reduction: `**pp = 7` → `**72 = 7` (read) → `*p = 7`
(deref) → `*64 = 7` (read) → `a = 7` (deref) → write.

## Fixtures and demo

`fixtures.py` writes the manual pointer and struct traces from the approved prototypes to
`fixtures/*.json`; the tests check they are current. `demo.py` writes `demo.html` (git-ignored)
with real tracer outputs for lesson 2 examples and every fixture, each in a `<details>`, plus
theme and language switches:

```sh
python3 visualizations/player/fixtures.py
nix develop --command python3 visualizations/player/demo.py
```
