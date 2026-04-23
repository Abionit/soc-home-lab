from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

SCENARIOS = [
    {"rule_id": 100100, "level": 10, "detection": "ssh_bruteforce", "description": "SSH brute force pattern detected", "technique": "T1110", "severity": "high", "user": "ubuntu", "srcip": "203.0.113.20", "host": "linux-web-01", "outcome": "blocked"},
    {"rule_id": 100110, "level": 10, "detection": "rdp_bruteforce", "description": "RDP brute force pattern detected", "technique": "T1110", "severity": "high", "user": "maria", "srcip": "198.51.100.44", "host": "win-dc-01", "outcome": "investigate"},
    {"rule_id": 100120, "level": 12, "detection": "suspicious_powershell_encoded", "description": "Suspicious encoded PowerShell command observed", "technique": "T1059.001", "severity": "critical", "user": "svc-backup", "srcip": "10.10.20.14", "host": "win-app-02", "outcome": "contain"},
    {"rule_id": 100130, "level": 10, "detection": "local_admin_created", "description": "Local administrator account creation observed", "technique": "T1136.001", "severity": "high", "user": "helpdesk01", "srcip": "10.10.10.8", "host": "win-fin-03", "outcome": "validate"},
    {"rule_id": 100140, "level": 7, "detection": "sensitive_file_modified", "description": "Sensitive file modification observed", "technique": "T1565.001", "severity": "medium", "user": "root", "srcip": "10.10.30.5", "host": "linux-db-01", "outcome": "review"},
    {"rule_id": 100150, "level": 10, "detection": "malware_test_artifact", "description": "Malware test artifact observed", "technique": "T1204", "severity": "high", "user": "analyst", "srcip": "10.10.40.22", "host": "win-lab-01", "outcome": "lab_test"},
    {"rule_id": 100160, "level": 10, "detection": "web_path_traversal", "description": "Web path traversal attempt observed", "technique": "T1190", "severity": "high", "user": "-", "srcip": "192.0.2.77", "host": "nginx-edge-01", "outcome": "blocked"},
    {"rule_id": 100170, "level": 10, "detection": "suspicious_sudo_escalation", "description": "Suspicious sudo escalation observed", "technique": "T1548", "severity": "high", "user": "deploy", "srcip": "10.10.50.9", "host": "linux-ci-01", "outcome": "investigate"},
    {"rule_id": 100180, "level": 12, "detection": "credential_access_indicator", "description": "Credential access tool indicator observed", "technique": "T1003", "severity": "critical", "user": "admin", "srcip": "10.10.60.12", "host": "win-admin-01", "outcome": "contain"},
]

def build_events() -> list[dict]:
    base_time = datetime(2026, 4, 22, 14, 0, tzinfo=timezone.utc)
    events = []
    for index, scenario in enumerate(SCENARIOS):
        detected_at = base_time + timedelta(minutes=index * 7)
        triage_minutes = 8 + index * 3
        resolution_minutes = 45 + index * 15 if scenario["severity"] != "critical" else 120 + index * 20
        events.append({
            "timestamp": detected_at.isoformat(),
            "rule": {"id": str(scenario["rule_id"]), "level": scenario["level"], "description": f"SOC Lab: {scenario['description']}", "mitre": {"id": [scenario["technique"]]}},
            "agent": {"name": scenario["host"]},
            "data": {"soclab_detection": scenario["detection"], "user": scenario["user"], "srcip": scenario["srcip"], "outcome": scenario["outcome"], "triage_minutes": triage_minutes, "resolution_minutes": resolution_minutes, "status": "investigating" if scenario["outcome"] in {"investigate", "contain"} else "closed", "severity": scenario["severity"]},
        })
    return events

def main() -> None:
    events = build_events()
    log_lines = []
    for event in events:
        data = event["data"]
        log_lines.append(f"soclab_detection={data['soclab_detection']} user={data['user']} srcip={data['srcip']} host={event['agent']['name']} outcome={data['outcome']}")
    (OUTPUT / "generated_lab_events.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    with (OUTPUT / "sample_wazuh_alerts.jsonl").open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")
    print(f"Generated {len(events)} lab events.")

if __name__ == "__main__":
    main()
