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

st.set_page_config(page_title="SOC Home Lab v2 Dashboard", layout="wide")
st.title("SOC Home Lab v2 Dashboard")
st.caption(
    "Simulated SOC telemetry, enriched detections, SQL reporting, and operational metrics suitable for a portfolio project."
)

if not ALERTS_PATH.exists():
    st.warning("No alerts file found. Run: python src/run_pipeline.py")
    st.stop()

alerts = pd.read_csv(ALERTS_PATH)

if alerts.empty:
    st.info("No alerts detected in current dataset")
    st.stop()

for column in ["first_seen", "last_seen", "detected_at", "resolved_at"]:
    alerts[column] = pd.to_datetime(alerts[column], errors="coerce")

for column in ["triage_minutes", "resolution_minutes"]:
    alerts[column] = pd.to_numeric(alerts[column], errors="coerce")

alerts["sla_breached"] = alerts["sla_breached"].astype(str).str.lower().isin(["true", "1"])
alerts["alert_bucket"] = alerts["detected_at"].dt.floor("15min")

with st.sidebar:
    st.header("Filters")
    severities = st.multiselect("Severity", sorted(alerts["severity"].dropna().unique()), default=None)
    rules = st.multiselect("Rule", sorted(alerts["rule_id"].dropna().unique()), default=None)
    statuses = st.multiselect("Status", sorted(alerts["status"].dropna().unique()), default=None)
    hosts = st.multiselect("Hostname", sorted(alerts["hostname"].dropna().unique()), default=None)
    departments = st.multiselect("Department", sorted(alerts["department"].dropna().unique()), default=None)

filtered_alerts = alerts.copy()
if severities:
    filtered_alerts = filtered_alerts[filtered_alerts["severity"].isin(severities)]
if rules:
    filtered_alerts = filtered_alerts[filtered_alerts["rule_id"].isin(rules)]
if statuses:
    filtered_alerts = filtered_alerts[filtered_alerts["status"].isin(statuses)]
if hosts:
    filtered_alerts = filtered_alerts[filtered_alerts["hostname"].isin(hosts)]
if departments:
    filtered_alerts = filtered_alerts[filtered_alerts["department"].isin(departments)]

total_events = None
if DB_PATH.exists():
    with sqlite3.connect(DB_PATH) as connection:
        total_events = pd.read_sql_query("SELECT COUNT(*) AS total_events FROM raw_events", connection).iloc[0][
            "total_events"
        ]

active_alerts = int(filtered_alerts["status"].isin(["open", "investigating"]).sum())
critical_alerts = int((filtered_alerts["severity"] == "critical").sum())
sla_breaches = int(filtered_alerts["sla_breached"].sum())
avg_triage = round(filtered_alerts["triage_minutes"].dropna().mean(), 1) if not filtered_alerts.empty else 0.0
closed_alerts = filtered_alerts[filtered_alerts["resolution_minutes"].notna()]
avg_resolution = round(closed_alerts["resolution_minutes"].mean(), 1) if not closed_alerts.empty else 0.0

metric_columns = st.columns(6)
metric_columns[0].metric("Events ingested", total_events if total_events is not None else "n/a")
metric_columns[1].metric("Filtered alerts", len(filtered_alerts))
metric_columns[2].metric("Critical alerts", critical_alerts)
metric_columns[3].metric("Active backlog", active_alerts)
metric_columns[4].metric("Avg triage (min)", avg_triage)
metric_columns[5].metric("SLA breaches", sla_breaches)

secondary_metrics = st.columns(3)
secondary_metrics[0].metric("Closed alerts", len(closed_alerts))
secondary_metrics[1].metric("Avg resolution (min)", avg_resolution)
secondary_metrics[2].metric("Unique hosts", filtered_alerts["hostname"].nunique())

left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Alert trend by 15-minute window")
    trend = (
        filtered_alerts.groupby("alert_bucket")
        .size()
        .rename("alert_count")
        .reset_index()
        .sort_values("alert_bucket")
    )
    if not trend.empty:
        st.line_chart(trend.set_index("alert_bucket"))
    else:
        st.info("No alerts match the selected filters.")

with right_chart:
    st.subheader("Severity distribution")
    severity_counts = filtered_alerts["severity"].value_counts().rename_axis("severity").reset_index(name="count")
    if not severity_counts.empty:
        st.bar_chart(severity_counts.set_index("severity"))
    else:
        st.info("No severity data available for the selected filters.")

left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Status distribution")
    status_counts = filtered_alerts["status"].value_counts().rename_axis("status").reset_index(name="count")
    if not status_counts.empty:
        st.bar_chart(status_counts.set_index("status"))
    else:
        st.info("No status data available for the selected filters.")

with right_chart:
    st.subheader("Rule distribution")
    rule_counts = filtered_alerts["rule_id"].value_counts().rename_axis("rule_id").reset_index(name="count")
    if not rule_counts.empty:
        st.bar_chart(rule_counts.set_index("rule_id"))
    else:
        st.info("No rule data available for the selected filters.")

left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Top users by alerts")
    user_counts = filtered_alerts["user"].value_counts().head(10).rename_axis("user").reset_index(name="count")
    if not user_counts.empty:
        st.bar_chart(user_counts.set_index("user"))
    else:
        st.info("No user data available for the selected filters.")

with right_chart:
    st.subheader("Top hosts by alerts")
    host_counts = filtered_alerts["hostname"].value_counts().head(10).rename_axis("hostname").reset_index(name="count")
    if not host_counts.empty:
        st.bar_chart(host_counts.set_index("hostname"))
    else:
        st.info("No host data available for the selected filters.")

st.subheader("Alerts table")
st.dataframe(
    filtered_alerts[
        [
            "rule_id",
            "severity",
            "status",
            "user",
            "department",
            "hostname",
            "source_ip",
            "geo",
            "triage_minutes",
            "resolution_minutes",
            "sla_breached",
            "details",
        ]
    ],
    use_container_width=True,
)

if SQL_QUERIES_PATH.exists():
    with st.expander("Portfolio SQL queries used for analytics"):
        st.code(SQL_QUERIES_PATH.read_text(encoding="utf-8"), language="sql")

if REPORT_PATH.exists():
    st.subheader("Report preview")
    st.markdown(REPORT_PATH.read_text(encoding="utf-8"))

st.divider()
st.markdown("### Screenshot checklist")
st.markdown("1. Metrics cards with events, critical alerts, backlog, and SLA breaches")
st.markdown("2. Alert trend and severity distribution")
st.markdown("3. Status and rule distribution")
st.markdown("4. Alerts table with enriched columns")
st.markdown("5. SQL query snippet and report preview")
