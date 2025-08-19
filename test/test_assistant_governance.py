#!/usr/bin/env python3
"""
Tests for SPECTRA AI Assistant Governance Infrastructure

Tests that the governance infrastructure (schemas, templates, workflows)
functions correctly for AI assistant repositories.
"""

import pytest
import json
import yaml
import jsonschema
import tempfile
import os
from pathlib import Path


class TestAssistantGovernance:
    """Test assistant governance infrastructure."""
    
    def get_contracts_dir(self) -> Path:
        """Get path to contracts directory."""
        return Path(__file__).parent.parent / "contracts" / "assistant"
    
    def get_template_dir(self) -> Path:
        """Get path to assistant template directory."""
        return Path(__file__).parent.parent / "templates" / "assistant"
    
    def test_assistant_blueprint_schema_exists(self):
        """Test that assistant blueprint schema exists and is valid JSON."""
        schema_path = self.get_contracts_dir() / "assistantBlueprint.json"
        assert schema_path.exists(), "Assistant blueprint schema missing"
        
        with open(schema_path, 'r') as f:
            schema = json.load(f)
            
        # Validate it's a valid JSON Schema
        assert '$schema' in schema
        assert 'type' in schema
        assert schema['type'] == 'object'
        
    def test_mcp_config_schema_exists(self):
        """Test that MCP config schema exists and is valid JSON."""
        schema_path = self.get_contracts_dir() / "mcpConfig.json"
        assert schema_path.exists(), "MCP config schema missing"
        
        with open(schema_path, 'r') as f:
            schema = json.load(f)
            
        # Validate it's a valid JSON Schema
        assert '$schema' in schema
        assert 'type' in schema
        assert schema['type'] == 'object'
        
    def test_template_blueprint_validates(self):
        """Test that template blueprint validates against schema."""
        blueprint_path = self.get_template_dir() / "blueprint" / "assistantBlueprint.yaml"
        schema_path = self.get_contracts_dir() / "assistantBlueprint.json"
        
        assert blueprint_path.exists(), "Template blueprint missing"
        assert schema_path.exists(), "Blueprint schema missing"
        
        # Load blueprint and schema
        with open(blueprint_path, 'r') as f:
            blueprint = yaml.safe_load(f)
            
        with open(schema_path, 'r') as f:
            schema = json.load(f)
            
        # Validate blueprint against schema
        jsonschema.validate(blueprint, schema)
        
    def test_template_mcp_config_validates(self):
        """Test that template MCP config validates against schema."""
        config_path = self.get_template_dir() / "config" / "mcpConfig.yaml"
        schema_path = self.get_contracts_dir() / "mcpConfig.json"
        
        assert config_path.exists(), "Template MCP config missing"
        assert schema_path.exists(), "MCP config schema missing"
        
        # Load config and schema
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        with open(schema_path, 'r') as f:
            schema = json.load(f)
            
        # Validate config against schema
        jsonschema.validate(config, schema)
        
    def test_template_structure_complete(self):
        """Test that template has all required components."""
        template_dir = self.get_template_dir()
        
        required_files = [
            "blueprint/assistantBlueprint.yaml",
            "config/mcpConfig.yaml", 
            "src/router/modelRouter.py",
            "src/client/chatCli.py",
            "src/providers/dataProvider.py",
            "src/providers/gitProvider.py",
            "src/providers/ticketingProvider.py",
            "tests/test_router.py",
            "tests/test_persona.py",
            "tests/test_providers.py",
            "docs/persona.md",
            "docs/usage.md",
            "docs/testing.md",
            "docs/guardrails.md",
            ".github/workflows/ci.yml",
            ".spectra/metadata.yml",
            "requirements.txt",
            ".gitignore",
            "README.md"
        ]
        
        for file_path in required_files:
            full_path = template_dir / file_path
            assert full_path.exists(), f"Required template file missing: {file_path}"
            
    def test_template_security_compliance(self):
        """Test that template enforces security requirements."""
        blueprint_path = self.get_template_dir() / "blueprint" / "assistantBlueprint.yaml"
        config_path = self.get_template_dir() / "config" / "mcpConfig.yaml"
        
        # Load configurations
        with open(blueprint_path, 'r') as f:
            blueprint = yaml.safe_load(f)
            
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Check blueprint security
        guardrails = blueprint.get('guardrails', {})
        
        # Secret redaction must be enabled
        secret_redaction = guardrails.get('secretRedaction', {})
        assert secret_redaction.get('enabled') is True, "Secret redaction must be enabled"
        
        # Tool access must be default-deny
        tool_access = guardrails.get('toolAccess', {})
        assert tool_access.get('defaultPolicy') == 'deny', "Must use default-deny policy"
        
        # Check MCP config security
        security = config.get('security', {})
        required_security = {
            'defaultPolicy': 'deny',
            'authenticationRequired': True,
            'auditLogging': True,
            'secretRedaction': True
        }
        
        for setting, required_value in required_security.items():
            actual_value = security.get(setting)
            assert actual_value == required_value, f"Security setting {setting} must be {required_value}"
            
    def test_template_british_english_compliance(self):
        """Test that template enforces British English."""
        blueprint_path = self.get_template_dir() / "blueprint" / "assistantBlueprint.yaml"
        
        with open(blueprint_path, 'r') as f:
            blueprint = yaml.safe_load(f)
            
        metadata = blueprint.get('metadata', {})
        assert metadata.get('language') == 'en-GB', "Must use British English (en-GB)"
        
    def test_template_camelcase_compliance(self):
        """Test that template uses camelCase naming."""
        blueprint_path = self.get_template_dir() / "blueprint" / "assistantBlueprint.yaml"
        
        with open(blueprint_path, 'r') as f:
            blueprint = yaml.safe_load(f)
            
        # Check assistant name is camelCase
        name = blueprint.get('metadata', {}).get('name', '')
        assert name[0].islower() if name else False, "Assistant name must start with lowercase"
        assert '_' not in name and '-' not in name, "Assistant name must not contain underscores or hyphens"
        
    def test_organizational_structure_compliance(self):
        """Test that template follows organizational structure."""
        metadata_path = self.get_template_dir() / ".spectra" / "metadata.yml"
        
        assert metadata_path.exists(), "Organizational metadata missing"
        
        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)
            
        assert metadata.get('pillar') == 'Innovation', "Must be Innovation pillar"
        assert metadata.get('domain') == 'assistantPlatform', "Must be assistantPlatform domain"
        assert metadata.get('capabilities') == 'customAiAssistant', "Must be customAiAssistant capability"
        
    def test_reusable_workflow_exists(self):
        """Test that reusable validation workflow exists."""
        workflow_path = Path(__file__).parent.parent / "workflows" / "validate-assistant-blueprint.yml"
        
        assert workflow_path.exists(), "Reusable validation workflow missing"
        
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            
        # Check it's a reusable workflow
        assert 'workflow_call' in workflow.get('on', {}), "Must be a reusable workflow"
        
        # Check it has required jobs
        jobs = workflow.get('jobs', {})
        assert 'validate-assistant-config' in jobs, "Missing validation job"


class TestSchemaValidation:
    """Test schema validation functionality."""
    
    def create_test_blueprint(self, data: dict) -> str:
        """Create temporary blueprint for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_schema_path(self, schema_name: str) -> Path:
        """Get path to schema file."""
        return Path(__file__).parent.parent / "contracts" / "assistant" / f"{schema_name}.json"
    
    def test_blueprint_schema_validation_success(self):
        """Test valid blueprint passes validation."""
        schema_path = self.get_schema_path("assistantBlueprint")
        
        valid_blueprint = {
            'metadata': {
                'name': 'testAssistant',
                'version': '1.0.0', 
                'description': 'Test assistant',
                'language': 'en-GB'
            },
            'persona': {
                'identity': 'Test identity',
                'tone': 'professional',
                'specialisation': ['testing'],
                'behavioralRules': ['Test rule']
            },
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview'
                }
            },
            'memory': {
                'contextWindow': 32000,
                'retentionPolicy': 'session',
                'summaryThreshold': 1000
            },
            'guardrails': {
                'secretRedaction': {
                    'enabled': True,
                    'patterns': ['test-pattern']
                },
                'toolAccess': {
                    'defaultPolicy': 'deny',
                    'allowedTools': ['test-tool']
                },
                'responseFilters': ['test-filter']
            },
            'mcpIntegration': {
                'enabled': True,
                'onDemandOnly': True,
                'allowedProviders': ['data']
            }
        }
        
        blueprint_path = self.create_test_blueprint(valid_blueprint)
        
        try:
            # Load and validate
            with open(blueprint_path, 'r') as f:
                blueprint = yaml.safe_load(f)
                
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                
            jsonschema.validate(blueprint, schema)
            
        finally:
            os.unlink(blueprint_path)
            
    def test_blueprint_schema_validation_failure(self):
        """Test invalid blueprint fails validation."""
        schema_path = self.get_schema_path("assistantBlueprint")
        
        # Missing required fields
        invalid_blueprint = {
            'metadata': {
                'name': 'testAssistant'
                # Missing required fields
            }
        }
        
        blueprint_path = self.create_test_blueprint(invalid_blueprint)
        
        try:
            with open(blueprint_path, 'r') as f:
                blueprint = yaml.safe_load(f)
                
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                
            with pytest.raises(jsonschema.ValidationError):
                jsonschema.validate(blueprint, schema)
                
        finally:
            os.unlink(blueprint_path)
            
    def test_mcp_config_schema_validation(self):
        """Test MCP config schema validation."""
        schema_path = self.get_schema_path("mcpConfig")
        
        valid_config = {
            'metadata': {
                'version': '1.0.0',
                'environment': 'development',
                'lastUpdated': '2024-01-01T00:00:00Z'
            },
            'security': {
                'defaultPolicy': 'deny',
                'authenticationRequired': True,
                'auditLogging': True,
                'secretRedaction': True
            },
            'providers': {},
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
        
        config_path = self.create_test_blueprint(valid_config)
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                
            jsonschema.validate(config, schema)
            
        finally:
            os.unlink(config_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])