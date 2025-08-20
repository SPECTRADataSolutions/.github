# Testing Guide

This guide covers testing strategies, validation procedures, and quality assurance for your SPECTRA AI assistant implementation.

## 🧪 Testing Overview

SPECTRA AI assistants require comprehensive testing to ensure:
- Persona adherence and consistency
- Security and privacy compliance
- Model routing accuracy
- Provider integration reliability
- Performance and reliability standards

## 🏗️ Test Architecture

### Test Categories

**Unit Tests (`tests/test_*.py`)**
- Individual component testing
- Router logic validation
- Provider functionality
- Configuration parsing

**Integration Tests (`tests/integration/`)**
- End-to-end workflow testing
- Provider connectivity
- Cross-component interactions

**Persona Tests (`tests/test_persona.py`)**
- Identity consistency
- Tone validation
- British English compliance
- Behavioural rule adherence

**Security Tests**
- Secret redaction validation
- Access control verification
- Rate limiting enforcement
- Audit logging compliance

## 🚀 Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Set test environment variables
export OPENAI_API_KEY="test-key"
export DATA_TOKEN="test-token"      # Optional
export GITHUB_TOKEN="test-token"    # Optional
export TICKETING_TOKEN="test-token" # Optional
```

### Basic Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_router.py -v
pytest tests/test_persona.py -v
pytest tests/test_providers.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### CI/CD Testing
```bash
# Security scans
bandit -r src/ -f json -o security-report.json
safety check --json --output safety-report.json

# Blueprint validation
python scripts/validate_blueprint.py

# Provider health checks
python scripts/provider_health_check.py
```

## 🎭 Persona Testing

### Identity Consistency Tests
```python
def test_persona_identity_consistency():
    """Test that assistant maintains consistent identity."""
    # Multiple interactions should show same persona
    responses = []
    for prompt in test_prompts:
        response = assistant.respond(prompt)
        responses.append(response)
    
    # All responses should reference SPECTRA standards
    assert all('SPECTRA' in response for response in responses)
```

### Tone Validation
```python
def test_communication_tone():
    """Test that assistant maintains configured tone."""
    assistant = create_assistant(tone='professional')
    response = assistant.respond("Hello")
    
    # Should demonstrate professional tone
    assert validate_professional_tone(response)
```

### British English Compliance
```python
def test_british_english_usage():
    """Test British English spelling and terminology."""
    test_cases = [
        ("color", "colour"),
        ("realize", "realise"), 
        ("center", "centre"),
        ("elevator", "lift")
    ]
    
    for american, british in test_cases:
        response = assistant.respond(f"Tell me about {american}")
        assert british in response or american not in response
```

### Behavioural Rules Testing
```python
def test_behavioural_rules():
    """Test adherence to defined behavioural rules."""
    rules = assistant.get_behavioural_rules()
    
    for rule in rules:
        # Test rule implementation
        test_response = test_rule_adherence(rule)
        assert test_response.compliant
```

## 🔒 Security Testing

### Secret Redaction Tests
```python
def test_secret_redaction():
    """Test that secrets are properly redacted."""
    test_secrets = [
        "sk-1234567890abcdef1234567890abcdef12345678",  # OpenAI key
        "ghp_abcdefghijklmnopqrstuvwxyz123456789",       # GitHub token
        "user@example.com",                               # Email
    ]
    
    for secret in test_secrets:
        text_with_secret = f"Here is a secret: {secret}"
        redacted = assistant.redact_secrets(text_with_secret)
        assert secret not in redacted
        assert '[REDACTED]' in redacted
```

### Access Control Tests
```python
def test_default_deny_policy():
    """Test that default-deny policy is enforced."""
    # Attempt to use non-allowed tool
    result = assistant.use_tool("unauthorized_tool")
    assert result.error == "Tool not in allowlist"
    
    # Attempt to access non-allowed provider
    result = assistant.access_provider("unauthorized_provider")
    assert result.error == "Provider access denied"
```

### Rate Limiting Tests
```python
def test_rate_limiting():
    """Test that rate limits are enforced."""
    provider = DataProvider()
    
    # Make requests up to limit
    for i in range(provider.rate_limits.requests_per_minute):
        result = provider.read(f"test_{i}")
        assert result.success
    
    # Next request should be rate limited
    with pytest.raises(ValueError, match="Rate limit exceeded"):
        provider.read("rate_limited_request")
```

## 🔧 Model Routing Tests

### Task-Specific Routing
```python
def test_task_routing():
    """Test that tasks are routed to appropriate models."""
    test_cases = [
        ("reasoning", "o1-preview"),
        ("summarise", "gpt-4o-mini"),
        ("classify", "gpt-4o-mini"),
        ("default", "gpt-4o")
    ]
    
    router = ModelRouter()
    for task_type, expected_model in test_cases:
        model = router.routeTaskModel(task_type)
        assert model == expected_model
```

### Fallback Behaviour
```python
def test_routing_fallback():
    """Test fallback to default model for unknown tasks."""
    router = ModelRouter()
    
    unknown_tasks = ["unknown", "invalid", "new_task"]
    for task in unknown_tasks:
        model = router.routeTaskModel(task)
        assert model == router.routing_config['defaultModel']
```

## 🔌 Provider Testing

### Connectivity Tests
```python
def test_provider_connectivity():
    """Test provider endpoint connectivity."""
    providers = [DataProvider(), GitProvider(), TicketingProvider()]
    
    for provider in providers:
        status = provider.get_status()
        assert status['enabled'] is not None
        assert status['endpoint'] is not None
```

### Authentication Tests
```python
def test_provider_authentication():
    """Test provider authentication handling."""
    provider = DataProvider()
    
    # Without credentials
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(RuntimeError, match="Authentication failed"):
            provider.read("test")
    
    # With credentials
    with patch.dict(os.environ, {'DATA_TOKEN': 'test-token'}):
        result = provider.read("test")
        assert result is not None
```

### Allowlist Enforcement
```python
def test_repository_allowlist():
    """Test git provider repository allowlist."""
    provider = GitProvider()
    
    # Allowed repository
    assert provider._validate_repository_access("SPECTRADataSolutions/allowed-repo")
    
    # Blocked repository
    assert not provider._validate_repository_access("external-org/repo")
```

## 📊 Performance Testing

### Response Time Tests
```python
def test_response_times():
    """Test that responses are within acceptable limits."""
    import time
    
    test_prompts = ["Hello", "Summarise this", "Help me reason"]
    
    for prompt in test_prompts:
        start_time = time.time()
        response = assistant.respond(prompt)
        response_time = time.time() - start_time
        
        assert response_time < 5.0  # 5 second limit
        assert len(response) > 0
```

### Memory Usage Tests
```python
def test_memory_constraints():
    """Test that memory usage stays within limits."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Process large context
    large_context = "test " * 10000
    response = assistant.respond(large_context)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Should not exceed reasonable limits
    assert memory_increase < 100 * 1024 * 1024  # 100MB limit
```

## 🤖 Integration Testing

### End-to-End Workflow
```python
def test_complete_workflow():
    """Test complete assistant workflow."""
    # Initialize assistant
    assistant = ChatCli()
    
    # Test persona loading
    assert assistant.persona is not None
    
    # Test model routing
    assert assistant.router.validate_routing_config()
    
    # Test provider status
    for provider in assistant.providers:
        status = provider.get_status()
        assert 'enabled' in status
    
    # Test chat interaction
    response = assistant._simulate_chat_response("Test message")
    assert len(response) > 0
    assert 'SPECTRA' in response
```

### Multi-Provider Integration
```python
def test_multi_provider_workflow():
    """Test workflow using multiple providers."""
    assistant = ChatCli()
    
    # Git provider workflow
    if assistant.git_provider.enabled:
        repos = assistant.git_provider.list_repositories("SPECTRADataSolutions")
        assert isinstance(repos, list)
    
    # Data provider workflow
    if assistant.data_provider.enabled:
        data = assistant.data_provider.search("test query")
        assert isinstance(data, list)
```

## 📋 Test Environment Setup

### Development Environment
```bash
# Set up test environment
export ENVIRONMENT=testing
export LOG_LEVEL=DEBUG

# Use test configurations
cp config/mcpConfig.test.yaml config/mcpConfig.yaml
cp blueprint/assistantBlueprint.test.yaml blueprint/assistantBlueprint.yaml
```

### Continuous Integration
```yaml
# .github/workflows/ci.yml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run Tests
        run: |
          pytest tests/ -v --cov=src
          bandit -r src/
          safety check
```

## 🔍 Test Validation Checklist

### Pre-Deployment Validation
- [ ] All unit tests pass
- [ ] Integration tests complete successfully
- [ ] Persona adherence validated
- [ ] Security tests pass
- [ ] Performance within limits
- [ ] Provider connectivity confirmed
- [ ] Configuration validation complete
- [ ] British English compliance verified
- [ ] Secret redaction working
- [ ] Rate limiting enforced

### Manual Testing
- [ ] Chat interface responsive
- [ ] Commands work correctly
- [ ] Error handling appropriate
- [ ] Logging functioning
- [ ] Documentation accurate

## 📚 Related Documentation

- [Persona Documentation](persona.md) - Assistant personality configuration
- [Usage Guide](usage.md) - Setup and operation instructions
- [Guardrails Documentation](guardrails.md) - Security and safety measures

---

*This testing guide ensures your SPECTRA AI assistant meets quality, security, and performance standards before deployment.*