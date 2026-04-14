# SOC Home Lab

This repository includes two full documentation versions:

- English: README.en.md
- Espanol: README.es.md

## Quick Start

```bash
cd security-projects/soc-home-lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py
streamlit run src/dashboard.py
```

## What to Screenshot for Portfolio

Take screenshots in this exact order and save them in the `evidence/` folder:

1. `01_pipeline_ success.png` - terminal with successful pipeline run.
2. `02_dashboard_metrics.png` - top dashboard metrics cards.
3. `03_dashboard_severity.png` - severity distribution chart.
4. `04_dashboard_rules.png` - rule distribution chart.
5. `05_dashboard_table.png` - alerts table with at least one critical alert.
6. `06_dashboard_report_preview.png` - report preview section.

Optional extras:
- `07_alerts_csv_preview.png`
- `08_alerts_report_md.png`

If you want the cleanest portfolio version, capture the screens in that order and place the images in [evidence/README.md](evidence/README.md).
