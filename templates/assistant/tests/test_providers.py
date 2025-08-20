#!/usr/bin/env python3
"""
Tests for SPECTRA Context Servers

Tests context server connectivity, security controls, and error handling.
"""

import pytest
import tempfile
import yaml
import os
import sys
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from providers.dataProvider import DataProvider
from providers.gitProvider import GitProvider
from providers.ticketingProvider import TicketingProvider


class TestDataProvider:
    """Test cases for DataProvider."""
    
    def create_test_config(self, config_data: dict) -> str:
        """Create a temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_standard_config(self) -> dict:
        """Get standard test configuration."""
        return {
            'metadata': {
                'version': '1.0.0',
                'environment': 'testing',
                'lastUpdated': '2024-01-01T00:00:00Z'
            },
            'security': {
                'defaultPolicy': 'deny',
                'authenticationRequired': True,
                'auditLogging': True,
                'secretRedaction': True
            },
            'providers': {
                'data': {
                    'enabled': True,
                    'endpoint': 'https://data.test.com/api',
                    'authentication': {
                        'type': 'token',
                        'envVariable': 'DATA_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 30,
                        'requestsPerHour': 1000
                    },
                    'allowedOperations': ['read', 'search', 'query']
                },
                'git': {
                    'enabled': True,
                    'endpoint': 'https://api.github.com',
                    'authentication': {
                        'type': 'token',
                        'envVariable': 'GITHUB_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 20,
                        'requestsPerHour': 500
                    },
                    'allowedOperations': ['read', 'search', 'list'],
                    'repositoryAllowlist': ['SPECTRADataSolutions/test-repo']
                },
                'ticketing': {
                    'enabled': True,
                    'endpoint': 'https://ticketing.test.com/api',
                    'authentication': {
                        'type': 'api-key',
                        'envVariable': 'TICKETING_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 10,
                        'requestsPerHour': 200
                    },
                    'allowedOperations': ['read', 'search', 'list'],
                    'projectAllowlist': ['TEST-001']
                }
            },
            'monitoring': {
                'metricsEnabled': True,
                'healthChecks': {
                    'enabled': True,
                    'intervalSeconds': 60
                },
                'alerting': {
                    'errorThreshold': 0.05,
                    'latencyThreshold': 2000
                }
            }
        }
    
    def test_data_provider_initialization(self):
        """Test DataProvider initialization with valid config."""
        config = self.get_standard_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            assert provider.provider_config is not None
            assert provider.rate_limits.requests_per_minute == 30
            assert provider.auth.env_variable == 'DATA_TOKEN'
        finally:
            os.unlink(config_path)
    
    def test_data_provider_disabled_check(self):
        """Test provider behaviour when disabled."""
        config = self.get_standard_config()
        config['providers']['data']['enabled'] = False
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            
            with pytest.raises(RuntimeError, match="Data provider is disabled"):
                provider.read("test_id")
                
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'DATA_TOKEN': 'test-token'})
    def test_data_provider_read_operation(self):
        """Test data provider read operation."""
        config = self.get_standard_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            result = provider.read("test_resource_123")
            
            assert result['id'] == 'test_resource_123'
            assert result['type'] == 'data_resource'
            assert 'Simulated data' in result['data']
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'DATA_TOKEN': 'test-token'})
    def test_data_provider_search_operation(self):
        """Test data provider search operation."""
        config = self.get_standard_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            results = provider.search("test query", limit=2)
            
            assert len(results) <= 2
            assert all('search_result' in result['type'] for result in results)
            
        finally:
            os.unlink(config_path)
    
    def test_data_provider_operation_not_allowed(self):
        """Test operation not in allowlist."""
        config = self.get_standard_config()
        config['providers']['data']['allowedOperations'] = ['read']  # Remove search
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            
            with pytest.raises(ValueError, match="Search operation not allowed"):
                provider.search("test query")
                
        finally:
            os.unlink(config_path)
    
    def test_data_provider_missing_auth(self):
        """Test provider behaviour without authentication."""
        config = self.get_standard_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            
            # No DATA_TOKEN environment variable set
            with pytest.raises(RuntimeError, match="Authentication failed"):
                provider.read("test_id")
                
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'DATA_TOKEN': 'test-token'})
    def test_data_provider_rate_limiting(self):
        """Test rate limiting functionality."""
        config = self.get_standard_config()
        config['providers']['data']['rateLimits']['requestsPerMinute'] = 1
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            
            # First request should succeed
            provider.read("test_1")
            
            # Second request should be rate limited
            with pytest.raises(ValueError, match="Rate limit exceeded"):
                provider.read("test_2")
                
        finally:
            os.unlink(config_path)


class TestGitProvider:
    """Test cases for GitProvider."""
    
    def create_test_config(self, config_data: dict) -> str:
        """Create a temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_git_config(self) -> dict:
        """Get git provider test configuration."""
        return {
            'security': {
                'defaultPolicy': 'deny',
                'authenticationRequired': True,
                'auditLogging': True,
                'secretRedaction': True
            },
            'providers': {
                'git': {
                    'enabled': True,
                    'endpoint': 'https://api.github.com',
                    'authentication': {
                        'type': 'token',
                        'envVariable': 'GITHUB_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 20,
                        'requestsPerHour': 500
                    },
                    'allowedOperations': ['read', 'search', 'list'],
                    'repositoryAllowlist': [
                        'SPECTRADataSolutions/test-repo',
                        'SPECTRADataSolutions/another-repo'
                    ]
                }
            }
        }
    
    def test_git_provider_initialization(self):
        """Test GitProvider initialization."""
        config = self.get_git_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = GitProvider(config_path)
            assert len(provider.repository_allowlist) == 2
            assert 'SPECTRADataSolutions/test-repo' in provider.repository_allowlist
        finally:
            os.unlink(config_path)
    
    def test_git_provider_repository_allowlist_validation(self):
        """Test repository allowlist enforcement."""
        config = self.get_git_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = GitProvider(config_path)
            
            # Allowed repository
            assert provider._validate_repository_access('SPECTRADataSolutions/test-repo') is True
            
            # Not allowed repository
            assert provider._validate_repository_access('other-org/repo') is False
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test-token'})
    def test_git_provider_read_repository(self):
        """Test reading repository information."""
        config = self.get_git_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = GitProvider(config_path)
            result = provider.read_repository('SPECTRADataSolutions/test-repo')
            
            assert result['full_name'] == 'SPECTRADataSolutions/test-repo'
            assert result['owner'] == 'SPECTRADataSolutions'
            assert result['name'] == 'test-repo'
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'test-token'})
    def test_git_provider_repository_access_denied(self):
        """Test access denied for non-allowlisted repository."""
        config = self.get_git_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = GitProvider(config_path)
            
            with pytest.raises(ValueError, match="Access denied to repository"):
                provider.read_repository('external-org/repo')
                
        finally:
            os.unlink(config_path)
    
    def test_git_provider_write_operations_blocked(self):
        """Test that write operations are blocked in configuration."""
        config = self.get_git_config()
        config['providers']['git']['allowedOperations'].append('push')  # Add write operation
        config_path = self.create_test_config(config)
        
        try:
            with pytest.raises(ValueError, match="Git provider must be read-only"):
                GitProvider(config_path)
                
        finally:
            os.unlink(config_path)


class TestTicketingProvider:
    """Test cases for TicketingProvider."""
    
    def create_test_config(self, config_data: dict) -> str:
        """Create a temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_ticketing_config(self) -> dict:
        """Get ticketing provider test configuration."""
        return {
            'security': {
                'defaultPolicy': 'deny',
                'authenticationRequired': True,
                'auditLogging': True,
                'secretRedaction': True
            },
            'providers': {
                'ticketing': {
                    'enabled': True,
                    'endpoint': 'https://ticketing.test.com/api',
                    'authentication': {
                        'type': 'api-key',
                        'envVariable': 'TICKETING_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 10,
                        'requestsPerHour': 200
                    },
                    'allowedOperations': ['read', 'search', 'list', 'create'],
                    'projectAllowlist': ['TEST-001', 'PROJ-002']
                }
            }
        }
    
    def test_ticketing_provider_initialization(self):
        """Test TicketingProvider initialization."""
        config = self.get_ticketing_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = TicketingProvider(config_path)
            assert len(provider.project_allowlist) == 2
            assert 'TEST-001' in provider.project_allowlist
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'TICKETING_TOKEN': 'test-token'})
    def test_ticketing_provider_read_ticket(self):
        """Test reading ticket information."""
        config = self.get_ticketing_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = TicketingProvider(config_path)
            result = provider.read_ticket('TEST-001', 'TICKET-123')
            
            assert result['project'] == 'TEST-001'
            assert result['id'] == 'TICKET-123'
            assert result['key'] == 'TEST-001-TICKET-123'
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'TICKETING_TOKEN': 'test-token'})
    def test_ticketing_provider_project_access_denied(self):
        """Test access denied for non-allowlisted project."""
        config = self.get_ticketing_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = TicketingProvider(config_path)
            
            with pytest.raises(ValueError, match="Access denied to project"):
                provider.read_ticket('EXTERNAL-001', 'TICKET-123')
                
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'TICKETING_TOKEN': 'test-token'})
    def test_ticketing_provider_create_ticket(self):
        """Test creating a new ticket."""
        config = self.get_ticketing_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = TicketingProvider(config_path)
            
            ticket_data = {
                'summary': 'Test ticket',
                'description': 'Test description',
                'type': 'Task',
                'priority': 'Medium'
            }
            
            result = provider.create_ticket('TEST-001', ticket_data)
            
            assert result['project'] == 'TEST-001'
            assert result['summary'] == 'Test ticket'
            assert result['type'] == 'Task'
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'TICKETING_TOKEN': 'test-token'})
    def test_ticketing_provider_create_ticket_missing_fields(self):
        """Test creating ticket with missing required fields."""
        config = self.get_ticketing_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = TicketingProvider(config_path)
            
            # Missing required fields
            ticket_data = {
                'summary': 'Test ticket'
                # Missing description and type
            }
            
            with pytest.raises(ValueError, match="Missing required field"):
                provider.create_ticket('TEST-001', ticket_data)
                
        finally:
            os.unlink(config_path)


class TestProviderHealthChecks:
    """Test provider health check functionality."""
    
    def create_test_config(self, config_data: dict) -> str:
        """Create a temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_full_config(self) -> dict:
        """Get full configuration for all providers."""
        return {
            'security': {
                'defaultPolicy': 'deny',
                'authenticationRequired': True,
                'auditLogging': True,
                'secretRedaction': True
            },
            'providers': {
                'data': {
                    'enabled': False,  # Disabled for health check testing
                    'endpoint': 'https://data.test.com/api',
                    'authentication': {
                        'type': 'token',
                        'envVariable': 'DATA_TOKEN'
                    },
                    'rateLimits': {
                        'requestsPerMinute': 30,
                        'requestsPerHour': 1000
                    },
                    'allowedOperations': ['read', 'search', 'query']
                }
            },
            'monitoring': {
                'metricsEnabled': True,
                'healthChecks': {
                    'enabled': True,
                    'intervalSeconds': 60
                },
                'alerting': {
                    'errorThreshold': 0.05,
                    'latencyThreshold': 2000
                }
            }
        }
    
    def test_provider_status_reporting(self):
        """Test provider status reporting."""
        config = self.get_full_config()
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            status = provider.get_status()
            
            assert 'provider' in status
            assert 'enabled' in status
            assert 'endpoint' in status
            assert 'auth_configured' in status
            assert 'allowed_operations' in status
            assert 'rate_limits' in status
            
            # Should show as disabled
            assert status['enabled'] is False
            
        finally:
            os.unlink(config_path)
    
    def test_provider_environment_validation(self):
        """Test validation of environment variable configuration."""
        config = self.get_full_config()
        config['providers']['data']['enabled'] = True
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            status = provider.get_status()
            
            # Without DATA_TOKEN environment variable
            assert status['auth_configured'] is False
            
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'DATA_TOKEN': 'test-token'})
    def test_provider_with_authentication(self):
        """Test provider status with authentication configured."""
        config = self.get_full_config()
        config['providers']['data']['enabled'] = True
        config_path = self.create_test_config(config)
        
        try:
            provider = DataProvider(config_path)
            status = provider.get_status()
            
            # With DATA_TOKEN environment variable
            assert status['auth_configured'] is True
            
        finally:
            os.unlink(config_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])