# ⚙️ .github – Organisation-Wide GitHub Templates & Automation

This repository serves as the **single source of truth** for all SPECTRA Data Solutions' GitHub configuration, templates, and automation workflows. It enforces governance, metadata completeness, and internal engineering standards across all organisation repositories.

---

## 📦 Contents

| File / Directory | Purpose | Coverage |
|-----------------|---------|----------|
| `.github/ISSUE_TEMPLATE/` | YAML-based structured issue forms with complete metadata requirements | All repositories |
| `.github/PULL_REQUEST_TEMPLATE.md` | Standard PR template with acceptance criteria and review checklists | All repositories |
| `CONTRIBUTING.md` | Template usage guidance, override policy, and SPECTRA framework references | Organisation-wide |
| `workflows/` | GitHub Actions for automation and enforcement | All repositories |
| `README.md` | This file - explains inheritance model and coverage | Documentation |

---

## 🏗️ Inheritance Model

### Automatic Application
This configuration **automatically applies** to all repositories in the SPECTRA Data Solutions GitHub organisation through GitHub's inheritance mechanism:

- **Issue templates**: Inherited by all repos unless locally overridden
- **PR templates**: Applied organisation-wide as the default
- **Workflows**: Available to all repositories
- **Standards**: Referenced in CONTRIBUTING.md as the authoritative source

### Template Features
Our templates enforce:

- **Complete metadata**: Labels, project assignment, milestone fields (always present)
- **Default assignee**: `@copilot` for triage and initial categorisation
- **Structured content**: Separate Summary (one sentence) and Description (detailed context)
- **Acceptance criteria**: Plain English checklists for measurable outcomes
- **Context & references**: Links, stakeholders, and background information
- **Professional tone**: Encouraging, clear instructions using British English
- **SPECTRA compliance**: All standards reference the official framework

### Override Policy
Local template overrides are **strongly discouraged** but permitted when:

1. **Justified by specific needs**: Regulatory compliance, legacy integration, unique workflows
2. **Properly documented**: Must be explained in project's CONTRIBUTING.md
3. **Regularly reviewed**: Evaluated for continued necessity

---

## 🎯 Coverage & Scope

### What This Repository Governs
- ✅ Issue and PR templates across all projects
- ✅ Contribution guidelines and workflow standards  
- ✅ GitHub automation and enforcement workflows
- ✅ Template inheritance and override policies
- ✅ Copilot and AI agent guidance

### What Individual Projects Should Handle
- 🏠 Project-specific documentation
- 🏠 Local build and deployment scripts
- 🏠 Repository-specific configurations
- 🏠 Custom labels beyond the standard set

### SPECTRA Framework Integration
All engineering standards, naming conventions, and documentation practices are defined in the **SPECTRA framework**. This repository:

- References framework standards without duplication
- Enforces framework compliance through templates
- Provides guidance on framework application
- **Never improvises** local standards—always defers to the framework

---

## 🤖 Copilot & Agent Guidance

### Assignment Protocol
- **Default assignment**: All new issues assigned to `@copilot` for triage
- **Categorisation**: Copilot reviews and assigns to appropriate maintainers
- **Template enforcement**: Agents should guide users to organisation templates
- **No duplication**: Never create project-specific template copies

### AI Agent Responsibilities
1. **Triage**: Review incoming issues and categorise appropriately
2. **Standards enforcement**: Ensure SPECTRA framework compliance
3. **Template guidance**: Direct users to correct templates and procedures
4. **Escalation**: Assign to human maintainers when specialised knowledge required

---

## 🔄 Usage Instructions

### For Contributors
1. Use the inherited templates when creating issues or PRs
2. Fill all required fields completely and thoughtfully
3. Follow SPECTRA framework standards for all engineering work
4. Consult CONTRIBUTING.md for detailed guidance

### For Maintainers
1. Review `@copilot` assignments and redistribute as needed
2. Enforce template usage and completeness
3. Maintain consistency with organisation standards
4. Document any necessary local overrides

### For Project Teams
1. Rely on inherited templates as the default
2. Only override when absolutely necessary and properly justified
3. Reference this repository in local documentation
4. Regularly review override necessity

---

## 📚 Related Resources

- **SPECTRA Framework**: [Link to framework documentation]
- **Contributing Guidelines**: See CONTRIBUTING.md in this repository
- **Template Examples**: Review .github/ISSUE_TEMPLATE/ for structure
- **Override Documentation**: Guidelines in CONTRIBUTING.md

---

> 🎯 **Purpose**: Ensure consistent, high-quality collaboration across all SPECTRA projects through standardised templates, clear governance, and automated enforcement.
