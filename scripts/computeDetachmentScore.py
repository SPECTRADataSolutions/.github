#!/usr/bin/env python3
"""
SPECTRA Context System Detachment Score Calculator

This script computes a detachment score (0-100) indicating how ready the context system
is for extraction into an independent repository. Higher scores indicate better readiness.

Scoring Factors:
- Cross-folder imports (decreases score)
- Server isolation (increases score)
- Configuration independence (increases score)
- API boundary clarity (increases score)
- Test coverage isolation (increases score)

Framework as Law: This script enforces architectural boundaries for future extraction.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple


class DetachmentScoreCalculator:
    def __init__(self, repo_root: str | os.PathLike[str] = "."):
        # Normalise to absolute path to avoid relative traversal issues
        self.repo_root = Path(repo_root).resolve()
        self.score: int = 100  # Start with perfect score, deduct for coupling
        # Keep (description, delta) pairs. Positive delta = bonus, negative = deduction.
        self._factors: List[Tuple[str, int]] = []

    def calculate_score(self):
        """Calculate the detachment score with detailed breakdown."""
        print("🔍 SPECTRA Context System Detachment Score Analysis")
        print("=" * 60)

        # Check for cross-folder imports
        self._check_cross_folder_imports()

        # Check server isolation
        self._check_server_isolation()

        # Check configuration independence
        self._check_configuration_independence()

        # Check API boundary clarity
        self._check_api_boundaries()

        # Check for hardcoded paths
        self._check_hardcoded_paths()

        # Calculate final score
        final_score = max(0, min(100, self.score))

        # Generate report
        self._generate_report(final_score)

        return final_score

    def _check_cross_folder_imports(self) -> None:
        """Check for problematic relative ("..") imports indicating upward coupling.

        Deduct 5 points per file containing at least one such import (capped).
        """
        context_folders = ["anchors", "manifests", "server", "governance"]
        for folder in context_folders:
            folder_path = self.repo_root / folder
            if not folder_path.is_dir():
                continue
            for py_file in folder_path.rglob("*.py"):
                try:
                    text = py_file.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                # Relative parent import pattern
                if re.search(r"^(?:from|import)\s+\.\.+", text, flags=re.MULTILINE):
                    delta = -5
                    self.score += delta
                    self._factors.append(
                        (f"Upward relative import in {py_file}", delta)
                    )

    def _check_server_isolation(self) -> None:
        """Check if server code is properly isolated (bonus points for separation)."""
        server_path = self.repo_root / "server"
        if not server_path.exists():
            delta = +5
            self.score += delta
            self._factors.append(("Server directory absent (can extract later)", delta))
            return
        # Config presence
        config_files = list(server_path.rglob("*.json")) + list(
            server_path.rglob("*.yaml")
        )
        if config_files:
            delta = +3
            self.score += delta
            self._factors.append((f"Server config files: {len(config_files)}", delta))
        # README in either server/ or server/placeholder/
        readme_candidates = [
            server_path / "README.md",
            server_path / "placeholder" / "README.md",
        ]
        if any(p.is_file() for p in readme_candidates):
            delta = +2
            self.score += delta
            self._factors.append(("Server has dedicated README", delta))

    def _check_configuration_independence(self) -> None:
        """Check if context system has independent configuration (bonuses)."""
        schema_meta = self.repo_root / "contracts" / "schemaMeta.json"
        if schema_meta.is_file():
            delta = +5
            self.score += delta
            self._factors.append(("Schema metadata tracking exists", delta))
        governance_workflows = self.repo_root / "governance" / "workflows"
        if governance_workflows.is_dir():
            workflow_count = len(list(governance_workflows.glob("*.yml")))
            if workflow_count:
                delta = workflow_count * 2
                self.score += delta
                self._factors.append(
                    (f"Independent governance workflows: {workflow_count}", delta)
                )

    def _check_api_boundaries(self) -> None:
        """Check for clear API boundary definitions (documented endpoints)."""
        readme_candidates = [
            self.repo_root / "server" / "README.md",
            self.repo_root / "server" / "placeholder" / "README.md",
        ]
        for candidate in readme_candidates:
            if not candidate.is_file():
                continue
            try:
                content = candidate.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            endpoint_patterns = [
                r"GET\s+/\w+",
                r"POST\s+/\w+",
                r"PUT\s+/\w+",
                r"DELETE\s+/\w+",
            ]
            endpoint_count = sum(
                len(re.findall(p, content, re.IGNORECASE)) for p in endpoint_patterns
            )
            if endpoint_count >= 3:
                delta = +5
                self.score += delta
                self._factors.append(
                    (f"API endpoints documented: {endpoint_count}", delta)
                )
                break

    def _check_hardcoded_paths(self) -> None:
        """Check for hardcoded repository-specific paths (deductions)."""
        context_folders = ["anchors", "manifests", "server", "governance"]
        pattern = re.compile(r"SPECTRADataSolutions/\\.github")
        for folder in context_folders:
            folder_path = self.repo_root / folder
            if not folder_path.is_dir():
                continue
            for file_path in folder_path.rglob("*"):
                if not (
                    file_path.is_file()
                    and file_path.suffix in {".py", ".js", ".yml", ".yaml", ".json"}
                ):
                    continue
                try:
                    text = file_path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if pattern.search(text):
                    delta = -5
                    self.score += delta
                    self._factors.append(
                        (f"Hardcoded .github reference in {file_path}", delta)
                    )

    def _generate_report(self, final_score: int) -> None:
        """Generate detailed scoring report and machine-readable JSON."""
        print(f"\n🎯 Final Detachment Score: {final_score}/100")
        if final_score >= 95:
            status = "🌟 EXCELLENT - Ready for extraction"
        elif final_score >= 80:
            status = "✅ GOOD - Minor coupling to resolve"
        elif final_score >= 60:
            status = "⚠️ MODERATE - Refactoring needed"
        else:
            status = "❌ POOR - Significant coupling detected"
        print(f"Status: {status}")

        positives = [d for d, delta in self._factors if delta > 0]
        negatives = [d for d, delta in self._factors if delta < 0]
        if positives:
            print("\n✅ Positive Factors:")
            for desc in positives:
                print(f"  • {desc}")
        if negatives:
            print("\n⚠️ Coupling Issues:")
            for desc in negatives:
                print(f"  • {desc}")

        total_bonuses = sum(delta for _, delta in self._factors if delta > 0)
        total_deductions = -sum(delta for _, delta in self._factors if delta < 0)
        print("\n📊 Score Breakdown:")
        print("  • Base Score: 100")
        print(f"  • Bonuses: +{total_bonuses}")
        print(f"  • Deductions: -{total_deductions}")
        print(f"  • Final: {final_score}")

        result: dict[str, object] = {
            "detachmentScore": final_score,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "factors": [
                {"description": d, "delta": delta} for d, delta in self._factors
            ],
            "recommendation": self._get_recommendation(final_score),
        }
        with open("detachment-score.json", "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print("\n📄 Detailed results saved to: detachment-score.json")

    def _get_recommendation(self, score: int) -> str:
        """Recommendation based on score bucket."""
        if score >= 95:
            return "System is ready for extraction. Proceed with migration checklist."
        if score >= 80:
            return "Resolve minor coupling issues before extraction."
        if score >= 60:
            return "Significant refactoring needed. Focus on eliminating cross-folder dependencies."
        return "Major architectural changes required. System not ready for extraction."


def main():
    """Main entry point."""
    # Change to script directory to ensure relative paths work
    script_dir = Path(__file__).resolve().parent
    # The script resides in .github/scripts; repo root is two levels up.
    repo_root = script_dir.parent.parent

    calculator = DetachmentScoreCalculator(repo_root)
    score = calculator.calculate_score()

    # Exit with status code based on score for CI/CD integration
    if score >= 95:
        exit_code = 0  # Ready for extraction
    elif score >= 80:
        exit_code = 1  # Minor issues
    else:
        exit_code = 2  # Major issues

    return exit_code


if __name__ == "__main__":
    exit(main())
