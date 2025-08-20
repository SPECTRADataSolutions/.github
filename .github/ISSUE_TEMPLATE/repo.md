# .github/ISSUE_TEMPLATE/repo.yml
name: "📦 Repo"
description: "Create a new SPECTRA repository (Pillar → Domain → Capability → Service). Non-blank description enforced."
title: "📦 [Repo] <repoName>"
assignees: ["copilot"]
projects: ["SPECTRADataSolutions/1"]
labels: ["type:task","status:todo","steward:guidance"]

body:
  - type: markdown
    attributes:
      value: |
        ## ✅ standards
        - british english spelling
        - SPECTRA in ALL CAPS
        - repo names: camelCase, singular nouns
        - camelCase only for fabric pipelines, repo names, and code
        - no secrets in code
        **core:** SPECTRA  
        ☁️ core — cross-pillar/meta/org-wide work lives under **core** (not a pillar or archetype).

  - type: dropdown
    id: pillar
    attributes:
      label: pillar
      options: [Doctrine, Transformation, Relations, Operations, Protection, Sustenance, Growth, Core]
      description: "pick the primary pillar. if higher than pillar scope, choose Core."
    validations:
      required: true

  - type: input
    id: domain
    attributes:
      label: domain
      placeholder: "platformSecurity"
      description: "single-token camelCase, pertinent to pillar (e.g., platformSecurity)."
    validations:
      required: true

  - type: input
    id: capability
    attributes:
      label: capability
      placeholder: "threatDetection"
      description: "single-token camelCase (e.g., threatDetection)."
    validations:
      required: true

  - type: input
    id: repoName
    attributes:
      label: repoName
      placeholder: "security"
      description: "service name in camelCase, singular noun (e.g., security)."
    validations:
      required: true

  - type: dropdown
    id: repoType
    attributes:
      label: repoType
      options: [engineering, operations, applications, governance, content]
      description: "classify the repository."
    validations:
      required: true

  - type: dropdown
    id: visibility
    attributes:
      label: visibility
      options: [public, private]
      description: "repository visibility."
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: description
      description: "short purpose & scope. cannot be blank."
      placeholder: "TBC"
      value: "TBC"
    validations:
      required: true

  - type: textarea
    id: command
    attributes:
      label: command
      description: "paste this as a comment after submitting (pre-filled to avoid blank)."
      render: bash
      value: |
        /repo create <repoName> --pillar <pillar> --domain <domain> --capability <capability> --type <repoType> --visibility <visibility> --desc "<description>"
    validations:
      required: true
