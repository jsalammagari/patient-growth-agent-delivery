# AI Workflow Note

**Assessment:** Ajaia LLC — AI Solutions Architect
**Candidate:** Jahnavi Salammagari

This note describes how I used AI during this assignment — what I delegated, what I did not, and what was accelerated.

## Tools used

- **Claude Code** (Anthropic Claude, Opus 4.7 in 1M-context mode) as the primary pair for planning, drafting, and coding
- **Python / Streamlit / PyYAML / pandas** — standard tooling for the prototype; no LLM calls in the prototype itself
- **QuickTime + YouTube (unlisted)** — for the walkthrough video
- **No paid APIs, no cloud services, no external model calls.** Everything runs locally.

## Workflow pattern

I ran the assignment in three explicit stages, each with a clear role for AI.

### 1. Plan before building
Before writing a single line, I asked Claude Code to propose a time-budgeted plan, then pushed back on it until it reflected *my* judgment on scope — one consolidated assignment doc, a single Streamlit prototype instead of a multi-page app, no LLM in the status generator. I converted the plan into **17 tracked tasks** and worked through them in order, marking each in_progress / completed as I went. The task list, not a vague "let's vibe on it," was the thing holding the work accountable.

### 2. Delegate drafting, keep judgment
For each task I gave Claude Code a specific brief — what to write, what constraints mattered, which prior artifacts to align with. I reviewed every output before committing and rewrote the parts where my framing differed. Concrete examples:

- **Part 1 workstream structure:** my call that compliance is its own workstream (not a QA sub-task), and that every stream has dual Ajaia + hospital ownership. These are opinions I had from thinking about healthcare delivery — AI drafted the language, I owned the structure.
- **Part 1 risk scoring:** I decided to use severity × likelihood with explicit governance thresholds (≥16 critical path, 12–15 weekly, <12 monthly). AI drafted the 8 risks; I reordered and rescored them based on how I actually see these risks play out.
- **Part 2 technical readiness:** my call to recommend FHIR-for-read + App Orchard-for-write, and to frame "ready to build" as a 10-item gate rather than a narrative. AI produced the failure-mode table; I validated the specific failure modes (stale slot, idempotency, timezone) against how these integrations actually fail.
- **Part 3 prototype:** AI wrote most of the Python; I specified the architecture (4 tabs, YAML source of truth, template-based status generator, no LLM at runtime). The decision to make the status generator *deterministic* rather than LLM-powered was deliberate — a hospital client trusts a repeatable format more than a creative one.
- **Part 4 client status:** I rewrote the auto-generated output into a VP-appropriate voice, added the RAG delta ("amber was green"), put a concrete recommendation on D1, and added the "what good looks like by next Friday" section. That editorial judgment is the job; the tool produces the raw material.

### 3. Verify, don't trust
- Every piece of Python was syntax-checked with `py_compile` after each edit.
- The prototype was end-to-end tested: venv install, YAML load, pure-function status generation, and a headless Streamlit run returning HTTP 200.
- The seed data was designed deliberately to tell a consistent week-3 story across every tab — I read through each rendered view to make sure the narrative lined up.

## What AI accelerated

- **Drafting speed.** Writing a 20+ page assignment document while building a working Streamlit app in under four hours is only realistic because I didn't hand-type every paragraph.
- **Scaffolding code.** The Streamlit boilerplate, the YAML loader, the progress-bar column, the pandas Styler row coloring — fast to generate, easy to review.
- **Consistency checks.** When I added a new workstream or renamed a risk, asking Claude to propagate the change across every artifact saved real time.

## What I did not let AI do

- **Structural decisions.** Workstream layout, gate placement, scoring model, the choice of a deterministic over an LLM-generated status update — all mine.
- **Risk prioritization.** Scoring is a judgment call; AI's first-pass ranking did not match how I weight these risks.
- **The narrative shape of the client status update.** Executive communication is about judgment and tone, not generation.
- **Claims about Epic integration paths.** I validated the FHIR-vs-App-Orchard recommendation against what I know about Epic's write APIs rather than deferring to the model.

## What I would do differently with more time

- **More explicit prompt logs.** I'd keep a running log of the prompts I used so a reviewer could see exactly how the work was partitioned.
- **Automated data-consistency checks.** A small Python test that asserts the story in `project.yaml` (overall RAG + reason) is still consistent with the underlying workstream/milestone/RAID data. Right now the consistency is enforced by me, not the code.
- **A second reviewer pass on the tech-readiness note.** I'd want a real Epic integration engineer to validate the failure-mode table — worth an hour of someone else's time before a real hospital read it.

## Bottom line

AI accelerated the typing. It did not replace the thinking. The structural choices, the prioritization, the editorial decisions in the client update, and the discipline of planning-before-building were mine. That's what I think an AI Solutions Architect is expected to do — operate confidently *with* AI, not around it.
