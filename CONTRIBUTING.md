# Contributing to SPECTRA Projects

Welcome to our development community! This guide explains how to contribute effectively using our organisation-wide templates and standards.

## Template Usage

### Issue Templates
All SPECTRA repositories inherit issue templates from this `.github` organisation repository. When creating issues:

1. **Use the provided template**: Our YAML-based issue template ensures consistency and completeness
2. **Fill all required fields**: Summary, Description, Acceptance Criteria, Priority, and Issue Type are mandatory
3. **Provide context**: Include relevant references, stakeholders, and background information
4. **Write clear acceptance criteria**: Use plain English checklists that define specific, measurable outcomes

### Pull Request Templates
Our organisation-wide PR template includes:

- **Summary and Description**: Clear, concise explanation of changes
- **Acceptance Criteria**: Verification checklist for completion
- **Testing requirements**: Ensure all changes are properly tested
- **Review checklist**: Guidelines for effective code review
- **Deployment considerations**: Special requirements or dependencies

### Default Assignments
- **Issues**: Default assignee is `@copilot` for triage and initial categorisation
- **Copilot guidance**: If unsure about assignment or categorisation, always assign to `@copilot`
- **Milestone field**: Always present but not required—use for planning and tracking

## Template Override Policy

### When Overrides Are Permitted
Local template overrides are **strongly discouraged** but may be justified in exceptional circumstances:

1. **Project-specific requirements**: Unique workflow needs that cannot be accommodated by the standard template
2. **Regulatory compliance**: Industry-specific requirements (e.g., medical, financial, aerospace)
3. **Legacy integration**: Temporary accommodation during migration periods

### Documentation Requirements for Overrides
If your project requires template overrides, you **must**:

1. **Document in local CONTRIBUTING.md**: Explain the specific need and justification
2. **Reference this organisation template**: Clearly state what differs and why
3. **Maintain consistency**: Preserve the spirit and structure of organisation standards
4. **Regular review**: Evaluate whether overrides are still necessary during retrospectives

### Example Override Documentation
```markdown
## Local Template Overrides

**Override**: Custom issue template for security vulnerabilities
**Justification**: Regulatory compliance requires additional security classification fields
**Standard template**: Inherits from organisation template with added security section
**Review date**: Quarterly evaluation of continued necessity
```

## Engineering Standards

### SPECTRA Framework Compliance
All engineering practices must follow the [SPECTRA framework]():

- **Naming conventions**: Use British English and camelCase throughout
- **Code structure**: Follow established patterns and architectural guidelines  
- **Documentation**: Maintain comprehensive, up-to-date documentation
- **Testing**: Implement appropriate test coverage for all changes
- **Security**: Follow security best practices and review requirements

### Do Not Improvise Locally
**Important**: Never improvise engineering standards at the project level. All guidelines, conventions, and practices are defined in the SPECTRA framework. If you identify a gap or need clarification:

1. Consult the SPECTRA framework documentation
2. Raise an issue in the appropriate governance repository
3. Follow existing patterns until official guidance is available

## Workflow Guidelines

### For Contributors
1. **Review templates**: Familiarise yourself with issue and PR templates before contributing
2. **Follow the process**: Use templates as intended—complete all sections thoughtfully
3. **Reference standards**: Always follow SPECTRA framework guidelines
4. **Seek guidance**: When in doubt, assign to `@copilot` or ask maintainers

### For Maintainers
1. **Enforce templates**: Ensure contributors use templates appropriately
2. **Triage assignments**: Review `@copilot` assignments and redistribute as needed
3. **Maintain consistency**: Uphold organisation standards across all projects
4. **Document exceptions**: Clearly justify and document any necessary deviations

### For Copilot & AI Agents
- **Triage role**: Accept assignments for categorisation and initial review
- **Template enforcement**: Remind users to use organisation templates, not project duplicates
- **Standards guidance**: Reference SPECTRA framework for all engineering decisions
- **Escalation**: Assign to appropriate human maintainers when specialised knowledge is required

## Getting Help

- **Template questions**: Create an issue in this `.github` repository
- **SPECTRA framework**: Consult the framework documentation or create a governance issue
- **Project-specific queries**: Contact project maintainers or use project channels
- **Urgent matters**: Tag relevant stakeholders or escalate through appropriate channels

---

**Remember**: This `.github` repository serves as the single source of truth for all organisation-wide templates and automation. Consistency across projects ensures efficient collaboration and maintains our engineering standards.