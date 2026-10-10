# Open items

Everything here is unresolved in the record. Nothing in this file has been confirmed by a worker; the
verification pass for this folder produced no output at all (see `index.md`).

## Unverified because the verifier never finished

`factual_verification` run 506 (`ses_ed98d41d2ffen8KPViviSeCXlC`) was bound to commit
`b3bdd61e1b5f926d5e6dee36228b503cfd755a54` and
timed out after 20 minutes with `cause=engine_failure`, `error_class=timeout`. Zero tool events. Its
session holds the verifier prompt twice and no assistant turn. So the following were **never checked by
anyone**:

- the 41 timestamp links in `notes.en.md` against their cues;
- the two `github.com/.../blob/<commit>/…` citations against the blobs they pin;
- the two relative lab links;
- the 40-entry coverage mapping in `internal/teaching-points.json` against the note's 11 headings;
- every reconstructed output block.

## Reconstructions that are explicitly labelled as such in the note

These are the note's inferences, not the recording's observations. They are honest as written; keep the
labels if the note is revised.

- **Output after removing the *middle* newline.** The recording says only "он, видите, не вставил переход на
  новую строку" (`00:03:41`) — it never shows the resulting line. The note's claim that the output is
  `Hello WorldAnton` followed by a newline is derived from the reconstruction, and the note says "In this
  reconstruction the output is …".
- **The final trace of the nested example.** The recording narrates `main → B → f` and the return chain
  (`00:06:49`–`00:07:40`) but never displays the four-line output the note prints. The note labels it "The
  predicted output of the reconstruction".
- **All code samples.** See `transcript-only-evidence.md`.

## Interpretations added by run 505 that the recording does not state

Each is defensible and each is an addition, not a transcript claim:

- **The percent sign is a terminal marker, not program output.** The instructor says "у нас, видите, терминал
  записан как процент. Это значит, что не было перехода на новую строку" (`00:03:34`). The note goes
  further at line 125, attributing the `%` to the shell. That attribution is the author's, and it is
  correct for the zsh/bash prompt shown, but no evidence in this record establishes it.
- **`std::endl` flushes the stream.** Standard-library behaviour, true, and never said in the recording.
- **Functions must be defined before use.** The note asserts "The functions are defined before their uses in
  this sample" (line 283). True of C++; the recording never discusses declaration order. The companion lab
  `en/labs/cpp/01_instruction.md` question 15 does teach it explicitly, which is likely where this came
  from — the note does not cite that lab for it.
- **"last call site" means the call being completed** (line 242). The instructor's wording at `00:05:56` and
  `00:06:23` is "место, где эта функция была вызвана в последний раз", which is ambiguous. The note's
  disambiguation is an interpretation.

## Minor, checkable, not yet checked

- Two timestamp links, `t=199s` and `t=291s`, have no cue at that exact second. The nearest cues are 197/200
  and 289/292 respectively. Both sit inside the right passage, so this is cosmetic, not a wrong link.
- The lab `en/labs/cpp/01_instruction.md` links back to this video as `&index=5` in playlist
  `PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`, matching the maintenance record's 0-based membership position 4.
  Good corroboration for the folder's playlist placement.
