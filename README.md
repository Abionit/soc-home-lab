# SOC Home Lab v2

Reproducible SOC detection and operational analytics pipeline.

## Operational Problem

Raw security telemetry does not provide enough context for prioritization. A SOC needs detections, enriched alerts, workload metrics, response-time indicators, and reusable reporting.

## Current Snapshot

- `332` events analyzed
- `5` alerts generated
- `2` critical alerts
- `3` SLA flags

## Pipeline

1. Generate simulated security telemetry.
2. Apply rule-based detections.
3. Enrich alerts with severity, ownership, asset, timing, and SLA context.
4. Export alert, KPI, trend, and rule-level datasets.
5. Materialize a SQLite analytical layer.
6. Review operations through Streamlit and SQL reports.

## Technical Stack

- Python
- SQL and SQLite
- Streamlit
- rule-based detection logic
- ATT&CK-style context
- automated regression testing

## Documentation

- English: [README.en.md](README.en.md)
- Espanol: [README.es.md](README.es.md)
- Evidence: [evidence/v2/README.md](evidence/v2/README.md)
- Detection logic: [src/detect_alerts.py](src/detect_alerts.py)
- SQL: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Report: [output/alerts_report.md](output/alerts_report.md)

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
python src/run_pipeline.py
python -m unittest discover -s tests
python -m streamlit run src/dashboard.py
```
