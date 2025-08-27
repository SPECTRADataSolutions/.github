#!/usr/bin/env python3
"""
Repository Provisioning Shim

This shim preserves backward compatibility while transitioning from the
deprecated 'Repository Factory' terminology. It re-exports the implementation
from repo_factory.py. New code should import RepositoryFactory from this module
using the clearer provisioning nomenclature during the deprecation window.
"""
from repo_factory import RepositoryFactory  # noqa: F401
