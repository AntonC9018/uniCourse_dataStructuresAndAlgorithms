# Commit-pinned citation truncated by parentheses in the folder name

## The defect

- Verifier run 501 (`factual_verification`, session `ses_ed99ef826ffeXc23VsmIecxvex`)
  returned `changes_requested` with exactly one finding, `F-001` / `bad_citation`,
  against `notes.en.md`.
- Evidence as recorded: `repository_blob` `AntonC9018/uniCourse_dataStructuresAndAlgorithms`
  at commit `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`, path
  `videos/cpp/02_Сложение,_умножение_в_других_системах_счисления_Перевод_из_одной_системы_в_другую_(сырой)/internal/transcript.md`.
- The deterministic citation check resolved the note's link to a path ending at
  `...(сырой` and reported `confirmed_missing`. The rest of the path
  (`)/internal/transcript.md`) never reached the check.

## Root cause (fixer run 502, session `ses_ed99a626affeLgAthDIr73p8Z3`)

- The note text was complete on disk; the *parsed* path was not. The video folder
  name ends in `_(сырой)`, and a Markdown inline link terminates at the first `)`.
  The link destination therefore resolved to `..._(сырой`.
- Fix applied: percent-encode the two parentheses in the URL as `%28сырой%29`.
  Line 25 of `notes.en.md` was the only line changed; no other text was touched.
- Reusable rule: **every** Markdown link in this repository whose destination path
  runs through a video folder ending in `_(сырой)` must percent-encode `(` and `)`.
  Angle-bracket link destinations (`<https://...>`) are an alternative that Markdown
  also permits.

## The same diagnosis was reached earlier and never published

- Superseded `english_authoring` run 487 (codex, session `01a124be-1d97-7f03-a55c-dd9c1f4612d2`)
  had already rewritten the citation with `(` → `%28`, `)` → `%29`, and had also
  inserted a simplified calculation beside the citation.
- Its structured result was `blocked`: the app-owned file tools refused the assigned
  path, and readback confirmed the repair was not in the file. The cycle was later
  superseded, so the finding surfaced again through run 501 / run 502.

## Diagnostic lesson

- `confirmed_missing` from the deterministic citation check is *not* proof that the
  file is absent at the pinned commit. Run 501 cross-checked with `git_history` and
  `git_read_file`, found the blob present at `d6b06478…`, and first returned
  `approved`. It only emitted `F-001` after its own result failed validation against
  the truncated path the application had parsed out of the note.
- Check the pinned blob with read-only Git before raising `bad_citation`; then
  suspect the link syntax, not the commit.

## Independent confirmation of the encoded path (fresh check, 2026-10-10)

Not a worker finding; performed while recreating this research.

- Locally, the blob exists: `git cat-file -e d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6:<full path>`
  succeeds in the course checkout.
- Remotely, the percent-encoded raw URL returns HTTP 200, while the same URL with
  `internal/transcript_missing.md` returns HTTP 404 — so the 200 is meaningful.
  Source: `https://raw.githubusercontent.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6/videos/cpp/02_%D0%A1%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5,_%D1%83%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B2_%D0%B4%D1%80%D1%83%D0%B3%D0%B8%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%D1%85_%D1%81%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%9F%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4_%D0%B8%D0%B7_%D0%BE%D0%B4%D0%BD%D0%BE%D0%B9_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B_%D0%B2_%D0%B4%D1%80%D1%83%D0%B3%D1%83%D1%8E_%28%D1%81%D1%8B%D1%80%D0%BE%D0%B9%29/internal/transcript.md`
- The HTML blob page could not be checked: `https://github.com/...` returned HTTP 503
  through this environment's proxy while `https://github.com/` itself returned 200.
  Whether the rendered blob page accepts the encoded form is therefore unverified.