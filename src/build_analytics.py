from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_EVENTS_PATH = ROOT / "data" / "raw_events.jsonl"
ALERTS_PATH = ROOT / "output" / "alerts.csv"
DB_PATH = ROOT / "analytics" / "soc_home_lab.db"
SCHEMA_PATH = ROOT / "sql" / "schema.sql"
OUTPUT_DIR = ROOT / "output"

EXPORT_QUERIES = {
    "alert_kpis": """
        SELECT
            (SELECT COUNT(*) FROM raw_events) AS total_events,
            (SELECT COUNT(*) FROM alerts) AS total_alerts,
            (SELECT COUNT(*) FROM alerts WHERE severity = 'critical') AS critical_alerts,
            (SELECT COUNT(*) FROM alerts WHERE status IN ('open', 'investigating')) AS active_alerts,
            ROUND((SELECT AVG(triage_minutes) FROM alerts), 1) AS avg_triage_minutes,
            ROUND((SELECT AVG(resolution_minutes) FROM alerts WHERE resolution_minutes IS NOT NULL), 1) AS avg_resolution_minutes,
            (SELECT COUNT(*) FROM alerts WHERE sla_breached = 1) AS sla_breaches
    """,
    "alert_trend": """
        SELECT
            strftime('%Y-%m-%d %H:00:00', detected_at) AS alert_hour,
            COUNT(*) AS alert_count,
            SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_alerts
        FROM alerts
        GROUP BY strftime('%Y-%m-%d %H:00:00', detected_at)
        ORDER BY alert_hour
    """,
    "rule_summary": """
        SELECT
            rule_id,
            severity,
            COUNT(*) AS alert_count,
            SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
            ROUND(AVG(triage_minutes), 1) AS avg_triage_minutes
        FROM alerts
        GROUP BY rule_id, severity
        ORDER BY alert_count DESC, rule_id
    """,
    "entity_hotspots": """
        SELECT
            hostname,
            user,
            COUNT(*) AS alert_count,
            MAX(severity) AS max_severity
        FROM alerts
        GROUP BY hostname, user
        ORDER BY alert_count DESC, hostname, user
    """,
}


def load_events_df(path: Path) -> pd.DataFrame:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    events_df = pd.DataFrame(rows)
    if not events_df.empty:
        events_df["timestamp"] = pd.to_datetime(events_df["timestamp"], errors="coerce")
    return events_df


def load_alerts_df(path: Path) -> pd.DataFrame:
    alerts_df = pd.read_csv(path)
    if alerts_df.empty:
        return alerts_df

    for column in ["first_seen", "last_seen", "detected_at", "resolved_at"]:
        alerts_df[column] = pd.to_datetime(alerts_df[column], errors="coerce")

    alerts_df["triage_minutes"] = pd.to_numeric(alerts_df["triage_minutes"], errors="coerce")
    alerts_df["resolution_minutes"] = pd.to_numeric(alerts_df["resolution_minutes"], errors="coerce")
    alerts_df["sla_breached"] = alerts_df["sla_breached"].astype(str).str.lower().isin(["true", "1"]).astype(int)

    return alerts_df


def write_database(connection: sqlite3.Connection, events_df: pd.DataFrame, alerts_df: pd.DataFrame) -> None:
    events_df.to_sql("raw_events", connection, if_exists="replace", index=False)
    alerts_df.to_sql("alerts", connection, if_exists="replace", index=False)
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def export_query_results(connection: sqlite3.Connection) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, query in EXPORT_QUERIES.items():
        export_path = OUTPUT_DIR / f"{name}.csv"
        pd.read_sql_query(query, connection).to_csv(export_path, index=False)


def main() -> None:
    if not RAW_EVENTS_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_EVENTS_PATH}")
    if not ALERTS_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {ALERTS_PATH}")
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    events_df = load_events_df(RAW_EVENTS_PATH)
    alerts_df = load_alerts_df(ALERTS_PATH)

    with sqlite3.connect(DB_PATH) as connection:
        write_database(connection, events_df, alerts_df)
        export_query_results(connection)

    print(f"Analytics database created at: {DB_PATH}")
    print("Exported CSVs: output/alert_kpis.csv, output/alert_trend.csv, output/rule_summary.csv, output/entity_hotspots.csv")


if __name__ == "__main__":
    main()
