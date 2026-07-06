# Hermes Teams Integration Workflow

This document documents the complete Teams integration workflow that emerged during setup, providing a comprehensive reference for future Teams + Hermes deployments.

## Overview

This workflow captures the step-by-step process for deploying Microsoft Teams bot integration with Hermes Agent, including all configuration, troubleshooting, and deployment steps.

## Complete Setup Workflow

### Step 1: Teams CLI Installation

```bash
# Install Teams CLI globally
npm install -g @microsoft/teams.cli@preview --omit=optional

# Verify installation
which teams
# Result: /opt/homebrew/bin/teams
```

### Step 2: Teams Bot Creation

```bash
# Create a new Teams application (THIS SHOWS CLIENT SECRET ONCE - SAVE!)
teams app create --name "Hermes Agent"

# Expected output:
Teams App ID: 30f80ff1-b765-484c-b414-5b1bba7b39bc
Bot ID: 30f80ff1-b765-484c-b414-5b1bba7b39bc
CLIENT_ID=30f80ff1-b765-484c-b414-5b1bba7b39bc
CLIENT_SECRET=tt28Q~...ya-9  # ⚠️ CRITICAL - SAVE NOW
TENANT_ID=5f037968-9e5f-4cb1-b85f-f11f1d752a72

# Installation link for Teams users:
https://teams.microsoft.com/l/app/30f80ff1-b765-484c-b414-5b1bba7b39bc?installAppPackage=true&appTenantId=5f037968-9e5f-4cb1-b85f-f11f1d752a72
```

### Step 3: Cloudflared Tunnel Setup

```yaml
tunnel: bedwuttipong
credentials-file: /Users/Jeff/.cloudflared/4050aa12-b8e4-46d7-9d78-7cd9a00d9211.json
ingress:
  - hostname: bestwuttipong.dev
    service: http://localhost:3978
  - service: http_status:404
```

### Step 4: Teams Manifest Configuration

**File**: `manifest.json`
```json
{
  "id": "30f80ff1-b765-484c-b414-5b1bba7b39bc",
  "bots": [
    {
      "botId": "30f80ff1-b765-484c-b414-5b1bba7b39bc",
      "scopes": ["personal", "team", "groupchat"]
    }
  ],
  "configurableProperties": ["botId"]
}
```

### Step 5: Environment Configuration

**File**: `.hermes/.env`
```bash
# Teams Integration
TEAMS_CLIENT_ID=30f80ff1-b765-484c-b414-5b1bba7b39bc
TEAMS_CLIENT_SECRET=tt28Q~...ya-9
TEAMS_TENANT_ID=5f037968-9e5f-4cb1-b85f-f11f1d752a72
TEAMS_PORT=3978
TEAMS_APP_ID=30f80ff1-b765-484c-b414-5b1bba7b39bc
TEAMS_ALLOWED_USERS=
TEAMS_HOME_CHANNEL=
TEAMS_HOME_CHANNEL_NAME=

# Hermes Configuration
GATEWAY_PORT=3978
HERMES_PORT=9120
```

### Step 6: Teams App Installation

**Two Installation Methods**:

#### Method 1: Direct Teams Link (Recommended)
1. Open: `https://teams.microsoft.com/l/app/30f80ff1-b765-484c-b414-5b1bba7b39bc?installAppPackage=true&appTenantId=5f037968-9e5f-4cb1-b85f-f11f1d752a72`
2. Opens directly in Teams client
3. Install immediately
4. Send a test message to verify

#### Method 2: Dev Portal
1. Navigate to: `https://dev.teams.microsoft.com/apps/30f80ff1-b765-484c-b414-5b1bba7b39bc`
2. Use "Install" button
3. Review and accept permissions
4. Add to Teams

### Step 7: Teams Configuration in Hermes

**File**: `~/.hermes/profiles/<profile>/config.yaml`
```yaml
messaging:
  platforms:
    teams:
      enabled: true
      extra:
        client_id: "30f80ff1-b765-484c-b414-5b1bba7b39bc"
        client_secret: "tt28Q~...ya-9"
        tenant_id: "5f037968-9e5f-4cb1-b85f-f11f1d752a72"
        port: 3978
```

### Step 8: Complete Setup Script

**File**: `setup_hermes_teams.sh`

This script automates the entire setup process:
1. Configures Teams CLI settings
2. Creates manifest.json
3. Sets up environment variables
4. Prepares gateway configuration
5. Provides Teams installation links

**Usage**:
```bash
# Make executable
chmod +x setup_hermes_teams.sh

# Run setup (requires Hermes process exit)
./setup_hermes_teams.sh
```

## Key Challenges & Workarounds

### Gateway Management Issues
**Problem**: Cannot run gateway management commands from within Hermes process due to process inheritance.

**Solution**: Run gateway commands from separate shell outside Hermes:
```bash
# ❌ blocked from inside Hermes:
hermes gateway restart

# ✅ must run from outside:
launchctl kickstart -k "gui/$(id -u)/ai.hermes.gateway-smith"
```

### Environment Configuration
**Problem**: `hermes config set` with dotted keys may silently write to wrong paths.

**Solution**: Use `hermes config edit` for explicit configuration:
```bash
# Good: Use explicit editor for complex configs
hermes config edit

# For simple settings:
hermes config set "messaging.platforms.teams.enabled" true
```

### Teams Client Secret Management
**Critical Timing**: CLIENT_SECRET is only shown once during `teams app create`.

**Action**: Save the secret immediately and store securely in environment variables.

## Troubleshooting

### Common Issues

#### Gateway Crash with Token Errors
**Symptom**: `SecretRefResolutionError: Environment variable "OPENCLAW_GATEWAY_TOKEN" is missing or empty`

**Solution**: 
```bash
# Add to service env file
export OPENCLAW_GATEWAY_TOKEN='your-token'

# Then restart the gateway
launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway"
```

#### Teams Configuration Failures
**Symptom**: Bot responds with auth errors

**Solution**: Verify all three critical credentials:
```bash
TEAMS_CLIENT_ID
TEAMS_CLIENT_SECRET
TEAMS_TENANT_ID
```

#### Plugin Compilation Issues
**Symptom**: "expected ./dist/index.js, ./dist/index.mjs, ./dist/index.cjs"

**Solution**: Refer to "Plugin compilation debugging" section for TypeScript compilation fixes.

### Verification Commands
```bash
# Check service status
openclaw gateway status --deep

# Verify config syntax
python -m py_compile openclaw.json

# Test Teams configuration
hermes doctor --check teams

# Review setup logs
~/Smith/.hermes-profile/logs/gateway.log
```

## Key Insights for Future Deployments

1. **Process Isolation**: Gateway management commands require separate shell execution from within Hermes process.

2. **Critical Timing**: Teams CLIENT_SECRET must be captured and saved immediately.

3. **Two Installation Paths**: Teams link (direct) vs Dev Portal (manual) - use Teams link when possible.

4. **Cross-Platform Compatibility**: Script and config should work for both OpenClaw and native Hermes environments.

5. **Environment Variable Security**: Never commit TEAM_CLIENT_SECRET to version control.

## File Structure

```
/setup_hermes_teams.sh          # Automated setup script
hermes.env.teams                 # Environment variables template
manifest.json                   # Teams app configuration

# Hidden files (should not be committed)
/.hermes/.env                    # Hermes environment variables
/.cloudflared/                   # Cloudflared credentials
```

## Dependencies

### Required Software
- macOS or Linux system
- Node.js and npm
- Cloudflare account for tunnel creation
- Microsoft 365/Teams license for bot deployment

### Python Packages
- hermes_tools (for team configuration)
- teams CLI SDK

## Security Considerations

1. **Secret Storage**: Use environment variables, not plaintext files
2. **Access Control**: Restrict access to sensitive configuration files
3. **Credential Rotation**: Implement regular secret rotation for Teams client credentials
4. **Audit Trail**: Log all configuration changes and deployments

## Migration Guide

### From Manual Setup to Scripted Setup
1. Copy `setup_hermes_teams.sh` to target environment
2. Customize environment variables
3. Execute script: `./setup_hermes_teams.sh`
4. Verify Teams app installation

### Troubleshooting Common Issues
1. **Gateway not starting**: Check service status with `openclaw gateway status`
2. **Teams auth failures**: Verify client ID, secret, and tenant ID
3. **Tunnel connectivity**: Check Cloudflared service status
4. **Configuration errors**: Validate JSON syntax and required fields

## Maintenance

### Regular Checks
- Monitor gateway status weekly
- Validate Teams app permissions
- Check for credential expiration
- Review access logs for anomalies

### Updates
- Monitor Teams API changes
- Update script compatibility
- Review security best practices
- Update troubleshooting documentation

## Quick Start Summary

```bash
# 1. Prepare environment
chmod +x setup_hermes_teams.sh

# 2. Execute setup (after exiting Hermes)
./setup_hermes_teams.sh

# 3. Complete Teams installation
# Open Teams link and install app

# 4. Test configuration
Send a test message to your Teams bot
```

## References

- `references/agent-lifecycle.md` - Detailed agent lifecycle management
- `references/workspace-inspection.md` - Configuration verification procedures
- Hermes Agent Documentation - Teams platform integration
- Microsoft Teams Developer Documentation - Bot setup guidelines

## Need Help?

For additional support:
- Review troubleshooting section
- Check application logs
- Contact the OpenClaw support team
- Refer to referenced documentation

---

*This Teams integration workflow documentation is continually improved based on deployment experiences. Report any issues or suggestions for enhancement.*

Created: 2026-07-04
Last Updated: 2026-07-04
Version: 1.0