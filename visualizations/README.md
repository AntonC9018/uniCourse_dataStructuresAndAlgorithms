# Execution visualizations

Lessons show how C++ examples execute: code on the left, memory above an expression-evaluation
pane on the right, values moving between them. This work belongs to [epic #50]; the integration
design is in [#55] and [#56].

- `discover.py` finds lesson examples the tracer supports and tags them.
- `tracing.py` uses Clang AST types and ranges to emit unified integer, pointer and struct traces.
- `records.py` validates aggregate definitions and reads field offsets, sizes and alignment
  from Clang.
- `execution.py` runs whitelisted statements under GDB and observes every post-statement state.
- `toolchain.py` selects compiler/debugger executables and bounds tool execution.
- `trace_format.py` defines and validates the unified format and builds manual traces.
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
checks syntax and types; an AST whitelist accepts flat integer, pointer and aggregate struct
examples.
Address-of, dereference chains, pointer reads/copies, shared targets and reassignment through
pointers are supported, including pointers to pointers. Null pointers are stored and reduced
to `0`. The pane follows lesson notation: `**pp` → `**72` → `*p` → `*64` → `a`.

Structs support aggregate and designated initialization, uninitialized field storage, whole-object
copies, `.` and `->`, field addresses and pointer fields. Copies are shallow: pointer fields keep
their original targets. Fields must be `int`, pointers to `int`, or pointers to another struct in
the snippet. Every live field is checked under GDB after every statement. The player uses the
existing struct frames, per-field colours and separate arc endpoints for objects and fields.

Pointer arithmetic/comparison, arrays, references, nested struct values, casts, heap allocation,
other field types, methods, inheritance, bitfields, default member initializers, empty structs,
qualified pointers, control flow, ill-formed snippets and undefined reads or
arithmetic are skipped with explicit reasons. Computed-address dereferences (`*(&a)`) and
address-of dereferences (`&*p`) are also outside this subset. A plain literal-initialized
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
verifies every post-statement value, output, storage size and frame location. Pointer targets
retain their typed object or field identity; GDB verifies their numeric addresses. Addresses
are normalized relative to observed stack offsets, aligned near 64, so no ASLR addresses are
published. Cells are ordered by address, so declaration order may differ from the source.
Unchanged-value writes, such as the failed swap, remain visible writes.

```sh
python3 visualizations/generate.py probe --source /tmp/snippet.cpp
python3 visualizations/generate.py trace --source /tmp/snippet.cpp
```

`trace` prints the unified format as deterministic JSON (sorted keys). `revision` hashes the
tracer modules (including record layouts) and the flake lock. Maintenance keys stored traces
by this revision, so a toolchain or format change re-traces every example.

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
