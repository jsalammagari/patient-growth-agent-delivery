"""
Patient Acquisition & Growth Agent — Delivery Ops Console.

A lightweight Streamlit tool for the Ajaia delivery team to track launch
readiness for the hospital engagement. All data is read from YAML files in
data/ so the underlying state is inspectable and editable.

Run:
    pip install -r requirements.txt
    streamlit run app.py
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import yaml

DATA_DIR = Path(__file__).parent / "data"

STATUS_COLOR = {
    "green": "#1f9d55",
    "amber": "#d97706",
    "red": "#b91c1c",
}

MILESTONE_STATUS_COLOR = {
    "done": "#1f9d55",
    "on_track": "#1f9d55",
    "at_risk": "#d97706",
    "blocked": "#b91c1c",
    "not_started": "#6b7280",
}


@st.cache_data
def load_yaml(filename: str) -> dict[str, Any]:
    with open(DATA_DIR / filename) as f:
        return yaml.safe_load(f)


def status_badge(status: str) -> str:
    color = STATUS_COLOR.get(status, "#6b7280")
    return (
        f'<span style="background:{color};color:white;padding:2px 10px;'
        f'border-radius:10px;font-size:0.85em;font-weight:600;">'
        f"{status.upper()}</span>"
    )


def milestone_status_badge(status: str) -> str:
    color = MILESTONE_STATUS_COLOR.get(status, "#6b7280")
    label = status.replace("_", " ").upper()
    return (
        f'<span style="background:{color};color:white;padding:2px 10px;'
        f'border-radius:10px;font-size:0.85em;font-weight:600;">{label}</span>'
    )


def render_sidebar(project: dict[str, Any]) -> None:
    eng = project["engagement"]
    st.sidebar.title("Delivery Ops Console")
    st.sidebar.caption("Patient Acquisition & Growth Agent")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Client:** {eng['client']}")
    st.sidebar.markdown(f"**Delivery Lead:** {eng['delivery_lead']}")
    st.sidebar.markdown(f"**Hospital Sponsor:** {eng['hospital_sponsor']}")
    st.sidebar.markdown(f"**Kickoff:** {eng['kickoff_date']}")
    st.sidebar.markdown(f"**Target go-live:** {eng['target_go_live']}")
    st.sidebar.markdown(f"**Status as of:** {eng['status_as_of']}  (week {eng['current_week']})")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Overall status**")
    st.sidebar.markdown(status_badge(eng["overall_status"]), unsafe_allow_html=True)
    st.sidebar.markdown(f"_{eng['overall_status_reason'].strip()}_")


def render_workstream_tab(workstreams: list[dict[str, Any]]) -> None:
    st.subheader("Workstream Health")
    st.caption("RAG status, owners, and progress per workstream. Data: data/workstreams.yaml")

    counts = {"green": 0, "amber": 0, "red": 0}
    for w in workstreams:
        counts[w["status"]] = counts.get(w["status"], 0) + 1

    cols = st.columns(3)
    cols[0].metric("Green", counts["green"])
    cols[1].metric("Amber", counts["amber"])
    cols[2].metric("Red", counts["red"])

    if counts["red"]:
        st.error(
            f"{counts['red']} workstream(s) red — escalate at this week's steering committee."
        )
    elif counts["amber"]:
        st.warning(f"{counts['amber']} workstream(s) amber — watch closely.")
    else:
        st.success("All workstreams green.")

    st.markdown("---")

    summary_rows = [
        {
            "ID": w["id"],
            "Workstream": w["name"],
            "Status": w["status"].upper(),
            "% Complete": w["percent_complete"],
            "Ajaia Owner": w["ajaia_owner"],
            "Hospital Owner": w["hospital_owner"],
            "Next Milestone": w["next_milestone"],
        }
        for w in workstreams
    ]
    df = pd.DataFrame(summary_rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "% Complete": st.column_config.ProgressColumn(
                "% Complete",
                min_value=0,
                max_value=100,
                format="%d%%",
            ),
        },
    )

    st.markdown("#### Details")
    for w in workstreams:
        header = (
            f"**{w['id']} — {w['name']}**  "
            f"{status_badge(w['status'])}  "
            f"_{w['percent_complete']}% complete_"
        )
        with st.expander(w["id"] + " — " + w["name"], expanded=(w["status"] == "red")):
            st.markdown(header, unsafe_allow_html=True)
            st.markdown(f"**Objective:** {w['objective']}")
            o1, o2 = st.columns(2)
            o1.markdown(f"**Ajaia owner:** {w['ajaia_owner']}")
            o2.markdown(f"**Hospital owner:** {w['hospital_owner']}")
            st.progress(w["percent_complete"] / 100.0)
            st.markdown(f"**Next milestone:** {w['next_milestone']}")
            if w.get("notes"):
                st.markdown(f"**Notes:** {w['notes']}")


def render_milestones_tab(milestones: list[dict[str, Any]]) -> None:
    st.subheader("Milestones")
    st.caption("8-week milestone plan with gate markers. Data: data/milestones.yaml")

    counts: dict[str, int] = {}
    for m in milestones:
        counts[m["status"]] = counts.get(m["status"], 0) + 1

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total", len(milestones))
    c2.metric("Done", counts.get("done", 0))
    c3.metric("On track", counts.get("on_track", 0))
    c4.metric("At risk", counts.get("at_risk", 0))
    c5.metric("Blocked", counts.get("blocked", 0))
    c6.metric("Not started", counts.get("not_started", 0))

    if counts.get("blocked", 0):
        blocked = [m for m in milestones if m["status"] == "blocked"]
        st.error(
            "🚫 Blocked: "
            + ", ".join(f"{m['id']} {m['name']}" for m in blocked)
        )
    if counts.get("at_risk", 0):
        at_risk = [m for m in milestones if m["status"] == "at_risk"]
        st.warning(
            "⚠ At risk: "
            + ", ".join(f"{m['id']} {m['name']}" for m in at_risk)
        )

    st.markdown("#### Gates")
    gates = [m for m in milestones if m.get("gate")]
    gate_cols = st.columns(len(gates)) if gates else []
    for col, g in zip(gate_cols, gates):
        col.markdown(
            f"**{g['gate']}** — W{g['week']}  \n"
            f"{g['name']}  \n"
            f"Target: {g['target_date']}  \n"
            f"{milestone_status_badge(g['status'])}",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    status_options = ["all", "done", "on_track", "at_risk", "blocked", "not_started"]
    selected_status = st.selectbox("Filter by status", status_options, index=0)
    week_options = ["all"] + [f"W{w}" for w in sorted({m["week"] for m in milestones})]
    selected_week = st.selectbox("Filter by week", week_options, index=0)

    filtered = milestones
    if selected_status != "all":
        filtered = [m for m in filtered if m["status"] == selected_status]
    if selected_week != "all":
        target_week = int(selected_week.lstrip("W"))
        filtered = [m for m in filtered if m["week"] == target_week]

    rows = [
        {
            "ID": m["id"],
            "Week": f"W{m['week']}",
            "Milestone": m["name"],
            "Gate": m.get("gate") or "",
            "Target": m["target_date"],
            "Actual": m.get("actual_date") or "",
            "Status": m["status"].replace("_", " ").upper(),
            "Owner": m["owner"],
            "Sign-off": m.get("sign_off", ""),
        }
        for m in filtered
    ]
    df = pd.DataFrame(rows)

    def highlight_row(row: pd.Series) -> list[str]:
        status = row["Status"]
        if status == "BLOCKED":
            return ["background-color: #fee2e2"] * len(row)
        if status == "AT RISK":
            return ["background-color: #fef3c7"] * len(row)
        if status == "DONE":
            return ["background-color: #f0fdf4"] * len(row)
        return [""] * len(row)

    if df.empty:
        st.info("No milestones match the selected filters.")
    else:
        st.dataframe(
            df.style.apply(highlight_row, axis=1),
            use_container_width=True,
            hide_index=True,
        )


def render_raid_tab(raid: dict[str, Any]) -> None:
    st.subheader("RAID Dashboard")
    st.caption(
        "Risks (severity x likelihood), Assumptions, Issues, Decisions. "
        "Data: data/raid.yaml"
    )

    risks = raid.get("risks", [])
    assumptions = raid.get("assumptions", [])
    issues = raid.get("issues", [])
    decisions = raid.get("decisions", [])

    open_risks = [r for r in risks if r["status"] != "closed"]
    high_risks = [r for r in open_risks if r["severity"] * r["likelihood"] >= 16]
    open_issues = [i for i in issues if i["status"] != "closed"]
    pending_decisions = [d for d in decisions if d["status"] == "pending"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open risks", len(open_risks))
    c2.metric("High risks (≥16)", len(high_risks))
    c3.metric("Open issues", len(open_issues))
    c4.metric("Pending decisions", len(pending_decisions))

    if high_risks:
        st.error(
            "High-severity risks demanding this week's attention: "
            + ", ".join(f"{r['id']} {r['title']}" for r in high_risks)
        )

    sub_r, sub_a, sub_i, sub_d = st.tabs(
        ["Risks", "Assumptions", "Issues", "Decisions"]
    )

    with sub_r:
        _render_risks(risks)
    with sub_a:
        _render_assumptions(assumptions)
    with sub_i:
        _render_issues(issues)
    with sub_d:
        _render_decisions(decisions)


def _score_color(score: int) -> str:
    if score >= 16:
        return "#fee2e2"  # red-tinted
    if score >= 12:
        return "#fef3c7"  # amber-tinted
    return "#f0fdf4"      # green-tinted


def _render_risks(risks: list[dict[str, Any]]) -> None:
    if not risks:
        st.info("No risks logged.")
        return

    status_filter = st.selectbox(
        "Filter by status",
        ["all", "open", "mitigating", "accepted", "closed"],
        index=0,
        key="risk_status",
    )
    filtered = risks if status_filter == "all" else [
        r for r in risks if r["status"] == status_filter
    ]

    rows = []
    for r in filtered:
        score = r["severity"] * r["likelihood"]
        rows.append(
            {
                "ID": r["id"],
                "Risk": r["title"],
                "Sev": r["severity"],
                "Like": r["likelihood"],
                "Score": score,
                "Status": r["status"].upper(),
                "Owner": r["owner"],
                "Workstream": r.get("workstream", ""),
                "Due": r.get("due_date", ""),
                "Mitigation": r["mitigation"].strip(),
            }
        )
    rows.sort(key=lambda x: x["Score"], reverse=True)
    df = pd.DataFrame(rows)

    def highlight(row: pd.Series) -> list[str]:
        color = _score_color(row["Score"])
        return [f"background-color: {color}"] * len(row)

    st.dataframe(
        df.style.apply(highlight, axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.NumberColumn(
                "Score", help="Severity x Likelihood (max 25)", format="%d"
            ),
        },
    )
    st.caption(
        "Scoring rule — ≥16 red (critical path, weekly exec visibility). "
        "12-15 amber (weekly review). <12 green (monthly review)."
    )


def _render_assumptions(assumptions: list[dict[str, Any]]) -> None:
    if not assumptions:
        st.info("No assumptions logged.")
        return
    df = pd.DataFrame(
        [
            {
                "ID": a["id"],
                "Assumption": a["title"],
                "Owner": a["owner"],
                "Status": a["status"].upper(),
                "Notes": a.get("notes", ""),
            }
            for a in assumptions
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_issues(issues: list[dict[str, Any]]) -> None:
    if not issues:
        st.info("No open issues.")
        return
    df = pd.DataFrame(
        [
            {
                "ID": i["id"],
                "Issue": i["title"],
                "Owner": i["owner"],
                "Status": i["status"].upper(),
                "Raised": i.get("raised_date", ""),
                "Notes": i.get("notes", ""),
            }
            for i in issues
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_decisions(decisions: list[dict[str, Any]]) -> None:
    if not decisions:
        st.info("No decisions pending.")
        return
    df = pd.DataFrame(
        [
            {
                "ID": d["id"],
                "Decision needed": d["title"],
                "Decision maker": d["decision_maker"],
                "Needed by": d.get("needed_by", ""),
                "Status": d["status"].upper(),
                "Notes": d.get("notes", ""),
            }
            for d in decisions
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_status_tab(
    project: dict[str, Any],
    workstreams: list[dict[str, Any]],
    milestones: list[dict[str, Any]],
    raid: dict[str, Any],
    readiness: list[dict[str, Any]],
) -> None:
    st.subheader("Weekly Status Generator")
    st.caption(
        "Compiles a client-ready weekly update from the live data. "
        "Regenerate after editing the YAML files. Download the .md to send."
    )

    if st.button("🔄 Regenerate from latest data"):
        st.cache_data.clear()
        st.rerun()

    md = generate_status_markdown(project, workstreams, milestones, raid, readiness)

    status_as_of = project["engagement"]["status_as_of"]
    filename = f"weekly_status_{status_as_of}.md"

    st.download_button(
        label="⬇ Download as Markdown",
        data=md,
        file_name=filename,
        mime="text/markdown",
    )

    st.markdown("---")
    st.markdown("#### Preview")
    st.markdown(md)

    with st.expander("View raw markdown (copyable)"):
        st.code(md, language="markdown")


def generate_status_markdown(
    project: dict[str, Any],
    workstreams: list[dict[str, Any]],
    milestones: list[dict[str, Any]],
    raid: dict[str, Any],
    readiness: list[dict[str, Any]],
) -> str:
    eng = project["engagement"]
    week = eng["current_week"]
    as_of = eng["status_as_of"]
    overall = eng["overall_status"]
    reason = eng["overall_status_reason"].strip()

    status_label = {"green": "ON TRACK", "amber": "AT RISK", "red": "OFF TRACK"}.get(
        overall, overall.upper()
    )

    completed_recent = [
        m for m in milestones
        if m["status"] == "done" and m.get("actual_date") and m["week"] in (week, week - 1)
    ]
    in_flight_this_week = [m for m in milestones if m["week"] == week and m["status"] != "done"]
    upcoming_next = [m for m in milestones if m["week"] == week + 1]
    blocked = [m for m in milestones if m["status"] == "blocked"]
    at_risk = [m for m in milestones if m["status"] == "at_risk"]

    risks = raid.get("risks", [])
    top_risks = sorted(
        [r for r in risks if r["status"] != "closed"],
        key=lambda r: r["severity"] * r["likelihood"],
        reverse=True,
    )[:3]
    open_issues = [i for i in raid.get("issues", []) if i["status"] != "closed"]
    pending_decisions = [d for d in raid.get("decisions", []) if d["status"] == "pending"]

    ready_complete = sum(1 for c in readiness if c["status"] == "complete")

    out: list[str] = []
    out.append(f"# Weekly Status — {eng['program']}")
    out.append(f"**Client:** {eng['client']}  ")
    out.append(f"**Week {week} of 8** · Status as of **{as_of}**  ")
    out.append(f"**Overall: {status_label}**\n")
    out.append(f"> {reason}\n")

    out.append("## Progress this week")
    if completed_recent:
        for m in completed_recent:
            out.append(
                f"- ✅ **{m['id']} {m['name']}** — completed {m['actual_date']} "
                f"(owner: {m['owner']})"
            )
    else:
        out.append("- _No milestones fully closed this week._")
    if in_flight_this_week:
        out.append("")
        out.append("**In flight this week:**")
        for m in in_flight_this_week:
            tag = "⚠ AT RISK" if m["status"] == "at_risk" else (
                "🚫 BLOCKED" if m["status"] == "blocked" else "→ in progress"
            )
            out.append(f"- {tag} — **{m['id']} {m['name']}** (target {m['target_date']}, owner: {m['owner']})")
    out.append("")

    out.append("## Upcoming priorities")
    if upcoming_next:
        for m in upcoming_next:
            gate = f" [**{m['gate']}**]" if m.get("gate") else ""
            out.append(f"- **{m['id']} {m['name']}**{gate} — target {m['target_date']} (owner: {m['owner']})")
    else:
        out.append("- _No milestones scheduled next week._")
    out.append("")

    out.append("## Workstream snapshot")
    out.append("| Workstream | Status | % Complete | Next milestone |")
    out.append("|---|---|---|---|")
    for w in workstreams:
        status_mark = {"green": "🟢", "amber": "🟡", "red": "🔴"}.get(w["status"], "⚪")
        out.append(
            f"| {w['id']} {w['name']} | {status_mark} {w['status'].upper()} | "
            f"{w['percent_complete']}% | {w['next_milestone']} |"
        )
    out.append("")

    out.append("## Risks and blockers")
    if blocked:
        out.append("**Blocked milestones:**")
        for m in blocked:
            out.append(f"- 🚫 {m['id']} {m['name']} — owner: {m['owner']}")
        out.append("")
    if at_risk:
        out.append("**At-risk milestones:**")
        for m in at_risk:
            out.append(f"- ⚠ {m['id']} {m['name']} — owner: {m['owner']}")
        out.append("")
    if top_risks:
        out.append("**Top risks this week:**")
        for r in top_risks:
            score = r["severity"] * r["likelihood"]
            out.append(
                f"- **{r['id']} (score {score})** {r['title']} — owner: {r['owner']}. "
                f"Mitigation: {r['mitigation'].strip().replace(chr(10), ' ')}"
            )
        out.append("")
    if open_issues:
        out.append("**Open issues:**")
        for i in open_issues:
            out.append(f"- {i['id']} {i['title']} — owner: {i['owner']} (raised {i.get('raised_date', 'n/a')})")
        out.append("")

    out.append("## Decisions needed")
    if pending_decisions:
        for d in pending_decisions:
            out.append(
                f"- **{d['id']} — {d['title']}** · decision maker: {d['decision_maker']} · "
                f"needed by: {d.get('needed_by', 'TBD')}"
            )
    else:
        out.append("- _No outstanding decisions._")
    out.append("")

    out.append("## Launch-readiness posture")
    out.append(
        f"- {ready_complete} of {len(readiness)} Gate-3 criteria complete. "
        f"See the readiness tracker for detail."
    )
    out.append("")

    out.append("---")
    out.append(f"_Generated from live delivery data on {date.today().isoformat()}._")

    return "\n".join(out)


def main() -> None:
    st.set_page_config(
        page_title="Patient Growth Agent — Delivery Ops",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    project = load_yaml("project.yaml")
    workstreams = load_yaml("workstreams.yaml")["workstreams"]
    milestones = load_yaml("milestones.yaml")["milestones"]
    raid = load_yaml("raid.yaml")
    readiness = load_yaml("readiness.yaml")["readiness_criteria"]

    render_sidebar(project)

    st.title("Patient Acquisition & Growth Agent — Delivery Ops")
    eng = project["engagement"]
    cols = st.columns(4)
    cols[0].metric("Week", f"{eng['current_week']} / 8")
    cols[1].metric("Workstreams", len(workstreams))
    cols[2].metric("Open risks", sum(1 for r in raid.get("risks", []) if r["status"] != "closed"))
    cols[3].metric(
        "Readiness complete",
        f"{sum(1 for c in readiness if c['status'] == 'complete')} / {len(readiness)}",
    )

    tab_health, tab_ms, tab_raid, tab_status = st.tabs(
        ["Workstream Health", "Milestones", "RAID", "Weekly Status"]
    )
    with tab_health:
        render_workstream_tab(workstreams)
    with tab_ms:
        render_milestones_tab(milestones)
    with tab_raid:
        render_raid_tab(raid)
    with tab_status:
        render_status_tab(project, workstreams, milestones, raid, readiness)


if __name__ == "__main__":
    main()
