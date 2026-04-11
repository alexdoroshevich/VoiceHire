---
paths:
  - "backend/app/api/**"
  - "backend/app/services/auth/**"
  - "backend/app/services/ats/**"
  - "frontend/lib/api.ts"
---

# Security Rules

## What Must NEVER Be Public / Committed

These are absolute rules. Violating any of them is a P0 incident.

### Secrets & Credentials
- Never commit `.env` files, API keys, or credentials
- Never hardcode secrets in source code — use environment variables
- Never log API keys, even partially — use structlog field filtering
- ATS credentials are Fernet-encrypted at rest (`ats_connection.credentials`)
- Retell.ai, Anthropic, Stripe, Twilio keys are in env vars only
- `.env.example` shows variable names but NEVER real values

### What Cannot Be Shared Publicly
- ATS provider credentials (Bullhorn OAuth tokens, Avionte API keys)
- Stripe secret keys, webhook signing secrets
- Retell.ai API keys and agent IDs
- Twilio auth tokens and phone numbers
- Database connection strings with passwords
- JWT secret keys
- Any candidate PII: names, phone numbers, emails, interview answers
- Call recordings, transcripts, evaluation scores
- Agency-specific settings or billing data
- Internal business strategy, pricing, cost calculations, margin data

### What Can Be Shared Publicly
- Project structure and architecture decisions (ADRs)
- API schema documentation (OpenAPI/Swagger — no real data)
- README, CONTRIBUTING, SECURITY policy
- CI/CD workflow configurations (no secrets in YAML)
- Database schema (model definitions, migrations — no data)
- Frontend component library code
- Open-source dependency list

## Data Protection
- Never log PII: no emails, names, phone numbers, transcripts, or candidate answers in logs
- Call recordings stored only via Retell.ai — never downloaded to our servers
- Transcripts stored in PostgreSQL JSONB — encrypted at rest via DB-level encryption
- Candidate data isolated by agency_id — mandatory on every query
- Compliance logs are immutable — append-only, never deleted

## Authentication
- JWT tokens with short expiry (access: 30min, refresh: 7 days via httpOnly cookie)
- bcrypt for password hashing (pinned `<4.0.0` for passlib compatibility)
- Account lockout after 5 failed login attempts (15-minute cooldown)
- All API endpoints require authentication except `/health` and `/api/v1/auth/*`
- CORS restricted to configured origins

## Multi-Tenant Data Isolation
- EVERY query that fetches agency data MUST filter by `agency_id`
- ID-based routes must verify ownership: load resource, check `resource.agency_id == current_user.agency_id`
- If not authorized: raise `HTTPException(status_code=404)` (not 403 — don't leak existence)
- Never return data from another agency, even in error messages

## Input Validation
- All user input validated through Pydantic schemas
- Phone numbers validated before passing to Retell.ai/Twilio
- ATS webhook payloads verified by signature before processing
- Stripe webhooks verified by `stripe.Webhook.construct_event()`
- Retell webhooks verified by signature header

## OWASP Awareness
- SQL injection: mitigated by SQLAlchemy ORM (never raw SQL)
- XSS: mitigated by React's default escaping + Next.js CSP headers
- CSRF: mitigated by JWT Bearer tokens (access) + httpOnly cookies (refresh)
- Bandit runs in CI for Python security scanning
- gitleaks runs in pre-commit for secret detection

## GitHub Actions Supply Chain Security
- **SHA pinning is the standard** — `@v4` tags are mutable and can be hijacked
- All actions pinned to full 40-char commit SHA with a version comment
- Dependabot configured to auto-PR action updates weekly — review before merging
- Never use `@master` or `@main` for third-party actions
