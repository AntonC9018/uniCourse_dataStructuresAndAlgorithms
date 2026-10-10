# Open items for `6ML34OuwZrc`

## The lesson was never written, verified, or fixed

- `notes.en.md` and `internal/teaching-points.json` do not exist. Both are the two
  outputs named in the `write_assignment` of every `english_authoring` and
  `factual_fixing` order for this video.
- The folder has 172 work orders: 2 `completed` (`acquisition`, `ledger`), 7 `admitted`,
  163 `superseded`. Only the two completed ones carry a `result`; the other 170 have
  `result = null` and `blocker_evidence = null`. `worker_runs` holds three rows for this
  video in total, all under the completed `ledger` order. **169 of the 172 orders were
  superseded before any worker started** — the cycle was re-planned repeatedly (input
  hashes changed under it) and only the transcript acquisition and the segment ledger
  ever got as far as running.
- `git log` for this folder returns exactly one commit, `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`
  "Acquire course transcripts".
- Nothing in this directory has ever been checked by a verifier or corrected by a fixer.
  Every "this is what the video claims" statement here is still just that.

## The teaching points exist only inside the maintenance database

The `ledger` work order completed with
`result = {"evidence": ["extraction and cue accounting recorded"], "outputHashes": {},
"status": "completed"}` — an **empty** `outputHashes` and an `expectedOutputs: []`
`write_assignment`. The 60-odd teaching points from runs 426 and 427 and the
per-cue dispositions from run 428 live only in `worker_runs.structured_result` and in
the three OpenCode sessions. If that database or those sessions are lost, the segment
plan for this video is lost with them and the whole lesson has to be re-segmented.

## A `test_result` was recorded without any execution

Run 426 labelled `00:06:47.830`–`00:06:57.670` a `test_result` — "Compiling code that
assigns 256 to a uint8_t variable is reported as an error". Nothing in this video's
record shows a compilation: `worker_tool_events` holds one row for these runs (a `bash`
call on run 426) with no repository path, no output and no outcome detail. The claim is
the speaker's, transcribed. It is also wrong — see `claims-that-need-qualification.md`
§4. Treat `kind` in the ledger as the worker's *label*, not as evidence of observation.

## Unresolved, needs the video itself

- The character-code run-on at `00:08:14.620`–`00:08:24.630`; see
  `caption-ambiguity-character-codes.md`. Two readings survive the caption.
- Whether the aside at `00:05:36.189`–`00:05:38.639` should be excluded from the note or
  kept as a pointer to `08_Как_целые_числа_хранятся_в_байтах`. The two ledger workers
  give it different windows and both run 12–15 s past its real end; see
  `ledger-coverage-dispositions.md`, disagreement 1.

## Cross-references with no target in this repository

- "Что такое overflow? Тоже есть в видосике" (`00:06:42.919`–`00:06:44.880`).
- Function overloading, deferred at `00:07:47.230`–`00:07:53.280`.

`videos/cpp` holds items 02–12 and neither has a folder. Do not invent a link; if the
note needs one, the reference has to stay as prose.

## Disagreements left standing

The two ledger workers contradict each other on three cue ranges. Nothing in the record
adjudicates them; `ledger-coverage-dispositions.md` states which reading the transcript
supports for each, but the resolution is this file's, not a worker's.