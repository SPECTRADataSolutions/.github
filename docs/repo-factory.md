# repoFactory — Automate new repository creation

## Purpose
- Create new SPECTRA repos from an Initiative issue comment using a slash command.

## Usage
1) Ensure an organisation secret ORG_ADMIN_TOKEN exists (scopes: repo, admin:org).
2) On an Initiative issue, comment:
```
/create-repo repoName=governancePolicy domain=governance archetype=Guidance visibility=private templateRepo=SPECTRADataSolutions/client-demo
```
3) The workflow validates the name, creates the repo, seeds labels from `.github/labels.json`, and replies with the URL. If no template is provided, a baseline README and .gitignore are added.

## Parameters
- **repoName** (required): single-token camelCase starting lowercase
- **visibility** (optional): private|public|internal (default private)
- **domain** (optional): single-token camelCase
- **archetype** (optional): Guidance|Innovation|Engagement|Operations|Protection|Sustenance|Growth
- **description** (optional)
- **templateRepo** (optional): owner/name of a template repository

## Notes
- Community health files and issue templates inherit automatically from this `.github` repo.
- Extend later with branch protection, default teams/permissions, and compliance initialisers.