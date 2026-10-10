# The worked example silently changes the player's y coordinate

## The board example

`00:02:02`–`00:02:09`: "этот враг находится в позиции 32. И игрок находится в позиции,
где каждая координата меньше, 1 то есть" — enemy at (3, 2), player at (1, 1). The
per-axis differences are then read off: X difference 2 (`00:02:19`), Y difference 1
(`00:02:24`), sum = 3 steps.

## The code example

`00:04:02`–`00:04:12`, the same positions written out as variables: "позиция икса
игрока … она у нас один … будет Y позиция игрока 3, будет X позиция врага 3 и Y позиция
врага будет два" — player (1, **3**), enemy (3, 2). Distance is still
`abs(1-3) + abs(3-2) = 3`.

## What changed and why it is invisible

The player's y moves from 1 to 3 with no remark. Both examples yield the same distance
3, so nothing in the narration calls attention to the substitution. The extraction
record contains both variants in different runs and never flags the change: run 477
(`ses_edd95c4e1ffelKnBxfFrxxdySf`) S-002 records "enemy at (3, 2) and a player at
(1, 1)", while run 477 S-004 records "the code sample places the player at X = 1,
Y = 3 and the enemy at X = 3, Y = 2".

The board arithmetic is then abandoned for a counterfactual, `00:02:37`–`00:02:51`:
"А что, если игрок был бы, например, больше позиция Y? Тогда здесь было бы больше
что-то три, да? … 3 - 1 - это было бы 2, 2 - 3 это было бы -1, и дистанция, это тогда
вышла бы один." That counterfactual moves the player to y = 3 — exactly the value the
code will use 90 seconds later — and the extraction run 477
(`ses_edd95c4e1ffelKnBxfFrxxdySf`) S-002 recorded it as the segment's `correction`
teaching point, phrased as if it described the current example rather than a
hypothetical.

## Consequence for a note

- A note showing both the board arithmetic and the code must not present them as the same
  diagram. Either state the player's y twice and say it changed, or pick one and say
  which one the code uses (the code uses y = 3).
- The failure case ("naive subtraction gives 1 instead of 3") is not reachable from
  player (1, 1); it needs the code's (1, 3). This is the trap a reader falls into when
  working the example by hand.
- The extraction ledger supports either reading, and no verifier ever reconciled them, so
  this is currently unresolved in the record.

## Related: what the run actually printed

`00:06:12`: "Вот 3,5. То, что мы ожидаем и здесь. Дистанция вот 1 2 3 и тут дистанция
1 2 3 4 5. То есть ответ правильный." The program prints `3` and `5` (enemy–player =
3, enemy–tree = 5). The "1 2 3" and "1 2 3 4 5" are the instructor counting cells on
screen, not output — the extraction run 478 (`ses_edd95c4b3ffe7C9rXws3Y9eW3a`) S-005
recorded the whole sentence as a `test_result`, which reads as though the program
printed the counting sequence.
