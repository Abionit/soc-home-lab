# SOC Home Lab v2

Portfolio project that simulates a small SOC detection pipeline and a lightweight analytics layer.

This repository includes two full documentation versions:

- English: [README.en.md](README.en.md)
- Espanol: [README.es.md](README.es.md)

## v2 Highlights

- Reproducible event generation with enriched telemetry fields
- Three detection rules with ATT&CK-aligned context
- Enriched alert output with triage ownership, SLA status, and response timing
- SQLite analytics database plus reusable SQL queries
- Streamlit dashboard for operational metrics and portfolio screenshots

## Portfolio Quick Links

- English documentation: [README.en.md](README.en.md)
- Spanish documentation: [README.es.md](README.es.md)
- Version guide: [CHANGELOG.md](CHANGELOG.md)
- Evidence folder for screenshots: [evidence/v2/README.md](evidence/v2/README.md)
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

