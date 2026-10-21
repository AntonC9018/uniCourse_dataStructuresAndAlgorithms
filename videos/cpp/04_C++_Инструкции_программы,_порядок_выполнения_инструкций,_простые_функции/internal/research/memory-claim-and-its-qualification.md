# The fixed-address claim, the ledger's copy of it, and the author's qualification

## The claim in the video

`00:00:58`–`00:01:15`, rolling caption:

> "…но вы и с памятью работаете не напрямую. Вы не можете вписать в регистр ноль процессор, например,
> что-то или не можете именно с какого-то фиксированного адреса считать какое-то значение. Вы работаете
> на уровне переменных."

Transcribed literally, the instructor asserts C++ *cannot* write to a processor register and *cannot* read
from a fixed address. As a statement about C++ this is false — pointers are exactly that, and the course's
own `09_Указатели` (`859Y0Q8pyLg`) teaches them eleven lessons later.

## The ledger recorded it at face value

The `ledger` work order `wo-0446f97cab1c1a19198b4806bf2638d7f647154628ccc33eddd9db8bc32b0072`
(runs 419 session `ses_ee32604fcffe6OgUUwtibO8cgR` for S-001…S-004, run 413 session
`ses_ee326b4bbffe80eNRA9i6xXI0d` for S-005…S-007) emitted it **twice**, as two separate `reason` points:

- `TP-006`, 54719–70360 ms — "Even memory is not touched directly in C++ because you cannot write into a
  processor register or read from a fixed address, so all access goes through an abstraction layer."
- `TP-007`, 63239–70360 ms — the same sentence, re-worded, overlapping TP-006 by seven seconds.

The duplication is a segment-boundary artifact: the S-001/S-002 cut at 63239 ms falls inside the claim.
Both anchor to `#from-machine-instructions-to-readable-actions`. Anyone rebuilding coverage from the ledger
alone will write the false sentence twice.

## What run 505 did about it

Run 505 (`english_authoring`, codex rollout `01a1266d-9ca4-7511-91c7-acd21c9024da`) stated its reasoning
in-session before publishing:

> "I'll keep the memory explanation scoped to these beginner examples; it shouldn't imply that C++ can never
> access memory through addresses."

It then read the committed pointer lesson at pinned commit `e6a198dd9d5f56bde01e2f74f0d71bf253316d82` and
used the section `### Writing to a memory address` (line 235 of that blob) as the counter-evidence. The note
carries it at line 38 with the pointer sample immediately below, and marks the sample as **"not an operation
taught in the video"**.

Independent check while recreating this file (2026-10-14, not a worker finding): the section exists at that
commit and supports the address-writing point, but its comments differ from the note. The pinned source uses
`// 'value' becomes equal to 10.` followed by a blank line; the note has `// Hold address of the value.` and
`// Write to valid location.` Do not describe the note sample as a verbatim reprint. The note’s code is:

```cpp
int value = 0;
// Hold address of the value.
int* pointerToValue = &value;

// Write to valid location.
*pointerToValue = 10;
```

`git cat-file -e e6a198dd…:en/05_programming_fundamentals/doc.md` succeeds; the blob is `beefe46f…`.
The commit is an ancestor of HEAD.

## Why this is the single most load-bearing correction in the folder

This is a consequential qualification for the note: it distinguishes the instructor's simplified explanation from the later pointer lesson, using an immutable source rather than an unsupported claim. It was never checked by a verifier —
run 506 died on timeout — so if the qualification is ever dropped, nothing in this record will catch it.
Keep it.
