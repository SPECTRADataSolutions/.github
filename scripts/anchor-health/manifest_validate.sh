#!/usr/bin/env bash
set -euo pipefail
MP="target-repo/${MANIFEST_PATH}"
if [ ! -f "$MP" ]; then
  echo "::error title=Manifest Missing::No manifest at ${MANIFEST_PATH}" >&2
  exit 4
fi
js-yaml "$MP" > /tmp/manifest.json || { echo "::error::YAML to JSON conversion failed"; exit 1; }
if [ -f "contracts-repo/contracts/context/contextManifest.json" ]; then
  if ! ajv validate -s contracts-repo/contracts/context/contextManifest.json -d /tmp/manifest.json; then
    echo "::error title=Schema Validation Failed::Manifest does not conform to schema"; exit 1;
  fi
else
  echo "::warning title=Schema Missing::Skipping structural validation" >&2
fi
ALLOWED_OWNER=$(jq -r '.allowedOwners[0] // empty' /tmp/manifest.json)
if [ -n "$ALLOWED_OWNER" ] && [ "$ALLOWED_OWNER" != "SPECTRADataSolutions" ]; then
  echo "::warning title=Owner Mismatch::First allowed owner is $ALLOWED_OWNER" >&2
fi
