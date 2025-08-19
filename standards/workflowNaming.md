# Workflow Naming Standard

## Purpose
Define a single, enforceable standard for naming GitHub Actions workflows across SPECTRA so they are readable, reusable, and governable.

## Scope
- Applies to every workflow file under `.github/workflows/` in all repositories.
- Covers the file name and the workflow display name (`name:` at the top of the YAML).
- Job and step identifiers are included for consistency, but display names for jobs/steps are flexible.

## Canonical Rule
- Workflow file names and workflow display names MUST be identical, verb-first, kebab-case, all lowercase.
- Grammar pattern: `{verb}-{noun}[-{qualifier}...]` or `{verb}-and-{verb}` for dual actions.
- No emoji, no spaces, only `[a-z0-9-]`.

Examples (good):
- `enforce-chief-of-staff`
- `validate-governance`
- `seed-labels`
- `plan-and-generate`
- `update-dependency-graph`
- `build-and-test` (dual verb)

Examples (not allowed):
- `ChiefOfStaffEnforcement` (camelCase/PascalCase)
- `chief-of-staff-enforcement` (noun-first)
- `labels-seeder` (agent suffix; use verb-first: `seed-labels`)
- `Governance Guards` (spaces, title case)
- `validate_workflow_names` (underscores)

## Location
- All workflows MUST be stored at `.github/workflows/`.
- In the governance repo (`SPECTRADataSolutions/.github`), reusable workflows MUST also be located at `.github/workflows/` to be callable via:
  `uses: SPECTRADataSolutions/.github/.github/workflows/<file>.yml@<ref>`

## Display Name
- The top-level `name:` MUST match the file's base name (without `.yml`/`.yaml`).
  - File: `.github/workflows/update-dependency-graph.yml`
  - Name: `update-dependency-graph`

## Verbs (recommended set)
Use clear, imperative verbs. Preferred list:
- build, test, lint, validate, verify, check
- enforce, guard, protect
- plan, generate, scaffold, seed, sync, update, publish, deploy, release, package, scan
- backup, restore, migrate, archive

For two actions in one workflow, connect with `-and-`:
- `build-and-test`, `plan-and-generate`

## Jobs and Steps
- Job IDs MUST be camelCase (e.g., `spectraLint`, `validateYaml`).
- Step IDs (if used) MUST be camelCase.
- Job and step display names SHOULD be short, sentence case (flexible).

## File Extension
- Use `.yml` (preferred). `.yaml` is permitted but must be consistent within a repository.

## Triggers
- Triggers (`on:`) MUST NOT be encoded in the workflow name. Use the YAML to express schedule/path-filter nuances, not the file name.

## Migration Guidance
1) Rename files to conform (kebab-case, verb-first).
2) Ensure `name:` at top matches file base name.
3) Update any callers of reusable workflows to new paths (must be `.github/workflows/...`).
4) Let the validator pass (see guard below).

## FAQ
- Can we include environments or branches in names?
  - No. Keep names stable; express conditions in YAML (`if:`, `on:`, `env:`).
- Are emojis allowed?
  - No. Emojis are reserved for notebook names, not filenames or identifiers here.
- Why verb-first?
  - Improves scanning ("what it does" first) and aligns with governance verbs (validate, enforce, seed, update).