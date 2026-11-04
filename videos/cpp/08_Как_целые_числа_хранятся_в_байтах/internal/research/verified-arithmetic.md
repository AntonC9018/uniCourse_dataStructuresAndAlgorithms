# Verified arithmetic behind the note's worked examples

Each item was checked inside `english_authoring` run 444 (session
`01a11d52-a02d-7252-8ccf-440602130dc3`, e.g. the recorded evaluation
`135*(2**24+2**16+2**8+1)`), re-derived by `factual_verification` run 447 (session
`ses_ee2a43041ffe4mVQUUr5pAvWmv`, e.g. "The 0x87878787 expansion … Correct arithmetic"), and
independently reproduced during this capture on 2026-10-10 (Python). All agree.

- `0x87878787` expansion: `135 × 2^24 + 135 × 2^16 + 135 × 2^8 + 135 = 2264924160 + 8847360 +
  34560 + 135 = 2273806215`. Confirms the note's four-byte expansion at 00:10:23 and the last
  term being 135 because `2^0 = 1`.

- Two-byte combination: `84 × 256 + 85 = 21589` (`01010100` high, `01010101` low). Confirmed by
  the verifier verbatim.

- `0xE1` read as a signed byte: `−128 + 64 + 32 + 1 = −31` (TP-050). The note uses this to show a
  positive-looking pattern reading negative; −31, not the −27 the transcript's ASR garbles at
  t=764s ("-27 плюс 2/6" is the recognizer's error for the E1 decomposition).

- Two's complement of −18: `256 − 18 = 238 = 11101110`.

- Signed sum: `106 + 96 = 202 = 11001010`; signed reading `−128 + 64 + 8 + 2 = −54`. Confirms
  TP-077's correction.

- Signed-byte corner patterns: `11111111 → −1`, `01111111 → 127`, `10000000 → −128`. Confirms
  TP-054's correction table.

- Nibble values: `0xF5 = 245` (`1111 0101`) and `0x87 = 135`, the byte value reused by the
  four-byte expansion.

Caveat for future reuse: these are arithmetic identities, not runtime results. The note deliberately
labels them "a check of the formula, not a reported program run"; keep that framing if this file is
mined later.
