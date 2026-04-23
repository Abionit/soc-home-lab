from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
ALERTS_PATH = OUTPUT / "sample_wazuh_alerts.jsonl"


def load_alerts() -> list[dict]:
    records = []
    with ALERTS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            alert = json.loads(line)
            data = alert.get("data", {})
            rule = alert.get("rule", {})
            mitre = rule.get("mitre", {})
            records.append({
                "timestamp": alert.get("timestamp"),
                "rule_id": rule.get("id"),
                "rule_level": rule.get("level"),
                "description": rule.get("description"),
                "mitre": ",".join(mitre.get("id", [])),
                "host": alert.get("agent", {}).get("name"),
                "user": data.get("user"),
                "srcip": data.get("srcip"),
                "detection": data.get("soclab_detection"),
                "severity": data.get("severity"),
                "status": data.get("status"),
                "outcome": data.get("outcome"),
                "triage_minutes": int(data.get("triage_minutes", 0)),
                "resolution_minutes": int(data.get("resolution_minutes", 0)),
            })
    return records


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_sql_table(conn: sqlite3.Connection, table_name: str, rows: list[dict]) -> None:
    if not rows:
        return
    columns = list(rows[0].keys())
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    column_sql = ", ".join(f"{column} TEXT" for column in columns)
    conn.execute(f"CREATE TABLE {table_name} ({column_sql})")
    placeholders = ", ".join("?" for _ in columns)
    conn.executemany(
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
        [[row.get(column) for column in columns] for row in rows],
    )


def write_reports(alerts: list[dict]) -> None:
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    total_alerts = len(alerts)
    avg_triage = round(sum(row["triage_minutes"] for row in alerts) / total_alerts, 1)
    avg_resolution = round(sum(row["resolution_minutes"] for row in alerts) / total_alerts, 1)
    metrics = {
        "total_alerts": total_alerts,
        "critical_alerts": sum(1 for row in alerts if row["severity"] == "critical"),
        "high_alerts": sum(1 for row in alerts if row["severity"] == "high"),
        "active_alerts": sum(1 for row in alerts if row["status"] in {"open", "investigating"}),
        "avg_triage_minutes": avg_triage,
        "avg_resolution_minutes": avg_resolution,
        "unique_hosts": len({row["host"] for row in alerts}),
        "unique_mitre_techniques": len({row["mitre"] for row in alerts}),
    }

    grouped = {}
    for row in alerts:
        key = (row["rule_id"], row["detection"], row["severity"], row["mitre"])
        grouped.setdefault(key, {"rule_id": row["rule_id"], "detection": row["detection"], "severity": row["severity"], "mitre": row["mitre"], "alert_count": 0, "triage_total": 0, "resolution_total": 0})
        grouped[key]["alert_count"] += 1
        grouped[key]["triage_total"] += row["triage_minutes"]
        grouped[key]["resolution_total"] += row["resolution_minutes"]

    detection_summary = []
    for item in grouped.values():
        count = item["alert_count"]
        detection_summary.append({
            "rule_id": item["rule_id"],
            "detection": item["detection"],
            "severity": item["severity"],
            "mitre": item["mitre"],
            "alert_count": count,
            "avg_triage_minutes": round(item["triage_total"] / count, 1),
            "avg_resolution_minutes": round(item["resolution_total"] / count, 1),
        })
    detection_summary.sort(key=lambda row: (-row["alert_count"], severity_order.get(row["severity"], 9)))

    triage_queue = sorted(alerts, key=lambda row: (severity_order.get(row["severity"], 9), -row["triage_minutes"]))

    metric_fields = ["total_alerts", "critical_alerts", "high_alerts", "active_alerts", "avg_triage_minutes", "avg_resolution_minutes", "unique_hosts", "unique_mitre_techniques"]
    detection_fields = ["rule_id", "detection", "severity", "mitre", "alert_count", "avg_triage_minutes", "avg_resolution_minutes"]
    triage_fields = ["timestamp", "severity", "status", "rule_id", "detection", "host", "user", "srcip", "mitre", "outcome", "triage_minutes"]

    write_csv(OUTPUT / "alert_metrics.csv", [metrics], metric_fields)
    write_csv(OUTPUT / "detection_summary.csv", detection_summary, detection_fields)
    write_csv(OUTPUT / "triage_queue.csv", [{field: row[field] for field in triage_fields} for row in triage_queue], triage_fields)

    with sqlite3.connect(OUTPUT / "wazuh_soc_lab.db") as conn:
        write_sql_table(conn, "alerts", alerts)
        write_sql_table(conn, "alert_metrics", [metrics])
        write_sql_table(conn, "detection_summary", detection_summary)
        write_sql_table(conn, "triage_queue", [{field: row[field] for field in triage_fields} for row in triage_queue])

    write_executive_report(metrics, detection_summary, triage_queue)


def write_executive_report(metrics: dict, detection_summary: list[dict], triage_queue: list[dict]) -> None:
    top_detection = detection_summary[0]
    top_priority = triage_queue[0]
    report = f"""# Wazuh SOC Detection Engineering Report

Generated from representative lab alert data.

## Executive Summary

- Total alerts reviewed: {metrics['total_alerts']}
- Critical alerts: {metrics['critical_alerts']}
- High severity alerts: {metrics['high_alerts']}
- Active alerts requiring review: {metrics['active_alerts']}
- Average triage time: {metrics['avg_triage_minutes']} minutes
- Average resolution time: {metrics['avg_resolution_minutes']} minutes
- Unique hosts involved: {metrics['unique_hosts']}
- MITRE techniques represented: {metrics['unique_mitre_techniques']}

## Highest Priority Alert

- Detection: {top_priority['detection']}
- Severity: {top_priority['severity']}
- Host: {top_priority['host']}
- User: {top_priority['user']}
- Source IP: {top_priority['srcip']}
- MITRE: {top_priority['mitre']}
- Recommended action: {top_priority['outcome']}

## Most Active Detection

- Rule ID: {top_detection['rule_id']}
- Detection: {top_detection['detection']}
- Severity: {top_detection['severity']}
- Alert count: {top_detection['alert_count']}
- MITRE: {top_detection['mitre']}

## Analyst Notes

The lab demonstrates how Wazuh detections can be converted into structured SOC reporting. The analytics layer supports alert prioritization, severity review, MITRE coverage, and operational metrics that can be discussed in technical interviews.
"""
    (OUTPUT / "executive_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    if not ALERTS_PATH.exists():
        raise FileNotFoundError(f"Missing {ALERTS_PATH}. Run generate_lab_events.py first.")
    alerts = load_alerts()
    write_reports(alerts)
    print(f"Processed {len(alerts)} alerts.")


if __name__ == "__main__":
    main()
