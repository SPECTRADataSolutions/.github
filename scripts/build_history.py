#!/usr/bin/env python3
"""TOMBSTONE: build_history.py has been removed.

This file is intentionally left as a hard-stop sentinel because direct file deletion
is currently not persisting in the automation environment.

Canonical replacement: initiative_lessons_indexer.py

To migrate:
    from initiative_lessons_indexer import InitiativeLessonsIndexer

Any attempt to execute or import symbols from this module will raise immediately.
"""
from __future__ import annotations

MESSAGE = "build_history.py has been retired. Use initiative_lessons_indexer.py / InitiativeLessonsIndexer instead."


def _abort() -> None:  # pragma: no cover - defensive sentinel
    raise RuntimeError(MESSAGE)


# If imported, raise loudly so lingering references are surfaced early.
_abort()

__all__ = []
