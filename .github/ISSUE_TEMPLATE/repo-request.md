---
name: "📦 Repo Request"
description: Create a new SPECTRA repository (Pillar → Domain → Capability → Service)
title: "📦 [Repo] <repoName>"
labels: ["type:task","status:todo","steward:guidance"]
---

### pillar
Guidance | Innovation | Engagement | Operations | Protection | Sustenance | Growth

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