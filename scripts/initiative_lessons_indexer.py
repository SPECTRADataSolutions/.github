#!/usr/bin/env python3
"""SPECTRA Initiative Lessons Indexer

Purpose
=======
Index past initiative issues into a lightweight lessons & evidence corpus
used by downstream automation (similarity matching, readiness labelling,
recommendation synthesis). This replaces the generic *build_history* name
with a governance-aligned, intent-revealing identity.

SPECTRA Principles Embodied
---------------------------
- Specificity: Focus on *lessons* and *indexing* (not vague "history")
- Provenance: Retains raw parsed fields alongside derived signals
- Efficiency: Single pass GitHub API collection with pagination safety
- Clarity: Deterministic field extraction using markdown section headers
- Traceability: Produces JSONL for append-friendly audit / replay

Output
------
analytics/initiatives-history.jsonl  (one JSON object per initiative)

Each record contains:
- initiativeId, issueNumber, title
- archetype, domain, status, timestamps
- lessons: risks, mitigations, root_causes, success_factors, recommendations
- similarity_keywords: curated keyword list for TF-IDF / vectorisation
- raw_fields: original parsed markdown sections (future enrichment)

Deprecation Note
----------------
Original module name build_history.py now shims to this file and will be
removed after the deprecation window.
"""
from __future__ import annotations

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

try:  # pragma: no cover
    import requests  # type: ignore
except ImportError:  # pragma: no cover
    requests = None  # type: ignore

STOP_WORDS = {
    "the",
    "and",
    "for",
    "are",
    "but",
    "not",
    "you",
    "all",
    "can",
    "had",
    "her",
    "was",
    "one",
    "our",
    "out",
    "day",
    "get",
    "has",
    "him",
    "his",
    "how",
    "man",
    "new",
    "now",
    "old",
    "see",
    "two",
    "way",
    "who",
    "boy",
    "did",
    "its",
    "let",
    "put",
    "say",
    "she",
    "too",
    "use",
}


class InitiativeLessonsIndexer:
    def __init__(
        self,
        github_token: Optional[str] = None,
        repo_owner: str = "SPECTRADataSolutions",
        repo_name: str = ".github",
    ):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Initiative-Lessons-Indexer",
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"

    def build_index(
        self, output_path: str = "analytics/initiatives-history.jsonl"
    ) -> List[Dict[str, Any]]:
        """Collect initiative issues and emit JSONL lessons index."""
        print("🔍 SPECTRA Initiative Lessons Indexer")
        print("=" * 52)
        initiatives = self._fetch_initiative_issues()
        print(f"📊 Found {len(initiatives)} initiative issues")

        entries: List[Dict[str, Any]] = []
        for issue in initiatives:
            entry = self._process_initiative(issue)
            if entry:
                entries.append(entry)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"✅ Built lessons index: {len(entries)} entries saved to {output_path}")
        return entries

    # --- Data Acquisition ---
    def _fetch_initiative_issues(self) -> List[Dict[str, Any]]:
        if requests is None:
            print("⚠️ 'requests' library not installed; skipping remote fetch")
            return []
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params: Dict[str, Any] = {
            "labels": "type:initiative",
            "state": "all",
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        }
        issues: List[Dict[str, Any]] = []
        page = 1
        while True:
            params["page"] = page
            try:
                response = requests.get(url, headers=self.headers, params=params)  # type: ignore[arg-type]
                response.raise_for_status()
                page_issues = response.json()
                if not page_issues:
                    break
                initiative_issues = [
                    issue
                    for issue in page_issues
                    if any(
                        label["name"] == "type:initiative"
                        for label in issue.get("labels", [])
                    )
                ]
                issues.extend(initiative_issues)
                page += 1
                if page > 10:  # safety bound
                    break
            except Exception as e:  # pragma: no cover
                print(f"⚠️ Error fetching issues (page {page}): {e}")
                break
        return issues

    # --- Processing ---
    def _process_initiative(self, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            title = issue.get("title", "")
            body = issue.get("body", "")
            state = issue.get("state", "open")
            initiative_id = self._extract_initiative_id(title, issue.get("number"))
            fields = self._parse_issue_body(body)
            lessons = self._extract_lessons(fields, state)
            keywords = self._generate_keywords(fields, title)
            return {
                "initiativeId": initiative_id,
                "issueNumber": issue.get("number"),
                "title": title,
                "archetype": fields.get("archetype", "Unknown"),
                "domain": fields.get("domain", "unknown"),
                "status": self._map_status(state, fields.get("outcomeStatus")),
                "createdAt": issue.get("created_at"),
                "updatedAt": issue.get("updated_at"),
                "lessons": lessons,
                "similarity_keywords": keywords,
                "raw_fields": fields,
            }
        except Exception as e:  # pragma: no cover
            print(f"⚠️ Error processing issue #{issue.get('number', 'unknown')}: {e}")
            return None

    def _extract_initiative_id(self, title: str, issue_number: Optional[int]) -> str:
        match = re.search(r"\[Initiative\]\s*([^[]+?)(?:\s|$)", title)
        if match:
            raw_title = match.group(1).strip()
            initiative_id = re.sub(r"[^a-zA-Z0-9]+", "", raw_title)
            if initiative_id:
                return initiative_id
        return f"initiative{issue_number}"

    def _parse_issue_body(self, body: str) -> Dict[str, str]:
        fields: Dict[str, str] = {}
        patterns = [
            "archetype",
            "domain",
            "initiativeTitle",
            "purpose",
            "scope",
            "capabilityAreas",
            "deliverables",
            "successIndicators",
            "constraints",
            "dependencies",
            "outcomeStatus",
            "postmortem",
            "lessonsFromPastInitiatives",
        ]
        for field in patterns:
            pattern = rf"###\s*{field}\s*\n\s*([^#]*?)(?=\n###|\n\n|\Z)"
            match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                content = re.sub(r"^[-*]\s*", "", content, flags=re.MULTILINE)
                fields[field] = content
        return fields

    def _extract_lessons(
        self, fields: Dict[str, str], state: str
    ) -> Dict[str, List[str]]:
        lessons: Dict[str, List[str]] = {
            "risks": [],
            "mitigations": [],
            "root_causes": [],
            "success_factors": [],
            "recommendations": [],
        }
        postmortem = fields.get("postmortem", "")
        if postmortem:
            lessons["root_causes"].extend(self._extract_root_causes(postmortem))
            lessons["mitigations"].extend(self._extract_mitigations(postmortem))
        constraints = fields.get("constraints", "")
        if constraints:
            lessons["risks"].extend(self._extract_risks_from_constraints(constraints))
        scope = fields.get("scope", "")
        if scope and "outOfScope" in scope:
            lessons["risks"].extend(self._extract_scope_risks(scope))
        if state == "closed" and fields.get("outcomeStatus") == "delivered":
            success_indicators = fields.get("successIndicators", "")
            if success_indicators:
                lessons["success_factors"].extend(
                    self._extract_success_factors(success_indicators)
                )
        return lessons

    def _extract_root_causes(self, postmortem: str) -> List[str]:
        causes: List[str] = []
        patterns = [
            r"rootCause[:\s]+([^,\n]+)",
            r"root\s+cause[:\s]+([^,\n]+)",
            r"caused\s+by[:\s]+([^,\n]+)",
            r"due\s+to[:\s]+([^,\n]+)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, postmortem, re.IGNORECASE)
            causes.extend([m.strip() for m in matches if m.strip()])
        return causes[:3]

    def _extract_mitigations(self, postmortem: str) -> List[str]:
        mitigations: List[str] = []
        patterns = [
            r"mitigation[s]?[:\s]+([^,\n]+)",
            r"to\s+prevent[:\s]+([^,\n]+)",
            r"solution[:\s]+([^,\n]+)",
            r"resolved\s+by[:\s]+([^,\n]+)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, postmortem, re.IGNORECASE)
            mitigations.extend([m.strip() for m in matches if m.strip()])
        return mitigations[:3]

    def _extract_risks_from_constraints(self, constraints: str) -> List[str]:
        risks: List[str] = []
        indicators = [
            "budget",
            "timeline",
            "resource",
            "dependency",
            "complexity",
            "security",
            "compliance",
            "integration",
            "scalability",
        ]
        for ind in indicators:
            if ind in constraints.lower():
                risks.append(f"Potential {ind} constraints")
        return risks[:2]

    def _extract_scope_risks(self, scope: str) -> List[str]:
        risks: List[str] = []
        m = re.search(r"outOfScope[:\s]*([^,\n]+)", scope, re.IGNORECASE)
        if m:
            out_items = m.group(1)
            if "sync" in out_items.lower():
                risks.append("Data synchronisation complexity")
            if "integration" in out_items.lower():
                risks.append("External integration challenges")
        return risks

    def _extract_success_factors(self, success_indicators: str) -> List[str]:
        factors: List[str] = []
        for line in success_indicators.split("\n"):
            line = line.strip()
            if line and not line.startswith("-"):
                factors.append(f"Achieved: {line}")
        return factors[:2]

    def _generate_keywords(self, fields: Dict[str, str], title: str) -> List[str]:
        keywords: List[str] = []
        if fields.get("archetype"):
            keywords.append(fields["archetype"].lower())
        if fields.get("domain"):
            keywords.append(fields["domain"].lower())
        text_fields = [
            title,
            fields.get("purpose", ""),
            fields.get("initiativeTitle", ""),
        ]
        for text in text_fields:
            if text:
                words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
                meaningful = [w for w in words if w not in STOP_WORDS]
                keywords.extend(meaningful)
        return list(dict.fromkeys(keywords))[:10]

    def _map_status(self, github_state: str, outcome_status: Optional[str]) -> str:
        if outcome_status:
            return outcome_status
        return "inProgress" if github_state == "open" else "completed"


def main():  # pragma: no cover
    print("🔍 SPECTRA Initiative Lessons Indexer")
    if not os.environ.get("GITHUB_TOKEN"):
        print("⚠️ Warning: No GITHUB_TOKEN found. API rate limits may apply.")
    indexer = InitiativeLessonsIndexer()
    try:
        entries = indexer.build_index()
        print(f"✅ Successfully built lessons index with {len(entries)} entries")
        return 0
    except Exception as e:
        print(f"❌ Error building lessons index: {e}")
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
