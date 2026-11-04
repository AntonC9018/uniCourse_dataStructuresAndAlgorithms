# Open uncertainties and simplifications in this note

None of the items below blocks the note as written; each is a place where the record is
ambiguous or the lesson deliberately simplifies.

## Caption evidence is lossy at exactly one decision point

- The cue at 00:12:45 (765839 ms) is truncated mid-word ("…в регистр о"), so the destination
  register of the second load cannot be read off the captions directly. The note resolves it to
  register one from the instruction's own earlier encoding `64 1 1` and from the lesson's
  5 + 6 = 11 trace; the ledger's "register 0" wording is the only contrary text. A speaker
  listening to the audio is the only stronger evidence available, and it is not in the record.

## Overlapping exercise state

- 00:10:17 says six lands in the destination while the store exercise is `65 1 4`, but the load
  exercise immediately before it produces ten in that same register. The note keeps both
  readings and states that the store copies current register contents. Which value the video's
  drawing shows is not recoverable from captions alone.

## Numbers the note defines beyond the video

- "One gigabyte is one billion bytes" is the SI reading of GB. The video says only "несколько
  гигабайт" (00:04:05) without defining it. RAM capacity in practice is usually quoted in GiB,
  where 1 GiB = 2^30 = 1,073,741,824 bytes. Checked 2026-10-10,
  https://physics.nist.gov/cuu/Units/binary.html. The note's figure is defensible as SI but is
  not what a "several GB of RAM" statement normally counts.

## Deliberate simplifications kept in the note, flagged as such

- Registers are drawn as cells like RAM cells but far fewer; the note marks the likeness as a
  teaching simplification (00:04:11).
- Arithmetic operating on registers only, with values loaded from RAM first, is described as the
  toy design rather than a rule about real instructions (00:05:02).
- One byte per addressable cell, with an unsigned range ending at 255, is the toy model; the note
  states it is not a claim that real processors cannot read several bytes at once (00:14:47).
- Multi-byte values, negative numbers, strings and detailed register/IP behaviour are explicitly
  out of scope; the note closes on "adjacent cells can be used together" (00:18:07) and defers the
  rest.

## One example whose justification is weak in the recording

- 00:03:18 lists "check whether a number is divisible by one" among instruction examples. The
  note reproduces it and adds that for an integer this always succeeds, framing it as a
  demonstration of how small each action is. Worth keeping only for that framing; it is not a
  meaningful operation and no real ISA reference would list it.

## Unresolved record-level gap

- The three ledger contradictions in `internal/teaching-points.json` (TP-045, TP-057, TP-058)
  remain uncorrected in the committed file. Nothing in the record corrects them, and the
  verification findings for them named no affected paths. Any later pass that reconciles the
  ledger should take the captions above as the authority.
