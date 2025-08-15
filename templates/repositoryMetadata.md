# Repository Metadata Template

Copy this template to `.spectra/metadata.yml` in your repository root.

```yaml
# .spectra/metadata.yml
# SPECTRA Canonical Organisational Structure Metadata
# This file defines the repository's position in the hierarchy:
# Pillar → Domain → Repository

pillar: [CHOOSE_ONE: Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth]
domain: [SINGLE_WORD_CAMELCASE_DOMAIN]
repository: [REPOSITORY_NAME]

# Pillar-Domain Mapping Reference:
# 
# Guidance: governance, standard, structure, intelligence
# Innovation: research, design, architecture, engineering
# Engagement: brand, marketing, messaging, media, network, developer
# Operations: coordination, schedule, response, delivery
# Protection: security, compliance, risk, safety, ethic, privacy
# Sustenance: infrastructure, platform, pipeline, reliability, support, maintenance
# Growth: finance, collaboration, acquisition, insight, revenue
```

## README Section Template

Add this section to your repository's README.md:

```markdown
## 🏛️ Organisational Structure
**Pillar:** [Your Pillar]  
**Domain:** [yourDomain]  
**Repository:** [repository-name]

This repository is part of SPECTRA's canonical organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```

## Workflow Integration Template

Add this workflow to `.github/workflows/org-structure-validation.yml`:

```yaml
name: Organisational Structure Validation

on:
  push:
    paths:
      - '.spectra/metadata.yml'
      - 'README.md'
  pull_request:
    paths:
      - '.spectra/metadata.yml'
      - 'README.md'

jobs:
  validate-structure:
    name: Validate Organisational Metadata
    uses: SPECTRADataSolutions/.github/.github/workflows/org-structure-validator.yml@main
    with:
      pillar: [YOUR_PILLAR]
      domain: [yourDomain]
      repository: ${{ github.event.repository.name }}
```

## Example Implementation

For a repository in the Guidance pillar with governance domain:

```yaml
# .spectra/metadata.yml
pillar: Guidance
domain: governance
repository: .github
```

```markdown
## 🏛️ Organisational Structure
**Pillar:** Guidance  
**Domain:** governance  
**Repository:** .github

This repository is part of SPECTRA's canonical organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```