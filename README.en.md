# SOC Home Lab v2 - Detection, Analytics, and Triage Pipeline

Portfolio project that demonstrates practical SOC analyst skills with a reproducible detection pipeline, SQL reporting, and a lightweight operational dashboard.

## Problem Statement

Security teams do not work from raw logs alone. They need a repeatable way to:

1. ingest telemetry,
2. detect suspicious behavior,
3. enrich alerts with triage context,
4. measure operational performance,
5. communicate results in a format that can be reviewed quickly.

This project simulates that workflow end to end.

## Skills Demonstrated

- Python data processing and orchestration
- Detection engineering with rule-based logic
- SQL analytics with SQLite
- KPI reporting for backlog, SLA, and triage timing
- Dashboard design with Streamlit
- Technical documentation for portfolio and interview use

## Project Navigation

- Spanish version: [README.es.md](README.es.md)
- Version guide: [CHANGELOG.md](CHANGELOG.md)
- Evidence artifacts: [evidence/v2/README.md](evidence/v2/README.md)
- Detection logic: [src/detect_alerts.py](src/detect_alerts.py)
- SQL portfolio queries: [sql/portfolio_queries.sql](sql/portfolio_queries.sql)
- Sample report: [output/alerts_report.md](output/alerts_report.md)

## Architecture

1. Event generation: `src/generate_sample_logs.py`
2. Detection engine: `src/detect_alerts.py`
3. Analytics build step: `src/build_analytics.py`
4. Pipeline orchestration: `src/run_pipeline.py`
5. Dashboard: `src/dashboard.py`
6. Outputs:
   - `data/raw_events.jsonl`
   - `output/alerts.csv`
   - `output/alerts_report.md`
   - `output/alert_kpis.csv`
   - `output/alert_trend.csv`
   - `output/rule_summary.csv`
   - `analytics/soc_home_lab.db`
   - `sql/portfolio_queries.sql`

## Detection Rules (v2)

- `R001` (`high`) - burst of failed logins from the same IP to the same user within a 10-minute window
- `R002` (`critical`) - privilege change from a non-trusted geography
- `R003` (`high`) - password reset followed by a successful login from a non-trusted geography

Each alert is enriched with:

- ATT&CK-style tactic and technique context
- asset and log-source metadata
- triage owner
- alert status
- triage and resolution timing
- SLA breach flag

## Version Overview

- `v1` focused on a compact detection and dashboard demo with two rules and basic outputs.
- `v2` adds enriched telemetry, a third rule, a SQL analytics layer, KPI exports, improved dashboarding, and cleaner portfolio-ready documentation.

## Setup

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

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Pipeline

```bash
python src/run_pipeline.py
```

## Run the Dashboard

```bash
python -m streamlit run src/dashboard.py
```

## Run the Regression Test

```bash
python -m unittest discover -s tests
```

## Representative Outputs

- Alert table with severity, user, host, source IP, geography, status, and SLA fields
- KPI summary covering total alerts, critical alerts, active backlog, triage timing, and SLA flags
- Rule summary for detection coverage and alert distribution
- SQL queries for reusable security analytics reporting
- Markdown report for fast review without running the dashboard

## Why the SQL Layer Matters

Many entry-level analyst roles ask for more than alert review. They often expect candidates to work with operational metrics, reporting, and reusable queries. This project includes:

- a local SQLite analytics database
- exported KPI CSVs
- reusable SQL queries in `sql/portfolio_queries.sql`

That makes the repository stronger for both SOC-oriented and data-oriented interviews.

## Interview Talking Points

1. Why each rule matters operationally
2. Which alerts might be false positives and how to tune them
3. How triage timing and SLA metrics help show analyst workload
4. Why SQL reporting is useful even in a SOC context
