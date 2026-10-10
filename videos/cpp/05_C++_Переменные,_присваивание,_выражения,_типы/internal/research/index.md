# What the maintenance record actually contains for `6ML34OuwZrc`

Course video `6ML34OuwZrc`, "C++ Переменные, присваивание, выражения, типы", folder
position 5 of `videos/cpp`. Playlist `PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`.

## The load-bearing fact

**No `english_authoring`, `factual_verification` or `factual_fixing` worker ever ran for
this video.** The folder has 172 work orders in `work_orders`. Only two carry a
non-null `result`, and only those two have runs attached:

| work order kind | orders | `completed` | `admitted`, never run | `superseded`, never run |
| --- | --- | --- | --- | --- |
| `acquisition` | 16 | 1 | 0 | 15 |
| `ledger` | 16 | 1 | 0 | 15 |
| `english_authoring` | 20 | 0 | 1 | 19 |
| `factual_fixing` | 20 | 0 | 1 | 19 |
| `factual_verification` | 20 | 0 | 1 | 19 |
| `git_publication` | 20 | 0 | 1 | 19 |
| `index_reference_repair` | 20 | 0 | 1 | 19 |
| `translation` | 20 | 0 | 1 | 19 |
| `translation_fidelity` | 20 | 0 | 1 | 19 |

`worker_runs` holds exactly three rows for this video in total, all under the one
completed `ledger` order. Every other order has `result = null` and
`blocker_evidence = null`.

Consequently `notes.en.md` and `internal/teaching-points.json` — the two outputs named
in the `write_assignment` of every authoring/fixing order — do not exist, and the only
commit touching this folder is the acquisition commit. Nothing in this directory is a
claim that a verifier confirmed or a fixer corrected; see `open-items.md`.

`/tmp/opencode/manifest.json` lists eight orders for this folder — three `admitted`
and five `superseded` — where the database holds 172 across nine kinds. The manifest is
the current planning tip, not the history; read the database before concluding anything
about what ran.

## The record that does exist

One `ledger` work order, `wo-4b2bb4ae9b51048ce192ca874fbc1e4e0effc92612dcacc276e801fc8146cd0b`,
`state = completed`, attempt 1, outcome `completed`,
`result.evidence = ["extraction and cue accounting recorded"]`. Three runs, all
`opencode` / `space-bunny-free`, all `completed`, no blocker, no claimed file writes:

- run 426, `EXTRACTION PROMPT (teaching-point extraction worker)`, session
  `ses_ee3239f33ffeV8qJZ9dsmR3wVN` — teaching points for segments S-005…S-008
- run 427, same prompt title, session `ses_ee3239f09ffeHnxyNZpHg7at8F` — teaching
  points for segments S-001…S-004
- run 428, `COMPLETENESS PROMPT (segment-accounting worker)`, session
  `ses_ee32321d0ffeN55Yfi5qsbSS7l` — a disposition for every planned cue

Transcript consumed by those workers, and the file every claim below is checked
against, is pinned at commit `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`, blob
`ce0c3bde7c36d19fae428c98e3e2934141e628a7`
(`videos/cpp/05_C++_Переменные,_присваивание,_выражения,_типы/internal/transcript.md`).
It has 425 cues (0…424), last cue at `00:09:36.320`.

## Files here

- `ledger-coverage-dispositions.md` — which stretches the two ledger workers agreed are
  teaching, and where they contradicted each other.
- `deferred-topics-and-cross-references.md` — the eight topics the video explicitly
  postpones, with the course videos it points at.
- `claims-that-need-qualification.md` — statements the video makes that the ledger
  recorded at face value and that no verifier ever checked.
- `caption-ambiguity-character-codes.md` — one passage where the auto-caption is
  ambiguous and the extraction run resolved it wrongly.
- `open-items.md` — what is unresolved.