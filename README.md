# SOC Home Lab v2

Portfolio project that simulates a small SOC detection pipeline and a lightweight analytics layer.

## At A Glance

- Business question: how can simulated telemetry be converted into enriched alerts, operational metrics, and analyst-ready reporting?
- Stack: Python, SQL, SQLite, Streamlit
- Main outputs: enriched alerts, alert KPIs, trend metrics, rule summaries, SQL report, and Streamlit dashboard
- Current snapshot: `332` events analyzed | `5` alerts generated | `2` critical alerts | `3` SLA flags

## Documentation

- English: [README.en.md](README.en.md)
- Espanol: [README.es.md](README.es.md)
- Version guide: [CHANGELOG.md](CHANGELOG.md)
- Evidence artifacts: [evidence/v2/README.md](evidence/v2/README.md)

## What This Project Demonstrates

- Reproducible event generation with enriched telemetry fields
- Rule-based detection logic with ATT&CK-style context
- Alert enrichment with triage ownership, SLA status, and response timing
- SQLite analytics database plus reusable SQL queries
- KPI reporting for backlog, severity, triage timing, and rule performance
- Streamlit dashboard for operational review

## Workflow

1. Generate simulated security telemetry.
2. Apply detection rules to identify suspicious behavior.
3. Enrich alerts with severity, ownership, asset, timing, and SLA context.
4. Export alert tables, KPI summaries, trend outputs, and rule summaries.
5. Materialize a SQLite analytics layer for reusable SQL analysis.
6. Review the workflow through a Streamlit dashboard and Markdown report.

## Repository Layout

- [src/](src): pipeline, detection logic, analytics build, and dashboard code
- [sql/](sql): reusable SQL portfolio queries
- [output/](output): representative reports and analytical outputs
- [analytics/](analytics): generated SQLite analytics database
- [evidence/v2/](evidence/v2): project evidence artifacts
- [tests/](tests): regression test for the failed-login burst rule

## Representative Outputs

- Alerts table: [output/alerts.csv](output/alerts.csv)
- Alert report: [output/alerts_report.md](output/alerts_report.md)
- KPI summary: [output/alert_kpis.csv](output/alert_kpis.csv)
- Alert trend: [output/alert_trend.csv](output/alert_trend.csv)
- Rule summary: [output/rule_summary.csv](output/rule_summary.csv)
- SQL queries: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)

## Run Locally

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and run the project:

```bash
pip install -r requirements.txt
python src/run_pipeline.py
python -m streamlit run src/dashboard.py
python -m unittest discover -s tests
```
