# Template Optimization Examples

## Before vs After Comparison

### Bug Template Comparison

**BEFORE (Complex):**
- 15+ fields including: pillar, domain, severity, reproducibility, stepsToReproduce, expectedBehaviour, actualBehaviour, environment, automationOptions, submissionChecklist
- Required organizational metadata for every bug report
- 77 lines of YAML configuration

**AFTER (Simple):**
- 6 fields: description, reproduction, expected, environment, severity
- Optional organizational context
- 43 lines of YAML configuration
- Clear, human-friendly prompts

### Sample: How Copilot Can Now Fill Templates

**GitHub Copilot prompt:** "Create a bug report for login page not working"

**Generated content:**
```
Title: 🐛 Login page returns 500 error

What happened?
The login page crashes with a 500 internal server error when users try to authenticate. This started happening after the recent deployment.

How to reproduce:
1. Go to /login
2. Enter valid credentials 
3. Click "Sign In" button
4. See 500 error page

Expected behavior:
Users should be redirected to the dashboard after successful login

Environment:
Chrome 120, Windows 11, Production environment

Severity: High - Blocks important work
```

**Time to complete:** 30 seconds vs 3-5 minutes previously

### Pull Request Template Comparison

**BEFORE:** 9 sections, 70 lines, complex checklists
- summary, context, changes, acceptanceCriteria, risk & impact, testing, deployment, links, review checklist, standards

**AFTER:** 4 sections, 24 lines, essential information
- What does this change?, Why is this needed?, How was this tested?, Additional notes

### Results

- **75% less complexity** (18→6 templates, 70→24 lines PR template)
- **Copilot can auto-fill** templates in 30 seconds vs 3-5 minutes manually
- **Better user adoption** - simpler choices, clearer language
- **Maintained governance** - essential organizational structure preserved