#!/usr/bin/env python3
"""SPECTRA Repository Provisioning (Canonical Module)

This is the canonical provisioning module (renamed from repository_provisioning).
Provides RepositoryProvisioner for creating new repositories under SPECTRA
standards. The previous filename `repository_provisioning.py` remains as a
compatibility shim and will be removed in a future cleanup.
"""
from __future__ import annotations

# Re-export the full implementation from the legacy module to keep single source
# of truth during the rename; after deprecation window we can inline here.
from repository_provisioning import RepositoryProvisioner, main  # type: ignore  # noqa: F401

__all__ = ["RepositoryProvisioner", "main"]
