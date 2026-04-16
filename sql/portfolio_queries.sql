-- Query 1: Executive KPI snapshot for the dashboard.
SELECT
    COUNT(*) AS total_alerts,
    SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_alerts,
    SUM(CASE WHEN status IN ('open', 'investigating') THEN 1 ELSE 0 END) AS active_alerts,
    ROUND(AVG(triage_minutes), 1) AS avg_triage_minutes,
    ROUND(AVG(resolution_minutes), 1) AS avg_resolution_minutes,
    SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
FROM alerts;

-- Query 2: Alert trend by hour.
SELECT
    strftime('%Y-%m-%d %H:00:00', detected_at) AS alert_hour,
    COUNT(*) AS alert_count,
    SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_alerts
FROM alerts
GROUP BY strftime('%Y-%m-%d %H:00:00', detected_at)
ORDER BY alert_hour;

-- Query 3: Rule-level performance and workload.
SELECT
    rule_id,
    severity,
    COUNT(*) AS alert_count,
    ROUND(AVG(triage_minutes), 1) AS avg_triage_minutes,
    SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
FROM alerts
GROUP BY rule_id, severity
ORDER BY alert_count DESC;

-- Query 4: Noisiest entities to investigate first.
SELECT
    hostname,
    user,
    department,
    COUNT(*) AS alert_count,
    MAX(severity) AS max_severity
FROM alerts
GROUP BY hostname, user, department
ORDER BY alert_count DESC, hostname, user;

-- Query 5: Active backlog by severity.
SELECT
    severity,
    status,
    COUNT(*) AS alert_count
FROM alerts
WHERE status IN ('open', 'investigating')
GROUP BY severity, status
ORDER BY severity, status;
