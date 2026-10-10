# The installer in this video is MSYS2, not MinGW

- The instructor repeatedly says "MinGW" and calls it something that "emulates Linux for Windows"
  (transcript 00:00:20–00:00:24). The recording's own artefacts contradict the name: he says
  "MC64" / "MCS" (ASR for `msys64`) at 00:14:29–00:14:53 and navigates `msys64/usr/bin` at
  00:05:21–00:05:45. `msys64` is MSYS2's default install root, not a MinGW directory.
  Source: folder `internal/transcript.md`, moments 20s, 24s, 321s, 869s, 889s.
- Established by `english_authoring`, run 443 (codex `gpt-6.1-sol`, session
  `01a11d52-8ce6-72e3-ae82-40db8878784e`): "This checkout has no existing note or coverage file
  for the video. The transcript shows an MSYS2 installation, although it uses 'MinGW' loosely."
  The note therefore retitles the section to "Choose and install MSYS2" and lists MSYS2 /
  MinGW-w64 / UCRT64 as three related-but-different names.
- Concrete consequence carried into the note: the different **build-environment** shortcuts
  (UCRT64 etc.) select different tool settings and search paths, so the recording's claim that
  "either icon opens the same console" (ledger TP-008) holds only for the two shortcuts actually
  compared at 00:01:56–00:02:17, not across all MSYS2 shortcuts.
- The compiler location the video reaches is `C:\msys64\usr\bin` — MSYS2's `/usr/bin`, where `usr`
  is a directory inside the MSYS2 tree, not the Windows user profile directory. The note flags
  this explicitly because "usr" reads like "user"; a MinGW-w64 UCRT64 package would land under
  that environment's directory instead. Ledger TP-023 as recorded ("При установке MinGW
  компилятор gcc кладётся в папку /usr/bin оболочки") is true only for the recorded package choice.
- Reusable sources opened by run 443 for this: `https://www.msys2.org/`,
  `https://www.msys2.org/docs/environments/`, `https://www.msys2.org/docs/filesystem-paths/`.
- The repository's own lab agrees on the name: `en/labs/common/05_compiler_install.md` lists the
  task as "Install GCC using msys2, WSL, or Zig" and links this exact video
  (`watch?v=bQnbkV6xgY4`) as the GCC route.