#!/usr/bin/env bash
# Verify GitHub Pages + branch-protection settings (issue #15, CI-12).
#
# Nothing here changes settings (no network side-effects besides read-only
# `gh api` GETs). When `gh` is missing or the network is unavailable, the
# script prints the manual checklist from docs/pages-deploy.md and exits 0
# (verification is then a human step, not a CI failure).
#
# Usage: bash scripts/verify-pages-settings.sh [--strict]
#   --strict: exit 1 (instead of 0) when live verification was skipped.
set -euo pipefail

STRICT=0
[ "${1:-}" = "--strict" ] && STRICT=1

REPO="AntonC9018/uniCourse_dataStructuresAndAlgorithms"
EXPECTED_BASE="https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms"

have_gh=0
command -v gh >/dev/null 2>&1 && have_gh=1

if [ "$have_gh" = "0" ]; then
  echo "SKIP: gh CLI not available; use the manual checklist in docs/pages-deploy.md"
  echo "  - Pages source: GitHub Actions"
  echo "  - Required status: course-site / validate"
  echo "  - No PR requirement; admin bypass retained"
  echo "  - Public URL: $EXPECTED_BASE/"
  [ "$STRICT" = "1" ] && exit 1 || exit 0
fi

fail=0
warn() { printf 'WARN: %s\n' "$*"; }
pass() { printf 'PASS: %s\n' "$*"; }
bad() { printf 'FAIL: %s\n' "$*"; fail=1; }

# 1. Pages source must be GitHub Actions (not branch deploy).
if pages_json="$(gh api "repos/$REPO/pages" 2>/dev/null)"; then
  echo "$pages_json" | grep -q '"build_type"[[:space:]]*:[[:space:]]*"workflow"' \
    && pass "Pages source is GitHub Actions" \
    || bad "Pages source is not GitHub Actions (see docs/pages-deploy.md)"
  echo "$pages_json" | grep -q 'AntonC9018.github.io' \
    && pass "Pages URL present" \
    || warn "Pages URL not found in API response"
else
  warn "cannot reach Pages API (offline?); falling back to manual checklist"
  echo "Manual checklist: docs/pages-deploy.md"
  [ "$STRICT" = "1" ] && exit 1 || exit 0
fi

# 2. Branch protection on master: required status, no PR mandate, admin bypass.
if prot_json="$(gh api "repos/$REPO/branches/master/protection" 2>/dev/null)"; then
  echo "$prot_json" | grep -q 'validate' \
    && pass "required status mentions validate" \
    || bad "required status does not mention validate"
  # required_pull_request_reviews absent/null => PRs not mandatory (CI-12).
  if echo "$prot_json" | grep -q '"required_pull_request_reviews"'; then
    # Present: check whether it enforces reviews (dismissal/review count).
    echo "$prot_json" | grep -q '"required_approving_review_count"[[:space:]]*:[[:space:]]*0' \
      && pass "PR reviews not mandated (count 0)" \
      || warn "required_pull_request_reviews present; ensure PRs are NOT mandatory (CI-12)"
  else
    pass "no required_pull_request_reviews block (PRs not mandatory)"
  fi
  echo "$prot_json" | grep -q '"enforce_admins"[[:space:]]*:[[:space:]]*[^,}]*enabled[^,}]*false' \
    && pass "admin bypass retained" \
    || warn "could not confirm enforce_admins=false; verify manually that admins can push to master"
else
  warn "cannot reach branch-protection API; verify manually per docs/pages-deploy.md"
fi

# 3. Smoke hint (does not fail here; smoke-test.sh owns post-deploy checks).
echo "INFO: run post-deploy smoke tests with:"
echo "  BASE_URL=$EXPECTED_BASE bash scripts/smoke-test.sh"

[ "$fail" -eq 0 ]
