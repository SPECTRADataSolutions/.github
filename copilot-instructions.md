## SPECTRA AI Coding Agent Instructions (Authoritative, MVP Scope)

Purpose: Enable immediate productive, safe contributions across the two core domains:

- `framework/` (Python package: minimal methodology + manifest & stage validation CLI)
- `execution/` (Operations control-plane: GitHub Actions automation & sprint orchestration)

### 1. Architecture & Domain Model

- Lifecycle stages (ordered, monotonic if used): `Source → Parameters (alias: Prepare) → Extract → Clean → Transform → Refine → Analyse` (`spectra.methodology.stages`). Do NOT reorder existing canonical stages; unknown experimental labels are tolerated but ignored—never break monotonicity.
- Manifest (JSON) holds `pipelines[]` each with ordered `activities` (id, activityType, inputs, outputs, config). Inputs always reference `upstreamId.outputName` and must resolve.
- CLI (`spectra` entrypoint) is pure file operations: no network / side‑effects beyond local filesystem. Preserve this invariant (no hidden I/O, no external API calls).
- Multi‑repo ecosystem: `execution/` embeds a read‑only `framework/` snapshot for contextual automation (Fabric auth actions, sprint workflows).

### 2. Key Workflows & Commands

Python (framework):

1. Create env (Conda): `conda env create -f env.yml`; activate then `pip install -e .[dev]`.
2. Run tests: `pytest` (expect minimal suite; governance tests auto-skip if `.spectra/` absent).
3. Lint/format: `ruff check .` and `ruff format .` (only Ruff; Black/isort listed but Ruff handles style/imports). Line length 120.
4. CLI examples (idempotent):
   - `spectra init demo`
   - `spectra add-activity demo transform --type notebook`
   - `spectra order demo` / `spectra graph demo --format mermaid`
   - `spectra validate` / `spectra schema`

Node (execution):

- Formatting only: `npm run format:check` / `npm run format` (Prettier; respect repo `.prettierrc` in `package.json`). Do not introduce build tooling.

### 3. Governance & Scoring (Spectrafy)

- Audit script: `framework/scripts/spectrafy_audit.py` computes score (0–600) from categories: automation, standards, documentation, security, quality. Writes JSON artefacts under `.spectra/evidence/scores/` & updates README badge markers. When modifying scoring logic: keep deterministic, pure, and weights summing to 1.0 (`.spectra/scoring.yml`).
- Exceptions with expired dates trigger penalties; do not silently ignore schema issues—extend `schema_validate` if adding mandatory keys.

### 4. Agent Contract & Safety Boundaries

- See `framework/docs/meta/agentContract.md`. MUST preserve existing stage ids/order; MAY add experimental stage labels (ignored). Do NOT add irreversible side‑effects or network calls inside validation / CLI paths.
- When adding a new activityType prefer updating `contracts/models.py` (if present) & extend schema generation—keep backwards compatible.
- Never rename or delete canonical stages; add mapping logic only if aliasing (e.g., legacy `Prepare`).

### 5. Conventions

- Language: British English (e.g., “optimise”). Directory & file naming: `camelCase` for scaffolded organisational folders (`initRepo.py`).
- Keep README content repository‑specific (see `docs/standards/markdownStandards.md`); avoid generic boilerplate.
- Python style enforced solely via Ruff config in `pyproject.toml` (`ignore E501`, custom selects). Do not introduce secondary linters.
- Prettier printWidth 120; keep Markdown prose wrapping as configured (no forced reflow unless formatting script).

### 6. High‑Impact Files (Treat Carefully)

- `framework/pyproject.toml` (scripts entrypoint `spectra` and dependency surface minimal: only `click`). Adding deps requires: justify necessity, keep lean; update `env.yml` & optional `dev` extras if needed.
- `.github/CODEOWNERS` indicates guarded resources: modifying any listed special file (e.g., security workflows, VERSION, manifest governance) should remain minimal & scoped.
- `framework/scripts/initRepo.py` defines scaffold layout; mirror its naming patterns when extending.

### 7. Extension Patterns (Examples)

- Add CLI command: implement pure function in `spectra/cli.py` (or adjacent module), register via `click` group, update README command table succinctly.
- Add validation rule: extend `validation/core.py` (ensure deterministic ordering of reported issues, no external state).
- Add manifest field: update JSON schema generator (`spectra schema`) & keep backward compatibility (optional field first; avoid breaking existing examples).

### 8. Things NOT To Do

- No network calls / cloud SDK usage inside framework core or audit script.
- No speculative dependencies or large frameworks (stay lean MVP).
- No reformatting wide swaths of Markdown beyond needed edits (respect authored layout & diagrams).
- Do not embed secrets, tokens, or environment-specific paths.

### 9. Quick Triage Checklist Before PR

1. Tests pass (`pytest`).
2. `ruff check .` clean; `ruff format .` run if structural Python changes.
3. `spectra validate` still succeeds on sample manifest(s).
4. If audit logic touched: run `python scripts/spectrafy_audit.py` within a repo containing `.spectra/` to confirm badge update & score output.
5. No unintended dependency additions.

### 10. Minimal Contribution Flow (Agent)

Identify change → apply smallest diff → run local validation (above) → update README tables/examples only if semantics changed → avoid scope creep.

---

Clarifications or missing primitives? Provide a focused diff proposal; avoid broad refactors unless explicitly requested.
