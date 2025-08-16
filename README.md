# ⚙️ SPECTRA Governance

## 🏛️ Pillar: Doctrine  
### 🌐 Domain: Governance  

## 🎯 purpose
The **SPECTRA Governance** repository enforces organisation-wide rules and conventions.  
It provides default templates, contribution guidelines, and CI workflows that every repository inherits, ensuring consistency and compliance across the framework.

## 📂 contents
- `.github/ISSUE_TEMPLATE/` — standardised issue forms for consistent reporting  
- `PULL_REQUEST_TEMPLATE.md` — default pull-request checklist  
- `CONTRIBUTING.md` — contribution rules, naming conventions, and review process  
- `.github/workflows/` — lightweight workflows for validation and governance  

## 🚀 domain workflows
- **validateTemplates** — ensure all repos include standard issue and PR templates  
- **enforceConventions** — lint repo metadata and naming conventions  
- **minimalQualityGate** — apply a baseline CI check across all repos  

## 🔗 references
This repo represents the **Governance domain** under the **Doctrine pillar**.  
Other Doctrine domains are: Intelligence, Standards, and Structure.  
For the full Doctrine pillar map see: [SPECTRA Doctrine](https://github.com/SPECTRADataSolutions/doctrine)

## 🚦 overridePolicy
Local overrides are discouraged. If absolutely necessary, they must:  
- Be documented  
- Have explicit approval  
- Be temporary and tracked for removal
