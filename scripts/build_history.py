#!/usr/bin/env python3
"""
SPECTRA Initiative History Builder

This script builds a history index from past initiative issues to power 
lessons automation. It extracts key data including status, postmortem, 
root causes, and mitigations for similarity matching.

Framework as Law: This script enforces historical data extraction standards.
"""

import os
import re
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


class InitiativeHistoryBuilder:
    def __init__(self, github_token: Optional[str] = None, repo_owner: str = "SPECTRADataSolutions", repo_name: str = ".github"):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Initiative-History-Builder"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def build_history(self, output_path: str = "analytics/initiatives-history.jsonl"):
        """Build history index from initiative issues."""
        print("🔍 SPECTRA Initiative History Builder")
        print("=" * 50)
        
        # Fetch initiative issues
        initiatives = self._fetch_initiative_issues()
        print(f"📊 Found {len(initiatives)} initiative issues")
        
        # Process each initiative
        history_entries = []
        for issue in initiatives:
            entry = self._process_initiative(issue)
            if entry:
                history_entries.append(entry)
        
        # Save to JSONL file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in history_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"✅ Built history index: {len(history_entries)} entries saved to {output_path}")
        return history_entries
    
    def _fetch_initiative_issues(self) -> List[Dict]:
        """Fetch all initiative issues from the repository."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {
            "labels": "type:initiative",
            "state": "all",  # Get both open and closed
            "per_page": 100,
            "sort": "updated",
            "direction": "desc"
        }
        
        issues = []
        page = 1
        
        while True:
            params["page"] = page
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                page_issues = response.json()
                
                if not page_issues:
                    break
                
                # Filter for initiatives
                initiative_issues = [
                    issue for issue in page_issues 
                    if any(label['name'] == 'type:initiative' for label in issue.get('labels', []))
                ]
                
                issues.extend(initiative_issues)
                page += 1
                
                # GitHub API pagination limit safety
                if page > 10:  # Reasonable limit for .github repo
                    break
                    
            except requests.RequestException as e:
                print(f"⚠️ Error fetching issues (page {page}): {e}")
                break
        
        return issues
    
    def _process_initiative(self, issue: Dict) -> Optional[Dict]:
        """Process a single initiative issue into history entry."""
        try:
            # Extract basic info
            title = issue.get('title', '')
            body = issue.get('body', '')
            state = issue.get('state', 'open')
            
            # Parse initiative ID from title or generate one
            initiative_id = self._extract_initiative_id(title, issue.get('number'))
            
            # Parse structured fields from issue body
            fields = self._parse_issue_body(body)
            
            # Extract lessons and insights
            lessons = self._extract_lessons(fields, state)
            
            # Generate similarity keywords
            keywords = self._generate_keywords(fields, title)
            
            entry = {
                "initiativeId": initiative_id,
                "issueNumber": issue.get('number'),
                "title": title,
                "archetype": fields.get('archetype', 'Unknown'),
                "domain": fields.get('domain', 'unknown'),
                "status": self._map_status(state, fields.get('outcomeStatus')),
                "createdAt": issue.get('created_at'),
                "updatedAt": issue.get('updated_at'),
                "lessons": lessons,
                "similarity_keywords": keywords,
                "raw_fields": fields  # For debugging and future enhancement
            }
            
            return entry
            
        except Exception as e:
            print(f"⚠️ Error processing issue #{issue.get('number', 'unknown')}: {e}")
            return None
    
    def _extract_initiative_id(self, title: str, issue_number: int) -> str:
        """Extract or generate initiative ID."""
        # Look for initiative title in square brackets
        match = re.search(r'\[Initiative\]\s*([^[]+?)(?:\s|$)', title)
        if match:
            # Clean and convert to camelCase-like format
            raw_title = match.group(1).strip()
            initiative_id = re.sub(r'[^a-zA-Z0-9]+', '', raw_title)
            if initiative_id:
                return initiative_id
        
        # Fallback: use issue number
        return f"initiative{issue_number}"
    
    def _parse_issue_body(self, body: str) -> Dict[str, str]:
        """Parse structured fields from issue body."""
        fields = {}
        
        # Define field patterns
        field_patterns = [
            'archetype', 'domain', 'initiativeTitle', 'purpose', 'scope',
            'capabilityAreas', 'deliverables', 'successIndicators', 
            'constraints', 'dependencies', 'outcomeStatus', 'postmortem',
            'lessonsFromPastInitiatives'
        ]
        
        for field in field_patterns:
            # Pattern to match field and its content
            pattern = rf"###\s*{field}\s*\n\s*([^#]*?)(?=\n###|\n\n|\Z)"
            match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                # Clean up common markdown formatting
                content = re.sub(r'^[-*]\s*', '', content, flags=re.MULTILINE)
                fields[field] = content
        
        return fields
    
    def _extract_lessons(self, fields: Dict[str, str], state: str) -> Dict[str, List[str]]:
        """Extract lessons including risks, mitigations, and root causes."""
        lessons = {
            "risks": [],
            "mitigations": [],
            "root_causes": [],
            "success_factors": [],
            "recommendations": []
        }
        
        # Extract from postmortem
        postmortem = fields.get('postmortem', '')
        if postmortem:
            lessons["root_causes"].extend(self._extract_root_causes(postmortem))
            lessons["mitigations"].extend(self._extract_mitigations(postmortem))
        
        # Extract from constraints (potential risks)
        constraints = fields.get('constraints', '')
        if constraints:
            lessons["risks"].extend(self._extract_risks_from_constraints(constraints))
        
        # Extract from scope (common risks)
        scope = fields.get('scope', '')
        if scope and 'outOfScope' in scope:
            lessons["risks"].extend(self._extract_scope_risks(scope))
        
        # Extract success factors from completed initiatives
        if state == 'closed' and fields.get('outcomeStatus') == 'delivered':
            success_indicators = fields.get('successIndicators', '')
            if success_indicators:
                lessons["success_factors"].extend(self._extract_success_factors(success_indicators))
        
        return lessons
    
    def _extract_root_causes(self, postmortem: str) -> List[str]:
        """Extract root causes from postmortem text."""
        causes = []
        
        # Look for explicit root cause patterns
        patterns = [
            r'rootCause[:\s]+([^,\n]+)',
            r'root\s+cause[:\s]+([^,\n]+)',
            r'caused\s+by[:\s]+([^,\n]+)',
            r'due\s+to[:\s]+([^,\n]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, postmortem, re.IGNORECASE)
            causes.extend([match.strip() for match in matches if match.strip()])
        
        return causes[:3]  # Limit to most relevant
    
    def _extract_mitigations(self, postmortem: str) -> List[str]:
        """Extract mitigations from postmortem text."""
        mitigations = []
        
        # Look for mitigation patterns
        patterns = [
            r'mitigation[s]?[:\s]+([^,\n]+)',
            r'to\s+prevent[:\s]+([^,\n]+)',
            r'solution[:\s]+([^,\n]+)',
            r'resolved\s+by[:\s]+([^,\n]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, postmortem, re.IGNORECASE)
            mitigations.extend([match.strip() for match in matches if match.strip()])
        
        return mitigations[:3]  # Limit to most relevant
    
    def _extract_risks_from_constraints(self, constraints: str) -> List[str]:
        """Extract potential risks from constraints."""
        risks = []
        
        # Common constraint patterns that indicate risks
        risk_indicators = [
            'budget', 'timeline', 'resource', 'dependency', 'complexity',
            'security', 'compliance', 'integration', 'scalability'
        ]
        
        for indicator in risk_indicators:
            if indicator in constraints.lower():
                risks.append(f"Potential {indicator} constraints")
        
        return risks[:2]  # Limit to avoid noise
    
    def _extract_scope_risks(self, scope: str) -> List[str]:
        """Extract risks from scope definition."""
        risks = []
        
        # Look for out-of-scope items that suggest risks
        out_of_scope_match = re.search(r'outOfScope[:\s]*([^,\n]+)', scope, re.IGNORECASE)
        if out_of_scope_match:
            out_items = out_of_scope_match.group(1)
            if 'sync' in out_items.lower():
                risks.append("Data synchronisation complexity")
            if 'integration' in out_items.lower():
                risks.append("External integration challenges")
        
        return risks
    
    def _extract_success_factors(self, success_indicators: str) -> List[str]:
        """Extract success factors from delivered initiatives."""
        factors = []
        
        # Look for measurable outcomes that worked
        lines = success_indicators.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-'):
                factors.append(f"Achieved: {line}")
        
        return factors[:2]  # Most important factors
    
    def _generate_keywords(self, fields: Dict[str, str], title: str) -> List[str]:
        """Generate keywords for similarity matching."""
        keywords = []
        
        # Add archetype and domain
        if fields.get('archetype'):
            keywords.append(fields['archetype'].lower())
        if fields.get('domain'):
            keywords.append(fields['domain'].lower())
        
        # Extract keywords from title and purpose
        text_fields = [title, fields.get('purpose', ''), fields.get('initiativeTitle', '')]
        
        for text in text_fields:
            if text:
                # Extract meaningful words (excluding common stop words)
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
                meaningful_words = [w for w in words if w not in stop_words]
                keywords.extend(meaningful_words)
        
        # Remove duplicates and limit
        return list(dict.fromkeys(keywords))[:10]
    
    def _map_status(self, github_state: str, outcome_status: Optional[str]) -> str:
        """Map GitHub issue state and outcome status to standard status."""
        if outcome_status:
            return outcome_status
        
        return 'inProgress' if github_state == 'open' else 'completed'


def main():
    """Main entry point."""
    print("🔍 SPECTRA Initiative History Builder")
    
    # Check for GitHub token
    if not os.environ.get('GITHUB_TOKEN'):
        print("⚠️ Warning: No GITHUB_TOKEN found. API rate limits may apply.")
    
    # Build history
    builder = InitiativeHistoryBuilder()
    
    try:
        entries = builder.build_history()
        print(f"✅ Successfully built history index with {len(entries)} entries")
        return 0
    except Exception as e:
        print(f"❌ Error building history: {e}")
        return 1


if __name__ == "__main__":
    exit(main())