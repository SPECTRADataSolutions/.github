# Project Provisioning Blueprint (Spectra Grade)

> Drafted: 2025-11-21 — Author: GitHub Copilot (GPT-5.1-Codex)

## 1. Purpose

Replace the fragile `bootstrap-project-backlog` workflow/script chain with a deterministic, schema-driven capability that can create or update GitHub Projects v2, issues, and Project field values straight from Spectra manifests. The new flow must be portable across all SPECTRA repos, reusable as an Actions workflow, and fully compliant with the Spectra Agent Contract.

## 2. Guiding Constraints

1. **Single Source of Truth** – All backlog definitions stay in `config/projects/**/*.yml` with matching JSON schemas under `config/projects/schemas/**`. No new manual lists in workflows.
2. **Pure CLI in `framework/`** – The `spectra` CLI only reads/writes files (plan artefacts, schema validation). API calls happen exclusively inside the execution layer.
3. **Reusable Execution Layer** – The `.github` repo provides reusable workflows & scripts that consume CLI plan artefacts and talk to GitHub via first-party APIs/`gh`.
4. **Deterministic Evidence** – Every run writes plan/apply artefacts under `.spectra/evidence/project-provisioning/` and publishes a concise summary to the job log & job summary.
5. **Org-Safe Secrets** – Workflows mint short-lived GitHub App tokens (or repo PATs) via standard Actions. Use the shared `SPECTRA_APP_*` org secrets and `scripts/spectra_assistant_token.py` helper to avoid copying PEM blobs by hand.
6. **Pagination & Idempotence** – GraphQL queries iterate via cursors; REST fallbacks honour pagination headers. All operations are idempotent (re-apply safe).

## 3. Component Breakdown

### 3.1 `framework/` (Python package)

| Capability | Description |
| --- | --- |
| Manifest schema extension | Add `projects[].activities[].projectProvisioning` (or sibling) sections that describe Project name, description, fields, views, issue derivations, etc. Schema published via `spectra schema`.
| CLI commands | `spectra project plan <manifest>` produces `plan.json` + `summary.md` in `.spectra/output/project/<slug>/`. Command validates schema, resolves includes, ensures stage ordering, and emits deterministic plan (create/update/delete ops without performing API calls).
| CLI config | Optional `spectra.toml` to map manifest IDs to GitHub org/repo IDs (pure file metadata).
| Tests | Extend PyTest suite for schema validation + plan emitter.

Outputs from CLI:
```json
{
  "project": {
    "title": "Alana Iterations 1-5",
    "description": "…",
    "owner": {"type": "org", "slug": "SPECTRADataSolutions"}
  },
  "fields": [...],
  "views": [...],
  "issues": [...],
  "links": [...]
}
```

### 3.2 `execution/` (GitHub Actions + helpers)

Since this `.github` repo houses cross-org workflows, we introduce an `execution/` folder with:

- `execution/actions/provision-project/` – Composite Action that:
  1. Checks out target repo (if different) and downloads plan artefacts.
  2. Uses a small Python helper (`execution/scripts/provision_project.py`) to call GitHub GraphQL (Create/Update ProjectV2, CreateProjectV2Field, AddProjectV2ItemById, AddSubIssue, UpdateProjectV2ItemFieldValue). Handles pagination, retries, and dry-run.
  3. Uploads results & evidence.
- `execution/workflows/provision-project.yml` – Reusable workflow that orchestrates: validate → plan (`spectra project plan`) → apply (composite action). Accepts inputs for manifest path, mode (plan/apply/destroy), force-new-project, etc.
- `execution/docs/provisioning.md` – Usage guide covering triggers, required secrets (GitHub App), and example consumer workflow snippet.

## 4. Data & Control Flow

```
Repo manifest (config/projects/*.yml)
          │
          │ 1. Validate + Plan (spectra CLI — file only)
          ▼
.plan.json + summary under .spectra/output
          │
          │ 2. Apply (execution workflow w/ GitHub App token)
          ▼
GitHub Project fields, views, issues, hierarchy, assignments
```

Steps in detail:

1. **Validate:** `spectra project plan` checks schema, stage order, dependency references, label/milestone mapping.
2. **Emit plan:** CLI writes `plan.json`, `plan.md`, checksum, and optional diff against previous plan for reproducibility.
3. **Apply plan:** Composite action reads plan sequentially and invokes GitHub GraphQL mutations. Supports `--dry-run` and `--apply` modes, preserving `planOnly` semantics.
4. **Evidence:** Workflow uploads `.spectra/output/project/<slug>` as artifact; also stores condensed summary in `.spectra/evidence/project-provisioning/latest.json`.
5. **Idempotence:** Each op compares desired state vs actual (e.g., field option colours, view filters). Issues rely on title + parent metadata; sub-issues created via `addSubIssue`.

## 5. GitHub API Surface

- `CreateProjectV2`, `UpdateProjectV2` – project container.
- `CreateProjectV2Field`, `UpdateProjectV2Field`, `DeleteProjectV2Field` – fields.
- `CreateProjectV2View`, `UpdateProjectV2View`.
- `AddProjectV2ItemById`, `ArchiveProjectV2Item`.
- `CreateIssue`, `UpdateIssue`, `AddSubIssue` – backlog items.
- `UpdateProjectV2ItemFieldValue`, `ClearProjectV2ItemFieldValue` – field assignments.

All queries/mutations implemented in a thin helper (`execution/scripts/github_projects.py`) with cursor-based pagination utilities.

## 6. Observability & Governance

- **Spectrafy Integration:** plan/apply stages append evidence (JSON + Markdown) to `.spectra/evidence/project-provisioning/`. The audit script can ingest these to adjust automation scores.
- **Job Summaries:** Each workflow run writes a GitHub Step Summary (counts created/updated/skipped, links to created project/board).
- **Logging:** Structured log lines (`provision.project.event=project-created`, `issue-linked=true`, etc.) for easy Kibana ingestion.

## 7. Migration Strategy

| Phase | Description |
| --- | --- |
| 1. Scaffolding | Add framework CLI scaffolding + schemas + tests. Create composite action + helper scripts with dry-run mode. No consumer workflows yet. |
| 2. Pilot | Point `operations` repo at new reusable workflow in plan-only mode. Compare plan outputs with legacy script. Iterate until diff-only noise resolved. |
| 3. Cutover | Switch `operations` repo workflow to `apply` mode. Keep legacy script around but disabled. Monitor evidence & Spectrafy scores. |
| 4. Cleanup | Remove old `bootstrap-project-backlog.yml` and `scripts/simple_project_bootstrap.py`. Update docs + DEPRECATED_WORKFLOWS. |

## 8. Open Questions

1. **Manifest ownership:** Should manifests stay in each functional repo (e.g., `Core/operations`) or centralise inside Data? (Assumed: stay local, CLI respects relative paths.)
2. **Field templates:** Do we need a registry of shared Project field definitions to avoid duplication? (Proposed: yes, via schema referencing `config/projects/schemas/<name>/fields.json`).
3. **Secret scoping:** Confirm which GitHub App (Spectra Assistant vs new automation) should mint tokens.

## 9. Next Steps

1. Create `execution/` scaffolding (composite action, scripts, docs) in this repo.
2. Update `framework` repo with schema + CLI commands (separate PR in that repo).
3. Build reusable workflow referencing new composite action, with inputs for manifest path + mode.
4. Pilot in `Core/operations` (plan-only) and capture evidence.

---

This blueprint will stay in the `.github` repo and act as the contract for implementation work across repos. Feedback welcome before coding begins.
