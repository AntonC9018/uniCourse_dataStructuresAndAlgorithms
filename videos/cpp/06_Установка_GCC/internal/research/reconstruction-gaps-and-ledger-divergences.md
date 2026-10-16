# Reconstruction gaps and ledger/note divergences the verifier saw but did not raise

`factual_verification` run 445 (opencode `space-bunny-free`, session
`ses_ee2a43085ffeU8DO4SYUVlfqmC`) recorded these during its reasoning and then returned
`"findings":[]`. They are worth keeping because a later re-verification would otherwise repeat the
same checks from scratch.

- **TP-048 — the ledger wording is the imprecise side.** Ledger TP-048 (547200–553670 ms,
  `scope_boundary`) says "author asks to repeat the same command". Transcript 00:09:05–00:09:13
  actually says "Перед тем, как компилировать, вот эту программу вот эту команду пропишите. Что она
  именно делает, чуть позже объясню." The note's reading — "the recording asks for a preparatory
  console command and postpones explaining its purpose", tied to the temporary `set` PATH step —
  matches the transcript; the ledger's "repeat the same command" does not. The verifier called
  this out ("Slight mismatch but ok").
- **TP-060 — the note and the ledger describe different orderings.** Ledger TP-060 says the PATH
  list "already contains the folder that holds the compiler" and that a new folder is appended
  after a semicolon. The note says an earlier command *prepended* it and this demonstration
  *appends* one at the end. Both readings appear in the record (TP-054 prepend vs TP-061 append);
  the verifier judged the divergence immaterial because the note marks the commands as
  reconstructions.
- **TP-024 — the note extends the recorded claim.** Recorded: "g++ добавляет значения по умолчанию
  для компиляции файлов C++". The note adds that `g++` "additionally arranges C++ library
  **linking** by default". Supported by <https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html>
  (opened in run 443), not by the video. The verifier accepted the extension.
- **`std::cin.get()` is a simplification, not the recorded code.** Transcript 00:17:02–00:17:08
  ("нужно здесь просто прописать std::cin.get(), и ему нужна ссылка на char, вот, вставь его сюда")
  shows the instructor passing a **char** to `get` — i.e. `std::cin.get(c)`, with a `char`
  variable he then names. Ledger TP-078 and the note both reduce it to argument-less
  `std::cin.get();`. The note hedges ("if input is already available or closed, it may not wait"),
  which is consistent with the no-argument form, but a reader following the recording literally
  will see a different statement. Neither worker raised this.
- **Fn+Esc is keyboard-specific, not a GCC requirement.** Ledger TP-012 (178400–194120 ms) states
  it as a requirement; transcript 00:03:16–00:03:19 shows it is a Fn-lock workaround for the
  demonstration keyboard before Shift+Insert. The note narrows it to "keyboard-specific, not a GCC
  installation requirement" — a deliberate de-escalation of a recorded point, recorded correctly.
- **The `pacman` command itself is not recoverable.** Ledger TP-011 (172320–175910 ms) says the
  install command is copied from the video description. The transcript does not contain the command
  text or the package name, so run 443 explicitly declines to reproduce it: "The spoken transcript
  does not preserve the complete command or package name, so it is not reproduced here as an exact
  command." Unresolved by design.
- **Playlist position disagrees between records.** Work-order `observations` for this video record
  `memberships: [["PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7", 6]]` / `playlist_order: 2`, while
  `en/labs/common/05_compiler_install.md` links the same video as `index=12`. Not reconciled; no
  worker looked at the playlist link.