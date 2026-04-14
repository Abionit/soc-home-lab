from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
RAW_EVENTS_PATH = ROOT / "data" / "raw_events.jsonl"
ALERTS_PATH = ROOT / "output" / "alerts.csv"
REPORT_PATH = ROOT / "output" / "alerts_report.md"

st.set_page_config(page_title="SOC Home Lab Dashboard", page_icon="🚨", layout="wide")
st.title("SOC Home Lab Dashboard")
st.caption("Visual evidence for portfolio: alerts, severities, users, and source IPs")

if not ALERTS_PATH.exists():
    st.warning("No alerts file found. Run: python src/run_pipeline.py")
    st.stop()

alerts = pd.read_csv(ALERTS_PATH)

if alerts.empty:
    st.info("No alerts detected in current dataset")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total alerts", len(alerts))
with col2:
    st.metric("Unique users", alerts["user"].nunique())
with col3:
    st.metric("Unique source IPs", alerts["source_ip"].nunique())

st.subheader("Alerts table")
st.dataframe(alerts, use_container_width=True)

st.subheader("Severity distribution")
severity_counts = alerts["severity"].value_counts().rename_axis("severity").reset_index(name="count")
st.bar_chart(severity_counts.set_index("severity"))

st.subheader("Rule distribution")
rule_counts = alerts["rule_id"].value_counts().rename_axis("rule_id").reset_index(name="count")
st.bar_chart(rule_counts.set_index("rule_id"))

st.subheader("Top users by alerts")
user_counts = alerts["user"].value_counts().head(10).rename_axis("user").reset_index(name="count")
st.bar_chart(user_counts.set_index("user"))

st.subheader("Top source IPs by alerts")
ip_counts = alerts["source_ip"].value_counts().head(10).rename_axis("source_ip").reset_index(name="count")
st.bar_chart(ip_counts.set_index("source_ip"))

if REPORT_PATH.exists():
    st.subheader("Report preview")
    st.markdown(REPORT_PATH.read_text(encoding="utf-8"))

st.divider()
st.markdown("### Screenshot checklist")
st.markdown("1. Metrics cards (total alerts, users, source IPs)")
st.markdown("2. Severity distribution chart")
st.markdown("3. Alerts table with at least one critical alert")
