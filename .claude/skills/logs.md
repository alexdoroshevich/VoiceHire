# /logs — View recent backend errors

Shows the last 100 lines of backend Docker logs, filtered to errors and warnings.

## Steps

1. Show recent errors and warnings:
```bash
docker compose logs backend --tail=150 2>&1 | grep -E '"level": "(error|warning)"' | tail -30
```

2. Show last 20 lines unfiltered (for context):
```bash
docker compose logs backend --tail=20 2>&1
```

3. If the user provides a call ID, filter by it:
```bash
docker compose logs backend --tail=500 2>&1 | grep "<CALL_ID>" | tail -20
```

Summarize what errors you see and what they likely mean.
