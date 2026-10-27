# In-video corrections (the recording corrects itself three times)

All three were extracted as ledger points of kind `correction`, written into the note by
`english_authoring` run 444 (session `01a11d52-a02d-7252-8ccf-440602130dc3`, work order
`wo-05d7e8a567d8a587d1a6384ec6f2d7401ca8b3c129a29c3e0f92173526d418c3`), and confirmed as
covered by `factual_verification` run 447 (session `ses_ee2a43041ffe4mVQUUr5pAvWmv`), verdict
`approved`, zero findings. `factual_fixing` (`wo-a1f010affbac970f35c02384b681fdb15ca36374f3b2ecb7bc90142dae82a3dd`)
recorded "clean factual verdict needs no fixing", so no post-verification rewrite happened.

## TP-054 — all-ones byte is neither most negative nor most positive (t=817–840, 13:37–14:00)

The instructor first calls the all-ones byte "the smallest negative number" ("чтобы компенсировать
значение -18"), then sums the weights, gets 127, and concludes the all-ones byte is "the largest
positive number" (transcript `internal/transcript.md` at `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`,
t=817s and t=839s). Both statements are wrong for two's complement:

- `11111111 = −128 + 127 = −1`
- `01111111 = 127` (largest positive)
- `10000000 = −128` (most negative)

The note's section "Correcting the signed byte limits" carries the three-pattern table and states
the signed range is −128 through 127. The instructor's 127 comes from the same borrow construction
that later yields −1 (all zero minus one), which is exactly the confusion the section names.

## TP-077 — signed sum 106 + 96 is −54, not −18 (t=1169–1177, 19:29–19:37)

At t=1169s the instructor names −18 ("будет равно -18 потому что самый верхний бит выставлен плю
64 + 8 + 2"); at t=1177s the same paragraph continues with −54 ("-54 в случае когда два
положительных числа при сумме выдают отрицательное"). The arithmetic settles it: `11001010 =
−128 + 64 + 8 + 2 = −54`. The note preserves the correction narratively ("The narration initially
names −18, then corrects the result") instead of silently using −54.

## TP-085 — two-byte signed top weight is −2^15, not −2^7 (t=1250, 20:50)

The instructor states the correction explicitly: "он будет равен не 2 в седьмой степени А 2 в 15
точнее -2 в 15 остальные позиции остаются такие же". The note ends with the weight table
(eight-bit signed: −2^7 = −128; sixteen-bit signed: −2^15 = −32768) and the general form
`−b15 × 32768 + b14 × 16384 + … + b0 × 1`.

Evidence type for each: transcript moment inside the ledger's transcript_range plus reproducible
arithmetic (see `verified-arithmetic.md`). No external source was needed to establish any of the
three corrections.
