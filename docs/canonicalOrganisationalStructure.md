# 🏛️ Canonical Organisational Structure

## Overview

This document defines SPECTRA's authoritative organisational structure based on **Pillars → Domains → Capabilities → Repositories**. This canonical structure ensures consistent classification, governance, and automated enforcement across all repositories.

## 📋 Hierarchy Definition

### Pillars
High-level capability categorisations that represent fundamental organisational functions, designed around human brain activity patterns:

- **Guidance** - Standards, policies, documentation, training, compliance, frameworks
- **Innovation** - Research, experimentation, prototyping, emerging technologies, futures  
- **Engagement** - Community, partnerships, communication, outreach, collaboration
- **Operations** - Infrastructure, deployment, monitoring, automation, maintenance
- **Sustenance** - Maintenance, support, optimisation, performance, reliability
- **Protection** - Security, privacy, compliance, risk management, auditing, recovery
- **Growth** - Expansion, acquisition, scaling, development, enhancement, evolution

#### CEO Experience Pillar Ordering
For the CEO experience interface, pillars are arranged in a semi-circle layout based on human brain activity patterns:
**Protection, Sustenance, Innovation, Operations, Engagement, Growth, Guidance**

#### Executive Identification
Executives are identified by canonical pillar names only. **C*O acronyms are legacy aliases and must not be used operationally.**

**Legacy Aliases (NOT for operational use):**
- CFO → use **Guidance** (canonical)
- CTO → use **Innovation** (canonical)
- CMO → use **Engagement** (canonical)
- COO → use **Operations** (canonical)
- CSO → use **Protection** (canonical)
- CDO → use **Sustenance** (canonical)
- CEO → use **Growth** (canonical)
- CIO, CKO, CAO, COS → use appropriate canonical pillar

### Domains
Single-word camelCase domains that are pertinent to their parent pillar:

#### Guidance Domains
- `governance`, `standard`, `structure`, `intelligence`

#### Innovation Domains  
- `research`, `design`, `architecture`, `engineering`

#### Engagement Domains
- `brand`, `marketing`, `messaging`, `media`, `network`, `developer`

#### Operations Domains
- `coordination`, `schedule`, `response`, `delivery`

#### Sustenance Domains
- `infrastructure`, `platform`, `pipeline`, `reliability`, `support`, `maintenance`

#### Protection Domains
- `security`, `compliance`, `risk`, `safety`, `ethic`, `privacy`

#### Growth Domains
- `finance`, `collaboration`, `acquisition`, `insight`, `revenue`

### Capabilities
Single-word camelCase capabilities that represent specific functional areas within each domain.

### Repositories
Individual GitHub repositories following standard naming conventions.

## 🔧 Implementation Requirements

### Repository Metadata
Every repository must declare its organisational position in machine-readable format:

```yaml
# .spectra/metadata.yml
pillar: Guidance
domain: governance
capabilities: framework
repository: .github
```

### README Declaration
Every repository README must include the organisational hierarchy:

```markdown
## 🏛️ Organisational Structure
**Pillar:** Guidance  
**Domain:** governance  
**Capabilities:** framework  
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
      pillar: Guidance
      domain: governance
      capabilities: framework
```

### CI Enforcement Rules
- **Schema Validation**: All metadata must conform to `contracts/orgStructureMetadata.json`
- **Naming Conventions**: Domains must be single-word camelCase
- **Pertinence Check**: Domains must be valid for their pillar
- **Completeness**: All levels must be declared

## 📚 Governance Rules

### Framework Authority
- **frameworkIsLaw**: No local variations permitted
- **britishEnglish**: All documentation uses British spelling
- **camelCase**: Consistent naming conventions throughout
- **canonicalSetsChangeByGovernanceOnly**: Archetype and domain enumerations require governance approval

### Change Management
1. **Pillar Changes**: Require leadership approval and organisation-wide impact assessment
2. **Domain Changes**: Must demonstrate pertinence to pillar and avoid naming conflicts
3. **Repository Migration**: Follow structured playbooks and validation checklists

## 🎯 Success Indicators

- ✅ 100% repositories declare pillar/domain in machine-readable metadata and README
- ✅ 0 non-pertinent domain assignments post-migration (CI + spot checks)
- ✅ CI blocks merge on invalid pillar/domain/single-word rule violations
- ✅ Quarterly stewardship review cadence established

## 🛠️ Migration Guide

### For Existing Repositories
1. **Assess Current State**: Identify existing metadata patterns
2. **Classify Repository**: Determine appropriate pillar and domain
3. **Add Metadata**: Create `.spectra/metadata.yml` with organisational structure
4. **Update README**: Add organisational structure section
5. **Configure CI**: Integrate org-structure-validator workflow
6. **Validate**: Run validation and fix any issues

### Repository Metadata Pattern
```yaml
# .spectra/metadata.yml
pillar: [Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth]
domain: [pertinent single-word camelCase domain]
capabilities: [single-word camelCase capabilities]
repository: [repository-name]
```

### README Snippet Template
```markdown
## 🏛️ Organisational Structure
**Pillar:** [Your Pillar]  
**Domain:** [yourDomain]  
**Capabilities:** [yourCapabilities]  
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