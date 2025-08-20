# Repository Factory Usage Examples

## Basic Repository Creation

### Create a Public Repository
```
/create-repo repoName=userDashboard domain=engagement visibility=public
```

### Create a Private Repository
```
/create-repo repoName=securityAudit domain=protection visibility=private
```

### Create from Template
```
/create-repo repoName=governancePolicy domain=governance visibility=private templateRepo=SPECTRADataSolutions/blueprint
```

## Command Parameters

### Required Parameters
- `repoName`: Must be camelCase (e.g., `userInterface`, `dataProcessor`)
- `domain`: Must be camelCase domain name (e.g., `governance`, `analytics`)
- `visibility`: Must be `public` or `private`

### Optional Parameters
- `templateRepo`: Must be `SPECTRADataSolutions/templateName`

## Expected Results

When successful, the command will:
1. Create the repository in SPECTRADataSolutions organisation
2. Set the default branch to `main`
3. Seed with all canonical SPECTRA labels
4. Add organisational metadata (`.spectra/metadata.yml`)
5. Create baseline README with organisational structure
6. Post success comment with repository URL

## Error Scenarios

### Invalid Repository Name
```
/create-repo repoName=user-dashboard domain=engagement visibility=public
```
**Error:** `❌ repoName must be single-token camelCase (e.g., 'governancePolicy')`

### Missing Required Parameter
```
/create-repo repoName=userDashboard domain=engagement
```
**Error:** `❌ Missing required parameter: visibility`

### Repository Already Exists
```
/create-repo repoName=existingRepo domain=governance visibility=private
```
**Error:** `❌ Repository 'existingRepo' already exists in SPECTRADataSolutions`

### Unauthorized User
If a non-organisation member tries to use the command:
**Error:** `❌ Access Denied - Repository creation is restricted to SPECTRADataSolutions organisation members only`

## Next Steps After Creation

1. **Update Archetype**: Edit `.spectra/metadata.yml` to set the correct archetype
2. **Configure Branch Protection**: Set up protection rules for the main branch
3. **Add CI/CD**: Configure GitHub Actions workflows as needed
4. **Update Documentation**: Customize the README with project-specific information
5. **Set Up Teams**: Configure appropriate team permissions

## Framework Compliance

All repositories created by the Factory automatically include:
- SPECTRA organisational metadata
- Canonical labelling system
- Baseline documentation structure
- British English compliance
- Framework-as-law principles