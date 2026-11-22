# The ledger merged three different identifier sets into one wrong one

The video uses three distinct name sets across the function-extraction part of the
lesson, and the extraction ledger collapsed them onto a single invented set
`xa / ya / xb / yb`. Any note written from the ledger alone gets the signature section
wrong.

## What the transcript says

The name sets, in the order the lesson introduces them:

- The full program's caller variables: `xPlayer`, `yPlayer`, `xEnemy`, `yEnemy`. The
  values are set at `00:04:02`–`00:04:12` (player x = 1, y = 3; enemy x = 3, y = 2), and
  the identifiers are named twice outright — `00:15:12`: "будете ссылаться не на X Player
  и Xemy, а на параметры", and `00:17:02`: "где у нас только есть X player, Y player,
  X enemy, Y enemy".
- The extracted function's parameters, `00:14:53`–`00:14:57`: "позиция X пер, позиция Y
  пер[вого], [позиция X] второго, позиция Y второго" — X of the first, Y of the first, X
  of the second, Y of the second. Confirmed by the argument-matching walkthrough at
  `00:16:00`–`00:16:09`: "X player идёт для параметра XA, Y player идёт для параметра Y[А],
  X enemy идёт для параметра XB, Y enemy идёт для параметра YB". Parameter names are
  therefore **XA, YA, XB, YB, in that order**.
- The reduced walkthrough example, `00:17:02`–`00:17:30`: the caller keeps the same
  `xPlayer`, `yPlayer`, `xEnemy`, `yEnemy` names with values 1, 3, 3, 2 ("int x player = 1 …
  вписываем три … вписывается три … вписывается два").
- After the struct refactor the parameters become `a` and `b` of type `Position`
  (`00:30:00`: "а — это будет имя, общее имя для этих двух ячеек"), accessed as `a.x`,
  `a.y`, `b.x`, `b.y` (`00:30:10`).

## What the extraction runs recorded

Run 480, session `ses_edd9542faffeNy0qbr2pt7GgFa`, segment S-013:

- "The distance function declares four parameters in the order **xa, xb, ya, yb**" —
  wrong order relative to the transcript, which is XA, YA, XB, YB.
- "Arguments are matched to parameters strictly by position, so **xa goes to the first
  parameter, ya to the second, xb to the third and yb to the fourth**" — this second
  point in the *same segment* gives the correct order and therefore contradicts the
  first. The pair cannot both be true; the transcript sides with the second.

Run 480 S-014/S-015/S-016 and run 482 (`ses_edd9542c0ffe4NPvYvg46Lwlx3`) S-017/S-018
then describe the reduced example's memory walkthrough entirely in terms of `xa`, `ya`,
`xb`, `yb` — "the first memory cell belongs to xa and the second to ya", "int xa = 1
allocates a cell for xa". Those are the caller variables, which the transcript calls
`xPlayer` and `yPlayer`. Run 482 S-017 compounds it: "the literal 1 becomes the value of
parameter x".

## Why it matters for a note

- The parameter *order* is the load-bearing detail of the whole "group coordinates into
  a struct" motivation. A note that says the parameters are `xa, xb, ya, yb` invites the
  reader to conclude the video itself is transposing axes before the struct refactor
  fixes it.
- The English note, when written, should present the caller variables and the parameters
  as different name sets (`xPlayer/yPlayer/xEnemy/yEnemy` vs `XA/YA/XB/YB`), because the
  video deliberately distinguishes "what the caller has" from "what the function
  receives" — the distinction the ledger erases.
- No verifier ran for this video, so this error is unexamined in the record and will
  survive into `teaching-points.json` if the ledger is merged as it stands.

## Caption hazard that produced it

The caption at `00:14:57` ends mid-list on "позиция Y пер" and the next cue resumes
"второго, позиция Y второго" — the "позиция X второго" phrase is missing from the caption
stream entirely, so a reader relying on the transcript can lose one parameter's position.
The same stream renders `X player` as `X layer` / `Xn` and `Y player` as `Yayр`, which is
how the identifiers came to look like bare letters.
