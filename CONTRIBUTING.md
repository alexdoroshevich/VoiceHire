# Contributing to VoiceHire

VoiceHire is a voice AI SaaS for staffing agencies. Before contributing, please read this document.

---

## Before You Start

1. **Check existing issues.** Search open issues before opening a new one.
2. **For significant changes:** Open an issue first to discuss the approach.
3. **Security issues:** See `SECURITY.md` — do NOT open a public issue.

---

## Development Setup

```bash
# Clone
git clone https://github.com/alexdoroshevich/VoiceHire.git
cd VoiceHire

# Backend
cd backend
cp .env.example .env        # fill in your API keys
pip install -e ".[dev]"

# Start infrastructure
docker compose up -d postgres redis

# Run migrations
alembic upgrade head

# Run backend
uvicorn app.main:app --reload

# Frontend (when available)
cd ../frontend
npm install
npm run dev

# Or: start everything with Docker
docker compose up
```

### Required API keys (for full functionality)
- `RETELL_API_KEY` — Retell.ai voice calls
- `ANTHROPIC_API_KEY` — Claude evaluation
- `STRIPE_SECRET_KEY` — Billing (optional for dev)

---

## Code Standards

### Python (backend)
- **Type hints on ALL functions.** Parameters and return types.
- **Docstrings on all public functions** (one-line minimum).
- **`structlog` for all logging.** Never `print()`. Never log PII.
- **`pytest -x -q` must pass** before opening a PR.
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`

### TypeScript (frontend)
- **Strict mode on.** No `any` types.
- `tsc --noEmit` must pass.
- `eslint` must pass with no errors.

### Multi-Tenancy
- Every query on business data MUST filter by `agency_id`.
- Test cross-tenant isolation for every resource endpoint.

### Tests
- Every new backend file needs at minimum a smoke test.
- Mark integration tests with `@pytest.mark.integration`.

---

## Pull Request Process

1. Create a feature branch: `feat/your-feature-name`
2. Make your changes + tests
3. Run `pytest -x -q` (backend)
4. Run `npm run type-check && npm run lint` (frontend, when available)
5. Open a PR filling ALL fields in the template

### PR review criteria
- [ ] Tests pass
- [ ] No `any` types introduced
- [ ] No PII logged
- [ ] `agency_id` filter on every query
- [ ] Follows existing patterns

---

## What We Won't Accept

- Stack changes (FastAPI -> Django, Next.js -> Remix, etc.)
- `console.log()` or `print()` debugging statements left in code
- Commits with `.env` files, API keys, or credentials
- Code that leaks data between agencies (missing tenant isolation)
- Skipping AI disclosure or consent in call flows

---

## Questions?

Open a GitHub Discussion or issue.
