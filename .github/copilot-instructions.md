# SPECTRA Governance Repository
SPECTRA governance framework repository providing organization-wide GitHub templates, workflows, and automated compliance for the Spectrafied 7×7×7 canonical organizational structure.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Environment Setup
- Install Node.js tools: `npm install -g ajv-cli js-yaml` -- takes 3-5 seconds
- Install Python dependencies: `pip install pyyaml requests jsonschema` -- takes 1-2 seconds, usually already installed
- **Validate installation**: `ajv help` and `python3 -c "import yaml, requests, jsonschema; print('Dependencies ready')"`

### Core Validation Commands
- **Test Python scripts**: `python3 scripts/computeDetachmentScore.py` -- takes <1 second
- **Test label readiness**: `python3 scripts/label_readiness.py --dry-run` -- takes <1 second  
- **Test anchor metrics**: `bash scripts/anchor_metrics.sh` -- takes <1 second
- **Validate labels JSON**: `python3 -c "import json; print(f'{len(json.load(open(\"labels.json\")))} labels loaded')"` -- takes <1 second
- **Check for tabs in workflows**: `grep -P "\t" workflows/*.yml | wc -l` should return 0 -- takes <1 second

### Repository Structure Validation
- **Run structure guard**: Use the validate-repository-structure workflow logic
- **Check organizational metadata**: All repositories must have proper pillar/domain/capability classification
- **Validate YAML syntax**: Most workflows are valid; some have known template issues in stabilise-source-links.yml and check-context-file.yml

## Key Scripts and Usage

### computeDetachmentScore.py
**Purpose**: Calculate SPECTRA Context System detachment score (readiness for extraction)
```bash
python3 scripts/computeDetachmentScore.py
# Output: Score 0-100, saves to detachment-score.json
# Time: <1 second
```

### label_readiness.py  
**Purpose**: Assess initiative readiness and generate GitHub labels
```bash
# Dry run (safe testing)
python3 scripts/label_readiness.py --dry-run

# With specific initiative file
python3 scripts/label_readiness.py --initiative-file path/to/initiative.json --dry-run

# Apply to GitHub issue (requires GITHUB_TOKEN)
python3 scripts/label_readiness.py --repo-owner SPECTRADataSolutions --repo-name .github --issue-number 123
# Time: <1 second for dry run, 1-2 seconds for GitHub API calls
```

### generate_lessons.py
**Purpose**: Generate initiative lessons from historical data
```bash
python3 scripts/generate_lessons.py --help
python3 scripts/generate_lessons.py --history analytics/initiatives-history.jsonl --max 10
# Time: <1 second
```

### initiative_lessons_indexer.py
**Purpose**: Index past initiative issues for lessons corpus
```bash
# Requires GITHUB_TOKEN for API access
python3 scripts/initiative_lessons_indexer.py
# Time: <1 second without token, 3-5 seconds with API calls
# Note: Will show 403 error without proper GitHub token
```

### anchor_metrics.sh
**Purpose**: Analyze anchor reachability and size metrics
```bash
bash scripts/anchor_metrics.sh
# Looks for .github/context/anchors.jsonl (not present in this repo)
# Time: <1 second
```

## Validation and Quality Gates

### Pre-commit Validation
**ALWAYS run these before committing changes (total time: <5 seconds):**
1. **Check for tabs**: `grep -P "\t" workflows/*.yml | wc -l` -- should return 0
2. **Test label JSON**: `python3 -c "import json; json.load(open('labels.json'))"`
3. **Run detachment score**: `python3 scripts/computeDetachmentScore.py`
4. **Validate core scripts**: `python3 scripts/label_readiness.py --dry-run`

### Complete Developer Scenario Validation
**Test the full developer onboarding process:**
```bash
# SCENARIO: New developer first-time setup (time: <10 seconds total)
# Step 1: Install dependencies (3-5 seconds)
npm install -g ajv-cli js-yaml
pip install pyyaml requests jsonschema

# Step 2: Validate installation (<1 second)
ajv help && python3 -c "import yaml, requests, jsonschema; print('Dependencies ready')"

# Step 3: Test core functionality (<3 seconds)
python3 scripts/computeDetachmentScore.py
python3 scripts/label_readiness.py --dry-run
bash scripts/anchor_metrics.sh

# Step 4: Validate repository compliance (<1 second)
grep -P "\t" workflows/*.yml | wc -l  # Should be 0
python3 -c "import json; print(f'{len(json.load(open(\"labels.json\")))} labels loaded')"

# SUCCESS: Developer ready for governance work
```

### Known Issues and Workarounds
- **YAML Syntax**: workflows/stabilise-source-links.yml and workflows/check-context-file.yml have template syntax issues in multiline strings
- **GitHub API**: Scripts requiring GITHUB_TOKEN will show 403 errors in testing without proper authentication
- **Missing Manifests**: anchor_metrics.sh expects .github/context/anchors.jsonl which doesn't exist in this repository (this is expected)

### Workflow Testing
- **Local validation**: Most validation can be done locally with installed tools
- **GitHub Actions**: Full workflow testing requires push to GitHub for Actions execution  
- **Dependency validation**: All Node.js and Python dependencies install successfully and quickly

## Organizational Structure Compliance

### Required Metadata
Every repository must declare:
```yaml
# .spectra/metadata.yml
pillar: [Guidance|Innovation|Engagement|Execution|Protection|Sustenance|Growth]  
domain: [single-word camelCase]
capabilities: [single-word camelCase list]
repository: [repository-name]
```

### README Navigation Block
```markdown
<!-- NAV_START -->
**Dream**: SPECTRA
**Pillar**: Guidance
**Domain**: governance  
**Capability**: framework
**Service**: .github
<!-- NAV_END -->
```

### Issue Template Integration
- 2 issue templates in .github/ISSUE_TEMPLATE/
- All templates must capture organizational metadata
- Use canonical labels from labels.json (41 labels total)

## Common Tasks

### Repository Provisioning
**Purpose**: Create new repositories with SPECTRA compliance
- **Manual**: Use repository-provisioning workflow via GitHub Actions
- **Script**: `python3 scripts/provision_repo.py` (requires GitHub App credentials)
- **Validation**: Enforces camelCase naming, canonical structure, metadata requirements

### Label Management  
**Purpose**: Maintain consistent labeling across organization
- **Sync labels**: Use sync-label-list workflow (applies labels.json to current repo)
- **Readiness assessment**: Use label_readiness.py for initiative evaluation
- **Time**: Label sync takes 5-10 seconds

### Governance Monitoring
**Purpose**: Continuous compliance validation
- **Structure validation**: validate-repository-structure workflow
- **Organization metadata**: check-org-metadata workflow  
- **Navigation blocks**: guard-canonical-navigation workflow
- **Time**: Each validation workflow runs in 30-60 seconds

## Reference Information

### Repository Contents
```
.github/                    # Organization templates
├── ISSUE_TEMPLATE/        # 2 standardized issue templates
└── workflows/             # 25 governance workflows

docs/                      # 9 governance documentation files
├── canonicalOrganisationalStructure.md
├── repositoryProvisioning.md  
├── repoStructureStandard.md
└── [other governance docs]

scripts/                   # 7 automation scripts
├── computeDetachmentScore.py     # <1s execution
├── label_readiness.py           # <1s execution  
├── generate_lessons.py          # <1s execution
├── initiative_lessons_indexer.py # <1s local, 3-5s with API
├── anchor_metrics.sh            # <1s execution
├── post_comment.py              # GitHub API integration
└── provision_repo.py            # Repository creation

workflows/                 # 25 workflow files
├── validate-repository-structure.yml
├── check-org-metadata.yml
├── sync-label-list.yml
└── [other governance workflows]

labels.json               # 41 canonical organizational labels
detachment-score.json     # Generated by score calculator
```

### Tool Dependencies
- **Node.js 10.8.2**: ajv-cli, js-yaml (install with npm -g)
- **Python 3.12**: requests, pyyaml, jsonschema (usually pre-installed)
- **System**: bash, git, standard Unix tools

### Timing Expectations
- **Script execution**: All Python/shell scripts complete in <1 second
- **Dependency installation**: npm packages install in 3-5 seconds
- **Workflow execution**: GitHub Actions workflows typically run 30-60 seconds
- **API operations**: GitHub API calls add 1-3 seconds when authenticated
- **Complete setup**: Full developer onboarding takes <10 seconds total

**NEVER CANCEL any script or validation command - they complete very quickly (<5 seconds max).**

## End-to-End Validation

### Testing All Instructions Work
**Run this comprehensive test to validate all documented functionality:**
```bash
# Validation Suite: Tests every command in the instructions
echo "=== COPILOT INSTRUCTIONS VALIDATION SUITE ==="

# 1. Test dependency installation  
npm install -g ajv-cli js-yaml
pip install pyyaml requests jsonschema

# 2. Validate tools are working
ajv help | head -1
python3 -c "import yaml, requests, jsonschema; print('✅ All Python deps ready')"

# 3. Test all core scripts with timing
echo "Testing computeDetachmentScore.py..."
time python3 scripts/computeDetachmentScore.py | tail -2

echo "Testing label_readiness.py..."  
time python3 scripts/label_readiness.py --dry-run | tail -2

echo "Testing anchor_metrics.sh..."
time bash scripts/anchor_metrics.sh | head -2

echo "Testing generate_lessons.py..."
python3 scripts/generate_lessons.py --help | head -3

echo "Testing initiative_lessons_indexer.py..."
python3 scripts/initiative_lessons_indexer.py | grep -E "(Warning|Found)" | head -2

# 4. Validate repository integrity
echo "Repository validation:"
echo "- Workflows: $(ls workflows/*.yml | wc -l) (expect 25)"
echo "- Scripts: $(ls scripts/* | wc -l) (expect 7)"  
echo "- Docs: $(ls docs/*.md | wc -l) (expect 9)"
echo "- Templates: $(ls .github/ISSUE_TEMPLATE/* | wc -l) (expect 2)"
echo "- Labels: $(python3 -c "import json; print(len(json.load(open('labels.json'))))")" "(expect 41)"

# 5. Test validation commands
echo "Tab check: $(grep -P "\t" workflows/*.yml | wc -l) (expect 0)"
python3 -c "import json; json.load(open('labels.json')); print('✅ Labels JSON valid')"

echo "=== VALIDATION COMPLETE: All instructions verified ==="
```

### Expected Results
- **Total execution time**: <15 seconds for complete validation
- **All scripts**: Should complete without errors  
- **File counts**: Must match documented numbers
- **Dependencies**: Should install and validate successfully
- **Validation**: All checks should pass with expected outputs

## Troubleshooting

### Common Issues and Solutions

**🔧 "ajv: command not found"**
```bash
# Solution: Install Node.js dependencies
npm install -g ajv-cli js-yaml
# Verify: ajv help
```

**🔧 "ImportError: No module named 'requests'"**
```bash  
# Solution: Install Python dependencies
pip install pyyaml requests jsonschema
# Verify: python3 -c "import yaml, requests, jsonschema"
```

**🔧 "403 Forbidden" errors in scripts**
- **Expected behavior**: Scripts requiring GITHUB_TOKEN will show API access errors in testing
- **Solution**: This is normal - scripts work correctly when proper GitHub credentials are available
- **For testing**: Use `--dry-run` flags where available

**🔧 "YAML syntax errors" in workflow validation**
- **Known issues**: workflows/stabilise-source-links.yml and workflows/check-context-file.yml have template syntax issues
- **Impact**: Does not affect core functionality or script execution
- **Workaround**: Individual workflows can be tested; bulk validation may show errors

**🔧 "Manifest missing" in anchor_metrics.sh**
- **Expected behavior**: Script looks for .github/context/anchors.jsonl which doesn't exist in this repository
- **Impact**: Normal operation - script handles missing manifests gracefully
- **Result**: Script completes successfully with empty metrics

### Performance Expectations
- **All scripts execute in <1 second** - if any script takes longer, check for environment issues
- **Dependencies install in <5 seconds** - if installation hangs, check network connectivity
- **Validation suite completes in <15 seconds total** - includes all dependency installation and testing