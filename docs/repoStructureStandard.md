# 🏗️ SPECTRA Repository Structure Standard (Pillar → Domain → Capability → Service)

Purpose
Defines the mandatory repository structure, navigation metadata, and governance rules for every SPECTRA repository.

Scope

- Applies to all repositories under SPECTRADataSolutions
- Enforced by the reusable repo-structure-guard workflow in this repo
- British English and camelCase everywhere

Required README Navigation Header (top of README.md)
Use the nav block; values must be accurate.

<!-- NAV_START -->
**Dream**: SPECTRA
**Pillar**: Guidance | Innovation | Engagement | Execution | Protection | Sustenance | Growth
**Domain**: <singleTokenCamelCase>
**Capability**: <singleTokenCamelCase>
**Service**: <serviceName or owner/repo>
<!-- NAV_END -->

Repository Types and Folder Maps
All repos satisfy "Common", then add type-specific folders.

- Common: docs/, scripts/, tests/, meta/, .github/workflows/
- Engineering: stages/, utils/, principles/, conventions/, Tables/
- Execution: templates/, scripts/, docs/
- Applications: src/, components/, pages/ or app/, styles/
- Governance: roles/, contracts/, specs/, tools/
- Content: knowledge/, journal/, discussions/, templates/

Compliance and Enforcement

Inline validation workflows now perform structure and navigation checks:

- Nav header (Dream=SPECTRA, Pillar, Domain, Capability, Service)
- Required root files
- British English cues
- Baseline folders & .gitignore essentials
- Type-specific folders (if repoType provided)

Adoption (per-repo)

```yaml
name: repoStructureGuard
on:
  pull_request:
  push:
    branches: [ main, master, develop ]
jobs:
  validate:
    uses: SPECTRADataSolutions/framework/.github/workflows/validate-repository-structure.yml@main
    with:
      repoType: engineering
```

Notes

- "Service" can be a simple serviceName (camelCase) or owner/repo.
- Keep Dream in the header; it must be SPECTRA.
