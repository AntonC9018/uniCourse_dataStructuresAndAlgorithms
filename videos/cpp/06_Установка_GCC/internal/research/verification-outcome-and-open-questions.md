# Verification outcome and the one claim that was waved through

## Outcome

- `factual_verification`, run 445 (opencode `space-bunny-free`, session
  `ses_ee2a43085ffeU8DO4SYUVlfqmC`, 2026-10-08T21:11:58Z → 21:12:49Z): verdict `approved`,
  `findings: []`, coverage `TP-001`…`TP-079` complete against commit
  `9524e929bc1df59b55902f900a34d87f1d4c94f7`. Method: `git rev-parse` on the commit,
  `git ls-tree`/`git show` to read the note, `grep '^#'` to confirm all 12 coverage anchors resolve
  (the note has 14 headings; the extra two are the H1 opening and the trailing "Code history trail"),
  then spot-checks of the transcript at 00:00:20, 00:00:37, 00:01:22, 00:05:07, 00:09:03, 00:14:14,
  00:16:23 against note claims.
- `factual_fixing` therefore had nothing to do: its recorded evidence is "clean factual verdict
  needs no fixing", `verificationReport.verdict = approved`, `fixingRecords: []`, and the output
  hashes it wrote back are byte-identical to the author's. **No factual error was ever found and
  fixed for this video** — the only corrections that exist are the author's own proactive ones in
  run 443 (see `gcc-predates-linux-correction.md`, `toolchain-naming-msys2-vs-mingw.md`).
- `english_authoring`, run 443, wrote both `internal/teaching-points.json` (79 coverage entries,
  12 distinct anchors) and `notes.en.md`, and self-validated before reporting: all 79 anchors
  resolved, 86 timestamp links with label/seconds agreement, balanced fences and `<details>`,
  note starts at the first content heading.

## Unresolved / not verified

- **The no-administrator-password claim is asserted, not evidenced.** The note opens with "The
  demonstrated installation can be done without an administrator password when the chosen
  installation location and account permissions allow it." Run 445 flagged this internally
  ("hmm, that's an unverified claim, but hedged … Acceptable-ish") and approved anyway. Nothing in
  the transcript or the cited sources establishes the non-admin path for the MSYS2 installer.
  Treat as unresolved.
- **Which MSYS2 shortcut was used is not pinned.** Transcript 00:01:56–00:02:17 compares two
  shortcuts and concludes they are equivalent, but the specific environment name is only audible
  as ASR fragments ("CRT. Вот этот он сам запускает"). The note names UCRT64 only as an *example*
  of a different environment, never as the one used.
- **The exact compiler directory for a given installer remains variant-dependent.** The instructor
  says so himself at 00:14:20–00:14:26 ("в зависимости от этого оно попадёт в разные папки") and
  the note repeats it; the note's `C:\msys64\usr\bin` is the recorded machine's value, not a rule.
- **The 2021 download page itself was never identified.** Only its date and its C++17-only claim
  are on record; the note names neither the product nor the URL.