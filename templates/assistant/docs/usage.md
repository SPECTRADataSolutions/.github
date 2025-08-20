# Usage Guide

This guide explains how to set up, configure, and use your SPECTRA AI assistant effectively whilst maintaining security and compliance standards.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- SPECTRA organisational access
- Required environment variables configured

### Installation
```bash
# Clone your assistant repository
git clone https://github.com/SPECTRADataSolutions/your-assistant.git
cd your-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-openai-key"
export DATA_TOKEN="your-data-token"      # If using data provider
export GITHUB_TOKEN="your-github-token"  # If using git provider
export TICKETING_TOKEN="your-ticket-token" # If using ticketing provider
```

### First Run
```bash
# Start the chat interface
python src/client/chatCli.py

# Or run a quick test
python src/router/modelRouter.py
```

## ⚙️ Configuration

### Blueprint Configuration
Edit `blueprint/assistantBlueprint.yaml` to customise your assistant:

```yaml
metadata:
  name: yourAssistant         # Change to your assistant name
  description: "Your purpose" # Update description
  
persona:
  identity: "Your identity definition"
  tone: professional          # professional|friendly|formal|helpful|technical
  specialisation:
    - your-domain            # Update to your specialisations
    - your-expertise
```

### Context Server Configuration
Edit `config/contextConfig.yaml` to enable/disable context servers:

```yaml
contextServers:
  data:
    enabled: true            # Enable if you need data access
    # Configure authentication and rate limits
    
  git:
    enabled: false           # Enable if you need git access
    repositoryAllowlist:     # Add specific repositories
      - SPECTRADataSolutions/your-repo
      
  ticketing:
    enabled: false           # Enable if you need ticketing access
    projectAllowlist:        # Add specific projects
      - YOUR-PROJECT-001
```

## 💬 Using the Chat Interface

### Starting a Session
```bash
python src/client/chatCli.py
```

### Available Commands
```
help     - Show available commands
models   - Display model routing configuration
persona  - Show current persona settings
status   - System status and health checks
exit     - Exit the assistant
```

### Chat Examples

**General Conversation:**
```
You: Hello, how can you help me today?
Assistant: Hello! I'm your SPECTRA AI assistant...
```

**Task-Specific Routing:**
```
You: Can you summarise this document for me?
Assistant: [Routes to summarisation model]

You: Help me reason through this problem...
Assistant: [Routes to reasoning model]
```

**Provider Integration:**
```
You: Search for SPECTRA repositories
Assistant: [Uses git provider if enabled and configured]

You: Create a ticket for this issue
Assistant: [Uses ticketing provider if enabled]
```

## 🔧 Advanced Configuration

### Model Routing Customisation
Edit routing preferences in your blueprint:

```yaml
routing:
  defaultModel: gpt-4o              # Your preferred default
  taskRouting:
    reasoning: o1-preview           # Complex reasoning tasks
    summarise: gpt-4o-mini         # Text summarisation
    classify: gpt-4o-mini          # Classification tasks
    extract: gpt-4o-mini           # Information extraction
    semantic: text-embedding-3-large # Semantic search
```

### Memory Configuration
Configure context and memory handling:

```yaml
memory:
  contextWindow: 32000              # Token limit
  retentionPolicy: session          # Only session memory
  summaryThreshold: 1000            # When to summarise
```

### Security Guardrails
Customise security settings:

```yaml
guardrails:
  secretRedaction:
    enabled: true                   # Always keep enabled
    patterns:                       # Add custom secret patterns
      - 'your-custom-pattern'
      
  toolAccess:
    defaultPolicy: deny             # Always deny by default
    allowedTools:                   # Explicitly allowed tools
      - chat
      - search
      - your-tool
```

## 🔐 Environment Variables

### Required Variables
```bash
export OPENAI_API_KEY="sk-..."     # OpenAI API access
```

### Optional Provider Variables
```bash
export DATA_TOKEN="your-token"      # For data provider
export GITHUB_TOKEN="ghp_..."       # For git provider  
export TICKETING_TOKEN="your-key"   # For ticketing provider
```

### Security Best Practices
- Store secrets in secure secret management
- Use environment-specific configurations
- Rotate tokens regularly
- Monitor for accidental exposure

## 📊 Monitoring and Debugging

### Health Checks
```bash
# Check provider status
python src/providers/dataProvider.py
python src/providers/gitProvider.py
python src/providers/ticketingProvider.py

# Validate configuration
python scripts/validate_config.py
```

### Logging
View logs for debugging:
```bash
# Application logs
tail -f logs/assistant.log

# Security audit logs
tail -f logs/security.log
```

### Performance Monitoring
- Monitor response times
- Track model usage
- Review rate limit consumption
- Validate persona adherence

## 🚀 Deployment

### Local Development
```bash
# Run tests
pytest tests/ -v

# Check security
bandit -r src/
safety check

# Validate blueprint
python scripts/validate_blueprint.py
```

### CI/CD Pipeline
The included workflow provides:
- Blueprint validation
- Security scanning
- Unit and integration tests
- Deployment readiness checks

### Production Deployment
1. Configure production secrets
2. Enable appropriate providers
3. Set production rate limits
4. Monitor performance and security

## 🔧 Troubleshooting

### Common Issues

**Authentication Failures:**
```
Error: Authentication failed
Solution: Check environment variables are set correctly
```

**Rate Limit Exceeded:**
```
Error: Rate limit exceeded
Solution: Review provider configuration and usage patterns
```

**Blueprint Validation Errors:**
```
Error: Invalid blueprint
Solution: Validate YAML syntax and schema compliance
```

**Provider Connectivity Issues:**
```
Error: Provider unreachable
Solution: Check network connectivity and endpoint configuration
```

### Debug Mode
Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python src/client/chatCli.py
```

### Getting Help
1. Check logs for error details
2. Validate configuration files
3. Review provider status
4. Consult SPECTRA documentation
5. Contact the Innovation → assistantPlatform team

## 📚 Related Documentation

- [Persona Documentation](persona.md) - Configure assistant personality
- [Testing Guide](testing.md) - Validation and testing procedures  
- [Guardrails Documentation](guardrails.md) - Security and safety measures
- [SPECTRA Standards](https://github.com/SPECTRADataSolutions/.github) - Organisational standards

---

*This usage guide ensures you can effectively deploy and operate your SPECTRA AI assistant whilst maintaining security and compliance.*