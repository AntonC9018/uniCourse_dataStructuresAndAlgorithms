# Statements in this video that the ledger recorded at face value and nobody checked

Because no `factual_verification` or `factual_fixing` run exists for `6ML34OuwZrc`
(see `index.md`), every claim below stands exactly as the speaker framed it, plus one
`ledger` transcription, plus nothing else. Each item names the moment, what the ledger
recorded, and what is actually true.

## 1. `int` is not ±4 billion — the speaker is off by a factor of two

- Video, `00:05:24.520`–`00:05:36.189`: *"Сейчас оно идёт от ми4 млрд до +4 млрд,
  потому что это 4 млрд влезает в 4 байта. И плюс и минус."*
- Ledger: run 426 (session `ses_ee3239f33ffeV8qJZ9dsmR3wVN`), S-005,
  `00:05:24.520`–`00:05:34.430`, kind `fact`: "As an int, i currently holds values from
  about minus 4 billion to plus 4 billion because that signed range fits in four bytes."
- Actual: a 32-bit two's-complement `int` spans −2 147 483 648 … 2 147 483 647, about
  ±2.15 × 10⁹. 4 294 967 295 is the range of the *unsigned* 32-bit type; the sign bit is
  what the speaker's trailing "и плюс и минус" gestures at.
- The note must give −2 147 483 648 … 2 147 483 647, or avoid the numbers. Do not
  reproduce "±4 billion".

## 2. `int` is 4 bytes — true on every machine this course uses, not guaranteed by the language

- Video: `00:04:27.800`–`00:04:29.190` ("целое число на 4 байта"), restated
  `00:05:05.560`–`00:05:09.190` and `00:09:18.920`–`00:09:20.230`.
- Ledger: run 427 (session `ses_ee3239f09ffeHnxyNZpHg7at8F`), S-004,
  `00:04:09.890`–`00:04:33.560`, kind `fact`: "The int type declares that the cell holds
  a whole number occupying four bytes of memory."
- Actual: the standard guarantees only a width of at least 16 bits; 32 bits holds for
  every common data model (LP32, ILP32, LLP64, LP64), which is why the course can say
  it plainly. Fresh check, 2026-10-10:
  <https://en.cppreference.com/w/cpp/language/types> ("If no length modifiers are
  present, it's guaranteed to have a width of at least 16 bits") and
  <https://learn.microsoft.com/en-us/cpp/cpp/data-type-ranges> ("portable code shouldn't
  depend on the size of `int` because the language standard allows this to be
  implementation-specific").
- Note wording: "4 bytes on the platforms used here", not "`int` is 4 bytes".

## 3. A byte is 8 bits and a cell is a byte — a textbook simplification, fine to keep, wrong to assert

- Video: `00:04:43.560`–`00:04:49.190` ("одна ячейка памяти — это 1 байт") and
  `00:06:27.110`–`00:06:30.270` ("8 бит — это 1 байт").
- Ledger: run 427, S-004, `00:04:38.350`–`00:04:51.960`, kind `explanation`: "Since one
  memory cell is one byte, an int variable occupies four consecutive cells rather than a
  single cell."
- Actual: in C++ a byte is `CHAR_BIT` bits and the standard only requires
  `CHAR_BIT >= 8`; cppreference notes the standard "allows the extreme case in which
  bytes are sized 64 bits, all types (including `char`) are 64 bits wide, and `sizeof`
  returns `1` for every type". Fresh check, 2026-10-10:
  <https://en.cppreference.com/w/cpp/language/types>.
- This is the load-bearing simplification of the whole lesson. Keep it, but the note
  should not present it as a guarantee.

## 4. `uint8_t x = 256;` is a **warning**, not a compile error — the ledger recorded it as a `test_result`

This is the most dangerous item in the folder: a `kind: test_result` label implies
observed execution, and no compilation appears anywhere in this video's record
(`worker_tool_events` has a single `bash` row for run 426, with no recorded output).

- Video, `00:06:49.919`–`00:06:57.670`: *"попытаться скомпилировать. Например, он даже
  даёт ошибку, что типа он не 256 сохранит, а ноль."*
- Ledger: run 426, S-006, `00:06:47.830`–`00:06:57.670`, kind **`test_result`**: "Compiling
  code that assigns 256 to a uint8_t variable is reported as an error because the value
  does not fit in the single byte."
- Actual, executed on 2026-10-10 with `g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`,
  `-std=c++17`:

  ```
  uint8_t a = 256;    // warning: unsigned conversion from 'int' to 'uint8_t'
                       //   {aka 'unsigned char'} changes value from '256' to '0' [-Woverflow]
  uint8_t b{256};     // error:   narrowing conversion of '256' from 'int' to
                       //   'uint8_t' {aka 'unsigned char'} [-Wnarrowing]
  ```

  Copy-initialisation warns and silently stores 0; brace initialisation is ill-formed
  and is a hard error. Warnings become errors under `-Werror`
  (<https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html>, `-Werror` section, checked
  2026-10-10).
- Same run, S-007, `00:07:21.759`–`00:07:34.220`, kind `correction`: "Printing yields zero
  even though 256 was stored, and the cause is the one-byte overflow rather than the
  value chosen." That half is confirmed: after `uint8_t a = 256;` the program printed
  character code 0.
- Note wording: "the compiler warns (and rejects the brace form outright); the value that
  actually gets stored is 0." Never "the compiler refuses to compile it".

## 5. "A variable is in fact on the stack" — true only for automatic storage

- Video, `00:00:14.550`–`00:00:16.910`: *"Она на самом деле на стеке, но мы до этого
  дойдём позже."*
- Ledger: run 427, S-001, same range, classified **`scope_boundary`** rather than `fact`
  — one of only seven such classifications in the whole ledger, all listed in
  `deferred-topics-and-cross-references.md`.
- Actual: only objects with automatic storage duration. Globals, `static` locals and
  `new`-allocated objects are not on the stack. Fresh check, 2026-10-10:
  <https://en.cppreference.com/w/cpp/language/storage_duration>.
- The video says it about the local `int i;` it has just declared, so it is fine in
  context. A note must not generalise it to "variables live on the stack".

## 6. Addresses 32 / 36 / 40 are a drawing, and the video knows it

- Video, `00:04:54.880`–`00:05:15.000`: `i` runs 32→36 exclusive, `a` runs 36→40.
- Ledger: run 426, S-005, `00:04:54.880`–`00:05:01.390` kind `explanation` and
  `00:05:06.320`–`00:05:15.000` kind `fact`, restating the layout as a consequence of the
  types.
- Nothing guarantees adjacent same-type variables occupy adjacent addresses, and nothing
  guarantees those numbers. The speaker hedges at `00:00:55.520`–`00:01:00.000`
  ("по факту чуть по-другому") before naming any address, so the record supports
  presenting the figure as illustrative. No external source needed; this one is settled
  by the transcript itself.

## Supporting execution, 2026-10-10 (fresh, not a worker finding)

`g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`, `-std=c++17`:

```
CHAR_BIT=8 sizeof(int)=4 INT_MIN=-2147483648 INT_MAX=2147483647 UINT_MAX=4294967295
sizeof(uint8_t)=1 sizeof(unsigned char)=1 std::is_same_v<std::uint8_t, unsigned char>=1
uint8_t a = 256;  ->  value is 0; printing yields character code 0
```

`std::uint8_t` is the same type as `unsigned char`, which is why the video's
number-vs-character printing difference at `00:07:53.280`–`00:08:14.620` happens at all
and why the video's own advice at `00:07:21.759`–`00:07:26.400` — convert to `int` before
printing — is the right fix. `uint8_t` is the one type in this lesson whose width *is*
guaranteed (<https://en.cppreference.com/w/cpp/types/integer>, "width of exactly N bits",
checked 2026-10-10).