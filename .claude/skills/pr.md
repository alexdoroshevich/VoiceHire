# /pr — Create a pull request with a fully filled description

Creates a PR from the current branch into main. ALWAYS fills in the description
using the project template — never leave fields empty or use placeholders.

## Steps

1. Gather context:
```bash
git branch --show-current
git log main..HEAD --oneline
git diff main..HEAD --stat
```

2. Read the PR template to get the exact structure:
```bash
cat .github/pull_request_template.md
```

3. Based on the commits and diff, write:
   - **Title**: under 70 chars, conventional commit format: `feat:`, `fix:`, `chore:`, `ci:`, etc.
   - **Body**: fill every section of the template with specific content about THIS change

4. Create the PR:
```bash
gh pr create \
  --base main \
  --title "<generated title>" \
  --body "$(cat <<'EOF'
<filled body here>
EOF
)"
```

## Rules

- Every field must be specific to THIS change — no generic placeholders
- Check boxes that apply with `[x]`, leave inapplicable ones unchecked `[ ]`
- After creating the PR, print the URL so the user can open it
