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
