# GitHub Actions Workflow Naming Standard

## Overview

This document establishes the naming convention for GitHub Actions workflows in SPECTRA repositories to ensure consistency, clarity, and discoverability.

## Naming Convention

### Format
```
{action}-{object}[-{modifier}]
```

### Rules

1. **Use kebab-case**: All lowercase with hyphens separating words
2. **Start with an action verb**: The first word should be a descriptive action (verb)
3. **Follow with the object**: What the action is performed on
4. **Add modifiers if needed**: Additional descriptive words to clarify the purpose

### Action Verbs

Common action verbs to use as the first word:

- `validate` - Check compliance, structure, or correctness
- `generate` - Create or produce files, reports, or artifacts
- `analyze` - Examine and report on data or code
- `create` - Build new resources or repositories
- `update` - Modify existing resources
- `assign` - Allocate tasks or responsibilities
- `enforce` - Apply rules or policies
- `seed` - Initialize or populate data
- `tally` - Count or calculate metrics
- `guard` - Protect or monitor for violations
- `govern` - Apply governance policies
- `pin` - Fix or lock versions/references

### Examples

| Purpose | Workflow Name |
|---------|---------------|
| Validates organizational structure | `validate-org-structure` |
| Creates new repositories | `create-repository` |
| Analyzes initiative proposals | `analyze-initiatives` |
| Updates dependency graphs | `update-dependency-graph` |
| Assigns initiatives automatically | `assign-initiatives` |
| Enforces governance policies | `enforce-governance` |
| Seeds repository labels | `seed-labels` |
| Tallies prayer requests | `tally-prayers` |
| Guards repository structure | `guard-repo-structure` |
| Validates context manifests | `validate-context-manifest` |
| Pins reference checksums | `pin-refs-checksums` |

## Migration Guide

When renaming existing workflows:

1. Only change the `name:` field in the workflow file
2. Keep the filename unchanged to preserve workflow history
3. Ensure the new name follows the action-object pattern
4. Test that the workflow still functions correctly after rename

## Benefits

- **Consistency**: All workflows follow the same pattern
- **Discoverability**: Easy to find workflows by action type
- **Clarity**: Purpose is immediately clear from the name
- **Sortability**: Workflows group naturally by action in the UI