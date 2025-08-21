# 🏛️ SPECTRA Context System Governance

This document describes the governance infrastructure for the SPECTRA Context System, providing canonical SPECTRA knowledge through Model Context Protocol (MCP) servers while enforcing "Framework is Law" principles.

## 🎯 Overview

The SPECTRA Context System enables IDEs and AI agents to access SPECTRA knowledge in a deterministic, auditable manner. This `.github` repository provides the governance contracts, validation workflows, and compliance automation for the entire context ecosystem.

### Key Capabilities
- **Deterministic Knowledge Access**: Immutable reference pinning and checksum validation
- **Privacy-First Design**: Default-deny policies with pattern-based redaction
- **Automated Compliance**: Continuous validation and drift detection
- **Performance Monitoring**: SLO enforcement with automated alerting

## 📋 Contract Schemas

The context system is governed by JSON Schema contracts located in `contracts/context/`:

### Context Manifest Schema (`contextManifest.json`)
Defines the structure for `contextManifest.yaml` files that configure:
- **Repository allowlists**: Only SPECTRADataSolutions repositories permitted
- **Reference constraints**: Immutable commit SHAs for production, floating refs for development
- **Size limits**: File size (KB) and total cache size (MB) constraints  
- **MIME type allowlists**: Permitted content types for security
- **Privacy settings**: Default-deny private repos, content redaction, no logging
- **Cache configuration**: TTL, LRU eviction, ETag support
- **Rate limiting**: Per-client request limits with exponential backoff

### Anchor Schema (`anchor.json`)
Defines the structure for context anchors served by the MCP server:
- **Identity**: Unique camelCase identifier and human-readable title
- **Repository metadata**: Owner, name, immutable ref, and file path
- **Content information**: MIME type, size, SHA-256 checksum for drift detection
- **SPECTRA metadata**: Pillar/domain classification, searchable tags, applicable roles
- **Cache headers**: ETag, last modified timestamp, TTL
- **Privacy tracking**: Redaction status and metrics (no content logging)

### Search Result Schema (`searchResult.json`)
Defines responses from the `spectra.search.find` endpoint:
- **Query structure**: Text search with metadata filters and pagination
- **Result format**: Ranked results with relevance scores and highlighted snippets
- **Metadata filtering**: By pillar/domain, tags, roles, MIME types
- **Performance metrics**: Query time, cache hit rates, index size

### Hierarchy Response Schema (`hierarchyResponse.json`)
Defines responses from the `spectra.org.hierarchy` endpoint:
- **Organisational structure**: Pillar → Domain → Capabilities → Repository hierarchy
- **Role definitions**: Hierarchical roles with responsibilities and permissions
- **Helper functions**: Role lookup utilities (`roles.list`, `roles.findByTitle`, `roles.pathTo`)
- **Source metadata**: Commit SHA, checksum, and version of `organisation/hierarchy.yaml`

### Redaction Policy Schema (`redactionPolicy.json`)
Defines privacy redaction policies and configuration:
- **Pattern-based redaction**: Regex patterns for sensitive data detection
- **Content filtering**: MIME type and size-based redaction rules
- **Audit logging**: Redaction event tracking without content exposure
- **Policy inheritance**: Repository and organization-level policy layering

## ⚙️ Governance Workflows

Automated workflows ensure continuous compliance:

### Manifest Validation (`validate-context-manifest.yml`)
Reusable workflow that validates `contextManifest.yaml` files:
- **Schema validation**: Ensures manifest structure matches contract
- **SPECTRA compliance**: Enforces owner allowlists and privacy settings
- **Reference validation**: Checks SHA format and warns about floating refs
- **Policy enforcement**: Validates redaction and privacy configurations

### Reference Pinning (`pin-refs-and-checksums.yml`)
Nightly automation for immutable reference management:
- **SHA pinning**: Converts floating refs to 40-character commit SHAs
- **Checksum calculation**: Generates SHA-256 checksums for content verification
- **Drift detection**: Compares checksums to detect content changes
- **Auto-issue creation**: Creates Initiative issues within 5 minutes of detected drift

### Anchor Reachability (`anchor-reachability-and-size.yml`)
Daily validation of context anchor availability:
- **Reachability testing**: Validates all anchors are accessible
- **Size compliance**: Ensures files within configured limits
- **Coverage analysis**: Reports anchor availability metrics
- **Gap alerting**: Creates issues for unreachable or oversized content

### Context Governance (`context-governance.yml`)
Weekly governance health assessment:
- **Performance monitoring**: Cache hit rates, latency metrics
- **Security auditing**: Privacy policy compliance verification
- **Coverage reporting**: SLO performance against targets
- **Health scoring**: Overall system health assessment

## 🔒 Security and Privacy

### Default-Deny Policies
- **Private Repositories**: Default deny access unless explicitly allowlisted
- **Content Logging**: Disabled by default to prevent data leaks
- **Redaction**: Enabled by default with pattern-based sensitive data removal
- **Access Control**: Organization membership verification required

### Reference Integrity
- **Immutable Refs**: All repository references pinned to 40-character SHA hashes
- **Checksum Verification**: SHA-256 checksums for drift detection
- **Automated Drift Alerts**: Initiative issues created within 5 minutes of detected changes
- **Audit Trail**: All reference changes logged and tracked

### Privacy Controls
- **Pattern-based Redaction**: Automatic detection and removal of sensitive patterns
- **Content Filtering**: MIME type restrictions and size limitations
- **No Content Logging**: System logs contain metadata only, never content
- **Consent Management**: Explicit allowlisting required for private repository access

## 📊 Compliance Monitoring

### Coverage SLOs
- **Anchor Reachability**: ≥95% of anchors must be reachable
- **Size Compliance**: All files within configured size limits (default 1MB)
- **Cache Performance**: ≥70% hit rate, p95 latency ≤300ms for ≤100KB files
- **Privacy Compliance**: 100% of private repositories must be explicitly allowlisted

### Automated Issue Creation
Governance violations automatically create Initiative issues using SPECTRA templates:
- **Reference Drift**: When checksums detect content changes
- **Reachability Failures**: When anchors become inaccessible
- **Size Violations**: When files exceed configured limits
- **Performance Degradation**: When SLOs are not met

### Reporting and Metrics
- **Weekly Health Reports**: Comprehensive governance status summaries
- **Performance Dashboards**: Real-time metrics on cache performance and availability
- **Security Audits**: Regular privacy and access control verification
- **Compliance Scores**: Quantified governance health metrics

## 🛠️ Implementation Guidelines

### For Context Server Deployments
1. **Manifest Configuration**: Create `contextManifest.yaml` following schema requirements
2. **Reference Pinning**: Use immutable SHA refs for production deployments
3. **Privacy Setup**: Configure redaction policies appropriate for content sensitivity
4. **Monitoring Integration**: Enable governance workflows for continuous compliance

### For Repository Integration
1. **Anchor Declaration**: Define context anchors in repository metadata
2. **Privacy Classification**: Set appropriate access levels for repository content
3. **Size Optimization**: Ensure content files meet size requirements
4. **Metadata Enrichment**: Add SPECTRA organizational metadata for discoverability

## 📞 Support and Governance

### Issue Resolution
- **Schema Questions**: Reference contract specifications in `contracts/context/`
- **Workflow Issues**: Check GitHub Actions logs and workflow documentation
- **Privacy Concerns**: Follow organizational privacy policy and redaction guidelines
- **Performance Problems**: Review SLO dashboards and performance metrics

### Change Management
- **Schema Updates**: Follow governance approval process for contract changes
- **Policy Modifications**: Require organizational approval for privacy policy changes
- **Workflow Enhancements**: Test changes in development environments first
- **Reference Updates**: Use automated pinning workflows for consistency

---

> 🏛️ **Governance Principle**: The SPECTRA Context System provides deterministic, auditable access to canonical knowledge while enforcing privacy-first principles and continuous compliance monitoring.
- **Security checks**: Ensures privacy-first configuration (no content logging, default-deny private)

**Usage:**
```yaml
uses: SPECTRADataSolutions/.github/.github/workflows/validate-context-manifest.yml@main
with:
  manifestPath: "context/config/contextManifest.yaml"
  repository: ${{ github.repository }}
```

### Ref Pinning and Drift Detection (`workflows/pin-refs-and-checksums.yml`)
Automated workflow for maintaining immutable references:
- **Nightly execution**: Runs at 2 AM UTC to convert floating refs to commit SHAs
- **Drift detection**: Validates existing commit SHAs are still accessible
- **Automatic issue creation**: Opens Initiative issues when drift or pinning needed
- **Production safety**: Ensures 100% of production refs are commit SHAs

**Automation:**
- Scheduled: Nightly at 2 AM UTC
- Manual: Workflow dispatch with dry-run option
- Issues: Auto-created using SPECTRA Initiative template

### Anchor Reachability and Size (`workflows/anchor-reachability-and-size.yml`)
Coverage and compliance validation for context anchors:
- **Reachability testing**: Validates all anchor paths are accessible via GitHub API
- **Size compliance**: Checks file sizes against manifest limits
- **Coverage metrics**: Ensures minimum percentage of expected anchors are reachable
- **Gap alerting**: Creates Initiative issues when coverage falls below threshold

**Thresholds:**
- Default coverage: 95% of expected anchors must be reachable
- Size limits: Per manifest configuration (default 1MB files, 50MB total)
- MIME validation: Files must match allowed types

## Framework Enforcement

### Immutable Reference Pinning
- **Production requirement**: All production manifests must use commit SHAs
- **Development flexibility**: Non-production can use `main` branch temporarily
- **Automated conversion**: Nightly workflow pins floating refs to current commit SHAs
- **Drift protection**: Validates commit SHAs remain accessible and unchanged

### SPECTRA-Only Repository Policy  
- **Owner constraint**: Only `SPECTRADataSolutions` organisation permitted
- **Validation**: All workflows enforce owner allowlists
- **Security**: Prevents external dependencies and supply chain risks

### Privacy-First Configuration
- **Default-deny private**: Private repositories blocked unless explicitly allowed
- **No content logging**: Manifest must set `privacySettings.logContent: false`
- **Automatic redaction**: Tokens, emails, and secrets redacted from served content
- **Metrics only**: Only redaction counts logged, never content itself

### Size and Resource Constraints
- **File size limits**: Configurable per-file size caps (default 1MB)
- **Cache size limits**: Total cache size constraints (default 50MB)
- **MIME type filtering**: Only allowed content types served
- **Rate limiting**: Per-client request limits with exponential backoff

## British English and camelCase Standards

All schemas, workflows, and documentation follow SPECTRA conventions:
- **British English**: "optimise", "colour", "behaviour", "organisation"
- **camelCase**: Field names, identifiers, and variables
- **SPECTRA capitalisation**: Always capitalised, never "Spectra" or "spectra"

## Integration with Framework

The context system governance integrates with other SPECTRA repositories:
- **`framework`**: Contracts stored in `framework/contracts/context` (validation schemas)
- **`organisation`**: Role hierarchy from `organisation/hierarchy.yaml`
- **`context`**: Target repository hosting the actual MCP server implementation
- **`.github`**: This repository providing governance automation

## Usage Examples

### Validate a Context Manifest
```bash
# In a repository with contextManifest.yaml
gh workflow run validate-context-manifest.yml \
  -f manifestPath="config/contextManifest.yaml" \
  -f repository="SPECTRADataSolutions/myrepo"
```

### Manual Ref Pinning Check
```bash
# Check for floating refs without creating PRs  
gh workflow run pin-refs-and-checksums.yml \
  -f dryRun=true \
  -f manifestPath="config/contextManifest.yaml"
```

### Coverage Validation
```bash
# Validate anchor reachability with custom threshold
gh workflow run anchor-reachability-and-size.yml \
  -f coverageThreshold=98 \
  -f manifestPath="config/contextManifest.yaml"
```

## Automated Issue Management

When governance violations are detected, workflows automatically create Initiative issues using SPECTRA templates:

### Drift Detection Issues
- **Title**: `🚨 [Initiative] Context Manifest Checksum Drift Detected`
- **Priority**: High
- **Content**: Root cause analysis requirements, resolution steps, affected refs

### Ref Pinning Issues  
- **Title**: `📌 [Initiative] Context Manifest Ref Pinning Required`
- **Priority**: Medium
- **Content**: Floating refs requiring pinning, automation enhancement needs

### Coverage Gap Issues
- **Title**: `📊 [Initiative] Context Anchor Coverage and Size Gap Alert`
- **Priority**: Medium  
- **Content**: Unreachable anchors, oversized files, coverage metrics

All issues include:
- Complete SPECTRA organisational metadata (pillar/domain)
- Capability areas mapped to epic requirements
- Success indicators and constraints
- Dependencies and automation options
- Detailed notes with specific failing items

---

> 🏛️ **Framework is Law**: Context system governance enforces SPECTRA framework standards without exception. Local standards, policy improvisation, and non-SPECTRA dependencies are prohibited.