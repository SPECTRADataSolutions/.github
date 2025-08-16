#!/usr/bin/env python3
"""
SPECTRA Repository Factory

This script processes slash commands to create new repositories with proper
organizational structure, canonical labels, and baseline files.

Framework as Law: This script enforces repository creation standards.
"""

import os
import re
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone


class RepositoryFactory:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SPECTRA-Repository-Factory",
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
        
        return params
    
    def validate_command_params(self, params: Dict) -> Tuple[bool, List[str]]:
        """Validate slash command parameters."""
        
        errors = []
        
        # Check required parameters
        if 'repoName' not in params:
            errors.append("❌ Missing required parameter: repoName")
        elif not self._is_valid_camel_case(params['repoName']):
            errors.append("❌ repoName must be single-token camelCase (e.g., 'governancePolicy')")
        
        if 'domain' not in params:
            errors.append("❌ Missing required parameter: domain")
        elif not self._is_valid_camel_case(params['domain']):
            errors.append("❌ domain must be single-token camelCase (e.g., 'governance')")
        
        if 'visibility' not in params:
            errors.append("❌ Missing required parameter: visibility")
        elif params['visibility'] not in ['public', 'private']:
            errors.append("❌ visibility must be 'public' or 'private'")
        
        # Optional templateRepo validation
        if 'templateRepo' in params:
            template_pattern = r'^SPECTRADataSolutions/[\w-]+$'
            if not re.match(template_pattern, params['templateRepo']):
                errors.append("❌ templateRepo must be in format 'SPECTRADataSolutions/repoName'")
        
        return len(errors) == 0, errors
    
    def _is_valid_camel_case(self, text: str) -> bool:
        """Check if text is valid single-token camelCase."""
        
        # Must start with lowercase letter, followed by letters/numbers only
        # No spaces, hyphens, underscores, or other special characters
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        return bool(re.match(pattern, text))
    
    def check_repository_exists(self, org: str, repo_name: str) -> bool:
        """Check if repository already exists in the organization."""
        
        url = f"{self.base_url}/repos/{org}/{repo_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.RequestException:
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
                "private": visibility == "private",
                "default_branch": "main",
                "has_issues": True,
                "has_projects": True,
                "has_wiki": False,
                "auto_init": template_repo is None,  # Only auto-init if not using template
                "gitignore_template": "Python" if template_repo is None else None,
                "license_template": None
            }
            
            # Create repository
            if template_repo:
                # Create from template
                template_parts = template_repo.split('/')
                template_owner = template_parts[0]
                template_name = template_parts[1]
                
                url = f"{self.base_url}/repos/{template_owner}/{template_name}/generate"
                repo_data.update({
                    "owner": org,
                    "include_all_branches": False
                })
            else:
                # Create new repository
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
            
            # Add organizational metadata and baseline files if not templated
            if not template_repo:
                self._add_organizational_metadata(org, repo_name, domain, warnings)
                self._add_baseline_readme(org, repo_name, domain, warnings)
            
            return True, repo_url, warnings
            
        except requests.RequestException as e:
            error_msg = f"❌ Failed to create repository: {str(e)}"
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    if 'message' in error_data:
                        error_msg += f" - {error_data['message']}"
                except:
                    pass
            return False, "", [error_msg]
    
    def _seed_canonical_labels(self, org: str, repo_name: str, warnings: List[str]) -> None:
        """Seed repository with canonical labels from .github/labels.json."""
        
        try:
            # Load canonical labels
            labels_path = os.path.join(os.path.dirname(__file__), '..', '.github', 'labels.json')
            if not os.path.exists(labels_path):
                warnings.append("⚠️ Canonical labels file not found, skipping label seeding")
                return
            
            with open(labels_path, 'r') as f:
                canonical_labels = json.load(f)
            
            url = f"{self.base_url}/repos/{org}/{repo_name}/labels"
            
            for label in canonical_labels:
                label_data = {
                    "name": label["name"],
                    "color": label["color"],
                    "description": label.get("description", "")
                }
                
                response = requests.post(url, headers=self.headers, json=label_data)
                if response.status_code not in [200, 201]:
                    warnings.append(f"⚠️ Failed to create label '{label['name']}'")
            
            print(f"✅ Seeded {len(canonical_labels)} canonical labels")
            
        except Exception as e:
            warnings.append(f"⚠️ Failed to seed canonical labels: {str(e)}")
    
    def _add_organizational_metadata(self, org: str, repo_name: str, domain: str, warnings: List[str]) -> None:
        """Add .spectra/metadata.yml organizational metadata."""
        
        try:
            # Create .spectra directory and metadata file
            metadata = {
                "dream": "SPECTRA",
                "archetype": "TBD",  # To be determined during repository setup
                "domain": domain,
                "repository": repo_name
            }
            
            metadata_content = "# SPECTRA Organizational Metadata\n"
            metadata_content += "# Update archetype based on repository purpose\n\n"
            for key, value in metadata.items():
                metadata_content += f"{key}: {value}\n"
            
            # Create the file via GitHub API
            url = f"{self.base_url}/repos/{org}/{repo_name}/contents/.spectra/metadata.yml"
            
            file_data = {
                "message": "Add organizational metadata",
                "content": self._encode_base64(metadata_content),
                "branch": "main"
            }
            
            response = requests.put(url, headers=self.headers, json=file_data)
            if response.status_code not in [200, 201]:
                warnings.append("⚠️ Failed to add organizational metadata")
            else:
                print("✅ Added organizational metadata")
                
        except Exception as e:
            warnings.append(f"⚠️ Failed to add organizational metadata: {str(e)}")
    
    def _add_baseline_readme(self, org: str, repo_name: str, domain: str, warnings: List[str]) -> None:
        """Add baseline README.md with organizational structure."""
        
        try:
            readme_content = f"""# {repo_name}

SPECTRA {domain} repository.

## 🏛️ Organisational Structure
**Dream:** SPECTRA  
**Archetype:** TBD  
**Domain:** {domain}  
**Repository:** {repo_name}

This repository is part of SPECTRA's canonical organisational structure. For more information, see [Canonical Organisational Structure](https://github.com/SPECTRADataSolutions/.github/docs/canonicalOrganisationalStructure.md).

## Getting Started

This repository was created using the SPECTRA Repository Factory. Please:

1. Update the archetype in `.spectra/metadata.yml` based on your repository's purpose
2. Update this README with specific project information
3. Configure appropriate branch protection rules
4. Set up CI/CD workflows as needed

## Documentation

- Add project-specific documentation here
- Link to relevant SPECTRA framework documentation
- Include setup and usage instructions

## Contributing

Please follow SPECTRA contribution guidelines and organizational standards.
"""
            
            # Check if README already exists (in case of auto-init)
            url = f"{self.base_url}/repos/{org}/{repo_name}/contents/README.md"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                # Update existing README
                existing_file = response.json()
                file_data = {
                    "message": "Update README with organizational structure",
                    "content": self._encode_base64(readme_content),
                    "sha": existing_file["sha"],
                    "branch": "main"
                }
            else:
                # Create new README
                file_data = {
                    "message": "Add baseline README with organizational structure",
                    "content": self._encode_base64(readme_content),
                    "branch": "main"
                }
            
            response = requests.put(url, headers=self.headers, json=file_data)
            if response.status_code not in [200, 201]:
                warnings.append("⚠️ Failed to add/update README.md")
            else:
                print("✅ Added/updated baseline README")
                
        except Exception as e:
            warnings.append(f"⚠️ Failed to add baseline README: {str(e)}")
    
    def _encode_base64(self, content: str) -> str:
        """Encode content to base64 for GitHub API."""
        import base64
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    def post_response_comment(self, repo_owner: str, repo_name: str, issue_number: int,
                            success: bool, repo_url: str, warnings: List[str], 
                            dry_run: bool = False) -> bool:
        """Post response comment with repository creation results."""
        
        if not self.github_token and not dry_run:
            print("❌ No GitHub token available for posting comment")
            return False
        
        # Format response comment
        if success:
            comment_body = f"""## 🏭 Repository Factory - Success

✅ **Repository Created:** [{repo_url.split('/')[-1]}]({repo_url})

**Repository Details:**
- **URL:** {repo_url}
- **Visibility:** {format_visibility(visibility)}
- **Default Branch:** main
- **Canonical Labels:** Seeded from .github/labels.json
- **Organizational Metadata:** Added to .spectra/metadata.yml

**Next Steps:**
1. Update the archetype in `.spectra/metadata.yml` based on repository purpose
2. Configure branch protection rules
3. Set up CI/CD workflows as needed
4. Update README with project-specific information

"""
        else:
            comment_body = """## 🏭 Repository Factory - Failed

❌ **Repository Creation Failed**

Please check the parameters and try again. Common issues:
- Repository name already exists
- Invalid parameter format
- Insufficient permissions

"""
        
        # Add warnings
        if warnings:
            comment_body += "**Warnings:**\n"
            for warning in warnings:
                comment_body += f"- {warning}\n"
            comment_body += "\n"
        
        comment_body += f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*"
        
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
            
            print(f"✅ Posted response comment: {comment_url}")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error posting response comment: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python repo_factory.py <comment_body> <repo_owner> <repo_name> <issue_number> [--dry-run]")
        sys.exit(1)
    
    comment_body = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]
    issue_number = int(sys.argv[4])
    dry_run = '--dry-run' in sys.argv
    
    factory = RepositoryFactory()
    
    # Parse command
    params = factory.parse_slash_command(comment_body)
    if not params:
        print("❌ No valid /create-repo command found in comment")
        sys.exit(1)
    
    print(f"📝 Parsed command parameters: {params}")
    
    # Validate parameters
    valid, errors = factory.validate_command_params(params)
    if not valid:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  {error}")
        
        # Post error comment
        factory.post_response_comment(
            repo_owner, repo_name, issue_number,
            success=False, repo_url="", warnings=errors, dry_run=dry_run
        )
        sys.exit(1)
    
    print("✅ Parameters validated successfully")
    
    # Create repository
    success, repo_url, warnings = factory.create_repository(params, dry_run=dry_run)
    
    if success:
        print(f"✅ Repository created successfully: {repo_url}")
    else:
        print("❌ Repository creation failed")
    
    # Post response comment
    factory.post_response_comment(
        repo_owner, repo_name, issue_number,
        success=success, repo_url=repo_url, warnings=warnings, dry_run=dry_run
    )


if __name__ == "__main__":
    main()