# Weekly Status — Patient Acquisition & Growth Agent

**To:** Hospital Sponsor (VP, Patient Access)
**From:** Ajaia Delivery Lead
**Week:** 3 of 8 — status as of **Friday, 17 April 2026**
**Overall status:** 🟡 **AT RISK** (was 🟢 last week)

---

## Executive summary

- **Discovery and compliance on track.** Primary-care routing signed, BAA executed, PIA draft circulated to legal.
- **Epic sandbox access is late** — credentials delayed 5 days. This is materializing into a schedule risk for the W4 integration milestone.
- **One ask:** sponsor decision needed this week on **autonomous booking vs. "hold + human confirm"** for the pilot (see Decisions Needed).

We expect to return to 🟢 next week if Epic credentials land Monday and cardiology rules close by Tuesday. If either slips, we will use the W4 steering committee to re-plan Gate 2 and the pilot go-live date, not to paper over it.

---

## Progress this week

- ✅ **Current-state patient journey** mapped and validated with patient access + marketing (W1)
- ✅ **BAA + vendor risk assessment** executed, one day ahead of target (W4)
- ✅ **Primary-care routing rules** signed and encoded as a testable decision tree
- **Conversation flow v1** for the inbound-inquiry use case drafted; review with clinical SME scheduled Tuesday (W3)
- **Integration architecture** complete in draft; security review slot confirmed for Monday (W2)

## Upcoming priorities (Week 4)

- **Gate 1 — Requirements freeze.** Slipping from Friday (W3) to Monday (W4) pending cardiology rule book closure. Session scheduled 10am Monday with cardiology clinic operations.
- **Epic sandbox end-to-end test** (search → hold → confirm). Dependent on credentials landing Monday; Ajaia engineering on standby to start same-day.
- **Conversation flows v1** for the other two use cases (dormant reactivation, waitlist fill). Reactivation flow is blocked on legal approval of SMS disclosure language — see decisions below.
- **Privacy Impact Assessment** target completion next Friday (W5). Legal review scheduled Tuesday.

## Risks and blockers

| ID | Risk / issue | Impact | Mitigation / ask |
|---|---|---|---|
| **R2** | Epic scheduling integration — sandbox credentials delayed 5 days | Puts the W4 Epic end-to-end test, and therefore the W5 Gate 2 prototype demo, at risk | Escalated to hospital CIO Friday. If credentials do not land by EOD Monday, we will spike the integration against Epic's public sandbox in parallel. **Help needed:** sponsor nudge on CIO ask. |
| **R3** | Cardiology routing rules — 7 open routing questions | Delays Gate 1 sign-off, compresses W4 | Rule-elicitation session confirmed with cardiology ops Monday. Unresolved rules default to "ask a human" in the agent. |
| **I1** | Epic non-prod credentials delayed 5 days (the specific blocker driving R2) | Blocks M07 | CIO escalation open; IT integration team aware |
| **I2** | 7 unresolved cardiology routing questions (the specific blocker driving part of R3) | Blocks M05 (Gate 1) | Session Monday |

Note: R2 and R3 are our two highest-scored risks this week (both at 16 on a 25-point scale). No change in top-5 risk ranking from last week.

## Decisions needed

1. **D1 — Autonomous booking vs. "hold + human confirm" for pilot.** Needed by Friday (W4). This decision materially changes Epic integration scope and pilot risk posture. My recommendation: **start pilot with "hold + human confirm"** and graduate to autonomous after the first two weeks of clean traffic. Happy to walk through tradeoffs in Tuesday's steering meeting.
2. **D3 — Approved SMS disclosure language.** Needed by Friday (W4). Blocking dormant-reactivation flow. Legal has the draft; needs executive sign-off.
3. **D2 — Pilot expansion cadence after the W8 review.** Not blocking this week; surfacing for awareness. Decision at the W8 retro.

## What good looks like by next Friday

- Gate 1 signed
- Epic sandbox end-to-end test passes at least once
- Conversation flows v1 for all three use cases in clinical-SME review
- PIA signed
- Pilot cohort list + KPI targets signed

If we hit those five, we are back to 🟢 and Gate 2 holds to W5.

---

_This update is generated from the delivery-ops tool and curated before send. The underlying data is browsable at any time via the internal dashboard._
