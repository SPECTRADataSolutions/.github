## SPECTRA Data Org Front Page (2025-11-22)

### Mission & Posture

- Build and ship the knowledge + data layer for the cosmos: SpectraCLI, Context MCP, ingestion gateways, brand systems.
- Provide the scaffolding primitives every org depends on (CLI, schemas, Spectrafy scoring, token tooling).
- Keep multi-modal assets (data, MCP, branding) in lockstep so automation + storytelling stay consistent.

| Indicator          | Signal                                                                         |
| ------------------ | ------------------------------------------------------------------------------ |
| CLI adoption       | 100% of Core manifests validated via `spectra` CLI.                            |
| Spectrafy coverage | Governance score emitted for 4 active programmes this week.                    |
| Branding freshness | Style guide updated Nov-2025; assets mirrored to Media vault.                  |
| Token health       | Spectra Assistant PEM standardised; installation scope pending Projects admin. |

### Canonical Model & Language

- Lifecycle: `Source → Prepare → Extract → Clean → Transform → Refine → Analyse`.
- Manifest discipline: ordered activities, resolved dependencies, alias `Parameters` → `Prepare` only when reading legacy files.
- CLI purity remains non-negotiable.
- British English for documentation + repo messaging.

### Shortcut Glossary (Data view)

| Keyword        | Meaning                                                      | Repo                   |
| -------------- | ------------------------------------------------------------ | ---------------------- |
| **SpectraCLI** | `spectra` entrypoint (scaffold, validate, graph, spectrafy). | `Data/framework`       |
| **Scaffold**   | `spectra init <name>` + `spectra add-activity`.              | `Data/framework`       |
| **TokenMint**  | GitHub App token helper CLI/script.                          | `Data/.github/scripts` |
| **ContextMCP** | Model Context Protocol server for AI clients.                | `Data/context`         |
| **BrandKit**   | Style guides + assets powering Media releases.               | `Data/branding`        |
| **Atlas**      | This file (Data edition).                                    | `Data/.github`         |

### Portfolio (Atlas)

| Nickname          | Repo             | Purpose                                             | Status                     |
| ----------------- | ---------------- | --------------------------------------------------- | -------------------------- |
| **SpectraCLI**    | `Data/framework` | Core CLI, schema validation, Spectrafy scoring.     | Stable; active dev.        |
| **ContextMCP**    | `Data/context`   | MCP server + demos for AI integrations.             | Live; HTTP + STDIO.        |
| **BridgeGateway** | `Data/bridge`    | Event ingestion & schema enforcement before Fabric. | Guardrails in place.       |
| **BrandKit**      | `Data/branding`  | Brand pillars, style guide, assets.                 | Fresh as of Nov-2025.      |
| **DesignSystem**  | `Data/design`    | Product/design documentation + references.          | Partnered with Design org. |
| **GraphLab**      | `Data/graph`     | Graph experimentation playground.                   | R&D mode.                  |
| **JiraAdapter**   | `Data/jira`      | Jira service definitions/tools.                     | Services directory active. |
| **MediaVault**    | `Data/media`     | Automation around media assets.                     | Syncs with Branding.       |
| **UnifiOps**      | `Data/unifi`     | Microsoft Fabric Unifi artefacts.                   | Use for Fabric workflows.  |
| **XeroOps**       | `Data/xero`      | Finance connectors + automation.                    | Secrets via GitHub.        |
| **ZephyrOps**     | `Data/zephyr`    | Experimental backlog (branch `dev`).                | Innovation lab.            |

### Rituals & Automations

- **Scaffolding**: run SpectraCLI commands; finish with `spectra order` + `spectra validate`.
- **Spectrafy**: `python scripts/spectrafy_audit.py` after scoring changes; capture `.spectra/evidence/scores/*`.
- **Token minting**: `python Data/.github/scripts/spectra_assistant_token.py --format token`; feed to `gh auth login --with-token`.
- **Brand releases**: update `Data/branding/styleGuide.md`, sync assets to Media vault, tag release.
- **Context MCP deploy**: `pip install -e .`, `spectra-context-mcp --mode http`, or ship via `render.yaml`.

### Telemetry & Performance

- Ruff + pytest mandatory on SpectraCLI contributions.
- CLI dependency surface stays lean (`click` + stdlib) — document any change in `pyproject.toml` + `env.yml`.
- Branding pipeline uses Shields badges to indicate freshness; keep README badge dates accurate.
- MCP server serves STDIO + HTTP + JSON-RPC; keep sample assessments (`assess.py`) passing.

### Focus Signals

- Finish provisioning permissions so CLI-driven provisioning can run apply mode from Core workflows.
- Publish more manifest exemplars under `docs/governance/` for downstream repos.
- Keep Atlas updated whenever a new capability appears; reuse nicknames in commit subjects to aid prompt grounding.
