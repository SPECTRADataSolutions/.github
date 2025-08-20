#!/usr/bin/env python3
"""
Blocks disallowed abbreviations such as 'org' when used as a standalone word.
British English spellings are preferred. This guard intentionally scans only
human-facing docs: .md, .mdx, .txt to avoid false positives in code.
"""

import re
import sys
from pathlib import Path


def initialiseLogger():
    import logging
    logger = logging.getLogger("languageStyleGuard")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
        logger.addHandler(handler)
    return logger


logger = initialiseLogger()

# Disallowed standalone abbreviations → preferred form (advice only used in messages)
banned = {
    r"\borg\b": "organisation",   # never shorten
    r"\bdept\b": "department",    # guard similar habits
    r"\binfo\b": "information"    # common shorthand in docs
}

# File types to scan (documentation only)
docGlobs = ["**/*.md", "**/*.mdx", "**/*.txt"]


def loadRepositoryFiles():
    files = []
    for pat in docGlobs:
        files.extend(Path(".").rglob(pat))
    return files


def scanRepositoryText(files):
    violations = []

    for f in files:
        # Skip common vendor or hidden folders
        if any(seg in f.parts for seg in (".git", ".venv", "node_modules", "dist", "build", ".mypy_cache")):
            continue

        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            # Non-fatal; skip unreadable files
            continue

        # Fast skip
        if not re.search(r"\b(org|dept|info)\b", text, re.IGNORECASE):
            continue

        for i, line in enumerate(text.splitlines(), start=1):
            for pat, preferred in banned.items():
                for m in re.finditer(pat, line, re.IGNORECASE):
                    # Check context around the match to allow certain patterns
                    start = max(0, m.start() - 10)
                    end = min(len(line), m.end() + 10)
                    context = line[start:end]
                    
                    # Skip if it's part of a URL
                    if re.search(r"https?://", context, re.IGNORECASE):
                        continue
                    
                    # Skip if it's a .org domain (word before .org or .org itself)
                    if re.search(r"\.org\b", context, re.IGNORECASE):
                        continue
                    
                    # Skip if followed by punctuation that suggests compound/filename
                    nxt = line[m.end():m.end()+1]
                    if nxt in ["/", ".", "-"]:
                        continue
                    
                    # Skip if preceded by colon (technical parameters like admin:org)
                    prev = line[max(0, m.start()-1):m.start()]
                    if prev == ":":
                        continue
                    
                    # Skip if the word appears within quotes (examples of what not to do)
                    line_before_match = line[:m.start()]
                    line_after_match = line[m.end():]
                    
                    # Count quotes before and after to see if we're inside quotes
                    quotes_before = line_before_match.count('"') + line_before_match.count("'")
                    quotes_after = line_after_match.count('"') + line_after_match.count("'")
                    
                    # If odd number of quotes before, we're likely inside quotes
                    if quotes_before % 2 == 1:
                        continue
                    
                    segment = line.strip()
                    violations.append((str(f), i, segment, preferred))
    return violations


def reportStyleViolations(violations):
    if not violations:
        logger.info("✅ Language style check passed: no disallowed abbreviations found in docs.")
        return 0
    logger.error("❌ Disallowed abbreviations detected (use full words, e.g., 'organisation'):")
    for path, lineNo, segment, preferred in violations[:100]:
        logger.error(f"{path}:{lineNo} → '{segment}'  (prefer: '{preferred}')")
    if len(violations) > 100:
        logger.error(f"... and {len(violations)-100} more occurrences.")
    return 1


if __name__ == "__main__":
    files = loadRepositoryFiles()
    violations = scanRepositoryText(files)
    sys.exit(reportStyleViolations(violations))