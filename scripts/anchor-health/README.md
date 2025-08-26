# Anchor Health Scripts

Purpose: Support the `check-anchor-health` workflow with isolated, testable shell scripts.

Scripts:
- manifest_validate.sh: Validate manifest presence & schema.
- extract_limits.sh: Derive size limits.
- scan_anchors.sh: Perform reachability, size and mime scan; emit key=value outputs and markdown + JSON summaries.
- issue_payload.sh: Produce JSON body for issue creation (if gaps found).

All scripts are idempotent and safe to re-run. They depend only on:
- `jq`, `curl`, `bash`, `sed`, `tr`
- Optional: `ajv` & `js-yaml` installed globally (workflow step installs)

Outputs are written to `/tmp`:
- /tmp/manifest.json
- /tmp/anchor_report.md
- /tmp/anchor_summary.json
- /tmp/issue_body.md (only if needed)

Environment variables consumed:
- MANIFEST_PATH
- COVERAGE_THRESHOLD
- CONTRACTS_REPO
- GITHUB_TOKEN (implicit from runner)

Return codes:
- 0 success
- 2 soft warning (e.g., schema missing)
- 3 coverage gate failed
- 4 manifest missing

