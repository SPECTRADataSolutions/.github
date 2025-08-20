# Security Guardrails Documentation

This document outlines the comprehensive security measures, privacy controls, and safety guardrails implemented in your SPECTRA AI assistant.

## 🛡️ Security Overview

SPECTRA AI assistants implement defence-in-depth security with multiple layers:

- **Default-Deny Architecture**: All access blocked unless explicitly allowed
- **Secret Redaction**: Automatic detection and removal of sensitive data
- **Rate Limiting**: Protection against abuse and resource exhaustion
- **Audit Logging**: Comprehensive monitoring without content exposure
- **Provider Isolation**: Restricted access to external services
- **Session-Only Memory**: No persistent storage of conversations

## 🔐 Access Control Framework

### Default-Deny Policy
All tools, providers, and operations are blocked by default:

```yaml
guardrails:
  toolAccess:
    defaultPolicy: deny          # Block everything by default
    allowedTools:               # Explicit allowlist only
      - chat
      - search
      - approved-tool
```

**Implementation:**
- Every operation checks allowlist before execution
- Unknown tools/providers automatically rejected
- Access decisions logged for audit

### Authentication Requirements
All provider access requires valid authentication:

```yaml
security:
  authenticationRequired: true   # Mandatory for all providers
  
providers:
  data:
    authentication:
      type: token               # Supported: token, bearer, api-key
      envVariable: DATA_TOKEN   # Environment variable only
```

**Security Measures:**
- No hard-coded credentials in code
- Environment variable validation
- Token expiry and rotation support
- Authentication failures logged

## 🔍 Secret Detection and Redaction

### Automatic Pattern Detection
Built-in patterns detect common secret types:

```yaml
guardrails:
  secretRedaction:
    enabled: true              # Always enabled
    patterns:
      # OpenAI API keys
      - 'sk-[A-Za-z0-9]{48}'
      # GitHub tokens  
      - 'ghp_[A-Za-z0-9]{36}'
      # Generic API keys
      - '[Aa]pi[_-]?[Kk]ey[s]?[\s]*[=:]+[\s]*["\']?[A-Za-z0-9_-]{20,}["\']?'
      # Email addresses
      - '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
```

### Custom Pattern Support
Add organisation-specific patterns:

```yaml
guardrails:
  secretRedaction:
    patterns:
      - 'SPECTRA-[A-Z0-9]{16}'     # SPECTRA internal tokens
      - 'PROJ-[0-9]{6}-[A-Z]{4}'   # Project identifiers
      - 'aws_secret_[a-zA-Z0-9]+'  # AWS secrets
```

### Redaction Implementation
```python
def _redact_secrets(self, text: str) -> str:
    """Redact secrets using configured patterns."""
    redacted_text = text
    redaction_count = 0
    
    for pattern in self.secret_patterns:
        matches = pattern.findall(redacted_text)
        if matches:
            redaction_count += len(matches)
            redacted_text = pattern.sub('[REDACTED]', redacted_text)
            
    if redaction_count > 0:
        self.logger.warning(f"Redacted {redaction_count} potential secrets")
        
    return redacted_text
```

## ⚡ Rate Limiting and Resource Protection

### Provider-Specific Limits
Each provider has configurable rate limits:

```yaml
providers:
  data:
    rateLimits:
      requestsPerMinute: 30      # Per-minute limit
      requestsPerHour: 1000      # Hourly limit
      
  git:
    rateLimits:
      requestsPerMinute: 20      # Conservative for external APIs
      requestsPerHour: 500
```

### Enforcement Implementation
```python
def _check_rate_limits(self) -> bool:
    """Check if request is within rate limits."""
    now = datetime.now()
    
    # Clean old requests
    self.request_history = [
        req_time for req_time in self.request_history
        if now - req_time < timedelta(hours=1)
    ]
    
    # Check hourly limit
    if len(self.request_history) >= self.rate_limits.requests_per_hour:
        return False
        
    # Check minute limit
    recent_requests = [
        req_time for req_time in self.request_history
        if now - req_time < timedelta(minutes=1)
    ]
    
    return len(recent_requests) < self.rate_limits.requests_per_minute
```

### Rate Limit Response
When limits are exceeded:
- Request immediately rejected
- Error logged with timestamp
- Client receives clear error message
- No partial processing occurs

## 📊 Audit Logging and Monitoring

### Security Event Logging
All security-relevant events are logged:

```python
def _log_request(self, operation: str, success: bool, error: Optional[str] = None):
    """Log request for audit purposes (no content logged)."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "provider": self.provider_name,
        "operation": operation,
        "success": success,
        "rate_limit_remaining": self._get_rate_limit_status(),
        "user_id": self._get_anonymised_user_id()  # If available
    }
    
    if error:
        log_entry["error"] = error
        
    # Never log actual content or secrets
    self.security_logger.info(json.dumps(log_entry))
```

### Privacy-First Logging
**What is logged:**
- Operation types and outcomes
- Timing and performance metrics
- Error types and frequencies
- Rate limit consumption
- Authentication success/failure

**What is never logged:**
- User input content
- Assistant responses
- Secret values (redacted)
- Personal information
- Provider response content

### Monitoring Dashboards
```yaml
monitoring:
  metricsEnabled: true
  healthChecks:
    enabled: true
    intervalSeconds: 60
  alerting:
    errorThreshold: 0.05        # 5% error rate alert
    latencyThreshold: 2000      # 2-second response alert
```

## 🏗️ Provider Security Architecture

### Repository Allowlists (Git Provider)
Strict repository access control:

```yaml
providers:
  git:
    repositoryAllowlist:
      - SPECTRADataSolutions/public-repo
      - SPECTRADataSolutions/approved-project
    # All other repositories blocked
```

### Project Allowlists (Ticketing Provider)
Controlled project access:

```yaml
providers:
  ticketing:
    projectAllowlist:
      - PROJ-001
      - SPECTRA-MAIN
    # All other projects blocked
```

### Read-Only Enforcement
Git provider prevents write operations:

```python
def _validate_git_config(self):
    """Validate git provider is read-only."""
    allowed_ops = self.provider_config.get('allowedOperations', [])
    write_ops = {'push', 'commit', 'merge', 'delete', 'create', 'write'}
    
    if any(op in write_ops for op in allowed_ops):
        raise ValueError("Git provider must be read-only")
```

## 🔒 Memory and Data Handling

### Session-Only Memory
No persistent conversation storage:

```yaml
memory:
  retentionPolicy: session      # Only session memory allowed
  contextWindow: 32000          # Token limit
  summaryThreshold: 1000        # When to summarise (in memory only)
```

### Data Flow Security
```
User Input → Secret Redaction → Processing → Response Filtering → Output
     ↓              ↓                           ↓              ↓
Rate Check → Audit Log → Model Routing → Audit Log → Deliver
```

### Context Handling
- Context window limits enforced
- No conversation persistence across sessions
- Automatic summarisation when approaching limits
- Memory cleared on session end

## 🛡️ Response Filtering

### Content Validation
All responses undergo filtering:

```yaml
guardrails:
  responseFilters:
    - no_secrets              # Remove any leaked secrets
    - appropriate_content     # Content policy compliance
    - structured_output       # Maintain response structure
    - british_english        # Language compliance
```

### Filter Implementation
```python
def _apply_response_filters(self, response: str) -> str:
    """Apply response filters for security and compliance."""
    filtered_response = response
    
    # Secret redaction
    filtered_response = self._redact_secrets(filtered_response)
    
    # Content policy check
    filtered_response = self._validate_content_policy(filtered_response)
    
    # British English validation
    filtered_response = self._ensure_british_english(filtered_response)
    
    return filtered_response
```

## 🚨 Incident Response

### Security Alert Triggers
Automatic alerts for:
- Multiple authentication failures
- Rate limit violations
- Secret detection events
- Unusual access patterns
- Provider connectivity issues
- Configuration changes

### Alert Response Procedures
1. **Immediate**: Log security event with details
2. **Automated**: Block suspicious requests temporarily
3. **Notification**: Alert security team if configured
4. **Investigation**: Preserve audit logs for analysis
5. **Recovery**: Restore normal operation when safe

### Breach Response
In case of suspected security breach:
1. Immediately disable affected providers
2. Rotate all authentication tokens
3. Review audit logs for extent of access
4. Update security patterns if needed
5. Document incident and lessons learned

## 🔧 Configuration Security

### Immutable Security Settings
Core security settings cannot be overridden:

```python
def _validate_security_config(self):
    """Validate immutable security requirements."""
    security = self.config.get('security', {})
    
    # These settings are mandatory and cannot be changed
    required_settings = {
        'defaultPolicy': 'deny',
        'authenticationRequired': True,
        'auditLogging': True,
        'secretRedaction': True
    }
    
    for setting, required_value in required_settings.items():
        if security.get(setting) != required_value:
            raise ValueError(f"Security setting {setting} must be {required_value}")
```

### Configuration Validation
All configuration changes are validated:
- Schema compliance checking
- Security requirement enforcement  
- Provider capability verification
- Rate limit reasonableness
- Allowlist format validation

## 📋 Security Checklist

### Deployment Security Validation
- [ ] All providers use authentication
- [ ] Rate limits configured appropriately
- [ ] Secret patterns include organisation-specific types
- [ ] Default-deny policy enforced
- [ ] Audit logging enabled
- [ ] Memory policy set to session-only
- [ ] Response filters active
- [ ] Provider allowlists configured
- [ ] No hard-coded secrets in configuration
- [ ] Environment variables properly set

### Operational Security
- [ ] Regular token rotation schedule
- [ ] Audit log monitoring in place
- [ ] Security alert notifications configured
- [ ] Incident response procedures documented
- [ ] Security team contact information current
- [ ] Regular security configuration reviews

## 📚 Compliance and Standards

### SPECTRA Framework Compliance
- Framework is Law principle enforced
- British English requirements met
- camelCase naming conventions followed
- Default-deny security model implemented

### Privacy Compliance
- No persistent data storage
- Content redaction implemented
- Audit logs privacy-compliant
- User data handling documented

### Industry Standards
- OWASP security principles applied
- Principle of least privilege enforced
- Defence in depth architecture
- Secure by default configuration

## 📖 Related Documentation

- [Persona Documentation](persona.md) - Assistant personality and behaviour
- [Usage Guide](usage.md) - Setup and operation instructions
- [Testing Guide](testing.md) - Security testing procedures

---

*These security guardrails ensure your SPECTRA AI assistant operates safely, securely, and in compliance with organisational and regulatory requirements.*