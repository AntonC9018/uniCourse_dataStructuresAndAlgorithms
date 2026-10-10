# Toy ISA taught in this video: encodings, operands, exercises

Everything below is the video's own instruction set, reconstructed from the recorded
captions in `internal/transcript.md` and confirmed by the note (`notes.en.md`).
No C++ is compiled in the lesson; the encodings are invented for the demonstration.

## Instruction encodings

| Opcode | Operation | Operand order | Evidence |
| --- | --- | --- | --- |
| `64` | copy RAM → register | source RAM address, destination register index | captions 00:07:10, 00:07:57 ("в следующих двух позициях процессор поймёт как адрес памяти и номер регистра") |
| `72` | fixed add: R0 + R1 → R0 | none (hard-wired to registers 0 and 1) | captions 00:08:18 – 00:08:50 ("сложение то, что в регистре 0 и регистре один", "сложить нулевой с первым и вписать в нулевой") |
| `65` | copy register → RAM | source register index, destination RAM address | captions 00:09:34 – 00:10:09 ("65 - это идентификатор копирования из регистра … принимает два аргумента: откуда и куда") |

- The two loads share opcode `64` because the operation is unchanged; only the operands
  differ (captions 00:07:57 – 00:08:03: "Второй шаг, какой идентификатор будет у этого? тоже 64").
- The add is deliberately *not* given operands: it is defined as fixed on registers 0 and 1,
  so the number after `72` starts the next instruction (00:08:41 – 00:09:16). The video also
  sketches an alternative variant that would take the second register as a trailing argument
  (00:08:58) and rejects it for this program.
- Operand order is always source-then-destination, but the *kinds* of location differ per
  opcode: `64` is RAM-then-register, `65` is register-then-RAM. This is the note's central
  encoding rule and it is what makes `64 0 0` readable: the two zeros have different roles.

## The sum program

```text
64 0 0
64 1 1
72
65 0 3
```

Traced with RAM[0] = 5, RAM[1] = 6, code loaded at address 32, this reproduces the note's
tables exactly:

| Address | Instruction | Registers after | RAM[3] |
| --- | --- | --- | --- |
| 32 | `64 0 0` | R0 = 5 | unchanged |
| 35 | `64 1 1` | R0 = 5, R1 = 6 | unchanged |
| 38 | `72` | R0 = 11, R1 = 6 | unchanged |
| 39 | `65 0 3` | R0 = 11, R1 = 6 | 11 |

- Instruction starts are 32, 35, 38 and 39 — 32, 33, 34, 35 are byte addresses, not four
  instruction starts. Re-simulated 2026-10-10 by re-running the recorded stream
  `64 0 0 64 1 1 72 65 0 3` with opcodes 64/65/72 as defined above; result 11 at address 3.
- The authoring run (`english_authoring`, run 503, session `01a12666-96bb-7602-9e9b-776475c4c508`)
  ran the same stream as a scripted self-check over `ram = {0:5, 1:6, 2:10}` before publishing,
  recording the per-step register and RAM[3] state; the note's tables match that trace.

## The two separate exercises (00:09:47 – 00:10:17)

```text
64 2 1
65 1 4
```

- Load exercise: "put ten into register one" — the caption at 00:09:56 states the source and
  destination explicitly: "Считай из памяти в регистр, из памяти **два** в регистр **один**".
  The source operand is therefore 2 (the address holding the data value ten), and 10 is *not*
  embedded in the instruction. `64 2 1` is what the note teaches.
- Store exercise: 00:10:06 – 00:10:15 identifies `65` as "copy out of register" taking source
  then destination, "Откуда один, куда? Четыре" → `65 1 4`.
- The 00:10:17 sentence that "six lands here" describes register one still holding six from the
  earlier narration. This is a genuine ambiguity in the recording: the exercises are separate
  from the four-instruction sum, so whether ten or six appears at address 4 depends on what ran
  before. The note's wording ("the demonstration describes six appearing in the destination …
  If the load of ten immediately precedes the store, ten appears there instead") is the
  evidence-respecting form: the store copies current register contents and picks neither value
  itself. Re-simulated 2026-10-10: after `64 2 1; 65 1 4` the value at address 4 is 10.

## Scope boundary that shapes the whole note

- The opcodes are invented; the note labels them as such in the Scope paragraph rather than
  presenting them as a real ISA.
- The lesson's only RAM operations are read and write (00:02:21), and memory means RAM only —
  disk and CPU cache are excluded (00:00:33 – 00:00:45); registers are introduced only far
  enough to make execution explainable.
- Execution detail is deferred: the video points at the course's function-execution video for the
  full role of the instruction pointer, so the note's IP section stops at the
  fetch-decode-execute-advance loop.
