from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_EVENTS_PATH = ROOT / "data" / "raw_events.jsonl"
ALERTS_CSV_PATH = ROOT / "output" / "alerts.csv"
ALERTS_MD_PATH = ROOT / "output" / "alerts_report.md"


@dataclass
class Alert:
    rule_id: str
    severity: str
    user: str
    source_ip: str
    first_seen: str
    last_seen: str
    details: str


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            event["timestamp"] = datetime.fromisoformat(event["timestamp"])
            events.append(event)
    return sorted(events, key=lambda x: x["timestamp"])


def detect_failed_login_burst(events: list[dict], window_minutes: int = 10, threshold: int = 5) -> list[Alert]:
    alerts: list[Alert] = []
    grouped: defaultdict[tuple[str, str], list[datetime]] = defaultdict(list)

    for event in events:
        if event["event_type"] == "login_failed":
            grouped[(event["user"], event["source_ip"])].append(event["timestamp"])

    for (user, source_ip), timestamps in grouped.items():
        timestamps = sorted(timestamps)
        left = 0
        max_count = 0
        best_window: tuple[datetime, datetime] | None = None

        for right in range(len(timestamps)):
            while timestamps[right] - timestamps[left] > timedelta(minutes=window_minutes):
                left += 1

            window_count = right - left + 1
            if window_count > max_count:
                max_count = window_count
                best_window = (timestamps[left], timestamps[right])

        if max_count >= threshold and best_window is not None:
            first_seen, last_seen = best_window
            alerts.append(
                Alert(
                    rule_id="R001",
                    severity="high",
                    user=user,
                    source_ip=source_ip,
                    first_seen=first_seen.isoformat(),
                    last_seen=last_seen.isoformat(),
                    details=f"{max_count} failed logins in <= {window_minutes} minutes",
                )
            )

    return alerts


def detect_privilege_change_from_external(events: list[dict]) -> list[Alert]:
    alerts: list[Alert] = []
    for event in events:
        if event["event_type"] == "privilege_change" and event.get("geo") not in {"CO", "INTERNAL"}:
            alerts.append(
                Alert(
                    rule_id="R002",
                    severity="critical",
                    user=event["user"],
                    source_ip=event["source_ip"],
                    first_seen=event["timestamp"].isoformat(),
                    last_seen=event["timestamp"].isoformat(),
                    details="Privilege change detected from external geography",
                )
            )
    return alerts


def build_summary(events: list[dict], alerts: list[Alert]) -> dict:
    event_type_counter = Counter(event["event_type"] for event in events)
    severity_counter = Counter(alert.severity for alert in alerts)

    return {
        "events_total": len(events),
        "alerts_total": len(alerts),
        "event_distribution": dict(event_type_counter),
        "severity_distribution": dict(severity_counter),
    }


def write_outputs(alerts: list[Alert], summary: dict) -> None:
    ALERTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([alert.__dict__ for alert in alerts])
    if df.empty:
        df = pd.DataFrame(
            columns=["rule_id", "severity", "user", "source_ip", "first_seen", "last_seen", "details"]
        )
    df.to_csv(ALERTS_CSV_PATH, index=False)

    lines = [
        "# SOC Alerts Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        f"- Total events analyzed: {summary['events_total']}",
        f"- Total alerts generated: {summary['alerts_total']}",
        f"- Event distribution: {summary['event_distribution']}",
        f"- Severity distribution: {summary['severity_distribution']}",
        "",
        "## Alerts",
    ]

    if alerts:
        for alert in alerts:
            lines.extend(
                [
                    f"### {alert.rule_id} | {alert.severity.upper()} | user={alert.user}",
                    f"- Source IP: {alert.source_ip}",
                    f"- First seen: {alert.first_seen}",
                    f"- Last seen: {alert.last_seen}",
                    f"- Details: {alert.details}",
                    "",
                ]
            )
    else:
        lines.append("No alerts detected.")

    ALERTS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not RAW_EVENTS_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_EVENTS_PATH}")

    events = load_events(RAW_EVENTS_PATH)
    alerts = []
    alerts.extend(detect_failed_login_burst(events))
    alerts.extend(detect_privilege_change_from_external(events))

    summary = build_summary(events, alerts)
    write_outputs(alerts, summary)

    print(f"Alerts generated: {len(alerts)}")
    print(f"CSV output: {ALERTS_CSV_PATH}")
    print(f"Report output: {ALERTS_MD_PATH}")


if __name__ == "__main__":
    main()
