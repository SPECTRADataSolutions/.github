# ⚙️ .github – Organisation-wide GitHub Templates & Automation

This repository serves as the **single source of truth** for GitHub configuration across all SPECTRA Data Solutions repositories. It provides standardised templates, workflows, and governance policies that ensure consistency, quality, and compliance with SPECTRA framework standards.

---

## 🎯 Purpose & Coverage

### Governance Model
This repository implements organisation-wide standards that:
- **Enforce metadata completeness** across all issues and pull requests
- **Standardise communication** with professional, consistent templates
- **Automate quality assurance** through structured workflows
- **Centralise engineering standards** to prevent local improvisation
- **Enable AI-assisted development** with clear Copilot guidance

### Coverage Scope
Templates and automation apply to:
- ✅ All SPECTRA Data Solutions repositories
- ✅ Public and private repositories
- ✅ New and existing projects
- ✅ All team members and external contributors

---

## 📦 Repository Contents

| Component | Purpose | Inheritance |
|-----------|---------|-------------|
| **`.github/ISSUE_TEMPLATE/`** | YAML-based issue forms with required metadata | Automatic |
| **`PULL_REQUEST_TEMPLATE.md`** | Standardised PR structure and quality checks | Automatic |
| **`CONTRIBUTING.md`** | Template usage, override policy, SPECTRA standards | Organisation-wide |
| **`workflows/`** | GitHub Actions for automation and governance | Automatic |
| **`README.md`** | This governance documentation | Reference |

### Template Features

**Issue Templates:**
- Complete metadata requirements (labels, project, assignee, milestone)
- Structured Summary and Description fields
- Plain English Acceptance Criteria checklists
- Context & References for stakeholder information
- Steps to Reproduce (with removal guidance)
- Default assignment to `@copilot` for triage

**Pull Request Template:**
- Comprehensive change documentation
- Testing verification requirements
- Standards compliance checklist
- Clear reviewer guidance

---

## 🔄 Template Inheritance Model

### Automatic Application
Templates in this repository **automatically apply** to all organisation repositories through GitHub's [default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) feature.

### Override Policy
Local template overrides are **strongly discouraged** and must be:
- ✋ **Documented** with business justification
- ✋ **Approved** by engineering leadership  
- ✋ **Reviewed** quarterly for continued necessity
- ✋ **Compliant** with SPECTRA framework standards

**Permitted overrides:**
- Domain-specific metadata requirements
- Highly specialised project workflows
- Temporary workarounds with expiration dates

**Prohibited overrides:**
- Style or personal preferences
- Convenience modifications
- Duplicate functionality
- Non-compliant standards

---

## 🤖 GitHub Automation & AI Integration

### Copilot Integration
- **Default assignee** for all new issues: `@copilot`
- **Triage automation** for uncertain classifications
- **Standards verification** through AI-assisted review
- **Quality assurance** for template compliance

### Workflow Automation
- **Template compliance** checking
- **Metadata validation** enforcement
- **Standards adherence** monitoring
- **Quality gate** implementation

### AI-Assisted Development
This repository enables AI tools to:
- Understand SPECTRA framework standards
- Apply consistent naming conventions (camelCase)
- Follow British English documentation standards
- Reference appropriate stakeholders and documentation

---

## 📋 Standards & Framework Compliance

### SPECTRA Framework Integration
All templates and automation reference the **SPECTRA framework** for:
- **Engineering standards**: architecture, patterns, practices
- **Naming conventions**: camelCase, British English
- **Documentation standards**: structure, tone, completeness
- **Quality requirements**: testing, validation, compliance

### Framework Locations
- 📚 [SPECTRA Engineering Standards](https://spectra.internal/standards)
- 🏷️ [Naming Conventions Guide](https://spectra.internal/naming)
- 🏗️ [Architecture Patterns](https://spectra.internal/architecture)
- 📝 [Documentation Standards](https://spectra.internal/documentation)

### Local Standards Prohibition
**Do not create local standards for:**
- Naming conventions → Use SPECTRA framework
- Code formatting → Use SPECTRA patterns  
- Documentation structure → Use SPECTRA templates
- Testing approaches → Use SPECTRA guidelines

---

## 🚀 Getting Started

### For Contributors
1. **Read** [CONTRIBUTING.md](CONTRIBUTING.md) for complete template guidance
2. **Use** the provided issue and PR templates
3. **Reference** SPECTRA framework for all engineering decisions
4. **Assign** to `@copilot` when uncertain about classification

### For Maintainers
1. **Review** template compliance in all repositories
2. **Monitor** override requests and justifications
3. **Update** templates based on framework evolution
4. **Ensure** AI guidance remains current and effective

### For New Repositories
Templates apply automatically - no setup required! 🎉

---

## 📞 Support & Contact

- **Template issues**: Create an issue in this repository
- **Standards questions**: Reference SPECTRA framework documentation
- **Override requests**: Contact engineering leadership
- **AI assistance**: Assign to `@copilot` for guidance

---

> 🏛️ **Governance Principle**: If it governs how we work on GitHub across SPECTRA Data Solutions, it lives here as the single source of truth.
