## When asked to maintain after edits

When edits are in, look at the latest revision hash in `revision.json`.
Create it if doesn't exist.

Maintenance scripts don't handle translations, 
translate into the languages that have been missed by the update.

When translating, try to match the style of the original and keep things sounding natural,
the translation should not feel mechanical.
Do up to 5 rounds of reviews of the translation in fresh subagents,
spotting unnatural sounding constructions, and fix those with subagents.
Only work on the diffs, reading the context around the diffs if needed.

If the revision json didn't exist, run maintenance on all labs.
If it did, see which files have changed, and run maintenance on those files.

Maintenance is handled by the `course_maintenance` submodule
(upstream: https://github.com/AntonC9018/course_maintenance —
not to be confused with `course_management`).
Follow `course_maintenance/AGENTS.md` for the full workflow. Quick version:
- `python3 course_maintenance/maintain.py --check <paths>` — preview
- `python3 course_maintenance/maintain.py <paths>` — apply
- file args never trigger renames; dir args (default `.`) do.

Commit once you're done.

## When asked to add an example to a lab or edit one

Insert the examples at their logical position in the document.
Disregard the fact that they'd have a duplicate number, 
that's going to be handled by the maintenance scripts.
Match the style in the target document, or the other documents 
(first few documents have most care put into them).


