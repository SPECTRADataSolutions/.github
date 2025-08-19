# 🏗️ Service Repository Generation (Pillar → Domain → Capability → Service)

Purpose
Create pillar/domain/capability/service repositories on demand with compliant navigation headers, labels, topics, a repository-structure guard workflow, and an intent manifest.

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
  - Enables repo-structure guard and applies basic branch protection
- Idempotent
  - Safe to retry; re-runs converge the repository to the requested state
</details>

---

## How to use

You can invoke the Service Repository Generator in two ways. Both accept the same logical inputs.

### 1) Comment on an Initiative issue (recommended)

Post a slash command on any issue labelled `type:initiative`:

```
/repo create governancePolicy --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
```

**Parameters:**
- `repoName` (required): camelCase service name that becomes the repository name
- `--pillar` (required): One of Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth
- `--domain` (required): Single-token camelCase (e.g. platformSecurity)
- `--capability` (required): Single-token camelCase (e.g. threatDetection)
- `--type` (required): One of engineering|operations|applications|governance|content
- `--visibility` (optional): public or private (default: private)
- `--desc` (optional): Short description of purpose and scope

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

When triggered, the Service Repository Generator will:

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

- **repoName**: Service name in camelCase — will become repository name
- **pillar**: Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth
- **domain**: Single-token camelCase (e.g. platformSecurity)
- **capability**: Single-token camelCase (e.g. threatDetection)
- **repoType**: engineering|operations|applications|governance|content
- **visibility**: public or private (default: private)
- **description**: Short description of purpose and scope
- **homepage**: Optional homepage URL

---

## Requirements

- **ORG_ADMIN_TOKEN** secret must be configured with organisation administration permissions
- Requester must be a member of SPECTRADataSolutions organisation (slash command version only)
- All inputs must follow naming conventions (camelCase for names, valid pillar/type selections)

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

### Example 1: Security governance repository
```
/repo create securityGovernance --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
```

### Example 2: Data engineering pipeline
```
/repo create dataPipeline --pillar Innovation --domain dataEngineering --capability pipelineOrchestration --type engineering --visibility public --desc "Reusable data pipeline components"
```

### Example 3: User interface application
```
/repo create adminPortal --pillar Engagement --domain userExperience --capability interfaceDesign --type applications --visibility private --desc "Administrative portal for platform management"
```

---

## Troubleshooting

- **Missing permission**: Ensure ORG_ADMIN_TOKEN is configured as an organisation secret and available to this workflow.
- **Name collisions**: If a repository with the same name exists, the generator will reconcile files and settings rather than failing.
- **Invalid inputs**: The bot will comment with a clear failure reason. Fix inputs and re-run.
- **Branch protection API errors**: Best-effort rules are applied; if an organisation policy blocks specific settings, the workflow continues and reports the deviation.

---

## Design notes

- Idempotent by design, so you can "apply" changes repeatedly.
- Clear separation of concerns: creation, seeding, labelling, topics, protection.
- Metadata-first: meta/intent.yml is the single source of truth for P → D → C → S.
- British English and camelCase conventions enforced throughout.
- Three-word, verb-first naming convention: generateServiceRepository.