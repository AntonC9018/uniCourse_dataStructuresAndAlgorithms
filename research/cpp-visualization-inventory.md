# C++ memory/pointer visualization inventory

Inventory of candidate examples in `en/labs/cpp` and their Russian mirrors, for the
wayfinder map [Automatic memory and pointer visualizations for CPP labs](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/issues/50).

- Branch: `research/cpp-visualization-inventory`
- Base commit: `d800f68bd659ba723ae6aea1baa5ebc311594671`
- Scope: the 13 lab files named in issue #52.
- Method: read every listed lab in full; checked the key compile/runtime claims with
  `g++ (Ubuntu 15.2.0) -std=c++20 -Wall -Wextra`, copying exact lab snippets where the
  answer was not obvious.
- Counts below are rows in this document, not total lab examples. Grouped rows are
  explicitly numbered and need one tag per source fence when tagging.

## Path convention and en/ru mirroring

Every filename in the tables is relative to `en/labs/cpp/`. The Russian counterpart is
`ru/labs/cpp/<same filename>` with the same example number and title, with two
exceptions caused by ordering differences:

| English | Russian |
| --- | --- |
| `en/labs/cpp/18_span.md` | `ru/labs/cpp/19_span.md` |
| `en/labs/cpp/21_advanced_practice.md` | `ru/labs/cpp/22_advanced_practice.md` |

There is also an English `19_optional.md` / Russian `18_optional.md` swap, but that lab
is outside this ticket. `12_array_practice.md` §23 has a slightly different Russian
title ("Хранение в байтах") but the same number and code. All other listed files match
number-for-number.

## How to read the flags

- **Compiles**: `yes` means the snippet builds as printed inside the lab's stated
  `main`/preamble; `no` means a deliberate type error or an undeclared identifier;
  `yes*` means it only builds after an insertion or a missing include is supplied.
  Fragment-only examples are assumed to be placed in the lab's documented preamble.
- **State changes**: any write after the initializing write. "no" means values are only
  initialized or read; the pointer relationship itself may still be the point.
- **int64_t**: `irrelevant` means no padding or width lesson is involved; `removes
  padding` means `int64_t` would remove unrelated padding and is recommended for the
  visual; `keep int` / `changes lesson` means the 4-byte `int` is part of the point.
- **Diagram**: only three lab examples currently have a real diagram, plus the ASCII
  stack tables in lab 30. `replace` means the map's prototype ticket explicitly targets
  the existing asset.

## Summary

| Category | Rows | Prototype ticket |
| --- | ---: | --- |
| Base timeline | 6 | #57 |
| Casts/bits | 7 | #58 |
| Pointers | 26 | #59 |
| Pointer type punning | 2 | #60 |
| Expression types | 17 | #61 |
| Struct layout | 14 | #62 |
| **Six requested categories** | **72** | |
| Missing: references/aliases | 9 | none |
| Missing: `std::span` / pointer+length | 8 | none |
| Missing: stack frames | 2 | none |
| **Total** | **91** | |

The current prototype list has no category for references, for `std::span`'s
pointer+length view, or for stack frames. Arrays/pointer decay can probably be folded
into the pointers category, but only if the scene library supports a contiguous strip of
cells; plain array indexing is otherwise only base-timeline material. Heap/dynamic
allocation has no canonical lab example (see "Task-only labs").

## 1. Base timeline

Prototype #57 already names §6 and §18 of `02_variables.md` as the vertical slice and
swap variation. These rows are the plain-variable state changes that fit the same scene.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `02_variables.md` §4 "Assigning one variable to another" | yes | yes: `a` 5→6, then `b` 6→7 | assignment / expression timeline | irrelevant | — | Shows that assignment copies the value at that moment; `b = 7` does not revisit `a`. |
| `02_variables.md` §6 "Assigning an expression to a variable" | yes | yes: `b`←11 before `a`←7 | expression timeline, assignment | irrelevant | — | This is the map's base example; animate `a + 6` → `5 + 6` → `11`. |
| `02_variables.md` §10 "Empty initialization" | yes | yes: `a`←0 | value initialization | irrelevant | — | No prior value; distinguish `int a{}` from uninitialized `int a;`. |
| `02_variables.md` §11 "Assigning empty braces" | yes | yes: `a` 7→0 | assignment, value initialization | irrelevant | — | `a = {}` writes zero; it does not de-initialize the cell. |
| `02_variables.md` §12 "An `int{}` expression" | yes | yes: `a` 7→0, `b`←0 | expression timeline, value initialization | irrelevant | — | `int{}` is a typed expression; same scene as §6 with a literal-like RHS. |
| `02_variables.md` §18 "Swapping variables" | yes | yes: `a` 1→2, `b` stays 2 | assignment/swap (failed swap) | irrelevant | — | The point is the lost old value; do not draw a successful swap. The corrected temp-variable version is printed in the answer. |

## 2. Casts/bits

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `03_numeric_conversions.md` §2 "A cast changes the expression type" | yes | no: initialization only | cast/bits, expression types | n/a | — | `static_cast<double>(value)` changes the expression type, not the `int` variable. Show `7`, `3.5`, `3`. |
| `03_numeric_conversions.md` §3 "`static_cast` to a larger type" | yes | no: initialization only | cast/bits (zero extension) | n/a | — | `uint8_t` 5 → `int` 5; upper bytes become zero. |
| `03_numeric_conversions.md` §4 "`static_cast` of a negative number to a larger type" | yes | no: initialization only | cast/bits (sign extension) | n/a | — | `int8_t` −3 is `1111 1101`; widening to 32 bits fills with 1s. The lab writes out the bits, no diagram. |
| `03_numeric_conversions.md` §5 "`static_cast`" | yes | no: `a`, `b`, `c` initialized once | cast/bits (truncation) | n/a | — | The prototype example for #58. `uint32_t` 256 → `uint8_t` 0 → `uint32_t` 0; high 3 bytes dropped. |
| `03_numeric_conversions.md` §6 "Bitwise operation (advanced level)" | yes | no: initialization only | cast/bits (invert, zero extension) | n/a | — | `uint8_t` 0 → `~` → 255; `int32_t` zero-extends `0xFF`. Distinguish bit width from value. |
| `03_numeric_conversions.md` §7 "Changing the sign (advanced level)" | yes | no: initialization only | cast/bits (sign interpretation) | n/a | — | 127 stays 127; the answer also explains 128 → −128. Use one concrete value per animation to avoid ambiguity. |
| `18_span.md` §28 "Looping in reverse (2)" | yes | yes: `size_t i` underflows | cast/bits (unsigned wraparound) | n/a | — | `s.size() - 1` wraps to `SIZE_MAX`; `assert` aborts. Platform-width dependent; do not use a literal max value without a note. |

## 3. Pointers

Prototype #59 names §1, §3, §13 and §14 of `04_pointer.md`. The table includes the
struct/array follow-ups that use the same pointer scene.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `04_pointer.md` §1 "Variable address" | yes | no: `b` initialized to `&a` | pointer address/arrow | irrelevant | — | Pointer storage is 8 bytes; `b` is not an `int`. The address itself is synthetic in the visual. |
| `04_pointer.md` §3 "Dereference operator (writing)" | yes | yes: `a` 1→2 | pointer write | irrelevant | — | Canonical write-through-pointer scene. |
| `04_pointer.md` §10 "Dependence of the address on the value" | yes | yes: `a` 5→6; `b`, `c` unchanged addresses | pointer address stability | irrelevant | — | `a = 6` writes the existing cell; `&a` does not change. Draw `b` and `c` as two arrows to the same cell. |
| `04_pointer.md` §11 "It is the same memory!" | yes | yes: `*ap` 5→6, then `a` 6→7 | pointer read/write alias | irrelevant | — | Both writes target one cell; show two names, one cell. |
| `04_pointer.md` §12 "Assigning a value through a pointer" | yes | yes: `*b = 5` initializes `a` | pointer write | irrelevant | — | Writing through a pointer to an uninitialized `int` is defined; reading `a` before the write would be UB. |
| `04_pointer.md` §13 "Reassigning a pointer" | yes | yes: `a` 5→6, `b` 7→8, `p` retargeted | pointer reassignment | irrelevant | — | Prototype #59 case. Old arrow must visibly detach from `a` and attach to `b`. |
| `04_pointer.md` §14 "Double pointer" | yes | yes: `a` 5→7, `b` 6→8, `p` retargeted via `*pp` | double pointer | irrelevant | — | Prototype #59 case. Show `pp → p → a/b`; `*pp = &b` changes the middle cell, `**pp` changes the final cell. |
| `04_pointer.md` §20 "Pointer to itself" | yes | yes: `p` nullptr→`&p` | pointer address/arrow (self-loop) | n/a | — | `void* p` stores its own address; draw a self-arrow. Only `void*` avoids type friction. |
| `04_pointer.md` §21 "Empty pointer initialization" | yes | no: `p`←nullptr | pointer address/arrow (null) | n/a | — | Null arrow must be visually distinct from "uninitialized/garbage"; `int* p;` is the contrasting case, not shown as executable. |
| `04_pointer.md` §22 "Copying a variable and a pointer with similar names" | yes | yes: `*px = 1`; `y` stays 0 | pointer copy vs value copy | irrelevant | — | `int y{x}` and `int* py{px}` look similar but one copies a value and one an address. Four cells plus two arrows. |
| `05_struct.md` §11 "Structure address (2)" | yes | yes: `a.f1` 5→7 before `b = *pa` | pointer read/arrow | irrelevant | — | `b` copies the current value, not the values at the moment `pa` was taken. |
| `05_struct.md` §12 "The `->` operator" | yes | yes: `a.f1` 5→7, `a.f2`←6 | pointer write/arrow | irrelevant | — | `(*pa).f2` and `pa->f1` are the same access path. |
| `05_struct.md` §14 "Overwriting through an address" | yes | yes: `*pa = {5, 6}` writes both fields | pointer write (whole struct) | irrelevant | — | Braced assignment writes the whole struct; not a partial field write. |
| `05_struct.md` §17 "An address field" | yes | yes: `*a.f1 = 2` writes `num` | pointer field, pointer write | irrelevant | — | `*a.f1` parses as `*(a.f1)`. Struct contains a pointer, not the pointee. |
| `09_c_array.md` §11 "auto from an array element address" | yes | yes: `*p = 9` writes `arr[1]` | pointer write, array element | irrelevant | — | Array element is a cell inside a contiguous strip; pointer arrow points into the strip. |
| `09_c_array.md` §12 "A pointer as the element type" | yes | yes: `a` and `b` become 3 | pointer array | irrelevant | — | Array cells contain 8-byte pointers; `*arr[0]` writes through the first pointer. |
| `09_c_array.md` §13 "Using an array as a pointer" | yes | yes: `*arr = 1` writes `arr[0]` | array decay, pointer alias | irrelevant | — | `arr` decays to `&arr[0]`; `p`, `*arr`, and `arr[0]` all hit the same cell. |
| `09_c_array.md` §17 "Array assignment (2)" | yes | yes: `arr1[0]`←3; other elements unchanged | partial write, array decay | irrelevant | — | `*arr1 = *arr2` copies one element only. Do not animate a whole-array copy; §16 is the non-compiling whole-array attempt. |
| `11_pointer_arithmetic.md` §1 "Moving a pointer by 1" | yes | yes: `p` advanced, `arr[1]`←2 | pointer arithmetic, pointer write | irrelevant | — | `p + 1` advances one `int` (4 bytes), not one byte. |
| `11_pointer_arithmetic.md` §2 "Returning the next array element address" | yes | yes: `*next = 8` writes `arr[1]` | pointer arithmetic, function return | irrelevant | — | Pointer outlives the callee because it points into `main`'s array; caller must ensure the element exists. |
| `11_pointer_arithmetic.md` §3 "Accessing an array element through an expression" | yes | yes: `*(p + 1) = 6`; `p` unchanged | pointer arithmetic, temporary address | irrelevant | — | The temporary address is not a new variable cell; only the write target changes. |
| `11_pointer_arithmetic.md` §10 "Advanced level: addresses of local variables" | yes | no: only reads addresses | stack address reuse | irrelevant | — | Addresses are implementation-defined; reuse after return is likely but not guaranteed. Use synthetic stack layout, not real addresses. |
| `11_pointer_arithmetic.md` §11 "Reading past a one-element array (advanced)" | yes | no: read only | pointer-to-larger/smaller overwrite (adjacent object read) | irrelevant | — | One-past pointer formation is valid, dereference is UB. Neighbor placement is not guaranteed; do not promise the printed `6`. |
| `11_pointer_arithmetic.md` §12 "Writing past an array (advanced)" | yes | yes: `*past = 7` (UB) | pointer write, adjacent object overwrite | irrelevant | — | Same one-past rule; the write is UB and may or may not hit `neighbor`. Show as UB, not as a guaranteed overwrite. |
| `15_const.md` §17 "Observing a change through a pointer to const" | yes | yes: `a.x` 1→3, `p->x` observes | pointer read (const access path) | irrelevant | — | `const Position*` restricts writes through `p`, not direct writes to `a`. Use a read-only arrow style. |
| `18_span.md` §1 "Pointer indexing" | yes | yes: several writes to `arr[0..2]` | pointer indexing, pointer write | irrelevant | — | Many equivalent spellings (`*p`, `*(p+n)`, `p[n]`, `n[p]`) target the same cells; one animation can show the address arithmetic once and then collapse the syntax. |

## 4. Pointer type punning

Both lab examples are deliberately non-compiling. They are still the source of
prototype #60, which must use an explicit `reinterpret_cast` or a byte-pointer view to
make the overwrite observable.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `04_pointer.md` §8 "Pointer to a larger data type" | no: `uint8_t*` → `int*` | no | pointer-to-larger overwrite | n/a: 1- and 4-byte types are the lesson; do not widen | — | The lab's direct snippet is a compile error. A demo variant must cast; a write through `int*` would touch 4 bytes starting at a 1-byte object, including padding/adjacent objects. UB; no guaranteed neighbor. |
| `04_pointer.md` §9 "Pointer to a smaller data type" | no: `int*` → `uint8_t*` | no | pointer-to-smaller/partial overwrite | n/a: keep `int` | — | Direct snippet does not compile. A demo variant writes only the low byte of the `int`; show which byte changes and note endianness. The other 3 bytes stay. |

## 5. Expression types

This category is mostly static: annotate the type of each subexpression, and only
animate when there is a write. Prototype #61 names `04_pointer.md` §7.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `02_variables.md` §5 "Literals, variables and operators are expressions" | yes | no: `b`, `c` initialized | expression timeline/types | irrelevant | — | Literal `5`, variable read `a`, and operator expression `a + 6` all evaluate to typed values. |
| `02_variables.md` §13 "The `sizeof` operator" | yes | no | expression types (`sizeof` operand unevaluated) | irrelevant | — | `sizeof(a + 1)` does not evaluate `a + 1`; only its type matters. No runtime cells change. |
| `02_variables.md` §14–17 "`auto`" series | yes (except §15) | no: initialization only | type inference | irrelevant | — | §15 (`auto a;`) does not compile; §14/§16/§17 infer `int`. Show `auto` as a compile-time replacement, not a runtime tag. |
| `03_numeric_conversions.md` §1 "`auto` and `static_cast`" | yes | no | cast changes expression type | n/a | — | `static_cast<uint8_t>(5)` has type `uint8_t`; `auto` takes that type. |
| `04_pointer.md` §7 "Printing a complex expression" | yes | no: read only | pointer read, expression types | irrelevant | — | Prototype #61 example: annotate `b` as `int*`, `*b` as `int`, `(*b) + 7` as `int`; show `5 + 7 = 12`. |
| `04_pointer.md` §15–17 "`auto` from address/pointer" series | yes | yes (each writes through inferred pointer) | type inference, pointer/double pointer | irrelevant | — | §15 deduces `int*`, §16 deduces `int*` for the pointer copy and `int` for the value copy, §17 deduces `int**`. |
| `04_pointer.md` §19 "Pointer and variable sizes" | yes | no | expression types (`sizeof` pointer vs pointee) | irrelevant | — | `sizeof(ap)` is 8, `sizeof(*ap)` is 4; `*ap` is not evaluated. |
| `04_pointer.md` type-checking puzzles §6, §7, §15 | mixed: §6 yes, §7 no, §15 yes | §6 no write; §15 `count`←3 | dereference types, double pointer, numeric conversion | irrelevant | — | §7 (`result = *pp`) is the key "one dereference instead of two" error; §15 is a numeric conversion despite the pointer read. |
| `05_struct.md` §5 "Assigning a field from a temporary structure" | yes | no: `a`←1 | temporary struct expression, field read | irrelevant | — | `A{1, 2}.f1` creates a temporary value, then reads one field; the temporary is not a named variable. |
| `05_struct.md` §13, §15, §16 | no | no | invalid address/type claims | irrelevant | — | §13 `(&a)->field` is `A**`; §15 `&A` is a type, not an object; §16 `&A.f1` is a type field. All static type puzzles, no execution. |
| `05_struct.md` type-checking puzzles §1–10 | mixed: §8 and §10 yes; rest no | §8 copy, §10 `result`←5 | pointer depth/type compatibility | irrelevant | — | Best used as static type overlays; do not try to execute the non-compiling majority. |
| `09_c_array.md` §10 "auto from an array element" | yes | yes: `arr[1]` 7→9; `value` stays 7 | copy vs reference, type inference | irrelevant | — | `auto value{arr[1]}` copies an `int`; the later array write must not change `value`. |
| `09_c_array.md` §16 and §18 | no | no | array assignment/decay type errors | irrelevant | — | §16 whole-array assignment does not exist; §18 array decays to `int*` and cannot initialize `int`. |
| `14_reference.md` §1–4 | no | no | rvalue/lvalue, reference binding | n/a | — | All four are compile errors; useful static annotations (`5` is an rvalue, `&5` invalid, `int& a = 5` invalid). |
| `14_reference.md` §19 "Size of a reference" | yes | no | `sizeof` reference expression | n/a | — | `sizeof(b)` yields `sizeof(int)`, not a reference size; reference representation is implementation-defined. |
| `14_reference.md` §22–23 "`auto` makes a copy / `auto&` makes a reference" | yes | yes: `b = 6`; §22 leaves `a` 5, §23 writes `a` 6 | type deduction, copy vs alias | irrelevant | — | Pair the two scenes side by side to make the deduction difference obvious. |
| `15_const.md` const type-checking examples §1, §3, §5, §8, §9, §10, §14, §16, §18; const `std::array` §1, §3, §6, §7 | no | no | const access/type errors | irrelevant | — | Mostly static overlays. Grouping is only for inventory; each fence needs its own tag if tagged. §6 of the const-array section is a non-constant array-size error, not a pointer issue. |

## 6. Struct layout

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `05_struct.md` §2 "An expression of a structure type" | yes | no: temporary value | struct value layout | irrelevant: two ints, no padding | PNG `01_example_value_of_type_of_struct.png`; keep | The existing image already explains "suspended" temporary struct value. Do not replace it; the map says not to replace good existing diagrams. |
| `05_struct.md` §7 "Field addresses" | yes | yes: `*b = 5` writes `a.f` | struct field address/offset | irrelevant: single int, offset 0 | — | Field is at offset 0. Add a byte ruler only if it helps the pointer scene. |
| `05_struct.md` §14 "Overwriting through an address" | yes | yes: `*pa = {5, 6}` | whole-struct write | irrelevant: two ints, no padding | — | Aggregate assignment writes both fields; no partial write to show. |
| `05_struct.md` §18 "A nested structure" | yes | yes: `a.f`←3, `a.nested`←5, `a.nested.f`←6 | nested struct layout | irrelevant: nested ints, no padding | — | Show nesting as containment, not as a pointer. Designated initialization order is part of the code. |
| `05_struct.md` §19 "Copying a nested structure" | yes | yes: `a.nested.f`←3, `a.f`←4; `b` copy stays 1/2 | nested struct copy | irrelevant | — | The nested struct is inside `A` by value; copying `A` copies it. |
| `05_struct.md` §21 "Linked list" | yes | yes: node fields written; traversal; third print crashes | struct layout, pointer field, null deref | **removes padding**: `int value` + `Node* next` has 4 bytes padding; `int64_t` gives 8+8 | Mermaid flowchart; keep | Mermaid already explains the list; the map excludes replacing good Mermaid. Runtime crashes on the third `current->value`; tag the visual before the crash, or show the null arrow and stop. |
| `05_struct.md` §22 "Structure size (1)" | yes | no | struct size | irrelevant: two ints = 8, no padding | — | `sizeof(a) == sizeof(A) == 8`; good candidate for a compact static layout. |
| `05_struct.md` §23 "Field address from a structure address" | yes | yes: `*pf = 2` writes `a.f` | field offset through `->` | irrelevant: single int, offset 0 | — | `&pa->f` parses as `&(pa->f)`; the field address is the struct address for the first field. |
| `05_struct.md` §24 "Structure size (3)" | **no as printed**: missing `#include <cstdint>` in both en and ru | no | struct padding/alignment | **keep `int`**: the 4-byte slot and 3-byte padding are the lesson; `int64_t` changes the lesson | SVG `05_struct_alignment.svg`; **replace** (issue #62 explicitly targets it) | Add `<cstdint>` before tracing. `uint8_t f1; int f2; uint8_t f3` gives 12 bytes with 3 bytes of padding after `f1` and after `f3`. Any generated layout must match this exactly; do not "pack" it. |
| `05_struct.md` §25 "Structure size (4)" | yes | no | empty struct size | n/a | — | Size is 1, not 0, so distinct objects can have distinct addresses. |
| `05_struct.md` §26 "Copying a structure with a pointer field" | yes | yes: `*s2.pa = 2` writes `s1.a` | shallow copy, pointer field | **removes padding**: `int* pa` + `int a` has 4 trailing bytes; `int64_t a` gives 8+8 | — | Issue #62's "pointer-containing struct" candidate. Show that `s2.pa` still points at `s1.a`, not `s2.a`. |
| `11_pointer_arithmetic.md` §7 "Field address relative to a structure address" | yes | no: addresses only | field offset | irrelevant: single int, offset 0 | — | Prints 0; implementation-defined pointer-to-integer mapping. |
| `11_pointer_arithmetic.md` §8 "Field offsets" | yes | no | `offsetof` | irrelevant: two ints, offsets 0 and 4 | — | Exact offsets are implementation/alignment dependent; on this ABI 0 and 4. |
| `12_array_practice.md` §23 "Raw-byte storage (advanced)" | yes | yes: placement-new writes buffer; `position` changes | struct layout/alignment, raw bytes | **changes lesson**: `int`/`double` sizes and alignment are the point; do not widen | — | Uses `std::align`, placement `new`, `reinterpret_cast`, `std::byte`; exact used bytes (typically 16) depend on ABI. Practice solution, not an explanatory example; still a good struct-layout stress case. |

## Missing category: references and aliases

References are not pointers: they cannot be null, cannot be rebound, and assignment
through a reference writes the referent. A pointer prototype could draw them as a
dashed/immutable arrow, but that is a separate visual rule and should be decided
explicitly rather than silently folded in.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `14_reference.md` §5–7 "Reference from a variable / from a reference / assigning a number" | yes | mixed: §6–7 write `a` 5→6; §5 read-only | alias, write through reference | n/a | — | `int& c = b` binds to `a`, not to `b` as a separate cell. Assignment through a reference is not rebinding. |
| `14_reference.md` §11–12 "Assigning a variable to a reference" | yes | yes: `a`←2, then `a`←3; `b` stays 2 | reference cannot rebind | n/a | — | `c = b` overwrites `a`; it does not make `c` refer to `b`. This is the key difference from pointer reassignment. |
| `14_reference.md` §13–15 "Reference from dereference / pointer reassignment / address and reference" | yes | yes: `a` written via `*pa`, `r`, and `*c`; `b` unchanged in §14 | alias through pointer and reference | n/a | — | §14 is the important one: reassigning `p` does not change what `r` refers to. |
| `14_reference.md` §16 "References to fields" | yes | yes: `ra.x`←3, `ra.y`←4 | field reference | n/a | — | References to members are aliases into a larger object; show `rx`/`ry` pointing inside the `Position` cells. |
| `14_reference.md` §17–18 "Reference to a pointer" | yes | yes: `b`←3 through `rpa`/`rb` | reference to pointer | n/a | — | `rpa` aliases the pointer variable itself; `pa = &b` then `*rpa` writes `b`. Different from a pointer to pointer. |
| `14_reference.md` §20–21 "Example of using references" | yes | yes: amount 6→0; power 1→2 | function parameter by reference | n/a | — | Caller and callee share one object; no copy. Good candidate for a call/return timeline. |
| `15_const.md` §6 "Observing a change through a const reference" | yes | yes: `a` 5→6; `r` observes 5 then 6 | const reference, alias | n/a | — | `const int&` restricts writes through `r`, not direct writes to `a`. |
| `15_const.md` §13 "A const reference parameter" | yes | yes: `a.x` 1→5 between calls | const reference parameter | n/a | — | No object copy; the function reads the current `a.x`. |
| `18_span.md` §14 "Changing elements of a C++ array passed as a parameter (2)" | yes | yes: `arr[0]`←1 | reference parameter, array alias | n/a | — | Contrast with §13 (by value, no change). The reference points at the caller's whole array object. |

## Missing category: `std::span` / pointer+length

`std::span` is a two-word view (pointer + `size_t`), not a pointer and not a struct with
`int` fields. It needs its own compact scene or a "view" overlay.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `18_span.md` §17 "`std::span`" | yes | no: view creation only | pointer+length view | n/a | — | `sizeof(span)` is 16 on x64: 8-byte pointer + 8-byte length. Do not draw it as an array. |
| `18_span.md` §18 "`std::span` from a C++ array" | yes | yes: `arr[0]`←3, `arr[1]`←4 | view aliases array | n/a | — | Span reads current array values; it does not snapshot. |
| `18_span.md` §23 "Creating a subspan manually" | yes | no: reads three views | pointer+length, subrange | n/a | — | Same array with three different `(pointer, length)` views; show range overlay rather than copying cells. |
| `18_span.md` §25 "A subspan with the `subspan` method" | yes | no: reads three views | subspan | n/a | — | `subspan(1, 3)` is `data()+1, 3`; overlapping ranges must be legible. |
| `18_span.md` §26 "Details of `subspan`" | yes*: insert into §25 | no | out-of-range span | n/a | — | `subspan(2, 3)` on a 4-element array creates an invalid span; the lab says creating it is not itself UB, but reading beyond the array is. Do not draw the invalid range as valid memory. |
| `18_span.md` §4 "Reading beyond an array" | yes | no: UB read | out-of-bounds read | n/a | — | `arr[2]` on a 2-element array is UB; may print anything. No guaranteed adjacent object. |
| `18_span.md` §29 "Pointer iteration (1)" | yes | no: reads | pointer bounds (inclusive end) | n/a | — | Uses `[start, last]` inclusive; contrast with §30's past-the-end. |
| `18_span.md` §30 "Pointer iteration (2)" | yes | no: reads | pointer bounds (past-the-end) | n/a | — | `[start, pastEnd)`; `arr.end()` is one past the last element, not dereferenceable. |

## Missing category: stack frames

Lab 30 is the only place where function-call stack layout is the subject. Both analyses
are conceptual, not ordinary runnable examples.

| Example | Compiles | State changes | Phenomenon | int64_t | Diagram | Special care |
| --- | --- | --- | --- | --- | --- | --- |
| `30_function_execution.md` Analysis 1 | **no**: `sp` is not declared; pseudo-C | yes: `x` 1→0 conceptually | stack frame, return address, stack corruption | n/a | ASCII stack tables; keep | The exercise explicitly says it will not compile and assumes a 4-byte return address. A visual must be conceptual, not a GDB trace. Changing `sp - 8` to `sp - 4` overwrites the return address and crashes. |
| `30_function_execution.md` Analysis 2 | yes | no data state; stack grows until overflow | infinite recursion, stack overflow | n/a | — | Compiles but has UB when the stack is exhausted; the crash is not guaranteed at a specific depth. |

## Task-only labs (not taggable examples)

- `21_advanced_practice.md` (ru: `22_advanced_practice.md`) has 27 task bullets, not one
  canonical program with expected output. Pointer-relevant prompts are "Active buff"
  (pointer to optional buff), "Parking lot" (walk spots with pointer arithmetic),
  "Barbershop" (clients referenced from queue and workers), and the three "Family hugs"
  variants (pointers vs indices vs bitset). They are good future scenarios, but they
  cannot be tagged until a reference solution is chosen.
- `34_dynamic_array.md` has only a task specification and tests, no implementation to
  trace. It is also the only place where heap growth/capacity doubling would live; there
  is no heap/allocation visualization category in the current prototype list.
- `05_struct.md` ends with an assignment referring to
  `en/05_programming_fundamentals/memory_example_2`, which is outside `en/labs/cpp` and
  was not inventoried here.

## Screened out

These were read but are not candidates under the map's rule that a plain cell with no
state change gets no visualization, or because they duplicate a listed phenomenon:

- `02_variables.md` §1–3, §7–9: definition/redefinition/type errors; no useful timeline.
- `04_pointer.md` §2, §4, §6, §18: address of uninitialized variable, invalid numeric
  address, whitespace syntax, and pointer-size printing. §2 is only an address print;
  §4 is a compile error; §6 is syntax; §18 is `sizeof`.
- `04_pointer.md` §5, §15–17, §19: read-only or inference cases already covered by the
  expression-types table.
- `05_struct.md` §1, §3, §4, §6, §8–10: plain init/copy/field reads, or non-compiling
  type errors; §1/§6/§8–10 duplicate struct copy scenes, and §4 is a basic field-write
  timeline that the field-address scenes cover more strongly.
- `09_c_array.md` §1–6, §8, §15: initialization/indexing/printing without a pointer or
  state change. §15 is array decay to an address, but the visual would be a single
  pointer cell; low value.
- `11_pointer_arithmetic.md` §5, §6, §9: address subtraction, byte-pointer subtraction,
  and whole-array-vs-first-element. Useful static address math, but no cell state change;
  fold into a pointer-arithmetic variant if that pass happens.
- `14_reference.md` §1–4, §8–10: compile-error or additional reference-write variants;
  §8/§10 duplicate the write-through-reference scenes, and §9 is an invalid rvalue
  binding. §19 and §22–23 are retained in the expression-types table.
- `15_const.md` most examples: compile-error/read-only variants of the reference and
  pointer scenes; the ones with a visible state change are listed above. §15 (reassigning
  a pointer to const) is a pointer-target change, but it duplicates `04_pointer.md` §13
  with a const-access overlay.
- `18_span.md` repetitive read-only loops (§2–3, §5–9, §11–13, §15–16, §19–22, §24,
  §27): they demonstrate function signatures or bounds checking, not new memory layout.
  §19 uses `std::array::at`; the lab also notes that `std::span::at` is C++26.

## Special-care register

1. **Non-compiling source examples**: `04_pointer.md` §8–9 (the punning pair),
   `05_struct.md` §3/§13/§15/§16/§20, `05_struct.md` §24 (missing include),
   `02_variables.md` §3/§7/§8/§15, `09_c_array.md` §16/§18,
   `14_reference.md` §1–4/§9, many examples in `15_const.md`, and `30_function_execution.md`
   Analysis 1. Static type overlays are safe; timelines/traces are not, unless a
   compilable variant is authored.
2. **Padding and adjacent objects**: `05_struct.md` §24 (3 bytes after `f1` and after
   `f3`), `04_pointer.md` §8–9, `11_pointer_arithmetic.md` §11–12, `18_span.md` §4/§26.
   Never imply that a neighbor follows an array or a small object.
3. **Partial writes**: `04_pointer.md` §9 writes one byte of an `int`;
   `09_c_array.md` §17 writes only `arr1[0]`; `05_struct.md` §14 writes a whole struct.
   Keep the byte count explicit.
4. **UB / crashes**: `05_struct.md` §21 dereferences `nullptr` on the third print;
   `11_pointer_arithmetic.md` §11–12; `18_span.md` §4/§19/§26/§28;
   `30_function_execution.md` Analysis 2. A generated animation must either stop before
   the UB or label it as UB and not present the result as deterministic.
5. **Missing include**: `05_struct.md` §24 is the only listed example that fails to
   compile as printed because both en and ru omit `#include <cstdint>`. Fixing it is a
   content change; do it before tagging/tracing.
6. **Existing diagrams**: keep `05_struct.md` §2's PNG and §21's Mermaid. Replace
   `05_struct.md` §24's `05_struct_alignment.svg`, because prototype #62 explicitly
   targets it. Lab 30's ASCII tables are the only stack-frame diagram and should be kept
   as a fallback until a stack-frame prototype exists.
7. **`int64_t` choices**: use it only for `05_struct.md` §21 and §26 to remove unrelated
   padding. Keep `int` in §24 and keep `int`/`double` in `12_array_practice.md` §23,
   where size/alignment is the lesson. Everywhere else it is irrelevant or changes the
   displayed width without removing padding.
8. **References vs pointers**: references cannot rebind and cannot be null. Do not reuse
   the pointer reassignment animation for `14_reference.md` §11–12 or §14; the whole
   point is that `c = b` writes `a` and `r` stays attached to `a`.

## Tagging implications

- Each table row is a tag target. Rows that group several example numbers ("§14–17",
  "type-checking puzzles §1–10") need one tag per source fence, because the tag contract
  uses the nearest preceding fence.
- For non-compiling examples, only the static expression-types overlay applies; do not
  attach a base timeline or pointer animation.
- For the three diagram-bearing struct examples, tag only the one being replaced
  (`05_struct.md` §24). The PNG and Mermaid cases should remain diagram-only.
- The map's synthetic-address rule matters most in `04_pointer.md` §1/§10/§20,
  `05_struct.md` §21/§26, and `11_pointer_arithmetic.md` §10; never show real addresses.
- `05_struct.md` §24 needs the missing include fixed before the clang/GDB layout data
  matches the snippet.
