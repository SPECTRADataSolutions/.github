name: "📦 Repo"
description: "Create a new SPECTRA repository (Pillar → Domain → Capability → Service)."
title: "📦 [Repo] <repoName>"
assignees: ["copilot"]
projects: ["SPECTRADataSolutions/1"]
labels: ["type:task","status:todo","steward:guidance"]

body:
  - type: markdown
    attributes:
      value: |
        ## Standards
        - British English spelling
        - SPECTRA in ALL CAPS
        - Repo names: camelCase, singular nouns
        - camelCase only for Fabric pipelines, repo names, and code
        - No secrets in code
        **Core:** SPECTRA
        ☁️ core — All cross-pillar, meta, or org-wide work is governed by core. Never categorise or label it as a pillar or archetype.

  - type: dropdown
    id: pillar
    attributes:
      label: pillar
      description: "Pick the primary pillar. If higher than pillar scope, choose Core."
      options:
        - Doctrine
        - Transformation
        - Relations
        - Operations
        - Protection
        - Sustenance
        - Growth
        - Core
    validations:
      required: true

  - type: input
    id: domain
    attributes:
      label: domain
      description: "Single-token camelCase pertinent to pillar (e.g., platformSecurity)."
      placeholder: "platformSecurity"
    validations:
      required: true

  - type: input
    id: capability
    attributes:
      label: capability
      description: "Single-token camelCase (e.g., threatDetection)."
      placeholder: "threatDetection"
    validations:
      required: true

  - type: input
    id: repoName
    attributes:
      label: repoName
      description: "Service name in camelCase, singular noun (e.g., security)."
      placeholder: "security"
    validations:
      required: true

  - type: dropdown
    id: repoType
    attributes:
      label: repoType
      description: "Classify the repository."
      options:
        - engineering
        - operations
        - applications
        - governance
        - content
    validations:
      required: true

  - type: dropdown
    id: visibility
    attributes:
      label: visibility
      description: "Repository visibility."
      options:
        - public
        - private
    validations:
      required: true

  - type: textarea
    id: repoDescription
    attributes:
      label: description
      description: "Short purpose & scope (cannot be blank)."
      placeholder: "TBC"
      value: "TBC"
    validations:
      required: true

  - type: textarea
    id: command
    attributes:
      label: command
      description: "Paste as a comment after submitting (pre-filled to avoid blank)."
      render: shell
      value: |
        /repo create <repoName> --pillar <pillar> --domain <domain> --capability <capability> --type <repoType> --visibility <visibility> --desc "<repoDescription>"
    validations:
      required: true
