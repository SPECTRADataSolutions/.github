# GitHub Actions Workflow Naming Standard

## Overview

This document establishes the naming convention for GitHub Actions workflows in SPECTRA repositories to ensure consistency, clarity, and discoverability.

## Naming Convention

### Format
```
{action}-{object}-{modifier}
```

### Rules

1. **Use kebab-case**: All lowercase with hyphens separating words
2. **Exactly 3 parts**: All workflow names must have exactly 3 hyphen-separated parts
3. **Start with an action verb**: The first word should be a descriptive action (verb)
4. **Follow with the object**: What the action is performed on
5. **End with a modifier**: Additional descriptive word that clarifies the purpose or context

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
| Creates new repositories | `create-repository-factory` |
| Analyzes initiative proposals | `analyze-initiative-proposals` |
| Updates dependency graphs | `update-dependency-graph` |
| Assigns initiative owners | `assign-initiative-owners` |
| Enforces governance policies | `guard-governance-policies` |
| Seeds repository labels | `seed-repository-labels` |
| Tallies prayer requests | `tally-prayer-requests` |
| Guards repository structure | `guard-repo-structure` |
| Validates context manifests | `validate-context-manifest` |
| Pins reference checksums | `pin-refs-checksums` |
| Governs context manifests | `govern-context-manifests` |
| Tallies devotion metrics | `tally-devotion-metrics` |

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