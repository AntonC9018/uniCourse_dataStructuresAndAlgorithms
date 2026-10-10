# Arithmetic established for this lesson

Video `cPKhqBM0gIc`, base-arithmetic lesson. Sources: author run 500
(`english_authoring`, codex rollout `01a12659-e944-70c3-97b8-d571940b863e`) and
verifier run 501 (`factual_verification`, session `ses_ed99ef826ffeXc23VsmIecxvex`).

## Machine-checked identities (run 500, executed before publishing)

Run 500 evaluated every identity in one script and refused to publish if any failed.
All ten held:

- `123₄ + 333₄ = 1122₄`
- `123₆ × 345₆ = 52203₆`
- `2 × 345₆ = 1134₆`
- `3 × 345₆ = 1523₆`
- `D₁₆ × E₁₆ = B6₁₆`
- `FD₁₆ × B5₁₆ = B2E1₁₆`
- `24₆² = 1104₆`
- `5 × 1104₆ = 5532₆`
- `23₆ × 24₆ + 22₆ = 1102₆`
- `5FE₁₆ = 11034₆`

## The verifier re-derived the same set by hand (run 501)

Run 501 recomputed the products and sums in decimal from the base digits and found no
false claim; the note's arithmetic stood. Its only finding was the citation defect
recorded in `citation-parenthesis-truncation.md`.

## Re-checked while recreating this file (fresh, 2026-10-10, not a worker finding)

All ten identities above, plus the two slip discriminators below, evaluated from
positional value:

- `104₆ = 40`, while `1104₆ = 256 = 24₆²`
- `5FE₁₆ = 1534₁₀ = 11034₆`

## Transcript slips the note corrects, with transcript moments

Evidence is `internal/transcript.md` (immutable at
`d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`), cited by its own YouTube timestamp links.

- **Hexadecimal letter values, ~00:20:51–00:21:04 (1251s → 1264s).** The instructor
  first says A = 11, B = 12, C = 13, D = 14, then retracts it in the same breath and
  settles on A = 10, B = 11, C = 12, D = 13. The note uses the corrected values, and
  the correction is what makes `D = 10₁₆ − 3` the useful complement.
- **Wrong written digit in a partial row, 00:40:57 (2457s).** The instructor says
  "Ой, блин" and replaces the digit; the completed first row is `144₆`, not `444₆`.
- **The square is spoken as "1 0 4", 00:42:14 (2534s).** The correct result is
  `1104₆`; `104₆` is only forty. `24₆ = 16₁₀`, so the square is `256₁₀ = 1104₆`. The
  note keeps the repeated leading ones.
- **The final conversion is spoken as "1 034", 00:45:13 (2713s).** The complete result
  is `11034₆`; the transcript drops a leading repeated 1.
- **A shortcut that belongs to another term, 00:42:37 (2557s).** The instructor offers
  `1 104 − 24`, which is `23₆ × 24₆` with `24 − 1 = 23`; it is the second conversion
  contribution, not the multiplication of the squared weight by five.

## Framing rule the note follows

Every one of these corrections is presented as a value check against the positional
contributions, never as a software test. The recording contains no program
implementation, so there is nothing in it that could be executed as a test.