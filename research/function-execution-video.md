# How video 11 draws function execution (issue #91)

Primary source: `videos/cpp/11_C++_Базовые_техники_блоки,_функции,_структуры/internal/transcript.md`
on branch `origin/course-maintenance/20260929T222206Z-f69d5b84`
(YouTube: https://www.youtube.com/watch?v=6JtlzvwhHr0, Russian auto-captions, ~37 min).
The transcript is speech only. Every on-screen detail below that is not explicitly
named by the lecturer is marked **(inferred)**. Secondary sources consulted for this
question: the transcripts of video 04 (Z8AFpeE7hOo) and video 09 (859Y0Q8pyLg).
No screenshots, frames, or stills of any of these videos exist anywhere on the branch
(verified with `git ls-tree -r` + grep for png/jpg/jpeg/webp/gif/bmp: 14 image files
in the repo, all in `en/`/`ru/` labs, none under `videos/`).

## Short answer

The video's central segment (17:02–23:06, repeated with structs at 26:52–31:35) walks
through one call — `distance(xPlayer, yPlayer, xEnemy, yEnemy)` — as a sequence of
memory **cells** ("ячейки") in what the lecturer calls *temporary memory*:

1. Caller's locals are allocated and filled cell by cell.
2. A cell for the call's result is allocated **first**, still empty ("some garbage").
3. Arguments are evaluated as expressions: each variable name is "converted" into a
   read of its cell.
4. Cells for each parameter are allocated **in parameter order**, empty at first.
5. Argument values are written into the parameter cells **by position** (copy).
6. Execution "moves to the first line" of the function; body locals get their own
   cells as their declaration lines execute.
7. `return` first evaluates its expression, the value is "saved, remembered", and
   the whole call expression is *replaced by* that value at the call site.
8. Only then are all locals of the call (parameters and body locals) "erased" — and
   the lecturer immediately adds the honest footnote: in reality the values stay in
   memory; only the names/ability to refer to them disappear.
9. The returned value lands in the target variable.

There are no stack frames as objects, no return address, no base pointer, no stack
pointer anywhere in the video: the word "стек" appears exactly once, in a garbled
caption (6:42), and is never developed. The entire mechanism is name-based cells,
positional argument copying, and textual substitution of the call by the return
value. Details the prototype must not invent: frame layout, register use, and how
the CPU finds its way back are simply not modelled.

## Timestamped walk-through of the function/stack segment

Setup before the segment: `main` declares `xPlayer = 1`, `yPlayer = 3`,
`xEnemy = 3`, `yEnemy = 2`; a `distance` function with parameters `xa, ya, xb, yb`,
locals `xd`, `yd`, and `return xd + yd;` is called as
`disPlayerEnemy = distance(xPlayer, yPlayer, xEnemy, yEnemy)` (the player's y is 3
here even though the earlier board example used y = 1 — see the repo's existing
research note `board-example-drifts-from-code-example.md`; the distance is 3 either way).

### Caller locals and the result cell

- [17:02](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1022s) — the lecturer switches to
  a "более простом примере" (a simpler example) with only the four player/enemy
  coordinates, and starts enumerating cells: "первая ячейка памяти у нас будет под Xра.
  Вторая ячейка памяти будет под Y" (the first memory cell will be for xPlayer, the
  second for yPlayer). The diagram is a row of named cells — **(inferred layout)**.
- [17:19](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1039s) — each declaration is
  executed one at a time: "int x player = 1. Выделится ячейка под xплеера и туда впишем
  один" (a cell for xPlayer is allocated and 1 is written in), then 3, 3, 2 for
  yPlayer, xEnemy, yEnemy. Allocation and initialization are two separate steps, and
  the value is written immediately after allocation.
- [17:33](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1053s) — the assignment line with
  the call: "В первую очередь выделяется ячейка под вывод. Покаместь без значений…
  по сути там будет какой-то мусор" (first a cell for the output is allocated, for now
  without a value… in essence there will be some garbage there). The result cell
  comes **before** anything else on that line, and it is explicitly uninitialized.
- [17:49](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1069s) — "Далее в эту ячейку
  вписывается результат вот этого выражения" (then the result of this expression is
  written into that cell). So the order on the line is: result cell → evaluate → write.

### Argument evaluation

- [17:59](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1079s) — "чтобы вычислить
  результат этого выражения, нам нужно вызвать функцию distance. А чтобы вызвать
  функцию distance, мы должны знать значение каждого из аргументов" (to compute the
  expression we must call distance; to call it we must know the value of each
  argument).
- [18:06](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1086s) — argument names are
  treated as expressions: "они конвертируются в то, что в них находится. То есть
  X player у нас конвертируется в считывание как бы из ячейки … то есть в единицу"
  (they convert into what is inside them; xPlayer converts into a read of its cell,
  i.e. into 1). Each of the four arguments becomes a value: 1, 3, 3, 2.
- [18:38](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1118s) — "оно как бы временно
  сохраняется процессором" (it is temporarily saved by the processor, as it were).
  Where those temporaries live is not said — no cell is drawn for them as far as the
  speech reveals. (inferred: a scratch area outside the drawn cells.)
- [18:45](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1125s) — "эти аргументы
  передадутся, эти значения для параметров попадут в дальнейшие локальные перемены"
  (these arguments will be passed; these values for the parameters will land in the
  upcoming local variables).

### Parameter cells and positional copy

- [18:52](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1132s) — "Смотрите, далее идёт
  вызов функции distance. При вызове функции distance первое, что происходит - это
  выделяются ячейки памяти под каждый из параметров" (at the call, the first thing
  that happens is that memory cells are allocated for each of the parameters).
- [19:03](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1143s) — allocation is in
  declaration order and valueless: "в том же порядке выделится ячейка памяти под xa,
  пока [без значений], … потом под ya, потом под xb и под yb".
- [19:17](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1157s) — "Выделили ячейки и
  далее по позициям эти ячейки получают изначальные значения. xa находится в первой
  позиции, поэтому он получит вот это первое значение, единицу. Значит, единица
  пишется сюда" (the cells are allocated and then, by position, get their initial
  values; xa is in the first position, so it gets the first value, 1; the 1 is
  written here). Matching is purely positional, first-to-first.
- [19:34](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1174s) — copy semantics made
  explicit: "Эту единицу мы перекопировали из переменной Xlayer… Xlayer как бы
  заменилась на эту единицу и потом эта единица попала в локальную переменную,
  которая существует на момент вызова этой функции" (we copied this 1 over from
  xPlayer; xPlayer was, as it were, replaced by the 1, and the 1 landed in a local
  variable that exists at the moment of the call). The parameter is described as a
  genuine local variable, not a reference.
- [19:51](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1191s) –
  [20:17](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1217s) — the remaining values
  walk into their slots in order: "три идёт во вторую позицию… три идёт в третью
  позицию XB… эта двойка идёт сюда YB" (3 goes to the second position [ya], 3 to the
  third [xb], the 2 to yb).

### Body execution and return

- [20:17](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1217s) — "И теперь выполнение
  переходит на первую строчку из функции distance" (now execution moves to the first
  line of the function). No return address is mentioned; the transfer is described
  only as execution moving.
- [20:26](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1226s) — "функция distance, она
  теперь уже работает с вот этими локальными переменнами. Выполняется код из
  distance… точно так же, как до этого" (the function now works with these local
  variables; its code executes just like before): reads of `xa` give 1, of `xb` give 3,
  etc.
- [20:45](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1245s) — body locals get cells
  too, on execution of their lines: "Это тоже локальные переменные. Для них тоже
  выделятся ячейки при выполнении этого кода. Выделится ячейка для XD. Она получит
  результат этого выражения" (these are also local variables; cells are also allocated
  for them when this code executes; a cell for xd is allocated and gets the result of
  the expression — 2; the same for yd — 1, at
  [21:04](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1264s)).
- [21:11](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1271s) — "Теперь переходим на
  строчку Return. Что делает Return? Return работает с выражениями. Опять он сначала
  вычисляет, чему равно это выражение" (now we come to the return line; return works
  with expressions; again it first evaluates the expression): reads `xd` and `yd`,
  "получает 2 и 1, 2 и 1 складывает и это будет три" (gets 2 and 1, adds them: 3,
  at [21:30](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1290s)).

### Substitution and teardown

- [21:35](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1295s) — "во время выполнения
  программы это как бы заменится на три" (during program execution this [the return
  expression] is, as it were, replaced by 3).
- [21:39](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1299s) — "Эта тройка идёт как бы
  на место вызова дистан" (this 3 goes, as it were, to the place of the distance call).
- [21:44](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1304s) — the substitution rule:
  "весь этот дистанс с параметрами как бы заменяется на то, что вы пропишете после
  [return]" (the whole `distance(...)` with its parameters is, as it were, replaced by
  whatever you write after return).
- [21:58](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1318s) — order of the two final
  steps: "Это всё заменяется на три, то есть оно как бы сохраняется, запоминается, и
  после этого стираются все локальные переменные, созданные для этого вызова дистан"
  (all of this is replaced by 3 — it is saved, remembered — and only after that all
  local variables created for this distance call are erased). "Вот эти две стираются
  [xd, yd] и также стираются все переменные, созданные для параметров… Они перестают
  существовать" (these two are erased, and also all variables created for the
  parameters; they cease to exist).
- [22:26](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1346s) — the honest footnote:
  "По факту, как это происходит? По факту их значения остаются в памяти. Во временной
  памяти они остаются, пропадают только лишь возможность к ним обратиться. Эти имена
  как бы пропадают, а значения остаются" (in fact their values remain in memory, in
  temporary memory; only the ability to refer to them disappears — the names
  disappear, the values remain). This is the closest the video comes to describing
  stack teardown without a stack: it is name availability that dies, not data.
- [22:45](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1365s) –
  [23:04](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1384s) — completion: "эта тройка…
  она идёт на место дис [distance]… идёт dis player enemy = 3… И этот три попадает в
  соответствующую переменную. Вот таким образом выполняется этот код" (the 3 goes to
  the place of the distance call; `disPlayerEnemy = 3`; and the 3 lands in the
  corresponding variable).
- [23:10](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1390s) — a caution drawn from
  the same positional model: parameters must be passed in exactly this order, and
  swapping them "не будет ошибкой" for the compiler — which motivates grouping X and Y
  into a struct (the rest of the video).

### Second pass with struct parameters (26:52–31:35)

The same walk is repeated after introducing `struct Position { int x; int y; }` and
`Position distance(Position a, Position b)`:

- [28:53](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1733s) — "Вызов функции. Снова
  же я объяснял. Сначала выделяется ячейка для выхода. Выделяется ячейка. Ячейка будет
  типа [int]. Это будет одно число" (again: first a cell for the output is allocated;
  the cell is of the return type — one number, not a Position). Here the result cell
  is described *before* argument evaluation, confirming the 17:33 ordering. **Note the
  mild inconsistency with the first pass**, where the result cell was introduced only
  when the assignment line was reached; in both tellings it precedes everything else
  on the line.
- [29:14](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1754s) — the argument `player`
  "заменится на то, что в данный момент в плеере. В данный момент в плеере 1,3. 1,3.
  как одно целое" (is replaced by what is currently in player — 1,3 — as one whole);
  and a generalisation: "Значение не обязательно числовое может быть. Может быть и как
  структура" (a value need not be numeric; it can be a structure,
  [29:30](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1770s)).
- [29:39](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1779s) — "Перед тем, как они
  передаются, мы выделяем ячейки для них. Ячейки для параметров" (before they are
  passed, we allocate cells for them — cells for the parameters). A parameter of type
  Position is two cells, X and Y, with `a` as "имя, общее имя для этих двух ячеек
  вместе" (a common name for the two cells together,
  [29:57](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1797s)).
- [30:28](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1828s) — "13 встаёт как бы в
  ячейку первой позиции и 32 встаёт в ячейку второй позиции… Мы копируем, как бы
  копируем значение полей с изначальной позиции… X будет 1, Y будет 3. Они по очереди
  скопируют" (the pair 1,3 lands in the first parameter's cells, 3,2 in the second;
  field values are copied from the original, one after another).
- [31:08](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1868s) — the identical ending,
  compressed: "Снова же две эти перемены создаются. Xдист Yди… В них пишется временные
  результаты. Потом вычисляется выражение вот это возвращаемое, это будет три. И после
  этого стираются все переменные вот эти. И на место вызова функции у вас как бы идёт
  то, что вы вернули из неё. А вы вернули три, и это три попадает в переменную"
  (xd and yd are created again, temporary results are written into them, the returned
  expression evaluates to 3, then all these variables are erased, and what you
  returned goes to the place of the call and into the variable).

### Earlier scaffolding the segment leans on

- [6:42](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=402s) — the only occurrence of
  the word "stack" in the whole transcript, in a garbled caption: "эти переменные во
  временную память идут и эти тоже во временную память, временную стек по-другому"
  (these variables go into temporary memory, and these also into temporary memory,
  temporary stack, differently). It is never expanded on; the operative term
  throughout is "временная память" (temporary memory).
- [8:54](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=534s) –
  [9:24](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=564s) — the same model applied to
  the standard-library call `abs(...)`: "Внешнее выражение - это вызов функции apps.
  Она зависит от значения параметра. Значит, вычисляем значение параметра… И этот
  ответ передаётся функции AS… И эта единица уже впишется в память" (the outer
  expression is a call of abs; it depends on the value of its parameter; the answer is
  passed to abs; and this one is written into memory). Standard function, same
  copy-in/write-out mechanics.
- [15:24](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=924s) — meaning of the `int`
  in front of the function name: "Он указывает, что вызов этой функции можно
  использовать в качестве выражений и что результат будет вот этот" (it says that a
  call of this function can be used as an expression and that the result will be of
  this type).
- [16:14](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=974s) — parameters are locals:
  "вот эти вот параметры для них на самом деле выделяются локальные переменные. И то,
  что вы передаёте здесь - это всего лишь изначальное значение этих локальных
  элементов" (for these parameters local variables are actually allocated; what you
  pass here is only the initial value of these local variables).

## Frames, parameters, locals

- A "frame" is never named and never drawn as a bounded object — at least, nothing in
  the speech suggests a box around the call's cells. What exists is a flat pool of
  named cells in "temporary memory": caller locals, one result cell, parameter cells,
  body-local cells. **(inferred: they are likely drawn in the same cell-row style as
  the caller's locals, since the lecturer says allocation "in the same order"
  continues and nothing suggests a separate region.)**
- Parameters are locals, full stop ([16:14](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=974s)):
  allocated at call time, valueless first, then initialized **by position** from the
  argument values ([19:03](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1143s),
  [19:17](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1157s)). Copying is explicit
  ("перекопировали", [19:34](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1174s)); for
  structs, field by field, "по очереди"
  ([30:45](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1845s)).
- Body locals are allocated later, at the moment their declaration lines execute
  ([20:45](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1245s)), not together with the
  parameter cells. A fresh uninitialized cell contains "какой-то мусор"
  ([17:40](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1060s)) — the video does show
  garbage in freshly allocated cells, which the prototype should reproduce.
- Names are the only handle: two calls of the same function produce independent cells
  (the whole point of parameter locals), and after teardown the names are gone but
  values linger ([22:26](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1346s)).

## Return value

- The return-value cell ("ячейка для выхода" / "ячейка под вывод") is allocated first
  on the calling line, before arguments are touched, and holds garbage until filled
  ([17:33](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1053s),
  [28:53](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1733s)). Its type is the
  function's return type: "Ячейка будет типа [int]. Это будет одно число" — for a
  Position-returning function it would be a Position-shaped cell.
- `return` first evaluates its expression like any expression: reads of the local
  cells, then the addition ([21:11](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1271s)).
- The value then "сохраняется, запоминается" (is saved, remembered) and the *entire
  call expression, parameters included*, is replaced by it at the call site
  ([21:58](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1318s)). The transport
  mechanism is deliberately vague ("как бы" recurs); no register, no cell, no channel
  is named for the journey from `return` to the call site. **(inferred: on the board
  the 3 is probably just written onto/next to the call site.)**
- Finally the value "попадает в соответствующую переменную" (lands in the
  corresponding variable) — for the example, into `disPlayerEnemy`
  ([23:01](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1381s)).
- `void` is explained later
  ([33:36](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=2016s)): no output → no result;
  "Void означает, что функция просто что-то делает… процедуры" — a procedure that
  affects memory/console but produces no result value.

## Return addresses, base and stack pointers

- **Return address: never mentioned.** The closest statement anywhere in the three
  transcripts is in video 04
  ([5:54](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=354s)): when the function's
  instruction list is exhausted, "процессор перепрыгнет обратно на то место, где эта
  функция была вызвана в последний раз" (the processor jumps back to where the
  function was last called) — an unconditional jump back to the call site, with no
  mechanism named for remembering it. Video 04 also says a call itself is an
  instruction the processor understands
  ([6:58](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=418s)) and demonstrates nested
  calls (main → B → F, returning up the chain,
  [7:05](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=425s)), but still without any
  saved address.
- **Base pointer (EBP/RBP/frame pointer): never mentioned** in video 11, 04, or 09.
- **Stack pointer (ESP/RSP): never mentioned.** The word "стек" occurs once in video
  11 ([6:42](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=402s), garbled caption) and
  not at all as a mechanism. The lecturer's operational term is "временная память"
  (temporary memory).
- The teardown story replaces all of this: variables "стираются… перестают
  существовать", qualified immediately by "по факту их значения остаются в памяти…
  пропадают только лишь возможность к ним обратиться"
  ([22:26](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1346s)). Nothing is popped;
  availability is revoked. A prototype that animates a stack pointer moving or a
  return address being pushed would be *inventing* content this video does not have.

## Order of events during a call and a return

Consolidated, as the lecturer states it (simple-int version, then struct version
matches step for step):

1. Caller's statement line is reached; the result cell for the call is allocated
   first, uninitialized (garbage).
2. Arguments are evaluated: variable names become reads of their cells; values are
   (somehow) temporarily held by the processor.
3. Parameter cells are allocated, in declaration order, empty.
4. Argument values are written into parameter cells by position (copied).
5. Execution moves to the first statement of the function body.
6. Body locals get cells as their declaration lines execute; expressions evaluate
   from cell reads as usual.
7. `return`: its expression is evaluated; the result is "saved, remembered".
8. The whole call expression (with arguments) is replaced by the returned value at
   the call site.
9. All locals of the call — body locals and parameter locals — are erased (names
   gone; values factually remain in memory).
10. The returned value is written into the target variable (if the call is used in
    an assignment/initialization).

The one ordering subtlety worth honoring in a prototype: substitution of the call by
the return value happens **before** the erase step ("оно как бы сохраняется,
запоминается, и после этого стираются…"), so the returned value must not be drawn as
dying with the frame.

## Terminology the lecturer uses (Russian → English)

- ячейка (памяти) — (memory) cell; the universal unit of the model
- выделить ячейку — to allocate a cell
- временная память — temporary memory (his stand-in for the stack region)
- локальная переменная — local variable
- параметр / аргумент — parameter / argument; "передать по позициям" — to pass by
  position
- перекопировать (значение) — to copy (a value) over
- впишем / впишется в память — (it) will be written into memory
- считывание (из ячейки) — reading (from a cell)
- мусор — garbage (uninitialized cell contents)
- ячейка для выхода / под вывод — the cell for the output (return-value cell)
- вызов функции / место вызова — function call / call site ("на место вызова дистан")
- стираются, перестают существовать — are erased, cease to exist
- имена пропадают, значения остаются — the names disappear, the values remain
- интерфейс функции, вывод, входные данные — function interface, output (return
  value), inputs
- стек — stack (once, garbled, never developed)
- перепрыгнет — (the processor) will jump (video 04's wording for call/return control
  flow)

## What the transcript cannot tell us

Everything below is invisible to this source; a prototype must decide these itself
and must not cite the video for them:

- **The exact on-screen layout.** We know cells exist and are named, but not whether
  call cells are drawn as a contiguous block, a separate table, or appended to the
  caller's row. Nothing in the speech distinguishes a "frame" visually.
- **Where argument temporaries live** while "временно сохраняется процессором"
  (18:38). No cell is spoken for them.
- **How the return value physically travels** from the `return` statement to the
  call site. "Сохраняется, запоминается" names no location.
- **Direction of growth / relative position** of the call's cells versus the
  caller's — never verbalized.
- **Any control-flow memory.** How the CPU returns, whether the return address is
  drawn, what `main`'s frame looks like — all absent.
- **Nested calls within the walk-through.** The `distance` example contains none;
  only video 04 shows nesting (main → B → F), and only as instruction jumping.
- **Recursion.** Not touched in this video (it appears in lab exercises, see below).

## How the lab text lines up

Repo layout: `en/labs/cpp/` and `ru/labs/cpp/` are parallel file-for-file translations
(same 37 numbered labs plus `test1.md`). Two labs are relevant:

- **`06_function.md` / `06_function.md` (ru)** — links to exactly this video
  (6JtlzvwhHr0) and its written answers mirror the video's model almost beat for
  beat: parameters get "a local variable … allocated" at call time with argument
  values "*copied* into these variables" from "the corresponding call positions";
  on return the local "ceases to exist — that is, its memory can no longer be
  referenced — however, the value 6 continues to remain in that memory location"
  (Q1 answer), which is precisely the video's "имена пропадают, значения остаются"
  ([22:26](https://www.youtube.com/watch?v=6JtlzvwhHr0&t=1346s)). Example 15's answer
  even enumerates the call in the video's order (locals created for parameters →
  argument value stored → "execution moves to the first statement" → `return` makes
  the expression's result the call's result → "all local variables created during
  the call disappear"). The labs call the region "temporary memory (the stack)" —
  the written text quietly attaches the standard name the video never uses.
- **`30_function_execution.md` / `30_function_execution.md` (ru)** — "Function
  Execution and the Stack". Its accompanying videos are different (jTRJM_gmhU4), and
  this is where everything the video 11 segment omits is taught explicitly: stack
  pointer, return address occupying 4 bytes, an ASCII stack table showing `x (1) |
  return address to 'return 0;' in main | ??`, overwriting `sp - 8`/`sp - 4`, stack
  corruption, infinite recursion and stack overflow. In other words, the lab
  supplies the frame/return-address/stack-pointer story the video deliberately stays
  silent about — so a prototype based on the video is complementary to, not a
  duplicate of, lab 30's mental model. Lab 30 also carries an explicit caveat that
  its stack layout is "a conceptual simplification" left to the implementation,
  which is consistent with the video refusing to model it at all.

One reconciliation note for the prototype: the video says the parameter and
body-local cells are *erased*, while both labs (and the video's own footnote at
22:26) agree the *values* persist and only name-availability is lost. The safest
visualization is to fade/lock the cells (names greyed out) rather than to blank them.
