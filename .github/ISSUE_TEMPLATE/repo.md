name: "🚀 Initiative"
description: Strategic or operational work starting point. Auto-generates projects, epics, stories, tasks, work packages, and sprint plans.
title: "🚀 [Initiative] <shortTitle>"
# Note: 'type' is not a standard Issue Forms key; GitHub ignores unknown keys.
type: "initiative"
assignees: ["copilot"]
projects: ["SPECTRADataSolutions/1"]
labels: ["type:initiative","status:planning"]

---
name: "📦 Repo"
description: Create a new SPECTRA repository (Pillar → Domain → Capability → Service)
title: "📦 [Repo] <repoName>"
assignees: ["copilot"]
projects: ["SPECTRADataSolutions/1"]
labels: ["type:task","status:todo","steward:guidance"]
---

### pillar
Doctrine | Transformation | Relations | Operations | Protection | Sustenance | Growth

### domain
single-token camelCase (e.g. platformSecurity)

### capability
single-token camelCase (e.g. threatDetection)

### repoName
service name in camelCase (e.g. security)

### repoType
engineering | operations | applications | governance | content

### visibility
public | private

### description
Short description of purpose and scope

### command
Paste this comment in the issue after filling the fields above:
```
/repo create <repoName> --pillar <pillar> --domain <domain> --capability <capability> --type <repoType> --visibility <visibility> --desc "<description>"
```
