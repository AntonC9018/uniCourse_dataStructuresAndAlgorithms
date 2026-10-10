# What the maintenance record contains for `6JtlzvwhHr0`

Folder `videos/cpp/11_C++_Базовые_техники_блоки,_функции,_структуры`, playlist
`PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`. The work-order observations for this video record
`position: 11` and `playlist_order: 2`, and `videos/cpp/index.md` lists it as the 10th of
11 video rows. Video etag `WGfnmW9l-vLxmwbKT2UI_Xvk2gs`, caption etag
`0yyOfls55yMts9cJciuVtIXYiP8` — the pair the work orders record and
`internal/video.json` carries.

## The load-bearing fact

**No `english_authoring`, `factual_verification`, or `factual_fixing` run ever executed
for this video.** `work_orders` holds 177 orders for `course_video_id = '6JtlzvwhHr0'`
across nine kinds. Every one of those three kinds has `result = null`,
`blocker_evidence = null`, and zero rows in `worker_runs` — including all eight the
manifest names for this folder.

Each authoring/fixing order's `write_assignment` names the same two outputs,
`internal/teaching-points.json` and `notes.en.md` (`factual_verification` orders name
none — they only consume them). Neither output exists in this checkout, and the only
commit touching the folder is `7c2ed1f` ("Acquire course transcripts"). So nothing in
this directory may be read as a verifier's finding or a fixer's correction: all worker
evidence for this video is *ledger* evidence.

`/tmp/opencode/manifest.json` lists 8 orders for this folder — 3 admitted, 5
superseded — each with an empty `runs` array. The database is the fuller record; read
it before concluding what ran.

## What did run

`worker_runs` holds 12 rows for `course_video_id = '6JtlzvwhHr0'`, all under `ledger`
orders, split across two generations of the order:

- 3 runs under `wo-cc1a4fd0797851b37689d751e65b3221804d4760014e938770d2baa1a46586a2`
  (superseded 2026-10-09). Their sessions contain only the dispatched prompt — no
  assistant turn and no stored result, so nothing is recoverable from this generation.
- 9 runs under `wo-6b35f759542007dad34cea0b40273f6fa957576f174f60dd5caef8cd2529500e`
  (created 2026-10-09, superseded 2026-10-10), all with stored results:
  - 8 teaching-point extraction runs, sessions `ses_edd95c4e1ffelKnBxfFrxxdySf`,
    `ses_edd95c4b3ffe7C9rXws3Y9eW3a`, `ses_edd95c49dffeUUUnGgzjO3Krp1`,
    `ses_edd9542faffeNy0qbr2pt7GgFa`, `ses_edd9542d3ffeCOUPfCGOetAKwZ`,
    `ses_edd9542c0ffe4NPvYvg46Lwlx3`, `ses_edd94d35cffeZhmwMEnFWuCwNE`,
    `ses_edd94d338ffek3VwIBe23VM6wJ` — segments S-001…S-030 between them.
  - 1 segment-accounting run, session `ses_edd948d82ffeRVAPp71blEUy5a` — a disposition
    for every cue in every segment.

All nine report `claimedChangedPaths: []`, so no ledger content reached the repository.

## Transcript the ledger consumed, pinned

`internal/transcript.md`, 1587 cues, `00:00:00.320`–`00:37:10.640`, added by
`7c2ed1f`. At HEAD it is blob `051929a9f68f7e39be35ecb9c836efff4f6a120b`,
sha256 `d04cbc2c25ea4a71f86c5c74429b635e964f8fb08bfab11e4d878524d8901558`.
`internal/transcript.vtt` at the same commit is blob `4d3f4d31760ef669040ad4878e4a0a4f3c15fbad`,
sha256 `a1e40177b6567a06e8994b38891d7ca6578de68c6faa38a125631928eb330b58` — which is
exactly the `canonical` value every work order for this video records in `input_hashes`,
so the pinned caption file is the file the workers were given.

The caption stream is the rolling-duplicate format: most sentences appear twice, once as
a tail of the previous cue and once as the head of the next, and 2–4 second gaps with no
cue separate some sentences. The accounting worker labels 11 cue ranges `repetition`,
4 `wait` and 1 `caption_noise`.

## Files here

- `extraction-identifier-confusion.md` — the ledger records the function's parameters and
  caller variables under one wrong name set; the transcript uses three different ones.
- `board-example-drifts-from-code-example.md` — the worked example silently changes the
  player's y coordinate when it moves from board to code.
- `caption-digit-hazards.md` — coordinates spoken as bare digit pairs ("13", "32") and a
  "1 2 3 / 1 2 3 4 5" count that reads like program output but is the instructor pointing
  at the screen.
- `abs-header-never-named.md` — the video asserts `abs` must be imported without naming a
  header; what to put in a note, with the source.
- `ledger-nonteaching-disagreement.md` — where the extraction worker's non-teaching flags
  and the accounting worker's dispositions contradict each other, and why the coverage
  verdict is still complete.
- `sources-and-open-items.md` — reusable pins and everything left unresolved.
