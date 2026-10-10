# Coordinates spoken as bare digit pairs

## The hazard

The instructor says coordinate pairs as bare digit sequences, and the caption renders
them as two-digit numbers:

- `00:02:02` enemy "в позиции 32" — means (3, 2), not thirty-two.
- `00:02:06` player "в позиции, где каждая координата меньше, 1" — means (1, 1).
- `00:30:32` "То есть 13 встаёт как бы в ячейку первой позиции и 32 встаёт в ячейку
  второй позиции" — means 1,3 and 3,2 i.e. player (1, 3) and enemy (3, 2). The same
  moment disambiguates itself seventeen seconds later: "Вот он был 1 3 … X будет 1, Y
  будет 3" (`00:30:49`–`00:30:52`).
- `00:00:26` "эта клетка будет иметь координату 5 0" — x = 5, y = 0.

The extraction ledger inherited the hazard verbatim: run 484
(`ses_edd94d338ffek3VwIBe23VM6wJ`) S-025 records "the value of 13 lands in the cell of
the first position and 32 in the cell of the second", with no indication that these are
coordinate pairs. A note that copies that sentence is wrong, and a reader who takes
"13" as a number cannot follow the memory-layout explanation at all.

## Consequence for a note

- Write coordinate pairs in the transcript's own arithmetic form (`1, 3` / `3, 2`), never
  as the caption's run-together digits.
- Where the caption's digit pair is the only available phrasing, carry the disambiguating
  cue that follows it.
- The same pattern appears in the very first grid discussion, so it recurs throughout the
  lesson rather than being a one-off.

## Related caption shape

The caption stream is a rolling duplicate: each sentence appears as the tail of one cue
and the head of the next, and gaps of 2–4 seconds with no cue at all appear between
sentences. Five of the extraction worker's non-teaching markers land in those gaps or on
empty intervals and therefore map to no cue — see `ledger-nonteaching-disagreement.md`.
