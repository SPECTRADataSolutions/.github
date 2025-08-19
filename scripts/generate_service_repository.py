#!/usr/bin/env python3
"""
SPECTRA Service Repository Generator

This script processes slash commands to create new repositories with proper
organisational structure, canonical labels, and baseline files.

Framework as Law: This script enforces repository creation standards.
"""

import os
import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone


class ServiceRepositoryGenerator:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Service-Repository-Generator",
            "Content-Type": "application/json"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def parse_slash_command(self, comment_body: str) -> Optional[Dict]:
        """Parse /create-repo slash command from comment body."""
        
        # Match the command pattern
        pattern = r'/create-repo\s+(.+)'
        match = re.search(pattern, comment_body, re.IGNORECASE)
        
        if not match:
            return None
        
        params_str = match.group(1).strip()
        
        # Parse parameters in key=value format
        params = {}
        param_pattern = r'(\w+)=([^\s]+)'
        
        for param_match in re.finditer(param_pattern, params_str):
            key = param_match.group(1)
            value = param_match.group(2)
            params[key] = value
        
        return params if params else None
    
    def validate_command_params(self, params: Dict) -> Tuple[bool, List[str]]:
        """Validate command parameters."""
        errors = []
        
        # Required parameters
        required = ['repoName', 'domain', 'visibility']
        for param in required:
            if param not in params:
                errors.append(f"Missing required parameter: {param}")
        
        # Validate repoName (camelCase)
        if 'repoName' in params:
            if not self._is_valid_camel_case(params['repoName']):
                errors.append("repoName must be camelCase (start with lowercase letter, no spaces/hyphens)")
        
        # Validate domain (camelCase)
        if 'domain' in params:
            if not self._is_valid_camel_case(params['domain']):
                errors.append("domain must be camelCase (start with lowercase letter, no spaces/hyphens)")
        
        # Validate visibility
        if 'visibility' in params:
            if params['visibility'].lower() not in ['public', 'private']:
                errors.append("visibility must be 'public' or 'private'")
        
        # Validate templateRepo if provided
        if 'templateRepo' in params:
            template = params['templateRepo']
            if not template.startswith('SPECTRADataSolutions/'):
                errors.append("templateRepo must be from SPECTRADataSolutions organisation")
        
        return len(errors) == 0, errors
    
    def _is_valid_camel_case(self, text: str) -> bool:
        """Check if text follows camelCase convention."""
        if not text:
            return False
        
        # Must start with lowercase letter, then letters/numbers only
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        return bool(re.match(pattern, text))
    
    def check_repository_exists(self, org: str, repo_name: str) -> bool:
        """Check if repository already exists."""
        url = f"{self.base_url}/repos/{org}/{repo_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def create_repository(self, params: Dict, dry_run: bool = False) -> Tuple[bool, str, List[str]]:
        """Create a new repository with the specified parameters."""
        
        repo_name = params['repoName']
        domain = params['domain']
        visibility = params['visibility']
        template_repo = params.get('templateRepo')
        
        org = "SPECTRADataSolutions"
        warnings = []
        
        if dry_run:
            return True, f"https://github.com/{org}/{repo_name}", ["🔍 DRY RUN - Repository would be created"]
        
        if not self.github_token:
            return False, "", ["❌ No GitHub token available for repository creation"]
        
        # Check if repository already exists
        if self.check_repository_exists(org, repo_name):
            return False, "", [f"❌ Repository '{repo_name}' already exists in {org}"]
        
        try:
            # Prepare repository data
            repo_data = {
                "name": repo_name,
                "description": f"SPECTRA {domain} repository",
                "private": visibility.lower() == 'private',
                "has_issues": True,
                "has_projects": True,
                "has_wiki": False,
                "auto_init": True
            }
            
            # Add template repository if specified
            if template_repo:
                template_owner, template_name = template_repo.split('/', 1)
                repo_data["template_owner"] = template_owner
                repo_data["template_repo"] = template_name
                url = f"{self.base_url}/repos/{template_repo}/generate"
            else:
                url = f"{self.base_url}/orgs/{org}/repos"
            
            response = requests.post(url, headers=self.headers, json=repo_data)
            response.raise_for_status()
            
            repo_info = response.json()
            repo_url = repo_info['html_url']
            
            # Wait briefly for repository to be fully created
            import time
            # Wait for repository to be fully created using polling
            self._wait_for_repo_ready(org, repo_name)
            
            # Seed with canonical labels
            self._seed_canonical_labels(org, repo_name, warnings)
            
            # Add organisational metadata and baseline files if not templated
            if not template_repo:
                self._add_organisational_metadata(org, repo_name, domain, warnings)
                self._add_baseline_readme(org, repo_name, domain, warnings)
            
            return True, repo_url, warnings
            
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Repository creation failed: {str(e)}"
            if hasattr(e, 'response') and e.response:
                try:
                    error_detail = e.response.json()
                    if 'message' in error_detail:
                        error_msg = f"❌ {error_detail['message']}"
                except:
                    pass
            return False, "", [error_msg]
        except Exception as e:
            return False, "", [f"❌ Unexpected error: {str(e)}"]
    
    def _wait_for_repo_ready(self, org: str, repo_name: str, max_attempts: int = 10) -> bool:
        """Wait for repository to be fully created and accessible."""
        import time
        
        for attempt in range(max_attempts):
            if self.check_repository_exists(org, repo_name):
                return True
            time.sleep(2)  # Wait 2 seconds between attempts
        
        return False
    
    def _seed_canonical_labels(self, org: str, repo_name: str, warnings: List[str]):
        """Seed repository with canonical labels from .github repo."""
        try:
            # Get labels from .github repository
            url = f"{self.base_url}/repos/{org}/.github/contents/.github/labels.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            import base64
            content = base64.b64decode(response.json()['content']).decode('utf-8')
            labels = json.loads(content)
            
            # Create labels in the new repository
            for label in labels:
                self._create_or_update_label(org, repo_name, label, warnings)
                
        except Exception as e:
            warnings.append(f"⚠️ Failed to seed canonical labels: {str(e)}")
    
    def _create_or_update_label(self, org: str, repo_name: str, label: Dict, warnings: List[str]):
        """Create or update a single label."""
        try:
            url = f"{self.base_url}/repos/{org}/{repo_name}/labels"
            response = requests.post(url, headers=self.headers, json=label)
            
            if response.status_code == 422:  # Label already exists, update it
                update_url = f"{url}/{label['name']}"
                requests.patch(update_url, headers=self.headers, json=label)
                
        except Exception as e:
            warnings.append(f"⚠️ Failed to create/update label '{label.get('name', 'unknown')}': {str(e)}")
    
    def _add_organisational_metadata(self, org: str, repo_name: str, domain: str, warnings: List[str]):
        """Add organisational metadata file."""
        try:
            metadata = {
                "dream": "SPECTRA",
                "archetype": "TBD",
                "domain": domain,
                "repository": repo_name
            }
            
            self._create_file(
                org, repo_name, 
                ".spectra/metadata.yml", 
                self._yaml_dump(metadata),
                "chore: add organisational metadata",
                warnings
            )
            
        except Exception as e:
            warnings.append(f"⚠️ Failed to add organisational metadata: {str(e)}")
    
    def _add_baseline_readme(self, org: str, repo_name: str, domain: str, warnings: List[str]):
        """Add baseline README file."""
        try:
            readme_content = f"""# {repo_name}

## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** TBD  
**Domain:** {domain}  
**Repository:** {repo_name}

## Purpose
This repository is part of SPECTRA's canonical organisational structure.

## Getting Started
1. Update the archetype in `.spectra/metadata.yml` based on repository purpose
2. Configure branch protection rules
3. Set up CI/CD workflows as needed
4. Update this README with project-specific information

## Links
- [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/blob/main/docs/canonicalOrganisationalStructure.md)
- [SPECTRA Framework](https://github.com/SPECTRADataSolutions)

---
*Generated by SPECTRA Service Repository Generator*
"""
            
            self._create_file(
                org, repo_name,
                "README.md",
                readme_content,
                "docs: add baseline README with organisational structure",
                warnings
            )
            
        except Exception as e:
            warnings.append(f"⚠️ Failed to add baseline README: {str(e)}")
    
    def _create_file(self, org: str, repo_name: str, path: str, content: str, message: str, warnings: List[str]):
        """Create a file in the repository."""
        try:
            import base64
            url = f"{self.base_url}/repos/{org}/{repo_name}/contents/{path}"
            
            file_data = {
                "message": message,
                "content": base64.b64encode(content.encode('utf-8')).decode('utf-8')
            }
            
            response = requests.put(url, headers=self.headers, json=file_data)
            response.raise_for_status()
            
        except Exception as e:
            warnings.append(f"⚠️ Failed to create {path}: {str(e)}")
    
    def _yaml_dump(self, data: Dict) -> str:
        """Simple YAML dumper for basic data structures."""
        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def post_response_comment(self, repo_owner: str, repo_name: str, issue_number: int,
                            success: bool, repo_url: str, warnings: List[str], 
                            dry_run: bool = False) -> bool:
        """Post response comment with repository creation results."""
        
        if dry_run:
            print(f"🔍 DRY RUN - Would post comment to issue #{issue_number}")
            return True
        
        try:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            
            if success:
                # Success response
                comment_body = f"""## 🏗️ Service Repository Generator - Success

✅ **Repository Created:** [{repo_url.split('/')[-1]}]({repo_url})

**Repository Details:**
- **URL:** {repo_url}
- **Canonical Labels:** Seeded from .github/labels.json
- **Organisational Metadata:** Added to .spectra/metadata.yml

**Next Steps:**
1. Update the archetype in `.spectra/metadata.yml` based on repository purpose
2. Configure branch protection rules
3. Set up CI/CD workflows as needed
4. Update README with project-specific information

*Generated on {timestamp}*"""
                
                if warnings:
                    comment_body += "\n\n**Warnings:**\n" + "\n".join(f"- {w}" for w in warnings)
            else:
                # Failure response
                comment_body = f"""## 🏗️ Service Repository Generator - Error

❌ **Repository Creation Failed**

**Errors:**
{chr(10).join(f"- {w}" for w in warnings)}

Please check the parameters and try again.

*Generated on {timestamp}*"""
            
            # Post the comment
            url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
            response = requests.post(
                url,
                headers=self.headers,
                json={"body": comment_body}
            )
            response.raise_for_status()
            
            print(f"✅ Response comment posted to issue #{issue_number}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to post response comment: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False


def main():
    """Main entry point for command line usage."""
    import sys
    
    if len(sys.argv) != 5:
        print("Usage: python generate_service_repository.py <comment_body> <repo_owner> <repo_name> <issue_number>")
        sys.exit(1)
    
    comment_body = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]
    issue_number = int(sys.argv[4])
    
    # Create generator instance
    generator = ServiceRepositoryGenerator()
    
    # Parse command
    print("🔍 Parsing slash command...")
    params = generator.parse_slash_command(comment_body)
    if not params:
        print("❌ No valid /create-repo command found in comment")
        return
    
    print(f"✅ Parsed parameters: {params}")
    
    # Validate parameters
    print("🔍 Validating parameters...")
    valid, errors = generator.validate_command_params(params)
    if not valid:
        print("❌ Parameter validation failed:")
        for error in errors:
            print(f"  - {error}")
        
        # Post error response
        generator.post_response_comment(
            repo_owner, repo_name, issue_number,
            success=False, repo_url="", warnings=errors
        )
        return
    
    print("✅ Parameters validated")
    
    # Create repository
    print("🏗️ Creating repository...")
    success, repo_url, warnings = generator.create_repository(params)
    
    if success:
        print(f"✅ Repository created: {repo_url}")
        if warnings:
            print("⚠️ Warnings:")
            for warning in warnings:
                print(f"  {warning}")
    else:
        print("❌ Repository creation failed")
        for warning in warnings:
            print(f"  {warning}")
    
    # Post response comment
    print("📝 Posting response comment...")
    comment_success = generator.post_response_comment(
        repo_owner, repo_name, issue_number,
        success=success, repo_url=repo_url, warnings=warnings
    )
    
    if comment_success:
        print("✅ Response comment posted")
    else:
        print("❌ Failed to post response comment")


if __name__ == "__main__":
    main()