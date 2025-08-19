# 🔄 Service Repository Generation (Migrated)

**This documentation has been superseded by the new Service Repository Generator.**

Please use the new documentation and workflows:

📄 **[Service Repository Generation Documentation](./generateServiceRepository.md)**

🔧 **New Workflows:**
- `generateServiceRepository.yml` - Main service repository creation workflow
- `generateServiceRepositorySlash.yml` - Slash command trigger for repository creation
- `repoStructureGuard.yml` - Repository structure validation

## What Changed

The repository creation automation has been updated to follow SPECTRA's three-word, camelCase, verb-first naming conventions:

- `repoFactory.yml` → `generateServiceRepository.yml`
- `repoFactorySlash.yml` → `generateServiceRepositorySlash.yml`
- Updated to use British English throughout
- Enhanced Pillar → Domain → Capability → Service metadata structure
- Improved compliance with SPECTRA standards

## Migration Note

All existing functionality remains the same, with improved naming and documentation. The slash command syntax is unchanged:

```
/repo create governancePolicy --pillar Protection --domain platformSecurity --capability threatDetection --type governance --visibility private
```

---

*This file is maintained for backwards compatibility. Please use [generateServiceRepository.md](./generateServiceRepository.md) for current documentation.*