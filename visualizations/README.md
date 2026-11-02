# Expression timeline design prototype

Review checkpoint for [#57], the first prototype in [epic #50]. Does one visual language make
expression evaluation, copying a value, and overwriting a value understandable?

This is a manual trace and a provisional shared library, awaiting design review. The failed swap
uses exactly the same renderer as the expression example. Later categories should import the base
rather than copy its layout. The labs have not been edited.

[#57]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/57
[epic #50]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/50

## Review

Open the generated `review.html` directly. It contains both videos, a scenario switcher, and a
slider for every state, including `a + 6`, `5 + 6`, `11`, and the subsequent writes.
It is self-contained and requires no server. Generate it with `python3 visualizations/review.py`
after the MP4 files exist. Generated HTML is ignored by the course repository.

- [Expression SVG](renders/expression.svg) and [MP4](renders/expression.mp4).
- [Failed swap SVG](renders/swap.svg) and [MP4](renders/swap.mp4).
- Numbered SVGs are individual states; unnumbered SVGs are the final snapshots.

Expected final states: expression `a = 7`, `b = 11`, stdout `11`; failed swap `a = 2`, `b = 2`.
The last frame holds for 3.5 seconds; key lesson moments get extra emphasis and pauses.
The inspection slider is independent of video playback.

## Layout alternatives (throwaway)

Run `python3 visualizations/layout-prototype.py` and open `layout-prototype.html`.
The page embeds both existing manual traces with playback, step controls, and a state slider.
Use the bottom arrows or keyboard left/right to compare `?variant=A`, `B`, and `C`:

- A opens a temporary evaluation row beneath the active source line. Later lines slide down
  while the expression is evaluated, then close up after its value is stored or printed.
  A write keeps the row open until the transfer animation finishes.
- B uses a fixed central evaluation workspace between code and memory.
- C places contiguous memory across the top, above code and evaluation.

These studies compare geometry; their transfer motion is schematic. They do not change the
Manim layout. Greyed-out future storage is already applied to the shared renderer and videos.
The tradeoffs are shown below each study. A layout decision is still pending.

### Variant A video

[Expression video, 1280 × 720 at 60 fps](renders/layout-a-expression-720p.mp4).
This exports the actual prototype SVG, including temporary evaluation rows, with a fixed
animation clock. Panel motion and transfers ease in and out. Opening evaluation copies the
highlighted source expression into the pane, preserving the original code. Evaluation matches
shared characters, gathers outgoing characters, and grows the result into place.
Reads pulse the source value; writes pulse the destination as the value arrives. Transfer
paths use rounded bends and finish at the actual glyph coordinates. Moving values have opaque
boxes above the arrows. Variable names sit below cells; addresses label the starting edge above.
It does not use the older Manim layout.

After generating `layout-prototype.html`, run:

```sh
node visualizations/render-layout-video.cjs expression
```

The exporter requires Playwright, Chromium, and ffmpeg. Set `PLAYWRIGHT_MODULE` to an installed
Playwright package when it is outside Node's module search path, and optionally set
`COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE` to the Chromium executable from the existing Nix shell.
Use `swap` instead of `expression` to export the other trace.

## Visual contract

- A fixed 1280 × 720 canvas, DejaVu Sans Mono, dark background `#101722`, panels `#192331`.
  Fixed dark media is a proposal for this checkpoint, not a settled theme policy for the epic.
- `a` is teal `#61d4c4`; `b` is amber `#ffbd69`, including source identifiers.
- The active line has a blue stripe; its evaluated expression has a focused highlight and
  underline. On entry to a source line, that expression is copied into the evaluation panel.
  Read slots turn blue when the read begins; write slots and source destinations turn yellow
  before a write. Temporary arrows show the route, and values slide along those exact paths.
  Overwritten glyphs leave the slot before the replacement arrives. Unchanged content stays still.
- Code occupies the left column; its panel height follows the number of source lines.
  Evaluation sits directly below memory in the right column, with its top derived from the
  final wrapped row. Its position stays fixed during a clip, including before declarations.
- Variables occupy adjacent horizontal slots, in address order. Each 4-byte integer occupies
  one 224-pixel slot. Rows wrap before an integer would be split. Wider whole variables fit
  where space permits or move to the next row.
- Read and write routes use separate vertical ports on opposite sides of each variable name.
  Separate gutters beside evaluation keep arrows away from its heading. Source copies use the
  inter-column gap and enter evaluation horizontally, clear of other source lines.
- A variable name is centered below its memory slot. Its decimal starting address is aligned
  with the slot's left edge, above it. Values are centered inside the slots.
- Future storage is shown in grey until allocation, with a blank value and muted name/address.
  A slot acquires its variable color when allocated. An explicitly declared but uninitialized
  variable uses `?`; future declarations do not show an unknown value. A new slot is empty
  while its first value arrives.
- Individual hex bytes appear only with `byte_detail=True`, for examples teaching byte layout,
  casts, or partial writes. The assumed ABI has 4-byte `int`, 8-byte pointers, and little-endian
  storage; this is illustrative, not portable C++ layout.
- Output appears as a plain bottom line only after the program prints; there is no empty output
  panel. The temporary expression panel is labeled **Expression evaluation**. Decorative titles,
  counters, type headers, footer notation, and the `C++ →` label have been removed.
  The English panel label can be localized when these prototypes are integrated into the labs.

## Shared library boundary

`model.py` owns immutable data:

- `Variable(name, address, size=4, color=...)` describes a synthetic storage slot.
- `Step(line, expression, values, read=None, write=None, transfer=None, stdout="", hold=1.2)`
  captures one visible evaluation state. `line` is zero-based; `values` follows variable order.
  A `None` value means storage is greyed out unless its name is in `declared`; an explicitly
  declared unknown value is shown as `?`. A write state contains values **after** the write.
  `transfer` is the decimal value copied from a read or into a write.
  `focus` lists slots to emphasize after the transfer, using a neutral outline to avoid implying
  an extra read. The expression trace emphasizes the unchanged `b`; the swap emphasizes both
  final values. The old value leaves on every overwrite, even when the new value is equal.
  `read_span=(start, end)` identifies the operand in the preceding expression, with an exclusive
  end index. Its replacement literal determines the destination of the moving value.
- `Timeline(name, title, source, variables, steps, byte_detail=False)` groups category data
  and selects whole-variable slots by default. `expression_spans` records the character range
  evaluated on each source line; the same range drives highlighting and the copy animation.

`drawing.py` owns style and layout, returning `Rect`, `Text`, and `Line` primitives from
`frame(timeline, index)`. `svg(primitives, title)` serializes them using only Python's standard
library. `WORD_WIDTH`, palette, font, expression position, and `memory_layout` live here.
Read/write animation positions come from the same packed slots as the static renderer.
`code_panel`, `evaluation_panel`, and `transfer_route` own content sizing and routing geometry.

`scenes.py` maps those same primitives to native Manim vector objects. `TimelineScene` handles
atomic state transitions, source-to-panel expression copies, arrow routes, overwrites, timing,
and the final pause. Only the overwritten glyph fades; unchanged content never fades.
Expression text has a fixed left edge so substitution preserves other operands.
To add a scene, subclass it and set `timeline`; the two concrete classes contain no drawing logic.
SVG text uses browser font
metrics and Manim uses Pango, so glyph baselines can differ slightly; the layout data is identical.

The current canvas fits three memory rows and ten source lines. Memory wraps horizontally
at variable boundaries. Objects wider than one row must first be represented as integer-sized
slots; pointer-arrow routing remains part of the pointer prototype.
No automatic AST/GDB tracing, tag grammar, uploads, source hashes, or maintenance integration
is implemented here. `course-publishing.json` will point at this directory when integration
is designed.

## Reproduce

Static SVGs need only Python 3:

```sh
python3 visualizations/render.py
```

For MP4, use the pinned Manim 0.22.0 maintenance environment from
`course_maintenance/visualizations/README.md`, then run from the course root:

```sh
bash visualizations/render-animation.sh
```

The scenes use native text rather than MathTex and do not invoke LaTeX. They do require the
native Cairo/Pango and font dependencies in that toolchain. Rendering stays outside CI.

On Anton's NixOS machine, the existing declarative `course-management` shell supplies these
libraries and fonts. The older copied maintenance venv has a broken `/usr/bin/python3` symlink;
use the shell interpreter with its installed packages rather than mutate that environment:

```sh
nix develop ~/nix-config#course-management --command bash -c '
  export LD_LIBRARY_PATH="$(pkg-config --variable=libdir gobject-2.0):$LD_LIBRARY_PATH"
  export PYTHONPATH="$PWD/course_maintenance/.venv/lib/python3.14/site-packages"
  export VISUALIZATION_PYTHON=python
  bash visualizations/render-animation.sh
'
```

This compatibility invocation was rendered with Python 3.14.7, Manim 0.22.0, and the pinned
maintenance packages. No global installations or machine configuration changes are required.
The Manim adapter uses native vector objects; it avoids an `ImageMobject` path that fails with
the currently pinned Pillow 13 package.

## Verification for this checkpoint

Both final videos decode without errors using `ffmpeg -v error -i <file> -f null -`.
They are H.264, 1280 × 720, 24 fps. Transitions switch atomically with no full-scene fades.
All generated SVGs parse as XML; trace reads/writes match their transferred values.
Source-copy, read/write-arrow, overwritten-value, and final-emphasis frames were inspected
visually. Unknown and undeclared states were checked independently in the shared drawing model.
Packing was checked with enough integer slots to force multiple rows, including the label
positions and shared animation coordinates. One-, two-, and three-row evaluation placements,
longer code panels, separate routing ports, and route lengths were checked against the canvas.
Full-scene fades remain disabled.

The review page is supplied as a file. T3's preview checker lacks host browser libraries.
The layout comparison was checked separately in headless Chromium using the existing Nix shell
browser, across both full traces and all three variants, with no JavaScript errors.

## Interactivity in Markdown

GitHub removes JavaScript from rendered repository markup, so the custom step buttons and slider
cannot run inside a GitHub lesson. Use the video there and link to the standalone interactive HTML.
The course website can host that HTML, or embed an interactive player with renderer integration;
this prototype does not implement that integration.

[GitHub's markup pipeline](https://github.com/github/markup#github-markup) documents sanitization.
