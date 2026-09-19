# GitHub Pages deployment (issue #15)

Thin course-owned side of CI-1..CI-12. Shared validation, renderer pins,
and the stable command live in `course_maintenance`; this repo owns only
`.github/workflows/course-site.yml`, `scripts/smoke-test.sh`,
`scripts/verify-pages-settings.sh`, `course-publishing.json`, Markdown
sources, and the `course_maintenance` submodule pointer.

## How it works

1. **Validate** (PRs targeting `master` + pushes to `master`): checks out
   the course with `submodules: recursive` at the committed
   `course_maintenance` revision, sets up Python 3.12 + Node 22, restores
   npm/Playwright caches, runs `npm ci` + `playwright install chromium`,
   then runs one shared command:
   `python3 course_maintenance/publish.py ci --course-repo . --out $RUNNER_TEMP/site-out`.
   In order: maintain check, publishing check, compatibility suite, full
   site build to `$RUNNER_TEMP/site-out` (`dist/` below). Read-only wrt
   sources; any failure fails the required check.
2. **Upload** (pushes to `master` only, same job after a green build):
   `actions/upload-pages-artifact` publishes `$RUNNER_TEMP/site-out/dist`
   — the exact validated build, not a rebuild.
3. **Deploy** (pushes to `master`, `needs: validate`): official
   `actions/deploy-pages` through the `github-pages` environment.
   PRs never upload or deploy; failed validation never reaches deploy, so
   the previously published site stays live (no auto-rollback).
4. **Smoke** (after deploy): `scripts/smoke-test.sh` with bounded retry
   against `https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/`.

`peer_repositories` stays `[]`; no peer checkout exists in CI (CI-7).

## Triggers

`pull_request` (`branches: [master]`) + `push` (`branches: [master]`),
no path filters. Feature-branch pushes without a PR do not run (CI-4).
Every revision validates completely; CI never writes source metadata.

## Permissions

Top-level `contents: read`. Only the `deploy` job escalates to
`pages: write` + `id-token: write`, and only for successful master builds
(CI-9). PR validation cannot write Pages or deploy content.

## Concurrency

```yaml
concurrency:
  group: course-site-${{ github.ref }}
  cancel-in-progress: true
```

A newer push on the same ref cancels the still-running older run, so an
older master revision can never upload/deploy after a newer one, and
superseded PR runs are discarded (CI-10).

## Pins and caches

Third-party actions are pinned to immutable SHAs (CI-8):

| Action | Version | SHA |
| --- | --- | --- |
| actions/checkout | v6 | `d23441a48e516b6c34aea4fa41551a30e30af803` |
| actions/setup-python | v6 | `ece7cb06caefa5fff74198d8649806c4678c61a1` |
| actions/setup-node | v6 | `249970729cb0ef3589644e2896645e5dc5ba9c38` |
| actions/cache | v5.1.0 | `caa296126883cff596d87d8935842f9db880ef25` |
| actions/configure-pages | v6.0.0 | `45bfe0192ca1faeb007ade9deae92b16b8254a0d` |
| actions/upload-pages-artifact | v5.0.0 | `fc324d3547104276b827a68afc52ff2a11cc49c9` |
| actions/deploy-pages | v5.0.1 | `368f82528645a54fb793d4d04e342629a3f51346` |

Runtimes: Python 3.12, Node 22 (match `publishing/ci.py`
`PINNED_PYTHON`/`PINNED_NODE` of the checked-out submodule revision).
Browsers: Playwright 1.48.2 + Chromium 130.0.6723.19 (match
`publishing/site.py` `PINNED_VERSIONS`/`PINNED_BROWSERS`).
Renderer: exact `renderer/package.json` + committed
`renderer/package-lock.json` of the submodule revision.

Cache keys (same as #14, safe against stale substitution):

- npm: `setup-node` cache with
  `cache-dependency-path: course_maintenance/renderer/package-lock.json`;
- browsers: `playwright-1.48.2-chromium-130.0.6723.19-${{ hashFiles('course_maintenance/renderer/package-lock.json') }}`.

Caches hold runtimes/dependencies only — never metadata, projections, or
deployable output.

## Submodule discipline (CI-6)

Real CI checks out `course_maintenance` via `submodules: recursive`: the
SHA pinned by this repo's gitlink is the only shared revision used. No
workflow fetches floating maintenance or a reusable workflow revision. A
shared-tooling change affects this course only after a commit updating the
`course_maintenance` pointer, which CI then validates before any deploy.

Local validation uses an explicit maintenance checkout instead (the local
`course_maintenance` path is an uninitialized gitlink in some clones):

```sh
python3 /tmp/opencode/worktrees/issue-15/publish.py ci \
  --course-repo /tmp/opencode/worktrees/course-15
```

## Smoke tests (CI-11)

```sh
BASE_URL=https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms \
  bash scripts/smoke-test.sh
```

Bounded retry (`SMOKE_RETRIES=30`, `SMOKE_SLEEP_S=10` by default). Checks:

- `/` references `/en/common/labs/computer-architecture/` (root redirect);
- `/en/common/labs/computer-architecture/` serves "Computer Architecture";
- `/ru/common/labs/computer-architecture/` serves "Архитектура компьютера";
- representative EN page references `pagefind` + `pagefind/pagefind.js`
  (fallback `_pagefind/pagefind.js`) is reachable (search);
- `/en/dsa/labs/graphs/` embeds `mermaid-static` (no client JS);
- `/mermaid/en-dsa-labs-graphs-0.svg` serves `<svg`;
- `/assets/AntonC9018/uniCourse_dataStructuresAndAlgorithms/en/04_compiler_and_ide/cpp_extension.png`
  returns 200 (copied asset).

## Manual settings checklist (CI-12, not automatable via repo files)

GitHub settings cannot be applied from the repository; a maintainer must
confirm them once in the web UI (or via `gh`), then re-verify with
`scripts/verify-pages-settings.sh`:

- [ ] Settings > Pages > Build and deployment > Source: **GitHub Actions**.
- [ ] Settings > Branches > `master` protection:
  - [ ] Require status checks: **`course-site / validate`** (exact name).
  - [ ] Do **not** require pull requests (changes may land via direct
        `master` commits; PRs stay optional).
  - [ ] Admin bypass **on** (administrators can push to `master`).
- [ ] Actions > `course-site` runs: a valid PR shows a green `validate`
  check; a broken link / stale metadata / build failure shows a red
  required check; PR runs never upload or deploy.
- [ ] Push/merge to `master` republishes the exact revision; the
  `github-pages` environment shows the deployment + URL.
- [ ] Post-deploy `smoke` job green at the public URL above.
- [ ] `gh` verification (read-only; prints the checklist and exits 0 when
      offline instead of failing):

```sh
bash scripts/verify-pages-settings.sh
```

## Acceptance mapping

- Valid PR → green full-build `validate` check; broken/stale/failing
  content → red required check; PR has no Pages write perms.
- Direct `master` commit/merge → validates, uploads, and deploys that
  exact revision; failed validation deploys nothing.
- Concurrent runs: older cannot win (concurrency above).
- Shared updates land only via submodule-pointer commits.
