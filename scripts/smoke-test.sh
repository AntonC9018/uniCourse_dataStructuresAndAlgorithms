#!/usr/bin/env bash
# Post-deploy smoke tests for the data-structures course site (issue #15, CI-11).
#
# Verifies at the public Pages URL (default below, override with BASE_URL):
#   1. root redirect -> /en/common/labs/computer-architecture/
#   2. representative English route
#   3. representative Russian route
#   4. Pagefind search (page markup references pagefind + index JS reachable)
#   5. static Mermaid output (inline SVG on graphs page + served .svg file)
#   6. copied image asset served from public Pages URL
#
# Bounded retry: Pages deployments propagate with delay, so every check
# retries with a fixed bound (SMOKE_RETRIES x SMOKE_SLEEP_S, defaults
# 30x10s = ~5min). Fails (exit 1) on first check that never passes.
# No network side-effects besides GET requests; safe to re-run.
#
# Usage:
#   BASE_URL=https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms \
#     bash scripts/smoke-test.sh
#   SMOKE_RETRIES=5 SMOKE_SLEEP_S=2 bash scripts/smoke-test.sh  # faster local
#
# Local validation against a built dist/:
#   python3 -m http.server 8080 --directory /tmp/site-out/dist &
#   BASE_URL=http://127.0.0.1:8080/uniCourse_dataStructuresAndAlgorithms \
#     SMOKE_RETRIES=3 SMOKE_SLEEP_S=1 bash scripts/smoke-test.sh
set -euo pipefail

BASE_URL="${BASE_URL:-https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms}"
RETRIES="${SMOKE_RETRIES:-30}"
SLEEP_S="${SMOKE_SLEEP_S:-10}"

BASE_URL="${BASE_URL%/}"
PASS=0
FAIL=0

log() { printf '%s\n' "$*"; }
ok() { PASS=$((PASS + 1)); log "PASS: $*"; }
fail() { FAIL=$((FAIL + 1)); log "FAIL: $*"; return 1; }

# fetch <url> -> prints body to stdout; returns nonzero on HTTP error.
fetch() {
  curl -fsSL --retry 0 --max-time 30 --user-agent "course-smoke/1.0" "$1"
}

# check_contains <label> <url> <expected-substring>
# Retries up to $RETRIES; passes when body contains the substring.
check_contains() {
  local label="$1" url="$2" needle="$3" attempt=1 body=""
  while [ "$attempt" -le "$RETRIES" ]; do
    if body="$(fetch "$url" 2>/dev/null)"; then
      if printf '%s' "$body" | grep -qF "$needle"; then
        ok "$label ($url contains $(printf '%s' "$needle" | head -c 60))"
        return 0
      fi
      log "attempt $attempt/$RETRIES: $label reachable but missing expected content; retrying in ${SLEEP_S}s"
    else
      log "attempt $attempt/$RETRIES: $label not reachable ($url); retrying in ${SLEEP_S}s"
    fi
    attempt=$((attempt + 1))
    [ "$attempt" -le "$RETRIES" ] && sleep "$SLEEP_S"
  done
  fail "$label ($url never contained $(printf '%s' "$needle" | head -c 60) after $RETRIES attempts)"
}

# check_status200 <label> <url>  (binary-safe, e.g. images)
check_status200() {
  local label="$1" url="$2" attempt=1 code=""
  while [ "$attempt" -le "$RETRIES" ]; do
    code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 --user-agent "course-smoke/1.0" "$url" 2>/dev/null || true)"
    if [ "$code" = "200" ]; then
      ok "$label ($url -> 200)"
      return 0
    fi
    log "attempt $attempt/$RETRIES: $label got HTTP $code ($url); retrying in ${SLEEP_S}s"
    attempt=$((attempt + 1))
    [ "$attempt" -le "$RETRIES" ] && sleep "$SLEEP_S"
  done
  fail "$label ($url never returned 200 after $RETRIES attempts; last: $code)"
}

log "smoke: BASE_URL=$BASE_URL retries=$RETRIES sleep=${SLEEP_S}s"

# 1. Root redirect: / follows to the default English lab. Astro emits a
# redirect page, so assert the served root references the target slug.
check_contains "root redirect" \
  "$BASE_URL/" \
  "/en/common/labs/computer-architecture/" || true

# 2. Representative English route.
check_contains "en route" \
  "$BASE_URL/en/common/labs/computer-architecture/" \
  "Computer Architecture" || true

# 3. Representative Russian route.
check_contains "ru route" \
  "$BASE_URL/ru/common/labs/computer-architecture/" \
  "Архитектура компьютера" || true

# 4. Search: representative page references Pagefind (proves the
# pagefind:true build + indexed routes are served).
check_contains "search markup (pagefind)" \
  "$BASE_URL/en/common/labs/computer-architecture/" \
  "pagefind" || true

# 4b. Search index JS reachable. Astro Starlight/Pagefind emits the index
# under pagefind/ (observed in dist/: pagefind/pagefind.js); older layouts
# use _pagefind/. Accept either (observed path first to avoid wasting the
# retry budget on the legacy path).
PAGEFIND_OK=0
for p in "pagefind/pagefind.js" "_pagefind/pagefind.js"; do
  if check_status200 "search index ($p)" "$BASE_URL/$p"; then
    PAGEFIND_OK=1
    break
  fi
done
[ "$PAGEFIND_OK" = "1" ] || true

# 5. Static Mermaid: graphs lesson embeds pre-rendered SVG (no client JS).
check_contains "mermaid inline SVG" \
  "$BASE_URL/en/dsa/labs/graphs/" \
  "mermaid-static" || true

check_contains "mermaid served SVG" \
  "$BASE_URL/mermaid/en-dsa-labs-graphs-0.svg" \
  "<svg" || true

# 6. Copied image asset at the public Pages URL (public/assets/... below
# the project base; source en/04_compiler_and_ide/cpp_extension.png).
check_status200 "copied asset (cpp_extension.png)" \
  "$BASE_URL/assets/AntonC9018/uniCourse_dataStructuresAndAlgorithms/en/04_compiler_and_ide/cpp_extension.png" || true

log "smoke: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
