# Expression timeline design prototype

Review checkpoint for [#57], the first prototype in [epic #50]. Does one visual language make
expression evaluation, copying a value, and overwriting a value understandable?

The under-memory expression timeline is approved. Lessons will embed it as an interactive player
rather than a video; until that integration is planned ([#55], [#56]), the lesson tags stay in
place but render nothing. The original manual traces remain as reference fixtures; traces for
lessons come from compiler-checked sources and GDB-verified runtime state.

[#57]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/57
[epic #50]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/50
[#55]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/55

## Tracing lesson examples

`discover.py` inventories all outside-answer C++ fences under the configured lab roots. Clang
checks syntax and types; an AST whitelist accepts only flat, side-effect-free integer examples.
Pointers, references, structures, casts, booleans, control flow, ill-formed snippets and undefined
reads/arithmetic are skipped with explicit reasons. A plain literal-initialized cell gets no
visualization. Empty initialization, value copies, arithmetic, assignments and output do.

```sh
python3 visualizations/discover.py --report /tmp/visualization-inventory.json
python3 visualizations/discover.py --apply
```

Discovery adds minimal tags in collapsed, localized execution-trace blocks. Video rendering, the
upload manifest and the maintenance step that filled those tags have been removed, and the
`visualizations` entry is gone from `course-publishing.json`, so maintenance neither fills nor
checks the tags. How the interactive player reaches a lesson is decided in [#55] and [#56].

Generation uses Clang AST types and operation ranges to build expression reductions. GDB verifies
every post-statement value, output, integer size, and frame location before rendering. Addresses
are normalized relative to observed stack offsets, starting at 64. Cells are ordered by those
addresses, so declaration order may differ from the manual reference fixtures. No ASLR addresses
are published. Unchanged-value writes, such as the failed swap, remain visible writes.

The approved layout currently fits up to three four-byte integers, six source lines of 30 columns,
31-column evaluated statements, and four output lines. Declaration attributes and noncontiguous
frame locations are rejected rather than drawn as adjacent cells. The pane has a little more width
than the prototype to accommodate two-digit results alongside `std::endl`.
Ineligible examples remain unchanged;
later prototypes can extend coverage without guessing unsupported behavior.

Local dependencies are Clang with C++ standard headers, Python-enabled GDB, Node, Chromium,
and DejaVu Sans Mono. Playwright is pinned in `package-lock.json`:

```sh
npm ci --prefix visualizations
export COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE=/path/to/chromium
# Optional when tools are outside PATH:
export CLANGXX=/path/to/clang++
export GDB=/path/to/gdb
```

The existing course-management Nix shell supplies Chromium and fonts. Compiler/GDB
paths can point to existing declarative installations. No global Python or npm install is needed.
`PLAYWRIGHT_MODULE` can select an existing compatible Playwright package instead of the local one.

For a single source, inspect the derived trace or render it directly:

```sh
python3 visualizations/generate.py probe --source /tmp/snippet.cpp
python3 visualizations/generate.py trace --source /tmp/snippet.cpp
python3 visualizations/generate.py render --source /tmp/snippet.cpp --output /tmp/trace.svg
```

`render` exports the settled final state of the approved SVG player as a static snapshot through
`export-layout-svg.cjs`; there is no video output. Multiple printed
values append to the visible output; only the newly printed value moves. Empty-brace initialization
retains its real source highlight and transforms into zero. Compiler/GDB tests run locally with
`python3 -m unittest discover -s visualizations/tests`. CI never installs or runs these tools.

Generated SVGs live in the ignored `visualizations/renders/` directory. Expected final states:
expression `a = 7`, `b = 11`, stdout `11`; failed swap `a = 2`, `b = 2`.

## Website controls prototype

Question: which controls make animated execution useful inside an existing lesson?
**Decided:** compact transport (variant A). The step navigator (B) and statement chapters (C)
were comparison studies and are rejected. The remaining work is production integration, not
another control-layout study.

```sh
python3 visualizations/website-controls-prototype.py
```

Open `visualizations/website-controls-prototype.html?variant=A` for the chosen compact transport,
or `?variant=B` and `?variant=C` for the rejected comparisons. The chosen layout is the default,
and the comparison footer has been removed.

Click a line in either the lesson's code block or the animation to jump to the start of that
statement. Earlier writes and output are restored, playback pauses, and Next animates execution
from that point. Code lines also support keyboard selection with Enter or Space.

The prototype embeds the same SVG renderer used for the static exports. Next and Replay animate
the transition; Back and direct step selection show the settled state. Play/Pause freezes and
resumes the SVG clock, and speed controls change both movement and holds. Expression and failed
swap examples share this player.

Shipping this control layout inside lessons is separate work: the course website does not embed
an interactive player yet, and the maintenance integration in [#56] settles how assets and tags
reach a lesson. Until then the prototype stays on `labs/visualizations`.

[#56]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/56

## Pointer prototype

Question for [#59]: how should pointers, the addresses they store, and dereference chains look,
so that `**pp = 7` stays legible? **Decided:** arcs above memory (variant A). Lanes below
memory (B) and address lookup without persistent arrows (C) are rejected comparisons.

```sh
python3 visualizations/pointer-prototype.py
```

Open `visualizations/pointer-prototype.html` (`?variant=B` or `?variant=C` for the rejected
comparisons). It covers writing through a pointer, reassigning a pointer, a pointer to a pointer,
and two pointers to one variable. The traces are manual; no compiler or GDB is involved yet.

- Memory keeps the under-memory (B) language. Integers occupy 4 bytes and pointers 8, at
  24 pixels per byte; addresses start at 64. Alignment gaps are drawn as dashed, unlabeled cells.
- A pointer cell shows its stored address in decimal. Each live pointer keeps an arc, in the
  pointer's color, from its cell over the address row to its pointee.
- Arcs start and end near the centers of their cells. When a cell carries several arc ends,
  the ends spread 20 pixels apart. Ends leading left sit left of ends leading right; on each side,
  the farther-reaching arc sits nearer the center and rises higher, nesting over the shorter one.
  Chains (`pp → p → a`) and shared pointees therefore never cross.
- Each arc has a background halo, keeping it legible where it passes address labels.
- Evaluation follows the lessons' reduction: `**pp = 7` → `**72 = 7` → `*p = 7` → `*64 = 7`
  → `a = 7`. Reads are blue, writes yellow. Dereference selects a location with a neutral
  outline, because it reads nothing; the followed arc brightens from pointer to pointee.
- `&a` copies the address label above storage, not the cell value. Copying a pointer
  (`int* q = p;`) is an ordinary read of the stored address.
- Redirecting a pointer fades its old arc when the new address arrives, then draws the new arc.

Pointing at a cell's center means "this object", not "this byte". Struct fields and array
elements may need arcs that land on the first byte; the struct study revisits this.

Folding this into the production player needs base-library changes: variable sizes and alignment
gaps in the memory layout, an address-valued cell kind, an arc layer, lvalue reductions in the
pane (address-of and dereference steps), and tracing support for pointers in `tracing.py`.

[#59]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/59

## Chosen layout: under memory (B)

Layout 2, **Under memory**, is the selected direction. Code stays fixed on the left. Compact,
contiguous memory sits above a fixed, unlabeled evaluation pane on the right, and the output line
appears just below it. Pane text, memory, and output share one left edge. A bracket links the
active line to the pane and glides with the active-line highlight when the statement changes.

- The canvas is 1280 × 720.
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
separate layout pass.

To export the settled final state of a trace as a static SVG, after generating the HTML:

```sh
node visualizations/export-layout-svg.cjs expression
```

It requires Playwright and Chromium. Set `PLAYWRIGHT_MODULE` to an installed Playwright package
when it is outside Node's module search path, and optionally set
`COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE` to the Chromium executable from the existing Nix shell.
The output is `visualizations/renders/layout-expression.svg` (or `swap`).

## Original visual contract

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

The current canvas fits three memory rows and ten source lines. Memory wraps horizontally
at variable boundaries. Objects wider than one row must first be represented as integer-sized
slots; pointer arcs are settled in the pointer prototype. The original Manim video adapter has
been removed; lessons use the approved SVG player and the compiler-backed adapter described above.

## Reproduce

Static SVGs need only Python 3:

```sh
python3 visualizations/render.py
```

## Verification for this checkpoint

All generated SVGs parse as XML; trace reads/writes match their transferred values.
Source-copy, read/write-arrow, overwritten-value, and final-emphasis frames were inspected
visually. Unknown and undeclared states were checked independently in the shared drawing model.
Packing was checked with enough integer slots to force multiple rows, including the label
positions and shared animation coordinates. One-, two-, and three-row evaluation placements,
longer code panels, separate routing ports, and route lengths were checked against the canvas.
Full-scene fades remain disabled.

The layout prototype was checked separately in headless Chromium using the existing Nix shell
browser, across both full traces and all three variants, with no JavaScript errors.

## Interactivity in Markdown

GitHub removes JavaScript from rendered repository markup, so the custom step buttons and slider
cannot run inside a GitHub lesson. Link to the standalone interactive HTML there.
The course website can host that HTML, or embed an interactive player with renderer integration;
this prototype does not implement that integration.

[GitHub's markup pipeline](https://github.com/github/markup#github-markup) documents sanitization.
