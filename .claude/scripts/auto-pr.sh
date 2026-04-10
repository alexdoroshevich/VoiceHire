#!/usr/bin/env bash
# Auto-creates a GitHub PR after every `git push origin <branch>`.
# Fires as a PostToolUse hook on Bash. Reads hook JSON from stdin.
# Silently exits on any error — never blocks the push.

set -euo pipefail

# ── Parse the bash command that was just run ─────────────────────────────────
input=$(cat)
cmd=$(python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('tool_input', {}).get('command', ''))
except:
    print('')
" <<< "$input" 2>/dev/null || echo "")

# Only trigger on: git push origin <branch>
echo "$cmd" | grep -qE "git push origin" || exit 0

# Extract branch name (first non-flag word after "origin")
branch=$(echo "$cmd" | grep -oP "(?<=git push origin )[\w/._-]+" | head -1 || echo "")
[[ -z "$branch" || "$branch" =~ ^(main|master|HEAD)$ ]] && exit 0

# Give GitHub a moment to register the push
sleep 2

# Resolve repo root and cd there
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$repo_root"

# Skip if a PR already exists for this branch
gh pr view "$branch" --json number &>/dev/null 2>&1 && exit 0

# ── Build description from git log ───────────────────────────────────────────
commits=$(git log "origin/main..$branch" --format="- %s" 2>/dev/null | head -10)
[[ -z "$commits" ]] && commits="- See commit history for full details"

# Use the oldest commit subject as the PR title
title=$(git log "origin/main..$branch" --format="%s" 2>/dev/null | tail -1)
[[ -z "$title" ]] && title="$branch"

read -r -d '' body << 'BODY' || true
## What does this PR do?

COMMITS_PLACEHOLDER

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor / cleanup
- [ ] Docs / config only
- [ ] CI/CD

## Checklist (author)

- [ ] Code follows style guide (ruff / eslint pass locally)
- [ ] Type hints on all Python functions; no TypeScript `any`
- [ ] No `print()` or `console.log()` — using structlog / proper logger
- [ ] No PII, transcripts, or API keys in logs or comments
- [ ] New files have at least a smoke test
- [ ] `pytest -x -q` passes locally
- [ ] agency_id filter on every query touching business data
- [ ] Conventional commit prefix used (`feat:`, `fix:`, `chore:`, etc.)

## How to test

1. Review the diff above
2. Run tests locally before merging
3. Verify no regressions in affected areas

## Related issues / spec sections

N/A
BODY

# Substitute commit list into body
body="${body/COMMITS_PLACEHOLDER/$commits}"

# ── Create the PR ─────────────────────────────────────────────────────────────
pr_url=$(gh pr create \
    --title "$title" \
    --base main \
    --head "$branch" \
    --body "$body" 2>/dev/null) || exit 0

echo "{\"systemMessage\": \"PR auto-created: $pr_url — fill in checklist boxes and How to test steps before merging.\"}"
