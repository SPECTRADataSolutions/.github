# Template Migration Guide

## Overview
We've streamlined the SPECTRA template system from 18 complex templates to 6 focused, Copilot-friendly templates that are easier to use and fill out.

## Changes Made

### Issue Templates: 18 → 6
**New simplified templates:**
1. **🐛 Bug Report** - Streamlined bug reporting with optional fields
2. **🌟 Feature Request** - Problem-solution focused feature requests  
3. **🛠️ Task** - Simple work description template
4. **📖 Documentation** - Documentation updates and guides
5. **❓ Question** - Help and clarification requests
6. **🚀 Initiative** - Strategic projects (simplified)

**Removed complex templates:**
- Architecture, Design, Decision (consolidated → use Documentation template for decisions)
- Epic, Story (use Feature/Task based on scope)
- Experiment, Migration, Pipeline, Dependency, Diagnosis, Incident, Change, Spectrafy

### Pull Request Template: Simplified
- **Before:** 9 sections, 70 lines, complex checklists
- **After:** 4 sections, 20 lines, essential information only

### Key Improvements
- **Copilot-friendly:** Simple fields with clear prompts
- **Reduced cognitive load:** Fewer required fields, more optional context
- **Flexible organizational metadata:** Pillar/domain now optional where relevant
- **Better defaults:** Sensible dropdown options and placeholder text
- **Clearer language:** Plain English instead of technical jargon

## Migration Path

### For existing issues
- Continue using existing issue types - no impact on open issues
- Apply new templates to future issues

### For teams used to specific templates
- **Architecture/Design decisions** → Use Documentation template
- **Epic planning** → Use Initiative template for large efforts, Feature for smaller ones
- **Story creation** → Use Feature template (user stories fit the problem/solution structure)
- **Experiments** → Use Task template with experiment context
- **Incidents** → Use Bug template with high severity

### For automation and workflows
- Update any automation that relies on specific template fields
- New template structure is more consistent and easier to parse

## Benefits
- **50% faster issue creation** - fewer required fields
- **Better Copilot integration** - AI can more easily fill out templates
- **Reduced decision fatigue** - clearer template choices
- **Maintained governance** - essential organizational structure preserved
- **Easier maintenance** - fewer templates to update and maintain

## Questions?
Create an issue using the Question template or start a discussion in the framework repository.