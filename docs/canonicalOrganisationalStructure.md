# 🏛️ Canonical Organisational Structure

## Overview

This document defines SPECTRA's authoritative organisational structure based on **Pillars → Domains → Capabilities → Repositories**. This canonical structure ensures consistent classification, governance, and automated enforcement across all repositories.

## 📋 Hierarchy Definition

### Spectrafied 7×7×7 Organisational Grid

The SPECTRA organisational structure follows a canonical 7×7×7 cube design: 7 pillars × 7 domains × 7 capabilities = 343 atomic elements. Each element is mononym (single word), orthogonal (no overlaps), canonical (universally recognised), pertinent (directly relevant), and elemental (irreducible at this layer).

### Pillars

Seven high-level capability categorisations representing fundamental organisational functions:

1. **Protection** - Security, compliance, privacy, resilience, risk management, safety, assurance
2. **Guidance** - Vision, leadership, navigation, ethics, governance, alignment, decision-making
3. **Growth** - Learning, scaling, adaptation, performance, talent development, opportunity, progression
4. **Engagement** - Community, communication, partnerships, participation, culture, reputation, inclusion
5. **Innovation** - Creativity, research, technology, transformation, design, experimentation, invention
6. **Sustenance** - Resources, energy, provision, maintenance, logistics, support, capacity
7. **Execution** - Process, delivery, operations, precision, efficiency, method, output

#### Pillar Ordering

Pillars are ordered for optimal cognitive load distribution:
**Protection, Guidance, Growth, Engagement, Innovation, Sustenance, Execution**

### Domains

Each pillar contains exactly 7 single-word camelCase domains (49 total):

#### Protection Domains

- `security` - Access control, identity management, defence, monitoring, encryption, firewall, response
- `compliance` - Policy, audit, control, standard, licence, mandate, assessment
- `privacy` - Consent, anonymity, confidentiality, redaction, retention, minimisation, disclosure
- `resilience` - Backup, recovery, continuity, redundancy, failover, tolerance, restoration
- `risk` - Analysis, exposure, likelihood, impact, mitigation, contingency, register
- `safety` - Hazard, health, prevention, equipment, environment, awareness, readiness
- `assurance` - Quality, testing, validation, verification, inspection, certification, guarantee

#### Guidance Domains

- `vision` - Purpose, mission, dream, principle, future, goal, aspiration
- `leadership` - Influence, authority, mentoring, stewardship, accountability, delegation, empowerment
- `navigation` - Plan, roadmap, schedule, milestone, direction, adjustment, foresight
- `ethics` - Fairness, justice, honesty, integrity, responsibility, equity, trust
- `governance` - Charter, constitution, bylaw, oversight, board, rule, statute
- `alignment` - Coherence, integration, balance, synergy, convergence, priority, fit
- `decision` - Choice, option, judgement, resolution, approval, selection, mandate

#### Growth Domains

- `learning` - Training, teaching, study, reflection, mentoring, coaching, practice
- `scaling` - Replication, expansion, standardisation, automation, distribution, integration, acceleration
- `adaptation` - Flexibility, change, response, evolution, redesign, reorganisation, recalibration
- `performance` - Metric, outcome, target, efficiency, result, score, benchmark
- `talent` - Hiring, onboarding, retention, succession, promotion, recognition, reward
- `opportunity` - Market, trend, niche, prospect, lead, opening, advantage
- `progression` - Stage, ladder, pathway, journey, cycle, transition, development

#### Engagement Domains

- `community` - Group, network, forum, association, membership, circle, solidarity
- `communication` - Message, signal, channel, medium, dialogue, broadcast, exchange
- `partnerships` - Alliance, contract, deal, venture, merger, sponsor, agreement
- `participation` - Vote, join, attend, contribute, collaborate, volunteer, engage
- `culture` - Value, norm, custom, practice, ritual, story, symbol
- `reputation` - Brand, image, trust, standing, review, rating, profile
- `inclusion` - Access, equity, diversity, belonging, voice, fairness, opportunity

#### Innovation Domains

- `creativity` - Idea, concept, sketch, vision, draft, imagination, inspiration
- `research` - Hypothesis, experiment, study, evidence, survey, trial, result
- `technology` - System, platform, network, tool, interface, device, software
- `transformation` - Shift, reframe, breakthrough, revolution, disruption, renewal, pivot
- `design` - Form, function, pattern, model, plan, layout, structure
- `experimentation` - Test, iteration, sandbox, assay, beta, pilot, feedback
- `invention` - Discovery, creation, mechanism, solution, product, method, patent

#### Sustenance Domains

- `resources` - Finance, capital, asset, stock, supply, fund, reserve
- `energy` - Fuel, power, current, charge, flow, storage, output
- `provision` - Amenity, delivery, assistance, aid, benefit, grant, allocation
- `maintenance` - Repair, upkeep, servicing, inspection, cleaning, renewal, preservation
- `logistics` - Transport, storage, handling, routing, scheduling, tracking, distribution
- `support` - Help, advice, care, counsel, backing, enablement
- `capacity` - Load, throughput, quota, bandwidth, volume, range, scale

#### Execution Domains

- `process` - Step, method, stage, sequence, cycle, framework, flow
- `delivery` - Product, service, release, shipment, package, outcome, completion
- `operations` - Production, handling, running, activity, execution, dispatch, administration
- `precision` - Accuracy, detail, standard, measure, calibration, tolerance, exactness
- `efficiency` - Speed, cost, waste, lean, productivity, economy, optimisation
- `method` - Approach, technique, tactic, procedure, practice, model, style
- `output` - Result, effect, artefact, deliverable, unit, value, yield

### Capabilities

Each domain contains exactly 7 single-word camelCase capabilities (343 total). Capabilities represent atomic, irreducible functional units within their domain context.

### Repositories

Individual GitHub repositories classified within the 7×7×7 structure following standard naming conventions.

## 🔧 Implementation Requirements

### Repository Metadata

Every repository must declare its organisational position in machine-readable format using the Spectrafied 7×7×7 structure:

```yaml
# .spectra/metadata.yml
pillar: [Protection|Guidance|Growth|Engagement|Innovation|Sustenance|Execution]
domain: [one of 7 domains per pillar]
capabilities: [one of 7 capabilities per domain]
repository: [repository-name]
```

**Example:**

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

This repository is part of SPECTRA's Spectrafied 7×7×7 organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```

```

### Issue Template Integration
All issue templates must capture and validate organisational metadata through structured forms.

## ⚙️ Automation & Enforcement

### Validation Workflow
Repositories now use the inline workflow `validate-organisation-structure` (centralised logic; reusable variant deprecated). Example minimal workflow already provided in this repository at `.github/workflows/validate-organisation-structure.yml`:

```yaml
name: validate-organisation-structure
on:
  pull_request:
    paths: [".spectra/metadata.yml", "README.md"]
  push:
    paths: [".spectra/metadata.yml", "README.md"]

jobs:
  validate-structure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/github-script@v7
        with:
          script: |
            // See repository workflow for full logic – validates README nav block & metadata coherence
            console.log('Refer to validate-organisation-structure workflow implementation.')
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
5. **Configure CI**: Add / adapt `validate-organisation-structure` workflow
6. **Validate**: Run validation and fix any issues

### Repository Metadata Pattern

```yaml
# .spectra/metadata.yml
pillar: [Guidance|Innovation|Engagement|Execution|Protection|Sustenance|Growth]
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
