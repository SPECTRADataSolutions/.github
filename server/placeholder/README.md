# SPECTRA Context Runtime Contract

This directory contains placeholder contracts for the future SPECTRA Context runtime implementation.

## 🎯 Runtime Endpoints

The SPECTRA Context runtime will expose the following RESTful endpoints:

### Health Check
```
GET /health
```
**Purpose:** System health and readiness check  
**Response:** JSON with status, uptime, schema version  
**Example:**
```json
{
  "status": "healthy",
  "uptime": 3600,
  "schemaVersion": "1.0.0",
  "frameworkCommit": "abc123...",
  "detachmentScore": 100
}
```

### List Anchors
```
GET /anchors
GET /anchors?tags=starfighter,technical&pillar=Guidance
```
**Purpose:** Retrieve all available anchors with optional filtering  
**Query Parameters:**
- `tags` - Comma-separated list of tags to filter by
- `pillar` - Filter by SPECTRA pillar (Guidance, Innovation, etc.)
- `domain` - Filter by domain within pillar
- `limit` - Maximum number of results (default: 50)
- `offset` - Pagination offset

**Response:** JSON array of anchor metadata (without content)

### Get Anchor by ID
```
GET /anchors/{id}
```
**Purpose:** Retrieve full anchor content by ID  
**Parameters:**
- `id` - Unique anchor identifier (camelCase)

**Response:** Complete anchor JSON with content, metadata, and cache information

### Search Anchors
```
GET /search?query=X-wing&limit=10
POST /search
```
**Purpose:** Full-text search across anchor content and metadata  
**Query Parameters (GET):**
- `query` - Search terms
- `limit` - Maximum results
- `pillar` - Filter by pillar
- `tags` - Filter by tags

**POST Body:**
```json
{
  "query": "X-wing fighter",
  "filters": {
    "pillar": ["Guidance"],
    "tags": ["starfighter", "technical"],
    "domain": "context"
  },
  "limit": 10,
  "includeContent": false
}
```

**Response:** Search results with ranking, snippets, and metadata

### Organisational Hierarchy
```
GET /hierarchy
GET /hierarchy/{role}
```
**Purpose:** Retrieve organisational structure and role-based context  
**Parameters:**
- `role` - Optional role filter for role-specific hierarchy view

**Response:** Hierarchical structure with role-aware helpers and context

## 🔧 Detachment Score

The runtime includes a **detachment score** system that measures how ready the context system is for extraction into its own repository:

**Current Detachment Score: 100**

### Score Calculation
- **100**: Perfect detachment readiness (no coupled imports, clear boundaries)
- **75-99**: Minor coupling detected  
- **50-74**: Moderate coupling requiring refactoring
- **25-49**: Significant coupling blocking extraction
- **0-24**: Tightly coupled, not ready for extraction

### Monitored Factors
- Cross-folder relative imports outside `server/`
- Dependencies on root-level configuration
- Shared utility functions requiring duplication
- Hard-coded paths or repository-specific logic

## 🚀 Split Trigger Thresholds

Extraction to independent repository will be triggered when ANY of the following criteria are met:

1. **Contributors Velocity:** >3 active contributors on context system per sprint
2. **Deploy Cadence Divergence:** Context system deployment needs differ from main repo by >2 weeks
3. **Performance Friction:** Context runtime resource usage >25% of total repository CI time
4. **External Consumer:** First external consumer (non-SPECTRA organisation) requests access

## 🏗️ Implementation Status

**Current Phase:** Scaffold & Contracts  
**Next Phase:** FastAPI Runtime Implementation  
**Future Phases:** Search Indexing, Bundle Release Pipeline

### Detachment Rules
- ✅ No cross-folder relative imports outside `server/`
- ✅ Self-contained configuration within `server/`
- ✅ Clear API boundaries defined in this contract
- ✅ Independent testing and validation workflows
- ✅ Dedicated governance in `governance/` folder

---

**Detachment Score:** 100 🎯  
**Framework Compliance:** ✅ Enforced  
**Delight Mode:** 🌟 Enabled