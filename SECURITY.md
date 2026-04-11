# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in VoiceHire, please **do not** open a public GitHub issue.

Instead:

1. Go to **[Security → Report a vulnerability](../../security/advisories/new)** on this repository (GitHub private advisory).
2. Include at minimum:
   - A clear description of the vulnerability
   - Steps to reproduce
   - Potential impact (what data or functionality is at risk)
   - Your GitHub handle (optional, for credit)

A maintainer will acknowledge your report within **48 hours** and work with you privately to validate and patch the issue before any public disclosure.

## Scope

The following are in scope:

- Authentication bypass or privilege escalation
- Multi-tenant data isolation failures (agency A accessing agency B data)
- Exposure of ATS credentials, API keys, or session tokens
- SQL injection, XSS, CSRF, or other OWASP Top 10 vulnerabilities
- Insecure storage or transmission of candidate PII
- Secrets or credentials leaked in logs, responses, or error messages
- Webhook signature verification bypass
- Compliance violations (missing AI disclosure, consent bypass)

## Out of Scope

- Denial-of-service attacks
- Issues in third-party dependencies (report to their maintainers directly)
- Vulnerabilities requiring physical access to the server
- Issues in Retell.ai, Stripe, or ATS provider platforms themselves

## Disclosure Policy

We follow [coordinated disclosure](https://docs.github.com/en/code-security/security-advisories/about-coordinated-disclosure-of-security-vulnerabilities). We ask that you give us reasonable time to patch before any public disclosure. We will credit reporters in the release notes unless they prefer to remain anonymous.
