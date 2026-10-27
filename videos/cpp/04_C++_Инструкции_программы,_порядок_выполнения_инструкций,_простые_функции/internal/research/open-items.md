# Open evidence and editorial questions

These are unresolved source limits, not a worker TODO list.

## Reconstruction boundaries

The transcript does not show the output after the middle newline is removed, nor the final four-line trace in the nested example. The note labels both as predicted outputs of its simplified reconstruction. Keep those labels if the note changes.

The recording describes function calls and output in Russian prose but does not provide C++ tokens for the code samples. Treat identifiers, declarations, includes, and syntax as reconstructed. The pinned transcript supports the described behavior, not the exact source spelling; `transcript-only-evidence.md` documents the distinction.

## Unsettled interpretations

- The terminal `%` is discussed as indicating that no newline was printed. The note attributes the marker to the shell, but the transcript does not establish which shell produced it; do not state a shell attribution as recorded fact.
- `std::endl` flushing behavior and function declaration order are accurate C++ explanations added for context, not points established by the video. Keep them identified as clarifications if retained.
- “Last call site” is ambiguous in the Russian phrasing at `00:05:56` and `00:06:23`; keep the note’s interpretation qualified.
- Timestamp links at `t=199s` and `t=291s` land near, rather than on, the closest transcript cues (197/200 and 289/292). They are passage-level anchors; tighten only if the note requires exact cue alignment.

The exact output and code shown on screen remain unverified because this audit has no captured frame evidence. The separate relative lab link identifies practice material, not the recording’s source code.
