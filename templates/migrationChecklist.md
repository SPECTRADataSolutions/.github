# 🛤️ Migration Checklist: Canonical Organisational Structure

Use this checklist to migrate an existing repository to SPECTRA's canonical organisational structure.

## Pre-Migration Assessment

- [ ] **Repository Audit**: Document current metadata, tags, and classification
- [ ] **Stakeholder Review**: Identify repository owners and primary contributors
- [ ] **Dependencies Check**: List repositories that depend on this one
- [ ] **Classification Decision**: Determine appropriate archetype and domain

## Implementation Steps

### 1. Metadata Declaration
- [ ] Create `.spectra/` directory in repository root
- [ ] Add `.spectra/metadata.yml` with organisational structure
- [ ] Validate metadata against schema using `ajv-cli`
- [ ] Ensure domain is single-word camelCase and pertinent to archetype

### 2. Documentation Updates
- [ ] Add "🏛️ Organisational Structure" section to README.md
- [ ] Include Dream → Archetype → Domain → Repository hierarchy
- [ ] Link to canonical structure documentation
- [ ] Update any existing architecture or governance documentation

### 3. CI/CD Integration
- [ ] Add `.github/workflows/org-structure-validation.yml`
- [ ] Configure workflow to use reusable validator
- [ ] Test validation workflow with sample commits
- [ ] Ensure CI blocks invalid metadata changes

### 4. Issue Template Updates
- [ ] Review existing issue templates for metadata requirements
- [ ] Add dream/archetype/domain fields where appropriate
- [ ] Ensure forms validate against canonical structure
- [ ] Test template submission and validation

### 5. Validation & Testing
- [ ] Run organisational structure validator workflow
- [ ] Verify all metadata constraints are enforced
- [ ] Test invalid submissions to confirm blocking
- [ ] Validate README display of organisational hierarchy

## Post-Migration Verification

### Automated Checks
- [ ] ✅ Metadata file validates against JSON schema
- [ ] ✅ Domain follows single-word camelCase format
- [ ] ✅ Domain is pertinent to selected archetype
- [ ] ✅ CI workflow executes successfully
- [ ] ✅ Invalid changes are blocked by validation

### Manual Verification
- [ ] ✅ README clearly displays organisational structure
- [ ] ✅ Documentation links are functional
- [ ] ✅ Repository appears correctly in organisational map
- [ ] ✅ Stakeholders understand new classification
- [ ] ✅ Issue templates capture required metadata

## Quality Assurance

### Compliance Checks
- [ ] **British English**: All documentation uses British spelling
- [ ] **camelCase**: Naming conventions are consistent
- [ ] **Framework Compliance**: No local variations or overrides
- [ ] **Schema Adherence**: Metadata validates against canonical contract

### Governance Validation
- [ ] **Archetype Justification**: Selected archetype aligns with repository purpose
- [ ] **Domain Pertinence**: Domain is relevant and appropriate for archetype
- [ ] **Repository Scope**: Repository content matches declared classification
- [ ] **Future Alignment**: Structure supports planned repository evolution

## Rollback Plan

If migration issues arise:

- [ ] **Immediate Rollback**: Remove `.spectra/metadata.yml` and workflow
- [ ] **Documentation Revert**: Restore original README structure
- [ ] **Issue Logging**: Document problems for governance review
- [ ] **Stakeholder Communication**: Notify affected teams of temporary rollback

## Sign-off Requirements

### Technical Validation
- [ ] **CI/CD Engineer**: Workflow configuration and validation
- [ ] **Repository Maintainer**: Metadata accuracy and documentation
- [ ] **Governance Representative**: Compliance with canonical structure

### Business Approval
- [ ] **Domain Owner**: Confirms appropriate domain assignment
- [ ] **Archetype Steward**: Validates archetype classification
- [ ] **Chief of Staff**: Final approval for organisational alignment

## Communication Template

Use this template to notify stakeholders:

```
Subject: Repository Migration to Canonical Organisational Structure

Repository: [REPO_NAME]
Classification: SPECTRA → [ARCHETYPE] → [domain] → [repository]

This repository has been migrated to SPECTRA's canonical organisational structure. 

Key Changes:
- Added .spectra/metadata.yml with organisational classification
- Updated README with hierarchy display
- Integrated validation workflow for compliance enforcement

No breaking changes to functionality. Questions? See documentation:
https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md
```

## Success Metrics

Post-migration, verify these outcomes:

- [ ] **Metadata Completeness**: 100% of required fields populated
- [ ] **Validation Coverage**: CI enforces all structural rules
- [ ] **Documentation Clarity**: Stakeholders understand classification
- [ ] **Governance Compliance**: Repository aligns with framework standards
- [ ] **Operational Continuity**: No disruption to existing workflows

---

> 📋 **Migration Principle**: Systematic, validated migration ensures consistent organisational classification while maintaining operational continuity.