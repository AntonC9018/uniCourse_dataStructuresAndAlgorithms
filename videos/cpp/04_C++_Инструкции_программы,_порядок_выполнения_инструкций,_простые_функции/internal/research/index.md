# Research record for `Z8AFpeE7hOo`

C++ lesson 4, "Инструкции программы, порядок выполнения инструкций, простые функции".
`internal/transcript.md`, 375 cues, `00:00:00.199`–`00:07:40.240`.

## What actually ran for this folder

Only two worker orders have runs in `worker_runs` for `course_video_id = Z8AFpeE7hOo`:

| order kind | run | engine | session | outcome |
| --- | --- | --- | --- | --- |
| `ledger` | 413, 419, 422 | opencode / space-bunny-free | `ses_ee326b4bbffe80eNRA9i6xXI0d`, `ses_ee32604fcffe6OgUUwtibO8cgR`, `ses_ee32596d5ffeWyPAYa2Voj6Vsr` | completed; produced the 40-entry teaching-point ledger |
| `english_authoring` | 505 | codex / gpt-6.1-sol, rollout `01a1266d-9ca4-7511-91c7-acd21c9024da` | wrote `notes.en.md` + coverage map, then the application merged the coverage into `internal/teaching-points.json` |
| `factual_verification` | 506 | opencode / space-bunny-free, `ses_ed98d41d2ffen8KPViviSeCXlC` | **interrupted**; `cause=engine_failure`, `error_class=timeout` after 20 min; no `structured_result`, zero `worker_tool_events` |

Consequences worth stating plainly:

- **`notes.en.md` has never been verified.** Run 506 produced no findings object of any kind; its session transcript contains the verifier prompt twice and no assistant turn. The `factual_verification` work order `wo-de8f3a2ae2be7157e39e65ca3e74415dbdaae74ba07c5cc8a36b1d987c978cab` is still `in_progress` with `result = null`.
- **No fixing pass ran.** `factual_fixing` `wo-8136fce260080c903117c2056dfefa316e0252fda27c4ea461c63e6f9596cab8` is `admitted` with no runs; the superseded `factual_fixing` orders likewise have none.
- Everything asserted about the note below therefore rests on **author run 505 alone**. No worker in this record ever challenged, confirmed, or corrected a single claim in it.

## Files here

- `transcript-only-evidence.md` — the transcript never names a single C++ token; what the note's code samples can and cannot be evidence for.
- `memory-claim-and-its-qualification.md` — the instructor's "you cannot read a fixed address" claim, the ledger recording it at face value, and the pointer qualification the author added.
- `related-committed-example.md` — why the only committed function example is cited as related-not-exact, and why the note's code-history trail is timestamps only.
- `open-items.md` — reconstructions presented as reconstructions, and everything still unchecked.

## Sources worth reusing

- Transcript, immutable: commit `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6` ("Acquire course transcripts"),
  `videos/cpp/04_C++_Инструкции_программы,_порядок_выполнения_инструкций,_простые_функции/internal/transcript.md`,
  blob `eec4320e7a33d2a37cb85ef4c295f12769c9ff3c`, sha256 `27ed98541903715374d9f791e015353dd15c561d421348b38331552d256dfe38`.
  `internal/transcript.vtt` at the same commit carries sha256 `8d3b4274…7bc4b0`, which is the `canonical` value the work orders record.
- The English note as committed: `b3bdd61e1b5f926d5e6dee36228b503cfd755a54` ("Update course video Z8AFpeE7hOo"),
  `notes.en.md` blob `fc9b0860e57abb01120729f4ecf59a175f7eecc1`, sha256 `4cc11ac02e12ade1f5216d19649ff52df54d4278b5605f241108cf85d8b753e1` —
  the same hash run 505 reported as its published output, so the committed note is exactly what run 505 wrote.
- Labs the note links relatively (both confirmed to resolve from this folder, checked 2026-10-10):
  `en/labs/cpp/01_instruction.md` and `en/labs/common/05_compiler_install.md`.
- Playlist `PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`, this video at 0-based position 4.
