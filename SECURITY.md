# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in GrowthOS, please report it responsibly.

### How to Report

1. **Do NOT open a public issue** for security vulnerabilities
2. Email your report to **security@melgateam.com** (or open a private security advisory on GitHub)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment** within 48 hours
- **Assessment** within 7 days
- **Fix timeline** communicated after assessment
- **Credit** in the changelog (unless you prefer anonymity)

## Security Design

GrowthOS is built with security-first principles:

- **No credentials in code** — All secrets via environment variables
- **Dry-run by default** — `GROWTHOS_DRY_RUN=true` prevents real API calls until explicitly disabled
- **Progressive autonomy** — Start in `supervised` mode, escalate trust gradually
- **Audit trail** — Every action logged to `.growthOS/audit/` with timestamps
- **Circuit breaker** — Automatic protection against cascading API failures
- **Path validation** — Obsidian vault operations prevent directory traversal
- **Safe subprocess execution** — Remotion rendering uses `exec` (not `shell`) to prevent injection
- **Rate limiting** — Per-platform token management prevents API abuse

## Scope

The following are in scope for security reports:

- Command injection via user input
- Path traversal in vault operations
- Credential leakage in logs or output
- Unauthorized API calls bypassing dry-run mode
- Privilege escalation in autonomy levels

## Out of Scope

- Vulnerabilities in third-party dependencies (report upstream)
- Issues requiring physical access to the machine
- Social engineering attacks
