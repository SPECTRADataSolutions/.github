# SPECTRA Context Server Foundation

This documentation outlines the governance foundation for the SPECTRA context server initiative, establishing the contracts, workflows, and compliance mechanisms that enforce "Framework is Law" principles.

## 🏛️ Governance Architecture

### Contract Schemas

The context server is governed by JSON Schema contracts located in `contracts/context/`:

- **`contextManifest.json`** - Declarative manifest schema for repository allowlists, ref pinning, and policies
- **`anchor.json`** - Schema for anchor responses from `spectra.anchor.get` calls
- **`searchResult.json`** - Schema for search responses from `spectra.search.find` calls  
- **`hierarchyResponse.json`** - Schema for organisation hierarchy from `spectra.org.hierarchy` calls
- **`redactionPolicy.json`** - Schema for privacy redaction policies and configuration

### Governance Workflows

Automated workflows ensure continuous compliance:

- **`validate-context-manifest.yml`** - Validates manifest schema, refs, policies on changes
- **`pin-refs-and-checksums.yml`** - Nightly ref pinning and drift detection with auto-issue creation
- **`anchor-reachability-and-size.yml`** - Daily anchor coverage scanning with gap alerting
- **`context-governance.yml`** - Weekly governance health assessment and reporting

## 🔒 Security and Privacy

### Default-Deny Policies

- **Private Repositories**: Default deny access unless explicitly allowlisted
- **Content Logging**: Disabled by default to prevent data leaks
- **Redaction**: Enabled by default with pattern-based sensitive data removal

### Ref Pinning and Integrity

- **Immutable Refs**: All repository references pinned to 40-character SHA hashes
- **Checksum Verification**: SHA-256 checksums for drift detection
- **Automated Drift Alerts**: Initiative issues created within 5 minutes of detected changes

## 📊 Compliance Monitoring

### Coverage SLOs

- **Anchor Reachability**: ≥95% of anchors must be reachable
- **Size Compliance**: All files within configured size limits (default 1MB)
- **Cache Performance**: ≥70% hit rate, p95 latency ≤300ms for ≤100KB files

### Automated Issue Creation

Governance violations automatically create Initiative issues using SPECTRA templates:

- **Drift Detection**: `contextDriftDetection` for checksum mismatches
- **Coverage Gaps**: `anchorCoverageGapRemediation` for reachability issues
- **Governance Health**: `contextGovernanceHealth` for infrastructure problems

## 🎯 Framework Compliance

### SPECTRA Organisational Structure

- **Dream**: SPECTRA
- **Archetype**: Guidance  
- **Domain**: governance
- **Repository**: .github

### British English and camelCase

- All documentation uses British English spelling
- All code and configuration uses camelCase naming
- Schemas enforce naming conventions through pattern validation

## 🔄 Operational Excellence

### Workflow Schedule

- **Nightly**: Ref pinning and checksum updates (2 AM UTC)
- **Daily**: Anchor reachability and size compliance (6 AM UTC)  
- **Weekly**: Governance health assessment (Sunday 8 AM UTC)

### Reporting and Metrics

- Structured logging with requestId for traceability
- No content logging to preserve privacy
- Redaction counters and alerting thresholds
- Governance health reports with recommendations

## 🚀 Implementation Notes

This foundation establishes the governance infrastructure for the context server. The actual server implementation would be deployed in the `SPECTRADataSolutions/context` repository, consuming these contracts and adhering to these policies.

Key implementation repositories:
- **SPECTRADataSolutions/.github** (this repo) - Governance contracts and workflows
- **SPECTRADataSolutions/framework** - Additional compliance contracts
- **SPECTRADataSolutions/organisation** - Hierarchy data source
- **SPECTRADataSolutions/context** - Context server implementation

All components must maintain strict compliance with these governance foundations to ensure the context server operates as a reliable, secure, and auditable source of canonical SPECTRA knowledge.