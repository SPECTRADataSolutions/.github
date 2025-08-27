#!/usr/bin/env bash
set -euo pipefail

manifest="${MANIFEST_PATH:-.github/context/anchors.jsonl}"
coverage_threshold="${COVERAGE_THRESHOLD:-85}"
max_total_mb="${MAX_TOTAL_MB:-50}"
max_anchor_kb="${MAX_ANCHOR_KB:-256}"

summary_file="${GITHUB_STEP_SUMMARY:-/dev/null}"
out_file="${GITHUB_OUTPUT:-/dev/null}"

echo "[anchor-metrics] Using manifest: $manifest"
if [[ ! -f "$manifest" ]]; then
  echo "[anchor-metrics] Manifest missing; emitting empty metrics." >&2
  {
    echo "total=0"; echo "reachable=0"; echo "unreachable=0"; echo "oversized=0";
    echo "coverage=0"; echo "total_kb=0"; echo "total_mb=0"; echo "size_exceeded=false";
    printf 'oversize_list<<EOF\nEOF\n'; printf 'unreachable_list<<EOF\nEOF\n';
  } >> "$out_file"
  echo "## 📊 Anchor Reachability & Size" >> "$summary_file"
  echo "Manifest not found at $manifest" >> "$summary_file"
  exit 0
fi

tmp_jsonl=$(mktemp)
first_char=$(grep -o "\S" "$manifest" | head -n1 || true)
if [[ "$first_char" == "[" ]]; then
  python - <<'PY' "$manifest" "$tmp_jsonl"
import json, sys
src, dst = sys.argv[1:]
with open(src, 'r', encoding='utf-8') as f:
    data = json.load(f)
with open(dst, 'w', encoding='utf-8') as out:
    for obj in data:
        out.write(json.dumps(obj)+'\n')
PY
else
  cp "$manifest" "$tmp_jsonl"
fi

total=0; reachable=0; unreachable=0; oversized=0; total_size_kb=0
oversize_list=""; unreachable_list=""

while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  [[ "$line" != \{* ]] && continue || true
  path=$(echo "$line" | jq -r '.path // .ref // empty') || path=""
  bytes=$(echo "$line" | jq -r '.sizeBytes // empty') || bytes=""
  [[ -z "$path" ]] && continue
  total=$((total+1))
  if [[ -n "$bytes" && "$bytes" =~ ^[0-9]+$ && "$bytes" -gt 0 ]]; then
    kb=$(( (bytes + 1023) / 1024 ))
    total_size_kb=$(( total_size_kb + kb ))
    if (( kb > max_anchor_kb )); then
      oversized=$((oversized+1))
      oversize_list+="$path (${kb}KB)\n"
    fi
  fi
  if [[ "$path" =~ ^https?:// ]]; then
    if curl -fsIL --max-time 10 "$path" > /dev/null 2>&1; then
      reachable=$((reachable+1))
    else
      unreachable=$((unreachable+1))
      unreachable_list+="$path\n"
    fi
  else
    if [[ -f "$path" ]]; then
      reachable=$((reachable+1))
    else
      unreachable=$((unreachable+1))
      unreachable_list+="$path\n"
    fi
  fi
done < "$tmp_jsonl"

if (( total > 0 )); then coverage=$(( reachable * 100 / total )); else coverage=0; fi
total_mb=$(( (total_size_kb + 1023) / 1024 ))
if (( total_mb > max_total_mb )); then size_exceeded=true; else size_exceeded=false; fi

{
  echo "total=$total"; echo "reachable=$reachable"; echo "unreachable=$unreachable"; echo "oversized=$oversized";
  echo "coverage=$coverage"; echo "total_kb=$total_size_kb"; echo "total_mb=$total_mb"; echo "size_exceeded=$size_exceeded";
  printf 'oversize_list<<EOF\n%sEOF\n' "$oversize_list"; printf 'unreachable_list<<EOF\n%sEOF\n' "$unreachable_list";
} >> "$out_file"

echo "## 📊 Anchor Reachability & Size" >> "$summary_file"
echo "**Coverage Threshold:** ${coverage_threshold}%" >> "$summary_file"
echo "**Total Anchors:** ${total}" >> "$summary_file"
echo "**Reachable:** ${reachable}" >> "$summary_file"
echo "**Unreachable:** ${unreachable}" >> "$summary_file"
echo "**Oversized:** ${oversized}" >> "$summary_file"
echo "**Coverage:** ${coverage}%" >> "$summary_file"
echo "**Aggregate Size:** ${total_mb}MB (limit ${max_total_mb}MB)" >> "$summary_file"
if [[ "$size_exceeded" == true ]]; then echo "**Size Status:** ❌ Exceeded" >> "$summary_file"; else echo "**Size Status:** ✅ Within Limit" >> "$summary_file"; fi
if (( coverage >= coverage_threshold )); then echo "**Coverage Gate (target ${coverage_threshold}%):** ✅ Passed" >> "$summary_file"; else echo "**Coverage Gate (target ${coverage_threshold}%):** ❌ Failed" >> "$summary_file"; fi

if [[ -n "$oversize_list" ]]; then
  echo -e "\n### Oversized Anchors" >> "$summary_file"
  echo -e "$oversize_list" >> "$summary_file"
fi
if [[ -n "$unreachable_list" ]]; then
  echo -e "\n### Unreachable Anchors" >> "$summary_file"
  echo -e "$unreachable_list" >> "$summary_file"
fi

echo "[anchor-metrics] Done." >&2
