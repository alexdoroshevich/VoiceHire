# /db — Inspect database state

Quick database inspection — counts, recent records, migration status.

## Steps

1. Migration status:
```bash
docker compose exec backend alembic current 2>&1
```

2. Row counts for key tables:
```bash
docker compose exec postgres psql -U voicehire -d voicehire -c "
SELECT
  (SELECT COUNT(*) FROM agencies) AS agencies,
  (SELECT COUNT(*) FROM users) AS users,
  (SELECT COUNT(*) FROM screening_flows) AS flows,
  (SELECT COUNT(*) FROM candidates) AS candidates,
  (SELECT COUNT(*) FROM calls) AS calls,
  (SELECT COUNT(*) FROM candidate_evaluations) AS evaluations,
  (SELECT COUNT(*) FROM compliance_logs) AS compliance_logs;
" 2>&1
```

3. Recent calls (last 5):
```bash
docker compose exec postgres psql -U voicehire -d voicehire -c "
SELECT id, status, duration_seconds, cost_cents, created_at
FROM calls ORDER BY created_at DESC LIMIT 5;
" 2>&1
```

Report the results clearly. Flag anything unusual.
