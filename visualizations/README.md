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
The last frame holds for 3.5 seconds. The inspection slider is independent of video playback.

## Visual contract

- A fixed 1280 × 720 canvas, DejaVu Sans Mono, dark background `#101722`, panels `#192331`.
  Fixed dark media is a proposal for this checkpoint, not a settled theme policy for the epic.
- `a` is teal `#61d4c4`; `b` is amber `#ffbd69`, including source identifiers.
- The active source line has a blue stripe and background. Read bytes have a blue outline and an
  outward arrow; write bytes have a yellow outline and an inward arrow. Direction remains legible
  without color. A moving number badge represents a copied value, not an address or pointer.
- Integers occupy four individually addressed bytes, with decimal addresses beginning at 64.
  Values are decimal above the row; bytes are two-digit hex, little-endian, left to right.
  The assumed ABI has 4-byte `int` and 8-byte pointers. This is illustrative,
  not portable C++ layout.
- `··` means the declaration has not executed; it does not imply zero or uninitialized object bytes.
  Future rows reserve display space, not live C++ objects.
- No prose is baked into media. `int`, `ptr`, `LE`, `stdout`, `R`, `W`, and `B` are shared notation.
  Review-page explanations are outside the media. No translated lab content changes in this step.

## Shared library boundary

`model.py` owns immutable data:

- `Variable(name, address, size=4, color=...)` describes a synthetic storage slot.
- `Step(line, expression, values, read=None, write=None, transfer=None, stdout="", hold=1.2)`
  captures one visible evaluation state. `line` is zero-based; `values` follows variable order.
  A `None` value means the declaration is pending. A write state contains the values **after** the
  write. `transfer` is the decimal value copied from a read or into a write.
- `Timeline(name, title, source, variables, steps)` groups category-specific data.

`drawing.py` owns style and layout, returning `Rect`, `Text`, and `Line` primitives from
`frame(timeline, index)`. `svg(primitives, title)` serializes them using only Python's standard
library. `CELL`, `ARROW_HEAD`, palette, font, evaluation position, and memory positions live here.

`scenes.py` maps those same primitives to native Manim vector objects. `TimelineScene` handles
frame transitions, moving copy badges, timing, and the final pause. To add a scene, subclass it
and set `timeline`; the two concrete classes contain no drawing logic. SVG text uses browser font
metrics and Manim uses Pango, so glyph baselines can differ slightly; the layout data is identical.

The present layout is deliberately bounded to two 4-byte integer rows and four source lines.
Pointers will require extending this shared layout for 8-byte rows and routing pointer arrows.
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
They are H.264, 1280 × 720, 24 fps: expression 21.67 s, failed swap 21.00 s.
All generated SVGs parse as XML; trace reads/writes match their transferred values.
Rendered evaluation and final-state frames were inspected visually, including punctuation sizing.

The review page is supplied as a file. T3's inline browser preview could not run because its host
is missing browser shared libraries; this task does not change host browser configuration.
