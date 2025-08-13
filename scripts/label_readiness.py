#!/usr/bin/env python3
"""
SPECTRA Initiative Readiness Labeller

This script analyses initiative completeness and applies readiness labels
based on available information, lessons analysis, and planning quality.

Framework as Law: This script enforces readiness assessment standards.
"""

import os
import re
import json
import requests
from typing import Dict, List, Optional, Tuple


class InitiativeReadinessLabeller:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Initiative-Readiness-Labeller"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def assess_readiness(self, initiative_data: Dict[str, str], lessons_data: Optional[Dict] = None) -> Dict:
        """Assess initiative readiness and determine appropriate labels."""
        
        print(f"🔍 Assessing readiness for: {initiative_data.get('initiativeTitle', 'Unknown')}")
        
        # Calculate readiness score
        readiness_score, score_details = self._calculate_readiness_score(initiative_data, lessons_data)
        
        # Determine readiness level
        readiness_level = self._determine_readiness_level(readiness_score)
        
        # Generate recommendations
        recommendations = self._generate_readiness_recommendations(score_details, readiness_level)
        
        # Determine labels to apply
        labels_to_add, labels_to_remove = self._determine_labels(readiness_level, initiative_data)
        
        return {
            "readiness_score": readiness_score,
            "readiness_level": readiness_level,
            "score_breakdown": score_details,
            "recommendations": recommendations,
            "labels_to_add": labels_to_add,
            "labels_to_remove": labels_to_remove
        }
    
    def apply_readiness_labels(self, repo_owner: str, repo_name: str, issue_number: int, 
                             labels_to_add: List[str], labels_to_remove: List[str], 
                             dry_run: bool = False) -> bool:
        """Apply readiness labels to the initiative issue."""
        
        if not self.github_token and not dry_run:
            print("❌ No GitHub token available for label updates.")
            return False
        
        if dry_run:
            print("🔍 DRY RUN - Label changes:")
            if labels_to_add:
                print(f"  Add: {', '.join(labels_to_add)}")
            if labels_to_remove:
                print(f"  Remove: {', '.join(labels_to_remove)}")
            return True
        
        success = True
        
        # Add new labels
        if labels_to_add:
            success &= self._add_labels(repo_owner, repo_name, issue_number, labels_to_add)
        
        # Remove old labels
        if labels_to_remove:
            success &= self._remove_labels(repo_owner, repo_name, issue_number, labels_to_remove)
        
        return success
    
    def _calculate_readiness_score(self, initiative_data: Dict[str, str], 
                                 lessons_data: Optional[Dict] = None) -> Tuple[float, Dict]:
        """Calculate overall readiness score (0-100)."""
        
        score_details = {
            "completeness": 0,
            "clarity": 0,
            "planning": 0,
            "lessons_integration": 0,
            "risk_awareness": 0
        }
        
        # 1. Completeness Score (30 points)
        required_fields = [
            'archetype', 'domain', 'initiativeTitle', 'purpose', 'scope',
            'capabilityAreas', 'deliverables', 'successIndicators'
        ]
        
        completed_fields = sum(1 for field in required_fields if initiative_data.get(field, '').strip())
        completeness_score = (completed_fields / len(required_fields)) * 30
        score_details["completeness"] = completeness_score
        
        # 2. Clarity Score (25 points)
        clarity_score = 0
        
        # Purpose clarity (clear, single sentence)
        purpose = initiative_data.get('purpose', '')
        if purpose:
            if len(purpose.split('.')) <= 2 and 50 <= len(purpose) <= 200:
                clarity_score += 8
            elif purpose:
                clarity_score += 4
        
        # Scope clarity (in/out of scope defined)
        scope = initiative_data.get('scope', '')
        if 'inScope' in scope and 'outOfScope' in scope:
            clarity_score += 8
        elif scope:
            clarity_score += 4
        
        # Success indicators clarity (measurable)
        success_indicators = initiative_data.get('successIndicators', '')
        if success_indicators:
            # Look for measurable indicators (numbers, percentages, time)
            measurable_patterns = [r'\d+%', r'\d+\s*min', r'\d+\s*days', r'<=?\d+', r'>=?\d+']
            if any(re.search(pattern, success_indicators) for pattern in measurable_patterns):
                clarity_score += 9
            else:
                clarity_score += 5
        
        score_details["clarity"] = clarity_score
        
        # 3. Planning Score (20 points)
        planning_score = 0
        
        # Capability areas defined
        capability_areas = initiative_data.get('capabilityAreas', '')
        if capability_areas:
            areas_count = len([area.strip() for area in capability_areas.split('\n') if area.strip()])
            if 2 <= areas_count <= 6:  # Sweet spot for manageable scope
                planning_score += 7
            elif areas_count > 0:
                planning_score += 4
        
        # Deliverables specificity
        deliverables = initiative_data.get('deliverables', '')
        if deliverables:
            # Look for specific deliverable patterns (files, systems, processes)
            specific_patterns = [r'\.(py|yml|md|json)', r'workflow', r'script', r'system', r'process']
            if any(re.search(pattern, deliverables, re.IGNORECASE) for pattern in specific_patterns):
                planning_score += 8
            else:
                planning_score += 4
        
        # Dependencies identified
        dependencies = initiative_data.get('dependencies', '')
        if dependencies:
            planning_score += 5
        
        score_details["planning"] = planning_score
        
        # 4. Lessons Integration Score (15 points)
        lessons_score = 0
        
        if lessons_data:
            confidence = lessons_data.get('confidence', 0)
            similar_count = lessons_data.get('similar_count', 0)
            
            # High confidence lessons available
            if confidence >= 70 and similar_count >= 2:
                lessons_score += 15
            elif confidence >= 50 and similar_count >= 1:
                lessons_score += 10
            elif similar_count > 0:
                lessons_score += 5
        
        # Check if lessons are already integrated in planning
        lessons_from_past = initiative_data.get('lessonsFromPastInitiatives', '')
        if lessons_from_past and lessons_from_past != "(auto-populated by analyse-initiatives workflow)":
            lessons_score += 5  # Bonus for manual integration
        
        score_details["lessons_integration"] = lessons_score
        
        # 5. Risk Awareness Score (10 points)
        risk_score = 0
        
        # Constraints identified (indicates risk awareness)
        constraints = initiative_data.get('constraints', '')
        if constraints:
            constraint_count = len([c.strip() for c in constraints.split('\n') if c.strip()])
            if constraint_count >= 3:
                risk_score += 5
            else:
                risk_score += 3
        
        # Security posture defined
        security_posture = initiative_data.get('securityPosture', '')
        if security_posture:
            risk_score += 3
        
        # Test strategy defined
        test_strategy = initiative_data.get('testStrategy', '')
        if test_strategy:
            risk_score += 2
        
        score_details["risk_awareness"] = risk_score
        
        # Calculate total score
        total_score = sum(score_details.values())
        
        return total_score, score_details
    
    def _determine_readiness_level(self, score: float) -> str:
        """Determine readiness level based on score."""
        if score >= 85:
            return "ready"
        elif score >= 70:
            return "mostly-ready"
        elif score >= 50:
            return "needs-work"
        else:
            return "not-ready"
    
    def _generate_readiness_recommendations(self, score_details: Dict, readiness_level: str) -> List[str]:
        """Generate specific recommendations based on score breakdown."""
        recommendations = []
        
        # Completeness recommendations
        if score_details["completeness"] < 25:
            recommendations.append("Complete all required initiative fields (archetype, domain, purpose, scope, etc.)")
        
        # Clarity recommendations
        if score_details["clarity"] < 20:
            recommendations.append("Improve clarity: ensure purpose is concise, scope has in/out defined, success indicators are measurable")
        
        # Planning recommendations
        if score_details["planning"] < 15:
            recommendations.append("Enhance planning: define 2-6 capability areas, specify concrete deliverables, identify dependencies")
        
        # Lessons recommendations
        if score_details["lessons_integration"] < 10:
            recommendations.append("Review and integrate lessons from similar past initiatives")
        
        # Risk recommendations
        if score_details["risk_awareness"] < 8:
            recommendations.append("Strengthen risk awareness: define constraints, security posture, and test strategy")
        
        # Level-specific recommendations
        if readiness_level == "not-ready":
            recommendations.insert(0, "Initiative needs significant work before proceeding - focus on core requirements first")
        elif readiness_level == "needs-work":
            recommendations.insert(0, "Initiative has good foundation but needs refinement in key areas")
        elif readiness_level == "mostly-ready":
            recommendations.insert(0, "Initiative is well-planned - address remaining gaps for optimal execution")
        
        return recommendations[:5]  # Limit to most important
    
    def _determine_labels(self, readiness_level: str, initiative_data: Dict[str, str]) -> Tuple[List[str], List[str]]:
        """Determine which labels to add and remove."""
        
        # Readiness labels
        readiness_labels = {
            "ready": "readiness:ready",
            "mostly-ready": "readiness:mostly-ready",
            "needs-work": "readiness:needs-work", 
            "not-ready": "readiness:not-ready"
        }
        
        labels_to_add = [readiness_labels[readiness_level]]
        labels_to_remove = [label for level, label in readiness_labels.items() if level != readiness_level]
        
        # Add archetype and domain labels
        archetype = initiative_data.get('archetype', '')
        if archetype:
            labels_to_add.append(f"archetype:{archetype.lower()}")
        
        domain = initiative_data.get('domain', '')
        if domain:
            labels_to_add.append(f"domain:{domain}")
        
        # Add priority labels based on readiness and type
        if readiness_level == "ready":
            labels_to_add.append("priority:high")
        elif readiness_level == "mostly-ready":
            labels_to_add.append("priority:medium")
        else:
            labels_to_add.append("priority:low")
        
        return labels_to_add, labels_to_remove
    
    def _add_labels(self, repo_owner: str, repo_name: str, issue_number: int, labels: List[str]) -> bool:
        """Add labels to an issue."""
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        
        try:
            response = requests.post(url, headers=self.headers, json={"labels": labels})
            response.raise_for_status()
            print(f"✅ Added labels: {', '.join(labels)}")
            return True
        except requests.RequestException as e:
            print(f"❌ Error adding labels: {e}")
            return False
    
    def _remove_labels(self, repo_owner: str, repo_name: str, issue_number: int, labels: List[str]) -> bool:
        """Remove labels from an issue."""
        success = True
        
        for label in labels:
            url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels/{label}"
            try:
                response = requests.delete(url, headers=self.headers)
                # 404 is OK - label might not exist
                if response.status_code not in [200, 204, 404]:
                    response.raise_for_status()
            except requests.RequestException as e:
                print(f"⚠️ Could not remove label '{label}': {e}")
                success = False
        
        if success and labels:
            print(f"✅ Removed labels: {', '.join(labels)}")
        
        return success


def main():
    """Main entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Assess and label initiative readiness")
    parser.add_argument("--repo-owner", default="SPECTRADataSolutions", help="Repository owner")
    parser.add_argument("--repo-name", default=".github", help="Repository name")
    parser.add_argument("--issue-number", type=int, help="Issue number to label")
    parser.add_argument("--initiative-file", help="JSON file containing initiative data")
    parser.add_argument("--lessons-file", help="JSON file containing lessons data")
    parser.add_argument("--dry-run", action="store_true", help="Show assessment without applying labels")
    
    args = parser.parse_args()
    
    # Load initiative data
    if args.initiative_file:
        with open(args.initiative_file, 'r') as f:
            initiative_data = json.load(f)
    else:
        # Use sample data for testing
        initiative_data = {
            "archetype": "Guidance",
            "domain": "governance",
            "initiativeTitle": "testReadinessAssessment",
            "purpose": "Test the readiness assessment system for initiative planning.",
            "scope": "inScope: readiness scoring\noutOfScope: advanced ML features",
            "capabilityAreas": "scoring\nanalysis\nreporting",
            "deliverables": "- readiness scoring algorithm\n- assessment reports",
            "successIndicators": "- 95% accuracy in readiness prediction\n- <2 minutes assessment time"
        }
    
    # Load lessons data if available
    lessons_data = None
    if args.lessons_file:
        with open(args.lessons_file, 'r') as f:
            lessons_data = json.load(f)
    
    labeller = InitiativeReadinessLabeller()
    assessment = labeller.assess_readiness(initiative_data, lessons_data)
    
    print("\n🎯 Readiness Assessment:")
    print(f"Score: {assessment['readiness_score']:.1f}/100 ({assessment['readiness_level']})")
    print("\nScore Breakdown:")
    for category, score in assessment['score_breakdown'].items():
        print(f"  {category}: {score:.1f}")
    
    print("\nRecommendations:")
    for rec in assessment['recommendations']:
        print(f"  • {rec}")
    
    if args.issue_number:
        success = labeller.apply_readiness_labels(
            args.repo_owner, args.repo_name, args.issue_number,
            assessment['labels_to_add'], assessment['labels_to_remove'],
            args.dry_run
        )
        return 0 if success else 1
    else:
        print("\nProposed Label Changes:")
        print(f"  Add: {', '.join(assessment['labels_to_add'])}")
        print(f"  Remove: {', '.join(assessment['labels_to_remove'])}")
        return 0


if __name__ == "__main__":
    exit(main())