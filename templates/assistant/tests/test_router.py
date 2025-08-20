#!/usr/bin/env python3
"""
Tests for SPECTRA Model Router

Tests routing logic, configuration validation, and error handling.
"""

import pytest
import tempfile
import yaml
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from router.modelRouter import ModelRouter


class TestModelRouter:
    """Test cases for ModelRouter class."""
    
    def create_test_blueprint(self, config_data: dict) -> str:
        """Create a temporary blueprint file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def test_valid_blueprint_loading(self):
        """Test loading a valid blueprint configuration."""
        config = {
            'metadata': {
                'name': 'testAssistant',
                'version': '1.0.0',
                'description': 'Test assistant',
                'language': 'en-GB'
            },
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini',
                    'classify': 'gpt-4o-mini'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            assert router.config is not None
            assert router.routing_config['defaultModel'] == 'gpt-4o'
        finally:
            os.unlink(blueprint_path)
    
    def test_missing_blueprint_file(self):
        """Test handling of missing blueprint file."""
        with pytest.raises(FileNotFoundError):
            ModelRouter("nonexistent_blueprint.yaml")
    
    def test_invalid_yaml_blueprint(self):
        """Test handling of invalid YAML content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        temp_file.write("invalid: yaml: content: [")
        temp_file.close()
        
        try:
            with pytest.raises(yaml.YAMLError):
                ModelRouter(temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_missing_routing_section(self):
        """Test handling of blueprint missing routing section."""
        config = {
            'metadata': {
                'name': 'testAssistant',
                'version': '1.0.0'
            }
            # Missing routing section
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            with pytest.raises(ValueError, match="Blueprint missing required 'routing' section"):
                ModelRouter(blueprint_path)
        finally:
            os.unlink(blueprint_path)
    
    def test_route_task_model_specific_tasks(self):
        """Test routing specific task types to appropriate models."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini',
                    'classify': 'gpt-4o-mini',
                    'extract': 'gpt-4o-mini',
                    'semantic': 'text-embedding-3-large'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            
            # Test specific task routing
            assert router.routeTaskModel('reasoning') == 'o1-preview'
            assert router.routeTaskModel('summarise') == 'gpt-4o-mini'
            assert router.routeTaskModel('classify') == 'gpt-4o-mini'
            assert router.routeTaskModel('extract') == 'gpt-4o-mini'
            assert router.routeTaskModel('semantic') == 'text-embedding-3-large'
            
        finally:
            os.unlink(blueprint_path)
    
    def test_route_task_model_default_fallback(self):
        """Test fallback to default model for unknown task types."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            
            # Test unknown task falls back to default
            assert router.routeTaskModel('unknown_task') == 'gpt-4o'
            assert router.routeTaskModel('general') == 'gpt-4o'
            
        finally:
            os.unlink(blueprint_path)
    
    def test_route_task_model_no_default(self):
        """Test error when no routing found and no default model."""
        config = {
            'routing': {
                'taskRouting': {
                    'reasoning': 'o1-preview'
                }
                # No defaultModel
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            
            # Should raise error for unknown task with no default
            with pytest.raises(ValueError, match="No model routing configured"):
                router.routeTaskModel('unknown_task')
                
        finally:
            os.unlink(blueprint_path)
    
    def test_route_task_model_empty_task_type(self):
        """Test error handling for empty task type."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {}
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            
            # Test empty task type
            with pytest.raises(ValueError, match="task_type cannot be empty"):
                router.routeTaskModel('')
                
            with pytest.raises(ValueError, match="task_type cannot be empty"):
                router.routeTaskModel(None)
                
        finally:
            os.unlink(blueprint_path)
    
    def test_get_available_models(self):
        """Test getting all available models."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            models = router.get_available_models()
            
            assert models['default'] == 'gpt-4o'
            assert models['reasoning'] == 'o1-preview'
            assert models['summarise'] == 'gpt-4o-mini'
            assert len(models) == 3
            
        finally:
            os.unlink(blueprint_path)
    
    def test_validate_routing_config_valid(self):
        """Test validation of valid routing configuration."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            assert router.validate_routing_config() is True
            
        finally:
            os.unlink(blueprint_path)
    
    def test_validate_routing_config_missing_default(self):
        """Test validation failure for missing default model."""
        config = {
            'routing': {
                'taskRouting': {
                    'reasoning': 'o1-preview'
                }
                # Missing defaultModel
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            assert router.validate_routing_config() is False
            
        finally:
            os.unlink(blueprint_path)
    
    def test_validate_routing_config_missing_task_routing(self):
        """Test validation failure for missing task routing."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o'
                # Missing taskRouting
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            assert router.validate_routing_config() is False
            
        finally:
            os.unlink(blueprint_path)
    
    def test_validate_routing_config_invalid_model_names(self):
        """Test validation failure for invalid model names."""
        config = {
            'routing': {
                'defaultModel': '',  # Empty string
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': None  # None value
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            assert router.validate_routing_config() is False
            
        finally:
            os.unlink(blueprint_path)
    
    def test_case_insensitive_task_routing(self):
        """Test that task routing handles case properly."""
        config = {
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini'
                }
            }
        }
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            router = ModelRouter(blueprint_path)
            
            # Test exact case
            assert router.routeTaskModel('reasoning') == 'o1-preview'
            
            # Test different cases should fall back to default
            # (since we convert to lowercase in the method)
            # Test different cases should match due to case-insensitive handling
            # (since we convert to lowercase in the method)
            assert router.routeTaskModel('REASONING') == 'o1-preview'  # Should match 'reasoning' key
            
        finally:
            os.unlink(blueprint_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])