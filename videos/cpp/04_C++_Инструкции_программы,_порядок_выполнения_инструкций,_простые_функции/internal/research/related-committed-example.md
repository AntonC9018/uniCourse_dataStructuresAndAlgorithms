# The only committed function example is related evidence, not the recording's program

## What exists in the repository

`en/05_programming_fundamentals/function_example_1/main.cpp` is the only committed C++ source in this
repository that models function calls. Run 505 read it at pinned commit
`83e6302c9a3af2c28f3a17539cbdff6d63159ec8` ("Lab 3", 2023-10-03), blob `6f2ed59c…`, ancestor of HEAD.

Its actual content, read back while recreating this file on 2026-10-10 (fresh check, not a worker finding):

```cpp
void a()
{
    int i = 5;
    i = i + 5;
    // return;
}

void b()
{
    a();
    return;
}

int main()
{
    b();
    return 0;
}
```

with hand-written comments describing stack allocation, saving the return address, and jumping to the
first instruction.

## Why it cannot stand in for the video's program

Three mismatches, all material:

- **Call graph is inverted in naming.** The commit has `main → b → a`; the video has `main → B → f`. The
  note says so explicitly at line 255: "That source uses `main → b → a` and arithmetic".
- **The bodies are arithmetic, not output.** `a` computes `i = 5; i = i + 5;`. It prints nothing. The
  video's `f` prints four statements.
- **The commit is a lab artifact.** Subject "Lab 3". The authoring contract's own rule — a commit that
  merely adds an exercise is not evidence for a taught code state — applies.

So run 505 cited it under the label "**related evidence, not the exact greeting program**" and reprinted a
shortened sample of the *reconstruction* beside it. That labelling is correct and must stay.

## The corollary: the code-history trail is timestamps only

Because no commit in this repository preserves the video's intermediate programs, run 505 could not build
a commit-backed history for them. The note's closing section, "Code history trail", says so in its first
line and then lists seven YouTube timestamps instead.

Checked 2026-10-10 (fresh, not a worker finding): the greeting program does not exist anywhere in the
repository's history.

- `git log --all -S'Anton' -- '*.cpp'` — no commits.
- `git grep -l 'Anton' -- '*.cpp'` — no files.
- At the authoring-time revision, `git grep -ln 'Hello World'` was used to distinguish committed source from prose. Current HEAD also contains this reconstructed research, so do not reuse a whole-checkout search result as a current inventory. Never a `.cpp`.

This is the correct outcome, not a gap to fill. Do not manufacture a citation for the greeting program.
