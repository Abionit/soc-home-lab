# SOC Home Lab v2

SOC analytics case study that converts simulated telemetry into enriched alerts, triage metrics, SQL reporting, and dashboard outputs.

Documentation is available in two languages:

- English: [README.en.md](README.en.md)
- Espanol: [README.es.md](README.es.md)

## Fast Review

If you want the quickest path through the project, start here:

- Evidence gallery: [evidence/v2/README.md](evidence/v2/README.md)
- Sample report: [output/alerts_report.md](output/alerts_report.md)
- SQL queries: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Detection logic: [src/detect_alerts.py](src/detect_alerts.py)

## Best Role Fit

- Operations Analyst
- Security Analytics / SOC
- Reporting Analyst in monitoring-heavy environments

## Questions Answered

- Which rules are generating the highest alert pressure?
- Where does backlog accumulate?
- How are severity and status distributed?
- Which users and hosts repeat most often?
- How long is triage and resolution taking across the queue?

## At A Glance

- Focus: alert enrichment, triage ownership, SLA-style metrics, and operational visibility
- Stack: Python, SQL, SQLite, Streamlit
- Main outputs: alerts report, KPI exports, rule summary, trend analysis, dashboard views
- Security context: ATT&CK-aligned detections with triage and reporting layers

## What This Project Demonstrates

- Reproducible event generation with enriched telemetry fields
- Three detection rules with ATT&CK-aligned context
- Enriched alert output with triage ownership, SLA status, and response timing
- SQLite analytics database plus reusable SQL queries
- Streamlit dashboard for operational metrics and visual review

## Documentation And References

- English documentation: [README.en.md](README.en.md)
- Spanish documentation: [README.es.md](README.es.md)
- Version guide: [CHANGELOG.md](CHANGELOG.md)
- Evidence gallery: [evidence/v2/README.md](evidence/v2/README.md)
- Detection logic: [src/detect_alerts.py](src/detect_alerts.py)
- SQL queries: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Sample report: [output/alerts_report.md](output/alerts_report.md)

## Quick Start

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
```

## Project Outputs

- `data/raw_events.jsonl`
- `output/alerts.csv`
- `output/alerts_report.md`
- `output/alert_kpis.csv`
- `output/alert_trend.csv`
- `output/rule_summary.csv`
- `analytics/soc_home_lab.db`
- `sql/portfolio_queries.sql`

## Evidence Gallery

Representative dashboard and reporting views are indexed in [evidence/v2/README.md](evidence/v2/README.md):

1. `01_pipeline_success.png` - terminal execution
2. `02_dashboard_metrics.png` - KPI cards and secondary metrics
3. `03_dashboard_trend_severity.png` - trend and severity distribution
4. `04_dashboard_status_rules.png` - status and rule distribution
5. `05_dashboard_table.png` - enriched alerts table
6. `06_dashboard_sql_report.png` - SQL report preview
7. `07_alert_kpis_csv.png` - KPI export
8. `08_rule_summary_csv.png` - rule summary export
9. `09_sqlite_db_tables.png` - SQLite objects overview
