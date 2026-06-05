# SOC Home Lab v2 - Detection, Analytics, and Triage Pipeline

Reproducible security operations workflow for detection, alert enrichment, SQL reporting, and operational monitoring.

## Problem

Security teams need more than raw logs. They need a repeatable process to ingest telemetry, detect suspicious behavior, add triage context, measure workload, and communicate operational status.

## Architecture

1. Event generation: `src/generate_sample_logs.py`
2. Detection engine: `src/detect_alerts.py`
3. Analytical build: `src/build_analytics.py`
4. Orchestration: `src/run_pipeline.py`
5. Operations dashboard: `src/dashboard.py`
6. SQLite and CSV reporting outputs

## Detection Rules

- `R001` high: failed-login burst from the same IP to the same user
- `R002` critical: privilege change from a non-trusted geography
- `R003` high: password reset followed by a successful login from a non-trusted geography

Each alert contains ATT&CK-style context, asset and log-source metadata, ownership, status, triage time, resolution time, and an SLA flag.

## Operational Outputs

- enriched alert queue
- alert and severity KPIs
- active backlog metrics
- triage and resolution timing
- rule-performance summary
- reusable SQL queries
- Streamlit operations dashboard

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
python src/run_pipeline.py
python -m unittest discover -s tests
python -m streamlit run src/dashboard.py
```

## References

- Spanish: [README.es.md](README.es.md)
- Evidence: [evidence/v2/README.md](evidence/v2/README.md)
- Detection logic: [src/detect_alerts.py](src/detect_alerts.py)
- SQL: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Report: [output/alerts_report.md](output/alerts_report.md)
