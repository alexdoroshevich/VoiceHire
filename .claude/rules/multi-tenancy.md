---
paths:
  - "backend/app/api/**"
  - "backend/app/models/**"
  - "backend/app/services/**"
---

# Multi-Tenancy Rules

VoiceHire is a multi-tenant B2B SaaS. Agencies are the tenants.

## Core Principle
Every piece of business data belongs to exactly one agency.
Leaking data between agencies is a P0 security incident.

## Implementation
- Every model with business data has `agency_id: Mapped[uuid.UUID]` FK to `agencies.id`
- JWT access tokens include `agency_id` claim
- `CurrentAgencyId` dependency extracts agency_id from the authenticated user
- Route handlers receive agency_id and pass it to all queries

## Mandatory Query Pattern
```python
# CORRECT — always filter by agency_id
result = await db.execute(
    select(Call).where(Call.id == call_id, Call.agency_id == agency_id)
)

# WRONG — never fetch by ID alone
result = await db.execute(
    select(Call).where(Call.id == call_id)  # MISSING agency_id!
)
```

This filter applies to **all operations** — reads, updates, and deletes. Never perform a
write (UPDATE/DELETE) without first confirming `agency_id` ownership via the SELECT above.

## Exceptions (tables without agency_id)
- `webhook_events` — raw inbound events before routing to agency
- Platform-level admin tables (if any)

## Super Admin
- `UserRole.super_admin` can access cross-agency data
- Used for platform operations, not exposed to agency users
- Super admin endpoints live in `api/v1/admin.py`

## Testing
- Every resource endpoint test must include a cross-tenant access test
- Verify that agency A cannot read/modify agency B's data
- Verify 404 (not 403) when accessing another agency's resource
