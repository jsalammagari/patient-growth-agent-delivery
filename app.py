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
    # Filled by Task #8
    st.info("Milestones view — implemented in Task #8.")


def render_raid_tab(raid: dict[str, Any]) -> None:
    st.subheader("RAID Dashboard")
    st.caption(
        "Risks (severity x likelihood), Assumptions, Issues, Decisions. "
        "Data: data/raid.yaml"
    )
    # Filled by Task #9
    st.info("RAID dashboard — implemented in Task #9.")


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
        "Button below renders markdown you can copy or download."
    )
    # Filled by Task #10
    st.info("Weekly status generator — implemented in Task #10.")


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
