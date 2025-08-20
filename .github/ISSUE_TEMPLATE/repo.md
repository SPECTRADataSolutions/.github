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
        ## standards
        - british english spelling
        - SPECTRA in ALL CAPS
        - repo names: camelCase, singular nouns
        - camelCase only for fabric pipelines, repo names, and code
        - no secrets in code  
        **core:** SPECTRA — cross-pillar/meta/org-wide work belongs under core.

  - type: dropdown
    id: pillar
    attributes:
      label: pillar
      description: "pick the primary pillar. if higher than pillar scope, choose Core."
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
      description: "single-token camelCase pertinent to pillar."
      placeholder: "platformSecurity"
    validations:
      required: true

  - type: input
    id: capability
    attributes:
      label: capability
      description: "single-token camelCase."
      placeholder: "threatDetection"
    validations:
      required: true

  - type: input
    id: repoName
    attributes:
      label: repoName
      description: "service name in camelCase, singular noun."
      placeholder: "security"
    validations:
      required: true

  - type: dropdown
    id: repoType
    attributes:
      label: repoType
      description: "classify the repository."
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
      description: "repository visibility."
      options:
        - public
        - private
    validations:
      required: true

  - type: textarea
    id: repoDescription
    attributes:
      label: description
      description: "short purpose & scope (cannot be blank)."
      placeholder: "TBC"
      value: "TBC"
    validations:
      required: true

  - type: textarea
    id: command
    attributes:
      label: command
      description: "paste this as a comment after submitting (pre-filled to avoid blank)."
      render: shell
      value: |
        /repo create <repoName> --pillar <pillar> --domain <domain> --capability <capability> --type <repoType> --visibility <visibility> --desc "<repoDescription>"
    validations:
      required: true
