---
paths:
  - "backend/app/**"
  - "docs/adr/**"
---

# Architecture Rules

These rules are non-negotiable. Violating them breaks core product invariants.

## Multi-Tenancy
- Every table with user/business data has `agency_id` FK
- JWT access tokens contain `agency_id` claim
- Every DB query filters by `agency_id` — no exceptions, including UPDATE and DELETE
- Agency isolation is application-level (not PostgreSQL RLS at MVP) — technical debt, tracked for post-MVP
- Super-admin role can access cross-agency data for platform operations

> **DML rule**: `agency_id` must appear in the WHERE clause of every UPDATE/DELETE, not just SELECTs.
> `session.execute(update(Model).where(Model.id == id).values(...))` is WRONG — add `Model.agency_id == agency_id`.

## Voice Call Flow (Retell.ai)
```
Agency clicks "Call" → POST /api/v1/calls
  → CallManager creates Call record (status: queued)
  → Loads ScreeningFlow + Questions
  → PromptBuilder builds system prompt
  → Creates/reuses Retell agent via API
  → Retell.ai makes phone call to candidate
  → Call ends → Retell fires webhook → POST /api/v1/webhooks/retell
  → WebhookService saves transcript
  → CandidateEvaluator scores with Claude (tool_use structured output)
  → Updates candidate status (qualified/disqualified)
  → Pushes results to ATS via ATSProvider
```

## Provider Architecture
- ATSProvider is an abstract base class (ABC) in `services/ats/interfaces.py`
- All ATS integrations implement ATSProvider — never call provider APIs directly
- ATSProviderFactory creates the right provider from ATSConnection
- Retell.ai client is a service wrapper in `services/voice_agent/retell_client.py`
- Evaluation uses Anthropic Claude via `services/evaluation/evaluator.py`

## Cost Awareness
- Log every Retell.ai call cost to `calls.cost_cents`
- Log every Claude evaluation cost (input_tokens, output_tokens) — applies to **all model tiers** (Haiku, Sonnet, Opus)
- Track usage per agency in `subscriptions.used_minutes`
- Use Claude Haiku for scoring where Opus/Sonnet isn't needed
- Use Anthropic prompt caching — structure prompts with stable prefix first

## Anthropic Model IDs (current as of 2026-04)
- Orchestration/architecture: `claude-opus-4-6`
- Evaluation + complex tasks: `claude-sonnet-4-6`
- Quick scoring/classification: `claude-haiku-4-5-20251001`

## Database (PostgreSQL 16)
- JSONB columns for flexible data: `voice_config`, `question_scores`, `ats_metadata`
- JSONB mutation: always reassign whole dict — SQLAlchemy ignores in-place changes
- Never use `::jsonb` cast with asyncpg — use `CAST(:param AS jsonb)`
- Transcripts and evaluation data: fine as JSONB (write-once, read-many)

## Redis (7.x)
- Used for: rate limiting, session cache, webhook deduplication
- Set eviction policy `allkeys-lru`
- Add TTL jitter (+-10%) to prevent thundering herd

## Deployment (Fly.io + Vercel)
- Backend: Fly.io with blue-green deployment
- Frontend: Vercel auto-deploy from git push to main
- Migrations: `alembic upgrade head` as Fly.io release command
