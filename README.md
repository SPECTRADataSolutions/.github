# 💠 SPECTRA Data

**The Intelligence Engine of the SPECTRA Cosmos**

---

## 🧭 Purpose

**SPECTRA Data** powers the Cosmos through truth, structure, and automation.  
It transforms raw information into clarity — building the pipelines, models, and insights that allow every other branch of SPECTRA to operate intelligently and consistently.

This organisation is where systems think.  
Where code becomes knowledge, and knowledge becomes decision.

---

## 🧩 Responsibilities

- **Data Engineering** — design and automation of pipelines using the Spectra Methodology.  
- **Architecture** — canonical schemas, Delta Lake structures, and Fabric integration.  
- **Analytics & AI** — semantic models, machine learning, and applied intelligence.  
- **Quality & Governance** — validation, lineage, and trust metrics across every dataset.  

---

## ⚙️ Data Repositories

| Repository | Purpose |
|-------------|----------|
| **framework** | Spectra Methodology and pipeline standards. |
| **fabric** | Microsoft Fabric configurations, workspaces, and environments. |
| **xero** | Financial data integration and reconciliation pipelines. |
| **jira** | Project analytics, metrics, and workflow insights. |
| **labs** | Experimental projects, training modules, and discovery prototypes. |

---

## 🔗 Navigation

### 🏠 Enterprise

[**SPECTRA Cosmos – Enterprise Home**](https://github.com/enterprises/spectraCosmos)

---

### 🌌 Organisations

- [**SPECTRA Core**](https://github.com/SPECTRACoreSolutions)  
- [**SPECTRA Data**](https://github.com/SPECTRADataSolutions)  
- [**SPECTRA Design**](https://github.com/SPECTRADesignSolutions)  
- [**SPECTRA Security**](https://github.com/SPECTRASecuritySolutions)  
- [**SPECTRA Audio**](https://github.com/SPECTRAAudioSolutions)  
- [**SPECTRA Engineering**](https://github.com/SPECTRAEngineeringSolutions)  
- [**SPECTRA Engagement**](https://github.com/SPECTRAEngagementSolutions)

---

## 🔐 Spectra Assistant Tokens

All seven SPECTRA organisations now publish shared GitHub App secrets:

| Secret | Purpose |
| --- | --- |
| `SPECTRA_APP_ID` | Spectra Assistant GitHub App identifier (2172220). |
| `SPECTRA_APP_INSTALLATION_ID` | Org-specific installation id (see GitHub → Settings → Secrets). |
| `SPECTRA_APP_PRIVATE_KEY` | PEM-encoded private key used to mint short-lived installation tokens. |

### Local helper

Use `scripts/spectra_assistant_token.py` to mint a token without copy/pasting PEM blobs:

1. `pip install -r scripts/requirements.txt`
2. Export the secrets (or pass via `--app-id`, `--installation-id`, `--key-file`).
3. Run `python scripts/spectra_assistant_token.py --format token > token.txt`
4. `setx /M GITHUB_TOKEN (Get-Content token.txt)` or `export GITHUB_TOKEN=$(cat token.txt)`

The helper accepts `--format text` (default) for a friendly summary, `--format json` for scripting, and auto-detects base64/private key inputs. Tokens expire within ~60 minutes, so mint a new one per session.

### Actions usage

Workflows reference the same secrets via `secrets.SPECTRA_APP_ID` etc. Pair the secrets with `tibdex/github-app-token` or the helper when a job needs Spectra Assistant privileges.

---

## 🔭 Philosophy

SPECTRA Data treats engineering as a language of truth.  
Every schema, model, and metric exists to remove ambiguity — revealing the patterns beneath complexity.  
This is where the Cosmos becomes measurable, testable, and self-improving.

---

[www.spectradatasolutions.com](https://www.spectradatasolutions.com)  
_© SPECTRA Data Solutions — Part of the SPECTRA Cosmos_
