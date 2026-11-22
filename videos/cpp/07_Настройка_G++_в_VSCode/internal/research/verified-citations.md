# Verified citations for lBVXv8Qaj9Y (G++ in VS Code)

All states below were inspected by the verifier (`factual_verification`, run 446, session `ses_ee2a43049ffeu853d2R6yPgsYt`) via `git rev-parse --verify`, `git show`, and `git ls-tree` against note commit `d4910de36592e8c4e9029bc07c2b7d7730f37975`. Verdict: approved, zero findings. Reuse these pins rather than re-resolving.

- `launch.json` at `c484907b6e6ac331c6ab4fe508ca432f6f2585d5`: `(gdb) Launch` is the third entry (after codelldb, `(Windows) Launch`); fields `program`, `cwd: ${fileDirname}`, `preLaunchTask: gcc_cpp_current_file` confirmed. Proves TP-016 and the note's simplified excerpt. Link form: `.../blob/c4849.../.vscode/launch.json`.
- `tasks.json` at `fef337c86c73ec8d197461ffe9327d69612ab81e`: exactly two tasks (`zig_cpp_current_file`, `gcc_cpp_current_file`); g++ entry has `command: g++`, `args: [${file}, -o, ${fileBasenameNoExtension}.exe]`, `options.cwd: ${fileDirname}`. Proves TP-023–TP-025, TP-028, TP-033. The note's "additional flags" caveat is accurate: the excerpt omits bookkeeping fields.
- `settings.json` at `cc744a22dcdfce37fa772561d7c9354af05b3b5a`: contains `"*.json": "jsonc"`. Proves TP-034's sample; nothing more is claimed from this file.
- `c_cpp_properties.json` at `ec49d61932f626869f9cc0e4050733b56aba6696`: `cppStandard: c++20`, `version: 4`. Proves TP-036/TP-037 sample.
- `c_cpp_properties.json` at `4548bceac3c7982861496f1d77d29ecb7eddf7a0`: `compilerPath: ${default}` with `cppStandard: c++20`. This is the *before* state; the video's on-screen edit to `g++` exists in no commit, so the note correctly labels this pin "related" and evidences the edit by timestamp `[00:09:55]` instead.
- Lab link `en/labs/common/05_compiler_install.md` confirmed present at `d4910de36592e8c4e9029bc07c2b7d7730f37975` via `git ls-tree`. Safe to keep as the note's relative lab reference.
- GDB package `mingw-w64-x86_64-gdb` verified live by the verifier against `https://packages.msys2.org/packages/mingw-w64-x86_64-gdb`. The note deliberately does not claim to reproduce the recording's pacman line character for character (TP-003); cite the package page, not the transcript, for the name.

## Pinning rule this video established

- Author (`english_authoring`, run 442, session `01a11d52-899f-7230-a10b-85357e4b3fb3`) labels every `.vscode` pin **related committed version**, never exact: later repo revisions drifted from the recording, and two on-screen states (launch entry with `preLaunchTask` deleted at `[00:05:16]`; `compilerPath: g++` at `[00:09:55]`) were temporary edits never committed. Temporary states are evidenced by video timestamps; the note's "Code history trail" section states this explicitly.
