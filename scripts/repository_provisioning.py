#!/usr/bin/env python3
"""Compatibility shim for renamed provisioning module.

The canonical implementation now lives in `provision_repo.py`.
Importing from this module will continue to work during the deprecation
window, but consumers should migrate to:

    from provision_repo import RepositoryProvisioner

This shim will be removed after the deprecation period.
"""
from __future__ import annotations

from provision_repo import RepositoryProvisioner, main  # type: ignore  # noqa: F401

__all__ = ["RepositoryProvisioner", "main"]
