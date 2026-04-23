# SOC Home Lab v2

SOC analytics project that simulates a compact detection pipeline with an analytics layer for triage, reporting, and operational visibility.

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

Representative dashboard and reporting views are indexed in [evidence/v2/README.md](evidence/v2/README.md). They show KPI cards, trend analysis, severity distribution, rule distribution, enriched alert fields, and report previews.
