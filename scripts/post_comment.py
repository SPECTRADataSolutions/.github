#!/usr/bin/env python3
"""
SPECTRA Initiative Comment Poster

This script posts lessons and mitigation tasks as comments on new initiative 
issues, providing automated guidance based on similar past initiatives.

Framework as Law: This script enforces lessons communication standards.
"""

import os
import json
import requests
from datetime import datetime, timezone
from typing import Dict, Optional


class InitiativeCommentPoster:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Initiative-Comment-Poster",
            "Content-Type": "application/json"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def post_lessons_comment(self, repo_owner: str, repo_name: str, issue_number: int, 
                           lessons_data: Dict, dry_run: bool = False) -> bool:
        """Post lessons as a comment on the initiative issue."""
        
        if not self.github_token and not dry_run:
            print("❌ No GitHub token available. Use --dry-run to test formatting.")
            return False
        
        # Format the comment
        comment_body = self._format_lessons_comment(lessons_data)
        
        if dry_run:
            print("🔍 DRY RUN - Comment that would be posted:")
            print("=" * 60)
            print(comment_body)
            print("=" * 60)
            return True
        
        # Post the comment
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
        payload = {"body": comment_body}
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            comment_data = response.json()
            comment_url = comment_data.get('html_url', '')
            
            print(f"✅ Posted lessons comment: {comment_url}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error posting comment: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False
    
    def _format_lessons_comment(self, lessons_data: Dict) -> str:
        """Format lessons data into a structured comment."""
        
        # Header
        comment = "## 🎓 Lessons from Past Initiatives\n\n"
        comment += "_Auto-generated insights based on similar initiatives in SPECTRA history_\n\n"
        
        # Add metadata
        confidence = lessons_data.get("confidence", 0)
        similar_count = lessons_data.get("similar_count", 0)
        
        comment += f"**Analysis Confidence:** {confidence:.1f}% (based on {similar_count} similar initiatives)\n\n"
        
        # Handle errors
        if "error" in lessons_data:
            comment += f"⚠️ **Analysis Status:** {lessons_data['error']}\n\n"
            comment += "This initiative will help build the lessons database for future analysis.\n"
            return comment
        
        lessons = lessons_data.get("lessons", {})
        
        # No lessons case
        if not lessons or lessons.get("message"):
            comment += "🆕 **First of its kind:** No directly similar initiatives found in history.\n\n"
            comment += "This is an opportunity to establish new patterns and best practices.\n\n"
            comment += "### 📋 Recommended Actions\n"
            comment += "- [ ] Document key decisions and rationale\n"
            comment += "- [ ] Track challenges and solutions for future reference\n"
            comment += "- [ ] Conduct thorough postmortem upon completion\n"
            return comment
        
        # Similar initiatives section
        similar_initiatives = lessons_data.get("similar_initiatives", [])
        if similar_initiatives:
            comment += "### 🔍 Similar Initiatives Analysed\n\n"
            for idx, similar in enumerate(similar_initiatives[:3], 1):
                similarity_pct = similar.get("similarity", 0) * 100
                comment += f"{idx}. **{similar.get('title', 'Unknown')}** "
                comment += f"({similar.get('archetype', 'Unknown')} → {similar.get('domain', 'unknown')}) "
                comment += f"- {similarity_pct:.0f}% similarity\n"
            comment += "\n"
        
        # Risks section
        risks = lessons.get("risks", [])
        if risks:
            comment += "### ⚠️ Identified Risks\n\n"
            comment += "Based on challenges faced by similar initiatives:\n\n"
            for idx, risk in enumerate(risks, 1):
                comment += f"{idx}. **{risk}**\n"
            comment += "\n"
        
        # Mitigations section
        mitigations = lessons.get("mitigations", [])
        if mitigations:
            comment += "### 🛡️ Proven Mitigations\n\n"
            comment += "Strategies that worked for similar initiatives:\n\n"
            for idx, mitigation in enumerate(mitigations, 1):
                comment += f"- [ ] {mitigation}\n"
            comment += "\n"
        
        # Success factors section
        success_factors = lessons.get("success_factors", [])
        if success_factors:
            comment += "### ✅ Success Factors\n\n"
            comment += "Patterns observed in successful similar initiatives:\n\n"
            for factor in success_factors:
                comment += f"- {factor}\n"
            comment += "\n"
        
        # Recommendations section
        recommendations = lessons.get("recommendations", [])
        summary_recommendations = lessons.get("summary", [])
        all_recommendations = recommendations + summary_recommendations
        
        if all_recommendations:
            comment += "### 💡 Recommendations\n\n"
            for rec in all_recommendations:
                comment += f"- {rec}\n"
            comment += "\n"
        
        # Action items section
        comment += "### 📋 Suggested Action Items\n\n"
        comment += "Consider adding these tasks to your initiative planning:\n\n"
        
        # Generate action items based on lessons
        action_items = self._generate_action_items(lessons)
        for action in action_items:
            comment += f"- [ ] {action}\n"
        
        # Footer
        comment += "\n---\n\n"
        comment += "_This analysis was generated by the SPECTRA lessons automation system. "
        comment += f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC._\n\n"
        comment += "💬 **Feedback:** If any suggestions seem irrelevant, please comment to help improve the system."
        
        return comment
    
    def _generate_action_items(self, lessons: Dict) -> list:
        """Generate actionable items based on lessons."""
        action_items = []
        
        # Risk-based actions
        risks = lessons.get("risks", [])
        if risks:
            action_items.append("Create risk assessment document covering identified risks")
            action_items.append("Schedule risk review checkpoint with stakeholders")
        
        # Mitigation-based actions
        mitigations = lessons.get("mitigations", [])
        if mitigations:
            action_items.append("Implement proven mitigation strategies from similar initiatives")
            action_items.append("Document mitigation plan for future reference")
        
        # Success factor actions
        success_factors = lessons.get("success_factors", [])
        if success_factors:
            action_items.append("Review success patterns and align initiative plan accordingly")
        
        # Default actions if no specific lessons
        if not any([risks, mitigations, success_factors]):
            action_items.extend([
                "Document initiative decisions for future lessons database",
                "Plan regular checkpoints to capture learnings",
                "Prepare for comprehensive postmortem documentation"
            ])
        
        return action_items[:5]  # Limit to avoid overwhelming
    
    def update_issue_body(self, repo_owner: str, repo_name: str, issue_number: int, 
                         current_body: str, lessons_summary: str, dry_run: bool = False) -> bool:
        """Update the issue body with lessons summary (optional feature)."""
        
        if not self.github_token and not dry_run:
            print("❌ No GitHub token available for issue body updates.")
            return False
        
        # Find the lessonsFromPastInitiatives section
        pattern = r'(### lessonsFromPastInitiatives\s*\n\s*)(.*?)(\n\s*###|\n\s*$)'
        
        # Check if section exists
        import re
        match = re.search(pattern, current_body, re.DOTALL)
        
        if not match:
            print("⚠️ lessonsFromPastInitiatives section not found in issue body")
            return False
        
        # Replace the content
        new_content = f"{match.group(1)}{lessons_summary}\n\n{match.group(3)}"
        updated_body = re.sub(pattern, new_content, current_body, flags=re.DOTALL)
        
        if dry_run:
            print("🔍 DRY RUN - Issue body update:")
            print("=" * 60)
            print("Updated lessonsFromPastInitiatives section:")
            print(lessons_summary)
            print("=" * 60)
            return True
        
        # Update the issue
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
        payload = {"body": updated_body}
        
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            print("✅ Updated issue body with lessons summary")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error updating issue body: {e}")
            return False


def main():
    """Main entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Post initiative lessons as comments")
    parser.add_argument("--repo-owner", default="SPECTRADataSolutions", help="Repository owner")
    parser.add_argument("--repo-name", default=".github", help="Repository name")
    parser.add_argument("--issue-number", type=int, help="Issue number to comment on")
    parser.add_argument("--lessons-file", help="JSON file containing lessons data")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted without posting")
    
    args = parser.parse_args()
    
    # Load lessons data
    if args.lessons_file:
        with open(args.lessons_file, 'r') as f:
            lessons_data = json.load(f)
    else:
        # Use sample data for testing
        lessons_data = {
            "confidence": 75.5,
            "similar_count": 3,
            "lessons": {
                "risks": ["Timeline constraints due to complexity", "Resource allocation challenges"],
                "mitigations": ["Early stakeholder alignment", "Incremental delivery approach"],
                "recommendations": ["Focus on MVP first", "Regular progress reviews"]
            },
            "similar_initiatives": [
                {"title": "Sample Initiative 1", "archetype": "Guidance", "domain": "governance", "similarity": 0.85}
            ]
        }
    
    poster = InitiativeCommentPoster()
    
    if args.issue_number:
        success = poster.post_lessons_comment(
            args.repo_owner, args.repo_name, args.issue_number, 
            lessons_data, args.dry_run
        )
        return 0 if success else 1
    else:
        # Just show the formatted comment
        comment = poster._format_lessons_comment(lessons_data)
        print("📝 Formatted lessons comment:")
        print("=" * 60)
        print(comment)
        return 0


if __name__ == "__main__":
    exit(main())