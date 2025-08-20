name: "📦 Repo"
description: "Create a new SPECTRA repository (Pillar → Domain → Capability → Service)."
title: "📦 [Repo] <repoName>"
assignees: ["copilot"]
projects: ["SPECTRADataSolutions/1"]
labels: ["type:task","status:todo","steward:guidance"]

body:
  - type: dropdown
    id: pillar
    attributes:
      label: pillar
      options: [Doctrine, Transformation, Relations, Operations, Protection, Sustenance, Growth, Core]
    validations:
      required: true

  - type: input
    id: domain
    attributes:
      label: domain
      placeholder: "platformSecurity"
    validations:
      required: true

  - type: input
    id: capability
    attributes:
      label: capability
      placeholder: "threatDetection"
    validations:
      required: true

  - type: input
    id: repoName
    attributes:
      label: repoName
      placeholder: "security"
    validations:
      required: true

  - type: dropdown
    id: repoType
    attributes:
      label: repoType
      options: [engineering, operations, applications, governance, content]
    validations:
      required: true

  - type: dropdown
    id: visibility
    attributes:
      label: visibility
      options: [public, private]
    validations:
      required: true

  - type: textarea
    id: repoDescription
    attributes:
      label: description
      placeholder: "TBC"
    validations:
      required: true

  - type: textarea
    id: command
    attributes:
      label: command
      render: shell
      value: |
        /repo create <repoName> --pillar <pillar> --domain <domain> --capability <capability> --type <repoType> --visibility <visibility> --desc "<repoDescription>"
