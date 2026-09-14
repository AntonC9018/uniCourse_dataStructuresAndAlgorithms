## When asked to maintain after edits

When edits are in, look at the latest revision hash in `revision.json`.
Create it if doesn't exist.
If didn't exist, run maintenance scripts on all labs.

If it did, see which files have changed, and run the maintenance scripts on those files.

The scripts are at `./scripts`.
If they aren't behaving like they should, fix them.


