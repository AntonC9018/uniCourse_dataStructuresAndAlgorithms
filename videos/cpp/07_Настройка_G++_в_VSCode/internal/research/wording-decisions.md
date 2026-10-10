# Wording and coverage decisions for lBVXv8Qaj9Y

Decisions made by the author (`english_authoring`, run 442, session `01a11d52-899f-7230-a10b-85357e4b3fb3`) and confirmed by the verifier (`factual_verification`, run 446, session `ses_ee2a43049ffeu853d2R6yPgsYt`, approved, TP-001–TP-039 all covered, no findings).

- F5 chooses a **launch configuration**, not a task (TP-009/TP-010 correction). The video calls it a "task" loosely; the note always routes F5 → launch entry → `preLaunchTask` label → task. Keep this phrasing in translations.
- Display name vs label: the recording says "G++ compile current file" but the inspected `tasks.json` label is `gcc_cpp_current_file` (TP-023). The note carries both and joins them via the `preLaunchTask` spelling requirement. Do not "fix" one to match the other.
- `compilerPath`/`cppStandard` configure **IntelliSense only**; the build runs the task's own `command`/`args` (TP-035–TP-039). Changing `c_cpp_properties.json` adds no `-std` flag to the build. The note states this separation explicitly, sourced to `https://code.visualstudio.com/docs/cpp/customize-cpp-settings` — the one external reference worth reusing.
- MSYS2-shell path vs Windows PATH (TP-004): `which gdb` prints an MSYS2-layout path; the Windows PATH entry must be its Windows-directory counterpart. Finding gdb in one shell does not prove the editor's processes resolve it.
- Stale-binary hazard (TP-021/TP-022): without `preLaunchTask`, a leftover `.exe` makes F5 succeed on old code. The note's prediction box exists because of this; the deletion step in the demo is load-bearing, not tidiness.
- `$` alone means nothing (TP-018): each variable (`${file}`, `${fileDirname}`, `${fileBasenameNoExtension}`) is defined by name per the [VS Code variable reference](https://code.visualstudio.com/docs/reference/variables-reference); the note's table is the agreed correction of the recording's loose "dollar means folder" line.
- Breakpoint semantics (TP-012): the highlighted line has **not** run yet; F10 executes it. The note's prediction/answer block records this.
- Variable meanings above and the IntelliSense/toolchain split are the two spots where the author fetched outside docs rather than the transcript; both URLs are in the note and need no re-verification unless the note is rewritten.

## Deliberately unresolved

- The exact recorded pacman invocation is not reproduced verbatim (TP-003 hedge in the note). Nothing in the record contradicts `pacman -S mingw-w64-x86_64-gdb`, but no transcript or commit pins the literal line, so the note marks its sample illustrative. Leave the hedge in place.
- `factual_fixing` (completed, no session) recorded "clean factual verdict needs no fixing" — no error was ever found or fixed for this video, so there is no before/after correction to retain.
