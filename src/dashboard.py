from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
ALERTS_PATH = ROOT / "output" / "alerts.csv"
REPORT_PATH = ROOT / "output" / "alerts_report.md"
DB_PATH = ROOT / "analytics" / "soc_home_lab.db"
SQL_QUERIES_PATH = ROOT / "sql" / "portfolio_queries.sql"

st.set_page_config(page_title="SOC Operations Dashboard", layout="wide")
st.title("SOC Operations Dashboard")
st.caption("Alert workload, severity, triage performance, backlog, rule activity, and SLA monitoring.")

if not ALERTS_PATH.exists():
    st.warning("No alerts file found. Run: python src/run_pipeline.py")
    st.stop()

alerts = pd.read_csv(ALERTS_PATH)
if alerts.empty:
    st.info("No alerts detected in the current dataset.")
    st.stop()

for column in ["first_seen", "last_seen", "detected_at", "resolved_at"]:
    alerts[column] = pd.to_datetime(alerts[column], errors="coerce")
for column in ["triage_minutes", "resolution_minutes"]:
    alerts[column] = pd.to_numeric(alerts[column], errors="coerce")

alerts["sla_breached"] = alerts["sla_breached"].astype(str).str.lower().isin(["true", "1"])
alerts["alert_bucket"] = alerts["detected_at"].dt.floor("15min")

with st.sidebar:
    st.header("Filters")
    severities = st.multiselect("Severity", sorted(alerts["severity"].dropna().unique()))
    rules = st.multiselect("Rule", sorted(alerts["rule_id"].dropna().unique()))
    statuses = st.multiselect("Status", sorted(alerts["status"].dropna().unique()))
    hosts = st.multiselect("Hostname", sorted(alerts["hostname"].dropna().unique()))
    departments = st.multiselect("Department", sorted(alerts["department"].dropna().unique()))

filtered = alerts.copy()
for values, column in [(severities, "severity"), (rules, "rule_id"), (statuses, "status"), (hosts, "hostname"), (departments, "department")]:
    if values:
        filtered = filtered[filtered[column].isin(values)]

total_events = None
if DB_PATH.exists():
    with sqlite3.connect(DB_PATH) as connection:
        total_events = pd.read_sql_query("SELECT COUNT(*) AS total_events FROM raw_events", connection).iloc[0]["total_events"]

active_alerts = int(filtered["status"].isin(["open", "investigating"]).sum())
critical_alerts = int((filtered["severity"] == "critical").sum())
sla_breaches = int(filtered["sla_breached"].sum())
avg_triage = round(filtered["triage_minutes"].dropna().mean(), 1) if not filtered.empty else 0.0
closed = filtered[filtered["resolution_minutes"].notna()]
avg_resolution = round(closed["resolution_minutes"].mean(), 1) if not closed.empty else 0.0

metrics = st.columns(6)
metrics[0].metric("Events ingested", total_events if total_events is not None else "n/a")
metrics[1].metric("Filtered alerts", len(filtered))
metrics[2].metric("Critical alerts", critical_alerts)
metrics[3].metric("Active backlog", active_alerts)
metrics[4].metric("Avg triage (min)", avg_triage)
metrics[5].metric("SLA breaches", sla_breaches)

secondary = st.columns(3)
secondary[0].metric("Closed alerts", len(closed))
secondary[1].metric("Avg resolution (min)", avg_resolution)
secondary[2].metric("Unique hosts", filtered["hostname"].nunique())

left, right = st.columns(2)
with left:
    st.subheader("Alert trend")
    trend = filtered.groupby("alert_bucket").size().rename("alert_count").reset_index().sort_values("alert_bucket")
    st.line_chart(trend.set_index("alert_bucket")) if not trend.empty else st.info("No matching alerts.")
with right:
    st.subheader("Severity distribution")
    counts = filtered["severity"].value_counts().rename_axis("severity").reset_index(name="count")
    st.bar_chart(counts.set_index("severity")) if not counts.empty else st.info("No severity data.")

left, right = st.columns(2)
with left:
    st.subheader("Status distribution")
    counts = filtered["status"].value_counts().rename_axis("status").reset_index(name="count")
    st.bar_chart(counts.set_index("status")) if not counts.empty else st.info("No status data.")
with right:
    st.subheader("Rule activity")
    counts = filtered["rule_id"].value_counts().rename_axis("rule_id").reset_index(name="count")
    st.bar_chart(counts.set_index("rule_id")) if not counts.empty else st.info("No rule data.")

left, right = st.columns(2)
with left:
    st.subheader("Top users")
    counts = filtered["user"].value_counts().head(10).rename_axis("user").reset_index(name="count")
    st.bar_chart(counts.set_index("user")) if not counts.empty else st.info("No user data.")
with right:
    st.subheader("Top hosts")
    counts = filtered["hostname"].value_counts().head(10).rename_axis("hostname").reset_index(name="count")
    st.bar_chart(counts.set_index("hostname")) if not counts.empty else st.info("No host data.")

st.subheader("Alert queue")
st.dataframe(filtered[["rule_id", "severity", "status", "user", "department", "hostname", "source_ip", "geo", "triage_minutes", "resolution_minutes", "sla_breached", "details"]], use_container_width=True, hide_index=True)

if SQL_QUERIES_PATH.exists():
    with st.expander("Operational SQL queries"):
        st.code(SQL_QUERIES_PATH.read_text(encoding="utf-8"), language="sql")
if REPORT_PATH.exists():
    with st.expander("Generated SOC report"):
        st.markdown(REPORT_PATH.read_text(encoding="utf-8"))
