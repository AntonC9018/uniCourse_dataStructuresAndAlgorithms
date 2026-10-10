# Citation and ledger decisions

Traceability: `english_authoring` run 444 (session `01a11d52-a02d-7252-8ccf-440602130dc3`);
`factual_verification` run 447 (session `ses_ee2a43041ffe4mVQUUr5pAvWmv`).

- The lesson teaches no code state, so the only immutable evidence for its worked states is the
  transcript itself. The note pins it at commit
  `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6` (blob URL in the note) rather than a movable ref.
  Reason: a branch-named link would not prove the text the note's claims were checked against; the
  pin keeps the checkpoint stable.

- The application supplied a deterministic citation check before verification:
  `transcript.md` at `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`, `status: resolved`,
  `commitCharacterCount: 40`, `commitHasFullFormat: true`, `source: local_git`. The verifier's
  standing rule — a resolved full-format check is a valid pinned reference and no length defect may
  be invented for it — was followed; the commit was copied verbatim, not reconstructed.

- Authoring validation failure and its repair (the author run's single correction round): the
  application rejected the first note because the immutable transcript citation had "no simplified
  sample beside it in the same section". The repair inserted
  `01010100 = 64 + 16 + 4 = 84` (t=262) directly under the citation paragraph. Reusable lesson:
  every immutable citation needs a small worked sample in the same section, or validation fails.

- Lab link: the note points to `../../../en/labs/common/03_numbers.md` ("How Numbers Are Stored in
  Bytes lab"), an actual lab file in the owned repository, inspected to exist and listed as a
  `sourcePaths` entry. It is an exercise pointer, not evidence for the taught states; those stay on
  the pinned transcript. The lab adding commit is deliberately not cited.

- Ledger/note notation discrepancy: TP-016's ledger text writes the combined decimal groups as
  `999.999` (dot), while the note writes `999,999` (comma). The verifier accepted it as "covered
  with clarification". Unresolved house convention for the thousands separator inside
  teaching-point text; a future reconciliation pass should pick one.

- Ledger duplication: TP-038 and TP-039 overlap in time (558949–577640 ms vs 567600–577640 ms) and
  are near-identical restatements of the same `int`-size segment. Harmless for coverage, but it
  shows the extraction pass emitted near-duplicate points for one topic change.

- The note's decimal totals are labelled as arithmetic checks, not runs: "This decimal total is a
  check of the formula, not a reported program run." No execution evidence was fabricated for a
  lesson that built nothing.
