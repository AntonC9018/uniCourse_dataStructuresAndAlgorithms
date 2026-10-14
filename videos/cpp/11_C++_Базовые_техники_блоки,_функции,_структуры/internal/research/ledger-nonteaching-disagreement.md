# Where the two ledger workers' calls on non-teaching material disagree

## Coverage verdict first

The segment-accounting run (`ses_edd948d82ffeRVAPp71blEUy5a`) accounts for all 1587 cues
of `internal/transcript.md` with no gap. Its segment plan runs S-001 `[0, 60)` through
S-030 `[1566, 1587)`, and the final exclusive bound matches the transcript's cue count
exactly. Overlapping boundary cues are counted in each segment that contains them, as the
worker was instructed to do: 174 cues appear in two segments' ranges.

Structured accounting totals: 1569 `teaching` cues, 11 `repetition`, 4 `wait`, and 3 `caption_noise`. The corresponding category ranges are separate from cue totals; do not infer range counts from these cue counts.

## The disagreements

The extraction runs flagged 14 non-teaching spans via their `nonTeaching` observations:
5 spans contain no cue at all (they fall inside caption gaps or are zero length), 5 were
honoured at least in part by the accounting, and 4 were overruled outright.

| cues | extraction call | accounting call | verdict against the transcript |
| --- | --- | --- | --- |
| 1085–1086 | `wait` (run 481 S-021) | `teaching` | **extraction wrong** — cues carry "Давайте теперь то же самое сделаем", real content |
| 1381–1382 | `navigation` (run 484 S-026) | `teaching` | **extraction wrong** — cues carry "ещё хотел показать, например, если бы у нас вот такой был код" |
| 1567–1570 | `caption_noise` (run 483 S-030) | `teaching` | **accounting wrong** — cue 1567 is an empty caption line |
| 1583 | `caption_noise` (run 483 S-030) | `teaching` | **accounting wrong** — cue 1583 is an empty caption line |
| 329 | `caption_noise` (run 478 S-006) | `caption_noise` | agreed; cue 329 is the truncated fragment "вот этого вот" |
| 1188–1192 | `repetition` (run 479 S-023) | `repetition` | agreed; verbatim repeat of S-022's point |
| 1242–1248 | `repetition` (run 484 S-024) | `repetition` | agreed; repeat of the x=1/y=3 overwrite |
| 864 | `caption_noise` (run 482 S-017) | `caption_noise` | agreed |
| 464 | `wait` (run 479 S-009) | `wait` | agreed |

The remaining 5 spans mark material the caption stream does not contain a cue for, so the
accounting worker could neither honour nor reject them:

- `397.400`–`397.400`, zero length at cue 276's start (run 478 S-005) — an empty
  interval, so it covers no cue.
- `1608.630`–`1609.300` (run 481 S-022) — the caption gap `00:26:46.679`–`00:26:50.310`.
- `1814.410`–`1814.910` (run 482 S-025) — the gap `00:30:12.600`–`00:30:15.190`.
- `2101.400`–`2101.960` and `2138.390`–`2138.990` (run 483 S-029) — the gaps
  `00:35:01.119`–`00:35:03.550` and `00:35:37.160`–`00:35:40.109`.

## Consequence for a note

- If the ledger is merged into `internal/teaching-points.json` as it stands, the two empty caption cues that the extraction marked as noise were counted as teaching by the accounting result. This is a two-cue classification difference, and it means the committed ledger's coverage claim ("every cue accounted") overstates what is actually
  teachable.
- The `nonTeaching` markers are unreliable in *both* directions; a fixer or verifier should
  re-derive dispositions from the cue text rather than trust either worker's label.
- Nothing in the record reconciles the two workers, and neither ran under a review gate
  that would have — the `factual_verification` order for this video has no runs at all.
