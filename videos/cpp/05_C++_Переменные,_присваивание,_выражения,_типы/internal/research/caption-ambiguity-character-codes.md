# The character-code passage at 00:08:14 is ambiguous, and the extraction run resolved it wrongly

## What the transcript says

`internal/transcript.md` at commit `d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6`,
`00:08:14.620`–`00:08:24.630`:

> А символ ноль — это это ничего. Если мы, например, бы взяли символ 32, тогда он
> напечатает букву А он пробел. 33 — это символ, то есть код для водатного знака.

Two things are wrong with this as an authority:

- `водатного знака` is an ASR corruption of `вос…лицательного знака`; read it as
  "exclamation mark".
- *"напечатает букву А он пробел"* is a run-on. It contains the claim for the letter A
  and the claim for the space **with a single code, 32, in front of them**. There is no
  `65` anywhere in the span.

## What the ledger turned it into

Run 426 (`ledger` work order
`wo-4b2bb4ae9b51048ce192ca874fbc1e4e0effc92612dcacc276e801fc8146cd0b`, session
`ses_ee3239f33ffeV8qJZ9dsmR3wVN`), S-007, `00:08:14.620`–`00:08:24.630`, kind `fact`:

> Character code 0 prints nothing, code 32 prints the letter A which is the space
> character, and code 33 is the exclamation mark.

"code 32 prints the letter A which is the space character" fuses two distinct claims and
is wrong as written. A note drafted from this ledger text would teach `32` as the code
for `A`.

## What is safe

Checked 2026-10-10 against the escape-sequence table at
<https://en.cppreference.com/w/cpp/language/escape>, which lists `0` as the null
character, `32` as the space character, `33` as `!` and `65` as `A`.

- `0` is `NUL`; printing it as a character emits nothing.
- `32` is the space character.
- `33` is `!`, the exclamation mark.
- `65` is `A`.

So the two safe statements are "32 is the space" and "33 is `!`". Neither ledger
statement about `A` is usable as written.

## Two readings of the audio, unresolved

- (a) The speaker said "32 — пробел. 65 — буква А. 33 — восклицательный знак" and the ASR
  dropped the `65`, gluing "букву А" onto the previous clause.
- (b) The speaker said only "32 — пробел. 33 — восклицательный знак" and "букву А" is a
  bleed from the surrounding audio.

Reading (a) fits the code sequence the video is walking through and the presence of the
words "букву А" at all; reading (b) explains the missing number more economically. The
caption cannot distinguish them. **Unresolved** — it needs the audio or a frame of the
slide, and no worker in this video's record ever captured either. If a note needs the
letter-A example, it must be re-checked against the video before publication; otherwise
drop it and keep 32 and 33 only.

Note that the video itself defers the rest of this material at `00:08:24.630`–`00:08:27.430`
("Об этом тоже позже будет"), so keeping the example minimal costs the lesson nothing.