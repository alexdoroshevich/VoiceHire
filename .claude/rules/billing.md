---
paths:
  - "backend/app/services/billing/**"
  - "backend/app/api/v1/billing.py"
  - "backend/app/api/v1/webhooks.py"
  - "backend/app/models/subscription.py"
---

# Billing Rules (Stripe)

## Subscription Model
- Tiered plans: trial, starter, professional, enterprise
- Metered billing based on call minutes used per billing period
- `subscriptions` table tracks: plan, status, included_minutes, used_minutes, overage_rate_cents
- Usage incremented after each call completes (from `calls.duration_seconds`)

## Stripe Integration Patterns
- `stripe.checkout.Session.create()` for initial subscription checkout
- `stripe.billing_portal.Session.create()` for self-service plan management
- `stripe.Subscription.retrieve()` for current plan status
- Usage reporting via `stripe.SubscriptionItem.create_usage_record()`

## Stripe Webhook Events (handle in webhooks.py)
- `checkout.session.completed` — new subscription created, activate agency plan
- `invoice.paid` — payment successful, reset used_minutes for new period
- `invoice.payment_failed` — payment failed, notify agency, grace period
- `customer.subscription.updated` — plan change (upgrade/downgrade)
- `customer.subscription.deleted` — cancellation, downgrade to trial/disabled

## Webhook Security
- ALWAYS verify webhook signature: `stripe.Webhook.construct_event(payload, sig_header, webhook_secret)`
- Never trust unverified webhook payloads
- Store raw events in `webhook_events` table for debugging
- Webhook processing must be idempotent — same event may fire multiple times

## Usage Enforcement
- Before initiating a call, check: `subscription.used_minutes < subscription.included_minutes` (or allow overage)
- If plan limit exceeded and no overage allowed: reject call with 402 Payment Required
- Track overage separately for billing: `overage_minutes = used_minutes - included_minutes`
- Grace period: allow calls to complete even if limit hit mid-call (charge overage after)

## Plan Limits

| Plan | Included Minutes | Overage | Notes |
|------|-----------------|---------|-------|
| trial | 30 | none | Auto-created on register, 14-day expiry |
| starter | configurable | per-minute | Entry-level paid plan |
| professional | configurable | per-minute | Most popular |
| enterprise | configurable | custom | Custom pricing |

## Never Do
- Never store Stripe secret key in code — env var `STRIPE_SECRET_KEY` only
- Never log full card numbers or payment method details
- Never skip webhook signature verification
- Never block call completion due to billing — charge overage after
- Never expose Stripe customer_id or subscription_id to frontend
