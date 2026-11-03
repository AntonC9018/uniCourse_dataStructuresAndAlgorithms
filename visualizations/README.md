# Expression timeline design prototype

Review checkpoint for [#57], the first prototype in [epic #50]. Does one visual language make
expression evaluation, copying a value, and overwriting a value understandable?

The under-memory expression timeline is approved and integrated automatically into applicable
C++ examples. The original manual traces remain as reference fixtures; generated lesson assets
come from compiler-checked sources and GDB-verified runtime state. Other categories remain separate.

[#57]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/57
[epic #50]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/50

## Automatic lesson integration

`discover.py` inventories all outside-answer C++ fences under the configured lab roots. Clang
checks syntax and types; an AST whitelist accepts only flat, side-effect-free integer examples.
Pointers, references, structures, casts, booleans, control flow, ill-formed snippets and undefined
reads/arithmetic are skipped with explicit reasons. A plain literal-initialized cell gets no
visualization. Empty initialization, value copies, arithmetic, assignments and output do.

```sh
python3 visualizations/discover.py --report /tmp/visualization-inventory.json
python3 visualizations/discover.py --apply
python3 course_maintenance/publish.py visualizations generate --course-repo .
```

Discovery adds minimal tags in collapsed, localized execution-trace blocks. Maintenance renders
only missing or changed media, uploads to the durable [asset issue], and places the bare attachment
URL between paired visualization markers. The site projection turns the block into a video player.
Identical English/Russian sources share one language-neutral attachment. Assets and
exact sources are recorded in `assets.json`; no source hash or manually authored trace is needed.
Old assets remain available. Moving a tag or rerunning unchanged maintenance performs no upload.

Generation uses Clang AST types and operation ranges to build expression reductions. GDB verifies
every post-statement value, output, integer size, and frame location before rendering. Addresses
are normalized relative to observed stack offsets, starting at 64. Cells are ordered by those
addresses, so declaration order may differ from the manual reference fixtures. No ASLR addresses
are published. Unchanged-value writes, such as the failed swap, remain visible writes.

The approved layout currently fits up to three four-byte integers, six source lines of 30 columns,
31-column evaluated statements, and four output lines. Declaration attributes and noncontiguous
frame locations are rejected rather than drawn as adjacent cells. The pane has a little more width
than the prototype to accommodate two-digit results alongside `std::endl`. Ineligible examples remain
unchanged; later prototypes can extend coverage without guessing unsupported behavior.

Local dependencies are Clang with C++ standard headers, Python-enabled GDB, Node, Chromium,
ffmpeg, and DejaVu Sans Mono. Playwright is pinned in `package-lock.json`:

```sh
npm ci --prefix visualizations
export COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE=/path/to/chromium
# Optional when tools are outside PATH:
export CLANGXX=/path/to/clang++
export GDB=/path/to/gdb
```

The existing course-management Nix shell supplies Chromium, ffmpeg, and fonts. Compiler/GDB
paths can point to existing declarative installations. No global Python or npm install is needed.
`PLAYWRIGHT_MODULE` can select an existing compatible Playwright package instead of the local one.

For a single source, inspect the derived trace or render it directly:

```sh
python3 visualizations/generate.py probe --source /tmp/snippet.cpp
python3 visualizations/generate.py trace --source /tmp/snippet.cpp
python3 visualizations/generate.py render --source /tmp/snippet.cpp --output /tmp/trace.mp4
python3 visualizations/generate.py render --source /tmp/snippet.cpp \
  --type static --output /tmp/trace.svg
```

The same approved SVG player supplies static snapshots and 720p/60 fps animations. Multiple printed
values append to the visible output; only the newly printed value moves. Empty-brace initialization
retains its real source highlight and transforms into zero. Compiler/GDB tests run locally with
`python3 -m unittest discover -s visualizations/tests`. CI never installs or runs these tools:
maintenance checks tag/source/manifest consistency and anonymous asset availability only.

See [the maintenance contract] for grammar, source-fence lookup, cache invalidation, failure
recovery, and read-only CI behavior.

[asset issue]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/67
[the maintenance contract]: ../course_maintenance/docs/visualization-assets.md

## Review

Open the generated `review.html` directly. It contains both videos, a scenario switcher, and a
slider for every state, including `a + 6`, `5 + 6`, `11`, and the subsequent writes.
It is self-contained and requires no server. Generate it with `python3 visualizations/review.py`
after the MP4 files exist. Generated HTML is ignored by the course repository.

Generated SVGs and videos live in the ignored `visualizations/renders/` directory. Run the
commands under **Reproduce** to create `expression.svg`, `expression.mp4`, `swap.svg`, and
`swap.mp4` locally. Numbered SVGs are individual states; unnumbered SVGs are the final snapshots.
Published lesson media lives in GitHub attachments referenced by `assets.json`.

Expected final states: expression `a = 7`, `b = 11`, stdout `11`; failed swap `a = 2`, `b = 2`.
The last frame holds for 3.5 seconds; key lesson moments get extra emphasis and pauses.
The inspection slider is independent of video playback.

## Chosen layout: under memory (B)

Layout 2, **Under memory**, is the selected direction. Code stays fixed on the left. Compact,
contiguous memory sits above a fixed, unlabeled evaluation pane on the right, and the output line
appears just below it. Pane text, memory, and output share one left edge. A bracket links the
active line to the pane and glides with the active-line highlight when the statement changes.

- The expression test video is exported at 1280 × 720, 60 fps.
- Each statement is copied once, whole and unhurried (1.2 s of travel, with extra step time):
  it lifts off in an opaque box, travels directly to the evaluation pane, and
  replaces the previous statement as it lands. The source line stays intact.
- In the pane, brace initialization reads as `int b = a + 6;`. Statement context is muted;
  the evaluated span keeps its code highlight and full syntax colors.
- A write's destination changes to its variable color, then stays highlighted for one second before
  the value flies to memory. The memory cell changes only when the value arrives, with a pulse to
  mark the update. The destination name returns to neutral after the write finishes.
- Reads and writes are short vertical hops through side ports beside the variable names.
  A 0.55-second preparation marks the operand or result with a tight, filled outline drawn
  beneath its glyphs, together with its memory cell. Memory highlights sit inside each cell,
  so adjacent outlines never overlap.
  Arrows stop at the moving box's outline and fade before it lands.
- The old operand or memory value stays until the boxed value arrives. Memory borders return
  to the variable color after arrival. Printing copies the value to the output line.
- Evaluation keeps shared glyphs, gathers the others, and grows the result without a blank frame;
  the rest of the statement slides to fit the result.

Run `python3 visualizations/layout-prototype.py` and open `layout-prototype.html`.
It opens on B, with playback, step controls, and a state slider for both traces.
The bottom arrows, keyboard left/right, or `?variant=A` and `?variant=C` show the reference
alternatives: A, **Bridge row**, attaches evaluation to the active line; C, **Code above memory**,
opens evaluation beneath the line above a full-width memory band.

All layouts use 112-pixel integer cells. Multi-row memory and long expressions still need a
separate layout pass. The Manim layout is unchanged.

The exporter records the actual prototype SVG with a fixed animation clock. After generating the
HTML, render the test video (B is the default; `swap`, `bridge`, and `memory-band` also work):

```sh
node visualizations/render-layout-video.cjs expression
```

It requires Playwright, Chromium, and ffmpeg. Set `PLAYWRIGHT_MODULE` to an installed Playwright
package when it is outside Node's module search path, and optionally set
`COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE` to the Chromium executable from the existing Nix shell.
The output is `visualizations/renders/layout-memory-strip-expression-720p.mp4`. To reproduce
the comparison layouts, pass `bridge` or `memory-band` as the second argument. Generated
comparisons remain local and are not committed.

## Original Manim visual contract

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
The original Manim adapter is retained for reference. Automatic lesson integration uses the
approved SVG player and the compiler-backed adapter described above.

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
The layout prototype was checked separately in headless Chromium using the existing Nix shell
browser, across both full traces and all three variants, with no JavaScript errors.
For B, every exported segment settles before the exporter reuses its last frame.

## Interactivity in Markdown

GitHub removes JavaScript from rendered repository markup, so the custom step buttons and slider
cannot run inside a GitHub lesson. Use the video there and link to the standalone interactive HTML.
The course website can host that HTML, or embed an interactive player with renderer integration;
this prototype does not implement that integration.

[GitHub's markup pipeline](https://github.com/github/markup#github-markup) documents sanitization.
