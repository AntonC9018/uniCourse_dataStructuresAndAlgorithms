# Code citations: what is pinnable for this lesson, and what is not

## No immutable source exists for the taught encodings

The lesson's program (`64 0 0 64 1 1 72 65 0 3`) has no exact committed source citation in the note. At authoring revision `79d34c4`, the available repository search found the literal encoding in the note; the former all-ref shell one-liner was not a valid exhaustive history scan and is removed. Do not infer that search as proof about every file in every ref.

- Consequence: the note's statement "No inspected repository commit contains the exact toy
  encoding used here" is correct, and citing any commit as the source of the taught code state
  would be a fabrication.
- What the note cites instead is the video moment (00:05:37, 00:07:38, 00:08:41, 00:09:16,
  00:10:25, 00:15:45) for each successive state of the program — see the "Code history through
  the video" trail at the end of the note.

## The one pinned repository citation that is needed

The note contrasts the video's toy ISA with the course's committed architecture lesson, whose
example program uses different invented opcodes:

```text
15 102 0
22 0 103
39 0 102
```

- Citation: `https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/e6a198dd9d5f56bde01e2f74f0d71bf253316d82/en/01_computer_architecture/doc.md#instructions-and-a-computer-program-example`
- Why pinned: the path is editable content, and the anchor `#instructions-and-a-computer-program-example`
  plus the exact numeric sample must both still resolve at that revision.
- Verified 2026-10-10 against the local checkout:
  - the commit exists and is the tip of the history of that file (`git log --oneline -5 -- en/01_computer_architecture/doc.md` → `e6a198d` first);
  - the heading exists at that revision (`## Instructions, and a computer program example`);
  - the sample `15 102 0` is present, with the surrounding text confirming the operand order
    (register = second argument after the memory address), matching the note's description.
- The note labels this as "a related conceptual source, not an exact repository copy of this
  video's program" — that distinction is the whole point of the comparison: the same numeric
  operand means different things in different ISAs.

## Deliberate omission

- The note links the related architecture lesson as a plain relative page link near the opening
  concept list *and* as the pinned blob next to its sample. It does not cite the commit that
  added the exercise (`en/labs/cpp/01_instruction.md`) as evidence for any installation or code
  state, because that commit only adds a lab and proves nothing about this lesson's states.
- `en/labs/cpp/01_instruction.md` is referenced once, in the "Optional later practice" section,
  explicitly marked as not taught in this video and as no evidence of an installation step.
