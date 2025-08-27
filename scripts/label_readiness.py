#!/usr/bin/env python3
"""SPECTRA Initiative Readiness Labeller

Assesses initiative metadata & inferred lessons to produce a readiness score,
recommendations, and a deterministic set of GitHub issue labels.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple, cast

try:  # optional dependency (script still usable in dry-run without it)
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore


class InitiativeReadinessLabeller:
    def __init__(self, github_token: Optional[str] = None) -> None:
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers: Dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Initiative-Readiness-Labeller",
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"

    # Public API ---------------------------------------------------------
    def assess_readiness(
        self,
        initiative_data: Dict[str, Any],
        lessons_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        print(
            f"🔍 Assessing readiness for: {initiative_data.get('initiativeTitle', 'Unknown')}"
        )
        score, breakdown = self._calculate_readiness_score(
            initiative_data, lessons_data
        )
        level = self._determine_readiness_level(score)
        recs = self._generate_readiness_recommendations(breakdown, level)
        add, remove = self._determine_labels(level, initiative_data)
        return {
            "readiness_score": score,
            "readiness_level": level,
            "score_breakdown": breakdown,
            "recommendations": recs,
            "labels_to_add": add,
            "labels_to_remove": remove,
        }

    def apply_readiness_labels(
        self,
        repo_owner: str,
        repo_name: str,
        issue_number: int,
        labels_to_add: List[str],
        labels_to_remove: List[str],
        dry_run: bool = False,
    ) -> bool:
        if not self.github_token and not dry_run:
            print("❌ No GitHub token available for label updates.")
            return False
        if requests is None and not dry_run:
            print("❌ 'requests' library not available; cannot modify labels.")
            return False
        if dry_run:
            print("🔍 DRY RUN - Label changes:")
            if labels_to_add:
                print("  Add: " + ", ".join(labels_to_add))
            if labels_to_remove:
                print("  Remove: " + ", ".join(labels_to_remove))
            return True
        ok = True
        if labels_to_add:
            ok &= self._add_labels(repo_owner, repo_name, issue_number, labels_to_add)
        if labels_to_remove:
            ok &= self._remove_labels(
                repo_owner, repo_name, issue_number, labels_to_remove
            )
        return ok

    # Scoring ------------------------------------------------------------
    def _calculate_readiness_score(
        self,
        initiative: Dict[str, Any],
        lessons: Optional[Dict[str, Any]] = None,
    ) -> Tuple[float, Dict[str, float]]:
        breakdown: Dict[str, float] = {
            "completeness": 0.0,
            "clarity": 0.0,
            "planning": 0.0,
            "lessons_integration": 0.0,
            "risk_awareness": 0.0,
        }

        # Completeness (30)
        required = [
            "archetype",
            "domain",
            "initiativeTitle",
            "purpose",
            "scope",
            "capabilityAreas",
            "deliverables",
            "successIndicators",
        ]

        def _nonempty(v: Any) -> bool:
            if v is None:
                return False
            if isinstance(v, str):
                return bool(v.strip())
            if isinstance(v, Sequence):
                return any(str(x).strip() for x in cast(Sequence[Any], v))
            return True

        filled = sum(1 for f in required if _nonempty(initiative.get(f)))
        breakdown["completeness"] = (filled / len(required)) * 30

        # Clarity (25)
        clar = 0.0
        purpose = str(initiative.get("purpose", "") or "")
        if purpose:
            sentences = [s for s in purpose.split(".") if s.strip()]
            clar += 8 if len(sentences) <= 2 and 50 <= len(purpose) <= 220 else 4
        scope = str(initiative.get("scope", "") or "")
        if scope:
            clar += 8 if ("inScope" in scope and "outOfScope" in scope) else 4
        indicators = str(initiative.get("successIndicators", "") or "")
        if indicators:
            measurable = [r"\d+%", r"\d+\s*min", r"\d+\s*days", r"<=?\d+", r">=?\d+"]
            clar += 9 if any(re.search(p, indicators) for p in measurable) else 5
        breakdown["clarity"] = clar

        # Planning (20)
        plan = 0.0
        caps_val = initiative.get("capabilityAreas", "")
        if isinstance(caps_val, list):
            areas = [
                str(a).strip() for a in cast(List[Any], caps_val) if str(a).strip()
            ]
        else:
            areas = [s.strip() for s in str(caps_val or "").split("\n") if s.strip()]
        if areas:
            plan += 7 if 2 <= len(areas) <= 6 else 4
        deliverables = str(initiative.get("deliverables", "") or "")
        if deliverables:
            spec_patterns = [
                r"\.(py|yml|md|json)",
                r"workflow",
                r"script",
                r"system",
                r"process",
            ]
            plan += (
                8
                if any(re.search(p, deliverables, re.IGNORECASE) for p in spec_patterns)
                else 4
            )
        dependencies = str(initiative.get("dependencies", "") or "")
        if dependencies:
            plan += 5
        breakdown["planning"] = plan

        # Lessons Integration (15)
        lscore = 0.0
        if lessons:
            confidence = float(lessons.get("confidence", 0) or 0)
            similar = int(lessons.get("similar_count", 0) or 0)
            if confidence >= 70 and similar >= 2:
                lscore = 15
            elif confidence >= 50 and similar >= 1:
                lscore = 10
            elif similar > 0:
                lscore = 5
        manual = str(initiative.get("lessonsFromPastInitiatives", "") or "")
        if manual and manual != "(auto-populated by analyse-initiatives workflow)":
            lscore = min(15, lscore + 3)
        breakdown["lessons_integration"] = lscore

        # Risk Awareness (10)
        risk = 0.0
        constraints = str(initiative.get("constraints", "") or "")
        if constraints:
            cnt = sum(1 for c in (s.strip() for s in constraints.split("\n")) if c)
            risk += 5 if cnt >= 3 else 3
        security_posture = str(initiative.get("securityPosture", "") or "")
        if security_posture:
            risk += 3
        test_strategy = str(initiative.get("testStrategy", "") or "")
        if test_strategy:
            risk += 2
        breakdown["risk_awareness"] = risk

        # Defensive caps then total
        caps = {
            "completeness": 30,
            "clarity": 25,
            "planning": 20,
            "lessons_integration": 15,
            "risk_awareness": 10,
        }
        for k, cap in caps.items():
            if breakdown[k] > cap:
                breakdown[k] = cap
        total = sum(breakdown.values())
        return total, breakdown

    # Derivations --------------------------------------------------------
    def _determine_readiness_level(self, score: float) -> str:
        if score >= 85:
            return "ready"
        if score >= 70:
            return "mostly-ready"
        if score >= 50:
            return "needs-work"
        return "not-ready"

    def _generate_readiness_recommendations(
        self, breakdown: Dict[str, float], level: str
    ) -> List[str]:
        recs: List[str] = []
        if breakdown["completeness"] < 25:
            recs.append(
                "Complete all required initiative fields (archetype, domain, purpose, scope, etc.)"
            )
        if breakdown["clarity"] < 20:
            recs.append(
                "Improve clarity: ensure purpose is concise, scope has in/out defined, success indicators are measurable"
            )
        if breakdown["planning"] < 15:
            recs.append(
                "Enhance planning: define 2-6 capability areas, specify concrete deliverables, identify dependencies"
            )
        if breakdown["lessons_integration"] < 10:
            recs.append("Review and integrate lessons from similar past initiatives")
        if breakdown["risk_awareness"] < 8:
            recs.append(
                "Strengthen risk awareness: define constraints, security posture, and test strategy"
            )
        if level == "not-ready":
            recs.insert(
                0,
                "Initiative needs significant work before proceeding - focus on core requirements first",
            )
        elif level == "needs-work":
            recs.insert(
                0, "Initiative has good foundation but needs refinement in key areas"
            )
        elif level == "mostly-ready":
            recs.insert(
                0,
                "Initiative is well-planned - address remaining gaps for optimal execution",
            )
        return recs[:5]

    def _determine_labels(
        self, level: str, initiative: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        mapping = {
            "ready": "readiness:ready",
            "mostly-ready": "readiness:mostly-ready",
            "needs-work": "readiness:needs-work",
            "not-ready": "readiness:not-ready",
        }
        add = [mapping[level]]
        remove = [v for k, v in mapping.items() if k != level]
        archetype = str(initiative.get("archetype", "") or "")
        if archetype:
            add.append(f"archetype:{archetype.lower()}")
        domain = str(initiative.get("domain", "") or "")
        if domain:
            add.append(f"domain:{domain}")
        add.append(
            "priority:high"
            if level == "ready"
            else "priority:medium" if level == "mostly-ready" else "priority:low"
        )
        return add, remove

    # GitHub label operations -------------------------------------------
    def _add_labels(self, owner: str, repo: str, issue: int, labels: List[str]) -> bool:
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue}/labels"
        try:
            if requests is None:
                raise RuntimeError("requests not available")
            resp = requests.post(url, headers=self.headers, json={"labels": labels})  # type: ignore
            resp.raise_for_status()
            print("✅ Added labels: " + ", ".join(labels))
            return True
        except Exception as e:  # pragma: no cover
            print(f"❌ Error adding labels: {e}")
            return False

    def _remove_labels(
        self, owner: str, repo: str, issue: int, labels: List[str]
    ) -> bool:
        ok = True
        for lbl in labels:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue}/labels/{lbl}"
            try:
                if requests is None:
                    raise RuntimeError("requests not available")
                resp = requests.delete(url, headers=self.headers)  # type: ignore
                if resp.status_code not in (200, 204, 404):
                    resp.raise_for_status()
            except Exception as e:  # pragma: no cover
                print(f"⚠️ Could not remove label '{lbl}': {e}")
                ok = False
        if ok and labels:
            print("✅ Removed labels: " + ", ".join(labels))
        return ok


def main() -> int:  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(
        description="Assess and label initiative readiness"
    )
    parser.add_argument("--repo-owner", default="SPECTRADataSolutions")
    parser.add_argument("--repo-name", default=".github")
    parser.add_argument("--issue-number", type=int)
    parser.add_argument("--initiative-file")
    parser.add_argument("--lessons-file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.initiative_file:
        with open(args.initiative_file, "r", encoding="utf-8") as fh:
            initiative = json.load(fh)
    else:
        initiative: Dict[str, Any] = {
            "archetype": "Guidance",
            "domain": "governance",
            "initiativeTitle": "testReadinessAssessment",
            "purpose": "Test the readiness assessment system for initiative planning.",
            "scope": "inScope: readiness scoring\noutOfScope: advanced ML features",
            "capabilityAreas": ["scoring", "analysis", "reporting"],
            "deliverables": "- readiness scoring algorithm\n- assessment reports",
            "successIndicators": "- 95% accuracy in readiness prediction\n- <2 minutes assessment time",
        }
    lessons = None
    if args.lessons_file:
        with open(args.lessons_file, "r", encoding="utf-8") as fh:
            lessons = json.load(fh)

    labeller = InitiativeReadinessLabeller()
    assessment = labeller.assess_readiness(initiative, lessons)
    print("\n🎯 Readiness Assessment:")
    print(
        f"Score: {assessment['readiness_score']:.1f}/100 ({assessment['readiness_level']})"
    )
    print("\nScore Breakdown:")
    for k, v in assessment["score_breakdown"].items():
        print(f"  {k}: {v:.1f}")
    print("\nRecommendations:")
    for rec in assessment["recommendations"]:
        print(f"  • {rec}")
    if args.issue_number:
        ok = labeller.apply_readiness_labels(
            args.repo_owner,
            args.repo_name,
            args.issue_number,
            assessment["labels_to_add"],
            assessment["labels_to_remove"],
            args.dry_run,
        )
        return 0 if ok else 1
    print("\nProposed Label Changes:")
    print("  Add: " + ", ".join(assessment["labels_to_add"]))
    print("  Remove: " + ", ".join(assessment["labels_to_remove"]))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
