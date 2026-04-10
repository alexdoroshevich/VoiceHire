# /migrate — Apply database migrations

Checks and automatically applies all pending Alembic migrations.

## Steps

1. Show current state:
```bash
docker compose exec backend alembic current 2>&1
```

2. Show pending migrations:
```bash
docker compose exec backend alembic history --indicate-current 2>&1 | head -30
```

3. Apply all pending:
```bash
docker compose exec backend alembic upgrade head 2>&1
```

4. Confirm final state:
```bash
docker compose exec backend alembic current 2>&1
```

Report what was applied. If a migration fails, show the full error and diagnose.
