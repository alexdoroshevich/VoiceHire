# Database Conventions

## Stack
- PostgreSQL 16 (via Docker)
- SQLAlchemy 2.x async ORM (`AsyncSession`)
- Alembic for migrations
- Models in `backend/app/models/`
- DB session factory in `backend/app/database.py`

## Migration Rules
- Migration files: `backend/alembic/versions/<NNN>_<description>.py`
- Numbering: sequential (001, 002, ...). Current: 001 (initial schema)
- NEVER use `::jsonb` cast syntax with asyncpg — use `CAST(:param AS jsonb)`
- NEVER use `json.dumps()` inline in SQL — pass Python objects, let SQLAlchemy serialize
  EXCEPTION: seeded JSONB data in `op.execute()` bulk inserts needs `json.dumps()` explicitly
- Enum types: always `create_type=False, checkfirst=True` to avoid duplicate type errors
- Always test with `alembic upgrade head` before committing

## Key Tables (current schema)

| Table | Key columns | Notes |
|-------|------------|-------|
| `agencies` | `id UUID`, `name`, `slug` (unique), `plan`, `is_active`, `settings JSONB` | Tenant table |
| `users` | `id UUID`, `email` (unique), `hashed_password`, `role`, `agency_id FK`, `agency_role` | Multi-tenant users |
| `screening_flows` | `id UUID`, `agency_id FK`, `name`, `job_type`, `voice_config JSONB`, `pass_threshold` | Configurable flows |
| `screening_questions` | `id UUID`, `flow_id FK`, `text`, `question_type`, `position`, `is_knockout` | Ordered questions |
| `candidates` | `id UUID`, `agency_id FK`, `ats_candidate_id`, `phone`, `status` | Synced from ATS |
| `calls` | `id UUID`, `agency_id FK`, `candidate_id FK`, `retell_call_id` (unique), `status`, `cost_cents` | Call records |
| `call_transcripts` | `id UUID`, `call_id FK` (unique), `turns JSONB`, `raw_retell_transcript JSONB` | 1:1 with call |
| `candidate_evaluations` | `id UUID`, `call_id FK` (unique), `overall_score`, `passed`, `question_scores JSONB` | Post-call scoring |
| `ats_connections` | `id UUID`, `agency_id FK` (unique), `provider`, `credentials JSONB` (encrypted) | One per agency |
| `compliance_logs` | `id UUID`, `agency_id FK`, `call_id FK`, `event_type`, immutable | Audit trail |
| `subscriptions` | `id UUID`, `agency_id FK` (unique), `stripe_subscription_id`, `used_minutes` | Billing |
| `webhook_events` | `id UUID`, `source`, `event_type`, `payload JSONB`, `processed` | Debug events |

## ORM Patterns

```python
# Fetch single record with tenant check
result = await db.execute(
    select(Call).where(Call.id == call_id, Call.agency_id == agency_id)
)
call = result.scalar_one_or_none()
if call is None:
    raise HTTPException(status_code=404, detail="Call not found")

# Fetch list
result = await db.execute(
    select(Candidate).where(Candidate.agency_id == agency_id).order_by(Candidate.created_at)
)
candidates = result.scalars().all()

# Insert
obj = MyModel(agency_id=agency_id, ...)
db.add(obj)
await db.commit()
await db.refresh(obj)
```

## JSONB Update Pattern
SQLAlchemy doesn't detect in-place JSONB mutations. Always reassign:
```python
# WRONG — SQLAlchemy won't detect this change:
flow.voice_config["key"] = value

# CORRECT — reassign the whole dict:
updated = dict(flow.voice_config or {})
updated["key"] = value
flow.voice_config = updated
await db.commit()
```

## Redis
- Client: `backend/app/redis_client.py`
- Used for: rate limiting, webhook deduplication, cache
- Eviction policy: `allkeys-lru`
- Always set TTL on cache keys — add +-10% jitter

## Connection String
- Dev: `postgresql+asyncpg://voicehire:voicehire@localhost:5432/voicehire`
- Loaded from `DATABASE_URL` env var in `backend/app/config.py`
