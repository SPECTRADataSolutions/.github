# Deprecated / Removed Workflows (Phase 1)

| Workflow File | Status | Replacement | Date |
|---------------|--------|-------------|------|
| anchor-reachability-and-size.yml | Removed (empty) | (future) validate-anchor-integrity.yml | 2025-08-26 |
| check-anchor-health.yml | Removed (corrupted stub) | (future) validate-anchor-integrity.yml | 2025-08-26 |
| create-repository-instance.yml | Deprecated (logic superseded) | dispatch-repository-factory + generate-repository-service | 2025-08-26 |

All replacements will be provided as reusable workflows in `framework` with thin wrappers here where needed.
