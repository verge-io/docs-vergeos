#!/usr/bin/env bash
# check-cross-space-links.sh — validate cross-space links in this GitBook monorepo.
#
# Cross-space links are written as https://app.gitbook.com/s/<spaceId>/<page-path>.
# GitBook resolves them to published-site URLs at import time; a path that does not
# match a real page in the target space is silently published as a literal
# app.gitbook.com URL (login-walled). Page paths also drift when pages are renamed
# or moved between SUMMARY groups, so re-run this after any such change.
#
# Check 1 (always): every cross-space link path in the repo's markdown matches a
#   real page path in the target space's live content (GitBook content API).
# Check 2 (--published): fetch every published page whose source contains a
#   cross-space link and fail if the rendered HTML contains an unresolved
#   href="https://app.gitbook.com..." anchor. Slower (~150 page fetches).
#
# Requires: curl, jq, and GITBOOK_API_TOKEN in .env.local at the repo root.
# Usage: .claude/scripts/check-cross-space-links.sh [--published]
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

PUBLISHED=0
[ "${1:-}" = "--published" ] && PUBLISHED=1

if [ ! -f .env.local ]; then
  echo "ERROR: .env.local not found at repo root (needs GITBOOK_API_TOKEN)" >&2
  exit 2
fi
# shellcheck disable=SC1091
source .env.local
if [ -z "${GITBOOK_API_TOKEN:-}" ]; then
  echo "ERROR: GITBOOK_API_TOKEN is not set in .env.local" >&2
  exit 2
fi

# dir : spaceId : published-section-path ("" = site root)
SPACES=(
  "home:uJc5d3O7cwI7qD8muSyG:"
  "deploy:Q2bN3ctQdjv01GivTI08:plan-and-deploy"
  "run:pODKGSQETqL1gSqyxIq3:run-the-platform"
  "automate:sppYQkyIET58BuAo0kqm:automate-protect-and-extend"
  "learn:qLUTTK5fxfW4S9FoS9GE:learn-the-platform"
  "knowledge-base:QZBMFpokMv2vWTIRbFzA:knowledge-base"
  "release-notes:33mA7es4mQYkyUa7dMvu:release-notes"
)
SPACE_DIRS=(home deploy run automate learn knowledge-base release-notes)

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "== Fetching live content for ${#SPACES[@]} spaces =="
for entry in "${SPACES[@]}"; do
  IFS=: read -r dir id _sect <<< "$entry"
  # map: repo file <TAB> GitBook page path
  curl -sf -m 30 -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "https://api.gitbook.com/v1/spaces/$id/content" \
    | jq -r '.. | objects | select(.path and .git) | "\(.git.path)\t\(.path)"' \
    > "$TMP/map-$id.txt" || { echo "ERROR: content API fetch failed for $dir ($id)" >&2; exit 2; }
  cut -f2 "$TMP/map-$id.txt" > "$TMP/paths-$id.txt"
  printf '  %-15s %s pages\n' "$dir" "$(wc -l < "$TMP/paths-$id.txt" | tr -d ' ')"
done

echo
echo "== Check 1: source link paths vs live page paths =="
grep -rnoE 'app\.gitbook\.com/s/[A-Za-z0-9]+/[A-Za-z0-9/_#.-]+' "${SPACE_DIRS[@]}" \
  --include='*.md' 2>/dev/null | sed 's/#[^:]*$//' | sort -u > "$TMP/links.txt" || true

FAIL=0
TOTAL=0
while IFS= read -r line; do
  loc="${line%%:app.gitbook.com*}"
  url="${line#*app.gitbook.com/s/}"
  id="${url%%/*}"
  path="${url#*/}"
  TOTAL=$((TOTAL + 1))
  if [ ! -f "$TMP/paths-$id.txt" ]; then
    echo "  UNKNOWN SPACE $id  ($loc)"
    FAIL=$((FAIL + 1))
  elif ! grep -qxF "$path" "$TMP/paths-$id.txt"; then
    echo "  BAD PATH $id/$path  ($loc)"
    FAIL=$((FAIL + 1))
  fi
done < "$TMP/links.txt"
echo "  checked $TOTAL link occurrences, $FAIL bad"

PUB_FAIL=0
if [ "$PUBLISHED" = 1 ]; then
  echo
  echo "== Check 2: published pages free of unresolved app.gitbook.com anchors =="
  grep -rlE 'app\.gitbook\.com/s/' "${SPACE_DIRS[@]}" --include='*.md' 2>/dev/null \
    | sort > "$TMP/linking-files.txt" || true

  check_page() {
    local file="$1" tmp="$2"
    local dir="${file%%/*}" id="" sect="" entry path url html code hits
    case "$dir" in
      home) id=uJc5d3O7cwI7qD8muSyG; sect="" ;;
      deploy) id=Q2bN3ctQdjv01GivTI08; sect=plan-and-deploy ;;
      run) id=pODKGSQETqL1gSqyxIq3; sect=run-the-platform ;;
      automate) id=sppYQkyIET58BuAo0kqm; sect=automate-protect-and-extend ;;
      learn) id=qLUTTK5fxfW4S9FoS9GE; sect=learn-the-platform ;;
      knowledge-base) id=QZBMFpokMv2vWTIRbFzA; sect=knowledge-base ;;
      release-notes) id=33mA7es4mQYkyUa7dMvu; sect=release-notes ;;
      *) echo "  SKIP $file (unknown space dir)"; return ;;
    esac
    path="$(awk -F'\t' -v f="$file" '$1==f{print $2; exit}' "$tmp/map-$id.txt")"
    if [ -z "$path" ]; then
      echo "  NOT-SYNCED $file (no live page yet — links resolve on its first sync)"
      return
    fi
    if [ "$path" = "readme" ]; then
      url="https://docs.verge.io/${sect:+$sect/}"
    else
      url="https://docs.verge.io/${sect:+$sect/}$path"
    fi
    html="$(curl -sL -m 25 -w '\n%{http_code}' "$url")"
    code="${html##*$'\n'}"
    hits="$(printf '%s' "$html" | grep -oE 'href="https://app\.gitbook\.com[^"]*"' | wc -l | tr -d ' ')"
    if [ "$code" != "200" ] || [ "$hits" != "0" ]; then
      echo "  UNRESOLVED http=$code anchors=$hits  $file  $url"
    fi
  }
  export -f check_page

  xargs -P 8 -I{} bash -c 'check_page "$@"' _ {} "$TMP" \
    < "$TMP/linking-files.txt" > "$TMP/pub-results.txt"
  cat "$TMP/pub-results.txt"
  PUB_FAIL="$(grep -c 'UNRESOLVED' "$TMP/pub-results.txt" || true)"
  echo "  checked $(wc -l < "$TMP/linking-files.txt" | tr -d ' ') published pages, $PUB_FAIL with unresolved links"
fi

echo
if [ "$FAIL" = 0 ] && [ "$PUB_FAIL" = 0 ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: $FAIL bad source paths, $PUB_FAIL pages with unresolved published links"
  exit 1
fi
