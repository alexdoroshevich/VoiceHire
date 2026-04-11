# /seed-demo — Seed realistic demo data

Creates a demo agency with candidates, screening flows, calls, and evaluations
so the live demo shows a fully-populated dashboard.

## Steps

1. Check if demo agency exists:
```bash
docker compose exec postgres psql -U voicehire -d voicehire -c \
  "SELECT id, name FROM agencies WHERE slug = 'demo-agency';" 2>&1
```

2. If not exists, create via the API:
```bash
curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@voicehire.app","password":"CHANGE_ME_BEFORE_RUNNING","full_name":"Demo Recruiter","agency_name":"Demo Staffing Agency"}' | jq .
```

3. Run the seed script (if it exists):
```bash
docker compose exec backend python scripts/seed_demo.py 2>&1
```

4. Report: demo login credentials and what data was seeded.

Note: if seed_demo.py doesn't exist, tell the user we need to create it first.
