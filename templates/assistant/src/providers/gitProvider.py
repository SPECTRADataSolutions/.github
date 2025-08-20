#!/usr/bin/env python3
"""
SPECTRA Git Context Server Stub

Stub implementation for git context server following SPECTRA security standards.
Implements repository allowlists, read-only operations, and audit logging.
"""

import os
import logging
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta
from dataProvider import DataProvider, RateLimit, ProviderAuth


class GitProvider(DataProvider):
    """
    Git provider stub extending base data provider with git-specific security.
    
    Additional Features:
    - Repository allowlist enforcement
    - Read-only operations only
    - GitHub API integration (stub)
    - Repository access validation
    """
    
    def __init__(self, config_path: str = "config/contextConfig.yaml"):
        """
        Initialise git provider with configuration.
        
        Args:
            config_path: Path to context configuration file
        """
        # Load config differently for git provider
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.provider_config = self.config.get('providers', {}).get('git', {})
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Validate configuration
        self._validate_git_config()
        
        # Initialize components
        self.rate_limits = self._get_rate_limits()
        self.request_history: List[datetime] = []
        self.auth = self._get_authentication()
        self.repository_allowlist = self._get_repository_allowlist()
        
    def _validate_git_config(self) -> None:
        """Validate git provider configuration."""
        if not self.provider_config:
            raise ValueError("Git provider configuration not found")
            
        required_fields = ['enabled', 'endpoint', 'authentication', 'rateLimits', 'allowedOperations', 'repositoryAllowlist']
        for field in required_fields:
            if field not in self.provider_config:
                raise ValueError(f"Missing required field in git provider config: {field}")
                
        # Validate security settings
        security_config = self.config.get('security', {})
        if security_config.get('defaultPolicy') != 'deny':
            raise ValueError("Security policy must be 'deny' (default-deny)")
            
        # Validate only read operations are allowed
        allowed_ops = self.provider_config.get('allowedOperations', [])
        write_ops = {'push', 'commit', 'merge', 'delete', 'create', 'write'}
        if any(op in write_ops for op in allowed_ops):
            raise ValueError("Git provider must be read-only (no write operations allowed)")
            
    def _get_repository_allowlist(self) -> List[str]:
        """Get repository allowlist from configuration."""
        return self.provider_config.get('repositoryAllowlist', [])
        
    def _validate_repository_access(self, repository: str) -> bool:
        """
        Validate repository access against allowlist.
        
        Args:
            repository: Repository in format 'owner/repo'
            
        Returns:
            True if repository access is allowed
        """
        if repository not in self.repository_allowlist:
            self.logger.warning(f"Repository access denied (not in allowlist): {repository}")
            return False
        return True
        
    def read_repository(self, repository: str) -> Dict[str, Any]:
        """
        Read repository information.
        
        Args:
            repository: Repository in format 'owner/repo'
            
        Returns:
            Repository information (stub implementation)
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Git provider is disabled")
            
        if not self._check_operation_allowed('read'):
            self._log_request('read_repository', False, "Operation not in allowlist")
            raise ValueError("Read operation not allowed")
            
        if not self._validate_repository_access(repository):
            self._log_request('read_repository', False, f"Repository not in allowlist: {repository}")
            raise ValueError(f"Access denied to repository: {repository}")
            
        if not self._check_rate_limits():
            self._log_request('read_repository', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('read_repository', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate repository read (stub implementation)
        try:
            # In real implementation, this would call GitHub API
            owner, repo_name = repository.split('/')
            result = {
                "full_name": repository,
                "owner": owner,
                "name": repo_name,
                "description": f"Repository {repository} (simulated)",
                "private": False,
                "default_branch": "main",
                "language": "Python",
                "topics": ["spectra", "ai", "assistant"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T00:00:00Z",
                "clone_url": f"https://github.com/{repository}.git"
            }
            
            self._log_request('read_repository', True)
            return result
            
        except Exception as e:
            self._log_request('read_repository', False, str(e))
            raise
            
    def list_repositories(self, owner: str) -> List[Dict[str, Any]]:
        """
        List repositories for an owner (filtered by allowlist).
        
        Args:
            owner: Repository owner/organisation
            
        Returns:
            List of allowed repositories
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Git provider is disabled")
            
        if not self._check_operation_allowed('list'):
            self._log_request('list_repositories', False, "Operation not in allowlist")
            raise ValueError("List operation not allowed")
            
        if not self._check_rate_limits():
            self._log_request('list_repositories', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('list_repositories', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Filter repositories by allowlist
        try:
            allowed_repos = []
            for repo in self.repository_allowlist:
                if repo.startswith(f"{owner}/"):
                    repo_name = repo.split('/', 1)[1]
                    allowed_repos.append({
                        "full_name": repo,
                        "name": repo_name,
                        "owner": owner,
                        "description": f"Repository {repo} (simulated)",
                        "private": False,
                        "url": f"https://github.com/{repo}"
                    })
                    
            self._log_request('list_repositories', True)
            return allowed_repos
            
        except Exception as e:
            self._log_request('list_repositories', False, str(e))
            raise
            
    def search_repositories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search repositories (limited to allowlist).
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            Search results filtered by allowlist
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Git provider is disabled")
            
        if not self._check_operation_allowed('search'):
            self._log_request('search_repositories', False, "Operation not in allowlist")
            raise ValueError("Search operation not allowed")
            
        if not self._check_rate_limits():
            self._log_request('search_repositories', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('search_repositories', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Search within allowlist only
        try:
            # Simulate search within allowlist
            matching_repos = []
            query_lower = query.lower()
            
            for repo in self.repository_allowlist:
                if query_lower in repo.lower():
                    owner, repo_name = repo.split('/')
                    matching_repos.append({
                        "full_name": repo,
                        "name": repo_name,
                        "owner": owner,
                        "description": f"Repository {repo} matching '{query}' (simulated)",
                        "score": 0.95,  # Simulated relevance score
                        "url": f"https://github.com/{repo}"
                    })
                    
                if len(matching_repos) >= limit:
                    break
                    
            self._log_request('search_repositories', True)
            return matching_repos
            
        except Exception as e:
            self._log_request('search_repositories', False, str(e))
            raise
            
    def read_file_content(self, repository: str, file_path: str, ref: str = "main") -> Dict[str, Any]:
        """
        Read file content from repository.
        
        Args:
            repository: Repository in format 'owner/repo'
            file_path: Path to file in repository
            ref: Git reference (branch, tag, commit)
            
        Returns:
            File content and metadata
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Git provider is disabled")
            
        if not self._check_operation_allowed('read'):
            self._log_request('read_file', False, "Operation not in allowlist")
            raise ValueError("Read operation not allowed")
            
        if not self._validate_repository_access(repository):
            self._log_request('read_file', False, f"Repository not in allowlist: {repository}")
            raise ValueError(f"Access denied to repository: {repository}")
            
        if not self._check_rate_limits():
            self._log_request('read_file', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('read_file', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate file read
        try:
            # In real implementation, this would fetch actual file content
            result = {
                "repository": repository,
                "path": file_path,
                "ref": ref,
                "content": f"# Simulated content for {file_path}\n\nThis is simulated file content from {repository}",
                "encoding": "utf-8",
                "size": 150,
                "sha": "simulated_sha_abc123",
                "url": f"https://github.com/{repository}/blob/{ref}/{file_path}"
            }
            
            self._log_request('read_file', True)
            return result
            
        except Exception as e:
            self._log_request('read_file', False, str(e))
            raise
            
    def clone_repository(self, repository: str, target_path: str) -> Dict[str, Any]:
        """
        Clone repository (simulation - returns clone information).
        
        Args:
            repository: Repository in format 'owner/repo'
            target_path: Local path for clone
            
        Returns:
            Clone operation results
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Git provider is disabled")
            
        if not self._check_operation_allowed('clone'):
            self._log_request('clone_repository', False, "Operation not in allowlist")
            raise ValueError("Clone operation not allowed")
            
        if not self._validate_repository_access(repository):
            self._log_request('clone_repository', False, f"Repository not in allowlist: {repository}")
            raise ValueError(f"Access denied to repository: {repository}")
            
        if not self._check_rate_limits():
            self._log_request('clone_repository', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('clone_repository', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate clone operation
        try:
            # In real implementation, this would perform actual git clone
            result = {
                "repository": repository,
                "target_path": target_path,
                "clone_url": f"https://github.com/{repository}.git",
                "status": "simulated",
                "branch": "main",
                "commit_count": 42,
                "size_mb": 15.6,
                "cloned_at": datetime.now().isoformat()
            }
            
            self._log_request('clone_repository', True)
            return result
            
        except Exception as e:
            self._log_request('clone_repository', False, str(e))
            raise
            
    def get_status(self) -> Dict[str, Any]:
        """Get git provider status and configuration."""
        base_status = super().get_status()
        base_status.update({
            "provider": "git",
            "repository_allowlist": self.repository_allowlist,
            "allowlist_size": len(self.repository_allowlist),
            "read_only": True
        })
        return base_status


def main():
    """Example usage of the GitProvider."""
    try:
        provider = GitProvider()
        
        print("🔧 Git Provider Status:")
        status = provider.get_status()
        for key, value in status.items():
            if key == 'repository_allowlist':
                print(f"  {key}: {len(value)} repositories")
            else:
                print(f"  {key}: {value}")
                
        if not status['enabled']:
            print("\n⚠️  Provider is disabled. Enable in config/contextConfig.yaml to test operations.")
            return
            
        if not status['auth_configured']:
            print("\n⚠️  Authentication not configured. Set GITHUB_TOKEN environment variable.")
            return
            
        if not status['repository_allowlist']:
            print("\n⚠️  No repositories in allowlist. Add repositories to config.")
            return
            
        print("\n🧪 Testing Operations:")
        
        # Test with first repository in allowlist
        test_repo = status['repository_allowlist'][0] if status['repository_allowlist'] else None
        
        if test_repo:
            # Test repository read
            try:
                result = provider.read_repository(test_repo)
                print(f"  ✅ Read Repository: {result['full_name']}")
            except Exception as e:
                print(f"  ❌ Read Repository: {e}")
                
            # Test file read
            try:
                result = provider.read_file_content(test_repo, "README.md")
                print(f"  ✅ Read File: {result['path']} ({result['size']} bytes)")
            except Exception as e:
                print(f"  ❌ Read File: {e}")
                
        # Test search
        try:
            results = provider.search_repositories("spectra", limit=2)
            print(f"  ✅ Search: {len(results)} results")
        except Exception as e:
            print(f"  ❌ Search: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()