#!/usr/bin/env python3
"""
SPECTRA Ticketing Context Server Stub

Stub implementation for ticketing context server following SPECTRA security standards.
Implements project allowlists, controlled operations, and audit logging.
"""

import os
import logging
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta
from dataProvider import DataProvider, RateLimit, ProviderAuth


class TicketingProvider(DataProvider):
    """
    Ticketing provider stub extending base data provider with ticketing-specific security.
    
    Additional Features:
    - Project allowlist enforcement
    - Controlled create/update operations
    - Ticketing system integration (stub)
    - Project access validation
    """
    
    def __init__(self, config_path: str = "config/contextConfig.yaml"):
        """
        Initialise ticketing provider with configuration.
        
        Args:
            config_path: Path to context configuration file
        """
        # Load config for ticketing provider
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.provider_config = self.config.get('providers', {}).get('ticketing', {})
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Validate configuration
        self._validate_ticketing_config()
        
        # Initialize components
        self.rate_limits = self._get_rate_limits()
        self.request_history: List[datetime] = []
        self.auth = self._get_authentication()
        self.project_allowlist = self._get_project_allowlist()
        
    def _validate_ticketing_config(self) -> None:
        """Validate ticketing provider configuration."""
        if not self.provider_config:
            raise ValueError("Ticketing provider configuration not found")
            
        required_fields = ['enabled', 'endpoint', 'authentication', 'rateLimits', 'allowedOperations', 'projectAllowlist']
        for field in required_fields:
            if field not in self.provider_config:
                raise ValueError(f"Missing required field in ticketing provider config: {field}")
                
        # Validate security settings
        security_config = self.config.get('security', {})
        if security_config.get('defaultPolicy') != 'deny':
            raise ValueError("Security policy must be 'deny' (default-deny)")
            
        # Validate operations are explicitly allowed
        allowed_ops = self.provider_config.get('allowedOperations', [])
        valid_ops = {'read', 'search', 'list', 'create', 'update'}
        for op in allowed_ops:
            if op not in valid_ops:
                raise ValueError(f"Invalid operation in allowlist: {op}")
                
    def _get_project_allowlist(self) -> List[str]:
        """Get project allowlist from configuration."""
        return self.provider_config.get('projectAllowlist', [])
        
    def _validate_project_access(self, project_id: str) -> bool:
        """
        Validate project access against allowlist.
        
        Args:
            project_id: Project ID or key
            
        Returns:
            True if project access is allowed
        """
        if project_id not in self.project_allowlist:
            self.logger.warning(f"Project access denied (not in allowlist): {project_id}")
            return False
        return True
        
    def read_ticket(self, project_id: str, ticket_id: str) -> Dict[str, Any]:
        """
        Read ticket information.
        
        Args:
            project_id: Project ID or key
            ticket_id: Ticket identifier
            
        Returns:
            Ticket information (stub implementation)
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Ticketing provider is disabled")
            
        if not self._check_operation_allowed('read'):
            self._log_request('read_ticket', False, "Operation not in allowlist")
            raise ValueError("Read operation not allowed")
            
        if not self._validate_project_access(project_id):
            self._log_request('read_ticket', False, f"Project not in allowlist: {project_id}")
            raise ValueError(f"Access denied to project: {project_id}")
            
        if not self._check_rate_limits():
            self._log_request('read_ticket', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('read_ticket', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate ticket read (stub implementation)
        try:
            # In real implementation, this would call ticketing system API
            result = {
                "id": ticket_id,
                "project": project_id,
                "key": f"{project_id}-{ticket_id}",
                "summary": f"Simulated ticket {ticket_id} in project {project_id}",
                "description": "This is a simulated ticket for demonstration purposes",
                "status": "Open",
                "priority": "Medium",
                "type": "Task",
                "assignee": "user@example.com",
                "reporter": "reporter@example.com",
                "created": "2024-01-01T00:00:00Z",
                "updated": "2024-01-15T00:00:00Z",
                "labels": ["simulation", "test"],
                "url": f"https://ticketing.example.com/browse/{project_id}-{ticket_id}"
            }
            
            self._log_request('read_ticket', True)
            return result
            
        except Exception as e:
            self._log_request('read_ticket', False, str(e))
            raise
            
    def list_tickets(self, project_id: str, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List tickets for a project.
        
        Args:
            project_id: Project ID or key
            status: Optional status filter
            limit: Maximum number of tickets
            
        Returns:
            List of tickets
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Ticketing provider is disabled")
            
        if not self._check_operation_allowed('list'):
            self._log_request('list_tickets', False, "Operation not in allowlist")
            raise ValueError("List operation not allowed")
            
        if not self._validate_project_access(project_id):
            self._log_request('list_tickets', False, f"Project not in allowlist: {project_id}")
            raise ValueError(f"Access denied to project: {project_id}")
            
        if not self._check_rate_limits():
            self._log_request('list_tickets', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('list_tickets', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate ticket listing
        try:
            tickets = []
            statuses = ['Open', 'In Progress', 'Closed'] if not status else [status]
            
            # Simulate a few tickets
            for i in range(min(limit, 5)):  # Max 5 simulated tickets
                ticket_status = statuses[i % len(statuses)]
                tickets.append({
                    "id": f"ticket_{i+1}",
                    "project": project_id,
                    "key": f"{project_id}-{i+1}",
                    "summary": f"Simulated ticket {i+1}",
                    "status": ticket_status,
                    "priority": "Medium",
                    "type": "Task",
                    "assignee": f"user{i+1}@example.com",
                    "created": "2024-01-01T00:00:00Z",
                    "url": f"https://ticketing.example.com/browse/{project_id}-{i+1}"
                })
                
            self._log_request('list_tickets', True)
            return tickets
            
        except Exception as e:
            self._log_request('list_tickets', False, str(e))
            raise
            
    def search_tickets(self, project_id: str, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search tickets within a project.
        
        Args:
            project_id: Project ID or key
            query: Search query
            limit: Maximum number of results
            
        Returns:
            Search results
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Ticketing provider is disabled")
            
        if not self._check_operation_allowed('search'):
            self._log_request('search_tickets', False, "Operation not in allowlist")
            raise ValueError("Search operation not allowed")
            
        if not self._validate_project_access(project_id):
            self._log_request('search_tickets', False, f"Project not in allowlist: {project_id}")
            raise ValueError(f"Access denied to project: {project_id}")
            
        if not self._check_rate_limits():
            self._log_request('search_tickets', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('search_tickets', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate search
        try:
            # Simulate search results
            results = []
            for i in range(min(limit, 3)):  # Max 3 simulated results
                results.append({
                    "id": f"search_result_{i+1}",
                    "project": project_id,
                    "key": f"{project_id}-SEARCH-{i+1}",
                    "summary": f"Ticket matching '{query}' (result {i+1})",
                    "status": "Open",
                    "score": 0.9 - (i * 0.1),  # Relevance score
                    "highlight": f"...matching content for '{query}' (redacted)...",
                    "url": f"https://ticketing.example.com/browse/{project_id}-SEARCH-{i+1}"
                })
                
            self._log_request('search_tickets', True)
            return results
            
        except Exception as e:
            self._log_request('search_tickets', False, str(e))
            raise
            
    def create_ticket(self, project_id: str, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new ticket.
        
        Args:
            project_id: Project ID or key
            ticket_data: Ticket creation data
            
        Returns:
            Created ticket information
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Ticketing provider is disabled")
            
        if not self._check_operation_allowed('create'):
            self._log_request('create_ticket', False, "Operation not in allowlist")
            raise ValueError("Create operation not allowed")
            
        if not self._validate_project_access(project_id):
            self._log_request('create_ticket', False, f"Project not in allowlist: {project_id}")
            raise ValueError(f"Access denied to project: {project_id}")
            
        if not self._check_rate_limits():
            self._log_request('create_ticket', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('create_ticket', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Validate required fields
        required_fields = ['summary', 'description', 'type']
        for field in required_fields:
            if field not in ticket_data:
                self._log_request('create_ticket', False, f"Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")
                
        # Simulate ticket creation
        try:
            # In real implementation, this would call ticketing system API
            new_ticket_id = f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            result = {
                "id": new_ticket_id,
                "project": project_id,
                "key": f"{project_id}-{new_ticket_id}",
                "summary": ticket_data['summary'],
                "description": ticket_data['description'],
                "type": ticket_data['type'],
                "status": "Open",
                "priority": ticket_data.get('priority', 'Medium'),
                "assignee": ticket_data.get('assignee'),
                "reporter": "system@example.com",  # Simulated system user
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "url": f"https://ticketing.example.com/browse/{project_id}-{new_ticket_id}"
            }
            
            self._log_request('create_ticket', True)
            return result
            
        except Exception as e:
            self._log_request('create_ticket', False, str(e))
            raise
            
    def update_ticket(self, project_id: str, ticket_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing ticket.
        
        Args:
            project_id: Project ID or key
            ticket_id: Ticket identifier
            update_data: Fields to update
            
        Returns:
            Updated ticket information
        """
        # Security checks
        if not self._check_enabled():
            raise RuntimeError("Ticketing provider is disabled")
            
        if not self._check_operation_allowed('update'):
            self._log_request('update_ticket', False, "Operation not in allowlist")
            raise ValueError("Update operation not allowed")
            
        if not self._validate_project_access(project_id):
            self._log_request('update_ticket', False, f"Project not in allowlist: {project_id}")
            raise ValueError(f"Access denied to project: {project_id}")
            
        if not self._check_rate_limits():
            self._log_request('update_ticket', False, "Rate limit exceeded")
            raise ValueError("Rate limit exceeded")
            
        # Authentication check
        token = self._get_auth_token()
        if not token:
            self._log_request('update_ticket', False, "Authentication failed")
            raise RuntimeError("Authentication failed")
            
        # Simulate ticket update
        try:
            # In real implementation, this would update via ticketing system API
            result = {
                "id": ticket_id,
                "project": project_id,
                "key": f"{project_id}-{ticket_id}",
                "summary": update_data.get('summary', f"Updated ticket {ticket_id}"),
                "description": update_data.get('description', "Ticket updated via SPECTRA assistant"),
                "status": update_data.get('status', 'Open'),
                "priority": update_data.get('priority', 'Medium'),
                "updated": datetime.now().isoformat(),
                "updated_by": "system@example.com",
                "changes": list(update_data.keys()),
                "url": f"https://ticketing.example.com/browse/{project_id}-{ticket_id}"
            }
            
            self._log_request('update_ticket', True)
            return result
            
        except Exception as e:
            self._log_request('update_ticket', False, str(e))
            raise
            
    def get_status(self) -> Dict[str, Any]:
        """Get ticketing provider status and configuration."""
        base_status = super().get_status()
        base_status.update({
            "provider": "ticketing",
            "project_allowlist": self.project_allowlist,
            "allowlist_size": len(self.project_allowlist)
        })
        return base_status


def main():
    """Example usage of the TicketingProvider."""
    try:
        provider = TicketingProvider()
        
        print("🎫 Ticketing Provider Status:")
        status = provider.get_status()
        for key, value in status.items():
            if key == 'project_allowlist':
                print(f"  {key}: {len(value)} projects")
            else:
                print(f"  {key}: {value}")
                
        if not status['enabled']:
            print("\n⚠️  Provider is disabled. Enable in config/contextConfig.yaml to test operations.")
            return
            
        if not status['auth_configured']:
            print("\n⚠️  Authentication not configured. Set TICKETING_TOKEN environment variable.")
            return
            
        if not status['project_allowlist']:
            print("\n⚠️  No projects in allowlist. Add projects to config.")
            return
            
        print("\n🧪 Testing Operations:")
        
        # Test with first project in allowlist
        test_project = status['project_allowlist'][0] if status['project_allowlist'] else None
        
        if test_project:
            # Test ticket read
            try:
                result = provider.read_ticket(test_project, "TEST-123")
                print(f"  ✅ Read Ticket: {result['key']}")
            except Exception as e:
                print(f"  ❌ Read Ticket: {e}")
                
            # Test ticket listing
            try:
                results = provider.list_tickets(test_project, limit=3)
                print(f"  ✅ List Tickets: {len(results)} tickets")
            except Exception as e:
                print(f"  ❌ List Tickets: {e}")
                
            # Test ticket creation (if allowed)
            try:
                ticket_data = {
                    "summary": "Test ticket from SPECTRA assistant",
                    "description": "This is a test ticket created by the assistant",
                    "type": "Task",
                    "priority": "Low"
                }
                result = provider.create_ticket(test_project, ticket_data)
                print(f"  ✅ Create Ticket: {result['key']}")
            except Exception as e:
                print(f"  ❌ Create Ticket: {e}")
                
        # Test search
        try:
            results = provider.search_tickets(test_project or "PROJ-001", "test query", limit=2)
            print(f"  ✅ Search: {len(results)} results")
        except Exception as e:
            print(f"  ❌ Search: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()