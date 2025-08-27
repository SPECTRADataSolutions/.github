# 🏗️ SPECTRA Repository Provisioning

This document supersedes the legacy 'Repository Factory' guide. It describes the governed process for creating new repositories with consistent classification, metadata, labels, topics, and baseline compliance automation.

> Legacy path: `repositoryFactory.md` now contains a redirect notice and will be removed after the deprecation window.

## 🎯 Purpose

Provide a single, explicit, self‑describing provisioning workflow (GitHub Actions + optional slash command integration) that:

- Enforces canonical organisational (7×7×7) metadata
- Seeds labels, topics, README, intent manifest, and metadata
- Applies baseline branch protection
- Is idempotent (safe to re-run)
- Authenticates via GitHub App (least privilege)

## 🚀 Invocation

### Manual Dispatch

Use the `repository-provisioning` workflow in the Actions tab and supply required inputs:

- repoName (camelCase)
- pillar (canonical Pillar name)
- domain (camelCase)
- capability (camelCase)
- repoType (engineering|operations|applications|governance|content)
- visibility (public|private)
- description (brief sentence)
- homepage (optional)
- templateRepo (optional org/name inside SPECTRADataSolutions)

### Slash Command (If integrated)

```bash
/create-repo repoName=governancePolicy pillar=Guidance domain=governance capability=framework repoType=governance visibility=private
```

## 🔐 Authentication

Provisioning uses a GitHub App (least privilege). Required secrets:

- SPECTRA_REPOSITORY_PROVISIONING_GITHUB_APP_ID
- SPECTRA_REPOSITORY_PROVISIONING_GITHUB_APP_PRIVATE_KEY
- SPECTRA_REPOSITORY_PROVISIONING_GITHUB_APP_INSTALLATION_ID

The workflow performs a preflight check and fails fast if any are missing.

## 📦 Outputs

- Repository created or confirmed existing
- Seeded README and `meta/intent.yml`
- Canonical labels applied (if labels file present)
- Topics applied: `spectra`, `framework`, pillar/domain/capability tags
- Template contents (if templateRepo provided)

## 🧪 Validation

Input validation enforces camelCase and canonical pillar membership; failures block provisioning and emit a job summary with reasons.

## 🕒 Idempotency

If the repository already exists, provisioning skips creation and continues with seeding steps (labels, metadata, protection), enabling safe re-runs for drift correction.

## 🗄️ Files Seeded

- README.md (navigation header + basic purpose section)
- meta/intent.yml (machine-readable classification)

## 🛡️ Branch Protection

Applies 1 approving review requirement and admin enforcement to `main` (expandable via future policy file).

## 🔄 Migration from Repository Factory

| Aspect | Old | New |
|--------|-----|-----|
| Terminology | Repository Factory | Repository Provisioning |
| Workflow name | generate-repository-service | repository-provisioning |
| Secrets prefix | (removed) SPECTRA_GOV_REPO_FACTORY_* | SPECTRA_REPOSITORY_PROVISIONING_GITHUB_APP_* |
| Doc file | repositoryFactory.md | repositoryProvisioning.md |

Legacy secret fallbacks have been removed; update any environments still referencing the old names.

## 🧩 Future Enhancements

- Policy-driven branch protection matrix
- Additional archetype templates
- Temporal attestation verification of metadata seeds
- SBOM & provenance annotations at creation time

---
Governance Principle: Provisioning must be explicit, reproducible, and policy‑driven; no hidden side effects.
