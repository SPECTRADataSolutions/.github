# 📦 Repo Factory (Pillar → Domain → Capability → Service)

Purpose
Create pillar/domain/capability service repositories on-demand with compliant navigation headers, labels, topics, guard workflow, and intent manifest.

Usage
- Preferred: comment on an issue in this repo:
```
/repo create security --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
```
- Or run the repoFactory workflow manually from the Actions tab with the same inputs.

What it does
- Creates/updates a repository in SPECTRADataSolutions
- Seeds README with nav header (Dream, Pillar, Domain, Capability, Service)
- Adds .gitignore and repoStructureGuard apply workflow
- Seeds labels from .github/.github/labels.json
- Sets topics: spectra, framework, pillar-*, domain-*, capability-*
- Adds meta/intent.yml with P→D→C→S values
- Best-effort main branch protection (1 review)

Requirements
- Org secret ORG_ADMIN_TOKEN (scopes: repo, admin:org)
- This repo must contain the reusable repo-structure-guard workflow and standard YAML

Notes
- Idempotent: re-running updates files/labels safely
- Set repoType per repository to enable type-specific checks