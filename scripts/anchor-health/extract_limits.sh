#!/usr/bin/env bash
set -euo pipefail
MAX_FILE_KB=$(jq -r '.sizeLimits.maxFileSizeKB // 1024' /tmp/manifest.json)
MAX_TOTAL_MB=$(jq -r '.sizeLimits.maxTotalSizeMB // 50' /tmp/manifest.json)
{
  echo "maxFileKB=$MAX_FILE_KB"
  echo "maxTotalMB=$MAX_TOTAL_MB"
} >> "$GITHUB_OUTPUT"
echo "Per-file limit: ${MAX_FILE_KB}KB; Total limit: ${MAX_TOTAL_MB}MB"
