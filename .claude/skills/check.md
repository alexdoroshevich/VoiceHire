# /check — Full type-check + lint pass

Runs ruff on the backend and TypeScript check on the frontend.

## Steps

1. Run backend ruff lint:
```bash
cd backend && python -m ruff check app/ 2>&1
```

2. Run frontend TypeScript check (when frontend exists):
```bash
cd frontend && npx tsc --noEmit 2>&1
```

3. Report: list all errors found. If clean, confirm "No type errors or lint warnings."

Do not fix errors unless the user explicitly asks — just report them.
