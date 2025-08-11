# Repository Metadata Template

Copy this template to `.spectra/metadata.yml` in your repository root.

```yaml
# .spectra/metadata.yml
# SPECTRA Canonical Organisational Structure Metadata
# This file defines the repository's position in the 4-level hierarchy:
# Dream → Archetype → Domain → Repository

dream: SPECTRA
archetype: [CHOOSE_ONE: Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth]
domain: [SINGLE_WORD_CAMELCASE_DOMAIN]
repository: [REPOSITORY_NAME]

# Archetype-Domain Mapping Reference:
# 
# Guidance: governance, standards, documentation, training, compliance, frameworks, policies
# Innovation: research, experimentation, prototyping, emerging, futures, ideation, discovery
# Engagement: community, partnerships, communication, outreach, collaboration, relationships, networking
# Operations: infrastructure, deployment, monitoring, automation, maintenance, support, tooling
# Protection: security, privacy, compliance, risk, auditing, backup, recovery
# Sustenance: maintenance, support, optimization, performance, reliability, scalability, efficiency
# Growth: expansion, acquisition, scaling, development, enhancement, evolution, advancement
```

## README Section Template

Add this section to your repository's README.md:

```markdown
## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** [Your Archetype]  
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
      dream: SPECTRA
      archetype: [YOUR_ARCHETYPE]
      domain: [yourDomain]
      repository: ${{ github.event.repository.name }}
```

## Example Implementation

For a repository in the Guidance archetype with governance domain:

```yaml
# .spectra/metadata.yml
dream: SPECTRA
archetype: Guidance
domain: governance
repository: .github
```

```markdown
## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** Guidance  
**Domain:** governance  
**Repository:** .github

This repository is part of SPECTRA's canonical organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```