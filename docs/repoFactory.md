# repoFactory — Automated Repository Creation

The repoFactory workflow allows stewards to create a new repository by commenting on an Initiative issue.

How to use
- In a valid Initiative issue, add a comment:
  - `/create-repo repoName=governancePolicy domain=governance pillar=Guidance visibility=private`
  - Optional: `templateRepo=SPECTRADataSolutions/blueprint`

What it does
- Validates name (single-token camelCase) and that the repo does not already exist
- Creates the repository under the organisation with main as default
- Seeds standard labels from .github/labels.json
- Seeds README.md and .gitignore when not templated
- Replies on the Initiative with the new repository URL

Required secret
- ORG_ADMIN_TOKEN at the organisation level (scopes: repo, admin:org)

Notes
- British English and SPECTRA in ALL CAPS throughout documentation
- This implements knowledge item #23