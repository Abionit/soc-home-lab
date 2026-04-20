# SOC Home Lab v2

SOC project that simulates a compact detection pipeline with an analytics layer for triage, reporting, and operational visibility.

Documentation is available in two languages:

- English: [README.en.md](README.en.md)
- Espanol: [README.es.md](README.es.md)

## v2 Highlights

- Reproducible event generation with enriched telemetry fields
- Three detection rules with ATT&CK-aligned context
- Enriched alert output with triage ownership, SLA status, and response timing
- SQLite analytics database plus reusable SQL queries
- Streamlit dashboard for operational metrics and visual review

## Documentation And References

- English documentation: [README.en.md](README.en.md)
- Spanish documentation: [README.es.md](README.es.md)
- Version guide: [CHANGELOG.md](CHANGELOG.md)
- Evidence index: [evidence/v2/README.md](evidence/v2/README.md)
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

## Review Artifacts

Representative views for this release are indexed in [evidence/v2/README.md](evidence/v2/README.md):

1. `01_pipeline_success.png` - terminal execution
2. `02_dashboard_metrics.png` - KPI cards and secondary metrics
3. `03_dashboard_trend_severity.png` - trend and severity distribution
4. `04_dashboard_status_rules.png` - status and rule distribution
5. `05_dashboard_table.png` - enriched alerts table
6. `06_dashboard_sql_report.png` - SQL report preview
7. `07_alert_kpis_csv.png` - KPI export
8. `08_rule_summary_csv.png` - rule summary export
9. `09_sqlite_db_tables.png` - SQLite objects overview