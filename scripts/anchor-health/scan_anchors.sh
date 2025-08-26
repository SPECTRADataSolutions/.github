#!/usr/bin/env bash
set -euo pipefail
MAX_FILE_KB="$1"; MAX_TOTAL_MB="$2"; MAX_TOTAL_KB=$(( MAX_TOTAL_MB * 1024 ))
TOTAL_ANCHORS=0; REACHABLE=0; UNREACHABLE=0; OVERSIZED=0; TOTAL_SIZE_KB=0
UNREACHABLE_LIST=""; OVERSIZED_LIST=""; UNSUPPORTED_MIME_LIST=""
ALLOWED_MIME=$(jq -r '.mimeTypeAllowlist[]' /tmp/manifest.json | tr '\n' ' ')
REPO_COUNT=$(jq '.allowedRepos | length' /tmp/manifest.json)
if [ "$REPO_COUNT" -eq 0 ]; then
  echo "::error title=No Repositories::allowedRepos array is empty"; exit 1
fi
REPORT=/tmp/anchor_report.md
{
  echo "# Anchor Reachability Report"; echo; echo "Coverage Threshold: ${COVERAGE_THRESHOLD}%"; echo;
} > "$REPORT"

mime_from_ext () { case "$1" in md|markdown) echo text/markdown;; json) echo application/json;; yaml|yml) echo application/yaml;; xml) echo application/xml;; txt) echo text/plain;; *) echo unknown;; esac; }

for i in $(seq 0 $(( REPO_COUNT - 1 ))); do
  R_OWNER=$(jq -r ".allowedRepos[$i].owner" /tmp/manifest.json)
  R_NAME=$(jq -r ".allowedRepos[$i].name" /tmp/manifest.json)
  REFS=$(jq -r ".allowedRepos[$i].allowedRefs[]" /tmp/manifest.json)
  PATHS=$(jq -r ".allowedRepos[$i].allowedPaths[]" /tmp/manifest.json)
  echo "## Repository: $R_OWNER/$R_NAME" >> "$REPORT"; echo >> "$REPORT"
  for REF in $REFS; do
    echo "### Ref: $REF" >> "$REPORT"; echo >> "$REPORT"
    for P in $PATHS; do
      RESP=$(curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/repos/$R_OWNER/$R_NAME/contents/$P?ref=$REF")
      TYPE=$(echo "$RESP" | jq -r '.type // empty')
      MESSAGE=$(echo "$RESP" | jq -r '.message // empty')
      if [ "$MESSAGE" = "Not Found" ] || [ -z "$RESP" ]; then
        TOTAL_ANCHORS=$((TOTAL_ANCHORS+1)); UNREACHABLE=$((UNREACHABLE+1))
        UNREACHABLE_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$P'@'$REF' (not found)'
        echo "- ❌ $P (not found)" >> "$REPORT"; continue
      fi
      if [ "$TYPE" = "file" ]; then
        TOTAL_ANCHORS=$((TOTAL_ANCHORS+1))
        SIZE_BYTES=$(echo "$RESP" | jq -r '.size // 0')
        SIZE_KB=$(( (SIZE_BYTES + 1023) / 1024 ))
        EXT="${P##*.}"; MIME=$(mime_from_ext "$EXT")
        REACHABLE=$((REACHABLE+1)); TOTAL_SIZE_KB=$((TOTAL_SIZE_KB+SIZE_KB))
        STATUS_ICON="✅"; NOTE="OK ${SIZE_KB}KB"
        if [ "$SIZE_KB" -gt "$MAX_FILE_KB" ]; then
          OVERSIZED=$((OVERSIZED+1)); STATUS_ICON="⚠️"; NOTE="Oversized ${SIZE_KB}KB > ${MAX_FILE_KB}KB";
          OVERSIZED_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$P'@'$REF' ('${SIZE_KB}'KB)'
        fi
        if [ "$MIME" != "unknown" ]; then
          echo "$ALLOWED_MIME" | tr ' ' '\n' | grep -qx "$MIME" || { UNSUPPORTED_MIME_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$P'@'$REF' ('$MIME')'; NOTE+="; MIME $MIME not allowlisted"; [ "$STATUS_ICON" = "✅" ] && STATUS_ICON="⚠️"; }
        fi
        echo "- ${STATUS_ICON} $P (${NOTE})" >> "$REPORT"
      elif echo "$RESP" | jq -e 'type=="array"' >/dev/null 2>&1; then
        FILES=$(echo "$RESP" | jq -r '.[] | select(.type=="file") | .path')
        for FP in $FILES; do
          FR=$(curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/repos/$R_OWNER/$R_NAME/contents/$FP?ref=$REF")
          SIZE_BYTES=$(echo "$FR" | jq -r '.size // 0'); SIZE_KB=$(( (SIZE_BYTES + 1023) / 1024 ))
          EXT="${FP##*.}"; MIME=$(mime_from_ext "$EXT")
          TOTAL_ANCHORS=$((TOTAL_ANCHORS+1)); REACHABLE=$((REACHABLE+1)); TOTAL_SIZE_KB=$((TOTAL_SIZE_KB+SIZE_KB))
          STATUS_ICON="✅"; NOTE="OK ${SIZE_KB}KB"
          if [ "$SIZE_KB" -gt "$MAX_FILE_KB" ]; then
            OVERSIZED=$((OVERSIZED+1)); STATUS_ICON="⚠️"; NOTE="Oversized ${SIZE_KB}KB > ${MAX_FILE_KB}KB"; OVERSIZED_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$FP'@'$REF' ('${SIZE_KB}'KB)'
          fi
          if [ "$MIME" != "unknown" ]; then
            echo "$ALLOWED_MIME" | tr ' ' '\n' | grep -qx "$MIME" || { UNSUPPORTED_MIME_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$FP'@'$REF' ('$MIME')'; NOTE+="; MIME $MIME not allowlisted"; [ "$STATUS_ICON" = "✅" ] && STATUS_ICON="⚠️"; }
          fi
          echo "- ${STATUS_ICON} $FP (${NOTE})" >> "$REPORT"
        done
      else
        TOTAL_ANCHORS=$((TOTAL_ANCHORS+1)); UNREACHABLE=$((UNREACHABLE+1))
        UNREACHABLE_LIST+=$'\n- '$R_OWNER'/'$R_NAME'/'$P'@'$REF' (unsupported type)'
        echo "- ❌ $P (unsupported type)" >> "$REPORT"
      fi
    done
    echo >> "$REPORT"
  done
done

if [ "$TOTAL_ANCHORS" -gt 0 ]; then COVERAGE=$(( REACHABLE * 100 / TOTAL_ANCHORS )); else COVERAGE=0; fi
TOTAL_MB=$(( TOTAL_SIZE_KB / 1024 )); SIZE_EXCEEDED=false; if [ "$TOTAL_SIZE_KB" -gt "$MAX_TOTAL_KB" ]; then SIZE_EXCEEDED=true; fi
{
  echo; echo "## Summary"; echo; echo "- Total anchors: $TOTAL_ANCHORS"; echo "- Reachable: $REACHABLE"; echo "- Unreachable: $UNREACHABLE"; echo "- Oversized: $OVERSIZED"; echo "- Coverage: ${COVERAGE}%"; echo "- Aggregate size: ${TOTAL_MB}MB (limit ${MAX_TOTAL_MB}MB)";
} >> "$REPORT"

cat > /tmp/anchor_summary.json <<JSON
{
  "totalAnchors": $TOTAL_ANCHORS,
  "reachable": $REACHABLE,
  "unreachable": $UNREACHABLE,
  "oversized": $OVERSIZED,
  "coverage": $COVERAGE,
  "totalSizeKB": $TOTAL_SIZE_KB,
  "sizeExceeded": $([ "$SIZE_EXCEEDED" = true ] && echo true || echo false)
}
JSON

{
  echo "totalAnchors=$TOTAL_ANCHORS";
  echo "reachable=$REACHABLE";
  echo "unreachable=$UNREACHABLE";
  echo "oversized=$OVERSIZED";
  echo "coverage=$COVERAGE";
  echo "totalSizeKB=$TOTAL_SIZE_KB";
  echo "totalSizeMB=$TOTAL_MB";
  echo "sizeExceeded=$SIZE_EXCEEDED";
  printf "unreachableList<<EOF\n%s\nEOF\n" "$(echo -e "$UNREACHABLE_LIST" | sed '/^$/d')";
  printf "oversizedList<<EOF\n%s\nEOF\n" "$(echo -e "$OVERSIZED_LIST" | sed '/^$/d')";
  printf "unsupportedMimeList<<EOF\n%s\nEOF\n" "$(echo -e "$UNSUPPORTED_MIME_LIST" | sed '/^$/d')";
} >> "$GITHUB_OUTPUT"

if [ $COVERAGE -lt $COVERAGE_THRESHOLD ] || [ "$SIZE_EXCEEDED" = true ] || [ $OVERSIZED -gt 0 ] || [ $UNREACHABLE -gt 0 ]; then
  EXIT_CODE=3
else
  EXIT_CODE=0
fi
exit $EXIT_CODE
