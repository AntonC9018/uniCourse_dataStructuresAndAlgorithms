# GitHub Pages deployment

`course-publishing.json` owns this course's document selection, CI policy,
navigation, deployment expectations, and post-deploy probes. Reusable code
lives in the pinned `course_maintenance` submodule. See
`course_maintenance/docs/course-configuration.md` for configuration fields.

`.github/workflows/course-site.yml` validates pull requests and branch
pushes through the shared composite action, uploads the exact successful
build, deploys it through the `github-pages` environment, then runs shared
smoke probes. PRs do not deploy. Validation is read-only and cancels
superseded runs. The `ci.required_pr_label` setting controls PR readiness;
workflow branch triggers match `deployment.branch`.

Course CI checks documents and builds the course site. Shared-tooling
unit and compatibility tests run in the shared repo's CI; this course
sets `ci.run_compatibility_tests` to `false`.

```sh
python3 course_maintenance/publish.py ci --course-repo . --out /tmp/course-site
python3 course_maintenance/publish.py smoke check --course-repo .
python3 course_maintenance/publish.py pages verify --course-repo . --strict
```

For a local built-site smoke check, pass `--base-url` with the local
server URL and project base path. Probe retry limits, route text, Mermaid
and asset checks are defined in this course's JSON. Root routes and public
URLs are inferred from configured metadata and the repository identity.

Pages-settings verification uses read-only `gh api` calls and compares
structured responses to `deployment` expectations. `--strict` fails when
verification is unavailable; without it, unavailable reads are reported
as skipped. It verifies classic branch protection, not repository rulesets.

Configure Pages to deploy through GitHub Actions. Branch protection should
match `deployment.required_status_checks`, `require_pull_requests`, and
`enforce_admins`; the verifier does not apply or alter these settings.
Changes to the shared tooling take effect only after an explicit submodule
pointer update. Runtime/action pins and caches belong to the shared
implementation; source metadata and deployable outputs are never cached
as authoritative results.
