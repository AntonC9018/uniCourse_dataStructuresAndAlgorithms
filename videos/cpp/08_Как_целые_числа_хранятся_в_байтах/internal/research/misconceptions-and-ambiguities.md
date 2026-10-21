# Misconceptions and ambiguities that shaped the note's wording

Traceability: `english_authoring` run 444 (session `01a11d52-a02d-7252-8ccf-440602130dc3`);
confirmed covered by `factual_verification` run 447 (session `ses_ee2a43041ffe4mVQUUr5pAvWmv`).

- The worked `1 + 1` carry-chain demo (TP-065) is per-bit positional addition, not whole-integer
  addition. Without a guardrail a reader concludes `1 + 1` overflows a byte. The note says it
  directly: "Ordinary whole-byte `1 + 1` is 2 and does not overflow; the repeated `1 + 1` steps
  here concern individual bit positions in a carry chain."

- Signed overflow does not require a ninth-bit carry (TP-073–TP-077). In `106 + 96` all eight
  unsigned result bits fit (`11001010`, unsigned 202). The failure comes purely from the sign
  interpretation. The note states the distinction explicitly at 00:20:09: "unsigned overflow can
  lose a carry beyond bit 7, but signed overflow does not require a ninth-bit carry." The recording
  itself blurs carry-out and range failure.

- Overflow vs underflow naming for signed cases is inconsistent in the recording (TP-080, TP-082,
  TP-083): the instructor names the same event both overflow and underflow. The recording also calls
  the unsigned `0 − 1 = 255` case "underflow" (TP-071, t=1073s). The note's decision: use
  "unsigned wraparound below zero" for the unsigned case and advise describing the mathematical sum
  and the permitted range rather than relying on either name.

- `135` in the four-byte expansion is a whole byte value (`0x87`), not one hexadecimal digit
  (TP-042–TP-043). The recording's line `135 × 2^24 + 135 × 2^16 + …` invites reading it as hex
  place values. The note clarifies before the expansion: "135 is a whole byte value, not one
  hexadecimal digit: it is `0x87`."

- Byte-group order in a written number is a positional interpretation only (TP-021). The note adds
  the boundary: combining `84 × 256 + 85` "does not specify which group a computer stores at the
  lower memory address" — endianness is out of the lesson's scope, so no memory-order claim is made.

- The recording's magnitude example for −18 compresses the two-step construction (invert all bits
  of the magnitude, add one) into one sentence; the ledger text for TP-052 records garbled
  contributions ("-64, -32 and -32") that do not match the actual weights. The note re-derives the
  pattern (`256 − 18 = 238 = 11101110`) instead of repeating the garbled intermediate values.
