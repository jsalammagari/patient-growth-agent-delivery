# Patient Acquisition & Growth Agent — Delivery Assessment

Submission for Ajaia LLC AI Solutions Architect assessment.
**Candidate:** Jahnavi Salammagari · jahnavi.salammagari@sjsu.edu

## What's in this repo

| File / folder | Purpose |
|---|---|
| `ASSIGNMENT.md` | Main deliverable — Parts 1 & 2 (Delivery Operating Model + Technical Readiness Note) |
| `CLIENT_STATUS_SAMPLE.md` | Part 4 — sample weekly client status update |
| `AI_WORKFLOW.md` | Part 5 — AI tooling and workflow note |
| `app.py` | Part 3 — Streamlit delivery-ops prototype |
| `data/` | Seed YAML data driving the prototype (edit these to change the UI) |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## Part 3 prototype — how to run

The prototype is a **Streamlit** app that reads from editable YAML files under `data/`. No external API keys, no cloud services, no paid dependencies.

### Prerequisites
- Python 3.9+ (tested on 3.13)
- `pip` (ships with Python)

### Install & run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Streamlit opens the app at [http://localhost:8501](http://localhost:8501).

### What you see

- **Sidebar** — engagement metadata and overall RAG status
- **Top metrics** — current week, workstream count, open risks, readiness progress
- **Tab 1: Workstream Health** — RAG counts, summary table with progress bars, per-workstream detail cards
- **Tab 2: Milestones** — 8-week plan, 3 named gates, filterable table with row coloring (red / amber / green)
- **Tab 3: RAID** — Risks (severity × likelihood, threshold-colored), Assumptions, Issues, Decisions in four sub-tabs
- **Tab 4: Weekly Status Generator** — click **Regenerate** to compile a client-ready markdown update from the live data; **Download as Markdown** saves it as `weekly_status_<date>.md`

### Editing the data

Open any file in `data/` and change values directly:

- `data/project.yaml` — overall status, current week, snapshot date
- `data/workstreams.yaml` — workstream RAG, % complete, owners
- `data/milestones.yaml` — milestone status (`done` / `on_track` / `at_risk` / `blocked` / `not_started`)
- `data/raid.yaml` — risks, assumptions, issues, decisions
- `data/readiness.yaml` — Gate-3 launch-readiness checklist

In the running app, hit **🔄 Regenerate from latest data** on the Weekly Status tab to pick up edits.

## What the seed data represents

A week-3 snapshot (status as of **2026-04-17**) of a hospital engagement mid-flight:

- Discovery and Compliance tracking well (W1 green, W4 green)
- Epic integration sandbox access delayed — **W2 red**, M07 blocked
- Cardiology routing rules unresolved — Gate 1 at risk, likely slips to Monday W4
- 2 open issues, 3 pending decisions, 8 tracked risks

Overall status: **AMBER**. The prototype is designed so this story surfaces consistently across every tab and the generated weekly status.

## Design choices worth noting

- **YAML over a DB** — inspectable, diff-able, easy for a delivery team to actually edit.
- **Status generation is template-based, not LLM-based** — deterministic, auditable, and safer for hospital-client communication than a creative model.
- **Risk scoring = severity × likelihood with explicit governance thresholds** (≥16 critical path, 12–15 weekly review, <12 monthly) — the score isn't decorative, it drives review cadence.
- **Dual ownership (Ajaia + hospital)** encoded everywhere — matches the operating reality that hospital-side responsiveness is the most common delivery risk.

## Scope

This is a lightweight prototype, not production software. Known limitations:

- No auth (single-team internal tool)
- No persistence of edits in-app — edit YAML files directly
- No integration with Epic, Salesforce, or other upstream systems (out of scope for a delivery-ops tracker)
- No test suite (syntax verified, runtime smoke tested)
