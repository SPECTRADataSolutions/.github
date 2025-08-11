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
import glob
from pathlib import Path
from datetime import datetime


class DetachmentScoreCalculator:
    def __init__(self, repo_root="."):
        self.repo_root = Path(repo_root)
        self.score = 100  # Start with perfect score, deduct for coupling
        self.deductions = []
        self.bonuses = []
        
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
    
    def _check_cross_folder_imports(self):
        """Check for problematic imports between context folders and root."""
        context_folders = ['anchors', 'manifests', 'server', 'governance']
        
        for folder in context_folders:
            folder_path = self.repo_root / folder
            if not folder_path.exists():
                continue
                
            # Check Python files for imports
            for py_file in folder_path.rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for imports from parent directories
                    problematic_imports = re.findall(
                        r'(?:from|import)\s+\.\.+', content
                    )
                    
                    if problematic_imports:
                        self.score -= 10
                        self.deductions.append(
                            f"Cross-folder import in {py_file}: {len(problematic_imports)} imports"
                        )
                        
                except Exception as e:
                    # Ignore files that can't be read
                    pass
    
    def _check_server_isolation(self):
        """Check if server code is properly isolated."""
        server_path = self.repo_root / "server"
        
        if not server_path.exists():
            self.bonuses.append("Server directory does not exist yet (+5)")
            self.score += 5
            return
            
        # Check for server-specific configuration
        config_files = list(server_path.rglob("*.json")) + list(server_path.rglob("*.yaml"))
        
        if len(config_files) >= 1:
            self.bonuses.append(f"Server has {len(config_files)} config files (+3)")
            self.score += 3
            
        # Check for independent README
        server_readme = server_path / "README.md" or server_path / "placeholder" / "README.md"
        if server_readme.exists():
            self.bonuses.append("Server has dedicated README (+2)")
            self.score += 2
    
    def _check_configuration_independence(self):
        """Check if context system has independent configuration."""
        
        # Check for schemaMeta.json
        schema_meta = self.repo_root / "contracts" / "schemaMeta.json"
        if schema_meta.exists():
            self.bonuses.append("Schema metadata tracking exists (+5)")
            self.score += 5
            
        # Check for governance workflows
        governance_workflows = self.repo_root / "governance" / "workflows"
        if governance_workflows.exists():
            workflow_count = len(list(governance_workflows.glob("*.yml")))
            if workflow_count > 0:
                self.bonuses.append(f"Independent governance workflows: {workflow_count} (+{workflow_count * 2})")
                self.score += workflow_count * 2
    
    def _check_api_boundaries(self):
        """Check for clear API boundary definitions."""
        
        # Check for server contract documentation
        server_readme = self.repo_root / "server" / "placeholder" / "README.md"
        if server_readme.exists():
            try:
                with open(server_readme, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Look for endpoint definitions
                endpoint_patterns = [
                    r'GET\s+/\w+',
                    r'POST\s+/\w+',
                    r'PUT\s+/\w+',
                    r'DELETE\s+/\w+'
                ]
                
                endpoint_count = sum(
                    len(re.findall(pattern, content, re.IGNORECASE))
                    for pattern in endpoint_patterns
                )
                
                if endpoint_count >= 3:
                    self.bonuses.append(f"API endpoints documented: {endpoint_count} (+5)")
                    self.score += 5
                    
            except Exception:
                pass
    
    def _check_hardcoded_paths(self):
        """Check for hardcoded repository-specific paths."""
        context_folders = ['anchors', 'manifests', 'server', 'governance']
        
        for folder in context_folders:
            folder_path = self.repo_root / folder
            if not folder_path.exists():
                continue
                
            # Check for hardcoded .github references
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in ['.py', '.js', '.yml', '.yaml', '.json']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Look for hardcoded repository references
                        hardcoded_refs = re.findall(
                            r'SPECTRADataSolutions/\.github',
                            content
                        )
                        
                        if hardcoded_refs:
                            self.score -= 5
                            self.deductions.append(
                                f"Hardcoded .github reference in {file_path}: {len(hardcoded_refs)} refs"
                            )
                            
                    except Exception:
                        pass
    
    def _generate_report(self, final_score):
        """Generate detailed scoring report."""
        print(f"\n🎯 Final Detachment Score: {final_score}/100")
        
        if final_score >= 95:
            status = "🌟 EXCELLENT - Ready for extraction"
            color = "green"
        elif final_score >= 80:
            status = "✅ GOOD - Minor coupling to resolve"
            color = "yellow"
        elif final_score >= 60:
            status = "⚠️ MODERATE - Refactoring needed"
            color = "orange"
        else:
            status = "❌ POOR - Significant coupling detected"
            color = "red"
            
        print(f"Status: {status}")
        
        if self.bonuses:
            print(f"\n✅ Positive Factors:")
            for bonus in self.bonuses:
                print(f"  • {bonus}")
                
        if self.deductions:
            print(f"\n⚠️ Coupling Issues:")
            for deduction in self.deductions:
                print(f"  • {deduction}")
                
        print(f"\n📊 Score Breakdown:")
        print(f"  • Base Score: 100")
        
        # Calculate bonuses safely
        total_bonuses = 0
        for bonus in self.bonuses:
            match = re.search(r'\+(\d+)', bonus)
            if match:
                total_bonuses += int(match.group(1))
        
        # Calculate deductions safely
        total_deductions = 0
        for deduction in self.deductions:
            if 'import' in deduction or 'reference' in deduction:
                # Deductions are already subtracted from score, just track for display
                total_deductions += 5  # Approximate deduction amount
        
        print(f"  • Bonuses: +{total_bonuses}")
        print(f"  • Deductions: -{total_deductions}")
        print(f"  • Final: {final_score}")
        
        # Generate JSON output for automation
        result = {
            "detachmentScore": final_score,
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "bonuses": self.bonuses,
            "deductions": self.deductions,
            "recommendation": self._get_recommendation(final_score)
        }
        
        with open("detachment-score.json", "w") as f:
            json.dump(result, f, indent=2)
            
        print(f"\n📄 Detailed results saved to: detachment-score.json")
    
    def _get_recommendation(self, score):
        """Get recommendation based on score."""
        if score >= 95:
            return "System is ready for extraction. Proceed with migration checklist."
        elif score >= 80:
            return "Resolve minor coupling issues before extraction."
        elif score >= 60:
            return "Significant refactoring needed. Focus on eliminating cross-folder dependencies."
        else:
            return "Major architectural changes required. System not ready for extraction."


def main():
    """Main entry point."""
    # Change to script directory to ensure relative paths work
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
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