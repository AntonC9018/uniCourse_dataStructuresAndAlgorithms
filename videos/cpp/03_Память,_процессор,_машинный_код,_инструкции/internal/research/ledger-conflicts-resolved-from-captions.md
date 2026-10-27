# Ledger conflicts: two captions settle the value; one register target remains inferential

The `english_authoring` note was written from the reconciled teaching-point ledger supplied to
the authoring run (`english_authoring`, run 503, session
`01a12666-96bb-7602-9e9b-776475c4c508`). Three ledger entries then contradicted the note, and
the `factual_verification` run (run 504, session `ses_ed9930e99ffeFqH04t4I7Xb5Hd`) raised one
`source_conflict` finding per entry. The committed ledger
(`internal/teaching-points.json`, TP-045, TP-057, TP-058) still carries the conflicting wording.

TP-045 and TP-058 are directly settled by their captions. For TP-057, the caption at 00:12:49 says only "сюда"; the register target is inferred from the earlier `64 1 1` construction and the arithmetic trace, not identified by that word alone.

## TP-045 (574560 – 596440 ms) — source address of "load ten into register one"

- Ledger wording: "loading ten into the first register uses opcode 64 with **memory address
  zero** as source and register one as destination."
- Caption at 00:09:56 (596440 ms): "Считай из памяти в регистр, из памяти **два** в регистр
  **один**" — from memory two into register one.
- Note: `64 2 1`. **Ledger is wrong; note is right.**

## TP-057 (761069 – 778150 ms) — destination register of the second load while decoding

- Ledger wording: "The next instruction is again 64, meaning a copy from RAM address 1 into
  **register 0**, so the second value is loaded the same way as the first."
- Caption at 00:12:45 (765839 ms) is truncated mid-word — "…из оперативной памяти один в регистр
  **о**" — so the destination is not legible from this cue alone.
- Register *one* is nevertheless established by three independent parts of the record:
  1. the same instruction was built earlier as `64 1 1` (00:07:57 – 00:08:03);
  2. the caption at 00:12:49 reads "берёт из оперативной памяти один и скидывает сюда". It names no register; identifying the destination as register one is an inference from the surrounding trace;
  3. logical consistency — with `72` defined as R0 + R1 → R0, loading address 1 into register 0
     would add 6 + 6 and yield 12, contradicting the lesson's own 5 + 6 = 11 trace.
- Note: register one, consistent with that inference. The cue itself does not settle the ledger conflict; the note’s value rests on the earlier construction and arithmetic consistency.

## TP-058 (778150 – 799710 ms) — register operands of opcode 72

- Ledger wording: "Opcode 72 is the addition of **register 1 and register 2** with the result
  written into register 0, and it takes no arguments at all."
- Captions at 00:13:00 – 00:13:04: "72 - это команда сложения … сложение регистраль с регистром
  **один** и записывание ответа в регистр **ноль**" — register 0 and register 1, result into
  register 0. The earlier 00:08:25 and 00:08:46 cues agree.
- Note: adds register zero and register one into register zero, no operands. **Ledger is wrong;
  note is right.**

## Net effect

- No factual error exists in `notes.en.md` at these three points; the defective text is in the
  audit ledger, whose entries were reconciled from the transcript before authoring and are
  internally inconsistent (TP-042/TP-044 vs TP-045/TP-058) as well as contradicting the captions.
- The verification findings carried `affectedPaths: []` because no safe correction to the *note*
  was established. The correction that is actually implied is to the ledger entry wording in
  `internal/teaching-points.json` (TP-045, TP-057, TP-058), i.e. the non-note half of the
  authoring work order's write assignment.
- The conflicting ledger wording is preserved verbatim above so a later pass can diff against it.
