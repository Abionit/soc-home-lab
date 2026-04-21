# SOC Home Lab - Version Guide

## v2

Current portfolio release.

Main improvements:

- richer simulated telemetry with department, role, asset, and source context
- three detection rules instead of two
- ATT&CK-style tactic and technique labels
- alert enrichment with status, assignment, triage timing, resolution timing, and SLA tracking
- SQLite analytics layer
- reusable SQL portfolio queries
- improved Streamlit dashboard
- regression test for the failed-login burst rule
- dedicated `evidence/v2/` folder for dashboard, reporting, and project evidence artifacts

## v1

Initial public portfolio version.

Characteristics:

- compact event generation
- two core detection rules
- CSV and Markdown outputs
- basic Streamlit dashboard
- lightweight repo structure for quick review

## Why this matters

`v1` was useful as a compact detection demo.

`v2` is designed to be easier to defend in interviews because it shows a broader set of skills that often appear in SOC, security analyst, and security analytics roles:

- detection logic
- analyst workflow
- reporting
- SQL
- KPI thinking
- documentation
- presentation
