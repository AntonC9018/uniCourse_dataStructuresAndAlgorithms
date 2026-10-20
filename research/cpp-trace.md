# C++ trace research: static types, expression values, and memory layout

**Ticket:** [#51](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/51)

**Branch:** `research/cpp-trace`

**Tested:** 2026-10-20 on Ubuntu, Clang 17.0.6, GDB 17.1, Python 3.14.4, LLDB 17.0.6, binutils 2.46.

**Scope.** This is research for the course visualizer; it does not change `course_maintenance` or any lab.

## Recommendation

Build the tracer as two cooperating passes:

1. **Static pass (Clang):** parse the snippet with `clang++ -fsyntax-only` and dump the AST as JSON (`-Xclang -ast-dump=json`) plus record layouts (`-Xclang -fdump-record-layouts-complete`). This is the source of truth for declarations, canonical and aliased types, sizes, offsets, padding, value categories, and the static type of every subexpression. It also works for ill-formed snippets: Clang emits `RecoveryExpr` nodes and diagnostics.
2. **Dynamic pass (GDB Python):** compile the snippet with `-g -O0 -fno-omit-frame-pointer`, break at each source line, and use the GDB Python API to read locals, bytes, and addresses. This is the source of truth for actual values, byte contents, pointer targets, and writes. Convert all real addresses to deterministic **synthetic addresses starting at 64** before anything reaches the renderer.

Do **not** build a Clang plugin/LibTooling tool, do **not** build a C++ interpreter, and do **not** use Cling/cppyy. A small pure expression evaluator over AST and snapshot values is acceptable for displaying intermediate results; it is not a language implementation.

Neither pass is sufficient alone. Clang knows types but does not execute. GDB knows bytes but does not expose a static type for every subexpression, and cannot parse ill-formed code. The combination also meets the local-maintenance constraint: invoke existing `clang++` and `gdb` binaries, with no compiler build.

## Requirement-to-mechanism map

| Requirement | Static source | Dynamic source |
|---|---|---|
| Declarations and declared types | AST `VarDecl`, `FieldDecl`, `FunctionDecl`, `CXXRecordDecl` | GDB `frame.read_var`, `gdb.lookup_type` |
| `sizeof`, alignment, field offsets, padding | `-fdump-record-layouts-complete`; AST `FieldDecl` | GDB `ptype /o`, `Type.fields()`, `Type.sizeof` |
| Static type of every subexpression | AST `type.qualType` / `desugaredQualType`, `valueCategory` | not available from GDB; runtime type can differ from static type |
| Evaluation order | C++ standard rules plus AST shape | observed stop order only; label it as observed |
| Subexpression results | pure AST evaluator over snapshot values; `sizeof`/type facts | GDB `parse_and_eval` at the correct stop, for pure expressions only |
| Variable values and bytes per line | declarations and lifetimes | GDB breakpoint snapshots, `Value.bytes`, `read_memory` |
| Pointer values and pointees | AST `&`, `*`, `[]`, `MemberExpr`, pointer arithmetic; layout | GDB value bytes plus an object/address table |
| Writes through pointers, partial/oversized | lvalue expression type and nominal width | byte diff between line snapshots |
| Ill-formed type puzzles | AST `RecoveryExpr` plus diagnostics | not executed |

## 1. Static pass: declarations, types, and layout

### 1.1 AST JSON

Command (the tested LLVM tree was not on `PATH`):

```bash
CLANGXX=/usr/lib/llvm-17/bin/clang++
"$CLANGXX" -std=c++17 -fsyntax-only \
  -Xclang -ast-dump=json \
  -Xclang -ast-dump-filter=main \
  snippet.cpp > ast-main.json
```

Important properties, verified on Clang 17.0.6:

- `-ast-dump-filter=<substring>` filters to declarations whose name contains the substring and emits **multiple concatenated JSON documents**, not one JSON array. A filter of `main` produced seven documents. Parse with repeated `json.JSONDecoder().raw_decode` until EOF, then select the `FunctionDecl` whose `name` is `main` and whose `loc.file` ends in `snippet.cpp`.
- Without a filter, the AST for a file including `<iostream>` was about 136 MB; the filtered main function was about 53 KB. Always filter, and cache by source hash.
- JSON locations are compressed: `file` and `line` are omitted when unchanged from the previous node; `range.begin.offset` / `range.end.offset` and `tokLen` are present for source tokens. Build an offset-to-line/column table from the source and resolve spans through it. Handle `spellingLoc`/`expansionLoc` for macros if they appear.
- Expression nodes carry `type.qualType`, often `type.desugaredQualType` (for example `__ostream_type` to `std::basic_ostream<char>`), and `valueCategory` (`lvalue`, `prvalue`, `xvalue`). Casts carry `castKind` (`LValueToRValue`, `ArrayToPointerDecay`, and so on).
- Declarations have `id` values that are stable within one AST dump. References such as `DeclRefExpr` may contain a `referencedDecl` object with the same `id`; build a declaration table keyed by `id` so references can be linked without locations.
- The JSON shape is defined by Clang's internal `clang/lib/AST/JSONNodeDumper.cpp`, not a stable public schema. Pin the compiler version and keep golden tests.

A text dump is useful while developing and as a fallback:

```bash
"$CLANGXX" -std=c++17 -fsyntax-only -Xclang -ast-dump -Xclang -ast-dump-filter=main snippet.cpp
```

For `int b{a + 6};` the text dump shows the structure directly:

```text
|-VarDecl ... b 'int' listinit
| `-InitListExpr ... 'int'
|   `-BinaryOperator ... 'int' '+'
|     |-ImplicitCastExpr ... 'int' <LValueToRValue>
|     | `-DeclRefExpr ... 'int' lvalue Var ... a 'int'
|     `-IntegerLiteral ... 'int' 6
```

The corresponding JSON gives `BinaryOperator.type.qualType = "int"`, `opcode = "+"`, `valueCategory = "prvalue"`; the `DeclRefExpr` is `"int"` and `lvalue`; the cast is `"int"` and `prvalue` with `castKind = "LValueToRValue"`. This is the static answer for "what is the type of `a + 6`?" without executing anything.

### 1.2 Wrapping snippets that have no `main`

Many lab examples are statement fragments. Wrap them without destroying line numbers:

```cpp
int main() {
#line 1 "snippet.cpp"
    // original snippet lines, unchanged
}
```

The `#line` directive must come **after** `int main() {` and before the snippet, so the snippet's first line is line 1. If the snippet already declares `main`, compile it as-is. Keep a line map from wrapper lines to original lines. Use the same wrapped source for the static and dynamic passes so AST offsets and GDB breakpoints agree.

### 1.3 Record sizes, field offsets, and padding

Command:

```bash
"$CLANGXX" -std=c++17 -fsyntax-only \
  -Xclang -fdump-record-layouts-complete \
  layout.cpp
```

Use `-complete`: plain `-fdump-record-layouts` only dumps records that the code uses, which is easy to miss for a type-only example. `-complete` also dumps records from included standard headers, so filter by the record name you asked about.

Verified output for the relevant records (abridged; `-complete` also dumps system records):

```cpp
struct A { char c; int i; double d; };
struct B { char c; int64_t i; };
```

```text
*** Dumping AST Record Layout
         0 | struct A
         0 |   char c
         4 |   int i
         8 |   double d
           | [sizeof=16, dsize=16, align=8,
           |  nvsize=16, nvalign=8]

*** Dumping AST Record Layout
         0 | struct B
         0 |   char c
         8 |   int64_t i
           | [sizeof=16, dsize=16, align=8,
           |  nvsize=16, nvalign=8]
```

The dump also prints bitfields, base classes, virtual bases, and vtable pointers when present. For the course's simple structs it is the cleanest static layout source.

GDB can independently confirm layout at runtime:

```text
(gdb) ptype /o struct S
/* offset      |    size */  type = struct S {
/*      0      |       1 */    char c;
/* XXX  3-byte hole      */
/*      4      |       4 */    int i;

                               /* total size (bytes):    8 */
                             }
```

and through Python:

```python
t = gdb.lookup_type("S")
[(f.name, f.bitpos, f.type.sizeof) for f in t.fields()]
# [('c', 0, 1), ('i', 32, 4)]
t.sizeof  # 8
```

`f.bitpos` is in bits, including padding. `f.bitsize` is for bitfields and is 0 for ordinary fields, so use `f.type.sizeof` for the field width. `ptype /o` prints the hole explicitly; the field API gives the offsets but not a convenience "padding size" field, so derive padding from adjacent offsets and the total size.

### 1.4 Ill-formed snippets

Clang still builds a partial AST for many type errors. Verified:

```cpp
int main() {
    int value{5};
    int* p{};
    p = value;
}
```

`clang++ -std=c++17 -fsyntax-only` exits 1 with:

```text
error: incompatible integer to pointer conversion assigning to 'int *' from 'int'
```

but the AST contains:

```text
|-BinaryOperator ... 'int *' '='
| |-DeclRefExpr ... 'int *' lvalue Var ... p 'int *'
| `-RecoveryExpr ... '<dependent type>' contains-errors
|   `-DeclRefExpr ... 'int' lvalue Var ... value 'int'
```

Likewise `a = "Hello"` produces a `RecoveryExpr` with children of type `int` and `const char[6]`. The recoverable expression's own type is not the answer; the **child** types plus the diagnostic are. The tracer should:

- run `-fsyntax-only` and parse the AST even when the exit code is non-zero;
- keep diagnostics (`-fno-color-diagnostics -fdiagnostics-format=json` if structured diagnostics are useful);
- mark the snippet ill-formed and skip the dynamic pass;
- answer "what type is this expression?" from the recovered child types when possible, and otherwise report "ill-formed; no single type".

This directly covers the deliberate `// doesn't compile` puzzles in the labs, for example `p = value` and `a = "Hello"`.

## 2. Dynamic pass: values, bytes, pointers, and writes

### 2.1 Compile and run under GDB

```bash
"$CLANGXX" -std=c++17 -g -O0 -fno-omit-frame-pointer snippet.cpp -o snippet
gdb -q -batch ./snippet \
  -ex 'set pagination off' \
  -ex 'break snippet.cpp:6' \
  -ex run \
  -ex 'info locals' \
  -ex 'ptype /o struct S' \
  -ex 'x/16bx &s'
```

For a line-by-line trace, a Python script is cleaner than a chain of `-ex` options. Verified APIs:

```python
import gdb

frame = gdb.selected_frame()
a = frame.read_var("a")
int(a)                 # value
a.bytes                # bytes in target byte order
a.address              # gdb.Value, or None
a.type.sizeof          # size in bytes
a.type.fields()        # records: name, bitpos, bitsize, type
gdb.selected_inferior().read_memory(addr, length)
gdb.parse_and_eval("a + 6")
```

At `-O0`, locals are normally addressable; `frame.read_var` returns a `gdb.Value` with `.address`. If a value is register-resident (`.address is None`), read its value but synthesize a slot and mark it "address not observable"; pointer relationships to it cannot be reconstructed. `-fno-omit-frame-pointer` keeps frame-base information available.

### 2.2 Stop semantics and snapshots

A breakpoint at `file:line` stops **before** that line's statements execute. Define the trace contract explicitly:

- `state_before(line)` is the snapshot at the breakpoint for that line.
- `state_after(line)` is the snapshot at the next breakpoint (or program exit), minus variables whose lifetime ended.
- A line's writes are the byte diff between `before` and `after`.
- For loops, the same line is visited multiple times; record an event sequence with hit count and call stack, not a single value per line.
- For declarations, hide a variable before its declaration and lifetime starts. At the declaration's own breakpoint, show "not initialized yet" rather than reading stack garbage. With `int b{a + 6};`, `b` has a value only after the line executes.

This contract matters for the proof: at line 4, the `b` declaration, `b` is not initialized; at line 5, `b` is 11; at line 6, `a` is 7 and `b` is still 11.

### 2.3 Pointer values and pointees

Read the pointer as an integer (`int(p)`), then map it through an object/address table:

- Build the table from AST declarations plus GDB addresses for locals, globals, and allocated blocks.
- For each tracked object, record its real address range and its synthetic range.
- Resolve a pointer to `(object_id, offset)` if the address falls inside a tracked object; otherwise `unknown`, `null`, or `dangling`.
- Represent pointer bytes in memory as the synthetic target address. For `int* q = &s.i`, if `s` is synthetic 108 and `i` has offset 4, `q` displays as `0x70` (112) and `*q` resolves to `s.i`.
- Pointer arithmetic is scaled by the pointee size from the AST/layout, not assumed to be 1.
- For pointers to pointers, apply the same mapping recursively; for arrays, record element size and length.

Do not rely on the numeric pointer value for teaching. The renderer should show `p -> s` and `q -> s.i`, with the synthetic address as a secondary label.

### 2.4 Writes: diff, nominal width, and out-of-bounds

Take a byte snapshot of the relevant regions at every stop. After the next stop, diff the snapshots and attribute changed ranges using the layout:

- **Full write:** changed length equals the lvalue's `sizeof` (for example `*q = 0x55667788`, an `int` lvalue, 4 bytes).
- **Partial write:** changed length is smaller than the enclosing object's size (for example `p[4] = 0xAA`, a `char` lvalue, 1 byte inside a 4-byte `int`). The lvalue's own width is still 1; "partial" describes the effect on the containing object.
- **Oversized/out-of-bounds write:** changed range extends beyond the lvalue's object or crosses into the next object (for example writing 8 bytes through `long long*` into the first `int` of `struct P { int a, b; }` changes both `a` and `b`). Mark it as undefined behavior in the explanation; the byte diff is what actually happened under this compiler at `-O0`, not a guarantee.

Verified pointer-write evidence:

```cpp
struct S { char c; int i; };
S s{1, 0x11223344};
char* p = reinterpret_cast<char*>(&s);
int* q = &s.i;
p[4] = 0xAA;
*q = 0x55667788;
```

At the relevant stops, `p[4] = 0xAA` changes one byte of `s.i`; `*q = 0x55667788` changes all four bytes. The raw bytes of `s` after the first write are `01 00 00 00 aa 33 22 11` (little-endian), demonstrating a partial modification of `i`. For the oversized case:

```cpp
struct P { int a, b; };
P p{0x11111111, 0x22222222};
*reinterpret_cast<long long*>(&p.a) = 0x3333333344444444LL;
```

GDB shows `p = {a = 0x44444444, b = 0x33333333}` and `x/8bx &p` shows `44 44 44 44 33 33 33 33`: an 8-byte write crossed the `a`/`b` boundary.

For writes performed by library calls (`memcpy`, `memset`, `std::cin >> x`, a function taking `T*`), the assignment AST may not identify the destination. Use the diff plus call arguments; if attribution to a specific source expression is required, break on the callee and inspect its pointer arguments. A diff is authoritative for "which bytes changed"; AST lvalue resolution explains "which object/field the source intended to write".

### 2.5 Resolving lvalues from the AST

To attribute a write, resolve the assignment's left-hand side:

| AST node | Resolution |
|---|---|
| `DeclRefExpr` | variable's object |
| `MemberExpr` (`.` / `->`) | base object plus `FieldDecl` layout offset; `->` first dereferences the pointer |
| `ArraySubscriptExpr` | base pointer/array plus index times element size |
| `UnaryOperator '*'` | pointer target |
| `ImplicitCastExpr` / `ParenExpr` | recurse through the child |
| `CXXOperatorCallExpr` (`[]`, `=`, `<<`) | use the operator's declaration and reference arguments; for `[]`, element size from the result type |

The static type of the lvalue gives the nominal write width. The runtime diff gives the actual bytes. If they disagree (aliasing, out-of-bounds, a function write), prefer the diff and add a diagnostic; do not "fix" the bytes to match the type.

## 3. Synthetic address model

### 3.1 Why normalization is necessary

Real stack addresses vary between runs when ASLR is enabled and between debuggers. On the test machine, with GDB's default randomization disabled, `a` was stable at `140737488344380`; with `set disable-randomization off`, two runs gave `140728135612988` and `140723484479868`. LLDB produced yet another address. None of these belong in course output.

### 3.2 Normalize using debug info, not declaration order

For the proof snippet, `readelf --debug-dump=info proof` reports:

```text
DW_AT_location : DW_OP_fbreg: -4   # a
DW_AT_location : DW_OP_fbreg: -8   # b
```

The frame base is the frame pointer (`rbp` on this x86-64 build); both offsets are relative to it. Map the lowest tracked frame byte to 64:

```text
b: frame_base - 8 -> 64
a: frame_base - 4 -> 68
```

This preserves compiler-chosen order, alignment, holes, and adjacency. Do **not** simply assign addresses in declaration order (`a=64`, `b=68`): that would misrepresent this frame, where `b` is at the lower address, and would break oversized-write examples that depend on the real neighbor.

Recommended regions:

| Region | Synthetic base | Contents |
|---|---:|---|
| stack frames | 64, then the next aligned region per frame | locals, parameters, temporaries |
| globals/statics | 4096 | global objects, string literals if modeled |
| heap | 8192 | allocations, in allocation order |
| unknown | 0 | null, dangling, or unmapped pointers |

Within a frame, use `synthetic = 64 + (real - real_frame_min)` (or, when using DWARF, `synthetic = frame_base_synth + DW_OP_fbreg`, with `frame_base_synth = 72` in the proof); align each object to its `alignof`. For objects without an address, allocate a slot but mark `address_observable: false`.

If debug info is unavailable, fall back to GDB's actual addresses and normalize by the minimum tracked address. The result is still deterministic, but it loses DWARF's explicit frame-relative explanation. Prefer the DWARF route for the production tool; it is stable and can be computed with `readelf`/`pyelftools` without a debugger stop.

### 3.3 Pointer width and `int64_t`

Pointers are 8 bytes on the course target. Verify, don't assume:

```python
gdb.lookup_type("void").pointer().sizeof  # 8
gdb.lookup_type("int").pointer().sizeof   # 8
```

The tracer must not rewrite source types. `int64_t` is a source-authoring option for examples where an 8-byte scalar slot next to a pointer makes the diagram clearer, not a tracer transformation. It is also not a cure for padding: `struct B { char c; int64_t i; }` has **7** bytes of padding, while `struct A { char c; int i; }` has **3**. Use the layout dump for every type. If a new example uses `int64_t`, add a `static_assert(sizeof(int64_t) == sizeof(void*))` only if the example actually depends on that equality; otherwise let the layout speak.

## 4. Evaluation order and subexpression results

### 4.1 Guarantees to encode

Use the C++ standard as the source of truth; the AST tells you which constructs are present, not what order the language guarantees.

| Construct | Guarantee |
|---|---|
| full-expressions in a block | sequenced in source order |
| braced-init-list `{a, b}` | initializer-clauses evaluated in order |
| built-in assignment `lhs = rhs` | right operand sequenced before left (since C++17); overloaded `operator=` follows the function-call rule below |
| function call `f(args)` | postfix expression sequenced before arguments; arguments indeterminately sequenced relative to each other |
| `&&`, `||`, `?:`, comma | left-to-right / conditional / left-to-right as specified |
| ordinary operands of most operators | unsequenced relative to each other |

Relevant standard clauses: [`[intro.execution]`](https://eel.is/c++draft/intro.execution), [`[expr.assign]`](https://eel.is/c++draft/expr.assign), [`[expr.call]`](https://eel.is/c++draft/expr.call), [`[dcl.init.list]`](https://eel.is/c++draft/dcl.init.list), [`[expr.log.and]`](https://eel.is/c++draft/expr.log.and), [`[expr.cond]`](https://eel.is/c++draft/expr.cond), [`[expr.comma]`](https://eel.is/c++draft/expr.comma). Note that `https://eel.is/c++draft/expr.ass` redirects to `expr.assign`.

The tracer should label the order it **observed** in GDB separately from the order the language **guarantees**. For unsequenced operands, do not present the debugger's left-to-right evaluation as a rule. For the course's examples, prefer snippets whose order is guaranteed, so the visualizer can make a definite claim.

### 4.2 Subexpression results

GDB can evaluate a pure expression at a stop:

```text
(gdb) break proof.cpp:4
(gdb) run
(gdb) print a
$1 = 5
(gdb) print a + 6
$2 = 11
```

But `gdb.parse_and_eval` uses the **current** state. At line 6, after `a = 7`, `a + 6` returns 13, not the 11 that initialized `b`. This is not a bug in GDB; it is the wrong state for the historical expression. Evaluate at the line where the expression is evaluated, or use the snapshot from that stop.

For displayed intermediate values, a pure AST evaluator over the snapshot is safer than re-evaluating source text:

- integer, boolean, and character literals;
- `DeclRefExpr` maps to the snapshot value;
- `UnaryOperator`, `BinaryOperator`, `ConditionalOperator`, `ParenExpr`, `ImplicitCastExpr` (numeric casts and lvalue-to-rvalue);
- `sizeof` and `alignof` map to Clang type facts;
- `MemberExpr` and `ArraySubscriptExpr` read bytes using the layout;
- anything with side effects or a function call is marked unknown, or uses a GDB call/return-value watchpoint; never execute the expression twice just to display it.

This evaluator is intentionally small. It is not a C++ interpreter and must not try to implement overload resolution, object lifetime, or undefined behavior.

## 5. Minimal proof

### 5.1 The requested snippet

```cpp
#include <iostream>

int main() {
    int a{5};
    int b{a + 6};
    a = 7;
    std::cout << b;
}
```

Line 1 is the include, line 3 is `int a{5};`, line 4 is `int b{a + 6};`, line 5 is `a = 7;`, and line 6 is the output.

Static facts from the AST:

- `a` and `b` are `int`;
- `a + 6` is `int`, `prvalue`, `BinaryOperator '+'`; its left operand is an lvalue `int` converted by `LValueToRValue`; its right operand is `IntegerLiteral 6`;
- `b` is initialized by an `InitListExpr` containing that binary operator;
- the `std::cout << b` expression is a `CXXOperatorCallExpr`; its type is the stream type (`__ostream_type`, which desugars to `std::basic_ostream<char>` in this dump), and `b` is the `int` argument.

A minimal GDB Python driver:

```python
import gdb

class LineBreakpoint(gdb.Breakpoint):
    def stop(self):
        frame = gdb.newest_frame()
        line = frame.find_sal().line
        values = {}
        for name in ("a", "b"):
            try:
                values[name] = int(frame.read_var(name))
            except gdb.error:
                values[name] = None
        print(line, values)
        return False

for line in range(3, 7):
    LineBreakpoint(f"proof.cpp:{line}")
gdb.execute("run")
```

Run it with:

```bash
gdb -q -batch ./proof -x trace-min.py
```

Raw output includes the declaration stop and uninitialized slots:

```text
3 {'a': 0, 'b': 1}
4 {'a': 5, 'b': 1}
5 {'a': 5, 'b': 11}
6 {'a': 7, 'b': 11}
11
```

After applying the declaration/lifetime filter, the runtime facts are:

```text
line 4 entry: a = 5, b not initialized yet
line 5 entry: a = 5, b = 11
line 6 entry: a = 7, b = 11
```

The program prints `11`, not `13`. `b` was initialized from the value of `a + 6` at line 4; assigning 7 to `a` later does not recompute `b`. This is exactly the distinction the visualizer must make between a **value copied at initialization** and a **live expression**.

Synthetic addresses from DWARF (`a: fbreg -4`, `b: fbreg -8`):

```text
b @ 64 = 0x0b 00 00 00
a @ 68 = 0x07 00 00 00   (line 6)
```

The real addresses were stripped; only the relative layout remains. At line 4, before `b` is initialized, its slot is shown as "uninitialized", not as garbage.

### 5.2 Pointer and write proof

```cpp
struct S { char c; int i; };
S s{1, 0x11223344};
char* p = reinterpret_cast<char*>(&s);
int* q = &s.i;
p[4] = 0xAA;
*q = 0x55667788;
```

Layout: `c` at offset 0, 3 bytes of padding, `i` at offset 4, `sizeof(S) = 8`. If `s` is synthetic 108, `p` displays as `0x6c` (`s + 0`) and `q` as `0x70` (`s.i`, 108 + 4). After `p[4] = 0xAA`, only the low byte of `i` changes (a partial write into `s.i`); after `*q = 0x55667788`, all four bytes of `i` change. The byte diff, not a guess from the pointer type, reports the exact bytes.

Oversized case:

```cpp
struct P { int a, b; };
P p{0x11111111, 0x22222222};
*reinterpret_cast<long long*>(&p.a) = 0x3333333344444444LL;
```

The `long long` lvalue is 8 bytes; it spans `p.a` and `p.b`. GDB shows `p = {a = 0x44444444, b = 0x33333333}`. The trace marks the write as out-of-bounds/undefined behavior while still showing the observed bytes.

## 6. Alternatives considered

### 6.1 Clang AST JSON + GDB Python (recommended)

Strengths: exact static types and layout from the compiler used to build; works on ill-formed snippets; runtime bytes from a mature debugger; no compiler plugin build; the Python API is sufficient for snapshots and pointer tracking. Weaknesses: Clang JSON is an internal, version-dependent format; GDB is Linux/Unix-centric; debugger line granularity; executing lab code requires sandboxing.

### 6.2 LLDB Python

Tested LLDB 17.0.6. Embedded Python works:

```bash
/usr/lib/llvm-17/bin/lldb -b ./proof \
  -o 'breakpoint set --file proof.cpp --line 6' \
  -o run \
  -o 'script import lldb; ...'
```

`SBFrame.FindVariable`, `SBValue.GetValue`, `SBValue.GetAddress().GetLoadAddress`, and `SBType.GetFieldAtIndex(i).GetOffsetInBytes()` all work; `GetType().GetByteSize()` gives record size. On this Ubuntu image, standalone `python3 -c "import lldb"` was unusable: the module directory existed but had no `SBDebugger` (the `python3-lldb-17` bindings were not installed). LLDB alone does not provide a source AST for arbitrary subexpressions or non-compiling code, so it cannot replace the Clang static pass. Keep it as an optional runtime adapter for macOS, not the primary implementation.

### 6.3 Clang tooling, `clang-repl`, Cling, cppyy

- **LibTooling and Clang tooling** give precise AST access, but require building and linking against LLVM and Clang, pin the binary to an LLVM version, and still provide no runtime values. Rejected for local maintenance.
- **`clang-repl`** is a REPL/JIT, not a source tracer. On the test image only the LLVM 21 tree provided it; LLVM 17 had none. It does not expose source-level stepping, breakpoints, or byte snapshots. In testing, value printing returned `Not implement yet.`, an invalid declaration printed `error: Parsing failed.`, and incremental state is not a substitute for tracing a file. Rejected.
- **Cling** requires building LLVM/Clang or installing ROOT; it is an interpreter/JIT, not a debugger, and brings a large dependency tree. **cppyy** is a Python-C++ binding layer on Cling, with the same problem plus Python binding complexity. Both are far heavier than invoking `clang++` and `gdb`, and neither gives the required per-line byte trace. Rejected.

### 6.4 A restricted AST interpreter

Attractive on paper: parse the AST, evaluate the small subset the labs use, and avoid a debugger. Rejected because C++ semantics are not small: overload resolution, implicit conversions, object lifetime, initialization order, aliasing, pointer provenance, undefined behavior, and library calls all matter. Clang's own constant interpreter is already a substantial component and only handles constant evaluation, not arbitrary runtime programs ([Clang Constant Interpreter](https://clang.llvm.org/docs/ConstantInterpreter.html)). A hand-written interpreter would be a second, subtly wrong compiler. A pure expression evaluator over debugger snapshots is the acceptable narrow exception.

## 7. Dependencies and integration

| Dependency | Tested version | Purpose | Required |
|---|---|---|---|
| `clang++` | 17.0.6 (`/usr/lib/llvm-17/bin`) | AST JSON, diagnostics, record layouts, compile | yes |
| `gdb` with Python 3 | 17.1 | runtime values, bytes, addresses | yes for dynamic traces |
| `python3` | 3.14.4 | orchestration, JSON, GDB scripting | yes |
| `readelf` (binutils) | 2.46 | DWARF `fbreg` and frame information | optional; GDB can substitute |
| `pyelftools` | optional | parse DWARF without `readelf` | optional |
| LLDB | 17.0.6 | alternate runtime adapter | no |
| Cling, cppyy, LLVM dev | not installed | rejected approaches | no |

On Ubuntu, the runtime packages are `clang`, `gdb`, `python3`, and `binutils`; the LLDB adapter additionally needs the matching `python3-lldb-<version>` package. The tested machine did not have `clang++` on `PATH`; the integration should resolve it via `shutil.which("clang++")`, an explicit `--clang` option, or a versioned `/usr/lib/llvm-*/bin/clang++` fallback, and report the chosen version in the trace metadata.

The natural home is a Python module in `course_maintenance` (the publishing and validation tool is already Python; CI runs `python3 course_maintenance/publish.py`). This worktree's `course_maintenance` submodule was not initialized, so the module layout below is a proposal, not a description of its current internals. A module can:

1. extract the snippet and line map from the lab Markdown;
2. run the static pass and cache AST/layout by source hash;
3. compile and run the dynamic pass in a temporary directory;
4. emit a deterministic JSON trace (sorted keys, no timestamps, synthetic addresses only);
5. expose a `--check` mode that verifies `clang++` and `gdb` versions and fails with an actionable message.

No compiler plugin build is needed. If CI lacks `gdb`, static traces can still be generated; runtime tests should be a separate job or an explicit local check. The course workflow currently runs on `ubuntu-latest`; adding `clang` and `gdb` there is a package-install step, not a build-from-source step.

## 8. Risks and limitations

- **Internal AST JSON schema.** Pin Clang and keep golden fixtures; test after compiler upgrades. Prefer stable node kinds and fields (`kind`, `type.qualType`, `valueCategory`, `opcode`, `castKind`) and treat unknown fields as optional.
- **Location compression and macros.** Offset/line mapping needs care; macro expansions may point at headers. The labs are mostly macro-free; handle `spellingLoc`/`expansionLoc` defensively.
- **Line granularity.** Multiple statements on one line cannot be separated by a line breakpoint. Require one statement per line in lab snippets, or use AST offsets and instruction addresses for finer stops.
- **Optimized code.** `-O0` is required for predictable values and frame layout; never trace optimized builds for teaching output.
- **Uninitialized values and undefined behavior.** Reading uninitialized storage or writing out of bounds is undefined behavior. Show "uninitialized" and label UB; do not imply the observed garbage or clobber is portable.
- **Library calls, templates, and std objects.** `std::cout`, `std::string`, and containers have complex internal layouts and pretty-printers. Trace the lab's scalar and struct objects; treat library internals as opaque unless explicitly modeled.
- **Threads and recursion.** A single breakpoint stream interleaves events; record thread and frame identity and event order. Recursion needs per-frame regions.
- **Security.** Tracing executes the lab program. Run it in a temp directory with a timeout and resource limits; do not enable network access for untrusted snippets.
- **Platform.** GDB Python is the primary Linux path; LLDB is the macOS fallback. Windows would need a separate debugger adapter; do not claim portability without testing.

## 9. Recommended next steps

1. Implement the static pass first, with fixtures for `int b{a + 6}`, a padded struct, a pointer/array, and the `p = value` ill-formed puzzle. Assert exact `qualType`, `valueCategory`, offsets, `sizeof`, and diagnostics.
2. Implement the GDB snapshot pass for straight-line snippets, with the entry/exit contract and synthetic stack mapping. Use the requested snippet as the acceptance test: line 4 `a=5`, line 5 `b=11`, line 6 `a=7, b=11`, output `11`.
3. Add byte diffs for pointer writes: partial `p[4]`, full `*q`, and oversized `long long*` into `struct P`.
4. Add a deterministic JSON schema and golden tests; strip all real addresses at the boundary.
5. Only then integrate extraction and rendering into `course_maintenance`.

## Sources

Primary sources used for this research (accessed 2026-10-20):

- Clang AST overview: <https://clang.llvm.org/docs/IntroductionToTheClangAST.html>
- Clang AST JSON implementation: <https://github.com/llvm/llvm-project/blob/main/clang/lib/AST/JSONNodeDumper.cpp>
- Clang record layout dump implementation: <https://github.com/llvm/llvm-project/blob/main/clang/lib/AST/RecordLayoutBuilder.cpp> (the `*** Dumping AST Record Layout` output)
- Clang tooling: <https://clang.llvm.org/docs/Tooling.html>
- Clang REPL: <https://clang.llvm.org/docs/ClangRepl.html>
- Clang constant interpreter: <https://clang.llvm.org/docs/ConstantInterpreter.html>
- GDB Python API: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-API.html>
- GDB values from inferior: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Values-From-Inferior.html>
- GDB types in Python: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Types-In-Python.html>
- GDB symbols and `ptype /o`: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Symbols.html>
- GDB memory and `x`: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Memory.html>
- GDB inferior memory API: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Inferiors-In-Python.html>
- GDB ASLR control: <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Starting.html>
- LLDB Python API: <https://lldb.llvm.org/python_api.html>
- C++ evaluation order: <https://eel.is/c++draft/intro.execution>
- C++ assignment: <https://eel.is/c++draft/expr.assign>
- C++ function calls: <https://eel.is/c++draft/expr.call>
- C++ list-initialization: <https://eel.is/c++draft/dcl.init.list>
- C++ logical AND: <https://eel.is/c++draft/expr.log.and>
- C++ conditional operator: <https://eel.is/c++draft/expr.cond>
- C++ comma operator: <https://eel.is/c++draft/expr.comma>
- DWARF 5: <https://dwarfstd.org/doc/DWARF5.pdf>
- Cling: <https://github.com/root-project/cling>
- cppyy: <https://cppyy.readthedocs.io/en/latest/>

Local commands used for verification: `clang++ -cc1 --help` (AST dump and record-layout flags), `gdb --version`, `lldb --version`, `readelf --debug-dump=info`, and the proof programs described above. The exact tool versions are recorded at the top of this document.
