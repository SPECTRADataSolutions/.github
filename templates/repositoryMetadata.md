# Repository Metadata Template

Copy this template to `.spectra/metadata.yml` in your repository root.

```yaml
# .spectra/metadata.yml
# SPECTRA Canonical Organisational Structure Metadata
# This file defines the repository's position in the Spectrafied 7×7×7 hierarchy:
# Pillar → Domain → Capabilities → Repository

pillar: [CHOOSE_ONE: Protection|Guidance|Growth|Engagement|Innovation|Sustenance|Execution]
domain: [SINGLE_WORD_CAMELCASE_DOMAIN]
capabilities: [SINGLE_WORD_CAMELCASE_CAPABILITIES]
repository: [REPOSITORY_NAME]

# Spectrafied 7×7×7 Pillar-Domain Mapping Reference:
# 
# Protection: security, compliance, privacy, resilience, risk, safety, assurance
# Guidance: vision, leadership, navigation, ethics, governance, alignment, decision
# Growth: learning, scaling, adaptation, performance, talent, opportunity, progression
# Engagement: community, communication, partnerships, participation, culture, reputation, inclusion
# Innovation: creativity, research, technology, transformation, design, experimentation, invention
# Sustenance: resources, energy, provision, maintenance, logistics, support, capacity
# Execution: process, delivery, operations, precision, efficiency, method, output
```

## README Section Template

Add this section to your repository's README.md:

```markdown
## 🏛️ Organisational Structure
**Pillar:** [Your Pillar]  
**Domain:** [yourDomain]  
**Capabilities:** [yourCapabilities]  
**Repository:** [repository-name]

This repository is part of SPECTRA's Spectrafied 7×7×7 organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
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
      capabilities: [yourCapabilities]
      repository: ${{ github.event.repository.name }}
```

## Example Implementation

For a repository in the Guidance pillar with governance domain:

```yaml
# .spectra/metadata.yml
pillar: Guidance
domain: governance
capabilities: framework
repository: .github
```

```markdown
## 🏛️ Organisational Structure
**Pillar:** Guidance  
**Domain:** governance  
**Capabilities:** framework  
**Repository:** .github

This repository is part of SPECTRA's Spectrafied 7×7×7 organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```