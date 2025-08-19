#!/usr/bin/env python3
"""
SPECTRA Model Router

Provides deterministic model routing based on task type, following the blueprint
configuration and SPECTRA governance standards.
"""

import yaml
import logging
from typing import Dict, Optional, Any
from pathlib import Path


class ModelRouter:
    """
    Routes tasks to appropriate models based on configuration and task type.
    
    Implements deterministic routing following SPECTRA blueprint specifications.
    """
    
    def __init__(self, blueprint_path: str = "blueprint/assistantBlueprint.yaml"):
        """
        Initialise the model router with blueprint configuration.
        
        Args:
            blueprint_path: Path to assistant blueprint YAML file
        """
        self.blueprint_path = Path(blueprint_path)
        
        # Set up logging with minimal output (no content logging)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.config = self._load_blueprint()
        self.routing_config = self.config.get('routing', {})
        
    def _load_blueprint(self) -> Dict[str, Any]:
        """Load and validate blueprint configuration."""
        try:
            with open(self.blueprint_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            # Basic validation
            if not isinstance(config, dict):
                raise ValueError("Blueprint must be a valid YAML object")
                
            if 'routing' not in config:
                raise ValueError("Blueprint missing required 'routing' section")
                
            return config
            
        except FileNotFoundError:
            self.logger.error(f"Blueprint file not found: {self.blueprint_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in blueprint: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading blueprint: {e}")
            raise
    
    def routeTaskModel(self, task_type: str, task_content: Optional[str] = None) -> str:
        """
        Route a task to the appropriate model based on task type.
        
        Args:
            task_type: Type of task (e.g., 'reasoning', 'summarise', 'classify')
            task_content: Task content (not logged for security)
            
        Returns:
            Model name to use for the task
            
        Raises:
            ValueError: If task_type is invalid or no routing found
        """
        if not task_type:
            raise ValueError("task_type cannot be empty")
            
        # Sanitise task_type for logging (no content)
        safe_task_type = str(task_type).lower().strip()
        
        # Get routing configuration
        task_routing = self.routing_config.get('taskRouting', {})
        default_model = self.routing_config.get('defaultModel')
        
        # Route based on task type
        if safe_task_type in task_routing:
            model = task_routing[safe_task_type]
            self.logger.info(f"Routed task type '{safe_task_type}' to model '{model}'")
            return model
            
        # Fall back to default model
        if default_model:
            self.logger.info(f"Using default model '{default_model}' for task type '{safe_task_type}'")
            return default_model
            
        # No routing found
        self.logger.error(f"No routing configuration found for task type '{safe_task_type}'")
        raise ValueError(f"No model routing configured for task type: {safe_task_type}")
    
    def get_available_models(self) -> Dict[str, str]:
        """
        Get all available models and their assigned task types.
        
        Returns:
            Dictionary mapping task types to model names
        """
        models = {}
        
        # Add default model
        default_model = self.routing_config.get('defaultModel')
        if default_model:
            models['default'] = default_model
            
        # Add task-specific models
        task_routing = self.routing_config.get('taskRouting', {})
        models.update(task_routing)
        
        return models
    
    def validate_routing_config(self) -> bool:
        """
        Validate that routing configuration is complete and consistent.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check required sections exist
            if 'defaultModel' not in self.routing_config:
                self.logger.error("Missing required 'defaultModel' in routing configuration")
                return False
                
            if 'taskRouting' not in self.routing_config:
                self.logger.error("Missing required 'taskRouting' in routing configuration")
                return False
                
            # Validate model names are strings
            default_model = self.routing_config['defaultModel']
            if not isinstance(default_model, str) or not default_model.strip():
                self.logger.error("defaultModel must be a non-empty string")
                return False
                
            task_routing = self.routing_config['taskRouting']
            if not isinstance(task_routing, dict):
                self.logger.error("taskRouting must be a dictionary")
                return False
                
            for task_type, model in task_routing.items():
                if not isinstance(model, str) or not model.strip():
                    self.logger.error(f"Model for task type '{task_type}' must be a non-empty string")
                    return False
                    
            self.logger.info("Routing configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating routing configuration: {e}")
            return False


def main():
    """Example usage of the ModelRouter."""
    try:
        router = ModelRouter()
        
        # Validate configuration
        if not router.validate_routing_config():
            print("❌ Invalid routing configuration")
            return
            
        # Show available models
        models = router.get_available_models()
        print("🤖 Available Models:")
        for task_type, model in models.items():
            print(f"  {task_type}: {model}")
            
        # Example routing
        test_tasks = [
            "reasoning",
            "summarise", 
            "classify",
            "extract",
            "semantic",
            "unknown_task"
        ]
        
        print("\n🧭 Routing Examples:")
        for task in test_tasks:
            try:
                model = router.routeTaskModel(task)
                print(f"  {task} → {model}")
            except ValueError as e:
                print(f"  {task} → Error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()