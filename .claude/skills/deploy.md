# /deploy — Deploy to staging or production

Deploys backend to Fly.io and frontend to Vercel.
Pass "staging" or "prod" as argument: `/deploy staging` or `/deploy prod`

## Steps

1. Run backend lint: `cd backend && ruff check app/`
2. Run backend tests: `cd backend && python -m pytest -x -q`
3. If either fails — stop and report errors. Do NOT deploy broken code.
4. If both pass:

**For staging:**
```bash
cd backend && flyctl deploy --config fly.toml --strategy bluegreen 2>&1
```

**For prod:**
```bash
cd backend && flyctl deploy --config fly.toml --app $FLY_APP_NAME --remote-only 2>&1
```

**Frontend**: Vercel auto-deploys from git push to main.

5. After deploy: hit the health endpoint to confirm it's live:
```bash
curl -s https://voicehire-api.fly.dev/health | jq .
```
