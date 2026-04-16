DROP VIEW IF EXISTS alert_daily_metrics;
CREATE VIEW alert_daily_metrics AS
SELECT
    date(detected_at) AS alert_date,
    severity,
    status,
    COUNT(*) AS alert_count,
    SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
FROM alerts
GROUP BY date(detected_at), severity, status;

DROP VIEW IF EXISTS rule_performance;
CREATE VIEW rule_performance AS
SELECT
    rule_id,
    severity,
    COUNT(*) AS alert_count,
    ROUND(AVG(triage_minutes), 1) AS avg_triage_minutes,
    ROUND(AVG(resolution_minutes), 1) AS avg_resolution_minutes,
    SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
FROM alerts
GROUP BY rule_id, severity;

DROP VIEW IF EXISTS entity_hotspots;
CREATE VIEW entity_hotspots AS
SELECT
    hostname,
    user,
    department,
    COUNT(*) AS alert_count,
    MAX(severity) AS max_severity
FROM alerts
GROUP BY hostname, user, department;
