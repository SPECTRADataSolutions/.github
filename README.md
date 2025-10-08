# 🏛️ SPECTRA Organization Templates and Governance

<!-- NAV_START -->
**Dream**: SPECTRA
**Pillar**: Guidance
**Domain**: governance
**Capability**: framework
**Service**: .github
<!-- NAV_END -->

The central governance repository for SPECTRADataSolutions, providing organization-wide GitHub templates, workflows, and governance automation that enforces the Spectrafied 7×7×7 canonical organizational structure across all repositories.

## 🎯 Purpose

This repository serves as the **framework governance hub** for SPECTRA, providing:

- **Organization Templates**: Issue templates, PR templates, and community health files
- **Reusable Workflows**: Governance automation and compliance validation
- **Canonical Structure**: Authority on the Spectrafied 7×7×7 organizational hierarchy
- **Repository Provisioning**: Automated repository creation with governed classification
- **Governance Automation**: Continuous compliance monitoring and enforcement

## 🏛️ Organisational Structure

**Pillar:** Guidance
**Domain:** governance
**Capabilities:** framework
**Repository:** .github

This repository is part of SPECTRA's Spectrafied 7×7×7 organisational structure. For more information, see [Canonical Organisational Structure](docs/canonicalOrganisationalStructure.md).

## 🌟 Spectrafy Score: 100/100

This repository maintains a perfect detachment score, indicating optimal organization and readiness for framework governance across the entire SPECTRA ecosystem.

## 📁 Repository Structure

.github/                    # Organization-wide GitHub configurations
├── .github/ISSUE_TEMPLATE/ # Standardized issue templates for all repositories
├── .github/workflow-templates/ # Reusable workflow templates for all repositories
├── workflows/              # Governance workflows (legacy or project-specific)

## 🛠️ Usage

- **Issue templates**: Automatically available to all repos in the org from `.github/ISSUE_TEMPLATE/`.
- **Pull request template**: Provided by `PULL_REQUEST_TEMPLATE.md` at the root.
- **Reusable workflow templates**: Reference in your project repo workflows like this:

```yaml
jobs:
 my_job:
  uses: SPECTRADataSolutions/.github/.github/workflow-templates/my-template.yml@main
```

---
├── labels.json           # Canonical label definitions
└── PULL_REQUEST_TEMPLATE.md

docs/                      # Governance documentation
├── canonicalOrganisationalStructure.md  # Authority on 7×7×7 structure
├── repositoryProvisioning.md   # Automated repository creation guide
├── contextSystemGovernance.md           # Context system governance
├── implementationSummary.md             # System implementation overview
└── repoStructureStandard.md            # Repository structure requirements

scripts/                   # Governance automation scripts
├── computeDetachmentScore.py            # Spectrafy score calculator
├── label_readiness.py                   # Initiative readiness assessment
├── repo_factory.py                     # Repository creation automation
└── generate_lessons.py                 # Learning extraction automation

.spectra/                  # Organizational metadata
└── metadata.yml           # Machine-readable organizational classification

```plaintext

.github/                    # Organization-wide GitHub configurations
├── ISSUE_TEMPLATE/        # Standardized issue templates for all repositories
├── workflows/             # Reusable governance workflows
├── labels.json           # Canonical label definitions
└── PULL_REQUEST_TEMPLATE.md

docs/                      # Governance documentation
├── canonicalOrganisationalStructure.md  # Authority on 7×7×7 structure
├── repositoryProvisioning.md   # Automated repository creation guide
├── contextSystemGovernance.md           # Context system governance
├── implementationSummary.md             # System implementation overview
└── repoStructureStandard.md            # Repository structure requirements

scripts/                   # Governance automation scripts
├── computeDetachmentScore.py            # Spectrafy score calculator
├── label_readiness.py                   # Initiative readiness assessment
├── repo_factory.py                     # Repository creation automation
└── generate_lessons.py                 # Learning extraction automation

.spectra/                  # Organizational metadata
└── metadata.yml           # Machine-readable organizational classification
```

## 🚀 Key Features

### 🏗️ Repository Provisioning

Automated repository creation via slash commands with canonical structure compliance:

```bash
/create-repo repoName=governancePolicy domain=governance visibility=private
```

See Repository Provisioning documentation (renamed from Repository Factory; pending file rename) for complete usage guide.

### 🏛️ Canonical Organizational Structure

Enforcement of the Spectrafied 7×7×7 hierarchy:

- **7 Pillars**: Protection, Guidance, Growth, Engagement, Innovation, Sustenance, Execution
- **7 Domains per Pillar**: Specialized functional areas
- **7 Capabilities per Domain**: Atomic operational units
- **343 Total Elements**: Complete organizational coverage

### 📋 Issue Templates

Streamlined, Copilot-friendly templates for efficient issue creation:

- **🐛 Bug Report**: Simple bug reporting with optional severity
- **🌟 Feature Request**: Problem-solution focused development
- **🛠️ Task**: Atomic work units with clear objectives
- **📖 Documentation**: Guides, processes, and knowledge capture
- **❓ Question**: Help requests and clarification
- **🚀 Initiative**: Strategic projects and large efforts

### ⚙️ Reusable Workflows

Organization-wide automation:

- **Organizational Structure Validation**: Ensures canonical compliance
- **Label Seeding**: Maintains consistent labeling across repositories
- **Governance Guards**: Blocks non-compliant changes
- **Context System Validation**: Enforces context governance policies

## 📖 Documentation

### Core Governance

- [**Canonical Organisational Structure**](docs/canonicalOrganisationalStructure.md) - Authority on the 7×7×7 hierarchy
- [**Repository Structure Standard**](docs/repoStructureStandard.md) - Required structure for all repositories
- [**Implementation Summary**](docs/implementationSummary.md) - Complete system overview

### Context System

- [**Context System Governance**](docs/contextSystemGovernance.md) - MCP server governance and contracts
- [**Extraction Checklist**](docs/extractionChecklist.md) - System extraction procedures

### Automation

- [**Repository Provisioning**](docs/repositoryProvisioning.md) - Automated repository creation
- [**Lessons Automation**](docs/lessonsAutomation.md) - Learning extraction and application

## 🛠️ Usage

### For Organization Members

1. **Creating Repositories**: Use the Repository Provisioning workflow via slash commands / dispatch
2. **Creating Issues**: Choose from 6 streamlined templates designed for easy completion
3. **Pull Requests**: Use the simplified PR template focused on essential information
4. **Governance Compliance**: Organizational metadata is now optional and contextual

### For Repository Maintainers

1. **Structure Compliance**: Include required organizational metadata
2. **Label Consistency**: Use canonical labels from `.github/labels.json`
3. **Workflow Integration**: Implement governance validation workflows
4. **Documentation Standards**: Follow established documentation patterns

### For System Administrators

1. **Template Updates**: Modify templates in ISSUE_TEMPLATE directory
2. **Workflow Maintenance**: Update reusable workflows as needed
3. **Governance Monitoring**: Review compliance across repositories
4. **Structure Evolution**: Update canonical structure following governance process

## 🔧 Scripts and Automation

### Detachment Score Calculator (`scripts/computeDetachmentScore.py`)

Calculate the "Spectrafy Score" measuring organizational optimization:

```bash
python3 scripts/computeDetachmentScore.py
```

### Label Readiness Assessment (`scripts/label_readiness.py`)

Evaluate Initiative readiness and apply appropriate labels automatically.

### Repository Provisioning (`scripts/repo_factory.py`)

Backend implementation for automated repository creation with governance compliance.

## 📊 Governance Metrics

- **Spectrafy Score**: 100/100 (Perfect organizational optimization)
- **Template Coverage**: 6 optimized issue templates designed for efficiency and Copilot integration
- **Workflow Automation**: 11 reusable workflows for continuous governance
- **Documentation Completeness**: Comprehensive coverage of all governance aspects

## 🛡️ Security and Compliance

### Access Control

- Organization membership required for repository creation
- Admin token secured for automation workflows
- Audit trail through GitHub Actions logs

### Privacy Protection

- Default-deny policies for private repository access
- Content redaction enabled by default
- No content logging in governance systems

### Governance Enforcement

- Continuous validation of organizational structure
- Automated blocking of non-compliant changes
- Regular compliance health checks and reporting

## 📞 Support

### Getting Help

- **Organizational Structure Questions**: Reference [Canonical Organisational Structure](docs/canonicalOrganisationalStructure.md)
- **Repository Creation Issues**: See Repository Provisioning documentation
- **Template Problems**: Create issue with `template` label
- **Governance Violations**: Review governance guard workflow logs

### Contributing

- **Template Improvements**: Submit PR with updated templates
- **Documentation Updates**: Follow documentation standards
- **Workflow Enhancements**: Test in development before production
- **Structure Changes**: Follow governance approval process

## 🚀 Future Enhancements

- **Advanced Analytics**: Repository health scoring and trend analysis
- **Automated Onboarding**: Enhanced new repository setup automation
- **Governance Dashboards**: Real-time compliance monitoring interfaces
- **Template Personalization**: Role-based template customization

---

> 🏛️ **Governance Principle**: This repository serves as the foundational framework for SPECTRA's governance, ensuring every repository maintains canonical structure, proper classification, and continuous compliance with organizational standards.
