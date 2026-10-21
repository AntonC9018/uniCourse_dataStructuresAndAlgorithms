# Coverage dispositions for `6ML34OuwZrc`, and where the two ledger workers disagree

Sources: `ledger` work order
`wo-4b2bb4ae9b51048ce192ca874fbc1e4e0effc92612dcacc276e801fc8146cd0b`.
Cue numbers and dispositions are run 428 (`COMPLETENESS PROMPT (segment-accounting
worker)`, session `ses_ee32321d0ffeN55Yfi5qsbSS7l`); `nonTeaching` ranges are run 426
(`EXTRACTION PROMPT`, session `ses_ee3239f33ffeV8qJZ9dsmR3wVN`). Timestamps were
converted from cue indices against `internal/transcript.md` at commit
`d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6` on 2026-10-10; that conversion is not a
worker finding.

## Non-teaching material the accounting worker assigned

- S-002 `caption_noise`, cue 99 only, `00:02:08.270`.
- S-004 `caption_noise`, cue 164 only, `00:03:32.280`.
- S-005 `off_topic`, cues 249…261, `00:05:36.189`–`00:05:51.280`.
- S-006 `off_topic`, cues 295…296, `00:06:44.870`–`00:06:47.830`.
- S-006 `repetition`, cues 307…309, `00:07:03.309`–`00:07:05.880`.
- S-008 `repetition`, cues 415…424, `00:09:25.910`–`00:09:36.320` (to end of video).

Everything else in all eight segments was accounted `teaching`.

## Non-teaching material the extraction worker flagged

Only two `nonTeaching` entries exist in either extraction run:

- run 426, S-005, `off_topic`, `00:05:40.000`–`00:05:53.840`, detail: the speaker points
  at another video covering how the plus/minus sign is stored.
- run 426, S-006, `repetition`, `00:07:01.749`–`00:07:04.000`, detail: the printing
  statement just described is rephrased with no new content.

Run 427 reported `nonTeaching: []` for S-001…S-004, and run 426 reported `[]` for
S-007 and S-008.

## Disagreement 1 — both workers run the "watch the other video" aside far past its end

The aside is one sentence: *"Посмотрите видео, там есть об этом, как плюс-минус
хранится"*. It runs `00:05:36.189`–`00:05:38.639` — it starts inside cue 249, which is
exactly where the accounting run's window starts, and it is over by the end of cue 250.

Both workers then keep the window open for far longer than that:

- accounting run: `off_topic` `00:05:36.189`–`00:05:51.280` — correct start, then
  **12.6 s of teaching material** past the end of the aside, over *"Как нам сделать,
  чтобы эта переменная И ссылалась только на одну ячейку памяти, а не на четыре
  сразу. Нам нужно сохранить туда байт … нам нужно сделать include SD in"*. That is the
  payload of the segment.
- run 426: `nonTeaching` `00:05:40.000`–`00:05:53.840` — starts 1.4 s *after* the aside
  has already ended, and runs 15.2 s past it over the same payload, stopping exactly
  where its own `code_change` teaching point for the `#include <cstdint>` begins at
  `00:05:53.840`.

Neither window is usable as-is. The aside itself is 2.5 s long.

## Disagreement 2 — the "overflow is in another video" aside in S-006 is mis-cut

Accounting `off_topic` `00:06:44.870`–`00:06:47.830` contains *"Тоже есть в видосике.
Ну, в общем, я могу попытаться вписать 256 и это попытаться скомпилировать."* The
second clause introduces the compilation demonstration that run 426 recorded as a
`test_result` teaching point at `00:06:47.830`–`00:06:57.670`. The genuine aside is
only *"Что такое overflow? Тоже есть в видосике."*, `00:06:42.919`–`00:06:44.880`,
which the accounting run does not mark at all.

## Disagreement 3 — the closing recap in S-008

Accounting marks cues 415…424 (`00:09:25.910`–`00:09:36.320`) `repetition`; run 426
carries a teaching point over `00:09:25.040`–`00:09:39.920` and an empty `nonTeaching`
list for S-008. The transcript supports the accounting label: the closing minute
repeats the type→size relation already established at `00:04:27`–`00:05:09` without
adding to it. Prefer `repetition`.

## Caption hazard for anyone working from this transcript (recreated 2026-10-10, not a worker finding)

`internal/transcript.md` is a rolling caption in which each cue repeats the tail of the
previous cue: line *N+1* usually ends with line *N*'s full text. Concretely, cue 99 is
literally `"вписать то, что вы говорите ваписываем."`, a duplicate of cue 98's tail.
That is what both `caption_noise` dispositions are. Line count is not sentence count:
425 cues carry roughly half as many distinct utterances, so any claim about "the video
says X" must be anchored to a timestamp, not to a line range.