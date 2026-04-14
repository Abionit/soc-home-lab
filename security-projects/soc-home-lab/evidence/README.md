# Evidence Pack Order

Take screenshots in this exact order and save them with these filenames:

1. 01_pipeline_success.png
- Terminal showing `python src/run_pipeline.py` finished successfully.

2. 02_dashboard_metrics.png
- Dashboard top section with total alerts, unique users, and unique source IPs.

3. 03_dashboard_severity.png
- Severity distribution chart.

4. 04_dashboard_rules.png
- Rule distribution chart.

5. 05_dashboard_table.png
- Alerts table with at least one `high` and one `critical` alert.

6. 06_dashboard_report_preview.png
- Report preview section.

Optional:
- 07_alerts_csv_preview.png
- 08_alerts_report_md.png

How to use:
- Run `python src/run_pipeline.py`
- Run `streamlit run src/dashboard.py`
- Capture the screens above in this order
- Place the images in this folder before pushing to GitHub
