# Source links worth reusing

All links are to evidence that actually exists and was inspected; each line says what it proves.

## The video itself (upload `Bmae710korE`, "Память, процессор, машинный код, инструкции")

- `https://www.youtube.com/watch?v=Bmae710korE&t=0s` — framing: C++ is studied a level below C#.
- `...&t=33s` — scope: "memory" means RAM only; disk and CPU cache excluded.
- `...&t=45s` — registers deferred, taught only far enough to explain execution.
- `...&t=52s` — RAM as contiguous cells (tape, no holes).
- `...&t=77s` — positions numbered from zero; address = start of the cell.
- `...&t=120s` — a cell can hold the address of another cell; value vs address ambiguity.
- `...&t=141s` — the only two RAM operations: write and read.
- `...&t=176s` — the processor's job is executing instructions; the "divisible by one" example.
- `...&t=200s` — ISA = the instructions a processor understands.
- `...&t=245s` — RAM spans many addresses, "several gigabytes".
- `...&t=302s` — registers exist because they are much faster.
- `...&t=337s` — the action plan (trace of 5 + 6 → address 3).
- `...&t=430s` — opcode 64 = copy RAM into register; two operands, source then destination.
- `...&t=477s` — the second load keeps `64`, changes operands → `64 1 1`.
- `...&t=498s` — addition gets opcode `72`.
- `...&t=521s` — `72` fixed on registers 0 and 1, no explicit operands.
- `...&t=538s` — the alternative add variant that would take a trailing register argument.
- `...&t=574s` — opcode `65` = copy register into RAM, two operands.
- `...&t=587s` — "from memory two into register one" → `64 2 1` (the load exercise).
- `...&t=600s` — `65 1 4`, the store exercise.
- `...&t=625s` — the whole program as one numeric stream.
- `...&t=655s` — the apparent gaps between instructions are display-only.
- `...&t=669s` — the open question: how does the CPU find instruction boundaries.
- `...&t=703s` — decoding walkthrough of the same stream.
- `...&t=813s` — an executable file contains this machine code.
- `...&t=846s` — reserve RAM, load the code, execute.
- `...&t=866s` — one byte per cell, unsigned, in this model.
- `...&t=894s` — IP records the current code position; detailed role deferred.
- `...&t=918s` — address layout starting at 32 (addresses 32…41 = `64 0 0 64 1 1 72 65 0 3`).
- `...&t=945s` — the fetch/decode/execute/advance loop; starts 32, 35, 38, 39.
- `...&t=961s` — how can a cell hold a number or a character at all.
- `...&t=996s` — a bit is 0/1 (absence/presence of current as physical analogy).
- `...&t=1025s` — unsigned interpretation; maximum `11111111` = 255.
- `...&t=1053s` — encodings, ASCII as the simple popular example.
- `...&t=1087s` — adjacent cells give more digits; closes the lesson.

## Repository sources

- `videos/cpp/03_Память,_процессор,_машинный_код,_инструкции/internal/transcript.md` — the
  caption record every per-timestamp claim above rests on. ASR quality is uneven (misspellings,
  one truncated cue at 00:12:45); treat it as the authority for wording, not as prose.
- `videos/cpp/03_Память,_процессор,_машинный_код,_инструкции/internal/transcript.vtt` — the same
  captions in cue form; useful when a millisecond range rather than a timestamp is needed.
- `.../internal/teaching-points.json` — the audited ledger, transcript-range evidence per entry,
  and the English coverage anchors. Three entries conflict with the captions; see
  `ledger-conflicts-resolved-from-captions.md`.
- `.../internal/video.json` — upload id `Bmae710korE`, caption etag `tOohcy1L3BleZ43WR5TrUt0oFdg`;
  use it to confirm which caption revision was transcribed.
- `en/01_computer_architecture/doc.md` at commit `e6a198dd9d5f56bde01e2f74f0d71bf253316d82` — the
  related lesson with a different toy ISA (`15 102 0`), and the anchor
  `#instructions-and-a-computer-program-example`.
- `en/labs/cpp/01_instruction.md` — the C++ practice lab; deliberately cited only as "not taught
  in this video".
- Commit `79d34c41deb876e5924ea4131064af588116bf82` — the commit-bound state the note was
  verified against.
