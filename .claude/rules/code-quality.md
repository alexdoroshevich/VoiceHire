---
paths:
  - "backend/**/*.py"
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
---

# Code Quality Rules

## Python
- Type hints on **all** functions — parameters and return types
- Docstrings on all public functions (one-liner minimum)
- Use `structlog` for all logging — never `print()`
- Never swallow exceptions silently — always log or re-raise
- Never log PII, transcripts, candidate answers, or API keys
- Allowed log fields: `call_id`, `agency_id`, `latency_ms`, `cost`, `error`, `provider`, `model`

## TypeScript
- Strict mode always enabled
- No `any` types — use proper interfaces or `unknown` with type guards
- Tailwind for styling — no inline styles or CSS modules
- Zustand for state management — no prop drilling beyond 2 levels

## Testing
- Every new file needs at minimum a smoke test
- Run `pytest -x -q` before declaring Python work done
- Run `npx tsc --noEmit` before declaring TypeScript work done
- Mark integration tests with `@pytest.mark.integration`

## Dependencies
- Never install packages not in the approved list without asking
- Python pins: see `pyproject.toml` version constraints
- Node: check `package.json` before adding anything

## Autonomous Operation — MANDATORY
- **Never ask permission** to run terminal commands, read files, explore directories
- Just do it — report results after, not before
- **Only ask before `git push`** — that is the single exception

## Git — MANDATORY WORKFLOW
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`
- Commit after every working feature — not after hours of accumulated work
- No single commit with 500+ changed lines — split into smaller commits
- Never commit `.env`, API keys, or secrets
- **Never push directly to `main` or `master`** — feature branch + PR always
- Branch guard hook enforces this — do not attempt to bypass

## Pre-push Verification — MANDATORY
Before every `git push`, verify:
1. **YAML syntax** — validate every new/modified `.github/workflows/*.yml`
2. **Action API compatibility** — verify input field names match the pinned version
3. **File path correctness** — trace every path in workflows
4. **Build output alignment** — verify deployment system finds output at correct location

## Pull Requests — MANDATORY
- **NEVER open a PR with empty or placeholder template fields**
- Every PR body must fill ALL fields in `.github/pull_request_template.md`
- Use `gh pr create --title "type: desc" --body "..."` to pre-fill body
