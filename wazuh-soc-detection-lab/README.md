# Wazuh SOC Detection Engineering Lab

Hands-on SOC project built around Wazuh SIEM/XDR, custom detection logic, MITRE ATT&CK mapping, alert triage, and security analytics reporting.

## At A Glance

- Platform: Wazuh SIEM/XDR using the official Docker deployment path
- Focus: detection engineering, alert enrichment, triage, reporting, and SOC metrics
- Data sources: synthetic security events, endpoint-style events, authentication activity, file integrity events, and web access patterns
- Analytics layer: Python, CSV, SQLite, Markdown reports, and an optional Streamlit dashboard
- Main outcome: a reviewable SOC lab that demonstrates both security operations and data analysis skills

## Why This Project Matters

Security teams do not only need alerts. They need detections that are mapped to real attack behaviors, triage context that helps prioritize work, and reporting that explains operational risk clearly.

This project demonstrates that workflow:

1. Deploy a Wazuh single-node lab.
2. Add custom detection rules for realistic SOC scenarios.
3. Generate controlled test events.
4. Review Wazuh alerts.
5. Export or simulate alert data.
6. Build SOC metrics and reports from alert evidence.

## Detection Coverage

| Scenario | Rule ID | Severity | MITRE ATT&CK |
| --- | --- | --- | --- |
| SSH brute force | 100100 | High | T1110 |
| RDP brute force | 100110 | High | T1110 |
| Suspicious encoded PowerShell | 100120 | Critical | T1059.001 |
| Local administrator account created | 100130 | High | T1136.001 |
| Sensitive file modified | 100140 | Medium | T1565.001 |
| Malware test artifact observed | 100150 | High | T1204 |
| Web path traversal attempt | 100160 | High | T1190 |
| Suspicious sudo escalation | 100170 | High | T1548 |
| Credential access tool indicator | 100180 | Critical | T1003 |

## Repository Layout

- [config/wazuh/rules/](config/wazuh/rules): custom Wazuh detection rules
- [config/wazuh/decoders/](config/wazuh/decoders): optional decoder references
- [config/agent/](config/agent): sample endpoint collection configuration
- [detections/](detections): detection catalog and validation notes
- [scripts/](scripts): setup, event generation, analytics, and dashboard scripts
- [output/](output): generated reports and representative alert analytics
- [evidence/](evidence): guidance for reviewable screenshots and validation artifacts
- [docs/](docs): architecture, runbook, and reporting documents

## Quick Start

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Generate representative lab events:

```bash
python scripts/generate_lab_events.py
```

Build analytics and reports:

```bash
python scripts/build_alert_analytics.py
```

Run the optional dashboard:

```bash
python -m streamlit run scripts/dashboard.py
```

## Wazuh Deployment

The lab is designed to run with the official Wazuh Docker single-node deployment. See [docs/runbook.md](docs/runbook.md) for setup steps.

The central Wazuh components are:

- Wazuh manager
- Wazuh indexer
- Wazuh dashboard

Official Wazuh Docker documentation: https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html

## Main Review Points

- Custom Wazuh rules use the documented custom-rule ID range.
- Detections are mapped to MITRE ATT&CK techniques.
- Test events are controlled and safe for a lab environment.
- Alert outputs are converted into SOC metrics and reporting.
- The project includes both technical and executive documentation.

## Current Outputs

- Executive report: [output/executive_report.md](output/executive_report.md)
- Alert metrics: [output/alert_metrics.csv](output/alert_metrics.csv)
- Triage queue: [output/triage_queue.csv](output/triage_queue.csv)
- Detection summary: [output/detection_summary.csv](output/detection_summary.csv)
- SQLite database: `output/wazuh_soc_lab.db`, generated locally

## Scope And Safety

This project is built for local lab use, controlled test events, and portfolio review. It does not include destructive actions, credential theft, exploitation against third-party systems, or offensive activity outside the lab.
