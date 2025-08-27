# Navigation Block Snippet

This reusable navigation block can be copied and pasted into any repository README to provide canonical organisational navigation.

## Usage

Copy the content below between the `<!-- NAVIGATION_START -->` and `<!-- NAVIGATION_END -->` markers into your README.md file, then replace the placeholders:

- `{owner}/{repo}` - Replace with your GitHub owner/repository name
- `{PillarName}` - Replace with your canonical pillar (Guidance, Innovation, Engagement, Execution, Protection, Sustenance, Growth)
- `{domainName}` - Replace with your domain name in camelCase

## Navigation Block Template

```markdown
<!-- NAVIGATION_START -->
## 🏛️ Organisational Structure
**Pillar:** {PillarName}
**Domain:** {domainName}
**Repository:** {owner}/{repo}

### Quick Links
- 📋 [Canonical Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md) - Organisational taxonomy and guidelines
- 🏷️ [Issue Templates](https://github.com/{owner}/{repo}/issues/new/choose) - Structured issue creation
- 📖 [Contributing Guidelines](https://github.com/{owner}/{repo}/blob/main/CONTRIBUTING.md) - How to contribute
- 🔒 [Security Policy](https://github.com/{owner}/{repo}/security/policy) - Security reporting

This repository is part of SPECTRA's canonical organisational structure. For governance questions or classification assistance, reference the [canonical structure documentation](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md).
<!-- NAVIGATION_END -->
```

## Alternative Format

For repositories that prefer the two-line format, use:

```markdown
**Pillar:** {PillarName}
**Domain:** {domainName}
```

## Requirements

Every repository must include either:

1. The full navigation block with `<!-- NAVIGATION_START -->` and `<!-- NAVIGATION_END -->` markers, OR
2. The two required lines: "Pillar:", "Domain:"

Repositories missing these requirements will fail CI validation.
