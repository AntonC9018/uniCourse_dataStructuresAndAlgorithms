# Execution visualizations

Lessons show how C++ examples execute: code on the left, memory above an expression-evaluation
pane on the right, values moving between them. This work belongs to [epic #50]; the integration
design is in [#55] and [#56].

- `discover.py` finds lesson examples the tracer supports and tags them.
- `tracing.py` traces an example with Clang and GDB into an integer `Timeline` (`model.py`).
- `trace_format.py` defines the unified trace format the site plays, converts timelines to it,
  validates traces and builds manual ones.
- `generate.py` is the command line maintenance uses: `trace`, `probe` and `revision`.
- `player/` holds the site engine (`player.js`, `player.css`), the manual pointer and struct
  fixtures, and a local demo. [`player/README.md`](player/README.md) documents the engine and
  the format.
- `struct-prototype.py` is the static struct-layout study for [#62].

[epic #50]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/50
[#55]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/55
[#56]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/56
[#62]: https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/62

## Tracing lesson examples

`discover.py` inventories all outside-answer C++ fences under the configured lab roots. Clang
checks syntax and types; an AST whitelist accepts only flat, side-effect-free integer examples.
Pointers, references, structures, casts, booleans, control flow, ill-formed snippets and
undefined reads or arithmetic are skipped with explicit reasons. A plain literal-initialized
cell gets no visualization; empty initialization, value copies, arithmetic, assignments and
output do.

```sh
python3 visualizations/discover.py --report /tmp/visualization-inventory.json
python3 visualizations/discover.py --apply
```

Discovery adds minimal tags in collapsed, localized execution-trace blocks. Course maintenance
traces every tag in CI inside the pinned toolchain and stores the results by content, so only
changed examples are traced again; a tag that cannot be traced fails the build.

Generation uses Clang AST types and operation ranges to build expression reductions. GDB
verifies every post-statement value, output, integer size and frame location. Addresses are
normalized relative to observed stack offsets, starting at 64, so no ASLR addresses are
published. Cells are ordered by address, so declaration order may differ from the source.
Unchanged-value writes, such as the failed swap, remain visible writes.

```sh
python3 visualizations/generate.py probe --source /tmp/snippet.cpp
python3 visualizations/generate.py trace --source /tmp/snippet.cpp
```

`trace` prints the unified format as deterministic JSON (sorted keys). `revision` hashes the
tracer and converter sources and the flake lock; maintenance keys stored traces by it, so a
toolchain or format change re-traces every example.

## Toolchain and tests

The course flake pins the tools. `nix develop .#visualizations` provides Clang with C++
standard headers and Python-enabled GDB, which is all tracing needs; CI uses the same shell.
The default shell (`nix develop`) adds Node and Chromium for headless screenshots of the demo.
`CLANGXX` and `GDB` select the tools; both shells set them.

```sh
nix develop .#visualizations --command python3 -m unittest discover -s visualizations/tests
```

The player's browser tests run headless Chromium through Playwright, in the default shell:

```sh
nix develop --command npm ci --prefix visualizations
nix develop --command npm test --prefix visualizations
```

## Interactivity in Markdown

GitHub removes JavaScript from rendered repository markup ([GitHub markup]), so the player runs
only on the course website.

[GitHub markup]: https://github.com/github/markup#github-markup
