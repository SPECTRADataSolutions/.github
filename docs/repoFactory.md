# 📦 Repo Factory (Pillar → Domain → Capability → Service)

Purpose
Create pillar/domain/capability/service repositories on demand with compliant navigation headers, labels, topics, a repository-structure guard workflow, and an intent manifest.

<details>
<summary>At a glance</summary>

- Triggers
  - Slash comment on an Initiative issue (recommended)
  - Manual workflow dispatch in Actions
- Inputs
  - repoName, pillar, domain, capability, repoType, visibility, description, homepage (optional), templateRepo (optional)
- Effects
  - Creates or updates a repository in the SPECTRADataSolutions organisation
  - Seeds README, .gitignore, labels, topics, meta/intent.yml
  - Enables repo-structure guard and applies basic branch protection
- Idempotent
  - Safe to retry; re-runs converge the repository to the requested state
</details>

---

## How to use

You can invoke Repo Factory in two ways. Both accept the same logical inputs.

### 1) Comment on an Initiative issue (recommended)

Post a supported slash command as a top-level comment on a valid Initiative issue in this repository.

- Canonical form (key=value)
  ```
  /create-repo repoName=securityGovernance pillar=Protection domain=platformSecurity capability=threatDetection repoType=governance visibility=private description="Security governance and reusable checks" templateRepo=SPECTRADataSolutions/blueprint
  ```

- Legacy alias (positional, still supported)
  ```
  /repo create security --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
  ```

Notes:
- Use camelCase for repoName, domain, and capability (e.g., platformSecurity, threatDetection).
- If omitted, templateRepo defaults to our standard blueprint.
- The bot reacts to your comment with status emojis and posts a result summary.

### 2) Run the workflow manually (Actions tab)

From the Actions tab, run “repoFactory” and provide the inputs:

- repoName: securityGovernance
- pillar: Protection
- domain: platformSecurity
- capability: threatDetection
- repoType: governance
- visibility: private
- description: Security governance and reusable checks
- homepage: Optional URL
- templateRepo: SPECTRADataSolutions/blueprint (optional when using the comment path; workflow-dispatch variant seeds baseline files if no template is used)

---

## What it does

When triggered, Repo Factory will:

- Create or update the target repository in the SPECTRADataSolutions organisation.
- Seed a README with the standard navigation header:
  - Dream → Pillar → Domain → Capability → Service
- Add a .gitignore suited to typical Fabric/analytics projects.
- Add and configure the repo-structure-guard reusable workflow (applied on pushes and PRs).
- Seed labels from .github/.github/labels.json (this repo).
- Set topics to include:
  - spectra, framework, pillar-<pillar>, domain-<domain>, capability-<capability>
- Add meta/intent.yml capturing P → D → C → S:
  ```yaml
  # meta/intent.yml
  dream: SPECTRA
  pillar: Protection
  domain: platformSecurity
  capability: threatDetection
  service: securityGovernance
  repoType: governance
  visibility: private
  ```
- Apply best-effort protection on the default branch:
  - Require 1 approving review for PRs, dismiss stale approvals on new commits.

All operations are idempotent: re-running will reconcile files, labels, topics, and rules without duplication.

---

## Inputs

- repoName (string, required): Repository name (camelCase).
- pillar (string, required): One of Guidance, Innovation, Engagement, Operations, Protection, Sustenance, Growth.
- domain (string, required): camelCase domain (e.g., platformSecurity).
- capability (string, required): camelCase capability (e.g., threatDetection).
- repoType (string, required): One of engineering, operations, applications, governance, content.
- visibility (string, required): public or private.
- description (string, required): Short repository description.
- homepage (string, optional): Repository homepage URL.
- templateRepo (string, optional in comment flow): Template repository in owner/repo format (e.g., SPECTRADataSolutions/blueprint).

---

## Requirements

- Organisation secret ORG_ADMIN_TOKEN with scopes:
  - repo, admin:org
- This repository must contain:
  - The reusable repo-structure-guard workflow
  - Standard YAML and label seed at .github/.github/labels.json

---

## Outputs (what you will see)

- New or updated repository under SPECTRADataSolutions/{repoName}
- README seeded with navigation header and structure overview
- .gitignore present at the repository root
- repo-structure-guard workflow configured
- Labels added/updated to match organisation catalogue
- Topics applied: spectra, framework, pillar-*, domain-*, capability-*
- meta/intent.yml created/updated with pillar/domain/capability/service

---

## Examples

- Governance repository (Protection → platformSecurity → threatDetection → securityGovernance)
  ```
  /create-repo repoName=securityGovernance pillar=Protection domain=platformSecurity capability=threatDetection repoType=governance visibility=private description="Security governance and reusable checks"
  ```

- Service repository from the blueprint
  ```
  /create-repo repoName=tatooineIngestion pillar=Guidance domain=dataAcquisition capability=eventStreaming repoType=engineering visibility=private description="Ingests Mos Eisley cantina telemetry" templateRepo=SPECTRADataSolutions/blueprint
  ```

---

## Troubleshooting

- Missing permission: Ensure ORG_ADMIN_TOKEN is configured as an organisation secret and available to this workflow.
- Name collisions: If a repository with the same name exists, Repo Factory will reconcile files and settings rather than failing.
- Invalid inputs: The bot will comment with a clear failure reason. Fix inputs and re-run.
- Branch protection API errors: Best-effort rules are applied; if an organisation policy blocks specific settings, the workflow continues and reports the deviation.

---

## Design notes

- Idempotent by design, so you can “apply” changes repeatedly.
- Clear separation of concerns: creation, seeding, labelling, topics, protection.
- Metadata-first: meta/intent.yml is the single source of truth for P → D → C → S.