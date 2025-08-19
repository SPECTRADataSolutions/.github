# 🏗️ SPECTRA Service Repository Generation

Automated creation of pillar/domain/capability/service repositories with compliant navigation headers, labels, topics, structure guard workflows, and intent manifests.

<details>
<summary>At a glance</summary>

- Triggers
  - Slash comment on an Initiative issue (recommended)
  - Manual workflow dispatch in Actions
- Inputs
  - repoName, pillar, domain, capability, repoType, visibility, description, homepage (optional)
- Effects
  - Creates or updates a repository in the SPECTRADataSolutions organisation
  - Seeds README, .gitignore, labels, topics, meta/intent.yml
  - Enables repoStructureGuard and applies basic branch protection
- Idempotent
  - Safe to retry; re-runs converge the repository to the requested state
</details>

---

## How to use

You can invoke the service repository generator in two ways. Both accept the same logical inputs.

### 1) Comment on an Initiative issue (recommended)

On any Initiative issue, comment with the slash command:

```
/repo create serviceName --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
```

### 2) Run the workflow manually (Actions tab)

From the Actions tab, run "generateServiceRepository" and provide the inputs:

- repoName: securityGovernance
- pillar: Protection
- domain: platformSecurity
- capability: threatDetection
- repoType: governance
- visibility: private
- description: Security governance and reusable checks
- homepage: Optional URL

---

## What it does

When triggered, the service repository generator will:

- Create or update the target repository in the SPECTRADataSolutions organisation.
- Seed a README with the standard navigation header:
  - Dream → Pillar → Domain → Capability → Service
- Add a .gitignore suited to typical Fabric/analytics projects.
- Add and configure the repoStructureGuard reusable workflow (applied on pushes and PRs).
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

- **repoName** (required): Service name in camelCase — will become repository name
- **pillar** (required): Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth
- **domain** (required): Single-token camelCase (e.g. platformSecurity)
- **capability** (required): Single-token camelCase (e.g. threatDetection)
- **repoType** (required): engineering|operations|applications|governance|content
- **visibility** (required): public or private (default: private)
- **description** (required): Short description of purpose and scope
- **homepage** (optional): Optional homepage URL

## Requirements

- **Naming**: All names must follow camelCase conventions
- **Access**: Requires ORG_ADMIN_TOKEN organisation secret for repository creation
- **Idempotency**: Safe to run multiple times against the same repository

## Outputs (what you will see)

- New or updated repository under SPECTRADataSolutions/{repoName}
- README seeded with navigation header and structure overview
- .gitignore present at the repository root
- repoStructureGuard workflow configured
- Labels added/updated to match organisation catalogue
- Topics applied: spectra, framework, pillar-*, domain-*, capability-*
- meta/intent.yml created/updated with pillar/domain/capability/service

---

## Examples

- Governance repository (Protection → platformSecurity → threatDetection → securityGovernance)
  ```
  /repo create securityGovernance --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
  ```

- Service repository for engineering
  ```
  /repo create tatooineIngestion --pillar Guidance --domain dataAcquisition --capability eventStreaming --type engineering --visibility private --desc "Ingests Mos Eisley cantina telemetry"
  ```

---

## Troubleshooting

- Missing permission: Ensure ORG_ADMIN_TOKEN is configured as an organisation secret and available to this workflow.
- Name collisions: If a repository with the same name exists, the generator will reconcile files and settings rather than failing.
- Invalid inputs: The bot will comment with a clear failure reason. Fix inputs and re-run.
- Branch protection API errors: Best-effort rules are applied; if an organisation policy blocks specific settings, the workflow continues and reports the deviation.

---

## Design notes

- Idempotent by design, so you can "apply" changes repeatedly.
- Clear separation of concerns: creation, seeding, labelling, topics, protection.
- Metadata-first: meta/intent.yml is the single source of truth for P → D → C → S.
- British English and camelCase enforced throughout.
- Follows three-word, verb-first naming conventions for all workflows.