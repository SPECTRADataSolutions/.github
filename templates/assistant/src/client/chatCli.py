#!/usr/bin/env python3
"""
SPECTRA Chat CLI

Simple command-line interface for interacting with AI assistant, demonstrating
proper persona adherence, secret redaction, and context integration.
"""

import os
import sys
import yaml
import re
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from router.modelRouter import ModelRouter


class ChatCli:
    """
    Command-line interface for AI assistant with security and governance controls.
    
    Implements SPECTRA standards for secret redaction, persona adherence,
    and default-deny security policies.
    """
    
    def __init__(self, blueprint_path: str = "blueprint/assistantBlueprint.yaml"):
        """
        Initialise the chat CLI with blueprint configuration.
        
        Args:
            blueprint_path: Path to assistant blueprint YAML file
        """
        self.blueprint_path = Path(blueprint_path)
        self.config = self._load_blueprint()
        self.router = ModelRouter(blueprint_path)
        
        # Set up logging with minimal, structured output
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize persona and guardrails
        self.persona = self.config.get('persona', {})
        self.guardrails = self.config.get('guardrails', {})
        self.secret_patterns = self._compile_secret_patterns()
        
        # Validate required environment variables
        self._validate_environment()
        
    def _load_blueprint(self) -> Dict[str, Any]:
        """Load and validate blueprint configuration."""
        try:
            with open(self.blueprint_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            # Basic validation
            required_sections = ['metadata', 'persona', 'routing', 'guardrails']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Blueprint missing required section: {section}")
                    
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading blueprint: {e}")
            raise
            
    def _compile_secret_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for secret detection."""
        patterns = []
        secret_config = self.guardrails.get('secretRedaction', {})
        
        if secret_config.get('enabled', False):
            pattern_strings = secret_config.get('patterns', [])
            for pattern_str in pattern_strings:
                try:
                    patterns.append(re.compile(pattern_str, re.IGNORECASE))
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern '{pattern_str}': {e}")
                    
        return patterns
        
    def _validate_environment(self) -> None:
        """Validate required environment variables are present."""
        required_vars = ['OPENAI_API_KEY']
        
        # Check for context server tokens if enabled
        context_config = self.config.get('contextIntegration', {})
        if context_config.get('enabled', False):
            allowed_servers = context_config.get('allowedServers', [])
            for provider in allowed_providers:
                if provider == 'data':
                    required_vars.append('DATA_TOKEN')
                elif provider == 'git':
                    required_vars.append('GITHUB_TOKEN')
                elif provider == 'ticketing':
                    required_vars.append('TICKETING_TOKEN')
                    
        missing_vars = []
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
                
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            print("Please set these variables before running the assistant.")
            sys.exit(1)
            
    def _redact_secrets(self, text: str) -> str:
        """
        Redact potential secrets from text using configured patterns.
        
        Args:
            text: Input text that may contain secrets
            
        Returns:
            Text with secrets redacted
        """
        if not self.secret_patterns:
            return text
            
        redacted_text = text
        redaction_count = 0
        
        for pattern in self.secret_patterns:
            matches = pattern.findall(redacted_text)
            if matches:
                redaction_count += len(matches)
                redacted_text = pattern.sub('[REDACTED]', redacted_text)
                
        if redaction_count > 0:
            self.logger.warning(f"Redacted {redaction_count} potential secrets from text")
            
        return redacted_text
        
    def _get_persona_prompt(self) -> str:
        """Generate persona prompt from blueprint configuration."""
        identity = self.persona.get('identity', '')
        tone = self.persona.get('tone', 'professional')
        rules = self.persona.get('behavioralRules', [])
        
        prompt = f"{identity}\n\n"
        prompt += f"Communication tone: {tone}\n\n"
        
        if rules:
            prompt += "Behaviour rules:\n"
            for rule in rules:
                prompt += f"- {rule}\n"
                
        return prompt
        
    def _display_welcome(self) -> None:
        """Display welcome message with assistant information."""
        metadata = self.config.get('metadata', {})
        name = metadata.get('name', 'Assistant')
        description = metadata.get('description', 'AI Assistant')
        
        print("🤖 SPECTRA AI Assistant")
        print("=" * 40)
        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"Language: {metadata.get('language', 'en-GB')}")
        print(f"Version: {metadata.get('version', '1.0.0')}")
        print()
        print("Type 'help' for commands, 'exit' to quit.")
        print("=" * 40)
        print()
        
    def _display_help(self) -> None:
        """Display available commands."""
        print("📋 Available Commands:")
        print("  help     - Show this help message")
        print("  models   - Show available models and routing")
        print("  persona  - Display current persona configuration")
        print("  status   - Show system status and configuration")
        print("  exit     - Exit the assistant")
        print()
        print("💬 Chat:")
        print("  Simply type your message to chat with the assistant")
        print("  The assistant will route your request to the appropriate model")
        print()
        
    def _display_models(self) -> None:
        """Display available models and routing configuration."""
        models = self.router.get_available_models()
        print("🤖 Model Routing Configuration:")
        for task_type, model in models.items():
            print(f"  {task_type}: {model}")
        print()
        
    def _display_persona(self) -> None:
        """Display current persona configuration."""
        print("🎭 Assistant Persona:")
        print(f"  Identity: {self.persona.get('identity', 'Not defined')}")
        print(f"  Tone: {self.persona.get('tone', 'Not defined')}")
        
        specialisation = self.persona.get('specialisation', [])
        if specialisation:
            print("  Specialisation:")
            for spec in specialisation:
                print(f"    - {spec}")
                
        rules = self.persona.get('behavioralRules', [])
        if rules:
            print("  Behaviour Rules:")
            for rule in rules:
                print(f"    - {rule}")
        print()
        
    def _display_status(self) -> None:
        """Display system status and configuration."""
        print("📊 System Status:")
        
        # Validate routing
        routing_valid = self.router.validate_routing_config()
        print(f"  Routing Configuration: {'✅ Valid' if routing_valid else '❌ Invalid'}")
        
        # Check environment variables (without exposing values)
        env_vars = ['OPENAI_API_KEY', 'DATA_TOKEN', 'GITHUB_TOKEN', 'TICKETING_TOKEN']
        print("  Environment Variables:")
        for var in env_vars:
            status = "✅ Set" if os.environ.get(var) else "❌ Missing"
            print(f"    {var}: {status}")
            
        # Context integration status
        context_config = self.config.get('contextIntegration', {})
        context_enabled = context_config.get('enabled', False)
        print(f"  Context Integration: {'✅ Enabled' if context_enabled else '❌ Disabled'}")
        
        if context_enabled:
            servers = context_config.get('allowedServers', [])
            print(f"  Allowed Servers: {', '.join(servers) if servers else 'None'}")
            
        print()
        
    def _simulate_chat_response(self, user_input: str, task_type: str = "default") -> str:
        """
        Simulate a chat response (placeholder for actual AI integration).
        
        Args:
            user_input: User's input message
            task_type: Type of task for model routing
            
        Returns:
            Simulated response
        """
        # Route to appropriate model
        try:
            model = self.router.routeTaskModel(task_type)
            self.logger.info(f"Routed to model: {model}")
        except ValueError as e:
            return f"❌ Routing error: {e}"
            
        # Redact any secrets from user input (for logging)
        safe_input = self._redact_secrets(user_input)
        self.logger.info(f"Processing user request (length: {len(user_input)} chars)")
        
        # Simulate response based on persona
        persona_prompt = self._get_persona_prompt()
        
        # This is a placeholder - in a real implementation, you would:
        # 1. Send persona_prompt + user_input to the selected model
        # 2. Get the actual AI response
        # 3. Apply response filters and redaction
        # 4. Return the filtered response
        
        response = f"""Thank you for your message. I'm operating as a SPECTRA AI assistant with the following characteristics:

- Model used: {model}
- Communication tone: {self.persona.get('tone', 'professional')}
- Language: British English
- Security: Secrets redacted, default-deny policy active

This is a template implementation. In a production system, this would connect to the actual AI model and provide a real response whilst maintaining all security and governance controls.

Your message length: {len(user_input)} characters
Task type: {task_type}"""

        return response
        
    def startChatLoop(self) -> None:
        """
        Start the interactive chat loop.
        
        Main entry point for the CLI application.
        """
        self._display_welcome()
        
        try:
            while True:
                try:
                    user_input = input("💬 You: ").strip()
                    
                    if not user_input:
                        continue
                        
                    # Handle commands
                    if user_input.lower() == 'exit':
                        print("👋 Goodbye!")
                        break
                    elif user_input.lower() == 'help':
                        self._display_help()
                        continue
                    elif user_input.lower() == 'models':
                        self._display_models()
                        continue
                    elif user_input.lower() == 'persona':
                        self._display_persona()
                        continue
                    elif user_input.lower() == 'status':
                        self._display_status()
                        continue
                        
                    # Handle chat
                    print("🤖 Assistant: ", end="")
                    
                    # Determine task type (simple heuristics for demo)
                    task_type = "default"
                    if any(word in user_input.lower() for word in ['summarise', 'summary']):
                        task_type = "summarise"
                    elif any(word in user_input.lower() for word in ['classify', 'categorise']):
                        task_type = "classify"
                    elif any(word in user_input.lower() for word in ['extract', 'find']):
                        task_type = "extract"
                    elif any(word in user_input.lower() for word in ['reason', 'think', 'analyse']):
                        task_type = "reasoning"
                        
                    response = self._simulate_chat_response(user_input, task_type)
                    
                    # Redact any secrets from response before displaying
                    safe_response = self._redact_secrets(response)
                    print(safe_response)
                    print()
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except EOFError:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    self.logger.error(f"Error processing input: {e}")
                    print(f"❌ Error: {e}")
                    
        except Exception as e:
            self.logger.error(f"Fatal error in chat loop: {e}")
            print(f"❌ Fatal error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the CLI application."""
    try:
        chat_cli = ChatCli()
        chat_cli.startChatLoop()
    except Exception as e:
        print(f"❌ Failed to start assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()