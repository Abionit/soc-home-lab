# SOC Home Lab

[Leer en espanol](README.es.md)

This repository is part of my public portfolio. I built it to practice a small SOC workflow end to end: generate events, detect suspicious behavior, and turn that into outputs that are easier to review during triage.

It is intentionally compact. I wanted a project that someone can understand in a few minutes and still use as a strong interview conversation piece.

## What this project does

1. Generates sample security events
2. Applies two detection rules
3. Writes alerts to CSV and Markdown
4. Shows the results in a simple Streamlit dashboard

## Files worth opening first

- `src/detect_alerts.py` for the detection logic
- `output/alerts_report.md` for the report generated from the sample run
- `src/dashboard.py` for the visual review layer
- `data/raw_events.jsonl` for the sample telemetry used by the pipeline

## Current detection rules

- `R001` `high`: repeated failed logins from the same user and source IP inside a 10 minute window
- `R002` `critical`: privilege change coming from a non-trusted geography

## Repo layout

```text
soc-home-lab/
|-- data/
|   `-- raw_events.jsonl
|-- evidence/
|   `-- README.md
|-- output/
|   |-- alerts.csv
|   `-- alerts_report.md
|-- src/
|   |-- dashboard.py
|   |-- detect_alerts.py
|   |-- generate_sample_logs.py
|   `-- run_pipeline.py
|-- requirements.txt
|-- README.md
`-- README.es.md
```

## Run it locally

### macOS or Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py
streamlit run src/dashboard.py
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_pipeline.py
streamlit run src/dashboard.py
```

## Why I keep this project public

This repo shows how I think about detection and triage in a simple but reviewable format. Instead of only listing tools, it shows a small workflow with data generation, alert logic, analyst outputs, and a basic dashboard.

## Next improvements

- add MITRE ATT&CK mapping for each rule
- add allowlists and adaptive thresholds
- enrich alerts with better source context
- add more detections such as impossible travel and password spray
