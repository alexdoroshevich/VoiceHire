# /test — Run the full test suite

Runs backend pytest and frontend vitest. Use after making changes to verify nothing is broken.

## Steps

1. Run backend tests (fast, stops on first failure):
```bash
cd backend && python -m pytest -x -q 2>&1 | head -60
```

2. Run frontend component tests (when frontend exists):
```bash
cd frontend && npm run test 2>&1 | tail -30
```

3. Report: show pass/fail counts and any failing test names with their error messages.

If tests fail, identify the root cause — don't just describe the error.
