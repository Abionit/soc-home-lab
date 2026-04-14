# SOC Home Lab - Detection and Triage Pipeline

Portfolio project to demonstrate junior SOC skills with a practical detection workflow.

## Problem Statement

SOC teams need fast triage signals, not just raw logs. This lab builds a mini pipeline that:

1. generates security events,
2. applies detection rules,
3. prioritizes alerts,
4. produces evidence for investigation.

## Architecture

1. Event generation: src/generate_sample_logs.py
2. Detection engine: src/detect_alerts.py
3. Orchestration: src/run_pipeline.py
4. Dashboard: src/dashboard.py
5. Outputs:
   - data/raw_events.jsonl
   - output/alerts.csv
   - output/alerts_report.md

## Detection Rules (v1)

- R001 (high): burst of failed logins for same user + source IP.
- R002 (critical): privilege change from non-trusted geography.

## Setup

```bash
cd security-projects/soc-home-lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Pipeline

```bash
python src/run_pipeline.py
```

## Run Visual Dashboard

```bash
streamlit run src/dashboard.py
```

## Screenshots to Include in Portfolio

Take screenshots in this exact order and save them in the `evidence/` folder:

1. `01_pipeline_success.png` - terminal showing a successful pipeline run.
2. `02_dashboard_metrics.png` - top dashboard metrics cards.
3. `03_dashboard_severity.png` - severity distribution chart.
4. `04_dashboard_rules.png` - rule distribution chart.
5. `05_dashboard_table.png` - alerts table including at least one critical alert.
6. `06_dashboard_report_preview.png` - report preview section.

Optional extras:
- `07_alerts_csv_preview.png`
- `08_alerts_report_md.png`

## Interview Talking Points

1. Explain why each rule indicates suspicious behavior.
2. Explain potential false positives.
3. Explain what data you would add in v2.

## v2 Improvements

1. MITRE ATT&CK mapping per rule.
2. Whitelisting and adaptive thresholds.
3. Better enrichment for source IP context.
4. Trend dashboard with triage SLA.
