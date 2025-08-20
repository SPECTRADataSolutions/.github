# SPECTRA AI Assistant Repository Template

This template provides the foundational structure for creating brand-agnostic, chat-ready AI assistants with proper governance, security, and SPECTRA compliance.

## 📁 Repository Structure

```
your-assistant/
├── blueprint/
│   └── assistantBlueprint.yaml     # Persona, routing, guardrails configuration
├── config/
│   └── mcpConfig.yaml              # MCP provider configuration
├── src/
│   ├── router/
│   │   └── modelRouter.py          # Model routing logic
│   ├── client/
│   │   └── chatCli.py              # CLI chat interface
│   └── providers/
│       ├── dataProvider.py        # Data MCP provider stub
│       ├── gitProvider.py         # Git MCP provider stub
│       └── ticketingProvider.py   # Ticketing MCP provider stub
├── tests/
│   ├── test_router.py              # Router unit tests
│   ├── test_persona.py             # Persona adherence tests
│   └── test_providers.py          # Provider integration tests
├── docs/
│   ├── persona.md                  # Persona documentation
│   ├── usage.md                    # Usage instructions
│   ├── testing.md                  # Testing guide
│   └── guardrails.md               # Security guardrails
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI/CD pipeline
├── .spectra/
│   └── metadata.yml               # Organisational metadata
├── .gitignore
├── requirements.txt                # Python dependencies
└── README.md
```

## 🎯 Key Features

- **Persona-driven**: Clear identity and behaviour rules loaded from YAML
- **Model routing**: Deterministic model selection based on task type
- **Default-deny security**: Explicit allow-list for tools and providers
- **MCP integration**: On-demand Model Context Protocol provider access
- **Secret safety**: Automatic redaction of tokens and sensitive data
- **British English**: Consistent language conventions throughout
- **SPECTRA compliance**: Follows organisational structure and governance

## 🚀 Quick Start

1. **Use Repository Factory**:
   ```
   /create-repo repoName=yourAssistant domain=assistantPlatform visibility=private templateRepo=SPECTRADataSolutions/assistant-template
   ```

2. **Configure Blueprint**: Edit `blueprint/assistantBlueprint.yaml` with your persona
3. **Set Secrets**: Configure `OPENAI_API_KEY` and provider tokens in GitHub secrets
4. **Test Locally**: Run `python src/client/chatCli.py` to test your assistant
5. **Deploy**: Push to trigger CI/CD pipeline

## 🛡️ Security Principles

- **No hard-coded secrets**: All credentials via environment variables
- **Default-deny policy**: Tools/providers blocked unless explicitly allowed  
- **Session-only memory**: No persistent storage of conversations
- **Audit logging**: All provider access logged (content redacted)
- **Rate limiting**: Built-in protection against abuse

## 📚 Documentation

Each assistant repository includes comprehensive documentation:

- **Persona definition**: Identity, tone, specialisation, behaviour rules
- **Usage guide**: Setup, configuration, deployment instructions  
- **Testing strategy**: Unit tests, integration tests, persona validation
- **Security guardrails**: Secret handling, access controls, monitoring

## 🔄 CI/CD Pipeline

Automated workflows provide:

- **Schema validation**: Blueprint and config validation against contracts
- **Secret scanning**: Detection of accidentally committed secrets
- **Persona adherence**: Automated testing of persona consistency
- **Provider health**: Validation of MCP provider connectivity
- **Security checks**: Dependency scanning and vulnerability assessment

## 🎨 Customisation

The template supports customisation whilst maintaining SPECTRA compliance:

- **Models**: Update routing configuration for different model preferences
- **Providers**: Add/remove MCP providers based on your needs
- **Persona**: Define unique identity and behaviour for your use case
- **Tools**: Extend allowed tools list with explicit approval process

## 🤝 Support

For template issues or questions:
1. Check existing [issues](https://github.com/SPECTRADataSolutions/.github/issues)
2. Review [SPECTRA documentation](https://github.com/SPECTRADataSolutions/.github/docs/)
3. Contact the Innovation → assistantPlatform team

---

*This template enforces Framework as Law principles and maintains consistency across all SPECTRA AI assistant implementations.*