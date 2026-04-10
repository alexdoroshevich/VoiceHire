# VoiceHire

Voice AI platform for staffing agencies — automates candidate screening calls with ATS integration.

## What It Does

VoiceHire automates the repetitive phone screening that staffing agencies perform daily. AI-powered voice calls handle structured candidate screening (availability, certifications, basic qualification checks) and sync results back to the agency's ATS.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.x async, PostgreSQL 16, Redis 7 |
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui, Zustand |
| Voice | Retell.ai |
| Evaluation | Anthropic Claude |
| Billing | Stripe |
| Deployment | Fly.io (backend), Vercel (frontend) |

## Development

```bash
# Clone
git clone https://github.com/alexdoroshevich/VoiceHire.git
cd VoiceHire

# Backend
cd backend
cp .env.example .env
pip install -e ".[dev]"

# Infrastructure
docker compose up -d postgres redis

# Run
uvicorn app.main:app --reload
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for code standards and PR process.

## Project Structure

```
VoiceHire/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/v1/    # Route handlers
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic request/response
│   │   └── services/  # Business logic
│   ├── alembic/       # Database migrations
│   └── tests/         # pytest test suite
├── frontend/          # Next.js application (planned)
├── .claude/           # Agent specs, rules, skills
├── .github/           # CI/CD workflows
└── docker-compose.yml
```

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

Proprietary. All rights reserved.
