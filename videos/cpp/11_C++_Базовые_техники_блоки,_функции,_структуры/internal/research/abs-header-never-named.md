# `abs` is asserted to need an import, but the header is never named

## What the video says

`00:04:23`–`00:04:29`: "абсолютное значение — это стандартная функция, которую нужно
импортировать. А импортируется она из ма, наверное, есть такой CL. И сюда мы передаём
разность." The instructor states the import requirement, then names the header only as an
uncertain filler ("мма… наверное").

The extraction ledger (run 477, session `ses_edd95c4e1ffelKnBxfFrxxdySf`, S-004) reduced
this to "Absolute value is a standard library function that must be imported" — correct
as far as it goes, but the uncertainty was dropped, so the ledger now reads as if the
video settled the header.

## The missing fact, and where it comes from

Not in the record — checked 2026-10-10 against
<https://en.cppreference.com/w/cpp/numeric/math/abs.html>:

- `std::abs(int)`, `std::abs(long)`, `std::abs(long long)` are declared in `<cstdlib>`.
- The floating-point `std::abs(float)`/`std::abs(double)` overloads are declared in
  `<cmath>`.
- LWG 2192 left the integer overloads declared in *both* headers, so either include
  compiles for the integer call this lesson makes.

The lesson's `distance` returns `int`, so `<cstdlib>` is the header a note should name —
which is, in effect, what the instructor guessed at out loud.

## Consequence for a note

- Name `<cstdlib>` explicitly and say the return type is `int`; the video's own hint is
  not enough for a reader to get the include right.
- Do not claim the video names the header — it does not.
- Mark this as a checked external fact, not a worker finding.
