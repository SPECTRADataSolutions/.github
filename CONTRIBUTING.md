# Contributing to SPECTRA Data Solutions

Welcome to SPECTRA Data Solutions. This document explains how to contribute effectively using our organisation-wide standards and templates.

## 📋 Template Usage

### Issue Templates

All issues should use the [General Issue template](.github/ISSUE_TEMPLATE/general.yml) which ensures:
- **Complete metadata**: labels, project assignment, milestone visibility
- **Structured information**: separate Summary and Description fields
- **Acceptance criteria**: plain English checklists defining completion
- **Context & references**: links to stakeholders, related issues, and documentation
- **Reproduction steps**: when applicable (with guidance to remove if not relevant)

**Required fields:**
- Summary (one clear sentence)
- Description (detailed context)
- Acceptance Criteria (testable checkboxes)
- Project specification

**Optional but encouraged:**
- Steps to Reproduce (remove if not applicable)
- Context & References
- Milestone assignment

### Pull Request Templates

All pull requests should follow the [PR template](PULL_REQUEST_TEMPLATE.md) structure:
- Clear summary and detailed description
- Testing approach and verification
- Complete metadata and project assignment
- Reference to related issues and stakeholders

## 🏛️ Governance Model

### Template Inheritance

This `.github` repository serves as the **single source of truth** for:
- Issue and PR templates
- Workflow automation
- Engineering standards
- Governance policies

**Inheritance rules:**
- Templates automatically apply to all SPECTRA repositories
- Local overrides are **strongly discouraged**
- Any local override must be:
  - Documented in the project's README
  - Justified with business requirements
  - Approved by the engineering team
  - Regularly reviewed for necessity

### Override Policy

**When local overrides are permitted:**
- Highly specific project requirements that cannot be generalised
- Temporary workarounds with defined expiration dates
- Domain-specific metadata requirements

**When local overrides are prohibited:**
- Style preferences
- Personal workflow preferences
- Convenience modifications
- Duplicate functionality

**Override documentation requirements:**
```markdown
## Template Overrides

### Issue Template Modification
- **Justification**: [Business requirement]
- **Approval**: [Team lead/Engineering manager]
- **Review date**: [Quarterly review date]
- **Expiration**: [When this override should be reconsidered]
```

## 🤖 Copilot & AI Assistance

### Assignment Guidelines

**Default assignment policy:**
- New issues: automatically assigned to `@copilot` for initial triage
- Uncertain classification: assign to `@copilot`
- Complex architectural decisions: involve `@copilot` in review

**Copilot responsibilities:**
- Initial issue triage and labelling
- Priority assessment
- Appropriate team member assignment
- Standards compliance verification

### AI-Assisted Development

When working with AI tools:
- Reference SPECTRA framework standards explicitly
- Include context about organisational conventions
- Verify AI suggestions against established patterns
- Ensure all generated code follows naming conventions

## 📚 Engineering Standards

### SPECTRA Framework Reference

**All engineering decisions must reference the SPECTRA framework:**
- **Naming conventions**: camelCase for variables and functions
- **Documentation standards**: British English, professional tone
- **Code organisation**: follow established patterns
- **Testing requirements**: comprehensive coverage expectations
- **Security practices**: follow established protocols

**Framework locations:**
- Main documentation: [SPECTRA Engineering Standards](https://spectra.internal/standards)
- Naming conventions: [SPECTRA Naming Guide](https://spectra.internal/naming)
- Architecture patterns: [SPECTRA Architecture](https://spectra.internal/architecture)

### Local Standards Prohibition

**Do not improvise local standards for:**
- Naming conventions
- Code formatting
- Documentation structure
- Testing patterns
- Security practices
- API design

**Always reference SPECTRA framework instead of:**
- Creating project-specific rules
- Copying standards from external sources
- Implementing personal preferences
- Following outdated practices

## 🔍 Quality Assurance

### Pre-submission Checklist

Before creating issues or PRs:
- [ ] All required metadata is complete
- [ ] Summary is clear and concise (one sentence)
- [ ] Acceptance criteria are testable
- [ ] British English spelling and grammar
- [ ] Professional, encouraging tone
- [ ] SPECTRA framework compliance
- [ ] Appropriate stakeholder references

### Review Standards

Reviewers should verify:
- Template compliance
- Metadata completeness
- Standards alignment
- Clear acceptance criteria
- Appropriate testing approach

## 🚀 Getting Started

1. **Read the SPECTRA framework** documentation before contributing
2. **Use the issue template** for all new issues
3. **Follow the PR template** for all pull requests
4. **Assign to @copilot** when uncertain about classification
5. **Reference relevant stakeholders** in Context & References
6. **Include clear acceptance criteria** for all work items

## 📞 Support

- **Template issues**: Create an issue in this repository
- **Standards questions**: Reference SPECTRA framework documentation
- **Technical guidance**: Assign to `@copilot` for assistance
- **Process clarification**: Contact the engineering team

---

*This contributing guide enforces SPECTRA Data Solutions governance and ensures consistent, high-quality contributions across all repositories.*