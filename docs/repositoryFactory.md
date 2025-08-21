# 🏭 SPECTRA Repository Factory

The Repository Factory provides automated creation of new repositories from Initiative issues using slash commands, ensuring all new repositories start with proper organizational structure, canonical labels, and compliance standards per the Spectrafied 7×7×7 canonical organizational structure.

## 🎯 Overview

The Repository Factory enables:
- **Automated Repository Creation**: Create repositories via slash commands or manual workflow dispatch
- **Canonical Structure Compliance**: All repositories follow SPECTRA's Spectrafied 7×7×7 organizational structure
- **Template Integration**: Optional use of template repositories for specific archetypes
- **Governance Automation**: Automatic seeding of labels, topics, metadata, and structure guards

## 🚀 Usage

### Slash Command (Recommended)

Post a comment on any Initiative issue with the following command:

```
/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint
```

### Manual Workflow Dispatch

From the Actions tab, run "generateServiceRepository" and provide the required inputs.

## 📋 Parameters

| Parameter | Required | Format | Description | Example |
|-----------|----------|--------|-------------|---------|
| `repoName` | ✅ | camelCase | Single-token repository name | `governancePolicy`, `userInterface` |
| `domain` | ✅ | camelCase | Single-token domain pertinent to pillar | `governance`, `security`, `analytics` |
| `visibility` | ✅ | `public` or `private` | Repository visibility setting | `private` |
| `templateRepo` | ⭕ | `SPECTRADataSolutions/repoName` | Optional template repository | `SPECTRADataSolutions/blueprint` |
| `pillar` | ⭕ | Canonical pillar name | Organizational pillar (auto-derived if not specified) | `Guidance`, `Protection` |
| `capability` | ⭕ | camelCase | Single-token capability within domain | `framework`, `monitoring` |
| `description` | ⭕ | Text | Repository description | "Security governance and reusable checks" |
| `homepage` | ⭕ | URL | Optional homepage URL | `https://docs.example.com` |

## 📝 Example Commands

### Basic Repository Creation
```bash
# Create a public repository
/create-repo repoName=userDashboard domain=engagement visibility=public

# Create a private repository  
/create-repo repoName=securityAudit domain=protection visibility=private

# Create with full organizational structure
/repo create serviceName --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private --desc "Security governance and reusable checks"
```

### Template-Based Creation
```bash
# Create from organizational template
/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint

# Create service repository from template
/create-repo repoName=apiGateway domain=infrastructure visibility=private templateRepo=SPECTRADataSolutions/service-template
```

## ⚙️ What It Does

When executed successfully, the Repository Factory will:

1. **Create Repository**: Creates repository in SPECTRADataSolutions organization
2. **Apply Template**: Copies content from templateRepo if specified
3. **Seed Structure**: Creates baseline README, .gitignore, and organizational files
4. **Add Metadata**: Creates `.spectra/metadata.yml` with organizational structure
5. **Configure Labels**: Seeds all canonical SPECTRA labels from `.github/labels.json`
6. **Set Topics**: Adds relevant GitHub topics for discoverability
7. **Enable Protection**: Applies basic branch protection rules
8. **Structure Guards**: Enables repo-structure-guard workflow
9. **Post Confirmation**: Comments on Initiative issue with repository URL

## 🏛️ Organizational Structure Compliance

Every created repository automatically includes:

### Required README Navigation Header
```markdown
<!-- NAV_START -->
**Dream**: SPECTRA  
**Pillar**: [Pillar Name]  
**Domain**: [domainName]  
**Capability**: [capabilityName]  
**Service**: [repository-name]
<!-- NAV_END -->
```

### Repository Metadata
```yaml
# .spectra/metadata.yml
pillar: [Protection|Guidance|Growth|Engagement|Innovation|Sustenance|Execution]
domain: [one of 7 domains per pillar]
capabilities: [one of 7 capabilities per domain]
repository: [repository-name]
```

### Organizational Declaration
```markdown
## 🏛️ Organisational Structure
**Pillar:** [Pillar Name]  
**Domain:** [domainName]  
**Capabilities:** [capabilityName]  
**Repository:** [repository-name]

This repository is part of SPECTRA's Spectrafied 7×7×7 organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
```

## ❌ Error Scenarios

### Invalid Repository Name
```bash
/create-repo repoName=user-dashboard domain=engagement visibility=public
```
**Error:** `❌ repoName must be single-token camelCase (e.g., 'governancePolicy')`

### Missing Required Parameter
```bash
/create-repo repoName=userDashboard domain=engagement
```
**Error:** `❌ Missing required parameter: visibility`

### Invalid Template Repository
```bash
/create-repo repoName=test domain=governance visibility=private templateRepo=InvalidOrg/template
```
**Error:** `❌ templateRepo must be from SPECTRADataSolutions organization`

## 🔧 Advanced Configuration

### Branch Protection Rules
All repositories receive automatic branch protection:
- Require pull request reviews before merging
- Dismiss stale PR approvals when new commits are pushed  
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in restrictions

### Label Seeding
Repositories automatically receive all canonical SPECTRA labels from `.github/labels.json`:
- Type labels (feature, bug, enhancement, etc.)
- Priority labels (P0-P3)
- Status labels (blocked, ready, in-progress, etc.)
- Domain-specific labels

### Structure Guard Integration
All repositories include the repo-structure-guard workflow that:
- Validates README navigation headers
- Enforces organizational metadata compliance
- Checks for required files and structure
- Blocks non-compliant changes via CI

## 🛠️ Troubleshooting

### Repository Creation Fails
1. Check organization permissions for the GitHub token
2. Verify repository name doesn't already exist
3. Ensure all required parameters are provided
4. Check template repository exists and is accessible

### Missing Labels or Topics
1. Verify `.github/labels.json` exists and is valid
2. Check organization settings allow topic modifications
3. Re-run the workflow with the same parameters (idempotent)

### Structure Guard Failures
1. Ensure README includes required navigation header
2. Verify `.spectra/metadata.yml` exists with correct format
3. Check organizational structure values are canonical

## 📞 Support

- **Repository Factory Issues**: Create issue in this repository with `repo-factory` label
- **Organizational Structure Questions**: Reference `docs/canonicalOrganisationalStructure.md`
- **Template Problems**: Check template repository accessibility and format
- **Workflow Failures**: Review Actions logs and error messages

---

> 🏛️ **Governance Principle**: The Repository Factory enforces SPECTRA's canonical organizational structure, ensuring every repository starts with proper classification, metadata, and compliance automation from day one.