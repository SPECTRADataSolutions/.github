# 🏛️ Canonical Organisational Structure

## Overview

This document defines SPECTRA's authoritative 4-level hierarchical organisational structure: **Dream → Archetype → Domain → Repository**. This canonical structure ensures consistent classification, governance, and automated enforcement across all repositories.

## 📋 Hierarchy Definition

### Level 1: Dream
**SPECTRA** - The overarching organisational vision and aspiration that drives all activities.

### Level 2: Archetype
High-level capability categorisations that represent fundamental organisational functions:

- **Guidance** - Standards, policies, documentation, training, compliance, frameworks
- **Innovation** - Research, experimentation, prototyping, emerging technologies, futures
- **Engagement** - Community, partnerships, communication, outreach, collaboration
- **Operations** - Infrastructure, deployment, monitoring, automation, maintenance
- **Protection** - Security, privacy, compliance, risk management, auditing, recovery
- **Sustenance** - Maintenance, support, optimisation, performance, reliability
- **Growth** - Expansion, acquisition, scaling, development, enhancement, evolution

#### Executive Identification
Executives are identified by canonical archetype names only. **C*O acronyms are legacy aliases and must not be used operationally.**

**Legacy Aliases (NOT for operational use):**
- CFO → use **Guidance** (canonical)
- CTO → use **Innovation** (canonical)
- CMO → use **Engagement** (canonical)
- COO → use **Operations** (canonical)
- CSO → use **Protection** (canonical)
- CDO → use **Sustenance** (canonical)
- CEO → use **Growth** (canonical)
- CIO, CKO, CAO, COS → use appropriate canonical archetype

### Level 3: Domain
Single-word camelCase domains that are pertinent to their parent archetype:

#### Guidance Domains
- `governance`, `standards`, `documentation`, `training`, `compliance`, `frameworks`, `policies`

#### Innovation Domains  
- `research`, `experimentation`, `prototyping`, `emerging`, `futures`, `ideation`, `discovery`

#### Engagement Domains
- `community`, `partnerships`, `communication`, `outreach`, `collaboration`, `relationships`, `networking`

#### Operations Domains
- `infrastructure`, `deployment`, `monitoring`, `automation`, `maintenance`, `support`, `tooling`

#### Protection Domains
- `security`, `privacy`, `compliance`, `risk`, `auditing`, `backup`, `recovery`

#### Sustenance Domains
- `maintenance`, `support`, `optimization`, `performance`, `reliability`, `scalability`, `efficiency`

#### Growth Domains
- `expansion`, `acquisition`, `scaling`, `development`, `enhancement`, `evolution`, `advancement`

### Level 4: Repository
Individual GitHub repositories following standard naming conventions.

## 🔧 Implementation Requirements

### Repository Metadata
Every repository must declare its organisational position in machine-readable format:

```yaml
# .spectra/metadata.yml
dream: SPECTRA
archetype: Guidance
domain: governance
repository: .github
```

### README Declaration
Every repository README must include the organisational hierarchy:

```markdown
## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** Guidance  
**Domain:** governance  
**Repository:** .github
```

### Issue Template Integration
All issue templates must capture and validate organisational metadata through structured forms.

## ⚙️ Automation & Enforcement

### Reusable Validator Workflow
Use the organisation-wide validator in your repository workflows:

```yaml
name: Validate Organisational Structure
on: [push, pull_request]

jobs:
  validate:
    uses: SPECTRADataSolutions/.github/.github/workflows/org-structure-validator.yml@main
    with:
      dream: SPECTRA
      archetype: Guidance
      domain: governance
```

### CI Enforcement Rules
- **Schema Validation**: All metadata must conform to `contracts/orgStructureMetadata.json`
- **Naming Conventions**: Domains must be single-word camelCase
- **Pertinence Check**: Domains must be valid for their archetype
- **Completeness**: All four levels must be declared

## 📚 Governance Rules

### Framework Authority
- **frameworkIsLaw**: No local variations permitted
- **britishEnglish**: All documentation uses British spelling
- **camelCase**: Consistent naming conventions throughout
- **canonicalSetsChangeByGovernanceOnly**: Archetype and domain enumerations require governance approval

### Change Management
1. **Archetype Changes**: Require leadership approval and organisation-wide impact assessment
2. **Domain Changes**: Must demonstrate pertinence to archetype and avoid naming conflicts
3. **Repository Migration**: Follow structured playbooks and validation checklists

## 🎯 Success Indicators

- ✅ 100% repositories declare dream/archetype/domain in machine-readable metadata and README
- ✅ 0 non-pertinent domain assignments post-migration (CI + spot checks)
- ✅ CI blocks merge on invalid archetype/domain/single-word rule violations
- ✅ Quarterly stewardship review cadence established

## 🛠️ Migration Guide

### For Existing Repositories
1. **Assess Current State**: Identify existing metadata patterns
2. **Classify Repository**: Determine appropriate archetype and domain
3. **Add Metadata**: Create `.spectra/metadata.yml` with organisational structure
4. **Update README**: Add organisational structure section
5. **Configure CI**: Integrate org-structure-validator workflow
6. **Validate**: Run validation and fix any issues

### Repository Metadata Pattern
```yaml
# .spectra/metadata.yml
dream: SPECTRA
archetype: [Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth]
domain: [pertinent single-word camelCase domain]
repository: [repository-name]
```

### README Snippet Template
```markdown
## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** [Your Archetype]  
**Domain:** [yourDomain]  
**Repository:** [repository-name]

This repository is part of SPECTRA's canonical organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/docs/canonicalOrganisationalStructure.md).
```

## 📞 Support & Governance

- **Schema Questions**: Reference `contracts/orgStructureMetadata.json`
- **Classification Help**: Create issue with `@copilot` assignment
- **Change Requests**: Follow governance approval process
- **Validation Issues**: Check CI logs and validator workflow

---

> 🏛️ **Governance Principle**: This structure provides the foundational taxonomy for all SPECTRA operations, enabling consistent classification, automated governance, and clear organisational visibility.