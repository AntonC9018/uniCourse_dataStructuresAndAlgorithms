# Correction: GCC was not "originally Linux-only"

- What the video says: "GCC … для Линукса, но есть такая штука, как MinW. Она типа эволирует
  Linux для Windows" (transcript 00:00:20–00:00:24). Recorded as ledger TP-002 ("GCC was originally
  Linux-only, but MinGW emulates a Linux-like environment on Windows"). This claim survived into
  the teaching-point text verbatim.
- Why it is wrong, established by `english_authoring`, run 443 (codex `gpt-6.1-sol`, session
  `01a11d52-8ce6-72e3-ae82-40db8878784e`): GCC's own release history begins before Linux existed.
  The worker opened `https://gcc.gnu.org/releases.html` (worker tool events 2419 and 2424) and then
  ran a targeted `find` for `1987` on that same page to confirm the date before writing the claim
  into the note.
- The note's wording, which is the retained form of the correction: "'originally Linux-only' is not
  accurate history: GCC's release history begins in 1987, before Linux. The useful lesson is that a
  Windows distribution makes GCC available on Windows."
- The retained source choice is the GCC release-history page; its history establishes the relevant ordering: GCC predates Linux. This dossier does not need exact Linux release dates.
- Second half of the same correction: MSYS2 "does not emulate a Linux operating system". It is a
  Windows development environment supplying a Unix-like command layer and MinGW-w64 toolchains.
- `factual_verification`, run 445 (opencode `space-bunny-free`, session
  `ses_ee2a43085ffeU8DO4SYUVlfqmC`), checked this specific correction against the transcript and the
  cited page and raised no finding.