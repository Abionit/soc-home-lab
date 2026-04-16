from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

RAW_EVENTS_PATH = Path("data/raw_events.jsonl")
ALERTS_CSV_PATH = Path("output/alerts.csv")
ALERTS_MD_PATH = Path("output/alerts_report.md")
TRUSTED_GEOS = {"CO", "INTERNAL"}


@dataclass
class Alert:
    rule_id: str
    severity: str
    tactic: str
    technique: str
    user: str
    department: str
    source_ip: str
    geo: str
    hostname: str
    asset_group: str
    asset_criticality: str
    log_source: str
    first_seen: str
    last_seen: str
    detected_at: str
    status: str
    assigned_to: str
    triage_minutes: int | None
    resolution_minutes: int | None
    resolved_at: str | None
    sla_breached: bool
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
    return sorted(events, key=lambda event: event["timestamp"])


def build_alert(
    *,
    rule_id: str,
    severity: str,
    tactic: str,
    technique: str,
    event: dict,
    first_seen: datetime,
    last_seen: datetime,
    details: str,
) -> Alert:
    return Alert(
        rule_id=rule_id,
        severity=severity,
        tactic=tactic,
        technique=technique,
        user=event["user"],
        department=event["department"],
        source_ip=event["source_ip"],
        geo=event["geo"],
        hostname=event["hostname"],
        asset_group=event["asset_group"],
        asset_criticality=event["asset_criticality"],
        log_source=event["log_source"],
        first_seen=first_seen.isoformat(),
        last_seen=last_seen.isoformat(),
        detected_at=last_seen.isoformat(),
        status="",
        assigned_to="",
        triage_minutes=None,
        resolution_minutes=None,
        resolved_at=None,
        sla_breached=False,
        details=details,
    )


def detect_failed_login_burst(events: list[dict], window_minutes: int = 10, threshold: int = 5) -> list[Alert]:
    alerts: list[Alert] = []
    grouped: defaultdict[tuple[str, str, str], list[dict]] = defaultdict(list)

    for event in events:
        if event["event_type"] == "login_failed":
            grouped[(event["user"], event["source_ip"], event["hostname"])].append(event)

    for grouped_events in grouped.values():
        grouped_events = sorted(grouped_events, key=lambda event: event["timestamp"])
        left = 0
        best_left = 0
        best_right = 0
        best_count = 0

        for right in range(len(grouped_events)):
            while grouped_events[right]["timestamp"] - grouped_events[left]["timestamp"] > timedelta(
                minutes=window_minutes
            ):
                left += 1

            current_count = right - left + 1
            if current_count > best_count:
                best_count = current_count
                best_left = left
                best_right = right

        if best_count >= threshold:
            first_event = grouped_events[best_left]
            last_event = grouped_events[best_right]
            alerts.append(
                build_alert(
                    rule_id="R001",
                    severity="high",
                    tactic="Credential Access",
                    technique="T1110 Brute Force",
                    event=last_event,
                    first_seen=first_event["timestamp"],
                    last_seen=last_event["timestamp"],
                    details=f"{best_count} failed logins from the same IP in <= {window_minutes} minutes",
                )
            )

    return alerts


def detect_privilege_change_from_external(events: list[dict]) -> list[Alert]:
    alerts: list[Alert] = []
    for event in events:
        if event["event_type"] == "privilege_change" and event.get("geo") not in TRUSTED_GEOS:
            alerts.append(
                build_alert(
                    rule_id="R002",
                    severity="critical",
                    tactic="Persistence / Privilege Escalation",
                    technique="T1098 Account Manipulation",
                    event=event,
                    first_seen=event["timestamp"],
                    last_seen=event["timestamp"],
                    details="Privilege change detected from a non-trusted geography",
                )
            )
    return alerts


def detect_password_reset_followed_by_external_login(
    events: list[dict],
    window_minutes: int = 15,
) -> list[Alert]:
    alerts: list[Alert] = []
    events_by_user: defaultdict[str, list[dict]] = defaultdict(list)

    for event in events:
        events_by_user[event["user"]].append(event)

    for ordered_events in events_by_user.values():
        ordered_events = sorted(ordered_events, key=lambda event: event["timestamp"])
        reset_events = [event for event in ordered_events if event["event_type"] == "password_reset"]

        for reset_event in reset_events:
            matching_login = next(
                (
                    event
                    for event in ordered_events
                    if event["event_type"] == "login_success"
                    and event["geo"] not in TRUSTED_GEOS
                    and timedelta(0)
                    <= event["timestamp"] - reset_event["timestamp"]
                    <= timedelta(minutes=window_minutes)
                ),
                None,
            )

            if matching_login is not None:
                alerts.append(
                    build_alert(
                        rule_id="R003",
                        severity="high",
                        tactic="Initial Access / Defense Evasion",
                        technique="T1078 Valid Accounts",
                        event=matching_login,
                        first_seen=reset_event["timestamp"],
                        last_seen=matching_login["timestamp"],
                        details=(
                            "Password reset was followed by a successful login from a non-trusted geography "
                            f"within {window_minutes} minutes"
                        ),
                    )
                )

    return alerts


def enrich_alerts(alerts: list[Alert]) -> list[Alert]:
    severity_profiles = {
        "critical": {
            "triage_target": 15,
            "resolution_target": 120,
            "owners": ["Tier2 SOC", "Incident Response"],
            "status_cycle": ["closed", "investigating", "closed", "open"],
        },
        "high": {
            "triage_target": 30,
            "resolution_target": 240,
            "owners": ["Tier1 SOC", "Threat Hunter"],
            "status_cycle": ["closed", "investigating", "closed"],
        },
        "medium": {
            "triage_target": 60,
            "resolution_target": 480,
            "owners": ["Tier1 SOC"],
            "status_cycle": ["closed", "open", "closed"],
        },
    }

    ordered_alerts = sorted(alerts, key=lambda alert: alert.detected_at)

    for index, alert in enumerate(ordered_alerts):
        profile = severity_profiles[alert.severity]
        triage_target = profile["triage_target"]
        resolution_target = profile["resolution_target"]
        detected_at = datetime.fromisoformat(alert.detected_at)

        triage_minutes = triage_target + ((index % 4) - 1) * 6 + (4 if alert.rule_id == "R002" else 0)
        triage_minutes = max(5, triage_minutes)
        status = profile["status_cycle"][index % len(profile["status_cycle"])]
        assigned_to = profile["owners"][index % len(profile["owners"])]

        alert.status = status
        alert.assigned_to = assigned_to
        alert.triage_minutes = triage_minutes

        if status == "closed":
            resolution_minutes = resolution_target + (index % 3) * 25 + (15 if alert.rule_id == "R002" else 0)
            alert.resolution_minutes = resolution_minutes
            alert.resolved_at = (detected_at + timedelta(minutes=resolution_minutes)).isoformat()
        else:
            alert.resolution_minutes = None
            alert.resolved_at = None

        alert.sla_breached = bool(
            triage_minutes > triage_target
            or (alert.resolution_minutes is not None and alert.resolution_minutes > resolution_target)
        )

    return ordered_alerts


def build_summary(events: list[dict], alerts: list[Alert]) -> dict:
    event_type_counter = Counter(event["event_type"] for event in events)
    severity_counter = Counter(alert.severity for alert in alerts)
    status_counter = Counter(alert.status for alert in alerts)
    rule_counter = Counter(alert.rule_id for alert in alerts)

    return {
        "events_total": len(events),
        "alerts_total": len(alerts),
        "event_distribution": dict(event_type_counter),
        "severity_distribution": dict(severity_counter),
        "status_distribution": dict(status_counter),
        "rule_distribution": dict(rule_counter),
    }


def write_outputs(alerts: list[Alert], summary: dict) -> None:
    ALERTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "rule_id",
        "severity",
        "tactic",
        "technique",
        "user",
        "department",
        "source_ip",
        "geo",
        "hostname",
        "asset_group",
        "asset_criticality",
        "log_source",
        "first_seen",
        "last_seen",
        "detected_at",
        "status",
        "assigned_to",
        "triage_minutes",
        "resolution_minutes",
        "resolved_at",
        "sla_breached",
        "details",
    ]
    df = pd.DataFrame([alert.__dict__ for alert in alerts], columns=columns)
    if df.empty:
        df = pd.DataFrame(columns=columns)
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
        f"- Status distribution: {summary['status_distribution']}",
        f"- Rule distribution: {summary['rule_distribution']}",
        "",
        "## Alerts",
    ]

    if alerts:
        for alert in alerts:
            lines.extend(
                [
                    f"### {alert.rule_id} | {alert.severity.upper()} | user={alert.user} | status={alert.status}",
                    f"- Source IP: {alert.source_ip} ({alert.geo})",
                    f"- Hostname: {alert.hostname} | Asset criticality: {alert.asset_criticality}",
                    f"- MITRE ATT&CK: {alert.tactic} / {alert.technique}",
                    f"- First seen: {alert.first_seen}",
                    f"- Last seen: {alert.last_seen}",
                    f"- Assigned to: {alert.assigned_to}",
                    f"- Triage minutes: {alert.triage_minutes}",
                    f"- Resolution minutes: {alert.resolution_minutes if alert.resolution_minutes is not None else 'pending'}",
                    f"- SLA breached: {'yes' if alert.sla_breached else 'no'}",
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
    alerts.extend(detect_password_reset_followed_by_external_login(events))
    alerts = enrich_alerts(alerts)

    summary = build_summary(events, alerts)
    write_outputs(alerts, summary)

    print(f"Alerts generated: {len(alerts)}")
    print(f"CSV output: {ALERTS_CSV_PATH}")
    print(f"Report output: {ALERTS_MD_PATH}")


if __name__ == "__main__":
    main()
