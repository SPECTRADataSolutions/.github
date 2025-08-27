# Deprecated / Removed Workflows (Phase 1)

| Workflow File | Status | Replacement | Date |
|---------------|--------|-------------|------|
| anchor-reachability-and-size.yml | Removed (empty) | (future) validate-anchor-integrity.yml | 2025-08-26 |
| check-anchor-health.yml | Removed (corrupted stub) | (future) validate-anchor-integrity.yml | 2025-08-26 |
| create-repository-instance.yml | Deprecated (logic superseded) | dispatch-repository-factory + generate-repository-service | 2025-08-26 |
| ci-python.yml | Removed (monolith) | validate-python-quality.yml + validate-python-tests.yml + scan-code-vulnerabilities.yml | 2025-08-27 |
| security-checks.yml | Renamed | scan-code-vulnerabilities.yml | 2025-08-27 |
| notify-workflow-migration.yml | Removed (transitional) | (none) | 2025-08-27 |
| report-workflow-summary.yml | Removed (redundant) | Integrated summaries inside modular workflows | 2025-08-27 |

All replacements will be provided as reusable workflows in `framework` with thin wrappers here where needed.
