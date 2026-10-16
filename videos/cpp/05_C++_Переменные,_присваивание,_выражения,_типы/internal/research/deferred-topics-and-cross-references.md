# Topics the video postpones, and the course videos it points at

All anchors are `internal/transcript.md` at commit
`d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`. The `scope_boundary` classification and
its timestamps are the `ledger` work order
`wo-4b2bb4ae9b51048ce192ca874fbc1e4e0effc92612dcacc276e801fc8146cd0b`, runs 426
(session `ses_ee3239f33ffeV8qJZ9dsmR3wVN`, S-005…S-008) and 427 (session
`ses_ee3239f09ffeHnxyNZpHg7at8F`, S-001…S-004). The quoted Russian is from the
transcript; it is quoted only to identify the deferral, not to restate the lesson.

## Deferrals the extraction worker classified as `scope_boundary`

- `00:00:14.550`–`00:00:17.710` — stack layout ("Она на самом деле на стеке, но мы до
  этого дойдём позже").
- `00:00:33.280`–`00:00:39.470` — what `int` means; postponed so the naming idea lands
  first.
- `00:01:24.470`–`00:01:26.830` — how a name is resolved to an address.
- `00:04:33.560`–`00:04:38.350` — how a multi-byte number is laid out, delegated to a
  different video.
- `00:07:47.230`–`00:07:53.280` — how the print instruction chooses a behaviour, because
  it depends on function overloading ("связано с перегрузками функций").
- `00:08:24.630`–`00:08:27.430` — character codes, and what a type means beyond size.
- `00:09:20.230`–`00:09:25.030` — types into which no numbers can be written.

A note for this lesson should stay inside those seven boundaries; each is a promise the
video makes about later material, so expanding one here contradicts the lesson.

The expression definition at `00:02:08.270`–`00:02:13.910` is classified as an explanation by the extraction result, not as a `scope_boundary`; it still provides useful evidence that the definition is introduced there.

## Cross-references the video makes to other videos

- `00:04:33.560`–`00:04:38.350`: "Посмотрите видосик с тем, как числа хранятся в
  нескольких байтах". Resolves in this repository to
  `videos/cpp/08_Как_целые_числа_хранятся_в_байтах`, video `3HnvK8WrK4M`. Topic match
  is exact; the speaker does not say a title or an id, so the link is a strong
  inference, not a stated one.
- `00:05:36.189`–`00:05:38.639`: "Посмотрите видео, там есть об этом, как плюс-минус
  хранится". Probably the same video 08, since representation of the sign bit belongs to
  that lesson's topic. **Unverified** — the caption names nothing.
- `00:06:42.919`–`00:06:44.880`: "Что такое overflow? Тоже есть в видосике." The video
  is **not present in this repository**. `videos/cpp` holds only items 02–12 and none of
  them is about integer overflow; a `course_videos` query for this course returns
  nothing whose title matches overflow either. Leave the reference dangling rather than
  inventing a target.
- "Перегрузки функций" at `00:07:47.230`–`00:07:53.280` likewise has no folder in this
  repository.
- `00:00:02.280` "Как я упоминал до этого" refers back without naming anything. The
  preceding folder is `videos/cpp/04_C++_Инструкции_программы,_порядок_выполнения_инструкций,_простые_функции`
  (`Z8AFpeE7hOo`), but the transcript does not establish that link and this research
  does not assert it.

## Reusable source links

- This video: <https://www.youtube.com/watch?v=6ML34OuwZrc>, playlist
  `PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7`.
- Video 08 (the deferral target most often needed by this lesson):
  <https://www.youtube.com/watch?v=3HnvK8WrK4M>.
- Course folder index: `videos/cpp/index.md`.