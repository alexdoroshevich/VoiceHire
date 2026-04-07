# Build-to-Sell Strategy

*How to build VoiceHire with the goal of acquisition, not infinite operation.*

---

## The Goal

Build a focused vertical AI SaaS, grow it to $30K–$80K MRR, then sell it
to a strategic acquirer for 3–5x ARR ($1M–$5M). Not a billion-dollar exit —
a life-changing, realistic exit for a solo developer.

---

## What Makes a SaaS Company Acquirable

Acquirers pay for these things, in this order:

1. **Recurring revenue** — MRR > $30K is the threshold where strategic buyers
   start caring. Below that, it's "interesting project," not "acquisition."

2. **Low churn** — Monthly churn < 3% signals product-market fit and sticky
   workflows. Churn > 8% means the product isn't essential.

3. **Integration moats** — Bullhorn ATS integration is hard to replicate quickly.
   Every integration you build raises switching costs for customers AND acquisition value.

4. **Clean, documented codebase** — Acquirers do technical due diligence.
   A messy codebase with no tests kills deals or reduces price 30–50%.
   (InterviewCraft's code quality standards apply here from day one.)

5. **Customer concentration < 30%** — If one customer is >30% of revenue,
   acquirers see existential risk. Diversify across 15+ customers before selling.

6. **Vertical expertise documented** — Staffing industry knowledge (compliance,
   ATS vocabulary, screening regulations) packaged as competitive moat, not just code.

---

## Valuation Reality

| MRR | ARR | Realistic multiple | Sale price range |
|-----|-----|--------------------|-----------------|
| $10K | $120K | 2–3x | $240K–$360K |
| $30K | $360K | 3–4x | $1.1M–$1.4M |
| $50K | $600K | 4–5x | $2.4M–$3M |
| $80K | $960K | 4–6x | $3.8M–$5.8M |

Voice AI + vertical focus currently commands premium multiples (4–6x ARR)
because acquirers pay for distribution, not just revenue.

---

## Timeline

### Phase 1: Validation (Months 0–3)
- Build MVP on Vapi/Bland infrastructure
- Focus: warehouse/logistics temp staffing screening flow
- Integration: Bullhorn ATS (API + webhook)
- Target: 3 beta agencies using it (free or $500/mo)
- Success metric: Agencies actually using it in production, not just demoing it

### Phase 2: Product-Market Fit (Months 3–6)
- Raise beta price to $1,000–$2,000/month
- Build self-service configuration UI (agencies set up their own screening flows)
- Target: 5–8 paying customers, $5K–$15K MRR
- Success metric: <5% monthly churn, customers referring other agencies

### Phase 3: Scale Narrow (Months 6–12)
- Deepen Bullhorn integration (two-way sync, placement tracking)
- Add second ATS: Avionte or TempWorks
- Expand to healthcare staffing (same call pattern, higher ARPU)
- Target: 15–20 customers, $20K–$35K MRR
- Success metric: NPS > 40, customers saying "I can't imagine going back"

### Phase 4: Acquisition-Ready (Months 12–24)
- Add NL2SQL analytics layer ("ask your placement data")
- Add compliance documentation (BIPA compliance, audit logs)
- Build proper onboarding, documentation, support processes
- Target: 25–40 customers, $35K–$80K MRR
- Start conversations with potential acquirers at $30K+ MRR

### Phase 5: Exit (Months 18–36)
- Approach strategic acquirers
- Use M&A advisors for deals > $1M (they take 5–10% but run better processes)

---

## Who Would Acquire VoiceHire

### Strategic acquirers (most likely, highest price)

| Acquirer | Why they'd buy | Price driver |
|----------|---------------|--------------|
| **Bullhorn** | Dominant staffing ATS ($400M+ revenue). Adding native voice AI is product roadmap. Buying distribution to their own customers. | High — they'd pay 5–6x ARR for customer overlap |
| **iCIMS** | Large ATS platform, actively acquiring AI features. | Medium-high |
| **Employ Inc** (Jobvite/JazzHR) | Mid-market ATS, looking for AI differentiation. | Medium |
| **Staffing industry rollups** | Private equity-backed staffing consolidators buying tech | Medium |
| **Vapi/Bland.ai** | If they want to move upmarket into vertical applications | Lower — infrastructure companies don't pay premium for vertical apps |

### Financial acquirers (less likely at this size)
- Private equity: Typically needs $5M+ ARR before caring
- Search funds: Possible at $1M–$3M ARR

---

## Solo + Claude: Is It Feasible?

### What's achievable solo

| Task | Solo feasible? | Claude's role |
|------|---------------|---------------|
| Full backend (FastAPI + DB + integrations) | Yes | Code generation, review, debugging |
| Full frontend (Next.js dashboard) | Yes | Component generation, UI logic |
| Voice agent configuration | Yes | Prompt engineering, flow design |
| Bullhorn ATS integration | Yes (4–6 weeks) | API exploration, error handling |
| First 10 customer support | Yes | Template responses, knowledge base |
| First 10 customer sales | Hard but possible | Pitch deck, email sequences |
| 10–30 customer scale | Needs part-time help | Customer success, demos |
| 30+ customer scale | Needs first hire | Sales, customer success |

### The honest constraint

Solo works through $20–30K MRR. Above that, sales and customer success become
the bottleneck — not engineering. At $30K MRR you can afford to hire one person.

**The critical path is: build fast, get paying customers, use early revenue to
hire the one person you can't replace (sales or customer success).**

### Claude's actual value in this

- Accelerates engineering 3–5x (you build in 3 months what takes 9 months solo)
- Reduces context-switching cost (documentation, test writing, code review)
- Strategic sounding board for product and business decisions
- Never takes vacation, never gets sick, available at 2am when you're debugging

Realistic engineering timeline with Claude support:
- MVP: 4–6 weeks (not 3–4 months)
- First integration: 2–3 weeks
- Self-service UI: 3–4 weeks

---

## The "Worth Trying" Case

**Best case:** $50K MRR in 18 months → sale at 4–5x ARR → $2.4M–$3M.
Solo developer, life-changing money, built in 18 months.

**Middle case:** $20K MRR in 18 months, sell for $800K–$1.2M.
Still very meaningful for 18 months of work alongside job search.

**Downside case:** Build for 6 months, get 3–5 customers, decide it's not working.
Exit with $10K–$30K in revenue and a production voice AI product to show interviewers.
Worst case: still improves the job search.

**There is no scenario where building and launching this hurts you.**

---

## Critical Decisions Before Starting

1. **Staffing vs. CPA firms first?**
   - Staffing: higher call volume, faster sales cycles, year-round revenue
   - CPA: natural urgency window (launch November → immediate January revenue)
   - Recommendation: Staffing first (lower seasonality risk, bigger market)

2. **Vapi vs. Bland vs. Retell for infrastructure?**
   - Vapi: Best developer experience, most integrations, $0.05/min
   - Bland: Good pricing, growing fast
   - Retell: Strong reliability, good WebSocket support
   - Recommendation: Start with Vapi (best docs, widest community)

3. **Build own ATS integration vs. use a middleware?**
   - Bullhorn has a REST API (key-based access, free for partners)
   - Build direct — middleware adds cost and latency on something that must be reliable

4. **Open source or closed?**
   - Closed source — this is a business, not a portfolio project
   - The moat is the vertical knowledge and integrations, not the code
