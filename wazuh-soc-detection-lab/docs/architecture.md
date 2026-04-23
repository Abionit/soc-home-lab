# Architecture

## Lab Goal

Build a compact SOC environment that demonstrates how endpoint and application events can be turned into detections, alerts, triage decisions, and reporting.

## Components

| Component | Purpose |
| --- | --- |
| Wazuh manager | Receives events, applies rules, and generates alerts |
| Wazuh indexer | Stores and indexes security events |
| Wazuh dashboard | Provides search, alert review, and dashboard access |
| Custom rules | Detect lab scenarios and map them to MITRE ATT&CK |
| Event generator | Creates safe synthetic events for validation |
| Analytics scripts | Convert alert data into metrics, reports, and SQLite tables |

## Data Flow

1. Synthetic security events are generated from `scripts/generate_lab_events.py`.
2. Events are sent to Wazuh through syslog or reviewed as local samples.
3. Custom Wazuh rules identify relevant detection scenarios.
4. Alerts are exported from Wazuh or represented through `output/sample_wazuh_alerts.jsonl`.
5. `scripts/build_alert_analytics.py` creates CSV, SQLite, and Markdown reporting outputs.
6. Analysts review dashboards, triage queue, detection summaries, and executive reporting.

## Detection Design

Each detection includes:

- rule ID
- severity
- log source
- MITRE ATT&CK mapping
- expected event pattern
- investigation notes
- tuning considerations

## Why This Architecture Works

The lab stays small enough to run locally but still demonstrates the core SOC workflow:

- collection
- detection
- enrichment
- triage
- reporting
- analytics
