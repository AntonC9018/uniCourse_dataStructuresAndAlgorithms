# Sources worth reusing, and what is still open

## Immutable sources used by this video

- Transcript, the note's only factual citation for spoken content:
  `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6` ("Acquire course transcripts", 2026-10-09),
  path `videos/cpp/02_Сложение,_умножение_в_других_системах_счисления_Перевод_из_одной_системы_в_другую_(сырой)/internal/transcript.md`.
  The blob URL must carry percent-encoded parentheses; see
  `citation-parenthesis-truncation.md`.
- Companion exercise: `en/labs/common/02_number_systems.md`, read at
  `037bd3c547a7f30f960d496acbac10ed6af38f5c` ("Update course index and references").
  The note links it relatively as `../../../en/labs/common/02_number_systems.md`
  and lists it in `sourcePaths`, per the authoring contract that a lab link must
  target the lab Markdown file in the owned repository, never a published site URL.
- English commit verified in this cycle: `bf28c48179d2f00d29633d4d737b8ca46c1fe902`
  ("Update course video cPKhqBM0gIc").
- Video: `cPKhqBM0gIc`; the note's timestamp links are `…&t=<seconds>s` and were
  checked against the transcript's own seconds by run 500 before publishing.

## Open items

- **The citation fix is not committed.** Checked 2026-10-10: HEAD
  `bf28c48179d2f00d29633d4d737b8ca46c1fe902` still carries the raw-parenthesis URL,
  while the working tree of `notes.en.md` carries the `%28сырой%29` repair from
  run 502. The cycle's `git_publication` work order had not completed. Anyone
  re-deriving this folder's state from the commit alone will not see the fix.
- **A second repair from run 487 was never published and its need was never
  re-established.** Run 487 also inserted a simplified calculation beside the
  immutable citation, because a validator reported the reference had "no simplified
  sample beside it in the same section". Run 502 changed only the URL. Whether the
  current note satisfies that validator is not established by the record.
- **Coverage was asserted, not deeply checked.** Run 501 reported all 186 ledger
  entries as covered while stating it could not deeply verify every one of them. Treat
  full coverage as a claim, not as established evidence.
- **The rendered GitHub blob page was never confirmed.** Only the raw endpoint was
  reachable from this environment; see `citation-parenthesis-truncation.md`.