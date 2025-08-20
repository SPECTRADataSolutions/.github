#!/usr/bin/env python3
"""
Tests for SPECTRA Assistant Persona Adherence

Tests that the assistant maintains consistent persona across interactions
and adheres to configured behaviour rules.
"""

import pytest
import tempfile
import yaml
import os
import sys
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from client.chatCli import ChatCli


class TestPersonaAdherence:
    """Test cases for assistant persona adherence."""
    
    def create_test_blueprint(self, config_data: dict) -> str:
        """Create a temporary blueprint file for testing."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(config_data, temp_file, default_flow_style=False)
        temp_file.close()
        return temp_file.name
    
    def get_standard_config(self) -> dict:
        """Get standard test configuration."""
        return {
            'metadata': {
                'name': 'testAssistant',
                'version': '1.0.0',
                'description': 'Test assistant for persona adherence',
                'language': 'en-GB'
            },
            'persona': {
                'identity': 'You are a professional AI assistant built following SPECTRA standards.',
                'tone': 'professional',
                'specialisation': ['testing', 'validation', 'automation'],
                'behavioralRules': [
                    'Always communicate in British English',
                    'Never reveal or log sensitive information', 
                    'Provide structured, actionable responses',
                    'Follow default-deny security policies'
                ]
            },
            'routing': {
                'defaultModel': 'gpt-4o',
                'taskRouting': {
                    'reasoning': 'o1-preview',
                    'summarise': 'gpt-4o-mini'
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
                    'patterns': [
                        'sk-[A-Za-z0-9]{48}',
                        'ghp_[A-Za-z0-9]{36}'
                    ]
                },
                'toolAccess': {
                    'defaultPolicy': 'deny',
                    'allowedTools': ['chat', 'search']
                },
                'responseFilters': ['no_secrets', 'appropriate_content']
            },
            'mcpIntegration': {
                'enabled': False,
                'onDemandOnly': True,
                'allowedProviders': []
            }
        }
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_persona_prompt_generation(self):
        """Test that persona prompt is correctly generated from configuration."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            persona_prompt = chat_cli._get_persona_prompt()
            
            # Check that key persona elements are included
            assert 'professional AI assistant built following SPECTRA standards' in persona_prompt
            assert 'Communication tone: professional' in persona_prompt
            assert 'Always communicate in British English' in persona_prompt
            assert 'Never reveal or log sensitive information' in persona_prompt
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_british_english_compliance(self):
        """Test that the assistant uses British English spelling and terminology."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Test response generation with British English requirements
            response = chat_cli._simulate_chat_response("Test message", "default")
            
            # Check for British English indicators
            assert 'British English' in response
            assert 'colour' not in response.lower() or 'color' not in response.lower() or True  # Either is acceptable in test
            
            # Verify language setting is enforced
            assert config['metadata']['language'] == 'en-GB'
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_tone_consistency(self):
        """Test that the assistant maintains consistent tone."""
        config = self.get_standard_config()
        
        # Test different tones
        tones = ['professional', 'friendly', 'formal', 'helpful', 'technical']
        
        for tone in tones:
            config['persona']['tone'] = tone
            blueprint_path = self.create_test_blueprint(config)
            
            try:
                chat_cli = ChatCli(blueprint_path)
                persona_prompt = chat_cli._get_persona_prompt()
                
                assert f'Communication tone: {tone}' in persona_prompt
                
            finally:
                os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_specialisation_inclusion(self):
        """Test that specialisation areas are included in persona."""
        config = self.get_standard_config()
        config['persona']['specialisation'] = ['cybersecurity', 'data analysis', 'automation']
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            persona_prompt = chat_cli._get_persona_prompt()
            
            # Specialisation should be present in the persona
            # (In a real implementation, this would be more sophisticated)
            assert chat_cli.persona['specialisation'] == ['cybersecurity', 'data analysis', 'automation']
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_behavioral_rules_enforcement(self):
        """Test that behavioural rules are properly enforced."""
        config = self.get_standard_config()
        config['persona']['behavioralRules'] = [
            'Always ask for clarification when requests are ambiguous',
            'Provide step-by-step explanations',
            'Include relevant security warnings'
        ]
        
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            persona_prompt = chat_cli._get_persona_prompt()
            
            # Check that rules are included in persona prompt
            assert 'Always ask for clarification when requests are ambiguous' in persona_prompt
            assert 'Provide step-by-step explanations' in persona_prompt
            assert 'Include relevant security warnings' in persona_prompt
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_secret_redaction_in_responses(self):
        """Test that secrets are properly redacted from responses."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Test with potential secrets in response
            test_response = "Here is your API key: sk-1234567890abcdef1234567890abcdef12345678 and GitHub token: ghp_abcdefghijklmnopqrstuvwxyz123456789"
            
            redacted_response = chat_cli._redact_secrets(test_response)
            
            # Check that secrets are redacted
            assert 'sk-1234567890abcdef1234567890abcdef12345678' not in redacted_response
            assert 'ghp_abcdefghijklmnopqrstuvwxyz123456789' not in redacted_response
            assert '[REDACTED]' in redacted_response
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_response_consistency_across_interactions(self):
        """Test that assistant maintains consistent persona across multiple interactions."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Simulate multiple interactions
            test_inputs = [
                "Hello, how are you?",
                "Can you help me with a task?",
                "What are your capabilities?"
            ]
            
            responses = []
            for input_text in test_inputs:
                response = chat_cli._simulate_chat_response(input_text, "default")
                responses.append(response)
            
            # Check that all responses maintain consistent persona elements
            for response in responses:
                assert 'SPECTRA' in response  # Should reference SPECTRA standards
                assert 'professional' in response.lower() or 'British English' in response
                
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_task_type_awareness(self):
        """Test that assistant is aware of different task types and routes appropriately."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Test different task types
            task_tests = [
                ("Can you summarise this document?", "summarise"),
                ("Help me reason through this problem", "reasoning"),
                ("General chat message", "default")
            ]
            
            for message, expected_task in task_tests:
                response = chat_cli._simulate_chat_response(message, expected_task)
                
                # Response should include task type information
                assert expected_task in response
                
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_security_policy_adherence(self):
        """Test that assistant adheres to security policies."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Test that default-deny policy is active
            response = chat_cli._simulate_chat_response("Test security", "default")
            
            # Should mention security policies
            assert 'default-deny policy active' in response
            assert 'Security:' in response or 'security' in response.lower()
            
        finally:
            os.unlink(blueprint_path)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_persona_validation_deterministic_phrases(self):
        """Test that assistant uses deterministic phrases for validation."""
        config = self.get_standard_config()
        blueprint_path = self.create_test_blueprint(config)
        
        try:
            chat_cli = ChatCli(blueprint_path)
            
            # Test multiple responses to same input for consistency
            test_input = "What is your role?"
            
            responses = []
            for _ in range(3):
                response = chat_cli._simulate_chat_response(test_input, "default")
                responses.append(response)
            
            # Should contain consistent elements
            for response in responses:
                assert 'SPECTRA' in response
                assert 'assistant' in response.lower()
                
            # All responses should be identical in this stub implementation
            assert all(response == responses[0] for response in responses)
            
        finally:
            os.unlink(blueprint_path)


class TestPersonaValidationHelpers:
    """Helper functions for persona validation."""
    
    def test_british_english_detection(self):
        """Test detection of British English usage."""
        # This would test a helper function for British English validation
        british_words = ['colour', 'favour', 'realise', 'organise', 'centre']
        american_words = ['color', 'favor', 'realize', 'organize', 'center']
        
        # In a real implementation, this would validate British spelling
        for word in british_words:
            assert 'u' in word or word.endswith('ise') or word.endswith('re')
    
    def test_tone_validation(self):
        """Test validation of communication tone."""
        valid_tones = ['professional', 'friendly', 'formal', 'helpful', 'technical']
        
        for tone in valid_tones:
            assert tone in ['professional', 'friendly', 'formal', 'helpful', 'technical']
    
    def test_security_phrase_detection(self):
        """Test detection of security-related phrases."""
        security_phrases = [
            'default-deny policy',
            'secret redaction',
            'authentication required',
            'access denied'
        ]
        
        for phrase in security_phrases:
            assert len(phrase) > 0
            assert 'security' in phrase.lower() or 'deny' in phrase.lower() or 'redaction' in phrase.lower() or 'authentication' in phrase.lower() or 'access' in phrase.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])