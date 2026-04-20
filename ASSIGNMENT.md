# Patient Acquisition & Growth Agent — Delivery Plan

**Candidate:** Jahnavi Salammagari
**Role:** AI Solutions Architect, Ajaia LLC
**Client:** Hospital system (mid-sized, multi-specialty)
**Engagement:** Delivery planning + launch readiness for the Patient Acquisition & Growth Agent

### Assumed stack (stated for realism)
- **EHR:** Epic (with scheduling module)
- **CRM:** Salesforce Health Cloud
- **Messaging:** Twilio (SMS + voice)
- **Agent platform:** vendor-provided LLM agent runtime with tool/function calling
- **Pilot scope:** 2 service lines (e.g., primary care + cardiology) across 3 clinic sites before system-wide rollout

---

## Part 1 — Delivery Operating Model

### 1. Workstream Structure

Six workstreams run in parallel with explicit hand-offs. Each has a single accountable owner on both sides (Ajaia + hospital) to prevent diffuse responsibility — the most common failure mode in healthcare AI rollouts.

#### W1 — Discovery & Requirements
- **Objective:** Document the current patient acquisition journey (inbound leads, dormant reactivation, waitlist), target-state workflow, and measurable success criteria. Lock scope.
- **Owner:** Ajaia Delivery Lead + Hospital VP of Patient Access
- **Key dependencies:** Access to patient access / call-center leaders, marketing, service-line operations; existing workflow documentation; 6 months of historical lead and scheduling data
- **Primary outputs:**
  - Current-state + target-state journey maps
  - Routing & scheduling rule book (who gets scheduled where, when, by whom)
  - Success metrics with baselines (lead-to-appointment rate, time-to-first-touch, waitlist fill rate, no-show rate)
  - Signed scope document with in/out list

#### W2 — Integrations & Scheduling Systems
- **Objective:** Connect the agent to Epic (read/write appointments), Salesforce Health Cloud (leads, activity logging), and Twilio (SMS + voice) through secure, auditable integrations.
- **Owner:** Ajaia Solutions Engineer + Hospital IT Integration Lead
- **Key dependencies:** Signed BAA; sandbox/non-prod environments for Epic + Salesforce; API credentials; security review slot; agreed data contracts; provider calendar rules (templates, blocks, overbooking policy)
- **Primary outputs:**
  - Integration architecture diagram + data-flow map
  - Working sandbox integrations with end-to-end test calls
  - Data contract specs (field-level, including PHI classification)
  - Error handling + retry spec; idempotency keys for scheduling writes

#### W3 — Conversation Design & Knowledge Setup
- **Objective:** Design the agent's conversation flows, knowledge base, tone, and escalation paths — tuned for patient-appropriate language and clinical safety.
- **Owner:** Ajaia Conversation Designer + Hospital Marketing Director + Clinical SME (per service line)
- **Key dependencies:** Discovery outputs; service-line content (prep instructions, insurance accepted, what to expect); FAQ data from call-center logs; brand voice guidelines
- **Primary outputs:**
  - Flow designs per use case: inbound inquiry, dormant reactivation, waitlist fill, appointment confirmation/reschedule
  - Structured knowledge base (service lines, locations, providers, insurance, hours)
  - Escalation matrix — when/how the agent hands off to a human
  - Prompt templates + guardrail rules (no clinical advice, no diagnosis, no medication guidance)

#### W4 — Compliance, Privacy & Security
- **Objective:** Ensure HIPAA-compliant PHI handling, documented patient consent, full auditability, and clinical safety guardrails. Run a Privacy Impact Assessment (PIA) before pilot.
- **Owner:** Hospital Privacy Officer (accountable) + Ajaia Compliance Lead + Hospital Legal
- **Key dependencies:** Executed BAA; vendor SOC 2 / HITRUST attestations; PIA review slot; patient consent language approved by legal; data retention policy
- **Primary outputs:**
  - Signed BAA + vendor risk assessment
  - Completed PIA with documented residual risks
  - Consent flow spec (opt-in for SMS, recorded disclosure for voice)
  - Audit log design (who asked what, agent said what, which PHI was accessed)
  - Guardrail ruleset with test cases

#### W5 — QA, Safety Testing & Pilot Readiness
- **Objective:** Validate agent behavior across happy paths, edge cases, and adversarial inputs; prove pilot readiness with a go/no-go checklist before go-live.
- **Owner:** Ajaia QA Lead + Hospital Pilot Clinic Manager
- **Key dependencies:** W3 flows complete; W2 sandbox integrations live; synthetic test patient set; pilot cohort and script selected; red-team plan approved
- **Primary outputs:**
  - Test plan + executed results (functional, integration, safety, load)
  - Red-team findings + remediation log
  - Go/no-go launch-readiness checklist with named sign-offs
  - Pilot runbook (who watches what, escalation tree, kill-switch procedure)

#### W6 — Rollout & Performance Monitoring
- **Objective:** Staged launch from pilot to system-wide with live monitoring, a structured feedback loop, and clean hand-off to hospital ops.
- **Owner:** Ajaia Delivery Lead + Hospital Patient Access Director
- **Key dependencies:** Pilot success criteria met; ops team trained; dashboards live; on-call rotation staffed; training materials delivered
- **Primary outputs:**
  - Phased rollout plan (pilot → service-line expansion → system-wide)
  - KPI dashboard tied to Discovery-phase baselines
  - Ops runbook (incident response, tuning workflow, content update process)
  - Weekly performance review cadence with documented decisions

### Why this structure

- **Six workstreams, not ten** — healthcare AI deliveries fail on diffuse ownership more than missing workstreams. I collapse overlaps (e.g., no separate "training" stream; training is an output of W6).
- **Compliance is its own workstream, not a checkbox inside QA** — in a hospital, privacy sign-off is the critical path to pilot. Making it a workstream forces it on the timeline and assigns a single accountable owner.
- **Every stream has a named hospital-side owner.** Ajaia cannot deliver alone; the most common blocker is hospital-side responsiveness. Naming owners up-front makes escalation legitimate.

### 2. Milestones and Timeline (8 weeks to pilot go-live)

The plan is organized around **gates** — points where work stops until a named owner signs off. Gates force integration across workstreams and make "silent drift" visible.

| Week | Milestone | Workstream(s) | Gate / Sign-off | Primary Owner |
|---|---|---|---|---|
| **W1** | Kickoff + discovery launch | W1, W4 | Kickoff deck signed; BAA in flight; discovery interviews scheduled | Ajaia Delivery Lead |
| **W1** | Stakeholder map + RACI locked | All | RACI signed by hospital sponsor | Ajaia Delivery Lead |
| **W2** | Current-state journey mapped | W1 | Journey map validated by patient access + marketing | Hospital VP Patient Access |
| **W2** | BAA + vendor risk assessment complete | W4 | Privacy officer sign-off on BAA | Hospital Privacy Officer |
| **W3** | **Gate 1: Requirements frozen** | W1, W3 | Scope doc + routing/scheduling rule book signed | Hospital sponsor + Ajaia Delivery Lead |
| **W3** | Integration architecture reviewed | W2 | IT security + integration lead sign-off on architecture | Hospital IT Integration Lead |
| **W4** | Integrations live in sandbox (Epic read + Salesforce) | W2 | End-to-end sandbox test passes (lead → appt hold) | Ajaia Solutions Engineer |
| **W4** | Conversation flows v1 drafted (3 use cases) | W3 | Marketing + clinical SME review | Ajaia Conversation Designer |
| **W5** | **Gate 2: Internal prototype demo** | W2, W3 | Agent completes 10 scripted patient journeys end-to-end in sandbox | Ajaia Delivery Lead |
| **W5** | Privacy Impact Assessment complete | W4 | PIA signed; residual risks accepted in writing | Hospital Privacy Officer |
| **W5** | Pilot cohort + success criteria agreed | W5, W6 | Cohort list + KPI targets signed | Hospital Patient Access Director |
| **W6** | Functional + integration QA complete | W5 | Test pass rate ≥ defined threshold; P0/P1 bugs closed | Ajaia QA Lead |
| **W6** | Red-team + safety testing complete | W5, W4 | Red-team report reviewed; guardrails hardened | Ajaia QA Lead + Privacy Officer |
| **W7** | Ops runbook + training delivered | W6 | Pilot clinic staff trained; on-call rotation staffed | Hospital Pilot Clinic Manager |
| **W7** | Monitoring dashboard live | W6 | Dashboard shows live sandbox traffic; alert thresholds set | Ajaia Solutions Engineer |
| **W7** | **Gate 3: Launch-readiness review** | All | Go/no-go checklist complete; named sign-offs from all 6 workstreams | Hospital sponsor |
| **W8** | **Pilot go-live** (2 service lines, 3 sites, limited hours) | W6 | First 48h of live traffic reviewed; kill-switch tested | Ajaia Delivery Lead + Patient Access Director |
| **W8** | Week-1 pilot review + tuning plan | W6 | Tuning backlog prioritized; decision on expansion cadence | Steering committee |

### Why this sequence

- **Three named gates, not a continuous timeline.** Healthcare deliveries drift because every week looks the same. Gates (W3, W5, W7) force explicit stop/go decisions with named sign-offs, which is what hospital governance actually requires.
- **BAA and PIA on the critical path, not parallel nice-to-haves.** If W4 slips, the pilot slips. That is called out on the timeline so it gets executive attention in week 1, not week 6.
- **Pilot scope is deliberately narrow** — 2 service lines, 3 sites, limited hours for the first week. This trades breadth for the ability to watch every conversation in week 8 and tune fast. Expansion cadence is a *decision* out of the week-8 review, not a pre-committed rollout.
- **Kill-switch tested before go-live.** The ability to turn the agent off cleanly is not optional in a patient-facing deployment; making it a W7 gate item ensures it is not discovered missing at 7am on go-live day.

### 3. Dependency and Risk View

Risks are scored **severity × likelihood** (1–5 each → max 25). Anything ≥ 12 gets weekly executive visibility; ≥ 16 gets a named owner on the critical path with a pre-committed mitigation budget.

| # | Risk | Sev | Like | Score | Owner |
|---|---|---|---|---|---|
| R1 | HIPAA / PHI handling failure (audit, BAA, logging) | 5 | 3 | **15** | Hospital Privacy Officer |
| R2 | Epic scheduling integration slips or fails QA | 4 | 4 | **16** | Hospital IT Integration Lead |
| R3 | Ambiguous routing / scheduling rules across service lines | 4 | 4 | **16** | Hospital VP Patient Access |
| R4 | Agent response quality — hallucination or unsafe clinical reply | 5 | 3 | **15** | Ajaia QA Lead |
| R5 | Escalation / fallback gaps (patient stuck, no human takeover) | 5 | 3 | **15** | Ajaia Conversation Designer |
| R6 | Poor lead data quality in Salesforce | 3 | 4 | **12** | Hospital Marketing Director |
| R7 | Stakeholder misalignment (clinical vs. marketing vs. IT) | 3 | 4 | **12** | Ajaia Delivery Lead |
| R8 | Patient consent / TCPA compliance for SMS + voice outreach | 4 | 2 | **8** | Hospital Legal |

#### R1 — HIPAA / PHI handling failure  (15)
- **Why it matters:** A PHI incident halts the pilot, triggers breach notification, and ends the vendor relationship. No other risk is more expensive.
- **Monitor:** Weekly PIA checkpoint through W5; automated PHI-access audit log review; vendor SOC 2 / HITRUST attestations on file.
- **Mitigate:** BAA signed in W1–W2 (critical path); PHI minimization at the integration layer (agent receives only what it needs); audit logging for every PHI read/write; red-team scenarios specifically targeting data exfiltration; privacy officer on Gate 1, 2, and 3 sign-offs.

#### R2 — Epic scheduling integration slips (16)
- **Why it matters:** Without reliable calendar writes, the agent cannot book — which is the core product promise. This is the most common schedule killer in healthcare AI deployments.
- **Monitor:** Daily sandbox integration test (synthetic patient, synthetic appointment write + read-back); integration burndown reviewed every Tuesday; escalate to hospital CIO if not live-in-sandbox by end of W3.
- **Mitigate:** Spike the hardest integration path in W2 (not W4); contract an Epic-certified integration partner for surge capacity; build idempotent scheduling calls with retry + replay; design a "hold + human confirm" fallback so pilot can launch even if autonomous booking is deferred.

#### R3 — Ambiguous routing / scheduling rules (16)
- **Why it matters:** Every clinic has undocumented rules — which insurance goes where, which provider sees new patients, overbooking policy, telehealth vs. in-person preferences. If the agent guesses, it misroutes patients and frustrates providers.
- **Monitor:** Rule-book completeness scored weekly in W1–W3 (% of service-line rules documented and validated); conflict log from conversation-design review.
- **Mitigate:** Dedicated W1–W3 rule-elicitation sessions per service line, each with a named clinic operations SME; encode rules as a testable decision tree, not free-text prompts; every unresolved rule gets an "ask a human" fallback rather than a guess.

#### R4 — Unsafe agent response (hallucination, clinical advice) (15)
- **Why it matters:** A patient receiving wrong medical guidance from a hospital-branded agent is a clinical safety event. This is the risk that keeps hospital general counsel up at night.
- **Monitor:** Adversarial prompt test suite run on every conversation-flow change; hallucination rate tracked against a labeled golden set; live conversation sampling (≥ 5% of pilot traffic) in W8.
- **Mitigate:** Explicit guardrails — the agent refuses clinical advice, diagnosis, medication guidance, and triage; keyword + intent-level classifiers route any clinical question to a nurse line; conservative RAG over a curated KB (no open-web retrieval); week-1 pilot = 100% human review of transcripts.

#### R5 — Escalation / fallback gaps (15)
- **Why it matters:** A patient stuck in an agent loop at 11pm who needed a human is both a safety risk and a reputational one. Healthcare agents fail loudly here.
- **Monitor:** Escalation rate tracked per intent; "dead-end" detector (>N turns without resolution) alerts on-call; patient-feedback channel monitored daily during pilot.
- **Mitigate:** Explicit escalation matrix (when + to whom + in what hours); default-escalate on any clinical or billing question; after-hours voicemail + next-business-day callback baked into flows; "talk to a human" is always a one-turn away option, not buried.

#### R6 — Poor lead data quality (12)
- **Why it matters:** The agent is only as good as the leads it contacts. Dirty phone numbers, missing consent flags, or duplicated records create wasted outreach and compliance risk.
- **Monitor:** Data-quality audit in W1 (bounce rate, duplication rate, missing-field rate); ongoing weekly quality score on the lead queue.
- **Mitigate:** Pre-launch data cleansing sprint in W2–W3; deduplication + phone validation before the agent touches a record; exclusion filters on records missing consent; QBR-level review of data quality trends.

#### R7 — Stakeholder misalignment (12)
- **Why it matters:** Marketing wants more appointments, clinical wants safety, IT wants stability, finance wants ROI. Without a single decision-making body, each week produces "yes, but…" from a different corner and no decision gets made.
- **Monitor:** Weekly steering-committee attendance + decision-log completeness; RAID "decisions needed" count trending up = a red flag.
- **Mitigate:** Single hospital sponsor (VP-level) with decision rights; weekly 30-min steering committee with a hard agenda; every workstream has a named Ajaia + hospital owner pair; decisions documented in the RAID with a deadline.

#### R8 — Patient consent / TCPA compliance (8)
- **Why it matters:** Automated outreach without documented consent is a regulatory and litigation risk (TCPA, state-level). Lower scored because it's well-understood and has clear legal guardrails — but it is a hard binary.
- **Monitor:** Consent-flag coverage audited per outbound batch; opt-out processing SLA tracked.
- **Mitigate:** Outreach only to records with explicit opt-in (or prior treatment relationship, legally reviewed); opt-out honored in real time and synced back to Salesforce; legal review of SMS language before any outbound send.

#### How this risk view is operationalized

- The prototype (Part 3) renders this table live, sorted by score, filterable by category — so the weekly steering committee opens it and sees the red items first.
- Every risk with score ≥ 12 is reviewed every week; score changes are a talking point in the client status update (Part 4).
- Mitigations are not suggestions — each has a named owner and a milestone tie-in. "Who and by when" is in the tool.

