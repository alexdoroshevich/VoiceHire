---
paths:
  - "backend/app/api/**"
  - "backend/app/schemas/**"
  - "frontend/lib/api.ts"
---

# API Conventions

## URL Structure
- All endpoints: `/api/v1/<resource>`
- Versioning is part of the path, not headers
- Plural nouns for collections: `/api/v1/calls`, `/api/v1/candidates`
- Sub-resources: `/api/v1/calls/{id}/transcript`, `/api/v1/screening-flows/{id}/questions`

## Authentication
- JWT Bearer token in `Authorization: Bearer <token>` header
- Get current user via `CurrentUser` dependency from `app.services.auth.dependencies`
- Get agency context via `CurrentAgencyId` dependency
- Public endpoints (no auth): `/health`, `/api/v1/auth/login`, `/api/v1/auth/register`, `/api/v1/auth/refresh`
- Webhook endpoints: signature-verified, no JWT auth

## Request / Response Schemas
- All request/response types defined in `backend/app/schemas/`
- Schemas use `pydantic` with `BaseModel`
- Response models always returned via `response_model=` on the route decorator
- Never return raw dicts — always use a typed schema
- IDs are always `UUID`, serialized as strings in JSON

## Error Handling
- Use `HTTPException(status_code=..., detail="human message")` for API errors
- Standard status codes:
  - 400 Bad Request — invalid input
  - 401 Unauthorized — missing/invalid token
  - 403 Forbidden — authenticated but not allowed (use sparingly, prefer 404)
  - 404 Not Found — resource doesn't exist OR belongs to another agency (never leak existence)
  - 409 Conflict — duplicate resource (e.g., email already registered)
  - 422 Unprocessable — validation logic error
  - 429 Too Many Requests — rate limited or account locked
  - 503 Service Unavailable — external API (Retell, Stripe, ATS) down

## Multi-Tenant Data Isolation
- EVERY query on agency data MUST filter by `agency_id`
- ID-based routes must verify tenant ownership: load resource, check `resource.agency_id == agency_id`
- If not owner: raise `HTTPException(status_code=404)` (not 403 — don't leak existence)

## Router Setup
Each router file follows this pattern:
```python
router = APIRouter(prefix="/api/v1/<resource>", tags=["<resource>"])
# Registered in backend/app/main.py via app.include_router(router)
```

## Async Pattern
- All route handlers are `async def`
- DB session via `db: Annotated[AsyncSession, Depends(get_db)]`
- Use `await db.execute(select(...))` + `.scalars().all()` or `.scalar_one_or_none()`
- Always `await db.commit()` after writes, `await db.refresh(obj)` to reload

## Webhook Endpoints
- Webhook routes do NOT require JWT auth
- Webhook routes MUST verify signatures (Retell, Stripe, Bullhorn)
- Raw webhook payloads saved to `webhook_events` table for debugging
- Webhook processing is idempotent — duplicate events are safe
