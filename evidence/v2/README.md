## SOC Home Lab v2 - Screenshot Checklist



1. <img width="1259" height="585" alt="image" src="https://github.com/user-attachments/assets/bc8bb495-b595-46c2-9115-63b9a0508211" />

2. `02_dashboard_metrics.png`
3. `03_dashboard_trend_severity.png`
4. `04_dashboard_status_rules.png`
5. `05_dashboard_table.png`
6. `06_dashboard_sql_report.png`
7. `07_alert_kpis_csv.png`
8. `08_rule_summary_csv.png`

Recommended capture flow:

1. Run `python src/run_pipeline.py`
2. Run `python -m streamlit run src/dashboard.py`
3. Capture the dashboard sections in the order listed above
4. Save the files in this folder with the exact names

This keeps the evidence aligned with the `v2` portfolio release and makes review easier for recruiters.
