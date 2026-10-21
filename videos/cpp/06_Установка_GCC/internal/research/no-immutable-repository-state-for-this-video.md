# No immutable repository state exists for this video, and why every sample is a reconstruction

- Finding, `english_authoring` run 443 (codex `gpt-6.1-sol`, session
  `01a11d52-8ce6-72e3-ae82-40db8878784e`): "I found no matching GCC code state in the inspected
  repository history, so the note will identify samples as reconstructions and link them to the
  recording." The worker ran `git_history` on `notes.en.md`, `en/04_compiler_and_ide/doc.md` and
  `en/labs/common/05_compiler_install.md` before concluding this.
- Because no commit holds the taught states, the note carries no commit-pinned blob citations at
  all. Its "Code history trail" is video timestamps only (364s, 397s, 534s, 577s, 596s, 966s,
  1002s, 1035s), preceded by an explicit statement that no matching repository commit was
  established and that the repository's installation lesson describes a different workflow.
- A relevant commit found in history, but not recorded as a worker file read; it is deliberately *not* cited in the note:
  `074743b9a53b16554d3c67a26d9ef9cef025590c` ("Add compiler installation instructions"), which holds
  `en/04_compiler_and_ide/doc.md` as blob `91709bf07c5bd712533ca8573854ee4dbcd38c7b`. The worker event record does not show a read of this commit: run 443 has a `git_read_file` event at `d6b06478…`; this commit/blob pairing was derived from history and checked locally on 2026-10-14. A commit that merely adds an exercise is not evidence for this
  video's installation or code states, so the note links the lesson page without its adding commit.
  (Commit and blob verified locally on 2026-10-10 with `git ls-tree` / `git rev-parse`.)
- The one repository link that *is* retained is relative, to the lab document the exercise lives in:
  `[compiler installation lab](../../../en/labs/common/05_compiler_install.md)` in
  `notes.en.md`. `factual_verification` run 445 (opencode `space-bunny-free`, session
  `ses_ee2a43085ffeU8DO4SYUVlfqmC`) resolved that relative path on disk and confirmed it lands on
  the real file — so the published-website URL was correctly *not* substituted for it. That file's
  slug is `en/common/labs/compiler-install` and its site backlink is
  <https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/common/labs/compiler-install/>,
  which is a published URL and therefore not usable as the exercise citation.
- `README.md` was read and listed in the author's `sourcePaths` but produced no citation.
- Verified English revision: commit `9524e929bc1df59b55902f900a34d87f1d4c94f7`
  ("Update course video bQnbkV6xgY4", 2026-10-09), immutable link
  <https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/9524e929bc1df59b55902f900a34d87f1d4c94f7/videos/cpp/06_%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0_GCC/notes.en.md>.
  Its `notes.en.md` sha256 is `c847792cf695e2d0341e80e0b07c5374c93fe6f0ca168178fd481639584b29df`
  and `internal/teaching-points.json` is
  `c885f29aba68f2a4d53474536cb4e97b4f8d234af24b175166071806315200f6` — the same two hashes both
  `english_authoring` (run 443) and `factual_fixing` recorded as outputs.
- Cost of the missing pinned state, stated plainly: any reader who wants the *exact* text the
  instructor typed must open the recording. The note compensates by labelling every fenced block as
  "a reconstruction using the path and filename discussed in the recording" and by never presenting
  the reconstructions as repository content.