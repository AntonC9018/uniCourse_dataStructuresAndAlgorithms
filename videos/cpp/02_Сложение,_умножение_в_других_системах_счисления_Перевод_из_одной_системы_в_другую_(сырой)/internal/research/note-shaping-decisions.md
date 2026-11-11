# Misconceptions and decisions that shaped the note

All items below were established by author run 500 (`english_authoring`, codex rollout
`01a12659-e944-70c3-97b8-d571940b863e`) while rewriting the lesson in transcript
order, and none of them was rejected by verifier run 501
(`factual_verification`, session `ses_ed99ef826ffeXc23VsmIecxvex`).

## Guard clauses the note had to state

- A position at its maximum digit does not gain a new digit; adding one rolls it over
  and carries. In ternary, after `2₃` the next numeral is `10₃`, not `3₃`.
- Multiplying by `1` leaves the numeral's digits untouched: `1₆ × 345₆ = 345₆`. The
  `100₆` factor of `123₆` still applies its own two-place shift to the whole row.
- A three-digit positional factor ending in two zeros (`100₆`) specifies **two**
  shifts, not three.
- `2 × D` is a product; `2D₁₆` is a two-digit numeral. The note marks the distinction
  wherever both forms appear.
- The remainder of `2 × 3` in base six is zero; the written digit becomes 1 only after
  the incoming carry is added.
- A positional expansion converts the **original base value** as well as the digit
  coefficients: `10₁₆ = 24₆`, `F₁₆ = 23₆`, `E₁₆ = 22₆`. Converting only the
  coefficients and concatenating them gives a different number, because the weights
  are powers of sixteen, not of six.
- The squared weight is `24₆ × 24₆`, not `10₆ × 10₆`; squaring `10₆` squares six and
  supplies the wrong weight, even though `100_b = (10_b)²` holds in every base.
- The "six + six + two" reading of `E = 14` describes E's value; it is not a carry
  entering E's term.
- The factoring shortcut `24 − 1` represents `23`, so it belongs to `23 × 24`; it must
  be kept apart from the `5 × 1104` multiplication.
- The spoken "1.0" for `10₃` means two whole-number digits, not a fractional numeral.
- The "14" recalled when the base-six multiplication resumes belongs to `2 × 5` in base
  six; it is not a value assigned to hexadecimal `D`.

## Coverage and scope decisions

- The lesson constructs calculations by hand; it contains no program implementation,
  language-syntax change, installation step or software test. The note therefore says
  so explicitly, and the closing code-history trail follows the video's calculation
  states rather than repository code commits.
- Addition concludes at ~00:11:22 (682s), multiplication follows, and conversion starts
  at ~00:35:39 (2139s). Section boundaries were taken from these transitions.
- The teaching-point ledger written in run 500 is mechanical: `TP-001`…`TP-186`, one
  entry per lesson second, each anchored to the slug of one of 22 section headings.
  Its value is coverage completeness, not a ranking of importance.

## Why the number-shifts were kept separate from carries

- Run 500 states the distinction twice and both times because the recording mixes
  them: a whole-row shift such as `1134₆ × 10₆ = 11340₆` is a positional factor,
  while the carries inside that row come from the digit products. Collapsing them is
  the most likely misreading of the multiplication segment.