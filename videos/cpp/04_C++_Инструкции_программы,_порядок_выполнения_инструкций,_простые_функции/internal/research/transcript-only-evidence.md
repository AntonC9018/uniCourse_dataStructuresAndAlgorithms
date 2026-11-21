# The transcript contains no C++ source-code spelling

The authoring session used the transcript to distinguish spoken prose from source-code tokens. Current text was checked against the pinned transcript on 2026-10-14; that is an independent current check, not proof of what any worker inspected.

`internal/transcript.md` at `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6` contains **zero occurrences** of:

- `int`, `void`, `return`
- `#include`, `iostream`
- `endl`
- `cout` (as a word — the caption renders it `SCD out` at `00:02:43`, and `команда DL` at `00:06:55`)

The recording describes the program in Russian prose only: "инструкция письма в консоль" (`00:01:59`),
"переход на новую строку" (`00:02:54`, and again at `00:03:41`), "команда", "функция с именем f",
"мейн". The only concrete tokens the caption does preserve are the two string literals, `Hello World`
(`00:02:37`) and `Антон` (`00:02:58`, `00:03:17`), and the executable name rendered as `A.out` (preceded by a Cyrillic “а” in the cue at `00:02:33`).

## What this means for every code sample in `notes.en.md`

- `#include <iostream>`, `int main()`, `void f()`, `void B()`, `std::cout`, `std::endl`, `return` types and
  the whole nesting of the reconstructions are **author-supplied C++**, chosen to make the spoken prose
  compilable and readable. The transcript supports their *behaviour*, not their spelling.
- This is why run 505 wrote into the note, at line 26, that the programs are "**simplified reconstructions**,
  not claims of exact committed source". That framing is load-bearing and must not be softened.
- No captured frame exists for this folder — `internal/frames/`, `internal/images/` and `internal/scenes/`
  were never granted or created, and `worker_tool_events` for run 505 contains no `video_frame` item.
  There is therefore **no visual evidence at all** for what the instructor's editor actually showed on
  screen. Anything about the literal source text of the recording is unresolved.

## Caption hazards for anyone re-reading this transcript

The caption is a rolling auto-caption: cue *N+1* repeats the tail of cue *N*, so 375 lines carry roughly
half as many distinct utterances. Line count is not sentence count; anchor to a timestamp.

Specific garbles that change meaning if taken literally:

- `00:02:43` "вот **SCD out** - это инструкция" — `std::cout`.
- `00:02:28` "можно ещё флагов подключить на **Wordling**" — linking.
- `00:06:55` "потом это команда **DL**" — `endl`.
- `00:05:19` "инструкции из **фаче**. **Hello и ан** вот эти две" — `f`; `Антон` mangled to `ан`.
- `00:04:18` "увидим просто **main и fтся**" — `main`; a garble of the `f` function's name.
