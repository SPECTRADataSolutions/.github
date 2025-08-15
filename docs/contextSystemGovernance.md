# SPECTRA Context System Governance

This document describes the governance infrastructure for the **spectraContextMcpServer** initiative, which provides canonical SPECTRA knowledge through a Model Context Protocol (MCP) server.

## Overview

The context system enables IDEs and AI agents to access SPECTRA knowledge in a deterministic, auditable manner while enforcing "Framework is Law" principles. This `.github` repository provides the governance contracts, validation workflows, and compliance automation.

## Contract Schemas

### Context Manifest Schema (`contracts/context/contextManifest.json`)
Defines the structure for `contextManifest.yaml` files that configure:
- **Repository allowlists**: Only SPECTRADataSolutions repositories permitted
- **Reference constraints**: Immutable commit SHAs for production, floating refs for development
- **Size limits**: File size (KB) and total cache size (MB) constraints  
- **MIME type allowlists**: Permitted content types for security
- **Privacy settings**: Default-deny private repos, content redaction, no logging
- **Cache configuration**: TTL, LRU eviction, ETag support
- **Rate limiting**: Per-client request limits with exponential backoff

### Anchor Schema (`contracts/context/anchor.json`)
Defines the structure for context anchors served by the MCP server:
- **Identity**: Unique camelCase identifier and human-readable title
- **Repository metadata**: Owner, name, immutable ref, and file path
- **Content information**: MIME type, size, SHA-256 checksum for drift detection
- **SPECTRA metadata**: Pillar/domain classification, searchable tags, applicable roles
- **Cache headers**: ETag, last modified timestamp, TTL
- **Privacy tracking**: Redaction status and metrics (no content logging)

### Search Result Schema (`contracts/context/searchResult.json`)
Defines responses from the `spectra.search.find` endpoint:
- **Query structure**: Text search with metadata filters and pagination
- **Result format**: Ranked results with relevance scores and highlighted snippets
- **Metadata filtering**: By pillar/domain, tags, roles, MIME types
- **Performance metrics**: Query time, cache hit rates, index size

### Hierarchy Response Schema (`contracts/context/hierarchyResponse.json`)
Defines responses from the `spectra.org.hierarchy` endpoint:
- **Organisational structure**: Pillar → Domain → Repository hierarchy
- **Role definitions**: Hierarchical roles with responsibilities and permissions
- **Helper functions**: Role lookup utilities (`roles.list`, `roles.findByTitle`, `roles.pathTo`)
- **Source metadata**: Commit SHA, checksum, and version of `organisation/hierarchy.yaml`

## Governance Workflows

### Manifest Validation (`workflows/validate-context-manifest.yml`)
Reusable workflow that validates `contextManifest.yaml` files:
- **Schema validation**: Ensures manifest structure matches contract
- **SPECTRA compliance**: Enforces owner allowlists and privacy settings
- **Reference validation**: Checks SHA format and warns about floating refs
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