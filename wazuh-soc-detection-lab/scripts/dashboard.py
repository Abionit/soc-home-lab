from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

st.set_page_config(page_title="Wazuh SOC Lab", layout="wide")
st.title("Wazuh SOC Detection Engineering Lab")
st.caption("Detection engineering, alert triage, MITRE mapping, and SOC reporting.")

metrics_path = OUTPUT / "alert_metrics.csv"
summary_path = OUTPUT / "detection_summary.csv"
triage_path = OUTPUT / "triage_queue.csv"

if not metrics_path.exists() or not summary_path.exists() or not triage_path.exists():
    st.warning("Run scripts/build_alert_analytics.py before opening the dashboard.")
    st.stop()

metrics = pd.read_csv(metrics_path).iloc[0]
summary = pd.read_csv(summary_path)
triage = pd.read_csv(triage_path)

cols = st.columns(4)
cols[0].metric("Total alerts", int(metrics["total_alerts"]))
cols[1].metric("Critical alerts", int(metrics["critical_alerts"]))
cols[2].metric("Active alerts", int(metrics["active_alerts"]))
cols[3].metric("MITRE techniques", int(metrics["unique_mitre_techniques"]))

cols = st.columns(2)
cols[0].subheader("Detection Summary")
cols[0].dataframe(summary, use_container_width=True)

cols[1].subheader("Severity Distribution")
severity_counts = triage["severity"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]
cols[1].bar_chart(severity_counts, x="severity", y="count")

st.subheader("Triage Queue")
st.dataframe(triage, use_container_width=True)
