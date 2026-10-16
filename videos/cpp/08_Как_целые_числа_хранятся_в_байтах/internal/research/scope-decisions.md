# Scope decisions and their reasons

Traceability: `english_authoring` run 444 (session `01a11d52-a02d-7252-8ccf-440602130dc3`);
`factual_verification` run 447 (session `ses_ee2a43041ffe4mVQUUr5pAvWmv`) approved the resulting note.

- `int` size: the recording says integers of type `int` are "обычно в четырёх байтах иногда в
  восьми" (usually four bytes, sometimes eight; t=560–570; ledger TP-038/TP-039). The note uses four
  bytes for the worked example but refuses to promote it to a guarantee: "do not turn that common
  size into a universal size guarantee", and the vocabulary entry says "its size is not fixed by
  this diagram". Reason: the eight-hex-digits claim follows from the chosen width, not from a
  portable fact about `int`.

- Fresh research supplement (not a worker finding; checked 2026-10-10, source
  https://en.cppreference.com/w/cpp/language/types.html): the C++ standard guarantees `int` a width
  of at least 16 bits, and `int` is 32 bits in every common data model (ILP32, LLP64, LP64). An
  eight-byte integer would be `long` (LP64) or `long long`, so the recording's "sometimes eight
  bytes" for `int` is loose speech, not a portable claim. The same page records that two's
  complement became the only allowed signed representation in C++20, and that the `−2^(N−1)` signed
  range guarantee (e.g. −128..127 for eight bits) is a C++20 guarantee — relevant if the lesson's
  range claims are ever tightened to standard guarantees instead of fixed-width modelling.

- No executable code exists in the recording: the lesson is diagram-and-arithmetic. The note's
  closing "Code and worked-state trail" therefore lists video states (with timestamps), not Git
  commits, and does not pad the trail with repository commits unrelated to the taught state.

- The lesson deliberately excludes C++ expression evaluation, automatic type conversions, and any
  guarantee that overflowing C++ expressions wrap; the note states this in its scope paragraph.

- Prediction/self-explanation questions with `<details>` answers were used to carry the "why"
  checks (why the maximum is one less than the number of patterns; why there is one more negative
  than positive signed value; would sixteen signed bits hold 202) without adding claims beyond the
  lesson.
