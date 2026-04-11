---
paths:
  - "backend/app/services/voice_agent/**"
  - "backend/app/services/evaluation/**"
  - "backend/app/services/screening/**"
  - "backend/app/api/v1/calls.py"
  - "backend/app/api/v1/webhooks.py"
---

# Voice Agent Rules (Retell.ai)

## Call Lifecycle
1. Agency initiates call via POST /api/v1/calls
2. CallManager creates Call record (status: queued)
3. PromptBuilder compiles screening flow into system prompt
4. Retell.ai agent created/reused via HTTP API
5. Retell.ai makes the outbound phone call
6. Call plays: greeting -> AI disclosure -> consent check -> questions
7. On call end: Retell fires webhook to our server
8. Transcript saved, evaluation triggered asynchronously
9. Results pushed to ATS if connected

## Retell.ai Integration
- HTTP client wrapper in `services/voice_agent/retell_client.py`
- Agent config builder in `services/voice_agent/agent_config.py`
- System prompt builder in `services/voice_agent/prompt_builder.py`
- Never store Retell API key in code — environment variable only
- Call cost tracked in `calls.cost_cents`

## Screening Flow Engine
- Flows compiled to ordered question list with knockout rules
- Questions asked in `position` order
- Knockout questions: if answer fails criteria, call can end early
- Follow-up questions defined in `follow_up_config` JSONB
- Multiple question types: yes_no, open_ended, multiple_choice, availability, certification

## Post-Call Evaluation
- Claude evaluates each Q&A pair with structured tool_use output
- Overall score computed from weighted question scores
- Knockout detection: any knockout question failure = disqualified
- Evaluation saved to `candidate_evaluations` table
- Results include: overall_score, per-question scores, summary, pass/fail

## Batch Calling
- POST /api/v1/calls/batch initiates calls for multiple candidates
- Batch creates individual Call records, each queued independently
- Concurrent call limit per agency (configurable, default 5 simultaneous)
- Rate limiting: max N calls per minute per agency to avoid Retell.ai throttling
- Retry logic for failed calls: no_answer → retry up to 2x with configurable delay
- Voicemail detection: if voicemail, mark call as `voicemail` status, do not retry

## Compliance (TCPA, state laws, EU AI Act)
- AI disclosure MUST be played at start of every call
- Consent MUST be obtained and logged before proceeding
- Both events logged to `compliance_logs` (immutable)
- Candidate can terminate call at any time — logged as compliance event
- Recording consent separate from AI screening consent

### Compliance Event Types (ComplianceEventType enum)
- `ai_disclosure_played` — AI nature disclosed to candidate
- `consent_given` — candidate consented to screening
- `consent_refused` — candidate refused, call ends gracefully
- `recording_started` — call recording began
- `recording_stopped` — call recording ended
- `call_terminated_by_candidate` — candidate hung up or requested stop
- `data_deletion_requested` — candidate requested data deletion (GDPR)
- `tcpa_consent_verified` — prior TCPA consent confirmed before outbound call

### Applicable Laws
- TCPA: prior express consent required for automated outbound calls
- NYC Local Law 144: AI bias audit + notice to candidates (10 business days before)
- Illinois HB 3773: consent required before AI analyzes video/audio interviews
- EU AI Act: high-risk AI system classification for hiring, requires conformity assessment

## Never Do
- Never store call audio on our servers — Retell.ai manages recordings
- Never log transcript content — only call_id, duration, cost
- Never call a candidate without consent being logged
- Never skip AI disclosure — it's a legal requirement
- Never exceed agency concurrent call limit without explicit override
