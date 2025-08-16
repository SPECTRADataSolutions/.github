# 🏭 SPECTRA Repository Factory

The Repository Factory provides an automated way to create new repositories from Initiative issues using slash commands. This ensures all new repositories start with proper organizational structure, canonical labels, and compliance standards.

## Usage

### Slash Command Syntax

Post a comment on any Initiative issue with the following command:

```
/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint
```

### Parameters

| Parameter | Required | Format | Description |
|-----------|----------|--------|-------------|
| `repoName` | ✅ | camelCase | Single-token repository name (e.g., `governancePolicy`, `userInterface`) |
| `domain` | ✅ | camelCase | Single-token domain pertinent to archetype (e.g., `governance`, `security`) |
| `visibility` | ✅ | `public` or `private` | Repository visibility setting |
| `templateRepo` | ⭕ | `SPECTRADataSolutions/repoName` | Optional template repository to use |

### Example Commands

```bash
# Create a private governance repository from template
/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint

# Create a public repository without template
/create-repo repoName=userInterface domain=engagement visibility=public

# Create a private operations repository
/create-repo repoName=monitoringDashboard domain=operations visibility=private
```

## Authorization

- Only SPECTRADataSolutions organization members can create repositories
- Comments from unauthorized users receive an access denied response
- Organization membership verification is performed automatically

## Repository Provisioning

When a repository is created, the following actions are performed:

### 1. Repository Creation
- Creates repository in SPECTRADataSolutions organization
- Sets default branch to `main`
- Configures visibility (public/private) as specified
- Creates from template if `templateRepo` is provided

### 2. Canonical Label Seeding
- Seeds repository with all canonical labels from `.github/labels.json`
- Includes standard SPECTRA labels for issues, status, and stewardship
- Maintains consistent labelling across all repositories

### 3. Organizational Metadata
- Adds `.spectra/metadata.yml` with organizational structure
- Includes dream, archetype (TBD), domain, and repository name
- Provides machine-readable organizational classification

### 4. Baseline Files (if not templated)
- Creates comprehensive `README.md` with organizational structure
- Includes setup instructions and SPECTRA framework links
- Adds Python `.gitignore` template
- Provides starting point for project documentation

## Response Handling

The Repository Factory provides immediate feedback through issue comments:

### Success Response
```markdown
## 🏭 Repository Factory - Success

✅ **Repository Created:** [governancePolicy](https://github.com/SPECTRADataSolutions/governancePolicy)

**Repository Details:**
- **URL:** https://github.com/SPECTRADataSolutions/governancePolicy
- **Visibility:** Private
- **Default Branch:** main
- **Canonical Labels:** Seeded from .github/labels.json
- **Organizational Metadata:** Added to .spectra/metadata.yml

**Next Steps:**
1. Update the archetype in `.spectra/metadata.yml` based on repository purpose
2. Configure branch protection rules
3. Set up CI/CD workflows as needed
4. Update README with project-specific information
```

### Error Response
```markdown
## 🏭 Repository Factory - Failed

❌ **Repository Creation Failed**

**Warnings:**
- ❌ repoName must be single-token camelCase (e.g., 'governancePolicy')
- ❌ Missing required parameter: visibility
```

## Validation Rules

### Repository Name (`repoName`)
- Must be single-token camelCase
- No spaces, hyphens, underscores, or special characters
- Must start with lowercase letter
- Examples: ✅ `governancePolicy`, ❌ `governance-policy`, ❌ `GovernancePolicy`

### Domain (`domain`)
- Must be single-token camelCase
- Should be pertinent to the repository's archetype
- Examples: ✅ `governance`, `security`, `analytics`

### Visibility (`visibility`)
- Must be exactly `public` or `private`
- Required parameter for security compliance

### Template Repository (`templateRepo`)
- Must be from SPECTRADataSolutions organization
- Format: `SPECTRADataSolutions/repositoryName`
- Optional parameter

## Governance Integration

### Framework as Law
- All repositories created follow SPECTRA organizational standards
- Consistent metadata structure across all repositories
- Enforced naming conventions and compliance requirements

### Organizational Structure
All created repositories include:
- **Dream:** SPECTRA (fixed)
- **Archetype:** TBD (requires manual classification)
- **Domain:** As specified in command
- **Repository:** Repository name

### Post-Creation Requirements
1. **Archetype Classification:** Update `.spectra/metadata.yml` with appropriate archetype
2. **Branch Protection:** Configure protection rules for main branch
3. **CI/CD Setup:** Add necessary workflows and automation
4. **Documentation:** Update README with project-specific information

## Technical Implementation

### Workflow Trigger
- Triggered on `issue_comment` events with `created` type
- Only processes comments on issues labeled `type:initiative`
- Only processes comments containing `/create-repo`

### Security
- Organization membership verification
- Admin token required for repository creation
- Audit trail through GitHub Actions logs

### Error Handling
- Parameter validation with detailed error messages
- Graceful failure with informative responses
- Warning collection for non-critical issues

## Extensibility

Future enhancements planned:
- **Branch Protection:** Automatic branch protection rule setup
- **Team Permissions:** Default team assignments based on domain
- **Compliance Workflows:** Reusable workflow integration
- **Template Validation:** Template repository compliance checking

## Support

For issues with the Repository Factory:
- Check parameter format and values
- Verify organization membership
- Review Initiative issue for proper labelling
- Contact SPECTRA stewards for assistance

---

> 🏛️ **Governance Principle**: The Repository Factory ensures every new repository starts compliant with SPECTRA standards and is traceable to its originating Initiative.