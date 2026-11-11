# Sources pinned, and what is still open

## Sources pinned

- Transcript, Russian, immutable: commit `7c2ed1f` "Acquire course transcripts",
  `videos/cpp/11_C++_Базовые_техники_блоки,_функции,_структуры/internal/transcript.md`,
  blob `051929a9f68f7e39be35ecb9c836efff4f6a120b`,
  sha256 `d04cbc2c25ea4a71f86c5c74429b635e964f8fb08bfab11e4d878524d8901558`.
  Same commit's `internal/transcript.vtt`, blob
  `4d3f4d31760ef669040ad4878e4a0a4f3c15fbad`, sha256
  `a1e40177b6567a06e8994b38891d7ca6578de68c6faa38a125631928eb330b58` — identical to the
  `input_hashes.canonical` recorded on all 177 work orders for this video, which is what
  pins the caption the ledger workers were given.
- `internal/video.json`: `courseVideoId` `6JtlzvwhHr0`, video etag
  `WGfnmW9l-vLxmwbKT2UI_Xvk2gs`, caption etag `0yyOfls55yMts9cJciuVtIXYiP8` — matches
  the `current` block of every work order, so no accepted reupload happened for this
  folder.
- Course index: `videos/cpp/index.md`, this video the 10th of 11 listed rows, playlist
  `PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`. The "Устройство алгоритма" and "Git" rows point
  at `uniCourse_csharp` folders and are unrelated to this video. (The work-order
  observations record `position: 11` and `playlist_order: 2` for the same entry, which
  disagrees with the index row count — worth not relying on either number without
  checking the playlist.)
- `std::abs` header facts, checked 2026-10-10 against
  <https://en.cppreference.com/w/cpp/numeric/math/abs.html> (external; not a worker
  finding — see `abs-header-never-named.md`).

## Labs relevant when the note is finally written

Checked 2026-10-10 by directory listing of the working tree's `en/labs/` and `ru/labs/`
trees — no worker ever linked these, they are candidates for the future authoring run to
consider:

- `en/labs/cpp/06_struct.md` (slug `en/cpp/labs/struct`) — the video's second half is a
  struct refactor.
- `en/labs/cpp/07_function.md` (slug `en/cpp/labs/function`) — the video's first half
  extracts a function.
- `en/labs/cpp/26_function_execution.md` (slug `en/cpp/labs/function-execution`) — the
  call-by-value memory walkthrough the video performs in S-014…S-019.
- `en/labs/cpp/08_modeling.md` (slug `en/cpp/labs/modeling`) — the game-grid object model
  the lesson builds toward.

The Russian mirrors under `ru/labs/...` exist for all of these; the repo's AGENTS.md
requires `en/` and `ru/` to be edited identically.

## Open, unresolved

- No `english_authoring`, `factual_verification`, or `factual_fixing` run exists for this
  video, so every claim above is either ledger evidence or a fresh check. Nothing here has
  been reviewed.
- The parameter identifier conflict (`xa/ya/xb/yb` vs `XA/YA/XB/YB` vs
  `xPlayer/yPlayer/xEnemy/yEnemy`) is unresolved: the extraction record contradicts both
  itself and the transcript, and no worker reconciled it.
- The board/code coordinate drift is unresolved: the record contains player (1, 1) and
  player (1, 3) with no reconciliation.
- Whether the two empty caption cues (1567, 1583) should be teaching is unresolved; the
  two ledger workers disagree.
- `internal/teaching-points.json` and `notes.en.md` do not exist, so no note wording is
  available to check any of the above against. Any future note must resolve the
  identifier and coordinate questions before it states the function signature or the
  worked example.
