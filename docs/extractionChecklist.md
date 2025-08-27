# SPECTRA Context System Extraction Checklist

This document provides mechanical steps for extracting the SPECTRA Context system from the `.github` repository into an independent `context` repository.

## 🎯 Pre-Extraction Validation

### Prerequisites Checklist

- [ ] **Split trigger criteria met** (see [splitTriggers.md](splitTriggers.md))
- [ ] **Detachment score ≥ 95** (validated via `scripts/computeDetachmentScore.py`)
- [ ] **All governance workflows passing** in past 30 days
- [ ] **No active schema drift issues** or drift resolved
- [ ] **Framework commit up-to-date** in `contracts/schemaMeta.json`
- [ ] **Engineering leadership approval** for extraction

### Technical Readiness

- [ ] **No cross-folder imports** outside `server/` directory
- [ ] **Self-contained configuration** within extracted folders
- [ ] **Independent CI/CD workflows** tested in isolation
- [ ] **API contracts defined** and documented
- [ ] **Database schema migrations** planned (if applicable)

## 🏗️ Repository Setup

### 1. Create Target Repository

```bash
# Create new repository
gh repo create SPECTRADataSolutions/context --public --description "SPECTRA Context System - Anchors, Manifests, and Runtime"

# Clone and set up initial structure
git clone https://github.com/SPECTRADataSolutions/context.git
cd context
```

### 2. Copy Core Directories

```bash
# Copy essential directories from .github repository
cp -r ../.github/anchors ./
cp -r ../.github/manifests ./
cp -r ../.github/server ./
cp -r ../.github/governance ./
cp -r ../.github/contracts ./
```

### 3. Copy Documentation

```bash
# Copy context-specific documentation
mkdir -p docs
cp ../.github/docs/splitTriggers.md ./docs/
cp ../.github/docs/extractionChecklist.md ./docs/
cp ../.github/docs/contextSystemGovernance.md ./docs/
```

### 4. Set Up Project Files

```bash
# Create README
cat > README.md << 'EOF'
# SPECTRA Context System

**Pillar:** Guidance
**Domain:** structure

This repository contains the SPECTRA Context system, providing anchors, manifests, and runtime services for organisational knowledge management.

## 🏛️ Spectral Panel

| Metric | Status |
|--------|--------|
| **Schema Commit** | `abc123...` |
| **Anchors Count** | 1 |
| **Drift Status** | ✅ Up to date |
| **Split Ready** | ✅ Extracted |
| **Detachment Score** | 100 |
| **Delight Mode** | 🌟 Enabled |

[... rest of README content ...]
EOF

# Create basic package.json for tooling
cat > package.json << 'EOF'
{
  "name": "@spectra/context",
  "version": "1.0.0",
  "description": "SPECTRA Context System",
  "scripts": {
    "validate": "npm run validate:anchors && npm run validate:manifests",
    "validate:anchors": "ajv validate -s contracts/context/anchor.json -d 'anchors/**/*.json'",
    "validate:manifests": "ajv validate -s contracts/context/contextManifest.json -d 'manifests/**/*.json'",
    "drift:check": "node scripts/checkSchemaDrift.js",
    "detachment:score": "python scripts/computeDetachmentScore.py"
  },
  "devDependencies": {
    "ajv-cli": "^5.0.0"
  }
}
EOF
```

## 🔧 Workflow Migration

### 1. Move GitHub Actions

```bash
# Create .github/workflows directory
mkdir -p .github/workflows

# Copy governance workflows
cp ../governance/workflows/schema-drift-check.yml .github/workflows/
cp ../governance/workflows/validate-content.yml .github/workflows/

# Update workflow paths and references
sed -i 's|governance/workflows/|.github/workflows/|g' .github/workflows/*.yml
```

### 2. Update Workflow References

```bash
# Update repository references in workflows
sed -i 's|SPECTRADataSolutions/\.github|SPECTRADataSolutions/context|g' .github/workflows/*.yml

# Update path filters for new repository structure
sed -i 's|contracts/context/|contracts/|g' .github/workflows/*.yml
```

### 3. Create CODEOWNERS

```bash
cat > CODEOWNERS << 'EOF'
# SPECTRA Context System Code Ownership

# Global ownership
* @SPECTRADataSolutions/context-maintainers

# Server runtime requires stricter review
/server/ @SPECTRADataSolutions/runtime-reviewers @SPECTRADataSolutions/context-maintainers

# Governance and contracts require architecture review
/governance/ @SPECTRADataSolutions/architecture-reviewers
/contracts/ @SPECTRADataSolutions/architecture-reviewers

# Documentation can be reviewed by maintainers
/docs/ @SPECTRADataSolutions/context-maintainers
EOF
```

## 📊 Configuration Updates

### 1. Update Schema Metadata

```bash
# Update schemaMeta.json with extraction timestamp
python -c "
import json
from datetime import datetime

with open('contracts/schemaMeta.json', 'r') as f:
    meta = json.load(f)

meta['metadata']['extractedAt'] = datetime.utcnow().isoformat() + 'Z'
meta['metadata']['extractedFrom'] = 'SPECTRADataSolutions/.github'
meta['metadata']['repository'] = 'SPECTRADataSolutions/context'

with open('contracts/schemaMeta.json', 'w') as f:
    json.dump(meta, f, indent=2)
"
```

### 2. Update Anchor References

```bash
# Update repository references in all anchor files
find anchors/ -name "*.json" -exec sed -i 's|"name": "\.github"|"name": "context"|g' {} \;
```

## 🧪 Testing and Validation

### 1. Run Local Validation

```bash
# Install dependencies
npm install

# Run all validations
npm run validate

# Check detachment score
npm run detachment:score

# Test schema drift detection
npm run drift:check
```

### 2. Test Workflows

```bash
# Create test commit to trigger workflows
git add .
git commit -m "Initial context system extraction"
git push origin main

# Monitor workflow execution in GitHub Actions
gh workflow list
gh run list --limit 5
```

### 3. Validation Checklist

- [ ] **All workflows passing** in new repository
- [ ] **Schema validation working** for anchors and manifests
- [ ] **Drift detection operational** with correct framework references
- [ ] **Content validation** catching errors appropriately
- [ ] **Detachment score** reporting correctly

## 🔄 Source Repository Updates

### 1. Remove Extracted Content

```bash
# In .github repository, remove extracted directories
cd ../.github
git rm -r anchors/ manifests/ server/ governance/

# Update contracts to reference external context repo
# Keep schemas but add deprecation notice
echo "# Deprecated: Schemas moved to SPECTRADataSolutions/context" > contracts/context/README.md
```

### 2. Update Documentation

```bash
# Update main README to reference external context system
sed -i 's|anchors/|External: [SPECTRADataSolutions/context](https://github.com/SPECTRADataSolutions/context)|g' README.md

# Add migration notice
cat >> README.md << 'EOF'

## 🔄 Context System Migration

The SPECTRA Context system (anchors, manifests, runtime) has been extracted to its own repository:

**📦 [SPECTRADataSolutions/context](https://github.com/SPECTRADataSolutions/context)**

This repository now provides organisation-wide GitHub templates and governance, with context-specific functionality managed independently.
EOF
```

### 3. Update Workflows

```bash
# Remove context-specific workflows or update to reference external repo
# Keep governance workflows that apply to .github repository itself
git rm workflows/validate-context-manifest.yml workflows/anchor-reachability-and-size.yml
```

## 🎉 Post-Extraction Tasks

### 1. Communication

- [ ] **Announce extraction** to all contributors
- [ ] **Update documentation** links across organisation repositories
- [ ] **Add context repository** to team access permissions
- [ ] **Update CI/CD integrations** that reference context system

### 2. Monitoring Setup

- [ ] **Configure alerts** for new repository workflows
- [ ] **Set up metrics collection** for context system performance
- [ ] **Monitor adoption** and external access requests
- [ ] **Track detachment score** in original repository (should be N/A)

### 3. 30-Day Transition Period

- [ ] **Parallel monitoring** of both repositories
- [ ] **Gradual migration** of external integrations
- [ ] **Documentation updates** across dependent repositories
- [ ] **Training sessions** for contributors on new workflow

## 🎭 Success Criteria

### Technical Validation

- [ ] **Zero downtime** during extraction process
- [ ] **All functionality preserved** in new repository
- [ ] **Performance maintained** or improved
- [ ] **Security boundaries** properly established

### Operational Validation

- [ ] **Contributors productive** in new repository within 1 week
- [ ] **External consumers** can access context system appropriately
- [ ] **Governance workflows** operating independently
- [ ] **Framework compliance** maintained post-extraction

---

**Extraction Difficulty:** Minimal (designed for easy extraction)
**Estimated Duration:** 4-6 hours
**Rollback Plan:** Revert commits in both repositories, restore directory structure
**Support Contact:** SPECTRA Context system maintainers
